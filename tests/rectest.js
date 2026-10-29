const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const errs=[],fails=[];const ok=(c,m)=>{if(!c)fails.push(m)};
const ctx=await b.newContext({viewport:{width:400,height:860}});
await ctx.addInitScript(()=>{sessionStorage.setItem("k521-hi","1");window.claude={use:async n=>null}});
const p=await ctx.newPage();p.setDefaultTimeout(3000);p.on('pageerror',e=>errs.push(e.message));
// simulate an old device: seed-like data without recV
await p.goto('file://'+process.cwd()+'/premium.html');await p.waitForTimeout(200);
await p.evaluate(()=>{const d=JSON.parse(localStorage.getItem("pos521"));delete d.cfg.recV;d.prod=d.prod.filter(x=>x.name!=="Black Caffe");d.prod.push({id:"americano",name:"Americano",cat:"Coffee",price:15000,rprice:0,active:1,color:"#8b5e3c",rec:[{i:"esp",q:30},{i:"air",q:170},{i:"cup",q:1},{i:"lid",q:1}]});localStorage.setItem("pos521",JSON.stringify(d))});
await p.reload();await p.waitForTimeout(300);
const st=await p.evaluate(()=>D.prod.map(x=>x.name+":"+x.rec.map(r=>r.i+r.q).join(",")).join(" | "));console.log(st);
ok(st.includes('Black Caffe:espt25,air155,cup1,lid1'),'black caffe migrated');ok(!st.includes('Americano'),'americano renamed');
ok(st.includes('Palm Sugar:esp30,ga15,ks40,su85,cup1,lid1'),'palm');
await p.click('#pub [data-a=masuk]');await p.fill('#lpw','1234');await p.waitForTimeout(200);await p.click('[data-a=nohelp]').catch(()=>{});
await p.click('#nav [data-v=menu]');await p.waitForTimeout(1200);await p.screenshot({path:'rc1.png',fullPage:false});
await p.click('[data-a=rview][data-id=palm]');await p.waitForTimeout(400);await p.screenshot({path:'rc2.png'});
await p.click('[data-a=rsz][data-v="4"]');await p.waitForTimeout(300);ok((await p.textContent('.rbig')).includes('2.425 ml'),'5L susu');
await p.click('.rall summary');await p.waitForTimeout(200);await p.screenshot({path:'rc3.png'});
await p.click('.sheet .x');await p.click('[data-a=rview][data-id=matcha]');await p.waitForTimeout(300);ok((await p.textContent('.rbig')).includes('M 15 · A 40'),'matcha sub');await p.screenshot({path:'rc4.png'});
await p.click('.sheet .x');await p.click('[data-a=edit][data-id=butter]');await p.waitForTimeout(300);
await p.fill('[data-bt="0"][data-bc="1"]','31 ml');await p.click('[data-a=btadd]');await p.locator('.bted').scrollIntoViewIfNeeded();await p.screenshot({path:'rc5.png'});
await p.click('[data-a=btrm][data-id="5"]');await p.click('[data-a=saveP]');await p.waitForTimeout(200);
ok(await p.evaluate(()=>prod("butter").batch.rows[0].v[1])==='31 ml','batch edit saved');
await p.click('[data-a=mcat][data-v="Coffee"]').catch(()=>fails.push('cat chip'));
await p.click('#nav [data-v=set]');await p.click('[data-a=setsub][data-v=resep]').catch(()=>{});await p.waitForTimeout(400);await p.screenshot({path:'rc6.png'});
// barista view recipe
await p.evaluate(()=>logout());await p.click('[data-a=lsel][data-v=bar]');await p.fill('#lpw','0000');await p.waitForTimeout(200);await p.click('[data-a=nohelp]').catch(()=>{});
await p.click('#nav [data-v=resep]');await p.click('[data-a=rview][data-id=palm]');ok(await p.locator('.sheet [data-a=edit]').count()===0,'barista no edit');
// sell one palm and check stock deduct ks
await p.evaluate(()=>logout());
console.log('FAILS',fails,'ERRS',errs);await b.close()})();
