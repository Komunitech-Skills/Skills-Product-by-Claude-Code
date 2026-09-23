#!/usr/bin/env python3
"""Buat kerangka kalender konten (default 30 hari) dengan tanggal, hari, momen lokal, pilar, dan
platform yang sudah benar. Kolom ide/hook/CTA dikosongkan untuk diisi AI agent.

Yang dilakukan script (supaya tanggal & rotasi tidak salah):
- Nama hari dalam Bahasa Indonesia untuk setiap tanggal.
- Menandai momen tanggal tetap (HUT RI, Hari Batik, Sumpah Pemuda, Hari Ibu, dll.), tanggal kembar
  (1.1 s.d. 12.12; 12.12 = Harbolnas), hari gajian, dan "tanggal tua".
- Momen yang tanggalnya berubah tiap tahun (Ramadan, Lebaran, Imlek, Idul Adha) TIDAK ditebak:
  masukkan lewat --momen "YYYY-MM-DD:Nama".
- Rotasi pilar konten; hari promo (tanggal kembar, gajian, momen bertipe promo) dipaksa ke pilar promo,
  hari peringatan (mis. 30 Sep, 1 Okt, 10 Nov) tidak pernah diberi pilar promo.

Hanya library standar Python 3.8+. Contoh:
  python3 buat_kalender.py --mulai 2026-10-01 --pilar "Edukasi,Promo,Di Balik Layar,Testimoni,Hiburan" \
      --platform "IG,TikTok,WA Status" --momen "2026-10-17:Ulang tahun toko ke-3" --format csv --pemisah ";"
"""
import argparse
import csv
import io
import json
import sys
from datetime import date, datetime, timedelta

