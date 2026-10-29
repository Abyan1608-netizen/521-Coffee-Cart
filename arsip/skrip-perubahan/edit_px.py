s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
rep('.k-order{position:relative;overflow:hidden;background:linear-gradient(110deg,var(--ac) 0%,var(--ac2) 45%,var(--ac) 90%);background-size:220% 100%;animation:flow 5s linear infinite,ringOut 2.2s ease-out infinite,breatheBtn 2.6s ease-in-out infinite}',
'''.k-order{position:relative;overflow:hidden;isolation:isolate;background:linear-gradient(110deg,var(--ac) 0%,var(--ac2) 45%,var(--ac) 90%);background-size:220% 100%;animation:flow 9s linear infinite,ringOut 3.2s ease-out 1.8s infinite}
/* Pixel wipe: mosaik kecil yang membuka tombol, lalu gelombang piksel halus berkala */
.pxw{position:absolute;inset:0;display:grid;grid-template-columns:repeat(var(--pc),1fr);grid-template-rows:repeat(var(--pr),1fr);pointer-events:none;z-index:3}
.pxw i{display:block;opacity:0;animation:pxIn .55s cubic-bezier(.4,0,.2,1) var(--d) both,pxWave 7s cubic-bezier(.4,0,.2,1) calc(var(--d) + 1.6s) infinite}
.pxw i.h{--hl:1}
@keyframes pxIn{0%{opacity:1;background:var(--bg);transform:scale(1)}60%{opacity:1;background:color-mix(in srgb,var(--bg) 55%,var(--ac))}100%{opacity:0;background:var(--ac);transform:scale(.4)}}
@keyframes pxWave{0%,100%{opacity:0;transform:scale(.3)}3%{opacity:1;transform:scale(1);background:color-mix(in srgb,var(--on) 26%,transparent)}6%{opacity:.9;background:rgba(255,255,255,.55)}10%{opacity:0;transform:scale(.3)}}
.pxw i.h{animation-name:pxIn,pxWaveH}
@keyframes pxWaveH{0%,100%{opacity:0;transform:scale(.3)}3%{opacity:1;transform:scale(1);background:rgba(255,255,255,.85)}7%{opacity:.6;background:color-mix(in srgb,var(--red) 40%,transparent)}11%{opacity:0;transform:scale(.3)}}''')
rep('.k-order .shine{z-index:0}','.k-order .shine{display:none}')
# generate pixel grid in kCTA
rep('''  return `<button class="k-order" data-a="order">${cupSteam()}''','''  const pc=40,pr=6;let px="";for(let r=0;r<pr;r++)for(let c=0;c<pc;c++){const d=(c/pc)*1.1+(r/pr)*.18+Math.random()*.16;px+=`<i class="${Math.random()<.18?"h":""}" style="--d:${d.toFixed(3)}s"></i>`}
  return `<button class="k-order" data-a="order"><span class="pxw" aria-hidden="true" style="--pc:${pc};--pr:${pr}">${px}</span>${cupSteam()}''')
open('p3.src.html','w').write(s);print('ok')
