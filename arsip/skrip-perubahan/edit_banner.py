s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
rep('.k-hero::after{','''.k-hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity .9s ease}
.k-hero img.on{opacity:1}
.k-dots{position:absolute;right:14px;bottom:20px;z-index:2;display:flex;gap:6px}
.k-dots i{width:7px;height:7px;border-radius:50%;background:rgba(255,255,255,.4)}
.k-dots i.on{background:#fff;width:18px;border-radius:4px}
.kbgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin:12px 0}
.kbgrid figure{margin:0;position:relative;border-radius:14px;overflow:hidden;border:1px solid var(--line);aspect-ratio:16/10;background:var(--sf2)}
.kbgrid img{width:100%;height:100%;object-fit:cover;display:block}
.kbgrid figcaption{position:absolute;inset:auto 6px 6px 6px;display:flex;gap:6px}
.kbgrid figcaption button{flex:1;border:0;border-radius:8px;padding:5px;font-size:12px;font-weight:700;background:rgba(11,8,6,.75);color:#fff}
.kbgrid .first{position:absolute;top:6px;left:6px;font-size:10px;font-weight:800;letter-spacing:.08em;text-transform:uppercase;background:var(--ac);color:var(--on);border-radius:6px;padding:2px 6px}
.k-hero::after{''')
rep('''function kHead(){const s=K.store,o=kOpen(s.hours);return `<div class="k-hero" role="img" aria-label="${esc(s.name||"521 Coffee")}">''','''function kHead(){const s=K.store,o=kOpen(s.hours),H=s.heroes||[];return `<div class="k-hero" role="img" aria-label="${esc(s.name||"521 Coffee")}">${H.map((h,i)=>`<img src="${h}" alt="" class="${i?"":"on"}">`).join("")}${H.length>1?`<div class="k-dots">${H.map((h,i)=>`<i class="${i?"":"on"}"></i>`).join("")}</div>`:""}''')
rep('''<button class="qbtn" data-a="kstore">Info toko & kontak</button>''','''<button class="qbtn" data-a="kbanner">Foto banner</button><button class="qbtn" data-a="kstore">Info toko & kontak</button>''')
rep('function kStoreSheet(){','''function kBannerSheet(){const H=K.store.heroes||[];
  show(`<h2>Foto banner</h2><p class="note" style="margin-top:-4px">Tampil paling atas di halaman pelanggan. Lebih dari satu foto akan bergantian otomatis setiap 5 detik.</p>
  ${H.length?`<div class="kbgrid">${H.map((h,i)=>`<figure><img src="${h}" alt="Foto banner ${i+1}">${i?"":'<span class="first">Pertama</span>'}<figcaption>${i?`<button data-a="kbfirst" data-v="${i}">Jadikan pertama</button>`:""}<button data-a="kbdel" data-v="${i}">Hapus</button></figcaption></figure>`).join("")}</div>`:`<div class="k-empty" style="margin:12px 0"><b>Masih memakai logo 521</b>Tambahkan foto gerobak, menu, atau suasana untuk menggantinya.</div>`}
  <label>${H.length?"Tambah foto":"Pilih foto"} (bisa beberapa sekaligus, maks. 6)<input id="kbf" type="file" accept="image/*" multiple></label>
  <p class="note" id="kbnote">Pakai foto mendatar. Foto otomatis diperkecil supaya halaman tetap cepat.${H.length?" Hapus semua foto untuk kembali ke logo 521.":""}</p>
  <button class="btn" data-a="close">Selesai</button>`)}
function kAddHeroes(files){
  const H=K.store.heroes=K.store.heroes||[],room=6-H.length;if(room<=0){toast("Maksimal 6 foto banner. Hapus salah satu dulu.");return}
  const list=[...files].slice(0,room);const n=$("#kbnote");if(n)n.textContent="Memproses "+list.length+" foto…";
  let done=0;list.forEach(f=>{const r=new FileReader();r.onload=()=>{const im=new Image();im.onload=()=>{try{const sc=Math.min(1,1400/Math.max(im.width,im.height)),cv=document.createElement("canvas");cv.width=Math.round(im.width*sc);cv.height=Math.round(im.height*sc);const x=cv.getContext("2d");x.fillStyle="#000";x.fillRect(0,0,cv.width,cv.height);x.drawImage(im,0,0,cv.width,cv.height);H.push(cv.toDataURL("image/jpeg",.8))}catch(e){}if(++done===list.length){kChanged();kBannerSheet();toast(list.length+" foto ditambahkan. Tekan Terbitkan agar pelanggan melihatnya.",1)}};im.onerror=()=>{if(++done===list.length){kChanged();kBannerSheet()}};im.src=r.result};r.readAsDataURL(f)});
  if(files.length>room)toast("Hanya "+room+" foto yang ditambahkan (maks. 6).");
}
function kStoreSheet(){''')
rep('''  else if(a==="kstore")kStoreSheet();''','''  else if(a==="kstore")kStoreSheet();
  else if(a==="kbanner")kBannerSheet();
  else if(a==="kbdel"){K.store.heroes.splice(+v,1);kChanged();kBannerSheet()}
  else if(a==="kbfirst"){const H=K.store.heroes;H.unshift(H.splice(+v,1)[0]);kChanged();kBannerSheet()}''')
rep('''  else if(t.id==="p-img"&&t.files''','''  else if(t.id==="kbf"&&t.files&&t.files.length&&own()){kAddHeroes(t.files)}
  else if(t.id==="p-img"&&t.files''')
rep('''setInterval(()=>{if(!$("#pub").hidden&&$("#m").hidden)pubRender()},60000);''','''setInterval(()=>{if(!$("#pub").hidden&&$("#m").hidden)pubRender()},60000);
setInterval(()=>{document.querySelectorAll(".k-hero").forEach(h=>{const I=h.querySelectorAll("img");if(I.length<2||!h.offsetParent)return;let i=[...I].findIndex(x=>x.classList.contains("on"));I[i].classList.remove("on");i=(i+1)%I.length;I[i].classList.add("on");h.querySelectorAll(".k-dots i").forEach((d,j)=>d.classList.toggle("on",j===i))})},5000);''')
open('p3.src.html','w').write(s);print('ok')
