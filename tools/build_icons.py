# Build the icon set (flat SVG, 16x16 grid) into ../icons.
# LabVIEW cues: folded page, yellow connector triangle, native glyph colours.
from pathlib import Path
O = Path(__file__).resolve().parent.parent / 'icons'
def svg(b): return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">{b}</svg>'
def page(fill='#FFFFFF', stroke='#5B6B8C', dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="M2 1h7l3.5 3.5V15H2z" fill="{fill}" stroke="{stroke}" stroke-linejoin="round"{d}/>'
            f'<path d="M9 1v3.5h3.5" fill="none" stroke="{stroke}" stroke-linejoin="round"/>')
TPL = dict(stroke='#D08A00', dash='2 1')
CONN = '<path d="M9.5 9.25l6 3.25-6 3.25z" fill="#FFD21F" stroke="#6B5600" stroke-width=".9" stroke-linejoin="round"/>'
SCREEN = ('<rect x="3.5" y="3" width="6" height="5" rx=".6" fill="#13301A"/>'
          '<path d="M4.3 6.2l1-1.6 1.1 2 1.1-2.2 1 1.4" fill="none" stroke="#3BE36B" stroke-width=".9" stroke-linecap="round" stroke-linejoin="round"/>')
SLIDER = lambda c: ('<path d="M4 4h1M4 7h1M4 10h1M4 13h1" stroke="#6E7B8B" stroke-width=".9"/>'
                    '<rect x="6" y="3" width="1.8" height="11" rx=".5" fill="#3A3F47"/>'
                    f'<path d="M7.3 8.5l3.2-2v4z" fill="{c}" stroke="#1F3A1F" stroke-width=".6" stroke-linejoin="round"/>')
def cube(x=8, y=8, s=1.0):
    t = f'transform="translate({x} {y}) scale({s}) translate(-8 -8)"'
    return (f'<g {t} stroke="#0D2A78" stroke-width=".9" stroke-linejoin="round">'
            '<path d="M8 1.5l5.5 2.9L8 7.3 2.5 4.4z" fill="#8DB4FF"/><path d="M2.5 4.4L8 7.3v7.2l-5.5-2.9z" fill="#2F66E0"/>'
            '<path d="M13.5 4.4L8 7.3v7.2l5.5-2.9z" fill="#1A3FA6"/></g>')
