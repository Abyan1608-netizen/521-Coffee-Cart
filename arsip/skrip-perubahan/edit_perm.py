s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
# core
rep('const own=()=>me&&me.role==="owner";','''const own=()=>me&&me.role==="owner";
/* Hak akses karyawan: Owner memilih fitur satu per satu. Tim & PIN serta Data & backup selalu khusus Owner. */
const PERMS=[
  ["Kasir","pos",[["pos","Kasir & terima pembayaran","Tambah pesanan, voucher, bayar, cetak struk"],["disc","Beri diskon manual","Ketik potongan harga sendiri di kasir"],["sold","Tandai menu habis / ada lagi","Tombol Habis di kartu menu"],["void","Batalkan transaksi","Membatalkan pesanan yang sudah lunas"]]],
  ["Penjualan","dash",[["dash","Penjualan hari ini","Omzet, pesanan, dan uang yang harus ada di laci"],["dashFull","Ringkasan lengkap","Pilih periode, laba, menu terlaris, per kasir"],["exp","Catat pengeluaran","Mencatat biaya seperti beli susu atau es"]]],
  ["Stok","stk",[["stk","Stok masuk & opname","Lihat stok, tambah stok, hitung ulang"],["stkSet","Atur bahan","Tambah bahan, ubah harga & batas minimum"]]],
  ["Menu & resep","book",[["resep","Lihat buku resep","Takaran dan cara membuat (tanpa mengubah)"],["menu","Kelola menu & resep","Tambah/ubah menu, harga, resep, kategori"]]],
  ["Halaman publik","mega",[["kabar","Kelola Kabar & promo","Tulis kabar, promo, banner, Instagram, opsi pesan"]]],
  ["Pengaturan","set",[["set","Buka Atur","Tampilan, pilihan kasir, QRIS, printer, jam buka. Tim & PIN dan Data & backup tetap khusus Owner."]]]];
const PRESETS={barista:["Barista",["pos","disc","sold","dash","stk","resep"]],kasir:["Kasir",["pos","dash"]],spv:["Supervisor",["pos","disc","sold","void","dash","dashFull","exp","stk","stkSet","resep","menu","kabar"]]};
const permOf=u=>u.role==="owner"?null:Array.isArray(u.perm)?u.perm:PRESETS.barista[1];
const can=k=>!!me&&(me.role==="owner"||permOf(me).includes(k));
const roleName=u=>u.role==="owner"?"Owner":(u.title||"Karyawan");
const permSum=u=>{if(u.role==="owner")return"Akses penuh";const p=permOf(u),all=PERMS.flatMap(g=>g[2]);return p.length?all.filter(x=>p.includes(x[0])).map(x=>x[1]).slice(0,3).join(", ")+(p.length>3?` +${p.length-3} lagi`:""):"Belum ada akses"};''')
# tabs
rep('''const TABS=()=>own()?[["pos","Kasir","pos"],["dash","Ringkasan","dash"],["stk","Stok","stk"],["menu","Menu","menu"],["kabar","Kabar","mega"],["set","Atur","set"]]:[["pos","Kasir","pos"],["dash","Hari ini","today"],["stk","Stok","stk"]];''',
'''const TABS=()=>own()?[["pos","Kasir","pos"],["dash","Ringkasan","dash"],["stk","Stok","stk"],["menu","Menu","menu"],["kabar","Kabar","mega"],["set","Atur","set"]]:[can("pos")&&["pos","Kasir","pos"],(can("dash")||can("dashFull"))&&["dash",can("dashFull")?"Ringkasan":"Hari ini",can("dashFull")?"dash":"today"],can("stk")&&["stk","Stok","stk"],can("menu")?["menu","Menu","menu"]:can("resep")&&["resep","Resep","book"],can("kabar")&&["kabar","Kabar","mega"],can("set")&&["set","Atur","set"]].filter(Boolean);''')
rep('''const T=TABS();if(!T.some(t=>t[0]===tab)&&!(tab==="resep"&&own()))tab="pos";''','''const T=TABS();if(!T.length){$("#nav").innerHTML="";$("#v").innerHTML=`<div class="k-empty" style="margin-top:40px"><b>Belum ada fitur yang dibuka</b>Minta Owner mengatur hak akses akun ${esc(me.name)} di Atur › Tim & PIN.</div>`;return}
  if(!T.some(t=>t[0]===tab)&&!(tab==="resep"&&(can("resep")||can("menu"))))tab=T[0][0];''')
