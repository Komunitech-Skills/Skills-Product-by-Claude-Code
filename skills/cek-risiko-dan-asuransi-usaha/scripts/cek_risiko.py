#!/usr/bin/env python3
"""Hitung skor risiko usaha dan dana darurat. Python standar saja.

Pakai (Windows: python / py):
  python3 scripts/cek_risiko.py risiko berkas.json
  python3 scripts/cek_risiko.py dana --biaya "Sewa=3000000,Gaji=8000000" --bulan 3 [--kas 5000000] [--cicil 6]

berkas.json: [{"nama": "Kebakaran", "kemungkinan": 2, "dampak": 5, "kerugian_rp": 80000000}, ...]
kemungkinan dan dampak: bilangan bulat 1-5. kerugian_rp opsional.
bisa_diasuransikan: opsional (default true); false untuk risiko tanpa asuransi umum
(mis. akun marketplace dibekukan, orang kunci keluar).
kategori: opsional. "bpjs" = risiko karyawan cedera/sakit/kecelakaan kerja; kolom asuransi diisi
label BPJS otomatis. Tanpa field ini, nama risiko yang jelas soal karyawan cedera/sakit/kecelakaan
kerja dikenali otomatis. "umum" = matikan pengenalan otomatis.
Angka: tulis 3000000 atau 3.000.000 (titik = ribuan); desimal ditolak.
"""
import argparse
import json
import re
import sys

LABEL_BPJS = ("BPJS: kewajiban pemberi kerja, cek aturan terbaru "
              "(JKK untuk kecelakaan kerja; BPJS Kesehatan untuk sakit)")
RESPONS_BPJS = "Kurangi (K3, perlengkapan kerja) + daftarkan BPJS karyawan"
KATEGORI_SAH = ("umum", "bpjs")
_PEKERJA = r"(karyawan|pegawai|pekerja|buruh|staf|staff|kasir|koki|barista|mekanik|teknisi|kurir|pelayan|asisten)"
_KERJA = r"cedera kerja|kecelakaan kerja|\bk3\b"
_KONDISI = r"cedera|kecelakaan|sakit|luka|tertusuk|terpeleset|terjepit"
_POLA_BPJS = re.compile(_KERJA + "|" + _PEKERJA + r"\b[^|]{0,40}(" + _KONDISI + ")", re.IGNORECASE)
# bukan risiko BPJS: korban pelanggan/pihak luar, pemilik, atau orang kunci yang keluar
_POLA_BUKAN = re.compile(r"pelanggan|pembeli|tamu|pengunjung|konsumen|pemilik|owner|pemasok|supplier|"
                         r"keluar|pindah|resign|mundur", re.IGNORECASE)

PERINGKAT = [(15, "KRITIS"), (10, "TINGGI"), (5, "SEDANG"), (1, "RENDAH")]


def rp(n):
    return "Rp" + f"{int(n):,}".replace(",", ".")


def tingkat(skor):
    for batas, nama in PERINGKAT:
        if skor >= batas:
            return nama
    return "RENDAH"


def jenis_bpjs(nama, kategori=None):
    """True bila risiko ini soal karyawan cedera/sakit/kecelakaan kerja (label BPJS)."""
    if kategori is not None:
        return kategori == "bpjs"
    return bool(_POLA_BPJS.search(nama)) and not _POLA_BUKAN.search(nama)


def respons(k, d, skor, kerugian=None, dana=None, asuransi_ada=True, bpjs=False):
    """Kembalikan (respons, perlu_asuransi). Aturan eksplisit, lihat SKILL.md."""
    if bpjs:
        return RESPONS_BPJS, LABEL_BPJS
    besar = d >= 4 or (kerugian is not None and dana is not None and kerugian > dana)
    if skor <= 4 and not besar:
        return "Terima (cukup dana cadangan)", "Tidak"
    if not asuransi_ada:
        return ("Kurangi + alihkan lewat kontrak/cadangan (orang, pemasok, kanal)",
                "Tidak ada asuransi umum; pakai mitigasi lain")
    if besar and k <= 3:
        return "Kurangi + alihkan (asuransi/kontrak)", "Ya, pertimbangkan"
    if besar:
        return "Kurangi dulu, lalu alihkan", "Ya, setelah dikurangi"
    if k >= 4:
        return "Kurangi (langkah murah)", "Tidak perlu"
    return "Kurangi + siapkan dana cadangan", "Tidak perlu"


