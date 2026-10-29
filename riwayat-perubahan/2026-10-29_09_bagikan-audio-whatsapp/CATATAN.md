# 09 · Suara dari WhatsApp: "Bagikan → 521 Coffee App" + dukungan pesan suara (.opus)
**Tanggal:** 29 Oktober 2026 · **Diminta oleh:** Raihan (Samsung A25)

## Apa yang berubah
- Aplikasi muncul di daftar **Bagikan** untuk file audio. Di WhatsApp: tekan lama pesan audio → **Bagikan** → **521 Coffee App** → suara langsung masuk ke **Atur → Notifikasi → Suara saya** (diputar sebagai pratinjau).
- Bila belum login: suara disimpan sementara, otomatis ditambahkan setelah Owner/Admin masuk.
- **Pesan suara WhatsApp (.opus)** kini diterima (disimpan sebagai OGG), juga lewat "📁 Impor dari HP…".
- Batas tetap: maks 1,5 MB · maks 20 detik.

## File yang diubah
`src/index.src.html` (`perubahan-src.diff`; skrip `scripts/patches/patch_v9_bagikan_audio.py`),
`AndroidManifest.xml` (filter Bagikan audio), `MainActivity.java`, `android-web/shim.js` (`perubahan-lain.diff`)

## Uji otomatis (lulus)
Audio dibagikan saat belum login → diminta masuk → setelah login otomatis masuk "Suara saya", halaman Atur → Notifikasi terbuka & suara diputar; audio 45 detik ditolak dengan pesan jelas. Kode Android lolos cek kompilasi.
