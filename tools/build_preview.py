# Build images/icons-preview.svg (all icons, light and dark panel) from ../icons.
# Render to images/icons-preview.png for the README (the Marketplace rejects SVG images).
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ITEMS = [
    ('vi', '.vi', 'VI'), ('vi-class', '.vi', 'class member VI'), ('vim', '.vim', 'malleable VI'),
    ('vit', '.vit', 'VI template'), ('ctl', '.ctl', 'control'), ('ctt', '.ctt', 'control template'),
    ('xctl', '.xctl', 'XControl'), ('lvclass', '.lvclass', 'class'), ('lvlib', '.lvlib', 'library'),
    ('lvlibp', '.lvlibp', 'packed library'), ('llb', '.llb', 'VI library'), ('lvproj', '.lvproj', 'project'),
    ('lvlps', '.lvlps', 'project settings'), ('aliases', '.aliases', 'aliases'), ('lvsc', '.lvsc', 'statechart'),
    ('xnode', '.xnode', 'XNode'), ('rtm', '.rtm', 'run-time menu'), ('lvbitx', '.lvbitx', 'FPGA bitfile'),
    ('tdms', '.tdms', 'TDMS data'), ('lvm', '.lvm', 'measurement'),
]
COLS, CW, CH, ICON, PAD = 4, 190, 48, 32, 20
ROWS = -(-len(ITEMS) // COLS)
PW, PH = COLS * CW + 2 * PAD, ROWS * CH + 2 * PAD
THEMES = [('#FFFFFF', '#1F2328', '#59636E'), ('#1E1E1E', '#E6EDF3', '#9198A1')]


def inner(name):
    s = (ROOT / 'icons' / f'{name}.svg').read_text()
    return re.search(r'<svg[^>]*>(.*)</svg>', s, re.S).group(1)


parts = []
for t, (bg, fg, sub) in enumerate(THEMES):
    oy = t * PH
    parts.append(f'<rect x="0" y="{oy}" width="{PW}" height="{PH}" fill="{bg}"/>')
    for i, (name, ext, label) in enumerate(ITEMS):
        x = PAD + (i % COLS) * CW
        y = oy + PAD + (i // COLS) * CH
        s = ICON / 16
        parts.append(f'<g transform="translate({x} {y + (CH - ICON) / 2}) scale({s})">{inner(name)}</g>')
        tx = x + ICON + 10
        parts.append(f'<text x="{tx}" y="{y + 21}" fill="{fg}" font-size="14" font-weight="600">{ext}</text>')
        parts.append(f'<text x="{tx}" y="{y + 38}" fill="{sub}" font-size="12">{label}</text>')

svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {PW} {2 * PH}" width="{PW}" height="{2 * PH}" '
       'font-family="Segoe UI, Helvetica, Arial, sans-serif">' + ''.join(parts) + '</svg>\n')
(ROOT / 'images' / 'icons-preview.svg').write_text(svg, newline='\n')
print(f'images/icons-preview.svg {PW}x{2 * PH}')
