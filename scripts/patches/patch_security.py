"""Patch keamanan + kesiapan Android untuk src/index.src.html (sekali jalan, idempotent-check).
Dipakai sekali saat migrasi; hasilnya sudah tersimpan di src/. Disimpan sebagai catatan perubahan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*SEC-PATCH-v1*/" in s:
    print("Sudah dipatch."); sys.exit(0)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:160]}")
    s = s.replace(old, new)

PLAY = "https://play.google.com/store/apps/details?id=id.coffee521.pos"

# 1) Semua link halaman claude.ai -> link aplikasi di Play Store
rep('const DEF={', '/*SEC-PATCH-v1*/const PLAY_URL="' + PLAY + '";\nconst DEF={')
rep('promo:"https://claude.ai/artifact/3AdqCGi73y9hsp7Ls8b89x"};', 'promo:PLAY_URL};')
rep('const PROMO_DEF="https://claude.ai/artifact/3AdqCGi73y9hsp7Ls8b89x"', 'const PROMO_DEF=PLAY_URL')
rep('if(!d.cfg.promo||d.cfg.promo==="https://claude.ai/artifact/2wqVXCUtJHCucmRZF7UWYX")d.cfg.promo="https://claude.ai/artifact/3AdqCGi73y9hsp7Ls8b89x";',
    'if(!d.cfg.promo||/^https:\\/\\/claude\\.ai\\//.test(d.cfg.promo))d.cfg.promo=PLAY_URL;')
rep('placeholder="https://claude.ai/artifact/..."', 'placeholder="${PLAY_URL}"')

# 2) URL gambar aman (cegah injeksi atribut lewat data gambar dari backup/sinkron)
rep('const esc=s=>', 'const su=s=>{s=String(s==null?"":s);return /^data:image\\/(png|jpe?g|webp|gif|avif);base64,[A-Za-z0-9+\\/=]+$/.test(s)||/^media\\/[\\w.-]+$/.test(s)||/^https:\\/\\/[^\\s"\'<>()\\\\]+$/.test(s)?s:""};\nconst esc=s=>')
for v in ["PROMO_QR", "h", "p.img", "qsrc()", "src", "t.img", "u", "x.img"]:
    old = 'src="${' + v + '}"'
    s = s.replace(old, 'src="${su(' + v + ')}"')
rep("--src:url('${src}')", "--src:url('${su(src)}')")
rep("--src:url('${u}')", "--src:url('${su(u)}')")

# 3) CSV: cegah formula injection saat dibuka di Excel/Sheets
rep('function csv(h,rows){return[h,...rows].map(r=>r.map(v=>{v=String(v==null?"":v);return',
    'function csv(h,rows){return[h,...rows].map(r=>r.map(v=>{v=String(v==null?"":v);if(/^[=+\\-@\\t\\r]/.test(v)&&!/^-?\\d+([.,]\\d+)?$/.test(v))v="\'"+v;return')

# 4) PIN: hash PBKDF2 + salt acak, perbandingan waktu-konstan, migrasi PIN lama, batas salah PIN
rep('const b64u8=b=>Uint8Array.from(atob(b),c=>c.charCodeAt(0));',
    '''const b64u8=b=>Uint8Array.from(atob(b),c=>c.charCodeAt(0));
/* PIN/kata sandi disimpan sebagai hash PBKDF2-SHA256 (salt acak per akun), bukan teks asli */
const PWI=100000,tsEq=(a,b)=>{a=String(a);b=String(b);if(a.length!==b.length)return false;let r=0;for(let i=0;i<a.length;i++)r|=a.charCodeAt(i)^b.charCodeAt(i);return r===0};
async function pwDer(id,p,salt){const km=await crypto.subtle.importKey("raw",new TextEncoder().encode("521|"+id+"|"+p),"PBKDF2",false,["deriveBits"]);
  return u8b64(new Uint8Array(await crypto.subtle.deriveBits({name:"PBKDF2",salt,iterations:PWI,hash:"SHA-256"},km,256)))}
async function pwHash(id,p){const salt=crypto.getRandomValues(new Uint8Array(16));return "pb2$"+u8b64(salt)+"$"+await pwDer(id,p,salt)}
async function pwCheck(u,b){if(!u||!b)return false;if(u.pin!=null&&u.pin!=="")return tsEq(b,u.pin);if(!u.ph)return false;
  if(String(u.ph).startsWith("pb2$")){const [,sa,h]=u.ph.split("$");return tsEq(await pwDer(u.id,b,b64u8(sa)),h)}
  return tsEq(await sha256h("521|"+u.id+"|"+b),u.ph)}
async function pinMigrate(){let n=0;for(const u of D.users){if(u.pin!=null&&u.pin!==""){u.ph=await pwHash(u.id,String(u.pin));delete u.pin;n++}}
  if(n){try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}}return n}
pinMigrate().catch(()=>{});''')

rep('''let tlN=0;
async function tryLogin(force){
  const u=D.users.find(x=>x.id===lsel);if(!u)return;const n=++tlN,b=buf;
  let okp=u.pin!=null&&u.pin!==""?b===u.pin:false;if(!okp&&u.ph&&b)okp=(await sha256h("521|"+u.id+"|"+b))===u.ph;
  if(n!==tlN||b!==buf)return;
  if(okp){me=u;buf="";peek=false;$("#lerr").textContent="";try{sessionStorage.setItem("pos521u",u.id)}catch(e){}enter();return}
  if(force){$("#lerr").textContent=buf?"PIN atau kata sandi belum cocok. Coba lagi.":"Masukkan PIN atau kata sandi dulu.";buf="";dots(true)}else dots();
}''', '''let tlN=0,lgPrev="";
/* Batas salah PIN: 5x salah -> jeda 30 dtk, berlipat sampai maks. 15 menit. Tersimpan di HP, tidak hilang saat aplikasi ditutup. */
const lkGet=()=>{try{return JSON.parse(localStorage.getItem("pos521lk"))||{n:0,u:0}}catch(e){return{n:0,u:0}}};
const lkSet=o=>{try{localStorage.setItem("pos521lk",JSON.stringify(o))}catch(e){}};
const lkWait=()=>Math.max(0,(lkGet().u||0)-Date.now());
function lkFail(){const o=lkGet();o.n=(o.n||0)+1;if(o.n>=5)o.u=Date.now()+Math.min(9e5,3e4*Math.pow(2,o.n-5));lkSet(o)}
function lkMsg(){const w=lkWait();if(!w)return false;const m=Math.ceil(w/1000);$("#lerr").textContent=`Terlalu banyak percobaan. Coba lagi dalam ${m>90?Math.ceil(m/60)+" menit":m+" detik"}.`;return true}
function lgSet(nb){if(lgPrev&&!nb.startsWith(lgPrev)){lkFail();lgPrev=""}buf=nb}
function lgAuto(){if(buf.length>=4&&!lkWait()){lgPrev=buf;tryLogin()}else dots()}
async function tryLogin(force){
  const u=D.users.find(x=>x.id===lsel);if(!u)return;
  if(lkMsg()){if(force){buf="";lgPrev="";dots(true)}return}
  const n=++tlN,b=buf;
  const okp=b.length>=4&&await pwCheck(u,b);
  if(n!==tlN||b!==buf)return;
  if(okp){lkSet({n:0,u:0});lgPrev="";me=u;buf="";peek=false;$("#lerr").textContent="";try{sessionStorage.setItem("pos521u",u.id)}catch(e){}enter();
    if(/^(1234|0000)$/.test(b))setTimeout(()=>{openUsr(u.id,1);toast("Demi keamanan, ganti PIN awal ini dulu ya")},350);return}
  if(force){if(buf)lkFail();lgPrev="";$("#lerr").textContent=buf?"PIN atau kata sandi belum cocok. Coba lagi.":"Masukkan PIN atau kata sandi dulu.";lkMsg();buf="";dots(true)}else dots();
}''')
rep('if(a==="lsel"){lsel=v;buf="";', 'if(a==="lsel"){if(lgPrev){lkFail();lgPrev=""}lsel=v;buf="";')
rep('if(a==="kp"){if(buf.length<32){buf+=v;$("#lerr").textContent="";tryLogin()}return}',
    'if(a==="kp"){if(buf.length<32){lgSet(buf+v);$("#lerr").textContent="";lgAuto()}return}')
rep('if(a==="kdel"){buf=buf.slice(0,-1);dots();return}', 'if(a==="kdel"){lgSet(buf.slice(0,-1));dots();return}')
rep('if(t.id==="lpw"){buf=t.value.slice(0,32);$("#lerr").textContent="";t.classList.remove("err");const u=D.users.find(x=>x.id===lsel);if(u&&(buf===u.pin||u.ph))tryLogin()}',
    'if(t.id==="lpw"){lgSet(t.value.slice(0,32));$("#lerr").textContent="";t.classList.remove("err");const u=D.users.find(x=>x.id===lsel);if(u)lgAuto()}')

# Cek password Chat 521 memakai pwCheck
rep('let ok=u.pin!=null&&u.pin!==""?b===u.pin:false;const fin=ok=>{', 'const fin=ok=>{')
rep('if(!ok&&u.ph&&b)sha256h("521|"+u.id+"|"+b).then(h=>fin(h===u.ph));else fin(ok)}', 'pwCheck(u,b).then(fin,()=>fin(false))}')

# Buka lembar akun (dipakai juga untuk paksa ganti PIN awal)
rep('else if(a==="usr"){const u=D.users.find(x=>x.id===id);if(u){eu=Object.assign({},u);if(u.role!=="owner")eu.perm=[...permOf(u)],eu.title=u.title||"Barista",eu.pms=Array.isArray(u.pms)?[...u.pms]:undefined;usrSheet()}}',
    'else if(a==="usr")openUsr(id);')
rep('function shut(){', '''function openUsr(id,force){const u=D.users.find(x=>x.id===id);if(!u)return;eu=Object.assign({},u);delete eu.pin;delete eu.ph;if(force)eu.force=1;
  if(u.role!=="owner")eu.perm=[...permOf(u)],eu.title=u.title||"Barista",eu.pms=Array.isArray(u.pms)?[...u.pms]:undefined;usrSheet()}
function shut(){''')
rep('if((eu.isNew||p)&&(p.length<4||p.length>32)){toast("Minimal 4 karakter, maksimal 32");$("#u-pin").focus();return}',
    'if((eu.isNew||eu.force||p)&&(p.length<4||p.length>32)){toast(eu.force&&!p?"Isi PIN atau kata sandi baru dulu":"Minimal 4 karakter, maksimal 32");$("#u-pin").focus();return}\n    if(p&&/^(1234|0000|1111|123456|000000)$/.test(p)){toast("PIN ini terlalu mudah ditebak. Pakai yang lain.");$("#u-pin").focus();return}')
rep('save();shut();toast(nm+" tersimpan",1);', 'save();pinMigrate().catch(()=>{});shut();toast(nm+" tersimpan",1);')

# 5) Teks yang menyebut aplikasi Claude -> sesuai aplikasi Android
rep('btMsg="Bluetooth tidak tersedia di tampilan ini. Di dalam aplikasi Claude, halaman tidak diberi izin Bluetooth. Pakai cara salin ke aplikasi printer di bawah.";',
    'btMsg=window.A521?"Cetak Bluetooth langsung belum tersedia di aplikasi ini. Pakai cara salin ke aplikasi printer di bawah.":"Bluetooth tidak tersedia di tampilan ini. Di dalam aplikasi Claude, halaman tidak diberi izin Bluetooth. Pakai cara salin ke aplikasi printer di bawah.";')
rep('toast("Akun Claude ini bukan pemilik halaman, jadi tidak bisa menerbitkan.")',
    'toast(window.A521?"HP ini belum dijadikan HP Owner (Atur → Sinkron semua HP).":"Akun Claude ini bukan pemilik halaman, jadi tidak bisa menerbitkan.")')
rep('if(!AR||!kcan)return `<p class="note" style="margin-top:0">Sinkron hanya bisa diaktifkan dari HP yang membuka aplikasi dengan akun Claude pemilik halaman (akun Kakak).</p>`;',
    '''if(!AR||!kcan)return window.A521?`<p class="note" style="margin-top:0">Sinkron & terbit Kabar hanya dari <b>HP Owner</b>. Masukkan <b>Kunci Owner</b> (dibuat saat server dipasang) sekali saja di HP ini.</p><label>Kunci Owner<input id="okey" type="password" autocomplete="off" autocapitalize="off" spellcheck="false"></label><button class="btn" data-a="olink">Jadikan HP Owner</button>`:`<p class="note" style="margin-top:0">Sinkron hanya bisa diaktifkan dari HP yang membuka aplikasi dengan akun Claude pemilik halaman (akun Kakak).</p>`;''')
rep('else if(a==="tsync"&&own()){', '''else if(a==="olink"&&own()&&window.A521){const k=(($("#okey")||{}).value||"").trim();if(!k){toast("Isi Kunci Owner dulu");return}
    A521.ownerLink(k).then(ok=>{if(ok){toast("HP ini sekarang HP Owner. Memuat ulang…",1);setTimeout(()=>location.reload(),900)}else toast("Kunci Owner salah, atau server belum bisa dihubungi.")})}
  else if(a==="tsync"&&own()){''')

# 6) Chat 521: tombol laporkan jawaban AI (kebijakan Google Play untuk konten buatan AI)
rep('<button class="chb" data-a="c_clear"',
    '<button class="chb" data-a="c_report" aria-label="Laporkan jawaban" title="Laporkan jawaban yang keliru atau tidak pantas"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 21V4m0 0h11l-2 4 2 4H5"/></svg></button><button class="chb" data-a="c_clear"')
rep('else if(a==="c_clear"){', '''else if(a==="c_report"){const L=[...chatH].reverse().find(m=>m.role==="assistant"&&m.content);if(!L){toast("Belum ada jawaban untuk dilaporkan");return}
    const t="Laporan jawaban Chat 521 (AI) yang keliru/tidak pantas:\\n\\n"+L.content.slice(0,1500),w=waNum((K.store||{}).wa);
    if(w){const u="https://wa.me/"+w+"?text="+encodeURIComponent(t);if(window.A521)A521.open(u);else window.open(u,"_blank","noopener")}else copy(t,"Teks laporan tersalin. Kirim ke Owner ya.");toast("Terima kasih sudah melapor 🙏",1)}
  else if(a==="c_clear"){''')

P.write_text(s)
print("OK, patch diterapkan:", P)
