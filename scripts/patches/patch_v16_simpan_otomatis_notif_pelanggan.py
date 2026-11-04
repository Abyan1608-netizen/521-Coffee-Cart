"""Perubahan 16: tombol "Terbitkan" diganti "Simpan" (HP Owner langsung menerbitkan otomatis, tidak tersangkut di "Menerbitkan…");
notifikasi pelanggan (promo/diskon/kabar/kegiatan) bisa dikirim langsung saat terbit DAN/ATAU pada beberapa jam pilihan;
saat aplikasi terbuka, promo baru tampil sebagai pemberitahuan + suara. Sekali jalan."""
import pathlib, re, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V16-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


# ------------------------------------------------------------------ CSS
rep(".hubn{", """/*V16-PATCH*/
.kst{display:flex;gap:8px;align-items:center;margin:14px 0 4px;padding:12px 14px;border-radius:14px;background:var(--sf);border:1px solid var(--line);font-size:14px;font-weight:700;color:var(--ink)}
.kst.ok{color:var(--ok)}.kst.wait i{width:10px;height:10px;border-radius:50%;background:var(--ac);flex:none;animation:kpulse 1s infinite alternate}
@keyframes kpulse{from{opacity:.35}to{opacity:1}}
.nfc .nfnow{grid-column:1/-1;margin:2px 0 0}
.nfc .nfnow span{color:var(--ink);font-weight:600;font-size:14px}
.hubn{""")

# ------------------------------------------------------------------ 1. Simpan = langsung terbit (HP Owner), tanpa tombol Terbitkan
rep('function kChanged(){kdirty=kHash(JSON.stringify(K))!==K_BASE;',
    'function kChanged(){kdirty=kHash(JSON.stringify(K))!==K_BASE;if(kdirty)kAuto();')
rep('''async function kPublish(){
  if(!AR){toast("Menerbitkan hanya bisa dari aplikasi Claude dengan akun pemilik halaman.");return}
  const b=$("[data-a=kpublish]");if(b){b.disabled=true;b.textContent="Menerbitkan…"}''',
    '''async function kPublish(auto){
  if(!AR){if(!auto)toast("Tersimpan di HP ini. Agar terlihat pelanggan, ubah dari HP Owner.");return}
  if(kPubBusy){kAuto(1500);return}kPubBusy=true;clearTimeout(kAutoT);
  const b=$("[data-a=kpublish]");if(b){b.disabled=true;b.textContent="Menyimpan…"}''')
rep('''D.cfg.teamAt=new Date().toISOString();try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}}toast("Terbit. Pelanggan sudah bisa melihatnya.",1)}''',
    '''D.cfg.teamAt=new Date().toISOString();try{localStorage.setItem("pos521",JSON.stringify(D))}catch(e){}}kPubBusy=false;kFail=0;toast(auto?"Tersimpan ✓ Pelanggan sudah bisa melihatnya.":"Tersimpan ✓ Langsung terlihat di semua HP & pelanggan.",1);if(me&&$("#m").hidden)render();else if(!$("#pub").hidden)pubRender()}''')
rep('''else toast("Belum berhasil terbit. Coba lagi sebentar.");if(b){b.disabled=false;b.textContent="Terbitkan"}}''',
    '''else{kFail++;if(!auto||kFail===1)toast("Tersimpan di HP ini. Belum terkirim ke pelanggan (cek internet), dicoba lagi otomatis.");kAuto(Math.min(120000,15000*kFail))}kPubBusy=false;if(b&&b.isConnected){b.disabled=false;b.textContent="Simpan"}if(me&&$("#m").hidden)render()}''')
# menu otomatis tidak bersamaan dengan Simpan
rep('if(msBusy||!AR||!kcan||!me||!teamReady||!kSync())return;', 'if(msBusy||kPubBusy||!AR||!kcan||!me||!teamReady||!kSync())return;')

