"""Bayrak ve motif SVG'lerini (sprite) üretir -> tools/build/sprite.svg.inc
Bayraklar 30x20 görünüm kutusunda, sade ve doğru oranlı çizilir.
Motifler (defne çelengi, küre, yıldız halkası) jeneriktir; hiçbir kurumun resmi amblemi değildir.
"""
import math

out = []


def star(cx, cy, R, rot_deg=-90, ratio=0.382):
    pts = []
    for i in range(10):
        r = R if i % 2 == 0 else R * ratio
        a = math.radians(rot_deg + i * 36)
        pts.append(f"{cx + r * math.cos(a):.3f},{cy + r * math.sin(a):.3f}")
    return " ".join(pts)


def sym(id_, body, vb="0 0 30 20"):
    par = ' preserveAspectRatio="xMidYMid slice"' if id_.startswith("flag-") else ""
    out.append(f'<symbol id="{id_}" viewBox="{vb}"{par}>{body}</symbol>')


# --- Bayraklar ---
sym("flag-tr", '<rect width="30" height="20" fill="#E30A17"/>'
    '<circle cx="11" cy="10" r="5" fill="#fff"/><circle cx="12.25" cy="10" r="4" fill="#E30A17"/>'
    f'<polygon points="{star(16.6, 10, 2.5, 180)}" fill="#fff"/>')
sym("flag-it", '<rect width="10" height="20" fill="#009246"/><rect x="10" width="10" height="20" fill="#fff"/>'
    '<rect x="20" width="10" height="20" fill="#CE2B37"/>')
sym("flag-de", '<rect width="30" height="6.67" fill="#000"/><rect y="6.67" width="30" height="6.67" fill="#DD0000"/>'
    '<rect y="13.33" width="30" height="6.67" fill="#FFCE00"/>')
# İspanya: 1:2:1 kırmızı-sarı-kırmızı, arma direğe yakın (merkezi bayrak yüksekliğinin yarısı kadar içeride)
ES_ARMS = (
    '<g transform="translate(5.6 5.4) scale(0.11)" stroke="#7a5a12" stroke-width="0.9">'
    # Herkül sütunları
    + ''.join(
        f'<rect x="{x}" y="14" width="10" height="5" fill="#E8B923"/>'
        f'<path d="M{x+1} 14 l1 -6 h6 l1 6 z" fill="#E8B923"/><circle cx="{x+5}" cy="7" r="1.6" fill="#C8102E"/>'
        f'<rect x="{x+2}" y="19" width="6" height="50" fill="#D9D9D9"/>'
        f'<rect x="{x}" y="69" width="10" height="5" fill="#E8B923"/>'
        f'<rect x="{x-2}" y="38" width="14" height="6" fill="#C8102E"/>'
        for x in (0, 70))
    # Kalkan
    + '<clipPath id="es-shield"><path d="M22 24 H58 V56 Q58 72 40 72 Q22 72 22 56 Z"/></clipPath>'
    + '<g clip-path="url(#es-shield)" stroke="none">'
      '<rect x="22" y="24" width="18" height="24" fill="#C8102E"/>'
      '<rect x="27" y="30" width="8" height="10" fill="#E8B923"/><rect x="29" y="27" width="4" height="4" fill="#E8B923"/>'
      '<rect x="40" y="24" width="18" height="24" fill="#F2F2F2"/>'
      '<path d="M44 44 q2 -12 9 -12 q-2 6 1 12 z" fill="#7B2D8E"/>'
      '<rect x="22" y="48" width="18" height="24" fill="#FCDD09"/>'
      + ''.join(f'<rect x="{24+i*4}" y="48" width="2" height="24" fill="#C8102E"/>' for i in range(4))
    + '<rect x="40" y="48" width="18" height="24" fill="#C8102E"/>'
      '<path d="M41 49 L57 71 M57 49 L41 71 M49 48 V72 M40 60 H58" stroke="#E8B923" stroke-width="1.6"/>'
      '</g>'
    + '<path d="M22 24 H58 V56 Q58 72 40 72 Q22 72 22 56 Z" fill="none"/>'
    + '<ellipse cx="40" cy="48" rx="6" ry="7" fill="#003DA5"/>'
    # Taç
    + '<path d="M25 22 Q40 2 55 22 Z" fill="#C8102E"/><path d="M25 22 Q40 6 55 22" fill="none" stroke="#E8B923" stroke-width="2.4"/>'
    + '<rect x="24" y="18" width="32" height="6" fill="#E8B923"/>'
    + '<path d="M40 4 v-4 M38 2 h4" stroke="#E8B923" stroke-width="1.6"/>'
    + '</g>'
)
sym("flag-es", '<rect width="30" height="20" fill="#AA151B"/><rect y="5" width="30" height="10" fill="#F1BF00"/>' + ES_ARMS)
sym("flag-gb", '<rect width="30" height="20" fill="#012169"/>'
    '<path d="M0 0 L30 20 M30 0 L0 20" stroke="#fff" stroke-width="4"/>'
    '<path d="M0 0 L30 20 M30 0 L0 20" stroke="#C8102E" stroke-width="1.4"/>'
    '<path d="M15 0 V20 M0 10 H30" stroke="#fff" stroke-width="6"/>'
    '<path d="M15 0 V20 M0 10 H30" stroke="#C8102E" stroke-width="3.4"/>')
