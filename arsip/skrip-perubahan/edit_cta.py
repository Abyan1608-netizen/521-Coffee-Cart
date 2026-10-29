s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
i=s.index('/* ---------- Animasi ---------- */');s=s[:i]+open('cta.css').read()+s[i:]
rep('''<button class="k-order" data-a="order">${ic("pos")} Pesan sekarang</button>`}''','''${kCTA()}`}''')
rep('''<button class="k-fab" data-a="order">${ic("pos")} Pesan</button>''','''<button class="k-fab" data-a="order">${cupSteam()} Pesan<i class="shine"></i></button>''')
rep('function pubRender(){','''const cupSteam=()=>`<svg class="cupst" viewBox="0 0 24 24" aria-hidden="true"><path class="st" d="M8 2.5c-.8 1 .8 1.6 0 2.6"/><path class="st" d="M11.5 2.5c-.8 1 .8 1.6 0 2.6"/><path class="st" d="M15 2.5c-.8 1 .8 1.6 0 2.6"/><path d="M4.5 8h12v5a6 6 0 0 1-12 0z"/><path d="M16.5 9.5h1.5a2.5 2.5 0 0 1 0 5h-1.5M3.5 21h15"/></svg>`;
function kCTA(){
  const np=K.posts.filter(p=>p.type==="promo"&&kVis(p)).length,M=(K.menu||[]).filter(m=>m.n);
  const items=M.map(m=>`<span><i>●</i> ${esc(m.n)}<b>${rp(m.p)}</b></span>`).join("");
  return `<button class="k-order" data-a="order">${cupSteam()}<span class="lbl">Pesan sekarang</span><span class="arr">${ic("arrow")}</span>${np?`<em class="k-ob">${np} promo aktif</em>`:""}<i class="shine"></i></button>${M.length?`<div class="k-tick" aria-hidden="true"><div class="k-tick-in">${items}${items}</div></div>`:""}`;
}
function pubRender(){''')
open('p3.src.html','w').write(s);print('ok')