# status di tab Kabar & pengaturan, tanpa tombol Terbitkan
rep('''${kNeed()?"● Ada perubahan yang belum terbit":"✓ Semua sudah terbit"}''', '''${kNeed()?(AR&&kcan?"⏳ Menyimpan…":"● Tersimpan di HP ini, belum terlihat pelanggan"):"✓ Semua tersimpan & terlihat pelanggan"}''')
rep('''${kNeed()?`<div class="k-pub"><span>${kdirty?"":"Menu atau nama toko berubah. "}Ada perubahan yang belum terbit.${K.posts.filter(p=>p.draft).length?` ${K.posts.filter(p=>p.draft).length} draf belum terlihat pelanggan.`:""}</span><button class="btn" data-a="kpublish">Terbitkan</button></div>`:""}''',
    '''${kStat()}''')
rep('''${kNeed()&&can("kabar")?`<div class="k-note" style="justify-content:space-between;flex-wrap:wrap">${ic("mega")}<span style="flex:1;min-width:160px">Ada perubahan yang belum terbit ke pelanggan.</span><button class="btn sm" data-a="kpublish" style="margin:0">Terbitkan</button></div>`:`<p class="note">Perubahan tampil ke pelanggan setelah Anda menekan <b>Terbitkan</b>.</p>`}''',
    '''${kStat()}''')
rep('''<p class="note">${kNeed()?"Ada perubahan yang belum terbit. Tekan Terbitkan di tab Kabar atau ":"Tersimpan. "}Banner login terlihat di semua perangkat setelah diterbitkan.${kNeed()?' <button class="link" data-a="kpublish" style="padding:0">Terbitkan sekarang</button>':""}</p>''',
    '''${kStat()}''')
rep('''${kNeed()?`<button class="btn" data-a="kpublish">Simpan & terbitkan</button><p class="note">Perubahan jam buka baru terlihat pelanggan setelah diterbitkan.</p>`:`<p class="note">✓ Jadwal sudah terbit di halaman pelanggan.</p>`}''',
    '''${kNeed()?`<button class="btn" data-a="kpublish">Simpan</button>`:""}${kStat()}''')
rep('<button class="btn" data-a="nfsave">${AR&&kcan?"Simpan & terbitkan":"Simpan"}</button>', '<button class="btn" data-a="nfsave">Simpan</button>')
rep('''<p class="note">${AR&&kcan?"Langsung berlaku untuk semua HP tim & pelanggan.":"Tersimpan di HP ini. Agar sampai ke pelanggan & HP lain, terbitkan dari HP Owner."}''',
    '''<p class="note">${AR&&kcan?"Langsung berlaku untuk semua HP tim & pelanggan.":"Tersimpan di HP ini. Agar sampai ke pelanggan & HP lain, ubah dari HP Owner."}''')
rep('if(AR&&kcan){kPublish()}else toast("Pengaturan notifikasi tersimpan di HP ini",1)}', 'if(AR&&kcan){kPublish()}else toast("Pengaturan notifikasi tersimpan di HP ini. Ubah dari HP Owner supaya berlaku di semua HP.",1)}')
# teks lama yang menyuruh menekan Terbitkan
for a, b in [
    (" · terlihat setelah Terbitkan", ""),
    ("Atur pilihan pesan di halaman pelanggan. Terlihat setelah Terbitkan.", "Atur pilihan pesan di halaman pelanggan. Langsung terlihat setelah disimpan."),
    ("dan galeri postingan pilihan. Terlihat setelah Terbitkan.", "dan galeri postingan pilihan. Langsung terlihat setelah disimpan."),
    (" foto ditambahkan. Tekan Terbitkan agar pelanggan melihatnya.", " foto ditambahkan."),
    ("Perubahan belum bisa disimpan sementara karena foto terlalu banyak. Tekan Terbitkan sekarang.", "Foto terlalu banyak untuk disimpan sementara. Kurangi foto, lalu simpan lagi."),
    ("Testimoni tersimpan. Tekan Terbitkan agar pelanggan melihatnya.", "Testimoni tersimpan."),
    ("Tersimpan. Tekan Terbitkan agar pelanggan melihatnya.", "Tersimpan."),
    ("Hilang dari halaman pelanggan setelah Anda menekan Terbitkan.", "Langsung hilang dari halaman pelanggan."),
    (" Tekan Terbitkan agar pelanggan melihatnya.", ""),
    ("Menu hilang dari kasir, buku resep, dan halaman Kabar (setelah Terbitkan).", "Menu hilang dari kasir, buku resep, dan halaman Kabar."),
    ("Tekan Terbitkan agar pelanggan melihat tampilan ini", "Tampilan tersimpan"),
    ("Tekan Simpan & terbitkan agar dipakai.", "Tekan Simpan agar dipakai."),
    ("lalu Simpan & terbitkan.", "lalu Simpan."),
    ("Tekan Simpan & terbitkan.", "Tekan Simpan."),
]:
    if a not in s:
        raise SystemExit("Tidak ditemukan: " + a)
    s = s.replace(a, b)

