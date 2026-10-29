s=open('p3.src.html').read()
def rep(a,b,n=1):
    global s
    assert s.count(a)==n,(s.count(a),a[:90])
    s=s.replace(a,b)
rep('''  --bg:#0b0806;--sf:#15100c;--sf2:#1d1611;--sf3:#2a2018;--ink:#faf3e8;--mute:#a6927c;--dim:#6f604f;--line:#2c2219;
  --ac:#f2a91c;--ac2:#e2560f;--on:#160c03;--warn:#ff8a5c;--ok:#9be0a9;''','''  /* Warna dasar brand 521: lime #D8FF00 + merah bata #C03200 → #862401 */
  --lime:#D8FF00;--red:#C03200;--red2:#862401;
  --bg:#120504;--sf:#1d0a06;--sf2:#270f09;--sf3:#37170d;--ink:#fff4ec;--mute:#c49a87;--dim:#8a5d4b;--line:#3a1a10;
  --ac:#D8FF00;--ac2:#B8E600;--on:#1a0700;--warn:#ff8a5c;--ok:#9be0a9;''')
rep('''  color-scheme:dark;--heroimg:url(__HERO__);''','''  color-scheme:dark;''')
rep('''radial-gradient(60% 50% at 92% -8%,color-mix(in srgb,var(--ac) 22%,transparent),transparent 70%)''','''radial-gradient(60% 50% at 92% -8%,color-mix(in srgb,var(--red) 45%,transparent),transparent 70%)''')
rep('''.hero{background:#1a0d04 var(--heroimg) center/cover no-repeat;''','''.brandart{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:4px;color:var(--lime)}
.brandart svg{width:44%;max-width:300px;height:auto;aspect-ratio:1565/1015}
.brandart span{font:700 clamp(15px,3.2vw,26px) var(--f-d);letter-spacing:.01em}
.hero{background:linear-gradient(180deg,var(--red2),var(--red));''')
rep('''background:#1a0d04 var(--heroimg) center 40%/cover;''','''background:linear-gradient(180deg,var(--red2),var(--red));''')
rep('''<div class="hero" role="img" aria-label="Logo 521 Coffee Cart"></div>''','''<div class="hero" role="img" aria-label="Logo 521 Coffee Cart"><div class="brandart"><svg aria-hidden="true"><use href="#logo"/></svg><span>Coffee Cart</span></div></div>''')
rep('''aria-label="${esc(s.name||"521 Coffee")}">${H.map(''','''aria-label="${esc(s.name||"521 Coffee")}">${H.length?"":'<div class="brandart"><svg aria-hidden="true"><use href="#logo"/></svg><span>Coffee Cart</span></div>'}${H.map(''')
rep('''const SW={ember:''','''const SW={lime:["#D8FF00","#B8E600"],ember:''')
rep('''color:"ember",big:0,''','''color:"lime",big:0,''')
rep('''if(!SW[d.cfg.color])d.cfg.color="ember";''','''if(!SW[d.cfg.color]||!d.cfg.brand2){d.cfg.color="lime";d.cfg.brand2=1}''')
rep('''const c=C(),r=document.documentElement,s=SW[c.color]||SW.ember;''','''const c=C(),r=document.documentElement,s=SW[c.color]||SW.lime;''')
open('p3.src.html','w').write(s);print('ok')
