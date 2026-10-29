s=open('p3.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,(s.count(a),a[:90])
    s=s.replace(a,b)
# BT module before newset SETF
rep('const SETF=[','''/* ---------- Printer Bluetooth (Web Bluetooth, ESC/POS) ---------- */
const BT_SVCS=["000018f0-0000-1000-8000-00805f9b34fb","0000ff00-0000-1000-8000-00805f9b34fb","0000ffe0-0000-1000-8000-00805f9b34fb","0000fee7-0000-1000-8000-00805f9b34fb","e7810a71-73ae-499d-8c15-faa9aef0c3f2","49535343-fe7d-4ae5-8fa9-9fafd205e455"];
let BT=null,btMsg="";
const btOK=()=>!!(BT&&BT.ch&&BT.dev&&BT.dev.gatt&&BT.dev.gatt.connected);
async function btConnect(){
  if(!navigator.bluetooth){btMsg="Bluetooth tidak tersedia di tampilan ini. Di dalam aplikasi Claude, halaman tidak diberi izin Bluetooth. Pakai cara salin ke aplikasi printer di bawah.";render();return}
  try{
    const dev=await navigator.bluetooth.requestDevice({acceptAllDevices:true,optionalServices:BT_SVCS});
    btMsg="Menyambungkan ke "+(dev.name||"printer")+"…";render();
    const srv=await dev.gatt.connect();let ch=null;
    for(const s of await srv.getPrimaryServices()){for(const c of await s.getCharacteristics()){if(c.properties.write||c.properties.writeWithoutResponse){ch=c;break}}if(ch)break}
    if(!ch)throw{name:"NoChar"};
    BT={dev,ch};dev.addEventListener("gattserverdisconnected",()=>{btMsg="Printer terputus.";render()});btMsg="";toast("Tersambung ke "+(dev.name||"printer"),1);render();
  }catch(e){const n=e&&e.name;btMsg=n==="NotFoundError"?"Tidak ada printer yang dipilih.":n==="SecurityError"||n==="NotAllowedError"?"Bluetooth diblokir di tampilan ini. Pakai cara salin ke aplikasi printer di bawah.":n==="NoChar"?"Perangkat tersambung, tapi bukan printer thermal yang dikenali.":"Gagal menyambung: "+(e&&e.message||"coba lagi.");render()}
}
async function btPrint(text){
  const ascii=String(text).normalize("NFKD").replace(/[^\\x0a\\x20-\\x7e]/g,"");
  const enc=new TextEncoder().encode(ascii),data=new Uint8Array(enc.length+7);
  data.set([27,64],0);data.set(enc,2);data.set([10,29,86,66,0],enc.length+2);
  for(let i=0;i<data.length;i+=100){const part=data.slice(i,i+100);if(BT.ch.properties.writeWithoutResponse)await BT.ch.writeValueWithoutResponse(part);else await BT.ch.writeValue(part)}
}
const SETF=[''')
# printer folder body: add connect UI at top
rep('''  if(id==="printer")return `<p class="note" style="margin-top:0">Halaman ini belum bisa tersambung langsung ke Bluetooth. Struk dirapikan untuk printer thermal, lalu dicetak lewat aplikasi printer di HP.</p>''','''  if(id==="printer")return `<div class="btbox ${btOK()?"on":""}">${ic("print")}<span><b>${btOK()?"Tersambung: "+esc(BT.dev.name||"Printer"):"Printer belum tersambung"}</b><small>${btOK()?"Tombol Printer di layar Lunas langsung mencetak.":"Untuk printer thermal Bluetooth (BLE) 58/80 mm."}</small></span></div>
  ${btMsg?`<p class="verr">${esc(btMsg)}</p>`:""}
  <div class="chips">${btOK()?'<button data-a="bttest">Cetak tes</button><button data-a="btoff">Putuskan</button>':'<button data-a="bton">Sambungkan printer Bluetooth</button>'}</div>
  <h3>Kalau Bluetooth tidak bisa dari sini</h3><p class="note" style="margin-top:-4px">Di dalam aplikasi Claude, halaman biasanya tidak diberi izin Bluetooth. Struk tetap bisa dicetak lewat aplikasi printer di HP.</p>''')
rep('.verr{color:var(--warn);','''.btbox{display:flex;align-items:center;gap:12px;padding:14px;border-radius:16px;background:var(--sf2);border:1px solid var(--line)}
.btbox svg{width:26px;height:26px;color:var(--mute)}
.btbox.on{border-color:color-mix(in srgb,var(--ok) 45%,var(--line))}.btbox.on svg{color:var(--ok)}
.btbox b{display:block}.btbox small{color:var(--mute)}
.verr{color:var(--warn);''')
# handlers
rep('''  else if(a==="copyp"){const t=D.tx.find(x=>x.no===id);if(t)copy(printText(t),"Struk tersalin. Tempel di aplikasi printer.")}''','''  else if(a==="copyp"){const t=D.tx.find(x=>x.no===id);if(!t)return;if(btOK()){btPrint(printText(t)).then(()=>toast("Struk dicetak",1),()=>{copy(printText(t),"Gagal mencetak. Struk tersalin untuk aplikasi printer.")})}else copy(printText(t),"Struk tersalin. Tempel di aplikasi printer.")}''')
rep('''  else if(a==="paper"){''','''  else if(a==="bton"){btConnect()}
  else if(a==="btoff"){try{BT.dev.gatt.disconnect()}catch(x){}BT=null;btMsg="";render()}
  else if(a==="bttest"){btPrint(printText({no:"TES-PRINTER",at:iso(),by:me.name,items:[{n:"Tes cetak",q:1,pr:0}],disc:0,total:0,pm:"-",paid:0})).then(()=>toast("Tes terkirim ke printer",1),e=>{btMsg="Gagal mengirim ke printer: "+(e&&e.message||"");render()})}
  else if(a==="paper"){''')
# printer folder description
rep('''["printer","print","Printer Bluetooth",()=>`Kertas ${Number(C().paper)===48?"80":"58"} mm · format struk`],''','''["printer","print","Printer Bluetooth",()=>`${btOK()?"Tersambung":"Belum tersambung"} · kertas ${Number(C().paper)===48?"80":"58"} mm`],''')
open('p3.src.html','w').write(s);print('ok')
