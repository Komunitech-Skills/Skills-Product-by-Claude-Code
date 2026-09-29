#!/usr/bin/env python3
"""Hitung hasil uji pasar: konversi, rentang wajar (Wilson 95%), perbandingan dua varian
(uji z dua proporsi), dan ukuran sampel kasar. Hanya Python standar (3.8+).

Windows: pakai `python` atau `py` sebagai ganti `python3`.

  python3 scripts/hasil_eksperimen.py hasil   --ditawari 80 --aksi 14 [--target 15] [--batas-stop 8]
  python3 scripts/hasil_eksperimen.py banding --a-ditawari 100 --a-aksi 12 --b-ditawari 100 --b-aksi 24
  python3 scripts/hasil_eksperimen.py sampel  --margin 10 [--perkiraan 20]

Angka dihitung, bukan dikira. Ini alat bantu keputusan skala UMKM, bukan bukti ilmiah.
"""
import argparse
import math
import sys

Z95 = 1.96
SAMPEL_MIN = 30          # di bawah ini hanya "sinyal arah"
SAMPEL_MIN_BANDING = 50  # per varian


class InputSalah(Exception):
    pass


def cek_hitungan(ditawari, aksi, label=""):
    """Validasi: bilangan bulat, ditawari > 0, 0 <= aksi <= ditawari."""
    p = f" {label}" if label else ""
    for nama, v in (("ditawari", ditawari), ("aksi", aksi)):
        if isinstance(v, bool) or not isinstance(v, int):
            raise InputSalah(f"Jumlah{p} '{nama}' harus bilangan bulat (orang), bukan {v!r}.")
    if ditawari <= 0:
        raise InputSalah(f"Jumlah orang yang ditawari{p} harus lebih dari 0.")
    if aksi < 0:
        raise InputSalah(f"Jumlah yang beraksi{p} tidak boleh negatif.")
    if aksi > ditawari:
        raise InputSalah(
            f"Yang beraksi{p} ({aksi}) lebih banyak dari yang ditawari ({ditawari}). "
            "Cek lagi catatan: satu orang hanya dihitung sekali.")


def wilson(x, n, z=Z95):
    """Rentang wajar (interval Wilson) untuk proporsi x/n. Kembali (bawah, atas) dalam 0..1."""
    p = x / n
    z2 = z * z
    penyebut = 1 + z2 / n
    tengah = (p + z2 / (2 * n)) / penyebut
    setengah = z * math.sqrt(p * (1 - p) / n + z2 / (4 * n * n)) / penyebut
    return max(0.0, tengah - setengah), min(1.0, tengah + setengah)


def _phi(z):
    """Fungsi sebaran normal baku (CDF)."""
    return 0.5 * math.erfc(-z / math.sqrt(2))


def dua_proporsi(xa, na, xb, nb):
    """Uji z dua proporsi (dua sisi, proporsi gabungan). Kembali (z, p_value)."""
    pg = (xa + xb) / (na + nb)
    se = math.sqrt(pg * (1 - pg) * (1 / na + 1 / nb))
    if se == 0:  # keduanya 0% atau keduanya 100%
        return 0.0, 1.0
    z = (xb / nb - xa / na) / se
    return z, math.erfc(abs(z) / math.sqrt(2))


def ukuran_sampel(margin, perkiraan=0.5, z=Z95):
    """Jumlah orang agar tebakan konversi meleset paling jauh +-margin (0..1)."""
    return math.ceil(z * z * perkiraan * (1 - perkiraan) / (margin * margin))


def pct(v, d=1):
    return f"{v * 100:.{d}f}".replace(".", ",") + "%"


