/*V20-PATCH*/
/* ===== Struk pelanggan + struk barista (1 penjualan = 2 struk) =====
   Pengaturan per HP kasir (Atur → Printer & struk): tab Umum, Pelanggan, Barista + Contoh struk.
   Pratinjau dibuat dari byte ESC/POS yang sama persis dengan yang dikirim ke printer. */
const PDEF={plogo:true,plsize:50,pcut:false,pauto:true,pcust:true,pbar:true,pque:true,paddr:true,pwa:true,pig:false,pkasir:true,pch:true,bbig:true,bch:true,bkasir:false};
const pc=k=>{const v=C()[k];return v===undefined?PDEF[k]:v};
const qNo=tx=>{const m=String(tx&&tx.no||"").match(/-(\d{1,4})$/);return m?"#"+(+m[1]):""};
const BOTL=" · Botol";
const pWidth=()=>Number(C().paper)===48?48:32;
const pKinds=()=>{const k=[];if(pc("pcust"))k.push("cust");if(pc("pbar"))k.push("bar");return k.length?k:["cust"]};
async function logoRaster(W){const pct=Math.max(30,Math.min(80,+pc("plsize")||50)),key=W+":"+pct;if(LOGO_RAS&&LOGO_RAS.k===key)return LOGO_RAS.b;
  try{const sym=document.getElementById("logo");if(!sym)return null;const vb=(sym.getAttribute("viewBox")||"0 0 1565 1015").trim().split(/\s+/).map(Number);
    const dots=W===48?576:384,w=Math.max(64,Math.round(dots*pct/100/8)*8),h=Math.max(8,Math.round(w*vb[3]/vb[2]));
    const svg=`<svg xmlns="http://www.w3.org/2000/svg" viewBox="${vb.join(" ")}" width="${w}" height="${h}" style="color:#000">${sym.innerHTML}</svg>`;
    const img=new Image();await new Promise((ok,no)=>{img.onload=ok;img.onerror=no;img.src="data:image/svg+xml;charset=utf-8,"+encodeURIComponent(svg)});
    const cv=document.createElement("canvas");cv.width=w;cv.height=h;const g=cv.getContext("2d");g.fillStyle="#fff";g.fillRect(0,0,w,h);g.drawImage(img,0,0,w,h);
    const d=g.getImageData(0,0,w,h).data,xb=w/8,out=[29,118,48,0,xb&255,xb>>8,h&255,h>>8];
    for(let y=0;y<h;y++)for(let x=0;x<xb;x++){let v=0;for(let k=0;k<8;k++){const i=(y*w+x*8+k)*4;if((d[i]+d[i+1]+d[i+2])/3<140)v|=128>>k}out.push(v)}
    LOGO_RAS={k:key,b:out};return out}catch(e){return null}}
