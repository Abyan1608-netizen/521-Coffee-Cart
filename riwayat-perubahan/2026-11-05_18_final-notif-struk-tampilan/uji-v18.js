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
  await ctx.addInitScript(()=>{window.__nat=[];window.A521Native={postMessage(s){const m=JSON.parse(s);window.__nat.push(m.m);(window.__natA=window.__natA||[]).push(m);if(m.m==='kStore')window.__kstore(m.a.text);if(m.m.startsWith('bt')){const B=window.__bt=window.__bt||{addr:'',name:'',printed:[],fail:'',perm:true,on:false};let r={id:m.id,ok:true};
  const st=()=>({supported:true,on:B.on,perm:B.perm,locOff:false,addr:B.addr,name:B.name,connected:!!B.addr,scanning:false});
  if(m.m==='btState')r.r=st();
  if(m.m==='btPrepare'){B.on=true;r.r=st()}
  if(m.m==='btScan'){const D=[{ev:'dev',addr:'11:22:33:44:55:66',name:'Headphone Budi',bonded:true,le:false,printer:false},{ev:'dev',addr:'AA:BB:CC:DD:EE:01',name:'RPP02N',bonded:false,le:false,printer:true},{ev:'dev',addr:'AA:BB:CC:DD:EE:02',name:'MPT-II',bonded:true,le:false,printer:true}];
    D.forEach((d,i)=>setTimeout(()=>window.__a521bt(JSON.stringify(d)),60*(i+1)));setTimeout(()=>window.__a521bt(JSON.stringify({ev:'done'})),400)}
  if(m.m==='btConnect'){B.addr=m.a.addr;B.name=m.a.addr==='AA:BB:CC:DD:EE:02'?'MPT-II':'RPP02N';r.r={name:B.name}}
  if(m.m==='btPrint'){if(!B.addr)r={id:m.id,ok:false,e:'no_printer'};else if(B.fail)r={id:m.id,ok:false,e:B.fail};else B.printed.push(m.a.data)}
  if(m.m==='btForget'){B.addr='';B.name=''}
  setTimeout(()=>this.onmessage&&this.onmessage({data:JSON.stringify(r)}),5);return}
const r=m.m==='notifStatus'?{id:m.id,ok:true,r:{perm:true,brand:'samsung',strict:false,battery:true,sdk:34,last:Date.now()-5*60000,version:'1.5.0',off:[],push:true,pushSub:true}}:m.m==='kabarSync'?{id:m.id,ok:true,r:{sent:1,perm:window.__perm!==false}}:m.m==='notifyTest'?{id:m.id,ok:true,r:{sent:true}}:{id:m.id,ok:true};setTimeout(()=>this.onmessage&&this.onmessage({data:JSON.stringify(r)}),5)},onmessage:null};try{localStorage.setItem("a521hp","1");localStorage.setItem("a521npa","-1")}catch(e){}});
  const p=await ctx.newPage();p.__ctx=ctx;p.on('pageerror',e=>{console.log(name,'PAGEERR',e.message);fails++});
  p.on('console',m=>{if(m.type()==='error'&&!/40[1349]|423|Failed to load resource/.test(m.text()))console.log(name,'ERR',m.text().slice(0,200))});return p}
async function localLogin(p,id,pin){await p.evaluate(()=>showLogin());await W(300);await p.evaluate(v=>{lsel=v;loginView()},id);
  for(const d of pin)await p.click(`[data-a=kp][data-v="${d}"]`);await W(1500)}
async function acctLogin(p,name,pin){await p.evaluate(()=>showLogin());await W(400);await p.fill('#acn',name);await p.fill('#acp',pin);await p.click('[data-a=acgo]');await W(800);try{await p.waitForFunction(()=>me||!acBusy,null,{timeout:40000})}catch(e){}await W(2500)}
const st=p=>p.evaluate(()=>({fg:D.fg.filter(b=>b.q>0).map(b=>b.n+":"+b.q).sort().join(", "),susu:(ing("su")||{}).qty,sq:(D.sq||[]).length,code:C().teamCode,bad:teamBad,me:me&&me.name}));
async function newUser(O,name,role,pin){await O.evaluate(()=>{tab="set";setSub="tim";render()});await W(200);await O.click('[data-a=newu]');await W(300);
  await O.fill('#u-name',name);if(role!=="barista"){await O.click(`[data-a=urole][data-v=${role}]`);await W(200)}await O.fill('#u-pin',pin);await O.click('[data-a=usave]');await W(900)}




