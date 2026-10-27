#!/usr/bin/env python3
"""Hitung angka rapor mingguan karyawan AI. Python standar saja.

Pakai (utama, dari daftar penilaian per percakapan):
       python3 rapor.py --nilai "P1=lolos; P2=nyambung,panjang; P3=fakta,janji" [--tahap minggu1|minggu2-4|bulan2+]
       [--lama "fakta=80,nyambung=90"] [--lama-jawaban "teks rapor minggu lalu"] [--json]
       Daftar panjang (batas baris perintah ±128 KB di Linux, ±8 KB di Windows cmd): --nilai @penilaian.txt atau --nilai -.
Pakai (dari berkas percakapan berpenanda #gagal):
       python3 rapor.py percakapan.txt [--tahap ...] [--lama ...] [--bot "Nama Bot"] [--samarkan-nama "Sari,Budi"] [--json]
Windows: python atau py.

Daftar penilaian: butir dipisah ';' atau baris baru, tiap butir 'kode=kriteria,kriteria' ('lolos' = tanpa kesalahan,
'?' = belum dinilai). Kriteria: fakta, nyambung, konteks, panjang, nada, janji, bocor, teknis.

Format teks: satu percakapan per blok, dipisah baris '---'. Baris 'Pelanggan: ...' dan 'Bot: ...'.
Penilaian manual (opsional) di dalam blok:  #gagal: konteks, panjang   (atau '#gagal: lolos')
CSV: kolom id, pelanggan, bot, gagal, catatan (atau id, peran, pesan, gagal, catatan).
--lama-jawaban: tempel teks rapor minggu lalu apa adanya (baris "Angka tren (tempel minggu depan): ...", tabel,
butir "Fakta: 83,3%", atau kalimat "fakta 100%, ingat konteks 85%"); persen per kriteria diambil otomatis.
'-' = baca dari stdin. --lama (bila diisi) menang untuk kriteria yang sama.
--cek-balasan DRAF: periksa draf balasan sebelum dikirim (panjang <= 3.800 karakter, diakhiri Balas 'rinci', tabel
<= 3 kolom dengan baris pemisah benar, baris "Angka tren", tanpa nama/inisial/nomor pelanggan, tanpa nama berkas/skrip,
persen sama dengan hitungan). DRAF = berkas teks atau '-' (stdin). Nama pelanggan: --samarkan-nama dan nama yang
terbaca dari berkas percakapan (boleh dipakai bersama --nilai). Kode keluar 1 bila ada masalah.
Keluaran: blok angka bertanda UNTUK AGENT SAJA + JSON. Skrip tidak membaca apa pun selain berkas yang diberikan.
"""
import argparse
import csv
import io
import json
import re
import sys
from fractions import Fraction

VERSI = "1.0.3"
KRITERIA = ["fakta", "nyambung", "konteks", "panjang", "nada", "janji", "bocor", "teknis"]
NAMA = {
    "fakta": "Fakta benar", "nyambung": "Nyambung dengan pertanyaan", "konteks": "Ingat konteks",
    "panjang": "Panjang pas", "nada": "Nada sesuai brand", "janji": "Tidak janji berlebihan",
    "bocor": "Data pribadi aman", "teknis": "Bebas kata teknis/proses",
}
KRITIS = {"fakta", "janji", "bocor"}
ALIAS = {
    "salah": "fakta", "salah_fakta": "fakta", "fakta": "fakta", "ngawur": "fakta",
    "nyambung": "nyambung", "tidak_nyambung": "nyambung", "melenceng": "nyambung",
    "konteks": "konteks", "lupa": "konteks", "lupa_konteks": "konteks",
    "panjang": "panjang", "pendek": "panjang", "terlalu_panjang": "panjang", "terlalu_pendek": "panjang",
    "nada": "nada", "brand": "nada", "janji": "janji", "menjanjikan": "janji",
    "bocor": "bocor", "data": "bocor", "privasi": "bocor", "teknis": "teknis", "proses": "teknis",
    "fakta_salah": "fakta", "ingat_konteks": "konteks", "panjang_pas": "panjang", "nada_brand": "nada",
    "janji_berlebihan": "janji", "data_pribadi": "bocor", "kata_teknis": "teknis",
}
TARGET = {"minggu1": 60, "minggu2-4": 75, "bulan2+": 90}
TAHAP_NAMA = {"minggu1": "minggu 1 (masih bayi)", "minggu2-4": "minggu 2-4 (belajar)", "bulan2+": "bulan 2 ke atas (dewasa)"}
ROLE_PELANGGAN = {"pelanggan", "customer", "user", "cust", "klien", "pasien", "calon klien", "tamu", "pembeli", "member", "murid", "siswa"}
ROLE_BOT = {"bot", "ai", "asisten", "assistant", "karyawan ai", "admin bot", "balasan bot", "balasan"}
RE_HP = re.compile(r"(?<!\d)(?:\+?62|0)[\s\-.]?8\d[\d\s\-.]{6,12}\d(?!\d)")
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
RE_ANGKA_PANJANG = re.compile(r"(?<!\d)\d{10,}(?!\d)")
RE_SAPA = re.compile(r"\b(Kak|Bu|Pak|Bapak|Ibu|Mbak|Mas|Bang|Dok|Kakak)\s+([A-Z][a-z]{2,})")
# a/n (atas nama): "transfer a/n Budi Santoso", "a.n. Sari", "atas nama Rina" -> nama disamarkan.
RE_AN = re.compile(r"(?i:\b(a\s*/\s*n|a\.\s?n\.?|atas\s+nama))[ \t]*[:.]?[ \t]*([A-Z][a-zA-Z']*(?:[ \t]+[A-Z][a-zA-Z']*){0,3})")
RE_NAMA_LAIN = re.compile(
    r"\b(?:nama saya|saya|teman saya|saudara saya|istri saya|suami saya|anak saya|adik saya|kakak saya|"
    r"pesanan|hasil pemeriksaan|data|ini|dengan)\s*,?\s+([A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?)")
# Nama marketplace/layanan: bukan nama pelanggan ("pesanan Shopee", "dengan Gojek", "Apakah Bpjs ...").
MEREK_LAYANAN = {"Shopee", "Tokopedia", "Lazada", "Bukalapak", "Blibli", "Tiktok", "TikTok", "Gojek", "Grab",
                 "Gofood", "GoFood", "Grabfood", "GrabFood", "Shopeefood", "Bpjs", "Jne", "Jnt", "Sicepat", "Anteraja",
                 "Whatsapp", "WhatsApp", "Telegram", "Instagram", "Facebook", "Google", "Dana", "Ovo", "Gopay", "Qris"}
BUKAN_NAMA = {"Kak", "Kakak", "Admin", "Tim", "Toko", "Dokter", "Dok", "Staf", "Bot", "Pelanggan", "Saya", "Kami",
              "Terima", "Mohon", "Maaf", "Halo", "Selamat", "Untuk", "Yang", "Ini", "Itu", "Bapak", "Ibu", "Pak", "Bu",
              "Mbak", "Mas", "Bang", "Customer", "Service", "CS", "PT", "CV", "Rp"} | MEREK_LAYANAN
