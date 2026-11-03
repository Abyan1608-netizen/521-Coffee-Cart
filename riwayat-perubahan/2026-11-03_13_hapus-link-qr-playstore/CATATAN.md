# 13 · Link & QR Play Store dihapus (aplikasi belum terbit di Play Store)
**Tanggal:** 3 November 2026 · **Diminta oleh:** Raihan

## Apa yang berubah
- **Aplikasi:** link Play Store tidak lagi dipasang otomatis. Akibatnya tombol **"QR kabar & promo"** di kasir dan baris "Promo & kegiatan terbaru: …" di struk WhatsApp hilang. HP yang sudah memakai link Play Store dibersihkan otomatis sekali saat update.
- Owner tetap bisa mengisi link sendiri kapan saja di **Atur → Halaman publik → Link halaman** (mis. link web publik). Bila diisi, tombol QR & baris di struk muncul lagi.
- **Bagikan cara masuk ke tim** (Atur → Sinkron) kini memakai link APK GitHub.
- **Web publik:** tombol "Download aplikasi" disembunyikan (`android-web/config.json` → `web_app_link` kosong). Isi lagi dengan link Play Store setelah aplikasi terbit.
- Versi 1.3.1 (versionCode 5).

## File yang diubah
`src/index.src.html` (`perubahan-src.diff`; skrip `scripts/patches/patch_v13_tanpa_link_playstore.py`), `android-web/config.json`, `server/web/` (dirakit ulang).

## Wajib
`cd server` lalu `npx wrangler deploy` (agar tombol download di web hilang).

## Uji otomatis (lulus)
`uji-v13.js`: data lama berisi link Play Store → kosong setelah update; tombol QR di kasir hilang; struk tanpa link; link buatan Owner tetap berfungsi; web tanpa tombol download & tanpa tombol Masuk.
