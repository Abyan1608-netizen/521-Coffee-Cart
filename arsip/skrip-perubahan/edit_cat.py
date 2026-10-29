s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
rep('''  d.seq=d.seq||{};return d;''','''  d.seq=d.seq||{};
  if(!d.cfg.catv2){d.prod.forEach(p=>{if(/^(matcha|non[\\s-]*kopi|non[\\s-]*coffee?)$/i.test(String(p.cat).trim()))p.cat="Non Coffee"});d.cfg.catv2=1}
  if(!Array.isArray(d.cfg.cats))d.cfg.cats=[];
  d.prod.forEach(p=>{if(p.cat&&!d.cfg.cats.includes(p.cat))d.cfg.cats.push(p.cat)});
  if(!d.cfg.cats.includes("Non Coffee"))d.cfg.cats.push("Non Coffee");
  return d;''')
rep('''  const cats=["Semua",...new Set(D.prod.filter(p=>p.active).map(p=>p.cat))],tc=''','''  const used=new Set(D.prod.filter(p=>p.active).map(p=>p.cat)),cats=["Semua",...C().cats.filter(c=>used.has(c)),...[...used].filter(c=>!C().cats.includes(c))],tc=''')
rep('''  const e=ed,cats=[...new Set(D.prod.map(p=>p.cat))];''','''  const e=ed,cats=C().cats;''')
open('p3.src.html','w').write(s);print('ok')
