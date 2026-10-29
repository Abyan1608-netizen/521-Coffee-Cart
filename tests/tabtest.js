const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();
for(const [n,w,h] of [['land',1024,768],['port',768,1024]]){
const p=await b.newPage({viewport:{width:w,height:h}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{try{sessionStorage.setItem('k521-hi','1')}catch(e){}});
await p.goto('file://'+process.cwd()+'/premium.html');await p.waitForTimeout(800);
await p.evaluate(()=>{document.querySelectorAll('.hi').forEach(e=>e.remove());const c=document.createElement('canvas');c.width=800;c.height=1000;const x=c.getContext('2d');const g=x.createLinearGradient(0,0,800,1000);g.addColorStop(0,'#c46');g.addColorStop(1,'#46c');x.fillStyle=g;x.fillRect(0,0,800,1000);x.fillStyle='#fff';x.font='80px sans-serif';x.fillText('FOTO',300,500);const u=c.toDataURL('image/jpeg');
K.posts.unshift({id:'tn1',type:'news',title:'Kayak Kenal?',img:u,body:'Menu baru Butterscotch sudah hadir dengan karamel gurih yang bikin nagih. Mampir ya, kami tunggu di cart kami setiap hari.',created:'2026-10-05'});pubRender();document.getElementById('pub').hidden=false;document.getElementById('login').hidden=true});
await p.waitForTimeout(600);const el=await p.$('.k-news');await el.scrollIntoViewIfNeeded();await p.waitForTimeout(700);
await p.screenshot({path:'tab_'+n+'_list.png'});
await p.evaluate(()=>kOpen('tn1'));await p.waitForTimeout(600);await p.screenshot({path:'tab_'+n+'_pv.png'});console.log(n,errs);await p.close()}
await b.close()})();
