/* ---------- Kabar: halaman publik + kelola (owner) ---------- */
let K;try{K=JSON.parse(document.getElementById("kdata").textContent)}catch(e){K={}}
K.store=K.store||{};K.posts=Array.isArray(K.posts)?K.posts:[];K.menu=Array.isArray(K.menu)?K.menu:[];
const PAGE_CSS=document.getElementById("css").textContent,PAGE_APP=document.getElementById("app").textContent;
let kdirty=false,kp=null,AR=null,UAPI=null,kcan=false;
try{const st=sessionStorage.getItem("k521-pending");if(st){K=JSON.parse(st);kdirty=true}}catch(e){}
const kToday=()=>ymd(new Date());
const kFmt=s=>{if(!s)return"";return new Date(s+"T00:00").toLocaleDateString("id-ID",{day:"numeric",month:"short"})};
function kOpen(h){const m=String(h||"").match(/(\d{1,2})[.:](\d{2})\s*[-–]\s*(\d{1,2})[.:](\d{2})/);if(!m)return null;const n=new Date(),c=n.getHours()*60+n.getMinutes(),a=+m[1]*60+ +m[2],b=+m[3]*60+ +m[4];return a<=b?(c>=a&&c<b):(c>=a||c<b)}
function kVis(p){if(p.draft)return false;const t=kToday();if(p.type==="event")return !p.date||p.date>=t;if(p.end&&p.end<t)return false;return true}
function kCtl(p,m){return m?`<div class="k-ctl"><button data-a="ked" data-v="${p.id}">Ubah</button><button data-a="ktog" data-v="${p.id}">${p.draft?"Tampilkan":"Jadikan draf"}</button><button data-a="kdel" data-v="${p.id}">Hapus</button></div>`:""}
const kPill=(p,m)=>p.draft?'<span class="pill">Draf</span>':(m&&!kVis(p)?'<span class="pill">Sudah lewat</span>':"");
function kPromo(p,m){const t=kToday(),up=p.start&&p.start>t,last=p.end&&p.end===t;
  return `<article class="k-promo${p.draft?" k-draft":""}">${p.badge?`<div class="k-badge">${esc(p.badge)}</div>`:""}<h3>${esc(p.title)}${kPill(p,m)}</h3>${p.body?`<p>${esc(p.body)}</p>`:""}<div class="k-meta">${up?`<span class="soon">${ic("cal")}Mulai ${kFmt(p.start)}</span>`:last?`<span class="soon">${ic("today")}Berakhir hari ini</span>`:p.end?`<span class="when">${ic("cal")}Sampai ${kFmt(p.end)}</span>`:`<span>${ic("today")}Selama persediaan ada</span>`}${p.code?`<button class="k-code" data-a="kcopy" data-v="${esc(p.code)}" aria-label="Salin kode ${esc(p.code)}">${esc(p.code)}<small>SALIN</small></button>`:""}</div>${kCtl(p,m)}</article>`}
function kEv(p,m){const d=p.date?new Date(p.date+"T00:00"):null;
  return `<article class="k-ev${p.draft?" k-draft":""}"><div class="k-date">${d?`<b>${d.getDate()}</b><span>${d.toLocaleDateString("id-ID",{month:"short"})}</span>`:"<b>?</b><span>Segera</span>"}</div><div style="min-width:0"><h3>${esc(p.title)}${kPill(p,m)}</h3><div class="k-meta" style="margin-top:2px">${d?`<span class="when">${d.toLocaleDateString("id-ID",{weekday:"long"})}${p.time?" · "+esc(p.time):""}</span>`:""}${p.place?`<span>${ic("pin")}${esc(p.place)}</span>`:""}</div>${p.body?`<p>${esc(p.body)}</p>`:""}${kCtl(p,m)}</div></article>`}
