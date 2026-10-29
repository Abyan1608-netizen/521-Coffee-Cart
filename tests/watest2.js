const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
async function phone(name,role,pin){const ctx=await b.newContext({viewport:{width:390,height:860}});
 await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){};window.claude={use:async()=>null};try{Object.defineProperty(navigator,'share',{value:undefined})}catch(e){}});
 const p=await ctx.newPage();p.on('pageerror',e=>console.log(name,'ERR',e.message));
 await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
 await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
 await p.evaluate(()=>{D.cfg.teamCode="TIM-521X";D.users=[{id:"own",name:"Owner",role:"owner",pin:"1234"},{id:"o2",name:"Owner2",role:"owner",pin:"2222"},{id:"bar",name:"Barista",role:"barista",pin:"0000"}];localStorage.setItem("pos521",JSON.stringify(D))});
 await p.reload();await p.waitForTimeout(400);await p.evaluate(()=>document.querySelectorAll('.hi').forEach(e=>e.remove()));
 await p.click('#pub [data-a=masuk]');await p.click(`[data-a=lsel][data-v=${role}]`);await p.fill('#lpw',pin);await p.waitForTimeout(400);return p}
const A=await phone('A','bar','0000');
await A.evaluate(()=>{const p=D.prod.find(x=>x.active);const t={no:"521-T-0001",at:new Date().toISOString(),d:ymd(new Date()),ch:"Offline Store",pm:"Cash",by:me.name,dev:DEV,items:[{p:p.id,n:p.name,q:2,pr:20000,hpp:8000}],use:{},disc:0,vc:"",vd:0,total:40000,hpp:16000,paid:40000,status:"paid"};D.tx.push(t);
 D.exp.push({id:"eAAA",d:ymd(new Date()),cat:"Bahan",amt:15000,note:"susu",by:me.name,dev:DEV});save();tab="dash";render()});
await A.waitForTimeout(300);await A.screenshot({path:'wa_a.png'});
await A.click('[data-a=wash]');await A.waitForTimeout(800);
const textA=await A.evaluate(()=>$("#waout")&&$("#waout").value);console.log(textA&&textA.split("#521TX")[0]);
const B=await phone('B','own','1234');
await B.evaluate(()=>{tab="dash";render()});await B.click('[data-a=wain]');await B.fill('#wain',textA);await B.click('[data-a=waingo]');await B.waitForTimeout(800);
console.log('B',await B.evaluate(()=>JSON.stringify([D.tx.length,D.exp.length,D.exp.map(e=>e.amt)])));
await B.screenshot({path:'wa_b.png'});
await B.click('[data-a=washall]');await B.waitForTimeout(800);const textB=await B.evaluate(()=>$("#waout")&&$("#waout").value);
const C=await phone('C','o2','2222');
await C.evaluate(()=>{tab="dash";render()});await C.click('[data-a=wain]');await C.fill('#wain',textB);await C.click('[data-a=waingo]');await C.waitForTimeout(800);
console.log('C',await C.evaluate(()=>JSON.stringify([D.tx.length,D.tx.map(t=>t.by),D.exp.length])));
// paste again no dup
await C.click('[data-a=wain]');await C.fill('#wain',textB+textA);await C.click('[data-a=waingo]');await C.waitForTimeout(800);
console.log('C2',await C.evaluate(()=>JSON.stringify([D.tx.length,D.exp.length])));
await b.close()})();
