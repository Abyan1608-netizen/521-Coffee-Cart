# 10 · Masuk tanpa kode tim, stok sama di semua HP, peran Reseller, tombol Cup/Botol
**Tanggal:** 30 Oktober 2026 · **Diminta oleh:** Raihan

## Apa yang berubah
- **Tidak ada lagi kode tim.** Owner membuat akun di Atur → Tim & PIN. Di HP lain cukup: pasang aplikasi → Masuk → isi **nama & PIN** → langsung tersambung ke HP Owner.
- **Peran: Owner / Barista / Reseller.** Untuk Barista & Reseller, aksesnya diatur dengan saklar yang sudah ada. Reseller otomatis memakai saluran "Reseller" (harga reseller) di kasir. Nama akun harus unik.
- **Stok sama di semua HP** (bahan baku & produk jadi). Jual, tambah, kurangi, atau hapus batch di HP mana pun langsung terlihat di HP lain. Saat offline, perubahan menunggu dan terkirim otomatis begitu ada internet.
- **Stok lama ikut masuk.** Batch yang sudah dicatat di HP mana pun (mis. stok di HP Bang Urwah: Palm Sugar 5, Butterscotch 9, Black Caffe 9) otomatis digabung ke stok bersama saat HP itu memakai versi ini. Angka bahan baku awal diambil dari HP Owner.
- **Penjualan, pengeluaran, dan langganan** dari HP tim masuk ke HP Owner lewat server, walau HP Owner sedang mati (sebelumnya harus online bersamaan atau lewat WhatsApp).
- **Menghapus anggota** otomatis mengganti kunci tim: HP orang itu langsung terputus. HP anggota lain tersambung lagi sendiri.
- Atur → Sinkron semua HP: tidak menampilkan kode lagi. Ada tombol "Bagikan cara masuk ke tim" dan "Putuskan semua HP lain" (bila HP hilang).
- Lupa PIN di HP baru: Owner menyambungkan HP dengan Kunci Owner lalu mengatur PIN baru.
- **Kasir:** tombol Cup/Botol tanpa ikon, tulisan lebih besar.

## File yang diubah
- `src/index.src.html` (`perubahan-src.diff`; skrip `scripts/patches/patch_v10_akun_stok_bersama.py`)
- `server/src/index.js`, `server/wrangler.toml` (`perubahan-lain.diff`): `/acct`, `/login`, `/t/stock`, `/t/log`, cek kunci tim di `/room`, kebijakan privasi
- `android/app/build.gradle.kts`: versi 1.1.0 (versionCode 2)
- `docs/LAPORAN-KEAMANAN.md`, `docs/PANDUAN-RILIS.md`

## Wajib setelah pembaruan
1. Server: `cd server` lalu `npx wrangler deploy` (endpoint baru + 2 pembatas laju baru).
2. Pasang versi baru di **HP Owner (yang punya Kunci Owner) lebih dulu**, buka aplikasi, masuk. HP Owner mengunggah daftar akun.
3. Lalu perbarui HP lain. HP yang sudah tersambung tetap memakai daftar akun + keypad seperti biasa (bisa offline).
4. Setelah semua HP diperbarui, cek Stok → Bahan baku dan lakukan **hitung ulang** bila angkanya belum sesuai (dulu bahan baku dicatat per HP).

## Uji otomatis (lulus, 28 pemeriksaan)
Server lokal + 5 HP (Playwright): Owner menyiapkan akun tanpa tombol; nama kembar ditolak; Reseller dapat akses awal pos+penjualan; HP baru masuk dengan nama & PIN; PIN salah ditolak & dikunci setelah 5×; stok lama HP Bang Urwah muncul di semua HP; jual 2 botol + 1 cup di HP Barista → stok botol & susu berkurang di semua HP dan penjualan masuk ke Owner; perubahan saat offline terkirim setelah online; hapus anggota → HP-nya terputus & tidak bisa masuk, HP lain tersambung lagi sendiri; hapus batch hilang di semua HP; HP versi lama yang memakai kode tim ikut tergabung. Tanpa server, aplikasi tetap jalan seperti biasa. Skrip: `uji-banyak-hp.js`.
