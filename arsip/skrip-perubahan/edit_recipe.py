s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
# ---------- master data + migration ----------
master=r'''
/* Master Resep 521 Coffee Cart (dari dokumen Owner). Kolom pertama = ukuran cup = takaran yang memotong stok. */
const MASTER=[
  {re:/palm/i,name:"Palm Sugar",size:"170 ml",formula:"Espresso + Aren + Krimer 1:2 + Susu",notes:["Rasio krimer : air = 1 : 2"],
   cols:["170 ml","200 ml","500 ml","1 Liter","5 Liter"],rows:[["Espresso","30 ml","30 ml","75 ml","150 ml","750 ml"],["Gula Aren","15 ml","13 ml","32,5 ml","65 ml","325 ml"],["Krimer Set","40 ml","60 ml","150 ml","300 ml","1.500 ml","1:1 Air & Krimer"],["Susu UHT","85 ml","97 ml","242,5 ml","485 ml","2.425 ml"]],
   rec:[["esp",30],["ga",15],["ks",40],["su",85]]},
  {re:/butter/i,name:"Butterscotch",size:"170 ml",formula:"Espresso + Aren + Butterscotch + Krimer 1:2 + Susu",notes:["Rasio krimer : air = 1 : 2"],
   cols:["170 ml","200 ml","500 ml","1 Liter","5 Liter"],rows:[["Espresso","30 ml","30 ml","75 ml","150 ml","750 ml"],["Gula Aren","10 ml","10 ml","25 ml","50 ml","250 ml"],["Butterscotch","10 ml","10 ml","25 ml","50 ml","250 ml"],["Krimer Set","40 ml","60 ml","150 ml","300 ml","1.500 ml","1:1 Air & Krimer"],["Susu UHT","80 ml","90 ml","225 ml","450 ml","2.250 ml"]],
   rec:[["esp",30],["ga",10],["bs",10],["ks",40],["su",80]]},
  {re:/matcha/i,name:"Matcha Latte",size:"170 ml",formula:"Matcha + Air + Susu",notes:["M = Matcha, A = Air"],
   cols:["170 ml","200 ml","500 ml","1 Liter","5 Liter"],rows:[["Matcha Set","55 ml","55 ml","137,5 ml","275 ml","1.342 ml","M 15 · A 40 | M 15 · A 40 | M 37,5 · A 100 | M 75 · A 200 | M 325 · A 1.000"],["Susu","115 ml","145 ml","362,5 ml","725 ml","3.625 ml"]],
   rec:[["mt",15],["air",40],["su",115]]},
  {re:/black\s*caf|americano/i,name:"Black Caffe",size:"180 ml",formula:"Espresso + Air",notes:["Espresso memakai biji Temanggung"],
   cols:["180 ml","200 ml","500 ml","1 Liter","5 Liter"],rows:[["Espresso Temanggung","25 ml","30 ml","75 ml","150 ml","750 ml"],["Air","155 ml","170 ml","425 ml","850 ml","4.250 ml"]],
   rec:[["espt",25],["air",155]]}];
const MASTER_TIP="Barista cukup melihat kolom ukuran yang sedang dibuat, tanpa perlu menghitung ulang.";
function applyMaster(d){
  const need=[["esp","Espresso","ml"],["espt","Espresso Temanggung","ml"],["ga","Gula aren","ml"],["ks","Krimer Set","ml"],["su","Susu UHT","ml"],["bs","Sirup Butterscotch","ml"],["mt","Matcha","g"],["air","Air","ml"]];
  const idOf={};need.forEach(([id,nm,u])=>{let g=d.ing.find(x=>x.id===id)||d.ing.find(x=>x.name.toLowerCase()===nm.toLowerCase());if(!g){g={id,name:nm,unit:u,type:"bahan",qty:0,min:0,cost:0};d.ing.push(g)}idOf[id]=g.id});
  const packs=new Set(d.ing.filter(g=>g.type==="packaging").map(g=>g.id));
  MASTER.forEach(m=>{
    let p=d.prod.find(x=>x.name.toLowerCase()===m.name.toLowerCase())||d.prod.find(x=>m.re.test(x.name));
    if(!p){p={id:"p"+Math.random().toString(36).slice(2,8),name:m.name,cat:m.name==="Black Caffe"?"Coffee":m.name==="Matcha Latte"?"Non Coffee":"Kopi Susu",price:m.name==="Black Caffe"?15000:20000,rprice:0,active:1,color:"#8b5e3c",rec:["cup","lid"].filter(i=>d.ing.some(g=>g.id===i)).map(i=>({i,q:1}))};d.prod.push(p)}
    p.name=m.name;
    p.rec=m.rec.map(([i,q])=>({i:idOf[i],q})).concat((p.rec||[]).filter(r=>packs.has(r.i)));
    p.size=m.size;p.formula=m.formula;p.notes=m.notes.slice();
    p.batch={cols:m.cols.slice(),rows:m.rows.map(r=>({n:r[0],v:r.slice(1,6),note:r[6]||""}))};
  });
  d.log.push({at:new Date().toISOString(),a:"Revisi resep",d:"Master Resep 521 Coffee Cart (4 menu)",by:"Sistem"});
}
'''
rep("function fix(d){",master.lstrip("\n")+"function fix(d){")
rep("  if(!d.cfg.cats.includes(\"Non Coffee\"))d.cfg.cats.push(\"Non Coffee\");\n  return d;","  if(!d.cfg.cats.includes(\"Non Coffee\"))d.cfg.cats.push(\"Non Coffee\");\n  if((d.cfg.recV||0)<2){applyMaster(d);d.cfg.recV=2}\n  return d;")
rep("fix(D);\nconst C=()=>D.cfg;","fix(D);try{localStorage.setItem(\"pos521\",JSON.stringify(D))}catch(e){}\nconst C=()=>D.cfg;")
# ---------- helpers: formula pills, batch table, recipe sheet ----------
helpers=r'''
const fPills=p=>p.formula?`<div class="fpills">${p.formula.split(/\s*\+\s*/).map((x,i)=>`${i?'<i>+</i>':""}<span>${esc(x)}</span>`).join("")}</div>`:"";
const bCell=(r,c)=>{const v=r.v[c]||"";const parts=(r.note||"").split("|").map(x=>x.trim());const sub=parts.length>1?parts[c]:"";return `${esc(v)}${sub?`<small>${esc(sub)}</small>`:""}`};
let rsz=0;
function rSheet(id){const p=prod(id);if(!p)return;const B=p.batch,h=hpp(p),mg=p.price?Math.round((p.price-h)/p.price*100):0;if(B&&rsz>=B.cols.length)rsz=0;
  show(`<div class="rhead" style="--pc:${p.color||"var(--sf3)"}"><span class="rgl" aria-hidden="true">${esc(glyph(p.name))}</span><div><p class="eyebrow" style="margin:0">${esc(p.cat)}${p.size?" · cup "+esc(p.size):""}</p><h2 style="margin:4px 0 0">${esc(p.name)}</h2></div></div>
  ${fPills(p)}
  ${B?`<div class="lbl">Sedang membuat ukuran</div><div class="szs" role="tablist">${B.cols.map((c,i)=>`<button role="tab" data-a="rsz" data-id="${p.id}" data-v="${i}" aria-selected="${i===rsz}">${esc(c)}${i===0?"<small>cup</small>":""}</button>`).join("")}</div>
  <div class="rbig">${B.rows.map(r=>`<div class="rrow"><span>${esc(r.n)}${r.note&&r.note.split("|").length<2?`<small>${esc(r.note)}</small>`:""}</span><b>${bCell(r,rsz)}</b></div>`).join("")}</div>
  <details class="rall"><summary>Lihat tabel semua ukuran</summary><div class="rtw"><table class="rtab"><thead><tr><th>Bahan</th>${B.cols.map((c,i)=>`<th>${esc(c)}${i===0?"<small>cup</small>":""}</th>`).join("")}</tr></thead><tbody>${B.rows.map(r=>`<tr><th>${esc(r.n)}</th>${B.cols.map((_,i)=>`<td>${bCell(r,i)}</td>`).join("")}</tr>`).join("")}</tbody></table></div></details>`
  :`<h3>Takaran per cup</h3><div class="rbig">${p.rec.map(r=>{const g=ing(r.i);return `<div class="rrow"><span>${g?esc(g.name):"(bahan dihapus)"}</span><b>${fq(r.q)} ${g?g.unit:""}</b></div>`}).join("")}</div>`}
  ${(p.notes||[]).length?`<div class="rnotes">${p.notes.map(x=>`<p>${ic("alert")}${esc(x)}</p>`).join("")}</div>`:""}
  ${p.steps?`<h3>Cara membuat</h3><p class="steps">${esc(p.steps)}</p>`:""}
  <p class="note">${MASTER_TIP}</p>
  ${can("menu")?`<div class="sumr"><span>Modal per cup</span><span>${rp(h)} · untung ${mg}%</span></div><button class="btn ghost" data-a="edit" data-id="${p.id}">Ubah menu & resep</button>`:""}`)}
'''
rep("function edSheet(){",helpers.lstrip("\n")+"function edSheet(){")
# ---------- menu tab redesign ----------
i=s.index("function menu(){");j=s.index("\n}\n",i)+3
menu=r'''let mcat="Semua";
function menu(){
  const cats=["Semua",...C().cats.filter(c=>D.prod.some(p=>p.cat===c))],L=D.prod.filter(p=>mcat==="Semua"||p.cat===mcat);
  const act=D.prod.filter(p=>p.active),avg=act.length?Math.round(act.reduce((a,p)=>a+(p.price?(p.price-hpp(p))/p.price*100:0),0)/act.length):0;
  const best=act.slice().sort((a,b)=>(b.price-hpp(b))-(a.price-hpp(a)))[0];
  return `<div class="mhero"><div><p class="eyebrow">Menu & resep</p><h2>${D.prod.length} menu, satu standar rasa</h2><p>Ketuk kartu untuk melihat takaran per ukuran. Tahan ${ic("grip")} lalu geser untuk mengatur urutan di kasir.</p></div>
  <div class="mstats"><div><b>${act.length}</b><span>tampil di kasir</span></div><div><b>${avg}%</b><span>rata-rata untung</span></div>${best?`<div><b>${esc(best.name)}</b><span>untung terbesar / cup</span></div>`:""}</div>
  <div class="mact"><button class="qbtn" data-a="tab" data-v="resep">${ic("book")}Buku resep</button><button class="btn sm" data-a="newp" style="margin:0">+ Menu baru</button></div></div>
  ${cats.length>2?`<div class="chips scroll">${cats.map(c=>`<button data-a="mcat" data-v="${esc(c)}" aria-pressed="${c===mcat}">${esc(c)}</button>`).join("")}</div>`:""}
  <div class="mcards${mcat==="Semua"?" sortable":""}"${mcat==="Semua"?' data-sort="prod"':""}>${L.map((p,k)=>{const h=hpp(p),mg=p.price?Math.max(0,Math.min(100,Math.round((p.price-h)/p.price*100))):0;
    return `<div class="mcard${p.active?"":" off"}" data-si="${p.id}" style="--pc:${p.color||"#6b4a2f"};--d:${k*60}ms">
      <button class="mc-main" data-a="rview" data-id="${p.id}" aria-label="Lihat resep ${esc(p.name)}">
        <span class="mc-art" aria-hidden="true"><span>${esc(glyph(p.name))}</span></span>
        <span class="mc-body"><span class="mc-tags"><em>${esc(p.cat)}</em>${p.size?`<em>cup ${esc(p.size)}</em>`:""}${p.active?"":"<em class=\"x\">Disembunyikan</em>"}${p.out?"<em class=\"x\">Habis</em>":""}</span>
          <b class="mc-name">${esc(p.name)}</b>${fPills(p)}
          <span class="mc-foot"><span class="mc-price">${rp(p.price)}</span><span class="mc-mg"><span class="mc-bar"><i style="width:${mg}%"></i></span><small>modal ${rp(h)} · untung <b>${mg}%</b></small></span></span></span>
      </button>
      <span class="mc-side"><button class="mc-edit" data-a="edit" data-id="${p.id}" aria-label="Ubah ${esc(p.name)}">${ic("set")}</button>${mcat==="Semua"?grip(p.name):""}</span></div>`}).join("")||'<div class="empty"><b>Belum ada menu</b>Tambahkan menu pertama untuk mulai berjualan.</div>'}</div>`;
}
'''
s=s[:i]+menu.lstrip("\n")+s[j:]
# recipe book card upgrade
rep('''  ${p.steps?`<p class="steps">${esc(p.steps)}</p>`:""}
  <footer>''','''  ${fPills(p)}${p.steps?`<p class="steps">${esc(p.steps)}</p>`:""}
  ${p.batch?`<button class="btn ghost sm" data-a="rview" data-id="${p.id}" style="margin:0">${ic("book")}Takaran 170 ml – 5 liter</button>`.replace("170 ml",esc(p.batch.cols[0])).replace("5 liter",esc(p.batch.cols[p.batch.cols.length-1])):""}
  <footer>''')
