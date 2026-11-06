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





const WEB="https://abyan1608-netizen.github.io/521-Coffee-Cart-Web/";
const G='/tmp/claude-0/-home-claude/ff7c566e-7b36-53ac-96e7-ed70e572208b/scratchpad/gsap/node_modules/gsap/dist/';
const fs=require('fs');
/* website & API asli dialihkan ke salinan lokal: website (8097) dan server uji (8787) */
async function webRoutes(ctx){
  await ctx.route(WEB+'**',async r=>{const u=new URL(r.request().url());const f=u.pathname.replace('/521-Coffee-Cart-Web','')||'/';
    const res=await fetch('http://127.0.0.1:8097'+(f==='/'?'/index.html':f));r.fulfill({status:res.status,body:Buffer.from(await res.arrayBuffer()),contentType:res.headers.get('content-type')||'text/html'})});
  await ctx.route('https://coffee521-api.coffee521.workers.dev/**',async r=>{const u=new URL(r.request().url());const res=await fetch(SRV+u.pathname);
    r.fulfill({status:res.status,body:Buffer.from(await res.arrayBuffer()),contentType:res.headers.get('content-type')||'application/octet-stream'})});
  await ctx.route('https://cdnjs.cloudflare.com/**',r=>{const f=r.request().url().split('/').pop();r.fulfill({contentType:'text/javascript',body:fs.readFileSync(G+f)})});
}
/* sama persis dengan MainActivity.siteJs() */
const siteJs=k=>`(function(){try{if(!document.getElementById('a521app')){var b=document.createElement('a');b.id='a521app';b.href="https:\\/\\/appassets.androidplatform.net\\/app\\/index.html#masuk";b.textContent=${JSON.stringify(k?"← Kembali ke kasir":"Masuk")};b.setAttribute('style','position:fixed;left:12px;bottom:14px;z-index:2147483000;display:inline-flex;align-items:center;height:44px;padding:0 18px;border-radius:999px;background:#fff;color:#0a0a0a;font:800 15px/1 system-ui,sans-serif;text-decoration:none;box-shadow:0 6px 22px rgba(0,0,0,.4);border:2px solid #0a0a0a');document.body.appendChild(b)}return getComputedStyle(document.body).backgroundColor}catch(e){return ''}})()`;
(async()=>{
  const b=await chromium.launch(ARGS);
  const O=await mk(b,'OWNER');await webRoutes(O.__ctx);
  console.log("1) Aplikasi dibuka tanpa login → yang tampil website 521 (bukan halaman Kabar lama)");
  await O.goto('http://127.0.0.1:8099/index.html');await W(4000);
  ok(O.url().startsWith(WEB)&&!/dari=kasir/.test(O.url()),"pindah ke website: "+O.url());
  ok(await O.evaluate(()=>!!document.querySelector('.hero')&&!!document.querySelector('[data-sec=menu]')),"tampilan website lengkap (hero & menu)");
  const bg=await O.evaluate(siteJs(false));
  ok(/rgb/.test(bg)&&await O.evaluate(()=>document.getElementById('a521app').textContent==='Masuk'),"tombol Masuk dari aplikasi tampil, warna bilah HP = "+bg);
  await O.screenshot({path:SHOT+"s21_site_masuk.png"});
  console.log("2) Tanpa internet (#luring) → halaman Kabar tersimpan di aplikasi tetap tampil");
  await O.goto('http://127.0.0.1:8099/index.html#luring');await W(2500);
  ok(O.url().startsWith('http://127.0.0.1:8099')&&await O.evaluate(()=>!$("#pub").hidden),"halaman Kabar aplikasi tampil saat luring");
  console.log("3) Tombol Masuk → login Owner");
  await O.goto('about:blank');await O.goto('http://127.0.0.1:8099/index.html#masuk');await W(2500);
  ok(O.url().startsWith('http://127.0.0.1:8099')&&await O.evaluate(()=>!$("#login").hidden),"layar Masuk tampil (tidak dialihkan ke website)");
  await localLogin(O,'own','1234');await O.fill('#u-pin','8642');await O.click('[data-a=usave]');await W(900);
  await O.evaluate(k=>{localStorage.setItem('a521owner',k);localStorage.setItem('a521ownerOk','1')},KEY);await O.reload();await W(2500);
  await localLogin(O,'own','8642');await W(4000);
  ok(await O.evaluate(()=>!!me&&me.role==='owner'),"Owner masuk");
  console.log("4) Tab Kabar: tambah promo & jadikan headline website");
  await O.evaluate(()=>{tab="kabar";render()});await W(500);
  ok(/tampil di website 521/.test(await O.evaluate(()=>document.querySelector('.greet').innerText)),"keterangan tab Kabar menyebut website");
  ok(await O.evaluate(()=>!!document.querySelector('[data-a=kview]')&&/Lihat di website/.test(document.querySelector('[data-a=kview]').textContent)),"tombol 'Lihat di website'");
  await O.click('[data-a=knew][data-v=promo]');await W(500);
  ok(await O.evaluate(()=>/Headline website/.test(document.querySelector('#s').innerText)),"pilihan Headline website ada di lembar promo");
  await O.fill('#p-title','Nobar Final Liga LIPIA');await O.fill('#p-body','Ramein bareng 521!');
  await O.click('[data-a=khead][data-v="1"]');await W(300);
  ok(await O.evaluate(()=>document.querySelector('[data-a=khead][data-v="1"]').getAttribute('aria-pressed')==='true'&&$('#p-title').value==='Nobar Final Liga LIPIA'),"Jadikan headline terpilih, isian tidak hilang");
  await O.screenshot({path:SHOT+"s21_post_headline.png",fullPage:true});
  await O.click('[data-a=ksavep]');await W(800);
  const pid=await O.evaluate(()=>K.posts.find(p=>p.title==='Nobar Final Liga LIPIA').id);
  ok(await O.evaluate(id=>K.store.web.news.headMode==='pick'&&K.store.web.news.headId===id&&!('_head' in K.posts.find(p=>p.id===id)),pid),"tersimpan: headline = promo ini");
  await O.click('[data-a=knew][data-v=news]');await W(400);await O.fill('#p-title','Kabar biasa');await O.click('[data-a=ksavep]');await W(800);
  console.log("5) Atur → Website: headline & kartu menu");
  await O.evaluate(()=>{tab="set";setSub="web";render()});await W(600);
  ok(await O.evaluate(id=>document.querySelector('[data-wh]').value==='p:'+id,pid),"pilihan headline di Atur → Website = promo tadi");
  const prods=await O.evaluate(()=>D.prod.filter(p=>p.active).map(p=>({id:p.id,n:p.name,auto:[p.cat,p.size].filter(Boolean).join(" · ")})));
  ok(prods.length>=3&&await O.evaluate(n=>document.querySelectorAll('[data-wm]').length===n,prods.length),"semua menu aktif tampil di Kartu menu ("+prods.length+")");
  ok(await O.evaluate(a=>document.querySelector('[data-wm] [data-wn]').textContent===(a||"(kosong)"),prods[0].auto),"keterangan otomatis terlihat: "+prods[0].auto);
  const c0=`[data-wm="${prods[0].id}"]`,c1=`[data-wm="${prods[1].id}"]`;
  await O.fill(c0+' [data-wl]','Kopi Susu Botol · 250 ml');await W(200);
  ok(await O.evaluate(s=>document.querySelector(s+' [data-wn]').textContent==='Kopi Susu Botol · 250 ml',c0),"pratinjau 'Tampil:' ikut berubah saat mengetik");
  await O.check(c1+' [data-wx]');await W(200);
  ok(await O.evaluate(s=>document.querySelector(s+' [data-wl]').disabled&&/tanpa keterangan/.test(document.querySelector(s+' [data-wn]').textContent),c1),"Tanpa keterangan: kolom terkunci");
  await O.setInputFiles(c0+' [data-wi]','/home/claude/proj/521-coffee-app/assets/hero.jpg');await W(2500);
  ok(await O.evaluate(s=>{const i=document.querySelector(s+' .wmc-ph img');return !!i&&i.complete&&i.naturalWidth>0&&i.naturalWidth<=1350&&i.naturalHeight<=1350},c0),"foto dipilih, diperkecil, pratinjau tampil");
  await O.screenshot({path:SHOT+"s21_atur_web.png",fullPage:true});
  await O.click('[data-a=websave]');await W(1200);
  ok(await O.evaluate(a=>{const m=K.store.web.mi;return m[a[0]].lb==='Kopi Susu Botol · 250 ml'&&/^data:image\/jpeg|^media\//.test(m[a[0]].img)&&m[a[1]].lb===""&&!m[a[2]]},prods.map(p=>p.id)),"tersimpan per menu (keterangan, foto, tanpa keterangan)");
  ok(await O.evaluate(id=>K.store.web.news.headMode==='pick'&&K.store.web.news.headId===id,pid),"headline tidak hilang setelah simpan");
  console.log("6) Terbit ke server");
  let kd=null;for(let i=0;i<40;i++){await W(1000);const t=await (await fetch(SRV+'/kdata.js')).text();const m=/window.__K=(.*);$/.exec(t);if(m){const k=JSON.parse(m[1]);if(k.store&&k.store.web&&k.store.web.mi&&(k.menu||[]).some(x=>x.lb)){kd=k;break}}}
  ok(!!kd,"data terbit");
  if(kd){const m0=kd.menu.find(x=>x.n===prods[0].n),m1=kd.menu.find(x=>x.n===prods[1].n),m2=kd.menu.find(x=>x.n===prods[2].n);
    ok(m0.lb==='Kopi Susu Botol · 250 ml'&&/^media\/[a-f0-9]{32}\.jpg$/.test(m0.img),"menu 1: keterangan + foto (file media) → "+m0.img);
    ok(m1.lb===""&&!m1.img,"menu 2: tanpa keterangan");ok(!('lb' in m2)&&!m2.img,"menu 3: otomatis kategori · ukuran");
    ok(kd.store.web.news.headId===pid,"headline ikut terbit");
    ok(!JSON.stringify(kd).includes('data:image'),"tidak ada foto mentah (base64) di data terbit")}
  console.log("7) Website menampilkan persis seperti di aplikasi");
  const Wp=await b.newPage({...devices['Pixel 7']});await webRoutes(Wp.context());Wp.on('pageerror',e=>{console.log('WEB PAGEERR',e.message);fails++});
  await Wp.goto('http://127.0.0.1:8097/index.html');await W(5000);
  const card=n=>Wp.evaluate(n=>{const f=[...document.querySelectorAll('.pc')].find(x=>x.querySelector('.pc-n').textContent===n);return f?{sub:f.querySelector('.pc-sub').textContent,img:(f.querySelector('.pc-in img')||{}).src||'',ok:!!f.querySelector('.pc-in img')}:null},n);
  const w0=await card(prods[0].n),w1=await card(prods[1].n),w2=await card(prods[2].n);
  ok(w0&&w0.sub==='Kopi Susu Botol · 250 ml',"kartu 1 keterangan: "+(w0&&w0.sub));
  ok(w0&&/coffee521-api.*\/media\/[a-f0-9]{32}\.jpg/.test(w0.img),"kartu 1 foto dari aplikasi");
  await Wp.evaluate(()=>document.querySelector('[data-sec=menu]').scrollIntoView());await W(1500);
  ok(await Wp.evaluate(n=>{const f=[...document.querySelectorAll('.pc')].find(x=>x.querySelector('.pc-n').textContent===n);const i=f.querySelector('.pc-in img');return i.complete&&i.naturalWidth>0},prods[0].n),"foto kartu 1 termuat");
  ok(w1&&w1.sub==='',"kartu 2 tanpa keterangan");
  ok(w2&&w2.sub===prods[2].auto,"kartu 3 = kategori · ukuran dari aplikasi: "+(w2&&w2.sub));
  const hd=await Wp.evaluate(()=>{const t=document.querySelector('.nh-t');return t?t.textContent:''});
  ok(hd==='Nobar Final Liga LIPIA',"headline website: "+hd);
  await Wp.evaluate(()=>document.querySelector('.nh-t').scrollIntoView({block:'center'}));await W(1200);await Wp.screenshot({path:SHOT+"s21_web_headline.png"});
  await Wp.evaluate(n=>{const f=[...document.querySelectorAll('.pc')].find(x=>x.querySelector('.pc-n').textContent===n);f.scrollIntoView({block:'center'})},prods[0].n);await W(1500);await Wp.screenshot({path:SHOT+"s21_web_card.png"});
  console.log("8) Headline diganti ke 'Otomatis' dari Atur → Website");
  await O.evaluate(()=>{tab="set";setSub="web";render()});await W(500);await O.selectOption('[data-wh]','auto');await O.click('[data-a=websave]');await W(800);
  ok(await O.evaluate(()=>K.store.web.news.headMode==='auto'&&!K.store.web.news.headId),"mode otomatis tersimpan");
  await O.evaluate(()=>{tab="set";setSub="web";render()});await W(400);await O.click('[data-a=websave]');await W(600);
  ok(await O.evaluate(()=>K.store.web.news.headMode==='auto'),"simpan ulang tanpa mengubah pilihan → tetap otomatis");
  ok(await O.evaluate(()=>K.store.web.mi&&Object.keys(K.store.web.mi).length===2),"pengaturan kartu menu tetap ada");
  await O.evaluate(()=>{tab="kabar";render()});await W(400);
  await O.evaluate(id=>{kp=JSON.parse(JSON.stringify(K.posts.find(p=>p.id===id)));kPostSheet()},pid);await W(300);
  ok(await O.evaluate(()=>document.querySelector('[data-a=khead][data-v="0"]').getAttribute('aria-pressed')==='true'),"lembar promo: bukan headline lagi");
  await O.evaluate(()=>shut());
  console.log("9) Owner 'Lihat di website' → website dengan tombol Kembali ke kasir");
  await O.click('[data-a=kview]');await W(3500);
  ok(O.url().startsWith(WEB)&&/dari=kasir/.test(O.url()),"website dibuka: "+O.url());
  await O.evaluate(siteJs(true));ok(await O.evaluate(()=>/Kembali ke kasir/.test(document.getElementById('a521app').textContent)),"tombol 'Kembali ke kasir'");
  await O.goto('about:blank');await O.goto('http://127.0.0.1:8099/index.html#masuk');await W(2500);
  ok(await O.evaluate(()=>!!me&&!$("#app").hidden),"kembali ke kasir tanpa login ulang");
  console.log(fails?`\nHASIL: ${fails} GAGAL`:"\nHASIL: SEMUA LULUS");await b.close();process.exit(fails?1:0)})();
