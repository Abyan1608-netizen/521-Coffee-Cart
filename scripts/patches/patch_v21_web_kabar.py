"""Perubahan 21 (masukan tim 5 Nov 2026):
1. Halaman Kabar untuk pelanggan di aplikasi = website 521 (tampilan sama persis). Aplikasi tanpa login / "Lihat di website"
   membuka website di dalam aplikasi; tombol "Masuk" / "Kembali ke kasir" di website kembali ke aplikasi.
   Tanpa internet: halaman Kabar tersimpan di aplikasi tetap tampil.
2. Headline Kabar website diatur dari aplikasi (Atur → Website, atau tombol "Jadikan headline" di tiap promo/kabar).
3. Kartu menu website: keterangan kecil (Kategori · Ukuran cup, atau tulis sendiri / tanpa keterangan) dan foto diatur
   dari Atur → Website → Kartu menu.
Sekali jalan."""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parents[1] / "src/index.src.html"
s = P.read_text()
if "/*V21-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


# 1. halaman pelanggan → website (hanya di aplikasi Android; versi web server tetap)
rep("function showPub(){",
    "function showPub(){/*V21-PATCH*/if(!WEB&&window.A521&&A521.native&&navigator.onLine!==false&&location.hash!==\"#luring\"&&typeof WEB_URL===\"string\"){"
    "$(\"#m\").hidden=true;try{location.replace(WEB_URL+(me?\"?dari=kasir\":\"\"));return}catch(e){}}")
rep("Halaman yang dilihat pelanggan saat membuka link tanpa masuk.",
    "Promo, kegiatan, dan kabar di sini tampil di website 521 untuk pelanggan.")
rep('data-a="kview">Lihat sebagai pelanggan</button>', 'data-a="kview">Lihat di website</button>')

# 2. headline dari tiap promo/kabar
rep('<div class="lbl">Tampil di halaman pelanggan?</div>',
    '<div class="lbl">Headline website?</div><div class="chips"><button data-a="khead" data-v="1" aria-pressed="${kIsHead(p)}">Jadikan headline</button>'
    '<button data-a="khead" data-v="0" aria-pressed="${!kIsHead(p)}">Tidak</button></div>'
    '<p class="note" style="margin-top:-4px">Headline = kartu paling besar & paling atas di bagian Kabar website.</p>'
    '<div class="lbl">Tampil di halaman pelanggan?</div>')
rep("const nw=kp.isNew;delete kp.isNew;", "const nw=kp.isNew;delete kp.isNew;{const hd=kp._head;delete kp._head;kHeadSave(kp,hd)}")

# 3. kartu menu website: foto & keterangan ikut terbit bersama menu
rep("if(p.out)x.o=1;return x})}",
    "if(p.out)x.o=1;const w=webMI(p);if(w.img)x.img=w.img;if(typeof w.lb===\"string\")x.lb=w.lb;return x})}")
rep("<h3>Bagian yang tampil</h3>", "${webHeadHTML()}${webMenuHTML()}<h3>Bagian yang tampil</h3>")
rep("K.store.web=W;kChanged();", "webMenuSave(W);K.store.web=W;try{if(Array.isArray(K.menu))K.menu=menuSnap()}catch(e){}kChanged();")

JS = (HERE / "patch_v21_app.js").read_text()
rep("/* ---------- Printer Bluetooth (Web Bluetooth, ESC/POS) ---------- */", JS + "\n/* ---------- Printer Bluetooth (Web Bluetooth, ESC/POS) ---------- */")
rep("\n</style>\n", """
/* V21: kartu menu website di Atur → Website */
.wmc{display:grid;grid-template-columns:84px minmax(0,1fr);gap:12px;align-items:start;padding:12px;margin:10px 0;border:1px solid var(--line);border-radius:16px;background:var(--sf)}
.wmc-ph{width:84px;aspect-ratio:4/5;border-radius:12px;overflow:hidden;background:var(--sf2);display:grid;place-items:center;text-align:center}
.wmc-ph img{width:100%;height:100%;object-fit:cover;display:block}.wmc-ph span{font-size:11px;font-weight:700;color:var(--mute);padding:6px;line-height:1.25}
.wmc-b>b{display:block;font-size:16px;margin-bottom:4px}.wmc-b label{margin-top:6px}
.wmc-now{margin:6px 0 0;font-size:13px;color:var(--mute)}.wmc-now b{color:var(--ink)}
.wmc-x{display:flex!important;align-items:center;gap:8px;font-size:14px;font-weight:600}.wmc-x input{width:20px;height:20px;margin:0}
.wmc-up{font-size:14px;font-weight:700}
</style>
""")

P.write_text(s)
print("OK, perubahan 21 diterapkan.")
