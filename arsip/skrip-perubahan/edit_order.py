s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
i=s.index('/* ---------- Animasi ---------- */');s=s[:i]+open('order.css').read()+s[i:]
rep('function pubRender(){',open('order.js').read()+'\nfunction pubRender(){')
# CTA after info grid in kHead (both public & manage)
rep('''Buka di Google Maps</em></a>`:`<div><span>Lokasi</span><b>${esc(s.place||"-")}</b></div>`}</div>`}''','''Buka di Google Maps</em></a>`:`<div><span>Lokasi</span><b>${esc(s.place||"-")}</b></div>`}</div><button class="k-order" data-a="order">${ic("pos")} Pesan sekarang</button>`}''')
# floating button on public
rep('''<div class="k-foot"><svg class="mark" aria-hidden="true"><use href="#logo"/></svg>${esc(s.name)} · ${esc(s.tagline)}</div></div>`;''','''<div class="k-foot"><svg class="mark" aria-hidden="true"><use href="#logo"/></svg>${esc(s.name)} · ${esc(s.tagline)}</div></div><button class="k-fab" data-a="order">${ic("pos")} Pesan</button>`;''')
# manage button
rep('''<button class="qbtn" data-a="kbanner">Foto banner</button>''','''<button class="qbtn" data-a="kbanner">Foto banner</button><button class="qbtn" data-a="kord">Pesan sekarang</button>''')
# public handlers
rep('''  if(a==="ggo"){''','''  if(a==="order"){ordV="";orderSheet();return}
  if(a==="ordv"){ordV=ordV===v?"":v;orderSheet();return}
  if(a==="ggo"){''')
# owner handlers
rep('''  else if(a==="kbanner")kBannerSheet();''','''  else if(a==="kbanner")kBannerSheet();
  else if(a==="kord")kOrderSheet();
  else if(a==="ordradd"){ordGrab();kOrd().resellers.push({n:"",wa:"",loc:"",maps:""});kOrderSheet()}
  else if(a==="ordrdel"){ordGrab();kOrd().resellers.splice(+v,1);kOrderSheet()}
  else if(a==="ordsadd"){ordGrab();kOrd().shops.push({label:"",url:""});kOrderSheet()}
  else if(a==="ordsdel"){ordGrab();kOrd().shops.splice(+v,1);kOrderSheet()}
  else if(a==="ordsave"){ordGrab();const o=kOrd();const bad=o.shops.find(x=>x.url&&!/^https?:\\/\\//.test(x.url))||o.resellers.find(r=>r.maps&&!/^https:\\/\\//.test(r.maps));if(bad){toast("Link harus diawali https://");return}shut();kChanged();toast("Tersimpan. Tekan Terbitkan agar pelanggan melihatnya.",1)}''')
open('p3.src.html','w').write(s);print('ok')
