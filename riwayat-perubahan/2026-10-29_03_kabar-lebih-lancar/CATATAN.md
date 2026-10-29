# 03 · Halaman Kabar lebih lancar (tidak patah-patah)
**Tanggal:** 29 Oktober 2026 · **Diminta oleh:** Raihan

## Masalah
Scroll halaman Kabar patah-patah, terutama di HP menengah ke bawah.

## Penyebab (diukur, simulasi HP lambat CPU 4×)
1. **±430 kotak piksel beranimasi tanpa henti** di tombol "Pesan sekarang" dan tombol chat. Tiap kotak jadi lapisan GPU sendiri → penyebab utama.
2. Saat scroll, kelas `scrl` dipasang/dilepas di `<html>` → browser menghitung ulang gaya **seluruh halaman** di setiap awal & akhir scroll.
3. Animasi yang memaksa gambar ulang tiap frame (cincin bayangan, kilau latar).

## Perbaikan (desain tidak berubah)
1. Efek piksel digambar di **satu canvas per tombol** dengan waktu, warna, dan pola yang sama persis. Hanya bekerja saat tombol terlihat & pikselnya sedang muncul. (Lihat `perbandingan-efek-piksel.png`: atas = lama, bawah = baru.)
2. Gelombang piksel pembuka disembunyikan setelah selesai.
3. Jeda animasi berat saat scroll lewat Web Animations API, tanpa mengganti kelas di `<html>`.

## Hasil
| | Sebelum | Sesudah |
|---|---|---|
| Frame tersendat (>33 ms) saat scroll | ±58% | ±9% |
| Frame yang tampil dalam uji yang sama | ±190 | ±295 |
| Animasi berjalan bersamaan | 220 | 26 |

## File yang diubah
`src/index.src.html` (lihat `perubahan-src.diff`; skrip: `scripts/patches/patch_kabar_smooth.py`)
