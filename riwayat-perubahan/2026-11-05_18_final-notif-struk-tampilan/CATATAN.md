# 18 · Final: notifikasi real-time, cetak struk Bluetooth, tampilan terang, website ikut aplikasi
**Tanggal:** 5 November 2026 · **Diminta oleh:** Raihan — "Notif, fitur struk dan interface. Go final."

## 1. Website ikut menu Atur di aplikasi
Website baru (`521-Coffee-Cart-Web`, desain dari Raihan) sekarang mengambil data langsung dari server aplikasi setiap dibuka dan tiap 1 menit:
- **Data toko:** nama, lokasi, jam & jadwal buka, WhatsApp, Instagram, Maps.
- **Menu:** harga, deskripsi, menu baru. Menu yang ditandai **Habis** di kasir tidak bisa dipesan di website.
- **Kabar:** promo, diskon, kegiatan, kabar (draf tidak tampil), dan testimoni.
- **Pesan:** reseller dan link ShopeeFood/GoFood/GrabFood. Nomor WA yang tidak valid disembunyikan.
- **Teks website:** menu baru **Atur → Website** (khusus Owner) untuk mengatur teks khusus website, yaitu judul tampilan awal, pita teks, Cerita, judul Menu/Kabar/Testimoni, teks Lokasi & kaki halaman, serta tampil/sembunyikan bagian.

Desain dan foto website tetap dari Raihan. Bila server tidak bisa dihubungi, isi bawaan website yang tampil. **Syarat:** server sudah di-deploy (`npx wrangler deploy`).

## 2. Tema terang lebih kontras
- **Teks:** teks abu-abu dibuat lebih gelap. Label menu bawah tadinya 3,1:1, sekarang 6:1 atau lebih.
- **Kartu:** kartu dibuat putih bersih dengan garis & bayangan tipis. Latar oranye pucat diredam, dan efek kaca terang tidak lagi tembus pandang.
- **Hasil audit otomatis:** 147 teks berkontras rendah turun menjadi 0 di semua layar utama (sisanya hanya animasi pembuka). Label menu bawah di tema gelap juga dipertajam.

## 3. Notifikasi promo/diskon real-time
- **Perubahan ikut dikabari:** promo/diskon/kabar yang **diubah** sekarang ikut dikabari secara bawaan, tidak hanya yang baru. Owner bisa mematikannya di Atur → Notifikasi.
- **Notifikasi instan (Firebase):** server mengirim colekan ke semua HP begitu Owner menyimpan promo, sehingga notifikasi masuk beberapa detik walau aplikasi tertutup. Aktif setelah Firebase dipasang (lihat `docs/PANDUAN-NOTIFIKASI-INSTAN.md`). Tanpa Firebase, perilakunya tetap seperti versi 1.4.1.
- **Cek notifikasi:** Atur → Notifikasi → Cek menampilkan status notifikasi instan.

## 4. Cetak struk lewat printer Bluetooth
- **Menyambung printer:** Atur → Printer Bluetooth → **Cari printer**. Aplikasi meminta izin, Bluetooth dinyalakan lewat dialog Android, lalu printer langsung dicari. Printer tampil paling atas. Ketuk nama printer, maka aplikasi tersambung dan mencetak struk tes.
- **Mencetak:** tombol **Printer** di layar Lunas langsung mencetak. Bila belum ada printer, lembar pilih printer terbuka, lalu struk itu langsung dicetak setelah memilih.
- **Isi struk:** logo 521, nama toko besar, TOTAL tebal, dan potong kertas (kertas 58/80 mm).
- **Pilihan:** cetak logo dan **cetak otomatis setelah bayar**.
- **Jenis printer:** mendukung printer Bluetooth klasik (SPP, kebanyakan printer thermal) dan BLE. Bila printer mati, muncul pesan yang jelas dan struk tersalin untuk aplikasi printer.

## 5. Lain-lain
- Kotak "Dari HP lain hari ini" tidak tampil lagi di HP Owner.
- Versi 1.5.0 (versionCode 10).

## File
- **Kode aplikasi:**
  - `src/index.src.html`, diubah lewat `scripts/patches/patch_v18_final.py` dan `patch_v18_app.js`;
  - `android-web/shim.js`;
  - `BtPrinter.java` (baru), `PushService.java` (baru);
  - `MainActivity.java`, `KabarJob.java`, `HpSettings.java`;
  - `AndroidManifest.xml`, `build.gradle.kts`, `scripts/build_android.py`.
- **Server:** `server/src/index.js` (colekan Firebase, `/push`).
- **Dokumen:** `docs/PANDUAN-NOTIFIKASI-INSTAN.md`, `docs/LAPORAN-KEAMANAN.md`.
- **Website:** repo `521-Coffee-Cart-Web`, `tools/patch_sinkron_aplikasi.py`.

## Uji
- **`uji-v18.js` (aplikasi):**
  - cari printer, urutan printer, cetak tes, dan isi byte ESC/POS (reset, logo, nama besar, potong);
  - cetak struk penjualan, lebar baris 58/80 mm, dan cetak otomatis;
  - printer mati, lupakan printer, dan lembar pilih printer;
  - Atur → Website terbit ke server;
  - notifikasi perubahan dan status notifikasi instan;
  - kotak HP lain hilang.
- **`uji-server-v18.mjs`:** JWT Firebase ditandatangani benar, dikirim ke topik yang tepat, isi promo tidak dikirim, dan tidak ada colekan untuk perubahan menu atau draf.
- **`uji-website-v18.js`:** harga/menu/Habis/promo/lokasi/WA/reseller/teks website ikut aplikasi, serta tidak menggambar ulang bila tidak ada perubahan atau saat panel Pesan terbuka.
- **Kontras:** audit kontras tema terang.
- **Regresi:** uji perubahan 10, 11, 14, 16, 17, web, offline, dan 13 diulang.
- **Kode Android:** dikompilasi di GitHub Actions.
- **Belum bisa diuji di sini:** printer sungguhan dan Firebase sungguhan. Logikanya sudah diuji dengan tiruan.
