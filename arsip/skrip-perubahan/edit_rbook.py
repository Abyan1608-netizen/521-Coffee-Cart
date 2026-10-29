import re
s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
a=s.index('  <div class="sec" id="resep"><h3>Buku resep</h3>')
b=s.index('<button class="btn ghost" data-a="newp">+ Menu & resep baru</button></div>\n',a)+len('<button class="btn ghost" data-a="newp">+ Menu & resep baru</button></div>\n')
old=s[a:b]
s=s[:a]+'''  <button class="folder" data-a="tab" data-v="resep">${ic("book")}<span><b>Buku resep</b><small>${D.prod.length} resep · ${new Set(D.prod.map(p=>p.cat)).size} kategori · takaran, cara membuat, modal</small></span>${ic("arrow")}</button>
'''+s[b:]
# card markup from old
m=re.search(r'\$\{D\.prod\.map\(p=>\{(.*?)\}\)\.join\(""\)\}</div>',old,re.S)
card=m.group(1)
rep('function set(){','''function rcardHTML(p){'''+card.replace('return `','return `',1)+'''}
function resep(){
  const groups=[...C().cats.filter(c=>D.prod.some(p=>p.cat===c)),...[...new Set(D.prod.map(p=>p.cat))].filter(c=>!C().cats.includes(c))];
  return `<button class="back" data-a="tab" data-v="set" style="margin-top:18px">← Atur</button>
  <div class="greet" style="margin-top:6px"><div><h2>Buku resep</h2><p>Takaran per cup, cara membuat, dan modal. Terhubung ke tab Menu, stok, dan halaman Kabar.</p></div><button class="btn sm" data-a="newp" style="margin:0">+ Menu & resep baru</button></div>
  <div class="chips scroll">${groups.map(g=>`<a class="qbtn" href="#rg-${encodeURIComponent(g)}" style="text-decoration:none">${esc(g)} <b class="num">${D.prod.filter(p=>p.cat===g).length}</b></a>`).join("")}</div>
  ${groups.map(g=>`<h3 id="rg-${encodeURIComponent(g)}" style="scroll-margin-top:90px">${esc(g)}</h3><div class="rbook">${D.prod.filter(p=>p.cat===g).map(rcardHTML).join("")}</div>`).join("")||'<div class="k-empty"><b>Belum ada resep</b>Tambahkan menu pertama beserta resepnya.</div>'}`;
}
function set(){''')
rep('.rbook{display:grid;','''.folder{display:flex;align-items:center;gap:14px;width:100%;text-align:left;margin:14px 0;padding:16px;border-radius:var(--r);border:1px solid color-mix(in srgb,var(--ac) 35%,var(--line));background:linear-gradient(135deg,color-mix(in srgb,var(--ac) 10%,var(--sf)),var(--sf) 60%)}
.folder > svg:first-child{width:28px;height:28px;color:var(--ac)}
.folder span{flex:1;min-width:0}.folder b{display:block;font:800 17px var(--f-d)}.folder small{color:var(--mute)}
.folder > svg:last-child{color:var(--mute)}
.rbook{display:grid;''')
rep("  mega:'","  book:'<path d=\"M5 4.5h11a2 2 0 0 1 2 2V20H7a2 2 0 0 1-2-2z\"/><path d=\"M5 18a2 2 0 0 1 2-2h11M9 8.5h5\"/>',\n  mega:'")
rep('const V={pos,dash,stk,menu,set,kabar};','const V={pos,dash,stk,menu,set,kabar,resep};')
rep('''  const T=TABS();if(!T.some(t=>t[0]===tab))tab="pos";''','''  const T=TABS();if(!T.some(t=>t[0]===tab)&&!(tab==="resep"&&own()))tab="pos";''')
rep('''aria-pressed="${t[0]===tab}">${ic(t[2])}${t[1]}</button>`).join("");''','''aria-pressed="${t[0]===tab||(tab==="resep"&&t[0]==="set")}">${ic(t[2])}${t[1]}</button>`).join("");''')
open('p3.src.html','w').write(s);print('ok')
