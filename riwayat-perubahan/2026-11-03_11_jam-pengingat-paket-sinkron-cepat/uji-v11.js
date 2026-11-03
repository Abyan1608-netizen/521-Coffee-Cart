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
  await newUser(O,"Suma","barista","2468");await newUser(O,"Owner Dua","owner","5210");await W(7000);
  const K2=await mk(b,'KASIR');await K2.goto('http://127.0.0.1:8099/index.html');await W(2500);await acctLogin(K2,"suma","2468");
  const O2=await mk(b,'OWNER2');await O2.goto('http://127.0.0.1:8099/index.html');await W(2500);await acctLogin(O2,"owner dua","5210");
  ok(await K2.evaluate(()=>me&&me.name==="Suma")&&await O2.evaluate(()=>me&&me.name==="Owner Dua"),"kasir & owner kedua masuk");
  await W(4000);
  console.log("1) Kotak 'Dari HP lain hari ini'");
  await O.evaluate(()=>{tab="dash";render()});await W(300);
  ok(!(await O.evaluate(()=>/Dari HP lain hari ini/.test(document.body.innerText))),"kotak tidak tampil lagi di Ringkasan Owner");
  console.log("2) Jenis paket sampai cepat");
  const t0=Date.now();
  await O.evaluate(()=>{C().subPk.push({id:"pk1",name:"Paket wisata",price:10000,items:[{p:"*",n:"Menu bebas",q:10}],days:30,on:true});save()});
  let tK=0,tO2=0;for(let i=0;i<40&&(!tK||!tO2);i++){await W(500);
    if(!tK&&await K2.evaluate(()=>(C().subPk||[]).some(p=>p.id==="pk1")))tK=Date.now()-t0;
    if(!tO2&&await O2.evaluate(()=>(C().subPk||[]).some(p=>p.id==="pk1")))tO2=Date.now()-t0}
  ok(tK&&tK<12000,`jenis paket muncul di HP kasir dalam ${(tK/1000).toFixed(1)} dtk`);ok(tO2&&tO2<12000,`dan di HP owner kedua dalam ${(tO2/1000).toFixed(1)} dtk`);
  await K2.evaluate(()=>{tab="mem";render()});await W(400);
  const kt=await K2.evaluate(()=>document.body.innerText);ok(/Paket wisata/.test(kt)&&/Jual paket langganan/.test(kt),"HP kasir melihat daftar jenis paket + petunjuk izin jual paket");
  await K2.screenshot({path:SHOT+"s11_paket_kasir.png"});
  await O2.evaluate(()=>{tab="set";setSub="";render()});await W(300);ok(await O2.evaluate(()=>!!document.querySelector(".hubn")),"owner kedua (tanpa Kunci Owner) diberi peringatan");
  await O2.screenshot({path:SHOT+"s11_owner2.png"});
  console.log("3) Chat 521 dimatikan di HP Owner");
  ok(await K2.evaluate(()=>chatOn()),"awal: chat aktif di kasir");
  const t1=Date.now();await O.evaluate(()=>{tab="set";setSub="chat";render()});await W(300);await O.click('[data-a=chatoff]');
  let tc=0;for(let i=0;i<40&&!tc;i++){await W(500);if(!(await K2.evaluate(()=>chatOn())))tc=Date.now()-t1}
  ok(tc&&tc<12000,`chat mati di HP kasir dalam ${(tc/1000).toFixed(1)} dtk`);ok(!(await O.evaluate(()=>kdirty)),"HP Owner tidak menyisakan 'belum terbit'");
  console.log("4) Jam pengingat lebih dari satu");
  await O.evaluate(()=>{tab="set";setSub="notif";render()});await W(400);
  const ex=O.locator('.nfc[data-nfk=exp]');
  await ex.locator('.nftin').fill('10:00');await ex.locator('[data-a=nftadd]').click();await W(200);
  await ex.locator('.nftin').fill('15:00');await ex.locator('[data-a=nftadd]').click();await W(200);
  await ex.locator('.nftin').fill('10:00');await ex.locator('[data-a=nftadd]').click();await W(200);
  await ex.locator('.tchip >> nth=0').scrollIntoViewIfNeeded();await O.screenshot({path:SHOT+"s11_jam.png"});
  await O.click('[data-a=nfsave]');await W(3000);
  const tms=await O.evaluate(()=>nfCfg().exp.times);ok(JSON.stringify(tms)==='["08:00","10:00","15:00"]',"jam tersimpan: "+tms);
  let tn=0;for(let i=0;i<30&&!tn;i++){await W(500);if((await K2.evaluate(()=>nfCfg().exp.times.length))===3)tn=1}ok(tn,"jam pengingat ikut ke HP kasir");
  const items=await K2.evaluate(()=>{let got=null;const o=A521.notify;A521.notify=x=>{got=x};
    D.fg=[{id:"bx",p:"palm",n:"Palm Sugar",q:4,q0:4,made:ymd(new Date()),exp:ymd(new Date(Date.now()+2*864e5)),at:"",by:"",ok:1}];fgSchedule();A521.notify=o;return got.map(x=>x.id+"@"+new Date(x.at).toTimeString().slice(0,5))});
  ok(items.length===3,"HP kasir menjadwalkan 3 pengingat untuk 1 batch: "+items.join(", "));
  console.log(fails?`\nADA ${fails} YANG GAGAL`:"\nSEMUA LULUS");await b.close();
})();