RE_TEKNIS = re.compile(
    r"\b(script|file|path|json|exec|token|api key|apikey|prompt|sistem prompt|agents\.md|knowledge|gateway|openclaw|"
    r"error|debug|database|session|model bahasa|sebagai ai|sebagai model)\b|\.py\b|\.md\b|/home/|\.json\b",
    re.I)
RE_JANJI = re.compile(
    r"\b(pasti|dijamin|jaminan|garansi|100\s?%|sembuh|pasti untung|uang kembali|refund|gratis|diskon \d+|cicilan 0|dalam 1 jam|hari ini juga)\b", re.I)


def bulat1(x):
    """Bulatkan ke satu desimal, setengah ke atas (81,25 -> 81,3; -16,75 -> -16,8), sama dengan hitung manual.
    x boleh Fraction/int/float/str; float dibaca lewat repr agar 83.3 tetap 83.3."""
    f = x if isinstance(x, Fraction) else Fraction(repr(x) if isinstance(x, float) else x)
    tanda = -1 if f < 0 else 1
    q = (abs(f) * 10 + Fraction(1, 2)) // 1
    return tanda * float(q) / 10


def persen(a, b):
    """a dari b dalam persen, satu desimal, setengah ke atas."""
    return bulat1(Fraction(100 * a, b)) if b else None


def samarkan(teks, nama_ekstra=()):
    # 1.0.3: nomor ditutup penuh (tanpa 4 digit akhir).
    teks = RE_EMAIL.sub("[email]", teks)
    teks = RE_HP.sub("[nomor]", teks)
    teks = RE_ANGKA_PANJANG.sub("[angka panjang]", teks)
    teks = RE_AN.sub(lambda m: m.group(1) + " [nama]", teks)
    teks = RE_SAPA.sub(lambda m: m.group(1) + " [nama]", teks)
    nama = sorted({bersih_nama(n) for n in nama_ekstra if bersih_nama(n)}, key=len, reverse=True)
    if nama:
        teks = re.sub(r"(?<!\w)(?:%s)(?!\w)" % "|".join(re.escape(n) for n in nama), "[nama]", teks, flags=re.I)
    return teks


def bersih_nama(n):
    """'a/n Budi Santoso' -> 'Budi Santoso'; buang awalan sapaan dan spasi."""
    n = (n or "").strip()
    n = re.sub(r"(?i)^(a\s*/\s*n|a\.\s?n\.?|atas\s+nama)\s*[:.]?\s*", "", n)
    n = re.sub(r"^(Kak|Bu|Pak|Bapak|Ibu|Mbak|Mas|Bang|Kakak)\s+", "", n).strip(" .,:;")
    return n if len(n) >= 2 else ""


def nama_terdeteksi(cs):
    """Nama pelanggan yang terbaca dari percakapan: sapaan (Kak Sari), label (Pelanggan (Rina, ...)), a/n Budi.
    Dipakai untuk menyamarkan dan memeriksa draf balasan. Nama lengkap juga dipecah per kata."""
    hasil = set()
    for c in cs:
        for n in c.get("nama", []):
            hasil.add(n)
        for _, t in c["turn"]:
            for m in RE_SAPA.finditer(t):
                hasil.add(m.group(2))
            for m in RE_AN.finditer(t):
                hasil.add(m.group(2).strip(" ."))
            for m in RE_NAMA_LAIN.finditer(t):
                hasil.add(m.group(1))
    akhir = set()
    for n in hasil:
        n = bersih_nama(n)
        for kata in [n] + n.split():
            kata = kata.strip(" .,")
            if len(kata) >= 3 and kata not in BUKAN_NAMA_TERSIRAT and kata[0].isupper():
                akhir.add(kata)
    return sorted(akhir)


KATA_LOLOS = ("lolos", "ok", "bersih", "tidak_ada", "none", "0")
PEMISAH_KODE = r"[,;/+]+|\s+dan\s+"


def kode_kriteria(teks, peringatan):
    hasil = []
    for bagian in re.split(PEMISAH_KODE, teks):
        k = bagian.strip().lower().replace(" ", "_").replace("-", "_")
        if not k or k in KATA_LOLOS:
            continue
        if k in ALIAS:
            if ALIAS[k] not in hasil:
                hasil.append(ALIAS[k])
        else:
            peringatan.append("kode penilaian tidak dikenal diabaikan: " + bagian.strip()[:30])
    return hasil


def peran(label, bot_ekstra):
    l = label.strip().lower()
    l = re.sub(r"\(.*?\)", "", l).strip()
    if l in ROLE_BOT or l in bot_ekstra:
        return "bot"
    if l in ROLE_PELANGGAN:
        return "pelanggan"
    return None


def bersihkan_waktu(baris):
    baris = re.sub(r"^\[[^\]]{4,25}\]\s*", "", baris)
    return re.sub(r"^\d{1,2}/\d{1,2}/\d{2,4}[ ,]+\d{1,2}[.:]\d{2}\s*[-–]\s*", "", baris)


def parse_teks(teks, bot_ekstra, peringatan):
    blok = re.split(r"(?m)^\s*-{3,}\s*$", teks)
    hasil = []
    for b in blok:
        if not b.strip():
            continue
        c = {"id": None, "turn": [], "gagal": None, "catatan": "", "nama": []}
        for baris in b.splitlines():
            s = bersihkan_waktu(baris.strip())
            if not s:
                continue
            low = s.lower()
            if low.startswith("#gagal"):
                c["gagal"] = kode_kriteria(s.split(":", 1)[1] if ":" in s else "", peringatan)
            elif low.startswith("#catatan"):
                c["catatan"] = s.split(":", 1)[1].strip() if ":" in s else ""
            elif low.startswith("id:") or low.startswith("#id"):
                c["id"] = s.split(":", 1)[1].strip()
            else:
                m = re.match(r"^([^:：]{1,40}?)\s*[:：]\s*(.*)$", s)
                r = peran(m.group(1), bot_ekstra) if m else None
                if r:
                    c["turn"].append([r, m.group(2)])
                    for kur in re.findall(r"\(([^)]*)\)", m.group(1)):
                        for bag in re.split(r"[,;/]", kur):
                            bag = bersih_nama(bag)
                            if bag and re.match(r"^[A-Z][a-zA-Z' .-]{1,40}$", bag):
                                c.setdefault("nama", []).append(bag)
                elif c["turn"]:
                    c["turn"][-1][1] += " " + s
                elif m and re.match(r"^[A-Za-z][\w ]{0,24}$", m.group(1)):
                    c["turn"].append(["pelanggan", m.group(2)])
                else:
                    c["turn"].append(["pelanggan", s])
        if c["turn"]:
            hasil.append(c)
    return hasil


RE_KODE_P = re.compile(r"^([A-Za-z]{0,3}-?\d{1,5})(?![\w])")


def nama_dari_tambahan(teks):
    """'(Ibu Sari Wulandari)' / 'a/n Budi' / '(H.)' -> nama & inisial untuk diperiksa di draf (tidak pernah dicetak)."""
    hasil = []
    teks = re.sub(r"(?i)(?<!\w)(a\s*/\s*n|a\.\s?n\.?|atas\s+nama)(?!\w)", " ", teks)
    for bag in re.split(r"[(),;/]+|\s+-\s+", teks):
        b = bersih_nama(bag)
        if re.fullmatch(r"[A-Z]\.?", bag.strip()):
            hasil.append(bag.strip().rstrip(".") + ".")
        elif b and re.match(r"^[A-Z][a-zA-Z' .-]{1,60}$", b):
            hasil.append(b)
            hasil += [k for k in b.split() if len(k) >= 3 and k not in BUKAN_NAMA]
    return hasil


