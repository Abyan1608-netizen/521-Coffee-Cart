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
  await ctx.addInitScript(()=>{window.__nat=[];window.A521Native={postMessage(s){const m=JSON.parse(s);window.__nat.push(m.m);if(m.m==='kStore')window.__kstore(m.a.text);const r=m.m==='notifStatus'?{id:m.id,ok:true,r:{perm:true,brand:'samsung',strict:false,battery:true,sdk:34}}:{id:m.id,ok:true};setTimeout(()=>this.onmessage&&this.onmessage({data:JSON.stringify(r)}),5)},onmessage:null};try{localStorage.setItem("a521hp","1");localStorage.setItem("a521npa","-1")}catch(e){}});
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
  console.log("1) Simpan = langsung terbit, tanpa tombol Terbitkan");
  await O.evaluate(()=>{tab="kabar";render()});await W(300);
  ok(await O.evaluate(()=>!document.querySelector('[data-a=kpublish]')&&!/Terbitkan/.test(document.querySelector('#v').innerText)),"tab Kabar tanpa tombol/teks Terbitkan");
  const r0=(await (await fetch(SRV+"/k")).json()).rev;
  await O.evaluate(()=>{K.posts.unshift({id:"p-uji",type:"promo",title:"Beli 2 Gratis 1",body:"Khusus hari ini",badge:"Hari ini",start:"",end:""});kChanged()});
  let pub=0;for(let i=0;i<20&&!pub;i++){await W(500);const r=await (await fetch(SRV+"/k")).json();if(r.rev>r0&&r.k.posts.some(p=>p.id==="p-uji"))pub=1}
  ok(pub,"promo baru langsung terbit tanpa menekan apa pun");await W(800);
  const st=await O.evaluate(()=>({d:kdirty,txt:document.querySelector('.kst')&&document.querySelector('.kst').textContent,busy:kPubBusy}));
  ok(!st.d&&!st.busy&&/Tersimpan & sudah terlihat/.test(st.txt||""),"status tidak tersangkut: "+JSON.stringify(st));
  await O.screenshot({path:SHOT+"s16_kabar.png"});
  console.log("2) HP kasir menerima promo saat aplikasi terbuka");
  let ann=null;for(let i=0;i<20&&!ann;i++){await W(500);ann=await K2.evaluate(()=>{const t=document.querySelector('#toast');return (K.posts||[]).some(p=>p.id==="p-uji")?{t:t&&t.textContent,snd:window.__nat.includes('playSound'),sync:window.__nat.includes('kabarSync')}:null})}
  ok(ann&&/Promo baru: Beli 2 Gratis 1/.test(ann.t||"")&&ann.snd&&ann.sync,"pemberitahuan + suara di HP kasir: "+JSON.stringify(ann));
  console.log("3) Jam notifikasi pelanggan");
  await O.evaluate(()=>{tab="set";setSub="notif";render()});await W(400);
  const pr=O.locator('.nfc[data-nfk=promo]');
  ok(await pr.locator('.nfnowc').isChecked(),"promo: 'Kirim langsung saat diterbitkan' aktif secara bawaan");
  for(const t of ['07:00','12:00','16:30']){await pr.locator('.nftin').fill(t);await pr.locator('[data-a=nftadd]').click();await W(150)}
  const dk=O.locator('.nfc[data-nfk=diskon]');await dk.locator('.nftin').fill('10:00');await dk.locator('[data-a=nftadd]').click();await W(150);await dk.locator('[data-a=nftdel]').click();await W(150);
  await O.locator('.nfc[data-nfk=kabar] .nfnowc').uncheck();
  await pr.scrollIntoViewIfNeeded();await O.screenshot({path:SHOT+"s16_notif.png"});
  await O.click('[data-a=nfsave]');await W(3500);
  const n=await O.evaluate(()=>{const c=nfCfg();return{p:c.promo.times,pn:c.promo.now,d:c.diskon.times,kn:c.kabar.now}});
  ok(JSON.stringify(n)==='{"p":["07:00","12:00","16:30"],"pn":1,"d":[],"kn":0}',"tersimpan: "+JSON.stringify(n));
  const sv=(await (await fetch(SRV+"/k")).json()).k.store.notif;ok(sv&&JSON.stringify(sv.promo.times)==='["07:00","12:00","16:30"]'&&sv.kabar.now===0,"terkirim ke server untuk HP pelanggan");
  ok(await O.evaluate(()=>!kdirty&&!kPubBusy),"tidak tersangkut setelah Simpan");
  console.log(fails?`\nADA ${fails} YANG GAGAL`:"\nSEMUA LULUS");await b.close();
})();