sym("flag-pl", '<rect width="30" height="10" fill="#fff"/><rect y="10" width="30" height="10" fill="#DC143C"/>')
sym("flag-be", '<rect width="10" height="20" fill="#000"/><rect x="10" width="10" height="20" fill="#FDDA24"/>'
    '<rect x="20" width="10" height="20" fill="#EF3340"/>')
eu_stars = "".join(
    f'<polygon points="{star(15 + 6.667 * math.cos(math.radians(-90 + k * 30)), 10 + 6.667 * math.sin(math.radians(-90 + k * 30)), 1.11)}" fill="#FFCC00"/>'
    for k in range(12))
sym("flag-eu", f'<rect width="30" height="20" fill="#003399"/>{eu_stars}')

# --- Motif: defne çelengi (jenerik) ---
leaves = []
for side in (-1, 1):
    for i in range(9):
        # yay üzerinde nokta (alttan üste)
        ang = math.radians(110 + i * 16) if side == -1 else math.radians(70 - i * 16)
        x = 50 + 38 * math.cos(ang)
        y = 54 + 38 * math.sin(ang) * -1
        rot = math.degrees(-ang) + (32 if side == -1 else -32)
        leaves.append(f'<ellipse cx="{x:.2f}" cy="{y:.2f}" rx="3.2" ry="8" transform="rotate({rot:.1f} {x:.2f} {y:.2f})"/>')
stems = ('<path d="M42.1 91.2 A38 38 0 0 1 38.3 17.9" fill="none" stroke="currentColor" stroke-width="1.2"/>'
         '<path d="M57.9 91.2 A38 38 0 0 0 61.7 17.9" fill="none" stroke="currentColor" stroke-width="1.2"/>')
sym("laurel", f'<g fill="currentColor">{"".join(leaves)}</g>{stems}', "0 0 100 100")

# --- Motif: küre (meridyen/paralel çizgileri) ---
globe = ['<circle cx="50" cy="50" r="46"/>']
for rx in (14, 30):
    globe.append(f'<ellipse cx="50" cy="50" rx="{rx}" ry="46"/>')
globe.append('<line x1="50" y1="4" x2="50" y2="96"/>')
for dy in (-30, -15, 0, 15, 30):
    w = math.sqrt(46 ** 2 - dy ** 2)
    globe.append(f'<line x1="{50 - w:.2f}" y1="{50 + dy}" x2="{50 + w:.2f}" y2="{50 + dy}"/>')
sym("globe", f'<g fill="none" stroke="currentColor" stroke-width="0.8">{"".join(globe)}</g>', "0 0 100 100")

# --- Motif: yıldız halkası ---
ring = "".join(
    f'<polygon points="{star(50 + 38 * math.cos(math.radians(-90 + k * 30)), 50 + 38 * math.sin(math.radians(-90 + k * 30)), 5)}"/>'
    for k in range(12))
sym("starring", f'<g fill="currentColor">{ring}</g>', "0 0 100 100")

svg = '<svg xmlns="http://www.w3.org/2000/svg" style="display:none">' + "".join(out) + "</svg>"
open("tools/build/sprite.svg.inc", "w", encoding="utf-8").write(svg)
print(len(svg), "bytes,", len(out), "symbols")

# --- Arka plan deseni (açık zeminli bölümler için, çok soluk) ---
defs = "".join(o for o in out if any(f'id="{k}"' in o for k in ("laurel", "globe", "starring")))
placements = [("laurel", 30, 40, 120, -12), ("globe", 330, 30, 96, 0), ("starring", 460, 290, 120, 8),
              ("laurel", 230, 370, 96, 16), ("globe", 40, 430, 72, 0), ("starring", 170, 200, 64, 0),
              ("globe", 470, 520, 54, 0)]
uses = "".join(f'<use href="#{n}" x="{x}" y="{y}" width="{s}" height="{s}" transform="rotate({r} {x + s / 2} {y + s / 2})"/>'
               for n, x, y, s, r in placements)
pattern = ('<svg xmlns="http://www.w3.org/2000/svg" width="600" height="600" viewBox="0 0 600 600">'
           f'<defs>{defs}</defs><g color="#c39a46" opacity="0.085">{uses}</g></svg>')
import os
os.makedirs("site/img", exist_ok=True)
open("site/img/pattern.svg", "w", encoding="utf-8").write(pattern)
print("pattern.svg", len(pattern), "bytes")
