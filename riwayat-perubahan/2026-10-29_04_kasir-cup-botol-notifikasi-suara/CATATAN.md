# 04 · Kasir Cup | Botol, hapus stok, pengaturan notifikasi + suara, notifikasi pelanggan
**Tanggal:** 29 Oktober 2026 · **Diminta oleh:** Raihan

## Apa yang berubah
1. **Kasir: tab ☕ Cup | 🧴 Botol** (muncul bila ada menu yang punya stok botol)
   - **Cup** = dibuat saat dipesan → memotong bahan baku seperti biasa.
   - **Botol** = diambil dari stok produk jadi (batch paling dekat kedaluwarsa dulu). Menampilkan sisa stok & ukuran; habis = tidak bisa dijual.
   - Di struk/laporan tercatat terpisah: "Palm Sugar · Botol".
   - **Pengaturan botol** per menu (Stok → Produk jadi → ketuk menu): harga botol, harga reseller botol, ukuran, *bahan per botol (× resep cup)*: dipakai untuk potong bahan saat produksi & menghitung modal.
2. **Hapus stok**: tombol **Hapus** per batch, dan **Hapus dari daftar stok produk jadi** (juga untuk menu yang stoknya sudah 0). Semua tercatat di riwayat.
3. **Atur → Notifikasi** (Owner/Admin): untuk tiap jenis notifikasi, atur aktif/tidak, **untuk siapa** (Staf / Pelanggan / Semua), **suara**, dan tombol ▶ coba suara.
   - Produk hampir kedaluwarsa: **jam** & **H-1/H-2/H-3** · Stok bahan baku menipis: **jam**
   - Promo baru · Diskon baru · Kabar terbaru · Kegiatan
   - Opsi: kirim juga saat promo/kabar **diubah**.
   - Tersimpan bersama Kabar → **Simpan & terbitkan** dari HP Owner agar berlaku di semua HP & pelanggan.
4. **Notifikasi untuk pelanggan** yang memasang aplikasi: promo/diskon/kabar/kegiatan baru dari Owner. Aplikasi mengecek server ±15 menit sekali (Android JobScheduler, tanpa Firebase), dan langsung saat aplikasi dibuka.
5. **Suara notifikasi**: Ding, Lonceng, Ka-ching, Ceria, Lembut (dibuat khusus, total ±41 KB), Bawaan HP, atau Tanpa suara. HP Staf & HP Pelanggan menerima sesuai pilihan "Untuk".
6. **Halaman umum**: tanda **BARU** pada kabar/promo yang belum pernah dilihat di HP itu + pemberitahuan "Ada N kabar/promo baru".

## File yang diubah / baru
- `src/index.src.html` (lihat `perubahan-src.diff`; skrip: `scripts/patches/patch_v4_botol_notif.py`)
- `android-web/shim.js` (peran HP, coba suara, cek kabar)
- `android/.../MainActivity.java`, `AlertReceiver.java`, **baru** `Notif.java`, **baru** `KabarJob.java`
- `AndroidManifest.xml` (layanan KabarJob), **baru** `res/raw/snd_*.ogg` + `res/raw/keep.xml`
- Salinan versi sesudah ada di `salinan/`, tangkapan layar di `tampilan.png`

## Catatan penting
- Notifikasi pelanggan **bukan instan**: ±15–30 menit setelah diterbitkan (aturan hemat baterai Android). HP merek tertentu (Xiaomi/Oppo/Vivo) perlu *Autostart* & baterai *Tanpa batasan* agar tetap terkirim saat aplikasi ditutup.
- Saat pertama memasang aplikasi, kabar yang sudah ada tidak dikirim sebagai notifikasi (supaya tidak banjir). Yang dikirim hanya yang terbit setelahnya.
- HP Owner tidak menerima notifikasi promo buatannya sendiri.

## Cara menguji
1. Stok → Produk jadi → tambah stok → ketuk menu → isi Pengaturan botol → Kasir → tab **Botol**.
2. Atur → Notifikasi → ubah suara → ▶ coba → **Simpan & terbitkan**.
3. Di HP kedua (tanpa login = pelanggan): buka aplikasi sekali, tutup. Dari HP Owner terbitkan promo baru → dalam ±15–30 menit notifikasi muncul dengan suara pilihan.

## Uji otomatis (lulus)
Tab Cup/Botol, harga & ukuran botol, transaksi campuran cup+botol (botol dari stok FEFO, cup potong bahan), hapus batch, hapus dari daftar, simpan pengaturan notifikasi, coba suara, jadwal pengingat sesuai jam & H-n, pengingat stok bahan, tanda BARU. Kode Android lolos cek kompilasi. Tanpa error konsol.
