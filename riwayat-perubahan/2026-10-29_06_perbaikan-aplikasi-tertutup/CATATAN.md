# 06 · Perbaikan: aplikasi langsung tertutup saat dibuka
**Tanggal:** 29 Oktober 2026 · **Dilaporkan oleh:** Raihan

## Masalah
Setelah perubahan 04, aplikasi langsung tertutup sendiri setiap dibuka.

## Penyebab
Fitur cek promo/kabar berkala (perubahan 04) memakai JobScheduler dengan syarat "butuh internet".
Sejak **Android 14**, aplikasi yang menargetkan Android 14+ **wajib** mendeklarasikan izin
`ACCESS_NETWORK_STATE` untuk itu. Tanpa izin tersebut Android melempar `SecurityException`
saat aplikasi dibuka → aplikasi tertutup.

## Perbaikan
1. Tambah izin `ACCESS_NETWORK_STATE` di `AndroidManifest.xml` (izin normal, tidak memunculkan dialog ke pengguna).
2. Pengaman: penjadwalan notifikasi/pengingat dibungkus `try/catch`, sehingga bila suatu saat gagal, **hanya fiturnya yang tidak jalan, aplikasi tetap terbuka**.
3. Setelah HP dinyalakan ulang / aplikasi diperbarui, jadwal cek promo dipasang ulang.

## File yang diubah
`android/app/src/main/AndroidManifest.xml`, `MainActivity.java`, `AlertReceiver.java` (lihat `perubahan-android.diff`)