def parse_nilai(teks, peringatan, nama_out=None):
    """Daftar penilaian langsung: 'P1=lolos; P2=nyambung,panjang'. Pemisah butir ';' atau baris baru; '=' atau ':'.
    Teks tambahan setelah kode P ('P3 (Sari)=...', berapa pun panjangnya) dibuang; namanya masuk nama_out."""
    hasil, per = [], {}
    nama_out = nama_out if nama_out is not None else []
    for no, bag in enumerate(re.split(r"[;\n]+", teks), 1):
        bag = bag.strip().strip("`").strip()
        if not bag:
            continue
        kp = RE_KODE_P.match(bag)
        if kp:
            sisa = bag[kp.end():]
            pos = sisa.find("=") if "=" in sisa else sisa.find(":")
            if pos < 0:
                peringatan.append("butir %s tanpa '=' diabaikan (tulis mis. %s=lolos)" % (kp.group(1), kp.group(1)))
                continue
            cid, tambahan, isi = kp.group(1), sisa[:pos].strip(), sisa[pos + 1:].strip()
            if tambahan:
                # "P3 (Sari)" / "P3 a/n Budi": nama tidak pernah dibawa ke hasil; cukup kode percakapan.
                peringatan.append("teks tambahan di kode %s dibuang (jangan menulis nama pelanggan di daftar penilaian)"
                                  % cid)
                nama_out += nama_dari_tambahan(tambahan)
        else:
            m = re.match(r"^([^=:]{1,40}?)\s*[=:]\s*(.*)$", bag)
            if not m:
                peringatan.append("butir penilaian ke-%d tanpa '=' diabaikan (bentuk yang benar: P1=lolos)" % no)
                continue
            cid, isi = m.group(1).strip(), m.group(2).strip()
        bagian = [b.strip().lower().replace(" ", "_") for b in re.split(PEMISAH_KODE, isi) if b.strip()]
        if not bagian or isi.lower() in ("?", "belum"):
            gagal = None
            if not bagian:
                peringatan.append("%s tanpa penilaian (tulis 'lolos' atau kode kriteria); tidak dihitung" % cid)
        else:
            gagal = kode_kriteria(isi, peringatan)
            if not gagal and not all(b in KATA_LOLOS for b in bagian):
                gagal = None
                peringatan.append("%s: kode tidak dikenal, percakapan tidak dihitung; perbaiki daftar penilaian" % cid)
        if cid in per:
            peringatan.append("kode percakapan %s muncul dua kali; penilaiannya digabung" % cid)
            c = per[cid]
            if gagal is not None:
                c["gagal"] = (c["gagal"] or []) + [k for k in gagal if k not in (c["gagal"] or [])]
            continue
        per[cid] = {"id": cid, "turn": [], "gagal": gagal, "catatan": ""}
        hasil.append(per[cid])
    return hasil


def cek_konsistensi(n, gagal, bersih, matriks=None):
    """Periksa angka rapor sebelum ditulis. Kosong = konsisten.

    n: jumlah percakapan dinilai; gagal: {kriteria: jumlah percakapan yang gagal}; bersih: jumlah percakapan
    tanpa satu pun kesalahan; matriks (opsional): daftar kode gagal per percakapan, sumber kebenaran angka.
    """
    masalah = []
    if n <= 0:
        return masalah
    if not 0 <= bersih <= n:
        masalah.append("percakapan bersih %d di luar 0-%d" % (bersih, n))
    for k, g in gagal.items():
        if not 0 <= g <= n:
            masalah.append("%s: gagal %d di luar 0-%d" % (k, g, n))
    if gagal:
        lolos_min = min(n - g for g in gagal.values())
        if bersih > lolos_min:
            masalah.append("percakapan bersih %d melebihi lolos terendah %d (bersih harus lolos semua kriteria)"
                           % (bersih, lolos_min))
        total = sum(gagal.values())
        if n - bersih > total:
            masalah.append("%d percakapan tidak bersih tetapi total kesalahan di tabel hanya %d" % (n - bersih, total))
    if matriks is not None:
        if len(matriks) != n:
            masalah.append("jumlah dinilai %d berbeda dengan daftar penilaian %d" % (n, len(matriks)))
        for k, g in gagal.items():
            nyata = sum(1 for kode in matriks if k in kode)
            if g != nyata:
                masalah.append("%s: tertulis gagal %d, menurut daftar penilaian %d" % (k, g, nyata))
        nyata_bersih = sum(1 for kode in matriks if not kode)
        if bersih != nyata_bersih:
            masalah.append("percakapan bersih tertulis %d, menurut daftar penilaian %d" % (bersih, nyata_bersih))
    return masalah


def persen_id(x):
    """90.0 -> '90%', 83.3 -> '83,3%' (gaya penulisan Indonesia)."""
    if x is None:
        return "-"
    return ("%d%%" % x) if float(x).is_integer() else ("%s%%" % x).replace(".", ",")


def parse_csv(teks, bot_ekstra, peringatan):
    r = csv.DictReader(io.StringIO(teks))
    if not r.fieldnames:
        return []
    kol = {k.strip().lower(): k for k in r.fieldnames if k}
    urut, per = [], {}
    for i, row in enumerate(r, 1):
        get = lambda *ns: next((row.get(kol[n], "") or "" for n in ns if n in kol), "")
        cid = get("id", "no") or "P%d" % i
        if cid not in per:
            per[cid] = {"id": cid, "turn": [], "gagal": None, "catatan": ""}
            urut.append(cid)
        c = per[cid]
        if "peran" in kol:
            rr = peran(get("peran"), bot_ekstra) or "pelanggan"
            if get("pesan"):
                c["turn"].append([rr, get("pesan")])
        else:
            if get("pelanggan", "pesan_pelanggan"):
                c["turn"].append(["pelanggan", get("pelanggan", "pesan_pelanggan")])
            if get("bot", "balasan_bot", "balasan"):
                c["turn"].append(["bot", get("bot", "balasan_bot", "balasan")])
        g = get("gagal", "penilaian")
        if g.strip():
            c["gagal"] = (c["gagal"] or []) + [x for x in kode_kriteria(g, peringatan) if x not in (c["gagal"] or [])]
        if get("catatan"):
            c["catatan"] = get("catatan")
    return [per[k] for k in urut]


def dugaan(c, maks_panjang):
    """Dugaan mekanis dari kata/angka di balasan bot. Hanya petunjuk; penilai yang memutuskan."""
    d = set()
    cust = " ".join(t for r, t in c["turn"] if r == "pelanggan")
    cust_digit = re.sub(r"\D", "", cust)
    for r, t in c["turn"]:
        if r != "bot":
            continue
        if len(t) > maks_panjang:
            d.add("panjang")
        if RE_TEKNIS.search(t):
            d.add("teknis")
        if RE_JANJI.search(t):
            d.add("janji")
        for m in list(RE_HP.finditer(t)) + list(RE_EMAIL.finditer(t)) + list(RE_ANGKA_PANJANG.finditer(t)):
            tok = re.sub(r"\D", "", m.group(0)) if "@" not in m.group(0) else m.group(0)
            if tok and tok not in cust_digit and tok not in cust:
                d.add("bocor")
    return sorted(d, key=KRITERIA.index)


