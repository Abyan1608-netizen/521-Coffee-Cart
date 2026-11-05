// Uji website ↔ aplikasi: data dari /kdata.js menimpa isi website
const {chromium,devices}=require('playwright');const fs=require('fs');
const W=ms=>new Promise(r=>setTimeout(r,ms));let fails=0;const ok=(c,m)=>{console.log((c?"  ✔ ":"  ✘ GAGAL: ")+m);if(!c)fails++};
const base=JSON.parse(fs.readFileSync('/home/claude/521-coffee-cart/data/kdata.json','utf8'));delete base.team;
function K(mut){const k=JSON.parse(JSON.stringify(base));mut&&mut(k);return k}
(async()=>{const b=await chromium.launch();
 for(const dev of ['Pixel 7','Desktop Chrome']){
  const ctx=await b.newContext({...devices[dev]});let kd=null,rev=1000;
  await ctx.route('https://cdnjs.cloudflare.com/**',r=>r.fulfill({body:'',contentType:'text/javascript'}));
  await ctx.route('https://coffee521-api.coffee521.workers.dev/kdata.js*',r=>kd?r.fulfill({contentType:'text/javascript',body:'window.__KREV='+rev+';window.__K='+JSON.stringify(kd)+';'}):r.abort());
  await ctx.route('https://coffee521-api.coffee521.workers.dev/media/**',r=>r.fulfill({contentType:'image/jpeg',body:fs.readFileSync('/home/claude/521-coffee-cart/assets/hero.jpg')}));
  const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
  console.log("== "+dev);
  // 1) server mati → isi bawaan
  await p.goto('http://127.0.0.1:8097/index.html');await W(2500);
  const t0=await p.evaluate(()=>document.body.innerText);
  ok(/Palm Sugar/.test(t0)&&/Rp15\.000/.test(t0),"tanpa server: menu bawaan tampil");
  // 2) data dari aplikasi
  kd=K(k=>{k.store.name="521 Coffee Cart";k.store.place="Pejaten – Jakarta Selatan";k.store.wa="081234567890";
    k.menu=k.menu.map(m=>m.n==="Palm Sugar"?{...m,p:16000}:m.n==="Black Caffe"?{...m,o:1}:m);k.menu.push({n:"Caramel Latte",p:22000,c:"Kopi Susu",s:"170 ml",d:"Baru!"});
    k.posts.unshift({id:"pnew",type:"promo",title:"Promo Kamis Manis",body:"Diskon 2rb semua menu",badge:"HARI INI",start:"",end:"2099-12-31",draft:false,created:"2026-11-05",dval:2000});
    k.posts.push({id:"pdraft",type:"promo",title:"Rahasia Draf",draft:true});
    k.store.testi=[{id:"t1",name:"Dina",role:"Mahasiswi",text:"Palm Sugar-nya juara!",stars:5,draft:false}];
    k.store.order.resellers=[{n:"Aharis",wa:"085236187597",loc:"LIPIA IKHWAN",w:"Pejaten"},{n:"Budi",wa:"081111222333",loc:"Kampus",w:"Ciledug"},{n:"Asma",wa:"000000000",loc:"LIPIA AKHWAT",w:"Pejaten"}];
    k.store.web={hero:{title:"Kopi *jujur*\nuntuk kamu.",sub:"Uji dari aplikasi"},strip:["Satu","Dua"],show:{testi:false}}});
  await p.evaluate(()=>__k521.liveLoad());await W(1500);
  const t1=await p.evaluate(()=>document.body.innerText);
  ok(/Rp16\.000/.test(t1),"harga Palm Sugar ikut aplikasi (16.000)");
  ok(/Caramel Latte/.test(t1),"menu baru dari aplikasi muncul");
  ok(await p.evaluate(()=>{const f=[...document.querySelectorAll('.pc')].find(x=>/Black Caffe/.test(x.textContent));return !!f&&/Habis hari ini/.test(f.textContent)&&!f.querySelector('.pc-add')}),"menu Habis: tanpa tombol Pesan");
  ok(/Promo Kamis Manis/.test(t1)&&!/Rahasia Draf/.test(t1),"promo baru tampil, draf tidak");
  ok(/Pejaten – Jakarta Selatan/.test(t1),"lokasi ikut Atur");
  ok(/Uji dari aplikasi/.test(t1)&&/jujur/.test(t1),"teks hero dari Atur → Website");
  ok(await p.evaluate(()=>!document.querySelector('[data-sec="testi"]')),"bagian Testimoni disembunyikan dari aplikasi");
  ok(await p.evaluate(()=>[...document.querySelectorAll('a[href*="wa.me"]')].some(a=>/6281234567890/.test(a.href))),"nomor WhatsApp ikut aplikasi");
  ok(await p.evaluate(()=>__k521.st().S.resellers.some(r=>r.name==="Budi"&&r.area==="Ciledug")),"reseller dari aplikasi");
  ok(await p.evaluate(()=>!__k521.st().S.resellers.some(r=>r.name==="Asma")),"reseller dengan nomor WA tidak valid disembunyikan");
  // 3) tidak render ulang bila rev sama
  await p.evaluate(()=>{document.querySelector('#root').firstElementChild.dataset.mark='1';__k521.liveLoad()});await W(1200);
  ok(await p.evaluate(()=>document.querySelector('#root').firstElementChild.dataset.mark==='1'),"rev sama → tidak digambar ulang");
  // 4) panel pesan terbuka → tunda
  rev++;kd.menu[0].p=17000;await p.evaluate(()=>{__k521.setOp(true);__k521.liveLoad()});await W(1200);
  ok(await p.evaluate(()=>document.querySelector('#root').firstElementChild.dataset.mark==='1'&&__k521.st().liveWait),"saat panel pesan terbuka, perubahan ditunda");
  await p.evaluate(()=>{__k521.setOp(false);__k521.liveRender()});await W(500);
  ok(/Rp17\.000/.test(await p.evaluate(()=>document.body.innerText)),"setelah ditutup, data terbaru tampil");
  if(dev==='Pixel 7')await p.screenshot({path:'/home/claude/work/v18/web_live.png',fullPage:false});
  ok(!errs.length,"tanpa error JS "+JSON.stringify(errs));await ctx.close()}
 console.log(fails?`\nADA ${fails} YANG GAGAL`:"\nSEMUA LULUS");await b.close()})();
