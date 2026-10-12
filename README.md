# File Icons for LabVIEW

File icons for LabVIEW files in the VS Code explorer, tabs and breadcrumbs.

## Features

- Icons for LabVIEW file types. The icons keep the LabVIEW cues: folded page, yellow connector triangle and the native glyph colours.
- A class-member VI icon for VIs owned by a `.lvclass`.
- XML highlighting for XML-based LabVIEW files. INI highlighting for `.aliases` and `.lvlps`.

| Files | Icon |
|---|---|
| `.vi` | front panel |
| `.vi` owned by a `.lvclass` | class cube |
| `.vim` | coloured blocks |
| `.vit` `.ctt` | VI / control, dashed template border |
| `.ctl` `.xctl` | slider |
| `.lvclass` | cube |
| `.lvlib` `.lvlibp` `.llb` | library, packed library, VI library |
| `.lvproj` `.lvlps` `.aliases` | project, project settings, aliases |
| `.lvsc` `.xnode` `.rtm` `.mnu` `.lvbitx` | statechart, XNode, run-time menu, FPGA bitfile |
| `.tdms` `.tdms_index` `.lvm` | measurement data |

## Requirements

- An icon theme that shows language icons. Seti, the default theme, does. If your icon theme has its own icon for a file extension, that icon wins.

## Class-member VIs

The extension reads every `.lvclass` file in the workspace and finds the member VIs. It writes these VIs to `files.associations` in the workspace settings (`.vscode/settings.json`, or the `.code-workspace` file for multi-root) with the value `labview-vi-class`.

- When all VIs below a class folder are class members, the extension writes one glob for that folder. Otherwise it writes one entry for each VI.
- Entries with other values are not changed.
- The entries refresh when `.lvclass` or `.vi` files change.
- This feature needs a trusted workspace. File icons also work in Restricted Mode.

## Extension Settings

- `labviewIcons.classMemberIcons` (default `true`): show the class-member icon. Set `false` to remove the managed entries.

## Commands

- `LabVIEW Icons: Refresh Class Member Icons`
- `LabVIEW Icons: Remove Class Member Associations`

## Development

```sh
npm ci
npm run lint
npm test
npm run package   # writes dist/labview-file-icons-<version>.vsix
```

Press F5 to start an Extension Development Host.

To change an icon, edit `tools/build_icons.py` and run `npm run icons`. `images/icon.png` is rendered from `images/icon.svg`.

## Release

1. Update `version` in `package.json` and `CHANGELOG.md`.
2. Commit, then tag `v<version>` and push the tag.
3. CI builds the `.vsix` and attaches it to a GitHub Release. If the `VSCE_PAT` secret is set, CI also publishes to the Marketplace.

## Trademarks

LabVIEW is a trademark of NI (Emerson). This extension is not affiliated with or endorsed by NI.
