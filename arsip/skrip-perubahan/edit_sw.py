s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:60],s.count(a)); s=s.replace(a,b)
# icon
rep("""  ig:'<rect""","""  cart:'<circle cx="9.5" cy="19.5" r="1.3"/><circle cx="17" cy="19.5" r="1.3"/><path d="M2.5 3.5h2.4l2.4 11a1.6 1.6 0 0 0 1.6 1.3h8a1.6 1.6 0 0 0 1.6-1.2L20.3 8H6"/>',
  ig:'<rect""")
# JS: swap pixels helper + CTA + FAB
rep("const PX0=Date.now();","""const PX0=Date.now();
/* Pixel swap: piksel lime + merah bata menyapu kiri→kanan, sinkron dengan wipe antar muka tombol */
function pxSwap(pc,pr,sw){let px="";for(let r=0;r<pr;r++)for(let c=0;c<pc;c++){const x=c/(pc-1),q=Math.random(),k=q<.5?"r":q<.8?"l":"d";px+=`<i class="${k}" style="--s:${(x*sw+(Math.random()-.5)*.1).toFixed(3)}s"></i>`}return `<span class="pxs" aria-hidden="true" style="--pc:${pc};--pr:${pr}">${px}</span>`}""")
rep("""${cupSteam()}<span class="lbl">Pesan sekarang</span><span class="arr">${ic("arrow")}</span>${np?`<em class="k-ob">${np} promo aktif</em>`:""}<i class="shine"></i></button>""",
"""${np?`${pxSwap(26,5,1.1)}<span class="fc fa">${cupSteam()}<span class="lbl">Pesan sekarang</span><span class="arr">${ic("arrow")}</span></span><span class="fc fb"><b class="obn">${np}</b><span class="lbl">promo aktif · pesan sekarang</span><span class="arr">${ic("arrow")}</span></span>`:`${cupSteam()}<span class="lbl">Pesan sekarang</span><span class="arr">${ic("arrow")}</span>`}<i class="shine"></i></button>""")
rep("""<button class="k-order" data-a="order">""","""<button class="k-order${np?" sw":""}" data-a="order" aria-label="Pesan sekarang${np?` · ${np} promo aktif`:""}">""")
rep("""<button class="k-fab" data-a="order">${cupSteam()} Pesan<i class="shine"></i></button>""",
"""<button class="k-fab sw" data-a="order" aria-label="Pesan sekarang">${pxSwap(8,8,.5)}<span class="fc fa">${cupSteam()}</span><span class="fc fb">${ic("cart")}</span></button>""")
# CSS
css="""
/* ---------- Pixel swap (CTA + FAB) ---------- */
.sw{--cy:8s;--o:0s}
.k-order.sw{min-height:60px}
.sw > .fc{position:absolute!important;inset:0;z-index:1;display:flex;align-items:center;justify-content:center;gap:10px;color:var(--on)}
.sw > .fa{animation:faceA var(--cy) linear var(--o) infinite}
.sw > .fb{clip-path:inset(0 100% 0 0);animation:faceB var(--cy) linear var(--o) infinite}
.k-order.sw > .fb .lbl{font-size:16px}
.obn{display:inline-grid;place-items:center;min-width:26px;height:26px;padding:0 7px;border-radius:999px;background:var(--red2);color:#fff;font:800 14px var(--f-m);box-shadow:0 0 0 2px color-mix(in srgb,var(--red) 60%,transparent)}
@keyframes faceA{0%,40%{clip-path:inset(0 0 0 0)}53.75%{clip-path:inset(0 0 0 100%)}53.76%,86.25%{clip-path:inset(0 100% 0 0)}100%{clip-path:inset(0 0 0 0)}}
@keyframes faceB{0%,40%{clip-path:inset(0 100% 0 0)}53.75%,86.25%{clip-path:inset(0 0 0 0)}99.99%{clip-path:inset(0 0 0 100%)}100%{clip-path:inset(0 100% 0 0)}}
.pxs{position:absolute;inset:0;z-index:3;display:grid;grid-template-columns:repeat(var(--pc),1fr);grid-template-rows:repeat(var(--pr),1fr);pointer-events:none}
.pxs i{display:block;opacity:0;background:var(--red);animation:pxSw var(--cy) linear calc(var(--o) + var(--s)) infinite}
.pxs i.l{background:var(--lime);box-shadow:inset 0 0 0 1px rgba(0,0,0,.18)}
.pxs i.d{background:var(--red2)}
@keyframes pxSw{0%,38.9%,43.2%,85.1%,89.5%,100%{opacity:0;transform:scale(.35)}40%,41.2%,86.3%,87.5%{opacity:1;transform:scale(1)}}
.k-fab.sw{width:60px;height:60px;padding:0;justify-content:center;border-radius:50%;--o:2s}
.k-fab.sw .cupst,.k-fab.sw svg.i{width:26px;height:26px;stroke-width:2}
@media (prefers-reduced-motion:reduce){.sw > .fb{display:none}}
"""
i=s.index("/* ---------- Instagram ---------- */")
s=s[:i]+css.lstrip("\n")+s[i:]
open('p3.src.html','w').write(s);print("ok")
