const CHIPS=[["☕","Jelaskan menu kita","Cara menawarkan ke pelanggan","Tolong jelaskan semua menu 521 dan cara menawarkannya ke pelanggan."],["🌱","Arabika vs Robusta","Dua spesies utama dunia","Apa beda kopi arabika dan robusta?"],["🇮🇩","Kopi Indonesia","Yang mendunia","Apa saja kopi Indonesia yang terkenal di dunia?"],["🌍","Budaya kopi dunia","Italia, Turki, Ethiopia…","Bagaimana budaya minum kopi di berbagai negara?"],["💡","Wawasan hari ini","Belajar sedikit tiap hari","__tip"],["🔥","Tingkat roasting","Light, medium, dark","Apa beda light, medium, dan dark roast?"]];
const CAV='<i class="cav" aria-hidden="true"><svg><use href="#logo"/></svg></i>';
function chatWel(){return `<div class="cwel"><div class="ccup" aria-hidden="true"><span class="steam"><i></i><i></i><i></i></span><span class="mug">☕</span></div><b>Halo${me?", "+esc(me.name):""}!</b><span>Saya Asisten 521. Tanya seputar menu kita atau wawasan kopi dari seluruh dunia.</span>
  <div class="csug">${CHIPS.map((c,i)=>`<button data-a="c_chip" data-v="${i}" style="--i:${i}"><em>${c[0]}</em><b>${c[1]}</b><small>${c[2]}</small></button>`).join("")}</div></div>`}
function chatRender(){const o=$("#chat");if(!o)return;const L=o.querySelector(".cmsgs"),box=o.querySelector(".cbox");
  const near=L.scrollHeight-L.scrollTop-L.clientHeight<120;
  if(!chatH.length){if(!L.querySelector(".cwel"))L.innerHTML=chatWel()}
  else{const w=L.querySelector(".cwel");if(w)L.innerHTML="";
    let N=L.querySelectorAll(".cm");if(N.length>chatH.length){L.innerHTML="";N=[]}
    chatH.forEach((m,i)=>{let n=L.querySelectorAll(".cm")[i];const me2=m.role==="user";
      if(!n){n=document.createElement("div");n.className="cm "+(me2?"me":"ai");n.innerHTML=me2?'<div class="cbub"></div>':CAV+'<div class="cbub"></div>';L.appendChild(n)}
      const last=i===chatH.length-1,live=!me2&&last&&chatBusy;
      const h=me2?esc(m.content).replace(/\n/g,"<br>"):(m.content?chatFmt(m.content)+(live?'<span class="ccar"></span>':""):'<span class="ctyping"><i></i><i></i><i></i></span>');
      if(n._h!==h){n.querySelector(".cbub").innerHTML=h;n._h=h}n.classList.toggle("live",live)})}
  o.querySelector(".cchips").innerHTML=chatH.length?CHIPS.map((c,i)=>`<button data-a="c_chip" data-v="${i}"${chatBusy?" disabled":""}>${c[0]} ${c[1]}</button>`).join(""):"";
  o.querySelector(".cchips").hidden=!chatH.length;
  box.classList.toggle("busy",chatBusy);o.querySelector("[data-a=c_send]").hidden=chatBusy;o.querySelector("[data-a=c_stop]").hidden=!chatBusy;
  const ai=!!(SMP&&!smpOff);o.querySelector(".cmode").innerHTML=`<i class="${ai?"on":""}"></i>${chatBusy?"Sedang mengetik…":ai?"Online · didukung Claude":"Pengetahuan bawaan"}`;
  if(near||chatBusy)requestAnimationFrame(()=>L.scrollTo({top:L.scrollHeight,behavior:chatBusy?"auto":"smooth"}))}
function chatOpen(){let o=$("#chat");if(!o){o=document.createElement("div");o.id="chat";o.className="chat";
    o.innerHTML=`<div class="cbox" role="dialog" aria-modal="true" aria-label="Chat 521"><div class="cglow" aria-hidden="true"></div><div class="chd"><span class="cava"><svg aria-hidden="true"><use href="#logo"/></svg></span><span class="pv-who"><b>Chat 521</b><small class="cmode"></small></span><button class="chb" data-a="c_clear" aria-label="Mulai percakapan baru" title="Percakapan baru"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 12a8 8 0 1 0 2.4-5.7M4 4v4.5h4.5"/></svg></button><button class="chb" data-a="c_close" aria-label="Tutup chat">${ic("x")}</button></div>
    <div class="cmsgs" aria-live="polite"></div><div class="cchips scroll" hidden></div>
    <div class="cin"><div class="cfield"><textarea id="cq" rows="1" placeholder="Tanya soal menu atau kopi…" aria-label="Pesan untuk Chat 521"></textarea><button class="csend" data-a="c_send" aria-label="Kirim"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 19V5M5.5 11.5 12 5l6.5 6.5"/></svg></button><button class="csend stop" data-a="c_stop" aria-label="Hentikan" hidden><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="7" width="10" height="10" rx="2"/></svg></button></div></div></div>`;document.body.appendChild(o)}
  clearTimeout(o._t);o.classList.remove("closing");o.hidden=false;chatRender();setTimeout(()=>{const q=$("#cq");if(q&&matchMedia("(hover:hover)").matches)q.focus()},80)}
function chatClose(){const o=$("#chat");if(chatCtl)chatCtl.abort();if(!o||o.hidden)return;o.classList.add("closing");clearTimeout(o._t);o._t=setTimeout(()=>{o.hidden=true;o.classList.remove("closing")},230)}
