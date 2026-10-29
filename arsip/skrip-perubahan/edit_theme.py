s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
rep('''  if(a==="uitog"){const c=C(),m=uiMode()==="light"?"dark":"light";c.theme=m;c.uiSet=1;if(c.glass===undefined)c.glass=uiPref().glass;save();look();if(!$("#pub").hidden)pubRender();else if(me)render();return}''',
'''  if(a==="uitog"){const c=C(),m=uiMode()==="light"?"dark":"light";themeSwap(()=>{c.theme=m;c.uiSet=1;if(c.glass===undefined)c.glass=uiPref().glass;save();look();if(!$("#pub").hidden)pubRender();else if(me)render()},b);return}''')
rep('''  else if(a==="uitheme"){c.theme=v;c.uiSet=1;if(c.glass===undefined)c.glass=uiPref().glass;save();look();render()}''',
'''  else if(a==="uitheme"){if(c.theme===v&&uiMode()===v)return;themeSwap(()=>{c.theme=v;c.uiSet=1;if(c.glass===undefined)c.glass=uiPref().glass;save();look();render()},b)}''')
rep('''  else if(t.id==="uiglass"){const c=C();c.glass=t.checked?1:0;c.uiSet=1;if(!c.theme)c.theme=uiPref().theme;save();look();render()}''',
'''  else if(t.id==="uiglass"){const c=C(),on=t.checked;themeSwap(()=>{c.glass=on?1:0;c.uiSet=1;if(!c.theme)c.theme=uiPref().theme;save();look();render()},t.closest(".tgl")||t)}''')
# helper before PX0
rep("const PX0=Date.now();","""const PX0=Date.now();
/* Ganti tema dengan lingkaran yang membesar dari tombol (View Transitions), atau crossfade warna sebagai cadangan */
function themeSwap(fn,el){const r=document.documentElement,red=matchMedia("(prefers-reduced-motion: reduce)").matches;
  const spin=()=>document.querySelectorAll(".uitog svg").forEach(x=>x.classList.add("spin"));
  if(red){fn();return}
  const bb=el&&el.getBoundingClientRect?el.getBoundingClientRect():null,x=bb?bb.left+bb.width/2:innerWidth-40,y=bb?bb.top+bb.height/2:40;
  r.style.setProperty("--tx",x+"px");r.style.setProperty("--ty",y+"px");r.style.setProperty("--tr",Math.hypot(Math.max(x,innerWidth-x),Math.max(y,innerHeight-y))+"px");
  if(document.startViewTransition){try{document.startViewTransition(()=>{fn();spin()});return}catch(e){}}
  r.classList.add("theming");fn();spin();clearTimeout(themeSwap.t);themeSwap.t=setTimeout(()=>r.classList.remove("theming"),700)}""")
css='''/* ---------- Transisi tema ---------- */
::view-transition-old(root),::view-transition-new(root){animation:none;mix-blend-mode:normal}
::view-transition-new(root){animation:themeReveal .75s cubic-bezier(.65,0,.35,1) both}
@keyframes themeReveal{from{clip-path:circle(0 at var(--tx,90%) var(--ty,40px))}to{clip-path:circle(var(--tr,150vmax) at var(--tx,90%) var(--ty,40px))}}
html.theming,html.theming *,html.theming *::before,html.theming *::after{transition:background-color .6s ease,color .6s ease,border-color .6s ease,fill .6s ease,stroke .6s ease,box-shadow .6s ease!important}
.uitog svg.spin{animation:themeSpin .7s cubic-bezier(.2,1.3,.4,1)}
@keyframes themeSpin{from{transform:rotate(-120deg) scale(.4);opacity:0}to{transform:none;opacity:1}}
'''
i=s.index("/* ---------- Habis (stok kosong) ---------- */");s=s[:i]+css+s[i:]
open('p3.src.html','w').write(s);print("ok")
