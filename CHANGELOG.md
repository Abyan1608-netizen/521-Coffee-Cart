# Catatan perubahan 521 Coffee App
Terbaru di atas. Detail lengkap tiap perubahan ada di folder `riwayat-perubahan/`.

## 18b · 5 Nov 2026 · Firebase terpasang (notifikasi instan)
Proyek Firebase `coffee521` dibuat; konfigurasi aplikasi diisi di `android-web/config.json` → `fcm` (bukan rahasia). Versi 1.5.1. Notifikasi instan aktif setelah kunci server dipasang: `npx wrangler secret put FCM_SA < kunci.json` lalu `npx wrangler deploy`.

## 18 · 5 Nov 2026 · Final: notifikasi real-time, cetak struk Bluetooth, tema terang, website ikut aplikasi
Website ikut data Atur & Kabar di aplikasi (plus **Atur → Website**); tema terang jauh lebih kontras; perubahan promo ikut dikabari & notifikasi instan lewat Firebase (perlu dipasang sekali); cetak struk langsung ke printer thermal Bluetooth (cari printer otomatis, logo, cetak otomatis). Versi 1.5.0. **Perlu `npx wrangler deploy`.**
→ `riwayat-perubahan/2026-11-05_18_final-notif-struk-tampilan/`

## 17 · 4 Nov 2026 · Notifikasi promo tampil dengan pesannya
Promo/diskon/kabar baru selalu muncul sebagai notifikasi HP (judul + isi + suara), juga saat aplikasi terbuka; HP pelanggan yang terbuka ikut menerima dalam ±30 detik; Atur → Notifikasi → Cek punya tombol "Kirim notifikasi uji". Semua HP perlu memasang versi 1.4.1.
→ `riwayat-perubahan/2026-11-04_17_notifikasi-pesan-selalu-muncul/`

## 16 · 4 Nov 2026 · Simpan langsung terbit + jam notifikasi pelanggan
Tombol Terbitkan diganti Simpan (tidak tersangkut lagi); notifikasi promo/diskon kini sampai juga ke HP Owner/staf & saat aplikasi terbuka; promo/diskon/kabar/kegiatan bisa dikirim pada beberapa jam pilihan tiap hari.
→ `riwayat-perubahan/2026-11-04_16_simpan-otomatis-jam-notif-pelanggan/`

## 15 · 3 Nov 2026 · Tombol "Kirim ulang sekarang" dihapus
Pengiriman ke semua HP sudah otomatis.
→ `riwayat-perubahan/2026-11-03_15_hapus-tombol-kirim-ulang/`

## 14 · 3 Nov 2026 · Perbaikan tombol "Jadikan HP Owner"
Tombol pada peringatan di Langganan/Menu kini membuka Atur → Sinkron (kolom Kunci Owner).
→ `riwayat-perubahan/2026-11-03_14_tombol-jadikan-hp-owner/`

## 13 · 3 Nov 2026 · Link & QR Play Store dihapus
Tombol "QR kabar & promo", link di struk, dan tombol Download di web disembunyikan sampai aplikasi terbit di Play Store. Owner bisa mengisi link sendiri di Atur → Halaman publik.
→ `riwayat-perubahan/2026-11-03_13_hapus-link-qr-playstore/`

## 12 · 3 Nov 2026 · Web publik untuk link media sosial
Menu, promo & kabar bisa dibuka di browser tanpa download: `https://coffee521-api.coffee521.workers.dev/`. Selalu ikut data terbitan Owner, tanpa login/kasir. **Perlu `npx wrangler deploy`.**
→ `riwayat-perubahan/2026-11-03_12_web-publik-menu-promo/`

## 11 · 3 Nov 2026 · Jam pengingat ganda + jenis paket & Chat 521 sampai cepat
Kotak "Dari HP lain hari ini" dihapus; jam pengingat bisa banyak; perubahan dari HP Owner (jenis paket, Chat 521, menu, akun) sampai ke HP lain ±2 detik; jenis paket terlihat di HP kasir; peringatan owner tanpa Kunci Owner. **Perlu `npx wrangler deploy`.**
→ `riwayat-perubahan/2026-11-03_11_jam-pengingat-paket-sinkron-cepat/`

