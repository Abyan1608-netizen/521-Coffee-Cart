const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[],fails=[];const ok=(c,m)=>{if(!c)fails.push(m)};
const ctx=await b.newContext({viewport:{width:390,height:860}});
await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){};window.claude={use:async n=>n==="user"?{canEdit:async()=>true}:n==="artifact"?{publish:async h=>({})}:null}});
const p=await ctx.newPage();p.setDefaultTimeout(3000);p.on('pageerror',e=>errs.push(e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
await p.click('#pub [data-a=masuk]');await p.click('[data-a=lsel][data-v=own]');await p.fill('#lpw','1234');await p.waitForTimeout(300);
await p.evaluate(()=>{C().help=0});
await p.screenshot({path:'sub0.png'});
await p.click('[data-a=tab][data-v=mem]');await p.waitForTimeout(300);
// template 1
await p.click('[data-a=m_tpl]');await p.fill('#tpn','Paket 10 Cup');await p.fill('#tpp','150000');await p.fill('#tpd','30');await p.click('[data-a=m_tsave]');
// template 2 bundling
await p.click('[data-a=m_tpl] >> text=+ Buat jenis paket');await p.fill('#tpn','Paket Kerja');await p.fill('#tpp','120000');
const ids=await p.evaluate(()=>D.prod.filter(x=>x.active).map(x=>[x.id,x.name]));console.log(ids);
await p.selectOption('select.tp[data-tr="0"]',ids[0][0]);await p.fill('input.tq[data-tr="0"]','5');
await p.click('[data-a=m_trow]');await p.selectOption('select.tp[data-tr="1"]',ids[1][0]);await p.fill('input.tq[data-tr="1"]','5');
await p.screenshot({path:'sub_tpl.png'});
await p.click('[data-a=m_tsave]');await p.waitForTimeout(200);
ok(await p.evaluate(()=>C().subPk.length)===2,'2 tpl');
// sell
await p.click('[data-a=m_sell]');await p.fill('#mshp','0812-3456-789');await p.fill('#msnm','Budi');await p.screenshot({path:'sub_sell.png'});
await p.click('[data-a=m_save]');await p.waitForTimeout(400);await p.screenshot({path:'sub_sold.png'});
ok(await p.evaluate(()=>D.mem.length===1&&memLeft(D.mem[0])===10),'sold 10');
const wa=await p.getAttribute('a[href*="wa.me/62812"]','href');ok(!!wa,'wa link');
await p.click('#s [data-a=close]');
// sell bundling to same
await p.click('[data-a=m_sell]');await p.fill('#mshp','08123456789');await p.click('[data-a=m_pk] >> nth=1');await p.click('[data-a=m_save]');await p.waitForTimeout(300);await p.click('#s [data-a=close]');
ok(await p.evaluate(()=>memLeft(D.mem[0])===20),'20 left');
await p.screenshot({path:'sub_list.png',fullPage:true});
// redeem: 3x prod1 + 1x prod3 (prod3 not in bundle -> from bebas)
await p.click('[data-a=tab][data-v=pos]');
await p.evaluate(ids=>{cart[ids[0][0]]=3;cart[ids[2][0]]=1;render()},ids);
await p.click('#cbar');await p.fill('#mhp','08123456789');await p.click('[data-a=m_chk]');await p.waitForTimeout(200);
await p.screenshot({path:'sub_cart.png'});
await p.click('[data-a=m_go]');await p.waitForTimeout(300);await p.screenshot({path:'sub_rcp.png'});
const st=await p.evaluate(()=>{const m=D.mem[0];return m.packs.map(k=>k.items.map((_,i)=>pkLeft(k,i)))});console.log(JSON.stringify(st));
ok(JSON.stringify(st)==='[[9],[2,5]]','alloc '+JSON.stringify(st));
await p.click('#s [data-a=close]');
// void redemption
const key=await p.evaluate(()=>txKey(D.tx[D.tx.length-1]));
await p.evaluate(k=>{document.querySelector('#s').dataset.v=k;show('<input id="vr" value="tes">');document.querySelector('#s').dataset.v=k},key);
await p.evaluate(()=>{const b=document.createElement('button');b.dataset.a='vgo';document.body.appendChild(b);b.click()});await p.waitForTimeout(200);
ok(await p.evaluate(()=>memLeft(D.mem[0]))===20,'void restore');
// insufficient
await p.evaluate(ids=>{cart={};cart[ids[0][0]]=30;subM=D.mem[0].id;render()},ids);await p.click('#cbar');await p.waitForTimeout(200);
ok(await p.isVisible('.subcard .verr'),'short msg');
// merge test: simulate tx from other device
await p.evaluate(()=>{const m=D.mem[0],k=m.packs[0];txMerge([{no:"521-X-0001",dev:"zz",at:new Date().toISOString(),d:ymd(new Date()),items:[{n:"x",q:2,pr:0}],pm:"Langganan",total:0,hpp:0,status:"paid",by:"Bar",sub:{m:m.id,hp:m.hp,uses:[[k.id,0,2]]}}],"wa")});
ok(await p.evaluate(()=>memLeft(D.mem[0]))===18,'merge');
// bundle roundtrip memMerge idempotent
await p.evaluate(()=>memMerge(JSON.parse(JSON.stringify(D.mem))));ok(await p.evaluate(()=>memLeft(D.mem[0]))===18,'memMerge idem');
await p.evaluate(()=>{shut();tab='mem';render();memSheet(D.mem[0].id)});await p.waitForTimeout(200);await p.screenshot({path:'sub_mem.png',fullPage:true});
console.log('FAILS',fails,'ERRS',errs);await b.close()})();
