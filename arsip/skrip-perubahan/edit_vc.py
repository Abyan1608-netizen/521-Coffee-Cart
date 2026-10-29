s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
# CSS
rep('.k-empty{text-align:center;','''.vbox{margin:10px 0 4px;padding:12px;border-radius:16px;background:var(--sf2);border:1px solid var(--line)}
.vbox .add input{margin:0;text-transform:uppercase;font-family:var(--f-m)}
.vbox .add .btn{margin:0}
.vlist{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.vlist button{display:flex;flex-direction:column;align-items:flex-start;gap:1px;border:1.5px dashed color-mix(in srgb,var(--ac) 60%,var(--line));background:none;border-radius:12px;padding:7px 10px;text-align:left}
.vlist b{font:600 13px var(--f-m);color:var(--ac)}
.vlist small{font-size:11px;color:var(--mute)}
.von{display:flex;align-items:center;gap:10px;padding:10px 12px;border-radius:12px;background:color-mix(in srgb,var(--ok) 10%,var(--sf2));border:1px solid color-mix(in srgb,var(--ok) 30%,var(--line));font-size:14px}
.von b{font-family:var(--f-m);color:var(--ok)}
.von span{flex:1;min-width:0}
.von small{color:var(--mute)}
.von button{border:0;background:var(--sf3);border-radius:8px;width:30px;height:30px;color:var(--mute)}
.verr{color:var(--warn);font-size:13px;margin:8px 0 0}
.k-empty{text-align:center;''')
# voucher engine after total def
rep('''const sub=()=>lines().reduce((s,l)=>s+price(l.p)*l.q,0),total=()=>Math.max(0,sub()-disc);''','''const sub=()=>lines().reduce((s,l)=>s+price(l.p)*l.q,0),total=()=>Math.max(0,sub()-disc-vAmt());
const DAYS=["Minggu","Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"];
let vch="",verr="";
function vRule(p){if(p.dtype==="pct"||p.dtype==="rp")return{t:p.dtype,v:Number(p.dval)||0};if(p.dtype==="none")return{t:"",v:0};const m=String(p.badge||"").match(/(\\d{1,3})\\s*%/);if(m)return{t:"pct",v:+m[1]};const r=String(p.badge||"").match(/(?:rp\\.?\\s*)(\\d[\\d.]*)/i);if(r)return{t:"rp",v:+r[1].replace(/\\./g,"")};return{t:"",v:0}}
const vLabel=r=>r.t==="pct"?"Diskon "+r.v+"%":r.t==="rp"?"Potongan "+rp(r.v):"Nilai potongan belum diatur";
function vActive(){const t=kToday(),dw=new Date().getDay();return K.posts.filter(p=>p.type==="promo"&&!p.draft&&p.code&&(!p.start||p.start<=t)&&(!p.end||p.end>=t)&&(!(p.days||[]).length||p.days.includes(dw)))}
function vEval(code){
  code=String(code||"").trim().toUpperCase();if(!code)return null;
  const p=K.posts.find(x=>x.type==="promo"&&!x.draft&&String(x.code||"").toUpperCase()===code);
  if(!p)return{err:"Kode "+code+" tidak ditemukan. Cek ejaannya, atau promo belum diterbitkan di tab Kabar."};
  const t=kToday(),dw=new Date().getDay(),days=p.days||[];
  if(p.start&&p.start>t)return{p,err:"Promo ini baru berlaku mulai "+kFmt(p.start)+"."};
  if(p.end&&p.end<t)return{p,err:"Promo ini sudah berakhir "+kFmt(p.end)+"."};
  if(days.length&&!days.includes(dw))return{p,err:"Promo ini hanya berlaku hari "+days.map(d=>DAYS[d]).join(", ")+"."};
  const pr=(p.prods||[]).map(x=>x.toLowerCase()),L=lines().filter(l=>!pr.length||pr.includes(l.p.name.toLowerCase()));
  if(!L.length)return{p,err:"Promo ini khusus "+p.prods.join(", ")+". Belum ada di pesanan."};
  const base=L.reduce((s,l)=>s+price(l.p)*l.q,0),r=vRule(p);
  const amt=r.t==="pct"?Math.round(base*r.v/100):r.t==="rp"?Math.min(r.v,base):0;
  return{p,amt,r,base,note:r.t?"":"Nilai potongan promo ini belum diatur. Isi potongan manual, atau Owner bisa mengaturnya di tab Kabar."};
}
function vAmt(){if(!vch)return 0;const e=vEval(vch);return e&&!e.err?Math.min(e.amt,Math.max(0,sub()-disc)):0}
function vBox(){
  const e=vch?vEval(vch):null,act=vActive();
  if(e&&!e.err)return `<div class="vbox"><div class="von">${ic("check")}<span><b>${esc(e.p.code)}</b> · ${esc(e.p.title)}<small style="display:block">${vLabel(e.r)}${(e.p.prods||[]).length?" · khusus "+esc(e.p.prods.join(", ")):""}</small></span><button data-a="vrm" aria-label="Lepas voucher">${ic("x")}</button></div>${e.note?`<p class="verr">${e.note}</p>`:""}</div>`;
  return `<div class="vbox"><div class="add"><input id="vin" placeholder="Kode voucher" aria-label="Kode voucher" value="${esc(vch)}" autocapitalize="characters"><button class="btn sm" data-a="vgo">Pakai</button></div>${verr?`<p class="verr">${esc(verr)}</p>`:""}${act.length?`<div class="vlist">${act.map(p=>`<button data-a="vpick" data-v="${esc(p.code)}"><b>${esc(p.code)}</b><small>${esc(p.title)} · ${vLabel(vRule(p))}</small></button>`).join("")}</div>`:`<p class="note" style="margin:8px 0 0">Tidak ada promo berkode yang berlaku hari ini.</p>`}</div>`;
}''')
# cart body: voucher section after cara bayar, summary row
rep('''  <div class="lbl">Cara bayar</div>''','''  <div class="lbl">Voucher promo</div>${vBox()}
  <div class="lbl">Cara bayar</div>''')
