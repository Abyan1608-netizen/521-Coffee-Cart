s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:90],s.count(a)); s=s.replace(a,b)
# ---- login markup
rep('''    <div class="users" id="ulist"></div>''','''    <div id="tjoin"></div>
    <div class="users" id="ulist"></div>''')
# ---- login with hashed PIN
rep('''function tryLogin(force){
  const u=D.users.find(x=>x.id===lsel);if(!u)return;
  if(buf===u.pin){me=u;''','''let tlN=0;
async function tryLogin(force){
  const u=D.users.find(x=>x.id===lsel);if(!u)return;const n=++tlN,b=buf;
  let okp=u.pin!=null&&u.pin!==""?b===u.pin:false;if(!okp&&u.ph&&b)okp=(await sha256h("521|"+u.id+"|"+b))===u.ph;
  if(n!==tlN||b!==buf)return;
  if(okp){me=u;''')
rep('''const u=D.users.find(x=>x.id===lsel);if(u&&buf===u.pin)tryLogin()}''','''const u=D.users.find(x=>x.id===lsel);if(u&&(buf===u.pin||u.ph))tryLogin()}''')
# ---- cart keep across reloads
rep('''  b.innerHTML=`${typeof pxSwap==="function"?pxSwap(24,4,.6''','''  try{if(me)sessionStorage.setItem("pos521c",JSON.stringify({u:me.id,cart,disc,paid,pm,ch,vch,tab}))}catch(e){}
  b.innerHTML=`${typeof pxSwap==="function"?pxSwap(24,4,.6''')
rep('''function logout(){me=null;cart={};disc=0;paid=0;showDisc=false;try{sessionStorage.removeItem("pos521u")}catch(e){}''','''function logout(){me=null;cart={};disc=0;paid=0;showDisc=false;try{sessionStorage.removeItem("pos521u");sessionStorage.removeItem("pos521c")}catch(e){}''')
rep('''$("#wav").textContent=ini(me.name);$("#wnm").textContent=me.name;tab="pos";render();window.scrollTo(0,0)}''','''$("#wav").textContent=ini(me.name);$("#wnm").textContent=me.name;tab="pos";
  try{const sv=JSON.parse(sessionStorage.getItem("pos521c")||"null");if(sv&&sv.u===me.id){cart=Object.fromEntries(Object.entries(sv.cart||{}).filter(([k])=>prod(k)));disc=+sv.disc||0;paid=+sv.paid||0;if(sv.pm)pm=sv.pm;if(sv.ch)ch=sv.ch;vch=sv.vch||"";if(sv.tab)tab=sv.tab}}catch(e){}
  render();window.scrollTo(0,0)}''')