rep('''<header><b>${esc(p.name)}</b>${p.active?"":'<span class="pill">Disembunyikan</span>'}<span class="num">${rp(p.price)}</span></header>''','''<header><b>${esc(p.name)}</b>${p.size?`<span class="pill">cup ${esc(p.size)}</span>`:""}${p.active?"":'<span class="pill">Disembunyikan</span>'}<span class="num">${rp(p.price)}</span></header>''')
# ---------- edit sheet additions ----------
rep('''  <h3>Resep per cup</h3>${e.rec.map(''','''  <div class="two"><label>Ukuran cup<input data-f="size" value="${esc(e.size||"")}" placeholder="170 ml"></label><label>Rumus singkat<input data-f="formula" value="${esc(e.formula||"")}" placeholder="Espresso + Aren + Susu"></label></div>
  <h3>Resep per cup <small class="mute" style="text-transform:none;letter-spacing:0;font-weight:500;display:inline">· memotong stok setiap terjual</small></h3>${e.rec.map(''')
rep('''  <label>Cara membuat (opsional)<textarea class="kt" id="f-steps"''','''  <h3>Tabel takaran per ukuran</h3><p class="note" style="margin-top:-6px">Untuk barista: cukup lihat kolom ukuran yang sedang dibuat. Ketik bebas, misalnya “32,5 ml”.</p>
  ${e.batch?`<div class="btw"><table class="bted"><thead><tr><th>Bahan</th>${e.batch.cols.map((c,ci)=>`<th><input data-bh="${ci}" value="${esc(c)}" aria-label="Ukuran ${ci+1}"></th>`).join("")}<th></th></tr></thead><tbody>${e.batch.rows.map((r,ri)=>`<tr><th><input data-bt="${ri}" data-bc="n" value="${esc(r.n)}" aria-label="Nama bahan"></th>${e.batch.cols.map((_,ci)=>`<td><input data-bt="${ri}" data-bc="${ci}" value="${esc(r.v[ci]||"")}" aria-label="${esc(r.n)} ${esc(e.batch.cols[ci])}"></td>`).join("")}<td><button data-a="btrm" data-id="${ri}" aria-label="Hapus baris">✕</button></td></tr>`).join("")}</tbody></table></div>
  <button class="link" data-a="btadd">+ Tambah baris bahan</button>`:`<button class="btn ghost sm" data-a="btnew">+ Buat tabel 5 ukuran</button>`}
  <label>Catatan resep (satu per baris)<textarea class="kt" data-f="notesTxt" placeholder="Contoh: Rasio krimer : air = 1 : 2">${esc((e.notes||[]).join("\\n"))}</textarea></label>
  <label>Cara membuat (opsional)<textarea class="kt" id="f-steps"''')
