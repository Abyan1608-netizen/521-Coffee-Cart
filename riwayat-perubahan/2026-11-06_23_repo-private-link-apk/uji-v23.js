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
const siteJs=k=>`(function(){try{if(!document.getElementById('a521app')){var b=document.createElement('a');b.id='a521app';b.href="https:\\/\\/appassets.androidplatform.net\\/app\\/index.html#masuk";b.textContent=${JSON.stringify("\u2190 Kembali ke aplikasi")};b.setAttribute('style','position:fixed;left:12px;bottom:14px;z-index:2147483000;display:inline-flex;align-items:center;height:44px;padding:0 18px;border-radius:999px;background:#fff;color:#0a0a0a;font:800 15px/1 system-ui,sans-serif;text-decoration:none;box-shadow:0 6px 22px rgba(0,0,0,.4);border:2px solid #0a0a0a');document.body.appendChild(b)}return getComputedStyle(document.body).backgroundColor}catch(e){return ''}})()`;
(async()=>{
  const b=await chromium.launch(ARGS);const O=await mk(b,'OWNER');await O.__ctx.grantPermissions(['clipboard-read','clipboard-write']);
  await O.goto('http://127.0.0.1:8099/index.html');await W(2500);
  await localLogin(O,'own','1234');await O.fill('#u-pin','8642');await O.click('[data-a=usave]');await W(900);
  await O.evaluate(k=>{localStorage.setItem('a521owner',k);localStorage.setItem('a521ownerOk','1')},KEY);await O.reload();await W(2500);
  await localLogin(O,'own','8642');await W(3000);
  console.log("1) Atur → Sinkron tim: kolom link unduh aplikasi");
  await O.evaluate(()=>{tab="set";setSub="sinkron";render()});await W(500);
  ok(await O.evaluate(()=>!!$("#apklink")&&$("#apklink").value===""),"kolom 'Link unduh aplikasi (APK)' ada, kosong");
  await O.evaluate(()=>{Object.defineProperty(navigator,'share',{value:d=>{window.__sh=d.text;return Promise.resolve()},configurable:true})});
  await O.click('[data-a=tcopy]');await W(600);
  let clip=await O.evaluate(()=>window.__sh||'');
  ok(/Minta file aplikasi 521 Coffee App \(APK\) ke Owner/.test(clip)&&!/github/i.test(clip),"tanpa link: teks meminta APK ke Owner, tanpa link GitHub");
  await O.fill('#apklink','drive.google.com/abc');await O.click('[data-a=tcopy]');await W(500);
  ok(/harus diawali https/.test(await O.evaluate(()=>document.body.innerText)),"link tanpa https ditolak");
  const L='https://drive.google.com/file/d/1AbCdEf/view?usp=sharing';
  await O.fill('#apklink',L);await O.click('[data-a=tcopy]');await W(600);
  clip=await O.evaluate(()=>window.__sh||'');
  ok(clip.startsWith('Pasang aplikasi 521 Coffee App: '+L)&&/Masuk/.test(clip),"teks berisi link Drive: "+clip.split('\n')[0]);
  await O.evaluate(()=>render());await W(300);
  ok(await O.evaluate(l=>$("#apklink").value===l&&C().apkLink===l,L),"link tersimpan di HP ini");
  ok(await O.evaluate(()=>!JSON.stringify(K).includes('drive.google.com')),"link tidak ikut data yang terbit ke website");
  await O.screenshot({path:SHOT+"s23_link.png"});
  console.log(fails?`\nHASIL: ${fails} GAGAL`:"\nHASIL: SEMUA LULUS");await b.close();process.exit(fails?1:0)})();