function kNews(p,m){return `<article class="k-news${p.draft?" k-draft":""}"><time>${kFmt(p.date||p.created)}</time><h3>${esc(p.title)}${kPill(p,m)}</h3>${p.body?`<p>${esc(p.body)}</p>`:""}${kCtl(p,m)}</article>`}
const kEmpty=(t,s)=>`<div class="k-empty"><b>${t}</b>${s}</div>`;
function kMenuList(m){const L=m?D.prod.filter(p=>p.active).map(p=>({n:p.name,p:p.price})):K.menu;return L.length?`<div class="k-menu">${L.map(x=>`<div class="k-mi"><b>${esc(x.n)}</b><i></i><span>${rp(x.p)}</span></div>`).join("")}</div>`:kEmpty("Menu segera hadir","")}
function kSections(m){
  const sh=p=>m||kVis(p),P=K.posts;
  const pr=P.filter(p=>p.type==="promo"&&sh(p)).sort((a,b)=>(a.end||"9999").localeCompare(b.end||"9999"));
  const ev=P.filter(p=>p.type==="event"&&sh(p)).sort((a,b)=>(a.date||"9999").localeCompare(b.date||"9999"));
  const nw=P.filter(p=>p.type==="news"&&sh(p)).sort((a,b)=>(b.date||b.created||"").localeCompare(a.date||a.created||""));
  const s=K.store,wa=String(s.wa||"").replace(/\D/g,"").replace(/^0/,"62"),ig=String(s.ig||"").replace(/^@/,"").trim();
  return `<nav class="k-tabs" aria-label="Bagian halaman"><a href="#k-promo">Promo<b>${pr.filter(kVis).length||""}</b></a><a href="#k-kegiatan">Kegiatan<b>${ev.filter(kVis).length||""}</b></a><a href="#k-kabar">Kabar</a><a href="#k-menu">Menu</a>${wa||ig?'<a href="#k-kontak">Kontak</a>':""}</nav>
  <h2 class="k-h2" id="k-promo">Promo${m?`<button class="k-add" data-a="knew" data-v="promo">+ Promo</button>`:""}</h2>${pr.map(p=>kPromo(p,m)).join("")||kEmpty("Belum ada promo saat ini","Mampir lagi ya, promo baru diumumkan di sini.")}
  <h2 class="k-h2" id="k-kegiatan">Kegiatan${m?`<button class="k-add" data-a="knew" data-v="event">+ Kegiatan</button>`:""}</h2>${ev.map(p=>kEv(p,m)).join("")||kEmpty("Belum ada kegiatan terjadwal","Event, pop-up, dan kumpul bareng akan muncul di sini.")}
  <h2 class="k-h2" id="k-kabar">Kabar${m?`<button class="k-add" data-a="knew" data-v="news">+ Kabar</button>`:""}</h2>${nw.map(p=>kNews(p,m)).join("")||kEmpty("Belum ada kabar","Info menu baru dan perubahan jam buka diumumkan di sini.")}
  <h2 class="k-h2" id="k-menu">Menu</h2>${m?'<p class="note" style="margin-top:-6px">Diambil otomatis dari tab Menu (yang tidak disembunyikan) setiap kali Anda menerbitkan.</p>':""}${kMenuList(m)}
  ${wa||ig?`<h2 class="k-h2" id="k-kontak">Kontak</h2><div class="k-contact">${wa?`<a href="https://wa.me/${wa}" target="_blank" rel="noopener">${ic("wa")}<span><b>WhatsApp</b><small>+${esc(wa)}</small></span>${ic("arrow")}</a>`:""}${ig?`<a href="https://instagram.com/${encodeURIComponent(ig)}" target="_blank" rel="noopener">${ic("ig")}<span><b>Instagram</b><small>@${esc(ig)}</small></span>${ic("arrow")}</a>`:""}</div>`:""}`;
}
function kHead(){const s=K.store,o=kOpen(s.hours);return `<div class="k-hero" role="img" aria-label="${esc(s.name||"521 Coffee")}"><div class="st">${o===null?"":`<span class="k-chip${o?"":" closed"}"><i></i>${o?"Buka sekarang":"Sedang tutup"}</span>`}${s.hours?`<span class="k-chip">${ic("today")}${esc(s.hours)}</span>`:""}</div></div>
  <h1 class="k-h1">${esc(s.headline||s.name)}</h1><p class="k-tagl">${esc(s.tagline)}</p>
  <div class="k-info"><div><span>Jam buka</span><b>${esc(s.hours||"-")}</b></div><div><span>Lokasi</span><b>${esc(s.place||"-")}</b></div></div>`}
