s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:70],s.count(a)); s=s.replace(a,b)
K=lambda k,lbl: (f'<div><span>{lbl}</span>', f'<button data-a="kpi" data-v="{k}"><span>{lbl}</span>')
old='''  <div class="kpi"><div class="main"><span>Omzet</span><b>${rp(s.rev)}</b>${rng==="today"?delta(s.rev,ys.rev):`<em class="mute">${s.n} pesanan</em>`}</div><div><span>Laba kotor</span><b>${rp(gp)}</b></div><div><span>Pengeluaran</span><b>${rp(ex)}</b></div><div><span>Laba bersih (perkiraan)</span><b class="${gp-ex<0?"down":""}">${rp(gp-ex)}</b></div><div><span>Pesanan</span><b>${s.n}</b></div><div><span>Cup terjual</span><b>${s.items}</b></div><div><span>Rata-rata / pesanan</span><b>${rp(s.n?s.rev/s.n:0)}</b></div></div>'''
new='''  <div class="kpi kpib"><button class="main" data-a="kpi" data-v="rev"><span>Omzet</span><b>${rp(s.rev)}</b>${rng==="today"?delta(s.rev,ys.rev):`<em class="mute">${s.n} pesanan</em>`}<i class="kmore">Rincian ›</i></button><button data-a="kpi" data-v="gp"><span>Laba kotor</span><b>${rp(gp)}</b><i class="kmore">Rincian ›</i></button><button data-a="kpi" data-v="ex"><span>Pengeluaran</span><b>${rp(ex)}</b><i class="kmore">Rincian ›</i></button><button data-a="kpi" data-v="net"><span>Laba bersih (perkiraan)</span><b class="${gp-ex<0?"down":""}">${rp(gp-ex)}</b><i class="kmore">Rincian ›</i></button><button data-a="kpi" data-v="n"><span>Pesanan</span><b>${s.n}</b><i class="kmore">Rincian ›</i></button><button data-a="kpi" data-v="cup"><span>Cup terjual</span><b>${s.items}</b><i class="kmore">Rincian ›</i></button><button data-a="kpi" data-v="avg"><span>Rata-rata / pesanan</span><b>${rp(s.n?s.rev/s.n:0)}</b><i class="kmore">Rincian ›</i></button></div>
  <p class="note" style="margin-top:-4px">Ketuk kotak mana saja untuk melihat rincian dan cara hitungnya.</p>'''
