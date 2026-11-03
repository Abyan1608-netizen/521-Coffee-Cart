"""Perubahan 14: tombol "Jadikan HP Owner" pada peringatan di Langganan/Menu kini membuka Atur → Sinkron (sebelumnya diam). Sekali jalan."""
import pathlib, sys
P = pathlib.Path(__file__).resolve().parents[2] / "src/index.src.html"
s = P.read_text()
if "/*V14-PATCH*/" in s:
    print("Sudah dipatch."); sys.exit(0)
old = 'else if(a==="setsub"){if(v==="resep"){tab="resep"}else setSub=v;render();window.scrollTo(0,0)}'
assert s.count(old) == 1
s = s.replace(old, 'else if(a==="setsub"){/*V14-PATCH*/if(v==="resep"){tab="resep"}else{tab="set";setSub=v}render();window.scrollTo(0,0)}')
P.write_text(s)
print("OK, perubahan 14 (tombol Jadikan HP Owner) diterapkan.")
