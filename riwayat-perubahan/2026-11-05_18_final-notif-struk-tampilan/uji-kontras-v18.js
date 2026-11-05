// Audit kontras teks tema terang/gelap di semua layar utama
const {chromium,devices}=require('playwright');
const MODE=process.argv[2]||'light',OUT='/home/claude/work/v18/';
const W=ms=>new Promise(r=>setTimeout(r,ms));
const AUDIT=()=>{const res=[];const p=s=>{const m=s.match(/rgba?\(([^)]+)\)/);if(!m)return null;const a=m[1].split(/[ ,\/]+/).filter(Boolean).map(Number);return {r:a[0],g:a[1],b:a[2],a:a.length>3?a[3]:1}};
 const L=c=>{const f=v=>{v/=255;return v<=.04045?v/12.92:Math.pow((v+.055)/1.055,2.4)};return .2126*f(c.r)+.7152*f(c.g)+.0722*f(c.b)};
 const mix=(top,bot)=>({r:top.r*top.a+bot.r*(1-top.a),g:top.g*top.a+bot.g*(1-top.a),b:top.b*top.a+bot.b*(1-top.a),a:1});
 const bgOf=el=>{const stack=[];let e=el;while(e&&e.nodeType===1){const cs=getComputedStyle(e);if(cs.backgroundImage&&cs.backgroundImage!=='none'&&!/gradient/.test(cs.backgroundImage))return null; const c=p(cs.backgroundColor);if(c&&c.a>0){stack.push(c);if(c.a>=.99)break}
   if(/gradient/.test(cs.backgroundImage)){const m=cs.backgroundImage.match(/rgba?\([^)]+\)/g);if(m){const c2=p(m[0]);if(c2){stack.push({...c2,a:Math.max(c2.a,.99)});break}}}
   e=e.parentElement}
  let base=p(getComputedStyle(document.body).backgroundColor)||{r:255,g:255,b:255,a:1};if(base.a<1)base={...base,a:1};let c=base;for(let i=stack.length-1;i>=0;i--)c=mix(stack[i],c);return c};
 const walker=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);const seen=new Set();let n;
 while(n=walker.nextNode()){const t=n.textContent.trim();if(!t)continue;const el=n.parentElement;if(!el||seen.has(el))continue;seen.add(el);
  const r=el.getBoundingClientRect();if(r.width<2||r.height<2)continue;const cs=getComputedStyle(el);if(cs.visibility==='hidden'||+cs.opacity<.1)continue;
  if(el.closest('[hidden],.modal[hidden]'))continue;let op=1,e=el;while(e){op*=+getComputedStyle(e).opacity;e=e.parentElement}if(op<.35)continue;
  const fg=p(cs.color);const bg=bgOf(el);if(!fg||!bg)continue;const f2=fg.a<1?mix(fg,bg):fg;const l1=L(f2),l2=L(bg);const cr=(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05);
  const fs=parseFloat(cs.fontSize),bold=+cs.fontWeight>=600;const big=fs>=24||(fs>=18.66&&bold);const need=big?3:4.5;
  if(cr<need)res.push({t:t.slice(0,40),cr:+cr.toFixed(2),need,fs,cls:(el.className&&el.className.baseVal===undefined?el.className:'')+'|'+el.tagName,fg:cs.color,bg:`rgb(${bg.r|0},${bg.g|0},${bg.b|0})`})}
 return res};
(async()=>{const b=await chromium.launch({args:['--disable-features=LocalNetworkAccessChecks,LocalNetworkAccessChecksWebSockets,PrivateNetworkAccessSendPreflights,PrivateNetworkAccessRespectPreflightResults,BlockInsecurePrivateNetworkRequests']});const ctx=await b.newContext({...devices['Pixel 7']});const SRV="http://127.0.0.1:8787";
 await ctx.route('**/shim.js',async r=>{const res=await r.fetch();let t=await res.text();t=t.replace(/server:"[^"]*"/,`server:"${SRV}"`).replace('.replace(/^http/,"ws")+"/room/"','.replace(/^http/,"ws").replace("8787","8788")+"/room/"');r.fulfill({response:res,body:t})});
 await ctx.route('**/index.html',async r=>{const res=await r.fetch();let t=await res.text();t=t.replace(/connect-src [^;]*;/,`connect-src 'self' ${SRV} ws://127.0.0.1:8788;`);r.fulfill({response:res,body:t})});
 await ctx.addInitScript(()=>{try{localStorage.setItem("a521hp","1");localStorage.setItem("a521npa","-1")}catch(e){}});
 const p=await ctx.newPage();p.on('pageerror',e=>console.log('PAGEERR',e.message));
 await p.goto('http://127.0.0.1:8099/index.html');await W(2500);
 await p.evaluate(m=>{const c=C();c.theme=m;c.uiSet=1;save();look()},MODE);await W(300);
 const shots=[];const snap=async(name)=>{await W(700);const r=await p.evaluate(AUDIT);shots.push([name,r]);await p.screenshot({path:OUT+`c_${MODE}_${name}.png`,fullPage:false})};
 await p.evaluate(()=>{try{pubRender()}catch(e){}});await snap('publik');
 await p.evaluate(()=>showLogin());await W(400);await snap('login');
 await p.evaluate(()=>{lsel='own';loginView()});for(const d of '1234')await p.click(`[data-a=kp][data-v="${d}"]`);await W(1500);
 if(await p.$('#u-pin')){await p.fill('#u-pin','8642');await p.click('[data-a=usave]');await W(900)}
 for(const t of ['pos','dash','stk','mem','kabar','resep','set']){await p.evaluate(v=>{tab=v;setSub="";render();scrollTo(0,0)},t);await snap(t)}
 for(const s of ['notif','tampil','printer','toko','buka','publik','tim']){await p.evaluate(v=>{tab="set";setSub=v;render();scrollTo(0,0)},s);await snap('set_'+s)}
 // transaksi: tambah 2 item lalu bayar
 await p.evaluate(()=>{tab="pos";setSub="";render()});await W(300);for(let i=0;i<2;i++){const x=await p.$("[data-a=add]");if(x){await x.click();await W(300)}}
 await W(300);await snap('pos_cart');
 let tot=0;for(const [n,r] of shots){tot+=r.length;console.log(`== ${n}: ${r.length} teks kontras rendah`);r.slice(0,14).forEach(x=>console.log('   ',x.cr,'<',x.need,JSON.stringify(x.t),x.cls,x.fg,'on',x.bg))}
 console.log('TOTAL',tot);await b.close()})();
