const {chromium,devices}=require('playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({...devices['Pixel 7']});
await ctx.route('**/shim.js',async r=>{const res=await r.fetch();let t=await res.text();t=t.replace(/server:"[^"]*"/,'server:""');r.fulfill({response:res,body:t})});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('http://127.0.0.1:8099/index.html');await p.waitForTimeout(1500);
// data lama: promo = link Play Store
await p.evaluate(()=>{D.cfg.promo="https://play.google.com/store/apps/details?id=id.coffee521.pos";delete D.cfg.promoV13;localStorage.setItem("pos521",JSON.stringify(D))});await p.reload();await p.waitForTimeout(2000);
console.log('promo setelah update:',JSON.stringify(await p.evaluate(()=>C().promo)));
await p.evaluate(()=>{showLogin();lsel='own';loginView()});for(const d of '1234')await p.click(`[data-a=kp][data-v="${d}"]`);await p.waitForTimeout(1500);await p.evaluate(()=>shut());
console.log('tombol QR kabar & promo di kasir:',await p.evaluate(()=>!!document.querySelector('[data-a=promoqr]')));
await p.evaluate(()=>{cart={"palm":1};pm="Transfer";pay()});await p.waitForTimeout(300);
console.log('struk menyebut link:',await p.evaluate(()=>/play\.google|Promo & kegiatan terbaru/.test(waText(D.tx[D.tx.length-1]))));
await p.evaluate(()=>{shut();C().promo="https://contoh.id/menu";save()});await p.evaluate(()=>{tab="pos";render()});
console.log('link milik owner tetap bisa dipakai:',await p.evaluate(()=>!!document.querySelector('[data-a=promoqr]')),await p.evaluate(()=>{location.reload;return C().promo}));
const w=await ctx.newPage();await w.goto('http://127.0.0.1:8098/');await w.waitForTimeout(2500);
console.log('web: tombol download:',await w.evaluate(()=>document.querySelectorAll('a.k-login,a.k-app').length),'| tombol masuk:',await w.evaluate(()=>!!document.querySelector('[data-a=masuk]')));
console.log('ERRORS',errs.length?errs:'none');await b.close()})()
