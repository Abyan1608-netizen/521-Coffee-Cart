# Catatan perubahan 521 Coffee App
Terbaru di atas. Detail lengkap tiap perubahan ada di folder `riwayat-perubahan/`.

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
