#!/usr/bin/env python3
"""Skor kecocokan kata kunci antara CV dan lowongan kerja.

Hanya memakai library standar Python (3.8+). Tidak ada koneksi internet,
tidak membaca file lain selain yang diberikan lewat argumen.

Cara pakai:
    python3 skor_kecocokan.py --cv cv.txt --lowongan lowongan.txt
    python3 skor_kecocokan.py --cv cv.txt --lowongan lowongan.txt --format teks

Kedua file input adalah teks biasa (.txt) — salin-tempel isi CV dan isi
lowongan ke dua file terpisah sebelum menjalankan script ini.

Catatan penting: skor ini HANYA mengukur kemunculan kata kunci (proksi ATS
sederhana), BUKAN penilaian kualitas CV atau kecocokan sebenarnya dengan
pekerjaan. Kata kunci yang "hilang" tidak boleh ditambahkan ke CV kecuali
pengguna memang punya pengalaman/keahlian tersebut — dilarang mengarang.
"""
import argparse
import json
import re
import sys

# Kata umum yang diabaikan (ID + EN) agar tidak mendominasi hasil kata kunci.
STOPWORDS = {
    # Indonesia
    "yang", "dan", "di", "ke", "dari", "untuk", "pada", "dengan", "atau",
    "ini", "itu", "adalah", "akan", "juga", "dapat", "bisa", "serta",
    "para", "oleh", "sebagai", "dalam", "tidak", "ada", "kami", "anda",
    "kita", "saya", "mereka", "sudah", "belum", "harus", "minimal",
    "maksimal", "tahun", "bulan", "hari", "jam", "orang", "salah", "satu",
    "kerja", "kami", "perusahaan", "posisi", "kualifikasi", "tanggung",
    "jawab", "jobdesk", "requirement", "kandidat", "pelamar", "lowongan",
    "gaji", "benefit", "fasilitas", "lokasi", "penempatan", "kami",
    "mampu", "bawah", "atas", "bekerja", "berkala", "menjadi", "memiliki",
    "melakukan", "membuat", "baik", "sesuai", "setiap", "secara", "agar",
    "terhadap", "antara", "sehingga", "lebih", "mau", "siap", "diutamakan",
    "berpengalaman", "pengalaman", "bersedia", "usia", "pria", "wanita",
    "lulusan", "terbiasa", "menguasai", "memahami", "tinggi", "cepat",
    "besar", "baru", "lain", "hal", "tersebut", "yaitu", "seperti", "pt", "cv", "tbk",
    # Inggris
    "the", "and", "or", "of", "to", "in", "on", "for", "with", "a", "an",
    "is", "are", "be", "will", "we", "you", "our", "job", "role", "team",
    "years", "year", "experience", "work", "working", "required",
    "requirements", "responsibilities", "qualifications", "candidate",
    "including", "such", "as", "etc", "min", "max", "plus", "good",
    "strong", "ability", "skills", "skill", "please", "send", "apply",
}

# Kata kunci pendek yang tetap bermakna meski < 3 huruf (istilah teknis umum).
IZINKAN_PENDEK = {
    "hr", "it", "ui", "ux", "b2b", "b2c", "crm", "erp", "sql", "php", "css",
    "api", "seo", "kpi", "roi", "sop", "pr", "ai", "ml", "qa", "ci", "cd",
}

POLA_TOKEN = re.compile(r"[a-zA-Z][a-zA-Z0-9+#.\-]*")


def baca_teks(path):
    try:
        with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
            return f.read()
    except OSError as e:
        keluar_error(f"Gagal membaca file '{path}': {e}")


