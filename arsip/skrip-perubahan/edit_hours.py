s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
# schedule engine after kOpen
i=s.index('function kOpen(h){');j=s.index('\n',i)
s=s[:j+1]+'''const HARI=["Minggu","Senin","Selasa","Rabu","Kamis","Jumat","Sabtu"];
function kSched(){const s=K.store;if(!Array.isArray(s.sched)||s.sched.length!==7){const m=String(s.hours||"05.00–21.00").match(/(\\d{1,2})[.:](\\d{2})\\s*[-–]\\s*(\\d{1,2})[.:](\\d{2})/),o=m?m[1].padStart(2,"0")+":"+m[2]:"05:00",c=m?m[3].padStart(2,"0")+":"+m[4]:"21:00";s.sched=[...Array(7)].map(()=>({on:true,o,c}))}return s.sched}
const hm=t=>{const [a,b]=String(t||"0:0").split(":");return (+a)*60+(+b||0)},dot=t=>String(t||"").replace(":",".");
function kStatus(){
  const s=K.store,S=kSched(),n=new Date(),d=S[n.getDay()],cur=n.getHours()*60+n.getMinutes();
  const todayTxt=d.on?dot(d.o)+"–"+dot(d.c):"Libur";
  if(s.mode==="open")return{open:true,label:"Buka sekarang",todayTxt,note:s.note};
  if(s.mode==="closed")return{open:false,label:"Tutup sementara",todayTxt,note:s.note};
  if(!d.on){let k=1;while(k<7&&!S[(n.getDay()+k)%7].on)k++;const nx=S[(n.getDay()+k)%7];return{open:false,label:"Libur hari ini",todayTxt,next:k<7?"Buka lagi "+(k===1?"besok":HARI[(n.getDay()+k)%7])+" "+dot(nx.o):"",note:s.note}}
  const a=hm(d.o),b=hm(d.c),open=a<=b?(cur>=a&&cur<b):(cur>=a||cur<b);
  return{open,label:open?"Buka sekarang":"Sedang tutup",todayTxt,next:open?"Tutup "+dot(d.c):(cur<a?"Buka "+dot(d.o):""),note:s.note};
}
'''+s[j+1:]
# kHead use status
rep('''function kHead(){const s=K.store,o=kOpen(s.hours),H=s.heroes||[];''','''function kHead(){const s=K.store,st=kStatus(),o=st.open,H=s.heroes||[];''')
rep('''<span class="k-chip${o?"":" closed"}"><i></i>${o?"Buka sekarang":"Sedang tutup"}</span>`}${s.hours?`<span class="k-chip">${ic("today")}${esc(s.hours)}</span>`:""}</div></div>''','''<span class="k-chip${o?"":" closed"}"><i></i>${st.label}</span>`}<span class="k-chip">${ic("today")}${st.todayTxt==="Libur"?"Hari ini libur":esc(st.todayTxt)}</span></div></div>''')
rep('''<h1 class="k-h1">${esc(s.headline||s.name)}</h1><p class="k-tagl">${esc(s.tagline)}</p>
  <div class="k-info"><div><span>Jam buka</span><b>${esc(s.hours||"-")}</b></div>''','''${st.note?`<div class="k-note">${ic("mega")}<span>${esc(st.note)}</span></div>`:""}<h1 class="k-h1">${esc(s.headline||s.name)}</h1><p class="k-tagl">${esc(s.tagline)}</p>
  <div class="k-info"><div><span>Jam buka hari ini</span><b>${esc(st.todayTxt)}</b>${st.next?`<em class="k-next">${esc(st.next)}</em>`:""}</div>''')
rep('''<div class="k-foot"><svg class="mark" aria-hidden="true"><use href="#logo"/></svg>${esc(s.name)} · ${esc(s.tagline)}</div></div>`;''','''<details class="k-week"><summary>${ic("today")}Jadwal buka seminggu</summary><ul>${[1,2,3,4,5,6,0].map(d=>{const x=kSched()[d];return `<li class="${d===new Date().getDay()?"now":""}"><span>${HARI[d]}</span><b>${x.on?dot(x.o)+"–"+dot(x.c):"Libur"}</b></li>`}).join("")}</ul></details><div class="k-foot"><svg class="mark" aria-hidden="true"><use href="#logo"/></svg>${esc(s.name)} · ${esc(s.tagline)}</div></div>`;''')
# CSS
rep('.k-empty{text-align:center;','''.k-note{display:flex;gap:10px;align-items:center;margin:16px 0 0;padding:12px 14px;border-radius:14px;background:color-mix(in srgb,var(--ac) 12%,var(--sf));border:1px solid color-mix(in srgb,var(--ac) 40%,var(--line));font-weight:700;font-size:14px}
.k-note svg{color:var(--ac)}
.k-next{display:block;font-style:normal;font-size:12px;font-weight:700;color:var(--ac);margin-top:4px}
.k-week{margin-top:28px;background:var(--sf);border:1px solid var(--line);border-radius:18px;padding:4px 16px}
.k-week summary{display:flex;align-items:center;gap:8px;cursor:pointer;padding:12px 0;font-weight:700;list-style:none}
.k-week summary::-webkit-details-marker{display:none}
.k-week summary svg{color:var(--ac)}
.k-week ul{list-style:none;margin:0 0 10px;padding:0}
.k-week li{display:flex;justify-content:space-between;padding:7px 0;border-top:1px dashed var(--line);font-size:14px;color:var(--mute)}
.k-week li b{font-family:var(--f-m);color:var(--ink);font-weight:600}
.k-week li.now span,.k-week li.now b{color:var(--ac)}
.schedrow{display:grid;grid-template-columns:92px auto minmax(0,1fr) minmax(0,1fr);gap:8px;align-items:center;padding:8px 0;border-bottom:1px solid var(--line)}
.schedrow input[type=time]{margin:0;padding:9px 8px}
.schedrow.off input[type=time]{opacity:.35}
.tgl{position:relative;width:46px;height:28px;flex:none}
.tgl input{position:absolute;inset:0;opacity:0;margin:0;cursor:pointer;width:100%;height:100%}
.tgl span{position:absolute;inset:0;border-radius:999px;background:var(--sf3);transition:background .2s;pointer-events:none}
.tgl span::after{content:"";position:absolute;top:3px;left:3px;width:22px;height:22px;border-radius:50%;background:var(--ink);transition:transform .2s}
.tgl input:checked + span{background:var(--ac)}
.tgl input:checked + span::after{transform:translateX(18px);background:var(--on)}
.statusbox{display:flex;align-items:center;gap:10px;padding:12px 14px;border-radius:14px;background:var(--sf2);border:1px solid var(--line);margin-bottom:12px;font-weight:700}
.statusbox i{width:10px;height:10px;border-radius:50%;background:var(--ok);box-shadow:0 0 10px var(--ok);flex:none}
.statusbox.closed i{background:var(--warn);box-shadow:none}
.k-empty{text-align:center;''')
# Settings folder
rep('''  ["kasir","pos","Pilihan kasir",''','''  ["buka","today","Jam buka toko",()=>{const st=kStatus();return `${st.label} · hari ini ${st.todayTxt}`}],
  ["kasir","pos","Pilihan kasir",''')