rep(old,new)
# staff view too
rep('''<h2>Hari ini</h2><div class="kpi"><div class="main"><span>Omzet</span><b>${rp(s.rev)}</b>${delta(s.rev,ys.rev)}</div><div><span>Pesanan</span><b>${s.n}</b></div><div><span>Cup terjual</span><b>${s.items}</b></div></div>''',
'''<h2>Hari ini</h2><div class="kpi kpib"><button class="main" data-a="kpi" data-v="rev"><span>Omzet</span><b>${rp(s.rev)}</b>${delta(s.rev,ys.rev)}<i class="kmore">Rincian ›</i></button><button data-a="kpi" data-v="n"><span>Pesanan</span><b>${s.n}</b><i class="kmore">Rincian ›</i></button><button data-a="kpi" data-v="cup"><span>Cup terjual</span><b>${s.items}</b><i class="kmore">Rincian ›</i></button></div>''')
js=r'''
/* Rincian KPI: arti angka, rumus, dan pecahannya untuk periode yang dipilih */
function kpiSheet(k){
  const r=own()?range():[ymd(new Date()),ymd(new Date())],T=okTx(r),s=agg(T),X=D.tx.filter(t=>t.status==="cancelled"&&t.d>=r[0]&&t.d<=r[1]);
  const E=D.exp.filter(e=>e.d>=r[0]&&e.d<=r[1]),ex=E.reduce((a,e)=>a+e.amt,0),gp=s.rev-s.hpp,net=gp-ex;
  const per=r[0]===r[1]?kFmt(r[0]):kFmt(r[0])+" – "+kFmt(r[1]);
  const row=(a,b,c="")=>`<div class="kr${c?" "+c:""}"><span>${a}</span><b>${b}</b></div>`;
  const pct=(a,b)=>b?Math.round(a/b*100)+"%":"–";
  const sec=(t,h)=>`<h3>${t}</h3>${h}`;
  const pq={},pp={},prv={};Object.entries(s.prod).forEach(([n,o])=>{pq[n]=o.q;pp[n]=o.pf});T.forEach(t=>t.items.forEach(i=>{prv[i.n]=(prv[i.n]||0)+i.pr*i.q}));
  const disc=T.reduce((a,t)=>a+(t.disc||0),0),gross=T.reduce((a,t)=>a+(t.sub||t.total),0);
  const hours={};T.forEach(t=>{const h=new Date(t.at).getHours();const l=String(h).padStart(2,"0")+".00";hours[l]=(hours[l]||0)+1});
  const days={};T.forEach(t=>{days[t.d]=(days[t.d]||0)+t.total});
  const H={
    rev:["Omzet",rp(s.rev),"Total uang yang masuk dari pesanan yang lunas, setelah diskon dan voucher. Pesanan yang dibatalkan tidak dihitung.",
      row("Harga menu (sebelum potongan)",rp(gross))+row("Diskon & voucher","− "+rp(disc))+row("Omzet",rp(s.rev),"tot")+
      sec("Cara bayar",bars(desc(s.pm)))+sec("Asal pesanan",bars(desc(s.ch)))+(Object.keys(days).length>1?sec("Per hari",bars(Object.entries(days).sort(),rp)):"")+sec("Per menu",bars(desc(prv)))],
    gp:["Laba kotor",rp(gp),"Omzet dikurangi modal bahan (HPP) dari resep setiap menu. Ini untung sebelum biaya lain seperti gaji, sewa, dan listrik.",
      row("Omzet",rp(s.rev))+row("Modal bahan (HPP)","− "+rp(s.hpp))+row("Laba kotor",rp(gp),"tot")+row("Margin kotor",pct(gp,s.rev))+
      sec("Laba per menu",bars(desc(pp)))+`<p class="note">HPP diambil dari Buku Resep × harga bahan di Stok saat transaksi terjadi. Kalau resep atau harga bahan belum diisi, HPP dianggap 0 dan laba terlihat lebih besar.</p>`],
    ex:["Pengeluaran",rp(ex),"Semua biaya yang Anda catat di periode ini lewat “Catat pengeluaran”.",
      sec("Per kategori",bars(desc(E.reduce((o,e)=>{o[e.cat]=(o[e.cat]||0)+e.amt;return o},{}))))+
      sec(`Daftar (${E.length})`,E.length?`<div class="list">${E.slice().reverse().map(e=>`<div class="txr"><span><b>${esc(e.cat)}</b><small>${kFmt(e.d)}${e.note?" · "+esc(e.note):""}${e.by?" · "+esc(e.by):""}</small></span><span class="num">${rp(e.amt)}</span></div>`).join("")}</div>`:'<p class="mute" style="font-size:14px">Belum ada pengeluaran di periode ini.</p>')],
    net:["Laba bersih (perkiraan)",rp(net),"Perkiraan untung bersih: laba kotor dikurangi pengeluaran yang dicatat. Disebut perkiraan karena hanya menghitung biaya yang sudah Anda catat.",
      row("Omzet",rp(s.rev))+row("Modal bahan (HPP)","− "+rp(s.hpp))+row("Pengeluaran","− "+rp(ex))+row("Laba bersih",rp(net),"tot"+(net<0?" neg":""))+row("Margin bersih",pct(net,s.rev))+
      `<p class="note">${net<0?"Periode ini masih minus. Cek pengeluaran besar di rincian Pengeluaran, atau naikkan penjualan menu dengan laba tertinggi.":"Tips: catat semua pengeluaran harian supaya angka ini makin akurat."}</p>`],
    n:["Pesanan",String(s.n),"Jumlah transaksi yang lunas. Satu pesanan bisa berisi beberapa cup.",
      row("Pesanan lunas",s.n)+row("Dibatalkan",X.length)+row("Rata-rata cup / pesanan",s.n?(s.items/s.n).toFixed(1).replace(".",","):"–")+
      sec("Jam paling ramai",bars(Object.entries(hours).sort(),v=>v+" pesanan"))+sec("Per kasir",bars(desc(T.reduce((o,t)=>{const b=t.by||"-";o[b]=(o[b]||0)+1;return o},{})),v=>v+" pesanan"))],
    cup:["Cup terjual",String(s.items),"Total cup/porsi dari semua pesanan yang lunas.",
      sec("Per menu",bars(desc(pq),v=>v+" cup"))+(own()?"":"")],
    avg:["Rata-rata / pesanan",rp(s.n?s.rev/s.n:0),"Omzet dibagi jumlah pesanan. Naikkan angka ini dengan menawarkan tambahan atau paket.",
      row("Omzet",rp(s.rev))+row("Jumlah pesanan","÷ "+s.n)+row("Rata-rata",rp(s.n?s.rev/s.n:0),"tot")+
      (T.length?row("Pesanan terbesar",rp(Math.max(...T.map(t=>t.total))))+row("Pesanan terkecil",rp(Math.min(...T.map(t=>t.total)))):"")]
  }[k];if(!H)return;
  show(`<p class="eyebrow" style="margin:0 0 4px">${per}</p><h2>${H[0]}</h2><div class="kbig">${H[1]}</div><p class="note">${H[2]}</p><div class="kdet">${H[3]}</div>`);
}
'''
i=s.index("function dash(){");s=s[:i]+js.lstrip("\n")+s[i:]
rep('''  else if(a==="sold"){''','''  else if(a==="kpi")kpiSheet(v);
  else if(a==="sold"){''')
