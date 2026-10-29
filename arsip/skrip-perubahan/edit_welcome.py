s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
rep("const PX0=Date.now();","let PX0=Date.now();")
rep('if(me)enter();else if(location.hash==="#masuk")showLogin();else showPub();',
'if(me)enter();else if(location.hash==="#masuk")showLogin();else{showPub();welcome()}')
js=r'''
/* ---------- Welcome: logo tergambar → terisi → kilau → "Selamat datang" → zoom menembus ke halaman ---------- */
function welcome(){
  let seen=false;try{seen=sessionStorage.getItem("k521-hi")==="1"}catch(e){}
  if(seen||matchMedia("(prefers-reduced-motion: reduce)").matches)return;
  try{sessionStorage.setItem("k521-hi","1")}catch(e){}
  const paths=[...document.querySelectorAll("#logo path")].map((p,i)=>`<path pathLength="1" style="--i:${i}" d="${p.getAttribute("d")}"/>`).join("");
  const nm=esc(K.store.name||C().name||"521 Coffee"),tg=esc(K.store.tagline||C().sub||"");
  const word=(t,d0)=>[...t].map((ch,i)=>`<span style="--d:${(d0+i*.045).toFixed(3)}s">${ch===" "?"&nbsp;":esc(ch)}</span>`).join("");
  const w=document.createElement("div");w.className="hi";w.setAttribute("role","dialog");w.setAttribute("aria-label","Selamat datang di "+(K.store.name||"521 Coffee"));
  w.innerHTML=`<div class="hi-glow"></div><div class="hi-c"><div class="hi-logo"><svg viewBox="210 60 1565 1015" aria-hidden="true"><g class="hi-stroke">${paths}</g><g class="hi-fill">${paths}</g></svg><i class="hi-sheen"></i></div>
    <h1 class="hi-t">${word("Selamat datang",1.55)}</h1><p class="hi-s">di <b>${nm}</b></p>${tg?`<p class="hi-g">${tg}</p>`:""}</div>
    <button class="hi-skip" data-hi="skip">Lewati</button>`;
  document.body.appendChild(w);document.documentElement.classList.add("hi-on");
  let done=false;const P=$("#pub");
  const end=()=>{if(done)return;done=true;w.classList.add("out");P.classList.add("hi-in");
    setTimeout(()=>{PX0=Date.now();P.classList.remove("intro");void P.offsetWidth;pubRender();P.classList.add("intro");clearTimeout(P._t);P._t=setTimeout(()=>P.classList.remove("intro"),1400)},380);
    setTimeout(()=>{w.remove();document.documentElement.classList.remove("hi-on");P.classList.remove("hi-in")},1100)};
  w.addEventListener("click",end);addEventListener("keydown",function k(e){if(e.key==="Escape"||e.key==="Enter"||e.key===" "){removeEventListener("keydown",k);end()}});
  setTimeout(end,3900);
}
'''
i=s.index("look();\ntry{const sid=sessionStorage.getItem(\"pos521u\")")
s=s[:i]+js.lstrip("\n")+s[i:]
css='''/* ---------- Welcome ---------- */
html.hi-on,html.hi-on body{overflow:hidden}
.hi{position:fixed;inset:0;z-index:50;display:grid;place-items:center;background:#0a0302;color:#fff;cursor:pointer;overflow:hidden;-webkit-tap-highlight-color:transparent}
:root[data-ui="light"] .hi{background:#fbf6f1;color:#1f0b05}
.hi-glow{position:absolute;inset:-20%;background:radial-gradient(38% 30% at 50% 44%,color-mix(in srgb,var(--red) 55%,transparent),transparent 70%),radial-gradient(30% 24% at 50% 52%,color-mix(in srgb,var(--lime) 18%,transparent),transparent 70%);opacity:0;animation:hiGlow 3.2s cubic-bezier(.22,1,.36,1) .2s both}
@keyframes hiGlow{0%{opacity:0;transform:scale(.7)}45%{opacity:1}100%{opacity:.75;transform:scale(1.08)}}
.hi-c{position:relative;display:flex;flex-direction:column;align-items:center;text-align:center;padding:0 24px;will-change:transform}
.hi-logo{position:relative;width:min(46vw,230px);aspect-ratio:1565/1015;animation:hiLogo 1.6s cubic-bezier(.22,1,.36,1) .1s both}
@keyframes hiLogo{from{transform:scale(.86);filter:blur(8px)}to{transform:none;filter:none}}
.hi-logo svg{width:100%;height:100%;overflow:visible}
.hi-stroke path{fill:none;stroke:var(--lime);stroke-width:7;stroke-linejoin:round;stroke-dasharray:1;stroke-dashoffset:1;animation:hiDraw 1.15s cubic-bezier(.65,0,.35,1) calc(.25s + var(--i)*.12s) forwards,hiFade .5s ease 1.55s forwards}
:root[data-ui="light"] .hi-stroke path{stroke:var(--red)}
@keyframes hiDraw{to{stroke-dashoffset:0}}
@keyframes hiFade{to{opacity:0}}
.hi-fill path{fill:var(--lime);opacity:0;animation:hiFill .7s cubic-bezier(.22,1,.36,1) calc(1.05s + var(--i)*.06s) forwards}
:root[data-ui="light"] .hi-fill path{fill:var(--red)}
@keyframes hiFill{to{opacity:1}}
.hi-sheen{position:absolute;inset:-10% -30%;background:linear-gradient(105deg,transparent 40%,rgba(255,255,255,.85) 50%,transparent 60%);mix-blend-mode:overlay;transform:translateX(-120%);animation:hiSheen 1.1s cubic-bezier(.65,0,.35,1) 1.75s forwards;-webkit-mask:var(--m);pointer-events:none}
@keyframes hiSheen{to{transform:translateX(120%)}}
.hi-t{margin:34px 0 0;font:800 clamp(34px,9vw,64px)/1 var(--f-d);font-stretch:112%;letter-spacing:-.035em;white-space:nowrap}
.hi-t span{display:inline-block;opacity:0;transform:translateY(.45em);filter:blur(10px);animation:hiChar .9s cubic-bezier(.22,1,.36,1) var(--d) forwards}
@keyframes hiChar{to{opacity:1;transform:none;filter:none}}
.hi-t{background:linear-gradient(180deg,currentColor 55%,color-mix(in srgb,currentColor 55%,transparent));-webkit-background-clip:text;background-clip:text}
.hi-s{margin:14px 0 0;font:500 clamp(16px,4.2vw,20px) var(--f-b);color:color-mix(in srgb,currentColor 62%,transparent);opacity:0;animation:hiUp .9s cubic-bezier(.22,1,.36,1) 2.15s forwards}
.hi-s b{color:currentColor;font-weight:700;color:inherit}
:root:not([data-ui="light"]) .hi-s b{color:#fff}
.hi-g{margin:6px 0 0;font:500 14px var(--f-b);letter-spacing:.02em;color:var(--lime);opacity:0;animation:hiUp .9s cubic-bezier(.22,1,.36,1) 2.35s forwards}
:root[data-ui="light"] .hi-g{color:var(--red)}
@keyframes hiUp{from{opacity:0;transform:translateY(10px);filter:blur(6px)}to{opacity:1;transform:none;filter:none}}
.hi-skip{position:absolute;right:18px;bottom:calc(20px + env(safe-area-inset-bottom,0px));border:1px solid color-mix(in srgb,currentColor 22%,transparent);background:color-mix(in srgb,currentColor 6%,transparent);color:inherit;border-radius:999px;padding:8px 16px;font:600 13px var(--f-b);opacity:0;animation:hiUp .6s ease .8s forwards;backdrop-filter:blur(10px)}
.hi.out{pointer-events:none;animation:hiOut 1s cubic-bezier(.7,0,.2,1) forwards}
.hi.out .hi-c{animation:hiZoom 1s cubic-bezier(.7,0,.2,1) forwards}
.hi.out .hi-skip{opacity:0!important;transition:opacity .2s}
@keyframes hiZoom{0%{transform:none;opacity:1;filter:none}100%{transform:scale(2.6);opacity:0;filter:blur(14px)}}
@keyframes hiOut{0%,25%{opacity:1}100%{opacity:0}}
#pub.hi-in{animation:hiPage 1.1s cubic-bezier(.22,1,.36,1) both}
@keyframes hiPage{from{transform:scale(.94);filter:blur(12px);opacity:.3}to{transform:none;filter:none;opacity:1}}
'''
i=s.index("/* ---------- Transisi tema ---------- */");s=s[:i]+css+s[i:]
open('p3.src.html','w').write(s);print("ok")
