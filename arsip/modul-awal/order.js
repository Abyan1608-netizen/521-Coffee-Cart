/* ---------- Pesan sekarang ---------- */
const waNum=n=>String(n||"").replace(/\D/g,"").replace(/^0/,"62");
function kOrd(){const s=K.store,o=s.order=s.order||{};if(!Array.isArray(o.resellers))o.resellers=[];if(!Array.isArray(o.shops)||!o.shops.length)o.shops=[{label:"Shopee",url:""},{label:"Tokopedia",url:""},{label:"GoFood",url:""}];return o}
let ordV="";
function orderSheet(){
  const o=kOrd(),wa=waNum(K.store.wa),R=o.resellers.filter(r=>r.n||r.wa),S=o.shops.filter(x=>/^https?:\/\//.test(x.url||"")),msg=encodeURIComponent("Halo 521 Coffee, saya mau pesan:\n");
  const opt=(v,icn,t,d,dis)=>`<button class="ordopt${dis?" dis":""}" data-a="ordv" data-v="${v}" aria-expanded="${ordV===v}">${ic(icn)}<span><b>${t}</b><small>${d}</small></span>${ic("arrow")}</button>`;
  let body="";
  if(ordV==="res")body=R.length?R.map(r=>{const w=waNum(r.wa);return `<div class="ordcard"><b>${esc(r.n||"Reseller")}</b>${r.loc?`<small>${ic("pin")}${esc(r.loc)}</small>`:""}<div class="ordbtns">${w?`<a class="btn sm" href="https://wa.me/${w}?text=${encodeURIComponent("Halo "+(r.n||"")+", saya mau pesan 521 Coffee:\n")}" target="_blank" rel="noopener">${ic("wa")} Chat WA</a>`:""}${/^https:\/\//.test(r.maps||"")?`<a class="btn ghost sm" href="${esc(r.maps)}" target="_blank" rel="noopener">${ic("pin")} Lihat lokasi</a>`:""}</div>${w?`<small class="mute num">+${w}</small>`:""}</div>`}).join(""):`<p class="note">Daftar reseller segera hadir.</p>`;
  if(ordV==="wa")body=wa?`<div class="ordcard"><b>WhatsApp 521 Coffee</b><small class="num">+${wa}</small><div class="ordbtns"><a class="btn sm" href="https://wa.me/${wa}?text=${msg}" target="_blank" rel="noopener">${ic("wa")} Chat sekarang</a></div><small class="mute">Tulis menu, jumlah, dan alamat atau jam ambil. Kami balas secepatnya.</small></div>`:`<p class="note">Nomor WhatsApp belum diatur.</p>`;
  if(ordV==="shop")body=S.length?`<div class="ordshops">${S.map(x=>`<a class="ordshop" href="${esc(x.url)}" target="_blank" rel="noopener"><b>${esc(x.label||"Toko online")}</b>${ic("arrow")}</a>`).join("")}</div>`:`<p class="note">Toko online segera hadir.</p>`;
  show(`<h2>Pesan sekarang</h2><p class="mute" style="margin-top:-6px">Pilih cara pesan yang paling mudah buat kamu.</p>
  <div class="ordlist">${opt("res","pin","Hubungi reseller",R.length?`${R.length} reseller terdekat`:"Segera hadir",!R.length)}${ordV==="res"?`<div class="ordbody">${body}</div>`:""}
  ${opt("wa","wa","Hubungi WA kami",wa?"Pesan langsung ke 521 Coffee":"Belum tersedia",!wa)}${ordV==="wa"?`<div class="ordbody">${body}</div>`:""}
  ${opt("shop","pos","E-commerce",S.length?S.map(x=>esc(x.label)).join(" · "):"Segera hadir",!S.length)}${ordV==="shop"?`<div class="ordbody">${body}</div>`:""}</div>`);
}
function kOrderSheet(){
  const o=kOrd();
  show(`<h2>Pesan sekarang</h2><p class="note" style="margin-top:-4px">Atur pilihan pesan di halaman pelanggan. Terlihat setelah Terbitkan.</p>
  <h3>WhatsApp kami</h3><input id="o-wa" inputmode="tel" value="${esc(K.store.wa||"")}" placeholder="08xxxxxxxxxx" aria-label="Nomor WhatsApp toko">
  <h3>Reseller</h3>${o.resellers.map((r,i)=>`<div class="ordedit"><div class="two"><input data-or="${i}" data-of="n" value="${esc(r.n||"")}" placeholder="Nama reseller" aria-label="Nama reseller"><input data-or="${i}" data-of="wa" inputmode="tel" value="${esc(r.wa||"")}" placeholder="No. WA" aria-label="WA reseller"></div><input data-or="${i}" data-of="loc" value="${esc(r.loc||"")}" placeholder="Lokasi, misalnya Ciledug Indah" aria-label="Lokasi reseller"><div class="add"><input data-or="${i}" data-of="maps" value="${esc(r.maps||"")}" placeholder="Link Google Maps (opsional)" aria-label="Link maps reseller"><button class="btn ghost sm" data-a="ordrdel" data-v="${i}" style="color:var(--warn)">Hapus</button></div></div>`).join("")||'<p class="note">Belum ada reseller.</p>'}
  <button class="link" data-a="ordradd">+ Tambah reseller</button>
  <h3>E-commerce</h3>${o.shops.map((x,i)=>`<div class="rr3" style="grid-template-columns:minmax(0,.8fr) minmax(0,1.4fr) auto"><input data-os="${i}" data-of="label" value="${esc(x.label||"")}" placeholder="Nama" aria-label="Nama toko online"><input data-os="${i}" data-of="url" inputmode="url" value="${esc(x.url||"")}" placeholder="https://..." aria-label="Link toko online"><button class="btn ghost sm" data-a="ordsdel" data-v="${i}" style="color:var(--warn)">✕</button></div>`).join("")}
  <button class="link" data-a="ordsadd">+ Tambah link</button><p class="note">Link yang kosong tidak ditampilkan ke pelanggan.</p>
  <button class="btn" data-a="ordsave">Simpan</button>`);
}
function ordGrab(){const o=kOrd();const w=$("#o-wa");if(w)K.store.wa=w.value.trim();
  document.querySelectorAll("[data-or]").forEach(el=>{const r=o.resellers[+el.dataset.or];if(r)r[el.dataset.of]=el.value.trim()});
  document.querySelectorAll("[data-os]").forEach(el=>{const x=o.shops[+el.dataset.os];if(x)x[el.dataset.of]=el.value.trim()})}