rep('''  if(id==="log")return''','''  if(id==="buka"){const st=kStatus(),S=kSched(),md=K.store.mode||"auto";return `<div class="statusbox ${st.open?"":"closed"}"><i></i><span>Di halaman pelanggan: ${st.label}${st.next?` <span class="mute" style="font-weight:600">· ${esc(st.next)}</span>`:""}</span></div>
  <div class="lbl" style="margin-top:0">Status toko</div><div class="chips">${[["auto","Ikuti jadwal"],["open","Buka sekarang"],["closed","Tutup sementara"]].map(o=>`<button data-a="kmode" data-v="${o[0]}" aria-pressed="${md===o[0]}">${o[1]}</button>`).join("")}</div>
  <p class="note" style="margin-top:-4px">“Buka sekarang” dan “Tutup sementara” berlaku sampai Anda kembali ke “Ikuti jadwal”.</p>
  <label>Pengumuman untuk pelanggan (opsional)<input id="knote" value="${esc(K.store.note||"")}" placeholder="Contoh: Libur Lebaran, buka lagi 10 April"></label>
  <h3>Jadwal mingguan</h3>${[1,2,3,4,5,6,0].map(d=>{const x=S[d];return `<div class="schedrow ${x.on?"":"off"}"><b>${HARI[d]}</b><label class="tgl" aria-label="${HARI[d]} buka"><input type="checkbox" data-sd="${d}" data-sf="on" ${x.on?"checked":""}><span></span></label><input type="time" data-sd="${d}" data-sf="o" value="${x.o}" aria-label="${HARI[d]} jam buka" ${x.on?"":"disabled"}><input type="time" data-sd="${d}" data-sf="c" value="${x.c}" aria-label="${HARI[d]} jam tutup" ${x.on?"":"disabled"}></div>`}).join("")}
  <button class="link" data-a="ksamakan">Samakan semua hari dengan Senin</button>
  ${kdirty?`<button class="btn" data-a="kpublish">Simpan & terbitkan</button><p class="note">Perubahan jam buka baru terlihat pelanggan setelah diterbitkan.</p>`:`<p class="note">✓ Jadwal sudah terbit di halaman pelanggan.</p>`}`}
  if(id==="log")return''')
# handlers
rep('''  else if(a==="bton"){btConnect()}''','''  else if(a==="kmode"){K.store.mode=v==="auto"?"":v;kChanged()}
  else if(a==="ksamakan"){const S=kSched();for(let d=0;d<7;d++)if(d!==1)S[d]={...S[1]};kChanged();toast("Semua hari disamakan dengan Senin",1)}
  else if(a==="bton"){btConnect()}''')
rep('''  else if(t.id==="kbf"&&t.files''','''  else if(t.dataset.sd!==undefined&&own()){const S=kSched(),x=S[+t.dataset.sd],f=t.dataset.sf;if(f==="on")x.on=t.checked;else if(t.value)x[f]=t.value;kChanged()}
  else if(t.id==="knote"&&own()){K.store.note=t.value.trim();kChanged()}
  else if(t.id==="kbf"&&t.files''')
# kasir greet status
rep('''<p>${tc?`${tc} pesanan sudah tercatat hari ini.`:"Belum ada pesanan hari ini. Semangat!"}</p>''','''<p>${tc?`${tc} pesanan sudah tercatat hari ini.`:"Belum ada pesanan hari ini. Semangat!"}</p>${(()=>{const st=kStatus();return `<p style="margin-top:6px;font-size:13px;font-weight:700;color:${st.open?"var(--ok)":"var(--warn)"}">● ${st.label}${st.next?" · "+esc(st.next):""}</p>`})()}''')
# store sheet: hours field -> note pointing to folder
rep('''<label>Jam buka<input id="s-hours" value="${esc(s.hours)}" placeholder="05.00–21.00"></label>''','''<label>Jam buka (cadangan)<input id="s-hours" value="${esc(s.hours)}" placeholder="05.00–21.00"></label>''')
open('p3.src.html','w').write(s);print('ok')
