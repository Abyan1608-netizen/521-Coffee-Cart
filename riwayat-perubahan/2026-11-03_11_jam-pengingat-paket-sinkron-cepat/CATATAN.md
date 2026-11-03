# 11 · Jam pengingat lebih dari satu, jenis paket & Chat 521 sampai cepat, perbaikan
**Tanggal:** 3 November 2026 · **Diminta oleh:** Raihan

## Apa yang berubah
- **Ringkasan:** kotak "Dari HP lain hari ini" dihapus (penjualan HP lain sudah masuk otomatis). Yang tersisa hanya tanda kecil bila ada transaksi yang masih menunggu internet.
- **Atur → Notifikasi:** jam pengingat bisa lebih dari satu (mis. 08.00, 10.00, 12.00, 15.00), maks. 8 jam, untuk "Produk jadi hampir kedaluwarsa" dan "Stok bahan baku menipis". Jam yang terlewat saat HP mati hanya dikirim satu kali (yang terakhir), tidak menumpuk.
- **Sinkron cepat:** begitu HP Owner menerbitkan perubahan (jenis paket, menu, akun, Chat 521 nyala/mati, pengaturan notifikasi), HP tim lain langsung mengambilnya dalam ±1–3 detik tanpa memuat ulang aplikasi. Sebelumnya bisa sampai ±5 menit.
- **Chat 521 nyala/mati** dari HP Owner langsung terbit ke semua HP (dulu menunggu tombol Terbitkan di Kabar).
- **Langganan di HP kasir:** daftar jenis paket kini terlihat oleh semua akun. Bila akun belum boleh menjual paket, muncul petunjuk: Owner menyalakan **Jual paket langganan** di Atur → Tim & PIN.
- **Owner di HP tanpa Kunci Owner** mendapat peringatan di Atur, Menu, dan Jenis paket: perubahan dari HP itu hanya tersimpan di HP itu (sebab jenis paket dari "HP owner lain" tidak sampai).
- **Perbaikan:** HP anggota lain tersambung lagi lebih andal setelah ada anggota yang dihapus; judul pengingat "N hari lagi" kini sesuai; server menolak data berlebihan (pengaman).

## Penyebab bug yang dilaporkan
- Jenis paket lambat: HP lain hanya mengecek data terbitan tiap ±5 menit dan baru memakainya setelah aplikasi dimuat ulang. Sekarang HP Owner memberi tahu HP lain saat itu juga.
- Jenis paket tidak muncul di HP kasir: daftar jenis paket hanya tampil untuk akun yang boleh mengatur paket, dan tombol "Jual paket" hanya untuk akun yang boleh menjual paket. Itu soal hak akses, bukan data hilang.

## File yang diubah
`src/index.src.html` (`perubahan-src.diff`; skrip `scripts/patches/patch_v11_jam_paket_sinkron_cepat.py`), `android-web/shim.js`, `server/src/index.js` (`perubahan-lain.diff`), versi 1.2.0 (versionCode 3).

## Wajib setelah pembaruan
`cd server` lalu `npx wrangler deploy` (pengaman server baru). Lalu pasang APK baru di semua HP, HP Owner lebih dulu.

## Uji otomatis (lulus)
`uji-v11.js`: kotak hilang; jenis paket sampai ke HP kasir & owner kedua ±2 dtk; HP kasir melihat jenis paket + petunjuk izin; peringatan owner tanpa Kunci Owner; Chat 521 mati di HP kasir ±1 dtk; 3 jam pengingat tersimpan, ikut ke HP kasir, dan terjadwal 3 notifikasi per batch. Uji perubahan 10 (`uji-banyak-hp.js`, 28 pemeriksaan) diulang dan tetap lulus.
