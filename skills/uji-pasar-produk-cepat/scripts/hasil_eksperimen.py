#!/usr/bin/env python3
"""Hitung hasil uji pasar: konversi, rentang wajar (Wilson 95%), perbandingan dua varian
(uji z dua proporsi; uji Fisher tepat bila sampel kecil), dan ukuran sampel
(satu uji, atau dua varian dengan power 80%). Hanya Python standar (3.8+).

Windows: pakai `python` atau `py` sebagai ganti `python3`.

  python3 scripts/hasil_eksperimen.py hasil   --ditawari 80 --aksi 14 [--target 15] [--batas-stop 8]
  python3 scripts/hasil_eksperimen.py banding --a-ditawari 100 --a-aksi 12 --b-ditawari 100 --b-aksi 24
  python3 scripts/hasil_eksperimen.py sampel  --margin 10 [--perkiraan 20]
  python3 scripts/hasil_eksperimen.py sampel  --banding --a 15 --b 25

Angka dihitung, bukan dikira. Ini alat bantu keputusan skala UMKM, bukan bukti ilmiah.
"""
import argparse
import math
import re
import sys

Z95 = 1.96
Z_ALFA = 1.959964   # alfa 5% dua sisi
Z_POWER = 0.841621  # power 80%
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


def fisher_tepat(xa, na, xb, nb):
    """Uji Fisher tepat dua sisi untuk tabel 2x2 (pakai math.comb). Kembali p_value.
    Dua sisi = jumlah peluang semua tabel (total baris & kolom tetap) yang peluangnya
    <= peluang tabel teramati."""
    k = xa + xb          # total yang beraksi
    n = na + nb
    total = math.comb(n, k)
    def peluang(x):     # x = aksi di varian A
        return math.comb(na, x) * math.comb(nb, k - x) / total
    amati = peluang(xa)
    batas = amati * (1 + 1e-7)
    p = sum(peluang(x) for x in range(max(0, k - nb), min(k, na) + 1) if peluang(x) <= batas)
    return min(1.0, p)


def sampel_banding(pa, pb, z_alfa=Z_ALFA, z_power=Z_POWER):
    """Orang per varian agar selisih pa vs pb (0..1) terdeteksi: alfa 5% dua sisi, power 80%.
    Rumus pendekatan normal standar (tanpa koreksi kontinuitas)."""
    rata = (pa + pb) / 2
    atas = (z_alfa * math.sqrt(2 * rata * (1 - rata))
            + z_power * math.sqrt(pa * (1 - pa) + pb * (1 - pb))) ** 2
    return math.ceil(atas / (pa - pb) ** 2)


def ukuran_sampel(margin, perkiraan=0.5, z=Z95):
    """Jumlah orang agar tebakan konversi meleset paling jauh +-margin (0..1)."""
    return math.ceil(z * z * perkiraan * (1 - perkiraan) / (margin * margin))


def ribuan(n):
    return f"{n:,}".replace(",", ".")


def pct(v, d=1):
    return f"{v * 100:.{d}f}".replace(".", ",") + "%"


