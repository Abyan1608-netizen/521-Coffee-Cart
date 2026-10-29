const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [n,glass,theme] of [['d',0,'dark'],['g',1,'dark'],['l',0,'light']]){
const ctx=await b.newContext({viewport:{width:390,height:860}});await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){}});
const p=await ctx.newPage();
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.click('#pub [data-a=masuk]');await p.click('[data-a=lsel][data-v=own]');await p.fill('#lpw','1234');await p.waitForTimeout(500);
await p.evaluate(([g,t])=>{C().glass=!!g;C().theme=t;C().uiSet=1;look();render()},[glass,theme]);
await p.click('#cfab');await p.waitForTimeout(900);
const e0=await p.$('.cin');await e0.screenshot({path:`bar_${n}_empty.png`});console.log('emptyH',await p.evaluate(()=>getComputedStyle($('#cq')).height));await p.fill('#cq','Halo, apa beda arabika dan robusta? Tolong jelaskan dengan detail ya kak');await p.dispatchEvent('#cq','input');await p.waitForTimeout(300);
const el=await p.$('.cin');await el.screenshot({path:`bar_${n}.png`});
console.log(n,await p.evaluate(()=>{const t=getComputedStyle($('#cq'));return [t.height,t.padding,t.border,t.backgroundColor,t.backdropFilter,t.boxShadow.slice(0,40),t.minHeight]}));
await ctx.close()}
await b.close()})();
