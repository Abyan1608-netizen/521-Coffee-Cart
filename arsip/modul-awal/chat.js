/* ===== Chat 521 (pop up di Kasir) =====
   Asisten produk 521 + wawasan kopi internasional. Pakai Claude lewat capability `sample` (memakai akun Claude
   yang membuka halaman); bila tidak tersedia, jawab dari pengetahuan bawaan di bawah (tetap jalan offline). */
const BOSS="Pak Urwah Seftion";
const CKB=[
 {k:/arabika|arabica|robusta|liberika|liberica|excelsa|jenis kopi|spesies/i,e:"🌱",t:"Arabika vs Robusta",a:"Di dunia ada dua spesies kopi utama:\n- **Arabika (Coffea arabica)**: tumbuh di dataran tinggi (±1.000–2.000 mdpl), rasa lebih kompleks, asam buahnya cerah, kafein ±1,2–1,5%. Sekitar 60% produksi kopi dunia.\n- **Robusta (Coffea canephora)**: tumbuh di dataran rendah, tubuh (body) tebal, pahit lebih tegas, kafein ±2–2,7%, crema espresso lebih tebal.\nAda juga **Liberika** dan **Excelsa** yang lebih jarang, aromanya khas seperti nangka.\nIndonesia termasuk produsen kopi terbesar dunia, dan Robusta mendominasi produksinya."},
 {k:/espresso|crema|shot/i,e:"☕",t:"Espresso",a:"**Espresso** lahir di Italia awal abad ke-20. Air panas (±90–96°C) ditekan ±9 bar melewati ±18 g bubuk kopi halus selama ±25–30 detik, menghasilkan ±36 g cairan pekat.\n- **Crema** adalah busa keemasan di atasnya, dari minyak dan gas CO₂ kopi.\n- Espresso menjadi dasar latte, cappuccino, americano, dan flat white."},
 {k:/latte|cappuccino|flat white|macchiato|americano|perbedaan minuman|beda.*(latte|cappuccino)/i,e:"🥛",t:"Latte, cappuccino, americano",a:"Semua berbasis espresso, bedanya di susu dan air:\n- **Americano**: espresso + air panas. Ringan, kopinya tetap terasa.\n- **Latte**: espresso + banyak susu steamed + busa tipis. Lembut.\n- **Cappuccino**: espresso, susu, dan busa kurang lebih sepertiga-sepertiga. Lebih berbusa dan terasa kopinya.\n- **Flat white** (Australia/Selandia Baru): susu lebih sedikit dengan microfoam halus, rasa kopi lebih kuat.\n- **Macchiato**: espresso dengan sedikit busa susu di atasnya."},
 {k:/roast|sangrai|light|medium|dark/i,e:"🔥",t:"Tingkat sangrai (roasting)",a:"Roasting mengubah biji hijau menjadi cokelat dan memunculkan aroma (reaksi Maillard dan karamelisasi).\n- **Light roast**: asam buah dan floral lebih menonjol, karakter asal biji paling terasa.\n- **Medium roast**: seimbang, manis karamel dan cokelat.\n- **Dark roast**: pahit-smoky, body tebal, karakter asal biji berkurang.\nTanda penting: *first crack* (bunyi letupan pertama) menandai biji mulai matang."},
 {k:/proses|natural|washed|full wash|honey|giling basah|wet hull|pascapanen|pasca panen/i,e:"🍒",t:"Proses pascapanen",a:"Cara buah kopi diolah sangat memengaruhi rasa:\n- **Washed (full wash)**: kulit dan lendir dibuang lalu difermentasi dan dicuci. Rasa bersih dan asamnya cerah.\n- **Natural (dry)**: buah utuh dijemur. Rasa manis buah, kadang winey.\n- **Honey**: sebagian lendir (mucilage) dibiarkan saat dijemur. Manis dan body sedang.\n- **Giling basah (wet hulled)**: khas Indonesia (Sumatra). Earthy, body tebal, asam rendah."},
 {k:/gayo|toraja|kintamani|temanggung|flores|bajawa|java|jawa|sumatra|mandailing|papua|wamena|kopi indonesia|nusantara|single origin/i,e:"🇮🇩",t:"Kopi Indonesia di mata dunia",a:"Indonesia punya banyak kopi terkenal di dunia:\n- **Gayo (Aceh)**: arabika, body tebal, rempah dan cokelat.\n- **Mandailing (Sumatra Utara)**: earthy dan herbal. Namanya populer di pasar internasional.\n- **Toraja (Sulawesi)**: seimbang, ada rempah dan karamel.\n- **Kintamani (Bali)**: asam segar seperti jeruk, ditanam bersama tanaman jeruk.\n- **Flores Bajawa**: manis cokelat dan floral.\n- **Temanggung (Jawa Tengah)**: robusta dan arabika dengan aroma tembakau dan cokelat. Biji Black Caffe 521 berasal dari sini.\n- **Java**: sejak era kolonial, nama \"Java\" sampai menjadi julukan kopi di dunia."},
 {k:/sejarah|asal.?usul|kaldi|ethiopia|etiopia|yaman|mocha|ditemukan/i,e:"📜",t:"Sejarah kopi",a:"Menurut legenda, kopi ditemukan di **Ethiopia** oleh penggembala bernama **Kaldi**, yang melihat kambingnya bersemangat setelah memakan buah merah.\n- Abad ke-15: kopi diseduh para sufi di **Yaman**. Pelabuhan **Mocha** jadi pusat perdagangannya.\n- Abad ke-17: kedai kopi menyebar ke Turki, Eropa, lalu dunia.\n- 1696–1699: VOC membawa bibit kopi ke Jawa, dan Indonesia menjadi salah satu produsen awal dunia."},
 {k:/v60|pour.?over|manual brew|seduh manual|french press|aeropress|kalita|chemex|tubruk|vietnam drip/i,e:"🫖",t:"Metode seduh manual",a:"Beberapa metode seduh populer di dunia:\n- **V60 / pour over (Jepang)**: rasa bersih dan jernih. Rasio umum 1:15 (15 g kopi : 225 g air), air ±90–94°C.\n- **French press (Prancis)**: direndam ±4 menit, body tebal.\n- **AeroPress**: praktis, dengan tekanan tangan.\n- **Vietnam drip (phin)**: tetes perlahan, biasa dengan susu kental manis.\n- **Kopi tubruk (Indonesia)**: bubuk diseduh langsung di gelas, ampasnya mengendap."},
 {k:/cold brew|es kopi|iced|kopi dingin/i,e:"🧊",t:"Cold brew vs iced coffee",a:"- **Cold brew**: bubuk kasar direndam air dingin 12–24 jam. Rasanya halus, asam rendah, manis alami.\n- **Iced coffee**: kopi diseduh panas lalu didinginkan dengan es. Aromanya lebih cerah.\nKeduanya populer di Amerika dan Asia, termasuk tren **es kopi susu** di Indonesia."},
 {k:/kafein|caffeine|begadang|ngantuk|berapa cangkir|sehari/i,e:"⚡",t:"Kafein",a:"- Satu shot espresso berisi ±60–75 mg kafein. Secangkir kopi seduh ±80–120 mg.\n- Banyak lembaga kesehatan menyebut hingga ±400 mg per hari umumnya aman untuk orang dewasa sehat. Ibu hamil disarankan lebih sedikit.\n- Robusta berkafein hampir dua kali lipat arabika.\nKalau pelanggan sensitif kafein, tawarkan menu non-kopi seperti Matcha Latte."},
 {k:/cupping|flavor wheel|tasting|rasa kopi|acidity|body|aftertaste|q.?grader|sca/i,e:"👅",t:"Cara mencicipi kopi",a:"Para profesional memakai **cupping** standar **SCA (Specialty Coffee Association)**:\n- **Aroma**: bau bubuk dan seduhan.\n- **Acidity**: rasa segar dan asam yang menyenangkan, bukan asam basi.\n- **Body**: kekentalan di mulut.\n- **Sweetness & aftertaste**: manis dan rasa yang tertinggal.\nSkor 80+ dari 100 masuk kategori *specialty coffee*. Penilainya disebut **Q-Grader**."},
 {k:/latte art|rosetta|tulip|microfoam|steam susu|susu/i,e:"🎨",t:"Latte art & steam susu",a:"- Susu di-steam sampai ±55–65°C. Lebih panas dari itu, manis alaminya hilang.\n- Tujuannya **microfoam**: busa halus mengilap seperti cat.\n- Pola dasar latte art: **heart**, **tulip**, dan **rosetta**, dituang dari dekat permukaan dengan goyangan halus.\nKompetisi tingkat dunia: **World Latte Art Championship**."},
 {k:/budaya|dunia|italia|turki|turkish|internasional|negara|kopi luwak|luwak/i,e:"🌍",t:"Budaya kopi dunia",a:"- **Italia**: espresso diminum cepat sambil berdiri di bar. Cappuccino umumnya hanya pagi hari.\n- **Turki**: kopi digiling sangat halus dan dimasak di *cezve*. Masuk Warisan Budaya Tak Benda UNESCO.\n- **Ethiopia**: upacara kopi (*buna*) sebagai tanda keramahan.\n- **Vietnam**: kopi susu kental manis dan *egg coffee*.\n- **Indonesia**: kopi tubruk, warung kopi Aceh, es kopi susu gula aren, dan kopi luwak yang terkenal di dunia."},
 {k:/gula aren|palm sugar|aren|kopi susu/i,e:"🌴",t:"Gula aren",a:"Gula aren dibuat dari nira pohon aren (*Arenga pinnata*). Rasa manisnya legit dengan aroma karamel-smoky. Gula ini membuat **es kopi susu gula aren** menjadi ikon minuman kopi modern Indonesia sejak ±2017.\nDi 521, rasa ini hadir di menu **Palm Sugar**."},
 {k:/butterscotch|karamel|caramel/i,e:"🧈",t:"Butterscotch",a:"**Butterscotch** adalah perisa manis dari gula cokelat dan mentega yang dimasak bersama, mirip karamel tetapi lebih gurih. Asalnya dari Doncaster, Inggris (abad ke-19).\nDi 521, rasa ini dipadukan dengan kopi susu di menu **Butterscotch**."},
 {k:/matcha|teh hijau|green tea/i,e:"🍵",t:"Matcha",a:"**Matcha** adalah bubuk daun teh hijau Jepang yang ditanam di tempat teduh sebelum dipanen, lalu digiling halus. Rasanya *umami*, sedikit pahit, dan segar.\nMatcha mengandung kafein dan L-theanine, jadi energinya terasa lebih tenang.\nDi 521, ada **Matcha Latte** untuk pelanggan yang ingin minuman tanpa kopi."},
 {k:/simpan|menyimpan|kemasan|fresh|segar|basi|expired|kedaluwarsa biji/i,e:"📦",t:"Menyimpan kopi",a:"- Simpan biji di wadah kedap udara, jauh dari cahaya, panas, dan lembap.\n- Biji paling enak dipakai ±7–30 hari setelah roasting.\n- Bubuk kopi cepat kehilangan aroma, jadi giling sesaat sebelum seduh.\n- Hindari kulkas untuk pemakaian harian karena kopi menyerap bau dan embun."}
];
const CTIPS=[0,1,4,5,6,10,12,3,7,11];
let chatH=[],chatBusy=false,chatCtl=null,SMP=null,smpOff=false;
(async()=>{try{if(window.claude&&claude.use)SMP=await claude.use("sample")}catch(e){SMP=null}})();
const chatSalam=()=>"Assalamu'alaikum warahmatullahi wabarakatuh 🙏";
function chatMenu(){return D.prod.filter(p=>p.active).map(p=>`- ${p.name} (${p.cat||"-"}${p.size?", "+p.size:""}): ${rp(price(p))}${p.out?" · sedang habis":""}${p.desc?" — "+p.desc:""}`).join("\n")}
function chatRules(){const s=K.store||{};return `Kamu adalah "Asisten 521", asisten chat untuk kasir dan barista ${C().name||"521 Coffee Cart"}, sebuah coffee cart di ${s.place||"Indonesia"} (jam buka ${s.hours||"-"}). Tagline: "${C().sub||""}".
TUGAS (hanya dua topik ini):
1. Menjelaskan produk 521 berdasarkan DATA MENU di bawah, termasuk cara menjelaskan dan menawarkannya dengan baik kepada pelanggan.
2. Mengajarkan wawasan kopi secara internasional: sejarah, spesies dan varietas, kopi Indonesia dan dunia, proses pascapanen, roasting, metode seduh, espresso dan minuman berbasis susu, latte art, cupping, budaya kopi berbagai negara, istilah barista, kafein, penyimpanan biji. Boleh juga bahan minuman di menu 521 (gula aren, butterscotch, matcha).
GAYA JAWABAN:
- SELALU awali dengan salam: "Assalamu'alaikum warahmatullahi wabarakatuh 🙏".
- Bahasa Indonesia yang santun, baik, tertata, dan diksinya sopan. Sapa lawan bicara dengan "Kak".
- Gunakan emoji yang sesuai dengan topik yang dibahas (secukupnya, 2–4 emoji).
- Rapi dan ringkas: paragraf pendek atau poin "- ". Tebalkan istilah penting dengan **dua bintang**. Maksimal ±170 kata kecuali diminta lebih rinci.
- Akurat. Jangan mengarang fakta, harga, atau menu yang tidak ada di data. Bila ragu, katakan dengan jujur.
- JANGAN membuka resep, takaran, HPP, modal, atau data internal toko.
JIKA PERTANYAAN DI LUAR DUA TOPIK DI ATAS (misalnya PR sekolah, politik, gosip, coding, kesehatan pribadi, atau hal pribadi), tolak dengan santun. Awali dengan salam, lalu sampaikan bahwa kamu hanya boleh membahas produk 521 dan wawasan kopi, dan kalau menjawab di luar itu "nanti saya ditegur ${BOSS}, atau bahkan bisa di-DO ${BOSS} 🙏😅". Setelah itu tawarkan satu topik kopi yang menarik.
DATA MENU 521 (harga dalam Rupiah):
${chatMenu()}`}
/* Jawaban bawaan (tanpa Claude) */
const OFF=/\b(pr|tugas sekolah|matematika|politik|pemilu|presiden|gosip|artis|bola|game|coding|program|pacar|cinta|zodiak|saham|crypto|bitcoin|resep masakan|obat|sakit|diet|cuaca|berita)\b/i;
const COFFEEISH=/kopi|coffee|kafe|cafe|barista|seduh|biji|bean|susu|menu|minum|harga|521|rasa|aroma|espresso|latte|teh|matcha|aren|butter|pelanggan/i;
function chatLocal(q){const S=chatSalam(),ql=q.toLowerCase();
  const P=D.prod.filter(p=>p.active&&ql.includes(p.name.toLowerCase().split(" ")[0]));
  if(P.length&&!/sejarah|asal/i.test(q))return `${S}\n\nTerima kasih sudah bertanya, Kak 😊 Berikut penjelasan menunya:\n\n${P.map(p=>`☕ **${p.name}** · ${rp(price(p))}${p.out?" (sedang habis)":""}\n${p.desc||"Salah satu menu andalan 521."}`).join("\n\n")}\n\n💡 Saat menawarkan, sebutkan rasa utamanya dulu, lalu tanyakan apakah pelanggan suka manis atau pahit.`;
  if(/menu|produk|jual apa|ada apa|rekomendasi|andalan|harga/i.test(q))return `${S}\n\nBerikut menu 521 yang tersedia, Kak ☕✨\n\n${D.prod.filter(p=>p.active).map(p=>`- **${p.name}** · ${rp(price(p))}${p.out?" (habis)":""}${p.desc?"\n  "+p.desc:""}`).join("\n")}\n\n💡 Untuk pelanggan baru, tawarkan yang paling laris dulu.`;
  const hit=CKB.find(x=>x.k.test(q));
  if(hit)return `${S}\n\n${hit.e} **${hit.t}**\n\n${hit.a}\n\nSemoga menambah wawasan, Kak 🙏`;
  if(/^(halo|hai|hi|assalamu|selamat|pagi|siang|sore|malam|permisi)/i.test(q.trim()))return `${S}\n\nWa'alaikumussalam juga, Kak 😊 Saya Asisten 521. Saya siap membantu menjelaskan **menu 521** dan berbagi **wawasan kopi dari berbagai negara** ☕🌍\n\nSilakan pilih topik di bawah atau ketik pertanyaan.`;
  if(OFF.test(q)||!COFFEEISH.test(q))return `${S}\n\nMohon maaf sebelumnya, Kak 🙏 Saya hanya diperbolehkan membahas **produk 521** dan **wawasan seputar kopi**. Kalau saya menjawab di luar itu, nanti saya ditegur ${BOSS}, atau bahkan bisa di-DO ${BOSS} 😅\n\nBagaimana kalau kita bahas yang ini saja: *apa beda Arabika dan Robusta?* ☕🌱`;
  return `${S}\n\nPertanyaan yang bagus, Kak ☕ Saat ini saya sedang memakai pengetahuan bawaan, jadi jawabannya terbatas. Coba tanyakan salah satu topik ini:\n${CKB.slice(0,8).map(x=>`- ${x.e} ${x.t}`).join("\n")}`;
}
function chatTip(){const d=new Date(),i=CTIPS[(d.getFullYear()*372+d.getMonth()*31+d.getDate())%CTIPS.length],x=CKB[i];return `${chatSalam()}\n\n${x.e} **Wawasan kopi hari ini: ${x.t}**\n\n${x.a}\n\nSemoga bermanfaat dan bisa dibagikan ke pelanggan, Kak 😊`}
/* Tampilan */
function chatFmt(t){return esc(t).replace(/\*\*(.+?)\*\*/g,"<b>$1</b>").replace(/(^|[\s(])\*(?!\s)(.+?)\*(?=[\s).,!?]|$)/g,"$1<i>$2</i>").split(/\n/).map(l=>/^\s*[-•]\s+/.test(l)?`<span class="cli">${l.replace(/^\s*[-•]\s+/,"")}</span>`:l).join("<br>").replace(/<br>(<span class="cli">)/g,"$1").replace(/(<\/span>)<br>/g,"$1")}
const CHIPS=[["☕ Jelaskan menu kita","Tolong jelaskan semua menu 521 dan cara menawarkannya ke pelanggan."],["🌱 Arabika vs Robusta","Apa beda kopi arabika dan robusta?"],["🇮🇩 Kopi Indonesia","Apa saja kopi Indonesia yang terkenal di dunia?"],["🌍 Budaya kopi dunia","Bagaimana budaya minum kopi di berbagai negara?"],["💡 Wawasan hari ini","__tip"],["🔥 Tingkat roasting","Apa beda light, medium, dan dark roast?"]];
function chatRender(scroll){const o=$("#chat");if(!o)return;const L=o.querySelector(".cmsgs");
  L.innerHTML=(chatH.length?"":`<div class="cwel"><b>Chat 521</b><span>Tanya seputar menu 521 dan wawasan kopi dunia ☕🌍</span></div>`)+chatH.map(m=>`<div class="cm ${m.role==="user"?"me":"ai"}${m.err?" err":""}">${m.role==="user"?esc(m.content).replace(/\n/g,"<br>"):(m.content?chatFmt(m.content):'<span class="ctyping"><i></i><i></i><i></i></span>')}</div>`).join("");
  o.querySelector(".cchips").innerHTML=CHIPS.map((c,i)=>`<button data-a="c_chip" data-v="${i}"${chatBusy?" disabled":""}>${c[0]}</button>`).join("");
  const sb=o.querySelector("[data-a=c_send]");sb.hidden=chatBusy;o.querySelector("[data-a=c_stop]").hidden=!chatBusy;
  o.querySelector(".cmode").textContent=SMP&&!smpOff?"Didukung Claude":"Mode pengetahuan bawaan";
  if(scroll!==false)L.scrollTop=L.scrollHeight}