def cmd_hasil(a):
    cek_hitungan(a.ditawari, a.aksi)
    n, x = a.ditawari, a.aksi
    p = x / n
    lo, hi = wilson(x, n)
    out = [f"Konversi: {x} dari {n} orang = {pct(p)}",
           f"Rentang wajar 95% (Wilson): {pct(lo)} sampai {pct(hi)}",
           f"Artinya: kalau uji diulang, hasil sebenarnya kemungkinan besar ada di antara {pct(lo, 0)} dan {pct(hi, 0)}."]
    if n < SAMPEL_MIN:
        out.append(f"PERINGATAN SAMPEL KECIL: baru {n} orang (< {SAMPEL_MIN}). Rentangnya lebar; "
                   "anggap ini sinyal arah saja, jangan keputusan besar. Tambah sampel bila bisa.")
    if a.target is not None:
        t = a.target / 100
        stop = (a.batas_stop if a.batas_stop is not None else a.target / 2) / 100
        if not (0 < t <= 1) or not (0 <= stop < t):
            raise InputSalah("Target harus antara 0 dan 100 (persen), dan batas stop harus lebih kecil dari target.")
        out.append(f"Kriteria (ditetapkan SEBELUM uji): lanjut jika >= {pct(t)}, stop jika < {pct(stop)}.")
        if p >= t:
            if lo >= t:
                v = "LANJUT (kuat): bahkan batas bawah rentang wajar sudah mencapai target."
            else:
                v = ("LANJUT DENGAN CATATAN: angka mencapai target, tapi batas bawah rentang "
                     f"({pct(lo)}) masih di bawah target. Lanjut bertahap kecil (mis. produksi batch kecil) "
                     "atau tambah sampel dulu.")
        elif p >= stop:
            v = ("UBAH: di bawah target tapi belum sampai batas stop. Ubah SATU hal (harga, tawaran, "
                 "kemasan, atau kelompok pembeli) lalu uji ulang. Lihat pilihan pivot di SKILL.md.")
        else:
            v = "STOP: di bawah batas stop. Hentikan atau ganti arah; jangan menambah modal."
            if hi >= t:
                v += (f" Catatan: batas atas rentang ({pct(hi)}) masih menyentuh target, "
                      "jadi sampel terlalu kecil untuk yakin; boleh satu kali uji ulang murah.")
        out.append("KEPUTUSAN: " + v)
    print("\n".join(out))


def cmd_banding(a):
    cek_hitungan(a.a_ditawari, a.a_aksi, "varian A")
    cek_hitungan(a.b_ditawari, a.b_aksi, "varian B")
    na, xa, nb, xb = a.a_ditawari, a.a_aksi, a.b_ditawari, a.b_aksi
    pa, pb = xa / na, xb / nb
    la, ha = wilson(xa, na)
    lb, hb = wilson(xb, nb)
    z, pv = dua_proporsi(xa, na, xb, nb)
    out = [f"Varian A: {xa}/{na} = {pct(pa)} (rentang wajar {pct(la)} - {pct(ha)})",
           f"Varian B: {xb}/{nb} = {pct(pb)} (rentang wajar {pct(lb)} - {pct(hb)})",
           f"Selisih B - A: {(pb - pa) * 100:+.1f} poin persen".replace(".", ","),
           f"Nilai z = {z:.2f}; p = {pv:.4f}".replace(".", ",")]
    if pv < 0.05:
        unggul = "B" if pb > pa else "A"
        out.append(f"Artinya: selisih ini cukup jelas (p < 0,05). Varian {unggul} memang lebih baik, "
                   "bukan kebetulan (dengan keyakinan sekitar 95%).")
    elif pv < 0.20:
        out.append("Artinya: ada kecenderungan, tapi BELUM meyakinkan (p antara 0,05 dan 0,20). "
                   "Tambah sampel atau ulang uji sebelum memutuskan.")
    else:
        out.append("Artinya: selisih ini bisa saja kebetulan. Belum ada bukti satu varian lebih baik. "
                   "Pilih yang biayanya lebih murah atau uji ulang dengan sampel lebih besar.")
    for nm, n, x in (("A", na, xa), ("B", nb, xb)):
        if n < SAMPEL_MIN_BANDING:
            out.append(f"PERINGATAN SAMPEL KECIL: varian {nm} hanya {n} orang (< {SAMPEL_MIN_BANDING}). "
                       "Perbandingan dua varian butuh minimal sekitar 50 orang per varian.")
    pg = (xa + xb) / (na + nb)
    if min(na * pg, na * (1 - pg), nb * pg, nb * (1 - pg)) < 5:
        out.append("PERINGATAN: hitungan sangat kecil (ada sel < 5 orang) sehingga rumus ini kurang akurat. "
                   "Anggap hasil hanya gambaran kasar.")
    if abs(na - nb) > 0.5 * max(na, nb):
        out.append("CATATAN: jumlah orang di dua varian timpang jauh; pastikan dua kelompok setara "
                   "(waktu, kanal, jenis pembeli sama).")
    print("\n".join(out))


