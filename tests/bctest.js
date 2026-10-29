const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:860}});await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){}});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.click('#pub [data-a=masuk]');await p.click('[data-a=lsel][data-v=own]');await p.fill('#lpw','1234');await p.waitForTimeout(500);
await p.click('#cfab');await p.waitForTimeout(800);
for(const q of ['Kenapa namanya Black Caffe?','Ada americano?','Halo']){await p.fill('#cq',q);await p.press('#cq','Enter');await p.waitForTimeout(700)}
const t=await p.evaluate(()=>chatH.filter(m=>m.role==='assistant').map(m=>m.content));console.log(t.map(x=>x.slice(0,140)),t.join().includes('Kak'));
await p.evaluate(()=>{const L=document.querySelector('.cmsgs');L.style.scrollBehavior='auto';L.scrollTop=0});await p.waitForTimeout(200);await p.screenshot({path:'bc.png'});
console.log(errs);await b.close()})();
