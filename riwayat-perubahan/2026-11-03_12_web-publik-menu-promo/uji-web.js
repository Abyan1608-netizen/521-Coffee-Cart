const {chromium,devices}=require('playwright');const fs=require('fs');
(async()=>{
  const raw=fs.readFileSync('/home/claude/proj/521-coffee-app/android/app/src/main/assets/www/kdata.js','utf8');const K=JSON.parse(raw.slice(raw.indexOf('window.__K=')+11).replace(/;\s*$/,''));delete K.team;
  K.posts=(K.posts||[]);K.posts.unshift({id:"pweb1",type:"promo",title:"PROMO UJI WEB 521",body:"Beli 2 gratis 1 khusus hari ini",badge:"Hari ini",start:"",end:""});
  const r=await fetch("http://127.0.0.1:8787/k",{method:"PUT",headers:{Authorization:"Bearer kunci-owner-rahasia-123"},body:JSON.stringify({base:0,k:K})});console.log("terbit",r.status);
  const b=await chromium.launch();const ctx=await b.newContext({...devices['Pixel 7']});
  await ctx.route('**/kdata.js',async rt=>{const x=await fetch("http://127.0.0.1:8787/kdata.js");rt.fulfill({status:200,contentType:"text/javascript",body:await x.text()})});
  const p=await ctx.newPage();const errs=[];p.on('pageerror',e=>errs.push(e.message));p.on('console',m=>{if(m.type()==='error')errs.push(m.text())});
  await p.goto('http://127.0.0.1:8098/');await p.waitForTimeout(1200);try{await p.click('text=Lewati',{timeout:2500})}catch(e){}await p.waitForTimeout(1500);
  const t=await p.evaluate(()=>document.body.innerText);
  console.log("promo terbaru tampil:",/PROMO UJI WEB 521/.test(t),"| tombol Masuk:",await p.evaluate(()=>!!document.querySelector('[data-a=masuk]')),"| Download aplikasi:",await p.evaluate(()=>[...document.querySelectorAll('a.k-login,a.k-app')].map(a=>a.href)));
  await p.screenshot({path:'w_atas.png'});
  await p.evaluate(()=>{const e=document.querySelector('.k-app');if(e)e.scrollIntoView({block:"center"})});await p.waitForTimeout(400);await p.screenshot({path:'w_bawah.png'});
  await p.goto('http://127.0.0.1:8098/#masuk');await p.waitForTimeout(2500);
  console.log("buka #masuk → login tampil?",await p.evaluate(()=>!$("#login").hidden),"| app kasir tampil?",await p.evaluate(()=>!$("#app").hidden));
  await p.evaluate(()=>{try{showLogin()}catch(e){}});await p.waitForTimeout(300);console.log("showLogin() dipaksa → login tampil?",await p.evaluate(()=>!$("#login").hidden));
  await p.evaluate(()=>{document.querySelector('.k-fab')&&document.querySelector('.k-fab').click()});await p.waitForTimeout(500);console.log("tombol Pesan sekarang buka lembar:",await p.evaluate(()=>!$("#m").hidden));
  console.log('ERRORS',errs.length?errs:'none');await b.close()})()
