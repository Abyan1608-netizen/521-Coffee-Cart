const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const ctx=await b.newContext();
await ctx.addInitScript(()=>{try{sessionStorage.setItem("k521-hi","1")}catch(e){};window.claude={use:async()=>null}});
const p=await ctx.newPage();p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(400);
console.log(await p.evaluate(()=>{const m={id:"m1",hp:"0811",name:"Tama",packs:[{id:"k1",name:"Teman Berproses",exp:"2026-11-02",items:[{p:"*",n:"Menu bebas",q:10}],u:{}}]};D.mem.push(m);
 const pk=m.packs[0];const tx={at:"2026-10-08T00:14:00",items:[{q:1,n:"Butterscotch"},{q:6,n:"Black Caffe"},{q:1,n:"Matcha Latte"}],sub:{m:"m1",nm:"Tama"}};
 let o=[];try{o.push(waCust(tx))}catch(e){o.push("ERR "+e.message)}
 try{o.push(waInfo(m))}catch(e){o.push("ERR "+e.message)}
 m.packs=[];o.push(waInfo(m));return o.join("\n\n=====\n\n")}));
await b.close()})();
