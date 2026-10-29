# Panduan Rilis 521 Coffee App ke Google Play

Urutannya: **(A) pasang server → (B) build aplikasi → (C) upload ke Play Console.**
Server boleh dilewati dulu. Tanpa server, aplikasi tetap jalan penuh secara offline, hanya tanpa sinkron antar-HP dan Chat 521 AI.

---

## Yang perlu disiapkan (sekali saja)

| Kebutuhan | Untuk apa | Biaya |
|---|---|---|
| **Android Studio** (developer.android.com/studio) | Build file `.aab` + tes di emulator/HP | Gratis |
| **Node.js LTS** (nodejs.org) | Deploy server & minify kode | Gratis |
| **Python 3** (sudah ada di Mac) | Merakit file web untuk Android | Gratis |
| Akun **Cloudflare** (dash.cloudflare.com) | Server mini (sinkron + Chat 521) | Gratis |
| Akun **Anthropic Console** (console.anthropic.com) | Kunci Claude API untuk Chat 521 | Bayar sesuai pemakaian (isi saldo, pasang batas) |
| Akun **Google Play Console** | Menerbitkan aplikasi | USD 25 sekali bayar |

VSCode **tidak wajib**. Semua file bisa diedit di editor apa pun.

---

## A. Pasang server (±15 menit)

Buka Terminal di Mac, masuk ke folder proyek:

```bash
cd 521-coffee-app/server
npm install
npx wrangler login                       # buka browser, izinkan Cloudflare
openssl rand -base64 24                  # buat KUNCI OWNER acak, simpan di password manager
npx wrangler secret put OWNER_KEY        # tempel kunci owner tadi
npx wrangler secret put ANTHROPIC_API_KEY  # tempel API key dari console.anthropic.com
npx wrangler deploy
```

Hasilnya alamat seperti `https://coffee521-api.NAMAKAMU.workers.dev`. Cek di browser:
- `.../health` harus menampilkan `{"ok":true,...}`
- `.../privacy` adalah **halaman Kebijakan Privasi** (dipakai di Play Console)

Lalu tulis alamat itu di `android-web/config.json`:

```json
{ "server": "https://coffee521-api.NAMAKAMU.workers.dev" }
```

**Pengaman biaya Claude API:** di console.anthropic.com → *Limits*, pasang batas belanja bulanan (misalnya USD 10).
Server juga membatasi 6 pertanyaan/menit per HP dan 400 pertanyaan/hari total (`CHAT_DAILY_MAX` di `wrangler.toml`).

---

## B. Build aplikasi

### 1. Rakit file web
Setiap kali mengubah `src/`, `data/`, atau `android-web/`:

```bash
cd 521-coffee-app
python3 scripts/build_android.py
```

### 2. Buka di Android Studio
*File → Open →* pilih folder **`521-coffee-app/android`**. Tunggu proses "Gradle sync" selesai (pertama kali agak lama karena mengunduh SDK).
Kalau Android Studio menawarkan *upgrade* Android Gradle Plugin, boleh diterima.

### 3. Tes dulu
Colok HP (aktifkan *Developer options → USB debugging*) atau buat emulator di *Device Manager*, lalu tekan ▶ **Run**.
Checklist tes singkat:
- [ ] Halaman Kabar tampil, foto muncul
- [ ] Masuk → Owner → PIN `1234` → aplikasi **memaksa ganti PIN**
- [ ] Salah PIN 5x → terkunci 30 detik
- [ ] Transaksi kasir, cetak/salin struk, laporan WhatsApp terbuka di WhatsApp
- [ ] Atur → Data & backup → simpan backup (muncul dialog simpan file)
- [ ] Tambah foto Kabar dari galeri
- [ ] Tombol kembali Android menutup lembar/chat dulu
- [ ] (Dengan server) Atur → Sinkron semua HP → isi **Kunci Owner** → aktifkan sinkron → HP kedua isi kode tim
- [ ] (Dengan server) Chat 521 menjawab "Online · didukung Claude"

### 4. Buat file rilis `.aab`
*Build → Generate Signed App Bundle / APK → Android App Bundle → Create new…* (buat **upload key**).
- Simpan file `.jks` dan passwordnya di tempat aman (password manager + cadangan). **Jangan dikirim ke siapa pun.**
- Pilih *release*. Hasilnya: `android/app/release/app-release.aab`.

Untuk versi berikutnya, naikkan `versionCode` (1 → 2 → 3…) dan `versionName` di `android/app/build.gradle.kts`.

---

## C. Upload ke Google Play Console

1. **Buat aplikasi**: nama `521 Coffee App`, bahasa Indonesia, *App*, *Free*.
2. **Play App Signing**: terima (bawaan). Google menyimpan kunci penandatanganan, kamu cukup menjaga upload key.
3. **Store listing**: pakai file di folder `play-store/`:
   - Ikon `icon-512.png`, gambar fitur `feature-graphic-1024x500.png`
   - Tangkapan layar `screenshot-1..4.png` (1080×1920)
4. **App content**:
   - *Privacy policy*: `https://coffee521-api.NAMAKAMU.workers.dev/privacy`
   - *Ads*: Tidak ada iklan
   - *App access*: "Sebagian fitur butuh login. Setelah instal: Masuk → Owner → PIN 1234, lalu aplikasi meminta PIN baru."
   - *Target audience*: 18+ (aplikasi kerja/kasir)
   - *Content rating*: isi kuesioner (tidak ada kekerasan/judi/dll)
   - *Data safety*: lihat tabel di bawah
5. **Tes tertutup (wajib untuk akun pribadi baru)**: buat *Closed testing*, undang **minimal 12 penguji** (barista, keluarga, teman) yang **tetap ikut selama 14 hari berturut-turut**. Setelah itu baru bisa ajukan *Production*.
6. **Production**: upload `app-release.aab`, isi catatan rilis, kirim untuk review.

### Jawaban Data safety (sesuai cara kerja aplikasi ini)

| Pertanyaan | Jawaban |
|---|---|
| Mengumpulkan/berbagi data? | Ya (hanya bila server diaktifkan) |
| Data dienkripsi saat dikirim? | Ya (HTTPS) |
| Pengguna bisa minta hapus data? | Ya (kontak di kebijakan privasi) |
| **Foto** | Dikumpulkan, untuk *App functionality* (foto Kabar yang diterbitkan Owner), opsional |
| **Pesan / konten buatan pengguna lain** | Dikumpulkan, *diproses sementara* (ephemeral), untuk *App functionality* (pertanyaan Chat 521) |
| **ID perangkat atau ID lain** | Dikumpulkan, *diproses sementara*, untuk *Fraud prevention, security* (ID acak pembatas laju) |
| Transaksi, member, akun tim | **Tidak** perlu dicantumkan: tersimpan di HP; yang dikirim antar-HP terenkripsi ujung-ke-ujung dengan kode tim |
| Dibagikan ke pihak ketiga? | Tidak (Anthropic & Cloudflare berstatus penyedia layanan yang memproses atas nama kita) |

---

## Setelah rilis: semua link & QR
Semua link dan QR yang dulu menunjuk ke halaman claude.ai sekarang menunjuk ke
`https://play.google.com/store/apps/details?id=id.coffee521.pos`.
Link ini baru aktif setelah aplikasi lolos review. Sebelum itu, bagikan link undangan tes tertutup.
Catatan: QR dan poster lama yang sudah dicetak masih mengarah ke halaman claude.ai lama.

## Kalau ada error saat build
Salin teks error dari Android Studio (panel *Build*) dan kirim ke Claude. Biasanya cukup satu-dua baris perbaikan.