# ---- team sync core (before kChanged)
js=r'''
/* ===== Sinkron semua HP =====
   HP Owner (akun Claude pemilik) mengunci data tim — menu, resep, kategori, bahan, akun & PIN (di-hash), pilihan kasir, QRIS —
   dengan KODE TIM (AES-GCM), lalu menyematkannya di halaman yang diterbitkan. HP lain yang membuka link + memasukkan kode tim
   mengambil data itu otomatis. Pelanggan tanpa kode hanya melihat menu publik, kabar, dan promo. Stok & transaksi tetap per HP. */
const TCFG=["name","sub","foot","color","ch","pm","ec","qk","qris","cats"];
let teamReady=false,teamBad=false;
const u8b64=u=>{let s="";for(let i=0;i<u.length;i+=0x8000)s+=String.fromCharCode.apply(null,u.subarray(i,i+0x8000));return btoa(s)};
const b64u8=b=>Uint8Array.from(atob(b),c=>c.charCodeAt(0));
async function sha256h(t){const h=await crypto.subtle.digest("SHA-256",new TextEncoder().encode(t));return [...new Uint8Array(h)].map(x=>x.toString(16).padStart(2,"0")).join("")}
async function tKey(code,salt){const km=await crypto.subtle.importKey("raw",new TextEncoder().encode(String(code).trim().toUpperCase()),"PBKDF2",false,["deriveKey"]);
  return crypto.subtle.deriveKey({name:"PBKDF2",salt,iterations:120000,hash:"SHA-256"},km,{name:"AES-GCM",length:256},false,["encrypt","decrypt"])}
const teamSrc=()=>!K.team||(!!C().teamCode&&(C().teamRev||0)>=K.team.rev);
function teamCore(){const c=C(),cfg={};TCFG.forEach(k=>{if(c[k]!==undefined)cfg[k]=c[k]});
  return{prod:D.prod,ing:D.ing.map(g=>{const x=Object.assign({},g);delete x.qty;return x}),cfg,
    users:D.users.map(u=>({id:u.id,name:u.name,role:u.role,title:u.title,perm:u.perm,pms:u.pms,k:u.pin!=null&&u.pin!==""?"p"+kHash(u.id+"|"+u.pin):u.ph}))}}
const teamSig=()=>kHash(JSON.stringify(teamCore()));
const teamDirty=()=>!!(C().teamCode&&teamSrc()&&teamSig()!==((K.team||{}).sig));
async function teamBundle(){const core=teamCore(),sig=kHash(JSON.stringify(core));
  core.users=await Promise.all(D.users.map(async u=>({id:u.id,name:u.name,role:u.role,title:u.title,perm:u.perm,pms:u.pms,ph:u.pin!=null&&u.pin!==""?await sha256h("521|"+u.id+"|"+u.pin):u.ph})));
  const salt=crypto.getRandomValues(new Uint8Array(16)),iv=crypto.getRandomValues(new Uint8Array(12)),key=await tKey(C().teamCode,salt);
  const ct=new Uint8Array(await crypto.subtle.encrypt({name:"AES-GCM",iv},key,new TextEncoder().encode(JSON.stringify(core))));
  return{v:1,rev:Date.now(),sig,salt:u8b64(salt),iv:u8b64(iv),ct:u8b64(ct)}}
async function teamOpen(code,T){const key=await tKey(code,b64u8(T.salt));const pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:b64u8(T.iv)},key,b64u8(T.ct));return JSON.parse(new TextDecoder().decode(pt))}
function teamApply(o,T){
  const qty=Object.fromEntries(D.ing.map(g=>[g.id,g.qty||0]));
  D.prod=o.prod||D.prod;D.ing=(o.ing||[]).map(g=>Object.assign({},g,{qty:qty[g.id]||0}));
  Object.assign(D.cfg,o.cfg||{});D.cfg.defpin=0;
  if(Array.isArray(o.users)&&o.users.some(u=>u.role==="owner")){D.users=o.users.map(u=>{const x={id:u.id,name:u.name,role:u.role,ph:u.ph};if(u.title)x.title=u.title;if(u.perm)x.perm=u.perm;if(u.pms)x.pms=u.pms;return x});
    if(me){const nu=D.users.find(u=>u.id===me.id);if(nu)me=nu;else{logout()}}}
  D.cfg.teamRev=T.rev;D.cfg.teamAt=new Date().toISOString();
  Object.keys(cart).forEach(k=>{if(!prod(k))delete cart[k]});
  try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}look();
}
async function teamPull(){
  try{const T=K.team;if(T&&C().teamCode&&(C().teamRev||0)<T.rev){const o=await teamOpen(C().teamCode,T);teamApply(o,T);teamBad=false;
      if(me){render();toast("Menu & data tim diperbarui dari Owner",1)}else if(!$("#login").hidden)loginView()}}
  catch(e){teamBad=true;if(!$("#login").hidden)loginView()}
  teamReady=true;
}
async function teamJoin(){const i=$("#tcode"),code=(i&&i.value||"").trim().toUpperCase();if(!code){if(i)i.focus();return}
  if(!K.team){toast("Owner belum mengaktifkan sinkron tim.");return}
  const b=$("[data-a=tjoin]");if(b){b.disabled=true;b.textContent="Menyambungkan…"}
  try{const o=await teamOpen(code,K.team);D.cfg.teamCode=code;teamApply(o,K.team);teamBad=false;teamReady=true;toast("HP ini tersambung ke tim 521",1);
    if(me)render();else loginView()}
  catch(e){toast("Kode tim belum cocok. Cek lagi ke Owner.");if(b){b.disabled=false;b.textContent="Sambungkan"}}
}
const genCode=()=>{const A="ABCDEFGHJKMNPQRSTUVWXYZ23456789",r=crypto.getRandomValues(new Uint8Array(8));return "521-"+[...r].map((x,i)=>(i===4?"-":"")+A[x%A.length]).join("")};
function teamJoinCard(){
  if(!K.team)return"";
  if(C().teamCode&&!teamBad)return `<p class="tok">${ic("check")}HP ini tersambung ke tim 521${C().teamAt?` · diperbarui ${new Date(C().teamAt).toLocaleString("id-ID",{day:"numeric",month:"short",hour:"2-digit",minute:"2-digit"})}`:""}</p>`;
  return `<div class="tjoin"><b>${teamBad?"Kode tim sudah diganti Owner":"Sambungkan HP ini ke tim 521"}</b><small>Masukkan kode tim dari Owner sekali saja. Setelah itu menu, resep, akun, dan PIN ikut terbarui otomatis.</small><div class="add"><input id="tcode" placeholder="521-XXXX-XXXX" autocapitalize="characters" autocomplete="off" spellcheck="false" aria-label="Kode tim"><button class="btn sm" data-a="tjoin" style="margin:0">Sambungkan</button></div></div>`;
}
'''
i=s.index("function kChanged(){");s=s[:i]+js.lstrip("\n")+s[i:]
# kSync includes team
rep('''function kSync(){try{return JSON.stringify(menuSnap())!==JSON.stringify(K.menu||[])''','''function kSync(){try{if(K.team&&!teamSrc())return false;return teamDirty()||JSON.stringify(menuSnap())!==JSON.stringify(K.menu||[])''')
# kMenuPublish: add team + readiness
rep('''  if(msBusy||!AR||!kcan||!me||!kSync())return;''','''  if(msBusy||!AR||!kcan||!me||!teamReady||!kSync())return;''')
rep('''pub.store.name=C().name;pub.store.tagline=C().sub;
  const nb=kHash(JSON.stringify(pub));''','''pub.store.name=C().name;pub.store.tagline=C().sub;
  if(C().teamCode&&teamSrc()&&teamDirty()){try{pub.team=await teamBundle()}catch(e){msBusy=false;return}}
  const nb=kHash(JSON.stringify(pub));''')
