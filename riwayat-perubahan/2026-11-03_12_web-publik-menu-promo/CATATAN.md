# 12 · Versi web publik: menu, promo & kabar tanpa download aplikasi
**Tanggal:** 3 November 2026 · **Diminta oleh:** Raihan

## Apa yang berubah
- **Halaman web publik** di alamat server: `https://coffee521-api.coffee521.workers.dev/`. Link ini bisa ditaruh di bio Instagram/TikTok, WhatsApp, atau QR. Pelanggan langsung melihat menu & harga, promo, diskon, kabar, jam buka, lokasi, kontak, dan tombol Pesan sekarang, tanpa download.
- **Selalu terbaru:** isinya diambil dari data yang diterbitkan HP Owner (sama dengan aplikasi). Begitu Owner menerbitkan, web ikut berubah (maks. ±20 detik).
- **Aman:** di web tidak ada login, kasir, stok, data penjualan, akun, atau QRIS. Data tim tidak ikut dikirim ke web.
- Tombol **Download aplikasi** (atas & bawah halaman). Tujuan tombol diatur di `android-web/config.json` → `web_app_link` (kosongkan untuk menyembunyikan).
- Halaman GitHub Pages lama (`index.html` di repo) kini mengarah ke web publik ini.
- Aplikasi Android versi 1.3.0 (kode web sama; mode web hanya aktif di halaman web).

## File yang diubah / baru
- `src/index.src.html` (`perubahan-src.diff`; skrip `scripts/patches/patch_v12_web_publik.py`)
- `scripts/build_web.py` (baru) → menghasilkan `server/web/` (dipanggil otomatis oleh `build_android.py`)
- `server/src/index.js` (`/kdata.js`), `server/wrangler.toml` (`[assets]` → folder `web`) (`perubahan-lain.diff`)
- `android-web/config.json`: `web_app_link`

## Wajib
`cd server` lalu `npx wrangler deploy`. Setelah itu buka `https://coffee521-api.coffee521.workers.dev/` di HP.

## Uji otomatis (lulus)
`uji-web.js`: promo yang baru diterbitkan langsung tampil; tidak ada tombol Masuk; membuka `#masuk` atau memaksa layar login tetap di halaman publik; tombol Pesan sekarang berjalan; tidak ada error CSP/konsol. Uji aplikasi (perubahan 10 & 11) diulang dan tetap lulus.