# Windows: pastikan teks Indonesia/emoji tercetak tanpa error encoding
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HARI = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
BULAN = ["", "Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

# (bulan, tanggal): (nama, tipe). tipe: promo | tema | peringatan
MOMEN_TETAP = {
    (1, 1): ("Tahun Baru", "tema"),
    (2, 14): ("Hari Valentine", "tema"),
    (3, 8): ("Hari Perempuan Internasional", "tema"),
    (4, 21): ("Hari Kartini", "tema"),
    (5, 1): ("Hari Buruh", "tema"),
    (5, 2): ("Hari Pendidikan Nasional", "tema"),
    (6, 1): ("Hari Lahir Pancasila", "tema"),
    (7, 23): ("Hari Anak Nasional", "tema"),
    (8, 17): ("HUT Kemerdekaan RI", "tema"),
    (9, 4): ("Hari Pelanggan Nasional", "tema"),
    (9, 30): ("Peringatan G30S", "peringatan"),
    (10, 1): ("Hari Kesaktian Pancasila", "peringatan"),
    (10, 2): ("Hari Batik Nasional", "tema"),
    (10, 22): ("Hari Santri", "tema"),
    (10, 28): ("Hari Sumpah Pemuda", "tema"),
    (11, 10): ("Hari Pahlawan", "peringatan"),
    (11, 25): ("Hari Guru Nasional", "tema"),
    (12, 22): ("Hari Ibu", "tema"),
    (12, 25): ("Hari Natal", "tema"),
    (12, 31): ("Malam Tahun Baru", "tema"),
}
FORMAT_PILAR = [
    ("promo", "Video pendek + Story/Status"),
    ("jual", "Video pendek + Story/Status"),
    ("edukasi", "Carousel / video tips"),
    ("tips", "Carousel / video tips"),
    ("testimoni", "Foto ulasan / Story"),
    ("bukti", "Foto ulasan / Story"),
    ("balik", "Video pendek proses"),
    ("proses", "Video pendek proses"),
    ("ulasan", "Foto ulasan / Story"),
    ("review", "Foto ulasan / Story"),
    ("resep", "Carousel / video tips"),
    ("koleksi", "Foto/video produk"),
    ("ootd", "Video try-on / mix-match"),
    ("bts", "Video pendek proses"),
    ("hiburan", "Video tren / polling"),
    ("interaksi", "Polling / kuis Story"),
]
KOLOM = ["No", "Tanggal", "Hari", "Momen", "Pilar", "Platform", "Format", "Ide Konten", "Hook / Judul",
         "CTA", "Status"]


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def parse_tanggal(teks, nama="Tanggal"):
    t = teks.strip()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%Y/%m/%d"):
        try:
            return datetime.strptime(t, fmt).date()
        except ValueError:
            pass
    galat("{} '{}' tidak dikenali. Pakai format YYYY-MM-DD, mis. 2026-10-01.".format(nama, teks))


def fmt_tgl(d):
    return "{:02d} {} {}".format(d.day, BULAN[d.month], d.year)


def default_mulai(hari_ini):
    return date(hari_ini.year + (hari_ini.month == 12), hari_ini.month % 12 + 1, 1)


def format_untuk(pilar):
    p = pilar.lower()
    for kunci, fmt in FORMAT_PILAR:
        if kunci in p:
            return fmt
    return "Bebas (sesuaikan ide)"


def momen_hari(d, gajian, momen_user):
    """Kembalikan list (nama, tipe) untuk tanggal d."""
    daftar = []
    for nama, tipe in momen_user.get(d, []):
        daftar.append((nama, tipe))
    if (d.month, d.day) in MOMEN_TETAP:
        daftar.append(MOMEN_TETAP[(d.month, d.day)])
    if d.day == d.month:
        if d.month == 12:
            daftar.append(("Harbolnas 12.12 (cek jadwal resmi)", "promo"))
        elif d.month >= 9:
            daftar.append(("Tanggal kembar {0}.{0} — musim promo akhir tahun (cek kampanye marketplace)".format(d.month), "promo"))
        else:
            daftar.append(("Tanggal kembar {0}.{0} (cek kampanye marketplace)".format(d.month), "promo"))
    akhir_bulan = (d + timedelta(days=1)).month != d.month
    for g in gajian:
        if d.day == g or (akhir_bulan and g > d.day):
            daftar.append(("Hari gajian (tgl {})".format(g if g <= d.day else "akhir bulan"), "promo"))
            break
    if not daftar and 20 <= d.day <= 24 and 25 in gajian:
        daftar.append(("Tanggal tua — konten hemat/nilai", "tema"))
    return daftar


def susun(mulai, jumlah, pilar, platform, gajian, momen_user):
    idx_promo = next((i for i, p in enumerate(pilar) if "promo" in p.lower() or "jual" in p.lower()), None)
    hari = [mulai + timedelta(days=i) for i in range(jumlah)]
    info = [momen_hari(d, gajian, momen_user) for d in hari]
    paksa_promo = [any(t == "promo" for _, t in m) for m in info]
    larang_promo = [any(t == "peringatan" for _, t in m) for m in info]

    baris, putar = [], 0
    for i, d in enumerate(hari):
        if paksa_promo[i] and not larang_promo[i] and idx_promo is not None:
            p = pilar[idx_promo]
        else:
            p = None
            for _ in range(len(pilar)):
                kandidat = pilar[putar % len(pilar)]
                putar += 1
                dekat_promo = any(paksa_promo[j] for j in (i - 1, i + 1) if 0 <= j < len(hari))
                if idx_promo is not None and kandidat == pilar[idx_promo] and (larang_promo[i] or dekat_promo):
                    continue
                p = kandidat
                break
            if p is None:
                p = pilar[0] if not (idx_promo == 0 and larang_promo[i]) else pilar[-1]
        catatan = "; ".join(n for n, _ in info[i])
        if larang_promo[i]:
            catatan += " — hari peringatan: konten penghormatan, hindari hard-selling"
        baris.append({
            "No": i + 1, "Tanggal": d.isoformat(), "Tanggal_tampil": fmt_tgl(d), "Hari": HARI[d.weekday()],
            "Momen": catatan, "Pilar": p, "Platform": " + ".join(platform), "Format": format_untuk(p),
            "Ide Konten": "", "Hook / Judul": "", "CTA": "", "Status": "Belum",
        })
    return baris


def baca_isi(path):
    """Baca baris kalender yang sudah diisi. Hari dihitung ulang dari tanggal agar tidak salah."""
    try:
        with open(path, encoding="utf-8-sig") as f:
            data = json.load(f)
    except FileNotFoundError:
        galat("File tidak ditemukan: {}".format(path))
    except (ValueError, UnicodeDecodeError) as e:
        galat("File {} bukan JSON yang valid: {}".format(path, e))
    baris = data.get("baris") if isinstance(data, dict) else data
    if not isinstance(baris, list) or not baris:
        galat("JSON harus berisi daftar baris (kunci \"baris\") yang tidak kosong.")
    hasil = []
    for i, b in enumerate(baris, start=1):
        if not isinstance(b, dict) or not b.get("Tanggal"):
            galat("Baris ke-{} tidak punya kolom 'Tanggal'.".format(i))
        d = parse_tanggal(str(b["Tanggal"]), "Tanggal baris ke-{}".format(i))
        r = {k: ("" if b.get(k) is None else str(b.get(k))) for k in KOLOM}
        r["No"] = i
        r["Tanggal"] = d.isoformat()
        r["Tanggal_tampil"] = fmt_tgl(d)
        r["Hari"] = HARI[d.weekday()]
        r["Pilar"] = r["Pilar"] or "-"
        r["Status"] = r["Status"] or "Belum"
        hasil.append(r)
    kosong = [str(r["No"]) for r in hasil if not r["Ide Konten"].strip()]
    if kosong:
        print("PERINGATAN: kolom 'Ide Konten' masih kosong di baris: " + ", ".join(kosong), file=sys.stderr)
    return hasil


def main():
    p = argparse.ArgumentParser(description="Kerangka kalender konten dengan momen lokal Indonesia.")
    p.add_argument("--mulai", help="tanggal mulai YYYY-MM-DD (default: tanggal 1 bulan depan)")
    p.add_argument("--hari", type=int, default=30, help="jumlah hari (7–92), default 30")
    p.add_argument("--pilar", default="Edukasi,Promo,Di Balik Layar,Testimoni,Hiburan",
                   help="pilar konten dipisah koma (2–7)")
    p.add_argument("--platform", default="IG,TikTok,WA Status", help="platform dipisah koma")
    p.add_argument("--gajian", default="25,1", help="tanggal gajian pelanggan dipisah koma, default 25,1")
    p.add_argument("--momen", action="append", default=[],
                   help="momen tambahan \"YYYY-MM-DD:Nama\" atau \"YYYY-MM-DD:Nama:promo|tema|peringatan\". Boleh diulang")
    p.add_argument("--tanpa-momen-nasional", action="store_true", help="jangan tandai momen tanggal tetap")
    p.add_argument("--format", choices=["md", "csv", "json"], default="md")
    p.add_argument("--pemisah", default=",", help="pemisah CSV: ',' (Google Sheets) atau ';' (Excel Indonesia)")
    p.add_argument("--output", help="simpan ke file ini (default: tampil di layar)")
    p.add_argument("--isi", help="file JSON berisi baris yang SUDAH diisi ide (hasil --format json yang dilengkapi); "
                                 "script hanya memeriksa & mengekspor ke md/csv")
    p.add_argument("--hari-ini", help=argparse.SUPPRESS)
    a = p.parse_args()

    if not 7 <= a.hari <= 92:
        galat("--hari harus antara 7 dan 92.")
    hari_ini = parse_tanggal(a.hari_ini, "--hari-ini") if a.hari_ini else date.today()
    mulai = parse_tanggal(a.mulai, "--mulai") if a.mulai else default_mulai(hari_ini)
    pilar = [x.strip() for x in a.pilar.split(",") if x.strip()]
    if not 2 <= len(pilar) <= 7:
        galat("Isi 2 sampai 7 pilar konten, dipisah koma.")
    if len(set(x.lower() for x in pilar)) != len(pilar):
        galat("Ada nama pilar yang sama. Pakai nama pilar yang berbeda.")
    platform = [x.strip() for x in a.platform.split(",") if x.strip()]
    if not platform:
        galat("Isi minimal 1 platform.")
    try:
        gajian = sorted({int(x) for x in a.gajian.split(",") if x.strip()})
    except ValueError:
        galat("--gajian harus berisi angka tanggal, mis. 25 atau 25,1.")
    if any(not 1 <= g <= 31 for g in gajian):
        galat("Tanggal gajian harus 1–31.")
    if a.pemisah not in (",", ";", "\\t", "\t"):
        galat("--pemisah hanya boleh ',' atau ';' (atau \\t).")
    pemisah = "\t" if a.pemisah in ("\\t", "\t") else a.pemisah

    momen_user = {}
    for m in a.momen:
        bagian = m.split(":")
        if len(bagian) < 2 or not bagian[1].strip():
            galat("Format --momen harus \"YYYY-MM-DD:Nama\" (dapat: '{}').".format(m))
        tipe = "tema"
        if len(bagian) >= 3 and bagian[-1].strip().lower() in ("promo", "tema", "peringatan"):
            tipe = bagian[-1].strip().lower()
            nama = ":".join(bagian[1:-1]).strip()
        else:
            nama = ":".join(bagian[1:]).strip()
        d = parse_tanggal(bagian[0], "Tanggal momen")
        momen_user.setdefault(d, []).append((nama, tipe))

    global MOMEN_TETAP
    if a.tanpa_momen_nasional:
        MOMEN_TETAP = {}
    if a.isi:
        baris = baca_isi(a.isi)
        mulai = parse_tanggal(baris[0]["Tanggal"])
        akhir = parse_tanggal(baris[-1]["Tanggal"])
        a.hari = len(baris)
        pilar = list(dict.fromkeys(b["Pilar"] for b in baris))
    else:
        baris = susun(mulai, a.hari, pilar, platform, gajian, momen_user)
        akhir = mulai + timedelta(days=a.hari - 1)
    di_luar = sorted(d.isoformat() for d in momen_user if not mulai <= d <= akhir)

    hitung = {}
    for b in baris:
        hitung[b["Pilar"]] = hitung.get(b["Pilar"], 0) + 1
    ringkasan = {"mulai": mulai.isoformat(), "selesai": akhir.isoformat(), "jumlah_hari": a.hari,
                 "sebaran_pilar": hitung, "momen_di_luar_rentang": di_luar, "peringatan": []}
    idx_promo = next((x for x in pilar if "promo" in x.lower() or "jual" in x.lower()), None)
    if idx_promo and hitung.get(idx_promo, 0) > 0.4 * a.hari:
        ringkasan["peringatan"].append(
            "Pilar {} mengisi {} dari {} hari (>40%). Audiens mudah bosan; pertimbangkan menambah pilar non-promo.".format(
                idx_promo, hitung[idx_promo], a.hari))

    if a.format == "json":
        teks = json.dumps({"ringkasan": ringkasan, "baris": baris}, ensure_ascii=False, indent=2)
    elif a.format == "csv":
        buf = io.StringIO()
        w = csv.writer(buf, delimiter=pemisah, lineterminator="\n")
        w.writerow(KOLOM)
        for b in baris:
            w.writerow([b["No"], b["Tanggal"]] + [b[k] for k in KOLOM[2:]])
        teks = buf.getvalue()
    else:
        out = ["Kalender konten {} s.d. {} ({} hari)".format(fmt_tgl(mulai), fmt_tgl(akhir), a.hari), "",
               "| " + " | ".join(KOLOM) + " |", "|" + "---|" * len(KOLOM)]
        for b in baris:
            sel = [str(b["No"]), b["Tanggal_tampil"]] + [str(b[k]).replace("|", "/").replace("\n", " ") for k in KOLOM[2:]]
            out.append("| " + " | ".join(sel) + " |")
        out.append("")
        out.append("Sebaran pilar: " + ", ".join("{} {}".format(k, v) for k, v in hitung.items()))
        if di_luar:
            out.append("Momen di luar rentang (diabaikan): " + ", ".join(di_luar))
        for w in ringkasan["peringatan"]:
            out.append("PERINGATAN: " + w)
        teks = "\n".join(out) + "\n"

    if a.output:
        try:
            # utf-8-sig agar Excel membaca huruf/emoji dengan benar
            with open(a.output, "w", encoding="utf-8-sig" if a.format == "csv" else "utf-8", newline="") as f:
                f.write(teks)
        except OSError as e:
            galat("Gagal menyimpan ke {}: {}".format(a.output, e))
        print("Tersimpan: {}".format(a.output))
        print(json.dumps(ringkasan, ensure_ascii=False))
    else:
        sys.stdout.write(teks)
        if a.format == "csv":
            print(json.dumps(ringkasan, ensure_ascii=False), file=sys.stderr)


if __name__ == "__main__":
    main()
