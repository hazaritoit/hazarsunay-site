"""Blog yazılarını tools/data/posts.json'dan (WordPress.com dışa aktarımı) site/blog/<slug>.html olarak üretir.
Ayrıca ana sayfa için tools/build/cards.inc (kart listesi) yazar.
Çalıştırma (proje kökünden):  python tools/build_blog.py
"""
import html
import json
import re

POSTS = json.load(open("tools/data/posts.json", encoding="utf-8"))["posts"]

# Yazı başına konum (kartlarda ve yazı başlığında gösterilir)
PLACE = {
    "meeting-h-e-elif-comoglu-ulgen-ambassador-of-the-republic-of-turkiye-to-rome": "Rome",
    "cultural-bridges-insights-from-the-yunus-emre-event-in-rome": "Rome",
    "building-bridges-global-changemakers-at-summer-academy-2025": "Karlsruhe",
    "exploring-the-european-parliament-a-students-insight": "Brussels",
    "insights-from-erasmus-staff-mobility-in-krakow": "Kraków",
}
MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August",
          "September", "October", "November", "December"]


def nice_date(d):
    y, m, day = d[:10].split("-")
    return f"{int(day)} {MONTHS[int(m) - 1]} {y}"


def clean_inline(s):
    """Satır içi HTML'i sadeleştir: class/style/data öznitelikleri at, bağlantıları yeni sekmede aç."""
    s = re.sub(r'\s(class|style|data-[\w-]+|id|rel|target)="[^"]*"', "", s)
    s = re.sub(r"<a\s+href=", '<a target="_blank" rel="noopener" href=', s)
    s = re.sub(r"<(?!/?(a|strong|em|b|i|br)\b)[^>]+>", "", s)  # izin verilmeyen etiketleri at
    return s.strip()


def strip_q(url):
    return url.split("?")[0]


def parse(content):
    blocks = []
    for m in re.finditer(r"<(p|ul|ol|h2|h3|h4)\b[^>]*>(.*?)</\1>", content, flags=re.S):
        tag, inner = m.group(1), m.group(2)
        if tag in ("ul", "ol"):
            items = [clean_inline(li) for li in re.findall(r"<li\b[^>]*>(.*?)</li>", inner, flags=re.S)]
            items = [i for i in items if i]
            if items:
                blocks.append(f"<{tag}>" + "".join(f"<li>{i}</li>" for i in items) + f"</{tag}>")
        else:
            txt = clean_inline(inner)
            if txt and re.sub(r"<[^>]+>|&nbsp;|\s", "", txt):
                blocks.append(f"<{tag}>{txt}</{tag}>")
    imgs = []
    for src in re.findall(r'<img[^>]+src="([^"]+)"', content):
        u = strip_q(html.unescape(src))
        if "/wp-content/uploads/" in u and u not in imgs:
            imgs.append(u)
    return blocks, imgs


HEADER = """<header class="top">
  <div class="wrap top__in">
    <a href="../index.html" class="crest" aria-label="Hazar Sunay, home">
      <span class="crest__mark"><svg><use href="#laurel"/></svg><b>HS</b></span>
      <span class="crest__name">Hazar Sunay<small>Public &amp; Cultural Diplomacy</small></span>
    </a>
    <nav class="nav" id="nav">
      <a href="../index.html#profile">Profile</a>
      <a href="../index.html#experience">Experience</a>
      <a href="../index.html#education">Education</a>
      <a href="../index.html#research">Research</a>
      <a href="../index.html#blog">Blog</a>
      <a href="../index.html#contact" class="nav__cta">Contact</a>
    </nav>
    <button class="burger" aria-label="Open menu" aria-expanded="false"><span></span><span></span></button>
  </div>
</header>"""

import glob
import os

sprite = open("tools/build/sprite.svg.inc", encoding="utf-8").read()
posts = sorted(POSTS, key=lambda p: p["date"], reverse=True)
cards = []

# WordPress'te silinen yazıların sayfalarını kaldır
live = {p["slug"] for p in posts}
for f in glob.glob("site/blog/*.html"):
    if os.path.splitext(os.path.basename(f))[0] not in live:
        os.remove(f)


def where_when(place, date):
    return f"{place} · {date}" if place else date

for i, p in enumerate(posts):
    slug = p["slug"]
    title = html.unescape(p["title"])
    feat = strip_q(p["featured_image"] or "")
    blocks, imgs = parse(p["content"])
    gallery = [u for u in imgs if u != feat]
    place = PLACE.get(slug, "")
    date = nice_date(p["date"])
    prev_p = posts[i + 1] if i + 1 < len(posts) else None
    next_p = posts[i - 1] if i > 0 else None

    gal_html = ""
    if gallery:
        gal_html = '<section class="gallery">' + "".join(
            f'<a href="{u}" target="_blank" rel="noopener"><img src="{u}?w=900" alt="" loading="lazy"></a>' for u in gallery
        ) + "</section>"

    def navlink(q, cls, label):
        if not q:
            return "<span></span>"
        return (f'<a class="{cls}" href="{q["slug"]}.html"><small>{label}</small>'
                f'{html.escape(html.unescape(q["title"]))}</a>')

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} · Hazar Sunay</title>
<meta name="description" content="{html.escape(re.sub(r'<[^>]+>', '', blocks[0])[:155] if blocks else title)}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:image" content="{feat}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="../style.css">
</head>
<body class="article-page">
{sprite}
{HEADER}
<main>
  <article class="article">
    <header class="article__head">
      <div class="wrap">
        <a class="article__back" href="../index.html#blog">← Blog</a>
        <p class="eyebrow">{where_when(place, date)}</p>
        <h1>{html.escape(title)}</h1>
      </div>
    </header>
    <figure class="article__cover wrap"><img src="{feat}?w=1600" alt=""></figure>
    <div class="article__body">
      {"".join(blocks)}
    </div>
    <div class="wrap">{gal_html}</div>
    <nav class="article__nav wrap">
      {navlink(prev_p, "older", "Previous post")}
      {navlink(next_p, "newer", "Next post")}
    </nav>
  </article>
</main>
<footer class="mini-foot"><div class="wrap"><span>© 2026 Hazar Sunay</span><a href="../index.html#contact">Contact</a></div></footer>
<script src="../main.js"></script>
</body>
</html>
"""
    open(f"site/blog/{slug}.html", "w", encoding="utf-8").write(page)

    cards.append(
        f'<a class="bcard reveal" href="blog/{slug}.html">'
        f'<span class="bcard__img"><img src="{feat}?w=900" alt="" loading="lazy"></span>'
        f'<span class="bcard__meta">{where_when(place, date)}</span>'
        f'<h3>{html.escape(title)}</h3></a>'
    )
    print(f"{slug}: {len(blocks)} paragraf, {len(gallery)} galeri görseli")

open("tools/build/cards.inc", "w", encoding="utf-8").write("\n".join(cards))
