s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:80])
    s=s.replace(a,b)
rep('''function kCtl(p,m){return m?`<div class="k-ctl"><button data-a="ked" data-v="${p.id}">Ubah</button><button data-a="ktog" data-v="${p.id}">${p.draft?"Tampilkan":"Jadikan draf"}</button><button data-a="kdel" data-v="${p.id}">Hapus</button></div>`:""}''','''function kCtl(p,m){return m?`${p.draft?`<div class="k-dnote">${ic("alert")}<span>Draf: belum terlihat pelanggan.</span><button class="btn sm" data-a="ktog" data-v="${p.id}" style="margin:0">Tampilkan ke pelanggan</button></div>`:""}<div class="k-ctl"><button data-a="ked" data-v="${p.id}">Ubah</button>${p.draft?"":`<button data-a="ktog" data-v="${p.id}">Jadikan draf</button>`}<button data-a="kdel" data-v="${p.id}">Hapus</button></div>`:""}''')
rep('''const kPill=(p,m)=>p.draft?'<span class="pill">Draf</span>':''','''const kPill=(p,m)=>p.draft?'<span class="pill x">Draf</span>':''')
rep('.k-draft{opacity:.62;border-style:dashed!important}','.k-draft{border-style:dashed!important}\n.k-draft > *:not(.k-dnote):not(.k-ctl){opacity:.6}\n.k-dnote{display:flex;flex-wrap:wrap;align-items:center;gap:10px;margin-top:14px;padding:10px 12px;border-radius:14px;background:color-mix(in srgb,var(--warn) 10%,var(--sf2));border:1px solid color-mix(in srgb,var(--warn) 30%,var(--line));font-size:13px;font-weight:700}\n.k-dnote svg{color:var(--warn)}\n.k-dnote span{flex:1;min-width:140px}\n.k-ev .k-dnote,.k-ev .k-ctl{grid-column:auto}')
rep('''  <label class="chk"><input type="checkbox" id="p-draft" ${p.draft?"checked":""}> Simpan sebagai draf (belum terlihat pelanggan)</label>''','''  <div class="lbl">Tampil di halaman pelanggan?</div><div class="chips"><button data-a="kvis" data-v="1" aria-pressed="${!p.draft}">Ya, tampilkan</button><button data-a="kvis" data-v="0" aria-pressed="${!!p.draft}">Simpan sebagai draf</button></div>''')
rep('''const d=$("#p-draft");if(d)kp.draft=d.checked}''','''}''')
rep('''draft:$("#p-draft").checked});''','''draft:!!kp.draft});''')
rep('''  else if(a==="kimgdel"){kGrab();kp.img="";kPostSheet()}''','''  else if(a==="kimgdel"){kGrab();kp.img="";kPostSheet()}
  else if(a==="kvis"){kGrab();kp.draft=v==="0";kPostSheet()}''')
rep('''<span>${kdirty?"Ada perubahan yang belum terbit.":"Draf hanya terlihat di sini, tidak oleh pelanggan."}</span>''','''<span>${kdirty?"Ada perubahan yang belum terbit.":"Semua sudah terbit."}${K.posts.filter(p=>p.draft).length?` ${K.posts.filter(p=>p.draft).length} draf belum terlihat pelanggan.`:""}</span>''')
rep('''toast(nw?"Ditambahkan. Tekan Terbitkan agar pelanggan melihatnya.":"Tersimpan. Tekan Terbitkan agar pelanggan melihatnya.",1)}''','''toast(kp&&false?"":(nw?"Ditambahkan.":"Tersimpan.")+" Tekan Terbitkan agar pelanggan melihatnya.",1)}''')
open('p3.src.html','w').write(s);print('ok')
