# Hazar Sunay — kişisel site

Düz HTML/CSS/JS. Vercel'de yayınlanır (`site/` klasörü).
Blog yazıları WordPress.com'da (hazarsunay.wordpress.com) yazılmaya devam eder; site onları otomatik çeker.

## Blog nasıl güncellenir?
- **Otomatik:** GitHub Actions her gün 06:00 UTC'de WordPress'teki yazıları çeker, değişiklik varsa commit atar, Vercel siteyi yeniden yayınlar.
- **Hemen:** GitHub > Actions > "Sync blog from WordPress" > **Run workflow**.

## Yerelde derleme
```
python tools/fetch_posts.py     # WordPress'ten yazıları çek
python tools/make_sprite.py     # bayrak/motif çizimleri + arka plan deseni
python tools/build_blog.py      # site/blog/*.html sayfaları
python tools/inject_sprite.py   # ana sayfaya çizimleri ve blog kartlarını yerleştir
```

## Dosyalar
- `site/` — yayınlanan site (index.html, style.css, main.js, img/, blog/)
- `tools/` — derleme scriptleri; `tools/data/posts.json` WordPress'ten gelen yazılar
- Yeni yazının şehir bilgisi: `tools/build_blog.py` içindeki `PLACE` sözlüğüne eklenir (yoksa sadece tarih görünür).
