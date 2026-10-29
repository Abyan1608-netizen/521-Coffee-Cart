"""Perubahan 09: terima audio dari tombol "Bagikan" (WhatsApp dll) sebagai suara notifikasi + dukung .opus. Sekali jalan."""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V9-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)
def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:200]}")
    s = s.replace(old, new)

rep("function nfCfg(){", r'''/*V9-PATCH*/
/* Audio yang dibagikan ke aplikasi (WhatsApp → Bagikan → 521 Coffee App) */
function sndIn(){let m=null;try{m=JSON.parse(sessionStorage.getItem("a521sndin")||"null")}catch(e){}if(!m)return;
  if(!me){if(!sndIn.t){sndIn.t=1;toast("🎵 Suara diterima. Masuk sebagai Owner/Admin dulu, nanti otomatis ditambahkan.");if($("#login").hidden)showLogin()}return}
  try{sessionStorage.removeItem("a521sndin")}catch(e){}
  if(!can("set")){toast("Hanya Owner/Admin yang bisa menambah suara notifikasi.");return}
  if(!m.ok){const c=String(m.e||"");const t=c.startsWith("too_long")?`Suara terlalu panjang (${c.split(":")[1]||"?"} detik). Maksimal 20 detik.`:SNDERR[c]??"Gagal mengimpor suara.";if(t)toast(t);return}
  const r=m.r||{},L=K.store.sounds=nfSounds(),f="media/"+r.f;let x=L.find(s=>s.f===f);
  if(!x){if(L.length>=10){toast("Maksimal 10 suara impor. Hapus yang tidak dipakai dulu.");return}x={f,n:String(r.n||"Suara WhatsApp").slice(0,40),ms:+r.ms||0};L.push(x)}
  tab="set";setSub="notif";if(!$("#m").hidden)shut();render();window.scrollTo(0,0);
  setTimeout(()=>{const w=$("#sndl");if(w)w.scrollIntoView({behavior:"smooth",block:"center"})},300);
  if(window.A521&&A521.playSound)A521.playSound("c:"+r.f);
  toast(`🎵 "${x.n}" ditambahkan ke Suara saya. Pilih di jenis notifikasi, lalu Simpan & terbitkan.`,1)}
function nfCfg(){''')
rep('function enter(){if(!D.cfg.staffDev){D.cfg.staffDev=1;save()}', 'function enter(){if(!D.cfg.staffDev){D.cfg.staffDev=1;save()}setTimeout(()=>{try{sndIn()}catch(e){}},1200);')
rep('<p>Impor suara sendiri dari HP (MP3, OGG, M4A, AAC, WAV · maks 1,5 MB · maks 20 detik). Ikut terkirim ke semua HP saat diterbitkan.</p>',
    '<p>Impor suara sendiri dari HP (MP3, OGG, M4A, AAC, WAV, pesan suara WhatsApp · maks 1,5 MB · maks 20 detik). Bisa juga dari WhatsApp: tekan lama audio → <b>Bagikan</b> → <b>521 Coffee App</b>. Ikut terkirim ke semua HP saat diterbitkan.</p>')
P.write_text(s)
print("OK, perubahan 09 (bagikan audio ke aplikasi) diterapkan.")