/* satu struk (kind: "cust" pelanggan, "bar" barista) → array byte ESC/POS */
function escOne(tx,kind,logo){const c=C(),st=K.store||{},W=pWidth(),hr="-".repeat(W),B=[];
  const raw=a=>{for(let i=0;i<a.length;i++)B.push(a[i])},ln=s=>{for(const ch of asc(s))B.push(ch.charCodeAt(0));B.push(10)};
  const lr=(a,b)=>{a=asc(a);b=asc(b);const sp=W-a.length-b.length;return sp>=1?a+" ".repeat(sp)+b:a.slice(0,W)+"\n"+" ".repeat(Math.max(0,W-b.length))+b};
  const dt=new Date(tx.at||Date.now()),tm=dt.toLocaleTimeString("id-ID",{hour:"2-digit",minute:"2-digit"}),dd=dt.toLocaleDateString("id-ID"),q=qNo(tx);
  raw([27,64,27,116,0]);
  if(kind==="bar"){
    raw([27,97,1,27,69,1]);ln("STRUK BARISTA");raw([27,69,0]);
    if(q){raw([27,33,48]);ln(q);raw([27,33,0])}
    ln(tm+(pc("bch")&&tx.ch?" - "+tx.ch:""));raw([27,97,0]);ln(hr);
    const big=pc("bbig");
    (tx.items||[]).forEach(i=>{const nm=String(i.n||""),bot=nm.endsWith(BOTL),n=bot?nm.slice(0,-BOTL.length):nm;
      if(big)raw([27,33,16,27,69,1]);wrap(asc(i.q+"x "+n),W).forEach(ln);if(big)raw([27,33,0,27,69,0]);
      if(bot)ln("   BOTOL - ambil dari stok")});
    ln(hr);
    if(tx.note){raw([27,33,16,27,69,1]);wrap(asc("Catatan: "+tx.note),W).forEach(ln);raw([27,33,0,27,69,0]);ln(hr)}
    if(pc("bkasir"))ln("Kasir: "+(tx.by||"-"));
    ln(tx.no||"");
  }else{
    raw([27,97,1]);
    if(logo&&logo.length){raw(logo);B.push(10)}
    raw([27,33,48]);wrap(asc(c.name||st.name||"521 Coffee"),W/2).forEach(ln);raw([27,33,0]);
    if(c.sub)wrap(asc(c.sub),W).forEach(ln);
    if(pc("paddr")&&st.place)wrap(asc(st.place),W).forEach(ln);
    if(pc("pwa")&&st.wa)ln("WA "+st.wa);
    if(pc("pig")&&st.ig)ln("IG "+st.ig);
    if(pc("pque")&&q){ln("");ln("No. antrian");raw([27,33,48]);ln(q);raw([27,33,0])}
    raw([27,97,0]);ln(hr);ln(tx.no||"");ln(lr(dd,tm));if(pc("pkasir"))ln("Kasir: "+(tx.by||"-"));if(pc("pch")&&tx.ch)ln("Pesanan: "+tx.ch);ln(hr);
    (tx.items||[]).forEach(i=>{wrap(asc(i.n),W).forEach(ln);ln(lr("  "+i.q+" x "+rp(i.pr),rp(i.pr*i.q)))});
    if(tx.note){ln(hr);wrap(asc("Catatan: "+tx.note),W).forEach(ln)}
    ln(hr);if(tx.vd)ln(lr("Voucher "+(tx.vc||""),"-"+rp(tx.vd)));if((tx.disc||0)-(tx.vd||0)>0)ln(lr("Diskon","-"+rp(tx.disc-(tx.vd||0))));
    raw([27,69,1]);ln(lr("TOTAL",rp(tx.total)));raw([27,69,0]);ln(lr(tx.pm||"-",rp(tx.paid)));
    if(isC(tx.pm)&&tx.paid>=tx.total)ln(lr("Kembali",rp(tx.paid-tx.total)));
    ln(hr);raw([27,97,1]);wrap(asc(c.foot),W).forEach(ln);raw([27,97,0]);
  }
  return B}
/* beberapa struk dalam satu kiriman: dipotong otomatis (bila printer punya pisau) atau diberi garis sobek */
function escJob(tx,kinds,logo){const W=pWidth(),B=[];kinds.forEach((k,i)=>{const b=escOne(tx,k,logo);for(let j=0;j<b.length;j++)B.push(b[j]);
    if(pc("pcut"))B.push(27,100,4,29,86,66,0);
    else{B.push(27,100,i<kinds.length-1?2:4);if(i<kinds.length-1){const s="- - - sobek di sini - - -";B.push(27,97,1);for(const ch of s.slice(0,W))B.push(ch.charCodeAt(0));B.push(10,27,97,0,27,100,2)}}});
  return new Uint8Array(B)}
function escTx(tx,logo){return escJob(tx,["cust"],logo)}
async function btPrintTx(tx,quiet,kinds){
  if(!NBT()||!tx)return;kinds=kinds||pKinds();
  if(!btName()){await btRefresh();if(!btName()){if(!quiet)btSheet(tx);return}}
  const send=async()=>{const logo=kinds.includes("cust")&&pc("plogo")?await logoRaster(pWidth()):null;await A521.bt.print(b64(escJob(tx,kinds,logo)))};
  try{await send();toast(kinds.length>1?"Struk pelanggan & barista dicetak 🧾":kinds[0]==="bar"?"Struk barista dicetak 🧾":"Struk dicetak 🧾",1)}
  catch(e){const code=e&&e.code;
    if(code==="no_printer"){if(!quiet)btSheet(tx);return}
    if((code==="off"||code==="perm")&&!quiet){try{await A521.bt.prepare();await send();toast("Struk dicetak 🧾",1);return}catch(x){e=x}}
    if(quiet){toast(btErr(e),1);return}try{copy(printText(tx),btErr(e)+" Struk tersalin untuk aplikasi printer.")}catch(x){toast(btErr(e),1)}}}
