#!/usr/bin/env python3
"""Pra-saring CV pelamar: skor per kriteria (kata kunci + lama pengalaman) lalu ranking.

Pemakaian:
  python3 scripts/nilai_cv.py kriteria.json folder_cv/            (Windows: python / py)
  python3 scripts/nilai_cv.py kriteria.json cv.csv --top 5 --format ringkas|json|csv

Sumber CV: folder berisi .txt/.md (satu berkas satu CV) ATAU CSV berkolom id/nama/kode + teks/cv/isi.
Hanya Python standar. Tidak memakai jaringan, tidak menulis berkas, tidak mengubah masukan.
Hasil adalah PRA-SARING kata kunci. Agent wajib membaca CV sendiri untuk bukti kutipan.
Usia, jenis kelamin, agama, suku, status kawin, foto/penampilan TIDAK dibaca dan tidak boleh jadi kriteria.
NIK, alamat, HP, email disamarkan di cuplikan.
"""
import argparse
import csv
import io
import json
import re
import sys
from datetime import date
from pathlib import Path

MAKS_CV = 500
MAKS_BYTE = 200_000
BOBOT_WAJIB, BOBOT_TAMBAH = 0.75, 0.25

# Kriteria yang tidak boleh dipakai (UU 13/2003 Pasal 5-6; SE Menaker M/6/HK.04/V/2025).
LARANGAN = [
    r"\busia\b", r"\bumur\b", r"\bkelahiran\b", r"tahun lahir", r"tanggal lahir", r"\bmuda\b", r"\bfresh\s*graduate\b.*\bmaks",
    r"laki[- ]?laki", r"\bpria\b", r"perempuan", r"wanita", r"\bgender\b", r"jenis kelamin", r"\bagama\b", r"\bislam\b",
    r"\bmuslim", r"kristen", r"katolik", r"\bhindu\b", r"\bbuddha\b", r"jilbab", r"hijab", r"berkerudung", r"\bsuku\b", r"\bras\b",
    r"menikah", r"lajang", r"status pernikahan", r"status kawin", r"hamil", r"tinggi badan", r"berat badan", r"\bbmi\b",
    r"penampilan menarik", r"berpenampilan", r"good ?looking", r"\bpas ?foto\b", r"foto diri", r"warna kulit", r"disabilitas",
    r"domisili\s+(?:asli|asal)", r"putra daerah",
]
BULAN = r"(?:jan|feb|mar|apr|mei|may|jun|jul|agu|aug|sep|okt|oct|nov|des|dec)[a-z]*\.?"
AKHIR = r"(?:sekarang|saat ini|present|now|current|kini|sekarang ini)"
RENTANG = re.compile(
    r"(?:" + BULAN + r"[\s/,]+)?(?<!\d)((?:19|20)\d{2})\s*(?:-|–|—|s/d|s\.d\.?|sd|sampai|to|hingga|until)\s*"
    r"(?:" + BULAN + r"[\s/,]+)?((?:19|20)\d{2}|" + AKHIR + r")(?!\d)", re.I)
LAMA = re.compile(r"(?<![\d.,])(\d{1,2}(?:[.,]\d)?)\s*\+?\s*(tahun|thn|th|years?|yrs?|bulan|months?)\b", re.I)
LAMA_ABAIKAN = re.compile(r"(usia|umur|age|berumur|lahir)\W{0,12}$", re.I)
EDU = re.compile(r"\b(sma|smk|smp|stm|s1|s2|s3|d1|d2|d3|d4|universitas|institut|politeknik|sekolah|ipk|gpa|lulus|kuliah|akademi|mahasiswa)\b", re.I)
HEAD_EDU = re.compile(r"^\W*(pendidikan|education|riwayat pendidikan)\W*$", re.I)
HEAD_KERJA = re.compile(r"^\W*(pengalaman(?: kerja)?|riwayat (?:pekerjaan|kerja)|work experience|experience|employment)\W*$", re.I)
HEAD_LAIN = re.compile(r"^\W*(keahlian|skills?|kemampuan|kursus|pelatihan|sertifikat\w*|organisasi|data pribadi|profil|ringkasan|summary|referensi|prestasi|bahasa|tentang saya|curriculum vitae)\W*$", re.I)
PRIBADI = re.compile(r"(lahir|usia|umur|agama|jenis kelamin|gender|status\s*:|status pernikahan|menikah|alamat|domisili|tinggi|berat|nik\b|ktp|jl\.|jalan\s|kode pos|\bhp\b|telp|email|e-mail|whatsapp|\bwa\b\s*:)", re.I)
PRIBADI_LABEL = re.compile(r"^\W*(alamat|agama|status|jenis kelamin|gender|tempat|tanggal lahir|usia|umur|nik|no\.? ?hp|hp|email|e-mail|telp\w*)\b\s*[:/]", re.I)
SENSITIF = re.compile(r"(tinggi badan|berat badan|usia|umur|lahir|agama|menikah|lajang|status\s*(?:pernikahan|kawin|:)|hamil|suami|istri|berusia|\bsaya\s+\d{2}\s*(?:tahun|th)\b)", re.I)
KURSUS = re.compile(r"\b(kursus|pelatihan|training|bootcamp|workshop|webinar|seminar|sertifikasi|sertifikat|course|diklat)\b", re.I)
INJEKSI = re.compile(r"(abaikan|ignore (all|previous|the)|loloskan saya|beri (saya )?(nilai|skor)|skor\s*100|nilai\s*100|system prompt|instruksi (untuk )?(ai|penilai)|jangan nilai)", re.I)


