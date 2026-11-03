"""Perubahan 12: versi web publik (menu, promo, kabar) untuk link media sosial — tanpa login/kasir,
dengan tombol Download aplikasi. Kode yang sama dipakai aplikasi Android; mode web aktif bila window.A521_WEB ada. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V12-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


rep(".hubn{", """/*V12-PATCH*/
a.k-login{text-decoration:none;color:var(--ink)}
.k-app{display:flex;gap:12px;align-items:center;margin:18px 0 6px;padding:14px 16px;border-radius:18px;background:var(--ac);color:var(--on);text-decoration:none}
.k-app span{flex:1;font-size:13.5px;line-height:1.4;font-weight:600}.k-app b{display:block;font-size:16px;font-weight:800}
.k-app i{font-style:normal;flex:none;padding:9px 14px;border-radius:999px;background:rgba(0,0,0,.2);font-weight:800;font-size:14px}
.hubn{""")

# mode web: tidak ada login/kasir
rep('function showLogin(){', 'function showLogin(){if(WEB){showPub();return}')
rep('if(me)enter();else if(location.hash==="#masuk")showLogin();else{showPub();welcome()}',
    'if(WEB){me=null;showPub();welcome()}else if(me)enter();else if(location.hash==="#masuk")showLogin();else{showPub();welcome()}')
rep('<button class="k-login" data-a="${me?"toapp":"masuk"}">${ic("user")}${me?"Kembali ke kasir":"Masuk"}</button>',
    '${WEB?(webApp()?`<a class="k-login" href="${esc(webApp())}" target="_blank" rel="noopener">${ic("phone")}Download aplikasi</a>`:""):`<button class="k-login" data-a="${me?"toapp":"masuk"}">${ic("user")}${me?"Kembali ke kasir":"Masuk"}</button>`}')
rep('<details class="k-week"><summary>${ic("today")}Jadwal buka seminggu</summary>',
    '${WEB&&webApp()?`<a class="k-app" href="${esc(webApp())}" target="_blank" rel="noopener">${ic("phone")}<span><b>Download aplikasi ${esc(s.name||"521")}</b>Dapat notifikasi promo, diskon & kabar terbaru langsung di HP.</span><i>Download</i></a>`:""}<details class="k-week"><summary>${ic("today")}Jadwal buka seminggu</summary>')

NEW = r'''
/*V12-PATCH*/
/* Versi web publik (dibuka dari link media sosial): hanya menu, promo & kabar. Tidak ada login, kasir, atau data toko. */
var WEB=!!window.A521_WEB;
function webApp(){const u=String((window.A521_WEB||{}).app||"");return /^https:\/\//.test(u)?u:""}
'''
rep("/*V11-PATCH*/\n/* Owner masuk di HP", NEW + "/*V11-PATCH*/\n/* Owner masuk di HP")

P.write_text(s)
print("OK, perubahan 12 (versi web publik) diterapkan.")
