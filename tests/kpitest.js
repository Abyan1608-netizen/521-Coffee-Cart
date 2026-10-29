const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[],fails=[];const ok=(c,m)=>{if(!c)fails.push(m)};
const ctx=await b.newContext({viewport:{width:400,height:860}});
await ctx.addInitScript(()=>{sessionStorage.setItem("k521-hi","1");window.claude={use:async n=>n==="user"?{canEdit:async()=>false}:null}});
const p=await ctx.newPage();p.setDefaultTimeout(3000);p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/premium.html');await p.waitForTimeout(300);
await p.click('#pub [data-a=masuk]');await p.fill('#lpw','1234');await p.waitForTimeout(200);await p.click('[data-a=nohelp]').catch(()=>{});
await p.click('[data-a=add][data-id=palm]');await p.click('[data-a=add][data-id=butter]');await p.click('#cbar');await p.fill('#paid','50000');await p.click('#go');await p.click('.sheet [data-a=close].btn');
await p.click('#nav [data-v=dash]');await p.fill('#ea','5000');await p.click('[data-a=exp]');
for(const k of ['rev','gp','ex','net','n','cup','avg']){await p.click(`[data-a=kpi][data-v=${k}]`);ok(await p.isVisible('.sheet .kbig'),'sheet '+k);if(k==='net'||k==='rev')await p.screenshot({path:`kpi_${k}.png`});await p.click('.sheet .x')}
await p.screenshot({path:'kpi_dash.png'});
console.log('FAILS',fails,'ERRS',errs);await b.close()})();