const btTest=()=>({no:"521-TES-0012",at:new Date().toISOString(),by:(me&&me.name)||"Kasir",ch:"Offline Store",items:[{n:"Palm Sugar",q:2,pr:15000},{n:"Matcha Latte · Botol",q:1,pr:20000}],disc:0,total:50000,pm:"Cash",paid:50000,note:"Tes cetak - less sugar"});
/* pratinjau: ubah byte ESC/POS kembali menjadi tampilan kertas */
function escHTML(u){const W=pWidth(),dots=W===48?576:384,out=[];let al="left",sz=0,bd=false,line="",i=0;
  const flush=()=>{const t=esc(line)||"&nbsp;",s=`text-align:${al};font-weight:${bd?800:500}`;
    out.push(sz&32?`<div style="${s};font-size:2em;line-height:1.15">${t}</div>`:sz&16?`<div style="${s};height:2.5em"><span style="display:inline-block;transform:scaleY(2);transform-origin:top">${t}</span></div>`:`<div style="${s}">${t}</div>`);line=""};
  while(i<u.length){const b=u[i];
    if(b===27){const c=u[i+1];if(c===64){i+=2;continue}if(c===97){al=["left","center","right"][u[i+2]]||"left";i+=3;continue}if(c===33){sz=u[i+2];i+=3;continue}if(c===69){bd=!!u[i+2];i+=3;continue}
      if(c===100){if(line)flush();for(let k=0;k<u[i+2];k++)out.push("<div>&nbsp;</div>");i+=3;continue}i+=3;continue}
    if(b===29){const c=u[i+1];if(c===86){out.push('<div class="pcut">✂ dipotong otomatis</div>');i+=4;continue}
      if(c===118){const xb=u[i+4]+u[i+5]*256,h=u[i+6]+u[i+7]*256,w=xb*8,cv=document.createElement("canvas");cv.width=w;cv.height=h;const g=cv.getContext("2d"),im=g.createImageData(w,h);
        for(let y=0;y<h;y++)for(let x=0;x<w;x++){const on=(u[i+8+y*xb+(x>>3)]>>(7-(x&7)))&1,p=(y*w+x)*4;im.data[p]=im.data[p+1]=im.data[p+2]=on?20:255;im.data[p+3]=255}
        g.putImageData(im,0,0);out.push(`<div style="text-align:${al}"><img src="${cv.toDataURL()}" alt="Logo" style="width:${(w/dots*100).toFixed(1)}%;image-rendering:pixelated"></div>`);i+=8+xb*h;continue}
      i+=3;continue}
    if(b===10){flush();i++;continue}line+=String.fromCharCode(b);i++}
  if(line)flush();return `<div class="paper" style="--w:${W}">${out.join("")}</div>`}
let PV={k:"cust"};
async function pvSheet(k){if(k)PV.k=k;const tx=D.tx.slice().reverse().find(x=>x.status!=="cancelled"&&x.items&&x.items.length)||btTest();
  const kinds=PV.k==="both"?pKinds():[PV.k],logo=kinds.includes("cust")&&pc("plogo")?await logoRaster(pWidth()):null;
  show(`<h2>Contoh struk</h2><div class="chips" style="margin-top:0">${[["cust","Pelanggan"],["bar","Barista"],["both","Keduanya"]].map(([v,l])=>`<button data-a="pvk" data-v="${v}" aria-pressed="${PV.k===v}">${l}</button>`).join("")}</div>
  <div class="chips" style="margin-top:0"><button data-a="pvpaper" data-v="32" aria-pressed="${pWidth()===32}">58 mm</button><button data-a="pvpaper" data-v="48" aria-pressed="${pWidth()===48}">80 mm</button></div>
  <div class="pvwrap">${escHTML(escJob(tx,kinds,logo))}</div>${NBT()?`<button class="btn" data-a="pvprint">${ic("print")}Cetak contoh ini</button>`:""}`);PV.tx=tx;PV.kinds=kinds}
