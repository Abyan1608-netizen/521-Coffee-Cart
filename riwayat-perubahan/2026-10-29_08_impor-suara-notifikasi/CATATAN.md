# 08 · Impor suara notifikasi dari HP
**Tanggal:** 29 Oktober 2026 · **Diminta oleh:** Raihan

## Apa yang berubah
- **Atur → Notifikasi**: setiap pilihan suara punya opsi **📁 Impor dari HP…**, plus kartu **🎵 Suara saya** (putar ▶, hapus, impor).
- Format: **MP3, OGG, M4A, AAC, WAV** · maks **1,5 MB** · maks **20 detik** (dicek otomatis; pesan jelas bila terlalu besar/panjang/format salah). Maks 10 suara.
- Saat **Simpan & terbitkan**, file suara diunggah ke server → **HP staf & pelanggan mengunduhnya otomatis** dan notifikasi berbunyi sama. Bila suara belum terunduh di suatu HP, sementara memakai suara bawaan HP.
- Menghapus suara → jenis notifikasi yang memakainya kembali ke "Ding".

## ⚠️ Wajib sekali: perbarui server
Server perlu menerima file audio. Di Terminal Mac:
```
cd ~/Documents/"Projek 521"/521-coffee-app/server
npx wrangler deploy
```

## Cara kerja teknis
- File disalin ke penyimpanan aplikasi dengan nama = hash isi (`media/<hash>.mp3`).
- `SoundProvider` (baru) menyajikan file itu **hanya-baca** ke sistem Android supaya bisa jadi suara kanal notifikasi.
- Kanal notifikasi otomatis dibuat ulang saat suara diganti.

## File yang diubah / baru
- `src/index.src.html` (`perubahan-src.diff`; skrip `scripts/patches/patch_v8_impor_suara.py`)
- `server/src/index.js` (izinkan audio), `android-web/shim.js`, **baru** `SoundProvider.java`, `Notif.java`, `MainActivity.java`, `KabarJob.java`, `AndroidManifest.xml` (`perubahan-lain.diff`)

## Uji otomatis (lulus)
Impor (pemilih file tiruan), tolak suara 34 detik, suara muncul di semua dropdown & "Suara saya", ▶ memutar, terbit → server menyimpan daftar suara & file MP3 utuh (12.582 byte, `audio/mpeg`), hapus suara → kembali ke Ding. Kode Android lolos cek kompilasi.
