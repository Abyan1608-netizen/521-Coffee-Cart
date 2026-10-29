# 521 Coffee App: Android (Play Store) + Web

📲 **Unduh APK uji (Android):** [521-Coffee-App.apk](https://github.com/Abyan1608-netizen/521-Coffee-Cart/releases/latest/download/521-Coffee-App.apk)
· semua versi di [Releases](https://github.com/Abyan1608-netizen/521-Coffee-Cart/releases) (dibangun otomatis oleh GitHub Actions setiap push ke `main`).

🌐 **Versi web:** `index.html` di folder utama (GitHub Pages).

**Mulai dari sini:** `docs/PANDUAN-RILIS.md` (langkah rilis), `docs/LAPORAN-KEAMANAN.md` (audit keamanan), `CHANGELOG.md` (daftar perubahan).

## Struktur baru
| Folder / file | Isi |
|---|---|
| `android/` | Proyek Android Studio (Java, 1 Activity + WebView, hanya dependensi `androidx.webkit`). Buka folder ini di Android Studio. |
| `android/app/src/main/assets/www/` | Hasil `scripts/build_android.py`: web yang sudah diringkas (jangan diedit langsung). |
| `android-web/` | Lapisan Android untuk web: `shim.js` (sinkron, terbit Kabar, Chat 521, simpan file, tombol kembali), QR lokal, `config.json` (alamat server). |
| `server/` | Server mini Cloudflare Worker: proxy Claude API + sinkron + kebijakan privasi (`/privacy`). |
| `play-store/` | Ikon 512, gambar fitur 1024×500, 4 tangkapan layar 1080×1920. |
| `scripts/build_android.py` | Merakit versi Android: foto/font jadi file biner, minify JS/CSS, CSP, QR lokal. |
| `scripts/patches/` | Skrip patch yang sudah diterapkan ke `src/` (catatan teknis, tidak perlu dijalankan lagi). |
| `scripts/catat_perubahan.py` | Membuat folder catatan untuk perubahan baru. |
| `riwayat-perubahan/` | **Satu folder per perubahan**: catatan, diff kode, salinan file. |
| `docs/` | Panduan rilis & laporan keamanan. |
| `CHANGELOG.md` | Ringkasan semua perubahan, terbaru di atas. |

## Perintah cepat
```
python3 scripts/build_android.py   # setelah mengubah src/ data/ android-web/
python3 scripts/build.py           # versi web (Artifact) seperti sebelumnya
cd server && npx wrangler deploy   # perbarui server
```

## Hasil optimasi (tanpa mengubah kualitas foto: byte JPEG asli)
| | Sebelum | Sesudah |
|---|---|---|
| File yang di-parse saat buka | 1 HTML 3,05 MB (foto & font base64) | ±370 KB kode + file foto/font biner |
| Foto kembar | 2 salinan | 1 (nama = hash isi) |
| Waktu buka (HP lambat disimulasikan, CPU 4×) | ±1,8 dtk | ±0,9 dtk |
| Memori JS | ±18 MB | ±9,5 MB |
| Library QR | CDN (butuh internet) | Lokal 15 KB |

---

## Catatan proyek asli (versi web)

Satu aplikasi web (satu file HTML) berisi:
- **Kasir/POS**: transaksi, member & paket langganan, stok, resep, pengeluaran, ringkasan, laporan WhatsApp ke Owner.
- **Kabar (halaman publik)**: promo, kegiatan, kabar, testimoni, menu, reseller per wilayah, kontak, Chat 521.

## Isi folder

| Folder / file | Isi |
|---|---|
| `src/index.src.html` | **Kode sumber utama** (HTML + CSS + JavaScript). Edit di sini. Berisi penanda `__KDATA__`, `__LOGO__`, `__FONTS__`, `__HERO__`, `__QRIS__`, `__PQR__` yang diisi saat build. |
| `data/kdata.json` | Data toko yang ikut terbit: menu, promo, kabar, testimoni, reseller, pengaturan. Diambil dari versi live terakhir. |
| `assets/` | Logo (`logo.sym`), foto hero, gambar QRIS, QR POS, dan font Paralucent (`fonts/`). |
| `scripts/build.py` | Merakit semuanya menjadi file siap pakai di `dist/`. |
| `dist/index.html` | Hasil build, **file yang diterbitkan** sebagai Artifact. |
| `dist/preview.html` | Sama, ditambah tag viewport, jadi bisa dibuka langsung di browser laptop/HP. |
| `dist/app.js` | Hanya bagian JavaScript (untuk dibaca/dicek). |
| `tests/` | Skrip uji otomatis (Playwright): testimoni, member, laporan WA, paste foto, izin akun, kelancaran scroll, dll. |
| `arsip/` | Riwayat: skrip perubahan per fitur dan modul awal sebelum digabung. Tidak dipakai saat build, hanya catatan. |

## Cara build
Butuh Python 3.
```
python3 scripts/build.py
```
Hasilnya ada di `dist/`. Untuk melihat, buka `dist/preview.html` di browser.

## Cara uji (opsional)
Butuh Node.js + Playwright (`npm i playwright` lalu `npx playwright install chromium`).
```
cd tests
node tth.js         # tangkapan layar testimoni tema gelap & terang
node perf.js        # ukur kelancaran scroll (simulasi HP lambat)
```
Sebagian skrip uji dibuat saat data toko masih lebih sedikit, jadi bisa perlu disesuaikan dengan data sekarang.
Login uji: Masuk → Owner → password `1234` (password contoh di data uji, ganti di aplikasi untuk pemakaian nyata).

## Catatan penting
- Fitur yang butuh claude.ai (sinkron langsung antar-HP, terbit dari dalam halaman, Chat 521 berbasis AI) **hanya jalan saat dibuka sebagai Artifact di claude.ai**. Dibuka sebagai file biasa, aplikasi tetap jalan, tapi tanpa fitur-fitur itu.
- Data transaksi kasir disimpan di browser masing-masing HP (localStorage `pos521`), tidak ada di dalam file ini.
- `data/kdata.json` di repo publik ini sudah **tanpa paket data tim** (akun, PIN ter-hash, member). Kontak reseller tetap ada karena memang tampil di halaman publik.
- Setelah mengubah `src/` atau `data/`, jalankan build lagi sebelum menerbitkan.
