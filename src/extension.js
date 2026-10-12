'use strict';
// Class-member VI icons: map VIs owned by a .lvclass to the
// "labview-vi-class" language through files.associations.
const vscode = require('vscode');
const { LANG, computePatterns, mergeAssociations, sameAssociations } = require('./associations');

const CFG = 'labviewIcons';
let timer;
let log = { appendLine() {} };

async function patternsFor(folder) {
  const uris = await vscode.workspace.findFiles(new vscode.RelativePattern(folder, '**/*.lvclass'));
  const classes = [];
  for (const uri of uris) {
    try {
      classes.push({ path: uri.fsPath, xml: Buffer.from(await vscode.workspace.fs.readFile(uri)).toString('utf8') });
    } catch { /* unreadable class: skip */ }
  }
  const listVIs = async dir =>
    (await vscode.workspace.findFiles(new vscode.RelativePattern(dir, '**/*.vi'))).map(u => u.fsPath);
  return computePatterns(folder.uri.fsPath, classes, listVIs);
}

// files.associations is window-scoped: write to workspace settings
// (.vscode/settings.json, or the .code-workspace file for multi-root).
async function apply(pats) {
  const cfg = vscode.workspace.getConfiguration('files');
  const cur = cfg.inspect('associations').workspaceValue || {};
  const next = mergeAssociations(cur, pats);
  if (!sameAssociations(cur, next)) {
    await cfg.update('associations', Object.keys(next).length ? next : undefined, vscode.ConfigurationTarget.Workspace);
  }
}

async function refresh(off) {
  if (!vscode.workspace.workspaceFolders || !vscode.workspace.isTrusted) return;
  const pats = new Set();
  if (off !== true && vscode.workspace.getConfiguration(CFG).get('classMemberIcons', true)) {
    for (const folder of vscode.workspace.workspaceFolders) {
      if (folder.uri.scheme !== 'file') continue;
      try { (await patternsFor(folder)).forEach(p => pats.add(p)); }
      catch (e) { log.appendLine(`${folder.name}: ${(e && e.stack) || e}`); }
    }
  }
  try {
    await apply(pats);
    log.appendLine(`${pats.size} class-member pattern(s) (${LANG})`);
  } catch (e) { log.appendLine(`write failed: ${(e && e.message) || e}`); }
}

const schedule = () => { clearTimeout(timer); timer = setTimeout(() => refresh(), 1000); };

function activate(ctx) {
  log = vscode.window.createOutputChannel('LabVIEW Icons');
  const w1 = vscode.workspace.createFileSystemWatcher('**/*.lvclass');
  const w2 = vscode.workspace.createFileSystemWatcher('**/*.vi', false, true, false);
  ctx.subscriptions.push(log, w1, w2,
    w1.onDidCreate(schedule), w1.onDidChange(schedule), w1.onDidDelete(schedule),
    w2.onDidCreate(schedule), w2.onDidDelete(schedule),
    vscode.workspace.onDidChangeWorkspaceFolders(schedule),
    vscode.workspace.onDidGrantWorkspaceTrust(schedule),
    vscode.workspace.onDidChangeConfiguration(e => { if (e.affectsConfiguration(`${CFG}.classMemberIcons`)) schedule(); }),
    vscode.commands.registerCommand('labviewIcons.refresh', () => refresh()),
    vscode.commands.registerCommand('labviewIcons.clear', () => refresh(true)),
  );
  refresh();
}

function deactivate() { clearTimeout(timer); }

module.exports = { activate, deactivate };
