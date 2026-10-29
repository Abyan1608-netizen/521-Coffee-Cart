s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
i=s.index('let loginT=0;\nfunction loginBanner(){');j=s.index('function loginView(){')
s=s[:i]+'''let loginT=0,lIdx=0,lSw=null;
function loginBanner(){
  const h=$("#lhero");if(!h)return;const L=(K.store&&K.store.login)||{},I=L.imgs||[],sec=Math.max(2,Math.min(30,+L.sec||5)),z=L.zoom||"in";
  h.style.setProperty("--zanim",z==="out"?"kzout":z==="none"?"none":"kzin");h.style.setProperty("--zdur",(sec+1)+"s");
  clearInterval(loginT);lIdx=0;
  if(!I.length){h.classList.remove("gal");h.innerHTML='<div class="brandart"><svg aria-hidden="true"><use href="#logo"/></svg><span>Coffee Cart</span></div>';return}
  h.classList.add("gal");h.classList.toggle("single",I.length===1);
  const slide=(u,k)=>`<div class="lslide${k===0?" on":""}" style="--src:url('${u}')"><img src="${u}" alt=""></div>`;
  h.innerHTML=`<div class="ltrack">${I.map(slide).join("")}${I.length>1?slide(I[0],-1):""}</div>${I.length>1?`<div class="k-dots">${I.map((u,i)=>`<button class="${i?"":"on"}" data-a="lgo" data-v="${i}" aria-label="Foto ${i+1}"></button>`).join("")}</div>`:""}`;
  if(I.length>1)loginT=setInterval(()=>{if(h.offsetParent!==null&&!lSw)lGo(lIdx+1)},sec*1000);
}
function lGo(n){
  const h=$("#lhero"),tr=h&&h.querySelector(".ltrack");if(!tr)return;const S=tr.children,N=S.length-1;
  lIdx=n;tr.style.transition="transform .9s cubic-bezier(.65,0,.25,1)";tr.style.transform=`translateX(${-n*100}%)`;
  [...S].forEach((x,k)=>x.classList.toggle("on",k===n));h.querySelectorAll(".k-dots button").forEach((d,k)=>d.classList.toggle("on",k===(n%N)));
  if(n===N){setTimeout(()=>{tr.style.transition="none";tr.style.transform="translateX(0)";lIdx=0;S[N].classList.remove("on");S[0].classList.remove("on");void S[0].offsetWidth;S[0].classList.add("on")},950)}
}
document.addEventListener("pointerdown",e=>{const h=e.target.closest&&e.target.closest("#lhero.gal");if(!h||e.target.closest(".k-dots"))return;lSw={x:e.clientX}});
document.addEventListener("pointerup",e=>{if(!lSw)return;const dx=e.clientX-lSw.x;lSw=null;const h=$("#lhero"),N=h?h.querySelectorAll(".lslide").length-1:0;if(N<2||Math.abs(dx)<40)return;if(dx<0)lGo(lIdx+1);else lGo(lIdx>0?lIdx-1:N-1)});
'''+s[j:]
# CSS replace old hero img rules
rep('''.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1s ease}
.hero img.on{opacity:1;animation:var(--zanim,kzin) var(--zdur,6s) ease-out forwards}
.hero.single img.on{animation-iteration-count:infinite;animation-direction:alternate;animation-timing-function:ease-in-out}
.hero .k-dots{bottom:auto;top:16px;right:16px}''','''.hero.gal{overflow:hidden;touch-action:pan-y}
.hero.gal::after{display:none}
.ltrack{position:absolute;inset:0;display:flex;will-change:transform}
.lslide{position:relative;flex:0 0 100%;height:100%;overflow:hidden;display:grid;place-items:center}
.lslide::before{content:"";position:absolute;inset:-30px;background:var(--src) center/cover no-repeat;filter:blur(28px) brightness(.45) saturate(1.3)}
.lslide img{position:relative;max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block;box-shadow:0 20px 60px -20px rgba(0,0,0,.7)}
.lslide.on img{animation:var(--zanim,kzin) var(--zdur,6s) ease-out forwards}
.hero.single .lslide.on img{animation-iteration-count:infinite;animation-direction:alternate;animation-timing-function:ease-in-out}
.hero .k-dots{bottom:16px;right:50%;transform:translateX(50%);z-index:2}
.hero .k-dots button{width:8px;height:8px;border-radius:50%;border:0;padding:0;background:rgba(255,255,255,.45);transition:width .3s,background .3s;cursor:pointer}
.hero .k-dots button.on{width:22px;border-radius:5px;background:#fff}''')
rep('@keyframes kzin{from{transform:scale(1)}to{transform:scale(1.14)}}','@keyframes kzin{from{transform:scale(1)}to{transform:scale(1.08)}}')
rep('@keyframes kzout{from{transform:scale(1.14)}to{transform:scale(1)}}','@keyframes kzout{from{transform:scale(1.08)}to{transform:scale(1)}}')
rep('''  if(a==="tokabar"){showPub();return}''','''  if(a==="lgo"){lGo(+v);return}
  if(a==="tokabar"){showPub();return}''')
open('p3.src.html','w').write(s);print('ok')
