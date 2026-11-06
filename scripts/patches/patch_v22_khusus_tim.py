"""Perubahan 22: aplikasi khusus tim (Owner, barista, reseller). Pelanggan memakai website 521.
1. Aplikasi dibuka → langsung layar Masuk (atau langsung kasir bila masih masuk). Tidak ada lagi halaman Kabar di awal,
   tombol "← Kabar & promo" di layar Masuk dihapus, tombol kembali di layar Masuk menutup aplikasi.
2. Website tanpa internet: tetap di aplikasi + pesan "Website tidak bisa dibuka".
3. Atur → Notifikasi: satu tombol on/off "Notifikasi promo & kabar" untuk semua HP tim (promo, diskon, kabar, kegiatan).
   Pilihan "Untuk: Staf/Pelanggan/Semua" untuk promo dihapus (semua HP tim menerima).
Sekali jalan."""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parents[1] / "src/index.src.html"
s = P.read_text()
if "/*V22-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


# 1. langsung ke layar Masuk (versi web publik di server tetap seperti dulu)
rep("else{showPub();welcome()}",
    "else showLogin();/*V22-PATCH*/\nif(location.hash===\"#luring\")setTimeout(()=>toast(\"Website tidak bisa dibuka. Periksa koneksi internet.\",1),700);")
rep('    <button class="back" data-a="tokabar">← Kabar & promo</button>\n', "")
# website hanya dibuka saat ada internet; tanpa internet tetap di aplikasi (halaman Kabar lama tidak dipakai lagi)
rep('function showPub(){/*V21-PATCH*/if(!WEB&&window.A521&&A521.native&&navigator.onLine!==false&&location.hash!=="#luring"&&typeof WEB_URL==="string"){'
    '$("#m").hidden=true;try{location.replace(WEB_URL+(me?"?dari=kasir":""));return}catch(e){}}',
    'function showPub(){/*V21-PATCH*/if(!WEB&&typeof WEB_URL==="string"){if(navigator.onLine===false){toast("Website tidak bisa dibuka. Periksa koneksi internet.",1);return}'
    '$("#m").hidden=true;try{location.replace(WEB_URL+(me?"?dari=kasir":""));return}catch(e){}}')
rep("<h2>Kabar & promo</h2>", "<h2>Kabar website</h2>")

# 3. notifikasi promo & kabar: satu tombol on/off untuk semua HP tim
rep("${NFT.filter(x=>!x[3]).map(card).join(\"\")}<h3 style=\"margin-top:24px\">2",
    "${(()=>{const on=NFT.filter(x=>!x[3]).some(x=>card.c&&card.c[x[0]].on);return `<div class=\"swrow nfmaster\"><span><b>Notifikasi promo & kabar</b><small>${on?\"Aktif di semua HP tim\":\"Mati di semua HP tim\"}</small></span>"
    "<label class=\"tgl\" aria-label=\"Notifikasi promo & kabar\"><input type=\"checkbox\" id=\"nfpromo\"${on?\" checked\":\"\"}><span></span></label></div>"
    "<div id=\"nfpg\"${on?\"\":\" hidden\"}>${NFT.filter(x=>!x[3]).map(card).join(\"\")}</div>`})()}<h3 style=\"margin-top:24px\">2")
rep("Dikirim ke HP tim & pelanggan", "Dikirim ke semua HP tim")
rep("return NFGRP(card)})()}", "card.c=c;return NFGRP(card)})()}")
rep('`<label>Untuk<select class="nfto">${TO.map(([v,l])=>`<option value="${v}"${x.to===v?" selected":""}>${l}</option>`).join("")}</select></label>`', '""')
rep('const to=el.querySelector(".nfto");if(to&&!to.disabled)x.to=to.value;',
    'const to=el.querySelector(".nfto");if(to&&!to.disabled)x.to=to.value;'
    'if(!["exp","low"].includes(k)){x.to="semua";const mo=$("#nfpromo");if(mo&&!mo.checked)x.on=0}')
rep("Langsung berlaku untuk semua HP tim & pelanggan.", "Langsung berlaku untuk semua HP tim.")
rep("Agar sampai ke pelanggan & HP lain, ubah dari HP Owner.", "Agar sampai ke HP lain, ubah dari HP Owner.")
rep("/* ---------- Printer Bluetooth (Web Bluetooth, ESC/POS) ---------- */",
    """/* V22: tombol on/off notifikasi promo & kabar (langsung tersimpan untuk semua HP tim) */
document.addEventListener("change",e=>{const t=e.target;if(!t||t.id!=="nfpromo")return;const g=$("#nfpg");if(g)g.hidden=!t.checked;
  if(t.checked&&g&&![...g.querySelectorAll(".nfon")].some(x=>x.checked))g.querySelectorAll(".nfon").forEach(x=>{x.checked=true;const c=x.closest(".nfc");if(c)c.classList.remove("off")});
  const sm=t.closest(".nfmaster")&&t.closest(".nfmaster").querySelector("small");if(sm)sm.textContent=t.checked?"Aktif di semua HP tim":"Mati di semua HP tim";
  if(can("set"))nfSave()},true);
/* ---------- Printer Bluetooth (Web Bluetooth, ESC/POS) ---------- */""")
rep("\n</style>\n", "\n.nfmaster{margin:6px 0 12px;padding:14px;border:1px solid var(--line);border-radius:16px;background:var(--sf)}.nfmaster small{display:block;color:var(--mute);font-size:13px}\n</style>\n")

# 4. teks: "halaman pelanggan" kini = website 521
for a, b in [("Tersimpan ✓ Langsung terlihat di semua HP & pelanggan.", "Tersimpan ✓ Langsung terlihat di semua HP & website."),
             ("Menyimpan ke semua HP & pelanggan…", "Menyimpan ke semua HP & website…"),
             ("✓ Semua tersimpan & terlihat pelanggan", "✓ Semua tersimpan & terlihat di website"),
             ("● Tersimpan di HP ini, belum terlihat pelanggan", "● Tersimpan di HP ini, belum terlihat di website"),
             ("Tersimpan ✓ Pelanggan sudah bisa melihatnya.", "Tersimpan ✓ Sudah terlihat di website."),
             ("Belum terkirim ke pelanggan (cek internet)", "Belum terkirim ke website (cek internet)"),
             ("Agar terlihat pelanggan, ubah dari HP Owner.", "Agar terlihat di website, ubah dari HP Owner."),
             ("Semua HP tim & halaman pelanggan sudah diperbarui", "Semua HP tim & website sudah diperbarui"),
             ("Menu di halaman pelanggan sudah ikut diperbarui", "Menu di website sudah ikut diperbarui"),
             ("Tampil di halaman pelanggan?", "Tampil di website?"),
             ("tersimpan di Kabar → berlaku di semua HP & pelanggan", "tersimpan di Kabar → berlaku di semua HP tim"),
             ("Atur <b>apa saja</b> yang dikirim, <b>untuk siapa</b>, <b>jamnya</b>, dan <b>suaranya</b>.", "Atur <b>apa saja</b> yang dikirim, <b>jamnya</b>, dan <b>suaranya</b>.")]:
    rep(a, b)
s = s.replace("dari halaman pelanggan", "dari website")

P.write_text(s)
print("OK, perubahan 22 diterapkan.")
