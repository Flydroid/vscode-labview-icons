'use strict';
// Pure logic (no vscode API): find class-member VIs and build
// files.associations patterns. Unit-tested in test/associations.test.js.
const path = require('path');

const LANG = 'labview-vi-class';
const ITEM_RE = /<Item\b[^>]*>/g;
const ATTR_RE = /(\w+)="([^"]*)"/g;
const GLOB_SPECIAL = /[[\]{}*?]/g;

function decode(s) {
  return s.replace(/&quot;/g, '"').replace(/&apos;/g, "'").replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>').replace(/&#(\d+);/g, (_, n) => String.fromCharCode(+n)).replace(/&amp;/g, '&');
}

// LabVIEW URLs are relative to the owning file itself ("../X.vi" = sibling).
function resolveUrl(ownerFsPath, url) {
  const u = decode(url);
  const drive = /^\/([A-Za-z])\/(.*)$/.exec(u); // "/C/dir/x.vi" -> "C:/dir/x.vi"
  if (drive && process.platform === 'win32') return path.normalize(`${drive[1]}:/${drive[2]}`);
  if (u.startsWith('/')) return path.normalize(u);
  return path.resolve(ownerFsPath, u);
}

// Absolute paths of the .vi members listed in a .lvclass XML document.
function members(ownerFsPath, xml) {
  const out = [];
  for (const tag of xml.match(ITEM_RE) || []) {
    const a = {};
    for (const m of tag.matchAll(ATTR_RE)) a[m[1]] = m[2];
    if (a.URL && /\.vi$/i.test(decode(a.URL))) out.push(resolveUrl(ownerFsPath, a.URL));
  }
  return out;
}

const key = p => (process.platform === 'win32' ? p.toLowerCase() : p);
const rel = (root, p) => path.relative(root, p).split(path.sep).join('/');
const inside = (dir, p) => {
  const r = path.relative(dir, p);
  return Boolean(r) && !r.startsWith('..') && !path.isAbsolute(r);
};
const glob = r => '**/' + r.replace(GLOB_SPECIAL, '?');

/**
 * Build association patterns for one workspace folder.
 * @param {string} root workspace folder path
 * @param {{path: string, xml: string}[]} classes .lvclass files and their content
 * @param {(dir: string) => Promise<string[]>} listVIs all .vi paths below dir
 * @returns {Promise<Set<string>>}
 */
async function computePatterns(root, classes, listVIs) {
  const all = new Set();
  const perClass = classes.map(c => {
    const m = members(c.path, c.xml);
    m.forEach(p => all.add(key(p)));
    return { dir: path.dirname(c.path), m };
  });
  const pats = new Set();
  for (const { dir, m } of perClass) {
    // One directory glob when every VI below the class dir is a class member.
    let dirGlob = false;
    if (m.filter(p => inside(dir, p)).length > 1 && path.resolve(dir) !== path.resolve(root)) {
      const vis = await listVIs(dir);
      dirGlob = vis.length > 0 && vis.every(v => all.has(key(v)));
    }
    if (dirGlob) pats.add(glob(rel(root, dir)) + '/**/*.vi');
    for (const p of m) {
      if (dirGlob && inside(dir, p)) continue;
      if (inside(root, p)) pats.add(glob(rel(root, p)));
    }
  }
  return pats;
}

// Replace managed entries (value LANG) in an associations object; keep the rest.
function mergeAssociations(current, pats) {
  const next = {};
  for (const [k, v] of Object.entries(current || {})) if (v !== LANG) next[k] = v;
  for (const p of [...pats].sort()) if (!(p in next)) next[p] = LANG;
  return next;
}

function sameAssociations(a, b) {
  const s = o => JSON.stringify(Object.entries(o || {}).sort());
  return s(a) === s(b);
}

module.exports = { LANG, decode, resolveUrl, members, computePatterns, mergeAssociations, sameAssociations };
