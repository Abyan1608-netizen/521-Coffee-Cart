# 17 · Notifikasi promo selalu tampil dengan pesannya (bukan hanya suara)
**Tanggal:** 4 November 2026 · **Dilaporkan oleh:** Raihan — "suara notifikasi masuk akan tetapi pesan notifikasinya hilang… suara hanya muncul di HP saya."

## Penyebab
1. **Suara tanpa pesan.** Bila aplikasi sedang terbuka saat promo terbit, versi 1.4.0 hanya membunyikan suara dan menampilkan tulisan kecil di dalam aplikasi selama 2 detik. Notifikasi HP sungguhan sengaja ditahan "karena aplikasi terbuka", jadi tidak ada pesan di layar atas maupun di panel notifikasi.
2. **Hanya HP Raihan yang berbunyi.** Pemberitahuan cepat saat aplikasi terbuka hanya berjalan di HP yang tersambung tim. HP pelanggan (tanpa login) yang sedang terbuka tidak mengecek sama sekali. HP yang tertutup bergantung pada cek otomatis Android (±15 menit, bisa lebih lama bila HP tidur / dibatasi baterai), dan HP yang belum memasang 1.4.0 masih memakai aturan lama (HP Owner dilewati).
3. **Notifikasi yang sudah tampil bisa hilang** saat suara satu jenis diganti (kanal notifikasi lama dihapus beserta isinya).
4. Saat aplikasi dibuka setelah promo terbit, promo itu ditandai "sudah dikenal" tanpa notifikasi.

## Apa yang berubah
- Promo/diskon/kabar/kegiatan baru **selalu dikirim sebagai notifikasi HP** (judul + isi + suara pilihan Owner), juga saat aplikasi sedang terbuka atau baru dibuka. Tidak ada lagi suara tanpa pesan. HP yang menerbitkan tetap tidak menerima notifikasi untuk kabarnya sendiri.
- HP pelanggan yang sedang membuka aplikasi kini mengecek promo baru tiap 30 detik (sama seperti HP tim).
- Kanal notifikasi lama tidak dihapus selama masih ada notifikasinya di layar.
- Bila notifikasi aplikasi dimatikan di pengaturan HP, aplikasi memberi tahu.
- **Atur → Notifikasi → Cek** kini menampilkan kapan cek promo otomatis terakhir berjalan, versi aplikasi, jenis notifikasi yang dimatikan di pengaturan HP, dan tombol **Kirim notifikasi uji**.
- Versi 1.4.1 (versionCode 9).

## Batasan yang tetap ada
HP yang **aplikasinya tertutup** menerima promo lewat cek otomatis Android: biasanya ±15–30 menit, bisa lebih lama bila HP sedang tidur atau aplikasinya dibatasi baterai. Agar langsung masuk detik itu juga saat aplikasi tertutup dibutuhkan Firebase Cloud Messaging (belum dipasang).

## File yang diubah
`src/index.src.html` (`perubahan-src.diff`; skrip `scripts/patches/patch_v17_notif_pesan_muncul.py`), `android-web/shim.js`, `KabarJob.java`, `MainActivity.java`, `Notif.java`, `HpSettings.java`, `AlertReceiver.java` (`perubahan-lain.diff`).

## Uji (lulus)
`uji-v17.js`: HP Owner yang menerbitkan tidak memberi notifikasi ke dirinya; HP kasir yang terbuka meminta Android mengirim notifikasi (tidak lagi hanya suara); HP pelanggan tanpa login yang terbuka menerima promo dalam ±30 detik; peringatan bila notifikasi HP mati; halaman Cek menampilkan status dan tombol uji. Uji perubahan 16, 14, 11, 10, web, offline, dan 13 diulang. Kode Android dikompilasi.
