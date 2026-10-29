# 05 · Izin notifikasi + panduan pengaturan HP (Xiaomi, OPPO, vivo, dll)
**Tanggal:** 29 Oktober 2026 · **Diminta oleh:** Raihan

## Masalah
- HP Xiaomi/Redmi/POCO, OPPO/realme/OnePlus, vivo/iQOO, Huawei/Honor, Samsung, Infinix/Tecno sering **menahan aplikasi di latar belakang**, sehingga notifikasi terlambat atau tidak muncul.
- HP pelanggan (Android 13+) **belum pernah diminta izin notifikasi**, jadi notifikasi promo tidak bisa tampil sama sekali.

## Apa yang berubah
1. **Pelanggan** (halaman umum, tanpa login): ±6 detik setelah membuka aplikasi muncul tawaran *"Mau dapat info promo & diskon?"* → **Ya, nyalakan** memunculkan izin notifikasi Android. Bila "Nanti saja", ditawarkan lagi paling cepat 7 hari kemudian.
2. Setelah izin, untuk HP yang agresif muncul **panduan sesuai merek** dengan tombol yang langsung membuka layar pengaturan yang tepat:
   - **Mulai otomatis / Autostart** (Xiaomi, OPPO, realme, OnePlus, vivo, Huawei, Infinix…)
   - **Baterai tanpa batasan** (semua merek)
   - Status ditampilkan (Aktif/Sudah) dan diperbarui otomatis saat kembali dari pengaturan.
3. **Kartu kecil di bawah halaman umum** bila notifikasi belum aktif/bisa terlambat → tombol *Atur*.
4. **Staf**: panduan yang sama muncul sekali setelah login bila perlu, dan bisa dibuka kapan saja di **Atur → Notifikasi → Notifikasi di HP ini → Cek**.

## Aman untuk Google Play
Tidak memakai izin `REQUEST_IGNORE_BATTERY_OPTIMIZATIONS` (sering membuat aplikasi ditolak). Aplikasi hanya **membuka layar pengaturan**, pengguna sendiri yang memilih.

## File yang diubah / baru
- `src/index.src.html` (lihat `perubahan-src.diff`; skrip: `scripts/patches/patch_v5_izin_hp.py`)
- `android-web/shim.js` (status & buka pengaturan)
- **baru** `android/.../HpSettings.java` (deteksi merek, buka layar Autostart/baterai/notifikasi)
- `MainActivity.java` (jembatan `notifStatus`, `openSettings`), `AndroidManifest.xml` (daftar paket pengaturan merek HP)

## Cara menguji
1. Hapus data aplikasi (atau pasang di HP lain) → buka tanpa login → tunggu 6 detik → **Ya, nyalakan** → Izinkan.
2. Di HP Xiaomi/OPPO/vivo: tekan **Buka pengaturan** pada *Mulai otomatis* dan *Baterai* → atur → kembali ke aplikasi → status berubah.

## Uji otomatis (lulus)
Tawaran pelanggan muncul, izin diminta, panduan Xiaomi tampil dengan 3 langkah, tombol membuka pengaturan Autostart & baterai, kartu halaman umum, tidak menawar ulang setelah setuju. Kode Android lolos cek kompilasi.
