const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const pg=await b.newPage({viewport:{width:390,height:800}});pg.on('pageerror',e=>console.log('ERR',e.message));
await pg.addInitScript(()=>sessionStorage.setItem('k521-hi','1'));await pg.goto('file://'+process.cwd()+'/premium.html');await pg.waitForTimeout(800);
await pg.evaluate(()=>{document.querySelectorAll('.hi').forEach(e=>e.remove());document.getElementById('pub').hidden=true;document.getElementById('app').hidden=false;try{inCart=false;qrSheet()}catch(e){console.log('E',e.message)}});
await pg.waitForTimeout(500);await pg.screenshot({path:'qr.png'});await b.close()})()
