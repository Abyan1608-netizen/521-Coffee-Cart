# 07 · "Lupa PIN?" untuk Owner + penjelasan di lembar ganti PIN
**Tanggal:** 29 Oktober 2026 · **Dilaporkan oleh:** Raihan

## Masalah
Setelah login dengan PIN awal 1234, aplikasi langsung membuka lembar **wajib ganti PIN** tanpa penjelasan.
Kunci Owner bisa tertempel di kolom **Nama** atau **PIN** → nama Owner berubah jadi kode acak dan PIN lama/1234 tidak bisa dipakai lagi.

## Perbaikan
1. **Lupa PIN?** di layar login → pilih akun Owner, isi **Kunci Owner** (dicek ke server), isi PIN baru → PIN diatur ulang tanpa menghapus data. Opsi mengembalikan nama akun menjadi "Owner".
2. Lembar wajib ganti PIN kini punya **penjelasan jelas**: isi PIN login baru; Kunci Owner *tidak* diisi di sini.
3. **Pencegahan**: aplikasi menolak bila Kunci Owner (atau teks yang mirip kunci) dimasukkan sebagai Nama atau PIN.
4. Karyawan yang lupa PIN tetap diatur ulang oleh Owner di Atur → Tim & PIN.

## File yang diubah
`src/index.src.html` (lihat `perubahan-src.diff`; skrip: `scripts/patches/patch_v7_lupa_pin.py`)

## Uji otomatis (lulus)
Peringatan tampil; Kunci Owner ditolak di Nama & PIN; HP yang terlanjur rusak (nama & PIN = kunci) dipulihkan lewat Lupa PIN dengan kunci benar, kunci salah ditolak; login dengan PIN baru berhasil.
