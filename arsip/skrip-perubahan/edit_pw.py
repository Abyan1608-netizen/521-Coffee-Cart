s=open('p2.src.html').read()
def rep(a,b):
    global s
    assert s.count(a)==1,a[:70]
    s=s.replace(a,b)
rep('.dots{display:flex;','.pw{position:relative;margin:22px 0 0}\n.pw input{margin:0;padding:15px 52px 15px 16px;font:600 20px var(--f-m);letter-spacing:.12em;text-align:center;background:var(--sf);border-radius:16px}\n.pw input::placeholder{font:500 15px var(--f-b);letter-spacing:0;color:var(--dim)}\n.pw input.err{border-color:var(--warn);animation:shake .32s}\n.pw button{position:absolute;right:8px;top:50%;transform:translateY(-50%);width:38px;height:38px;border:0;border-radius:11px;background:var(--sf2);color:var(--mute);display:grid;place-items:center}\n.dots{display:flex;')
rep('<p class="sub">Pilih akun, lalu masukkan PIN.</p>','<p class="sub">Pilih akun, lalu masukkan PIN atau kata sandi.</p>')
rep('<div class="dots" id="dots" aria-live="polite"></div>','<div class="pw"><input id="lpw" type="password" autocomplete="current-password" autocapitalize="off" spellcheck="false" placeholder="PIN atau kata sandi" aria-label="PIN atau kata sandi"><button type="button" data-a="peek" id="peek" aria-label="Tampilkan kata sandi"></button></div>')
rep("  x:'<path d=\"M6 6l12 12M18 6 6 18\"/>'","  x:'<path d=\"M6 6l12 12M18 6 6 18\"/>',\n  eye:'<path d=\"M2.5 12S6 5.5 12 5.5 21.5 12 21.5 12 18 18.5 12 18.5 2.5 12 2.5 12z\"/><circle cx=\"12\" cy=\"12\" r=\"3\"/>',\n  eyeoff:'<path d=\"M3 3l18 18M10.6 6a9.6 9.6 0 0 1 1.4-.1c6 0 9.5 6.1 9.5 6.1a17 17 0 0 1-2.6 3.3M6.6 6.7C4 8.4 2.5 12 2.5 12S6 18.5 12 18.5c1.6 0 3-.4 4.3-1M9.9 9.9a3 3 0 0 0 4.2 4.2\"/>'")
rep('''function dots(err){const u=D.users.find(x=>x.id===lsel),L=Math.max(4,u?u.pin.length:4);$("#dots").className="dots"+(err?" err":"");$("#dots").innerHTML=[...Array(L)].map((_,i)=>`<i class="${i<buf.length?"on":""}"></i>`).join("")}
function tryLogin(force){
  const u=D.users.find(x=>x.id===lsel);if(!u)return;
  if(buf===u.pin){me=u;buf="";$("#lerr").textContent="";try{sessionStorage.setItem("pos521u",u.id)}catch(e){}enter();return}
  if(force||buf.length>=u.pin.length){$("#lerr").textContent="PIN belum cocok. Coba lagi.";buf="";dots(true)}else dots();
}''','''let peek=false;
function dots(err){const i=$("#lpw");i.value=buf;i.type=peek?"text":"password";i.classList.remove("err");if(err){void i.offsetWidth;i.classList.add("err")}$("#peek").innerHTML=ic(peek?"eyeoff":"eye");$("#peek").setAttribute("aria-label",peek?"Sembunyikan kata sandi":"Tampilkan kata sandi")}
function tryLogin(force){
  const u=D.users.find(x=>x.id===lsel);if(!u)return;
  if(buf===u.pin){me=u;buf="";peek=false;$("#lerr").textContent="";try{sessionStorage.setItem("pos521u",u.id)}catch(e){}enter();return}
  if(force){$("#lerr").textContent=buf?"PIN atau kata sandi belum cocok. Coba lagi.":"Masukkan PIN atau kata sandi dulu.";buf="";dots(true)}else dots();
}''')
rep('Ganti setelah masuk, di Atur → Tim & PIN.','Ganti setelah masuk, di Atur → Tim & PIN. Boleh angka, huruf, atau campuran.')
rep('''  if(a==="kp"){if(buf.length<6){buf+=v;$("#lerr").textContent="";tryLogin()}return}''','''  if(a==="kp"){if(buf.length<32){buf+=v;$("#lerr").textContent="";tryLogin()}return}
  if(a==="peek"){peek=!peek;dots();return}''')
rep('''  if(!me&&!$("#login").hidden){
    if(/^\\d$/.test(e.key)&&buf.length<6){buf+=e.key;$("#lerr").textContent="";tryLogin()}''','''  if(!me&&!$("#login").hidden){
    if(e.target.id==="lpw"){if(e.key==="Enter"){e.preventDefault();tryLogin(true)}return}
    if(/^\\d$/.test(e.key)&&buf.length<32){buf+=e.key;$("#lerr").textContent="";tryLogin()}''')
rep('''  if(t.id==="q"){q=t.value;$("#g").innerHTML=grid()}''','''  if(t.id==="lpw"){buf=t.value.slice(0,32);$("#lerr").textContent="";t.classList.remove("err");const u=D.users.find(x=>x.id===lsel);if(u&&buf===u.pin)tryLogin()}
  else if(t.id==="q"){q=t.value;$("#g").innerHTML=grid()}''')
rep('''<label>${u.isNew?"PIN (4–6 angka)":"PIN baru (kosongkan bila tidak diganti)"}<input id="u-pin" type="password" inputmode="numeric" autocomplete="new-password" maxlength="6"></label>''','''<label>${u.isNew?"PIN atau kata sandi":"PIN atau kata sandi baru (kosongkan bila tidak diganti)"}<input id="u-pin" type="password" autocomplete="new-password" autocapitalize="off" spellcheck="false" maxlength="32"></label><p class="note">Minimal 4 karakter. Boleh angka saja (cepat lewat keypad), huruf, atau campuran seperti <b>kopi521</b>. Huruf besar dan kecil dibedakan.</p>''')
rep('''if((eu.isNew||p)&&!/^\\d{4,6}$/.test(p)){toast("PIN harus 4–6 angka");$("#u-pin").focus();return}''','''if((eu.isNew||p)&&(p.length<4||p.length>32)){toast("Minimal 4 karakter, maksimal 32");$("#u-pin").focus();return}''')
rep('''p=$("#u-pin").value.trim();''','''p=$("#u-pin").value;''')
open('p2.src.html','w').write(s)
import base64,re
s=s.replace('__LOGO__',open('logo.sym').read().strip())
s=s.replace('__HERO__','data:image/jpeg;base64,'+base64.b64encode(open('hero.jpg','rb').read()).decode()).replace('__QRIS__','data:image/jpeg;base64,'+base64.b64encode(open('qris.jpg','rb').read()).decode())
open('premium.html','w').write(s)
open('t5.js','w').write(re.search(r'<script>(.*)</script>',s,re.S).group(1))
print("ok")