function pubRender(){
  const s=K.store;
  $("#pub").innerHTML=`<div class="kwrap"><div class="k-top"><svg class="mark" aria-hidden="true"><use href="#logo"/></svg><b>${esc(s.name||"521 Coffee")}</b><button class="k-login" data-a="${me?"toapp":"masuk"}">${ic("user")}${me?"Kembali ke kasir":"Masuk"}</button></div>${kHead()}${kSections(false)}<div class="k-foot"><svg class="mark" aria-hidden="true"><use href="#logo"/></svg>${esc(s.name)} · ${esc(s.tagline)}</div></div>`;
}
function showPub(){$("#m").hidden=true;$("#login").hidden=true;$("#app").hidden=true;$("#pub").hidden=false;pubRender();window.scrollTo(0,0)}
function showLogin(){$("#pub").hidden=true;$("#app").hidden=true;$("#login").hidden=false;buf="";loginView();window.scrollTo(0,0)}
function kabar(){
  return `<div class="greet"><div><h2>Kabar & promo</h2><p>Halaman yang dilihat pelanggan saat membuka link tanpa masuk.</p></div><span style="display:flex;gap:8px;flex-wrap:wrap"><button class="qbtn" data-a="kview">Lihat sebagai pelanggan</button><button class="qbtn" data-a="kstore">Info toko & kontak</button></span></div>
  ${kHead()}${kSections(true)}
  <div class="k-pub"><span>${kdirty?"Ada perubahan yang belum terbit.":"Draf hanya terlihat di sini, tidak oleh pelanggan."}</span><button class="btn" data-a="kpublish">Terbitkan</button></div>`;
}
function kPostSheet(){
  const p=kp,T=p.type;
  show(`<h2>${p.isNew?"Tambah":"Ubah"} ${T==="promo"?"promo":T==="event"?"kegiatan":"kabar"}</h2>
  <label>Judul<input id="p-title" value="${esc(p.title)}" placeholder="${T==="promo"?"Contoh: Senin Hemat Palm Sugar":T==="event"?"Contoh: Ngopi Pagi Bareng":"Contoh: Menu baru, Matcha Latte"}"></label>
  ${T==="promo"?`<label>Teks besar (opsional)<input id="p-badge" value="${esc(p.badge)}" placeholder="Contoh: Diskon 20% · Beli 2 Gratis 1"></label>`:""}
  <label>Keterangan<textarea class="kt" id="p-body" placeholder="Syarat, detail, atau cerita singkat">${esc(p.body)}</textarea></label>
  ${T==="promo"?`<div class="two"><label>Mulai<input id="p-start" type="date" value="${esc(p.start)}"></label><label>Sampai<input id="p-end" type="date" value="${esc(p.end)}"></label></div><label>Kode promo (opsional)<input id="p-code" value="${esc(p.code)}" placeholder="Contoh: SENIN521"></label>`:""}
  ${T==="event"?`<div class="two"><label>Tanggal<input id="p-date" type="date" value="${esc(p.date)}"></label><label>Jam<input id="p-time" value="${esc(p.time)}" placeholder="06.00–09.00"></label></div><label>Tempat<input id="p-place" value="${esc(p.place)}"></label>`:""}
  ${T==="news"?`<label>Tanggal<input id="p-date" type="date" value="${esc(p.date||kToday())}"></label>`:""}
  <label class="chk"><input type="checkbox" id="p-draft" ${p.draft?"checked":""}> Simpan sebagai draf (belum terlihat pelanggan)</label>
  <p class="note">${T==="promo"?"Promo yang lewat tanggal “Sampai” otomatis hilang dari halaman pelanggan.":T==="event"?"Kegiatan yang sudah lewat otomatis hilang dari halaman pelanggan.":"Kabar terbaru tampil paling atas."}</p>
  <button class="btn" data-a="ksavep">${p.isNew?"Tambahkan":"Simpan"}</button>`);
}
function kStoreSheet(){const s=K.store;
  show(`<h2>Info toko & kontak</h2><p class="note">Nama toko dan tagline mengikuti Atur → Identitas toko.</p><label>Judul besar<input id="s-headline" value="${esc(s.headline)}"></label>
  <div class="two"><label>Jam buka<input id="s-hours" value="${esc(s.hours)}" placeholder="05.00–21.00"></label><label>Lokasi<input id="s-place" value="${esc(s.place)}"></label></div>
  <div class="two"><label>Nomor WhatsApp<input id="s-wa" inputmode="tel" value="${esc(s.wa)}" placeholder="08xxxxxxxxxx"></label><label>Instagram<input id="s-ig" value="${esc(s.ig)}" placeholder="@521coffee"></label></div>
  <p class="note">Jam buka dipakai untuk status “Buka sekarang / Sedang tutup”. Tulis seperti 05.00–21.00.</p><button class="btn" data-a="ksaves">Simpan</button>`)}