def keluar_error(pesan):
    print(json.dumps({"error": pesan}, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


def ekstrak_kata_kunci(teks, min_kemunculan=1):
    """Kembalikan dict kata -> jumlah kemunculan di teks lowongan, sudah difilter stopword."""
    kata = defaultdict_int()
    for tok in POLA_TOKEN.findall(teks.lower()):
        tok = tok.strip(".-")
        if not tok:
            continue
        if tok in STOPWORDS:
            continue
        if len(tok) < 3 and tok not in IZINKAN_PENDEK:
            continue
        if tok.isdigit():
            continue
        kata[tok] = kata.get(tok, 0) + 1
    return {k: v for k, v in kata.items() if v >= min_kemunculan}


def defaultdict_int():
    return {}


def frasa_dua_kata(teks):
    """Tangkap frasa dua kata yang sering jadi istilah utuh, mis. 'data analyst'."""
    kata_mentah = [w.lower() for w in re.findall(r"[a-zA-Z][a-zA-Z\-]*", teks)]
    frasa = {}
    for i in range(len(kata_mentah) - 1):
        a, b = kata_mentah[i], kata_mentah[i + 1]
        if a in STOPWORDS or b in STOPWORDS or len(a) < 3 or len(b) < 3:
            continue
        f = f"{a} {b}"
        frasa[f] = frasa.get(f, 0) + 1
    return {k: v for k, v in frasa.items() if v >= 2}  # hanya yang muncul berulang = kemungkinan istilah


def main():
    p = argparse.ArgumentParser(description="Skor kecocokan kata kunci CV vs lowongan kerja")
    p.add_argument("--cv", required=True, help="Path file teks isi CV")
    p.add_argument("--lowongan", required=True, help="Path file teks isi lowongan kerja")
    p.add_argument("--top", type=int, default=25, help="Jumlah kata kunci teratas dari lowongan yang dianalisis")
    p.add_argument("--format", choices=["json", "teks"], default="json")
    a = p.parse_args()
    if a.top < 1:
        p.error("--top harus angka positif (mis. 25)")

    teks_cv = baca_teks(a.cv)
    teks_lowongan = baca_teks(a.lowongan)

    if not teks_cv.strip():
        keluar_error("File CV kosong")
    if not teks_lowongan.strip():
        keluar_error("File lowongan kosong")

    kk_lowongan = ekstrak_kata_kunci(teks_lowongan)
    if not kk_lowongan:
        keluar_error("Tidak ditemukan kata kunci bermakna di file lowongan (terlalu pendek atau semuanya kata umum)")

    # Urutkan berdasarkan frekuensi kemunculan di lowongan (proksi kepentingan), lalu alfabet
    terurut = sorted(kk_lowongan.items(), key=lambda x: (-x[1], x[0]))[: a.top]

    cv_lower = teks_cv.lower()
    cv_kata = set(POLA_TOKEN.findall(cv_lower))

    cocok, hilang = [], []
    for kata, freq in terurut:
        # cocok jika kata utuh ATAU muncul sebagai substring kata lebih panjang di CV
        ada = kata in cv_kata or kata in cv_lower
        (cocok if ada else hilang).append({"kata": kata, "muncul_di_lowongan": freq})

    frasa_lowongan = frasa_dua_kata(teks_lowongan)
    frasa_hilang = [f for f in frasa_lowongan if f not in cv_lower]

    total = len(cocok) + len(hilang)
    skor_persen = round(len(cocok) / total * 100, 1) if total else 0.0

    hasil = {
        "skor_kecocokan_persen": skor_persen,
        "jumlah_kata_kunci_dianalisis": total,
        "jumlah_cocok": len(cocok),
        "jumlah_hilang": len(hilang),
        "kata_kunci_cocok": cocok,
        "kata_kunci_hilang": hilang,
        "frasa_dua_kata_hilang": frasa_hilang[:10],
        "catatan": (
            "Skor ini hanya proksi kemunculan kata kunci (gaya pemeriksaan ATS sederhana), "
            "bukan penilaian kualitas atau kecocokan sebenarnya. JANGAN menambahkan kata kunci "
            "yang hilang ke CV kecuali pengguna benar-benar punya pengalaman/keahlian tersebut."
        ),
    }

    if a.format == "json":
        print(json.dumps(hasil, ensure_ascii=False, indent=2))
    else:
        print(f"Skor kecocokan kata kunci: {skor_persen}% ({len(cocok)}/{total})")
        print()
        print("Kata kunci yang SUDAH ada di CV:")
        for item in cocok:
            print(f"  - {item['kata']}")
        print()
        print("Kata kunci yang BELUM terlihat di CV (cek apakah relevan & benar dimiliki):")
        for item in hilang:
            print(f"  - {item['kata']}")
        if frasa_hilang:
            print()
            print("Frasa dua kata dari lowongan yang tidak ditemukan persis di CV:")
            for f in frasa_hilang[:10]:
                print(f"  - {f}")


if __name__ == "__main__":
    main()
