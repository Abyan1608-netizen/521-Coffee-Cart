const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [n,w,h] of [['m',390,860],['w',1280,820]]){
const ctx=await b.newContext({viewport:{width:w,height:h}});await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){}});
const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.click('#pub [data-a=masuk]');await p.click('[data-a=lsel][data-v=own]');await p.fill('#lpw','1234');await p.waitForTimeout(1200);
await p.screenshot({path:`fab_${n}0.png`});
await p.evaluate(()=>{C().help=0;cart[D.prod[0].id]=2;render()});await p.waitForTimeout(4500);await p.screenshot({path:`fab_${n}1.png`});
await p.click('#cfab');await p.waitForTimeout(700);const open=await p.evaluate(()=>!$('#chat').hidden);
await p.keyboard.press('Escape');await p.waitForTimeout(400);
await p.click('[data-a=tab][data-v=dash]');await p.waitForTimeout(200);
console.log(n,open,await p.evaluate(()=>$('#cfab').hidden),errs);await ctx.close()}
await b.close()})();