rep('''aria-pressed="${t[0]===tab||(tab==="resep"&&t[0]==="set")}"''','''aria-pressed="${t[0]===tab||(tab==="resep"&&t[0]===(own()||can("set")?"set":"resep"))}"''')
# resep view
rep('''  return `<button class="back" data-a="tab" data-v="set" style="margin-top:18px">← Atur</button>
  <div class="greet" style="margin-top:6px"><div><h2>Buku resep</h2><p>Takaran per cup, cara membuat, dan modal. Terhubung ke tab Menu, stok, dan halaman Kabar.</p></div><button class="btn sm" data-a="newp" style="margin:0">+ Menu & resep baru</button></div>''',
'''  return `${can("set")?`<button class="back" data-a="tab" data-v="set" style="margin-top:18px">← Atur</button>`:""}
  <div class="greet" style="margin-top:6px"><div><h2>Buku resep</h2><p>Takaran per cup, cara membuat, dan modal. Terhubung ke tab Menu, stok, dan halaman Kabar.</p></div>${can("menu")?`<button class="btn sm" data-a="newp" style="margin:0">+ Menu & resep baru</button>`:""}</div>''')
rep('''<button class="btn ghost sm" data-a="edit" data-id="${p.id}" style="margin:0">Ubah resep</button></footer>''','''${can("menu")?`<button class="btn ghost sm" data-a="edit" data-id="${p.id}" style="margin:0">Ubah resep</button>`:""}</footer>''')
# dash
rep('function range(){','function range(){',0) if False else None
rep('  if(!own())return[ymd(new Date()),ymd(new Date())];','  if(!can("dashFull"))return[ymd(new Date()),ymd(new Date())];')
rep('  const r=own()?range():[ymd(new Date()),ymd(new Date())],T=okTx(r)','  const r=can("dashFull")?range():[ymd(new Date()),ymd(new Date())],T=okTx(r)')
rep('''  if(!own()){
    const T=D.tx.filter(t=>t.d===r[0]);''','''  const expBox=`<div class="sec"><h3>Catat pengeluaran</h3><div class="two"><select id="ec" aria-label="Kategori pengeluaran">${C().ec.map(c=>`<option>${esc(c)}</option>`).join("")}</select><input id="ea" inputmode="numeric" placeholder="Nominal (Rp)" aria-label="Nominal"></div><input id="en" placeholder="Catatan, misalnya: beli susu 12 liter" aria-label="Catatan"><button class="btn" data-a="exp">Simpan pengeluaran</button></div>`;
  if(!can("dashFull")){
    const T=D.tx.filter(t=>t.d===r[0]);''')
rep('''<h3>Menu terjual</h3>${bars(desc(pq),v=>v+" cup")}<h3>Transaksi hari ini</h3>${txList(T)}`;''','''<h3>Menu terjual</h3>${bars(desc(pq),v=>v+" cup")}${can("exp")?expBox:""}<h3>Transaksi hari ini</h3>${txList(T)}`;''')
rep('''  <div class="sec"><h3>Catat pengeluaran</h3><div class="two"><select id="ec" aria-label="Kategori pengeluaran">${C().ec.map(c=>`<option>${esc(c)}</option>`).join("")}</select><input id="ea" inputmode="numeric" placeholder="Nominal (Rp)" aria-label="Nominal"></div><input id="en" placeholder="Catatan, misalnya: beli susu 12 liter" aria-label="Catatan"><button class="btn" data-a="exp">Simpan pengeluaran</button></div>
  <h3>Transaksi terbaru</h3>''','''  ${can("exp")?expBox:""}
  <h3>Transaksi terbaru</h3>''')
rep('''${t.status!=="cancelled"&&own()?`<button class="mini" data-a="void"''','''${t.status!=="cancelled"&&can("void")?`<button class="mini" data-a="void"''')
# stock
rep('''  ${own()?`<button class="btn ghost" data-a="newing">+ Tambah bahan</button>`:""}`;''','''  ${can("stkSet")?`<button class="btn ghost" data-a="newing">+ Tambah bahan</button>`:""}`;''')
rep('''  ${own()?`<h3>Pengaturan bahan</h3>''','''  ${can("stkSet")?`<h3>Pengaturan bahan</h3>''')
rep('else if(a==="unit"&&own()){','else if(a==="unit"&&can("stkSet")){')
rep('else if(a==="ingset"&&own()){','else if(a==="ingset"&&can("stkSet")){')
# kasir gates
rep('''`<button class="link" data-a="sdisc">+ Tambah diskon</button>`''','''(can("disc")?`<button class="link" data-a="sdisc">+ Tambah diskon</button>`:"")''')
rep('''<button class="soldb${p.out?" on":""}"''','''${can("sold")?"":"<!--"}<button class="soldb${p.out?" on":""}"''')
rep('''${p.out?"Ada lagi":"Habis"}</button>`}</div>`).join("");''','''${p.out?"Ada lagi":"Habis"}</button>${can("sold")?"":"-->"}`}</div>`).join("");''')
rep('''  else if(a==="sold"){const p=prod(id);''','''  else if(a==="sold"&&!can("sold"))return;
  else if(a==="sdisc"&&!can("disc"))return;
  else if(a==="sold"){const p=prod(id);''')
