const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const errs=[],fails=[];const ok=(c,m)=>{if(!c)fails.push(m)};
const ctx=await b.newContext({viewport:{width:400,height:860}});
await ctx.addInitScript(()=>{sessionStorage.setItem("k521-hi","1");window.claude={use:async n=>n==="user"?{canEdit:async()=>true}:n==="artifact"?{publish:async h=>{(window.__pubs=window.__pubs||[]).push(h);return{}}}:null}});
const p=await ctx.newPage();p.setDefaultTimeout(3000);p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(300);
await p.click('#pub [data-a=masuk]');await p.fill('#lpw','1234');await p.waitForTimeout(200);await p.click('[data-a=nohelp]').catch(()=>{});
await p.waitForTimeout(1600);const n0=await p.evaluate(()=>(window.__pubs||[]).length);console.log('initial pubs',n0);
// draft kabar post (pending) then change kasir menu
await p.click('#nav [data-v=kabar]');await p.click('[data-a=knew][data-v=news]');await p.fill('#p-title','DRAFT RAHASIA');await p.click('[data-a=ksavep]');await p.waitForTimeout(200);
const pend=await p.evaluate(()=>kdirty);ok(pend,'kabar pending');
await p.click('#nav [data-v=pos]');await p.click('[data-a=sold][data-id=matcha]');await p.waitForTimeout(1700);
const pubs=await p.evaluate(()=>window.__pubs||[]);ok(pubs.length===n0+1,'auto publish '+pubs.length);
const last=pubs[pubs.length-1];const kd=JSON.parse(last.match(/id="kdata">([\s\S]*?)<\/script>/)[1].replace(/\\u003c/g,'<'));
ok(kd.menu.find(x=>x.n==='Matcha Latte').o===1,'matcha habis published');ok(!JSON.stringify(kd).includes('DRAFT RAHASIA'),'draft not published');
ok(kd.menu[0].c&&kd.menu[0].s,'rich fields');ok(await p.evaluate(()=>kdirty),'draft still pending');
// cart non-empty defers
await p.click('[data-a=add][data-id=butter]');await p.click('[data-a=sold][data-id=palm]');await p.waitForTimeout(1600);ok((await p.evaluate(()=>window.__pubs.length))===n0+1,'deferred with cart');
fs.writeFileSync('ms_pub.html',last);
const c2=await b.newContext({viewport:{width:400,height:860}});await c2.addInitScript(()=>{sessionStorage.setItem("k521-hi","1");window.claude={use:async()=>null}});const q=await c2.newPage();q.on('pageerror',e=>errs.push(e.message));
await q.goto('file://'+process.cwd()+'/ms_pub.html');await q.waitForTimeout(400);await q.locator('#k-menu').scrollIntoViewIfNeeded();await q.waitForTimeout(400);await q.screenshot({path:'ms1.png'});
const mt=await q.textContent('.k-menu');ok(mt.includes('gula aren asli')&&!mt.includes('Espresso +'),'public desc no recipe');
console.log('FAILS',fails,'ERRS',errs);await b.close()})();
