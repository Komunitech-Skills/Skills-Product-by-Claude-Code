#!/usr/bin/env python3
"""Hitung skor risiko usaha dan dana darurat. Python standar saja.

Pakai (Windows: python / py):
  python3 scripts/cek_risiko.py risiko berkas.json
  python3 scripts/cek_risiko.py dana --biaya "Sewa=3000000,Gaji=8000000" --bulan 3 [--kas 5000000]

berkas.json: [{"nama": "Kebakaran", "kemungkinan": 2, "dampak": 5, "kerugian_rp": 80000000}, ...]
kemungkinan dan dampak: bilangan bulat 1-5. kerugian_rp opsional.
"""
import argparse
import json
import sys

PERINGKAT = [(15, "KRITIS"), (10, "TINGGI"), (5, "SEDANG"), (1, "RENDAH")]


def rp(n):
    return "Rp" + f"{int(n):,}".replace(",", ".")


def tingkat(skor):
    for batas, nama in PERINGKAT:
        if skor >= batas:
            return nama
    return "RENDAH"


def respons(k, d, skor, kerugian=None, dana=None):
    """Kembalikan (respons, perlu_asuransi). Aturan eksplisit, lihat SKILL.md."""
    if skor <= 4:
        return "Terima (cukup dana cadangan)", "Tidak"
    besar = d >= 4 or (kerugian is not None and dana is not None and kerugian > dana)
    if besar and k <= 3:
        return "Kurangi + alihkan (asuransi/kontrak)", "Ya, pertimbangkan"
    if besar and k >= 4:
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
        resp, asuransi = respons(k, d, skor, kr, dana)
        hasil.append({"nama": str(r["nama"]).strip(), "kemungkinan": k, "dampak": d,
                      "skor": skor, "tingkat": tingkat(skor), "respons": resp,
                      "perlu_asuransi": asuransi, "kerugian_rp": kr})
    hasil.sort(key=lambda x: (-x["skor"], -x["dampak"], x["nama"]))
    return hasil


def hitung_dana(biaya, bulan, kas=None):
    if not biaya:
        raise ValueError("biaya tetap kosong")
    if isinstance(bulan, bool) or not isinstance(bulan, int) or not 1 <= bulan <= 24:
        raise ValueError("bulan harus bilangan bulat 1-24")
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
        out["tercukupi_bulan"] = round(kas / total, 1) if total else None
    return out


def parse_biaya(teks):
    biaya = {}
    for bagian in teks.split(","):
        if not bagian.strip():
            continue
        if "=" not in bagian:
            raise ValueError(f"format biaya salah: '{bagian}' (pakai Nama=Angka)")
        n, v = bagian.rsplit("=", 1)
        v = v.strip().replace(".", "")
        if not v.isdigit():
            raise ValueError(f"angka biaya '{n.strip()}' tidak valid: '{v}'")
        biaya[n.strip()] = int(v)
    return biaya


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("risiko")
    a.add_argument("berkas")
    a.add_argument("--dana", type=int, help="dana darurat (Rp) untuk pembanding kerugian_rp")
    b = sub.add_parser("dana")
    b.add_argument("--biaya", required=True)
    b.add_argument("--bulan", type=int, default=3)
    b.add_argument("--kas", type=int)
    args = p.parse_args(argv)
    try:
        if args.cmd == "risiko":
            try:
                with open(args.berkas, encoding="utf-8") as f:
                    data = json.load(f)
            except (OSError, json.JSONDecodeError) as e:
                raise ValueError(f"berkas tidak bisa dibaca: {e}")
            h = hitung_risiko(data, args.dana)
            print("| No | Risiko | K | D | Skor | Tingkat | Respons | Perlu asuransi? |")
            print("|---|---|---|---|---|---|---|---|")
            for i, r in enumerate(h, 1):
                print(f"| {i} | {r['nama']} | {r['kemungkinan']} | {r['dampak']} | {r['skor']} | "
                      f"{r['tingkat']} | {r['respons']} | {r['perlu_asuransi']} |")
        else:
            o = hitung_dana(parse_biaya(args.biaya), args.bulan, args.kas)
            print(f"Biaya tetap per bulan: {rp(o['biaya_tetap_bulanan'])}")
            print(f"Target dana darurat ({o['bulan']} bulan): {rp(o['target'])}")
            if "kas" in o:
                print(f"Kas cadangan saat ini: {rp(o['kas'])} (cukup {o['tercukupi_bulan']} bulan)")
                print(f"Kekurangan: {rp(o['kekurangan'])}")
    except ValueError as e:
        print(f"Input tidak valid: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
