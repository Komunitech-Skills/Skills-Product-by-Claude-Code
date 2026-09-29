#!/usr/bin/env python3
"""Uji angka hasil_eksperimen.py dengan nilai yang dihitung tangan / dari rumus tertutup.
Jalankan: python3 tests/uji_hasil_eksperimen.py  (exit 0 = lolos)."""
import importlib.util
import io
import os
import contextlib
import sys

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sp = importlib.util.spec_from_file_location("he", os.path.join(D, "scripts", "hasil_eksperimen.py"))
he = importlib.util.module_from_spec(sp)
sp.loader.exec_module(he)
gagal = []


def dekat(nama, aktual, harap, tol=1e-4):
    if abs(aktual - harap) > tol:
        gagal.append(f"{nama}: dapat {aktual}, harap {harap}")


def jalan(*argv):
    o, e = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(o), contextlib.redirect_stderr(e):
        try:
            kode = he.main(list(argv))
        except SystemExit as x:
            kode = x.code
    return kode, o.getvalue(), e.getvalue()


# Wilson: 6/20 -> tengah 0.33222, setengah 0.18675 (hitung tangan) => 0.1455 - 0.5190
lo, hi = he.wilson(6, 20)
dekat("wilson 6/20 bawah", lo, 0.1455)
dekat("wilson 6/20 atas", hi, 0.5190)
# 0/10: batas atas = z^2/(n+z^2) = 3.8416/13.8416 = 0.27754
lo, hi = he.wilson(0, 10)
dekat("wilson 0/10 bawah", lo, 0.0)
dekat("wilson 0/10 atas", hi, 3.8416 / 13.8416)
# 10/10: batas bawah = n/(n+z^2) = 10/13.8416
lo, hi = he.wilson(10, 10)
dekat("wilson 10/10 bawah", lo, 10 / 13.8416)
dekat("wilson 10/10 atas", hi, 1.0)
# 50/100: 0.5 -> 0.4038 - 0.5962
lo, hi = he.wilson(50, 100)
dekat("wilson 50/100 bawah", lo, 0.4038)
dekat("wilson 50/100 atas", hi, 0.5962)

# Dua proporsi 12/100 vs 24/100: pg=.18, se=sqrt(.18*.82*.02)=.054332, z=2.2087, p=.0272
z, p = he.dua_proporsi(12, 100, 24, 100)
dekat("z 12v24", z, 2.2087, 1e-3)
dekat("p 12v24", p, 0.0272, 1e-3)
# Sama -> z=0, p=1
z, p = he.dua_proporsi(10, 50, 10, 50)
dekat("z sama", z, 0.0)
dekat("p sama", p, 1.0)
# Nol semua -> tidak error
z, p = he.dua_proporsi(0, 50, 0, 50)
dekat("p nol", p, 1.0)

# Ukuran sampel: 1.96^2*.25/.01 = 96.04 -> 97 ; margin 5 -> 384.16 -> 385 ; p=.2 margin 5 -> 245.86 -> 246
if he.ukuran_sampel(0.10) != 97: gagal.append("sampel 10% harus 97")
if he.ukuran_sampel(0.05) != 385: gagal.append("sampel 5% harus 385")
if he.ukuran_sampel(0.05, 0.2) != 246: gagal.append("sampel 5% p20 harus 246")

# CLI: keputusan
k, o, _ = jalan("hasil", "--ditawari", "80", "--aksi", "14", "--target", "15")
if k != 0 or "17,5%" not in o or "LANJUT DENGAN CATATAN" not in o: gagal.append("hasil 14/80 target 15: " + o)
k, o, _ = jalan("hasil", "--ditawari", "200", "--aksi", "60", "--target", "15")
if "LANJUT (kuat)" not in o: gagal.append("hasil 60/200 harus LANJUT kuat: " + o)
k, o, _ = jalan("hasil", "--ditawari", "80", "--aksi", "8", "--target", "15", "--batas-stop", "8")
if "UBAH" not in o: gagal.append("hasil 8/80 (10%) harus UBAH: " + o)
k, o, _ = jalan("hasil", "--ditawari", "100", "--aksi", "3", "--target", "15")
if "STOP" not in o: gagal.append("hasil 3/100 harus STOP: " + o)
k, o, _ = jalan("hasil", "--ditawari", "10", "--aksi", "4")
if "SAMPEL KECIL" not in o: gagal.append("n=10 harus peringatan sampel kecil")
k, o, _ = jalan("banding", "--a-ditawari", "100", "--a-aksi", "12", "--b-ditawari", "100", "--b-aksi", "24")
if "Varian B memang lebih baik" not in o: gagal.append("banding 12v24: " + o)
k, o, _ = jalan("banding", "--a-ditawari", "20", "--a-aksi", "3", "--b-ditawari", "20", "--b-aksi", "6")
if "SAMPEL KECIL" not in o or "kebetulan" not in o: gagal.append("banding kecil: " + o)

# Data rusak -> kode 2 + pesan jelas, bukan traceback
for argv in (("hasil", "--ditawari", "0", "--aksi", "0"),
             ("hasil", "--ditawari", "10", "--aksi", "12"),
             ("hasil", "--ditawari", "10", "--aksi", "-1"),
             ("banding", "--a-ditawari", "10", "--a-aksi", "11", "--b-ditawari", "10", "--b-aksi", "1"),
             ("hasil", "--ditawari", "10", "--aksi", "3", "--target", "10", "--batas-stop", "20"),
             ("hasil", "--ditawari", "10", "--aksi", "3", "--target", "0"),
             ("sampel", "--margin", "0"),
             ("sampel", "--margin", "10", "--perkiraan", "100")):
    k, o, e = jalan(*argv)
    if k != 2 or "INPUT TIDAK VALID" not in e or "Traceback" in e:
        gagal.append(f"data rusak {argv}: kode={k} err={e!r}")
for argv in (("hasil", "--ditawari", "abc", "--aksi", "3"), ("hasil", "--ditawari", "1.000", "--aksi", "3")):
    k, o, e = jalan(*argv)
    if k == 0 or "bilangan bulat" not in e: gagal.append(f"non-angka {argv}: {k} {e!r}")

if gagal:
    print("GAGAL:\n- " + "\n- ".join(gagal))
    sys.exit(1)
print("Semua uji lolos.")
