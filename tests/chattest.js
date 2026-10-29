const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const mode of ['off','ai']){
const errs=[];const ctx=await b.newContext({viewport:{width:390,height:860}});
await ctx.addInitScript(m=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){};window.claude={use:async n=>{if(n==="sample"&&m==="ai"){const f=async(inp,o)=>{window.__inp=inp;const t="Assalamu'alaikum warahmatullahi wabarakatuh 🙏\n\nTentu, Kak ☕ **Espresso** adalah:\n- poin satu\n- poin dua";let x="";for(const ch of t.match(/.{1,8}/gs)){x+=ch;o.onText&&o.onText({text:x,delta:ch});await new Promise(r=>setTimeout(r,20))}return{text:t}};return f}return null}}},mode);
const p=await ctx.newPage();p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.click('#pub [data-a=masuk]');await p.click('[data-a=lsel][data-v=own]');await p.fill('#lpw','1234');await p.waitForTimeout(300);
await p.click('[data-a=c_open]');await p.waitForTimeout(1200);await p.screenshot({path:`chat_${mode}0.png`});
if(mode==='off'){
 for(const q of ['Apa beda arabika dan robusta?','Tolong kerjakan PR matematika saya','Palm Sugar itu apa?']){await p.fill('#cq',q);await p.press('#cq','Enter');await p.waitForTimeout(700)}
 await p.click('.cchips [data-a=c_chip][data-v="4"]');await p.waitForTimeout(300);
 const txt=await p.evaluate(()=>chatH.filter(m=>m.role==='assistant').map(m=>m.content.slice(0,60)));console.log(txt);
 await p.screenshot({path:`chat_off1.png`});
 await p.evaluate(()=>{document.querySelector('.cmsgs').scrollTop=0});await p.waitForTimeout(100);await p.screenshot({path:`chat_off2.png`});
}else{
 await p.fill('#cq','Apa itu espresso?');await p.click('.csend[data-a=c_send]');await p.waitForTimeout(1200);
 console.log(await p.evaluate(()=>[window.__inp.length,window.__inp[0].content.slice(0,80),window.__inp[1]]));
 await p.screenshot({path:`chat_ai1.png`});
}
await p.keyboard.press('Escape');console.log(mode,'hidden',await p.evaluate(()=>$("#chat").hidden),errs);await ctx.close()}
await b.close()})();
