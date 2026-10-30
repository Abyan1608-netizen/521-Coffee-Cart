const {chromium,devices}=require('playwright');
const SRV="http://127.0.0.1:8787",KEY="kunci-owner-rahasia-123",SHOT="/home/claude/work/v10/";
const ARGS={args:['--disable-features=LocalNetworkAccessChecks,LocalNetworkAccessChecksWebSockets,PrivateNetworkAccessSendPreflights,PrivateNetworkAccessRespectPreflightResults,BlockInsecurePrivateNetworkRequests']};
const W=ms=>new Promise(r=>setTimeout(r,ms));
let fails=0;const ok=(c,msg)=>{console.log((c?"  ✔ ":"  ✘ GAGAL: ")+msg);if(!c)fails++};
async function mk(b,name){const ctx=await b.newContext({...devices['Pixel 7']});
  await ctx.route('**/shim.js',async r=>{const res=await r.fetch();let t=await res.text();t=t.replace(/server:"[^"]*"/,`server:"${SRV}"`).replace('.replace(/^http/,"ws")+"/room/"','.replace(/^http/,"ws").replace("8787","8788")+"/room/"');r.fulfill({response:res,body:t})});
  await ctx.route('**/index.html',async r=>{const res=await r.fetch();let t=await res.text();t=t.replace(/connect-src [^;]*;/,`connect-src 'self' ${SRV} ws://127.0.0.1:8788;`);r.fulfill({response:res,body:t})});
  let kbody=null;
  await ctx.route('**/kdata.js',async r=>{if(kbody)return r.fulfill({body:kbody,contentType:'text/javascript'});r.continue()});
  await ctx.exposeFunction('__kstore',t=>{kbody=t});
  await ctx.addInitScript(()=>{window.__nat=[];window.A521Native={postMessage(s){const m=JSON.parse(s);window.__nat.push(m.m);if(m.m==='kStore')window.__kstore(m.a.text);const r=m.m==='notifStatus'?{id:m.id,ok:true,r:{perm:true,brand:'samsung',strict:false,battery:true,sdk:34}}:{id:m.id,ok:true};setTimeout(()=>this.onmessage&&this.onmessage({data:JSON.stringify(r)}),5)},onmessage:null};try{localStorage.setItem("a521hp","1");localStorage.setItem("a521npa","-1")}catch(e){}});
  const p=await ctx.newPage();p.__ctx=ctx;p.on('pageerror',e=>{console.log(name,'PAGEERR',e.message);fails++});
  p.on('console',m=>{if(m.type()==='error'&&!/40[1349]|423|Failed to load resource/.test(m.text()))console.log(name,'ERR',m.text().slice(0,200))});return p}
async function localLogin(p,id,pin){await p.evaluate(()=>showLogin());await W(300);await p.evaluate(v=>{lsel=v;loginView()},id);
  for(const d of pin)await p.click(`[data-a=kp][data-v="${d}"]`);await W(1500)}
async function acctLogin(p,name,pin){await p.evaluate(()=>showLogin());await W(400);await p.fill('#acn',name);await p.fill('#acp',pin);await p.click('[data-a=acgo]');await W(800);try{await p.waitForFunction(()=>me||!acBusy,null,{timeout:40000})}catch(e){}await W(2500)}
const st=p=>p.evaluate(()=>({fg:D.fg.filter(b=>b.q>0).map(b=>b.n+":"+b.q).sort().join(", "),susu:(ing("su")||{}).qty,sq:(D.sq||[]).length,code:C().teamCode,bad:teamBad,me:me&&me.name}));
async function newUser(O,name,role,pin){await O.evaluate(()=>{tab="set";setSub="tim";render()});await W(200);await O.click('[data-a=newu]');await W(300);
  await O.fill('#u-name',name);if(role!=="barista"){await O.click(`[data-a=urole][data-v=${role}]`);await W(200)}await O.fill('#u-pin',pin);await O.click('[data-a=usave]');await W(900)}

(async()=>{
  const b=await chromium.launch(ARGS);
  console.log("1) HP Owner (HP Raihan, punya Kunci Owner)");
  const O=await mk(b,'OWNER');await O.goto('http://127.0.0.1:8099/index.html');await W(2500);
  await O.evaluate(()=>showLogin());await W(400);
  ok(await O.evaluate(()=>!$("#ulist").hidden),"server belum punya akun → HP pertama tetap bisa pakai akun bawaan");
  await localLogin(O,'own','1234');await O.fill('#u-pin','8642');await O.click('[data-a=usave]');await W(900);
  await O.evaluate(k=>{localStorage.setItem('a521owner',k);localStorage.setItem('a521ownerOk','1')},KEY);await O.reload();await W(2500);
  await localLogin(O,'own','8642');await W(5000);
  const oc=await O.evaluate(()=>[me&&me.name,isHub(),C().teamCode]);ok(oc[1]&&/^521-/.test(oc[2]),"HP Owner otomatis menyiapkan kunci tim (tanpa tombol) "+oc[2]);
  await newUser(O,"Raka","barista","2468");await newUser(O,"Sari","reseller","1357");await newUser(O,"Urwah Sefri","owner","5210");
  await newUser(O,"raka ","barista","9999");ok(await O.evaluate(()=>!$("#m").hidden&&/sudah dipakai/.test(document.body.innerText)),"nama kembar ditolak");await O.evaluate(()=>shut());
  const sari=await O.evaluate(()=>{const u=D.users.find(x=>x.name==="Sari");return u&&[u.role,u.title,u.perm.join(",")]});ok(sari&&sari[1]==="Reseller"&&sari[2]==="pos,dash","peran Reseller: jabatan & akses awal "+JSON.stringify(sari));
  await O.evaluate(()=>{eu=JSON.parse(JSON.stringify(D.users.find(x=>x.name==="Sari")));usrSheet()});await W(300);await O.screenshot({path:SHOT+"s_peran_reseller.png"});await O.evaluate(()=>shut());
  await W(6000);
  const on=await (await fetch(SRV+"/acct/on")).json();ok(on.on,"daftar akun terunggah ke server");
  await O.evaluate(()=>{tab="set";setSub="sinkron";render()});await W(300);await O.screenshot({path:SHOT+"s_sinkron_owner.png",fullPage:true});
  console.log("   owner:",JSON.stringify(await st(O)));

  console.log("2) HP Bang Urwah: sudah punya stok botol (data lama di HP itu)");
  const U=await mk(b,'URWAH');await U.goto('http://127.0.0.1:8099/index.html');await W(2500);
  await U.evaluate(()=>{const mkb=(id,p,n,q,made,exp)=>({id,p,n,q,q0:q,made,exp,at:new Date().toISOString(),by:"Urwah",ok:1});
    D.fg=[mkb("bU1","palm","Palm Sugar",5,"2026-10-30","2026-11-05"),mkb("bU2","butter","Butterscotch",9,"2026-10-29","2026-11-01"),mkb("bU3","americano","Black Caffe",9,"2026-10-29","2026-11-01")];save()});
  await U.evaluate(()=>showLogin());await W(500);
  ok(await U.evaluate(()=>$("#ulist").hidden&&!!$("#acn")),"HP baru: layar masuk = nama & PIN (tanpa kode tim, akun bawaan disembunyikan)");
  await U.screenshot({path:SHOT+"s_masuk_baru.png"});
  await acctLogin(U,"urwah  sefri","5210");
  ok(await U.evaluate(()=>me&&me.name==="Urwah Sefri"&&own()),"Bang Urwah masuk dengan nama & PIN → peran Owner");
  await W(5000);console.log("   urwah:",JSON.stringify(await st(U)));
  await W(4000);const so=await st(O);console.log("   owner:",JSON.stringify(so));
  ok(so.fg==="Black Caffe:9, Butterscotch:9, Palm Sugar:5","stok di HP Bang Urwah sekarang juga ada di HP Owner");

  console.log("3) HP Barista Raka (baru)");
  const B=await mk(b,'BARISTA');await B.goto('http://127.0.0.1:8099/index.html');await W(2500);
  await B.evaluate(()=>showLogin());await W(300);await B.fill('#acn','Raka');await B.fill('#acp','1111');await B.click('[data-a=acgo]');await W(2500);
  ok(/belum cocok/.test(await B.evaluate(()=>$("#acerr").textContent)),"PIN salah ditolak server: "+await B.evaluate(()=>$("#acerr").textContent));
  await B.fill('#acp','2468');await B.click('[data-a=acgo]');await W(4500);
  ok(await B.evaluate(()=>me&&me.name==="Raka"&&!own()),"Raka masuk sebagai Barista");
  await W(2500);let sb=await st(B);console.log("   barista:",JSON.stringify(sb));ok(sb.fg==="Black Caffe:9, Butterscotch:9, Palm Sugar:5","stok botol sama di HP Barista");
  await B.evaluate(()=>{tab="pos";posV="botol";render()});await W(300);await B.screenshot({path:SHOT+"s_kasir_botol.png"});
  await B.evaluate(()=>{tab="pos";posV="cup";render()});await W(300);await B.screenshot({path:SHOT+"s_kasir_cup.png"});
  const su0=(await st(O)).susu;
  await B.evaluate(()=>{cart={"palm@b":2,"palm":1};pm="Transfer";pay()});await W(400);await B.evaluate(()=>shut());await W(5000);
  const sO=await st(O),sB=await st(B),sU=await st(U);console.log("   setelah Raka jual 2 botol + 1 cup Palm Sugar:\n   owner",JSON.stringify(sO),"\n   barista",JSON.stringify(sB),"\n   urwah",JSON.stringify(sU));
  ok(sO.fg.includes("Palm Sugar:3")&&sU.fg.includes("Palm Sugar:3")&&sB.fg.includes("Palm Sugar:3"),"botol terjual di HP Barista mengurangi stok di semua HP");
  ok(Math.abs(sO.susu-(su0-85))<0.01&&Math.abs(sB.susu-sO.susu)<0.01,`susu (bahan baku) ikut berkurang di semua HP: ${su0} → ${sO.susu}`);
  const tx=await O.evaluate(()=>D.tx.filter(t=>t.by==="Raka").map(t=>t.total+"/"+t.rx));ok(tx.length===1,"penjualan Raka masuk ke HP Owner lewat server: "+tx);
  ok(await B.evaluate(()=>D.tx.every(t=>t.dev!==DEV||t.sent)),"HP Barista mencatat transaksi sudah terkirim");

  console.log("4) Owner mematikan internet, lalu kembali online");
  await O.__ctx.route('**/t/**',r=>r.abort());
  await O.evaluate(()=>{const b=D.fg.find(x=>x.n==="Butterscotch");cur=null;mvPush({at:iso(),i:"fg:"+b.p,b:b.id,type:"fg-keluar",q:-1,cost:0,sup:"",ref:"uji"});b.q-=1;save()});await W(2500);
  ok((await st(O)).sq>0,"perubahan offline tersimpan di antrean HP Owner");
  await O.__ctx.unroute('**/t/**');await O.evaluate(()=>syncKick());await W(4000);
  ok((await st(O)).sq===0&&(await st(B)).fg.includes("Butterscotch:8"),"setelah online, antrean terkirim & HP lain ikut: "+(await st(B)).fg);

  console.log("5) HP Reseller Sari");
  const S=await mk(b,'RESELLER');await S.goto('http://127.0.0.1:8099/index.html');await W(2500);await acctLogin(S,"sari","1357");
  const sr=await S.evaluate(()=>[me&&me.name,ch,can("pos"),can("stk"),can("menu")]);ok(sr[0]==="Sari"&&/reseller/i.test(sr[1])&&sr[2]&&!sr[3]&&!sr[4],"Reseller: saluran otomatis Reseller, hanya akses yang diizinkan "+JSON.stringify(sr));

  console.log("6) Owner menghapus Raka → HP Raka terputus, HP lain tersambung lagi sendiri");
  await O.evaluate(()=>{const u=D.users.find(x=>x.name==="Raka");openUsr(u.id)});await W(300);await O.click('[data-a=udel]');await W(300);await O.click('[data-a=udgo]');await W(6000);
  const c2=await O.evaluate(()=>C().teamCode);ok(c2!==oc[2],"kunci tim diganti otomatis");
  await B.evaluate(()=>stSync());await W(4000);
  const bb=await B.evaluate(()=>[!!me,teamBad,!$("#login").hidden,$("#acn")?1:0]);ok(!bb[0]&&bb[1]&&bb[2]&&bb[3],"HP Raka keluar & tidak bisa sinkron lagi "+JSON.stringify(bb));
  await B.fill('#acn','Raka');await B.fill('#acp','2468');await B.click('[data-a=acgo]');await W(2500);
  ok(/belum terdaftar/.test(await B.evaluate(()=>$("#acerr").textContent)),"Raka tidak bisa masuk lagi");
  await S.evaluate(()=>stSync());await W(5000);
  const ss=await st(S);ok(ss.code===c2&&!ss.bad&&ss.me==="Sari","HP Sari tersambung lagi otomatis dengan kunci baru");
  await U.evaluate(()=>stSync());await W(5000);ok((await st(U)).code===c2,"HP Bang Urwah tersambung lagi otomatis");
  ok(!(await st(O)).bad,"HP Owner tetap tersambung");
  await S.evaluate(()=>{cart={"butter@b":1};pm="Cash";paid=99999;pay()});await W(400);await S.evaluate(()=>shut());await W(5000);
  ok((await st(O)).fg.includes("Butterscotch:7"),"penjualan setelah ganti kunci tetap sinkron: "+(await st(O)).fg);

  console.log("7) Stok Bang Urwah: hapus batch dari HP Owner");
  await O.evaluate(()=>{const b=D.fg.find(x=>x.n==="Black Caffe");document.body.insertAdjacentHTML("beforeend",`<div id="s" data-v="${b.id}"></div>`);tab="stk";render()});
  await O.evaluate(()=>{const b=D.fg.find(x=>x.n==="Black Caffe");$("#s").dataset.v=b.id;document.body.insertAdjacentHTML("beforeend",'<button id="tdel" data-a="fgdelgo">x</button>')});await O.$eval('#tdel',e=>e.click());await W(5000);
  ok(!(await st(U)).fg.includes("Black Caffe"),"batch yang dihapus hilang di semua HP: "+(await st(U)).fg);
  await U.evaluate(()=>{tab="stk";stkV="fg";render()});await W(300);await U.screenshot({path:SHOT+"s_stok_urwah.png"});
  console.log("8) HP lama yang dulu tersambung pakai kode tim (versi sebelumnya), lalu diperbarui");
  const V=await mk(b,'HPLAMA');await V.goto('http://127.0.0.1:8099/index.html');await W(2500);
  const code=await O.evaluate(()=>C().teamCode);
  await V.evaluate(async c=>{const T=K.team;const o=await teamOpen(c,T);D.cfg.teamCode=c;teamApply(o,T);delete D.cfg.stkMig;
    D.fg.push({id:"bOLD",p:"matcha",n:"Matcha Latte",q:4,q0:4,made:"2026-10-30",exp:"2026-11-03",at:new Date().toISOString(),by:"x",ok:1});localStorage.setItem("pos521",JSON.stringify(D))},code);
  await V.reload();await W(6000);
  await V.evaluate(()=>showLogin());await W(400);
  ok(await V.evaluate(()=>!$("#ulist").hidden&&!$("#acn")),"HP yang sudah tersambung tetap pakai daftar akun + keypad (bisa offline)");
  ok((await st(O)).fg.includes("Matcha Latte:4"),"stok lama di HP itu ikut masuk ke stok bersama: "+(await st(O)).fg);
  console.log(fails?`\nADA ${fails} YANG GAGAL`:"\nSEMUA LULUS");
  await b.close();
})();