css='''/* ---------- KPI bisa diketuk ---------- */
.kpib > button{display:block;width:100%;text-align:left;font:inherit;color:inherit;background:var(--sf);border:1px solid var(--line);border-radius:var(--r);padding:16px;min-width:0;cursor:pointer;transition:border-color .15s,transform .12s}
.kpib > button.main{background:radial-gradient(120% 120% at 100% 0,color-mix(in srgb,var(--ac) 28%,transparent),transparent 60%),var(--sf);border-color:color-mix(in srgb,var(--ac) 35%,var(--line))}
.kpib > button:hover{border-color:color-mix(in srgb,var(--ac) 55%,var(--line))}
.kpib > button:active{transform:scale(.98)}
.kpib span{display:block;font-size:11px;font-weight:700;color:var(--mute);text-transform:uppercase;letter-spacing:.1em}
.kpib b{display:block;font:600 21px var(--f-m);letter-spacing:-.03em;margin-top:6px;overflow:hidden;text-overflow:ellipsis}
.kpib .main b{font-size:clamp(30px,6vw,44px)}
.kpib em{font-style:normal;font-size:13px;font-weight:700;display:block}
.kmore{display:block;font-style:normal;font-size:12px;font-weight:700;color:var(--ac);margin-top:6px;opacity:.85}
:root[data-glass] .kpib > button{-webkit-backdrop-filter:blur(18px) saturate(1.5);backdrop-filter:blur(18px) saturate(1.5)}
.kbig{font:600 36px var(--f-m);letter-spacing:-.04em;margin:-6px 0 4px}
.kdet .kr{display:flex;justify-content:space-between;gap:12px;padding:9px 0;border-bottom:1px dashed var(--line);font-size:15px}
.kdet .kr span{color:var(--mute)}.kdet .kr b{font:600 15px var(--f-m)}
.kdet .kr.tot{border-bottom:0;border-top:1.5px solid var(--ink);margin-top:2px}.kdet .kr.tot span{color:var(--ink);font-weight:700}.kdet .kr.tot b{font-size:18px}
.kdet .kr.neg b{color:var(--warn)}
'''
i=s.index("/* ---------- Welcome ---------- */");s=s[:i]+css+s[i:]
open('p3.src.html','w').write(s);print("ok")
