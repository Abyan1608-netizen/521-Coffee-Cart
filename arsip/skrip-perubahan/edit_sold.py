s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
MAP="map(p=>({n:p.name,p:p.price}))"
MAP2="map(p=>p.out?{n:p.name,p:p.price,o:1}:{n:p.name,p:p.price})"
assert s.count(MAP)==3; s=s.replace(MAP,MAP2)
# tile
rep('''<button class="tile${cart[p.id]?" has":""}${p.id===justAdd?" just":""}"''','''<button class="tile${cart[p.id]?" has":""}${p.out?" out":""}${p.id===justAdd?" just":""}"''')
rep('''aria-label="Tambah ${esc(p.name)}"><span class="cat">''','''aria-label="${p.out?esc(p.name)+" habis":"Tambah "+esc(p.name)}"><span class="cat">''')
rep('''<span class="gl" aria-hidden="true">${esc(glyph(p.name))}</span></button>${cart[p.id]?''','''<span class="gl" aria-hidden="true">${esc(glyph(p.name))}</span>${p.out?'<span class="stamp" aria-hidden="true">Habis</span>':""}</button>${cart[p.id]?''')
rep('''aria-label="Kurangi ${esc(p.name)}">−</button>`:""}</div>`).join("");''','''aria-label="Kurangi ${esc(p.name)}">−</button>`:`<button class="soldb${p.out?" on":""}" data-a="sold" data-id="${p.id}" aria-pressed="${!!p.out}">${p.out?"Ada lagi":"Habis"}</button>`}</div>`).join("");''')
# add guard + toggle handler
rep('''  else if(a==="add"){cart[id]''','''  else if(a==="add"&&prod(id)&&prod(id).out){toast(prod(id).name+" sedang habis. Ketuk “Ada lagi” kalau sudah tersedia.")}
  else if(a==="sold"){const p=prod(id);if(!p)return;p.out=!p.out;delete cart[id];lg(p.out?"Tandai habis":"Tersedia lagi",p.name);save();$("#g").innerHTML=grid();cartUI();
    if(AR&&kcan&&!kdirty&&!lines().length){toast(p.name+(p.out?" ditandai habis":" tersedia lagi")+". Memperbarui halaman pelanggan…",1);kPublish()}
    else toast(p.name+(p.out?" ditandai habis.":" tersedia lagi.")+(AR&&kcan?" Tekan Terbitkan di tab Kabar agar pelanggan melihatnya.":" Owner perlu menerbitkan di tab Kabar agar pelanggan melihatnya."),1)}
  else if(a==="add"){cart[id]''')
# public menu
rep('''`<div class="k-mi"><b>${esc(x.n)}</b><i></i><span>${rp(x.p)}</span></div>`''','''`<div class="k-mi${x.o?" out":""}"><b>${esc(x.n)}</b>${x.o?'<em class="k-sold">Habis</em>':""}<i></i><span>${rp(x.p)}</span></div>`''')
rep("M=(K.menu||[]).filter(m=>m.n)","M=(K.menu||[]).filter(m=>m.n&&!m.o)")
css='''
/* ---------- Habis (stok kosong) ---------- */
.soldb{position:absolute;bottom:10px;right:10px;z-index:2;height:30px;padding:0 11px;border-radius:999px;border:1px solid var(--line);background:color-mix(in srgb,var(--bg) 78%,transparent);color:var(--mute);font:700 12px var(--f-b);backdrop-filter:blur(6px)}
.soldb:hover{color:var(--ink);border-color:var(--sf3)}
.soldb.on{background:var(--ac);color:var(--on);border-color:transparent}
.tile.out{filter:grayscale(.85);opacity:.55;cursor:not-allowed}
.tile.out .pr{text-decoration:line-through}
.tile .stamp{position:absolute;top:50%;left:50%;z-index:2;transform:translate(-50%,-60%) rotate(-12deg);padding:4px 12px;border:2px solid var(--red);border-radius:8px;color:var(--red);font:900 18px var(--f-d);letter-spacing:.12em;text-transform:uppercase;background:color-mix(in srgb,var(--bg) 60%,transparent)}
.k-mi.out b,.k-mi.out span{opacity:.45}.k-mi.out span{text-decoration:line-through}
.k-sold{font:800 10px var(--f-b);font-style:normal;letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--red2);color:#fff;align-self:center}
'''
i=s.index("/* ---------- Pixel swap (CTA + FAB) ---------- */");s=s[:i]+css.lstrip("\n")+s[i:]
open('p3.src.html','w').write(s);print("ok")
