"""site/index.html içine sprite'ı ve blog kartlarını yerleştirir (tekrar çalıştırılabilir).
Sıra: python tools/make_sprite.py && python tools/build_blog.py && python tools/inject_sprite.py
"""
import re


def fill(html, name, content):
    return re.sub(rf"<!--{name}-->.*?<!--/{name}-->", lambda m: f"<!--{name}-->{content}<!--/{name}-->", html, flags=re.S)


html = open("site/index.html", encoding="utf-8").read()
html = fill(html, "SPRITE", open("tools/build/sprite.svg.inc", encoding="utf-8").read())
html = fill(html, "CARDS", open("tools/build/cards.inc", encoding="utf-8").read())
open("site/index.html", "w", encoding="utf-8").write(html)
print("index.html güncellendi")
