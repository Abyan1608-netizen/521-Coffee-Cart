import re
s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
i=s.index("function welcome(){");j=s.index("\n}\n",i)+3
s=s[:i]+r'''const hiCfg=()=>{const c=(K.store&&K.store.intro)||{};return{on:c.on!==0,sec:Math.min(10,Math.max(3,+c.sec||6)),fs:Math.min(130,Math.max(80,+c.fs||100))}};
let hiN=0;
/* Layar pembuka. host = body (asli) atau bingkai preview di Atur. Durasi diskalakan lewat playbackRate (desain dasar 6 detik). */
function hiPlay(host,prev,cfg){
  cfg=cfg||hiCfg();const k=cfg.sec/6,rate=1/k,n=++hiN;
  const paths=[...document.querySelectorAll("#logo path")].map((p,i)=>`<path pathLength="1" style="--i:${i}" d="${p.getAttribute("d")}"/>`).join("");
  const nm=esc(K.store.name||C().name||"521 Coffee"),tg=esc(K.store.tagline||C().sub||"");
  const word=(t,d0)=>[...t].map((ch,i)=>`<span style="--d:${(d0+i*.055).toFixed(3)}s">${ch===" "?"&nbsp;":esc(ch)}</span>`).join("");
  const w=document.createElement("div");w.className="hi"+(prev?" prev":"");w.style.setProperty("--fs",cfg.fs/100);
  if(!prev){w.setAttribute("role","dialog");w.setAttribute("aria-label","Selamat datang di "+(K.store.name||"521 Coffee"))}else w.setAttribute("aria-hidden","true");
  w.innerHTML=`<div class="hi-glow"></div><div class="hi-pos"><div class="hi-c"><div class="hi-logo"><svg viewBox="210 60 1565 1015" aria-hidden="true"><defs><clipPath id="hiclip${n}">${paths}</clipPath><linearGradient id="hisg${n}" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".9"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient></defs><g class="hi-stroke">${paths}</g><g class="hi-fill">${paths}</g><g clip-path="url(#hiclip${n})"><rect class="hi-sh" x="-200" y="0" width="420" height="1200" fill="url(#hisg${n})"/></g></svg></div>
    <h1 class="hi-t">${word("Selamat datang",1.95)}</h1><p class="hi-s">di <b>${nm}</b></p>${tg?`<p class="hi-g">${tg}</p>`:""}</div></div>
    <button class="hi-skip" data-hi="skip" tabindex="${prev?-1:0}">Lewati</button>`;
  host.appendChild(w);if(!prev)document.documentElement.classList.add("hi-on");
  const speed=el=>{try{getComputedStyle(el).opacity;el.getAnimations({subtree:true}).forEach(a=>a.playbackRate=rate)}catch(e){}};speed(w);
  const PHI=1.618,fit=()=>{const t=w.querySelector(".hi-t"),L=w.querySelector(".hi-logo");if(!t||!L)return;const tw=t.offsetWidth;if(!tw)return;
    const lw=tw/PHI,lh=lw*1015/1565;L.style.width=lw+"px";t.style.marginTop=(lh/(PHI*PHI*PHI))+"px"};
  fit();try{document.fonts&&document.fonts.ready.then(fit)}catch(e){}
  let done=false;const P=$("#pub"),timers=[];
  const end=()=>{if(done)return;done=true;timers.forEach(clearTimeout);w.classList.add("out");speed(w);
    if(prev){setTimeout(()=>{w.remove();const f=host.closest(".hiframe");if(f)f.classList.add("ended")},1350*k);return}
    P.classList.add("hi-in");speed(P);
    setTimeout(()=>{PX0=Date.now();P.classList.remove("intro");void P.offsetWidth;pubRender();P.classList.add("intro");clearTimeout(P._t);P._t=setTimeout(()=>P.classList.remove("intro"),1400)},480*k);
    setTimeout(()=>{w.remove();document.documentElement.classList.remove("hi-on");P.classList.remove("hi-in")},1350*k)};
  w.addEventListener("click",e=>{e.stopPropagation();end()});
  if(!prev)addEventListener("keydown",function kd(e){if(e.key==="Escape"||e.key==="Enter"||e.key===" "){removeEventListener("keydown",kd);end()}});
  timers.push(setTimeout(end,4750*k));
  w._stop=()=>{done=true;timers.forEach(clearTimeout);w.remove()};
  return w;
}
function welcome(){
  let seen=false;try{seen=sessionStorage.getItem("k521-hi")==="1"}catch(e){}
  if(seen||!hiCfg().on||matchMedia("(prefers-reduced-motion: reduce)").matches)return;
  hiPlay(document.body,false);
}
function hiPreview(){const box=$("#hibox");if(!box)return;box.querySelectorAll(".hi").forEach(x=>x._stop&&x._stop());const f=box.closest(".hiframe");if(f)f.classList.remove("ended");hiPlay(box,true)}
'''+s[j:]
# CSS font scale + preview
rep(".hi-c{--F:clamp(32px,8.4vw,60px);",".hi-c{--F:calc(clamp(32px,8.4vw,60px)*var(--fs,1));")
css='''/* Preview layar pembuka (ponsel virtual 390×760, diperkecil) */
.hiframe{position:relative;width:234px;height:456px;margin:14px auto 6px;border-radius:30px;overflow:hidden;border:6px solid var(--sf3);background:#0a0302;box-shadow:0 24px 50px -24px rgba(0,0,0,.8)}
.hibox{position:absolute;left:0;top:0;width:390px;height:760px;transform:scale(.6);transform-origin:0 0}
.hi.prev{position:absolute;z-index:1}
.hi.prev .hi-c{--F:calc(32.76px*var(--fs,1))}
.hiframe .hiagain{position:absolute;inset:0;z-index:2;display:none;place-items:center;border:0;background:rgba(10,3,2,.55);color:#fff;font:700 14px var(--f-b);cursor:pointer}
.hiframe.ended .hiagain{display:grid}
.hiframe .hiagain span{display:inline-flex;align-items:center;gap:8px;padding:10px 16px;border-radius:999px;background:var(--ac);color:var(--on)}
.rng{display:flex;align-items:center;gap:12px}
.rng input[type=range]{flex:1;margin:6px 0;padding:0;border:0;background:none;accent-color:var(--ac)}
.rng output{min-width:52px;text-align:right;font:600 15px var(--f-m)}
'''
k=s.index("/* ---------- Transisi tema ---------- */");s=s[:k]+css+s[k:]
# settings folder
rep('''  ["tampil","set","Tampilan",()=>"Warna utama & ukuran kartu menu"],''','''  ["tampil","set","Tampilan",()=>"Warna utama & ukuran kartu menu"],
  ["intro","eye","Layar pembuka",()=>{const c=hiCfg();return c.on?`Aktif · ${String(c.sec).replace(".",",")} detik · font ${c.fs}%`:"Nonaktif"}],''')