## 10 · 30 Okt 2026 · Masuk tanpa kode tim + stok sama di semua HP
Masuk dengan nama & PIN (tanpa kode), peran Owner/Barista/Reseller, stok bahan baku & botol sama di semua HP, penjualan masuk ke Owner walau HP Owner mati, tombol Cup/Botol tanpa ikon. **Perlu `npx wrangler deploy`, lalu perbarui HP Owner lebih dulu.**
→ `riwayat-perubahan/2026-10-30_10_akun-tanpa-kode-tim-stok-bersama/`

## 09 · 29 Okt 2026 · Suara dari WhatsApp lewat "Bagikan" + .opus
WhatsApp → tekan lama audio → Bagikan → 521 Coffee App → masuk ke Suara saya. Pesan suara WhatsApp (.opus) didukung.
→ `riwayat-perubahan/2026-10-29_09_bagikan-audio-whatsapp/`

## 08 · 29 Okt 2026 · Impor suara notifikasi dari HP
Atur → Notifikasi: impor MP3/OGG/M4A/AAC/WAV (maks 1,5 MB/20 dtk), terkirim ke semua HP saat terbit. **Perlu `npx wrangler deploy` sekali.**
→ `riwayat-perubahan/2026-10-29_08_impor-suara-notifikasi/`

## 07 · 29 Okt 2026 · Lupa PIN Owner + penjelasan ganti PIN
Atur ulang PIN Owner dengan Kunci Owner dari layar login; cegah Kunci Owner tertempel di Nama/PIN.
→ `riwayat-perubahan/2026-10-29_07_lupa-pin-owner/`

## 06 · 29 Okt 2026 · Perbaikan: aplikasi langsung tertutup
Tambah izin ACCESS_NETWORK_STATE (wajib Android 14+ untuk cek promo berkala) + pengaman agar fitur tambahan tidak bisa menutup aplikasi.
→ `riwayat-perubahan/2026-10-29_06_perbaikan-aplikasi-tertutup/`

## 05 · 29 Okt 2026 · Izin notifikasi + panduan pengaturan HP
Pelanggan ditawari notifikasi promo; panduan per merek (Xiaomi, OPPO, vivo, dll) yang membuka layar Autostart & Baterai; status di Atur → Notifikasi.
→ `riwayat-perubahan/2026-10-29_05_izin-notifikasi-pengaturan-hp/`

## 04 · 29 Okt 2026 · Kasir Cup | Botol, hapus stok, notifikasi & suara
Tab Cup/Botol di kasir, hapus batch/daftar stok, Atur → Notifikasi (kapan, apa, untuk siapa, suara), notifikasi promo/diskon/kabar untuk pelanggan, tanda BARU.
→ `riwayat-perubahan/2026-10-29_04_kasir-cup-botol-notifikasi-suara/`

## 03 · 29 Okt 2026 · Halaman Kabar lebih lancar
Scroll tidak patah-patah lagi (frame tersendat ±58% → ±9%), tampilan tetap sama.
→ `riwayat-perubahan/2026-10-29_03_kabar-lebih-lancar/`

## 02 · 29 Okt 2026 · Stok produk jadi + pengingat H-1 + Laporkan AI
Stok botol/gelas per batch dengan tanggal produksi & kedaluwarsa (FEFO), notifikasi H-1, panel "Laporkan AI".
→ `riwayat-perubahan/2026-10-29_02_stok-produk-jadi-notifikasi-laporkan-ai/`

## 01 · 29 Okt 2026 · Aplikasi Android + keamanan + server
Versi Android siap Play Store, perbaikan keamanan PIN/XSS, server Chat 521 & sinkron.
→ `riwayat-perubahan/2026-10-29_01_android-keamanan-server/`
