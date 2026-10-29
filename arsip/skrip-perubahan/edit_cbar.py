s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
rep('function pxSwap(pc,pr,sw){','function pxSwap(pc,pr,sw,cls=""){')
rep('return `<span class="pxs" aria-hidden="true" style="--pc','return `<span class="pxs${cls}" aria-hidden="true" style="--pc')
rep('''  if(b.dataset.c!==String(c)){if(b.dataset.c&&c)''','''  const chg=b.dataset.c!==String(c)&&c>0;
  if(b.dataset.c!==String(c)){if(b.dataset.c&&c)''')
rep('''  b.innerHTML=`<span class="n">${c}</span>''','''  b.innerHTML=`${typeof pxSwap==="function"?pxSwap(24,4,.6,chg?" pxc go":" pxc"):""}<span class="n">${c}</span>''')
css='''.cbar{overflow:hidden;isolation:isolate;--cy:8s;--o:1.5s}
.cbar > span:not(.pxs){position:relative;z-index:1}
.pxc.go i{animation:pxOnce .6s cubic-bezier(.4,0,.2,1) var(--s) both}
@keyframes pxOnce{0%{opacity:0;transform:scale(.35)}30%{opacity:1;transform:scale(1)}100%{opacity:0;transform:scale(.35)}}
'''
i=s.index("/* ---------- Habis (stok kosong) ---------- */");s=s[:i]+css+s[i:]
open('p3.src.html','w').write(s);print("ok")