function chatOpen(){let o=$("#chat");if(!o){o=document.createElement("div");o.id="chat";o.className="chat";
    o.innerHTML=`<div class="cbox" role="dialog" aria-modal="true" aria-label="Chat 521"><div class="chd"><span class="pv-av"><svg aria-hidden="true"><use href="#logo"/></svg></span><span class="pv-who"><b>Chat 521</b><small class="cmode"></small></span><button class="pv-x" data-a="c_clear" aria-label="Mulai percakapan baru" title="Percakapan baru">↺</button><button class="pv-x" data-a="c_close" aria-label="Tutup chat">${ic("x")}</button></div>
    <div class="cmsgs" aria-live="polite"></div><div class="cchips scroll"></div>
    <div class="cin"><textarea id="cq" rows="1" placeholder="Tanya soal menu atau kopi…" aria-label="Pesan untuk Chat 521"></textarea><button class="btn sm" data-a="c_send" aria-label="Kirim">Kirim</button><button class="btn sm ghost" data-a="c_stop" hidden>Stop</button></div></div>`;document.body.appendChild(o)}
  o.hidden=false;chatRender();setTimeout(()=>{const q=$("#cq");if(q&&matchMedia("(hover:hover)").matches)q.focus()},60)}
function chatClose(){const o=$("#chat");if(o)o.hidden=true;if(chatCtl)chatCtl.abort()}
async function chatSend(q){q=String(q||"").trim();if(!q||chatBusy)return;
  if(q==="__tip"){chatH.push({role:"user",content:"Wawasan kopi hari ini"},{role:"assistant",content:chatTip()});chatRender();return}
  chatH.push({role:"user",content:q});const a={role:"assistant",content:""};chatH.push(a);chatBusy=true;chatRender();
  if(!SMP||smpOff){await new Promise(r=>setTimeout(r,450));a.content=chatLocal(q);chatBusy=false;chatRender();return}
  chatCtl=new AbortController();
  const turns=chatH.slice(0,-1).filter(m=>m.content&&!m.err).slice(-10);while(turns.length&&turns[0].role!=="user")turns.shift();
  try{const r=await SMP([{role:"user",content:chatRules()},...turns],{cache:false,modelTier:"quick",signal:chatCtl.signal,onText:({text})=>{a.content=text;chatRender()}});a.content=r.text||a.content}
  catch(e){const c=e&&e.code;
    if(c==="cancelled"){a.content=(e.text||a.content||"")+(e.text||a.content?"\n\n_(dihentikan)_":"Dihentikan.")}
    else if(["not_granted","sampling_disabled","not_declared","capability_disabled","capability_removed","session_expired"].includes(c)){smpOff=true;a.content=chatLocal(q)}
    else if(c==="refused"){a.content=chatLocal(q)}
    else{a.content=e&&e.text?e.text:chatLocal(q)}}
  chatBusy=false;chatCtl=null;chatRender()}
function chatAct(a,v){
  if(a==="c_open")chatOpen();else if(a==="c_close")chatClose();
  else if(a==="c_send"){const i=$("#cq");const q=i.value;i.value="";i.style.height="";chatSend(q)}
  else if(a==="c_chip"){const c=CHIPS[+v];if(c)chatSend(c[1])}
  else if(a==="c_stop"){if(chatCtl)chatCtl.abort()}
  else if(a==="c_clear"){if(chatBusy)return;chatH=[];chatRender()}
}
document.addEventListener("keydown",e=>{const o=$("#chat");if(!o||o.hidden)return;
  if(e.key==="Escape"){chatClose();return}
  if(e.target.id==="cq"&&e.key==="Enter"&&!e.shiftKey){e.preventDefault();chatAct("c_send")}});
document.addEventListener("input",e=>{if(e.target.id==="cq"){const t=e.target;t.style.height="";t.style.height=Math.min(120,t.scrollHeight)+"px"}});
document.addEventListener("click",e=>{if(e.target.id==="chat")chatClose()});
