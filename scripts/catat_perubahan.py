"""Buat folder catatan untuk perubahan baru + tambahkan ke CHANGELOG.md.
Pakai:  python3 scripts/catat_perubahan.py "judul singkat perubahan"
Lalu isi CATATAN.md di folder yang dibuat."""
import datetime, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = ROOT / "riwayat-perubahan"
if len(sys.argv) < 2:
    sys.exit('Pakai: python3 scripts/catat_perubahan.py "judul singkat"')
judul = " ".join(sys.argv[1:]).strip()
nomor = 1 + max([int(m.group(1)) for d in H.glob("*_*_*") if (m := re.match(r"\d{4}-\d{2}-\d{2}_(\d+)_", d.name))] or [0])
tgl = datetime.date.today().isoformat()
slug = re.sub(r"[^a-z0-9]+", "-", judul.lower()).strip("-")[:50]
d = H / f"{tgl}_{nomor:02d}_{slug}"
(d / "salinan").mkdir(parents=True)
(d / "CATATAN.md").write_text(f"""# {nomor:02d} · {judul}
**Tanggal:** {tgl}

## Apa yang berubah
-

## Alasan
-

## File yang diubah
-

## Cara menguji
-

## Cara membatalkan
-
""")
cl = ROOT / "CHANGELOG.md"
t = cl.read_text()
entry = f"## {nomor:02d} · {tgl} · {judul}\n(isi ringkasan)\n→ `riwayat-perubahan/{d.name}/`\n\n"
i = t.find("\n## ")
cl.write_text(t[:i + 1] + entry + t[i + 1:] if i >= 0 else t + "\n" + entry)
print("Dibuat:", d.relative_to(ROOT))