def _bulat15(v, nama):
    if isinstance(v, bool) or not isinstance(v, int) or not 1 <= v <= 5:
        raise ValueError(f"{nama} harus bilangan bulat 1-5, diterima: {v!r}")
    return v


def hitung_risiko(daftar, dana=None):
    if not isinstance(daftar, list) or not daftar:
        raise ValueError("daftar risiko kosong atau bukan list")
    hasil = []
    for i, r in enumerate(daftar, 1):
        if not isinstance(r, dict) or not str(r.get("nama", "")).strip():
            raise ValueError(f"risiko ke-{i}: nama wajib diisi")
        k = _bulat15(r.get("kemungkinan"), f"{r['nama']}: kemungkinan")
        d = _bulat15(r.get("dampak"), f"{r['nama']}: dampak")
        kr = r.get("kerugian_rp")
        if kr is not None:
            if isinstance(kr, bool) or not isinstance(kr, int) or kr < 0:
                raise ValueError(f"{r['nama']}: kerugian_rp harus bilangan bulat >= 0")
        skor = k * d
        ada = r.get("bisa_diasuransikan", True)
        if not isinstance(ada, bool):
            raise ValueError(f"{r['nama']}: bisa_diasuransikan harus true atau false")
        kat = r.get("kategori")
        if kat is not None and kat not in KATEGORI_SAH:
            raise ValueError(f"{r['nama']}: kategori harus salah satu dari {', '.join(KATEGORI_SAH)}")
        nama = " ".join(str(r["nama"]).replace("|", "/").split())
        bpjs = jenis_bpjs(nama, kat)
        resp, asuransi = respons(k, d, skor, kr, dana, ada, bpjs)
        hasil.append({"nama": nama, "kemungkinan": k, "dampak": d,
                      "skor": skor, "tingkat": tingkat(skor), "respons": resp,
                      "perlu_asuransi": asuransi, "kerugian_rp": kr, "bpjs": bpjs})
    hasil.sort(key=lambda x: (-x["skor"], -x["dampak"], x["nama"]))
    return hasil


