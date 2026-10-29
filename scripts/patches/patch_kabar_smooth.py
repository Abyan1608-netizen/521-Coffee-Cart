"""Perbaikan kelancaran halaman Kabar (scroll patah-patah) tanpa mengubah desain.
Penyebab utama (diukur, CPU HP lambat 4x): ±430 kotak piksel animasi tak berujung di tombol
"Pesan sekarang" & tombol chat (masing-masing jadi layer GPU sendiri), plus pergantian kelas
global saat scroll yang memaksa hitung ulang gaya seluruh halaman. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*SMOOTH-PATCH-v1*/" in s:
    print("Sudah dipatch."); sys.exit(0)

def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:200]}")
    s = s.replace(old, new)

# 1) Efek piksel tukar-wajah tombol: 1 canvas per tombol (bukan 130–190 elemen beranimasi)
rep('function pxSwap(pc,pr,sw,cls=""){let px="";',
    r'''/*SMOOTH-PATCH-v1*/
/* Efek piksel digambar di satu <canvas> per tombol dengan waktu & warna yang sama seperti versi CSS,
   dan hanya bekerja saat tombol terlihat & piksel sedang muncul. Jauh lebih ringan untuk HP. */
const PXK=[[0,0,.35],[.389,0,.35],[.40,1,1],[.412,1,1],[.432,0,.35],[.851,0,.35],[.863,1,1],[.875,1,1],[.895,0,.35],[1,0,.35]];
const PXT={};let pxTimer=0,pxRaf=0;
const pxIO=window.IntersectionObserver?new IntersectionObserver(es=>es.forEach(e=>{e.target._vis=e.isIntersecting;if(e.isIntersecting)pxKick()})):null;
function pxAt(ph){for(let i=1;i<PXK.length;i++){const a=PXK[i-1],b=PXK[i];if(ph<=b[0]){const t=(ph-a[0])/((b[0]-a[0])||1);return [a[1]+(b[1]-a[1])*t,a[2]+(b[2]-a[2])*t]}}return [0,.35]}
const pxSec=v=>{v=String(v||"").trim();return v.endsWith("ms")?parseFloat(v)/1000:parseFloat(v)||0};
function pxInit(cv){const T=PXT[cv.dataset.px];if(!T)return null;const cs=getComputedStyle(cv);
  cv._px={T,t0:performance.now(),cy:pxSec(cs.getPropertyValue("--cy"))||8,o:pxSec(cs.getPropertyValue("--o")),drawn:false,col:null};
  if(pxIO)pxIO.observe(cv);else cv._vis=true;return cv._px}
function pxFrame(){pxRaf=0;const now=performance.now();let active=false,next=1e9;
  document.querySelectorAll("canvas.pxcv").forEach(cv=>{const S=cv._px||pxInit(cv);if(!S)return;
    const sec=(now-S.t0)/1000,T=S.T,n=T.k.length;let any=false;
    if(cv._vis!==false){const W=Math.round(cv.clientWidth*(devicePixelRatio||1)),H=Math.round(cv.clientHeight*(devicePixelRatio||1));
      const tiles=[];for(let i=0;i<n;i++){const st=sec-(S.o+T.s[i]);if(st<0)continue;const ph=(st/S.cy)%1;const [op,sc]=pxAt(ph);if(op>0.001)tiles.push([i,op,sc])}
      any=tiles.length>0;
      if(any||S.drawn){if(cv.width!==W||cv.height!==H){cv.width=W;cv.height=H}const x=cv.getContext("2d");x.clearRect(0,0,W,H);
        if(any){if(!S.col||!S.drawn){const cs=getComputedStyle(cv);S.col={r:cs.getPropertyValue("--red").trim()||"#C03200",l:cs.getPropertyValue("--lime").trim()||"#D8FF00",d:cs.getPropertyValue("--red2").trim()||"#862401"}}
          const cw=W/T.pc,ch=H/T.pr,dp=devicePixelRatio||1;
          for(const [i,op,sc] of tiles){const c=i%T.pc,r=(i/T.pc)|0,w=cw*sc,h=ch*sc,X=c*cw+(cw-w)/2,Y=r*ch+(ch-h)/2,k=T.k[i];
            x.globalAlpha=op;x.fillStyle=S.col[k];x.fillRect(X,Y,w+.5,h+.5);
            if(k==="l"){x.strokeStyle="rgba(0,0,0,.18)";x.lineWidth=dp*sc;x.strokeRect(X+x.lineWidth/2,Y+x.lineWidth/2,w-x.lineWidth,h-x.lineWidth)}}
          x.globalAlpha=1}
        S.drawn=any}}
    if(any)active=true;
    else if(cv._vis!==false){/* kapan sweep berikutnya mulai */let soon=1e9;for(let i=0;i<n;i++){const st=sec-(S.o+T.s[i]),ph=st<0?-st/S.cy:(st/S.cy)%1;
        const w=st<0?-st:ph<.389?(.389-ph)*S.cy:ph<.851?(.851-ph)*S.cy:(1.389-ph)*S.cy;if(w<soon)soon=w}next=Math.min(next,soon)}});
  clearTimeout(pxTimer);
  if(active)pxRaf=requestAnimationFrame(pxFrame);
  else if(next<1e9)pxTimer=setTimeout(()=>{pxRaf=requestAnimationFrame(pxFrame)},Math.max(16,next*1000-30))}
function pxKick(){if(!pxRaf){clearTimeout(pxTimer);pxRaf=requestAnimationFrame(pxFrame)}}
document.addEventListener("visibilitychange",()=>{if(!document.hidden)pxKick()});
function pxSwap(pc,pr,sw,cls=""){if(!cls.includes("pxc")){const k=[],ss=[];for(let r=0;r<pr;r++)for(let c=0;c<pc;c++){const x=c/(pc-1),q=Math.random();k.push(q<.5?"r":q<.8?"l":"d");ss.push(x*sw+(Math.random()-.5)*.1)}
    const id="px"+uid()+uid();PXT[id]={pc,pr,k,s:ss};setTimeout(pxKick,0);return `<canvas class="pxs pxcv${cls}" data-px="${id}" aria-hidden="true"></canvas>`}
  let px="";''')
rep("</style>\n\n__LOGO__", ".pxcv{display:block!important;width:100%;height:100%}\n.pxw.done{display:none!important}\n</style>\n\n__LOGO__")

# 2) Gelombang piksel intro (240 kotak) disembunyikan setelah selesai, bukan dibiarkan menempel
rep('const pc=40,pr=6,intro=Date.now()-PX0<3500;let px="";',
    'const pc=40,pr=6,intro=Date.now()-PX0<3500;let px="";if(intro){clearTimeout(window.__pxwT);window.__pxwT=setTimeout(()=>document.querySelectorAll(".pxw").forEach(w=>w.classList.add("done")),Math.max(600,4200-(Date.now()-PX0)))}')

# 3) Saat scroll: jeda animasi yang memaksa repaint (ring, kilau, kedip) lewat Web Animations API,
#    tanpa mengganti kelas di <html> (yang memicu hitung ulang gaya seluruh halaman)
rep('(()=>{let t;addEventListener("scroll",()=>{const h=document.documentElement;if(!h.classList.contains("scrl"))h.classList.add("scrl");clearTimeout(t);t=setTimeout(()=>h.classList.remove("scrl"),180)},{passive:true,capture:true})})();',
    '(()=>{let t=0,P=null;const HV=new Set(["ringOut","pulseRing","flow","shimmer","breathe"]);addEventListener("scroll",()=>{if(!P&&document.getAnimations){P=document.getAnimations().filter(a=>HV.has(a.animationName)&&a.playState==="running");P.forEach(a=>{try{a.pause()}catch(e){}})}clearTimeout(t);t=setTimeout(()=>{(P||[]).forEach(a=>{try{a.play()}catch(e){}});P=null},160)},{passive:true,capture:true})})();')

P.write_text(s)
print("OK, perbaikan kelancaran Kabar diterapkan.")