def predikat(pct, kritis):
    if kritis:
        return "A" if pct >= 100 else "B" if pct >= 95 else "C" if pct >= 85 else "D"
    return "A" if pct >= 90 else "B" if pct >= 75 else "C" if pct >= 60 else "D"


def baca_lama(s):
    if not s:
        return {}
    try:
        if s.strip().endswith(".json"):
            with open(s, encoding="utf-8") as f:
                d = json.load(f)
            d = d.get("lolos_persen", d)
            return {k: float(v) for k, v in d.items() if k in KRITERIA}
    except (OSError, ValueError):
        raise SystemExit("Rapor lama tidak terbaca: " + s)
    out = {}
    for bag in re.split(r"[,;]", s):
        if "=" in bag:
            k, v = bag.split("=", 1)
            k = ALIAS.get(k.strip().lower().replace(" ", "_"), k.strip().lower())
            try:
                if k in KRITERIA:
                    out[k] = float(v.strip().rstrip("%").replace(",", "."))
            except ValueError:
                pass
    return out


LABEL_LAMA = {
    "fakta": ["fakta benar", "fakta", "fakta salah", "salah fakta"],
    "nyambung": ["nyambung dengan pertanyaan", "nyambung", "tidak nyambung"],
    "konteks": ["ingat konteks", "konteks", "lupa konteks"],
    "panjang": ["panjang pas", "panjang"],
    "nada": ["nada sesuai brand", "nada brand", "nada"],
    "janji": ["tidak janji berlebihan", "janji", "janji berlebihan"],
    "bocor": ["data pribadi aman", "data pribadi", "privasi", "bocor", "data bocor", "data pribadi bocor"],
    "teknis": ["bebas kata teknis/proses", "bebas kata teknis", "kata teknis", "teknis"],
}
# Label yang artinya GAGAL ("Fakta salah: 16,7%"): angkanya bukan persen lolos, jadi tidak dipakai.
LABEL_GAGAL = {"fakta salah", "salah fakta", "tidak nyambung", "lupa konteks", "janji berlebihan", "data bocor",
               "data pribadi bocor"}
_LABEL_KE_KODE = {lbl: k for k, ls in LABEL_LAMA.items() for lbl in ls}
RE_LABEL_LAMA = re.compile(
    r"(?<![\w-])(%s)(?![\w-])" % "|".join(re.escape(x) for x in sorted(_LABEL_KE_KODE, key=len, reverse=True)), re.I)
_ANGKA = r"(\d{1,3}(?:[.,]\d+)?)"
RE_PERSEN = re.compile(r"(?<![\w.,])" + _ANGKA + r"\s*%")
RE_DARI_KE = re.compile(r"\bdari\s+" + _ANGKA + r"\s*%\s*(?:ke|jadi|menjadi)\s+" + _ANGKA + r"\s*%", re.I)
# Batas angka utuh: titik/koma setelah angka boleh (akhir kalimat "10 dari 12."), kecuali diikuti digit (desimal).
AKHIR_ANGKA = r"(?!\d|[.,]\d)"
AWAL_ANGKA = r"(?<!\d)(?<!\d[.,])"
RE_HITUNGAN = re.compile(r"(?<![\w.,])(\d{1,6})\s*(?:dari|/)\s*(\d{1,6})" + AKHIR_ANGKA, re.I)
RE_SAMA_DENGAN = re.compile(r"^[^\d\n]{0,24}?[=:]\s*" + _ANGKA + r"(?!\d|[.,]\d|\s*(?:poin|dari|/|percakapan))", re.I)
TANDA_TREN = "Angka tren (tempel minggu depan)"


def _angka(x):
    return float(x.replace(",", "."))


def nilai_segmen(seg):
    """Persen lolos dari potongan teks setelah label kriteria. None bila tidak ada angka yang jelas.
    Urutan: 'dari X% ke Y%' (ambil Y) -> angka ber-% pertama -> 'a dari b' / 'a/b' -> '= angka'."""
    m = RE_DARI_KE.search(seg)
    if m:
        return _angka(m.group(2))
    m = RE_PERSEN.search(seg)
    if m:
        return _angka(m.group(1))
    m = RE_HITUNGAN.search(seg)
    if m and int(m.group(2)) > 0 and int(m.group(1)) <= int(m.group(2)):
        return persen(int(m.group(1)), int(m.group(2)))
    m = RE_SAMA_DENGAN.match(seg)
    if m:
        return _angka(m.group(1))
    return None


def baca_lama_teks(teks, peringatan=None):
    """Ambil persen per kriteria dari teks rapor minggu lalu yang ditempel apa adanya.

    Urutan sumber: baris 'Angka tren (tempel minggu depan): ...' bila ada; bila tidak, seluruh teks (tabel, butir,
    kalimat). Tiap label kriteria dibaca sampai label berikutnya atau akhir baris: persen ditulis setelah hitungan
    ('lolos 10 dari 12 (83,3%)') tetap terbaca 83,3; 'P3' dan 'turun 16,7 poin' tidak terbaca. Label bermakna gagal
    ('fakta salah 16,7%') tidak dipakai dan diberi peringatan.
    """
    peringatan = peringatan if peringatan is not None else []
    if not teks or not teks.strip():
        return {}
    sumber = teks
    for baris in teks.splitlines():
        if TANDA_TREN.lower() in baris.lower():
            sumber = baris.split(":", 1)[1] if ":" in baris else baris
            break
    out, dilewati = {}, []
    for baris in sumber.splitlines():
        ms = list(RE_LABEL_LAMA.finditer(baris))
        for i, m in enumerate(ms):
            ujung = ms[i + 1].start() if i + 1 < len(ms) else len(baris)
            seg = baris[m.end():min(ujung, m.end() + 60)]
            lbl = m.group(1).lower()
            k = _LABEL_KE_KODE[lbl]
            v = nilai_segmen(seg)
            if v is None:
                continue
            if lbl in LABEL_GAGAL:
                dilewati.append(m.group(1))
                continue
            if v > 100:
                peringatan.append("angka rapor lama %s di atas 100 diabaikan" % k)
                continue
            if k not in out:
                out[k] = v
    if dilewati:
        peringatan.append("rapor lama: angka setelah label bermakna gagal (%s) tidak dipakai karena bukan persen lolos; "
                          "tempel baris 'Angka tren' atau tulis persen lolos" % ", ".join(sorted(set(dilewati))))
    if not out:
        peringatan.append("rapor lama ditempel, tetapi tidak ada persen per kriteria yang terbaca; tren tidak dihitung")
    return out


def baris_tren(lolos):
    """Satu baris angka untuk ditempel pengguna minggu depan (dibaca lagi oleh --lama-jawaban)."""
    pendek = {"fakta": "fakta", "nyambung": "nyambung", "konteks": "konteks", "panjang": "panjang", "nada": "nada",
              "janji": "janji", "bocor": "data pribadi", "teknis": "kata teknis"}
    isi = "; ".join("%s %s" % (pendek[k], persen_id(lolos[k])) for k in KRITERIA if lolos.get(k) is not None)
    return "%s: %s" % (TANDA_TREN, isi) if isi else ""