# input handler for batch + notes
rep('''    else ed[f]=(f==="price"||f==="rprice")?rpv(t.value):t.value;''','''    else if(f==="notesTxt")ed.notes=t.value.split("\\n").map(x=>x.trim()).filter(Boolean);
    else ed[f]=(f==="price"||f==="rprice")?rpv(t.value):t.value;''')
rep('''  else if(t.dataset.f&&ed){''','''  else if(t.dataset.bt!==undefined&&ed&&ed.batch){const r=ed.batch.rows[+t.dataset.bt];if(r){if(t.dataset.bc==="n")r.n=t.value;else r.v[+t.dataset.bc]=t.value}}
  else if(t.dataset.bh!==undefined&&ed&&ed.batch){ed.batch.cols[+t.dataset.bh]=t.value}
  else if(t.dataset.f&&ed){''')
# actions (pre-gate view ones + menu ones)
rep('''  else if(a==="kpi")kpiSheet(v);''','''  else if(a==="kpi")kpiSheet(v);
  else if(a==="rview"&&(can("resep")||can("menu"))){rsz=0;rSheet(id)}
  else if(a==="rsz"&&(can("resep")||can("menu"))){rsz=+v;const st=$(".sheet").scrollTop;rSheet(id);$(".sheet").scrollTop=st}
  else if(a==="mcat"){mcat=v;render()}''')
