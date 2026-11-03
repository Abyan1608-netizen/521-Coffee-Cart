"""Perubahan 13: link & QR Play Store dihapus dari aplikasi (aplikasi belum terbit di Play Store).
Link halaman promo kini kosong secara bawaan; tombol "QR kabar & promo" dan baris link di struk otomatis hilang.
Owner tetap bisa mengisi link sendiri di Atur → Halaman publik. Bagikan cara masuk ke tim memakai link APK GitHub. Sekali jalan."""
import pathlib, sys

P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V13-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)


def rep(old, new, count=1):
    global s
    n = s.count(old)
    if n != count:
        raise SystemExit(f"Jumlah cocok {n} != {count} untuk:\n{old[:220]}")
    s = s.replace(old, new)


rep('qris:"default",paper:32,promo:PLAY_URL};', 'qris:"default",paper:32,promo:""};')
rep('if(!d.cfg.promo||/^https:\\/\\/claude\\.ai\\//.test(d.cfg.promo))d.cfg.promo=PLAY_URL;',
    '/*V13-PATCH*/if(!d.cfg.promoV13){if(/^https:\\/\\/(claude\\.ai\\/|play\\.google\\.com\\/)/.test(d.cfg.promo||""))d.cfg.promo="";d.cfg.promoV13=1}if(/^https:\\/\\/claude\\.ai\\//.test(d.cfg.promo||""))d.cfg.promo="";')
rep('placeholder="${PLAY_URL}"></label>', 'placeholder="https://… (kosongkan bila belum ada)"></label>')
rep('const t=`Pasang aplikasi 521 Coffee App: ${C().promo||location.href}\\nBuka aplikasinya → Masuk → isi nama & PIN dari Owner. HP langsung tersambung ke tim.`;',
    'const t=`Pasang aplikasi 521 Coffee App: https://github.com/Abyan1608-netizen/521-Coffee-Cart/releases/latest/download/521-Coffee-App.apk\\n(Bila HP bertanya, izinkan pemasangan aplikasi dari sumber ini.)\\nBuka aplikasinya → Masuk → isi nama & PIN dari Owner. HP langsung tersambung ke tim.`;')
P.write_text(s)
print("OK, perubahan 13 (link & QR Play Store dihapus) diterapkan.")