class Galat(Exception):
    pass


def samarkan(s):
    s = re.sub(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", "[email]", s)
    s = re.sub(r"(?:\+?62|0)\s*8[\d\s().-]{7,14}\d", "[hp]", s)
    s = re.sub(r"\d[\d\s.-]{10,}\d", "[angka]", s)
    return s


def periksa_kriteria(k):
    if not isinstance(k, dict):
        raise Galat("Berkas kriteria harus berupa objek JSON.")
    wajib, tambah = k.get("wajib", []), k.get("nilai_tambah", [])
    if not isinstance(wajib, list) or not wajib:
        raise Galat("Kriteria 'wajib' kosong. Isi minimal satu kriteria wajib.")
    if not isinstance(tambah, list):
        raise Galat("'nilai_tambah' harus berupa daftar.")
    hasil = {"posisi": str(k.get("posisi", "")), "wajib": [], "nilai_tambah": []}
    for bagian in ("wajib", "nilai_tambah"):
        for i, c in enumerate(k.get(bagian, []), 1):
            if not isinstance(c, dict) or not c.get("nama") or not c.get("kata"):
                raise Galat(f"Kriteria {bagian} no. {i} harus punya 'nama' dan daftar 'kata'.")
            kata = [str(x).strip().lower() for x in c["kata"] if str(x).strip()]
            if not kata:
                raise Galat(f"Kriteria '{c['nama']}' tidak punya kata kunci.")
            teks = " ".join([str(c["nama"])] + kata).lower()
            for pola in LARANGAN:
                if re.search(pola, teks):
                    raise Galat(f"Kriteria '{c['nama']}' menyangkut hal yang tidak boleh dinilai (usia, jenis kelamin, agama, suku, "
                                "status kawin, penampilan, dan sejenisnya; UU 13/2003 Pasal 5-6). Ganti dengan kemampuan kerja.")
            try:
                bobot = float(c.get("bobot", 1))
                tahun = float(c.get("min_tahun", 0))
            except (TypeError, ValueError):
                raise Galat(f"'bobot'/'min_tahun' pada '{c['nama']}' harus angka.")
            if bobot <= 0 or tahun < 0:
                raise Galat(f"'bobot' harus > 0 dan 'min_tahun' >= 0 pada '{c['nama']}'.")
            hasil[bagian].append({"nama": str(c["nama"]), "kata": kata, "bobot": bobot, "min_tahun": tahun,
                                  "gugur": bool(c.get("gugur_bila_tidak_ada", False)) and bagian == "wajib",
                                  "pendidikan": bool(c.get("termasuk_pendidikan", False))})
    return hasil


def baca_teks(path):
    mentah = Path(path).read_bytes()[:MAKS_BYTE]
    if b"\x00" in mentah[:4096]:
        raise Galat(f"{Path(path).name}: bukan teks (mungkin PDF/DOCX/gambar). Ubah ke teks dulu.")
    return mentah.decode("utf-8", errors="replace")


def muat_cv(sumber):
    p = Path(sumber)
    cvs = []
    if p.is_dir():
        berkas = sorted(x for x in p.iterdir() if x.is_file() and x.suffix.lower() in (".txt", ".md"))
        if not berkas:
            raise Galat("Folder tidak berisi .txt/.md. PDF/DOCX harus diubah ke teks dulu.")
        for x in berkas[:MAKS_CV]:
            try:
                cvs.append((x.name, baca_teks(x)))
            except Galat as e:
                cvs.append((x.name, ""))
                print(f"Peringatan: {e}", file=sys.stderr)
    elif p.is_file():
        teks = baca_teks(p) if p.suffix.lower() != ".csv" else p.read_bytes()[:MAKS_BYTE * 20].decode("utf-8-sig", errors="replace")
        if p.suffix.lower() != ".csv":
            cvs.append((p.name, teks))
        else:
            baris = list(csv.DictReader(io.StringIO(teks)))
            if not baris:
                raise Galat("CSV kosong.")
            kol = {k.strip().lower(): k for k in baris[0].keys() if k}
            kt = next((kol[a] for a in ("teks", "cv", "isi", "text", "resume") if a in kol), None)
            ki = next((kol[a] for a in ("id", "nama", "kode", "berkas", "no") if a in kol), None)
            if not kt:
                raise Galat("CSV butuh kolom teks CV bernama teks/cv/isi.")
            for n, r in enumerate(baris[:MAKS_CV], 1):
                cvs.append(((r.get(ki) or f"baris-{n}") if ki else f"baris-{n}", r.get(kt) or ""))
    else:
        raise Galat(f"Sumber CV tidak ditemukan: {sumber}")
    if not cvs:
        raise Galat("Tidak ada CV yang bisa dibaca.")
    return cvs


def pisah_blok(teks):
    """Pisahkan CV: blok kerja (baris + rentang tahun), baris lain, dan baris pendidikan."""
    mode = None
    ada_kepala = False
    blok, lain, edu = [], [], []
    kursus_aktif = False
    for baris in teks.splitlines():
        s = baris.strip()
        if not s:
            continue
        if len(s) < 40 and HEAD_EDU.match(s):
            mode, ada_kepala = "edu", True
            continue
        if len(s) < 40 and HEAD_KERJA.match(s):
            mode, ada_kepala = "kerja", True
            continue
        if len(s) < 40 and HEAD_LAIN.match(s):
            mode, ada_kepala = "lain", True
            continue
        pribadi = PRIBADI_LABEL.match(s) if mode == "kerja" else (PRIBADI.search(s) and not RENTANG.search(s))
        if mode == "edu" or (mode is None and EDU.search(s) and not blok):
            edu.append(s)
            continue
        if mode == "lain" or pribadi:
            lain.append(s)
            continue
        m = RENTANG.search(s)
        if m and KURSUS.search(s):  # baris kursus/pelatihan bukan pengalaman kerja
            kursus_aktif = True
            lain.append(s)
            continue
        if m:
            kursus_aktif = False
        elif kursus_aktif:
            lain.append(s)
            continue
        if m and not (mode is None and EDU.search(s)):
            a = int(m.group(1))
            b = m.group(2).lower()
            b = date.today().year if re.fullmatch(AKHIR, b, re.I) else int(b)
            blok.append({"baris": [s], "a": a, "b": b})
        elif blok:
            sisa = re.sub(BULAN, "", RENTANG.sub("", blok[-1]["baris"][0]), flags=re.I)
            if len(blok[-1]["baris"]) == 1 and KURSUS.search(s) and not re.search(r"[A-Za-z]{3}", sisa):
                # rentang tahun di baris sendiri, judul di baris berikut berisi kata kursus: bukan pengalaman kerja
                lain.extend(blok.pop()["baris"] + [s])
                kursus_aktif = True
            else:
                blok[-1]["baris"].append(s)
        else:
            lain.append(s)
    return blok, lain, edu


def gabung_tahun(rentang):
    rentang = sorted((a, b) for a, b in rentang if b >= a)
    total, akhir = 0.0, None
    for a, b in rentang:
        panjang = max(b - a, 0.5)
        if akhir is None or a >= akhir:
            total += panjang
            akhir = max(b, a)
        elif b > akhir:
            total += b - akhir
            akhir = b
    return total


def kalimat(baris):
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+|;\s*", baris) if x.strip()]


def lama_tertulis(s):
    maks = 0.0
    for m in LAMA.finditer(s):
        if LAMA_ABAIKAN.search(s[:m.start()][-14:]):
            continue
        n = float(m.group(1).replace(",", "."))
        if n > 40:
            continue
        if m.group(2).lower().startswith(("bulan", "month")):
            n /= 12
        maks = max(maks, n)
    return maks


def cocok(kata, teks):
    return any(re.search(r"(?<!\w)" + re.escape(k) + r"(?!\w)", teks) for k in kata)


def baris_bukti(kata, baris_list):
    for b in baris_list:
        if PRIBADI_LABEL.match(b):
            continue
        for k in kalimat(b):
            if cocok(kata, k.lower()) and not SENSITIF.search(k):
                s = samarkan(k)
                return (s[:110] + "...") if len(s) > 110 else s
    return ""


def nilai_kriteria(c, blok, lain, edu, seluruh):
    tahun_blok, bukti, ketemu = [], "", False
    for b in blok:
        isi = "\n".join(b["baris"])
        if cocok(c["kata"], isi.lower()):
            ketemu = True
            tahun_blok.append((b["a"], b["b"]))
            bukti = bukti or baris_bukti(c["kata"], b["baris"])
    tahun = gabung_tahun(tahun_blok)
    bersih = [x for x in lain + (edu if c["pendidikan"] else []) if not PRIBADI_LABEL.match(x)]
    if not ketemu and cocok(c["kata"], "\n".join(bersih).lower()):
        ketemu = True
        bukti = baris_bukti(c["kata"], bersih)
    if ketemu:  # "5 tahun" di baris yang sama dengan kata kunci
        for x in [k for b in seluruh if not PRIBADI_LABEL.match(b) for k in kalimat(b) if cocok(c["kata"], k.lower())]:
            if not SENSITIF.search(x):
                tahun = max(tahun, lama_tertulis(x))
    if not ketemu:
        frac = 0.0
    elif c["min_tahun"] <= 0:
        frac = 1.0
    else:
        frac = 1.0 if tahun >= c["min_tahun"] else 0.5 + 0.5 * (tahun / c["min_tahun"])
    return {"nama": c["nama"], "ditemukan": ketemu, "tahun": round(tahun, 1), "nilai": round(frac, 2), "bukti_awal": bukti}


def nilai_cv(nama_berkas, teks, kr):
    seluruh = [x.strip() for x in teks.splitlines() if x.strip()]
    r = {"sumber": nama_berkas, "peringatan": []}
    if len(re.sub(r"\s+", "", teks)) < 80:
        r.update(status="cv_tidak_terbaca", skor=0, wajib_pct=0, tambah_pct=0, tahun_kerja=0, kriteria=[])
        r["peringatan"].append("CV kosong/terlalu pendek (mungkin hasil ubah PDF/gambar gagal); minta pelamar kirim ulang, jangan dinilai rendah.")
        return r
    if INJEKSI.search(teks):
        r["peringatan"].append("Ada kalimat di CV yang mencoba mengarahkan penilai (abaikan/skor); diabaikan, nilai hanya dari isi kerja.")
    blok, lain, edu = pisah_blok(teks)
    tahun_kerja = gabung_tahun([(b["a"], b["b"]) for b in blok])
    if not blok:
        tahun_kerja = max([lama_tertulis(k) for b in seluruh if not PRIBADI_LABEL.match(b) for k in kalimat(b)
                           if not SENSITIF.search(k)] or [0])
    ws = [nilai_kriteria(c, blok, lain, edu, seluruh) for c in kr["wajib"]]
    ts = [nilai_kriteria(c, blok, lain, edu, seluruh) for c in kr["nilai_tambah"]]
    w_pct = sum(x["nilai"] * c["bobot"] for x, c in zip(ws, kr["wajib"])) / sum(c["bobot"] for c in kr["wajib"])
    t_pct = (sum(x["nilai"] * c["bobot"] for x, c in zip(ts, kr["nilai_tambah"])) / sum(c["bobot"] for c in kr["nilai_tambah"])) if ts else 0
    skor = round(100 * (BOBOT_WAJIB * w_pct + BOBOT_TAMBAH * t_pct)) if ts else round(100 * w_pct)
    gugur = [c["nama"] for x, c in zip(ws, kr["wajib"]) if c["gugur"] and not x["ditemukan"]]
    r.update(skor=skor, wajib_pct=round(100 * w_pct), tambah_pct=round(100 * t_pct), tahun_kerja=round(tahun_kerja, 1),
             status="belum_memenuhi_syarat_dasar" if gugur else "lanjut", syarat_dasar_belum=gugur,
             kriteria=[dict(x, jenis="wajib") for x in ws] + [dict(x, jenis="nilai_tambah") for x in ts])
    return r


def proses(kr, cvs, top):
    hasil = [nilai_cv(n, t, kr) for n, t in cvs]
    for r in hasil:  # seri skor: pengalaman relevan terlama (maks. lama pada kriteria), lalu urutan nama berkas
        r["tahun_relevan"] = max([k["tahun"] for k in r["kriteria"]] or [0])
    for i, r in enumerate(hasil, 1):  # kode mengikuti urutan masuk, bukan peringkat
        r["kode"] = f"C{i}"
    urut = sorted(hasil, key=lambda r: (r["status"] != "lanjut", -r["skor"], -r["tahun_relevan"], r["sumber"]))
    for i, r in enumerate(urut, 1):
        r["peringkat"] = i
    lanjut = [r for r in urut if r["status"] == "lanjut"]
    batas = lanjut[top - 1]["skor"] if top and len(lanjut) >= top else None
    for r in urut:
        r["shortlist"] = bool(top) and r["status"] == "lanjut" and r["peringkat"] <= top
        # CV yang skornya dekat batas shortlist harus dibaca teliti; shortlist pun wajib dibaca.
        r["baca_teliti"] = r["shortlist"] or (batas is not None and r["status"] == "lanjut" and abs(r["skor"] - batas) <= 8)
    return {
        "posisi": kr["posisi"], "jumlah_cv": len(urut), "top": top,
        "jumlah_lanjut": len(lanjut), "jumlah_tidak_terbaca": sum(r["status"] == "cv_tidak_terbaca" for r in urut),
        "jumlah_belum_syarat_dasar": sum(r["status"] == "belum_memenuhi_syarat_dasar" for r in urut),
        "cv": urut,
        "ringkasan_untuk_agent": "UNTUK AGENT SAJA, jangan tampilkan ke pengguna. Ini pra-saring kata kunci, bukan penilaian. "
                                 "Baca setiap CV sendiri, ambil bukti kutipan pendek dari CV, koreksi skor yang meleset. Jangan menilai "
                                 "usia/jenis kelamin/agama/suku/status kawin/penampilan. Jangan salin NIK/alamat/HP ke rekap; pakai kode C1...",
    }


def cetak(h, fmt, out):
    if fmt == "json":
        out.write(json.dumps(h, ensure_ascii=False, indent=2) + "\n")
        return
    if fmt == "csv":
        w = csv.writer(out, lineterminator="\n")
        namas = [k["nama"] for k in h["cv"][0]["kriteria"]] if h["cv"] and h["cv"][0]["kriteria"] else []
        for r in h["cv"]:
            if r["kriteria"]:
                namas = [k["nama"] for k in r["kriteria"]]
                break
        w.writerow(["peringkat", "kode", "sumber", "skor", "status", "tahun_kerja", "shortlist", "baca_teliti"] + namas)
        for r in h["cv"]:
            nil = {k["nama"]: k["nilai"] for k in r["kriteria"]}
            w.writerow([r["peringkat"], r["kode"], r["sumber"], r["skor"], r["status"], r["tahun_kerja"],
                        int(r["shortlist"]), int(r["baca_teliti"])] + [nil.get(n, "") for n in namas])
        return
    out.write(f"Posisi: {h['posisi'] or '-'} | CV: {h['jumlah_cv']} | lanjut: {h['jumlah_lanjut']} | "
              f"tidak terbaca: {h['jumlah_tidak_terbaca']} | belum syarat dasar: {h['jumlah_belum_syarat_dasar']}\n")
    for r in h["cv"]:
        tanda = "*" if r["shortlist"] else ("?" if r["baca_teliti"] else " ")
        out.write(f"{tanda}{r['kode']:>4} {r['skor']:>3} {r['status']:<28} thn={r['tahun_kerja']:<5} {r['sumber']}\n")
        for k in r["kriteria"]:
            out.write(f"        - {k['nama']}: {k['nilai']} (thn {k['tahun']}) {k['bukti_awal']}\n")
        for p in r["peringatan"]:
            out.write(f"        ! {p}\n")
    out.write("\n" + h["ringkasan_untuk_agent"] + "\n")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pra-saring CV pelamar (kata kunci + lama pengalaman).")
    ap.add_argument("kriteria")
    ap.add_argument("sumber")
    ap.add_argument("--top", type=int, default=0, help="jumlah shortlist")
    ap.add_argument("--format", choices=["ringkas", "json", "csv"], default="ringkas")
    a = ap.parse_args(argv)
    try:
        if a.top < 0:
            raise Galat("--top tidak boleh negatif.")
        try:
            kr = periksa_kriteria(json.loads(Path(a.kriteria).read_text(encoding="utf-8-sig")))
        except FileNotFoundError:
            raise Galat(f"Berkas kriteria tidak ditemukan: {a.kriteria}")
        except json.JSONDecodeError as e:
            raise Galat(f"Kriteria bukan JSON yang valid (baris {e.lineno}).")
        cetak(proses(kr, muat_cv(a.sumber), a.top), a.format, sys.stdout)
    except Galat as e:
        print(f"Galat: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
