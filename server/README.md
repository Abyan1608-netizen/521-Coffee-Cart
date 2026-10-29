# Server mini 521 Coffee App

Cloudflare Worker + Durable Objects (paket gratis cukup). Langkah pasang ada di `../PANDUAN-RILIS.md` bagian A.

| Endpoint | Fungsi |
|---|---|
| `POST /chat` | Proxy ke Claude API (streaming teks). Dibatasi laju & kuota harian. |
| `GET/PUT /k` | Data Kabar/menu/tim terbitan HP Owner (PUT butuh Kunci Owner). |
| `GET/PUT /media/<sha256>.jpg` | Foto Kabar (PUT butuh Kunci Owner, isi diverifikasi). |
| `GET /room/<id>` | WebSocket realtime per tim (isi terenkripsi kode tim). |
| `POST /auth` | Cek Kunci Owner. |
| `GET /privacy` | Kebijakan privasi untuk Google Play. |

Ganti model atau batas: edit `[vars]` di `wrangler.toml`, lalu `npx wrangler deploy`.
