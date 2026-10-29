s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
# helpers before stk()
rep('function stk(){','''/* Satuan: stok disimpan dalam satuan dasar (ml / g / pcs) supaya resep tetap cocok; tampilan & input bisa liter / kg */
const UF={ml:1,l:1000,g:1,kg:1000,pcs:1},UL={ml:"ml",l:"liter",g:"gram",kg:"kg",pcs:"pcs"},USH={ml:"ml",l:"L",g:"g",kg:"kg",pcs:"pcs"};
const fam=b=>b==="ml"?["ml","l"]:b==="g"?["g","kg"]:["pcs"];
const baseOf=u=>u==="l"?"ml":u==="kg"?"g":u;
const dU=g=>fam(g.unit).includes(g.disp)?g.disp:g.unit;
const fq=v=>{const r=Math.round(v*100)/100;return new Intl.NumberFormat("id-ID",{maximumFractionDigits:2}).format(r)};
const qtyTxt=(g,v)=>fq((v===undefined?g.qty:v)/UF[dU(g)])+" "+USH[dU(g)];
const uSel=(id,g)=>{const F=fam(g.unit);return F.length>1?`<select id="${id}" aria-label="Satuan" style="margin:4px 0 10px">${F.map(u=>`<option value="${u}"${u===dU(g)?" selected":""}>${UL[u]}</option>`).join("")}</select>`:""};
function stk(){''')
# list display
rep('''${g.min?"min "+g.min+" "+g.unit:"Atur batas minimum"}${own()&&g.cost?" · "+rp(g.cost)+"/"+g.unit:""}</small>''','''${g.min?"min "+qtyTxt(g,g.min):"Atur batas minimum"}${own()&&g.cost?" · "+rp(g.cost*UF[dU(g)])+"/"+USH[dU(g)]:""}</small>''')
rep('''<b class="num ${lo?"lowv":""}">${+g.qty.toFixed(1)} ${g.unit}</b>''','''<b class="num ${lo?"lowv":""}">${qtyTxt(g)}</b>''')
# ingSheet
rep('''  show(`<h2>${esc(g.name)}</h2><p class="mute num" style="margin-top:-6px">Stok sekarang ${+g.qty.toFixed(1)} ${g.unit}</p>
  <h3>Catat belanja</h3><div class="two"><input id="inq" inputmode="decimal" placeholder="Jumlah (${g.unit})" aria-label="Jumlah masuk"><input id="inp" inputmode="numeric" placeholder="Total harga (Rp)" aria-label="Total harga"></div><input id="ins" placeholder="Supplier (opsional)" aria-label="Supplier"><button class="btn" data-a="stin">Tambah ke stok</button>
  <h3>Hitung ulang (stock opname)</h3><div class="add"><input id="opn" inputmode="decimal" placeholder="Jumlah sebenarnya (${g.unit})" aria-label="Stok aktual"><button class="btn sm" data-a="opname">Simpan</button></div>
  ${own()?`<h3>Pengaturan bahan</h3><input id="gnm" value="${esc(g.name)}" aria-label="Nama bahan"><div class="two"><label>Batas minimum<input id="mn" inputmode="decimal" value="${g.min||""}"></label><label>Harga per ${g.unit}<input id="cs" inputmode="decimal" value="${g.cost||""}"></label></div><button class="btn ghost" data-a="ingset">Simpan pengaturan</button>`:""}`);''','''  const F=fam(g.unit),du=dU(g),uf=UF[du];
  show(`<h2>${esc(g.name)}</h2><p class="mute num" style="margin-top:-6px">Stok sekarang ${qtyTxt(g)}${du!==g.unit?` <span class="mute">(${fq(g.qty)} ${g.unit})</span>`:""}</p>
  <h3>Catat belanja</h3><div class="${F.length>1?"rr3":"two"}"><input id="inq" inputmode="decimal" placeholder="Jumlah" aria-label="Jumlah masuk">${uSel("inu",g)}<input id="inp" inputmode="numeric" placeholder="Total harga (Rp)" aria-label="Total harga"></div><input id="ins" placeholder="Supplier (opsional)" aria-label="Supplier"><button class="btn" data-a="stin">Tambah ke stok</button>
  <h3>Hitung ulang (stock opname)</h3><div class="${F.length>1?"rr3":"add"}"><input id="opn" inputmode="decimal" placeholder="Jumlah sebenarnya" aria-label="Stok aktual">${uSel("opu",g)}<button class="btn sm" data-a="opname">Simpan</button></div>
  ${own()?`<h3>Pengaturan bahan</h3><input id="gnm" value="${esc(g.name)}" aria-label="Nama bahan">
  <div class="lbl">Satuan</div><div class="chips">${["ml","l","g","kg","pcs"].map(u=>`<button data-a="unit" data-v="${u}" aria-pressed="${u===du}">${UL[u]}</button>`).join("")}</div>
  <p class="note" style="margin-top:-4px">ml ↔ liter dan gram ↔ kg dikonversi otomatis. Resep tetap memakai ${g.unit==="pcs"?"pcs":g.unit==="ml"?"ml":"gram"}.</p>
  <div class="two"><label>Batas minimum (${USH[du]})<input id="mn" inputmode="decimal" value="${g.min?fq(g.min/uf):""}"></label><label>Harga per ${UL[du]}<input id="cs" inputmode="decimal" value="${g.cost?Math.round(g.cost*uf*100)/100:""}"></label></div><button class="btn ghost" data-a="ingset">Simpan pengaturan</button>`:""}`);''')
