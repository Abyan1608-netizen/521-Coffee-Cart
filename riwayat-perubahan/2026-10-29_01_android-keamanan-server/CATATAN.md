# 01 · Aplikasi Android + perbaikan keamanan + server mini
**Tanggal:** 29 Oktober 2026

## Apa yang berubah
- Aplikasi web dibungkus jadi aplikasi Android (`android/`), dimuat dari dalam aplikasi, bukan dari internet.
- Keamanan: PIN di-hash PBKDF2, batas salah PIN, wajib ganti PIN awal, URL gambar disaring, CSP ketat, QR lokal, CSV aman, kode tim 10 karakter. Detail di `docs/LAPORAN-KEAMANAN.md`.
- Semua link/QR claude.ai → link Play Store `id.coffee521.pos`.
- Server mini Cloudflare (`server/`): Chat 521 lewat Claude API, sinkron antar-HP, terbit Kabar, kebijakan privasi.
- Optimasi: foto & font jadi file biner, minify, foto kembar disimpan sekali (buka ±2× lebih cepat, memori ±½).

## File/folder baru
`android/`, `android-web/`, `server/`, `play-store/`, `docs/`, `scripts/build_android.py`, `scripts/patches/patch_security.py`

## File yang diubah
`src/index.src.html` (lihat `perubahan-src.diff`), `assets/posqr.png` (QR baru ke Play Store), `README.md`

## Cara membatalkan
Kode asli ada di `asli/index.src.html`. Salin ke `src/index.src.html` lalu jalankan `python3 scripts/build.py`.
