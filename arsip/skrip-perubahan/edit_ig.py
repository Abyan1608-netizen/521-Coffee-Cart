s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
i=s.index('/* ---------- Animasi ---------- */');s=s[:i]+open('ig.css').read()+s[i:]
rep('function pubRender(){','''const igH=()=>String(K.store.ig||"").replace(/^@/,"").replace(/^https?:\\/\\/(www\\.)?instagram\\.com\\//,"").replace(/\\/.*$/,"").trim();
function kIG(m){const h=igH(),P=(K.store.igPosts||[]).filter(x=>x.img);if(!h&&!P.length&&!m)return "";
  const prof=h?`https://instagram.com/${encodeURIComponent(h)}`:"";
  return `<h2 class="k-h2" id="k-ig">Instagram${m?`<button class="k-add" data-a="kig">Atur Instagram</button>`:""}</h2><div class="k-ig"><div class="k-igtop"><span class="k-igav"><span><svg aria-hidden="true"><use href="#logo"/></svg></span></span><span><b>${h?"@"+esc(h):"Instagram belum diatur"}</b><small>${P.length?"Postingan terbaru · ketuk untuk buka":"Ikuti untuk kabar & promo terbaru"}</small></span>${prof?`<a class="k-igfollow" href="${prof}" target="_blank" rel="noopener">${ic("ig")}Ikuti</a>`:""}</div>
  ${P.length?`<div class="k-iggrid">${P.slice(0,9).map(x=>`<a href="${esc(/^https:\\/\\//.test(x.url||"")?x.url:prof||"#")}" target="_blank" rel="noopener" aria-label="Buka postingan Instagram"><img src="${x.img}" alt="" loading="lazy"></a>`).join("")}</div>`:""}</div>`}
function kIGSheet(){const P=K.store.igPosts=K.store.igPosts||[];
  show(`<h2>Instagram</h2><p class="note" style="margin-top:-4px">Tampil di halaman pelanggan: profil, tombol Ikuti, dan galeri postingan pilihan. Terlihat setelah Terbitkan.</p>
  <label>Username Instagram<input id="ig-h" value="${esc(K.store.ig||"")}" placeholder="@521coffee" autocapitalize="off"></label>
  <h3>Galeri postingan (maks. 9)</h3>${P.map((x,i)=>`<div class="igedit"><img src="${x.img}" alt="Postingan ${i+1}"><input data-ig="${i}" inputmode="url" value="${esc(x.url||"")}" placeholder="Link postingan (opsional)" aria-label="Link postingan ${i+1}"><button class="btn ghost sm" data-a="igdel" data-v="${i}" style="margin:0;color:var(--warn)">✕</button></div>`).join("")||'<p class="note">Belum ada postingan. Unggah screenshot atau foto postingan Instagram Anda.</p>'}
  ${P.length<9?`<label>Tambah foto postingan (bisa beberapa)<input id="igf" type="file" accept="image/*" multiple></label>`:""}
  <p class="note">Tips: buka postingan di Instagram → ⋯ → Salin tautan, lalu tempel di kolom link supaya pelanggan langsung ke postingan itu.</p>
  <button class="btn" data-a="igsave">Simpan</button>`)}
function igGrab(){const h=$("#ig-h");if(h)K.store.ig=h.value.trim();document.querySelectorAll("[data-ig]").forEach(el=>{const x=(K.store.igPosts||[])[+el.dataset.ig];if(x)x.url=el.value.trim()})}
function pubRender(){''')
rep('''  <h2 class="k-h2" id="k-menu">Menu</h2>''','''  ${kIG(m)}
  <h2 class="k-h2" id="k-menu">Menu</h2>''')
rep('''<a href="#k-menu">Menu</a>''','''${igH()||(K.store.igPosts||[]).length?'<a href="#k-ig">Instagram</a>':""}<a href="#k-menu">Menu</a>''')
# order sheet: DM Instagram option
rep('''  if(ordV==="shop")body=''','''  const ig=igH();if(ordV==="igdm")body=ig?`<div class="ordcard"><b>@${esc(ig)}</b><small class="mute">Kirim DM untuk tanya varian, pesan, atau kerja sama.</small><div class="ordbtns"><a class="btn sm" href="https://ig.me/m/${encodeURIComponent(ig)}" target="_blank" rel="noopener">${ic("ig")} DM Instagram</a><a class="btn ghost sm" href="https://instagram.com/${encodeURIComponent(ig)}" target="_blank" rel="noopener">Lihat profil</a></div></div>`:"";
  if(ordV==="shop")body=''')
rep('''  ${opt("shop","pos","E-commerce"''','''  ${ig?opt("igdm","ig","DM Instagram","@"+esc(ig))+(ordV==="igdm"?`<div class="ordbody">${body}</div>`:""):""}
  ${opt("shop","pos","E-commerce"''')
# manage button
rep('''<button class="qbtn" data-a="kord">Pesan sekarang</button>''','''<button class="qbtn" data-a="kord">Pesan sekarang</button><button class="qbtn" data-a="kig">Instagram</button>''')
# handlers (owner)
rep('''  else if(a==="kord")kOrderSheet();''','''  else if(a==="kord")kOrderSheet();
  else if(a==="kig")kIGSheet();
  else if(a==="igdel"){igGrab();K.store.igPosts.splice(+v,1);kIGSheet()}
  else if(a==="igsave"){igGrab();if((K.store.igPosts||[]).some(x=>x.url&&!/^https:\\/\\//.test(x.url))){toast("Link postingan harus diawali https://");return}shut();kChanged();toast("Tersimpan. Tekan Terbitkan agar pelanggan melihatnya.",1)}''')
rep('''  else if(t.id==="kbf"&&t.files''','''  else if(t.id==="igf"&&t.files&&t.files.length&&own()){igGrab();const P=K.store.igPosts=K.store.igPosts||[],room=9-P.length,list=[...t.files].slice(0,room);let done=0;
    list.forEach(f=>{const r=new FileReader();r.onload=()=>{const im=new Image();im.onload=()=>{try{const sz=Math.min(im.width,im.height),cv=document.createElement("canvas"),o=Math.min(640,sz);cv.width=cv.height=o;cv.getContext("2d").drawImage(im,(im.width-sz)/2,(im.height-sz)/2,sz,sz,0,0,o,o);P.push({img:cv.toDataURL("image/jpeg",.8),url:""})}catch(e){}if(++done===list.length){kIGSheet();toast(list.length+" foto ditambahkan",1)}};im.onerror=()=>{if(++done===list.length)kIGSheet()};im.src=r.result};r.readAsDataURL(f)})}
  else if(t.id==="kbf"&&t.files''')
# store sheet ig field kept; contact section already uses ig
open('p3.src.html','w').write(s);print('ok')