def cmd_sampel(a):
    m = a.margin / 100
    pr = a.perkiraan / 100
    if not (0 < m < 1) or not (0 < pr < 1):
        raise InputSalah("Margin dan perkiraan harus antara 0 dan 100 (persen), bukan 0 atau 100.")
    n = ukuran_sampel(m, pr)
    print(f"Agar konversi meleset paling jauh +-{pct(m, 0)} (keyakinan 95%), dengan perkiraan konversi {pct(pr, 0)}: "
          f"butuh sekitar {n} orang.")
    if a.perkiraan != 50:
        print(f"Kalau tidak punya perkiraan (paling aman, anggap 50%): {ukuran_sampel(m)} orang.")
    print("Untuk membandingkan dua varian, kira-kira butuh SEBANYAK itu untuk TIAP varian bila selisih yang dicari kecil.")


def angka_bulat(s):
    try:
        return int(str(s).strip())
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{s}' bukan bilangan bulat. Tulis jumlah orang tanpa titik/koma/huruf (contoh: 80).")


def angka_desimal(s):
    try:
        v = float(str(s).strip().replace(",", "."))
    except ValueError:
        raise argparse.ArgumentTypeError(f"'{s}' bukan angka. Tulis persen tanpa tanda % (contoh: 15).")
    if math.isnan(v) or math.isinf(v):
        raise argparse.ArgumentTypeError(f"'{s}' bukan angka yang valid.")
    return v


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hitung hasil uji pasar (konversi, Wilson, banding varian).")
    sub = ap.add_subparsers(dest="perintah", required=True)
    h = sub.add_parser("hasil", help="satu uji: konversi + rentang wajar + keputusan")
    h.add_argument("--ditawari", type=angka_bulat, required=True)
    h.add_argument("--aksi", type=angka_bulat, required=True, help="yang benar-benar pre-order/bayar/klik target")
    h.add_argument("--target", type=angka_desimal, help="kriteria lanjut, persen (ditetapkan sebelum uji)")
    h.add_argument("--batas-stop", type=angka_desimal, help="batas stop, persen (default: setengah target)")
    h.set_defaults(f=cmd_hasil)
    b = sub.add_parser("banding", help="dua varian: uji z dua proporsi")
    for k in ("a-ditawari", "a-aksi", "b-ditawari", "b-aksi"):
        b.add_argument("--" + k, type=angka_bulat, required=True)
    b.set_defaults(f=cmd_banding)
    s = sub.add_parser("sampel", help="ukuran sampel kasar")
    s.add_argument("--margin", type=angka_desimal, required=True, help="toleransi meleset, poin persen")
    s.add_argument("--perkiraan", type=angka_desimal, default=50.0, help="perkiraan konversi, persen (default 50)")
    s.set_defaults(f=cmd_sampel)
    a = ap.parse_args(argv)
    try:
        a.f(a)
    except InputSalah as e:
        print(f"INPUT TIDAK VALID: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
