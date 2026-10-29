s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
rep('''const waNum=n=>''','''const ORD_MSG="Assalamu’alaikum warahmatullahi wabarakaatuh\\nHalo, saya mau beli kopi 521 kak!\\n\\nBtw, ready varian apa yang ada sekarang?";
const ordMsg=()=>encodeURIComponent((K.store.order&&K.store.order.msg)||ORD_MSG);
const waNum=n=>''')
rep('''msg=encodeURIComponent("Halo 521 Coffee, saya mau pesan:\\n");''','''msg=ordMsg();''')
rep('''href="https://wa.me/${w}?text=${encodeURIComponent("Halo "+(r.n||"")+", saya mau pesan 521 Coffee:\\n")}"''','''href="https://wa.me/${w}?text=${msg}"''')
rep('''<small class="mute">Tulis menu, jumlah, dan alamat atau jam ambil. Kami balas secepatnya.</small>''','''<small class="mute">Pesan pembuka sudah terisi otomatis, tinggal kirim.</small>''')
rep('''  <h3>WhatsApp kami</h3><input id="o-wa" inputmode="tel" value="${esc(K.store.wa||"")}" placeholder="08xxxxxxxxxx" aria-label="Nomor WhatsApp toko">''','''  <h3>WhatsApp kami</h3><input id="o-wa" inputmode="tel" value="${esc(K.store.wa||"")}" placeholder="08xxxxxxxxxx" aria-label="Nomor WhatsApp toko">
  <label>Isi chat otomatis (untuk WA kami & reseller)<textarea class="kt" id="o-msg" rows="5">${esc(o.msg||ORD_MSG)}</textarea></label><button class="link" data-a="ordmsgdef" style="padding:0">Kembalikan ke teks awal</button>''')
rep('''function ordGrab(){const o=kOrd();const w=$("#o-wa");if(w)K.store.wa=w.value.trim();''','''function ordGrab(){const o=kOrd();const w=$("#o-wa");if(w)K.store.wa=w.value.trim();const m=$("#o-msg");if(m)o.msg=m.value.trim()===ORD_MSG?"":m.value.trim();''')
rep('''  else if(a==="ordradd"){''','''  else if(a==="ordmsgdef"){ordGrab();kOrd().msg="";kOrderSheet()}
  else if(a==="ordradd"){''')
open('p3.src.html','w').write(s);print('ok')
