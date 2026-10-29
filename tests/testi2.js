const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const w of [320,390,1100]){const ctx=await b.newContext({viewport:{width:w,height:860}});
await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){};window.claude={use:async()=>null}});
const p=await ctx.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.click('#pub [data-a=masuk]');await p.click('[data-a=lsel][data-v=own]');await p.fill('#lpw','1234');await p.waitForTimeout(400);
await p.addStyleTag({content:'*{animation:none!important}'});
const av='data:image/svg+xml;base64,'+Buffer.from('<svg xmlns="http://www.w3.org/2000/svg" width="80" height="80"><rect width="80" height="80" fill="#a67"/></svg>').toString('base64');
await p.evaluate(av=>{K.store.testi=[{id:'a',name:'Aisyah Nur Rahmawati Putri',role:'Mahasiswi LIPIA',text:'Kopinya enak banget, aren latte-nya pas manisnya. Tempatnya nyaman buat nugas sore-sore, pelayanannya juga ramah. Pasti balik lagi!',stars:5,img:av},{id:'b',name:'Bima',role:'',text:'Harga bersahabat.',stars:4},{id:'c',name:'Rina',role:'Karyawan',text:'Mantap',stars:0,draft:true}];tab="kabar";render()},av);await p.waitForTimeout(300);
const h=await p.$('#k-testi');await h.scrollIntoViewIfNeeded();await p.evaluate(()=>scrollBy(0,-60));await p.waitForTimeout(200);
await p.screenshot({path:`testi_${w}.png`});
console.log(w,'overflow',await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth));
await p.evaluate(()=>showPub());await p.waitForTimeout(400);const h2=await p.$('#pub #k-testi');if(h2){await h2.scrollIntoViewIfNeeded();await p.evaluate(()=>scrollBy(0,-60));await p.waitForTimeout(200);await p.screenshot({path:`testi_pub_${w}.png`})}
await ctx.close()}
await b.close()})();