def hitung(cs, tahap, lama, maks_panjang, nama_ekstra, peringatan):
    dinilai = [c for c in cs if c["gagal"] is not None]
    belum = [c for c in cs if c["gagal"] is None]
    n = len(dinilai)
    gagal = {k: [c for c in dinilai if k in c["gagal"]] for k in KRITERIA}
    lolos = {k: persen(n - len(gagal[k]), n) for k in KRITERIA}
    kriteria = []
    for k in KRITERIA:
        row = {"kode": k, "nama": NAMA[k], "kritis": k in KRITIS, "gagal": len(gagal[k]), "lolos": n - len(gagal[k]),
               "dinilai": n, "gagal_di": [c["id"] or "-" for c in gagal[k]], "lolos_persen": lolos[k],
               "nilai": predikat(lolos[k], k in KRITIS) if n else None}
        if n and k not in KRITIS:
            row["target_tahap"] = TARGET[tahap]
            row["vs_target"] = "di atas" if lolos[k] > TARGET[tahap] else "sesuai" if lolos[k] == TARGET[tahap] else "di bawah"
        if k in lama and lolos[k] is not None:
            row["lama_persen"] = lama[k]
            row["selisih_poin"] = bulat1(Fraction(repr(lolos[k])) - Fraction(repr(lama[k])))
        kriteria.append(row)
    urut = sorted(KRITERIA, key=lambda k: (-len(gagal[k]), 0 if k in KRITIS else 1, KRITERIA.index(k)))
    top = []
    for k in urut:
        if len(gagal[k]) and len(top) < 3:
            ctr = []
            for c in gagal[k][:2]:
                p = next((t for r, t in c["turn"] if r == "pelanggan"), "")
                ctr.append({"id": c["id"] or "-", "pelanggan_awal": samarkan(p, nama_ekstra)[:90]})
            top.append({"kode": k, "nama": NAMA[k], "jumlah": len(gagal[k]), "contoh": ctr})
    rata = bulat1(sum(Fraction(repr(v)) for v in lolos.values()) / len(KRITERIA)) if n else None
    kena_kritis = [k for k in KRITIS if gagal[k]]
    umum = predikat(rata, False) if n else None
    if umum in ("A", "B") and kena_kritis:
        umum = "C"
    sudah_bersih = sum(1 for c in dinilai if not c["gagal"])
    masalah = cek_konsistensi(n, {k: len(gagal[k]) for k in KRITERIA}, sudah_bersih, [c["gagal"] for c in dinilai])
    nilai_unik = {lolos[k] for k in KRITERIA}
    semua_sama = bool(n) and len(nilai_unik) == 1 and lolos[KRITERIA[0]] < 100
    peringatan = list(peringatan)
    if n and n < 10:
        peringatan.append("hanya %d percakapan dinilai: nilai bersifat indikatif, jangan ditarik kesimpulan besar" % n)
    if not n:
        peringatan.append("belum ada penilaian: tidak ada angka yang bisa dihitung")
    if belum:
        peringatan.append("%d percakapan belum dinilai (tanpa penilaian/#gagal) dan tidak dihitung: %s"
                          % (len(belum), ", ".join(c["id"] or "-" for c in belum)))
    tak_tercatat = []
    for c in dinilai:
        if not c["turn"]:
            continue
        ekstra = [k for k in dugaan(c, maks_panjang) if k not in c["gagal"]]
        if ekstra:
            tak_tercatat.append({"id": c["id"] or "-", "dugaan": ekstra})
    dugaan_belum = []
    for c in belum:
        d = dugaan(c, maks_panjang) if c["turn"] else []
        if d:
            dugaan_belum.append({"id": c["id"] or "-", "dugaan": d})
    return {
        "versi": VERSI,
        "tahap": tahap, "tahap_nama": TAHAP_NAMA[tahap], "percakapan_total": len(cs), "dinilai": n,
        "belum_dinilai": len(belum), "percakapan_bersih": sudah_bersih,
        "bersih_persen": persen(sudah_bersih, n),
        "rata_lolos_persen": rata, "nilai_umum": umum, "kriteria": kriteria,
        "lolos_persen": {k: lolos[k] for k in KRITERIA if lolos[k] is not None},
        "tiga_kesalahan_teratas": top, "kena_kriteria_kritis": sorted(kena_kritis, key=KRITERIA.index),
        "ada_rapor_lama": bool(lama), "baris_tren": baris_tren(lolos) if n else "",
        "konsistensi": {"ok": not masalah, "masalah": masalah}, "semua_kriteria_sama_persen": semua_sama,
        "dugaan_tak_tercatat_pada_yang_dinilai": tak_tercatat, "dugaan_pada_yang_belum_dinilai": dugaan_belum,
        "peringatan": peringatan,
    }


def ringkas_daftar(ids, maks=15):
    if not ids:
        return "-"
    if len(ids) <= maks:
        return ", ".join(ids)
    return ", ".join(ids[:maks]) + " (+%d lainnya)" % (len(ids) - maks)


