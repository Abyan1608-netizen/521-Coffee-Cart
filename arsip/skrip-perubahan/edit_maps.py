s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
rep('.k-info b{display:block;font-size:15px;overflow-wrap:anywhere}','''.k-info b{display:block;font-size:15px;overflow-wrap:anywhere}
.k-info a{display:block;text-decoration:none;color:inherit;background:var(--sf);border:1px solid color-mix(in srgb,var(--ac) 35%,var(--line));border-radius:16px;padding:12px 14px;min-width:0;transition:border-color .15s}
.k-info a:hover{border-color:var(--ac)}
.k-info a em{display:inline-flex;align-items:center;gap:4px;font-style:normal;font-size:12px;font-weight:700;color:var(--ac);margin-top:4px}
.k-info a em svg{width:14px;height:14px}''')
rep('''<div class="k-info"><div><span>Jam buka</span><b>${esc(s.hours||"-")}</b></div><div><span>Lokasi</span><b>${esc(s.place||"-")}</b></div></div>`}''','''<div class="k-info"><div><span>Jam buka</span><b>${esc(s.hours||"-")}</b></div>${/^https:\\/\\//.test(s.maps||"")?`<a href="${esc(s.maps)}" target="_blank" rel="noopener" aria-label="Buka lokasi di Google Maps"><span>Lokasi</span><b>${esc(s.place||"Lihat di peta")}</b><em>${ic("pin")}Buka di Google Maps</em></a>`:`<div><span>Lokasi</span><b>${esc(s.place||"-")}</b></div>`}</div>`}''')
rep('''<div class="two"><label>Jam buka<input id="s-hours" value="${esc(s.hours)}" placeholder="05.00–21.00"></label><label>Lokasi<input id="s-place" value="${esc(s.place)}"></label></div>''','''<div class="two"><label>Jam buka<input id="s-hours" value="${esc(s.hours)}" placeholder="05.00–21.00"></label><label>Lokasi<input id="s-place" value="${esc(s.place)}"></label></div>
  <label>Link Google Maps<input id="s-maps" inputmode="url" value="${esc(s.maps)}" placeholder="https://maps.app.goo.gl/..."></label><p class="note" style="margin-top:2px">Di Google Maps: buka lokasi → Bagikan → Salin link. Kotak Lokasi di halaman pelanggan jadi bisa diketuk.</p>''')
rep('''["headline","hours","place","wa","ig"].forEach(k=>K.store[k]=$("#s-"+k).value.trim());''','''["headline","hours","place","wa","ig","maps"].forEach(k=>K.store[k]=$("#s-"+k).value.trim());if(K.store.maps&&!/^https:\\/\\//.test(K.store.maps)){toast("Link Google Maps harus diawali https://");return}''')
open('p3.src.html','w').write(s);print('ok')
