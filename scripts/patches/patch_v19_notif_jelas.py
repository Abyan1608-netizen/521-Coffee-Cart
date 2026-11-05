"""Perubahan 19: notifikasi lebih jelas & HP Owner ikut menerima notifikasi promonya sendiri. Sekali jalan.
- HP yang menyimpan promo/diskon/kabar/kegiatan kini juga mendapat notifikasi HP (sebelumnya sengaja dilewati,
  sehingga Owner yang menguji dengan satu HP tidak pernah melihat notifikasinya).
- Atur → Notifikasi disusun ulang: bagian "Promo, diskon, kabar & kegiatan" di atas, "Pengingat stok (khusus tim)" di bawah,
  dengan penjelasan kapan tiap notifikasi muncul."""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V19-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:200]}")
    s = s.replace(old, new)

rep('const NFT=[["exp","Produk jadi hampir kedaluwarsa","Pengingat H-n sebelum kedaluwarsa, berisi tanggal produksi",1],\n  ["low","Stok bahan baku menipis","Daftar bahan di bawah batas minimum",1],',
    '/*V19-PATCH*/\nconst NFT=[["exp","Produk jadi hampir kedaluwarsa","Muncul hanya bila ada produk jadi yang akan kedaluwarsa (H-1/H-2/H-3), tepat pada jam pengingat. Tidak ada yang mau kedaluwarsa = tidak ada notifikasi.",1],\n  ["low","Stok bahan baku menipis","Muncul hanya bila ada bahan baku di bawah batas minimum, tepat pada jam pengingat.",1],')
rep('["promo","Promo","Promo tanpa potongan harga",0],["diskon","Diskon","Promo yang punya potongan harga",0],\n  ["kabar","Kabar terbaru","Berita & kabar toko",0],["event","Kegiatan","Kegiatan/event",0]];',
    '["promo","Promo","Promo tanpa potongan harga",0],["diskon","Diskon","Promo yang punya potongan harga",0],\n  ["kabar","Kabar terbaru","Berita & kabar toko",0],["event","Kegiatan","Kegiatan/event",0]];\nconst NFGRP=card=>`<h3 style="margin-top:20px">1 · Promo, diskon, kabar & kegiatan</h3><p class="note" style="margin-top:-4px">Dikirim ke HP tim & pelanggan <b>beberapa detik setelah Owner menyimpan</b> (walau aplikasi tertutup), termasuk ke HP Owner sendiri. Isi <b>Kirim juga pada jam</b> bila ingin diulang tiap hari pada jam tertentu selama promo masih berlaku.</p>${NFT.filter(x=>!x[3]).map(card).join("")}<h3 style="margin-top:24px">2 · Pengingat stok (khusus tim)</h3><p class="note" style="margin-top:-4px">Jam di bagian ini <b>hanya</b> untuk pengingat stok, bukan untuk promo.</p>${NFT.filter(x=>x[3]).map(card).join("")}`;')
rep('<p class="note" style="margin-top:0">Atur <b>kapan</b> dan <b>apa saja</b> yang dikirim sebagai notifikasi HP, <b>untuk siapa</b>, dan <b>suaranya</b>. Promo/diskon/kabar baru sampai ke HP yang memasang aplikasi dalam ±15–30 menit setelah disimpan (langsung saat aplikasi dibuka). Bisa juga dikirim tepat pada jam-jam pilihan, tiap hari selama masih berlaku (tanpa tanggal berakhir: maks. 7 hari).</p>',
    '<p class="note" style="margin-top:0">Notifikasi HP = pesan yang muncul di panel notifikasi (geser layar dari atas), seperti WhatsApp. Atur <b>apa saja</b> yang dikirim, <b>untuk siapa</b>, <b>jamnya</b>, dan <b>suaranya</b>.</p>')
rep('  ${NFT.map(([k,t,d,staffOnly])=>{const x=c[k];return `<div class="nfc',
    '  ${(()=>{const card=([k,t,d,staffOnly])=>{const x=c[k];return `<div class="nfc')
rep('${staffOnly?"":`<label class="fgck nfnow"><input type="checkbox" class="nfnowc" ${x.now!==0?"checked":""}><span>Kirim langsung saat diterbitkan</span></label>${nfTimesUI(x,1)}`}</div></div>`}).join("")}',
    '${staffOnly?"":`<label class="fgck nfnow"><input type="checkbox" class="nfnowc" ${x.now!==0?"checked":""}><span>Kirim langsung saat disimpan</span></label>${nfTimesUI(x,1)}`}</div></div>`};return NFGRP(card)})()}')
P.write_text(s)

# HP yang menyimpan juga menerima notifikasi
SH = pathlib.Path(__file__).resolve().parents[2] / "android-web/shim.js"
t = SH.read_text()
old = 'A.kabarSync(true); /* kabar yang diterbitkan HP ini tidak dikirim sebagai notifikasi ke HP ini sendiri */'
if old in t:
    t = t.replace(old, 'A.kabarSync(); /* HP yang menyimpan juga mendapat notifikasi HP, sama seperti HP lain (V19) */')
    SH.write_text(t)
print("OK, perubahan 19 diterapkan.")
