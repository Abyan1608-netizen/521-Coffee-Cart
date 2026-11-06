# 23 · Repo aplikasi private, link unduh APK lewat Google Drive
**Tanggal:** 6 November 2026 · **Diminta oleh:** Raihan: "saya ingin membuat private repo aplikasi… untuk link download bisa kita pindahkan dengan cara lain". Pilihan link: **Google Drive**. Penguatan PIN: tidak.

## Apa yang berubah
- Repo `521-Coffee-Cart` dijadikan **private**:
  - kode aplikasi, data contoh, dan APK tidak bisa lagi dilihat atau diunduh orang di luar;
  - GitHub Actions tetap membangun APK setiap push dan menyimpannya di Releases (perlu login GitHub).
- **Atur → Sinkron semua HP** (HP Owner) punya kolom **Link unduh aplikasi (APK)**:
  - tempel link Google Drive file APK;
  - **Bagikan cara masuk ke tim** memakai link itu;
  - link hanya tersimpan di HP Owner tersebut, tidak ikut terbit ke website;
  - tanpa link, teksnya "Minta file aplikasi 521 Coffee App (APK) ke Owner".
  Link GitHub lama sudah dihapus dari aplikasi.
- README & catatan workflow diperbarui.
- Versi 1.8.1 (16).

## Cara membagikan versi baru (link Drive tetap sama)
1. Saya taruh file APK terbaru di Mac: `Projek 521/521-coffee-app/APK/`.
2. **Pertama kali:** unggah ke Google Drive → Bagikan → "Siapa saja yang memiliki link" → salin link → tempel di aplikasi (Atur → Sinkron semua HP).
3. **Versi berikutnya:** di Google Drive klik kanan file APK → **Informasi file → Kelola versi → Upload versi baru**. Linknya tetap sama, tim cukup membuka link lama.

## Uji (lulus): `uji-v23.js`
- Kolom link ada.
- Tanpa link → teks meminta APK ke Owner, tanpa link GitHub.
- Link tanpa https ditolak.
- Dengan link → teks berisi link Drive.
- Link tersimpan di HP ini dan tidak ikut data website.

Uji 22 (48 cek) dan uji 20 (33 cek) diulang dan tetap lulus.
