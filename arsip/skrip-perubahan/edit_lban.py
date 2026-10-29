s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
rep('<div class="hero" role="img" aria-label="Logo 521 Coffee Cart">','<div class="hero" id="lhero" role="img" aria-label="Logo 521 Coffee Cart">')
rep('function loginView(){','''let loginT=0;
function loginBanner(){
  const h=$("#lhero");if(!h)return;const L=(K.store&&K.store.login)||{},I=L.imgs||[],sec=Math.max(2,Math.min(30,+L.sec||5)),z=L.zoom||"in";
  h.style.setProperty("--zanim",z==="out"?"kzout":z==="none"?"none":"kzin");h.style.setProperty("--zdur",(sec+1.2)+"s");
  h.classList.toggle("single",I.length===1);
  h.innerHTML=I.length?I.map((u,i)=>`<img src="${u}" alt="" class="${i?"":"on"}">`).join("")+(I.length>1?`<div class="k-dots">${I.map((u,i)=>`<i class="${i?"":"on"}"></i>`).join("")}</div>`:""):'<div class="brandart"><svg aria-hidden="true"><use href="#logo"/></svg><span>Coffee Cart</span></div>';
  clearInterval(loginT);if(I.length>1)loginT=setInterval(()=>{if(h.offsetParent===null)return;const im=h.querySelectorAll("img"),dt=h.querySelectorAll(".k-dots i");let i=[...im].findIndex(x=>x.classList.contains("on"));im[i].classList.remove("on");i=(i+1)%im.length;void im[i].offsetWidth;im[i].classList.add("on");dt.forEach((d,j)=>d.classList.toggle("on",j===i))},sec*1000);
}
function loginView(){
  loginBanner();''')
rep('.k-hero::after{','''.hero img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;transition:opacity 1s ease}
.hero img.on{opacity:1;animation:var(--zanim,kzin) var(--zdur,6s) ease-out forwards}
.hero.single img.on{animation-iteration-count:infinite;animation-direction:alternate;animation-timing-function:ease-in-out}
.hero .k-dots{bottom:auto;top:16px;right:16px}
@keyframes kzin{from{transform:scale(1)}to{transform:scale(1.14)}}
@keyframes kzout{from{transform:scale(1.14)}to{transform:scale(1)}}
.lbgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:8px;margin:8px 0}
.lbgrid figure{margin:0;position:relative;border-radius:12px;overflow:hidden;border:1px solid var(--line);aspect-ratio:3/4;background:var(--sf2)}
.lbgrid img{width:100%;height:100%;object-fit:cover;display:block}
.lbgrid figcaption{position:absolute;inset:auto 4px 4px 4px;display:flex;gap:4px}
.lbgrid figcaption button{flex:1;border:0;border-radius:7px;padding:4px;font-size:11px;font-weight:700;background:rgba(11,8,6,.75);color:#fff}
.k-hero::after{''')
# Tampilan body: add login banner section before Warna utama
rep('''  <div class="lbl">Warna utama</div>''','''  <h3>Banner layar login</h3>${(()=>{const L=K.store.login||{},I=L.imgs||[],sec=+L.sec||5,z=L.zoom||"in";return `<p class="note" style="margin-top:-4px">Foto di sisi kiri (laptop) atau atas (HP) layar login. Kosongkan untuk memakai logo 521.</p>
  ${I.length?`<div class="lbgrid">${I.map((u,i)=>`<figure><img src="${u}" alt="Banner login ${i+1}"><figcaption>${i?`<button data-a="lbfirst" data-v="${i}">Pertama</button>`:""}<button data-a="lbdel" data-v="${i}">Hapus</button></figcaption></figure>`).join("")}</div>`:""}
  <label>${I.length?"Tambah foto":"Pilih foto"} (bisa beberapa, maks. 6)<input id="lbf" type="file" accept="image/*" multiple></label>
  <div class="lbl">Ganti foto setiap</div><div class="chips">${[3,5,8,10,15].map(x=>`<button data-a="lbsec" data-v="${x}" aria-pressed="${sec===x}">${x} detik</button>`).join("")}</div>
  <div class="lbl">Efek zoom</div><div class="chips">${[["in","Zoom in"],["out","Zoom out"],["none","Tanpa zoom"]].map(o=>`<button data-a="lbzoom" data-v="${o[0]}" aria-pressed="${z===o[0]}">${o[1]}</button>`).join("")}</div>
  <div class="chips"><button data-a="masuk">Lihat layar login</button></div>
  <p class="note">${kdirty?"Ada perubahan yang belum terbit. Tekan Terbitkan di tab Kabar atau ":"Tersimpan. "}Banner login terlihat di semua perangkat setelah diterbitkan.${kdirty?' <button class="link" data-a="kpublish" style="padding:0">Terbitkan sekarang</button>':""}</p>`})()}
  <div class="lbl">Warna utama</div>''')
rep('''  else if(a==="uitheme"){''','''  else if(a==="lbdel"){K.store.login.imgs.splice(+v,1);kChanged()}
  else if(a==="lbfirst"){const I=K.store.login.imgs;I.unshift(I.splice(+v,1)[0]);kChanged()}
  else if(a==="lbsec"){K.store.login=K.store.login||{};K.store.login.sec=+v;kChanged();toast("Foto berganti setiap "+v+" detik",1)}
  else if(a==="lbzoom"){K.store.login=K.store.login||{};K.store.login.zoom=v;kChanged()}
  else if(a==="uitheme"){''')
rep('''  else if(t.id==="uiglass"){''','''  else if(t.id==="lbf"&&t.files&&t.files.length&&own()){const L=K.store.login=K.store.login||{},I=L.imgs=L.imgs||[],room=6-I.length;if(room<=0){toast("Maksimal 6 foto. Hapus salah satu dulu.");return}const list=[...t.files].slice(0,room);let done=0;
    list.forEach(f=>{const r=new FileReader();r.onload=()=>{const im=new Image();im.onload=()=>{try{const sc=Math.min(1,1400/Math.max(im.width,im.height)),cv=document.createElement("canvas");cv.width=Math.round(im.width*sc);cv.height=Math.round(im.height*sc);const x=cv.getContext("2d");x.drawImage(im,0,0,cv.width,cv.height);I.push(cv.toDataURL("image/jpeg",.8))}catch(e){}if(++done===list.length){kChanged();toast(list.length+" foto banner login ditambahkan",1)}};im.onerror=()=>{if(++done===list.length)kChanged()};im.src=r.result};r.readAsDataURL(f)})}
  else if(t.id==="uiglass"){''')
open('p3.src.html','w').write(s);print('ok')