# ------------------------------------------------------------------ 2. Notifikasi pelanggan: langsung saat terbit + beberapa jam pilihan
rep('''["exp","low"].forEach(k=>{const x=c[k],ok=t=>/^\\d{2}:\\d{2}$/.test(t);''',
    '''["promo","diskon","kabar","event"].forEach(k=>{const x=c[k],ok=t=>/^\\d{2}:\\d{2}$/.test(t);x.times=Array.isArray(x.times)?[...new Set(x.times.filter(ok))].sort().slice(0,8):[];x.now=x.now===0?0:1});
  ["exp","low"].forEach(k=>{const x=c[k],ok=t=>/^\\d{2}:\\d{2}$/.test(t);''')
rep('const nfTimesUI=x=>`<div class="nftw"><span>Jam pengingat (bisa lebih dari satu)</span><div class="nftimes">${tChips(x.times)}</div>',
    'const nfTimesUI=(x,cust)=>`<div class="nftw"${cust?\' data-empty="1"\':""}><span>${cust?"Kirim juga pada jam (tiap hari selama masih berlaku, boleh kosong)":"Jam pengingat (bisa lebih dari satu)"}</span><div class="nftimes">${tChips(x.times)||(cust?\'<small class="mute">Belum ada jam</small>\':"")}</div>')
rep('function nfTimeDel(b){const w=b.closest(".nftw"),c=b.closest(".tchip");if(!w||!c)return;if(w.querySelectorAll(".tchip").length<2){toast("Minimal satu jam pengingat");return}c.remove()}',
    'function nfTimeDel(b){const w=b.closest(".nftw"),c=b.closest(".tchip");if(!w||!c)return;if(w.dataset.empty!=="1"&&w.querySelectorAll(".tchip").length<2){toast("Minimal satu jam pengingat");return}c.remove();if(!w.querySelector(".tchip")&&w.dataset.empty==="1")w.querySelector(".nftimes").innerHTML=\'<small class="mute">Belum ada jam</small>\'}')
rep('''    ${k==="low"?nfTimesUI(x):""}''',
    '''    ${k==="low"?nfTimesUI(x):""}
    ${staffOnly?"":`<label class="fgck nfnow"><input type="checkbox" class="nfnowc" ${x.now!==0?"checked":""}><span>Kirim langsung saat diterbitkan</span></label>${nfTimesUI(x,1)}`}''')
rep('''if(ti&&ok(ti.value)&&!T.includes(ti.value)&&T.length<8)T.push(ti.value);if(T.length){x.times=[...new Set(T)].sort();x.time=x.times[0]}}''',
    '''if(ti&&ok(ti.value)&&!T.includes(ti.value)&&T.length<8)T.push(ti.value);if(tw.dataset.empty==="1")x.times=[...new Set(T)].sort();else if(T.length){x.times=[...new Set(T)].sort();x.time=x.times[0]}}
    const nw=el.querySelector(".nfnowc");if(nw)x.now=nw.checked?1:0;''')
