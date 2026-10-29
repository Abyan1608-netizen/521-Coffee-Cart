const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[],fails=[];const ok=(c,m)=>{if(!c)fails.push(m)};
const ctx=await b.newContext({viewport:{width:400,height:860}});
await ctx.addInitScript(()=>{sessionStorage.setItem("k521-hi","1");window.claude={use:async n=>null}});
const p=await ctx.newPage();p.setDefaultTimeout(3000);p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/premium.html');await p.waitForTimeout(200);
const sum=()=>p.evaluate(()=>D.prod.filter(x=>/palm|butter/i.test(x.name)).map(x=>x.name+":"+x.rec.map(r=>r.i+r.q).join(",")+" | "+x.batch.rows.map(r=>r.n+"["+r.v.join("/")+"]").join(" ")).join("\n"));
const fresh=await sum();console.log(fresh);ok(fresh.includes('kr20,air20')&&!fresh.includes('ks'),'fresh rec');
// simulate v2 device (old master)
await p.evaluate(()=>{const d=JSON.parse(localStorage.getItem("pos521"));d.cfg.recV=2;const pp=d.prod.find(x=>x.name==="Palm Sugar");pp.rec=[{i:"esp",q:30},{i:"ga",q:15},{i:"ks",q:40},{i:"su",q:85},{i:"cup",q:1},{i:"lid",q:1}];pp.batch.rows=[{n:"Espresso",v:["30 ml","30 ml","75 ml","150 ml","750 ml"],note:""},{n:"Krimer Set",v:["40 ml","60 ml","150 ml","300 ml","1.500 ml"],note:"1:1 Air & Krimer"},{n:"Susu UHT",v:["85 ml","97 ml","242,5 ml","485 ml","2.425 ml"],note:""}];localStorage.setItem("pos521",JSON.stringify(d))});
await p.reload();await p.waitForTimeout(300);const v3=await sum();console.log(v3);ok(v3.includes('Palm Sugar:esp30,ga15,kr20,air20,su85'),'patched rec');ok(v3.includes('Krimer 1:1[40 ml////]')&&v3.includes('Krimer Set[/60 ml/150 ml/300 ml/1.500 ml]'),'patched rows');
await p.reload();await p.waitForTimeout(200);ok((await sum())===v3,'idempotent');
await p.click('#pub [data-a=masuk]');await p.fill('#lpw','1234');await p.waitForTimeout(200);await p.click('[data-a=nohelp]').catch(()=>{});
await p.click('#nav [data-v=menu]');await p.click('[data-a=rview][data-id=butter]');await p.waitForTimeout(300);
let t=await p.textContent('.rbig');ok(t.includes('Krimer 1:1')&&!t.includes('Krimer Set'),'170 shows krimer 1:1');await p.screenshot({path:'kr1.png'});
await p.click('[data-a=rsz][data-v="1"]');await p.waitForTimeout(200);t=await p.textContent('.rbig');ok(t.includes('Krimer Set')&&!t.includes('Krimer 1:1'),'200 shows set');
await p.click('.rall summary');await p.waitForTimeout(200);await p.screenshot({path:'kr2.png'});
console.log('FAILS',fails,'ERRS',errs);await b.close()})();