def cmd_hasil(a):
    cek_hitungan(a.ditawari, a.aksi)
    n, x = a.ditawari, a.aksi
    p = x / n
    lo, hi = wilson(x, n)
    out = [f"Konversi: {x} dari {n} orang = {pct(p)}",
           f"Rentang wajar 95% (Wilson): {pct(lo)} sampai {pct(hi)}",
           f"Artinya: dengan data ini, angka sebenarnya kemungkinan besar ada di antara {pct(lo, 0)} dan {pct(hi, 0)}."]
    if n < SAMPEL_MIN:
        out.append(f"PERINGATAN SAMPEL KECIL: baru {n} orang (< {SAMPEL_MIN}). Rentangnya lebar; "
                   "anggap ini sinyal arah saja, jangan keputusan besar. Tambah sampel bila bisa.")
    if a.target is None and a.batas_stop is not None:
        out.append("PERINGATAN: --batas-stop diberikan tanpa --target, jadi tidak dipakai dan tidak ada keputusan "
                   "LANJUT/UBAH/STOP. Tambahkan --target (persen ambang lanjut) untuk mendapat keputusan.")
    if a.target is not None:
        t = a.target / 100
        stop = (a.batas_stop if a.batas_stop is not None else a.target / 2) / 100
        if not (0 < t <= 1) or not (0 <= stop < t):
            raise InputSalah("Target harus antara 0 dan 100 (persen), dan batas stop harus lebih kecil dari target.")
        out.append(f"Kriteria (ditetapkan SEBELUM uji): lanjut jika >= {pct(t)}, stop jika < {pct(stop)}.")
        if p >= t:
            if lo >= t and n >= SAMPEL_MIN:
                v = "LANJUT (kuat): bahkan batas bawah rentang wajar sudah mencapai target."
            elif lo >= t:
                v = (f"LANJUT BERTAHAP (sampel kecil): batas bawah rentang sudah mencapai target, tapi baru {n} orang "
                     f"(< {SAMPEL_MIN}). Mulai dari batch kecil dan tambah sampel sebelum modal besar.")
            else:
                v = ("LANJUT BERTAHAP: angka mencapai target, tapi batas bawah rentang "
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
    pg = (xa + xb) / (na + nb)
    sel_kecil = min(na * pg, na * (1 - pg), nb * pg, nb * (1 - pg)) < 5
    kecil = sel_kecil or min(na, nb) < SAMPEL_MIN_BANDING
    out = [f"Varian A: {xa}/{na} = {pct(pa)} (rentang wajar {pct(la)} - {pct(ha)})",
           f"Varian B: {xb}/{nb} = {pct(pb)} (rentang wajar {pct(lb)} - {pct(hb)})",
           f"Selisih B - A: {(pb - pa) * 100:+.1f} poin persen".replace(".", ","),
           f"Nilai z = {z:.2f}; p (uji z) = {pv:.4f}".replace(".", ",")]
    if kecil:
        pf = fisher_tepat(xa, na, xb, nb)
        out.append(f"Sampel kecil, jadi dipakai uji Fisher tepat: p = {pf:.4f}".replace(".", ","))
        pv = pf
    unggul = "B" if pb > pa else "A"
    if pv < 0.05 and not kecil:
        out.append(f"Artinya: selisih sebesar ini jarang muncul hanya karena kebetulan (p < 0,05). "
                   f"Varian {unggul} layak dipilih sebagai pemenang untuk kelompok pembeli seperti ini.")
    elif pv < 0.05:
        out.append(f"Artinya: ada tanda varian {unggul} lebih baik (p < 0,05), tapi sampel terlalu kecil untuk yakin. "
                   "Anggap sementara; uji ulang dengan sampel lebih besar sebelum keputusan modal "
                   "(hitung dengan: sampel --banding).")
    elif pv < 0.20:
        out.append("Artinya: ada kecenderungan, tapi BELUM meyakinkan (p antara 0,05 dan 0,20). "
                   "Tambah sampel atau ulang uji sebelum memutuskan (hitung dengan: sampel --banding).")
    else:
        out.append("Artinya: selisih ini bisa saja muncul karena kebetulan. Belum ada bukti satu varian lebih baik. "
                   "Pilih yang biayanya lebih murah atau uji ulang dengan sampel lebih besar.")
    for nm, n, x in (("A", na, xa), ("B", nb, xb)):
        if n < SAMPEL_MIN_BANDING:
            out.append(f"PERINGATAN SAMPEL KECIL: varian {nm} hanya {n} orang (< {SAMPEL_MIN_BANDING}). "
                       "Perbandingan dua varian butuh minimal sekitar 50 orang per varian.")
    if sel_kecil:
        out.append("PERINGATAN: hitungan sangat kecil (ada sel harapan < 5 orang), jadi uji z kurang akurat; "
                   "p di atas memakai uji Fisher tepat. Tetap anggap hasil gambaran kasar.")
    if abs(na - nb) > 0.5 * max(na, nb):
        out.append("CATATAN: jumlah orang di dua varian timpang jauh; pastikan dua kelompok setara "
                   "(waktu, kanal, jenis pembeli sama).")
    print("\n".join(out))


def cmd_sampel(a):
    if a.banding:
        if a.a is None or a.b is None:
            raise InputSalah("Untuk --banding, isi --a dan --b (perkiraan konversi tiap varian, persen). "
                             "Contoh: sampel --banding --a 15 --b 25")
        pa, pb = a.a / 100, a.b / 100
        if not (0 < pa < 1) or not (0 < pb < 1):
            raise InputSalah("--a dan --b harus antara 0 dan 100 (persen), bukan 0 atau 100.")
        if pa == pb:
            raise InputSalah("--a dan --b sama; isi selisih terkecil yang ingin bisa dibedakan (mis. --a 15 --b 25).")
        n = sampel_banding(pa, pb)
        print(f"Agar selisih {pct(pa, 1)} vs {pct(pb, 1)} bisa terdeteksi (power 80%, alfa 5% dua sisi): "
              f"butuh sekitar {ribuan(n)} orang PER VARIAN (total {ribuan(2 * n)}).")
        print("Artinya: kalau selisih sebenarnya memang sebesar itu, peluang uji menemukannya sekitar 80%. "
              "Selisih lebih kecil butuh jauh lebih banyak orang.")
        if n > 400:
            print("CATATAN: ini banyak untuk skala UMKM. Pilihan: uji perbedaan yang lebih besar (mis. harga yang "
                  "jauh berbeda), kumpulkan beberapa minggu, atau terima hasil 'belum ada pemenang' dan pilih yang lebih murah.")
        return
    if a.margin is None:
        raise InputSalah("Isi --margin (toleransi meleset, poin persen), atau pakai --banding --a X --b Y "
                         "untuk membandingkan dua varian.")
    m = a.margin / 100
    pr = a.perkiraan / 100
    if not (0 < m < 1) or not (0 < pr < 1):
        raise InputSalah("Margin dan perkiraan harus antara 0 dan 100 (persen), bukan 0 atau 100.")
    n = ukuran_sampel(m, pr)
    print(f"Agar konversi meleset paling jauh +-{pct(m, 0)} (keyakinan 95%), dengan perkiraan konversi {pct(pr, 0)}: "
          f"butuh sekitar {ribuan(n)} orang.")
    if a.perkiraan != 50:
        print(f"Kalau tidak punya perkiraan (paling aman, anggap 50%): {ribuan(ukuran_sampel(m))} orang.")
    if m >= pr:
        saran = a.perkiraan / 2
        print(f"PERINGATAN: margin (+-{pct(m, 1)}) sama atau lebih besar dari perkiraan konversi ({pct(pr, 1)}), "
              "jadi rentangnya bisa menyentuh 0% dan hasilnya tidak berguna untuk keputusan. "
              "Pakai margin sekitar separuh perkiraan (mis. --margin " + f"{saran:g}".replace(".", ",") + ").")
    if n < SAMPEL_MIN:
        print(f"PERINGATAN: hasil hitungan di bawah {SAMPEL_MIN} orang. Tetap tawari minimal {SAMPEL_MIN} orang; "
              "di bawah itu hanya sinyal arah.")
    print("Angka ini untuk SATU uji. Untuk membandingkan dua varian, jumlahnya berbeda (biasanya jauh lebih besar): "
          "pakai sampel --banding --a <persen A> --b <persen B>.")


def angka_bulat(s):
    try:
        return int(str(s).strip())
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"'{s}' bukan bilangan bulat. Tulis jumlah orang tanpa titik/koma/huruf (contoh: 80).")


