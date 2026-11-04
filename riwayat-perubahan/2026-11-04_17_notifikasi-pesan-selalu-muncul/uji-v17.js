const {chromium,devices}=require('playwright');
const SRV="http://127.0.0.1:8787",KEY="kunci-owner-rahasia-123",SHOT="/home/claude/work/v10/";
const ARGS={args:['--disable-features=LocalNetworkAccessChecks,LocalNetworkAccessChecksWebSockets,PrivateNetworkAccessSendPreflights,PrivateNetworkAccessRespectPreflightResults,BlockInsecurePrivateNetworkRequests']};
const W=ms=>new Promise(r=>setTimeout(r,ms));
let fails=0;const ok=(c,msg)=>{console.log((c?"  ✔ ":"  ✘ GAGAL: ")+msg);if(!c)fails++};
async function mk(b,name){const ctx=await b.newContext({...devices['Pixel 7']});
  await ctx.route('**/shim.js',async r=>{const res=await r.fetch();let t=await res.text();t=t.replace(/server:"[^"]*"/,`server:"${SRV}"`).replace('.replace(/^http/,"ws")+"/room/"','.replace(/^http/,"ws").replace("8787","8788")+"/room/"');r.fulfill({response:res,body:t})});
  await ctx.route('**/index.html',async r=>{const res=await r.fetch();let t=await res.text();t=t.replace(/connect-src [^;]*;/,`connect-src 'self' ${SRV} ws://127.0.0.1:8788;`);r.fulfill({response:res,body:t})});
  let kbody=null;
  await ctx.route('**/kdata.js',async r=>{if(kbody)return r.fulfill({body:kbody,contentType:'text/javascript'});r.continue()});
  await ctx.exposeFunction('__kstore',t=>{kbody=t});
  await ctx.addInitScript(()=>{window.__nat=[];window.A521Native={postMessage(s){const m=JSON.parse(s);window.__nat.push(m.m);(window.__natA=window.__natA||[]).push(m);if(m.m==='kStore')window.__kstore(m.a.text);const r=m.m==='notifStatus'?{id:m.id,ok:true,r:{perm:true,brand:'samsung',strict:false,battery:true,sdk:34,last:Date.now()-5*60000,version:'1.4.1',off:['Diskon']}}:m.m==='kabarSync'?{id:m.id,ok:true,r:{sent:1,perm:window.__perm!==false}}:m.m==='notifyTest'?{id:m.id,ok:true,r:{sent:true}}:{id:m.id,ok:true};setTimeout(()=>this.onmessage&&this.onmessage({data:JSON.stringify(r)}),5)},onmessage:null};try{localStorage.setItem("a521hp","1");localStorage.setItem("a521npa","-1")}catch(e){}});
  const p=await ctx.newPage();p.__ctx=ctx;p.on('pageerror',e=>{console.log(name,'PAGEERR',e.message);fails++});
  p.on('console',m=>{if(m.type()==='error'&&!/40[1349]|423|Failed to load resource/.test(m.text()))console.log(name,'ERR',m.text().slice(0,200))});return p}
async function localLogin(p,id,pin){await p.evaluate(()=>showLogin());await W(300);await p.evaluate(v=>{lsel=v;loginView()},id);
  for(const d of pin)await p.click(`[data-a=kp][data-v="${d}"]`);await W(1500)}
async function acctLogin(p,name,pin){await p.evaluate(()=>showLogin());await W(400);await p.fill('#acn',name);await p.fill('#acp',pin);await p.click('[data-a=acgo]');await W(800);try{await p.waitForFunction(()=>me||!acBusy,null,{timeout:40000})}catch(e){}await W(2500)}
const st=p=>p.evaluate(()=>({fg:D.fg.filter(b=>b.q>0).map(b=>b.n+":"+b.q).sort().join(", "),susu:(ing("su")||{}).qty,sq:(D.sq||[]).length,code:C().teamCode,bad:teamBad,me:me&&me.name}));
async function newUser(O,name,role,pin){await O.evaluate(()=>{tab="set";setSub="tim";render()});await W(200);await O.click('[data-a=newu]');await W(300);
  await O.fill('#u-name',name);if(role!=="barista"){await O.click(`[data-a=urole][data-v=${role}]`);await W(200)}await O.fill('#u-pin',pin);await O.click('[data-a=usave]');await W(900)}



(async()=>{
  const b=await chromium.launch(ARGS);
  const O=await mk(b,'OWNER');await O.goto('http://127.0.0.1:8099/index.html');await W(2500);
  await localLogin(O,'own','1234');await O.fill('#u-pin','8642');await O.click('[data-a=usave]');await W(900);
  await O.evaluate(k=>{localStorage.setItem('a521owner',k);localStorage.setItem('a521ownerOk','1')},KEY);await O.reload();await W(2500);
  await localLogin(O,'own','8642');await W(5000);
  await newUser(O,"Suma","barista","2468");await W(6000);
  const K2=await mk(b,'KASIR');await K2.goto('http://127.0.0.1:8099/index.html');await W(2500);await acctLogin(K2,"suma","2468");await W(3000);
  const P=await mk(b,'PELANGGAN');await P.goto('http://127.0.0.1:8099/index.html');await W(4000);
  ok(await P.evaluate(()=>!me&&!$("#pub").hidden),"HP pelanggan di halaman umum (tanpa login)");
  const syncs=p=>p.evaluate(()=>(window.__natA||[]).filter(m=>m.m==='kabarSync').map(m=>!!(m.a&&m.a.quiet)));
  await O.evaluate(()=>window.__natA=[]);await K2.evaluate(()=>window.__natA=[]);await P.evaluate(()=>window.__natA=[]);
  console.log("1) Owner menerbitkan promo");
  await O.evaluate(()=>{K.posts.unshift({id:"p-17",type:"promo",title:"Kopi Susu 10rb",body:"Hari ini saja",badge:"Hari ini",start:"",end:""});kChanged()});
  let pub=0;for(let i=0;i<20&&!pub;i++){await W(500);const r=await (await fetch(SRV+"/k")).json();if(r.k.posts.some(p=>p.id==="p-17"))pub=1}
  ok(pub,"promo terbit");await W(1500);
  const os=await syncs(O);ok(os.length>=1&&os.every(q=>q===true),"HP Owner (penerbit) hanya menandai, tidak memberi notifikasi ke diri sendiri: "+JSON.stringify(os));
  console.log("2) HP kasir (aplikasi terbuka): notifikasi HP sungguhan, bukan hanya suara");
  let ann=null;for(let i=0;i<40&&!ann;i++){await W(500);ann=await K2.evaluate(()=>(K.posts||[]).some(p=>p.id==="p-17")?{t:(document.querySelector('#toast')||{}).textContent,snd:window.__nat.includes('playSound'),sync:(window.__natA||[]).filter(m=>m.m==='kabarSync').map(m=>!!(m.a&&m.a.quiet))}:null)}
  ok(ann&&/Kopi Susu 10rb/.test(ann.t||""),"tulisan pemberitahuan di aplikasi: "+JSON.stringify(ann&&ann.t));
  ok(ann&&!ann.snd,"tidak lagi membunyikan suara saja (suara ikut notifikasi HP)");
  await W(800);const ks=await syncs(K2);ok(ks.includes(false),"Android diminta mengirim notifikasi (kabarSync tanpa quiet): "+JSON.stringify(ks));
  console.log("3) HP pelanggan (aplikasi terbuka, tanpa tim) ikut menerima dalam ±30 detik");
  let pc=null;for(let i=0;i<80&&!pc;i++){await W(500);pc=await P.evaluate(()=>(K.posts||[]).some(p=>p.id==="p-17")?{t:(document.querySelector('#toast')||{}).textContent,card:!!document.querySelector('#pub')&&/Kopi Susu 10rb/.test(document.querySelector('#pub').innerText)}:null)}
  ok(pc&&pc.card,"promo tampil di halaman pelanggan tanpa membuka ulang: "+JSON.stringify(pc));
  await W(800);const ps=await syncs(P);ok(ps.includes(false),"HP pelanggan meminta Android mengirim notifikasi: "+JSON.stringify(ps));
  console.log("4) Notifikasi HP mati → diberi tahu");
  await K2.evaluate(()=>{window.__perm=false;kAnnounce([{id:"x",type:"promo",title:"Tes",dval:0}])});await W(600);
  ok(/Notifikasi HP ini mati/.test(await K2.evaluate(()=>(document.querySelector('#toast')||{}).textContent)),"peringatan bila izin notifikasi mati");
  console.log("5) Atur → Notifikasi → Cek: status & tombol uji");
  await O.evaluate(()=>{tab="set";setSub="notif";render()});await W(400);
  await O.click('[data-a=hpsheet]');await W(800);
  const sh=await O.evaluate(()=>document.querySelector('#m').innerText);
  ok(/Cek promo otomatis terakhir: 5 menit lalu/.test(sh)&&/versi aplikasi 1\.4\.1/.test(sh),"status cek otomatis & versi tampil");
  ok(/Dimatikan di pengaturan HP: Diskon/.test(sh),"jenis notifikasi yang dimatikan di HP ditampilkan");
  await O.screenshot({path:SHOT+"s17_cek.png"});
  await O.evaluate(()=>window.__natA=[]);await O.click('[data-a=nftest]');await W(600);
  const tm=await O.evaluate(()=>(window.__natA||[]).find(m=>m.m==='notifyTest'));
  ok(tm&&/Uji notifikasi/.test(tm.a.title)&&tm.a.body&&tm.a.type==="promo","tombol uji mengirim notifikasi uji: "+JSON.stringify(tm&&tm.a));
  ok(/Notifikasi uji dikirim/.test(await O.evaluate(()=>(document.querySelector('#toast')||{}).textContent)),"pesan konfirmasi uji");
  console.log(fails?`\nADA ${fails} YANG GAGAL`:"\nSEMUA LULUS");await b.close();
})();
