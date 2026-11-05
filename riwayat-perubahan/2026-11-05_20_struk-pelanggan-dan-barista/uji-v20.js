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
const count=(buf,arr)=>{let n=0;for(let i=0;i<=buf.length-arr.length;i++){let k=0;while(k<arr.length&&buf[i+k]===arr[k])k++;if(k===arr.length)n++}return n};
/* teks per baris dari byte ESC/POS: buang perintah & gambar logo, catat ukuran huruf tiap baris */
function lines(u){const out=[];let sz=0,bd=0,line="",i=0;const fl=()=>{out.push({t:line,sz,bd});line=""};
  while(i<u.length){const b=u[i];if(b===27){const c=u[i+1];if(c===64){i+=2;continue}if(c===33){sz=u[i+2];i+=3;continue}if(c===69){bd=u[i+2];i+=3;continue}if(c===100){if(line)fl();i+=3;continue}i+=3;continue}
    if(b===29){const c=u[i+1];if(c===86){out.push({t:"<<POTONG>>",sz:0});i+=4;continue}if(c===118){const xb=u[i+4]+u[i+5]*256,h=u[i+6]+u[i+7]*256;out.push({t:"<<LOGO "+xb*8+"x"+h+">>",sz:0});i+=8+xb*h;continue}i+=3;continue}
    if(b===10){fl();i++;continue}line+=String.fromCharCode(b);i++}if(line)fl();return out}
