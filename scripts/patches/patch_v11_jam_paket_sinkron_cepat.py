"""Perubahan 11: hapus kotak "Dari HP lain hari ini"; jam pengingat bisa lebih dari satu; jenis paket & Chat 521
sampai ke HP lain dalam hitungan detik; jenis paket terlihat di HP kasir; peringatan HP Owner tanpa Kunci Owner. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V11-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


# ------------------------------------------------------------------ CSS
rep(".nfc .nfr{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}",
    """/*V11-PATCH*/
.nfc .nfr{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
.nfc .nftw{grid-column:1/-1;font-size:12.5px}
.nftimes{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 8px}
.tchip{display:inline-flex;align-items:center;gap:4px;padding:6px 6px 6px 12px;border-radius:999px;background:var(--ac);color:var(--on);font:800 15px/1 var(--f-b);letter-spacing:.01em}
.tchip button{margin:0;width:26px;height:26px;border-radius:50%;border:0;background:rgba(0,0,0,.18);color:inherit;font:800 15px/1 var(--f-b);padding:0;display:grid;place-items:center}
.nfadd{display:flex;gap:8px;align-items:center}.nfadd input{flex:1;margin:0}.nfadd .btn{margin:0;flex:none;white-space:nowrap}
.hubn{display:flex;gap:10px;align-items:flex-start;padding:12px 14px;margin:0 0 14px;border-radius:16px;border:1px solid var(--line);background:var(--sf);font-size:13.5px;line-height:1.45;color:var(--ink)}
.hubn b{display:block;font-size:14.5px;margin-bottom:2px}.hubn .btn{margin:8px 0 0}
""")

# ------------------------------------------------------------------ 1. Kotak "Dari HP lain hari ini" dihapus (sinkron sudah otomatis)
rep('''function teamTxBox(){
  const today=ymd(new Date());''', '''function teamTxBox(){
  const today=ymd(new Date());
  if(stOn()){const Q=myQueue().length;return Q?`<p class="rtl wait" style="margin:4px 0 14px"><i></i>${Q} transaksi menunggu internet, terkirim otomatis ke Owner</p>`:""}''')

# ------------------------------------------------------------------ 2. Jam pengingat lebih dari satu
rep('Object.keys(c).forEach(k=>{if(typeof c[k]==="object")Object.assign(c[k],n[k]||{});else if(n[k]!=null)c[k]=n[k]});return c}',
    '''Object.keys(c).forEach(k=>{if(typeof c[k]==="object")Object.assign(c[k],n[k]||{});else if(n[k]!=null)c[k]=n[k]});
  ["exp","low"].forEach(k=>{const x=c[k],ok=t=>/^\\d{2}:\\d{2}$/.test(t);let T=Array.isArray(x.times)?x.times.filter(ok):[];if(!T.length)T=[ok(x.time)?x.time:"08:00"];x.times=[...new Set(T)].sort().slice(0,8);x.time=x.times[0]});return c}
const tLbl=t=>String(t).replace(":",".");
const tChips=T=>T.map(t=>`<span class="tchip" data-t="${t}">${tLbl(t)}<button type="button" data-a="nftdel" aria-label="Hapus jam ${tLbl(t)}">×</button></span>`).join("");
const nfTimesUI=x=>`<div class="nftw"><span>Jam pengingat (bisa lebih dari satu)</span><div class="nftimes">${tChips(x.times)}</div><div class="nfadd"><input type="time" class="nftin" aria-label="Jam pengingat baru"><button type="button" class="btn ghost sm" data-a="nftadd">+ Tambah jam</button></div></div>`;
function nfTimeAdd(b){const w=b.closest(".nftw"),i=w&&w.querySelector(".nftin");if(!i)return;const v=i.value;
  if(!/^\\d{2}:\\d{2}$/.test(v)){i.focus();try{i.showPicker&&i.showPicker()}catch(e){}toast("Pilih jamnya dulu, lalu tekan Tambah jam");return}
  const T=[...w.querySelectorAll(".tchip")].map(e=>e.dataset.t);if(T.includes(v)){toast("Jam "+tLbl(v)+" sudah ada");return}
  if(T.length>=8){toast("Maksimal 8 jam pengingat");return}
  w.querySelector(".nftimes").innerHTML=tChips(T.concat(v).sort());i.value="";toast("Jam "+tLbl(v)+" ditambahkan. Tekan Simpan supaya berlaku.",1)}
function nfTimeDel(b){const w=b.closest(".nftw"),c=b.closest(".tchip");if(!w||!c)return;if(w.querySelectorAll(".tchip").length<2){toast("Minimal satu jam pengingat");return}c.remove()}''')
rep('${k==="exp"?`<label>Jam pengingat<input type="time" class="nftime" value="${x.time}"></label>',
    '${k==="exp"?`${nfTimesUI(x)}')
rep('${k==="low"?`<label>Jam pengingat<input type="time" class="nftime" value="${x.time}"></label>`:""}',
    '${k==="low"?nfTimesUI(x):""}')
rep('const tm=el.querySelector(".nftime");if(tm&&/^\\d{2}:\\d{2}$/.test(tm.value))x.time=tm.value;',
    '''const tw=el.querySelector(".nftw");if(tw){const ok=t=>/^\\d{2}:\\d{2}$/.test(t),T=[...tw.querySelectorAll(".tchip")].map(e=>e.dataset.t).filter(ok),ti=tw.querySelector(".nftin");
    if(ti&&ok(ti.value)&&!T.includes(ti.value)&&T.length<8)T.push(ti.value);if(T.length){x.times=[...new Set(T)].sort();x.time=x.times[0]}}''')
rep('Pengingat stok berlaku di HP yang mencatat stoknya.', 'Pengingat stok muncul di semua HP staf karena stoknya sama.')
rep('else if(a==="nfsave"&&can("set"))nfSave();',
    'else if(a==="nfsave"&&can("set"))nfSave();\n  else if(a==="nftadd"&&can("set"))nfTimeAdd(b);\n  else if(a==="nftdel"&&can("set"))nfTimeDel(b);')
i = s.find('function fgSchedule(){')
j = s.find('function fgRemind', i)
assert i > 0 and j > i
s = s[:i] + r'''function fgSchedule(){
  /* Pengingat H-n di HP ini (Android), bisa beberapa jam sehari. Mencantumkan tanggal produksi. */
  if(!window.A521||!A521.notify)return;const items=[],N=nfCfg(),hm=t=>String(t||"08:00").split(":").map(Number);
  if(N.exp.on){const dd=+N.exp.days||1;D.fg.filter(b=>b.q>0&&fgDays(b)>=1).forEach(b=>{const p=prod(b.p),k=Math.min(dd,Math.max(1,fgDays(b)));
    N.exp.times.forEach(tm=>{const [H,M]=hm(tm),at=fgD0(b.exp);at.setDate(at.getDate()-k);at.setHours(H,M||0,0,0);
      items.push({id:"fg-"+b.id+"-"+b.exp+"-"+dd+"-"+tm,g:"fg-"+b.id,at:at.getTime(),type:"exp",snd:N.exp.snd,title:(k<=1?"⚠️ Besok kedaluwarsa: ":`⚠️ ${k} hari lagi kedaluwarsa: `)+(p?p.name:b.n),
        body:`${b.q} ${fgUnit(p)} · produksi ${kFmt(b.made)} · kedaluwarsa ${kFmt(b.exp)}. Jual lebih dulu atau tarik dari etalase.`})})})}
  const low=D.ing.filter(g=>g.min>0&&g.qty<g.min);
  if(N.low.on&&low.length){const key=low.map(g=>g.id).sort().join(",");
    N.low.times.forEach(tm=>{const [H,M]=hm(tm),at=new Date();at.setHours(H,M||0,0,0);
      items.push({id:"low-"+ymd(new Date())+"-"+tm+"-"+kHash(key),g:"low",at:at.getTime(),type:"low",snd:N.low.snd,title:`📦 ${low.length} bahan baku hampir habis`,body:low.slice(0,6).map(g=>g.name).join(", ")+(low.length>6?", …":"")+". Cek tab Stok → Bahan baku."})})}
  /* jam yang sudah lewat: cukup satu (yang terakhir) yang dikirim saat aplikasi dibuka */
  const now=Date.now(),last={};items.forEach(x=>{if(x.at<=now&&(!last[x.g]||last[x.g].at<x.at))last[x.g]=x});
  A521.notify(items.filter(x=>x.at>now||last[x.g]===x).sort((a,b)=>a.at-b.at).slice(0,200).map(x=>{const y=Object.assign({},x);delete y.g;return y}))}
''' + s[j:]

# ------------------------------------------------------------------ 3. Data tim, jenis paket & Chat 521 sampai ke HP lain dalam hitungan detik
rep('if(lines().length||!$("#m").hidden||drag){menuAuto(15000);return}', 'if(lines().length||!$("#m").hidden||drag){menuAuto(5000);return}')
rep('function kSync(){try{if(K.team&&!teamSrc())return false;return teamDirty()||',
    'function kSync(){try{if(K.team&&!teamSrc())return false;return kQuickF||teamDirty()||')
rep('await AR.publish(kDoc(pub));PUBK=pub;K_BASE=nb;memForce=0;msMemAt=Date.now();', 'await AR.publish(kDoc(pub));kQuickF=0;kCast();PUBK=pub;K_BASE=nb;memForce=0;msMemAt=Date.now();if(kdirty){kdirty=kHash(JSON.stringify(K))!==K_BASE;if(!kdirty)try{sessionStorage.removeItem("k521-pending")}catch(e){}}')
rep('try{await AR.publish(kDoc());', 'try{await AR.publish(kDoc());kQuickF=0;kCast();')
rep('else if(a==="chatoff"&&chatAdmin()){K.store.chat={on:0};chatClose();kChanged();toast("Chat 521 dinonaktifkan",1);render()}',
    'else if(a==="chatoff"&&chatAdmin()){K.store.chat={on:0};chatClose();const q=kQuick(k=>{k.store.chat={on:0}});kChanged();toast(q?"Chat 521 dinonaktifkan di semua HP":"Chat 521 dinonaktifkan di HP ini. Supaya berlaku di semua HP, ubah dari HP Owner (yang memakai Kunci Owner).",1);render()}')
rep('K.store.chat={on:1};kChanged();toast("Chat 521 diaktifkan",1);render()};',
    'K.store.chat={on:1};const q=kQuick(k=>{k.store.chat={on:1}});kChanged();toast(q?"Chat 521 diaktifkan di semua HP":"Chat 521 diaktifkan di HP ini. Supaya berlaku di semua HP, ubah dari HP Owner (yang memakai Kunci Owner).",1);render()};')
rep('RM.on("_stk",m=>{const d=m.data||{};if(d.dev!==DEV)stAuto(150)});',
    'RM.on("_stk",m=>{const d=m.data||{};if(d.dev!==DEV)stAuto(150)});RM.on("_k",m=>{const d=m.data||{};if(d.dev!==DEV)setTimeout(kHot,300)});')
rep('setInterval(()=>{if(document.visibilityState==="visible"&&stOn()){stAuto(0);logAuto(500)}},30000);',
    'setInterval(()=>{if(document.visibilityState==="visible"&&stOn()){stAuto(0);logAuto(500);kHot()}},30000);')
rep('document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="visible"){syncKick();if(acctOn!==true)acctCheck()}});',
    'document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="visible"){syncKick();if(stOn())kHot();if(acctOn!==true)acctCheck()}});')

# ------------------------------------------------------------------ 4. Langganan: jenis paket terlihat semua, petunjuk izin, teks diperbarui
rep('''own()&&K.team?`<div class="sec"><p class="note" style="margin:0 0 8px">Pelanggan & sisa kuota dikirim ke semua HP tim otomatis (paling lambat ±15 menit) saat aplikasi Owner terbuka. Pemakaian dari HP karyawan masuk lewat realtime atau laporan WhatsApp.</p><button class="btn ghost sm" data-a="m_sync" style="margin:0">Kirim ke semua HP sekarang</button></div>`:""}''',
    '''""}''')
rep('''${can("subSet")?`<h3 style="margin-top:22px">Jenis paket</h3>${PK.length?''',
    '''${!can("subSet")&&PK.length?`<h3 style="margin-top:22px">Jenis paket</h3><div class="list">${PK.filter(p=>p.on!==false).map(p=>`<div class="mrow"><span class="li" style="cursor:default"><span><b>${esc(p.name)}</b><small class="mute">${rp(p.price)} · ${p.items.map(i=>esc(i.n)+" ×"+i.q).join(", ")} · ${p.days?p.days+" hari":"tanpa batas waktu"}</small></span></span></div>`).join("")}</div>${can("subSell")?"":`<p class="note">Untuk menjual paket dari akun ini, minta Owner menyalakan <b>Jual paket langganan</b> di Atur → Tim & PIN.</p>`}`:""}
  ${can("subSet")?`<h3 style="margin-top:22px">Jenis paket</h3>${hubNote()}${PK.length?''')

# ------------------------------------------------------------------ 5. Peringatan: Owner di HP yang belum memakai Kunci Owner
rep('''  return `<div class="greet"><div><h2>Atur toko</h2>''', '''  return `${hubNote()}<div class="greet"><div><h2>Atur toko</h2>''')
rep('''  return `<div class="mhero"><div><p class="eyebrow">Menu & resep</p>''', '''  return `${hubNote()}<div class="mhero"><div><p class="eyebrow">Menu & resep</p>''')

# ------------------------------------------------------------------ 6. Sambung ulang otomatis lebih tahan banting (kunci tim baru belum sampai)
rep("""async function acctHeal(u){
  if(!u||!SRVU()||Date.now()-healAt<15000)return;healAt=Date.now();const ph=String(u.ph||"");if(!ph.startsWith("pb2$"))return;
  try{const r=await api("/login",{m:"POST",body:{id:u.id,d:ph.split("$")[2]}});
    if(r.s===200&&r.j&&r.j.code){await acctJoin(r.j.code,r.j.team);if(me){render();toast("HP ini tersambung lagi ke tim 521",1)}syncKick();return}
    if(r.s===401){teamBad=true;if(me&&me.id===u.id){logout();toast("Akun ini sudah dihapus atau PIN-nya diganti Owner. Masuk dengan nama & PIN terbaru.")}}
  }catch(e){}}""", """async function acctHeal(u,n){
  n=n||0;if(!u||!SRVU())return;const ph=String(u.ph||"");if(!ph.startsWith("pb2$"))return;
  const later=ms=>{if(n<8){clearTimeout(acctHeal.t);acctHeal.t=setTimeout(()=>{if(teamBad||!C().teamCode)acctHeal(u,n+1)},ms)}};
  if(Date.now()-healAt<4000){later(5000);return}healAt=Date.now();
  try{const r=await api("/login",{m:"POST",body:{id:u.id,d:ph.split("$")[2]}});
    if(r.s===200&&r.j&&r.j.code){try{await acctJoin(r.j.code,r.j.team)}catch(e){later(7000);return}if(me){render();toast("HP ini tersambung lagi ke tim 521",1)}syncKick();return}
    if(r.s===401){teamBad=true;if(me&&me.id===u.id){logout();toast("Akun ini sudah dihapus atau PIN-nya diganti Owner. Masuk dengan nama & PIN terbaru.")}return}
    later(15000);
  }catch(e){later(15000)}}""")
rep('if(teamBad)return;teamBad=true;if(me)acctHeal(me);else if(!$("#login").hidden)loginView()}',
    'if(teamBad){if(me)acctHeal(me);return}teamBad=true;if(me)acctHeal(me);else if(!$("#login").hidden)loginView()}')
rep('D.cfg.acctSig="";menuAuto(0);acctAuto();return true}', 'D.cfg.acctSig="";acctPush();menuAuto(1500);return true}')

# ------------------------------------------------------------------ Blok baru
NEW = r'''
/*V11-PATCH*/
/* Owner masuk di HP yang belum memakai Kunci Owner: perubahan menu/paket/akun hanya tersimpan di HP ini */
function hubNote(){if(!own()||isHub()||!SRVU()||!C().teamCode)return"";
  return `<div class="hubn">${ic("alert")}<span><b>Perubahan dari HP ini belum dikirim ke HP lain</b>Menu, jenis paket, akun, dan pengaturan yang diubah di sini hanya tersimpan di HP ini. Ubah dari HP Owner, atau jadikan HP ini HP Owner dengan Kunci Owner.<br><button class="btn ghost sm" data-a="setsub" data-v="sinkron">Jadikan HP Owner</button></span></div>`}
/* Data yang diterbitkan HP Owner (menu, akun, jenis paket, Chat 521, notifikasi) langsung diambil HP tim lain */
var kQuickF=0,kHotBusy=false;
function kCast(){try{if(RM)RM.emit("_k",{dev:DEV}).catch(()=>{})}catch(e){}}
function kQuick(f){if(!(AR&&kcan))return false;PUBK.store=PUBK.store||{};f(PUBK);kQuickF=1;menuAuto(0);return true}
async function kHot(){
  if(kHotBusy||!SRVU()||!window.A521||!A521.kRev||kdirty||(isHub()&&(msBusy||kQuickF)))return;kHotBusy=true;
  try{const r=await api("/k?since="+A521.kRev());if(r.s!==200||!r.j||!r.j.k||!(r.j.rev>A521.kRev())||kdirty)return;
    await A521.kSet(r.j.rev,r.j.k);
    K=r.j.k;K.store=K.store||{};K.posts=Array.isArray(K.posts)?K.posts:[];K.menu=Array.isArray(K.menu)?K.menu:[];
    K_BASE=kHash(JSON.stringify(K));PUBK=JSON.parse(JSON.stringify(K));
    await teamPull();
    try{fgSchedule()}catch(e){}try{const L=nfSounds();if(L.length&&A521.soundSync)A521.soundSync(L.map(x=>x.f))}catch(e){}
    if(!chatOn())try{chatClose()}catch(e){}
    if(!$("#pub").hidden)pubRender();else if(me&&$("#m").hidden){const a=document.activeElement;if(!(a&&/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName))){const y=window.scrollY;render();window.scrollTo(0,y)}}
  }catch(e){}finally{kHotBusy=false}}
'''
rep("/*V10-PATCH*/\n/* ===== Akun tim & sinkron otomatis", NEW + "/*V10-PATCH*/\n/* ===== Akun tim & sinkron otomatis")

P.write_text(s)
print("OK, perubahan 11 (jam pengingat ganda, sinkron jenis paket & Chat 521 cepat, kotak HP lain dihapus) diterapkan.")