rep('''  else if(a==="addr"){''','''  else if(a==="btadd"){ed.batch.rows.push({n:"",v:ed.batch.cols.map(()=>""),note:""});const st=$(".sheet").scrollTop;edSheet();$(".sheet").scrollTop=st}
  else if(a==="btrm"){ed.batch.rows.splice(+id,1);const st=$(".sheet").scrollTop;edSheet();$(".sheet").scrollTop=st}
  else if(a==="btnew"){ed.batch={cols:[ed.size||"Cup","200 ml","500 ml","1 Liter","5 Liter"],rows:ed.rec.filter(r=>{const g=ing(r.i);return g&&g.type!=="packaging"}).map(r=>{const g=ing(r.i);return{n:g.name,v:[fq(r.q)+" "+g.unit,"","","",""],note:""}})};const st=$(".sheet").scrollTop;edSheet();$(".sheet").scrollTop=st}
  else if(a==="addr"){''')
rep('''"edit":"menu","newp":"menu"''','''"edit":"menu","newp":"menu","btadd":"menu","btrm":"menu","btnew":"menu"''')
# saveP: log batch change
rep('''      if(JSON.stringify(o.rec)!==JSON.stringify(ed.rec))lg("Ubah resep",ed.name);''','''      if(JSON.stringify(o.rec)!==JSON.stringify(ed.rec)||JSON.stringify(o.batch||null)!==JSON.stringify(ed.batch||null))lg("Ubah resep",ed.name);''')
css=r'''/* ---------- Menu & resep (kartu) ---------- */
.mhero{position:relative;margin:18px 0 14px;padding:20px;border-radius:26px;overflow:hidden;background:radial-gradient(90% 120% at 100% 0,color-mix(in srgb,var(--red) 40%,transparent),transparent 60%),radial-gradient(70% 90% at 0 100%,color-mix(in srgb,var(--ac) 16%,transparent),transparent 65%),var(--sf);border:1px solid var(--line)}
.mhero h2{margin:6px 0 6px;font-size:clamp(24px,5.4vw,34px)}
.mhero p{margin:0;color:var(--mute);font-size:14px}
.mhero p svg.i{width:15px;height:15px;vertical-align:-3px;fill:currentColor}
.mstats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:16px 0 14px}
.mstats div{background:color-mix(in srgb,var(--bg) 55%,transparent);border:1px solid var(--line);border-radius:14px;padding:10px 12px;min-width:0}
.mstats b{display:block;font:700 18px var(--f-m);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mstats span{display:block;font-size:11px;color:var(--mute);line-height:1.25;margin-top:2px}
.mact{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.mcards{display:grid;gap:12px}
.mcard{position:relative;display:flex;align-items:stretch;gap:8px;animation:fadeUp .5s cubic-bezier(.22,1,.36,1) var(--d) both}
.mcard.off .mc-main{opacity:.6}
.mc-main{flex:1;min-width:0;display:grid;grid-template-columns:96px minmax(0,1fr);gap:14px;padding:12px;text-align:left;border-radius:22px;border:1px solid var(--line);background:radial-gradient(120% 100% at 0 0,color-mix(in srgb,var(--pc) 22%,transparent),transparent 55%),var(--sf);transition:border-color .2s,transform .15s,box-shadow .2s}
.mc-main:hover{border-color:color-mix(in srgb,var(--pc) 70%,var(--line));box-shadow:0 18px 40px -26px var(--pc)}
.mc-main:active{transform:scale(.985)}
.mc-art{position:relative;border-radius:16px;overflow:hidden;background:linear-gradient(160deg,color-mix(in srgb,var(--pc) 85%,#fff 15%),color-mix(in srgb,var(--pc) 60%,#000 40%));display:grid;place-items:center;min-height:118px}
.mc-art::before{content:"";position:absolute;inset:0;background:radial-gradient(60% 50% at 30% 20%,rgba(255,255,255,.35),transparent 70%)}
.mc-art::after{content:"";position:absolute;left:-30%;top:0;width:40%;height:100%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.25),transparent);transform:skewX(-18deg);animation:mcSheen 5s ease-in-out infinite;animation-delay:var(--d)}
@keyframes mcSheen{0%,70%{left:-40%}100%{left:130%}}
.mc-art span{position:relative;font:900 44px/1 var(--f-d);font-stretch:125%;letter-spacing:-.06em;color:rgba(255,255,255,.92);text-shadow:0 6px 20px rgba(0,0,0,.25)}
.mc-body{display:flex;flex-direction:column;gap:6px;min-width:0}
.mc-tags{display:flex;flex-wrap:wrap;gap:5px}
.mc-tags em{font-style:normal;font-size:10.5px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;padding:3px 8px;border-radius:999px;background:var(--sf2);color:var(--mute);border:1px solid var(--line)}
.mc-tags em.x{color:var(--warn)}
.mc-name{font:800 21px/1.1 var(--f-d);font-stretch:110%;letter-spacing:-.015em}
.fpills{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:2px 0}
.fpills span{font-size:12px;font-weight:700;padding:3px 9px;border-radius:999px;background:color-mix(in srgb,var(--pc,var(--ac)) 18%,var(--sf2));border:1px solid color-mix(in srgb,var(--pc,var(--ac)) 35%,var(--line));color:var(--ink)}
.fpills i{font-style:normal;color:var(--dim);font-weight:800;font-size:12px}
.mc-foot{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;margin-top:auto;flex-wrap:wrap}
.mc-price{font:700 20px var(--f-m);letter-spacing:-.03em}
.mc-mg{display:grid;gap:4px;min-width:130px;flex:1;max-width:220px}
.mc-bar{height:6px;border-radius:999px;background:var(--sf3);overflow:hidden}
.mc-bar i{display:block;height:100%;border-radius:999px;background:linear-gradient(90deg,var(--ac2),var(--ac));animation:mcGrow 1s cubic-bezier(.22,1,.36,1) calc(var(--d) + .2s) both}
@keyframes mcGrow{from{width:0}}
.mc-mg small{font-size:11.5px;color:var(--mute)}.mc-mg small b{color:var(--ink);font-family:var(--f-m)}
.mc-side{display:flex;flex-direction:column;gap:8px}
.mc-edit{flex:1;width:42px;border:1px solid var(--line);background:var(--sf);border-radius:14px;color:var(--mute);display:grid;place-items:center;padding:0}
.mc-edit:hover{color:var(--ink);border-color:var(--sf3)}
.mc-side .grip{flex:1}
@media (min-width:640px){.mc-main{grid-template-columns:132px minmax(0,1fr);padding:14px}.mc-art{min-height:140px}.mc-art span{font-size:56px}}
/* lembar resep */
.rhead{display:flex;align-items:center;gap:14px;margin:0 40px 12px 0}
.rgl{width:64px;height:64px;flex:none;border-radius:18px;display:grid;place-items:center;font:900 26px var(--f-d);color:#fff;background:linear-gradient(160deg,color-mix(in srgb,var(--pc) 85%,#fff 15%),color-mix(in srgb,var(--pc) 60%,#000 40%))}
.szs{display:flex;gap:6px;overflow-x:auto;scrollbar-width:none;margin:6px -18px 12px;padding:0 18px}
.szs::-webkit-scrollbar{display:none}
.szs button{flex:none;display:flex;flex-direction:column;align-items:center;gap:1px;min-width:74px;padding:10px 12px;border-radius:14px;border:1px solid var(--line);background:var(--sf2);font:700 15px var(--f-m);color:var(--mute)}
.szs button small{font:700 9.5px var(--f-b);letter-spacing:.08em;text-transform:uppercase;opacity:.8}
.szs button[aria-selected="true"]{background:var(--ac);color:var(--on);border-color:var(--ac);box-shadow:0 10px 24px -12px var(--ac)}
.rbig{background:var(--sf2);border:1px solid var(--line);border-radius:18px;padding:4px 16px;animation:fadeUp .3s both}
.rrow{display:flex;align-items:center;justify-content:space-between;gap:12px;padding:13px 0;border-bottom:1px dashed var(--line)}
.rrow:last-child{border-bottom:0}
.rrow span{font-weight:700;font-size:16px}.rrow span small{display:block;font-weight:500;color:var(--mute);font-size:12px}
.rrow b{font:700 24px var(--f-m);letter-spacing:-.03em;text-align:right}.rrow b small{display:block;font:600 12px var(--f-m);color:var(--ac);letter-spacing:0}
:root[data-ui="light"] .rrow b small{color:var(--red)}
.rall{margin-top:12px}.rall summary{cursor:pointer;font-weight:700;font-size:14px;color:var(--ac);padding:6px 0}
:root[data-ui="light"] .rall summary{color:var(--red)}
.rtw,.btw{overflow-x:auto;margin:6px -18px 0;padding:0 18px}
.rtab{border-collapse:collapse;width:100%;min-width:520px;font-size:13.5px}
.rtab th,.rtab td{padding:9px 8px;border-bottom:1px solid var(--line);text-align:right;white-space:nowrap;font-family:var(--f-m)}
.rtab thead th{font:700 12px var(--f-b);color:var(--mute);vertical-align:bottom}
.rtab thead th small,.rtab td small{display:block;font-size:10.5px;color:var(--mute);font-weight:500}
.rtab tbody th{text-align:left;font-family:var(--f-b)}
.rtab th:nth-child(2),.rtab td:nth-child(2){background:color-mix(in srgb,var(--ac) 10%,transparent)}
.rnotes{margin-top:12px;display:grid;gap:6px}
.rnotes p{display:flex;gap:8px;align-items:flex-start;margin:0;padding:10px 12px;border-radius:12px;background:color-mix(in srgb,var(--ac) 8%,var(--sf2));border:1px solid var(--line);font-size:13.5px;font-weight:600}
.rnotes svg{width:16px;height:16px;flex:none;color:var(--ac);margin-top:1px}
.bted{border-collapse:separate;border-spacing:4px;min-width:620px}
.bted input{margin:0;padding:8px;font-size:13px;border-radius:9px;min-width:70px}
.bted th input{font-weight:700}.bted thead input{text-align:center;font-family:var(--f-m)}
.bted td button{border:0;background:none;color:var(--warn);font-size:16px}
'''
k=s.index("/* ---------- Welcome ---------- */");s=s[:k]+css+s[k:]
open('p3.src.html','w').write(s);print("ok")
