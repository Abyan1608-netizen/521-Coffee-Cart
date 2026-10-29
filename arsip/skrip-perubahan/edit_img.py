s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
rep('.k-empty{text-align:center;','.k-img{display:block;width:100%;aspect-ratio:16/10;object-fit:cover;border-radius:16px;margin:0 0 14px;background:var(--sf2)}\n.k-promo .k-img{width:calc(100% + 36px);margin:-18px -18px 16px;border-radius:0}\n.k-ev .k-img{grid-column:1/-1;margin:0}\n.k-news .k-img{margin:8px 0 6px}\n.k-photo{display:flex;gap:12px;align-items:center;margin-top:8px}\n.k-photo img{width:96px;height:64px;object-fit:cover;border-radius:10px;border:1px solid var(--line)}\n.k-empty{text-align:center;')
rep('''return `<article class="k-promo${p.draft?" k-draft":""}">${p.badge''','''return `<article class="k-promo${p.draft?" k-draft":""}">${p.img?`<img class="k-img" src="${p.img}" alt="" loading="lazy">`:""}${p.badge''')
rep('''return `<article class="k-ev${p.draft?" k-draft":""}"><div class="k-date">''','''return `<article class="k-ev${p.draft?" k-draft":""}">${p.img?`<img class="k-img" src="${p.img}" alt="" loading="lazy">`:""}<div class="k-date">''')
rep('''<time>${kFmt(p.date||p.created)}</time><h3>${esc(p.title)}${kPill(p,m)}</h3>''','''<time>${kFmt(p.date||p.created)}</time><h3>${esc(p.title)}${kPill(p,m)}</h3>${p.img?`<img class="k-img" src="${p.img}" alt="" loading="lazy">`:""}''')
rep('''  <label>Keterangan<textarea class="kt" id="p-body"''','''  <div class="lbl">Foto (opsional)</div>${p.img?`<div class="k-photo"><img src="${p.img}" alt="Foto terpilih"><button class="btn ghost sm" data-a="kimgdel" style="margin:0">Hapus foto</button></div>`:""}<label style="margin-top:6px">${p.img?"Ganti foto":"Pilih foto dari galeri atau kamera"}<input id="p-img" type="file" accept="image/*"></label><p class="note" id="p-imgnote">Foto otomatis diperkecil supaya halaman tetap ringan.</p>
  <label>Keterangan<textarea class="kt" id="p-body"''')
# grab helper + handlers
rep('function kStoreSheet(){','''function kGrab(){const g=q=>{const el=$(q);return el?el.value.trim():undefined};const m={title:"#p-title",body:"#p-body",badge:"#p-badge",start:"#p-start",end:"#p-end",code:"#p-code",date:"#p-date",time:"#p-time",place:"#p-place"};for(const k in m){const v=g(m[k]);if(v!==undefined)kp[k]=v}const d=$("#p-draft");if(d)kp.draft=d.checked}
function kLoadImg(f){
  const n=$("#p-imgnote");if(n)n.textContent="Memproses foto…";
  const r=new FileReader();r.onload=()=>{const im=new Image();im.onload=()=>{try{const sc=Math.min(1,1000/Math.max(im.width,im.height)),cv=document.createElement("canvas");cv.width=Math.round(im.width*sc);cv.height=Math.round(im.height*sc);const x=cv.getContext("2d");x.fillStyle="#000";x.fillRect(0,0,cv.width,cv.height);x.drawImage(im,0,0,cv.width,cv.height);kGrab();kp.img=cv.toDataURL("image/jpeg",.78);kPostSheet()}catch(e){toast("Foto ini tidak bisa dipakai. Coba foto lain.")}};im.onerror=()=>toast("File ini bukan foto. Pilih file gambar.");im.src=r.result};r.readAsDataURL(f);
}
function kStoreSheet(){''')
rep('''  else if(a==="kpublish")kPublish();''','''  else if(a==="kpublish")kPublish();
  else if(a==="kimgdel"){kGrab();kp.img="";kPostSheet()}''')
rep('''  else if(t.id==="qf"&&t.files''','''  else if(t.id==="p-img"&&t.files&&t.files[0]&&kp){kLoadImg(t.files[0])}
  else if(t.id==="qf"&&t.files''')
rep('''function kChanged(){kdirty=true;try{sessionStorage.setItem("k521-pending",JSON.stringify(K))}catch(e){}if(me)render()}''','''function kChanged(){kdirty=true;try{sessionStorage.setItem("k521-pending",JSON.stringify(K))}catch(e){toast("Perubahan belum bisa disimpan sementara karena foto terlalu banyak. Tekan Terbitkan sekarang.")}if(me)render()}''')
open('p3.src.html','w').write(s);print('ok')
