s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
K1='["Krimer 1:1","40 ml","","","","","Krimer biasa + air 1:1, dicampur langsung"],["Krimer Set","","60 ml","150 ml","300 ml","1.500 ml","Krimer + air 1:2, sudah dicampur"]'
rep('["Krimer Set","40 ml","60 ml","150 ml","300 ml","1.500 ml","1:1 Air & Krimer"]',K1,2)
NOTES='["Cup 170 ml: Krimer 1:1 (krimer biasa + air 1:1, dicampur langsung)","200 ml – 5 liter: Krimer Set (krimer yang sudah dicampur air, krimer : air = 1 : 2)"]'
rep('formula:"Espresso + Aren + Krimer 1:2 + Susu",notes:["Rasio krimer : air = 1 : 2"]','formula:"Espresso + Aren + Krimer + Susu",notes:'+NOTES)
rep('formula:"Espresso + Aren + Butterscotch + Krimer 1:2 + Susu",notes:["Rasio krimer : air = 1 : 2"]','formula:"Espresso + Aren + Butterscotch + Krimer + Susu",notes:'+NOTES)
rep('rec:[["esp",30],["ga",15],["ks",40],["su",85]]','rec:[["esp",30],["ga",15],["kr",20],["air",20],["su",85]]')
rep('rec:[["esp",30],["ga",10],["bs",10],["ks",40],["su",80]]','rec:[["esp",30],["ga",10],["bs",10],["kr",20],["air",20],["su",80]]')
rep('["ks","Krimer Set","ml"]','["kr","Krimer","g"],["ks","Krimer Set","ml"]')
# v3 patch: devices that already got v2 — only touch Palm Sugar & Butterscotch krimer parts
rep('  if((d.cfg.recV||0)<2){applyMaster(d);d.cfg.recV=2}','''  if((d.cfg.recV||0)<2){applyMaster(d);d.cfg.recV=3}
  else if(d.cfg.recV<3){patchKrimer(d);d.cfg.recV=3}''')
rep("function applyMaster(d){",'''function patchKrimer(d){
  let kr=d.ing.find(g=>g.id==="kr")||d.ing.find(g=>/^krimer$/i.test(g.name));if(!kr){kr={id:"kr",name:"Krimer",unit:"g",type:"bahan",qty:0,min:0,cost:0};d.ing.push(kr)}
  let air=d.ing.find(g=>g.id==="air")||d.ing.find(g=>/^air$/i.test(g.name));if(!air){air={id:"air",name:"Air",unit:"ml",type:"bahan",qty:0,min:0,cost:0};d.ing.push(air)}
  const ks=d.ing.find(g=>g.id==="ks");
  MASTER.filter(m=>/palm|butter/i.test(m.name)).forEach(m=>{const p=d.prod.find(x=>x.name.toLowerCase()===m.name.toLowerCase());if(!p)return;
    if(ks)p.rec=p.rec.filter(r=>r.i!==ks.id);if(!p.rec.some(r=>r.i===kr.id)){const at=Math.max(0,p.rec.findIndex(r=>r.i==="su"));p.rec.splice(at,0,{i:kr.id,q:20},{i:air.id,q:20})}
    if(p.batch){const i=p.batch.rows.findIndex(r=>/^krimer set$/i.test(r.n)&&r.v[0]);if(i>=0){const o=p.batch.rows[i];p.batch.rows.splice(i,1,{n:"Krimer 1:1",v:[o.v[0],"","","",""],note:"Krimer biasa + air 1:1, dicampur langsung"},{n:"Krimer Set",v:["",o.v[1],o.v[2],o.v[3],o.v[4]],note:"Krimer + air 1:2, sudah dicampur"})}}
    p.formula=m.formula;p.notes=m.notes.slice()});
  if(ks&&/^krimer set$/i.test(ks.name))ks.name="Krimer Set (krimer + air 1:2)";
  d.log.push({at:new Date().toISOString(),a:"Revisi resep",d:"Pisahkan Krimer 1:1 (cup 170 ml) dan Krimer Set (200 ml – 5 liter)",by:"Sistem"});
}
function applyMaster(d){''')
rep('''  d.log.push({at:new Date().toISOString(),a:"Revisi resep",d:"Master Resep 521 Coffee Cart (4 menu)",by:"Sistem"});
}''','''  const ksI=d.ing.find(g=>g.id===idOf.ks);if(ksI&&/^krimer set$/i.test(ksI.name))ksI.name="Krimer Set (krimer + air 1:2)";
  d.log.push({at:new Date().toISOString(),a:"Revisi resep",d:"Master Resep 521 Coffee Cart (4 menu)",by:"Sistem"});
}''')
# display: empty cell -> dash; size view hides rows empty for that size
rep('''const bCell=(r,c)=>{const v=r.v[c]||"";''','''const bCell=(r,c)=>{const v=r.v[c]||"";if(!v)return '<span class="nil" aria-label="tidak dipakai">–</span>';''')
rep('''<div class="rbig">${B.rows.map(r=>`<div class="rrow">''','''<div class="rbig">${B.rows.filter(r=>r.v[rsz]).map(r=>`<div class="rrow">''')
rep(".rnotes{margin-top:12px;display:grid;gap:6px}",".rnotes{margin-top:12px;display:grid;gap:6px}\n.rtab .nil{color:var(--dim)}")
open('p3.src.html','w').write(s);print("ok")
