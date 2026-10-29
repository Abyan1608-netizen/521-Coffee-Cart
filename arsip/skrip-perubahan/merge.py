import re,json
s=open('p2.src.html').read()
def rep(a,b,cnt=1):
    global s
    assert s.count(a)==cnt,(s.count(a),a[:80])
    s=s.replace(a,b)
POS="https://claude.ai/artifact/3AdqCGi73y9hsp7Ls8b89x"; OLD="https://claude.ai/artifact/2wqVXCUtJHCucmRZF7UWYX"
# style id + css additions + hero var
rep('<style>\n/* Layout: login','<style id="css">\n/* Layout: login')
rep('  color-scheme:dark;\n}','  color-scheme:dark;--heroimg:url(__HERO__);\n}')
rep('.hero{background:#1a0d04 center/cover no-repeat;','.hero{background:#1a0d04 var(--heroimg) center/cover no-repeat;')
i=s.index('</style>'); s=s[:i]+open('kcss.css').read()+s[i:]
# body shell -> JS
a=s.index('__LOGO__\n'); b=s.index('<script src="https://cdnjs')
shell=s[a+len('__LOGO__\n'):b].strip()
shell=shell.replace(' style="background-image:url(__HERO__)"','')
shell=shell.replace('<section class="login" id="login">','<section id="pub" hidden></section>\n<section class="login" id="login" hidden>')
shell=shell.replace('<div class="lp">\n','<div class="lp">\n    <button class="back" data-a="tokabar">← Kabar & promo</button>\n',1)
assert '`' not in shell and '${' not in shell
s=s[:a]+'__LOGO__\n<div id="mount"></div>\n\n'+s[b:]
rep('<script>\nconst $=s=>','<script type="application/json" id="kdata">__KDATA__</script>\n<script id="app">\ndocument.getElementById("mount").innerHTML=`'+shell+'`;\nconst $=s=>')
# icons
rep("  mega:'","  user:'<circle cx=\"12\" cy=\"8.5\" r=\"3.8\"/><path d=\"M4.5 20a7.5 7.5 0 0 1 15 0\"/>',\n  cal:'<rect x=\"3.5\" y=\"5\" width=\"17\" height=\"15\" rx=\"2\"/><path d=\"M3.5 9.5h17M8 3v4M16 3v4\"/>',\n  pin:'<path d=\"M12 21s-6.5-5.6-6.5-11a6.5 6.5 0 0 1 13 0C18.5 15.4 12 21 12 21z\"/><circle cx=\"12\" cy=\"10\" r=\"2.3\"/>',\n  ig:'<rect x=\"4\" y=\"4\" width=\"16\" height=\"16\" rx=\"5\"/><circle cx=\"12\" cy=\"12\" r=\"3.6\"/><path d=\"M16.8 7.2h.01\"/>',\n  arrow:'<path d=\"M9 6l6 6-6 6\"/>',\n  mega:'")
# links
rep('promo:"'+OLD+'"};','promo:"'+POS+'"};')
rep('const PROMO_DEF="'+OLD+'"','const PROMO_DEF="'+POS+'"')
rep('if(!SW[d.cfg.color])d.cfg.color="ember";','if(!SW[d.cfg.color])d.cfg.color="ember";\n  if(!d.cfg.promo||d.cfg.promo==="'+OLD+'")d.cfg.promo="'+POS+'";')
# insert kabar module before Render section
rep('/* ---------- Render ---------- */',open('kjs.js').read()+'\n/* ---------- Render ---------- */')
rep('const V={pos,dash,stk,menu,set};','const V={pos,dash,stk,menu,set,kabar};')
rep('[["pos","Kasir","pos"],["dash","Ringkasan","dash"],["stk","Stok","stk"],["menu","Menu","menu"],["set","Atur","set"]]','[["pos","Kasir","pos"],["dash","Ringkasan","dash"],["stk","Stok","stk"],["menu","Menu","menu"],["kabar","Kabar","mega"],["set","Atur","set"]]')
# enter/logout
rep('function enter(){$("#login").hidden=true;','function enter(){$("#login").hidden=true;$("#pub").hidden=true;')
# settings section text
rep('<h3>Halaman promo pelanggan</h3><p class="note">Tempat pelanggan melihat promo, kegiatan, kabar, dan menu. Link ini ikut di struk WhatsApp, dan QR-nya bisa ditunjukkan di kasir.</p>','<h3>Halaman publik (Kabar & promo)</h3><p class="note">Orang yang membuka link aplikasi ini tanpa masuk akan melihat Kabar & promo. Tombol Masuk ada di pojok kanan atas. Link ini ikut di struk WhatsApp, dan QR-nya bisa ditunjukkan di kasir.</p>')
rep('''${c.promo?`<a class="btn ghost sm" href="${esc(c.promo)}" target="_blank" rel="noopener" style="margin:0">Buka & kelola halaman</a>`:""}''','''<button data-a="tab" data-v="kabar">Kelola kabar & promo</button>''')
rep('<p class="note">Agar pelanggan tanpa akun Claude bisa membuka, atur halaman itu ke “siapa saja yang punya link” lewat menu Share.</p>','<p class="note">Agar pelanggan tanpa akun Claude bisa membuka, atur aplikasi ini ke “siapa saja yang punya link” lewat menu Share. Data penjualan tetap aman karena hanya tersimpan di perangkat yang dipakai berjualan.</p>')
rep('${ic("mega")}QR promo pelanggan</button>','${ic("mega")}QR kabar & promo</button>')
# click handler public actions
rep('''  if(a==="kgo"){tryLogin(true);return}
  if(!me)return;''','''  if(a==="kgo"){tryLogin(true);return}
  if(a==="tokabar"){showPub();return}
  if(a==="masuk"){showLogin();return}
  if(a==="kcopy"){copy(v,"Kode "+v+" tersalin");return}
  if(a==="toapp"){if(me)enter();return}
  if(!me)return;''')
