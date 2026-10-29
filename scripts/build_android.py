"""Rakit versi Android: src/ + data/ + assets/ -> android/app/src/main/assets/www/
- Foto & font disimpan sebagai file biner (bukan base64) -> ±25% lebih kecil dan jauh lebih cepat di-parse.
- Foto kembar disimpan sekali (nama file = hash isinya).
- JS & CSS di-minify (esbuild). Kualitas foto TIDAK diubah sama sekali (byte JPEG asli).
- QR lokal (tanpa CDN), CSP ketat, lapisan Android (shim.js).
Jalankan dari folder utama proyek:  python3 scripts/build_android.py
Butuh: Python 3 + esbuild (npx esbuild / npm i -g esbuild). Server opsional: isi android-web/config.json"""
import base64, hashlib, json, os, pathlib, re, shutil, subprocess, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
A, AW = ROOT / "assets", ROOT / "android-web"
OUT = ROOT / "android/app/src/main/assets/www"
PLAY = "https://play.google.com/store/apps/details?id=id.coffee521.pos"


def esbuild():
    for c in (os.environ.get("ESBUILD"), shutil.which("esbuild"), "/opt/npm-tools/node_modules/.bin/esbuild"):
        if c and pathlib.Path(c).exists():
            return [c]
    return ["npx", "--yes", "esbuild@0.25.0"]


def minify(code, loader, extra=()):
    r = subprocess.run(esbuild() + [f"--loader={loader}", "--minify", "--target=chrome90", "--charset=utf8", "--legal-comments=none", *extra],
                       input=code.encode(), capture_output=True)
    if r.returncode:
        sys.exit(r.stderr.decode())
    return r.stdout.decode()


cfg = json.loads((AW / "config.json").read_text()) if (AW / "config.json").exists() else {}
server = str(cfg.get("server", "")).rstrip("/")
if server and not server.startswith("https://"):
    sys.exit("android-web/config.json: server harus diawali https://")

if OUT.exists():
    shutil.rmtree(OUT)
(OUT / "media").mkdir(parents=True)
(OUT / "fonts").mkdir()

EXT = {"image/jpeg": "jpg", "image/png": "png", "image/webp": "webp", "image/gif": "gif"}
saved = {}


def put_media(raw: bytes, ext: str, name: str = None) -> str:
    name = name or hashlib.sha256(raw).hexdigest()[:32] + "." + ext
    if name not in saved:
        (OUT / "media" / name).write_bytes(raw)
        saved[name] = len(raw)
    return "media/" + name


def externalize(o):
    if isinstance(o, dict):
        return {k: externalize(v) for k, v in o.items()}
    if isinstance(o, list):
        return [externalize(v) for v in o]
    if isinstance(o, str):
        m = re.match(r"^data:(image/[a-z+.-]+);base64,(.+)$", o, re.S)
        if m and m.group(1) in EXT:
            return put_media(base64.b64decode(m.group(2)), EXT[m.group(1)])
    return o


# --- Data toko (Kabar, menu, tim) ---
K = externalize(json.loads((ROOT / "data/kdata.json").read_text()))
# Paket data tim (resep, akun, member — terenkripsi kode tim lama) TIDAK ikut ke APK publik.
# Owner mengaktifkan sinkron tim baru dari aplikasi; data tim lalu dikirim lewat server.
K.pop("team", None)
(OUT / "kdata.js").write_text("window.__KREV=0;window.__K=" + json.dumps(K, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c") + ";")

# --- QR promo (link Play Store) & QRIS bawaan ---
put_media((A / "qris.jpg").read_bytes(), "jpg", "qris.jpg")
put_media((A / "posqr.png").read_bytes(), "png", "posqr.png")

# --- Font: file .woff asli, hanya ketebalan yang dipakai ---
W = [("Light", "300"), ("Text_Book", "400"), ("Medium", "500"), ("Demi_Bold", "600"), ("Bold", "700"), ("Heavy", "800 900")]
fonts = ""
for n, w in W:
    shutil.copy(A / f"fonts/par-{n}.woff", OUT / f"fonts/par-{n}.woff")
    fonts += f'@font-face{{font-family:"Paralucent521";src:url(fonts/par-{n}.woff) format("woff");font-weight:{w};font-style:normal;font-display:swap}}'

s = (ROOT / "src/index.src.html").read_text()
s = s.replace("__PQR__", "media/posqr.png").replace("__QRIS__", "media/qris.jpg")
logo = (A / "logo.sym").read_text().strip().replace('<svg width="0"', '<svg id="logo-sprite" width="0"', 1)

css = re.search(r'<style id="css">(.*?)</style>', s, re.S).group(1).replace("__FONTS__", fonts)
js = re.search(r'<script id="appjs">(.*)</script>', s, re.S).group(1)
css_min = minify(css, "css")
js_min = minify(js, "js")
for must in ("function chatClose", "function shut", "function showPub", "function lines"):
    if must.split()[1] + "(" not in js_min and must not in js_min:
        sys.exit("Minify mengganti nama fungsi global yang dipakai shim: " + must)
(OUT / "app.js").write_text(js_min)

shim = "window.A521_CFG=" + json.dumps({"server": server}) + ";\n" + (AW / "shim.js").read_text()
(OUT / "shim.js").write_text(minify(shim, "js"))
r = subprocess.run(esbuild() + [str(AW / "qrcode-entry.js"), "--bundle", "--minify", "--format=iife", "--target=chrome90", "--legal-comments=none",
                                "--banner:js=/* QRCode for JavaScript (c) 2009 Kazuhiko Arase, MIT */"], capture_output=True)
if r.returncode:
    sys.exit(r.stderr.decode())
(OUT / "qrcode.js").write_bytes(r.stdout)

conn = "'self'" + (f" {server} {server.replace('https://', 'wss://', 1)}" if server else "")
csp = ("default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data: blob:; "
       f"font-src 'self'; connect-src {conn}; media-src 'self' data: blob:; object-src 'none'; base-uri 'none'; "
       "form-action 'none'; frame-src 'none'; worker-src 'none'")

html = ('<!doctype html><html lang="id"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f'<meta http-equiv="Content-Security-Policy" content="{csp}">'
        '<meta name="color-scheme" content="dark light"><title>521 Coffee App</title>'
        f'<style id="css">{css_min}</style></head><body>'
        f'{logo}<div id="mount"></div>'
        '<script type="application/json" id="kdata"></script>'
        '<script src="kdata.js"></script><script src="shim.js"></script><script src="qrcode.js"></script>'
        '<script id="appjs" src="app.js"></script></body></html>')
(OUT / "index.html").write_text(html)
(OUT / "a521.json").write_text(json.dumps({"server": server}))

tot = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
print(f"Selesai: {OUT.relative_to(ROOT)}  ({tot/1024:.0f} KB, {len(saved)} file media)  server={'(offline)' if not server else server}")
