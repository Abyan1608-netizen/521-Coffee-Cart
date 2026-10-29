const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext({viewport:{width:390,height:860}});
await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){};window.claude={use:async()=>null}});
const p=await ctx.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.click('#pub [data-a=masuk]');await p.click('[data-a=lsel][data-v=own]');await p.fill('#lpw','1234');await p.waitForTimeout(400);
await p.addStyleTag({content:'*{animation:none!important}'});
await p.evaluate(()=>{tab="kabar";render()});await p.waitForTimeout(300);
await p.click('[data-a=ktnew]');await p.fill('#t-n','Rina');await p.fill('#t-r','Mahasiswa');await p.fill('#t-x','Kopinya enak dan pas buat nugas.');await p.click('[data-a=ktstar][data-v="4"]');
await p.waitForTimeout(200);console.log('kept',await p.$eval('#t-n',e=>e.value));
await p.screenshot({path:'testi_sheet.png'});
await p.click('[data-a=ktsave]');await p.waitForTimeout(300);
await p.click('[data-a=ktnew]');await p.fill('#t-n','Bima');await p.fill('#t-x','Pelayanan ramah, harga bersahabat.');await p.click('[data-a=ktsave]');await p.waitForTimeout(300);
console.log(await p.evaluate(()=>JSON.stringify(K.store.testi.map(t=>[t.name,t.stars,t.draft]))));
const h=await p.$('#k-testi');await h.scrollIntoViewIfNeeded();await p.evaluate(()=>scrollBy(0,-60));await p.waitForTimeout(200);await p.screenshot({path:'testi_list.png'});
// delete
await p.click('[data-a=ktdel]');await p.click('[data-a=ktdelgo]');await p.waitForTimeout(200);console.log('after del',await p.evaluate(()=>K.store.testi.length));
// public view
await p.evaluate(()=>{showPub()});await p.waitForTimeout(400);console.log('public cards',await p.evaluate(()=>document.querySelectorAll('#pub .kt-card').length));
await b.close()})();
