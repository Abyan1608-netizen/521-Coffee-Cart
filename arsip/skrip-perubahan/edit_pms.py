s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(a[:80],s.count(a)); s=s.replace(a,b)
rep("const roleName=u=>","""const pmsOf=u=>{const all=C().pm;if(!u||u.role==="owner"||!Array.isArray(u.pms))return all;const a=all.filter(m=>u.pms.includes(m));return a.length?a:all};
const myPm=()=>pmsOf(me);
const roleName=u=>""")
rep('''return p.length?all.filter(x=>p.includes(x[0])).map(x=>x[1]).slice(0,3).join(", ")+(p.length>3?` +${p.length-3} lagi`:""):"Belum ada akses"};''',
'''const r=Array.isArray(u.pms)&&pmsOf(u).length<C().pm.length?` · bayar: ${pmsOf(u).join("/")}`:"";return p.length?all.filter(x=>p.includes(x[0])).map(x=>x[1]).slice(0,3).join(", ")+(p.length>3?` +${p.length-3} lagi`:"")+r:"Belum ada akses"};''')
rep("function cartBody(){","function cartBody(){\n  if(!myPm().includes(pm))pm=myPm()[0];")
rep('''<div class="pays">${c.pm.map(m=>''','''<div class="pays">${myPm().map(m=>''')
rep('cart={};disc=0;paid=0;showDisc=false;vch="";verr="";pm=C().pm[0];inCart=false;headStat();','cart={};disc=0;paid=0;showDisc=false;vch="";verr="";pm=myPm()[0];inCart=false;headStat();')
rep('  else if(a==="pm"){pm=v;cartUI()}','  else if(a==="pm"){if(!myPm().includes(v))return;pm=v;cartUI()}')
rep("function pay(){","function pay(){\n  if(!myPm().includes(pm)){pm=myPm()[0];cartUI();toast(\"Cara bayar ini tidak diizinkan untuk akun Anda\");return}")
# user sheet: insert after Kasir group toggles
rep('''<div class="permbox">${PERMS.map(g=>`<div class="permg"><h3>${ic(g[1])}${g[0]}</h3>${g[2].map(x=>`<div class="swrow"><span><b>${x[1]}</b><small>${x[2]}</small></span><label class="tgl" aria-label="${x[1]}"><input type="checkbox" data-pk="${x[0]}" ${permOf(u).includes(x[0])?"checked":""}><span></span></label></div>`).join("")}</div>`).join("")}''',
'''<div class="permbox">${PERMS.map(g=>`<div class="permg"><h3>${ic(g[1])}${g[0]}</h3>${g[2].map(x=>`<div class="swrow"><span><b>${x[1]}</b><small>${x[2]}</small></span><label class="tgl" aria-label="${x[1]}"><input type="checkbox" data-pk="${x[0]}" ${permOf(u).includes(x[0])?"checked":""}><span></span></label></div>`).join("")}${g[1]==="pos"&&permOf(u).includes("pos")?`<div class="pmpick"><b>Cara bayar yang boleh diterima</b><small>Misalnya hanya Cash, atau hanya QRIS. Cara bayar lain tidak muncul di kasir akun ini.</small><div class="chips">${C().pm.map(m=>`<label class="pmchip"><input type="checkbox" data-upm="${esc(m)}" ${pmsOf(u).includes(m)?"checked":""}><span>${ic(pmIcon(m))}${esc(m)}</span></label>`).join("")}</div></div>`:""}</div>`).join("")}''')
rep('''if(!eu.perm)eu.perm=[...PRESETS.barista[1]]}''','''if(!eu.perm)eu.perm=[...PRESETS.barista[1]];const pb=document.querySelectorAll("[data-upm]");if(pb.length){const sel=[...pb].filter(x=>x.checked).map(x=>x.dataset.upm);eu.pms=sel.length===C().pm.length?undefined:sel}}''')
rep('''    if(eu.role!=="owner"&&!["pos",''','''    if(eu.role!=="owner"&&eu.perm.includes("pos")&&Array.isArray(eu.pms)&&!eu.pms.length){toast("Pilih minimal satu cara bayar untuk akun ini");return}
    if(eu.role!=="owner"&&!["pos",''')
rep('''    const ext=eu.role==="owner"?{}:{perm:[...eu.perm],title:eu.title||""};''','''    const ext=eu.role==="owner"?{}:{perm:[...eu.perm],title:eu.title||"",pms:Array.isArray(eu.pms)?[...eu.pms]:undefined};''')
rep('''u.name=nm;u.role=eu.role;if(u.role==="owner"){delete u.perm;delete u.title}else{const was=JSON.stringify(permOf(u));Object.assign(u,ext);if(was!==JSON.stringify(u.perm))''','''u.name=nm;u.role=eu.role;if(u.role==="owner"){delete u.perm;delete u.title;delete u.pms}else{const was=JSON.stringify(permOf(u))+JSON.stringify(u.pms||null);Object.assign(u,ext);if(!ext.pms)delete u.pms;if(was!==JSON.stringify(u.perm)+JSON.stringify(u.pms||null))''')
rep('''if(u.role!=="owner")eu.perm=[...permOf(u)],eu.title=u.title||"Barista";''','''if(u.role!=="owner")eu.perm=[...permOf(u)],eu.title=u.title||"Barista",eu.pms=Array.isArray(u.pms)?[...u.pms]:undefined;''')
# change on pm chip: keep sheet state (no rerender needed) but prevent unchecking all
rep('''document.addEventListener("change",e=>{''','''document.addEventListener("change",e=>{
  if(e.target.dataset&&e.target.dataset.upm!==undefined){const pb=[...document.querySelectorAll("[data-upm]")];if(!pb.some(x=>x.checked)){e.target.checked=true;toast("Minimal satu cara bayar harus aktif")}return}''')
css='''.pmpick{padding:12px 0 14px;border-top:1px solid var(--line)}
.pmpick b{display:block}.pmpick small{color:var(--mute);font-size:12px}
.pmchip{position:relative;margin:0}
.pmchip input{position:absolute;opacity:0;inset:0;margin:0;cursor:pointer}
.pmchip span{display:inline-flex;align-items:center;gap:6px;border:1px solid var(--line);background:var(--sf);border-radius:999px;padding:8px 14px;font-size:14px;font-weight:700;color:var(--mute);pointer-events:none}
.pmchip span svg{width:16px;height:16px}
.pmchip input:checked + span{background:var(--ac);color:var(--on);border-color:var(--ac)}
.pmchip input:focus-visible + span{outline:2px solid var(--ac);outline-offset:2px}
'''
i=s.index("/* ---------- Welcome ---------- */");s=s[:i]+css+s[i:]
open('p3.src.html','w').write(s);print("ok")
