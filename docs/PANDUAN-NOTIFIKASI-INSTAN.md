# Notifikasi instan promo & diskon (Firebase) — sekali pasang ±15 menit

**Tanpa Firebase**, notifikasi promo/diskon/kabar tetap jalan:
- **Aplikasi sedang terbuka:** masuk dalam ±2 detik (HP tim) atau ±30 detik (HP pelanggan).
- **Aplikasi tertutup:** masuk lewat cek otomatis Android, biasanya **±15–30 menit**, kadang lebih lama saat HP tidur.

**Dengan Firebase**, notifikasi masuk **beberapa detik** setelah Owner menyimpan promo, **walau aplikasi tertutup**.
Gratis, tanpa batas wajar. Isi promo tidak dikirim lewat Google: server hanya mengirim "colekan", lalu HP mengambil promonya sendiri dari server 521.

---

## Langkah 1 — Buat proyek Firebase (di browser)
1. Buka **https://console.firebase.google.com** → masuk dengan akun Google 521 → **Create a project / Buat proyek**.
2. Nama: `coffee521` → Google Analytics **tidak perlu** (matikan) → **Create project**.

## Langkah 2 — Daftarkan aplikasi Android
1. Di halaman proyek, klik ikon **Android**.
2. **Android package name:** `id.coffee521.pos.debug` (ini APK uji yang sekarang dipakai) → **Register app**.
3. Unduh **`google-services.json`** → simpan. Langkah lain di layar itu (Gradle) **lewati saja**, sudah disiapkan.
4. Ulangi untuk versi Play Store: **Add app → Android →** `id.coffee521.pos`.

> File `google-services.json` **bukan rahasia** (isinya memang ikut di dalam APK). Kirim file itu ke Claude, nanti diisikan ke `android-web/config.json` bagian `"fcm"` dan APK baru dibuat otomatis.

## Langkah 3 — Kunci server (RAHASIA, jangan dikirim ke siapa pun)
1. Firebase → ⚙️ **Project settings → Service accounts → Generate new private key → Generate key**.
2. File `.json` terunduh (misal `coffee521-firebase-adminsdk-xxxx.json`). **Jangan** kirim file ini di chat atau WhatsApp.
3. Di Terminal Mac:
   ```bash
   cd "/Users/mac/Documents/Projek 521/521-coffee-app/server"
   npx wrangler secret put FCM_SA < ~/Downloads/coffee521-firebase-adminsdk-xxxx.json
   npx wrangler deploy
   ```
   (Ganti nama file sesuai yang terunduh.) Setelah berhasil, file kunci di Downloads boleh dihapus.

## Langkah 4 — Cek
- Buka `https://coffee521-api.coffee521.workers.dev/push` → harus tampil `{"on":true}`.
- Pasang APK terbaru di semua HP → **Atur → Notifikasi → Cek** → harus tertulis **⚡ Notifikasi instan aktif**.
- Tutup aplikasi di HP lain, lalu Owner simpan promo baru → notifikasi masuk beberapa detik kemudian.

## Bila notifikasi tetap terlambat di HP tertentu
Xiaomi/OPPO/vivo/realme/Infinix sering menahan aplikasi yang tertutup. Di HP itu: **Atur → Notifikasi → Cek**, lalu izinkan **Mulai otomatis** dan **Baterai tanpa batasan**.