# post-gate: action → permission map
rep('  else if(!own())return;','''  else if(!own()&&!can(ACT[a]||"_owner"))return;''')
acts={"kabar":"kview kstore kbanner kord kig igdel igsave ordmsgdef ordradd ordrdel ordsadd ordsdel ordsave hbsec hbzoom kbdel kbfirst ksaves knew ked ktog kpdel kpdelgo ksavep kpublish kimgdel kvis kdt kprod kday",
 "stkSet":"newing mking","menu":"edit newp pcol pcat addr rmr saveP togp mv pdel pdelgo","exp":"exp","void":"void vgo",
 "set":"color big qdef qdel lbdel lbfirst lbsec lbzoom uitheme uipub kmode ksamakan bton btoff bttest paper ptest copyx ladd lrm catadd catmv catren catsave catmvdel catdelall catdelallgo catdel"}
m={}
for k,v in acts.items():
    for a in v.split(): m[a]=k
import json
rep("const PRESETS=",f"const ACT={json.dumps(m,separators=(',',':'))};\nconst PRESETS=")
# change handler gates
rep('else if(t.dataset.c&&own()){','else if(t.dataset.c&&can("set")){')
rep('else if(t.id==="lbf"&&t.files&&t.files.length&&own()){','else if(t.id==="lbf"&&t.files&&t.files.length&&can("set")){')
rep('else if(t.dataset.sd!==undefined&&own()){','else if(t.dataset.sd!==undefined&&(can("set")||can("kabar"))){')
rep('else if(t.id==="knote"&&own()){','else if(t.id==="knote"&&can("kabar")){')
rep('else if(t.id==="igf"&&t.files&&t.files.length&&own()){','else if(t.id==="igf"&&t.files&&t.files.length&&can("kabar")){')
rep('else if(t.id==="kbf"&&t.files&&t.files.length&&own()){','else if(t.id==="kbf"&&t.files&&t.files.length&&can("kabar")){')
rep('else if(t.id==="qf"&&t.files&&t.files[0]&&own()){','else if(t.id==="qf"&&t.files&&t.files[0]&&can("set")){')
# settings folders filtered
rep('const F=Object.fromEntries(SETF.map(f=>[f[0],f]));','const F=Object.fromEntries(SETF.map(f=>[f[0],f])),OWNF=["tim","data","log"];')
rep('${setOrder().map(id=>{const f=F[id];return','${setOrder().filter(id=>own()||!OWNF.includes(id)).map(id=>{const f=F[id];return')
rep('if(setSub){const f=SETF.find(x=>x[0]===setSub);','if(setSub&&!own()&&["tim","data","log"].includes(setSub))setSub="";\n  if(setSub){const f=SETF.find(x=>x[0]===setSub);')
# labels
rep('''<small>${u.role==="owner"?"Owner":"Barista"}</small></span></button>`''','''<small>${esc(roleName(u))}</small></span></button>`''')
rep('''<span class="pill ${u.role==="owner"?"own":""}">${u.role==="owner"?"Owner":"Barista"}</span><small class="mute">${u.role==="owner"?"Akses penuh":"Kasir, stok, dan penjualan hari ini"}</small>''','''<span class="pill ${u.role==="owner"?"own":""}">${esc(roleName(u))}</span><small class="mute">${esc(permSum(u))}</small>''')
# user sheet
rep('''  <div class="lbl">Peran</div><div class="chips"><button data-a="urole" data-v="owner" aria-pressed="${u.role==="owner"}">Owner · akses penuh</button><button data-a="urole" data-v="barista" aria-pressed="${u.role==="barista"}">Barista · kasir & stok</button></div>''',
'''  <div class="lbl">Peran</div><div class="chips"><button data-a="urole" data-v="owner" aria-pressed="${u.role==="owner"}">Owner · akses penuh</button><button data-a="urole" data-v="barista" aria-pressed="${u.role!=="owner"}">Karyawan · akses diatur</button></div>
  ${u.role==="owner"?`<p class="note">Owner bisa membuka semua fitur, termasuk Tim & PIN dan Data & backup.</p>`:`<label>Jabatan (tampil di daftar tim & login)<input id="u-title" value="${esc(u.title||"")}" placeholder="Contoh: Barista, Kasir, Supervisor" maxlength="24"></label>
  <div class="lbl">Mulai dari template</div><div class="chips">${Object.entries(PRESETS).map(([k,p])=>`<button data-a="upre" data-v="${k}" aria-pressed="${JSON.stringify([...p[1]].sort())===JSON.stringify([...permOf(u)].sort())}">${p[0]}</button>`).join("")}<button data-a="upre" data-v="none">Kosongkan</button></div>
  <div class="permbox">${PERMS.map(g=>`<div class="permg"><h3>${ic(g[1])}${g[0]}</h3>${g[2].map(x=>`<div class="swrow"><span><b>${x[1]}</b><small>${x[2]}</small></span><label class="tgl" aria-label="${x[1]}"><input type="checkbox" data-pk="${x[0]}" ${permOf(u).includes(x[0])?"checked":""}><span></span></label></div>`).join("")}</div>`).join("")}
  <p class="note">${ic("alert")} Tim & PIN, Data & backup, dan Riwayat perubahan selalu khusus Owner.</p></div>`}''')
