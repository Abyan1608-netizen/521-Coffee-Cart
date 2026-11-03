"""Perubahan 15: tombol "Kirim ulang sekarang" di Atur → Sinkron dihapus (pengiriman sudah otomatis). Sekali jalan."""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V15-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)
old = '<button class="btn ghost" data-a="tsync">Kirim ulang sekarang</button><button class="btn ghost" data-a="tnew"'
assert s.count(old) == 1
s = s.replace(old, '<button class="btn ghost" data-a="tnew"')
old = 'function syncView(){'
assert s.count(old) == 1
s = s.replace(old, '/*V15-PATCH*/function syncView(){')
P.write_text(s)
print("OK, perubahan 15 (tombol Kirim ulang dihapus) diterapkan.")
