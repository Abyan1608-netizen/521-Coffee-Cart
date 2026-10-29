"""Rakit src/index.src.html + data + aset menjadi dist/index.html (siap terbit),
dist/preview.html (bisa dibuka langsung di browser/HP) dan dist/app.js (kode JS saja).
Jalankan dari folder utama proyek:  python3 scripts/build.py"""
import base64, json, re, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
A, D = ROOT / "assets", ROOT / "dist"
b64 = lambda p: base64.b64encode(p.read_bytes()).decode()

s = (ROOT / "src/index.src.html").read_text()
K = json.loads((ROOT / "data/kdata.json").read_text())
logo = (A / "logo.sym").read_text().strip().replace('<svg width="0"', '<svg id="logo-sprite" width="0"', 1)
s = s.replace("__LOGO__", logo)
s = s.replace("__KDATA__", json.dumps(K, ensure_ascii=False).replace("<", "\\u003c"))
s = s.replace("__PQR__", "data:image/png;base64," + b64(A / "posqr.png"))
s = s.replace("__HERO__", "data:image/jpeg;base64," + b64(A / "hero.jpg"))
s = s.replace("__QRIS__", "data:image/jpeg;base64," + b64(A / "qris.jpg"))
W = [("Light", "300"), ("Text_Book", "400"), ("Medium", "500"), ("Demi_Bold", "600"), ("Bold", "700"), ("Heavy", "800 900")]
s = s.replace("__FONTS__", "".join(
    '@font-face{font-family:"Paralucent521";src:url(data:font/woff;base64,' + b64(A / f"fonts/par-{n}.woff")
    + f') format("woff");font-weight:{w};font-style:normal;font-display:swap}}' for n, w in W))

D.mkdir(exist_ok=True)
(D / "index.html").write_text(s)
(D / "preview.html").write_text('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" '
    'content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>' + s + "</body></html>")
(D / "app.js").write_text(re.search(r'<script id="appjs">(.*)</script>', s, re.S).group(1))
print("Selesai: dist/index.html, dist/preview.html, dist/app.js")
