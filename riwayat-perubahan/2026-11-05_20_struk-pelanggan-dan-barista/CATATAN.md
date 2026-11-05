# 20 · Cetak otomatis 2 struk: pelanggan & barista
**Tanggal:** 5 November 2026 · **Diminta oleh:** Raihan, dengan video contoh pengaturan struk dari aplikasi kasir lain: "1 penjualan itu minimal 2 struk."

## Apa yang berubah
- **Atur → Printer & struk** (dulu "Printer Bluetooth") kini punya tiga tab:
  - **Umum:**
    - pilih/ganti printer, cetak tes;
    - **Cetak otomatis setelah bayar** (bawaan: aktif);
    - pilih struk yang dicetak: **Struk pelanggan** dan/atau **Struk barista** (bawaan: keduanya);
    - lebar kertas 58/80 mm;
    - **Potong otomatis (auto cutter)**. Bila mati, di antara dua struk dicetak garis "sobek di sini";
    - logo 521 aktif/mati & **ukuran logo** 30–80%.
  - **Struk pelanggan:** nomor antrian, lokasi toko, WhatsApp, Instagram, nama kasir, asal pesanan.
  - **Struk barista:** huruf menu besar, asal pesanan, nama kasir.
- **Struk barista** (tanpa harga):
  - "STRUK BARISTA", **nomor antrian besar**, jam & asal pesanan;
  - daftar **jumlah × menu** dengan huruf besar; menu botol ditandai "ambil dari stok";
  - **catatan pesanan**.
- **Catatan untuk barista** di layar bayar (opsional, misal "a.n. Budi, less sugar"). Catatan ikut tersimpan di transaksi, tampil di layar Lunas, dan tercetak di kedua struk.
- **Nomor antrian** (#1, #2, … per hari) sama di struk pelanggan & barista, supaya pesanan mudah dicocokkan.
- Kedua struk dikirim dalam **satu kali cetak**: pelanggan dulu, lalu barista. Tombol **Printer** di layar Lunas mencetak ulang struk yang sama.
- **Contoh struk:**
  - pratinjau Pelanggan/Barista/Keduanya, 58/80 mm, dengan tombol "Cetak contoh ini";
  - pratinjau dibuat dari **byte printer yang sama persis** dengan yang dikirim ke printer.
- **Bluetooth mati saat menekan Printer:** aplikasi meminta Bluetooth dinyalakan lalu langsung mencetak.
- Versi 1.6.0 (13).

## Uji (lulus) — `uji-v20.js`
Setiap byte yang dikirim ke printer tiruan dibaca ulang baris demi baris:
- **Satu kiriman:** dua struk dalam satu kiriman, urutan pelanggan → barista.
- **Pemisah:** garis sobek bila tanpa pisau, perintah potong bila dengan pisau.
- **Isi struk barista:** tanpa harga, nomor antrian besar & sama di kedua struk, menu besar, tanda botol, catatan.
- **Logo & lebar:** logo 50%/80%, semua baris muat di 58 mm & 80 mm.
- **Catatan:** tidak hilang saat jumlah diubah, tersimpan, tercetak, dan kosong lagi untuk pesanan berikutnya.
- **Cetak otomatis & ulang:** otomatis setelah bayar, cetak ulang dari Lunas, hanya struk barista, tiap pilihan tab pelanggan/barista.
- **Contoh struk:** pratinjau 3 pilihan & cetak dari contoh.
- **Bluetooth mati:** dinyalakan lalu tercetak.

Uji perubahan 18, 17, 16, 14, 11, 10, web, offline, dan 13 diulang.

**Belum diuji dengan printer sungguhan.** Mohon coba "Cetak tes" di printer kasir.
