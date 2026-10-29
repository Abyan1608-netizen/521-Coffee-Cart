s=open('p2.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:70]
    s=s.replace(a,b)
rep('<script>\nconst $=s=>','<script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>\n<script>\nconst $=s=>')
rep('.toast{position:fixed;left:50%;','.qrw{background:#fff;border-radius:22px;padding:18px;margin:8px auto;width:max-content;max-width:100%;box-shadow:0 20px 50px -20px var(--ac)}\n.qrw img,.qrw canvas{display:block;width:240px;height:240px;max-width:100%}\n.lnk{font:500 12px var(--f-m);color:var(--mute);background:var(--sf2);border-radius:10px;padding:10px 12px;overflow-wrap:anywhere;margin:10px 0 0;user-select:all}\n.qbtn{display:inline-flex;align-items:center;gap:8px;border:1px solid color-mix(in srgb,var(--ac) 40%,var(--line));background:var(--sf);color:var(--ac);border-radius:12px;padding:8px 12px;font-size:13px;font-weight:700}\n.toast{position:fixed;left:50%;')
rep('lastCh:"Offline Store",qris:"default",paper:32};','lastCh:"Offline Store",qris:"default",paper:32,promo:"https://claude.ai/artifact/2wqVXCUtJHCucmRZF7UWYX"};')
rep("  x:'<path d=\"M6 6l12 12M18 6 6 18\"/>',","  x:'<path d=\"M6 6l12 12M18 6 6 18\"/>',\n  mega:'<path d=\"M4 10v4h3l7 4V6L7 10z\"/><path d=\"M17.5 9.5a3.5 3.5 0 0 1 0 5\"/>',")
# greeting button
rep('''<span class="clk num" id="clk"></span></div>''','''<span style="display:flex;flex-direction:column;align-items:flex-end;gap:8px"><span class="clk num" id="clk"></span>${C().promo?`<button class="qbtn" data-a="promoqr">${ic("mega")}QR promo pelanggan</button>`:""}</span></div>''')
# wa text
rep('''"",c.foot].join("\\n")}''','''"",c.foot,...(c.promo?["","Promo & kegiatan terbaru: "+c.promo]:[])].join("\\n")}''')
# settings section, before Printer
rep('''  <div class="sec"><h3>Printer Bluetooth</h3>''','''  <div class="sec"><h3>Halaman promo pelanggan</h3><p class="note">Tempat pelanggan melihat promo, kegiatan, kabar, dan menu. Link ini ikut di struk WhatsApp, dan QR-nya bisa ditunjukkan di kasir.</p>
  <label>Link halaman<input id="c-promo" data-c="promo" value="${esc(c.promo||"")}" placeholder="https://claude.ai/artifact/..."></label>
  <div class="chips"><button data-a="promoqr">Tampilkan QR</button>${c.promo?`<a class="btn ghost sm" href="${esc(c.promo)}" target="_blank" rel="noopener" style="margin:0">Buka & kelola halaman</a>`:""}</div>
  <p class="note">Agar pelanggan tanpa akun Claude bisa membuka, atur halaman itu ke “siapa saja yang punya link” lewat menu Share.</p></div>
  <div class="sec"><h3>Printer Bluetooth</h3>''')
# handler
rep('''  else if(a==="close")shut();''','''  else if(a==="close")shut();
  else if(a==="promoqr"){const L=(c.promo||"").trim();if(!/^https?:\\/\\//.test(L)){toast("Isi link halaman promo dulu di Atur.");return}
    show(`<h2>Scan untuk promo & kegiatan</h2><p class="mute" style="margin-top:-4px">Arahkan kamera HP pelanggan ke kode ini.</p><div class="qrw" id="qrw"></div><div class="lnk">${esc(L)}</div><button class="btn ghost" data-a="copyl">${ic("copy")} Salin link</button>`);
    try{new QRCode($("#qrw"),{text:L,width:480,height:480,colorDark:"#160c03",colorLight:"#ffffff",correctLevel:QRCode.CorrectLevel.M})}catch(err){$("#qrw").hidden=true}}
  else if(a==="copyl")copy((c.promo||"").trim(),"Link tersalin");''')
open('p2.src.html','w').write(s)
import base64,re
s=s.replace('__LOGO__',open('logo.sym').read().strip())
s=s.replace('__HERO__','data:image/jpeg;base64,'+base64.b64encode(open('hero.jpg','rb').read()).decode()).replace('__QRIS__','data:image/jpeg;base64,'+base64.b64encode(open('qris.jpg','rb').read()).decode())
open('premium.html','w').write(s)
open('t7.js','w').write(re.search(r'<script>\n(.*)</script>',s,re.S).group(1))
print('ok')
