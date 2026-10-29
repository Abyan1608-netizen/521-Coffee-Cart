const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:860}});
await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){};window.claude={use:async()=>null}});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.click('#pub [data-a=masuk]');await p.click('[data-a=lsel][data-v=own]');await p.fill('#lpw','1234');await p.waitForTimeout(300);
await p.click('[data-a=c_open]');await p.waitForTimeout(800);
for(const q of ['Apa filosofi brand 521?','Berapa BEP dan strategi ekspansi 521?','Apa itu espresso?']){await p.fill('#cq',q);await p.press('#cq','Enter');await p.waitForTimeout(800)}
console.log(await p.evaluate(()=>chatH.filter(m=>m.role==='assistant').map(m=>m.content.slice(0,110))));
await p.screenshot({path:'br.png'});console.log(errs);await b.close()})();
