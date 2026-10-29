# 02 · Stok produk jadi + pengingat H-1 + "Laporkan AI"
**Tanggal:** 29 Oktober 2026 · **Diminta oleh:** Raihan

## Apa yang berubah
1. **Tab Stok** punya dua bagian: *Produk jadi* (botol/gelas) dan *Bahan baku*.
   - Stok produk jadi dicatat per **batch**: jumlah, tanggal produksi, masa simpan → tanggal kedaluwarsa.
   - Wajib centang 3 pemeriksaan kelayakan; ditolak bila tanggal produksi di masa depan atau produk sudah/hari ini kedaluwarsa.
   - Kasir menjual batch yang paling dekat kedaluwarsa dulu (FEFO); produk kedaluwarsa tidak bisa terjual.
   - Pengurangan stok dengan alasan; tombol buang produk kedaluwarsa; batal transaksi mengembalikan stok.
   - Saat produksi, bahan baku dipotong sesuai resep (bisa dimatikan per input).
   - Ekspor CSV `stok-produk-jadi`.
2. **Notifikasi HP H-1** pukul 08.00 berisi jumlah, tanggal produksi & kedaluwarsa. Tetap jalan setelah HP restart. Diketuk → buka Stok.
3. **Chat 521:** tombol bendera membuka panel **"Laporkan AI"** (alasan + catatan) sebelum ke WhatsApp.

## File yang diubah
- `src/index.src.html` (lihat `perubahan-src.diff`; skrip: `scripts/patches/patch_fg.py`)
- `android-web/shim.js`, `android/app/src/main/AndroidManifest.xml` (izin notifikasi & boot)
- `android/.../MainActivity.java`, **baru** `android/.../AlertReceiver.java`, `res/drawable/ic_stat_521.xml`, `res/values/strings.xml`
- Salinan versi sesudah ada di `salinan/`

## Cara menguji
Stok → Produk jadi → Tambah stok: produksi 2 hari lalu, masa simpan 3 hari → status H-1, notifikasi langsung muncul.
Jual 1 botol di kasir → batch H-1 berkurang lebih dulu.

## Uji otomatis (lulus)
Validasi input, FEFO (4 dari batch H-1 lalu 2 dari batch lain), tolak jual melebihi stok, batal transaksi mengembalikan stok, jadwal notifikasi, panel Laporkan AI, CSV. Tanpa error konsol.
