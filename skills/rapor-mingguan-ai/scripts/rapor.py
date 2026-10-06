#!/usr/bin/env python3
"""Hitung angka rapor mingguan karyawan AI. Python standar saja.

Pakai: python3 rapor.py percakapan.txt [--tahap minggu1|minggu2-4|bulan2+] [--lama "fakta=80,nyambung=90"]
       [--bot "Nama Bot"] [--samarkan-nama "Sari,Budi"] [--json]
Windows: python atau py.

Format teks: satu percakapan per blok, dipisah baris '---'. Baris 'Pelanggan: ...' dan 'Bot: ...'.
Penilaian manual (opsional) di dalam blok:  #gagal: konteks, panjang   (atau '#gagal: lolos')
CSV: kolom id, pelanggan, bot, gagal, catatan (atau id, peran, pesan, gagal, catatan).
Keluaran: blok angka bertanda UNTUK AGENT SAJA + JSON. Skrip tidak membaca apa pun selain berkas yang diberikan.
"""
import argparse
import csv
import io
import json
import re
import sys

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
}
TARGET = {"minggu1": 60, "minggu2-4": 75, "bulan2+": 90}
TAHAP_NAMA = {"minggu1": "minggu 1 (masih bayi)", "minggu2-4": "minggu 2-4 (belajar)", "bulan2+": "bulan 2 ke atas (dewasa)"}
ROLE_PELANGGAN = {"pelanggan", "customer", "user", "cust", "klien", "pasien", "calon klien", "tamu", "pembeli", "member", "murid", "siswa"}
ROLE_BOT = {"bot", "ai", "asisten", "assistant", "karyawan ai", "admin bot", "balasan bot", "balasan"}
RE_HP = re.compile(r"(?<!\d)(?:\+?62|0)[\s\-.]?8\d[\d\s\-.]{6,12}\d(?!\d)")
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
RE_ANGKA_PANJANG = re.compile(r"(?<!\d)\d{10,}(?!\d)")
RE_SAPA = re.compile(r"\b(Kak|Bu|Pak|Bapak|Ibu|Mbak|Mas|Bang|Dok|Kakak)\s+([A-Z][a-z]{2,})")
RE_TEKNIS = re.compile(
    r"\b(script|file|path|json|exec|token|api key|apikey|prompt|sistem prompt|agents\.md|knowledge|gateway|openclaw|"
    r"error|debug|database|session|model bahasa|sebagai ai|sebagai model)\b|\.py\b|\.md\b|/home/|\.json\b",
    re.I)
RE_JANJI = re.compile(
    r"\b(pasti|dijamin|jaminan|garansi|100\s?%|sembuh|pasti untung|uang kembali|refund|gratis|diskon \d+|cicilan 0|dalam 1 jam|hari ini juga)\b", re.I)


def samarkan(teks, nama_ekstra=()):
    def hp(m):
        d = re.sub(r"\D", "", m.group(0))
        return d[:4] + "-xxxx-" + d[-4:] if len(d) >= 9 else "[nomor]"
    teks = RE_EMAIL.sub("[email]", teks)
    teks = RE_HP.sub(hp, teks)
    teks = RE_ANGKA_PANJANG.sub("[angka panjang]", teks)
    teks = RE_SAPA.sub(lambda m: m.group(1) + " [nama]", teks)
    for n in nama_ekstra:
        if n:
            teks = re.sub(re.escape(n), "[nama]", teks, flags=re.I)
    return teks


def kode_kriteria(teks, peringatan):
    hasil = []
    for bagian in re.split(r"[,;/]+", teks):
        k = bagian.strip().lower().replace(" ", "_").replace("-", "_")
        if not k or k in ("lolos", "ok", "tidak_ada", "none", "0"):
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
        c = {"id": None, "turn": [], "gagal": None, "catatan": ""}
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
                m = re.match(r"^([^:：]{1,30}?)\s*[:：]\s*(.*)$", s)
                r = peran(m.group(1), bot_ekstra) if m else None
                if r:
                    c["turn"].append([r, m.group(2)])
                elif c["turn"]:
                    c["turn"][-1][1] += " " + s
                elif m and re.match(r"^[A-Za-z][\w ]{0,24}$", m.group(1)):
                    c["turn"].append(["pelanggan", m.group(2)])
                else:
                    c["turn"].append(["pelanggan", s])
        if c["turn"]:
            hasil.append(c)
    return hasil


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


