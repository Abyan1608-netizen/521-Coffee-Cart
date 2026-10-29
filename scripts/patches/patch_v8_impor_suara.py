"""Perubahan 08: impor suara notifikasi dari HP di Atur → Notifikasi (MP3/OGG/M4A/AAC/WAV, maks 1,5 MB / 20 dtk).
Suara diunggah ke server saat terbit sehingga HP staf & pelanggan memutar suara yang sama. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V8-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:200]}")
    s = s.replace(old, new)

rep(".hpst{", """/*V8-PATCH*/
.sndl{border:1px solid var(--line);border-radius:16px;padding:12px 14px;margin:0 0 12px;background:var(--sf)}
.sndl h4{margin:0 0 4px;font-size:15px}.sndl p{margin:0 0 8px;font-size:12.5px;color:var(--mute)}
.sndl .sr{display:flex;align-items:center;gap:8px;padding:8px 0;border-top:1px solid var(--line)}
.sndl .sr:first-of-type{border-top:0}.sndl .sr span{flex:1;font-size:14px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}
.sndl .sr small{color:var(--mute);font-size:12px;margin-left:4px}
.sndl .sr button{margin:0;flex:none}
.hpst{""")

# daftar suara impor + pilihan "Impor dari HP…" di setiap dropdown suara
rep("function nfCfg(){", r'''const nfSounds=()=>Array.isArray(K.store&&K.store.sounds)?K.store.sounds.filter(x=>x&&/^media\/[a-f0-9]{32}\.(mp3|ogg|m4a|aac|wav)$/.test(x.f)):[];
const sndName=v=>{if(String(v).startsWith("c:")){const x=nfSounds().find(s=>s.f==="media/"+v.slice(2));return x?"🎵 "+x.n:"🎵 Suara impor"}const b=NFS.find(s=>s[0]===v);return b?b[1]:v};
function nfOpts(sel){const C=nfSounds();if(String(sel).startsWith("c:")&&!C.some(x=>"c:"+x.f.slice(6)===sel))sel="ding";
  return NFS.map(([v,l])=>`<option value="${v}"${sel===v?" selected":""}>${l}</option>`).join("")
   +(C.length?`<optgroup label="Suara saya">${C.map(x=>{const v="c:"+x.f.slice(6);return `<option value="${v}"${sel===v?" selected":""}>🎵 ${esc(x.n)}</option>`}).join("")}</optgroup>`:"")
   +`<option value="__imp">📁 Impor dari HP…</option>`}
function nfSndList(){const C=nfSounds();return `<div class="sndl" id="sndl"><h4>🎵 Suara saya</h4><p>Impor suara sendiri dari HP (MP3, OGG, M4A, AAC, WAV · maks 1,5 MB · maks 20 detik). Ikut terkirim ke semua HP saat diterbitkan.</p>
  ${C.length?C.map(x=>`<div class="sr"><span>${esc(x.n)}<small>${x.ms?Math.round(x.ms/100)/10+" dtk":""}</small></span><button class="btn ghost sm" data-a="sndplay" data-v="c:${x.f.slice(6)}" aria-label="Putar">▶</button><button class="fgdel" data-a="snddel" data-v="${x.f}">Hapus</button></div>`).join(""):'<p style="margin:0">Belum ada. Pilih "📁 Impor dari HP…" pada salah satu pilihan suara.</p>'}
  <button class="btn ghost sm" data-a="sndimp" style="margin-top:8px">📁 Impor suara dari HP</button></div>`}
const SNDERR={cancelled:"",too_big:"File terlalu besar (maks 1,5 MB). Potong atau kompres dulu.",format:"Format belum didukung. Pakai MP3, OGG, M4A, AAC, atau WAV.",rusak:"File suara tidak bisa dibaca.",io:"Gagal menyalin file suara.",no_picker:"Tidak ada aplikasi pemilih file di HP ini.",busy:""};
async function sndImport(selEl){if(!(window.A521&&A521.native&&A521.pickSound)){toast("Impor suara hanya bisa di aplikasi Android");return null}
  try{const r=await A521.pickSound();const L=K.store.sounds=nfSounds();const f="media/"+r.f;let x=L.find(s=>s.f===f);
    if(!x){if(L.length>=10){toast("Maksimal 10 suara impor. Hapus yang tidak dipakai dulu.");return null}x={f,n:String(r.n||"Suara").slice(0,40),ms:+r.ms||0};L.push(x)}
    const v="c:"+r.f,keep={};document.querySelectorAll(".nfsnd").forEach(el=>keep[el.closest(".nfc").dataset.nfk]=el===selEl?v:(el.value==="__imp"?el.dataset.prev||"ding":el.value));
    document.querySelectorAll(".nfsnd").forEach(el=>{const k=el.closest(".nfc").dataset.nfk;el.innerHTML=nfOpts(keep[k]);el.value=keep[k];el.dataset.prev=keep[k]});
    const w=$("#sndl");if(w)w.outerHTML=nfSndList();A521.playSound(v);toast(`Suara "${x.n}" ditambahkan. Tekan Simpan & terbitkan agar dipakai.`,1);return v}
  catch(e){const c=String(e&&e.code||"");const m=c.startsWith("too_long")?`Suara terlalu panjang (${c.split(":")[1]||"?"} detik). Maksimal 20 detik.`:SNDERR[c]??"Gagal mengimpor suara.";if(m)toast(m);return null}}
function nfCfg(){''')
# dropdown suara memakai nfOpts
rep('<select class="nfsnd">${NFS.map(([v,l])=>`<option value="${v}"${x.snd===v?" selected":""}>${l}</option>`).join("")}</select>',
    '<select class="nfsnd" data-prev="${x.snd}">${nfOpts(x.snd)}</select>')
rep('  <label class="fgck"><input type="checkbox" id="nfedit" ${c.edit?"checked":""}>',
    '  ${nfSndList()}\n  <label class="fgck"><input type="checkbox" id="nfedit" ${c.edit?"checked":""}>')

# perubahan dropdown: "__imp" → buka pemilih file; simpan nilai sebelumnya
rep('document.addEventListener("change",e=>{', '''document.addEventListener("change",e=>{
  if(e.target.classList&&e.target.classList.contains("nfsnd")){const el=e.target;if(el.value==="__imp"){const prev=el.dataset.prev||"ding";el.value=prev;sndImport(el).then(v=>{if(!v)el.value=prev})}else el.dataset.prev=el.value}''')

# tombol daftar suara
rep('  else if(a==="nfsave"&&can("set"))nfSave();', '''  else if(a==="nfsave"&&can("set"))nfSave();
  else if(a==="sndimp"&&can("set"))sndImport(null);
  else if(a==="sndplay"){if(window.A521&&A521.playSound)A521.playSound(v)}
  else if(a==="snddel"&&can("set")){const L=nfSounds(),x=L.find(s=>s.f===v);if(!x)return;K.store.sounds=L.filter(s=>s.f!==v);const cv="c:"+v.slice(6);
    document.querySelectorAll(".nfsnd").forEach(el=>{const cur=el.value===cv?"ding":el.value;el.innerHTML=nfOpts(cur);el.value=cur;el.dataset.prev=cur});
    const N=K.store.notif||{};Object.keys(N).forEach(k=>{if(N[k]&&N[k].snd===cv)N[k].snd="ding"});const w=$("#sndl");if(w)w.outerHTML=nfSndList();toast(`Suara "${x.n}" dihapus. Tekan Simpan & terbitkan.`,1)}''')

# HP lain: unduh suara impor Owner saat aplikasi dibuka
rep("return n}\npinMigrate().catch(()=>{});setTimeout(()=>{try{fgSchedule()}catch(e){}},1500);",
    "return n}\npinMigrate().catch(()=>{});setTimeout(()=>{try{fgSchedule()}catch(e){}},1500);setTimeout(()=>{try{const L=nfSounds();if(L.length&&window.A521&&A521.soundSync)A521.soundSync(L.map(x=>x.f))}catch(e){}},3000);")

rep('>Kirim juga notifikasi saat promo/diskon/kabar <b>diubah</b> (bukan hanya yang baru).</label>', '><span>Kirim juga notifikasi saat promo/diskon/kabar <b>diubah</b> (bukan hanya yang baru).</span></label>')
P.write_text(s)
print("OK, perubahan 08 (impor suara dari HP) diterapkan.")