def angka_desimal(s):
    t = str(s).strip()
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", t) or re.fullmatch(r"\d{1,3}(,\d{3}){2,}", t):
        raise argparse.ArgumentTypeError(
            f"'{s}' terlihat seperti angka ribuan, padahal ini persen. Tulis persen tanpa pemisah ribuan; "
            "untuk desimal pakai koma (contoh: 1,25 untuk satu koma dua lima persen).")
    try:
        v = float(t.replace(",", "."))
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
    b = sub.add_parser("banding", help="dua varian: uji z dua proporsi (Fisher tepat bila sampel kecil)")
    for k in ("a-ditawari", "a-aksi", "b-ditawari", "b-aksi"):
        b.add_argument("--" + k, type=angka_bulat, required=True)
    b.set_defaults(f=cmd_banding)
    s = sub.add_parser("sampel", help="ukuran sampel: satu uji (--margin) atau dua varian (--banding --a --b)")
    s.add_argument("--margin", type=angka_desimal, help="toleransi meleset, poin persen")
    s.add_argument("--perkiraan", type=angka_desimal, default=50.0, help="perkiraan konversi, persen (default 50)")
    s.add_argument("--banding", action="store_true", help="hitung orang per varian untuk membandingkan dua varian")
    s.add_argument("--a", type=angka_desimal, help="perkiraan konversi varian A, persen")
    s.add_argument("--b", type=angka_desimal, help="perkiraan konversi varian B, persen")
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