rep('''    if(kdirty){K.menu=pub.menu;K.store.name=pub.store.name;K.store.tagline=pub.store.tagline;''','''    if(pub.team)K.team=pub.team;
    if(kdirty){K.menu=pub.menu;K.store.name=pub.store.name;K.store.tagline=pub.store.tagline;''')
rep('''    await AR.publish(kDoc(pub));PUBK=pub;K_BASE=nb;''','''    await AR.publish(kDoc(pub));PUBK=pub;K_BASE=nb;if(pub.team){D.cfg.teamRev=pub.team.rev;D.cfg.teamAt=new Date().toISOString();try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}}''')
rep('''    toast("Menu di halaman pelanggan sudah ikut diperbarui",1);''','''    toast(pub.team?"Semua HP tim & halaman pelanggan sudah diperbarui":"Menu di halaman pelanggan sudah ikut diperbarui",1);''')
# kPublish: keep team / menu if not source; include fresh bundle if source
rep('''  K.store.name=C().name;K.store.tagline=C().sub;K.menu=menuSnap();
  try{sessionStorage.removeItem("k521-pending")}catch(e){}''','''  K.store.name=C().name;K.store.tagline=C().sub;
  if(!K.team||teamSrc())K.menu=menuSnap();
  if(C().teamCode&&teamSrc()&&teamDirty()){try{K.team=await teamBundle()}catch(e){}}
  try{sessionStorage.removeItem("k521-pending")}catch(e){}''')