def hitung_dana(biaya, bulan, kas=None, cicil=None):
    if not biaya:
        raise ValueError("biaya tetap kosong")
    if isinstance(bulan, bool) or not isinstance(bulan, int) or not 1 <= bulan <= 24:
        raise ValueError("bulan target harus bilangan bulat 1-24")
    total = 0
    for nama, v in biaya.items():
        if isinstance(v, bool) or not isinstance(v, int) or v < 0:
            raise ValueError(f"biaya '{nama}' harus bilangan bulat >= 0")
        total += v
    target = total * bulan
    out = {"biaya_tetap_bulanan": total, "bulan": bulan, "target": target}
    if kas is not None:
        if isinstance(kas, bool) or not isinstance(kas, int) or kas < 0:
            raise ValueError("kas harus bilangan bulat >= 0")
        out["kas"] = kas
        out["kekurangan"] = max(0, target - kas)
        # bulat setengah-ke-atas ke 1 desimal, murni bilangan bulat (tanpa float)
        out["tercukupi_bulan"] = ((kas * 20 + total) // (2 * total)) / 10 if total else None
        if cicil is not None:
            if isinstance(cicil, bool) or not isinstance(cicil, int) or not 1 <= cicil <= 120:
                raise ValueError("jumlah bulan cicilan harus bilangan bulat 1-120")
            out["cicil_bulan"] = cicil
            out["cicilan"] = -(-out["kekurangan"] // cicil)  # dibulatkan ke atas
    elif cicil is not None:
        raise ValueError("--cicil perlu --kas (kas cadangan saat ini)")
    return out


def parse_angka(teks, nama="angka"):
    """Angka rupiah bulat: 3000000 atau 3.000.000 (titik = ribuan). Desimal/ambigu ditolak."""
    t = str(teks).strip()
    if t[:2].lower() == "rp":
        t = t[2:].strip()
    if re.fullmatch(r"\d+", t):
        return int(t)
    if re.fullmatch(r"\d{1,3}(\.\d{3})+", t):
        return int(t.replace(".", ""))
    raise ValueError(f"angka {nama} '{teks}' tidak jelas. Tulis angka bulat tanpa desimal, "
                     "mis. 3000000 atau 3.000.000")


def parse_biaya(teks):
    biaya = {}
    for bagian in teks.split(","):
        if not bagian.strip():
            continue
        if re.fullmatch(r"\s*\d+\s*", bagian):
            raise ValueError(f"'{bagian.strip()}' berdiri sendiri. Koma memisahkan antar biaya, jadi "
                             "jangan pakai koma/desimal di angka: tulis 3000000 atau 3.000.000")
        if "=" not in bagian:
            raise ValueError(f"format biaya salah: '{bagian.strip()}' (pakai Nama=Angka)")
        n, v = bagian.rsplit("=", 1)
        n = n.strip()
        if not n:
            raise ValueError(f"nama biaya kosong di '{bagian.strip()}'. Tulis Nama=Angka, mis. Sewa=3000000")
        if n.lower() in {k.lower() for k in biaya}:
            raise ValueError(f"nama biaya '{n}' dobel. Jumlahkan dulu jadi satu angka "
                             "atau beri nama berbeda (mis. Gaji kasir, Gaji koki)")
        biaya[n] = parse_angka(v, f"biaya '{n}'")
    return biaya


def kata_cukup(o):
    if o.get("tercukupi_bulan") is None:
        return "(biaya tetap Rp0, lama cukup tidak dihitung)"
    return "(cukup " + str(o["tercukupi_bulan"]).replace(".", ",") + " bulan biaya tetap)"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("risiko")
    a.add_argument("berkas")
    a.add_argument("--dana", type=str, help="dana darurat (Rp) untuk pembanding kerugian_rp")
    b = sub.add_parser("dana")
    b.add_argument("--biaya", required=True)
    b.add_argument("--bulan", type=str, default="3")
    b.add_argument("--kas", type=str)
    b.add_argument("--cicil", type=str, help="cicil kekurangan selama N bulan")
    args = p.parse_args(argv)
    try:
        if args.cmd == "risiko":
            try:
                with open(args.berkas, encoding="utf-8-sig") as f:
                    data = json.load(f)
            except (OSError, json.JSONDecodeError) as e:
                raise ValueError(f"berkas tidak bisa dibaca: {e}")
            dana = parse_angka(args.dana, "--dana") if args.dana else None
            h = hitung_risiko(data, dana)
            print("| No | Risiko | K | D | Skor | Tingkat | Respons | Perlu asuransi? |")
            print("|---|---|---|---|---|---|---|---|")
            for i, r in enumerate(h, 1):
                print(f"| {i} | {r['nama']} | {r['kemungkinan']} | {r['dampak']} | {r['skor']} | "
                      f"{r['tingkat']} | {r['respons']} | {r['perlu_asuransi']} |")
        else:
            o = hitung_dana(parse_biaya(args.biaya), parse_angka(args.bulan, "--bulan"),
                            parse_angka(args.kas, "--kas") if args.kas else None,
                            parse_angka(args.cicil, "--cicil") if args.cicil else None)
            print(f"Biaya tetap per bulan: {rp(o['biaya_tetap_bulanan'])}")
            print(f"Target dana darurat ({o['bulan']} bulan): {rp(o['target'])}")
            if "kas" in o:
                print(f"Kas cadangan saat ini: {rp(o['kas'])} {kata_cukup(o)}")
                print(f"Kekurangan: {rp(o['kekurangan'])}")
                if o.get("cicil_bulan") and o["kekurangan"] == 0:
                    print("Kas sudah mencukupi target; tidak perlu cicilan menabung.")
                elif "cicilan" in o:
                    print(f"Cicilan menabung: {rp(o['cicilan'])} per bulan selama {o['cicil_bulan']} bulan")
    except ValueError as e:
        print(f"Input tidak valid: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
