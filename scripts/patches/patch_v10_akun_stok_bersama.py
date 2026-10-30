"""Perubahan 10: tanpa kode tim — masuk dengan nama & PIN; stok sama di semua HP; penjualan masuk ke Owner lewat server;
peran Owner/Barista/Reseller; tombol Cup/Botol tanpa ikon. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V10-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


# ------------------------------------------------------------------ CSS
rep(".posv{margin:4px 0 12px}.posv button{display:flex;align-items:center;justify-content:center;gap:6px}\n.posv small{font-size:11px;opacity:.8;font-weight:600}",
    """/*V10-PATCH*/
.posv{margin:4px 0 12px}.posv button{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px;padding:12px 10px 11px;min-height:68px}
.posv b{font:800 24px/1.05 var(--f-b);letter-spacing:-.01em}
.posv small{font-size:12px;opacity:.82;font-weight:600;line-height:1.2}
.tjoin.acct{display:flex;flex-direction:column;gap:6px;text-align:left}
.tjoin.acct label{margin:4px 0 0}.tjoin.acct .btn{margin-top:6px}
.tjoin.acct .lerr{min-height:0;margin:2px 0 0}
.aclnk{display:block;margin:10px auto 0;background:none;border:0;color:var(--mute);font:600 13px var(--f-b);text-decoration:underline;text-underline-offset:3px;padding:6px}
.rolec{display:grid;grid-template-columns:repeat(3,1fr);gap:8px}.rolec button{margin:0;padding:11px 6px;border-radius:14px;border:1px solid var(--line);background:var(--sf);color:var(--ink);font:700 14px var(--f-b);display:flex;flex-direction:column;align-items:center;gap:2px}
.rolec button small{font:600 11px var(--f-b);color:var(--mute)}
.rolec button[aria-pressed=true]{background:var(--ac);color:var(--on);border-color:transparent}.rolec button[aria-pressed=true] small{color:inherit;opacity:.85}
""")

# ------------------------------------------------------------------ Tombol Cup / Botol: tanpa ikon, tulisan besar
rep('aria-pressed="${posV==="cup"}">☕ Cup <small>dibuat saat dipesan</small></button>',
    'aria-pressed="${posV==="cup"}"><b>Cup</b><small>dibuat saat dipesan</small></button>')
rep('aria-pressed="${posV==="botol"}">🧴 Botol <small>dari stok</small></button>',
    'aria-pressed="${posV==="botol"}"><b>Botol</b><small>dari stok</small></button>')

# ------------------------------------------------------------------ simpan → sinkron otomatis
rep('if(typeof menuAuto==="function")menuAuto();if(typeof memCast==="function")memCast()};',
    'if(typeof menuAuto==="function")menuAuto();if(typeof memCast==="function")memCast();if(typeof syncHook==="function")syncHook()};')

# ------------------------------------------------------------------ Peran: Owner / Barista / Reseller
rep('const PRESETS={barista:["Barista",["pos","disc","sold","dash","stk","resep","subUse"]],',
    'const PRESETS={barista:["Barista",["pos","disc","sold","dash","stk","resep","subUse"]],reseller:["Reseller",["pos","dash"]],')
rep('''<div class="lbl">Peran</div><div class="chips"><button data-a="urole" data-v="owner" aria-pressed="${u.role==="owner"}">Owner · akses penuh</button><button data-a="urole" data-v="barista" aria-pressed="${u.role!=="owner"}">Karyawan · akses diatur</button></div>''',
    '''<div class="lbl">Peran</div><div class="rolec"><button data-a="urole" data-v="owner" aria-pressed="${u.role==="owner"}">Owner<small>akses penuh</small></button><button data-a="urole" data-v="barista" aria-pressed="${u.role!=="owner"&&!isResU(u)}">Barista<small>akses diatur</small></button><button data-a="urole" data-v="reseller" aria-pressed="${u.role!=="owner"&&isResU(u)}">Reseller<small>akses diatur</small></button></div>''')
rep('''<label>Jabatan (tampil di daftar tim & login)<input id="u-title" value="${esc(u.title||"")}" placeholder="Contoh: Barista, Kasir, Supervisor" maxlength="24"></label>
  <div class="lbl">Mulai dari template</div>''',
    '''<p class="note" style="margin-top:8px">Nyalakan fitur yang boleh dipakai <b>${esc(u.title||(isResU(u)?"Reseller":"Barista"))}</b> di bawah. Fitur yang mati tidak muncul di HP-nya.</p>
  <label>Nama jabatan (tampil di daftar tim & login)<input id="u-title" value="${esc(u.title||"")}" placeholder="Contoh: Barista, Reseller, Kasir" maxlength="24"></label>
  <div class="lbl">Isi cepat</div>''')
rep('else if(a==="urole"){uGrab();eu.role=v;usrSheet()}',
    '''else if(a==="urole"){uGrab();if(v==="owner")eu.role="owner";else{const P=PRESETS[v]||PRESETS.barista,was=eu.role==="owner"?"":(isResU(eu)?"reseller":"barista");eu.role="barista";
    if(was!==v){eu.title=P[0];eu.perm=[...P[1]]}}usrSheet()}''')
# nama akun harus unik (dipakai untuk masuk di HP lain)
rep('    if(!nm){$("#u-name").focus();return}\n',
    '''    if(!nm){$("#u-name").focus();return}
    if(D.users.some(x=>x.id!==eu.id&&x.name.trim().toLowerCase().replace(/\\s+/g," ")===nm.toLowerCase().replace(/\\s+/g," "))){toast("Nama ini sudah dipakai akun lain. Pakai nama berbeda supaya bisa masuk di HP lain.");$("#u-name").focus();return}
''')
rep('save();pinMigrate().catch(()=>{});shut();toast(nm+" tersimpan",1);',
    'save();pinMigrate().then(()=>acctAuto()).catch(()=>{});shut();toast(isHub()?nm+" tersimpan. Bisa masuk di HP mana pun dengan nama & PIN ini.":nm+" tersimpan",1);')
# hapus anggota → kunci tim diganti otomatis (HP orang itu langsung terputus)
rep('else if(a==="udgo"){const u=D.users.find(x=>x.id===id);if(!u)return;D.users=D.users.filter(x=>x.id!==u.id);lg("Hapus anggota tim",u.name);save();shut();toast(u.name+" dihapus dari tim",1)}',
    'else if(a==="udgo"){const u=D.users.find(x=>x.id===id);if(!u)return;D.users=D.users.filter(x=>x.id!==u.id);lg("Hapus anggota tim",u.name);const rot=teamRotate();save();shut();toast(rot?u.name+" dihapus. HP-nya langsung terputus dari tim.":u.name+" dihapus dari tim",1)}')
rep('"Akun ini tidak bisa masuk lagi. Riwayat transaksinya tetap tersimpan."',
    '(isHub()?"Akun ini tidak bisa masuk lagi dan HP-nya langsung terputus dari tim. HP anggota lain tersambung lagi otomatis saat memasukkan PIN. Riwayat transaksinya tetap tersimpan.":"Akun ini tidak bisa masuk lagi. Riwayat transaksinya tetap tersimpan.")')

# ------------------------------------------------------------------ Halaman masuk
rep('''function teamJoinCard(){
  if(!K.team)return"";''', '''function teamJoinCard(){
  if(acMode())return acctCard();
  if(!K.team)return"";''')
rep('''<small>Masukkan kode tim dari Owner sekali saja. Setelah itu menu, resep, akun, dan PIN ikut terbarui otomatis.</small><div class="add"><input id="tcode" placeholder="521-XXXXX-XXXXX" autocapitalize="characters" autocomplete="off" spellcheck="false" aria-label="Kode tim"><button class="btn sm" data-a="tjoin" style="margin:0">Sambungkan</button></div></div>`;''',
    '''<small>Masuk dengan nama & PIN dari Owner. Setelah itu menu, resep, akun, dan stok ikut terbarui otomatis.</small><button class="btn sm" data-a="acshow" style="margin:6px 0 0">Masuk dengan nama & PIN</button></div>`;''')
rep('''  $("#lgreet").textContent=greet();const tj=$("#tjoin");if(tj)tj.innerHTML=teamJoinCard();''',
    '''  $("#lgreet").textContent=greet();const tj=$("#tjoin");{const an=($("#acn")||{}).value,ap=($("#acp")||{}).value,af=(document.activeElement||{}).id;if(tj)tj.innerHTML=teamJoinCard();if(an&&$("#acn"))$("#acn").value=an;if(ap&&$("#acp"))$("#acp").value=ap;if(/^ac[np]$/.test(af||"")&&$("#"+af))$("#"+af).focus()}
  {const ac=acMode();["#ulist","#lpw","#peek","#lerr","#pad"].forEach(x=>{const e=$(x);if(e)e.hidden=ac});const pw=document.querySelector("#login .pw");if(pw)pw.hidden=ac;
   const sb=document.querySelector("#login .sub");if(sb)sb.textContent=ac?"Masuk dengan nama & PIN yang dibuat Owner.":"Pilih akun, lalu masukkan PIN atau kata sandi.";
   if(ac){const h0=$("#hint");if(h0)h0.hidden=true;return}}''')
rep('''if(okp){lkSet({n:0,u:0});lgPrev="";me=u;buf="";peek=false;$("#lerr").textContent="";try{sessionStorage.setItem("pos521u",u.id)}catch(e){}enter();''',
    '''if(okp){lkSet({n:0,u:0});lgPrev="";me=u;buf="";peek=false;$("#lerr").textContent="";try{sessionStorage.setItem("pos521u",u.id)}catch(e){}enter();if(teamBad)acctHeal(u);''')
rep('  if(a==="tjoin"){teamJoin();return}',
    '''  if(a==="tjoin"){teamJoin();return}
  if(a==="acgo"){acctLogin();return}
  if(a==="acshow"){acForce=true;loginView();return}
  if(a==="acloc"){acLocal=true;acForce=false;loginView();return}
  if(a==="acback"){acLocal=false;loginView();return}
  if(a==="orec"){ownerRecover();return}''')
rep('  if(a==="forgot"){forgotSheet();return}', '  if(a==="forgot"){if(acMode())acForgotSheet();else forgotSheet();return}')
# HP Owner mengunggah akun baru setelah PIN Owner diatur ulang
rep('''lkSet({n:0,u:0});lsel=u.id;D.log.push({at:iso(),a:"Atur ulang PIN Owner",d:u.name+" (dengan Kunci Owner)",by:"Sistem"});
  try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}shut();loginView();''',
    '''lkSet({n:0,u:0});lsel=u.id;D.log.push({at:iso(),a:"Atur ulang PIN Owner",d:u.name+" (dengan Kunci Owner)",by:"Sistem"});
  try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}kcan=true;acLocal=true;acctAuto();shut();loginView();''')

# reseller: saluran "Reseller" otomatis (harga reseller), HP Owner menyiapkan akun tim
rep('''$("#login").hidden=true;$("#pub").hidden=true;$("#app").hidden=false;$("#wav").textContent=ini(me.name);$("#wnm").textContent=me.name;tab="pos";''',
    '''$("#login").hidden=true;$("#pub").hidden=true;$("#app").hidden=false;$("#wav").textContent=ini(me.name);$("#wnm").textContent=me.name;tab="pos";
  if(me.role!=="owner"&&isResU(me)){const rc=C().ch.find(c=>/reseller/i.test(c));if(rc)ch=rc}
  if(D.cfg.lastRole!==me.role){D.cfg.lastRole=me.role;try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}}
  setTimeout(acctBoot,1200);''')

# ------------------------------------------------------------------ Sinkron data tim (bundle)
rep('''  catch(e){teamBad=true;if(!$("#login").hidden)loginView()}
  teamReady=true;
}''', '''  catch(e){teamBad=true;if(me)acctHeal(me);else if(!$("#login").hidden)loginView()}
  teamReady=true;
}''')
rep('''  Object.keys(cart).forEach(k=>{if(!cp(k))delete cart[k]});
  try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}look();
}''', '''  Object.keys(cart).forEach(k=>{if(!cp(k))delete cart[k]});
  try{if(typeof stApply==="function")stApply()}catch(e){}
  try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}look();
}''')
rep('const teamDirty=()=>!!(C().teamCode&&teamSrc()&&(teamSig()!==((K.team||{}).sig)||memDirty()));',
    'const teamDirty=()=>!!(C().teamCode&&teamSrc()&&(teamSig()!==((K.team||{}).sig)||memDirty()||C().tforce));')
rep('await AR.publish(kDoc(pub));PUBK=pub;K_BASE=nb;memForce=0;msMemAt=Date.now();if(pub.team){D.cfg.teamRev=pub.team.rev;',
    'await AR.publish(kDoc(pub));PUBK=pub;K_BASE=nb;memForce=0;msMemAt=Date.now();if(pub.team){D.cfg.teamRev=pub.team.rev;delete D.cfg.tforce;')
rep('try{await AR.publish(kDoc());try{sessionStorage.removeItem("k521-pending")}catch(e){}kdirty=false;PUBK=JSON.parse(JSON.stringify(K));K_BASE=kHash(JSON.stringify(K));if(K.team&&C().teamCode){D.cfg.teamRev=K.team.rev;',
    'try{await AR.publish(kDoc());try{sessionStorage.removeItem("k521-pending")}catch(e){}kdirty=false;PUBK=JSON.parse(JSON.stringify(K));K_BASE=kHash(JSON.stringify(K));if(K.team&&C().teamCode){D.cfg.teamRev=K.team.rev;delete D.cfg.tforce;')

# Atur → Sinkron: tanpa kode tim
rep('''  ["sinkron","phone","Sinkron semua HP",()=>!K.team?"Belum aktif · menu & akun hanya di HP ini":C().teamCode&&teamSrc()?(teamDirty()?"Ada perubahan, sedang dikirim…":"Aktif · semua HP tim memakai data ini"):"Masukkan kode tim untuk tersambung"],''',
    '''  ["sinkron","phone","Sinkron semua HP",()=>syncSum()],''')
i = s.find('if(id==="sinkron"){const T=K.team,src=teamSrc();')
j = s.find('if(id==="chat")', i)
assert i > 0 and j > i
s = s[:i] + 'if(id==="sinkron")return syncView();\n  ' + s[j:]
rep('''else if(a==="tson"&&own()){if(!AR||!kcan)return;D.cfg.teamCode=genCode();lg("Sinkron tim","Diaktifkan");save();render();toast("Kode tim dibuat. Mengirim data ke semua HP…",1);menuAuto(0)}''',
    '''else if(a==="tson"&&own()){if(!AR||!kcan)return;D.cfg.teamCode=genCode();lg("Sinkron tim","Diaktifkan");save();render();toast("Akun tim aktif. Mengirim data ke semua HP…",1);menuAuto(0)}''')
rep('''else if(a==="tnew"&&own()){confirmSheet("Buat kode tim baru?","Kode lama berhenti berlaku. Semua HP karyawan perlu memasukkan kode baru sekali lagi.","tnewgo","Buat kode baru","Batal","x")}''',
    '''else if(a==="tnew"&&own()){confirmSheet("Putuskan semua HP lain?","Pakai ini bila ada HP hilang atau dipinjam orang. Semua HP lain langsung terputus dari tim. Anggota tim tersambung lagi cukup dengan memasukkan nama & PIN mereka.","tnewgo","Putuskan semua HP","Batal","x")}''')
rep('''else if(a==="tnewgo"&&own()){D.cfg.teamCode=genCode();D.cfg.teamRev=0;lg("Sinkron tim","Kode baru dibuat");save();shut();render();menuAuto(0);toast("Kode baru dibuat. Bagikan ke tim.",1)}''',
    '''else if(a==="tnewgo"&&own()){if(!teamRotate())return;lg("Sinkron tim","Semua HP lain diputus");save();shut();render();toast("Semua HP lain terputus. Anggota tim masuk lagi dengan nama & PIN.",1)}''')
rep('''else if(a==="tcopy"&&own()){const t=`Aplikasi 521 Coffee Cart: ${C().promo||location.href}\\nKode tim: ${C().teamCode}\\nBuka link → Masuk → isi kode tim → login dengan PIN masing-masing.`;try{navigator.clipboard.writeText(t).then(()=>toast("Kode + link tersalin",1),()=>toast(C().teamCode))}catch(e){toast(C().teamCode)}}''',
    '''else if(a==="tcopy"&&own()){const t=`Pasang aplikasi 521 Coffee App: ${C().promo||location.href}\\nBuka aplikasinya → Masuk → isi nama & PIN dari Owner. HP langsung tersambung ke tim.`;try{navigator.share({text:t}).catch(()=>{})}catch(e){try{navigator.clipboard.writeText(t).then(()=>toast("Cara masuk tersalin",1))}catch(x){}}}''')

# ------------------------------------------------------------------ Transaksi antar-HP lewat server (antrean)
rep('''async function rtSend(){
  if(!RM||isHub())return;
  try{const Q=myQueue();if(!Q.length||!C().teamCode){''', '''async function rtSend(){
  logAuto(400);
  if(!RM||isHub())return;
  try{const Q=myQueue();if(!Q.length||!C().teamCode||stOn()){''')
rep('''try{if(!window.claude||!claude.use)return;RM=await claude.use("room");if(!RM)return;memListen();''',
    '''try{if(!window.claude||!claude.use)return;RM=await claude.use("room");if(!RM)return;memListen();
    RM.on("_stk",m=>{const d=m.data||{};if(d.dev!==DEV)stAuto(150)});
    RM.onPeers(ch=>{if((ch.joined||[]).some(p=>p.isMe)){syncKick();setTimeout(()=>{if(!stOn())return;RM.emit("_stk",{dev:DEV}).catch(()=>{});RM.emit("_log",{dev:DEV}).catch(()=>{})},2500)}});RM.on("_log",m=>{const d=m.data||{};if(d.dev!==DEV)logAuto(300)});''')
rep('if(!C().teamCode){toast("Sambungkan HP ini ke tim dulu (kode tim dari Owner).");return}',
    'if(!C().teamCode){toast("Masuk dengan akun tim dulu (nama & PIN dari Owner).");return}')
rep('''${RM&&isHub()?`<p class="rtl" id="rtlive"><i></i>${rtLiveTxt()}</p>`:`<p class="note">HP yang belum tersambung langsung ke HP Owner mengirim lewat laporan WhatsApp. Tempel laporannya di sini.</p>`}''',
    '''${stOn()?`<p class="rtl" id="rtlive"><i></i>Penjualan & pengeluaran dari semua HP tim masuk otomatis ke sini lewat server, walau HP ini sempat mati atau offline.</p>`:RM&&isHub()?`<p class="rtl" id="rtlive"><i></i>${rtLiveTxt()}</p>`:`<p class="note">HP yang belum tersambung langsung ke HP Owner mengirim lewat laporan WhatsApp. Tempel laporannya di sini.</p>`}''')
rep('''${C().teamCode?"":'<p class="note">Aktifkan Atur › Sinkron semua HP dulu supaya laporan bisa dikirim & dibuka.</p>'}</div>`}''',
    '''${C().teamCode?"":'<p class="note">Masuk dengan akun tim dulu supaya laporan bisa dikirim & dibuka.</p>'}</div>`}''')
rep('''return `<div class="sec ttx"><h3>Kirim ke Owner</h3>${!C().teamCode?'<p class="note">Sambungkan HP ini ke tim (kode tim dari Owner) supaya transaksi bisa dikirim.</p>':RM?''',
    '''return `<div class="sec ttx"><h3>Kirim ke Owner</h3>${!C().teamCode?'<p class="note">Masuk dengan akun tim (nama & PIN dari Owner) supaya transaksi bisa dikirim.</p>':stOn()?`<p class="rtl${Q?" wait":""}"><i></i>${Q?`${Q} transaksi menunggu internet, terkirim otomatis`:"Semua transaksi sudah terkirim ke Owner"}</p>`:RM?''')

# ------------------------------------------------------------------ Stok: setiap perubahan dicatat sebagai operasi bersama
rep('function applyUse(tx,s,type){if(s>0&&Array.isArray(tx.fgu)&&tx.fgu.length)fgBack(tx);Object.entries(tx.use).forEach(([i,qq])=>{const g=ing(i);if(!g)return;g.qty+=s*qq;D.mv.push({at:iso(),i,type,q:s*qq,cost:g.cost,sup:"",ref:tx.no})})}',
    'function applyUse(tx,s,type){if(s>0&&Array.isArray(tx.fgu)&&tx.fgu.length)fgBack(tx);Object.entries(tx.use).forEach(([i,qq])=>{const g=ing(i);if(!g)return;g.qty+=s*qq;mvPush({at:iso(),i,type,q:s*qq,cost:g.cost,sup:"",ref:tx.no})})}')
rep('''b.q-=t;need-=t;out.push({b:b.id,q:t,p:b.p});
    D.mv.push({at:iso(),i:"fg:"+b.p,type:"fg-jual",q:-t,cost:0,sup:"",ref})''',
    '''b.q-=t;need-=t;out.push({b:b.id,q:t,p:b.p});
    mvPush({at:iso(),i:"fg:"+b.p,b:b.id,type:"fg-jual",q:-t,cost:0,sup:"",ref})''')
rep('b.q+=u.q;D.mv.push({at:iso(),i:"fg:"+u.p,type:"fg-batal",q:u.q,cost:0,sup:"",ref:tx.no})',
    'b.q+=u.q;mvPush({at:iso(),i:"fg:"+u.p,b:b.id,type:"fg-batal",q:u.q,cost:0,sup:"",ref:tx.no})')
rep('''D.fg.push(b);p.fgOn=1;p.shelf=sh;p.fgu=u;
  D.mv.push({at:iso(),i:"fg:"+p.id,type:"fg-masuk",q,cost:0,sup:"",ref:"produksi "+m});''',
    '''D.fg.push(b);p.fgOn=1;p.shelf=sh;p.fgu=u;b.u=u;
  mvPush({at:iso(),i:"fg:"+p.id,nb:b,type:"fg-masuk",q,cost:0,sup:"",ref:"produksi "+m});''')
rep('const used=r.q*q*(+p.bfac||1);g.qty-=used;D.mv.push({at:iso(),i:g.id,type:"produksi",',
    'const used=r.q*q*(+p.bfac||1);g.qty-=used;mvPush({at:iso(),i:g.id,type:"produksi",')
rep('b.q-=k;D.mv.push({at:iso(),i:"fg:"+b.p,type:"fg-keluar",q:-k,cost:0,sup:"",ref:fgRR});',
    'b.q-=k;mvPush({at:iso(),i:"fg:"+b.p,b:b.id,type:"fg-keluar",q:-k,cost:0,sup:"",ref:fgRR});')
rep('X.forEach(b=>{t+=b.q;D.mv.push({at:iso(),i:"fg:"+b.p,type:"fg-keluar",q:-b.q,cost:0,sup:"",ref:"Kedaluwarsa, dibuang"});b.q=0});',
    'X.forEach(b=>{t+=b.q;mvPush({at:iso(),i:"fg:"+b.p,b:b.id,type:"fg-keluar",q:-b.q,cost:0,sup:"",ref:"Kedaluwarsa, dibuang"});b.q=0});')
rep('D.fg=D.fg.filter(x=>x.id!==id2);D.mv.push({at:iso(),i:"fg:"+b.p,type:"fg-hapus",q:-b.q,cost:0,sup:"",ref:"hapus batch "+b.made});',
    'D.fg=D.fg.filter(x=>x.id!==id2);mvPush({at:iso(),i:"fg:"+b.p,del:b.id,type:"fg-hapus",q:-b.q,cost:0,sup:"",ref:"hapus batch "+b.made});')
rep('B.forEach(b=>{if(b.q>0)D.mv.push({at:iso(),i:"fg:"+id2,type:"fg-hapus",q:-b.q,cost:0,sup:"",ref:"hapus dari daftar"})});',
    'B.forEach(b=>{mvPush({at:iso(),i:"fg:"+id2,del:b.id,type:"fg-hapus",q:-b.q,cost:0,sup:"",ref:"hapus dari daftar"})});')
rep('g.qty+=qq;D.mv.push({at:iso(),i:g.id,type:"in",q:qq,',
    'g.qty+=qq;mvPush({at:iso(),i:g.id,type:"in",q:qq,')
rep('g.qty=x;D.mv.push({at:iso(),i:g.id,type:"opname",q:d,cost:g.cost,sup:"",ref:""});',
    'g.qty=x;mvPush({at:iso(),i:g.id,type:"opname",q:d,set:x,cost:g.cost,sup:"",ref:""});')

rep('t.status="cancelled";t.reason=r;if(!t.rx)applyUse(t,1,"void");',
    't.status="cancelled";t.reason=r;if(!t.rx||(stOn()&&t.use))applyUse(t,1,"void");')
rep('Object.entries(tx.use).forEach(([i,qq])=>{const g=ing(i);if(!g)return;g.qty+=s*qq;mvPush(', 'Object.entries(tx.use||{}).forEach(([i,qq])=>{const g=ing(i);if(!g)return;g.qty+=s*qq;mvPush(')

# ------------------------------------------------------------------ Blok baru
NEW = r'''
/* ===== Akun tim & sinkron otomatis (tanpa kode tim) =====
   Owner membuat akun di Atur → Tim & PIN (Owner / Barista / Reseller). HP Owner mengunggah daftar akun ke server
   (nama + pemeriksa PIN, bukan PIN). HP lain cukup masuk dengan nama & PIN: server memeriksanya lalu memberi kunci tim
   yang dipakai diam-diam untuk sinkron. Menghapus anggota mengganti kunci tim, jadi HP orang itu langsung terputus.
   Stok bahan baku & produk jadi dipegang server sehingga angkanya sama di semua HP. Penjualan, pengeluaran, dan
   langganan dari HP mana pun dititipkan ke server (terenkripsi kunci tim) dan diambil HP Owner kapan pun ia online. */
const SRVU=()=>(window.A521&&A521.server)||"";
let acctOn=null,acForce=false,acLocal=false,acBusy=false;
const isResU=u=>!!u&&u.role!=="owner"&&/reseller/i.test(u.title||"");
const acMode=()=>!!(SRVU()&&!acLocal&&(acForce||((!C().teamCode||teamBad)&&acctOn!==false)));
async function api(path,o){o=o||{};const h=Object.assign({},o.h||{});if(o.body!==undefined)h["Content-Type"]="application/json";
  const r=await fetch(SRVU()+path,{method:o.m||"GET",headers:h,body:o.body!==undefined?JSON.stringify(o.body):undefined,cache:"no-store"});
  let j=null;if(r.status!==204){try{j=await r.json()}catch(e){}}return{s:r.status,j}}
let RID="",RIDc="";
async function ridNow(){const c=C().teamCode;if(!c)return"";if(RIDc!==c){RID=(await sha256h("521room|"+String(c).trim().toUpperCase())).slice(0,40);RIDc=c}return RID}
const okey=()=>{try{return localStorage.getItem("a521owner")||""}catch(e){return""}};
async function acctCheck(){if(!SRVU())return;try{const r=await api("/acct/on");if(r.s===200&&r.j){const was=acctOn;acctOn=!!r.j.on;if(was!==acctOn&&!me&&!$("#login").hidden)loginView()}}catch(e){}}
function acctCard(){const bad=teamBad&&C().teamCode;
  return `<div class="tjoin acct"><b>${bad?"Masuk lagi ke tim 521":"Masuk ke tim 521"}</b><small>${bad?"Akses tim diperbarui Owner. Masuk sekali lagi dengan nama & PIN.":"Setelah masuk, HP ini otomatis tersambung: menu, akun, dan stok sama dengan HP Owner. Tidak perlu kode tim."}</small>
  <label>Nama akun<input id="acn" autocomplete="username" autocapitalize="words" spellcheck="false" maxlength="40" placeholder="Contoh: Raka" enterkeyhint="next"></label>
  <label>PIN atau kata sandi<input id="acp" type="password" autocomplete="current-password" autocapitalize="off" spellcheck="false" maxlength="32" enterkeyhint="go"></label>
  <p class="lerr" id="acerr" role="alert"></p><button class="btn" data-a="acgo">Masuk</button>
  ${acForce?`<button class="aclnk" data-a="acloc" type="button">Kembali ke daftar akun di HP ini</button>`:""}</div>`}
document.addEventListener("keydown",e=>{if(e.key!=="Enter")return;const t=e.target;if(t&&t.id==="acn"){e.preventDefault();const p=$("#acp");if(p)p.focus()}else if(t&&t.id==="acp"){e.preventDefault();acctLogin()}});
/* Masuk ke server dengan bukti PIN (hash PBKDF2 di HP; PIN asli tidak pernah dikirim) */
async function acctJoin(code,team){
  if(team)K.team=team;if(!K.team)throw Object.assign(new Error("noteam"),{code:"noteam"});
  const T=await teamOpen(code,K.team);D.cfg.teamCode=code;ZK=null;RIDc="";teamApply(T,K.team);teamBad=false;teamReady=true;acForce=false;
  try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}syncKick()}
/* Akun baru dibuat Owner beberapa detik lalu: tunggu data tim terbaru dari HP Owner (maks ±30 detik) */
async function teamFresh(code){try{const r=await api("/k?since=0");const T=r.j&&r.j.k&&r.j.k.team;if(r.s===200&&T&&(!K.team||T.rev>K.team.rev)){K.team=T;teamApply(await teamOpen(code,T),T);return true}}catch(e){}return false}
async function acctLogin(){
  if(acBusy)return;const n=(($("#acn")||{}).value||"").trim(),p=($("#acp")||{}).value||"",er=$("#acerr"),say=t=>{if(er)er.textContent=t};
  if(!n){$("#acn").focus();say("Isi nama akun dulu.");return}if(p.length<4){$("#acp").focus();say("Isi PIN atau kata sandi (minimal 4 karakter).");return}
  if(looksKey(p)&&p.length>=24){say("Itu seperti Kunci Owner, bukan PIN. Isi PIN akun Anda.");return}
  acBusy=true;const b=$("[data-a=acgo]");if(b){b.disabled=true;b.textContent="Memeriksa…"}
  try{
    const r1=await api("/login",{m:"POST",body:{name:n}});
    if(r1.s===404){say("Nama ini belum terdaftar. Cek ejaannya, atau minta Owner membuat akun di Atur → Tim & PIN.");return}
    if(r1.s===409){acctOn=false;say("Akun tim belum aktif. Minta Owner membuka aplikasi versi terbaru di HP Owner sebentar.");return}
    if(r1.s===429){say("Terlalu banyak percobaan dari jaringan ini. Tunggu 1 menit.");return}
    if(r1.s!==200||!r1.j||!r1.j.id){say("Server belum bisa dihubungi. Pastikan ada internet, lalu coba lagi.");return}
    const d=await pwDer(r1.j.id,p,b64u8(r1.j.s));
    const r2=await api("/login",{m:"POST",body:{id:r1.j.id,d}});
    if(r2.s===423){const w=Math.ceil(((r2.j&&r2.j.wait)||30000)/1000);say(`Terlalu sering salah. Coba lagi dalam ${w>90?Math.ceil(w/60)+" menit":w+" detik"}.`);return}
    if(r2.s===401){say("PIN atau kata sandi belum cocok.");$("#acp").value="";$("#acp").focus();return}
    if(r2.s===429){say("Terlalu banyak percobaan dari jaringan ini. Tunggu 1 menit.");return}
    if(r2.s!==200||!r2.j||!r2.j.code){say("Belum berhasil masuk. Coba lagi sebentar.");return}
    try{await acctJoin(r2.j.code,r2.j.team)}catch(e){say(e&&e.code==="noteam"?"Data tim belum diterbitkan Owner. Minta Owner membuka aplikasi sebentar.":"Data tim belum bisa dibuka. Minta Owner membuka aplikasi sebentar, lalu coba lagi.");return}
    let u=D.users.find(x=>x.id===r2.j.id);
    for(let i=0;!u&&i<10;i++){say("Menyiapkan akun di HP ini…");await new Promise(r=>setTimeout(r,3000));await teamFresh(r2.j.code);u=D.users.find(x=>x.id===r2.j.id)}
    if(!u){say("Akun ini belum ada di data tim terbaru. Minta Owner membuka aplikasi sebentar, lalu coba lagi.");return}say("");
    lkSet({n:0,u:0});me=u;lsel=u.id;buf="";try{sessionStorage.setItem("pos521u",u.id)}catch(e){}
    enter();toast(`Halo ${u.name}! HP ini sudah tersambung ke tim 521`,1);syncKick();
    if(/^(1234|0000)$/.test(p))setTimeout(()=>{openUsr(u.id,1);toast("Demi keamanan, ganti PIN awal ini dulu ya")},450);
  }catch(e){say("Belum berhasil masuk. Periksa internet lalu coba lagi.")}
  finally{acBusy=false;if(b&&b.isConnected){b.disabled=false;b.textContent="Masuk"}}
}
/* Kunci tim diganti Owner (mis. ada anggota yang dihapus): sambung lagi otomatis memakai akun yang sedang masuk */
let healAt=0;
async function acctHeal(u){
  if(!u||!SRVU()||Date.now()-healAt<15000)return;healAt=Date.now();const ph=String(u.ph||"");if(!ph.startsWith("pb2$"))return;
  try{const r=await api("/login",{m:"POST",body:{id:u.id,d:ph.split("$")[2]}});
    if(r.s===200&&r.j&&r.j.code){await acctJoin(r.j.code,r.j.team);if(me){render();toast("HP ini tersambung lagi ke tim 521",1)}syncKick();return}
    if(r.s===401){teamBad=true;if(me&&me.id===u.id){logout();toast("Akun ini sudah dihapus atau PIN-nya diganti Owner. Masuk dengan nama & PIN terbaru.")}}
  }catch(e){}}
/* HP Owner: siapkan kunci tim (sekali) & unggah daftar akun setiap ada perubahan nama, peran, atau PIN */
let acT=0;
function acctAuto(){if(!SRVU()||!isHub()||!C().teamCode)return;clearTimeout(acT);acT=setTimeout(acctPush,1500)}
async function acctPush(){
  try{if(!isHub()||!C().teamCode)return;
    const U=D.users.filter(u=>String(u.ph||"").startsWith("pb2$")&&(u.pin==null||u.pin===""));if(!U.some(u=>u.role==="owner"))return;
    const users=await Promise.all(U.map(async u=>{const [,sa,h]=u.ph.split("$");return{id:u.id,name:u.name,role:u.role==="owner"?"owner":"staff",s:sa,v:await sha256h(h)}}));
    const body={code:C().teamCode,users},sig=kHash(JSON.stringify(body));
    if(sig===C().acctSig&&Date.now()-(C().acctAt||0)<864e5)return;
    const r=await api("/acct",{m:"PUT",h:{Authorization:"Bearer "+okey()},body});
    if(r.s===200){C().acctSig=sig;C().acctAt=Date.now();acctOn=true;try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}syncKick()}
    else if(r.s!==401&&r.s!==400)acT=setTimeout(acctPush,60000);
  }catch(e){acT=setTimeout(acctPush,60000)}}
function acctBoot(){try{if(isHub()&&own()&&!C().teamCode){D.cfg.teamCode=genCode();lg("Sinkron tim","Akun tim diaktifkan");save();menuAuto(0)}acctAuto();syncKick()}catch(e){}}
/* Ganti kunci tim (HP Owner): semua HP lain terputus, tersambung lagi lewat nama & PIN */
function teamRotate(){if(!isHub()||!C().teamCode)return false;D.cfg.teamCode=genCode();D.cfg.tforce=1;ZK=null;RIDc="";D.cfg.acctSig="";menuAuto(0);acctAuto();return true}
/* Lupa PIN di HP yang belum tersambung */
function acForgotSheet(){show(`<h2>Lupa PIN</h2><p class="mute" style="margin-top:-6px"><b>Karyawan / reseller:</b> minta Owner mengganti PIN di Atur → Tim & PIN, lalu masuk dengan PIN baru.</p>
  ${SRVU()?`<p class="mute"><b>Owner:</b> sambungkan HP ini memakai <b>Kunci Owner</b> (kunci rahasia yang dibuat saat memasang server, <i>bukan</i> PIN), lalu atur PIN baru.</p>
  <label>Kunci Owner<input id="ork" type="password" autocomplete="off" autocapitalize="off" spellcheck="false"></label><button class="btn" data-a="orec">Sambungkan & atur PIN baru</button>`:""}`)}
async function ownerRecover(){const k=(($("#ork")||{}).value||"").trim();if(!k){$("#ork").focus();toast("Isi Kunci Owner dulu");return}
  const b=$("[data-a=orec]");if(b){b.disabled=true;b.textContent="Memeriksa…"}
  try{const ok=await A521.ownerLink(k);if(!ok){toast("Kunci Owner salah, atau tidak ada internet.");return}
    const r=await api("/acct/code",{h:{Authorization:"Bearer "+k}});
    if(r.s===200&&r.j&&r.j.code){try{await acctJoin(r.j.code,r.j.team)}catch(e){}}
    kcan=true;acLocal=true;shut();loginView();setTimeout(forgotSheet,150);
  }finally{if(b&&b.isConnected){b.disabled=false;b.textContent="Sambungkan & atur PIN baru"}}}
function syncSum(){if(!SRVU())return K.team?"Aktif":"Belum aktif · menu & akun hanya di HP ini";
  if(!C().teamCode)return isHub()?"Menyiapkan akun tim…":"Belum tersambung · masuk dengan nama & PIN";
  if(teamBad)return"Perlu masuk lagi dengan nama & PIN";const q=(D.sq||[]).length+myQueue().length;
  return q?`${q} perubahan menunggu internet`:isHub()&&teamDirty()?"Ada perubahan, sedang dikirim…":"Aktif · menu, akun, stok & penjualan sama di semua HP"}
function syncView(){
  const st=`<div class="statusbox${teamBad||!C().teamCode?" closed":""}"><i></i>${esc(syncSum())}</div>`;
  if(!SRVU())return st+`<p class="note">Server belum dipasang di aplikasi ini, jadi sinkron antar-HP belum tersedia.</p>`;
  const what=`<p class="note">Yang otomatis sama di semua HP: menu, harga, status Habis, resep, kategori, akun & hak akses, pilihan kasir, QRIS, <b>stok bahan baku & produk jadi</b>, langganan. Penjualan & pengeluaran semua HP masuk ke Owner lewat server, walau HP Owner sedang mati.</p>`;
  if(!isHub())return st+what+(own()&&window.A521?`<p class="note" style="margin-top:14px"><b>Owner di HP ini:</b> untuk mengubah menu, akun, dan Kabar dari HP ini, masukkan <b>Kunci Owner</b> sekali.</p><label>Kunci Owner<input id="okey" type="password" autocomplete="off" autocapitalize="off" spellcheck="false"></label><button class="btn ghost" data-a="olink">Jadikan HP Owner</button>`:`<p class="note">Menu & akun diatur dari HP Owner.</p>`);
  return st+`<div class="tsteps"><p><b>1</b>Buat akun di Atur → Tim & PIN: nama, peran (Owner / Barista / Reseller), akses, dan PIN.</p><p><b>2</b>Di HP mereka: pasang 521 Coffee App → Masuk → isi nama & PIN.</p><p><b>3</b>Selesai. HP itu langsung tersambung, tanpa kode.</p></div>
    <button class="btn" data-a="tcopy">${ic("copy")}Bagikan cara masuk ke tim</button>${what}
    <button class="btn ghost" data-a="tsync">Kirim ulang sekarang</button><button class="btn ghost" data-a="tnew" style="color:var(--warn)">Putuskan semua HP lain</button>
    <p class="note">Menghapus anggota di Tim & PIN otomatis memutus HP orang itu.</p>`}

/* ---------- Stok bersama ---------- */
const stOn=()=>!!(SRVU()&&C().teamCode&&!teamBad);
let opN=0;
const fgClean=b=>({id:b.id,p:b.p,n:b.n||"",q0:+b.q0||+b.q||0,q:+b.q||0,made:b.made||"",exp:b.exp,at:b.at||"",by:b.by||"",ok:b.ok?1:0,u:b.u||""});
function mvOp(m){const at=Date.now(),id=DEV+"-"+at.toString(36)+"-"+(++opN).toString(36);
  if(String(m.i).startsWith("fg:")){if(m.nb)return{id,at,k:"fn",b:fgClean(m.nb)};if(m.del)return{id,at,k:"fx",b:m.del};if(m.b&&m.q)return{id,at,k:"fd",b:m.b,d:m.q};return null}
  if(m.set!=null)return{id,at,k:"s",i:m.i,v:+m.set||0};
  return m.q?{id,at,k:"d",i:m.i,d:m.q}:null}
function mvPush(m){const x=Object.assign({},m);delete x.nb;D.mv.push(x);const op=SRVU()&&C().teamCode?mvOp(m):null;if(op){(D.sq=D.sq||[]).push(op);stAuto(700)}}
/* Tampilan = angka resmi dari server + perubahan HP ini yang belum terkirim */
function stApply(){
  const S=D.ss;if(!S||!stOn())return;const Q=D.sq||[],gone=S.gone||{},fg={};
  Object.values(S.fg||{}).forEach(b=>{fg[b.id]=Object.assign({},b)});
  Q.forEach(o=>{if(o.k==="fn"){if(!fg[o.b.id]&&!gone[o.b.id])fg[o.b.id]=Object.assign({},o.b)}else if(o.k==="fd"){const b=fg[o.b];if(b)b.q=Math.round((b.q+o.d)*1000)/1000}else if(o.k==="fx")delete fg[o.b]});
  D.fg=Object.values(fg).sort((a,b)=>a.at<b.at?-1:a.at>b.at?1:0);
  D.fg.forEach(b=>{if(b.q>0){const p=prod(b.p);if(p&&!p.fgOn){p.fgOn=1;if(b.u&&!p.fgu)p.fgu=b.u}}});
  const I=S.ing||{};D.ing.forEach(g=>{const s=I[g.id];if(!s)return;let v=s.v,at=s.at||0;
    Q.forEach(o=>{if(o.i!==g.id)return;if(o.k==="s"){if(o.at>=at){v=o.v;at=o.at}}else if(o.k==="d"&&o.at>=at)v+=o.d});
    g.qty=Math.round(v*1000)/1000});
}
/* Sekali saja per HP: stok lama di HP ini ikut masuk ke stok bersama (batch produk jadi digabung; angka bahan baku dari HP Owner) */
function stMigrate(){const Q=D.sq=D.sq||[],at=Date.now();let n=0;
  D.fg.filter(b=>b.q>0).forEach(b=>Q.push({id:DEV+"-m"+(n++),at,k:"fn",b:fgClean(b)}));
  if(isHub())D.ing.forEach(g=>Q.push({id:DEV+"-m"+(n++),at,k:"s",i:g.id,v:+g.qty||0}));
  D.cfg.stkMig=1;}
let stT=0,stBusy=false,stAgain=false;
function stAuto(ms){if(!stOn())return;clearTimeout(stT);stT=setTimeout(stSync,ms==null?700:ms)}
const stSave=()=>{try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}};
function stDenied(){if(isHub()){C().acctSig="";acctAuto();stAuto(8000);logAuto(9000);return}if(teamBad)return;teamBad=true;if(me)acctHeal(me);else if(!$("#login").hidden)loginView()}
async function stSync(){
  if(!stOn())return;if(stBusy){stAgain=true;return}stBusy=true;
  try{const R=await ridNow();if(!R)return;
    if(!D.cfg.stkMig){const t=await api("/t/stock?rev=0",{h:{"X-A521-Room":R}});if(t.s===409){stAuto(60000);return}if(t.s===403){stDenied();return}if(t.s!==200&&t.s!==204){stAuto(30000);return}stMigrate();stSave()}
    let got=false,sent=false;
    for(let g=0;g<20;g++){const Q=D.sq||[];if(!Q.length)break;
      if(!D.sqp||!(D.sqn>0)){D.sqp=DEV+"-"+Date.now().toString(36)+"-"+(++opN).toString(36);D.sqn=Math.min(Q.length,200);stSave()}
      const r=await api("/t/stock",{m:"POST",h:{"X-A521-Room":R},body:{pid:D.sqp,ops:Q.slice(0,D.sqn)}});
      if(r.s===403){stDenied();return}if(r.s===409){stAuto(60000);return}if(r.s!==200||!r.j){stAuto(20000);return}
      D.sq=(D.sq||[]).slice(D.sqn);D.sqp="";D.sqn=0;D.ss=r.j;got=sent=true}
    if(!got){const r=await api("/t/stock?rev="+((D.ss&&D.ss.rev)||0),{h:{"X-A521-Room":R}});
      if(r.s===403){stDenied();return}if(r.s===200&&r.j){D.ss=r.j;got=true}}
    if(got){stApply();stSave();stRefresh();if(sent&&RM)RM.emit("_stk",{dev:DEV}).catch(()=>{})}
  }catch(e){stAuto(30000)}finally{stBusy=false;if(stAgain){stAgain=false;stAuto(300)}}}
function stRefresh(){try{fgSchedule()}catch(e){}if(!me||!$("#m").hidden)return;const a=document.activeElement;if(a&&/^(INPUT|TEXTAREA|SELECT)$/.test(a.tagName)&&a.id!=="lpw")return;
  if(tab==="stk"||tab==="pos"||tab==="dash"){const y=window.scrollY;render();window.scrollTo(0,y)}}

/* ---------- Penjualan, pengeluaran & langganan antar-HP lewat server ---------- */
let lgT=0,lgBusy=false,lgAgain=false;
function logAuto(ms){if(!stOn())return;clearTimeout(lgT);lgT=setTimeout(logSync,ms==null?900:ms)}
const ownDev=()=>own()||isHub()||C().lastRole==="owner";
async function logPack(){
  const T=D.tx.filter(t=>t.dev===DEV&&!t.sent).slice(0,25),E=D.exp.filter(e=>expMine(e)&&!e.lg).slice(0,40),H=C().lgmh||{},M=D.mem.filter(m=>H[m.id]!==mHash(m)).slice(0,30);
  if(!T.length&&!E.length&&!M.length)return null;const items=[];
  if(T.length)items.push(await zpack({dev:DEV,tx:T.map(t=>{const x=Object.assign({},t);delete x.sent;return x})}));if(E.length)items.push(await zpack({dev:DEV,exp:E.map(expSlim)}));if(M.length)items.push(await zpack({dev:DEV,mem:M}));
  return{pid:DEV+"-"+Date.now().toString(36)+"-"+(++opN).toString(36),code:C().teamCode,items,tk:T.map(t=>txKey(t)+"|"+t.status),ek:E.map(e=>e.id),mh:M.map(m=>[m.id,mHash(m)])}}
async function logSync(){
  if(!stOn())return;if(lgBusy){lgAgain=true;return}lgBusy=true;
  try{const R=await ridNow();if(!R)return;let sent=false;
    for(let g=0;g<10;g++){
      if(D.lgp&&D.lgp.code!==C().teamCode)D.lgp=null;
      if(!D.lgp){D.lgp=await logPack();if(!D.lgp)break;stSave()}
      const r=await api("/t/log",{m:"POST",h:{"X-A521-Room":R},body:{pid:D.lgp.pid,items:D.lgp.items}});
      if(r.s===403){stDenied();return}if(r.s!==200){logAuto(r.s===409?60000:20000);break}
      const P=D.lgp,H=C().lgmh=C().lgmh||{};D.tx.forEach(t=>{if(t.dev===DEV&&P.tk.includes(txKey(t)+"|"+t.status))t.sent=1});D.exp.forEach(e=>{if(P.ek.includes(e.id))e.lg=1});P.mh.forEach(([id,h])=>{H[id]=h});
      D.lgp=null;sent=true;stSave()}
    let n=0,ne=0,nm=0,who="";
    for(let g=0;g<20;g++){const r=await api("/t/log?since="+(C().logS||0),{h:{"X-A521-Room":R}});
      if(r.s===403){stDenied();return}if(r.s!==200||!r.j)break;
      for(const it of r.j.items||[]){try{const o=await zopen(it.p);if(!o||o.dev===DEV)continue;
        if(o.tx&&ownDev()){const x=txMerge(o.tx,"log");n+=x.n;who=x.who||who}
        if(o.exp&&ownDev())ne+=expMerge(o.exp,"log");
        if(Array.isArray(o.mem)){const b0=memSig();memMerge(o.mem);const H=C().lgmh=C().lgmh||{};o.mem.forEach(r=>{const m=r&&memBy(r.id);if(m){H[m.id]=mHash(m);mcMap[m.id]=mHash(m)}});if(memSig()!==b0)nm++}
      }catch(e){}}
      C().logS=r.j.head;stSave();if(!r.j.more)break}
    if(n||ne||nm){stSave();if(me&&$("#m").hidden&&(tab==="dash"||tab==="mem"||tab==="pos"))render();if(me&&n)toast(n+" transaksi baru dari "+(who||"HP tim"),1)}
    if(sent&&RM)RM.emit("_log",{dev:DEV}).catch(()=>{});
  }catch(e){logAuto(30000)}finally{lgBusy=false;if(lgAgain){lgAgain=false;logAuto(400)}}}

let shT=0;
function logNeed(){if(D.tx.some(t=>t.dev===DEV&&!t.sent)||D.exp.some(e=>expMine(e)&&!e.lg))return true;const H=C().lgmh||{};return D.mem.some(m=>H[m.id]!==mHash(m))}
function syncHook(){clearTimeout(shT);shT=setTimeout(()=>{acctAuto();if(stOn()&&logNeed())logAuto(0)},1200)}
function syncKick(){stAuto(200);logAuto(600)}
setTimeout(()=>{acctCheck();syncKick();if(isHub())acctAuto()},1800);
setInterval(()=>{if(document.visibilityState==="visible"&&stOn()){stAuto(0);logAuto(500)}},30000);
document.addEventListener("visibilitychange",()=>{if(document.visibilityState==="visible"){syncKick();if(acctOn!==true)acctCheck()}});
addEventListener("online",()=>syncKick());
'''
rep("let kcanKnown=false;rtInit();", "let kcanKnown=false;rtInit();\n/*V10-PATCH*/" + NEW)

P.write_text(s)
print("OK, perubahan 10 (akun tanpa kode tim, stok bersama, peran reseller, tombol Cup/Botol) diterapkan.")