rep('''  if(id==="tampil"){''','''  if(id==="intro"){const c=hiCfg();setTimeout(hiPreview,250);return `<div class="swrow" style="padding-top:0"><span><b>Tampilkan layar pembuka</b><small>Animasi “Selamat datang” setiap halaman publik dibuka</small></span><label class="tgl" aria-label="Tampilkan layar pembuka"><input type="checkbox" id="hio" ${c.on?"checked":""}><span></span></label></div>
    <label for="his">Durasi animasi</label><div class="rng"><input type="range" id="his" min="3" max="10" step="0.5" value="${c.sec}"><output id="hiso">${String(c.sec).replace(".",",")} dtk</output></div>
    <label for="hif">Ukuran font judul</label><div class="rng"><input type="range" id="hif" min="80" max="130" step="5" value="${c.fs}"><output id="hifo">${c.fs}%</output></div>
    <p class="note">Ukuran logo ikut menyesuaikan otomatis (golden ratio). Lebih pendek dari 5 detik terasa cepat, lebih dari 8 detik bisa membuat pengunjung menunggu.</p>
    <div class="hiframe"><div class="hibox" id="hibox"></div><button class="hiagain" data-a="hiplay"><span>${ic("eye")} Putar lagi</span></button></div>
    <button class="btn ghost" data-a="hiplay">Putar preview</button>
    <p class="note">Perubahan tampil ke pelanggan setelah Anda menekan <b>Terbitkan</b>.</p>`}
  if(id==="tampil"){''')
# actions
rep('''  else if(a==="kpi")kpiSheet(v);''','''  else if(a==="kpi")kpiSheet(v);
  else if(a==="hiplay")hiPreview();''')
# input / change handlers
rep('''document.addEventListener("input",e=>{''','''document.addEventListener("input",e=>{
  if(e.target.id==="his"){$("#hiso").textContent=String(e.target.value).replace(".",",")+" dtk"}
  if(e.target.id==="hif"){$("#hifo").textContent=e.target.value+"%"}''')
rep('''document.addEventListener("change",e=>{''','''document.addEventListener("change",e=>{
  if(["hio","his","hif"].includes(e.target.id)&&can("set")){const I=K.store.intro=Object.assign({},K.store.intro||{});
    if(e.target.id==="hio")I.on=e.target.checked?1:0;if(e.target.id==="his")I.sec=+e.target.value;if(e.target.id==="hif")I.fs=+e.target.value;
    kChanged();const sb=document.querySelector('[data-a="setsub"][data-v="intro"] small');if(sb)sb.textContent="";hiPreview();if(typeof pubBar==="function")pubBar();render();return}''')
open('p3.src.html','w').write(s);print("ok")