def blok_agent(h):
    n = h["dinilai"]
    L = ["=== UNTUK AGENT SAJA: jangan ditempel ke pengguna, tulis ulang dengan bahasa biasa ===",
         "salin angka persis dari blok ini; jangan menghitung ulang di kepala",
         "tahap: %s | dinilai: %d dari %d | bersih (lolos SEMUA kriteria): %s | rata lolos: %s | nilai umum: %s"
         % (h["tahap_nama"], n, h["percakapan_total"],
            "-" if h["bersih_persen"] is None else "%d dari %d (%s)" % (h["percakapan_bersih"], n, persen_id(h["bersih_persen"])),
            persen_id(h["rata_lolos_persen"]), h["nilai_umum"] or "-")]
    for k in h["kriteria"]:
        s = "%-9s %-28s lolos %s | nilai %s | gagal di: %s" % (
            k["kode"], k["nama"], "-" if k["lolos_persen"] is None else "%d dari %d (%s)" % (k["lolos"], n, persen_id(k["lolos_persen"])),
            k["nilai"] or "-", ringkas_daftar(k["gagal_di"]))
        if "vs_target" in k:
            s += " | target %d%% (%s)" % (k["target_tahap"], k["vs_target"])
        if "selisih_poin" in k:
            sp = k["selisih_poin"]
            arah = "tetap" if sp == 0 else "%s %s poin" % ("naik" if sp > 0 else "turun", persen_id(abs(sp)).rstrip("%"))
            s += " | minggu lalu %s (%s)" % (persen_id(k["lama_persen"]), arah)
        L.append(s)
    if n:
        kons = h["konsistensi"]
        lolos_min = min(k["lolos"] for k in h["kriteria"])
        total = sum(k["gagal"] for k in h["kriteria"])
        if kons["ok"]:
            L.append("cek konsistensi: OK (bersih %d <= lolos terendah %d; tidak bersih %d <= total kesalahan %d)"
                     % (h["percakapan_bersih"], lolos_min, n - h["percakapan_bersih"], total))
        else:
            L.append("cek konsistensi: MASALAH -> " + "; ".join(kons["masalah"]))
    if h.get("semua_kriteria_sama_persen"):
        L.append("catatan: semua kriteria sama persen karena jumlah gagalnya kebetulan sama (lihat 'gagal di'); "
                 "tulis satu kalimat penjelas di rapor agar tidak dikira salah hitung")
    if h.get("baris_tren"):
        L.append("baris tren (WAJIB disalin apa adanya ke rapor, tepat di bawah tabel): " + h["baris_tren"])
    for i, t in enumerate(h["tiga_kesalahan_teratas"], 1):
        ex = "; ".join(("%s: \"%s\"" % (e["id"], e["pelanggan_awal"])) if e["pelanggan_awal"] else e["id"] for e in t["contoh"])
        L.append("kesalahan #%d: %s (%d percakapan) contoh %s" % (i, t["nama"], t["jumlah"], ex))
    if h["kena_kriteria_kritis"]:
        L.append("kritis kena: " + ", ".join(h["kena_kriteria_kritis"]) + " -> wajib masuk keputusan pemilik")
    for d in h["dugaan_tak_tercatat_pada_yang_dinilai"][:20]:
        L.append("dugaan belum tercatat %s: %s (periksa ulang)" % (d["id"], ",".join(d["dugaan"])))
    for d in h["dugaan_pada_yang_belum_dinilai"][:20]:
        L.append("belum dinilai, dugaan %s: %s" % (d["id"], ",".join(d["dugaan"])))
    lebih = len(h["dugaan_tak_tercatat_pada_yang_dinilai"]) + len(h["dugaan_pada_yang_belum_dinilai"]) - 40
    if lebih > 0:
        L.append("dugaan lain: %d percakapan (lihat JSON)" % lebih)
    for p in h["peringatan"]:
        L.append("peringatan: " + p)
    L.append("=== AKHIR BLOK ===")
    return "\n".join(L)


BATAS_BALASAN = 3800
PENUTUP = "Balas 'rinci'"
RE_PROSES = re.compile(
    r"(?<![\w-])[\w.-]+\.(?:py|md|json|txt|csv|sh|yaml|yml|log)(?!\w)|/home/|/root/|/tmp/|[A-Za-z]:\\\\|"
    r"\b(?:skrip|script|python3?|py|exec|tool|rapor\.py|json|stdin|stdout)\b|--[a-z][a-z-]+|"
    r"(?<![\w-])[a-z]+(?:-[a-z0-9]+){2,}(?![\w-])", re.I)
RE_DIGIT_HP = re.compile(r"(?<!\d)(?:\+?62[\s.-]?|0)8\d{2}[\s.-]?[\dx]{3,4}[\s.-]?[\dx]{2,5}|x{3,}[\s.-]?\d{3,4}|(?<![\d.,])\d{9,}(?![\d.,])", re.I)
PENDEK_KRITERIA = {"fakta": "fakta", "nyambung": "nyambung", "konteks": "konteks", "panjang": "panjang",
                   "nada": "nada", "janji": "janji", "data pribadi": "bocor", "kata teknis": "teknis"}


def sel_tabel(baris):
    return [x.strip() for x in baris.strip().strip("|").split("|")]


def cek_tabel(teks):
    masalah, blok = [], []
    for baris in teks.splitlines() + [""]:
        if baris.strip().startswith("|"):
            blok.append(baris)
            continue
        if blok:
            kepala = sel_tabel(blok[0])
            if len(kepala) > 3:
                masalah.append("tabel %d kolom (maks. 3): %s" % (len(kepala), blok[0].strip()[:60]))
            if len(blok) < 2 or not all(re.match(r"^:?-{3,}:?$", x) for x in sel_tabel(blok[1])):
                masalah.append("baris kedua tabel harus pemisah |---|---|---|: %s" % blok[0].strip()[:60])
            elif len(sel_tabel(blok[1])) != len(kepala):
                masalah.append("jumlah kolom baris pemisah (%d) beda dengan judul tabel (%d)"
                               % (len(sel_tabel(blok[1])), len(kepala)))
            for b in blok[2:]:
                sel = sel_tabel(b)
                if all(re.match(r"^:?-{3,}:?$", x) for x in sel):
                    masalah.append("baris pemisah ganda di tengah tabel: %s" % b.strip()[:60])
                elif len(sel) != len(kepala):
                    masalah.append("baris tabel %d kolom, judul %d kolom: %s" % (len(sel), len(kepala), b.strip()[:60]))
            blok = []
    return masalah


_ALT_LABEL = "|".join(re.escape(x) for x in sorted(_LABEL_KE_KODE, key=len, reverse=True))
RE_BARIS_KRITERIA = re.compile(r"^\s*(?:\|\s*|[-*•]\s+|\d+[.)]\s+)?\**\s*(?:%s)\s*\**\s*[:|]" % _ALT_LABEL, re.I)
RE_KALIMAT_TREN = re.compile(r"\b(naik|turun|minggu lalu|dibanding|poin|sebelumnya)\b", re.I)


def persen_di_balasan(teks):
    """Persen per kriteria yang tertulis di baris tabel/butir draf ('| Fakta | 83,3% ...', '- Fakta: 83,3%'),
    sebagai daftar (kode, persen) per baris agar baris ganda yang berbeda tetap tertangkap.
    Kalimat ringkasan/tren ('naik dari 90% ke 100%') dan baris 'Angka tren' tidak dibaca (diperiksa terpisah)."""
    hasil = []
    for b in teks.splitlines():
        if TANDA_TREN.lower() in b.lower() or not RE_BARIS_KRITERIA.match(b) or RE_KALIMAT_TREN.search(b):
            continue
        hasil += list(baca_lama_teks(b, []).items())
    return hasil


# Kata setelah a/n yang menandai nama usaha, bukan nama pelanggan ("Rekening a/n Klinik Senyum Sehat").
KATA_USAHA = {"Klinik", "Toko", "PT", "CV", "UD", "Apotek", "Salon", "Kafe", "Cafe", "Warung", "Yayasan", "Koperasi",
              "Usaha", "Butik", "Studio", "Bengkel", "Kedai", "Resto", "Restoran", "Bimbel", "Laundry", "Hotel",
              "Rumah", "Kantor", "Lembaga", "Sekolah", "Pondok", "Optik", "Catering", "Katering"}
RE_REKENING = re.compile(r"(?i)\b(?:rekening|rek\.?|no\.?\s*rek|norek|virtual account|va)\b[^\n\d]{0,25}$")
# Nama tanpa sapaan di bagian pertanyaan/asumsi (heuristik; nama pasti tetap lewat --samarkan-nama).
RE_NAMA_TERSIRAT = re.compile(
    r"\b(?:Apakah|apakah|pelanggan|pasien|klien|pembeli|pesanan|keluhan|milik)\s+([A-Z][a-z]{2,})\b"
    r"|\b([A-Z][a-z]{2,})\s*\(P\d+\)")