rep('''  else if(a==="urole"){eu.name=$("#u-name").value;eu.role=v;usrSheet()}''','''  else if(a==="urole"){uGrab();eu.role=v;usrSheet()}
  else if(a==="upre"){uGrab();eu.perm=v==="none"?[]:[...PRESETS[v][1]];if(v!=="none"&&!eu.title)eu.title=PRESETS[v][0];usrSheet()}''')
rep('''    const nm=$("#u-name").value.trim(),p=$("#u-pin").value;''','''    uGrab();const nm=$("#u-name").value.trim(),p=$("#u-pin").value;
    if(eu.role!=="owner"&&!["pos","dash","dashFull","stk","resep","menu","kabar","set"].some(k=>eu.perm.includes(k))){toast("Pilih minimal satu fitur supaya akun ini bisa dipakai");return}''')
rep('''    if(eu.isNew){D.users.push({id:"u"+uid(),name:nm,role:eu.role,pin:p});lg("Anggota tim baru",nm)}''','''    const ext=eu.role==="owner"?{}:{perm:[...eu.perm],title:eu.title||""};
    if(eu.isNew){D.users.push(Object.assign({id:"u"+uid(),name:nm,role:eu.role,pin:p},ext));lg("Anggota tim baru",nm)}''')
rep('''      u.name=nm;u.role=eu.role;if(p){''','''      u.name=nm;u.role=eu.role;if(u.role==="owner"){delete u.perm;delete u.title}else{const was=JSON.stringify(permOf(u));Object.assign(u,ext);if(was!==JSON.stringify(u.perm))lg("Ubah hak akses",nm+": "+permSum(u))}if(p){''')
rep('''  else if(a==="newu"){eu={isNew:1,name:"",role:"barista",pin:""};usrSheet()}''','''  else if(a==="newu"){eu={isNew:1,name:"",role:"barista",pin:"",title:"Barista",perm:[...PRESETS.barista[1]]};usrSheet()}''')
rep('''  else if(a==="usr"){const u=D.users.find(x=>x.id===id);if(u){eu=Object.assign({},u);usrSheet()}}''','''  else if(a==="usr"){const u=D.users.find(x=>x.id===id);if(u){eu=Object.assign({},u);if(u.role!=="owner")eu.perm=[...permOf(u)],eu.title=u.title||"Barista";usrSheet()}}''')
rep("function usrSheet(){","""function uGrab(){const n=$("#u-name");if(n)eu.name=n.value;const t=$("#u-title");if(t)eu.title=t.value.trim();const b=document.querySelectorAll("[data-pk]");if(b.length)eu.perm=[...b].filter(x=>x.checked).map(x=>x.dataset.pk);if(!eu.perm)eu.perm=[...PRESETS.barista[1]]}
function usrSheet(){""")
# live preset highlight when toggling
rep('document.addEventListener("change",e=>{','''document.addEventListener("change",e=>{
  if(e.target.dataset&&e.target.dataset.pk!==undefined&&eu){const k=e.target.dataset.pk,on=e.target.checked;uGrab();const P=new Set(eu.perm);
    if(on&&k==="dashFull")P.add("dash");if(on&&k==="menu")P.add("resep");if(on&&k==="stkSet")P.add("stk");if(on&&(k==="disc"||k==="sold"||k==="void"))P.add("pos");
    if(!on&&k==="pos"){P.delete("disc");P.delete("sold")}if(!on&&k==="stk")P.delete("stkSet");
    eu.perm=[...P];const st=$(".sheet").scrollTop;usrSheet();$(".sheet").scrollTop=st;return}''')
css='''/* ---------- Hak akses ---------- */
.permbox{margin-top:6px}
.permg{background:var(--sf2);border:1px solid var(--line);border-radius:16px;padding:2px 14px;margin:10px 0}
.permg h3{display:flex;align-items:center;gap:8px;margin:12px 0 2px}
.permg h3 svg{width:16px;height:16px;color:var(--ac)}
.permg .swrow:last-child{border-bottom:0}
.permg .swrow small{font-size:12px}
'''
i=s.index("/* ---------- Welcome ---------- */");s=s[:i]+css+s[i:]
open('p3.src.html','w').write(s);print("ok")
