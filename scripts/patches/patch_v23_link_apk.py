"""Perubahan 23: repo aplikasi dijadikan private → link unduh APK di GitHub tidak bisa dibuka tim lagi.
"Bagikan cara masuk ke tim" (Atur → Sinkron tim) memakai link unduh yang diisi Owner sendiri (mis. Google Drive),
disimpan di HP Owner ini saja (tidak ikut terbit ke website). Tanpa link: tim diminta meminta file APK ke Owner.
Sekali jalan."""
import pathlib, sys

HERE = pathlib.Path(__file__).resolve().parent
P = HERE.parents[1] / "src/index.src.html"
s = P.read_text()
if "/*V23-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


rep('<button class="btn" data-a="tcopy">${ic("copy")}Bagikan cara masuk ke tim</button>${what}',
    '<label>Link unduh aplikasi (APK)<input id="apklink" type="url" inputmode="url" autocomplete="off" autocapitalize="off" spellcheck="false" '
    'placeholder="https://drive.google.com/…" value="${esc(C().apkLink||"")}"></label>'
    '<p class="note" style="margin-top:-4px">Tempel link Google Drive file APK terbaru. Hanya tersimpan di HP ini.</p>'
    '<button class="btn" data-a="tcopy">${ic("copy")}Bagikan cara masuk ke tim</button>${what}')
rep('else if(a==="tcopy"&&own()){const t=`Pasang aplikasi 521 Coffee App: https://github.com/Abyan1608-netizen/521-Coffee-Cart/releases/latest/download/521-Coffee-App.apk\\n(Bila HP bertanya, izinkan pemasangan aplikasi dari sumber ini.)\\n',
    'else if(a==="tcopy"&&own()){/*V23-PATCH*/const li=$("#apklink");let L=li?li.value.trim():(C().apkLink||"");'
    'if(L&&!/^https:\\/\\/\\S+$/.test(L)){toast("Link unduh harus diawali https://",1);if(li)li.focus();return}if(li){C().apkLink=L;save()}'
    'const t=`${L?"Pasang aplikasi 521 Coffee App: "+L:"Minta file aplikasi 521 Coffee App (APK) ke Owner, lalu pasang."}\\n(Bila HP bertanya, izinkan pemasangan aplikasi dari sumber ini.)\\n')
P.write_text(s)
print("OK, perubahan 23 diterapkan.")
