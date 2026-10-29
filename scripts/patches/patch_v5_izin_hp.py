"""Perubahan 05: minta izin notifikasi (pelanggan & staf) + panduan Autostart/baterai per merek HP
(Xiaomi, OPPO, realme, vivo, Huawei, Samsung, Infinix...) yang membuka layar pengaturan yang tepat. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V5-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:200]}")
    s = s.replace(old, new)

rep(".fgdel{", """/*V5-PATCH*/
.hpst{display:grid;gap:8px;margin:4px 0 14px}
.hpst div{display:flex;align-items:center;gap:10px;padding:12px 14px;border:1px solid var(--line);border-radius:14px;background:var(--sf);font-size:14px}
.hpst div b{flex:1}.hpst div .pill{margin:0}
.hpst div button{margin:0;flex:none}
.hpstep{margin:0 0 10px;padding:12px 14px;border-radius:14px;border:1px dashed var(--line);font-size:13.5px;color:var(--mute)}
.hpstep b{color:var(--ink)}
.k-npc{margin:18px 0 0;padding:14px 16px;border-radius:18px;border:1px solid color-mix(in srgb,var(--ac) 40%,var(--line));background:color-mix(in srgb,var(--ac) 8%,var(--sf));display:flex;gap:12px;align-items:center}
.k-npc span{flex:1;font-size:14px}.k-npc b{display:block;font-size:15px}
.k-npc button{margin:0;flex:none}
.fgdel{""")

rep("/* ---------- Menu ---------- */", r'''/* ---------- Izin notifikasi & keandalan di HP (Xiaomi/OPPO/vivo/dll menahan aplikasi di latar belakang) ---------- */
const HPN={xiaomi:"Xiaomi / Redmi / POCO",oppo:"OPPO",realme:"realme",oneplus:"OnePlus",vivo:"vivo / iQOO",huawei:"Huawei / Honor",samsung:"Samsung",transsion:"Infinix / Tecno / itel",asus:"ASUS",lain:"HP ini"};
const HPA={xiaomi:"Nyalakan <b>Autostart</b> untuk 521 Coffee App",oppo:"Izinkan <b>Mulai otomatis / Auto launch</b>",realme:"Izinkan <b>Mulai otomatis / Auto launch</b>",oneplus:"Izinkan <b>Auto launch</b>",vivo:"Aktifkan <b>Mulai otomatis / Background startup</b>",huawei:"Peluncuran aplikasi → <b>Kelola manual</b>, aktifkan semua",transsion:"Aktifkan <b>Auto-start</b>"};
const HPB={xiaomi:"Penghemat baterai → <b>Tanpa batasan</b>",oppo:"Penggunaan baterai → <b>Izinkan aktivitas latar belakang</b>",realme:"Penggunaan baterai → <b>Izinkan aktivitas latar belakang</b>",oneplus:"Baterai → <b>Jangan optimalkan</b>",vivo:"Konsumsi daya latar belakang tinggi → <b>Izinkan</b>",huawei:"Baterai → <b>Kelola manual</b>, aktifkan semua",samsung:"Baterai → <b>Tidak dibatasi</b>",transsion:"Baterai → <b>Tanpa batasan</b>",lain:"Baterai → <b>Tidak dibatasi / Jangan optimalkan</b>"};
let hpSt=null;
async function hpStatus(){if(!window.A521||!A521.notifStatus)return null;try{hpSt=await A521.notifStatus()}catch(e){hpSt=null}return hpSt}
async function hpSheet(who){const st=await hpStatus();if(!st){toast("Pengaturan ini hanya ada di aplikasi Android");return}
  const b=st.brand||"lain",tgt=who==="pelanggan"?"info <b>promo, diskon & kabar</b> dari 521":"pengingat <b>kedaluwarsa & stok</b> serta info promo";
  show(`<h2>🔔 Notifikasi di ${HPN[b]||"HP ini"}</h2><p class="mute" style="margin-top:-6px">Supaya ${tgt} tidak terlambat, izinkan hal berikut. Kamu yang memilih di layar pengaturan HP, aplikasi tidak mengubahnya diam-diam.</p>
  <div class="hpst">
    <div><b>1. Izin notifikasi</b>${st.perm?'<span class="pill ok">Aktif</span>':`<button class="btn sm" data-a="hpgo" data-v="perm">Izinkan</button>`}</div>
    ${st.strict?`<div><b>2. Mulai otomatis</b><button class="btn ghost sm" data-a="hpgo" data-v="autostart">Buka pengaturan</button></div>`:""}
    <div><b>${st.strict?"3":"2"}. Baterai tanpa batasan</b>${st.battery?'<span class="pill ok">Sudah</span>':`<button class="btn ghost sm" data-a="hpgo" data-v="battery">Buka pengaturan</button>`}</div>
  </div>
  ${st.strict&&HPA[b]?`<p class="hpstep">Di layar <b>Mulai otomatis</b>: ${HPA[b]}.</p>`:""}
  <p class="hpstep">Di layar <b>baterai</b>: ${HPB[b]||HPB.lain}.</p>
  <button class="btn" data-a="hpdone">Selesai</button>`);
  try{localStorage.setItem("a521hp",String(Date.now()))}catch(e){}}
function hpAsk(){/* pelanggan di halaman umum: tawarkan notifikasi promo sekali (diulang paling cepat 7 hari bila "Nanti") */
  if(!window.A521||!A521.native||me)return;let a=0;try{a=+localStorage.getItem("a521npa")||0}catch(e){}if(a<0||Date.now()-a<7*864e5)return;
  hpStatus().then(st=>{if(!st||(st.perm&&(!st.strict||st.battery)))return;if(!$("#m").hidden||!$("#login").hidden||me)return;
    show(`<div style="text-align:center"><div style="font-size:44px;line-height:1">🔔</div><h2 style="margin-top:6px">Mau dapat info promo & diskon?</h2><p class="mute">Kami kabari lewat notifikasi saat ada <b>promo, diskon, atau kabar terbaru</b> dari ${esc(K.store.name||"521")}. Tidak ada spam.</p></div>
      <button class="btn" data-a="hpyes">Ya, nyalakan notifikasi</button><button class="btn ghost" data-a="hpno">Nanti saja</button>`)})}
function hpPubCard(){/* kartu kecil di bawah halaman umum bila notifikasi belum aktif */
  if(!window.A521||!A521.native)return;hpStatus().then(st=>{const W=document.querySelector("#pub .kwrap");if(!st||!W||W.querySelector(".k-npc"))return;
    if(st.perm&&(!st.strict||st.battery))return;
    W.insertAdjacentHTML("beforeend",`<div class="k-npc"><span><b>🔔 Notifikasi promo ${st.perm?"bisa terlambat":"belum aktif"}</b>${st.perm?"Izinkan aplikasi berjalan di latar belakang.":"Nyalakan supaya tidak ketinggalan promo & diskon."}</span><button class="btn sm" data-a="hpsheet" data-v="pelanggan">Atur</button></div>`)})}

/* ---------- Menu ---------- */''')

# pasang di halaman umum (setelah render) & setelah login staf
rep("  galInit();setTimeout(kNewMark,60);\n}", "  galInit();setTimeout(kNewMark,60);setTimeout(hpPubCard,400);if(!hpAsk.t){hpAsk.t=setTimeout(hpAsk,6000)}\n}")
rep('function enter(){if(!D.cfg.staffDev){D.cfg.staffDev=1;save()}',
    'function enter(){if(!D.cfg.staffDev){D.cfg.staffDev=1;save()}setTimeout(()=>{try{let a=0;try{a=+localStorage.getItem("a521hp")||0}catch(e){}if(window.A521&&A521.native&&!a)hpStatus().then(st=>{if(st&&(!st.perm||(st.strict&&!st.battery))&&$("#m").hidden)hpSheet("staf")})}catch(e){}},4000);')

# Atur → Notifikasi: status HP ini
rep('''  return `<p class="note" style="margin-top:0">Atur <b>kapan</b> dan <b>apa saja</b>''',
    '''  return `${window.A521&&A521.native?`<div class="k-npc" style="margin:0 0 14px"><span><b>📱 Notifikasi di HP ini</b>Cek izin notifikasi, mulai otomatis & baterai supaya pengingat tidak terlambat.</span><button class="btn sm" data-a="hpsheet" data-v="staf">Cek</button></div>`:""}<p class="note" style="margin-top:0">Atur <b>kapan</b> dan <b>apa saja</b>''')

# aksi
rep('  if(!me)return;\n  if(a==="logout")logout();', '''  if(a==="hpsheet"){hpSheet(v);return}
  if(a==="hpgo"){if(v==="perm"){if(hpSheet.tried||(hpSt&&hpSt.sdk<33))A521.openSettings("notif");else{hpSheet.tried=1;A521.notifyPerm();setTimeout(()=>hpSheet(me?"staf":"pelanggan"),2500)}}else A521.openSettings(v);return}
  if(a==="hpdone"){shut();const c=document.querySelector("#pub .k-npc");if(c)c.remove();setTimeout(hpPubCard,300);return}
  if(a==="hpyes"){try{localStorage.setItem("a521npa","-1")}catch(e){}A521.notifyPerm();shut();setTimeout(()=>hpStatus().then(st=>{if(st&&(st.strict&&!st.battery||!st.perm))hpSheet("pelanggan");else if(st&&st.perm)toast("Notifikasi aktif. Kami kabari saat ada promo 🎉",1)}),1500);return}
  if(a==="hpno"){try{localStorage.setItem("a521npa",String(Date.now()))}catch(e){}shut();return}
  if(!me)return;
  if(a==="logout")logout();''')


# saat kembali dari layar pengaturan HP: perbarui lembar status
rep('document.addEventListener("change",e=>{', '''document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="visible"&&!$("#m").hidden&&document.querySelector("#s .hpst"))setTimeout(()=>hpSheet(me?"staf":"pelanggan"),400)});
document.addEventListener("change",e=>{''')

P.write_text(s)
print("OK, perubahan 05 (izin notifikasi + panduan pengaturan HP) diterapkan.")