rep('''  else if(!own())return;''','''  else if(!own())return;
  else if(a==="kview")showPub();
  else if(a==="kstore")kStoreSheet();
  else if(a==="ksaves"){["headline","hours","place","wa","ig"].forEach(k=>K.store[k]=$("#s-"+k).value.trim());shut();kChanged()}
  else if(a==="knew"){kp={isNew:1,id:"k"+uid(),type:v,title:"",body:"",badge:"",start:"",end:"",code:"",date:"",time:"",place:"",draft:false,created:kToday()};kPostSheet()}
  else if(a==="ked"){const p=K.posts.find(x=>x.id===v);if(p){kp={...p};kPostSheet()}}
  else if(a==="ktog"){const p=K.posts.find(x=>x.id===v);if(p){p.draft=!p.draft;kChanged()}}
  else if(a==="kdel"){const p=K.posts.find(x=>x.id===v);if(p)confirmSheet(`Hapus “${esc(p.title)}”?`,"Hilang dari halaman pelanggan setelah Anda menekan Terbitkan.","kdelgo","Hapus","Jangan hapus",p.id)}
  else if(a==="kdelgo"){K.posts=K.posts.filter(x=>x.id!==id);shut();kChanged()}
  else if(a==="ksavep"){
    const g=q=>{const el=$(q);return el?el.value.trim():""};const t=g("#p-title");if(!t){$("#p-title").focus();return}
    Object.assign(kp,{title:t,body:g("#p-body"),badge:g("#p-badge"),start:g("#p-start"),end:g("#p-end"),code:g("#p-code").toUpperCase(),date:g("#p-date"),time:g("#p-time"),place:g("#p-place"),draft:$("#p-draft").checked});
    if(kp.start&&kp.end&&kp.end<kp.start){toast("Tanggal “Sampai” harus setelah “Mulai”.");return}
    const nw=kp.isNew;delete kp.isNew;if(nw)K.posts.push(kp);else K.posts=K.posts.map(x=>x.id===kp.id?kp:x);kp=null;shut();kChanged();toast(nw?"Ditambahkan. Tekan Terbitkan agar pelanggan melihatnya.":"Tersimpan. Tekan Terbitkan agar pelanggan melihatnya.",1)}
  else if(a==="kpublish")kPublish();''')
# startup
rep('if(me)enter();else loginView();','if(me)enter();else if(location.hash==="#masuk")showLogin();else showPub();\nsetInterval(()=>{if(!$("#pub").hidden&&$("#m").hidden)pubRender()},60000);')
# keydown in login only when visible -> already checks #login hidden
open('p3.src.html','w').write(s)
print("merged")
