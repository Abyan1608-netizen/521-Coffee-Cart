# 21 · Kabar pelanggan = website, headline & kartu menu website diatur dari aplikasi
**Tanggal:** 6 November 2026 · **Diminta oleh:** Raihan, meneruskan masukan Bang Urwah (WhatsApp, 5 Nov):
- "fitur kabar di apk di apus aja disamain aja sama website tampilannya, soalnya tujuan fitur kabar kan bisa diliat tanpa download app"
- "fitur headline hilang jadi ga ada pengaturannya, gabisa dirubah headlinenya" (misalnya untuk ramein final LIPIA)
- kartu menu website ("KOPI SUSU · 170 ML"): "ini blm bisa di setting juga", "kan ngeri klo salah asumsi"

## Apa yang berubah

### Halaman Kabar pelanggan di aplikasi = website
- Aplikasi dibuka **tanpa login** langsung menampilkan **website 521** di dalam aplikasi. Halaman Kabar lama untuk pelanggan tidak dipakai lagi.
- Di website ada tombol putih kecil di kiri bawah:
  - **Masuk** membuka layar login aplikasi;
  - **← Kembali ke kasir** muncul bila dibuka dari "Lihat di website" (sudah login), langsung kembali tanpa login ulang.
- Tab **Kabar** (Owner) tetap menjadi tempat menambah dan mengubah promo, kegiatan, dan kabar.
  - Keterangannya kini "tampil di website 521".
  - Tombol "Lihat sebagai pelanggan" diganti **"Lihat di website"**.
- Tautan di website (WhatsApp, Maps, GoFood, Instagram, dll.) dibuka di aplikasinya masing-masing. Website tidak bisa memakai fitur kasir: jembatan aplikasi hanya untuk halaman aplikasi sendiri.
- **Tanpa internet:** halaman Kabar yang tersimpan di aplikasi tetap tampil.
- Notifikasi promo diketuk saat belum login: membuka website. Pengingat stok: membuka aplikasi.

### Headline Kabar website
Headline = kartu paling besar dan paling atas di bagian Kabar website. Diatur di dua tempat:
- **Atur → Website → Headline Kabar.** Pilihannya:
  - "Otomatis: kabar terbaru yang masih berlaku";
  - promo/kegiatan/kabar tertentu;
  - "Tanpa headline".
- **Tab Kabar → buka promo/kabar → "Headline website?" → Jadikan headline / Tidak.**
- Selama Owner belum memilih di aplikasi, headline yang sekarang tampil tetap dipakai. Saat ini headline-nya "521 bareng Kak Mikayla", pilihan lama dari editor website.

### Kartu menu website
**Atur → Website → Kartu menu** menampilkan setiap menu aktif.
- **Keterangan kecil** di bawah nama:
  - otomatis = **Kategori · Ukuran cup** dari Buku resep;
  - bisa ditulis sendiri;
  - bisa diatur **Tanpa keterangan**.
  - Baris "Tampil: …" menunjukkan persis apa yang akan muncul di website.
- **Foto kartu:** pilih dari galeri/kamera; foto otomatis diperkecil. Tombol "Pakai foto bawaan website" mengembalikan foto bawaan.
- Nama, harga, deskripsi, dan status habis tetap otomatis ikut menu di kasir.
- **Website tidak lagi menebak:** dulu kategori, ukuran, atau deskripsi yang kosong di aplikasi diam-diam memakai isi lama website. Sekarang selalu persis dari aplikasi (repo website, `tools/patch_sinkron_aplikasi.py` v3).

### Versi
1.7.0 (14).

## File yang diubah
- `src/index.src.html`, via `scripts/patches/patch_v21_web_kabar.py` + `patch_v21_app.js`.
- `android/.../MainActivity.java`:
  - website dibuka di dalam aplikasi;
  - tombol Masuk / Kembali ke kasir;
  - warna bilah HP mengikuti website;
  - cadangan saat luring;
  - notifikasi stok & suara impor tetap ke aplikasi.
- `android/app/build.gradle.kts`: versi 1.7.0 (14).
- Repo website `521-Coffee-Cart-Web`: `tools/patch_sinkron_aplikasi.py` (v3).

## Uji (lulus): `uji-v21.js`
Uji memakai website lokal + server lokal, dengan alamat website & server asli dialihkan.
1. Aplikasi tanpa login → website tampil; tombol Masuk tampil.
2. Tanpa internet → halaman Kabar aplikasi tampil.
3. Masuk → login Owner (tidak dialihkan ke website).
4. Promo baru + "Jadikan headline" → tersimpan sebagai headline; isian tidak hilang.
5. Atur → Website:
   - pilihan headline sesuai;
   - semua menu tampil;
   - keterangan otomatis = kategori · ukuran;
   - pratinjau "Tampil:" ikut berubah;
   - Tanpa keterangan;
   - foto dipilih & diperkecil.
6. Terbit ke server:
   - keterangan, foto (file media, bukan base64), dan headline ikut terbit;
   - menu yang tidak diubah tetap otomatis.
7. Website menampilkan persis:
   - kartu 1 keterangan & foto dari aplikasi;
   - kartu 2 tanpa keterangan;
   - kartu 3 = kategori · ukuran;
   - headline = promo tadi.
8. Headline diganti "Otomatis" → tersimpan, pengaturan kartu menu tetap ada; simpan ulang tanpa mengubah pilihan → tetap.
9. "Lihat di website" (sudah login) → tombol "Kembali ke kasir" → kembali tanpa login ulang.

Uji perubahan 20, 18, 17, 16, 14, 11, 10, web, offline, dan 13 diulang. Uji lama yang memeriksa halaman Kabar lama dijalankan dalam mode tanpa internet (`#luring`), karena di mode itu halaman lama masih dipakai.

**Bagian Android (membuka website di dalam aplikasi, tombol Masuk) diuji lewat versi browser yang sama logikanya. Mohon dicoba langsung di HP setelah update.**