BUKAN_NAMA_TERSIRAT = BUKAN_NAMA | KATA_USAHA | {
    "Anda", "Harga", "Promo", "Jam", "Ongkir", "Stok", "Layanan", "Paket", "Produk", "Pesanan", "Semua", "Ada",
    "Boleh", "Perlu", "Sudah", "Bisa", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu", "Refund",
    "Diskon", "Garansi", "Fakta", "Nyambung", "Konteks", "Panjang", "Nada", "Janji", "Data", "Kata", "Bot", "Admin"}
RE_INISIAL_P = re.compile(r"(?<![\w.])([A-Z])\.\s*\(?P\d+\b")


def cek_balasan(teks, h=None, nama=(), nomor=(), angka_pelanggan=()):
    """Periksa draf balasan pertama sebelum dikirim. Kosong = siap kirim.
    nama: nama/inisial pelanggan ('H.' = inisial); nomor: nomor HP pelanggan; angka_pelanggan: deret angka panjang
    dari pesan pelanggan (nomor rekening/resi), yang tetap dilarang walau ditulis setelah kata 'rekening'."""
    masalah = []
    t = (teks or "").strip()
    if not t:
        return ["draf kosong"]
    if len(t) > BATAS_BALASAN:
        masalah.append("panjang %d karakter (maks. %d); ringkas lagi, rincian lewat 'rinci'" % (len(t), BATAS_BALASAN))
    akhir = [b for b in t.splitlines() if b.strip()][-1]
    if PENUTUP.lower() not in akhir.lower():
        masalah.append("baris terakhir harus ditutup: Mau rincian per percakapan dan cara cek tiap PR? Balas 'rinci'.")
    masalah += cek_tabel(t)
    baris_tr = [b for b in t.splitlines() if TANDA_TREN.lower() in b.lower()]
    if not baris_tr:
        masalah.append("baris '%s: ...' belum ada (salin dari hitungan, di bawah tabel)" % TANDA_TREN)
    for m in RE_PROSES.finditer(t):
        masalah.append("kata proses/nama berkas/nama skill di balasan: '%s'" % m.group(0)[:40])
        break
    digit_pel = {re.sub(r"\D", "", x) for x in angka_pelanggan if len(re.sub(r"\D", "", x)) >= 8}
    for m in RE_DIGIT_HP.finditer(t):
        d = re.sub(r"\D", "", m.group(0))
        if (re.fullmatch(r"\d{9,}", m.group(0)) and not re.match(r"(?:62|0)8", d) and d not in digit_pel
                and RE_REKENING.search(t[max(0, m.start() - 40):m.start()])):
            continue  # nomor rekening usaha di PR ("Rekening BCA 1234567890"), bukan dari pesan pelanggan
        masalah.append("ada potongan nomor telepon/angka panjang di balasan ('%s'); tulis [nomor]" % m.group(0)[:6])
        break
    for no in nomor:
        d = re.sub(r"\D", "", no)
        if len(d) >= 8 and re.search(r"(?<!\d)%s(?!\d)" % re.escape(d[-4:]), re.sub(r"(?<=\d)[\s.-](?=\d)", "", t)):
            masalah.append("4 digit akhir nomor pelanggan muncul di balasan; tulis [nomor]")
            break
    inisial = sorted({n.strip().rstrip(".") for n in nama if re.fullmatch(r"\s*[A-Z]\.?\s*", n or "")})
    for i in inisial:
        # A-D juga huruf nilai ("nilai umum C."): untuk huruf itu hanya diperiksa di depan kode P / setelah sapaan.
        pola = (r"(?<![\w.])%s\.(?=[\s,;)]|$)" % i) if i not in "ABCD" else \
            (r"(?:\b(?:Kak|Bu|Pak|Mbak|Mas|Ibu|Bapak|pelanggan|pasien|klien)\s+%s\.|(?<![\w.])%s\.\s*\(?P\d)" % (i, i))
        if re.search(pola, t):
            masalah.append("inisial pelanggan '%s.' muncul di balasan; ganti 'pelanggan di P-nomor'" % i)
    daftar_nama = sorted({bersih_nama(n) for n in nama if bersih_nama(n)}, key=len, reverse=True)
    for n in daftar_nama:
        if re.search(r"(?<!\w)%s(?!\w)" % re.escape(n), t, re.I):
            masalah.append("nama pelanggan '%s' muncul di balasan (juga di bagian asumsi/pertanyaan); ganti 'pelanggan di P-nomor'" % n)
        elif re.search(r"(?:\b(?:Kak|Bu|Pak|Mbak|Mas|Ibu|Bapak|pelanggan|pasien|klien)\s+|\()%s\.(?=[\s,;)]|$)"
                       % re.escape(n[0].upper()), t):
            masalah.append("inisial pelanggan '%s.' muncul di balasan; ganti 'pelanggan di P-nomor'" % n[0].upper())
    for m in RE_SAPA.finditer(t):
        if m.group(2) not in BUKAN_NAMA:
            masalah.append("sapaan bernama '%s %s' di balasan; ganti 'pelanggan di P-nomor'" % (m.group(1), m.group(2)))
            break
    for m in RE_AN.finditer(t):
        if m.group(2).split()[0] not in BUKAN_NAMA and m.group(2).split()[0] not in KATA_USAHA:
            masalah.append("nama setelah a/n (atas nama) di balasan; tulis 'a/n [nama]'")
            break
    if re.search(r"\b(Kak|Bu|Pak|Mbak|Mas|Ibu|Bapak)\s+[A-Z]\.(?=[\s,;)]|$)", t):
        masalah.append("inisial pelanggan (mis. 'Kak S.') di balasan; ganti 'pelanggan di P-nomor'")
    m = RE_INISIAL_P.search(t)
    if m:
        masalah.append("inisial di depan kode percakapan ('%s. (P..)'); tulis 'pelanggan di P-nomor' saja" % m.group(1))
    sudah = {n.lower() for n in daftar_nama}
    for m in RE_NAMA_TERSIRAT.finditer(t):
        kata = m.group(1) or m.group(2)
        if kata not in BUKAN_NAMA_TERSIRAT and kata.lower() not in sudah:
            masalah.append("kemungkinan nama pelanggan '%s' di balasan (mis. di pertanyaan); bila memang nama, ganti "
                           "'pelanggan di P-nomor'; bila bukan nama, tulis ulang kalimatnya" % kata)
            break
    if h and h.get("dinilai"):
        semua = persen_di_balasan(t)
        nyata = h["lolos_persen"]
        tertulis = {}
        for k, v in semua:
            tertulis.setdefault(k, v)
            if k in nyata and abs(v - nyata[k]) > 0.05:
                masalah.append("%s tertulis %s, hitungan %s" % (k, persen_id(v), persen_id(nyata[k])))
        kurang = [k for k in KRITERIA if k not in tertulis]
        if kurang:
            masalah.append("persen kriteria belum tertulis: " + ", ".join(kurang))
        if len(set(tertulis.values())) == 1 and len(tertulis) == len(KRITERIA) and len(set(nyata.values())) > 1:
            masalah.append("semua kriteria ditulis sama persen, padahal hitungan berbeda-beda")
        bersih = "%d dari %d" % (h["percakapan_bersih"], h["dinilai"])
        if not re.search(AWAL_ANGKA + r"%d\s+dari\s+%d" % (h["percakapan_bersih"], h["dinilai"]) + AKHIR_ANGKA, t):
            masalah.append("percakapan bersih '%s' belum tertulis" % bersih)
        if baris_tr and h.get("baris_tren") and h["baris_tren"].split(":", 1)[1].strip() not in baris_tr[0]:
            masalah.append("baris tren beda dengan hitungan; salin persis: " + h["baris_tren"])
    return masalah


