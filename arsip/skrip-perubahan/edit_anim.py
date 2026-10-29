s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
# insert anim css before reduced-motion? reduced-motion rule is at line 56 (earlier) -> it must come AFTER to win; append anim css then re-add reduced motion at end of css
i=s.index('</style>');s=s[:i]+open('anim.css').read()+'@media (prefers-reduced-motion:reduce){*,*::before,*::after{animation:none!important;transition:none!important}}\n'+s[i:]
rep('''  b.innerHTML=`<span class="n">${c}</span>''','''  if(b.dataset.c!==String(c)){if(b.dataset.c&&c){b.classList.remove("bump");void b.offsetWidth;b.classList.add("bump")}b.dataset.c=c}
  b.innerHTML=`<span class="n">${c}</span>''')
rep('''<div class="tw"><button class="tile${cart[p.id]?" has":""}"''','''<div class="tw"><button class="tile${cart[p.id]?" has":""}${p.id===justAdd?" just":""}"''')
rep('''  else if(a==="add"){cart[id]=(cart[id]||0)+1;$("#g").innerHTML=grid();cartUI()}''','''  else if(a==="add"){cart[id]=(cart[id]||0)+1;justAdd=id;$("#g").innerHTML=grid();justAdd="";cartUI()}''')
rep('let setSub="",','let justAdd="",pubIntro=true,setSub="",')
rep('''  $("#v").innerHTML=V[tab]();
  if(tab==="pos"&&wide()&&lines().length)upd();''','''  const vv=$("#v");vv.innerHTML=V[tab]();
  if(vv.dataset.t!==tab+"/"+setSub){vv.dataset.t=tab+"/"+setSub;vv.classList.remove("enter");void vv.offsetWidth;vv.classList.add("enter");clearTimeout(vv._t);vv._t=setTimeout(()=>vv.classList.remove("enter"),900)}
  if(tab==="pos"&&wide()&&lines().length)upd();''')
rep('''function showPub(){$("#m").hidden=true;$("#login").hidden=true;$("#app").hidden=true;$("#pub").hidden=false;pubRender();window.scrollTo(0,0)}''','''function showPub(){$("#m").hidden=true;$("#login").hidden=true;$("#app").hidden=true;const P=$("#pub");P.hidden=false;P.classList.add("intro");pubRender();clearTimeout(P._t);P._t=setTimeout(()=>P.classList.remove("intro"),1400);window.scrollTo(0,0)}''')
rep('''  show(`<div class="done"><div class="ck">${ic("check")}</div>''','''  const cf=[...Array(26)].map((_,i)=>{const a=Math.random()*Math.PI*2,d=70+Math.random()*120;return `<i style="--x:${Math.round(Math.cos(a)*d)}px;--y:${Math.round(Math.sin(a)*d-40)}px;--r:${Math.round(Math.random()*540-270)}deg;background:${["var(--lime)","var(--red)","#fff","var(--ac2)"][i%4]};animation-delay:${Math.round(Math.random()*120)}ms"></i>`}).join("");
  show(`<div class="confetti" aria-hidden="true">${cf}</div><div class="done"><div class="ck">${ic("check")}</div>''')
rep('''return `<rect x="${x}" y="${y}" width="${bw}" height="${h}" rx="8"''','''return `<rect style="animation-delay:${i*60}ms" x="${x}" y="${y}" width="${bw}" height="${h}" rx="8"''')
open('p3.src.html','w').write(s);print('ok')
