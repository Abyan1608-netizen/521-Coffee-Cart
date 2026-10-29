"""Fitur: stok produk jadi (botol/gelas) per batch + tanggal produksi/kedaluwarsa (FEFO),
pengingat H-1 (notifikasi HP), dan konfirmasi "Laporkan AI" di Chat 521. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*FG-PATCH-v1*/" in s:
    print("Sudah dipatch."); sys.exit(0)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:200]}")
    s = s.replace(old, new)

# ---------- CSS ----------
rep("</style>\n\n__LOGO__", """/*FG-PATCH-v1*/
.pill.ok{color:var(--ok);background:color-mix(in srgb,var(--ok) 14%,var(--sf2))}
.pill.h1{color:#1a0700;background:#ffc44d}
.pill.ex{color:#fff;background:#c0392b}
.fgsw{display:flex;gap:8px;margin:0 0 14px}
.fgsw button{flex:1;padding:11px 10px;border-radius:14px;border:1px solid var(--line);background:var(--sf);color:var(--mute);font:700 14px var(--f-b)}
.fgsw button[aria-pressed=true]{background:var(--ac);color:var(--on);border-color:transparent}
.fgnum{text-align:right;line-height:1.1}.fgnum b{display:block;font-size:22px}.fgnum small{color:var(--mute);font-size:11px}
.fgbt{display:grid;grid-template-columns:1fr auto;gap:6px 10px;align-items:center;padding:12px 14px;border:1px solid var(--line);border-radius:16px;background:var(--sf);margin-bottom:8px}
.fgbt.ex{border-color:color-mix(in srgb,#c0392b 60%,var(--line))}.fgbt.h1{border-color:color-mix(in srgb,#ffc44d 60%,var(--line))}
.fgbt small{color:var(--mute);font-size:12.5px}
.fgck{display:flex;gap:10px;align-items:flex-start;padding:10px 12px;border:1px solid var(--line);border-radius:12px;margin:0 0 8px;font-size:14px;line-height:1.35;background:var(--sf)}
.fgck input{width:20px;height:20px;margin:1px 0 0;flex:none;accent-color:var(--ac)}
.fgexp{font-weight:700;margin:-2px 0 12px}
.tile .fgq{display:block;font-size:11px;font-weight:700;opacity:.85;margin-top:2px}
.crep{position:absolute;left:12px;right:12px;bottom:12px;z-index:6;padding:16px;border-radius:20px;background:var(--sf2);border:1px solid var(--line);box-shadow:0 20px 60px -20px rgba(0,0,0,.8);animation:fadeUp .2s ease both}
.crep h3{margin:0 0 4px;font-size:18px;display:flex;align-items:center;gap:8px}.crep h3 svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2}
.crep p{margin:0 0 10px;color:var(--mute);font-size:13.5px}
.crep blockquote{margin:0 0 10px;padding:8px 10px;border-left:3px solid var(--ac);background:var(--sf);border-radius:8px;font-size:13px;max-height:84px;overflow:auto;color:var(--ink)}
.crep .chips{margin-bottom:8px}.crep textarea{width:100%;min-height:58px;margin:0 0 10px;font:inherit;font-size:15px}
.crep .two{display:grid;grid-template-columns:1fr 1fr;gap:8px}.crep .two .btn{margin:0}
</style>\n\n__LOGO__""")

# ---------- Data ----------
rep('["tx","exp","mv","log","ing","prod","mem"].forEach(k=>{if(!Array.isArray(d[k]))d[k]=[]});',
    '["tx","exp","mv","log","ing","prod","mem","fg"].forEach(k=>{if(!Array.isArray(d[k]))d[k]=[]});'
    '{const lim=ymd(new Date(Date.now()-45*864e5));d.fg=d.fg.filter(b=>b&&b.id&&(b.q>0||b.exp>=lim))}')

# ---------- Halaman Stok: pilihan Produk jadi | Bahan baku ----------
rep("function stk(){\n  const low=D.ing.filter(g=>g.min>0&&g.qty<g.min);",
    "function stkBahan(){\n  const low=D.ing.filter(g=>g.min>0&&g.qty<g.min);")
rep("/* ---------- Menu ---------- */", r'''/* ---------- Stok produk jadi (botol/gelas) per batch: FEFO + kedaluwarsa ---------- */
let stkV="fg",fgCur="",fgRR="Rusak / tumpah";
const FGU=["botol","gelas","cup","pcs"];
const fgUnit=p=>(p&&p.fgu)||"botol";
const fgD0=s=>{const [y,m,d]=String(s).split("-").map(Number);return new Date(y,m-1,d)};
const fgDays=b=>Math.round((fgD0(b.exp)-fgD0(ymd(new Date())))/864e5);
const fgSell=b=>b.q>0&&fgDays(b)>=0;
const fgSort=(a,b)=>a.exp<b.exp?-1:a.exp>b.exp?1:a.made<b.made?-1:a.made>b.made?1:0;
const fgOf=pid=>D.fg.filter(b=>b.p===pid&&b.q>0).sort(fgSort);
const fgAvail=pid=>D.fg.reduce((t,b)=>t+(b.p===pid&&fgSell(b)?b.q:0),0);
function fgSt(b){const d=fgDays(b);return d<0?{k:"ex",t:"Kedaluwarsa"}:d===0?{k:"h1",t:"Hari terakhir"}:d===1?{k:"h1",t:"H-1 · besok"}:{k:"ok",t:"Layak · "+d+" hari lagi"}}
function fgShort(L){for(const l of L){if(!l.p.fgOn)continue;const a=fgAvail(l.p.id);if(a<l.q)return `Stok siap jual ${l.p.name} tinggal ${a} ${fgUnit(l.p)} (yang layak konsumsi). Tambah di tab Stok → Produk jadi.`}return ""}
function fgTake(L,ref){const out=[];L.forEach(l=>{if(!l.p.fgOn)return;let need=l.q;
  for(const b of D.fg.filter(x=>x.p===l.p.id&&fgSell(x)).sort(fgSort)){if(need<=0)break;const t=Math.min(b.q,need);b.q-=t;need-=t;out.push({b:b.id,q:t,p:b.p});
    D.mv.push({at:iso(),i:"fg:"+b.p,type:"fg-jual",q:-t,cost:0,sup:"",ref})}});return out}
function fgBack(tx){(tx.fgu||[]).forEach(u=>{const b=D.fg.find(x=>x.id===u.b);if(!b)return;b.q+=u.q;D.mv.push({at:iso(),i:"fg:"+u.p,type:"fg-batal",q:u.q,cost:0,sup:"",ref:tx.no})});tx.fgu=[]}
function fgSchedule(){
  /* Pengingat H-1 jam 08.00 di HP ini (Android). Mencantumkan tanggal produksi. */
  if(!window.A521||!A521.notify)return;const items=[];
  D.fg.filter(b=>b.q>0&&fgDays(b)>=1).forEach(b=>{const p=prod(b.p),at=fgD0(b.exp);at.setDate(at.getDate()-1);at.setHours(8,0,0,0);
    items.push({id:"fg-"+b.id+"-"+b.exp,at:at.getTime(),title:"⚠️ Besok kedaluwarsa: "+(p?p.name:b.n),
      body:`${b.q} ${fgUnit(p)} · produksi ${kFmt(b.made)} · kedaluwarsa ${kFmt(b.exp)}. Jual lebih dulu atau tarik dari etalase.`})});
  A521.notify(items)}
function fgRemind(){const S=D.fg.filter(b=>b.q>0&&fgDays(b)<=1);if(!S.length||!can("stk"))return;
  const ex=S.filter(b=>fgDays(b)<0).length,soon=S.length-ex;
  toast(`⚠️ Produk jadi: ${soon?soon+" batch kedaluwarsa hari ini/besok":""}${soon&&ex?", ":""}${ex?ex+" batch sudah kedaluwarsa":""}. Cek tab Stok.`)}
function stk(){return `<div class="fgsw" role="tablist"><button data-a="stkv" data-v="fg" aria-pressed="${stkV==="fg"}">Produk jadi</button><button data-a="stkv" data-v="bahan" aria-pressed="${stkV==="bahan"}">Bahan baku</button></div>`+(stkV==="fg"?fgView():stkBahan())}
function fgView(){
  const P=D.prod.filter(p=>p.fgOn||D.fg.some(b=>b.p===p.id&&b.q>0));
  const alert=D.fg.filter(b=>b.q>0&&fgDays(b)<=1).sort(fgSort);
  const exq=D.fg.filter(b=>b.q>0&&fgDays(b)<0);
  return `<div class="greet"><div><h2>Stok produk jadi</h2><p>Botol/gelas siap jual. Kasir otomatis mengambil batch yang paling dekat kedaluwarsa lebih dulu (FEFO).</p></div></div>
  ${alert.length?`<div class="warn">${ic("alert")}<span><b>Perlu perhatian:</b> ${alert.map(b=>{const p=prod(b.p);return `${esc(p?p.name:b.n)} ${b.q} ${fgUnit(p)} (${fgSt(b).t.toLowerCase()}, produksi ${kFmt(b.made)})`}).join("; ")}</span></div>`:""}
  ${P.length?`<div class="list">${P.map(p=>{const B=fgOf(p.id),a=fgAvail(p.id),nb=B.find(fgSell)||B[0],st=nb?fgSt(nb):null;
    return `<button class="li" data-a="fgp" data-id="${p.id}"><span><b>${esc(p.name)}</b><small class="mute">${B.length?`${B.length} batch · terdekat kedaluwarsa ${kFmt(nb.exp)}`:"Stok kosong"}</small>${st?` <span class="pill ${st.k}">${st.t}</span>`:""}</span><span class="fgnum num"><b class="${a?"":"lowv"}">${a}</b><small>${fgUnit(p)} siap</small></span></button>`}).join("")}</div>`
   :`<div class="empty"><b>Belum ada stok produk jadi</b>Catat botol/gelas yang sudah diproduksi supaya kasir tahu sisa stok & tanggal kedaluwarsanya.</div>`}
  ${can("stk")?`<button class="btn" data-a="fgadd">+ Tambah stok produk jadi</button>`:""}
  ${exq.length&&can("stk")?`<button class="btn ghost" data-a="fgwaste" style="color:var(--warn)">Buang ${exq.reduce((t,b)=>t+b.q,0)} produk kedaluwarsa</button>`:""}`}
function fgpSheet(pid){fgCur=pid;const p=prod(pid);if(!p)return;const B=fgOf(pid);
  show(`<h2>${esc(p.name)}</h2><p class="mute" style="margin-top:-6px">Siap jual: <b>${fgAvail(pid)} ${fgUnit(p)}</b>. Urutan di bawah = urutan dijual (paling dekat kedaluwarsa dulu).</p>
  ${B.length?B.map(b=>{const st=fgSt(b);return `<div class="fgbt ${st.k}"><span><b>${b.q} ${fgUnit(p)}</b> <span class="pill ${st.k}">${st.t}</span><br><small>Produksi ${kFmt(b.made)} · kedaluwarsa ${kFmt(b.exp)} · dicatat ${esc(b.by||"-")}</small></span>${can("stk")?`<button class="btn ghost sm" data-a="fgless" data-id="${b.id}" style="margin:0">− Kurangi</button>`:""}</div>`}).join("")
   :`<p class="note">Belum ada batch. Tambahkan stok produksi terbaru.</p>`}
  ${can("stk")?`<button class="btn" data-a="fgadd" data-id="${pid}">+ Tambah batch</button>`:""}
  ${can("stkSet")&&p.fgOn?`<button class="btn ghost" data-a="fgoff" data-id="${pid}">Jual tanpa stok jadi (dibuat saat dipesan)</button><p class="note">Bila dimatikan, kasir kembali memotong bahan baku per pesanan.</p>`:""}`)}
function fgAddSheet(pid){const A=D.prod.filter(p=>p.active);if(!A.length){toast("Belum ada menu aktif.");return}
  const p=prod(pid)||A.find(x=>x.fgOn)||A[0],t=ymd(new Date()),sh=p.shelf||3;fgCur=p.id;
  show(`<h2>Tambah stok produk jadi</h2><p class="mute" style="margin-top:-6px">Hanya untuk produk <b>layak konsumsi</b> yang baru diproduksi.</p>
  <label>Produk<select id="fgP">${A.map(x=>`<option value="${x.id}"${x.id===p.id?" selected":""}>${esc(x.name)}</option>`).join("")}</select></label>
  <div class="two"><label>Jumlah<input id="fgQ" inputmode="numeric" placeholder="mis. 12"></label><label>Satuan<select id="fgU">${FGU.map(u=>`<option${u===fgUnit(p)?" selected":""}>${u}</option>`).join("")}</select></label></div>
  <div class="two"><label>Tanggal produksi<input id="fgM" type="date" value="${t}" max="${t}"></label><label>Masa simpan (hari)<input id="fgS" inputmode="numeric" value="${sh}"></label></div>
  <p class="fgexp" id="fgE"></p>
  <div class="lbl">Pemeriksaan kelayakan (wajib)</div>
  <label class="fgck"><input type="checkbox" class="fgc">Kemasan tersegel rapat, tidak bocor/menggembung, label lengkap.</label>
  <label class="fgck"><input type="checkbox" class="fgc">Disimpan dingin (chiller 1–4 °C) sejak diproduksi.</label>
  <label class="fgck"><input type="checkbox" class="fgc">Warna, aroma, dan rasa sudah dicek: normal.</label>
  ${(p.rec||[]).length?`<label class="fgck"><input type="checkbox" id="fgR" checked>Potong bahan baku sesuai resep untuk jumlah ini.</label>`:""}
  <button class="btn" data-a="fgsave">Simpan stok</button>`);fgExpTxt()}
function fgExpTxt(){const e=$("#fgE");if(!e)return;const m=$("#fgM").value,sh=parseInt($("#fgS").value,10);
  if(!m||!(sh>0)){e.textContent="";return}const x=fgD0(m);x.setDate(x.getDate()+sh);const b={exp:ymd(x)},d=fgDays(b);
  e.innerHTML=`Kedaluwarsa: <b>${kFmt(b.exp)} ${x.getFullYear()}</b> · ${d<1?'<span style="color:var(--warn)">tidak layak masuk stok</span>':d===1?'<span style="color:var(--warn)">besok (H-1)</span>':d+" hari lagi"}`}
function fgSave(){
  const p=prod($("#fgP").value),q=parseInt($("#fgQ").value,10),m=$("#fgM").value,sh=parseInt($("#fgS").value,10),u=$("#fgU").value,t=ymd(new Date());
  if(!p)return;if(!(q>=1&&q<=9999)){$("#fgQ").focus();toast("Isi jumlah (angka bulat, minimal 1)");return}
  if(!/^\d{4}-\d{2}-\d{2}$/.test(m)||m>t){toast("Tanggal produksi tidak boleh di masa depan");return}
  if(!(sh>=1&&sh<=90)){$("#fgS").focus();toast("Masa simpan 1–90 hari");return}
  const x=fgD0(m);x.setDate(x.getDate()+sh);const exp=ymd(x);
  if(fgDays({exp})<1){toast("Produk ini sudah/hari ini kedaluwarsa. Tidak boleh masuk stok siap jual.");return}
  if([...document.querySelectorAll(".fgc")].some(c=>!c.checked)){toast("Centang semua pemeriksaan kelayakan dulu. Produk yang tidak lolos jangan dijual.");return}
  const b={id:"b"+uid()+uid(),p:p.id,n:p.name,q,q0:q,made:m,exp,at:iso(),by:me?me.name:"",ok:1};
  D.fg.push(b);p.fgOn=1;p.shelf=sh;p.fgu=u;
  D.mv.push({at:iso(),i:"fg:"+p.id,type:"fg-masuk",q,cost:0,sup:"",ref:"produksi "+m});
  if($("#fgR")&&$("#fgR").checked)(p.rec||[]).forEach(r=>{const g=ing(r.i);if(!g)return;const used=r.q*q;g.qty-=used;D.mv.push({at:iso(),i:g.id,type:"produksi",q:-used,cost:g.cost,sup:"",ref:p.name+" ×"+q})});
  lg("Stok produk jadi",`${p.name} +${q} ${u} (produksi ${m}, kedaluwarsa ${exp})`);save();fgSchedule();
  if(window.A521&&A521.notifyPerm)A521.notifyPerm();
  fgpSheet(p.id);toast(`${p.name} +${q} ${u} tersimpan. Pengingat H-1: ${(()=>{const y=fgD0(exp);y.setDate(y.getDate()-1);return kFmt(ymd(y))})()} pukul 08.00`,1)}
function fgLessSheet(id){const b=D.fg.find(x=>x.id===id);if(!b)return;const p=prod(b.p);fgRR=fgDays(b)<0?"Kedaluwarsa, dibuang":"Rusak / tumpah";
  show(`<h2>Kurangi stok</h2><p class="mute" style="margin-top:-6px">${esc(p?p.name:b.n)} · batch produksi ${kFmt(b.made)} · sisa ${b.q} ${fgUnit(p)}</p>
  <label>Jumlah dikurangi<input id="fgLQ" inputmode="numeric" value="${fgDays(b)<0?b.q:1}"></label>
  <div class="lbl">Alasan</div><div class="chips">${["Rusak / tumpah","Kedaluwarsa, dibuang","Terjual di luar kasir","Sampel / dipakai sendiri","Koreksi hitung"].map(r=>`<button data-a="fgrr" data-v="${r}" aria-pressed="${r===fgRR}">${r}</button>`).join("")}</div>
  <button class="btn" data-a="fglessgo" data-id="${b.id}">Simpan</button><button class="btn ghost" data-a="fgp" data-id="${b.p}">Kembali</button>`)}

/* ---------- Menu ---------- */''')

# ---------- Kasir: cek stok jadi & FEFO ----------
rep("L.forEach(l=>l.p.rec.forEach(r=>us[r.i]=(us[r.i]||0)+r.q*l.q));",
    "L.forEach(l=>{if(!l.p.fgOn)l.p.rec.forEach(r=>us[r.i]=(us[r.i]||0)+r.q*l.q)});", 2)
rep("D.tx.push(tx);applyUse(tx,-1,\"sale\");", "D.tx.push(tx);tx.fgu=fgTake(L,tx.no);applyUse(tx,-1,\"sale\");", 2)
rep("const L=lines();if(!L.length)return;\n  const now=new Date()", "const L=lines();if(!L.length)return;{const fs=fgShort(L);if(fs){toast(fs);return}}\n  const now=new Date()")
rep('if(!pl.ok){toast("Kuota paket tidak cukup: "+pl.short.join(", "));return}',
    'if(!pl.ok){toast("Kuota paket tidak cukup: "+pl.short.join(", "));return}{const fs=fgShort(L);if(fs){toast(fs);return}}')
rep("function applyUse(tx,s,type){", "function applyUse(tx,s,type){if(s>0&&Array.isArray(tx.fgu)&&tx.fgu.length)fgBack(tx);")
rep('<span class="pr">${rp(price(p))}</span>', '<span class="pr">${rp(price(p))}${p.fgOn?`<span class="fgq">${fgAvail(p.id)} ${fgUnit(p)} siap</span>`:""}</span>')
rep('else if(a==="add"){cart[id]=', 'else if((a==="add"||a==="inc")&&prod(id)&&prod(id).fgOn&&fgAvail(id)<=(cart[id]||0)){const p=prod(id);toast(`Stok siap jual ${p.name} tinggal ${fgAvail(id)} ${fgUnit(p)}. Tambah di tab Stok → Produk jadi.`)}\n  else if(a==="add"){cart[id]=')

# ---------- Aksi ----------
rep('else if(a==="ing")ingSheet(id);', '''else if(a==="ing")ingSheet(id);
  else if(a==="stkv"){stkV=v==="bahan"?"bahan":"fg";render()}
  else if(a==="fgp")fgpSheet(id);
  else if(a==="fgadd"&&can("stk"))fgAddSheet(id);
  else if(a==="fgsave"&&can("stk"))fgSave();
  else if(a==="fgless"&&can("stk"))fgLessSheet(id);
  else if(a==="fgrr"){fgRR=v;document.querySelectorAll('[data-a="fgrr"]').forEach(x=>x.setAttribute("aria-pressed",x.dataset.v===v))}
  else if(a==="fglessgo"&&can("stk")){const b=D.fg.find(x=>x.id===id),k=parseInt($("#fgLQ").value,10);if(!b)return;if(!(k>=1&&k<=b.q)){$("#fgLQ").focus();toast("Jumlah 1–"+b.q);return}
    b.q-=k;D.mv.push({at:iso(),i:"fg:"+b.p,type:"fg-keluar",q:-k,cost:0,sup:"",ref:fgRR});lg("Kurangi stok produk jadi",`${b.n} −${k} (${fgRR}, produksi ${b.made})`);save();fgSchedule();fgpSheet(b.p);toast("Stok dikurangi "+k,1)}
  else if(a==="fgwaste"&&can("stk")){const X=D.fg.filter(b=>b.q>0&&fgDays(b)<0);let t=0;X.forEach(b=>{t+=b.q;D.mv.push({at:iso(),i:"fg:"+b.p,type:"fg-keluar",q:-b.q,cost:0,sup:"",ref:"Kedaluwarsa, dibuang"});b.q=0});
    lg("Buang produk kedaluwarsa",t+" item");save();fgSchedule();render();toast(t+" produk kedaluwarsa dicatat dibuang",1)}
  else if(a==="fgoff"&&can("stkSet")){const p=prod(id);if(p){p.fgOn=0;lg("Stok jadi dimatikan",p.name);save();shut();toast(p.name+" kembali dibuat saat dipesan",1)}}''')
rep('document.addEventListener("input",e=>{\n', 'document.addEventListener("input",e=>{\n  if(e.target.id==="fgM"||e.target.id==="fgS")fgExpTxt();\n')
rep('document.addEventListener("change",e=>{', 'document.addEventListener("change",e=>{\n  if(e.target.id==="fgM")fgExpTxt();\n  if(e.target.id==="fgP"&&prod(e.target.value)){const p=prod(e.target.value);$("#fgS").value=p.shelf||3;$("#fgU").value=fgUnit(p);fgExpTxt()}')

# Pengingat saat login + jadwal notifikasi saat aplikasi dibuka
rep("function enter(){", "function enter(){setTimeout(()=>{try{fgRemind()}catch(e){}},900);")
rep("return n}\npinMigrate().catch(()=>{});", "return n}\npinMigrate().catch(()=>{});setTimeout(()=>{try{fgSchedule()}catch(e){}},1500);", 1)

# CSV ekspor stok produk jadi
rep("const EX={", 'const EX={\n  "stok-produk-jadi":()=>csv(["batch_id","product_id","product","qty_left","qty_in","production_date","expiry_date","status","recorded_by"],D.fg.map(b=>[b.id,b.p,b.n,b.q,b.q0,b.made,b.exp,fgSt(b).t,b.by])),')

# ---------- Chat 521: konfirmasi "Laporkan AI" sebelum WhatsApp ----------
s0 = s
start = s.index('else if(a==="c_report"){')
end = s.index('else if(a==="c_clear"){', start)
s = s[:start] + r'''else if(a==="c_report"){const L=[...chatH].reverse().find(m=>m.role==="assistant"&&m.content);if(!L){toast("Belum ada jawaban AI untuk dilaporkan");return}
    const box=document.querySelector("#chat .cbox");if(!box)return;const old=box.querySelector(".crep");if(old)old.remove();
    box.insertAdjacentHTML("beforeend",`<div class="crep" role="dialog" aria-modal="true" aria-label="Laporkan AI"><h3><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V4m0 0h11l-2 4 2 4H5"/></svg>Laporkan AI</h3>
      <p>Jawaban Chat 521 keliru atau tidak pantas? Laporan dikirim ke Owner lewat WhatsApp supaya bisa diperbaiki.</p>
      <blockquote>${esc(L.content.slice(0,400))}${L.content.length>400?"…":""}</blockquote>
      <div class="chips">${["Jawaban keliru","Tidak pantas","Di luar topik","Lainnya"].map((r,i)=>`<button data-a="c_rr" data-v="${r}" aria-pressed="${!i}">${r}</button>`).join("")}</div>
      <textarea id="crn" maxlength="300" placeholder="Catatan tambahan (opsional)" aria-label="Catatan laporan"></textarea>
      <div class="two"><button class="btn ghost" data-a="c_rx">Batal</button><button class="btn" data-a="c_rsend">Kirim laporan</button></div></div>`)}
  else if(a==="c_rr"){document.querySelectorAll('[data-a="c_rr"]').forEach(x=>x.setAttribute("aria-pressed",x.dataset.v===v))}
  else if(a==="c_rx"){const r=document.querySelector("#chat .crep");if(r)r.remove()}
  else if(a==="c_rsend"){const L=[...chatH].reverse().find(m=>m.role==="assistant"&&m.content);const r=document.querySelector("#chat .crep");if(!L||!r)return;
    const why=(r.querySelector('[data-a="c_rr"][aria-pressed="true"]')||{}).dataset?.v||"Lainnya",note=(($("#crn")||{}).value||"").trim();
    const t="Laporan AI (Chat 521)\nAlasan: "+why+(note?"\nCatatan: "+note:"")+"\n\nJawaban yang dilaporkan:\n"+L.content.slice(0,1500),w=waNum((K.store||{}).wa);r.remove();
    if(w){const u="https://wa.me/"+w+"?text="+encodeURIComponent(t);if(window.A521)A521.open(u);else window.open(u,"_blank","noopener")}else copy(t,"Teks laporan tersalin. Kirim ke Owner ya.");toast("Terima kasih sudah melapor 🙏",1)}
  ''' + s[end:]
assert s != s0
rep('aria-label="Laporkan jawaban" title="Laporkan jawaban yang keliru atau tidak pantas"', 'aria-label="Laporkan AI" title="Laporkan AI"')

P.write_text(s)
print("OK, fitur stok produk jadi + pengingat + Laporkan AI diterapkan.")
