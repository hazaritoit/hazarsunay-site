"""WordPress.com'daki blog yazılarını herkese açık API'den çeker -> tools/data/posts.json
Yazılar WordPress'te yazılmaya devam eder; bu script onları siteye taşır.
Çalıştırma (proje kökünden):  python tools/fetch_posts.py
"""
import json
import urllib.request

SITE = "hazarsunay.wordpress.com"
URL = (f"https://public-api.wordpress.com/rest/v1.1/sites/{SITE}/posts/"
       "?number=100&fields=ID,title,date,URL,slug,featured_image,content,tags")

req = urllib.request.Request(URL, headers={"User-Agent": "static-site-sync"})
with urllib.request.urlopen(req, timeout=30) as r:
    data = json.load(r)

posts = data.get("posts", [])
if not posts:
    raise SystemExit("API'den yazı gelmedi; mevcut posts.json korunuyor.")

with open("tools/data/posts.json", "w", encoding="utf-8") as f:
    json.dump({"found": data.get("found"), "posts": posts}, f, ensure_ascii=False, indent=1)
print(f"{len(posts)} yazı çekildi")
