"""Perubahan 17: notifikasi promo/diskon/kabar selalu tampil sebagai notifikasi HP (pesan + suara), juga saat aplikasi
sedang terbuka. Sebelumnya saat aplikasi terbuka hanya suara + tulisan kecil 2 detik, jadi "suara masuk, pesannya hilang".
- kAnnounce: tidak lagi membunyikan suara sendiri; Android yang mengirim notifikasi (suara ikut notifikasinya).
- HP pelanggan (tanpa tim) yang sedang membuka aplikasi ikut mengecek kabar baru tiap 30 detik.
- Atur → Notifikasi → Cek: status cek otomatis terakhir, jenis yang dimatikan di HP, dan tombol "Kirim notifikasi uji".
Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V17-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


# 1) aplikasi terbuka: notifikasi sungguhan dari Android, bukan hanya suara
rep("""  try{if(window.A521&&A521.playSound)A521.playSound((N[t]||{}).snd||"ding")}catch(e){}
  try{if(window.A521&&A521.kabarSync)A521.kabarSync()}catch(e){}}""",
    """  /*V17-PATCH*/ /* pesan & suara dikirim Android sebagai notifikasi HP (tidak lagi hanya bunyi) */
  try{if(window.A521&&A521.kabarSync)Promise.resolve(A521.kabarSync()).then(r=>{if(r&&r.perm===false)toast("Notifikasi HP ini mati. Nyalakan di Atur → Notifikasi → Cek",1)})}catch(e){}}""")

# 2) HP pelanggan yang sedang membuka aplikasi juga mengambil kabar baru
rep("""setInterval(()=>{if(document.visibilityState==="visible"&&stOn()){stAuto(0);logAuto(500);kHot()}},30000);""",
    """setInterval(()=>{if(document.visibilityState!=="visible")return;if(stOn()){stAuto(0);logAuto(500)}if(SRVU())kHot()},30000);""")
rep("""if(document.visibilityState==="visible"){syncKick();if(stOn())kHot();""",
    """if(document.visibilityState==="visible"){syncKick();if(SRVU())kHot();""")

# 3) Cek notifikasi: status + tombol uji
rep("""  ${st.strict&&HPA[b]?`<p class="hpstep">Di layar <b>Mulai otomatis</b>: ${HPA[b]}.</p>`:""}
  <p class="hpstep">Di layar <b>baterai</b>: ${HPB[b]||HPB.lain}.</p>
  <button class="btn" data-a="hpdone">Selesai</button>`);""",
    """  ${st.strict&&HPA[b]?`<p class="hpstep">Di layar <b>Mulai otomatis</b>: ${HPA[b]}.</p>`:""}
  <p class="hpstep">Di layar <b>baterai</b>: ${HPB[b]||HPB.lain}.</p>
  ${hpDiag(st)}
  <button class="btn ghost" data-a="nftest">🔔 Kirim notifikasi uji</button>
  <button class="btn" data-a="hpdone">Selesai</button>`);""")
rep("""function hpAsk(){""", """function hpDiag(st){const L=[],t=+st.last||0;
  if(Array.isArray(st.off)&&st.off.length)L.push(`<p class="hpstep">⚠️ Dimatikan di pengaturan HP: <b>${st.off.map(esc).join(", ")}</b>. <button class="btn ghost sm" data-a="hpgo" data-v="notif">Nyalakan</button></p>`);
  const ago=t?Math.round((Date.now()-t)/60000):-1;
  L.push(`<p class="hpstep mute">Cek promo otomatis terakhir: <b>${ago<0?"belum pernah":ago<1?"baru saja":ago<60?ago+" menit lalu":Math.round(ago/60)+" jam lalu"}</b>${st.version?` · versi aplikasi ${esc(st.version)}`:""}</p>`);
  return L.join("")}
function hpAsk(){""")
rep("""  if(a==="hpsheet"){hpSheet(v);return}""",
    """  if(a==="hpsheet"){hpSheet(v);return}
  if(a==="nftest"){const n=nfCfg();if(!window.A521||!A521.notifyTest){toast("Hanya di aplikasi Android");return}
    A521.notifyTest({type:"promo",snd:(n.promo||{}).snd||"ceria",title:"🔔 Uji notifikasi "+(K.store.name||"521"),body:"Kalau pesan ini muncul di panel notifikasi, notifikasi HP ini sudah benar."})
      .then(r=>toast(r&&r.sent?"Notifikasi uji dikirim. Lihat panel notifikasi di atas layar.":"Tidak terkirim: izinkan notifikasi dulu (tombol Izinkan di atas).",1));return}""")

P.write_text(s)
print("OK, perubahan 17 (notifikasi tampil dengan pesan) diterapkan.")