rep('''kdirty=false;PUBK=JSON.parse(JSON.stringify(K));K_BASE=kHash(JSON.stringify(K));''','''kdirty=false;PUBK=JSON.parse(JSON.stringify(K));K_BASE=kHash(JSON.stringify(K));if(K.team&&C().teamCode){D.cfg.teamRev=K.team.rev;D.cfg.teamAt=new Date().toISOString();try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}}''')
# login view card
rep('''  $("#lgreet").textContent=greet();''','''  $("#lgreet").textContent=greet();const tj=$("#tjoin");if(tj)tj.innerHTML=teamJoinCard();''')
# login-phase action
rep('''  if(a==="kgo"){tryLogin(true);return}''','''  if(a==="kgo"){tryLogin(true);return}
  if(a==="tjoin"){teamJoin();return}''')
# settings folder
rep('''  ["tim","user","Tim & PIN",''','''  ["sinkron","phone","Sinkron semua HP",()=>!K.team?"Belum aktif · menu & akun hanya di HP ini":C().teamCode&&teamSrc()?(teamDirty()?"Ada perubahan, sedang dikirim…":"Aktif · semua HP tim memakai data ini"):"Masukkan kode tim untuk tersambung"],
  ["tim","user","Tim & PIN",''')
rep('''OWNF=["tim","data","log"];''','''OWNF=["tim","data","log","sinkron"];''')
rep('''if(setSub&&!own()&&["tim","data","log"].includes(setSub))setSub="";''','''if(setSub&&!own()&&["tim","data","log","sinkron"].includes(setSub))setSub="";''')
rep('''  if(id==="intro"){''','''  if(id==="sinkron"){const T=K.team,src=teamSrc();
    if(T&&!src)return `<p class="note" style="margin-top:0">Tim 521 sudah memakai sinkron, tapi HP ini belum tersambung atau datanya lebih lama. Masukkan kode tim supaya HP ini memakai menu & akun yang sama.</p>${teamJoinCard()}`;
    if(!AR||!kcan)return `<p class="note" style="margin-top:0">Sinkron hanya bisa diaktifkan dari HP yang membuka aplikasi dengan akun Claude pemilik halaman (akun Kakak).</p>`;
    if(!C().teamCode)return `<p class="note" style="margin-top:0">Aktifkan supaya HP barista, reseller, dan owner lain memakai <b>menu, harga, resep, kategori, akun & PIN, pilihan kasir, dan QRIS</b> yang sama dengan HP ini. Setiap Kakak mengubahnya, semua HP ikut terbarui otomatis.</p>
      <div class="tsteps"><p><b>1</b>Tekan Aktifkan, aplikasi membuat <b>kode tim</b>.</p><p><b>2</b>Bagikan link aplikasi + kode tim ke tim.</p><p><b>3</b>Di HP mereka: buka link → Masuk → isi kode tim sekali → login dengan PIN masing-masing.</p></div>
      <button class="btn" data-a="tson">Aktifkan sinkron semua HP</button>
      <p class="note">Kabar & promo sudah otomatis terlihat di semua HP yang membuka link. Stok dan catatan transaksi tetap tersimpan per HP.</p>`;
    return `<div class="tcode"><small>Kode tim</small><b id="tcv">${esc(C().teamCode)}</b><button class="btn ghost sm" data-a="tcopy" style="margin:0">${ic("copy")}Salin kode + link</button></div>
      <div class="statusbox${teamDirty()?" closed":""}"><i></i>${teamDirty()?"Ada perubahan yang sedang dikirim ke semua HP…":`Semua HP tim sudah memakai data terbaru${C().teamAt?` · ${new Date(C().teamAt).toLocaleString("id-ID",{day:"numeric",month:"short",hour:"2-digit",minute:"2-digit"})}`:""}`}</div>
      <div class="tsteps"><p><b>1</b>Bagikan link aplikasi + kode tim ke barista, reseller, dan owner lain.</p><p><b>2</b>Di HP mereka: buka link → Masuk → isi kode tim sekali.</p><p><b>3</b>Login dengan PIN masing-masing (atur di Tim & PIN).</p></div>
      <p class="note">Yang ikut tersinkron: menu, harga, status Habis, resep & takaran, kategori, bahan (tanpa jumlah stok), akun & PIN, hak akses, pilihan kasir, QRIS. Kabar & promo juga terlihat di semua HP. Pelanggan tanpa kode tetap hanya melihat menu publik, kabar, dan promo.</p>
      <p class="note">Ubah menu & akun dari HP ini. Perubahan dari HP karyawan hanya tersimpan di HP mereka.</p>
      <button class="btn ghost" data-a="tsync">Kirim ulang sekarang</button><button class="btn ghost" data-a="tnew" style="color:var(--warn)">Buat kode tim baru</button>`}
  if(id==="intro"){''')
