s=open('p2.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:70]
    s=s.replace(a,b)
rep('promo:"https://claude.ai/artifact/2wqVXCUtJHCucmRZF7UWYX"};','promo:"https://claude.ai/artifact/2wqVXCUtJHCucmRZF7UWYX"};\nconst PROMO_DEF="https://claude.ai/artifact/2wqVXCUtJHCucmRZF7UWYX",PROMO_QR="__PQR__";')
rep('''    try{new QRCode($("#qrw"),{text:L,width:480,height:480,colorDark:"#160c03",colorLight:"#ffffff",correctLevel:QRCode.CorrectLevel.M})}catch(err){$("#qrw").hidden=true}}''','''    if(L===PROMO_DEF)$("#qrw").innerHTML=`<img src="${PROMO_QR}" alt="QR halaman promo" style="image-rendering:pixelated">`;
    else{try{new QRCode($("#qrw"),{text:L,width:480,height:480,colorDark:"#160c03",colorLight:"#ffffff",correctLevel:QRCode.CorrectLevel.M})}catch(err){$("#qrw").hidden=true}}}''')
open('p2.src.html','w').write(s)
import base64,re
s=s.replace('__LOGO__',open('logo.sym').read().strip()).replace('__PQR__','data:image/png;base64,'+base64.b64encode(open('promoqr.png','rb').read()).decode())
s=s.replace('__HERO__','data:image/jpeg;base64,'+base64.b64encode(open('hero.jpg','rb').read()).decode()).replace('__QRIS__','data:image/jpeg;base64,'+base64.b64encode(open('qris.jpg','rb').read()).decode())
open('premium.html','w').write(s)
open('t8.js','w').write(re.search(r'<script>\n(.*)</script>',s,re.S).group(1))
print('ok')
