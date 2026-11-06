/* ===== V21: website = halaman Kabar pelanggan; headline & kartu menu website diatur dari aplikasi ===== */
/* Pengaturan kartu menu website per menu (foto & keterangan kecil), disimpan di K.store.web.mi[id menu] */
function webMI(p){const w=(K.store&&K.store.web)||{};return ((w.mi||{})[p.id])||{}}
var webPend={};/* foto kartu menu yang baru dipilih, belum disimpan */
function webShrink(f,cb){const r=new FileReader();r.onload=()=>{const im=new Image();
    im.onload=()=>{try{const sc=Math.min(1,1350/Math.max(im.width,im.height)),cv=document.createElement("canvas");cv.width=Math.round(im.width*sc);cv.height=Math.round(im.height*sc);
      const x=cv.getContext("2d");x.fillStyle="#000";x.fillRect(0,0,cv.width,cv.height);x.drawImage(im,0,0,cv.width,cv.height);cb(cv.toDataURL("image/jpeg",.8))}catch(e){toast("Foto ini tidak bisa dipakai. Coba foto lain.")}};
    im.onerror=()=>toast("Foto ini tidak bisa dibaca. Coba foto lain.");im.src=r.result};r.readAsDataURL(f)}
const WTYPE={promo:"Promo",event:"Kegiatan",news:"Kabar"};
function webHeadVal(){const N=((K.store.web||{}).news)||{},P=K.posts.filter(p=>!p.draft&&p.title);
  return N.headMode==="pick"&&P.some(p=>p.id===N.headId)?"p:"+N.headId:N.headMode==="off"?"off":"auto"}
function webHeadHTML(){const P=K.posts.filter(p=>!p.draft&&p.title),val=webHeadVal();
  return `<h3>Headline Kabar</h3><p class="note" style="margin-top:-6px">Kartu paling besar & paling atas di bagian Kabar website. Cocok untuk yang sedang ramai, misalnya final Liga LIPIA.</p>
  <label>Yang dijadikan headline<select data-wh data-init="${esc(val)}">${[["auto","Otomatis: kabar terbaru yang masih berlaku"],...P.map(p=>["p:"+p.id,(WTYPE[p.type]||"Kabar")+" · "+p.title]),["off","Tanpa headline"]]
    .map(([v,l])=>`<option value="${esc(v)}"${v===val?" selected":""}>${esc(l)}</option>`).join("")}</select></label>
  <p class="note">Bisa juga dari tab Kabar: buka promo/kabar → “Jadikan headline”.</p>`}
function webCardPh(img,name){return su(img)?`<img src="${su(img)}" alt="Foto ${esc(name)}">`:`<span>Foto bawaan website</span>`}
function webMenuHTML(){const A=D.prod.filter(p=>p.active);if(!A.length)return "";
  return `<h3>Kartu menu</h3><p class="note" style="margin-top:-6px">Nama, harga, deskripsi, dan status habis otomatis ikut menu di kasir. Keterangan kecil di bawah nama otomatis = <b>Kategori · Ukuran cup</b> dari Buku resep, atau tulis sendiri di sini.</p>
  ${A.map(p=>{const w=webMI(p),pend=webPend[p.id],img=pend!==undefined?pend:(w.img||""),auto=[p.cat,p.size].filter(Boolean).join(" · "),hide=w.lb==="";
    return `<div class="wmc" data-wm="${esc(p.id)}"><div class="wmc-ph">${webCardPh(img,p.name)}</div><div class="wmc-b"><b>${esc(p.name)}</b>
    <label>Keterangan kecil<input data-wl value="${esc(hide?"":(w.lb||""))}" maxlength="40" placeholder="${esc(auto||"mis. Kopi Susu · 170 ml")}"${hide?" disabled":""}></label>
    <p class="wmc-now">Tampil: <b data-wn>${esc(hide?"(tanpa keterangan)":(w.lb||auto||"(kosong)"))}</b></p>
    <label class="wmc-x"><input type="checkbox" data-wx${hide?" checked":""}> Tanpa keterangan</label>
    <label class="wmc-up">${img?"Ganti foto":"Pilih foto"}<input type="file" accept="image/*" data-wi></label>
    ${img?`<button class="btn ghost sm" data-a="wimgdel" data-v="${esc(p.id)}" style="margin:6px 0 0">Pakai foto bawaan website</button>`:""}</div></div>`}).join("")}
  <p class="note">Foto tegak 4:5, misalnya 1080 × 1350 px. Foto otomatis diperkecil supaya website tetap ringan.</p>`}