function kChanged(){kdirty=true;try{sessionStorage.setItem("k521-pending",JSON.stringify(K))}catch(e){}if(me)render()}
function kDoc(){
  const reset=':root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px/1.4 system-ui,-apple-system,sans-serif;background:#fafaf7}img{max-width:100%}[hidden]{display:none!important}';
  const data=JSON.stringify(K).replace(/</g,"\\u003c");
  return '<!doctype html><html><head><meta charset=utf8><meta name=viewport content="width=device-width,initial-scale=1,viewport-fit=cover"><style>'+reset+'</style></head><body>'
   +'<title>521 Coffee Cart POS</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,400..900&family=IBM+Plex+Mono:wght@500;600&display=swap">\n'
   +'<style id="css">'+PAGE_CSS+'</style>\n'+document.getElementById("logo-sprite").outerHTML+'\n<div id="mount"></div>\n'
   +'<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"><\/script>\n<script type="application/json" id="kdata">'+data+'<\/script>\n<script id="app">'+PAGE_APP+'<\/script></body></html>';
}
async function kPublish(){
  if(!AR){toast("Menerbitkan hanya bisa dari aplikasi Claude dengan akun pemilik halaman.");return}
  const b=$("[data-a=kpublish]");if(b){b.disabled=true;b.textContent="Menerbitkan…"}
  K.store.name=C().name;K.store.tagline=C().sub;K.menu=D.prod.filter(p=>p.active).map(p=>({n:p.name,p:p.price}));
  try{sessionStorage.setItem("k521-pending",JSON.stringify(K))}catch(e){}
  try{await AR.publish(kDoc());try{sessionStorage.removeItem("k521-pending")}catch(e){}kdirty=false;toast("Terbit. Pelanggan sudah bisa melihatnya.",1)}
  catch(e){const c=e&&e.code;if(c==="conflict")toast("Halaman baru saja diubah di tempat lain. Memuat versi terbaru…");else if(c==="not_writer"||c==="not_granted")toast("Akun Claude ini bukan pemilik halaman, jadi tidak bisa menerbitkan.");else toast("Belum berhasil terbit. Coba lagi sebentar.");if(b){b.disabled=false;b.textContent="Terbitkan"}}
}
(async()=>{try{if(!window.claude||!claude.use)return;const [u,ar]=await Promise.all([claude.use("user"),claude.use("artifact")]);UAPI=u;AR=ar;try{kcan=!!(u&&await u.canEdit())}catch(x){}}catch(x){}})();