const dec=b=>Buffer.from(b,'base64');
const has=(buf,arr)=>{for(let i=0;i<=buf.length-arr.length;i++){let k=0;while(k<arr.length&&buf[i+k]===arr[k])k++;if(k===arr.length)return true}return false};
(async()=>{
  const b=await chromium.launch(ARGS);
  const O=await mk(b,'OWNER');await O.goto('http://127.0.0.1:8099/index.html');await W(2500);
  await localLogin(O,'own','1234');await O.fill('#u-pin','8642');await O.click('[data-a=usave]');await W(900);
  await O.evaluate(k=>{localStorage.setItem('a521owner',k);localStorage.setItem('a521ownerOk','1')},KEY);await O.reload();await W(2500);
  await localLogin(O,'own','8642');await W(4000);
  console.log("1) Atur → Printer: cari & pilih printer");
  await O.evaluate(()=>{tab="set";setSub="printer";render()});await W(500);
  ok(/Belum memilih printer/.test(await O.evaluate(()=>document.querySelector('#btset').innerText)),"status awal: belum memilih printer");
  await O.click('[data-a=btfind]');await W(900);
  const names=await O.evaluate(()=>[...document.querySelectorAll('#btsh [data-a=btpick] b')].map(x=>x.textContent));
  ok(JSON.stringify(names)==='["MPT-II","RPP02N","Headphone Budi"]',"printer diurutkan paling atas (yang sudah dipasangkan dulu): "+JSON.stringify(names));
  await O.screenshot({path:SHOT+"s18_pilih_printer.png"});
  await O.click('[data-a=btpick][data-v="AA:BB:CC:DD:EE:02"]');await W(1500);
  const pr=await O.evaluate(()=>window.__bt.printed.length);ok(pr===1,"tersambung → cetak tes otomatis");
  const t1=dec(await O.evaluate(()=>window.__bt.printed[0]));
  ok(t1[0]===27&&t1[1]===64,"diawali ESC @ (reset printer)");
  ok(has(t1,[29,118,48,0]),"logo 521 dicetak (GS v 0)");
  ok(has(t1,[27,33,48])&&t1.toString('latin1').includes('521 Coffee Cart'),"nama toko besar");
  ok(t1.toString('latin1').includes('TES-PRINTER'),"isi struk tes");
  ok(has(t1,[29,86,66,0]),"perintah potong kertas di akhir");
  ok(/MPT-II/.test(await O.evaluate(()=>document.querySelector('#btset')?document.querySelector('#btset').innerText:document.body.innerText)),"status: Printer MPT-II");
  await O.evaluate(()=>{tab="set";setSub="printer";render()});await W(500);await O.screenshot({path:SHOT+"s18_atur_printer.png"});
  console.log("2) Jual → tombol Printer di layar Lunas");
  await O.evaluate(()=>{shut();const p=D.prod.find(x=>x.active);cart={[p.id]:2};pm="Transfer";pay()});await W(700);
  await O.click('[data-a=copyp]');await W(900);
  const t2=dec(await O.evaluate(()=>window.__bt.printed.at(-1))).toString('latin1');
  ok(/TOTAL/.test(t2)&&/Transfer/.test(t2)&&/Kasir: /.test(t2)&&/2 x Rp/.test(t2),"struk penjualan terkirim ke printer");
  {const tx=t2.replace(/\x1d\x76\x30\x00[\s\S]*?\n(?=\x1b!0)/,"").replace(/\x1b[@ta!dE](.)?|\x1dVB\x00/g,"");const bad=tx.split('\n').filter(l=>l.length>32);ok(!bad.length,"lebar baris ≤ 32 huruf (kertas 58 mm) "+JSON.stringify(bad))}
  console.log("3) Kertas 80 mm, tanpa logo");
  await O.evaluate(()=>{shut();const c=C();c.paper=48;c.plogo=false;save();tab="set";setSub="printer";render()});await W(300);
  await O.click('[data-a=bttest2]');await W(800);const t3=dec(await O.evaluate(()=>window.__bt.printed.at(-1)));
  ok(!has(t3,[29,118,48,0])&&t3.toString('latin1').split('\n').some(l=>l.length===48),"80 mm: baris 48 huruf, tanpa logo");
  console.log("4) Cetak otomatis setelah bayar");
  await O.evaluate(()=>{const c=C();c.paper=32;c.plogo=true;c.pauto=true;save()});const n0=await O.evaluate(()=>window.__bt.printed.length);
  await O.evaluate(()=>{const p=D.prod.find(x=>x.active);cart={[p.id]:1};pm="Transfer";pay()});await W(1500);
  ok(await O.evaluate(()=>window.__bt.printed.length)===n0+1,"struk keluar sendiri setelah bayar");
  console.log("5) Printer mati → pesan jelas + struk tersalin");
  await O.evaluate(()=>{window.__bt.fail='io';});await O.click('[data-a=copyp]');await W(900);
  ok(/Printer tidak merespons/.test(await O.evaluate(()=>(document.querySelector('#toast')||{}).textContent)),"pesan printer tidak merespons");
  await O.evaluate(()=>{window.__bt.fail='';shut()});
  console.log("6) Lupakan printer → tombol Printer membuka pilihan printer");
  await O.evaluate(()=>{tab="set";setSub="printer";render()});await W(400);await O.click('[data-a=btforget]');await W(500);
  await O.evaluate(()=>{const c=C();c.pauto=false;save();const p=D.prod.find(x=>x.active);cart={[p.id]:1};pm="Transfer";pay()});await W(600);
  await O.click('[data-a=copyp]');await W(900);
  ok(await O.evaluate(()=>!!document.querySelector('#btsh')),"lembar Pilih printer terbuka");
  await O.click('[data-a=btpick][data-v="AA:BB:CC:DD:EE:01"]');await W(1500);
  const t6=dec(await O.evaluate(()=>window.__bt.printed.at(-1))).toString('latin1');
  ok(/TOTAL/.test(t6)&&!/TES-PRINTER/.test(t6),"setelah memilih, struk transaksi itu langsung dicetak");
  console.log("7) Atur → Website");
  await O.evaluate(()=>{shut();tab="set";setSub="web";render()});await W(400);
  await O.fill('[data-wf="hero.title"]','Kopi *jujur*\nuntuk kamu.');await O.fill('[data-wf="strip"]','Satu\nDua');
  await O.locator('[data-ws=testi]').uncheck();await O.screenshot({path:SHOT+"s18_atur_web.png"});
  await O.click('[data-a=websave]');let sv=null;for(let i=0;i<20&&!sv;i++){await W(500);const r=await (await fetch(SRV+"/k")).json();if(r.k.store.web)sv=r.k.store.web}
  ok(sv&&sv.hero.title==='Kopi *jujur*\nuntuk kamu.'&&JSON.stringify(sv.strip)==='["Satu","Dua"]'&&sv.show.testi===false,"teks website terbit ke server: "+JSON.stringify(sv));
  const kj=await (await fetch(SRV+"/kdata.js")).text();ok(/"web":\{"hero"/.test(kj)&&!/"team"/.test(kj),"/kdata.js untuk website berisi teks website, tanpa data tim");
  console.log("8) Notifikasi: perubahan promo ikut dikabari (bawaan)");
  ok(await O.evaluate(()=>nfCfg().edit===1),"bawaan: ubah promo juga dikabari");
  await O.evaluate(()=>{tab="set";setSub="notif";render()});await W(400);
  ok(await O.evaluate(()=>document.querySelector('#nfedit').checked),"kotak centang 'saat diubah' tercentang");
  await O.click('[data-a=hpsheet]');await W(700);
  ok(/Notifikasi instan aktif/.test(await O.evaluate(()=>document.querySelector('#m').innerText)),"Cek notifikasi: status notifikasi instan");
  await O.evaluate(()=>shut());
  console.log("9) HP Owner: kotak 'Dari HP lain hari ini' tidak ada");
  await O.evaluate(()=>{tab="dash";render()});await W(400);
  ok(!/Dari HP lain hari ini/i.test(await O.evaluate(()=>document.body.innerText)),"tidak tampil");
  console.log(fails?`\nADA ${fails} YANG GAGAL`:"\nSEMUA LULUS");await b.close();
})();
