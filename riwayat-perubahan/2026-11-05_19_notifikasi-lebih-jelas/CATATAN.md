# 19 · Notifikasi lebih jelas & HP Owner ikut menerima notifikasi
**Tanggal:** 5 November 2026 · **Dilaporkan oleh:** Raihan — "promo, diskon, kabar sudah diisi, kok notifikasinya tidak muncul… padahal jam sudah diatur."

## Temuan (dicek dari data server yang sebenarnya)
1. **HP yang menyimpan promo sengaja tidak diberi notifikasi** (aturan dari perubahan 16). Owner yang menguji dengan HP-nya sendiri jadi tidak pernah melihat notifikasi.
2. **Jam notifikasi promo/diskon/kabar/kegiatan semuanya kosong.** Jam yang diatur (11.24 dan 08.00) ada di kartu **pengingat stok** (produk kedaluwarsa & bahan menipis), bukan di kartu promo. Kartu stok ada di paling atas halaman, jadi mudah tertukar.
3. **Pengingat kedaluwarsa jam 11.24** hanya muncul bila ada produk jadi yang kedaluwarsa besok (H-1). Bila tidak ada, tidak ada notifikasi. Ini bukan bug.

## Perubahan
- HP yang menyimpan promo/diskon/kabar/kegiatan sekarang **juga** mendapat notifikasi HP, sama seperti HP lain.
- **Atur → Notifikasi** disusun ulang:
  - bagian **1 · Promo, diskon, kabar & kegiatan** di atas, lalu **2 · Pengingat stok (khusus tim)** di bawah;
  - tiap bagian diberi penjelasan kapan notifikasinya muncul;
  - "Kirim langsung saat diterbitkan" diganti menjadi "Kirim langsung saat disimpan".
- Versi 1.5.2 (12).

## Uji (lulus)
Uji perubahan 17 (disesuaikan: HP Owner kini juga meminta notifikasi), 16, dan 18.
