const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:390,height:900}});const errs=[];p.on('pageerror',e=>errs.push(e.message));
await p.addInitScript(()=>{try{sessionStorage.setItem('k521-hi','1')}catch(e){}});
await p.goto('file://'+process.cwd()+'/../dist/preview.html');await p.waitForTimeout(800);
await p.evaluate(()=>{document.querySelectorAll('.hi').forEach(e=>e.remove());K.posts.push({id:'tn1',type:'news',title:'Kayak Kenal?',body:'Menu baru Butterscotch sudah hadir dengan karamel gurih yang bikin nagih. Mampir ya, kami tunggu di cart kami setiap hari. Ada bonus topping di minggu ini untuk pembelian pertama.',created:'2026-10-05'},{id:'tn2',type:'news',title:'Libur Jumat',body:'Tutup sehari.',date:'2026-10-09'});pubRender()});
await p.waitForTimeout(400);const el=await p.$('.k-news');await el.scrollIntoViewIfNeeded();await p.waitForTimeout(600);
await p.screenshot({path:'news.png'});
await el.click({position:{x:30,y:30}});await p.waitForTimeout(500);const v=await p.$eval('#pv',e=>!e.hidden);console.log('open',v,'ERRS',errs);await b.close()})();