const widthOK=(L,W)=>L.filter(x=>!/^<</.test(x.t)).every(x=>x.t.length<=((x.sz&32)?W/2:W));
(async()=>{
  const b=await chromium.launch(ARGS);
  const O=await mk(b,'OWNER');await O.goto('http://127.0.0.1:8099/index.html');await W(2500);
  await localLogin(O,'own','1234');await O.fill('#u-pin','8642');await O.click('[data-a=usave]');await W(900);
  await O.evaluate(k=>{localStorage.setItem('a521owner',k);localStorage.setItem('a521ownerOk','1')},KEY);await O.reload();await W(2500);
  await localLogin(O,'own','8642');await W(4000);
  const lastJob=()=>O.evaluate(()=>window.__bt.printed.at(-1)).then(dec);
  console.log("1) Atur → Printer & struk: tab Umum (bawaan: cetak otomatis, pelanggan + barista)");
  await O.evaluate(()=>{tab="set";setSub="printer";render()});await W(600);
  const um=await O.evaluate(()=>document.querySelector('#btset').innerText);
  ok(/Struk pelanggan/.test(um)&&/Struk barista/.test(um)&&/2 struk/.test(um),"pilihan struk pelanggan & barista, keterangan 2 struk");
  ok(await O.evaluate(()=>['pauto','pcust','pbar'].every(k=>document.querySelector(`[data-pk=${k}]`).checked)&&!document.querySelector('[data-pk=pcut]').checked),"bawaan: otomatis + pelanggan + barista aktif, potong otomatis mati");
  await O.screenshot({path:SHOT+"s20_umum.png",fullPage:true});
  console.log("2) Pilih printer → cetak tes = 2 struk dalam satu kiriman");
  await O.click('[data-a=btfind]');await W(900);await O.click('[data-a=btpick][data-v="AA:BB:CC:DD:EE:02"]');await W(1600);
  let u=await lastJob(),L=lines(u),T=L.map(x=>x.t);
  ok(count(u,[27,64])===2,"dua struk (dua kali ESC @) dalam satu kiriman");
  const iBar=T.indexOf("STRUK BARISTA");ok(iBar>0&&T.indexOf("TOTAL"+" ".repeat(32-5-"Rp50.000".length)+"Rp50.000")>-1&&T.indexOf("TOTAL"+" ".repeat(32-5-"Rp50.000".length)+"Rp50.000")<iBar,"urutan: struk pelanggan lalu struk barista");
  ok(T.some(t=>/sobek di sini/.test(t))&&!T.includes("<<POTONG>>"),"tanpa pisau: ada garis sobek, tanpa perintah potong");
  const bar=L.slice(iBar);
  ok(!bar.some(x=>/Rp/.test(x.t)),"struk barista tanpa harga");
  ok(bar.some(x=>x.t==="#12"&&(x.sz&48)===48),"nomor antrian besar di struk barista (#12)");
  ok(bar.some(x=>x.t==="2x Palm Sugar"&&x.sz&16)&&bar.some(x=>x.t==="1x Matcha Latte"),"menu & jumlah, huruf besar");
  ok(bar.some(x=>/BOTOL - ambil dari stok/.test(x.t)),"menu botol ditandai ambil dari stok");
  ok(bar.some(x=>/Catatan: Tes cetak - less sugar/.test(x.t)),"catatan pesanan di struk barista");
  const cust=L.slice(0,iBar);
  ok(cust.some(x=>x.t==="No. antrian")&&cust.some(x=>x.t==="#12"),"nomor antrian juga di struk pelanggan");
  ok(cust.some(x=>/^<<LOGO 192x/.test(x.t)),"logo 50% (192 titik di kertas 58 mm)");
  ok(widthOK(L,32),"semua baris muat di kertas 58 mm");
  console.log("3) Penjualan dengan catatan → otomatis 2 struk");
  await O.evaluate(()=>{shut();tab="pos";setSub="";render()});await W(300);
  await O.evaluate(()=>{const p=D.prod.find(x=>x.active);cart={[p.id]:2};pm="Transfer";inCart=true;cartSheet()});await W(500);
  ok(await O.evaluate(()=>!!document.querySelector('#onote')),"kolom Catatan untuk barista ada di layar bayar");
  await O.fill('#onote','a.n. Budi, less sugar');await O.evaluate(()=>{const p=D.prod.find(x=>x.active);cart[p.id]=3;cartSheet()});await W(300);
  ok(await O.evaluate(()=>document.querySelector('#onote').value)==='a.n. Budi, less sugar',"catatan tidak hilang saat jumlah diubah");
  await O.screenshot({path:SHOT+"s20_catatan.png"});
  const n0=await O.evaluate(()=>window.__bt.printed.length);
  await O.evaluate(()=>pay());await W(1600);
  ok(await O.evaluate(()=>window.__bt.printed.length)===n0+1,"satu kiriman otomatis setelah bayar");
  u=await lastJob();L=lines(u);T=L.map(x=>x.t);const no=await O.evaluate(()=>D.tx.at(-1).no),q="#"+(+no.slice(-4));
  ok(await O.evaluate(()=>D.tx.at(-1).note)==="a.n. Budi, less sugar","catatan tersimpan di transaksi");
  ok(T.filter(t=>t===q).length===2,"nomor antrian "+q+" sama di kedua struk");
  ok(T.some(t=>/Catatan: a\.n\. Budi, less sugar/.test(t)),"catatan tercetak");
  ok(/📝 a\.n\. Budi/.test(await O.evaluate(()=>document.querySelector('#m').innerText)),"catatan tampil di layar Lunas");
  ok(await O.evaluate(()=>onote==="")," kolom catatan kosong lagi untuk pesanan berikutnya");
  console.log("4) Tombol Printer di Lunas = cetak ulang 2 struk");
  await O.click('[data-a=copyp]');await W(1200);u=await lastJob();ok(count(u,[27,64])===2,"cetak ulang 2 struk");
  console.log("5) Pengaturan: hanya struk barista, potong otomatis, 80 mm, tab pelanggan & barista");
  await O.evaluate(()=>{shut();tab="set";setSub="printer";render()});await W(400);
  await O.locator('[data-pk=pcust]').uncheck();await O.locator('[data-pk=pcut]').check();await O.click('[data-a=paper][data-v="48"]');await W(300);
  await O.click('[data-a=bttest2]');await W(1200);u=await lastJob();L=lines(u);T=L.map(x=>x.t);
  ok(count(u,[27,64])===1&&T[0]==="STRUK BARISTA"&&T.includes("<<POTONG>>"),"hanya struk barista + perintah potong");
  ok(widthOK(L,48)&&L.some(x=>x.t.length>32),"kertas 80 mm (48 huruf)");
  await O.evaluate(()=>{const c=C();c.paper=32;c.pcust=true;c.pcut=false;save();BTS.tab="cust";btPaint()});await W(300);
  ok(/Nomor antrian/.test(await O.evaluate(()=>document.querySelector('#btset').innerText)),"tab Struk pelanggan");
  await O.locator('[data-pk=pque]').uncheck();await O.locator('[data-pk=pkasir]').uncheck();await O.locator('[data-pk=pig]').check();
  await O.screenshot({path:SHOT+"s20_tab_pelanggan.png"});
  await O.evaluate(()=>{BTS.tab="bar";btPaint()});await W(200);await O.locator('[data-pk=bbig]').uncheck();await O.locator('[data-pk=bkasir]').check();
  await O.screenshot({path:SHOT+"s20_tab_barista.png"});
  await O.click('[data-a=ptab][data-v=umum]');await W(200);await O.click('[data-a=bttest2]');await W(1200);u=await lastJob();L=lines(u);T=L.map(x=>x.t);const ib=T.indexOf("STRUK BARISTA");
  ok(!L.slice(0,ib).some(x=>x.t==="No. antrian")&&!L.slice(0,ib).some(x=>/^Kasir:/.test(x.t)),"pelanggan: tanpa antrian & kasir sesuai pilihan");
  ok(L.slice(ib).some(x=>/^Kasir:/.test(x.t))&&!L.slice(ib).some(x=>/Palm/.test(x.t)&&x.sz&16),"barista: huruf normal + nama kasir sesuai pilihan");
  console.log("6) Ukuran logo & contoh struk");
  await O.evaluate(()=>{const r=document.querySelector('#plsize');r.value=80;r.dispatchEvent(new Event('input',{bubbles:true}))});await W(200);
  await O.click('[data-a=bttest2]');await W(1500);L=lines(await lastJob());ok(L.some(x=>/^<<LOGO 304x/.test(x.t)),"logo 80% (304 titik)");
  await O.evaluate(()=>{const c=C();c.plsize=50;c.pque=true;c.pkasir=true;c.bbig=true;c.bkasir=false;c.pig=false;save();LOGO_RAS=null});
  await O.click('[data-a=pvopen]');await W(1200);
  ok(await O.evaluate(()=>!!document.querySelector('.paper img')&&/No. antrian/.test(document.querySelector('.paper').innerText)),"contoh struk pelanggan: logo & teks");
  await O.screenshot({path:SHOT+"s20_contoh_pelanggan.png",fullPage:true});
  await O.click('[data-a=pvk][data-v=bar]');await W(800);ok(/STRUK BARISTA/.test(await O.evaluate(()=>document.querySelector('.paper').innerText)),"contoh struk barista");
  await O.screenshot({path:SHOT+"s20_contoh_barista.png",fullPage:true});
  await O.click('[data-a=pvk][data-v=both]');await W(800);
  const pvt=await O.evaluate(()=>document.querySelector('.paper').innerText);ok(/No. antrian/.test(pvt)&&/STRUK BARISTA/.test(pvt)&&/sobek/.test(pvt),"contoh keduanya dengan garis sobek");
  const n1=await O.evaluate(()=>window.__bt.printed.length);await O.click('[data-a=pvprint]');await W(1200);ok(await O.evaluate(()=>window.__bt.printed.length)===n1+1,"cetak dari contoh");
  console.log("7) Bluetooth mati saat cetak manual → minta nyalakan lalu cetak");
  await O.evaluate(()=>{shut();window.__bt.fail='off';const o=window.A521Native.postMessage.bind(window.A521Native);window.A521Native.postMessage=function(s){const m=JSON.parse(s);if(m.m==='btPrepare')window.__bt.fail='';return o(s)}});
  await O.evaluate(()=>btPrintTx(D.tx.at(-1),false));await W(1500);
  ok(/dicetak/.test(await O.evaluate(()=>(document.querySelector('#toast')||{}).textContent)),"setelah Bluetooth dinyalakan, struk tetap tercetak");
  console.log(fails?`\nADA ${fails} YANG GAGAL`:"\nSEMUA LULUS");await b.close();
})();