const pTog=(k,t,s)=>`<div class="swrow"><span><b>${t}</b>${s?`<small>${s}</small>`:""}</span><label class="tgl" aria-label="${esc(t)}"><input type="checkbox" data-pk="${k}" ${pc(k)?"checked":""}><span></span></label></div>`;
function btSetInner(){const c=C(),st=BTS.st||{},T=BTS.tab||"umum";
  const tabs=`<div class="chips ptabs" role="tablist">${[["umum","Umum"],["cust","Struk pelanggan"],["bar","Struk barista"]].map(([v,l])=>`<button data-a="ptab" data-v="${v}" aria-pressed="${T===v}">${l}</button>`).join("")}</div>`;
  let body="";
  if(T==="umum")body=`<div class="btbox ${st.addr?"on":""}">${ic("print")}<span><b>${st.addr?"Printer: "+esc(st.name||st.addr):"Belum memilih printer"}</b><small>${st.addr?"Siap mencetak struk.":"Printer thermal Bluetooth 58/80 mm (ESC/POS)."}</small></span></div>
    <button class="btn" data-a="btfind">${ic("print")}${st.addr?"Ganti printer":"Cari printer"}</button>
    ${st.addr?`<div class="two"><button class="btn ghost" data-a="bttest2">Cetak tes</button><button class="btn ghost" data-a="btforget" style="color:var(--warn)">Lupakan printer</button></div>`:""}
    <h3>Setelah bayar</h3>${pTog("pauto","Cetak otomatis setelah bayar","Struk langsung keluar saat layar Lunas muncul")}
    ${pTog("pcust","Struk pelanggan","Untuk diberikan ke pembeli (dengan harga)")}${pTog("pbar","Struk barista","Untuk barista membuat pesanan (tanpa harga)")}
    <p class="note">${pc("pcust")&&pc("pbar")?"1 penjualan = <b>2 struk</b>: pelanggan lalu barista, dalam satu kali cetak.":"Hanya 1 struk per penjualan."} Tombol <b>Printer</b> di layar Lunas mencetak struk yang sama.</p>
    <h3>Printer</h3><div class="lbl" style="margin-top:0">Lebar kertas</div><div class="chips"><button data-a="paper" data-v="32" aria-pressed="${pWidth()===32}">58 mm</button><button data-a="paper" data-v="48" aria-pressed="${pWidth()===48}">80 mm</button></div>
    ${pTog("pcut","Potong otomatis (auto cutter)","Aktifkan hanya bila printer punya pisau pemotong. Tanpa pisau, antar-struk diberi garis sobek.")}
    <h3>Logo</h3>${pTog("plogo","Cetak logo 521","Di atas struk pelanggan")}
    ${pc("plogo")?`<label for="plsize">Ukuran logo</label><div class="rng"><input type="range" id="plsize" min="30" max="80" step="10" value="${+pc("plsize")||50}"><output id="plsizeo">${+pc("plsize")||50}%</output></div>`:""}
    <p class="note">Printer yang meminta PIN saat dipasangkan biasanya memakai <b>0000</b> atau <b>1234</b>.</p>`;
  else if(T==="cust")body=`<p class="note" style="margin-top:0">Isi struk untuk pembeli. Nama toko, tagline & pesan penutup diatur di Atur → Identitas toko; lokasi, WA & Instagram di Kabar → Info toko.</p>
    ${pTog("pque","Nomor antrian","Nomor besar yang sama dengan struk barista")}${pTog("paddr","Lokasi toko",esc((K.store||{}).place||"Belum diisi"))}
    ${pTog("pwa","Nomor WhatsApp",esc((K.store||{}).wa||"Belum diisi"))}${pTog("pig","Instagram",esc((K.store||{}).ig||"Belum diisi"))}
    ${pTog("pkasir","Nama kasir","")}${pTog("pch","Asal pesanan","Offline Store, GoFood, WhatsApp, …")}`;
  else body=`<p class="note" style="margin-top:0">Struk barista <b>tanpa harga</b>: nomor antrian besar, jam, daftar menu & jumlah, dan catatan pesanan (diisi kasir saat bayar). Menu botol ditandai "ambil dari stok".</p>
    ${pTog("bbig","Huruf menu besar","Lebih mudah dibaca dari jauh")}${pTog("bch","Asal pesanan","")}${pTog("bkasir","Nama kasir","")}`;
  return `${tabs}${body}<button class="btn ghost" data-a="pvopen">${ic("eye")}Lihat contoh struk</button>`}
let onote="";
document.addEventListener("change",e=>{const t=e.target;if(!t||!t.dataset||!t.dataset.pk)return;C()[t.dataset.pk]=!!t.checked;save();LOGO_RAS=null;btPaint()});
document.addEventListener("input",e=>{const t=e.target;if(!t)return;if(t.id==="onote"){onote=t.value;return}
  if(t.id==="plsize"){C().plsize=+t.value;save();LOGO_RAS=null;const o=$("#plsizeo");if(o)o.textContent=t.value+"%"}});
document.addEventListener("click",e=>{const b=e.target.closest&&e.target.closest("[data-a]");if(!b)return;const a=b.dataset.a,v=b.dataset.v;
  const H={ptab:()=>{BTS.tab=v;btPaint()},pvopen:()=>pvSheet(),pvk:()=>pvSheet(v),pvpaper:()=>{C().paper=+v;save();LOGO_RAS=null;pvSheet()},
    pvprint:()=>{if(PV.tx)btPrintTx(PV.tx,false,PV.kinds)}};
  if(!H[a])return;e.preventDefault();e.stopImmediatePropagation();H[a]()},true);
