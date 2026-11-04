# 16 · Simpan langsung terbit, jam notifikasi pelanggan, perbaikan notifikasi promo
**Tanggal:** 4 November 2026 · **Dilaporkan/diminta oleh:** Raihan

## Masalah yang dilaporkan & penyebabnya
1. **Notifikasi promo/diskon tidak muncul, hanya stok.** Penyebab: (a) HP berperan Owner sengaja dilewati untuk notifikasi pelanggan; HP uji semuanya HP Owner. (b) Bila aplikasi sedang terbuka saat promo terbit, notifikasi ditahan (hanya tanda BARU) dan tidak pernah muncul.
2. **Tombol Terbitkan "tersangkut" di Menerbitkan…** walau sudah terbit. Penyebab: setelah berhasil, layar tidak digambar ulang, jadi tombol tetap bertuliskan Menerbitkan….

## Apa yang berubah
- **Tidak ada tombol Terbitkan lagi.** Di HP Owner, setiap perubahan Kabar/promo/banner/info toko yang disimpan langsung terbit (±1 detik). Status kecil "✓ Tersimpan & sudah terlihat pelanggan" menggantikan tombol. Tombol yang tersisa bertuliskan **Simpan**. Bila internet putus, dicoba lagi otomatis.
- **Notifikasi promo/diskon/kabar/kegiatan:**
  - HP Owner & staf juga menerima (sesuai pilihan "Untuk"). HP yang menerbitkan tidak menerima notifikasi untuk kabarnya sendiri.
  - Saat aplikasi terbuka, promo baru langsung muncul sebagai pemberitahuan di layar + suaranya.
  - **Atur → Notifikasi**: untuk Promo, Diskon, Kabar, Kegiatan kini ada **"Kirim langsung saat diterbitkan"** dan **"Kirim juga pada jam"** (bisa beberapa jam, maks. 8). Pada jam-jam itu, HP pelanggan/staf diingatkan tiap hari selama promo masih berlaku (tanpa tanggal akhir: promo/diskon 7 hari, kegiatan 3 hari, kabar 2 hari). Bekerja walau aplikasi tertutup (alarm Android).
- Versi 1.4.0 (versionCode 8).

## File yang diubah
`src/index.src.html` (`perubahan-src.diff`; skrip `scripts/patches/patch_v16_simpan_otomatis_notif_pelanggan.py`), `android-web/shim.js`, `AlertReceiver.java` (daftar jadwal kedua untuk pengingat kabar), `KabarJob.java` (aturan penerima, jam pengingat, cache) (`perubahan-lain.diff`).

## Uji (lulus)
`uji-v16.js`: tab Kabar tanpa Terbitkan; promo baru terbit otomatis tanpa menekan apa pun; status tidak tersangkut; HP kasir yang sedang terbuka menampilkan "🎉 Promo baru: …" + suara; jam pelanggan tersimpan & sampai ke server. Uji perubahan 10, 11, dan web diulang: lulus. Kode Android lolos kompilasi (GitHub Actions).