def hitung(cs, tahap, lama, maks_panjang, nama_ekstra, peringatan):
    dinilai = [c for c in cs if c["gagal"] is not None]
    belum = [c for c in cs if c["gagal"] is None]
    n = len(dinilai)
    gagal = {k: [c for c in dinilai if k in c["gagal"]] for k in KRITERIA}
    lolos = {k: (round(100.0 * (n - len(gagal[k])) / n, 1) if n else None) for k in KRITERIA}
    kriteria = []
    for k in KRITERIA:
        row = {"kode": k, "nama": NAMA[k], "kritis": k in KRITIS, "gagal": len(gagal[k]), "lolos_persen": lolos[k],
               "nilai": predikat(lolos[k], k in KRITIS) if n else None}
        if n and k not in KRITIS:
            row["target_tahap"] = TARGET[tahap]
            row["vs_target"] = "di atas" if lolos[k] > TARGET[tahap] else "sesuai" if lolos[k] == TARGET[tahap] else "di bawah"
        if k in lama and lolos[k] is not None:
            row["lama_persen"] = lama[k]
            row["selisih_poin"] = round(lolos[k] - lama[k], 1)
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
    rata = round(sum(v for v in lolos.values() if v is not None) / len(KRITERIA), 1) if n else None
    kena_kritis = [k for k in KRITIS if gagal[k]]
    umum = predikat(rata, False) if n else None
    if umum in ("A", "B") and kena_kritis:
        umum = "C"
    sudah_bersih = sum(1 for c in dinilai if not c["gagal"])
    peringatan = list(peringatan)
    if n and n < 10:
        peringatan.append("hanya %d percakapan dinilai: nilai bersifat indikatif, jangan ditarik kesimpulan besar" % n)
    if not n:
        peringatan.append("belum ada penilaian: tidak ada angka yang bisa dihitung")
    if belum:
        peringatan.append("%d percakapan belum dinilai (tanpa baris #gagal) dan tidak dihitung" % len(belum))
    tak_tercatat = []
    for c in dinilai:
        ekstra = [k for k in dugaan(c, maks_panjang) if k not in c["gagal"]]
        if ekstra:
            tak_tercatat.append({"id": c["id"] or "-", "dugaan": ekstra})
    dugaan_belum = [{"id": c["id"] or "-", "dugaan": dugaan(c, maks_panjang)} for c in belum if dugaan(c, maks_panjang)]
    return {
        "tahap": tahap, "tahap_nama": TAHAP_NAMA[tahap], "percakapan_total": len(cs), "dinilai": n,
        "belum_dinilai": len(belum), "percakapan_bersih": sudah_bersih,
        "bersih_persen": round(100.0 * sudah_bersih / n, 1) if n else None,
        "rata_lolos_persen": rata, "nilai_umum": umum, "kriteria": kriteria,
        "lolos_persen": {k: lolos[k] for k in KRITERIA if lolos[k] is not None},
        "tiga_kesalahan_teratas": top, "kena_kriteria_kritis": sorted(kena_kritis, key=KRITERIA.index),
        "ada_rapor_lama": bool(lama),
        "dugaan_tak_tercatat_pada_yang_dinilai": tak_tercatat, "dugaan_pada_yang_belum_dinilai": dugaan_belum,
        "peringatan": peringatan,
    }


