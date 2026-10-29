const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const b=await chromium.launch();const errs=[],fails=[];const ok=(c,m)=>{if(!c)fails.push(m)};
const mk=async(canEdit)=>{const ctx=await b.newContext({viewport:{width:400,height:860}});
 await ctx.addInitScript(([ce])=>{sessionStorage.setItem("k521-hi","1");window.claude={use:async n=>n==="user"?{canEdit:async()=>ce}:n==="artifact"&&ce?{publish:async h=>{(window.__pubs=window.__pubs||[]).push(h);return{}}}:null}},[canEdit]);
 const p=await ctx.newPage();p.setDefaultTimeout(4000);p.on('pageerror',e=>errs.push(e.message));return p};
const own=await mk(true);await own.goto('file://'+process.cwd()+'/premium.html');await own.waitForTimeout(300);
await own.click('#pub [data-a=masuk]');await own.fill('#lpw','1234');await own.waitForTimeout(300);await own.click('[data-a=nohelp]').catch(()=>{});
// owner: change barista pin, change a price, activate sync
await own.click('#nav [data-v=set]');await own.click('[data-a=setsub][data-v=tim]');await own.click('[data-a=usr][data-id=bar]');await own.fill('#u-pin','7777');await own.click('[data-a=usave]');await own.click('[data-a=setsub][data-v=""]');
await own.evaluate(()=>{prod("palm").price=16000;save()});
await own.click('[data-a=setsub][data-v=sinkron]');await own.click('[data-a=tson]');await own.waitForTimeout(2500);
const code=await own.textContent('#tcv');console.log('code',code);
const pubs=await own.evaluate(()=>window.__pubs||[]);ok(pubs.length>=1,'published');const html=pubs[pubs.length-1];fs.writeFileSync('team_pub.html',html);
ok(!html.includes('7777')&&!/"pin":"1234"/.test(html),'no plaintext pin');ok(html.includes('"team":{'),'team bundle');
await own.screenshot({path:'tm1.png'});
// staff device
const st=await mk(false);await st.goto('file://'+process.cwd()+'/team_pub.html');await st.waitForTimeout(300);
await st.click('#pub [data-a=masuk]');await st.waitForTimeout(300);ok(await st.isVisible('#tcode'),'join card');await st.screenshot({path:'tm2.png'});
await st.fill('#tcode','WRONG-CODE');await st.click('[data-a=tjoin]');await st.waitForTimeout(1500);ok(await st.isVisible('#tcode'),'wrong code rejected');
await st.fill('#tcode',code.toLowerCase());await st.click('[data-a=tjoin]');await st.waitForTimeout(2000);ok(await st.isVisible('.tok'),'joined');
ok(await st.evaluate(()=>prod("palm").price)===16000,'price synced');ok(await st.evaluate(()=>!!D.users.find(u=>u.id==="bar").ph&&D.users.find(u=>u.id==="bar").pin===undefined),'hashed users');
await st.click('[data-a=lsel][data-v=bar]');await st.fill('#lpw','0000');await st.press('#lpw','Enter');await st.waitForTimeout(500);ok(await st.isVisible('#lerr')&&(await st.textContent('#lerr')).length>0,'old pin rejected');
await st.fill('#lpw','7777');await st.waitForTimeout(800);ok(await st.isVisible('#app'),'new pin login');await st.click('[data-a=nohelp]').catch(()=>{});
await st.click('[data-a=add][data-id=palm]');await st.screenshot({path:'tm3.png'});
// reload keeps cart
console.log('ss',await st.evaluate(()=>sessionStorage.getItem('pos521c')));await st.reload();await st.waitForTimeout(800);console.log('after',await st.evaluate(()=>JSON.stringify(cart)+sessionStorage.getItem('pos521c')));ok((await st.evaluate(()=>cart.palm))===1,'cart kept after reload');
// owner updates again -> new publish; staff loads new version and pulls
await own.evaluate(()=>{prod("butter").price=21000;save()});await own.waitForTimeout(2200);
const pubs2=await own.evaluate(()=>window.__pubs);ok(pubs2.length>pubs.length,'auto re-publish');fs.writeFileSync('team_pub2.html',pubs2[pubs2.length-1]);
await st.goto('file://'+process.cwd()+'/team_pub2.html');await st.waitForTimeout(1500);ok(await st.evaluate(()=>prod("butter").price)===21000,'staff pulled update');
// public visitor
const pv=await mk(false);await pv.goto('file://'+process.cwd()+'/team_pub2.html');await pv.waitForTimeout(500);ok((await pv.textContent('.k-menu')).includes('16.000'),'public menu updated');
console.log('FAILS',fails,'ERRS',errs);await b.close()})();
