s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
rep('''  <div class="two"><label>Kategori<input id="f-cat" data-f="cat" list="catl" value="${esc(e.cat)}"></label><label>Harga jual<input id="f-price" data-f="price" inputmode="numeric" value="${e.price||""}"></label></div><datalist id="catl">${cats.map(c=>`<option value="${esc(c)}">`).join("")}</datalist>''','''  <div class="lbl">Kategori</div><div class="chips" style="margin-top:6px">${cats.map(c=>`<button data-a="pcat" data-v="${esc(c)}" aria-pressed="${e.cat===c}">${esc(c)}</button>`).join("")}</div><p class="note" style="margin-top:-4px">Tambah atau ganti nama kategori di Atur → Kategori menu.</p>
  <label>Harga jual<input id="f-price" data-f="price" inputmode="numeric" value="${e.price||""}"></label>''')
rep('''  <div class="sec"><h3>Kasir</h3>''','''  <div class="sec" id="kat"><h3>Kategori menu</h3><p class="note" style="margin-top:-4px">Urutan di sini = urutan tombol kategori di kasir. Ketuk nama untuk mengganti nama; ganti ke nama kategori lain untuk menggabungkan.</p>
  <div class="list" style="background:var(--bg)">${c.cats.map((k,i)=>{const n=D.prod.filter(p=>p.cat===k).length;return `<div class="mrow"><button class="li" data-a="catren" data-v="${esc(k)}"><span><b>${esc(k)}</b><small class="mute">${n?n+" menu":"Belum ada menu"}</small></span><span class="mute">Ubah ›</span></button><button class="mv" data-a="catmv" data-id="${i}" data-v="-1" aria-label="Naikkan ${esc(k)}"${i?"":" disabled"}>↑</button><button class="mv" data-a="catmv" data-id="${i}" data-v="1" aria-label="Turunkan ${esc(k)}"${i<c.cats.length-1?"":" disabled"}>↓</button></div>`}).join("")}</div>
  <div class="add" style="margin-top:10px"><input id="catnew" placeholder="Kategori baru, misalnya Snack" aria-label="Kategori baru"><button class="btn sm" data-a="catadd">Tambah</button></div></div>
  <div class="sec"><h3>Kasir</h3>''')
rep('''  else if(a==="pcol"){ed.color=v;edSheet()}''','''  else if(a==="pcol"){ed.color=v;edSheet()}
  else if(a==="pcat"){ed.cat=v;edSheet()}
  else if(a==="catadd"){const k=$("#catnew").value.trim();if(!k){$("#catnew").focus();return}if(c.cats.some(x=>x.toLowerCase()===k.toLowerCase())){toast("Kategori itu sudah ada");return}c.cats.push(k);lg("Kategori baru",k);save();render();toast("Kategori "+k+" ditambahkan",1)}
  else if(a==="catmv"){const i=+id,j=i+(+v);if(j<0||j>=c.cats.length)return;[c.cats[i],c.cats[j]]=[c.cats[j],c.cats[i]];save();render()}
  else if(a==="catren"){const n=D.prod.filter(p=>p.cat===v).length;show(`<h2>Kategori “${esc(v)}”</h2><label>Nama kategori<input id="catnm" value="${esc(v)}"></label><p class="note">Kalau diganti ke nama kategori lain yang sudah ada, kedua kategori digabung.</p><button class="btn" data-a="catsave" data-v="${esc(v)}">Simpan</button>${n?`<p class="note">Kategori ini dipakai ${n} menu, jadi belum bisa dihapus. Pindahkan menunya dulu atau gabungkan dengan kategori lain.</p>`:`<button class="btn ghost" data-a="catdel" data-v="${esc(v)}" style="color:var(--warn)">Hapus kategori</button>`}`)}
  else if(a==="catsave"){const nk=$("#catnm").value.trim();if(!nk){$("#catnm").focus();return}if(nk!==v){const ex=c.cats.find(x=>x.toLowerCase()===nk.toLowerCase()&&x!==v);const tgt=ex||nk;D.prod.forEach(p=>{if(p.cat===v)p.cat=tgt});if(cat===v)cat=tgt;if(ex)c.cats=c.cats.filter(x=>x!==v);else c.cats=c.cats.map(x=>x===v?nk:x);lg(ex?"Gabung kategori":"Ganti nama kategori",v+" → "+tgt);save();toast(ex?v+" digabung ke "+tgt:"Nama kategori diganti",1)}shut()}
  else if(a==="catdel"){if(D.prod.some(p=>p.cat===v))return;c.cats=c.cats.filter(x=>x!==v);lg("Hapus kategori",v);save();shut();toast("Kategori dihapus",1)}''')
open('p3.src.html','w').write(s);print('ok')
