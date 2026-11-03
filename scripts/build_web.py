"""Rakit versi WEB publik (menu, promo, kabar untuk link media sosial) dari hasil build_android.py.
Hasil: server/web/  → disajikan oleh server Cloudflare (npx wrangler deploy), di alamat server itu sendiri.
- Data selalu terbaru: /kdata.js dibuat server dari data yang diterbitkan HP Owner (tanpa data tim).
- Tanpa login, kasir, stok, atau QRIS toko.
Jalankan dari folder utama proyek:  python3 scripts/build_web.py   (otomatis dipanggil build_android.py)"""
import json, pathlib, re, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "android/app/src/main/assets/www"
OUT = ROOT / "server/web"
PLAY = "https://play.google.com/store/apps/details?id=id.coffee521.pos"

cfg = json.loads((ROOT / "android-web/config.json").read_text())
app_link = str(cfg.get("web_app_link", PLAY)).strip()
if app_link and not app_link.startswith("https://"):
    raise SystemExit("android-web/config.json: web_app_link harus diawali https:// (atau kosongkan untuk menyembunyikan tombol)")

if not (SRC / "index.html").exists():
    raise SystemExit("Jalankan dulu: python3 scripts/build_android.py")
if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "media").mkdir(parents=True)
shutil.copytree(SRC / "fonts", OUT / "fonts")

html = (SRC / "index.html").read_text()
# CSP: hanya ke server sendiri; data contoh di HTML dikosongkan (data asli datang dari /kdata.js)
html = re.sub(r"connect-src [^;]*;", "connect-src 'self';", html, count=1)
html = re.sub(r'(<script type="application/json" id="kdata">)[\s\S]*?(</script>)', r"\1{}\2", html, count=1)
html = html.replace("<title>521 Coffee App</title>",
                    '<title>521 Coffee Cart · Menu & Promo</title><meta name="description" content="Menu, harga, promo, dan kabar terbaru 521 Coffee Cart.">'
                    '<meta property="og:title" content="521 Coffee Cart · Menu & Promo"><meta property="og:description" content="Lihat menu, promo, dan kabar terbaru 521 Coffee Cart.">'
                    '<meta name="theme-color" content="#1a0b07">', 1)
assert 'src="shim.js"' in html
html = html.replace('<script src="shim.js">', '<script src="web.js"></script><script src="shim.js">', 1)
(OUT / "index.html").write_text(html)
(OUT / "web.js").write_text("window.A521_WEB=" + json.dumps({"app": app_link}) + ";\n")

# lapisan Android tanpa alamat server: web tidak menulis/menyinkronkan apa pun
shim = (SRC / "shim.js").read_text()
shim, nsub = re.subn(r'^window\.A521_CFG=\{"?server"?:\s*"[^"]*"\}', 'window.A521_CFG={server:""}', shim, count=1)
assert nsub == 1, "Format shim.js berubah: alamat server tidak ditemukan"
(OUT / "shim.js").write_text(shim)
for f in ("app.js", "qrcode.js"):
    shutil.copy2(SRC / f, OUT / f)

# foto bawaan (nama = hash isi). QRIS & QR kasir tidak ikut ke web.
n = 0
for f in (SRC / "media").iterdir():
    if re.match(r"^[a-f0-9]{32}\.(jpg|png|webp|gif|avif)$", f.name):
        shutil.copy2(f, OUT / "media" / f.name); n += 1

(OUT / "_headers").write_text("""/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  X-Frame-Options: DENY
  Permissions-Policy: camera=(), microphone=(), geolocation=(), payment=()
/media/*
  Cache-Control: public, max-age=31536000, immutable
/fonts/*
  Cache-Control: public, max-age=31536000, immutable
""")
size = sum(p.stat().st_size for p in OUT.rglob("*") if p.is_file())
print(f"Web publik siap: server/web  ({size // 1024} KB, {n} foto)  tombol Download → {app_link or '(disembunyikan)'}")
