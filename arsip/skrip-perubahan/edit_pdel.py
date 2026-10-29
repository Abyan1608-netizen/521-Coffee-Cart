s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
old_start='''  else if(a==="catren"){const n=D.prod.filter(p=>p.cat===v).length;show('''
i=s.index(old_start);j=s.index('\n',i)
s=s[:i]+'''  else if(a==="catren"){catSheet(v)}'''+s[j:]
rep('''  else if(a==="catdel"){''','''  else if(a==="pdel"){const p=prod(id);if(p)confirmSheet(`Hapus menu “${esc(p.name)}”?`,"Menu hilang dari kasir, buku resep, dan halaman Kabar (setelah Terbitkan). Riwayat penjualan tetap tersimpan.","pdelgo","Hapus menu","Jangan hapus",p.id)}
  else if(a==="pdelgo"){const p=prod(id);if(!p)return;D.prod=D.prod.filter(x=>x.id!==id);delete cart[id];lg("Hapus menu",p.name);save();shut();toast(p.name+" dihapus",1)}
  else if(a==="catmvdel"){const t=$("#catmvsel").value;if(!t||t===v)return;D.prod.forEach(p=>{if(p.cat===v)p.cat=t});c.cats=c.cats.filter(x=>x!==v);if(cat===v)cat="Semua";lg("Hapus kategori",v+" (menu pindah ke "+t+")");save();shut();toast("Menu dipindah ke "+t+", kategori "+v+" dihapus",1)}
  else if(a==="catdelall"){const n=D.prod.filter(p=>p.cat===v).length;confirmSheet(`Hapus kategori “${esc(v)}” dan ${n} menunya?`,"Semua menu di kategori ini ikut terhapus dari kasir, buku resep, dan halaman Kabar. Riwayat penjualan tetap tersimpan. Ini tidak bisa dibatalkan.","catdelallgo","Hapus semua","Jangan hapus",v)}
  else if(a==="catdelallgo"){const gone=D.prod.filter(p=>p.cat===id);gone.forEach(p=>delete cart[p.id]);D.prod=D.prod.filter(p=>p.cat!==id);c.cats=c.cats.filter(x=>x!==id);if(cat===id)cat="Semua";lg("Hapus kategori + menu",id+" ("+gone.length+" menu)");save();shut();toast("Kategori "+id+" dan "+gone.length+" menu dihapus",1)}
  else if(a==="catdel"){''')
rep('function set(){','''function catSheet(v){
  const P=D.prod.filter(p=>p.cat===v),others=C().cats.filter(x=>x!==v);
  show(`<h2>Kategori “${esc(v)}”</h2><label>Nama kategori<input id="catnm" value="${esc(v)}"></label><p class="note">Kalau diganti ke nama kategori lain yang sudah ada, kedua kategori digabung.</p><button class="btn" data-a="catsave" data-v="${esc(v)}">Simpan nama</button>
  <h3>Menu di kategori ini (${P.length})</h3>${P.length?`<div class="list" style="background:var(--bg)">${P.map(p=>`<div class="mrow"><span class="li" style="cursor:default"><span><b>${esc(p.name)}</b>${p.active?"":'<span class="pill">Disembunyikan</span>'}<small class="mute num">${rp(p.price)}</small></span></span><button class="mini" data-a="edit" data-id="${p.id}" style="color:var(--ink)">Ubah</button><button class="mini" data-a="pdel" data-id="${p.id}">Hapus</button></div>`).join("")}</div>`:'<p class="note">Belum ada menu.</p>'}
  <h3>Hapus kategori</h3>${P.length?`${others.length?`<label>Pindahkan ${P.length} menu ke<select id="catmvsel">${others.map(o=>`<option>${esc(o)}</option>`).join("")}</select></label><button class="btn ghost" data-a="catmvdel" data-v="${esc(v)}">Pindahkan menu & hapus kategori</button>`:""}<button class="btn danger" data-a="catdelall" data-v="${esc(v)}">Hapus kategori + ${P.length} menunya</button>`:`<button class="btn ghost" data-a="catdel" data-v="${esc(v)}" style="color:var(--warn)">Hapus kategori</button>`}`);
}
function set(){''')
# delete in edSheet
rep('''${e.isNew?"":`<button class="btn ghost" data-a="togp">${e.active?"Sembunyikan dari kasir":"Tampilkan lagi di kasir"}</button>`}`);''','''${e.isNew?"":`<button class="btn ghost" data-a="togp">${e.active?"Sembunyikan dari kasir":"Tampilkan lagi di kasir"}</button><button class="btn ghost" data-a="pdel" data-id="${e.id}" style="color:var(--warn)">Hapus menu</button>`}`);''')
open('p3.src.html','w').write(s);print('ok')