function webMenuSave(W){const old=K.store.web||{},mi=Object.assign({},old.mi||{});
  document.querySelectorAll("[data-wm]").forEach(el=>{const id=el.dataset.wm,x={},lb=el.querySelector("[data-wl]").value.trim(),hide=el.querySelector("[data-wx]").checked;
    if(hide)x.lb="";else if(lb)x.lb=lb.slice(0,40);
    const im=webPend[id]!==undefined?webPend[id]:(mi[id]||{}).img;if(im)x.img=im;
    if(Object.keys(x).length)mi[id]=x;else delete mi[id]});
  Object.keys(mi).forEach(id=>{if(!D.prod.some(p=>p.id===id))delete mi[id]});
  if(Object.keys(mi).length)W.mi=mi;
  const hs=document.querySelector("[data-wh]");W.news=W.news||{};
  /* headline hanya ditulis bila Owner mengubah pilihannya; selain itu pilihan sebelumnya dipertahankan */
  if(hs&&hs.value!==hs.dataset.init){const v=hs.value;if(v==="off")W.news.headMode="off";else if(v.indexOf("p:")===0){W.news.headMode="pick";W.news.headId=v.slice(2)}else W.news.headMode="auto"}
  else if(old.news&&old.news.headMode){W.news.headMode=old.news.headMode;if(old.news.headId)W.news.headId=old.news.headId}
  if(!Object.keys(W.news).length)delete W.news;
  webPend={}}
function kIsHead(p){if(p._head!==undefined)return p._head===1;const N=((K.store.web||{}).news)||{};return N.headMode==="pick"&&N.headId===p.id}
function kHeadSave(p,hd){if(hd===undefined)return;const W=K.store.web=K.store.web||{};W.news=W.news||{};
  if(hd){W.news.headMode="pick";W.news.headId=p.id}else if(W.news.headId===p.id){W.news.headMode="auto";delete W.news.headId}
  if(!Object.keys(W.news).length)delete W.news}
document.addEventListener("change",e=>{const t=e.target;if(!t||!t.matches)return;
  if(t.matches("[data-wi]")){const f=t.files&&t.files[0],box=t.closest("[data-wm]");if(!f||!box)return;const id=box.dataset.wm;
    box.querySelector(".wmc-ph").innerHTML="<span>Memproses foto…</span>";
    webShrink(f,d=>{webPend[id]=d;const p=prod(id);box.querySelector(".wmc-ph").innerHTML=webCardPh(d,p?p.name:"");toast("Foto dipilih. Ketuk “Simpan ke website”.")});return}
  if(t.matches("[data-wx]")){const box=t.closest("[data-wm]"),inp=box&&box.querySelector("[data-wl]");if(inp)inp.disabled=t.checked;webNowPaint(box)}},true);
document.addEventListener("input",e=>{const t=e.target;if(t&&t.matches&&t.matches("[data-wl]"))webNowPaint(t.closest("[data-wm]"))},true);
function webNowPaint(box){if(!box)return;const p=prod(box.dataset.wm),n=box.querySelector("[data-wn]");if(!p||!n)return;
  const hide=box.querySelector("[data-wx]").checked,lb=box.querySelector("[data-wl]").value.trim(),auto=[p.cat,p.size].filter(Boolean).join(" · ");
  n.textContent=hide?"(tanpa keterangan)":(lb||auto||"(kosong)")}
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-a]");if(!b)return;const a=b.dataset.a,v=b.dataset.v;
  if(a==="wimgdel"){e.preventDefault();e.stopImmediatePropagation();webPend[v]="";const box=b.closest("[data-wm]");if(box){box.querySelector(".wmc-ph").innerHTML=webCardPh("","");b.remove()}toast("Memakai foto bawaan website setelah disimpan.");return}
  if(a==="khead"&&typeof kp!=="undefined"&&kp){e.preventDefault();e.stopImmediatePropagation();kGrab();kp._head=v==="1"?1:0;kPostSheet();return}},true);