rep('Promo/diskon/kabar sampai ke pelanggan yang memasang aplikasi dalam ±15–30 menit setelah diterbitkan (langsung saat aplikasi dibuka).',
    'Promo/diskon/kabar baru sampai ke HP yang memasang aplikasi dalam ±15–30 menit setelah disimpan (langsung saat aplikasi dibuka). Bisa juga dikirim tepat pada jam-jam pilihan, tiap hari selama masih berlaku (tanpa tanggal berakhir: maks. 7 hari).')
rep('["promo","Promo baru","Saat promo diterbitkan",0]', '["promo","Promo","Promo tanpa potongan harga",0]')
rep('["diskon","Diskon baru","Promo yang punya potongan harga",0]', '["diskon","Diskon","Promo yang punya potongan harga",0]')
rep('["kabar","Kabar terbaru","Saat berita/kabar diterbitkan",0]', '["kabar","Kabar terbaru","Berita & kabar toko",0]')
rep('["event","Kegiatan","Saat kegiatan/event diterbitkan",0]', '["event","Kegiatan","Kegiatan/event",0]')

# ------------------------------------------------------------------ 3. Aplikasi terbuka: promo baru langsung diberitahukan (+ suara)
rep('''    await A521.kSet(r.j.rev,r.j.k);
    K=r.j.k;''', '''    const old=new Set((K.posts||[]).map(p=>p.id));
    await A521.kSet(r.j.rev,r.j.k);
    K=r.j.k;''')
rep('''    if(!chatOn())try{chatClose()}catch(e){}''', '''    if(!chatOn())try{chatClose()}catch(e){}
    try{kAnnounce((K.posts||[]).filter(p=>!p.draft&&!old.has(p.id)))}catch(e){}''')

NEW = r'''
/*V16-PATCH*/
/* Simpan = langsung terbit di HP Owner (tidak perlu tombol Terbitkan). Ditunda bila lembar edit masih terbuka. */
var kPubBusy=false,kAutoT=0,kFail=0;
function kAuto(ms){if(!(AR&&kcan))return;clearTimeout(kAutoT);kAutoT=setTimeout(()=>{if(!kdirty&&!kQuickF)return;if(kPubBusy||msBusy||!$("#m").hidden){kAuto(2000);return}kPublish(true)},ms==null?900:ms)}
function kStat(){if(!kNeed())return `<p class="kst ok">✓ Tersimpan & sudah terlihat pelanggan</p>`;
  if(AR&&kcan)return `<p class="kst wait"><i></i>Menyimpan ke semua HP & pelanggan…</p>`;
  return `<p class="kst">Tersimpan di HP ini, belum terlihat pelanggan. Ubah dari HP Owner supaya terlihat.</p>`}
/* Kabar/promo baru diterima saat aplikasi terbuka: tampilkan pemberitahuan & bunyikan suaranya */
function kAnnounce(L){if(!L.length)return;const N=nfCfg(),staff=!!(C().teamCode||C().staffDev||isHub());
  const tp=p=>p.type==="promo"?((+p.dval||0)>0?"diskon":"promo"):p.type==="event"?"event":"kabar";
  const ok=L.filter(p=>{const x=N[tp(p)]||{};return x.on!==0&&(x.to==="semua"||(x.to==="staf"&&staff)||(x.to==="pelanggan"&&!staff))});if(!ok.length)return;
  const p=ok[0],t=tp(p),lbl={promo:"🎉 Promo baru",diskon:"🏷️ Diskon",event:"📅 Kegiatan",kabar:"📰 Kabar terbaru"}[t];
  toast(ok.length>1?`📣 ${ok.length} kabar & promo baru dari ${K.store.name||"521"}`:`${lbl}: ${p.title||""}`,1);
  try{if(window.A521&&A521.playSound)A521.playSound((N[t]||{}).snd||"ding")}catch(e){}
  try{if(window.A521&&A521.kabarSync)A521.kabarSync()}catch(e){}}
'''
rep("/*V12-PATCH*/\n/* Versi web publik", NEW + "/*V12-PATCH*/\n/* Versi web publik")

P.write_text(s)
print("OK, perubahan 16 (Simpan otomatis terbit, jam notifikasi pelanggan, pemberitahuan dalam aplikasi) diterapkan.")
