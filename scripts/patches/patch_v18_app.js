/*V18-PATCH*/
/* ===== Printer struk Bluetooth langsung dari aplikasi Android =====
   Kasir cukup: Atur → Printer Bluetooth → Cari printer. Bluetooth dinyalakan lewat dialog sistem, printer dicari otomatis,
   ketuk nama printer → tersambung & cetak tes. Setelah itu tombol Printer di layar Lunas langsung mencetak. */
const NBT=()=>!!(window.A521&&A521.bt);
let BTS={st:null,list:[],scan:false,busy:"",msg:"",tx:null};
const btName=()=>BTS.st&&BTS.st.addr?(BTS.st.name||"Printer"):"";
async function btRefresh(){if(!NBT())return null;try{BTS.st=await A521.bt.state()}catch(e){}return BTS.st}
setTimeout(btRefresh,1500);
const asc=t=>String(t==null?"":t).replace(/[\u2013\u2014\u2212]/g,"-").replace(/[\u2018\u2019]/g,"'").replace(/[\u201c\u201d]/g,'"').replace(/\u00d7/g,"x").normalize("NFKD").replace(/[^\x0a\x20-\x7e]/g,"");
let LOGO_RAS=null;
/* logo 521 → gambar hitam-putih untuk printer (GS v 0). Gagal = struk tanpa logo. */
async function logoRaster(W){if(LOGO_RAS&&LOGO_RAS.w===W)return LOGO_RAS.b;
  try{const sym=document.getElementById("logo");if(!sym)return null;const vb=(sym.getAttribute("viewBox")||"0 0 1565 1015").trim().split(/\s+/).map(Number);
    const dots=W===48?576:384,w=Math.round(dots*0.5/8)*8,h=Math.max(8,Math.round(w*vb[3]/vb[2]));
    const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.join(" ")}" width="${w}" height="${h}" style="color:#000">${sym.innerHTML}</svg>`;
    const img=new Image();await new Promise((ok,no)=>{img.onload=ok;img.onerror=no;img.src="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(svg)});
    const cv=document.createElement("canvas");cv.width=w;cv.height=h;const g=cv.getContext("2d");g.fillStyle="#fff";g.fillRect(0,0,w,h);g.drawImage(img,0,0,w,h);
    const d=g.getImageData(0,0,w,h).data,xb=w/8,out=[29,118,48,0,xb&255,xb>>8,h&255,h>>8];
    for(let y=0;y<h;y++)for(let x=0;x<xb;x++){let v=0;for(let k=0;k<8;k++){const i=(y*w+x*8+k)*4;if((d[i]+d[i+1]+d[i+2])/3<140)v|=128>>k}out.push(v)}
    LOGO_RAS={w:W,b:out};return out}catch(e){return null}}
/* Struk ESC/POS: nama toko besar di tengah, TOTAL tebal, potong kertas (diabaikan printer tanpa pemotong) */
function escTx(tx,logo){const c=C(),W=Number(c.paper)===48?48:32,hr="-".repeat(W),B=[];
  const raw=a=>{for(const x of a)B.push(x)},txt=s=>{for(const ch of asc(s))B.push(ch.charCodeAt(0))},ln=s=>{txt(s);B.push(10)};
  const lr=(a,b)=>{a=asc(a);b=asc(b);const sp=W-a.length-b.length;return sp>=1?a+" ".repeat(sp)+b:a.slice(0,W)+"\n"+" ".repeat(Math.max(0,W-b.length))+b};
  const dt=new Date(tx.at||Date.now());
  raw([27,64,27,116,0,27,97,1]);
  if(logo&&logo.length){raw(logo);B.push(10)}
  raw([27,33,48]);wrap(asc(c.name||"521 Coffee"),W/2).forEach(ln);raw([27,33,0]);
  if(c.sub)wrap(asc(c.sub),W).forEach(ln);
  raw([27,97,0]);ln(hr);ln(tx.no||"");ln(lr(dt.toLocaleDateString("id-ID"),dt.toLocaleTimeString("id-ID",{hour:"2-digit",minute:"2-digit"})));ln("Kasir: "+(tx.by||"-"));ln(hr);
  (tx.items||[]).forEach(i=>{wrap(asc(i.n),W).forEach(ln);ln(lr("  "+i.q+" x "+rp(i.pr),rp(i.pr*i.q)))});
  ln(hr);if(tx.vd)ln(lr("Voucher "+(tx.vc||""),"-"+rp(tx.vd)));if((tx.disc||0)-(tx.vd||0)>0)ln(lr("Diskon","-"+rp(tx.disc-(tx.vd||0))));
  raw([27,69,1]);ln(lr("TOTAL",rp(tx.total)));raw([27,69,0]);ln(lr(tx.pm||"-",rp(tx.paid)));
  if(isC(tx.pm)&&tx.paid>=tx.total)ln(lr("Kembali",rp(tx.paid-tx.total)));
  ln(hr);raw([27,97,1]);wrap(asc(c.foot),W).forEach(ln);raw([27,97,0]);
  raw([27,100,4,29,86,66,0]);return new Uint8Array(B)}
const b64=u=>{let s="";for(let i=0;i<u.length;i+=8192)s+=String.fromCharCode.apply(null,u.subarray(i,i+8192));return btoa(s)};
const BTERR={no_printer:"Belum ada printer yang dipilih.",perm:"Izin Bluetooth belum diberikan.",off:"Bluetooth belum menyala.",unsupported:"HP ini tidak punya Bluetooth.",not_printer:"Perangkat ini bukan printer struk yang dikenali.",busy:"Masih memproses permintaan sebelumnya."};
const btErr=e=>BTERR[e&&e.code]||"Printer tidak merespons. Pastikan printer menyala, kertas terpasang, dan dekat dengan HP.";
async function btPrintTx(tx,quiet){
  if(!NBT())return;const c=C(),W=Number(c.paper)===48?48:32;
  if(!btName()){await btRefresh();if(!btName()){if(!quiet)btSheet(tx);return}}
  try{const logo=c.plogo===false?null:await logoRaster(W);await A521.bt.print(b64(escTx(tx,logo)));toast("Struk dicetak 🧾",1)}
  catch(e){if(e&&e.code==="no_printer"){if(!quiet)btSheet(tx);return}if(quiet){toast(btErr(e),1);return}try{copy(printText(tx),btErr(e)+" Struk tersalin untuk aplikasi printer.")}catch(x){toast(btErr(e),1)}}}
const btTest=()=>({no:"TES-PRINTER",at:new Date().toISOString(),by:(me&&me.name)||"-",items:[{n:"Tes cetak 521",q:1,pr:0}],disc:0,total:0,pm:"-",paid:0});
/* Lembar pilih printer: minta izin + nyalakan Bluetooth, lalu langsung mencari */
function btSheet(tx){BTS.tx=tx||null;BTS.list=[];BTS.msg="";BTS.busy="";
  show(`<h2>Pilih printer</h2><p class="note" style="margin-top:-6px">Nyalakan printer struk & dekatkan ke HP. Ketuk nama printer untuk menyambung.</p><div id="btsh">${btListHTML()}</div><button class="btn ghost" data-a="btscan">Cari lagi</button>`);
  btStart()}
async function btStart(){if(!NBT()||BTS.scan)return;BTS.msg="";BTS.list=[];btPaint();
  try{BTS.st=await A521.bt.prepare()}catch(e){BTS.msg=e&&e.code==="perm"?"perm":e&&e.code==="off"?"Bluetooth belum dinyalakan. Ketuk Cari lagi, lalu pilih Izinkan / Aktifkan.":btErr(e);btPaint();return}
  BTS.scan=true;btPaint();
  A521.bt.on(ev=>{if(ev.ev==="dev"){if(!BTS.list.some(x=>x.addr===ev.addr))BTS.list.push(ev);BTS.list.sort((a,b)=>(b.printer-a.printer)||(b.bonded-a.bonded)||String(a.name).localeCompare(String(b.name)))}
    else if(ev.ev==="done"){BTS.scan=false;if(ev.err==="perm")BTS.msg="perm"}btPaint()});
  try{await A521.bt.scan()}catch(e){BTS.scan=false;BTS.msg=btErr(e);btPaint()}}
function btListHTML(){const L=BTS.list,st=BTS.st||{};
  return `${BTS.msg==="perm"?`<p class="verr">Izin Bluetooth ditolak. Buka pengaturan aplikasi → Izin → <b>Perangkat di sekitar</b> → Izinkan.</p><button class="btn ghost sm" data-a="hpgo" data-v="app">Buka pengaturan aplikasi</button>`:BTS.msg?`<p class="verr">${esc(BTS.msg)}</p>`:""}
  ${st.locOff?`<p class="verr">Nyalakan <b>Lokasi</b> HP dulu: Android versi ini butuh Lokasi untuk menemukan printer Bluetooth.</p>`:""}
  ${BTS.scan?`<div class="btscan"><i></i>Mencari printer di sekitar…</div>`:""}
  <div class="btlist">${L.map(d=>`<button data-a="btpick" data-v="${esc(d.addr)}" aria-pressed="${st.addr===d.addr}">${ic("print")}<span style="flex:1;min-width:0"><b>${esc(d.name)}</b><small>${[d.printer?"Printer":"",d.bonded?"Sudah dipasangkan":"",d.le?"BLE":"",esc(d.addr)].filter(Boolean).join(" · ")}</small></span>${BTS.busy===d.addr?'<span class="btscan" style="margin:0"><i></i></span>':st.addr===d.addr?'<span class="pill own">Dipakai</span>':""}</button>`).join("")}</div>
  ${!BTS.scan&&!L.length&&!BTS.msg?`<p class="note">Belum ada perangkat ditemukan. Pastikan printer menyala (lampu berkedip), lalu ketuk <b>Cari lagi</b>.</p>`:""}`}
function btPaint(){const el=$("#btsh");if(el)el.innerHTML=btListHTML();const sb=$("#btset");if(sb)sb.innerHTML=btSetInner()}
async function btPick(addr){if(BTS.busy)return;BTS.busy=addr;btPaint();
  try{const r=await A521.bt.connect(addr);await btRefresh();BTS.busy="";const tx=BTS.tx;BTS.tx=null;
    toast("Tersambung ke "+(r&&r.name||"printer"),1);if($("#btsh"))shut();if(me&&tab==="set")render();await btPrintTx(tx||btTest(),false)}
  catch(e){BTS.busy="";BTS.msg=e&&e.code==="perm"?"perm":e&&BTERR[e.code]?btErr(e):"Gagal menyambung. Matikan lalu nyalakan printer, pastikan tidak sedang tersambung ke HP lain, lalu coba lagi.";btPaint()}}
function btSetInner(){const c=C(),st=BTS.st||{};
  return `<div class="btbox ${st.addr?"on":""}">${ic("print")}<span><b>${st.addr?"Printer: "+esc(st.name||st.addr):"Belum memilih printer"}</b><small>${st.addr?"Tombol Printer di layar Lunas langsung mencetak.":"Untuk printer thermal Bluetooth 58/80 mm (ESC/POS)."}</small></span></div>
  <button class="btn" data-a="btfind">${ic("print")}${st.addr?"Ganti printer":"Cari printer"}</button>
  ${st.addr?`<div class="two"><button class="btn ghost" data-a="bttest2">Cetak tes</button><button class="btn ghost" data-a="btforget" style="color:var(--warn)">Lupakan printer</button></div>`:""}
  <div class="lbl">Lebar kertas</div><div class="chips"><button data-a="paper" data-v="32" aria-pressed="${Number(c.paper)!==48}">58 mm</button><button data-a="paper" data-v="48" aria-pressed="${Number(c.paper)===48}">80 mm</button></div>
  <div class="swrow"><span><b>Cetak logo 521</b><small>Logo di bagian atas struk</small></span><label class="tgl" aria-label="Cetak logo"><input type="checkbox" id="plogo" ${c.plogo===false?"":"checked"}><span></span></label></div>
  <div class="swrow"><span><b>Cetak otomatis setelah bayar</b><small>Struk langsung keluar saat layar Lunas muncul</small></span><label class="tgl" aria-label="Cetak otomatis"><input type="checkbox" id="pauto" ${c.pauto?"checked":""}><span></span></label></div>
  <p class="note">Printer yang meminta PIN saat dipasangkan biasanya memakai <b>0000</b> atau <b>1234</b>.</p>`}
function btSetHTML(){btRefresh().then(()=>{const sb=$("#btset");if(sb)sb.innerHTML=btSetInner()});return `<div id="btset">${btSetInner()}</div>`}
document.addEventListener("change",e=>{const t=e.target;if(!t||(t.id!=="plogo"&&t.id!=="pauto"))return;const c=C();c[t.id]=!!t.checked;save();toast(t.checked?"Aktif":"Nonaktif")});

/* ===== Website (link media sosial) diatur dari aplikasi =====
   Teks halaman website disimpan di data toko (K.store.web) dan ikut terbit bersama menu, promo, jam buka, reseller, dll. */
const WEB_URL="https://abyan1608-netizen.github.io/521-Coffee-Cart-Web/";
const WEBF=[["Tampilan awal",[["hero.eyebrow","Label kecil di atas judul","Kopi 100% Arabika"],["hero.title","Judul utama (Enter = baris baru)","teman\n*belajar* & *bekerja*.",1],["hero.sub","Kalimat di bawah judul","Kopi botolan 100% Arabika di Ciledug – Pinang. Buka setiap hari, pagi sampai malam.",1],["hero.cta1","Tombol pertama","Pesan sekarang"],["hero.cta2","Tombol kedua","Lihat menu"]]],
  ["Pita teks berjalan",[["strip","Satu baris = satu teks","100% Arabika\nBuka 05.00–21.00\nCiledug – Pinang\nTeman kamu, belajar & bekerja",1]]],
  ["Cerita",[["story.title","Judul","Teman kamu, belajar & bekerja."],["story.soft","Sapaan","Assalamualaikum !"],["story.body","Isi cerita","Satu botol kopi, sejuta cerita yang menemani perjalananmu.",1]]],
  ["Menu",[["menu.title","Judul","Best from us"],["menu.sub","Keterangan","Dikemas dalam botol, siap dibawa ke kelas atau ke kantor.",1]]],
  ["Kabar",[["news.title","Judul","Siap jadi teman final Liga LIPIA!!!"],["news.sub","Keterangan","Kepoin promo, kegiatan, dan cerita terbaru dari kami.",1]]],
  ["Testimoni & lokasi",[["testi.title","Judul testimoni","Cerita dari yang sudah mampir."],["visit.sub","Keterangan lokasi","Mampir langsung, atau pesan lewat reseller terdekat dan aplikasi pesan antar.",1],["footer.bio","Teks paling bawah","Kopi botolan 100% Arabika untuk teman belajar & bekerja, dari gerobak kecil di Ciledug – Pinang.",1]]]];
const WEBS=[["strip","Pita teks"],["story","Cerita"],["menu","Menu"],["news","Kabar"],["testi","Testimoni"],["visit","Lokasi"]];
const wGet=(o,p)=>p.split(".").reduce((a,k)=>a&&a[k],o);
function webSetHTML(){const W=K.store.web||{},sh=W.show||{};
  return `<p class="note" style="margin-top:0">Website: <a href="${WEB_URL}" data-a="webopen">${esc(WEB_URL.replace("https://",""))}</a><br>Menu, harga, stok habis, promo, kabar, jam buka, testimoni, reseller, dan kontak <b>otomatis</b> ikut dari aplikasi. Di sini hanya teks khusus website. Tulis <b>*kata*</b> untuk warna menonjol.</p>
  ${WEBF.map(([g,F])=>`<h3>${g}</h3>${F.map(([p,l,d,area])=>{const v=p==="strip"?(Array.isArray(W.strip)?W.strip.join("\n"):""):(wGet(W,p)||"");return `<label>${l}${area?`<textarea class="kt" data-wf="${p}" placeholder="${esc(d)}">${esc(v)}</textarea>`:`<input data-wf="${p}" value="${esc(v)}" placeholder="${esc(d)}">`}</label>`}).join("")}`).join("")}
  <h3>Bagian yang tampil</h3>${WEBS.map(([k,l])=>`<div class="swrow"><span><b>${l}</b></span><label class="tgl" aria-label="Tampilkan ${l}"><input type="checkbox" data-ws="${k}" ${sh[k]===false?"":"checked"}><span></span></label></div>`).join("")}
  <p class="note">Kolom kosong = memakai teks bawaan website (tulisan abu-abu).</p>
  <button class="btn" data-a="websave">Simpan ke website</button>${kStat()}`}
function webSave(){const W={},all=q=>[...document.querySelectorAll(q)];
  all("[data-wf]").forEach(el=>{const v=el.value.trim();if(!v)return;if(el.dataset.wf==="strip"){W.strip=v.split("\n").map(x=>x.trim()).filter(Boolean).slice(0,12);return}
    const k=el.dataset.wf.split(".");W[k[0]]=W[k[0]]||{};W[k[0]][k[1]]=v.slice(0,1500)});
  const sh={};all("[data-ws]").forEach(el=>{if(!el.checked)sh[el.dataset.ws]=false});if(Object.keys(sh).length)W.show=sh;
  K.store.web=W;kChanged();toast(AR&&kcan?"Tersimpan. Website ikut berubah ±1 menit lagi.":"Tersimpan di HP ini. Simpan dari HP Owner supaya website ikut berubah.",1)}
/* tombol baru (didahulukan sebelum penangan klik utama) */
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-a]");if(!b)return;const a=b.dataset.a,v=b.dataset.v;
  const H={btfind:()=>btSheet(null),btscan:()=>btStart(),btpick:()=>btPick(v),bttest2:()=>btPrintTx(btTest(),false),
    btforget:async()=>{try{await A521.bt.forget()}catch(x){}await btRefresh();btPaint();toast("Printer dilupakan")},
    websave:()=>webSave(),webopen:()=>{if(window.A521&&A521.open)A521.open(WEB_URL);else window.open(WEB_URL,"_blank","noopener")},
    copyp:()=>{const t=txFind(b.dataset.id);if(t)btPrintTx(t,false)}};
  if(!H[a]||(a==="copyp"&&!NBT()))return;e.preventDefault();e.stopImmediatePropagation();H[a]()},true);
