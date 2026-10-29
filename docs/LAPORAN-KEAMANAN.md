# Laporan Keamanan 521 Coffee App

Cakupan: kode web `src/index.src.html` (±370 KB), data `data/kdata.json`, cara penyimpanan di HP, dan migrasi ke aplikasi Android + server.
Tanggal: 29 Oktober 2026.

## Ringkasan

| # | Temuan | Risiko | Status |
|---|---|---|---|
| 1 | PIN/kata sandi disimpan **teks asli** di penyimpanan HP (`localStorage`) | Tinggi | ✅ Diperbaiki |
| 2 | Hash PIN yang dikirim antar-HP = SHA-256 tanpa salt acak → PIN 4 digit tertebak dalam hitungan detik | Tinggi | ✅ Diperbaiki |
| 3 | Tidak ada batas salah PIN (bisa coba 0000–9999 terus-menerus) | Tinggi | ✅ Diperbaiki |
| 4 | PIN bawaan `1234`/`0000` ditampilkan di layar login dan tidak wajib diganti | Tinggi | ✅ Diperbaiki |
| 5 | URL gambar dimasukkan ke HTML tanpa validasi → injeksi atribut/XSS lewat file backup atau data sinkron | Sedang | ✅ Diperbaiki |
| 6 | Tidak ada Content-Security-Policy, jadi XSS apa pun bisa menjalankan skrip | Sedang | ✅ Diperbaiki (CSP ketat) |
| 7 | Library QR dimuat dari CDN pihak ketiga tanpa *integrity check* | Sedang | ✅ Dibundel lokal |
| 8 | Ekspor CSV rentan *formula injection* (mis. nama produk `=HYPERLINK(...)`) | Rendah | ✅ Diperbaiki |
| 9 | Paket data tim terenkripsi (resep, akun, member) ikut tersebar publik | Sedang | ✅ Tidak ikut ke APK |
| 10 | Kode tim 8 karakter (±40 bit) bisa di-*brute force* offline dari data publik | Sedang | ✅ Jadi 10 karakter (±50 bit, 1000× lebih sulit) |
| 11 | Rencana "pakai Claude API" berisiko kebocoran API key bila ditanam di aplikasi | Kritis (jika dilakukan) | ✅ Key hanya di server |
| 12 | Chat AI publik bisa disalahgunakan → tagihan membengkak | Sedang | ✅ Rate limit + kuota harian + batas topik |

## Detail perbaikan

**PIN & login**
- PIN disimpan sebagai **PBKDF2-SHA256, 100.000 iterasi, salt acak 16 byte per akun** (format `pb2$salt$hash`). Perbandingan waktu-konstan.
- PIN lama (teks asli / SHA-256 lama) **otomatis dimigrasi** saat aplikasi dibuka; backup lama tetap bisa dipulihkan.
- **Batas salah PIN**: 5x salah → jeda 30 detik, berlipat sampai 15 menit, tersimpan di HP (tidak hilang saat aplikasi ditutup). Penghitungan adil: mengetik bertahap tidak dihitung salah, yang dihitung tebakan yang dihapus/diganti.
- Login dengan `1234`/`0000` → **wajib ganti PIN**. PIN yang terlalu mudah (`1234`, `0000`, `1111`, `123456`, `000000`) ditolak.

**Konten & skrip**
- Semua `src` gambar lewat fungsi `su()`: hanya `data:image/(png|jpeg|webp|gif|avif);base64`, `media/<nama>`, atau `https://` tanpa karakter berbahaya.
- CSP aplikasi Android: `script-src 'self'` (tanpa inline/eval), `connect-src` hanya ke server sendiri, `img-src 'self' data: blob:`, `object-src/frame-src 'none'`. Aplikasi sudah dicek tidak memakai `eval`, handler inline, atau `javascript:`.

**Aplikasi Android**
- Konten dimuat dari `https://appassets.androidplatform.net` (WebViewAssetLoader), **akses file:// dan content:// dimatikan**.
- Jembatan JS→Android memakai `WebMessageListener` yang **hanya menerima origin aplikasi sendiri** dan frame utama. Fungsi jembatan terbatas: salin, bagikan, buka link (skema https/http/mailto/tel/whatsapp/geo saja), simpan file lewat dialog sistem, simpan data Kabar.
- Link luar (WhatsApp, Instagram, Maps) selalu dibuka di aplikasi lain, tidak pernah di dalam WebView.
- Hanya izin **INTERNET**. Tidak ada izin lokasi/kamera/kontak/penyimpanan; foto dipilih lewat pemilih file sistem.
- HTTPS saja (*cleartext* dimatikan), sertifikat pengguna tidak dipercaya, Safe Browsing aktif, debugging WebView hanya di build debug, R8 aktif di rilis.
- Cadangan Android: data kasir ikut cadangan Google **terenkripsi** (dinonaktifkan otomatis jika HP tidak mendukung enkripsi), supaya transaksi tidak hilang saat HP rusak.

**Server (Cloudflare Worker)**
- `ANTHROPIC_API_KEY` dan `OWNER_KEY` disimpan sebagai *secret*, tidak pernah ada di aplikasi.
- Tulis data (terbit Kabar, unggah foto) wajib **Kunci Owner**; percobaan dibatasi 8/menit per IP.
- Foto diverifikasi: nama file = hash SHA-256 isinya, maks. 1,9 MB.
- Data tim & transaksi antar-HP **terenkripsi ujung-ke-ujung (AES-GCM, kunci dari kode tim)**. Server dan Cloudflare tidak bisa membacanya.
- Chat 521: 6 pertanyaan/menit per HP & per IP, 400/hari total, maks 800 token jawaban, aturan topik di sisi server yang tidak bisa ditimpa aplikasi, dan **tombol "Laporkan jawaban"** (wajib menurut kebijakan Google Play untuk konten AI).

## Risiko yang tersisa (perlu diketahui)
1. **PIN 4 digit tetap lemah** bila seseorang bisa menyalin isi penyimpanan HP (HP di-root/terbuka). Sarankan Owner memakai kata sandi campuran (mis. `kopi521pagi`).
2. **Siapa pun yang memegang Kunci Owner bisa menerbitkan Kabar.** Simpan di password manager. Bila bocor: `npx wrangler secret put OWNER_KEY` dengan kunci baru; HP Owner lama otomatis berhenti jadi HP Owner.
3. **Kode tim** juga kunci enkripsi data tim. Bila karyawan keluar: Atur → Sinkron → *Buat kode tim baru*.
4. **Aturan Chat 521** dikirim dari aplikasi. Orang yang membongkar aplikasi bisa memakai server untuk bertanya hal lain. Dampaknya dibatasi oleh aturan topik di server, rate limit, kuota harian, dan batas belanja di Anthropic Console.
5. **Cetak Bluetooth langsung** tidak tersedia di WebView Android. Cara "salin ke aplikasi printer" tetap jalan.
6. Data kasir disimpan per HP. Tetap lakukan **backup rutin** (Atur → Data & backup).

## Cara menguji ulang
`tests/` berisi skrip Playwright lama. Pengujian migrasi ini memakai skenario: login, lockout, paksa ganti PIN, sanitasi gambar, CSV, QR lokal, terbit Kabar + unggah foto, konflik versi, Chat 521 streaming, sinkron transaksi barista → owner via WebSocket. Semuanya lulus tanpa error konsol/CSP.
