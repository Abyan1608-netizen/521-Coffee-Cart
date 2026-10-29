"""Perubahan 04: kasir Cup | Botol, hapus stok, pengaturan notifikasi (kapan, apa, untuk siapa, suara),
notifikasi pelanggan untuk promo/diskon/kabar, dan tanda BARU di halaman umum. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V4-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)

# ---------- CSS ----------
rep(".pxcv{display:block!important;width:100%;height:100%}", """.pxcv{display:block!important;width:100%;height:100%}
/*V4-PATCH*/
.posv{margin:4px 0 12px}.posv button{display:flex;align-items:center;justify-content:center;gap:6px}
.posv small{font-size:11px;opacity:.8;font-weight:600}
.k-newb{position:absolute;top:10px;left:10px;z-index:4;padding:4px 9px;border-radius:999px;background:var(--red);color:#fff;font:800 11px var(--f-b);letter-spacing:.08em;box-shadow:0 6px 18px -6px rgba(0,0,0,.6)}
.isnew{position:relative}
.nfc{border:1px solid var(--line);border-radius:16px;padding:12px 14px;margin:0 0 10px;background:var(--sf)}
.nfc .nfh{display:flex;align-items:center;justify-content:space-between;gap:10px}
.nfc .nfh b{font-size:15px}.nfc .nfh small{display:block;color:var(--mute);font-size:12.5px;font-weight:500;margin-top:2px}
.nfc .nfh input{width:22px;height:22px;flex:none;accent-color:var(--ac)}
.nfc .nfr{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}
.nfc .nfr label{margin:0;font-size:12.5px}.nfc .nfr select,.nfc .nfr input{margin-top:4px}
.nfc .nfp{display:flex;gap:8px;align-items:flex-end}.nfc .nfp select{flex:1}
.nfc .nfp button{margin:0;padding:10px 12px;flex:none}
.nfc.off .nfr{opacity:.45;pointer-events:none}
.fgdel{background:transparent;border:1px solid var(--line);color:var(--warn);border-radius:12px;padding:8px 10px;font:700 13px var(--f-b)}
""")

# ---------- Varian botol: proxy keranjang ----------
rep("const lines=()=>Object.keys(cart).filter(k=>cart[k]>0&&prod(k)).map(k=>({p:prod(k),q:cart[k]}));",
    r'''/* Varian Botol: kunci keranjang "idmenu@b" = botol dari stok produk jadi; tanpa akhiran = cup dibuat saat dipesan */
const isB=k=>String(k).endsWith("@b"),bid=k=>String(k).slice(0,-2);
function bProxy(p){const f=+p.bfac||1;return Object.assign({},p,{id:p.id+"@b",_pid:p.id,_b:1,name:p.name+" · Botol",size:p.bsize||"Botol",price:+p.bprice||p.price,rprice:+p.brprice||0,
  rec:(p.rec||[]).map(r=>({i:r.i,q:r.q*f})),out:fgAvail(p.id)<=0})}
const cp=k=>{if(isB(k)){const p=prod(bid(k));return p&&p.fgOn?bProxy(p):null}return prod(k)};
const lines=()=>Object.keys(cart).filter(k=>cart[k]>0&&cp(k)).map(k=>({p:cp(k),q:cart[k]}));
let posV="cup";''')
rep("cart=Object.fromEntries(Object.entries(sv.cart||{}).filter(([k])=>prod(k)));", "cart=Object.fromEntries(Object.entries(sv.cart||{}).filter(([k])=>cp(k)));")
rep("  Object.keys(cart).forEach(k=>{if(!prod(k))delete cart[k]});", "  Object.keys(cart).forEach(k=>{if(!cp(k))delete cart[k]});")

# grid: tab Botol menampilkan menu yang punya stok botol
rep("const l=D.prod.filter(p=>p.active&&(cat===\"Semua\"||p.cat===cat)&&p.name.toLowerCase().includes(q.toLowerCase()));",
    "const l=(posV===\"botol\"?D.prod.filter(p=>p.active&&p.fgOn).map(bProxy):D.prod.filter(p=>p.active)).filter(p=>(cat===\"Semua\"||p.cat===cat)&&p.name.toLowerCase().includes(q.toLowerCase()));\n  if(posV===\"botol\"&&!l.length)return `<div class=\"empty\" style=\"grid-column:1/-1\"><b>Belum ada stok botol</b>Tambah di tab Stok → Produk jadi. Botol yang layak jual otomatis muncul di sini.</div>`;")
rep('<span class="pr">${rp(price(p))}${p.fgOn?`<span class="fgq">${fgAvail(p.id)} ${fgUnit(p)} siap</span>`:""}</span>',
    '<span class="pr">${rp(price(p))}${p._b?`<span class="fgq">${fgAvail(p._pid)} ${fgUnit(p)} siap${p.bsize?" · "+esc(p.bsize):""}</span>`:""}</span>')
rep('`:`${can("sold")?"":"<!--"}<button class="soldb', '`:`${can("sold")&&!p._b?"":"<!--"}<button class="soldb')
rep('</button>${can("sold")?"":"-->"}`}</div>`).join("");', '</button>${can("sold")&&!p._b?"":"-->"}`}</div>`).join("");')
rep('  ${D.prod.length>6?`<div class="search">', '''  ${D.prod.some(p=>p.active&&p.fgOn)?`<div class="fgsw posv" role="tablist" aria-label="Jenis penyajian"><button data-a="posv" data-v="cup" aria-pressed="${posV==="cup"}">☕ Cup <small>dibuat saat dipesan</small></button><button data-a="posv" data-v="botol" aria-pressed="${posV==="botol"}">🧴 Botol <small>dari stok</small></button></div>`:""}
  ${D.prod.length>6?`<div class="search">''')

# kasir: cup selalu potong bahan baku; botol dari stok (FEFO)
rep("L.forEach(l=>{if(!l.p.fgOn)l.p.rec.forEach(r=>us[r.i]=(us[r.i]||0)+r.q*l.q)});",
    "L.forEach(l=>{if(!l.p._b)l.p.rec.forEach(r=>us[r.i]=(us[r.i]||0)+r.q*l.q)});", 2)
rep("function fgShort(L){for(const l of L){if(!l.p.fgOn)continue;const a=fgAvail(l.p.id);if(a<l.q)return `Stok siap jual ${l.p.name} tinggal ${a} ${fgUnit(l.p)} (yang layak konsumsi). Tambah di tab Stok → Produk jadi.`}return \"\"}",
    "function fgShort(L){for(const l of L){if(!l.p._b)continue;const a=fgAvail(l.p._pid);if(a<l.q)return `Stok botol ${prod(l.p._pid).name} tinggal ${a} ${fgUnit(l.p)} (yang layak konsumsi). Tambah di tab Stok → Produk jadi.`}return \"\"}")
rep("function fgTake(L,ref){const out=[];L.forEach(l=>{if(!l.p.fgOn)return;let need=l.q;\n  for(const b of D.fg.filter(x=>x.p===l.p.id&&fgSell(x)).sort(fgSort)){",
    "function fgTake(L,ref){const out=[];L.forEach(l=>{if(!l.p._b)return;let need=l.q;\n  for(const b of D.fg.filter(x=>x.p===l.p._pid&&fgSell(x)).sort(fgSort)){")
rep('else if((a==="add"||a==="inc")&&prod(id)&&prod(id).fgOn&&fgAvail(id)<=(cart[id]||0)){const p=prod(id);toast(`Stok siap jual ${p.name} tinggal ${fgAvail(id)} ${fgUnit(p)}. Tambah di tab Stok → Produk jadi.`)}',
    'else if((a==="add"||a==="inc")&&isB(id)&&prod(bid(id))&&fgAvail(bid(id))<=(cart[id]||0)){const p=prod(bid(id));toast(`Stok botol ${p.name} tinggal ${fgAvail(p.id)} ${fgUnit(p)} yang layak jual. Tambah di tab Stok → Produk jadi.`)}\n  else if(a==="posv"){posV=v==="botol"?"botol":"cup";render()}')
# produksi botol memotong bahan sesuai faktor botol
rep("(p.rec||[]).forEach(r=>{const g=ing(r.i);if(!g)return;const used=r.q*q;", "(p.rec||[]).forEach(r=>{const g=ing(r.i);if(!g)return;const used=r.q*q*(+p.bfac||1);")
rep('Potong bahan baku sesuai resep untuk jumlah ini.', 'Potong bahan baku sesuai resep${(+p.bfac||1)!==1?" (×"+p.bfac+" per botol)":""} untuk jumlah ini.')

# ---------- Stok: hapus batch / hapus dari daftar + pengaturan botol ----------
rep('${can("stk")?`<button class="btn ghost sm" data-a="fgless" data-id="${b.id}" style="margin:0">− Kurangi</button>`:""}</div>`}).join("")',
    '${can("stk")?`<span style="display:flex;flex-direction:column;gap:6px"><button class="btn ghost sm" data-a="fgless" data-id="${b.id}" style="margin:0">− Kurangi</button><button class="fgdel" data-a="fgdel" data-id="${b.id}">Hapus</button></span>`:""}</div>`}).join("")')
rep('''  ${can("stkSet")&&p.fgOn?`<button class="btn ghost" data-a="fgoff" data-id="${pid}">Jual tanpa stok jadi (dibuat saat dipesan)</button><p class="note">Bila dimatikan, kasir kembali memotong bahan baku per pesanan.</p>`:""}`)}''',
    '''  ${can("stkSet")||can("menu")?`<h3>Pengaturan botol</h3><div class="two"><label>Harga botol (Rp)<input id="fbP" inputmode="numeric" value="${p.bprice||""}" placeholder="${p.price}"></label><label>Harga reseller botol<input id="fbR" inputmode="numeric" value="${p.brprice||""}" placeholder="opsional"></label></div>
  <div class="two"><label>Ukuran botol<input id="fbS" value="${esc(p.bsize||"")}" placeholder="mis. 250 ml"></label><label>Bahan per botol (× resep cup)<input id="fbF" inputmode="decimal" value="${p.bfac||1}"></label></div>
  <p class="note">Contoh: resep cup 170 ml, botol 340 ml → isi 2. Dipakai untuk memotong bahan saat produksi & menghitung modal botol.</p><button class="btn ghost" data-a="fgbset" data-id="${pid}">Simpan pengaturan botol</button>`:""}
  ${can("stk")?`<button class="btn ghost" data-a="fgrm" data-id="${pid}" style="color:var(--warn)">Hapus dari daftar stok produk jadi</button><p class="note">Menghapus semua batch menu ini dari daftar & menyembunyikan tab Botol untuk menu ini. Riwayat tetap tercatat.</p>`:""}`)}''')
rep('else if(a==="fgoff"&&can("stkSet")){', '''else if(a==="fgdel"&&can("stk")){const b=D.fg.find(x=>x.id===id);if(!b)return;confirmSheet(`Hapus batch ${esc(b.n)} produksi ${kFmt(b.made)}?`,`Sisa ${b.q} ${fgUnit(prod(b.p))} ikut terhapus dari stok. Tercatat di riwayat.`,"fgdelgo","Hapus batch","Batal");$("#s").dataset.v=id}
  else if(a==="fgdelgo"&&can("stk")){const id2=$("#s").dataset.v,b=D.fg.find(x=>x.id===id2);if(!b)return;D.fg=D.fg.filter(x=>x.id!==id2);D.mv.push({at:iso(),i:"fg:"+b.p,type:"fg-hapus",q:-b.q,cost:0,sup:"",ref:"hapus batch "+b.made});lg("Hapus batch produk jadi",`${b.n} (${b.q}, produksi ${b.made})`);save();fgSchedule();fgpSheet(b.p);toast("Batch dihapus",1)}
  else if(a==="fgrm"&&can("stk")){const p=prod(id);if(!p)return;const n=D.fg.filter(b=>b.p===id&&b.q>0).reduce((t,b)=>t+b.q,0);confirmSheet(`Hapus ${esc(p.name)} dari stok produk jadi?`,n?`Masih ada ${n} ${fgUnit(p)} tersisa dan akan ikut terhapus.`:"Stok sudah 0. Menu ini hilang dari daftar & tab Botol.","fgrmgo","Hapus dari daftar","Batal");$("#s").dataset.v=id}
  else if(a==="fgrmgo"&&can("stk")){const id2=$("#s").dataset.v,p=prod(id2);if(!p)return;const B=D.fg.filter(b=>b.p===id2);B.forEach(b=>{if(b.q>0)D.mv.push({at:iso(),i:"fg:"+id2,type:"fg-hapus",q:-b.q,cost:0,sup:"",ref:"hapus dari daftar"})});D.fg=D.fg.filter(b=>b.p!==id2);p.fgOn=0;Object.keys(cart).forEach(k=>{if(k===id2+"@b")delete cart[k]});lg("Hapus dari stok produk jadi",p.name);save();fgSchedule();shut();toast(p.name+" dihapus dari stok produk jadi",1)}
  else if(a==="fgbset"&&(can("stkSet")||can("menu"))){const p=prod(id);if(!p)return;const bp=rpv($("#fbP").value),br=rpv($("#fbR").value),f=parseFloat(String($("#fbF").value).replace(",","."))||1;
    if(f<=0||f>20){toast("Bahan per botol 0,1–20");return}p.bprice=bp||0;p.brprice=br||0;p.bsize=$("#fbS").value.trim().slice(0,20);p.bfac=Math.round(f*100)/100;lg("Pengaturan botol",`${p.name}: ${rp(p.bprice||p.price)}${p.bsize?" · "+p.bsize:""}`);save();fgpSheet(id);toast("Pengaturan botol tersimpan",1)}
  else if(a==="fgoff"&&can("stkSet")){''')
rep('const fgOf=pid=>D.fg.filter(b=>b.p===pid&&b.q>0).sort(fgSort);', 'const fgOf=pid=>D.fg.filter(b=>b.p===pid&&b.q>0).sort(fgSort);/* stok kosong: baris tetap ada sampai dihapus */')

# ---------- Pengaturan notifikasi ----------
rep('  ["chat","chat","Chat 521",', '  ["notif","alert","Notifikasi",()=>{const c=nfCfg(),on=NFT.filter(t=>c[t[0]].on).length;return `${on} dari ${NFT.length} jenis aktif · pengingat ${c.exp.time}`}],\n  ["chat","chat","Chat 521",')
rep("function setBody(id){\n  const c=C();", "function setBody(id){\n  const c=C();\n  if(id===\"notif\")return nfSet();")
rep("/* ---------- Menu ---------- */", r'''/* ---------- Notifikasi: kapan, apa saja, untuk siapa, suara (tersimpan di Kabar → berlaku di semua HP & pelanggan) ---------- */
const NFT=[["exp","Produk jadi hampir kedaluwarsa","Pengingat H-n sebelum kedaluwarsa, berisi tanggal produksi",1],
  ["low","Stok bahan baku menipis","Daftar bahan di bawah batas minimum",1],
  ["promo","Promo baru","Saat promo diterbitkan",0],["diskon","Diskon baru","Promo yang punya potongan harga",0],
  ["kabar","Kabar terbaru","Saat berita/kabar diterbitkan",0],["event","Kegiatan","Saat kegiatan/event diterbitkan",0]];
const NFS=[["ding","Ding"],["lonceng","Lonceng"],["kaching","Ka-ching"],["ceria","Ceria"],["lembut","Lembut"],["bawaan","Bawaan HP"],["senyap","Tanpa suara"]];
const NFDEF={exp:{on:1,to:"staf",snd:"ding",time:"08:00",days:1},low:{on:1,to:"staf",snd:"lembut",time:"08:00"},promo:{on:1,to:"semua",snd:"ceria"},diskon:{on:1,to:"semua",snd:"kaching"},kabar:{on:1,to:"semua",snd:"lonceng"},event:{on:1,to:"semua",snd:"ding"},edit:0};
function nfCfg(){const c=JSON.parse(JSON.stringify(NFDEF)),n=(K.store&&K.store.notif)||{};Object.keys(c).forEach(k=>{if(typeof c[k]==="object")Object.assign(c[k],n[k]||{});else if(n[k]!=null)c[k]=n[k]});return c}
function nfSet(){const c=nfCfg(),TO=[["staf","Staf (owner, admin, karyawan, reseller)"],["pelanggan","Pelanggan"],["semua","Semua"]];
  return `<p class="note" style="margin-top:0">Atur <b>kapan</b> dan <b>apa saja</b> yang dikirim sebagai notifikasi HP, <b>untuk siapa</b>, dan <b>suaranya</b>. Promo/diskon/kabar sampai ke pelanggan yang memasang aplikasi dalam ±15–30 menit setelah diterbitkan (langsung saat aplikasi dibuka).</p>
  ${NFT.map(([k,t,d,staffOnly])=>{const x=c[k];return `<div class="nfc${x.on?"":" off"}" data-nfk="${k}"><div class="nfh"><span><b>${t}</b><small>${d}</small></span><input type="checkbox" class="nfon" ${x.on?"checked":""} aria-label="Aktifkan ${t}"></div>
    <div class="nfr">${staffOnly?`<label>Untuk<select class="nfto" disabled><option value="staf">Staf</option></select></label>`:`<label>Untuk<select class="nfto">${TO.map(([v,l])=>`<option value="${v}"${x.to===v?" selected":""}>${l}</option>`).join("")}</select></label>`}
    <label>Suara<span class="nfp"><select class="nfsnd">${NFS.map(([v,l])=>`<option value="${v}"${x.snd===v?" selected":""}>${l}</option>`).join("")}</select><button class="btn ghost sm" data-a="nfplay" data-v="${k}" aria-label="Coba suara">▶</button></span></label>
    ${k==="exp"?`<label>Jam pengingat<input type="time" class="nftime" value="${x.time}"></label><label>Diingatkan<select class="nfdays">${[1,2,3].map(n=>`<option value="${n}"${+x.days===n?" selected":""}>H-${n}</option>`).join("")}</select></label>`:""}
    ${k==="low"?`<label>Jam pengingat<input type="time" class="nftime" value="${x.time}"></label>`:""}</div></div>`}).join("")}
  <label class="fgck"><input type="checkbox" id="nfedit" ${c.edit?"checked":""}>Kirim juga notifikasi saat promo/diskon/kabar <b>diubah</b> (bukan hanya yang baru).</label>
  <button class="btn" data-a="nfsave">${AR&&kcan?"Simpan & terbitkan":"Simpan"}</button>
  <p class="note">${AR&&kcan?"Langsung berlaku untuk semua HP tim & pelanggan.":"Tersimpan di HP ini. Agar sampai ke pelanggan & HP lain, terbitkan dari HP Owner."} Pengingat stok berlaku di HP yang mencatat stoknya. Suara bisa diubah kapan saja.</p>`}
function nfRead(){const c=nfCfg();document.querySelectorAll(".nfc[data-nfk]").forEach(el=>{const k=el.dataset.nfk,x=c[k];x.on=el.querySelector(".nfon").checked?1:0;
  const to=el.querySelector(".nfto");if(to&&!to.disabled)x.to=to.value;x.snd=el.querySelector(".nfsnd").value;const tm=el.querySelector(".nftime");if(tm&&/^\d{2}:\d{2}$/.test(tm.value))x.time=tm.value;const dy=el.querySelector(".nfdays");if(dy)x.days=+dy.value||1});
  const e=$("#nfedit");if(e)c.edit=e.checked?1:0;return c}
function nfSave(){K.store.notif=nfRead();kChanged();fgSchedule();try{if(window.A521&&A521.syncRole)A521.syncRole()}catch(e){}
  if(AR&&kcan){kPublish()}else toast("Pengaturan notifikasi tersimpan di HP ini",1)}
/* Halaman umum: tanda BARU pada kabar/promo yang belum pernah dilihat di HP ini */
function kNewMark(){try{const V=K.posts.filter(p=>!p.draft&&kVis(p)).map(p=>p.id);let seen=null;try{seen=JSON.parse(localStorage.getItem("a521seen")||"null")}catch(e){}
  if(!Array.isArray(seen)){localStorage.setItem("a521seen",JSON.stringify(V));return}
  const N=V.filter(id=>!seen.includes(id));if(!N.length)return;
  N.forEach(id=>document.querySelectorAll(`#pub [data-a="kopen"][data-v="${id}"]`).forEach(el=>{if(!el.querySelector(".k-newb")){el.classList.add("isnew");el.insertAdjacentHTML("afterbegin",'<span class="k-newb">BARU</span>')}}));
  if(!kNewMark.t){kNewMark.t=1;toast(`📣 Ada ${N.length} kabar/promo baru dari ${K.store.name||"521"}`,1)}
  clearTimeout(kNewMark.s);kNewMark.s=setTimeout(()=>{try{localStorage.setItem("a521seen",JSON.stringify([...new Set(seen.concat(N))].slice(-200)))}catch(e){}},6000)}catch(e){}}

/* ---------- Menu ---------- */''')
rep("  galInit();\n}\nfunction galKick", "  galInit();setTimeout(kNewMark,60);\n}\nfunction galKick")
rep('else if(a==="ing")ingSheet(id);', '''else if(a==="ing")ingSheet(id);
  else if(a==="nfsave"&&can("set"))nfSave();
  else if(a==="nfplay"){const el=document.querySelector(`.nfc[data-nfk="${v}"] .nfsnd`);if(window.A521&&A521.native&&A521.playSound)A521.playSound(el?el.value:"ding");else toast("Suara bisa dicoba di aplikasi Android")}''')
rep('document.addEventListener("change",e=>{', 'document.addEventListener("change",e=>{\n  if(e.target.classList&&e.target.classList.contains("nfon")){const c=e.target.closest(".nfc");if(c)c.classList.toggle("off",!e.target.checked)}')

# Jadwal pengingat memakai pengaturan (jam, H-n, suara) + stok bahan menipis
rep('''  if(!window.A521||!A521.notify)return;const items=[];
  D.fg.filter(b=>b.q>0&&fgDays(b)>=1).forEach(b=>{const p=prod(b.p),at=fgD0(b.exp);at.setDate(at.getDate()-1);at.setHours(8,0,0,0);
    items.push({id:"fg-"+b.id+"-"+b.exp,at:at.getTime(),title:"⚠️ Besok kedaluwarsa: "+(p?p.name:b.n),
      body:`${b.q} ${fgUnit(p)} · produksi ${kFmt(b.made)} · kedaluwarsa ${kFmt(b.exp)}. Jual lebih dulu atau tarik dari etalase.`})});
  A521.notify(items)}''', '''  if(!window.A521||!A521.notify)return;const items=[],N=nfCfg(),hm=t=>String(t||"08:00").split(":").map(Number);
  if(N.exp.on){const [H,M]=hm(N.exp.time),dd=+N.exp.days||1;D.fg.filter(b=>b.q>0&&fgDays(b)>=1).forEach(b=>{const p=prod(b.p),at=fgD0(b.exp);at.setDate(at.getDate()-Math.min(dd,Math.max(1,fgDays(b))));at.setHours(H,M||0,0,0);const k=fgDays(b)<=1?1:Math.min(dd,fgDays(b));
    items.push({id:"fg-"+b.id+"-"+b.exp+"-"+dd,at:at.getTime(),type:"exp",snd:N.exp.snd,title:(k<=1?"⚠️ Besok kedaluwarsa: ":`⚠️ ${dd} hari lagi kedaluwarsa: `)+(p?p.name:b.n),
      body:`${b.q} ${fgUnit(p)} · produksi ${kFmt(b.made)} · kedaluwarsa ${kFmt(b.exp)}. Jual lebih dulu atau tarik dari etalase.`})})}
  const low=D.ing.filter(g=>g.min>0&&g.qty<g.min);
  if(N.low.on&&low.length&&me!==undefined){const [H,M]=hm(N.low.time),at=new Date();at.setHours(H,M||0,0,0);const key=low.map(g=>g.id).sort().join(",");
    items.push({id:"low-"+ymd(new Date())+"-"+kHash(key),at:at.getTime(),type:"low",snd:N.low.snd,title:`📦 ${low.length} bahan baku hampir habis`,body:low.slice(0,6).map(g=>g.name).join(", ")+(low.length>6?", …":"")+". Cek tab Stok → Bahan baku."})}
  A521.notify(items)}''')

# Tandai HP staf (untuk penerima notifikasi) saat login + buka tab sesuai notifikasi
rep('function enter(){setTimeout(()=>{', 'function enter(){if(!D.cfg.staffDev){D.cfg.staffDev=1;save()}try{if(window.A521&&A521.syncRole)A521.syncRole()}catch(e){}setTimeout(()=>{')

P.write_text(s)
print("OK, perubahan 04 (Cup/Botol, hapus stok, notifikasi & suara, tanda BARU) diterapkan.")