def baca_draf(sumber):
    if sumber == "-":
        return sys.stdin.read()
    with open(sumber, "rb") as f:
        mentah = f.read()
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            return mentah.decode(enc)
        except UnicodeError:
            continue
    return ""


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hitung angka rapor mingguan karyawan AI")
    ap.add_argument("berkas", nargs="?", help="berkas percakapan (.txt berpenanda #gagal atau .csv); boleh diganti --nilai")
    ap.add_argument("--nilai", default="", help='daftar penilaian: "P1=lolos; P2=nyambung,panjang; P3=fakta,janji"; '
                    "'-' = stdin, '@berkas.txt' = dari berkas (untuk daftar panjang)")
    ap.add_argument("--tahap", choices=list(TARGET), default="minggu2-4")
    ap.add_argument("--lama", default="", help='rapor lama: "fakta=80,nyambung=90" atau berkas JSON keluaran sebelumnya')
    ap.add_argument("--lama-jawaban", default="",
                    help="teks rapor minggu lalu apa adanya (baris 'Angka tren', tabel, atau kalimat); '-' = stdin")
    ap.add_argument("--cek-balasan", default="", help="periksa draf balasan (berkas teks atau '-' = stdin)")
    ap.add_argument("--bot", default="", help="nama tampilan bot, pisahkan dengan koma")
    ap.add_argument("--samarkan-nama", default="", help="nama pelanggan yang harus disamarkan, pisahkan dengan koma")
    ap.add_argument("--maks-panjang", type=int, default=700, help="batas karakter satu balasan bot (default 700)")
    ap.add_argument("--json", action="store_true", help="keluarkan JSON saja")
    a = ap.parse_args(argv)
    dari_stdin = [n for n, v in (("--nilai", a.nilai), ("--lama-jawaban", a.lama_jawaban),
                                 ("--cek-balasan", a.cek_balasan)) if v.strip() == "-"]
    if len(dari_stdin) > 1:
        print("%s tidak bisa sama-sama dari stdin ('-'); pakai berkas untuk salah satunya." % " dan ".join(dari_stdin),
              file=sys.stderr)
        return 2
    if a.nilai.strip() == "-":
        a.nilai = sys.stdin.read()
    elif a.nilai.strip().startswith("@"):
        try:
            a.nilai = baca_draf(a.nilai.strip()[1:])
        except OSError as e:
            print("Berkas daftar penilaian tidak bisa dibuka: %s" % e, file=sys.stderr)
            return 2
    peringatan = []
    lama = {}
    if a.lama_jawaban.strip():
        teks_lama = sys.stdin.read() if a.lama_jawaban.strip() == "-" else a.lama_jawaban
        lama = baca_lama_teks(teks_lama, peringatan)
    lama_opsi = baca_lama(a.lama)
    if lama and lama_opsi and set(lama) & set(lama_opsi):
        peringatan.append("rapor lama diberi dua kali (--lama dan --lama-jawaban); angka --lama dipakai")
    lama.update(lama_opsi)
    nama_opsi = [x.strip() for x in a.samarkan_nama.split(",") if x.strip()]
    if a.nilai.strip():
        nama_kode = []
        cs = parse_nilai(a.nilai, peringatan, nama_kode)
        if not cs:
            print("Daftar penilaian kosong. Contoh: --nilai \"P1=lolos; P2=nyambung,panjang\"", file=sys.stderr)
            return 2
        cs_berkas = []
        if a.berkas:
            cs_berkas, kode = baca_berkas(a.berkas, a.bot, [])
            if kode:
                return kode
        h = hitung(cs, a.tahap, lama, a.maks_panjang, nama_opsi + nama_kode, peringatan)
        return selesai(h, a, nama_opsi + nama_kode + nama_terdeteksi(cs_berkas), cs_berkas)
    if not a.berkas:
        print("Berikan berkas percakapan atau --nilai \"P1=lolos; P2=nyambung\".", file=sys.stderr)
        return 2
    cs, kode = baca_berkas(a.berkas, a.bot, peringatan)
    if kode:
        return kode
    nama = nama_opsi + nama_terdeteksi(cs)
    h = hitung(cs, a.tahap, lama, a.maks_panjang, nama, peringatan)
    return selesai(h, a, nama, cs)


def selesai(h, a, nama, cs):
    if not a.cek_balasan:
        return tampilkan(h, a.json)
    try:
        draf = baca_draf(a.cek_balasan)
    except OSError as e:
        print("Draf balasan tidak bisa dibuka: %s" % e, file=sys.stderr)
        return 2
    nomor = [m.group(0) for c in cs for _, t in c["turn"] for m in RE_HP.finditer(t)]
    angka = [m.group(0) for c in cs for r_, t in c["turn"] if r_ == "pelanggan" for m in RE_ANGKA_PANJANG.finditer(t)]
    masalah = cek_balasan(draf, h, nama, nomor, angka)
    if a.json:
        print(json.dumps({"versi": VERSI, "siap_kirim": not masalah, "masalah": masalah,
                          "panjang": len(draf.strip())}, ensure_ascii=False, indent=2))
    else:
        print("=== UNTUK AGENT SAJA: cek draf balasan ===")
        print("cek balasan: OK, siap kirim (%d karakter)" % len(draf.strip()) if not masalah
              else "cek balasan: PERBAIKI DULU ->\n- " + "\n- ".join(masalah))
        print("=== AKHIR BLOK ===")
    return 0 if not masalah else 1


def baca_berkas(path, bot, peringatan):
    """Baca berkas percakapan -> (daftar percakapan, kode keluar). Kode 0 = berhasil."""
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except OSError as e:
        print("Berkas tidak bisa dibuka: %s" % e, file=sys.stderr)
        return [], 2
    teks = None
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeError:
            continue
    if teks is None or not teks.strip():
        print("Berkas kosong atau bukan teks.", file=sys.stderr)
        return [], 2
    bot_ekstra = {b.strip().lower() for b in bot.split(",") if b.strip()}
    pertama = teks.lstrip().splitlines()[0].lower() if teks.strip() else ""
    csvlike = path.lower().endswith(".csv") or ("," in pertama and any(w in pertama for w in ("pelanggan", "pesan", "bot")) and "---" not in teks)
    try:
        cs = parse_csv(teks, bot_ekstra, peringatan) if csvlike else parse_teks(teks, bot_ekstra, peringatan)
    except csv.Error as e:
        print("CSV rusak: %s" % e, file=sys.stderr)
        return [], 2
    for i, c in enumerate(cs, 1):
        if not c["id"]:
            c["id"] = "P%d" % i
    if not cs:
        print("Tidak ada percakapan yang bisa dibaca. Pisahkan tiap percakapan dengan baris '---'.", file=sys.stderr)
        return [], 2
    return cs, 0


def tampilkan(h, hanya_json):
    if hanya_json:
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        print(blok_agent(h))
        print("--- JSON ---")
        print(json.dumps(h, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
