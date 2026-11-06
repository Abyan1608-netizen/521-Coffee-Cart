# 22 · Aplikasi khusus tim: langsung ke layar Masuk, pelanggan memakai website
**Tanggal:** 6 November 2026 · **Diminta oleh:** Raihan: "aplikasi difokuskan hanya untuk owner dan kasir… ketika pencet aplikasi itu langsung ke halaman login". Notifikasi promo & kabar: "diadakan tombol on off saja". APK baru dipakai Raihan & Urwah, belum ada pelanggan yang memasangnya.

## Apa yang berubah

### Aplikasi dibuka → langsung layar Masuk
- Tidak ada lagi halaman Kabar/website di awal. Kalau masih dalam sesi masuk, langsung ke kasir.
- Tombol "← Kabar & promo" di layar Masuk dihapus.
- Tombol kembali (back) di layar Masuk menutup aplikasi.
- Tab Kabar berjudul **"Kabar website"**. Di tab ini Owner mengelola promo, kegiatan, kabar, dan headline untuk website. Tombol **Lihat di website** tetap ada.
- Website yang dibuka dari aplikasi hanya punya tombol **← Kembali ke aplikasi**; tombol Masuk sudah tidak ada.
- Tanpa internet, "Lihat di website" tidak berpindah halaman, cukup muncul pesan "Website tidak bisa dibuka. Periksa koneksi internet." Halaman Kabar lama di aplikasi tidak dipakai lagi.
- Notifikasi kabar diketuk saat belum masuk: membuka website.

### Notifikasi promo & kabar: satu tombol on/off
- **Atur → Notifikasi → bagian 1** punya tombol **Notifikasi promo & kabar**.
  - **Mati:** promo, diskon, kabar, dan kegiatan tidak dikirim ke HP tim mana pun.
  - **Nyala:** keempatnya aktif lagi.
  - Langsung tersimpan dan berlaku di semua HP tim.
- Pengingat stok (produk jadi kedaluwarsa, bahan menipis) tidak terpengaruh.
- Pilihan "Untuk: Staf / Pelanggan / Semua" untuk promo dihapus karena penerimanya hanya HP tim.

### Alamat server lama
- `coffee521-api.coffee521.workers.dev` (link web lama di media sosial) kini langsung dialihkan ke website 521. **Berlaku setelah `npx wrangler deploy`.**
- Alamat website diatur di `android-web/config.json` → `"website"`.

### Teks
"Halaman pelanggan" pada pesan simpan/terbit diganti "website".

### Versi
1.8.0 (15).

## File yang diubah
- `src/index.src.html`, via `scripts/patches/patch_v22_khusus_tim.py`.
- `android-web/shim.js`: tombol kembali di layar Masuk.
- `android/.../MainActivity.java`: tombol di website "← Kembali ke aplikasi".
- `scripts/build_web.py` + `android-web/config.json` (`website`): halaman utama server dialihkan.
- `android/app/build.gradle.kts`: versi.

## Uji (lulus): `uji-v22.js`
Uji ini mencakup semua langkah uji 21, ditambah:
1. Aplikasi dibuka:
   - langsung layar Masuk, tidak dialihkan;
   - tombol "← Kabar & promo" tidak ada;
   - tombol kembali = keluar.
2. Notifikasi kabar diketuk saat belum masuk → website, dengan tombol "← Kembali ke aplikasi".
3. Website gagal dibuka → layar Masuk + pesan.
4. Judul tab "Kabar website".
5. Tanpa internet → "Lihat di website" tetap di kasir + pesan.
6. Tombol on/off notifikasi promo & kabar:
   - pilihan "Untuk" hilang;
   - **Mati** → empat jenis mati, pengingat stok tetap, tersimpan setelah dibuka ulang, terbit ke server;
   - **Nyala** → keempatnya aktif lagi.
7. Alamat server lama → dialihkan ke website.

Uji perubahan 20, 18, 17, 16, 14, 11, 10, offline, dan 13 diulang. Pemeriksaan halaman Kabar lama di aplikasi dan web lama di server sudah tidak berlaku, karena keduanya memang sudah tidak dipakai.
