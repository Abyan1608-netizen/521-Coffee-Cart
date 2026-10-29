s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a)); s=s.replace(a,b)
# ids
rep('data-a="copyr" data-id="${tx.no}"','data-a="copyr" data-id="${txKey(tx)}"')
rep('data-a="copyp" data-id="${tx.no}"','data-a="copyp" data-id="${txKey(tx)}"')
rep('data-a="void" data-id="${t.no}"','data-a="void" data-id="${txKey(t)}"')
rep('else if(a==="copyr"){const t=D.tx.find(x=>x.no===id);','else if(a==="copyr"){const t=txFind(id);')
rep('else if(a==="copyp"){const t=D.tx.find(x=>x.no===id);','else if(a==="copyp"){const t=txFind(id);')
rep('const id2=$("#s").dataset.v,t=D.tx.find(x=>x.no===id2),','const id2=$("#s").dataset.v,t=txFind(id2),')
rep('t.status="cancelled";t.reason=r;applyUse(t,1,"void");','t.status="cancelled";t.reason=r;if(!t.rx)applyUse(t,1,"void");t.sent=0;rtSend();')
rep('confirmSheet(`Batalkan transaksi ${id.slice(-4)}?`','confirmSheet(`Batalkan transaksi ${id.split("@")[0].slice(-4)}?`')
# tx gets device id
rep('by:me.name,items,use:us,','by:me.name,dev:DEV,items,use:us,')
rep('''  D.tx.push(tx);applyUse(tx,-1,"sale");C().lastCh=ch;save();''','''  D.tx.push(tx);applyUse(tx,-1,"sale");C().lastCh=ch;save();setTimeout(rtSend,300);''')
# show source in tx list
rep('''<span class="mute" style="font-size:14px">${new Date(t.at).toLocaleTimeString("id-ID",{hour:"2-digit",minute:"2-digit"})}</span>''','''<span class="mute" style="font-size:14px">${new Date(t.at).toLocaleTimeString("id-ID",{hour:"2-digit",minute:"2-digit"})}</span>${t.rx?`<span class="pill">${t.rx==="wa"?"via WA":"HP "+esc(t.by||"tim")}</span>`:""}''')
js=r'''
/* ===== Transaksi karyawan → Owner =====
   1) Realtime: HP karyawan menaruh antrean transaksinya (terkunci kode tim) di "presence" ruang artifact; HP Owner
      (akun Claude pemilik) yang sedang terbuka menyimpannya lalu mengirim tanda terima "txack". Butuh akun Claude yang diundang.
   2) WhatsApp: laporan ringkas + kode terkunci; Owner menempelkan kode di aplikasi. Jalan untuk semua HP. */
const DEV=(()=>{if(!D.cfg.dev){D.cfg.dev=Math.random().toString(36).slice(2,8);try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}}return D.cfg.dev})();
const txKey=t=>t.no+(t.dev?"@"+t.dev:"");
const txFind=id=>D.tx.find(x=>txKey(x)===id)||D.tx.find(x=>x.no===id&&(!x.dev||x.dev===DEV));
let RM=null,rtPeers=[],rtLast=0;
const isHub=()=>!!(AR&&kcan);
async function zpack(obj){const code=C().teamCode;if(!code)throw new Error("nocode");let u=new TextEncoder().encode(JSON.stringify(obj)),z="0";
  try{if(window.CompressionStream){u=new Uint8Array(await new Response(new Blob([u]).stream().pipeThrough(new CompressionStream("deflate-raw"))).arrayBuffer());z="1"}}catch(e){}
  const salt=crypto.getRandomValues(new Uint8Array(16)),iv=crypto.getRandomValues(new Uint8Array(12)),key=await tKey(code,salt);
  const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,u));return z+"."+u8b64(salt)+"."+u8b64(iv)+"."+u8b64(ct)}
async function zopen(str){const code=C().teamCode;const [z,sa,iv,ct]=String(str).split(".");const key=await tKey(code,b64u8(sa));
  let u=new Uint8Array(await crypto.subtle.decrypt({name:"AES-GCM",iv:b64u8(iv)},key,b64u8(ct)));
  if(z==="1")u=new Uint8Array(await new Response(new Blob([u]).stream().pipeThrough(new DecompressionStream("deflate-raw"))).arrayBuffer());
  return JSON.parse(new TextDecoder().decode(u))}
const txSlim=t=>{const x=Object.assign({},t);delete x.sent;delete x.use;return x};
function txMerge(list,src){let n=0,who="";(list||[]).forEach(t=>{if(!t||!t.no||!t.dev||t.dev===DEV)return;who=t.by||who;
  const i=D.tx.findIndex(x=>x.dev===t.dev&&x.no===t.no),nt=Object.assign({},t,{rx:src,rxAt:new Date().toISOString()});
  if(i<0){D.tx.push(nt);n++}else if(JSON.stringify(Object.assign({},D.tx[i],{rx:0,rxAt:0}))!==JSON.stringify(Object.assign({},nt,{rx:0,rxAt:0}))){D.tx[i]=Object.assign(D.tx[i],nt)}});
  D.tx.sort((a,b)=>a.at<b.at?-1:a.at>b.at?1:0);try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}return{n,who}}
const myQueue=()=>D.tx.filter(t=>t.dev===DEV&&!t.sent);
async function rtSend(){
  if(!RM||isHub())return;
  try{const Q=myQueue();if(!Q.length||!C().teamCode){await RM.presence({q:null,who:me?me.name:"",dev:DEV});return}
    let batch=[],pk="";for(const t of Q.slice(0,40)){const tryB=batch.concat([txSlim(t)]),p=await zpack({dev:DEV,tx:tryB});if(p.length>3300&&batch.length)break;batch=tryB;pk=p;if(p.length>3300)break}
    if(pk.length>3600){await RM.presence({q:null,who:me?me.name:"",dev:DEV});return}
    await RM.presence({q:{p:pk,n:Q.length},who:me?me.name:"",dev:DEV});
  }catch(e){}
}
async function rtHubPeers(ch){
  rtPeers=ch.peers.filter(p=>!p.isMe&&p.presence&&p.presence.dev);
  for(const p of ch.joined.concat(ch.updated)){const q=p.presence&&p.presence.q;if(p.isMe||!q||!q.p)continue;
    try{const o=await zopen(q.p);const r=txMerge(o.tx,"rt");RM.emit("txack",{dev:o.dev,ids:(o.tx||[]).map(t=>t.no+"|"+t.status)}).catch(()=>{});
      if(r.n){rtLast=Date.now();if(me&&(tab==="dash"))render();if(me)toast(r.n+" transaksi baru dari "+(r.who||"HP karyawan"),1)}}catch(e){}}
  if(me&&tab==="dash"&&$("#rtlive"))$("#rtlive").innerHTML=rtLiveTxt();
}
function rtLiveTxt(){const on=rtPeers.filter(p=>p.presence.who);return on.length?`${on.length} HP tim online: ${on.map(p=>esc(p.presence.who)).join(", ")}`:"Belum ada HP karyawan yang online"}
async function rtInit(){
  try{if(!window.claude||!claude.use)return;RM=await claude.use("room");if(!RM)return;
    for(let i=0;i<40&&!kcanKnown;i++)await new Promise(r=>setTimeout(r,250));
    if(isHub()){RM.onPeers(ch=>{rtHubPeers(ch)});}
    else{RM.on("txack",m=>{const d=m.data||{};if(d.dev!==DEV||!Array.isArray(d.ids))return;let ch=0;
        D.tx.forEach(t=>{if(t.dev===DEV&&!t.sent&&d.ids.includes(t.no+"|"+t.status)){t.sent=1;ch++}});
        if(ch){try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}if(me&&tab==="dash")render();rtSend()}});
      rtSend();}
  }catch(e){RM=null}
}
/* Laporan WhatsApp */
function waReport(){
  const today=ymd(new Date()),T=D.tx.filter(t=>t.dev===DEV&&t.d===today),ok=T.filter(t=>t.status!=="cancelled"),s=agg(ok);
  const pq={};ok.forEach(t=>t.items.forEach(i=>{pq[i.n]=(pq[i.n]||0)+i.q}));
  return `*Laporan Kasir ${C().name||"521 Coffee"}*\nKasir: ${me?me.name:"-"}\nTanggal: ${new Date().toLocaleDateString("id-ID",{weekday:"long",day:"numeric",month:"long",year:"numeric"})}\n\nOmzet: ${rp(s.rev)} (${s.n} pesanan, ${s.items} cup)\n${Object.entries(s.pm).map(([k,v])=>`${k}: ${rp(v)}`).join("\n")}${T.length-ok.length?`\nDibatalkan: ${T.length-ok.length}`:""}\n\nMenu terjual:\n${Object.entries(pq).map(([k,v])=>`• ${k} ×${v}`).join("\n")||"-"}`;
}
async function waShare(){
  if(!C().teamCode){toast("Sambungkan HP ini ke tim dulu (kode tim dari Owner).");return}
  const today=ymd(new Date()),T=D.tx.filter(t=>t.dev===DEV&&(t.d===today||!t.sent));
  if(!T.length){toast("Belum ada transaksi untuk dilaporkan hari ini.");return}
  let code;try{code=await zpack({dev:DEV,tx:T.map(txSlim)})}catch(e){toast("Laporan belum bisa dibuat.");return}
  const text=waReport()+`\n\nKode untuk aplikasi Owner (salin semua, jangan diubah):\n#521TX:${code}#`;
  D.tx.forEach(t=>{if(T.includes(t))t.wa=1});save();
  try{if(navigator.share){await navigator.share({text});toast("Pilih WhatsApp lalu kirim ke Owner",1);return}}catch(e){if(e&&e.name==="AbortError")return}
  try{await navigator.clipboard.writeText(text);toast("Laporan tersalin. Tempel di chat WhatsApp Owner.",1)}catch(e){show(`<h2>Laporan untuk Owner</h2><p class="note">Salin semua teks ini, lalu kirim ke WhatsApp Owner.</p><textarea class="kt" style="min-height:240px" readonly>${esc(text)}</textarea>`)}
}
function waInSheet(){show(`<h2>Tempel laporan WhatsApp</h2><p class="note">Salin seluruh pesan laporan dari karyawan (yang berisi <b>#521TX:</b>), lalu tempel di sini.</p><textarea class="kt" id="wain" style="min-height:180px" placeholder="Tempel pesan laporan di sini"></textarea><button class="btn" data-a="waingo">Masukkan ke Ringkasan</button>`)}
async function waIn(){const v=($("#wain")||{}).value||"",ms=[...v.matchAll(/#521TX:([0-9A-Za-z+/=.]+)#/g)];if(!ms.length){toast("Kode #521TX tidak ditemukan. Salin seluruh pesannya.");return}
  let n=0,who="",bad=0;for(const m of ms){try{const o=await zopen(m[1]);const r=txMerge(o.tx,"wa");n+=r.n;who=r.who||who}catch(e){bad++}}
  if(bad&&!n){toast("Kode tidak bisa dibuka. Pastikan HP karyawan memakai kode tim yang sama.");return}
  lg("Impor laporan WA",(who||"karyawan")+": "+n+" transaksi");save();shut();render();toast(n?n+" transaksi dari "+(who||"karyawan")+" masuk ke Ringkasan":"Semua transaksi di laporan ini sudah ada",1)}
function teamTxBox(){
  if(isHub()){const today=ymd(new Date()),R=D.tx.filter(t=>t.rx&&t.d===today&&t.status!=="cancelled"),by={};R.forEach(t=>{const k=t.by||"Karyawan";by[k]=by[k]||{n:0,rev:0};by[k].n++;by[k].rev+=t.total});
    return `<div class="sec ttx"><h3>Transaksi HP karyawan hari ini</h3>${RM?`<p class="rtl" id="rtlive"><i></i>${rtLiveTxt()}</p>`:`<p class="note">Realtime aktif bila karyawan membuka aplikasi dengan akun Claude yang Kakak undang lewat email. Tanpa itu, pakai laporan WhatsApp.</p>`}
      ${Object.keys(by).length?Object.entries(by).map(([k,v])=>`<div class="sumr"><span>${esc(k)} · ${v.n} pesanan</span><span>${rp(v.rev)}</span></div>`).join(""):'<p class="note">Belum ada transaksi dari HP karyawan hari ini.</p>'}
      <button class="btn ghost" data-a="wain">${ic("wa")}Tempel laporan WhatsApp</button></div>`}
  const Q=myQueue().length;
  return `<div class="sec ttx"><h3>Kirim ke Owner</h3>${!C().teamCode?'<p class="note">Sambungkan HP ini ke tim (kode tim dari Owner) supaya transaksi bisa dikirim.</p>':RM?`<p class="rtl${Q?" wait":""}"><i></i>${Q?`${Q} transaksi menunggu HP Owner online, terkirim otomatis`:"Semua transaksi sudah diterima Owner"}</p>`:'<p class="note">Kirim otomatis belum aktif di HP ini (perlu masuk dengan akun Claude yang diundang Owner). Kirim laporan lewat WhatsApp saat tutup kasir.</p>'}
    <button class="btn" data-a="wash">${ic("wa")}Kirim laporan via WhatsApp</button></div>`}
'''
i=s.index("function kChanged(){");s=s[:i]+js.lstrip("\n")+s[i:]
# kcanKnown flag
rep('''UAPI=u;AR=ar;try{kcan=!!(u&&await u.canEdit())}catch(x){}}catch(x){}})();''','''UAPI=u;AR=ar;try{kcan=!!(u&&await u.canEdit())}catch(x){}}catch(x){}kcanKnown=true})();
let kcanKnown=false;rtInit();''')
# dashboard insertions
rep('''<h3>Menu terjual</h3>${bars(desc(pq),v=>v+" cup")}${can("exp")?expBox:""}<h3>Transaksi hari ini</h3>${txList(T)}`;''','''${teamTxBox()}<h3>Menu terjual</h3>${bars(desc(pq),v=>v+" cup")}${can("exp")?expBox:""}<h3>Transaksi hari ini</h3>${txList(T)}`;''')
rep('''  <p class="note" style="margin-top:-4px">Ketuk kotak mana saja untuk melihat rincian dan cara hitungnya.</p>''','''  <p class="note" style="margin-top:-4px">Ketuk kotak mana saja untuk melihat rincian dan cara hitungnya.</p>
  ${C().teamCode||isHub()?teamTxBox():""}''')
# actions (pre-gate)
rep('''  else if(a==="kpi")kpiSheet(v);''','''  else if(a==="kpi")kpiSheet(v);
  else if(a==="wash")waShare();
  else if(a==="wain"&&own())waInSheet();
  else if(a==="waingo"&&own())waIn();''')
css='''/* ---------- Transaksi tim ---------- */
.rtl{display:flex;align-items:center;gap:8px;margin:0 0 8px;font-size:13.5px;font-weight:600}
.rtl i{width:9px;height:9px;border-radius:50%;background:var(--ok);box-shadow:0 0 0 0 var(--ok);animation:rtPulse 2s infinite;flex:none}
.rtl.wait i{background:var(--warn);animation:none}
@keyframes rtPulse{0%{box-shadow:0 0 0 0 color-mix(in srgb,var(--ok) 60%,transparent)}70%{box-shadow:0 0 0 8px transparent}100%{box-shadow:0 0 0 0 transparent}}
.ttx .btn{margin-top:10px}
'''
k=s.index("/* ---------- Welcome ---------- */");s=s[:k]+css+s[k:]
open('p3.src.html','w').write(s);print("ok")