# css rr3
rep('.rr{display:grid;grid-template-columns:1fr 84px 40px;','.rr3{display:grid;grid-template-columns:minmax(0,1fr) 92px minmax(0,1.1fr);gap:8px;align-items:start}\n.rr3 .btn{margin:4px 0 10px}\n.rr{display:grid;grid-template-columns:1fr 84px 40px;')
# stin / opname / ingset
rep('''    const g=ing(cur),qq=n($("#inq").value),tp=rpv($("#inp").value);if(qq<=0){$("#inq").focus();return}''','''    const g=ing(cur),iu=$("#inu")?$("#inu").value:dU(g),raw=n($("#inq").value),qq=raw*UF[iu],tp=rpv($("#inp").value);if(qq<=0){$("#inq").focus();return}''')
rep('''lg("Stok masuk",g.name+" +"+qq+" "+g.unit);save();shut();toast(g.name+" bertambah "+qq+" "+g.unit,1);''','''lg("Stok masuk",g.name+" +"+fq(raw)+" "+USH[iu]);save();shut();toast(g.name+" bertambah "+fq(raw)+" "+USH[iu],1);''')
rep('''    const g=ing(cur),val=$("#opn").value;if(val===""){$("#opn").focus();return}const x=n(val),d=x-g.qty;''','''    const g=ing(cur),val=$("#opn").value;if(val===""){$("#opn").focus();return}const ou=$("#opu")?$("#opu").value:dU(g),x=n(val)*UF[ou],d=x-g.qty;''')
rep('''lg("Stock opname",g.name+": "+(d>=0?"+":"")+(+d.toFixed(1))+" "+g.unit);''','''lg("Stock opname",g.name+": "+(d>=0?"+":"")+qtyTxt(g,d));''')
rep('''else if(a==="ingset"&&own()){const g=ing(cur),nm=$("#gnm").value.trim();if(nm)g.name=nm;g.min=n($("#mn").value);g.cost=n($("#cs").value);''','''else if(a==="ingset"&&own()){const g=ing(cur),nm=$("#gnm").value.trim(),uf=UF[dU(g)];if(nm)g.name=nm;g.min=n($("#mn").value)*uf;g.cost=n($("#cs").value)/uf;''')
rep('''  else if(a==="ingset"&&own()){''','''  else if(a==="unit"&&own()){const g=ing(cur),nb=baseOf(v);
    if(nb!==g.unit){if(!confirmUnit){confirmUnit=v;toast("Ketuk sekali lagi untuk mengganti jenis satuan. Angka stok dan resep tidak dikonversi.");return}D.prod.forEach(p=>p.rec.forEach(r=>{}));lg("Ganti jenis satuan",g.name+": "+g.unit+" → "+nb);g.unit=nb}
    confirmUnit=null;g.disp=v;lg("Ubah satuan",g.name+": "+UL[v]);save();ingSheet(cur)}
  else if(a==="ingset"&&own()){''')
rep('''let tab="pos",cart={}''','''let confirmUnit=null,tab="pos",cart={}''')
# new ingredient
rep('''<label>Satuan<select id="nu"><option>ml</option><option>g</option><option>pcs</option></select></label>''','''<label>Satuan<select id="nu"><option value="ml">ml</option><option value="l">liter</option><option value="g">gram</option><option value="kg">kg</option><option value="pcs">pcs</option></select></label>''')
rep('''D.ing.push({id:"i"+uid(),name:nm,unit:$("#nu").value,type:$("#nt").value,qty:0,min:0,cost:0});''','''const u0=$("#nu").value;D.ing.push({id:"i"+uid(),name:nm,unit:baseOf(u0),disp:u0,type:$("#nt").value,qty:0,min:0,cost:0});''')
open('p3.src.html','w').write(s);print('ok')