SQ = lambda x, y, c: f'<rect x="{x}" y="{y}" width="2.6" height="2.6" fill="{c}"/>'
W = 'fill="none" stroke-linecap="round" stroke-linejoin="round"'
icons = {
 'vi':       page() + SCREEN + CONN,
 'vit':      page(**TPL) + SCREEN + CONN,
 'vi-class': page() + cube(6.5, 7, .62) + CONN,
 'vim':      page() + SQ(3.5, 3, '#E020E0') + SQ(6.6, 3, '#0A8A1E') + SQ(3.5, 6.1, '#8A8A10') + SQ(6.6, 6.1, '#1E3CFF') + CONN,
 'ctl':      page() + SLIDER('#3DBB4B') + CONN,
 'ctt':      page(**TPL) + SLIDER('#3DBB4B') + CONN,
 'xctl':     page() + SLIDER('#1E9BFF') + CONN,
 'lvclass':  cube(),
 'lvlib':    page('#E3EEFF') + f'<path d="M4 4.5h4M4 6.5h4M4 8.5h3" stroke="#7C9BD6" {W}/>' + CONN,
 'lvlibp':   page('#E3EEFF') + cube(6.5, 7, .62).replace('#8DB4FF', '#B9D0FF') + f'<path d="M3.6 3.4h5.8" stroke="#0D2A78" stroke-width=".8"/>' + CONN,
 'llb':      '<path d="M4 .5h6.5l3 3V12" fill="none" stroke="#5B6B8C" stroke-linejoin="round"/>' + page().replace('M2 1h7l3.5 3.5V15H2z', 'M2 2.5h6.5l3 3V15H2z').replace('M9 1v3.5h3.5', 'M8.5 2.5V5.5h3') + SCREEN.replace('y="3"', 'y="6"').replace('M4.3 6.2l1-1.6 1.1 2 1.1-2.2 1 1.4', 'M4.3 9.2l1-1.6 1.1 2 1.1-2.2 1 1.4') + CONN,
 'lvproj':   page() + '<rect x="3.5" y="3" width="6" height="7" rx="1.2" fill="#3A3F47"/><circle cx="5.3" cy="5" r=".9" fill="#FFD21F"/><circle cx="7.7" cy="5" r=".9" fill="#3BE36B"/><path d="M4.8 8h3.4" stroke="#9AA5B1" stroke-width=".8"/>' + CONN,
 'lvsc':     page() + f'<rect x="3.5" y="2.8" width="3.6" height="2.6" rx=".9" stroke="#3A3F47" stroke-width=".9" {W}/><rect x="5.6" y="8" width="3.6" height="2.6" rx=".9" stroke="#3A3F47" stroke-width=".9" {W}/><path d="M5.3 5.4v3.9h.3" stroke="#3A3F47" stroke-width=".9" {W}/>' + CONN,
 'xnode':    page() + f'<path d="M4 3.5l5 5M9 3.5l-5 5" stroke="#B0249A" stroke-width="1.4" {W}/>' + CONN,
 'rtm':      page() + '<rect x="3.5" y="3" width="6.5" height="1.6" fill="#5B6B8C"/>' + f'<path d="M4.3 6.5h4.5M4.3 8.5h4.5M4.3 10.5h3" stroke="#5B6B8C" stroke-width=".9" {W}/>' + CONN,
 'lvbitx':   page() + '<rect x="4.2" y="3.7" width="4.6" height="4.6" rx=".6" fill="#1F7A35"/>' + f'<path d="M5.5 2.5v1.2M7.5 2.5v1.2M5.5 8.3v1.2M7.5 8.3v1.2M3 5h1.2M3 7h1.2M8.8 5H10M8.8 7H10" stroke="#1F7A35" stroke-width=".8" {W}/>' + CONN,
 'lvlps':    page() + f'<circle cx="6.5" cy="6.5" r="1.6" stroke="#5B6B8C" stroke-width="1" {W}/><path d="M6.5 3v1.2M6.5 8.8V10M3 6.5h1.2M8.8 6.5H10M4.1 4.1l.8.8M8.1 8.1l.8.8M8.9 4.1l-.8.8M4.9 8.1l-.8.8" stroke="#5B6B8C" stroke-width="1" {W}/>' + CONN,
 'aliases':  page() + f'<path d="M3.8 4.5h4.5M7 3.2l1.3 1.3L7 5.8M3.8 8.5h4.5M7 7.2l1.3 1.3L7 9.8" stroke="#5B6B8C" stroke-width=".9" {W}/>' + CONN,
 'tdms':     f'<ellipse cx="8" cy="3.5" rx="5" ry="2" fill="#7FD0D6" stroke="#0E5C64"/><path d="M3 3.5v9c0 1.1 2.2 2 5 2s5-.9 5-2v-9" fill="#1F9AA8" stroke="#0E5C64"/><path d="M3 7.5c0 1.1 2.2 2 5 2s5-.9 5-2M3 10.5c0 1.1 2.2 2 5 2s5-.9 5-2" {W} stroke="#0E5C64"/>',
 'lvm':      page() + f'<rect x="3.5" y="3" width="6.5" height="7" fill="#fff" stroke="#0E7C86" stroke-width=".9"/><path d="M3.5 5.3h6.5M3.5 7.7h6.5M6.7 3v7" stroke="#0E7C86" stroke-width=".8"/>' + CONN,
}
for k, v in icons.items(): open(O / f'{k}.svg', 'w', newline='\n').write(svg(v))
print(len(icons))