rep('''  <div class="sumr" id="sdr" ${disc?"":"hidden"}><span>Diskon</span><span id="sdv">−${rp(disc)}</span></div>''','''  <div class="sumr" id="svr" ${vAmt()?"":"hidden"}><span>Voucher ${esc(vch)}</span><span id="svv">−${rp(vAmt())}</span></div>
  <div class="sumr" id="sdr" ${disc?"":"hidden"}><span>Diskon</span><span id="sdv">−${rp(disc)}</span></div>''')
rep('''  const sd=$("#sdr");if(sd){sd.hidden=!disc;$("#sdv").textContent="−"+rp(Math.min(disc,sub()))}''','''  const sd=$("#sdr");if(sd){sd.hidden=!disc;$("#sdv").textContent="−"+rp(Math.min(disc,sub()))}
  const sv=$("#svr");if(sv){sv.hidden=!vAmt();$("#svv").textContent="−"+rp(vAmt())}''')
# pay record
rep('''sub:sub(),disc:Math.min(disc,sub()),total:t,''','''sub:sub(),disc:Math.min(disc+vAmt(),sub()),vc:vAmt()?vch:"",vd:vAmt(),total:t,''')
rep('''  cart={};disc=0;paid=0;showDisc=false;pm=C().pm[0];inCart=false;headStat();receipt(tx);''','''  cart={};disc=0;paid=0;showDisc=false;vch="";verr="";pm=C().pm[0];inCart=false;headStat();receipt(tx);''')
rep('''${tx.disc?`<div class="line"><span>Diskon</span><span>−${rp(tx.disc)}</span></div>`:""}</div>''','''${tx.vd?`<div class="line"><span>Voucher ${esc(tx.vc)}</span><span>−${rp(tx.vd)}</span></div>`:""}${tx.disc-(tx.vd||0)>0?`<div class="line"><span>Diskon</span><span>−${rp(tx.disc-(tx.vd||0))}</span></div>`:""}</div>''')
rep('''<div><h3>Per kasir</h3>${bars(desc(s.by))}</div></div>''','''<div><h3>Per kasir</h3>${bars(desc(s.by))}</div><div><h3>Voucher dipakai</h3>${bars(desc(okTx(r).reduce((o,t)=>{if(t.vc)o[t.vc]=(o[t.vc]||0)+1;return o},{})),v=>v+"×")}</div></div>''')
rep('''"total","hpp","gross_profit","status","cancel_reason"],D.tx.map(t=>[t.no,t.d,new Date(t.at).toTimeString().slice(0,5),t.by||"",t.ch,t.pm,t.sub,t.disc,t.total,''','''"voucher_code","voucher_discount","total","hpp","gross_profit","status","cancel_reason"],D.tx.map(t=>[t.no,t.d,new Date(t.at).toTimeString().slice(0,5),t.by||"",t.ch,t.pm,t.sub,t.disc,t.vc||"",t.vd||0,t.total,''')
rep('''"payment_method","subtotal","discount","voucher_code"''','''"payment_method","subtotal","discount","voucher_code"''')
rep('''  else if(a==="clr"){cart={};disc=0;paid=0;showDisc=false;''','''  else if(a==="vgo"){const c2=($("#vin").value||"").trim().toUpperCase();if(!c2){$("#vin").focus();return}const e2=vEval(c2);if(e2.err){verr=e2.err;vch=""}else{vch=c2;verr="";toast("Voucher "+c2+" dipakai",1)}cartUI()}
  else if(a==="vpick"){const e2=vEval(v);if(e2.err){verr=e2.err;vch=""}else{vch=v;verr="";toast("Voucher "+v+" dipakai",1)}cartUI()}
  else if(a==="vrm"){vch="";verr="";cartUI()}
  else if(a==="clr"){cart={};disc=0;paid=0;showDisc=false;vch="";verr="";''')
