# Riwayat perubahan

Setiap perubahan disimpan di **satu folder sendiri**, urut tanggal dan nomor:
`TANGGAL_NOMOR_judul-singkat/`

Isi tiap folder:
| File | Isi |
|---|---|
| `CATATAN.md` | Apa yang diubah, alasannya, file yang terdampak, cara menguji, cara membatalkan |
| `perubahan-src.diff` | Perbedaan persis kode `src/index.src.html` sebelum vs sesudah (bisa dibuka di VSCode/TextEdit) |
| `salinan/` | Salinan file selain `src/` yang berubah (versi sesudah perubahan) |
| `asli/` | (hanya di perubahan pertama) kode asli sebelum semua perubahan, sebagai cadangan |

Daftar ringkas semua perubahan ada di `../CHANGELOG.md`.
Membuat folder untuk perubahan baru: `python3 scripts/catat_perubahan.py "judul singkat"`.
