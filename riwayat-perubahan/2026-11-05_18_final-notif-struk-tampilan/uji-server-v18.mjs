// Uji server: notifikasi instan FCM saat promo baru/diubah (JWT ditandatangani benar, dikirim ke topik k521)
import { generateKeyPairSync, createVerify } from "node:crypto";
const W = await import("/home/claude/work/harness/worker.mjs");
const store=new Map(); const sc=v=>v===undefined?undefined:structuredClone(v);
const ctxS={storage:{get:async k=>sc(store.get(k)),put:async(k,v)=>{store.set(k,sc(v))},delete:async k=>{store.delete(k)},list:async()=>new Map()}};
const hubObj=new W.Hub(ctxS,{});
const { privateKey, publicKey } = generateKeyPairSync("rsa", { modulusLength: 2048 });
const SA={type:"service_account",project_id:"coffee521-test",client_email:"fcm@coffee521-test.iam.gserviceaccount.com",private_key:privateKey.export({type:"pkcs8",format:"pem"})};
const mk=(extra)=>({APP_ORIGIN:"http://x",OWNER_KEY:"kunci-owner-rahasia-123",HUB:{idFromName:()=>1,get:()=>hubObj},AUTH_LIMIT:{limit:async()=>({success:true})},CHAT_LIMIT:{limit:async()=>({success:true})},...extra});
let calls=[];const real=globalThis.fetch;
globalThis.fetch=async(u,o)=>{u=String(u);calls.push({u,o});
  if(u==="https://oauth2.googleapis.com/token"){const jwt=new URLSearchParams(o.body).get("assertion");const [h,c,sg]=jwt.split(".");
    const v=createVerify("RSA-SHA256");v.update(h+"."+c);const ok=v.verify(publicKey,Buffer.from(sg,"base64url"));const cl=JSON.parse(Buffer.from(c,"base64url"));
    globalThis.__jwt={ok,cl};return new Response(JSON.stringify({access_token:"ya29.test",expires_in:3600}),{status:ok?200:400})}
  if(u.startsWith("https://fcm.googleapis.com/")){return new Response("{}",{status:200})}
  return real(u,o)};
let fails=0;const ok=(c,m)=>{console.log((c?"  ✔ ":"  ✘ GAGAL: ")+m);if(!c)fails++};
const waits=[];const ctx={waitUntil:p=>waits.push(p)};
async function put(env,k){const g=await W.default.fetch(new Request("http://w/k"),env,ctx);const base=g.status===200?(await g.json()).rev:0;
  const r=await W.default.fetch(new Request("http://w/k",{method:"PUT",headers:{Authorization:"Bearer kunci-owner-rahasia-123","Content-Type":"application/json"},body:JSON.stringify({base,k})}),env,ctx);
  await Promise.all(waits.splice(0));return r.json()}
const P=(id,t,extra={})=>({id,type:"promo",title:t,body:"isi",draft:false,...extra});
console.log("1) Tanpa FCM_SA: tidak mengirim apa pun");
let env=mk({});calls=[];let r=await put(env,{store:{},posts:[P("a","Promo A")]});
ok(r.rev>0&&r.push===0&&!calls.some(c=>/googleapis/.test(c.u)),"terbit biasa, tanpa push");
ok((await (await W.default.fetch(new Request("http://w/push"),env,ctx)).json()).on===false,"/push → on:false");
console.log("2) Dengan FCM_SA: promo baru → push ke topik k521");
env=mk({FCM_SA:JSON.stringify(SA)});calls=[];r=await put(env,{store:{},posts:[P("a","Promo A"),P("b","Diskon B",{dval:3000})]});
const send=calls.find(c=>c.u.startsWith("https://fcm.googleapis.com/"));
ok(globalThis.__jwt&&globalThis.__jwt.ok,"JWT service account ditandatangani benar (RS256)");
ok(globalThis.__jwt&&globalThis.__jwt.cl.scope==="https://www.googleapis.com/auth/firebase.messaging"&&globalThis.__jwt.cl.iss===SA.client_email,"klaim JWT benar");
ok(send&&send.u==="https://fcm.googleapis.com/v1/projects/coffee521-test/messages:send","dikirim ke proyek Firebase yang benar");
const body=send&&JSON.parse(send.o.body);ok(body&&body.message.topic==="k521"&&body.message.android.priority==="HIGH"&&body.message.data.n==="1"&&!/Diskon B/.test(send.o.body),"topik k521, prioritas tinggi, isi promo tidak dikirim ke Google: "+JSON.stringify(body&&body.message.data));
ok(send&&send.o.headers.Authorization==="Bearer ya29.test","memakai token akses");
ok(r.push===1,"jawaban PUT menandai push");
console.log("3) Ubah menu saja (promo sama) → tidak push");
calls=[];r=await put(env,{store:{name:"x"},menu:[{n:"Kopi",p:1}],posts:[P("a","Promo A"),P("b","Diskon B",{dval:3000})]});
ok(!calls.some(c=>/fcm.googleapis/.test(c.u))&&r.push===0,"tanpa push");
console.log("4) Promo diubah → push; token dipakai ulang");
calls=[];r=await put(env,{store:{},posts:[P("a","Promo A — diperpanjang"),P("b","Diskon B",{dval:3000})]});
ok(calls.some(c=>/fcm.googleapis/.test(c.u))&&!calls.some(c=>/oauth2/.test(c.u)),"push terkirim, token tidak diminta ulang");
console.log("5) Draf → tidak push");
calls=[];r=await put(env,{store:{},posts:[P("a","Promo A — diperpanjang"),P("b","Diskon B",{dval:3000}),P("c","Draf",{draft:true})]});
ok(!calls.some(c=>/fcm.googleapis/.test(c.u)),"draf tidak memicu push");
console.log("6) FCM_SA rusak → terbit tetap jalan");
env=mk({FCM_SA:"bukan json"});calls=[];r=await put(env,{store:{},posts:[P("d","Baru D")]});ok(r.rev>0&&r.push===0,"terbit tetap berhasil");
console.log(fails?`\nADA ${fails} YANG GAGAL`:"\nSEMUA LULUS");process.exit(fails?1:0);