# WA text & print include voucher
rep('''...(tx.disc?["Diskon  -"+rp(tx.disc)]:[]),''','''...(tx.vd?["Voucher "+tx.vc+"  -"+rp(tx.vd)]:[]),...(tx.disc-(tx.vd||0)>0?["Diskon  -"+rp(tx.disc-(tx.vd||0))]:[]),''')
rep('''L.push(hr);if(tx.disc)L.push(lr("Diskon","-"+rp(tx.disc)));''','''L.push(hr);if(tx.vd)L.push(lr("Voucher "+tx.vc,"-"+rp(tx.vd)));if(tx.disc-(tx.vd||0)>0)L.push(lr("Diskon","-"+rp(tx.disc-(tx.vd||0))));''')
# public promo meta: days & prods
rep('''${p.code?`<button class="k-code" data-a="kcopy"''','''${(p.days||[]).length?`<span class="when">${ic("cal")}Setiap ${p.days.map(d=>DAYS[d]).join(", ")}</span>`:""}${(p.prods||[]).length?`<span>Khusus ${esc(p.prods.join(", "))}</span>`:""}${p.code?`<button class="k-code" data-a="kcopy"''')
# promo editor fields
rep('''<label>Kode promo (opsional)<input id="p-code" value="${esc(p.code)}" placeholder="Contoh: SENIN521"></label>`:""}''','''<label>Kode promo (opsional)<input id="p-code" value="${esc(p.code)}" placeholder="Contoh: SENIN521"></label>
  <div class="sec" style="margin:14px 0 0;padding-top:2px"><h3>Potongan otomatis di kasir</h3><p class="note" style="margin-top:-4px">Saat kasir memasukkan kode ini, potongan langsung dihitung.</p>
  <div class="chips">${[["pct","Persen (%)"],["rp","Rupiah"],["none","Tanpa potongan"]].map(o=>`<button data-a="kdt" data-v="${o[0]}" aria-pressed="${(p.dtype||vRule(p).t||"none")===o[0]||(o[0]==="none"&&!p.dtype&&!vRule(p).t)}">${o[1]}</button>`).join("")}</div>
  ${(p.dtype||vRule(p).t)&&(p.dtype!=="none")?`<label>${(p.dtype||vRule(p).t)==="pct"?"Besar diskon (%)":"Besar potongan (Rp)"}<input id="p-dval" inputmode="numeric" value="${p.dval!==undefined&&p.dval!==""?esc(p.dval):vRule(p).v||""}"></label>`:""}
  <div class="lbl">Berlaku untuk menu <span class="mute">(kosong = semua menu)</span></div><div class="chips">${D.prod.filter(x=>x.active).map(x=>`<button data-a="kprod" data-v="${esc(x.name)}" aria-pressed="${(p.prods||[]).includes(x.name)}">${esc(x.name)}</button>`).join("")}</div>
  <div class="lbl">Hari berlaku <span class="mute">(kosong = setiap hari)</span></div><div class="chips">${[1,2,3,4,5,6,0].map(d=>`<button data-a="kday" data-v="${d}" aria-pressed="${(p.days||[]).includes(d)}">${DAYS[d].slice(0,3)}</button>`).join("")}</div></div>`:""}''')
# kGrab add dval
rep('''const m={title:"#p-title",''','''const dv=$("#p-dval");if(dv)kp.dval=Number(dv.value.replace(/\\D/g,""))||0;const m={title:"#p-title",''')
rep('''  else if(a==="kvis"){kGrab();kp.draft=v==="0";kPostSheet()}''','''  else if(a==="kvis"){kGrab();kp.draft=v==="0";kPostSheet()}
  else if(a==="kdt"){kGrab();if(!kp.dtype){const r=vRule(kp);if(r.t&&kp.dval===undefined)kp.dval=r.v}kp.dtype=v;kPostSheet()}
  else if(a==="kprod"){kGrab();kp.prods=kp.prods||[];kp.prods=kp.prods.includes(v)?kp.prods.filter(x=>x!==v):kp.prods.concat(v);kPostSheet()}
  else if(a==="kday"){kGrab();const d=+v;kp.days=kp.days||[];kp.days=kp.days.includes(d)?kp.days.filter(x=>x!==d):kp.days.concat(d).sort();kPostSheet()}''')
# save: dval captured already by kGrab? ksavep uses Object.assign with explicit fields; add dval read
rep('''draft:!!kp.draft});''','''draft:!!kp.draft});{const dv=$("#p-dval");if(dv)kp.dval=Number(dv.value.replace(/\\D/g,""))||0}''')
open('p3.src.html','w').write(s);print('ok')