rep('''  else if(a==="kpi")kpiSheet(v);''','''  else if(a==="kpi")kpiSheet(v);
  else if(a==="tson"&&own()){if(!AR||!kcan)return;D.cfg.teamCode=genCode();lg("Sinkron tim","Diaktifkan");save();render();toast("Kode tim dibuat. Mengirim data ke semua HP…",1);menuAuto(0)}
  else if(a==="tsync"&&own()){menuAuto(0);toast("Mengirim…",1)}
  else if(a==="tnew"&&own()){confirmSheet("Buat kode tim baru?","Kode lama berhenti berlaku. Semua HP karyawan perlu memasukkan kode baru sekali lagi.","tnewgo","Buat kode baru","Batal","x")}
  else if(a==="tnewgo"&&own()){D.cfg.teamCode=genCode();D.cfg.teamRev=0;lg("Sinkron tim","Kode baru dibuat");save();shut();render();menuAuto(0);toast("Kode baru dibuat. Bagikan ke tim.",1)}
  else if(a==="tcopy"&&own()){const t=`Aplikasi 521 Coffee Cart: ${C().promo||location.href}\\nKode tim: ${C().teamCode}\\nBuka link → Masuk → isi kode tim → login dengan PIN masing-masing.`;try{navigator.clipboard.writeText(t).then(()=>toast("Kode + link tersalin",1),()=>toast(C().teamCode))}catch(e){toast(C().teamCode)}}''')
css='''/* ---------- Sinkron tim ---------- */
.tjoin{display:grid;gap:6px;margin:0 0 14px;padding:14px;border-radius:16px;background:color-mix(in srgb,var(--ac) 10%,var(--sf));border:1px solid color-mix(in srgb,var(--ac) 40%,var(--line))}
.tjoin small{color:var(--mute)}.tjoin .add{margin-top:4px}.tjoin input{margin:0;text-transform:uppercase;font-family:var(--f-m);letter-spacing:.06em}
.tok{display:flex;align-items:center;gap:8px;margin:0 0 12px;font-size:13px;font-weight:600;color:var(--ok)}.tok svg{width:16px;height:16px}
.tcode{display:grid;gap:8px;justify-items:start;padding:16px;border-radius:18px;background:var(--sf2);border:1px dashed color-mix(in srgb,var(--ac) 60%,var(--line));margin-bottom:12px}
.tcode small{font:700 11px var(--f-b);letter-spacing:.14em;text-transform:uppercase;color:var(--mute)}
.tcode b{font:700 30px var(--f-m);letter-spacing:.06em;user-select:all}
.tsteps{display:grid;gap:8px;margin:12px 0}
.tsteps p{display:flex;gap:10px;align-items:flex-start;margin:0;font-size:14px}
.tsteps p > b{flex:none;width:24px;height:24px;border-radius:50%;display:grid;place-items:center;background:var(--ac);color:var(--on);font:700 13px var(--f-m)}
'''
k=s.index("/* ---------- Welcome ---------- */");s=s[:k]+css+s[k:]
# boot: pull team
rep('''if(me)enter();else if(location.hash==="#masuk")showLogin();else{showPub();welcome()}''','''if(me)enter();else if(location.hash==="#masuk")showLogin();else{showPub();welcome()}
teamPull();''')
open('p3.src.html','w').write(s);print("ok")
