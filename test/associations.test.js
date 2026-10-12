'use strict';
const test = require('node:test');
const assert = require('node:assert/strict');
const path = require('path');
const { LANG, decode, members, computePatterns, mergeAssociations, sameAssociations } = require('../src/associations');

const root = path.resolve('/ws');
const cls = path.join(root, 'Subsystem.ICRH', 'Subsystem.ICRH.lvclass');
const xml = `<?xml version='1.0' encoding='UTF-8'?>
<LVClass LVVersion="23008000">
  <Item Name="Subsystem.ICRH.ctl" Type="Class Private Data" URL="Subsystem.ICRH.ctl"/>
  <Item Name="Support" Type="Folder">
    <Item Name="Calc.vi" Type="VI" URL="../Support/Calc.vi"/>
    <Item Name="Enum.ctl" Type="VI" URL="../Support/Enum.ctl"/>
  </Item>
  <Item Name="Populate [Test].vi" Type="VI" URL="../Test/Populate [Test].vi"/>
  <Item Name="Arm &amp; Fire.vi" Type="VI" URL="../Arm &amp; Fire.vi"/>
</LVClass>`;
const p = (...s) => path.join(root, 'Subsystem.ICRH', ...s);

test('decode XML entities', () => {
  assert.equal(decode('A &amp; B &quot;c&quot; &#65;'), 'A & B "c" A');
});

test('members resolves URLs relative to the .lvclass file', () => {
  assert.deepEqual(members(cls, xml), [p('Support', 'Calc.vi'), p('Test', 'Populate [Test].vi'), p('Arm & Fire.vi')]);
});

test('one directory glob when all VIs below the class are members', async () => {
  const listVIs = async () => members(cls, xml);
  const pats = await computePatterns(root, [{ path: cls, xml }], listVIs);
  assert.deepEqual([...pats], ['**/Subsystem.ICRH/**/*.vi']);
});

test('per-file entries when the class dir holds other VIs; glob chars escaped', async () => {
  const listVIs = async () => [...members(cls, xml), p('Scratch.vi')];
  const pats = await computePatterns(root, [{ path: cls, xml }], listVIs);
  assert.deepEqual([...pats].sort(), [
    '**/Subsystem.ICRH/Arm & Fire.vi',
    '**/Subsystem.ICRH/Support/Calc.vi',
    '**/Subsystem.ICRH/Test/Populate ?Test?.vi',
  ]);
});

test('merge keeps user entries and replaces managed ones', () => {
  const cur = { '*.foo': 'xml', '**/stale.vi': LANG };
  const next = mergeAssociations(cur, new Set(['**/a.vi']));
  assert.deepEqual(next, { '*.foo': 'xml', '**/a.vi': LANG });
  assert.ok(sameAssociations(next, { '**/a.vi': LANG, '*.foo': 'xml' }));
  assert.ok(!sameAssociations(cur, next));
});
