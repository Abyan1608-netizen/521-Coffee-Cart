s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
SNAP="D.prod.filter(p=>p.active).map(p=>p.out?{n:p.name,p:p.price,o:1}:{n:p.name,p:p.price})"
assert s.count(SNAP)==3; s=s.replace(SNAP,"menuSnap()")
rep('const save=()=>{try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){toast("Penyimpanan perangkat penuh. Unduh backup lalu hapus data lama.")}};',
    'const save=()=>{try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){toast("Penyimpanan perangkat penuh. Unduh backup lalu hapus data lama.")}if(typeof menuAuto==="function")menuAuto()};')
rep("const K_BASE=kHash(JSON.stringify(K));","let K_BASE=kHash(JSON.stringify(K));let PUBK=JSON.parse(JSON.stringify(K));")
rep('try{await AR.publish(kDoc());try{sessionStorage.removeItem("k521-pending")}catch(e){}kdirty=false;','try{await AR.publish(kDoc());try{sessionStorage.removeItem("k521-pending")}catch(e){}kdirty=false;PUBK=JSON.parse(JSON.stringify(K));K_BASE=kHash(JSON.stringify(K));')
rep("function kDoc(){","function kDoc(k){")
rep("  const data=JSON.stringify(K).replace(/</g,\"\\\\u003c\");","  const data=JSON.stringify(k||K).replace(/</g,\"\\\\u003c\");")
js=r'''
/* Menu kasir ↔ halaman pelanggan: setiap menu/harga/habis/urutan berubah di kasir, halaman pelanggan ikut diperbarui.
   Yang diterbitkan hanya bagian menu (dan nama toko), draf Kabar lain tetap jadi draf. */
function menuSnap(){return D.prod.filter(p=>p.active).map(p=>{const x={n:p.name,p:p.price,c:p.cat||""};if(p.size)x.s=p.size;if(p.formula)x.f=p.formula;if(p.color)x.col=p.color;if(p.out)x.o=1;return x})}
let msT=0,msBusy=false;
function menuAuto(delay){clearTimeout(msT);msT=setTimeout(kMenuPublish,delay==null?1200:delay)}
async function kMenuPublish(){
  if(msBusy||!AR||!kcan||!me||!kSync())return;
  if(lines().length||!$("#m").hidden||drag){menuAuto(15000);return}
  msBusy=true;const pub=JSON.parse(JSON.stringify(PUBK));pub.menu=menuSnap();pub.store=pub.store||{};pub.store.name=C().name;pub.store.tagline=C().sub;
  const nb=kHash(JSON.stringify(pub));
  try{
    if(kdirty){K.menu=pub.menu;K.store.name=pub.store.name;K.store.tagline=pub.store.tagline;try{sessionStorage.setItem("k521-pending",JSON.stringify({base:nb,k:K}))}catch(e){}}
    await AR.publish(kDoc(pub));PUBK=pub;K_BASE=nb;
    if(!kdirty){K.menu=pub.menu;K.store.name=pub.store.name;K.store.tagline=pub.store.tagline}
    toast("Menu di halaman pelanggan sudah ikut diperbarui",1);if(tab==="kabar"||!$("#pub").hidden)render();
  }catch(e){if(e&&e.code==="conflict")toast("Halaman baru saja diubah di tempat lain. Memuat versi terbaru…")}
  msBusy=false;
}
setInterval(()=>{if(me&&AR&&kcan&&kSync())menuAuto(0)},30000);
'''
i=s.index("function kChanged(){");s=s[:i]+js.lstrip("\n")+s[i:]
# sold handler: rely on auto sync
rep('''    if(AR&&kcan&&!kdirty&&!lines().length){toast(p.name+(p.out?" ditandai habis":" tersedia lagi")+". Memperbarui halaman pelanggan…",1);kPublish()}
    else toast(p.name+(p.out?" ditandai habis.":" tersedia lagi.")+(AR&&kcan?" Tekan Terbitkan di tab Kabar agar pelanggan melihatnya.":" Owner perlu menerbitkan di tab Kabar agar pelanggan melihatnya."),1)}''',
'''    toast(p.name+(p.out?" ditandai habis":" tersedia lagi")+(AR&&kcan?(lines().length?". Halaman pelanggan ikut diperbarui setelah pesanan selesai.":". Halaman pelanggan ikut diperbarui."):". Owner perlu membuka aplikasi agar halaman pelanggan ikut diperbarui."),1)}''')
# public menu rendering: grouped by category with size/formula
rep('''function kMenuList(m){const L=m?menuSnap():K.menu;return L.length?`<div class="k-menu">${L.map(x=>`<div class="k-mi${x.o?" out":""}"><b>${esc(x.n)}</b>${x.o?'<em class="k-sold">Habis</em>':""}<i></i><span>${rp(x.p)}</span></div>`).join("")}</div>`:kEmpty("Menu segera hadir","")}''',
'''function kMenuList(m){const L=m?menuSnap():(K.menu||[]);if(!L.length)return kEmpty("Menu segera hadir","");
  const G=[];L.forEach(x=>{const c=x.c||"Menu";let g=G.find(y=>y[0]===c);if(!g)G.push(g=[c,[]]);g[1].push(x)});
  return `<div class="k-menu">${G.map(([c,xs])=>`${G.length>1?`<p class="k-mcat">${esc(c)}</p>`:""}${xs.map(x=>`<div class="k-mi${x.o?" out":""}" style="--pc:${x.col||"var(--ac)"}"><span class="k-mdot" aria-hidden="true"></span><span class="k-mn"><b>${esc(x.n)}</b>${x.o?'<em class="k-sold">Habis</em>':""}${x.s||x.f?`<small>${[x.s?"Cup "+esc(x.s):"",x.f?esc(x.f):""].filter(Boolean).join(" · ")}</small>`:""}</span><i></i><span class="k-mp">${rp(x.p)}</span></div>`).join("")}`).join("")}</div>`}''')
rep('''<p class="note" style="margin-top:-6px">Diambil otomatis dari tab Menu (yang tidak disembunyikan) setiap kali Anda menerbitkan.</p>''','''<p class="note" style="margin-top:-6px">Tersambung dengan menu kasir: nama, harga, urutan, kategori, dan status Habis ikut diperbarui otomatis di halaman pelanggan.</p>''')
css='''/* Menu publik tersambung kasir */
.k-mcat{margin:14px 0 2px;font:700 11px var(--f-b);letter-spacing:.14em;text-transform:uppercase;color:var(--ac)}
:root[data-ui="light"] .k-mcat{color:var(--red)}
.k-mi{align-items:center}
.k-mdot{width:10px;height:28px;border-radius:5px;background:var(--pc);flex:none;box-shadow:0 0 14px -2px var(--pc)}
.k-mn{display:flex;flex-direction:column;min-width:0;flex:0 1 auto}
.k-mn b{display:inline}.k-mn .k-sold{align-self:flex-start;margin-top:3px}
.k-mn small{font-size:12px;color:var(--mute);margin-top:2px;line-height:1.3}
.k-mi .k-mp{font:600 15px var(--f-m);white-space:nowrap}
.k-mi.out .k-mdot{opacity:.35}
'''
k=s.index("/* ---------- Welcome ---------- */");s=s[:k]+css+s[k:]
open('p3.src.html','w').write(s);print("ok")
