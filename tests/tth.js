const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const th of ['dark','light']){const ctx=await b.newContext({viewport:{width:390,height:760}});
await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){};window.claude={use:async()=>null}});
const p=await ctx.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(500);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.addStyleTag({content:'*{animation:none!important}'});
await p.evaluate(th=>{if(th=='light')document.documentElement.setAttribute('data-ui','light');else document.documentElement.removeAttribute('data-ui')},th);
const h=await p.$('#pub #k-testi');if(!h){console.log('no testi');continue}await h.scrollIntoViewIfNeeded();await p.evaluate(()=>scrollBy(0,-40));await p.waitForTimeout(200);
const r=await p.$('#pub .kt-row');await r.screenshot({path:`tth_${th}.png`});await ctx.close()}
await b.close()})();
