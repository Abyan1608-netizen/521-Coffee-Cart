s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
# replace login-specific gallery with generic
i=s.index('let loginT=0,lIdx=0,lSw=null;');j=s.index('function loginView(){')
s=s[:i]+'''/* ---------- Galeri geser (banner login & halaman pelanggan) ---------- */
let gSw=null;
function galMarkup(I,zoom,sec){const z=zoom==="out"?"kzout":zoom==="none"?"none":"kzin",sl=(u,k)=>`<div class="lslide${k===0?" on":""}" style="--src:url('${u}')"><img src="${u}" alt=""></div>`;
  return `<div class="ltrack" style="--zanim:${z};--zdur:${(+sec||5)+1}s">${I.map(sl).join("")}${I.length>1?sl(I[0],-1):""}</div>${I.length>1?`<div class="gdots">${I.map((u,i)=>`<button class="${i?"":"on"}" data-a="ggo" data-v="${i}" aria-label="Foto ${i+1}"></button>`).join("")}</div>`:""}`}
function galGo(el,n){const tr=el.querySelector(".ltrack");if(!tr)return;const S=tr.children,N=S.length-1;if(N<1)return;
  el._i=n;tr.style.transition="transform .9s cubic-bezier(.65,0,.25,1)";tr.style.transform=`translateX(${-n*100}%)`;
  [...S].forEach((x,k)=>x.classList.toggle("on",k===n));el.querySelectorAll(".gdots button").forEach((d,k)=>d.classList.toggle("on",k===(n%N)));
  if(n===N)setTimeout(()=>{if(el._i!==N)return;tr.style.transition="none";tr.style.transform="translateX(0)";el._i=0;S[N].classList.remove("on");void S[0].offsetWidth;S[0].classList.add("on")},950)}
function galInit(){document.querySelectorAll("[data-gal]").forEach(el=>{if(el._t!==undefined)return;el._i=0;const n=el.querySelectorAll(".lslide").length-1,sec=Math.max(2,Math.min(30,+el.dataset.gal||5));
  el._t=n>1?setInterval(()=>{if(!el.isConnected){clearInterval(el._t);return}if(el.offsetParent!==null&&!gSw&&!document.hidden)galGo(el,el._i+1)},sec*1000):0})}
document.addEventListener("pointerdown",e=>{const el=e.target.closest&&e.target.closest("[data-gal]");if(!el||e.target.closest(".gdots"))return;gSw={el,x:e.clientX}});
document.addEventListener("pointerup",e=>{if(!gSw)return;const {el,x}=gSw,dx=e.clientX-x;gSw=null;const N=el.querySelectorAll(".lslide").length-1;if(N<2||Math.abs(dx)<40)return;if(dx<0)galGo(el,el._i+1);else galGo(el,el._i>0?el._i-1:N-1)});
function loginBanner(){
  const h=$("#lhero");if(!h)return;const L=(K.store&&K.store.login)||{},I=L.imgs||[];clearInterval(h._t);h._t=undefined;
  if(!I.length){h.classList.remove("gal");delete h.dataset.gal;h.innerHTML='<div class="brandart"><svg aria-hidden="true"><use href="#logo"/></svg><span>Coffee Cart</span></div>';return}
  h.classList.add("gal");h.classList.toggle("single",I.length===1);h.dataset.gal=+L.sec||5;h.innerHTML=galMarkup(I,L.zoom||"in",L.sec);galInit();
}
'''+s[j:]
rep('''  if(a==="lgo"){lGo(+v);return}''','''  if(a==="ggo"){const el=b.closest("[data-gal]");if(el)galGo(el,+v);return}''')
# CSS: generic
rep('''.hero.gal{overflow:hidden;touch-action:pan-y}
.hero.gal::after{display:none}''','''.gal{overflow:hidden;touch-action:pan-y}''')
rep('''.lslide img{position:relative;max-width:100%;max-height:100%;width:auto;height:auto;object-fit:contain;display:block;box-shadow:0 20px 60px -20px rgba(0,0,0,.7)}
.lslide.on img{animation:var(--zanim,kzin) var(--zdur,6s) ease-out forwards}
.hero.single .lslide.on img{animation-iteration-count:infinite;animation-direction:alternate;animation-timing-function:ease-in-out}
.hero .k-dots{bottom:16px;right:50%;transform:translateX(50%);z-index:2}
.hero .k-dots button{width:8px;height:8px;border-radius:50%;border:0;padding:0;background:rgba(255,255,255,.45);transition:width .3s,background .3s;cursor:pointer}
.hero .k-dots button.on{width:22px;border-radius:5px;background:#fff}''','''.lslide img{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;display:block}
.lslide.on img{animation:var(--zanim,kzin) var(--zdur,6s) ease-out forwards}
.single .lslide.on img{animation-iteration-count:infinite;animation-direction:alternate;animation-timing-function:ease-in-out}
.gdots{position:absolute;left:50%;transform:translateX(-50%);bottom:14px;z-index:3;display:flex;gap:6px}
.k-hero .gdots{left:auto;right:14px;transform:none;bottom:20px}
.gdots button{width:8px;height:8px;border-radius:50%;border:0;padding:0;background:rgba(255,255,255,.45);transition:width .3s,background .3s;cursor:pointer}
.gdots button.on{width:22px;border-radius:5px;background:#fff}
.hero.gal::after{z-index:2;pointer-events:none}
.k-hero .st{z-index:3}
.k-hero::after{z-index:2;pointer-events:none}''')
# public hero uses gallery
rep('''${H.map((h,i)=>`<img src="${h}" alt="" class="${i?"":"on"}">`).join("")}${H.length>1?`<div class="k-dots">${H.map((h,i)=>`<i class="${i?"":"on"}"></i>`).join("")}</div>`:""}''','''${H.length?galMarkup(H,s.hzoom||"in",s.hsec||5):""}''')
rep('''function kHead(){const s=K.store,st=kStatus(),o=st.open,H=s.heroes||[];return `<div class="k-hero" role="img"''','''function kHead(){const s=K.store,st=kStatus(),o=st.open,H=s.heroes||[];return `<div class="k-hero${H.length?" gal":""}${H.length===1?" single":""}"${H.length?` data-gal="${+s.hsec||5}"`:""} role="img"''')
# remove old k-hero rotation interval
i=s.index('setInterval(()=>{document.querySelectorAll(".k-hero")');j=s.index('\n',i)
s=s[:i]+s[j+1:]
# call galInit after pubRender & render
rep('''function showPub(){''','''function galKick(){setTimeout(galInit,0)}
function showPub(){''')
rep('''  clock();headStat();bar();
}''','''  clock();headStat();bar();galInit();
}''')
open('p3.src.html','w').write(s);print('ok')
