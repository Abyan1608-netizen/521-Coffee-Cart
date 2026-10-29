const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const errs=[],fails=[];const ok=(c,m)=>{if(!c)fails.push(m)};
const pages=[];
const mk=async(canEdit,withRoom)=>{const ctx=await b.newContext({viewport:{width:400,height:860},permissions:['clipboard-read','clipboard-write']});
 const id='p'+pages.length;
 await ctx.exposeBinding('busSend',async(src,msg)=>{for(const q of pages){if(q.__id!==id&&q.__room)await q.evaluate(m=>window.__busRecv&&window.__busRecv(m),msg).catch(()=>{})}});
 await ctx.addInitScript(([ce,wr,id])=>{sessionStorage.setItem("k521-hi","1");
  const L={},P=[];let mine={};const peers={};
  const room={presence:async p=>{Object.entries(p).forEach(([k,v])=>{if(v===null)delete mine[k];else mine[k]=v});busSend({t:"pres",id,presence:JSON.parse(JSON.stringify(mine))})},
   onPeers:h=>{P.push(h);return()=>{}},on:(t,f)=>{(L[t]=L[t]||[]).push(f);return()=>{}},emit:async(t,d)=>{busSend({t:"emit",topic:t,data:d,id})},peers:()=>[]};
  window.__busRecv=m=>{if(m.t==="pres"){const isNew=!peers[m.id];peers[m.id]={peer:m.id,isMe:false,presence:m.presence};const all=Object.values(peers);P.forEach(h=>h({peers:all,joined:isNew?[peers[m.id]]:[],updated:isNew?[]:[peers[m.id]],left:[]}))}
   if(m.t==="emit")(L[m.topic]||[]).forEach(f=>f({topic:m.topic,data:m.data,isMe:false}))};
  window.claude={use:async n=>n==="user"?{canEdit:async()=>ce}:n==="artifact"&&ce?{publish:async h=>{(window.__pubs=window.__pubs||[]).push(h);return{}}}:n==="room"&&wr?room:null}},[canEdit,withRoom,id]);
 const p=await ctx.newPage();p.__id=id;p.__room=withRoom;pages.push(p);p.setDefaultTimeout(5000);p.on('pageerror',e=>errs.push(id+': '+e.message));return p};
// owner sets up team
const own=await mk(true,true);await own.goto('file://'+process.cwd()+'/premium.html');await own.waitForTimeout(300);
await own.click('#pub [data-a=masuk]');await own.fill('#lpw','1234');await own.waitForTimeout(300);await own.click('[data-a=nohelp]').catch(()=>{});
await own.click('#nav [data-v=set]');await own.click('[data-a=setsub][data-v=sinkron]');await own.click('[data-a=tson]');await own.waitForTimeout(2500);
const code=await own.textContent('#tcv');const html=(await own.evaluate(()=>window.__pubs)).pop();fs.writeFileSync('tx_pub.html',html);
// staff A with room (realtime)
const sa=await mk(false,true);await sa.goto('file://'+process.cwd()+'/tx_pub.html');await sa.waitForTimeout(300);
await sa.click('#pub [data-a=masuk]');await sa.fill('#tcode',code);await sa.click('[data-a=tjoin]');await sa.waitForTimeout(1500);
await sa.click('[data-a=lsel][data-v=bar]');await sa.fill('#lpw','0000');await sa.waitForTimeout(800);await sa.click('[data-a=nohelp]').catch(()=>{});
await sa.click('[data-a=add][data-id=palm]');await sa.click('#cbar');await sa.fill('#paid','20000');await sa.click('#go');await sa.waitForTimeout(2500);
await own.click('#nav [data-v=dash]');await own.waitForTimeout(500);
let ot=await own.evaluate(()=>D.tx.filter(t=>t.rx==="rt").length);ok(ot===1,'realtime received '+ot);
ok(await sa.evaluate(()=>D.tx.every(t=>t.sent===1)),'staff acked');
await own.screenshot({path:'tx1.png'});
await sa.click('[data-a=close]').catch(()=>{});await sa.click('.sheet .x').catch(()=>{});await sa.click('#nav [data-v=dash]');await sa.waitForTimeout(400);await sa.screenshot({path:'tx2.png'});
// staff B no room (WA)
const sb=await mk(false,false);await sb.goto('file://'+process.cwd()+'/tx_pub.html');await sb.waitForTimeout(300);
await sb.click('#pub [data-a=masuk]');await sb.fill('#tcode',code);await sb.click('[data-a=tjoin]');await sb.waitForTimeout(1500);
await sb.click('[data-a=lsel][data-v=bar]');await sb.fill('#lpw','0000');await sb.waitForTimeout(800);await sb.click('[data-a=nohelp]').catch(()=>{});
for(const id of ['butter','matcha']){await sb.click(`[data-a=add][data-id=${id}]`);await sb.click('#cbar');await sb.fill('#paid','50000');await sb.click('#go');await sb.waitForTimeout(300);await sb.click('.sheet .x').catch(()=>{});await sb.waitForTimeout(200)}
await sb.click('#nav [data-v=dash]');await sb.click('[data-a=wash]');await sb.waitForTimeout(1500);
const txt=await sb.evaluate(()=>navigator.clipboard.readText().catch(()=>""));console.log(txt.slice(0,260));ok(/#521TX:/.test(txt),'wa text');
await sb.screenshot({path:'tx3.png'});
await own.click('[data-a=wain]');await own.fill('#wain',txt);await own.click('[data-a=waingo]');await own.waitForTimeout(1500);
ot=await own.evaluate(()=>D.tx.filter(t=>t.rx==="wa").length);ok(ot===2,'wa imported '+ot);
await own.click('[data-a=wain]');await own.fill('#wain',txt);await own.click('[data-a=waingo]');await own.waitForTimeout(1000);
ok((await own.evaluate(()=>D.tx.filter(t=>t.rx).length))===3,'dedupe');
await own.screenshot({path:'tx4.png'});
// void on staff A propagates
await sa.evaluate(()=>{const t=D.tx[D.tx.length-1];t.status='cancelled';t.sent=0;save();rtSend()});await sa.waitForTimeout(2000);
ok(await own.evaluate(()=>D.tx.find(t=>t.rx==="rt").status)==='cancelled','void propagated');
console.log('FAILS',fails,'ERRS',errs);await b.close()})();
