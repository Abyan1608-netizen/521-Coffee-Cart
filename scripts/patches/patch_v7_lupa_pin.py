"""Perubahan 07: "Lupa PIN?" (atur ulang PIN Owner dengan Kunci Owner dari server) + penjelasan jelas
di lembar wajib ganti PIN agar Kunci Owner tidak tertukar dengan PIN/Nama. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V7-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:200]}")
    s = s.replace(old, new)

# Tombol "Lupa PIN?" di bawah keypad
rep('    <p class="hint" id="hint" hidden></p>',
    '    <p class="hint" id="hint" hidden></p>\n    <button class="btn ghost sm" id="lforgot" data-a="forgot" type="button" style="margin:12px auto 0;display:block">Lupa PIN?</button>')

rep("/* ---------- Menu ---------- */", r'''/*V7-PATCH*/
/* ---------- Lupa PIN: Owner mengatur ulang PIN dengan Kunci Owner (dicek ke server) ---------- */
const looksKey=t=>{t=String(t||"").trim();return t.length>=20&&!/\s/.test(t)&&/^[A-Za-z0-9+\/=_-]+$/.test(t)&&/[A-Z]/.test(t)&&/[a-z]/.test(t)&&/\d/.test(t)};
function forgotSheet(){const O=D.users.filter(u=>u.role==="owner"),srv=!!(window.A521&&A521.server);
  show(`<h2>Lupa PIN</h2><p class="mute" style="margin-top:-6px"><b>Akun Owner:</b> atur ulang PIN memakai <b>Kunci Owner</b> (kunci rahasia yang dibuat saat memasang server, <i>bukan</i> PIN).<br><b>Akun karyawan:</b> minta Owner mengganti PIN di Atur → Tim & PIN.</p>
  ${srv?`<label>Akun Owner<select id="fpu">${O.map(u=>`<option value="${u.id}">${esc(u.name.length>24?u.name.slice(0,10)+"… (nama perlu dirapikan)":u.name)}</option>`).join("")}</select></label>
  <label>Kunci Owner<input id="fpk" type="password" autocomplete="off" autocapitalize="off" spellcheck="false"></label>
  <label>PIN atau kata sandi baru<input id="fpp" type="password" autocomplete="new-password" autocapitalize="off" spellcheck="false" maxlength="32"></label>
  <label class="fgck"><input type="checkbox" id="fpn" checked>Kembalikan nama akun ini menjadi "Owner" bila namanya berubah tidak sengaja.</label>
  <button class="btn" data-a="fpgo">Atur ulang PIN</button>`
  :`<p class="note">Server belum dipasang di aplikasi ini, jadi PIN Owner tidak bisa diatur ulang dari sini. Pilihan terakhir: Pengaturan HP → Aplikasi → 521 Coffee App → Penyimpanan → <b>Hapus data</b> (data di HP ini terhapus, PIN kembali ke awal).</p>`}`)}
async function forgotGo(){const u=D.users.find(x=>x.id===($("#fpu")||{}).value),k=(($("#fpk")||{}).value||"").trim(),p=($("#fpp")||{}).value||"";
  if(!u)return;if(!k){$("#fpk").focus();toast("Isi Kunci Owner dulu");return}
  if(p.length<4||p.length>32){$("#fpp").focus();toast("PIN baru minimal 4 karakter");return}
  if(/^(1234|0000|1111|123456|000000)$/.test(p)){toast("PIN ini terlalu mudah ditebak. Pakai yang lain.");return}
  if(p===k){toast("PIN jangan sama dengan Kunci Owner");return}
  const b=$("[data-a=fpgo]");if(b){b.disabled=true;b.textContent="Memeriksa kunci…"}
  const ok=await A521.ownerLink(k);
  if(!ok){if(b){b.disabled=false;b.textContent="Atur ulang PIN"}toast("Kunci Owner salah, atau tidak ada internet.");return}
  u.ph=await pwHash(u.id,p);delete u.pin;if($("#fpn")&&$("#fpn").checked&&(looksKey(u.name)||u.name.length>24))u.name="Owner";
  lkSet({n:0,u:0});lsel=u.id;D.log.push({at:iso(),a:"Atur ulang PIN Owner",d:u.name+" (dengan Kunci Owner)",by:"Sistem"});
  try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}shut();loginView();toast("PIN Owner diperbarui. Silakan masuk dengan PIN baru.",1)}

/* ---------- Menu ---------- */''')

# aksi publik (sebelum pengecekan login)
rep('  if(!me)return;\n  if(a==="logout")logout();',
    '  if(a==="forgot"){forgotSheet();return}\n  if(a==="fpgo"){forgotGo();return}\n  if(!me)return;\n  if(a==="logout")logout();')

# lembar wajib ganti PIN: penjelasan + cegah Kunci Owner tertempel di Nama/PIN
rep("function openUsr(id,force){const u=D.users.find(x=>x.id===id);if(!u)return;eu=Object.assign({},u);delete eu.pin;delete eu.ph;if(force)eu.force=1;\n  if(u.role!==\"owner\")eu.perm=[...permOf(u)],eu.title=u.title||\"Barista\",eu.pms=Array.isArray(u.pms)?[...u.pms]:undefined;usrSheet()}",
    "function openUsr(id,force){const u=D.users.find(x=>x.id===id);if(!u)return;eu=Object.assign({},u);delete eu.pin;delete eu.ph;if(force)eu.force=1;\n  if(u.role!==\"owner\")eu.perm=[...permOf(u)],eu.title=u.title||\"Barista\",eu.pms=Array.isArray(u.pms)?[...u.pms]:undefined;usrSheet();\n  if(force){const h=$(\"#s h2\");if(h)h.insertAdjacentHTML(\"afterend\",`<div class=\"warn\" style=\"margin:4px 0 12px\">${ic(\"alert\")}<span><b>Ganti PIN login dulu.</b> Isi kolom <b>PIN baru</b> di bawah dengan PIN yang mudah kamu ingat (bukan 1234). <b>Kunci Owner</b> server <u>tidak</u> diisi di sini, tapi nanti di Atur → Sinkron semua HP.</span></div>`)}}")
rep('if(!nm){$("#u-name").focus();return}',
    'if(!nm){$("#u-name").focus();return}\n    if(looksKey(nm)){toast("Nama ini terlihat seperti Kunci Owner. Isi nama orang (mis. Owner). Kunci Owner diisi di Atur → Sinkron.");$("#u-name").focus();return}\n    if(p&&(looksKey(p)&&p.length>=24||(()=>{try{return p===localStorage.getItem("a521owner")}catch(e){return false}})())){toast("Itu Kunci Owner, bukan PIN. Buat PIN login sendiri (mis. 6 angka).");$("#u-pin").focus();return}')

P.write_text(s)
print("OK, perubahan 07 (Lupa PIN + penjelasan ganti PIN) diterapkan.")