def blok_agent(h):
    L = ["=== UNTUK AGENT SAJA: jangan ditempel ke pengguna, tulis ulang dengan bahasa biasa ===",
         "tahap: %s | dinilai: %d dari %d | bersih (tanpa kesalahan): %s | rata lolos: %s | nilai umum: %s"
         % (h["tahap_nama"], h["dinilai"], h["percakapan_total"],
            "-" if h["bersih_persen"] is None else "%s%%" % h["bersih_persen"],
            "-" if h["rata_lolos_persen"] is None else "%s%%" % h["rata_lolos_persen"], h["nilai_umum"] or "-")]
    for k in h["kriteria"]:
        s = "%-9s %-28s gagal %d | lolos %s | nilai %s" % (
            k["kode"], k["nama"], k["gagal"], "-" if k["lolos_persen"] is None else "%s%%" % k["lolos_persen"], k["nilai"] or "-")
        if "vs_target" in k:
            s += " | target %d%% (%s)" % (k["target_tahap"], k["vs_target"])
        if "selisih_poin" in k:
            s += " | minggu lalu %s%% (%+g poin)" % (k["lama_persen"], k["selisih_poin"])
        L.append(s)
    for i, t in enumerate(h["tiga_kesalahan_teratas"], 1):
        ex = "; ".join("%s: \"%s\"" % (e["id"], e["pelanggan_awal"]) for e in t["contoh"])
        L.append("kesalahan #%d: %s (%d percakapan) contoh %s" % (i, t["nama"], t["jumlah"], ex))
    if h["kena_kriteria_kritis"]:
        L.append("kritis kena: " + ", ".join(h["kena_kriteria_kritis"]) + " -> wajib masuk keputusan pemilik")
    for d in h["dugaan_tak_tercatat_pada_yang_dinilai"]:
        L.append("dugaan belum tercatat %s: %s (periksa ulang)" % (d["id"], ",".join(d["dugaan"])))
    for d in h["dugaan_pada_yang_belum_dinilai"]:
        L.append("belum dinilai, dugaan %s: %s" % (d["id"], ",".join(d["dugaan"])))
    for p in h["peringatan"]:
        L.append("peringatan: " + p)
    L.append("=== AKHIR BLOK ===")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Hitung angka rapor mingguan karyawan AI")
    ap.add_argument("berkas")
    ap.add_argument("--tahap", choices=list(TARGET), default="minggu2-4")
    ap.add_argument("--lama", default="", help='rapor lama: "fakta=80,nyambung=90" atau berkas JSON keluaran sebelumnya')
    ap.add_argument("--bot", default="", help="nama tampilan bot, pisahkan dengan koma")
    ap.add_argument("--samarkan-nama", default="", help="nama pelanggan yang harus disamarkan, pisahkan dengan koma")
    ap.add_argument("--maks-panjang", type=int, default=700, help="batas karakter satu balasan bot (default 700)")
    ap.add_argument("--json", action="store_true", help="keluarkan JSON saja")
    a = ap.parse_args(argv)
    try:
        with open(a.berkas, "rb") as f:
            mentah = f.read()
    except OSError as e:
        print("Berkas tidak bisa dibuka: %s" % e, file=sys.stderr)
        return 2
    teks = None
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeError:
            continue
    if teks is None or not teks.strip():
        print("Berkas kosong atau bukan teks.", file=sys.stderr)
        return 2
    peringatan = []
    bot_ekstra = {b.strip().lower() for b in a.bot.split(",") if b.strip()}
    pertama = teks.lstrip().splitlines()[0].lower() if teks.strip() else ""
    csvlike = a.berkas.lower().endswith(".csv") or ("," in pertama and any(w in pertama for w in ("pelanggan", "pesan", "bot")) and "---" not in teks)
    try:
        cs = parse_csv(teks, bot_ekstra, peringatan) if csvlike else parse_teks(teks, bot_ekstra, peringatan)
    except csv.Error as e:
        print("CSV rusak: %s" % e, file=sys.stderr)
        return 2
    for i, c in enumerate(cs, 1):
        if not c["id"]:
            c["id"] = "P%d" % i
    if not cs:
        print("Tidak ada percakapan yang bisa dibaca. Pisahkan tiap percakapan dengan baris '---'.", file=sys.stderr)
        return 2
    h = hitung(cs, a.tahap, baca_lama(a.lama), a.maks_panjang,
               [x.strip() for x in a.samarkan_nama.split(",")], peringatan)
    if a.json:
        print(json.dumps(h, ensure_ascii=False, indent=2))
    else:
        print(blok_agent(h))
        print("--- JSON ---")
        print(json.dumps(h, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
