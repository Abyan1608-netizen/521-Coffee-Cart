"""Perubahan 18 (final): tema terang lebih kontras, notifikasi saat promo diubah, cetak struk Bluetooth native,
pengaturan Website di Atur, kotak "Dari HP lain hari ini" dihapus untuk Owner. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V18-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


# ------------------------------------------------------------------ 1. Tema terang: kontras teks & kartu
rep("\n</style>\n", """
/*V18-PATCH*/
/* Tema terang: teks lebih gelap, kartu putih bersih dengan garis & bayangan tipis, latar tidak lagi oranye pucat */
:root[data-ui="light"]{--bg:#f4f0eb;--sf:#ffffff;--sf2:#f0e9e2;--sf3:#e2d6cb;--ink:#1a0904;--mute:#5a4033;--dim:#6e5243;--line:#d9cbbf;--ok:#16723d;--warn:#b02e00;--glass:rgba(255,255,255,.93)}
:root[data-ui="light"] body::before{background:radial-gradient(55% 40% at 95% -6%,rgba(192,50,0,.10),transparent 70%),radial-gradient(40% 35% at -5% 105%,rgba(216,255,0,.16),transparent 70%)}
:root[data-ui="light"] body::after{opacity:.22}
:root:not([data-ui="light"]){--dim:#b38b79}
:root[data-glass][data-ui="light"]{--sf:rgba(255,255,255,.88);--sf2:rgba(255,255,255,.72);--sf3:rgba(120,60,30,.10);--line:rgba(110,60,30,.17);--glass:rgba(255,255,255,.84)}
:root[data-glass][data-ui="light"] body::before{background:radial-gradient(45% 35% at 85% 8%,rgba(192,50,0,.14),transparent 70%),radial-gradient(40% 35% at 8% 55%,rgba(216,255,0,.22),transparent 70%),radial-gradient(45% 40% at 90% 95%,rgba(134,36,1,.14),transparent 70%)}
:root[data-ui="light"] :is(.sec,.tile,.ticket,.kpi>div,.folder,.k-promo,.rcard,.chart){box-shadow:0 1px 2px rgba(60,25,10,.06),0 10px 24px -18px rgba(60,25,10,.35)}
:root[data-ui="light"] .tile.has{box-shadow:0 0 0 1px var(--ac) inset,0 12px 26px -16px color-mix(in srgb,var(--ac) 60%,transparent)}
:root[data-ui="light"] .tile .gl{opacity:.14}
:root[data-ui="light"] nav.dock{box-shadow:0 14px 34px -14px rgba(60,25,10,.45)}
:root[data-ui="light"] .chips button{color:var(--ink)}
:root[data-ui="light"] .chips button[aria-pressed="true"]{color:#fff}
:root[data-ui="light"] .kt-stars{color:#a65f00}
:root[data-ui="light"] .k-foot{color:var(--mute)}
:root[data-ui="light"] .kmore{opacity:1;color:#9a2800}
:root[data-ui="light"] .k-code small{color:#fff;background:#a82c00}
:root[data-ui="light"] input,:root[data-ui="light"] select,:root[data-ui="light"] textarea{background:#fff;border-color:#cdbcae}
:root[data-ui="light"] .btn.ghost{background:#fff;border-color:#cdbcae}
.k-igfollow{background:linear-gradient(45deg,#a8400f,#b51c60,#6f2b9a)!important;text-shadow:0 1px 2px rgba(0,0,0,.3)}
/* Printer Bluetooth */
.btlist{display:grid;gap:8px;margin:10px 0}
.btlist button{display:flex;align-items:center;gap:12px;width:100%;text-align:left;border:1px solid var(--line);background:var(--sf);border-radius:14px;padding:12px 14px;color:var(--ink)}
.btlist button b{display:block;font-size:15px}.btlist button small{color:var(--mute)}
.btlist button[aria-pressed="true"]{border-color:var(--ac);box-shadow:0 0 0 1px var(--ac) inset}
.btscan{display:flex;align-items:center;gap:10px;color:var(--mute);font-size:14px;margin:8px 0}
.btscan i{width:14px;height:14px;border-radius:50%;border:2px solid var(--ac);border-right-color:transparent;animation:spin .8s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
</style>
""")

# ------------------------------------------------------------------ 2. Kotak "Dari HP lain hari ini" tidak tampil lagi di HP Owner
rep("""  if(own()||isHub()){const R=D.tx.filter(t=>t.rx&&t.d===today""", """  if(own()||isHub())return "";
  if(false){const R=D.tx.filter(t=>t.rx&&t.d===today""")

# ------------------------------------------------------------------ 3. Notifikasi: promo/diskon/kabar yang DIUBAH juga dikabari (bawaan: ya)
rep('kabar:{on:1,to:"semua",snd:"lonceng"},event:{on:1,to:"semua",snd:"ding"},edit:0};',
    'kabar:{on:1,to:"semua",snd:"lonceng"},event:{on:1,to:"semua",snd:"ding"},edit:1};')
rep("x.times=[...new Set(T)].sort().slice(0,8);x.time=x.times[0]});return c}\nconst tLbl=",
    "x.times=[...new Set(T)].sort().slice(0,8);x.time=x.times[0]});\n  if(n.editSet!==1)c.edit=1;/*V18: sebelum Owner memilih sendiri, perubahan promo ikut dikabari*/return c}\nconst tLbl=")
rep('const e=$("#nfedit");if(e)c.edit=e.checked?1:0;return c}', 'const e=$("#nfedit");if(e){c.edit=e.checked?1:0;c.editSet=1}return c}')

# ------------------------------------------------------------------ 4. Printer Bluetooth langsung dari aplikasi + 5. Pengaturan Website
JS = (pathlib.Path(__file__).parent / "patch_v18_app.js").read_text()
rep("/* ---------- Printer Bluetooth (Web Bluetooth, ESC/POS) ---------- */", JS + "\n/* ---------- Printer Bluetooth (Web Bluetooth, ESC/POS) ---------- */")
rep('  ["printer","print","Printer Bluetooth",()=>`${btOK()?"Tersambung":"Belum tersambung"} · kertas ${Number(C().paper)===48?"80":"58"} mm`],',
    '  ["printer","print","Printer Bluetooth",()=>`${NBT()?(btName()?"Printer: "+esc(btName()):"Belum memilih printer"):btOK()?"Tersambung":"Belum tersambung"} · kertas ${Number(C().paper)===48?"80":"58"} mm`],\n  ["web","mega","Website",()=>"Teks halaman website · ikut terbit otomatis"],')
rep('  if(id==="printer")return `<div class="btbox', '  if(id==="printer"&&NBT())return btSetHTML();\n  if(id==="web")return webSetHTML();\n  if(id==="printer")return `<div class="btbox')
rep('  ${isC(tx.pm)?`<div class="kemb">', '  ${(()=>{if(C().pauto&&NBT()&&btName())setTimeout(()=>btPrintTx(tx,true),400);return ""})()}${isC(tx.pm)?`<div class="kemb">')

rep('if(setSub&&!own()&&["tim","data","log","sinkron"].includes(setSub))setSub="";', 'if(setSub&&!own()&&["tim","data","log","sinkron","web"].includes(setSub))setSub="";')
rep('OWNF=["tim","data","log","sinkron"];', 'OWNF=["tim","data","log","sinkron","web"];')

rep('function hpDiag(st){const L=[],t=+st.last||0;', 'function hpDiag(st){const L=[],t=+st.last||0;/*V18*/if(st.push!=null)L.push(`<p class="hpstep">${st.push&&st.pushSub?"⚡ <b>Notifikasi instan aktif</b>: promo & diskon masuk beberapa detik setelah Owner menyimpan, walau aplikasi tertutup.":st.push?"⏳ Notifikasi instan sedang didaftarkan. Pastikan HP terhubung internet.":"Notifikasi instan belum dipasang di aplikasi ini. Saat aplikasi tertutup, promo masuk lewat cek otomatis (±15–30 menit)."}</p>`);')

P.write_text(s)
print("OK, perubahan 18 diterapkan.")
