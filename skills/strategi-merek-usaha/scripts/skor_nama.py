#!/usr/bin/env python3
"""Skor & urutkan calon nama usaha/produk dengan matriks berbobot (Python standar saja).

Pakai:
  python3 scripts/skor_nama.py nama.csv --merek "Indomie, Kopi Kenangan"
  python3 scripts/skor_nama.py nama.csv --merek-file merek.txt --bobot "kemiripan=30,khas=10"
  python3 scripts/skor_nama.py nama.csv --format json
  python3 scripts/skor_nama.py --hitung "Sambal Nusa"      # panjang & suku kata satu nama
(Windows: ganti python3 dengan python atau py.)

CSV: kolom `nama` (wajib) + kolom penilaian manual 1-5 (kosong = 3, ditandai "belum dinilai"):
  aman_makna  5 = tidak ada arti negatif/lucu di bahasa Indonesia, daerah, atau slang
  khas        5 = jelas beda dari pesaing yang dikenal
  relevan     5 = langsung mengingatkan pada produk/manfaat
Otomatis dihitung script: panjang, suku_kata, ejaan, kemiripan (terhadap daftar merek yang DIBERIKAN pengguna).
Bobot awal (jumlah 100): panjang 10, suku_kata 10, ejaan 10, kemiripan 20, aman_makna 20, khas 15, relevan 15.
Skor = jumlah(bobot x nilai) / jumlah(bobot) x 20 -> skala 0-100. Bobot memakai TITIK untuk desimal.
Nama dengan koma wajib diberi tanda kutip di CSV.
Tanda TANDAI (nama tidak boleh dipilih sebelum diperiksa): kemiripan terlalu tinggi dengan merek yang diberikan
(ejaan ATAU bunyi kira-kira), mirip kata Inggris umum berkonotasi buruk (daftar KATA_INGGRIS_BURUK), atau
aman_makna = 1. Kemiripan bunyi memakai normalisasi sederhana (c/q/ck->k, ph/v->f, z->s, x->ks, ee/ea->i,
oo->u, y akhir->i, -s jamak dibuang, huruf ganda dirapatkan), jadi "Kicks Klin" ~ "Kick Clean" tertangkap.
Script TIDAK memeriksa ketersediaan domain/handle/merek terdaftar dan tidak benar-benar mendengar bunyi.
Dua nama teratas selisih <= 5 poin = SETARA.
Keluar kode 0 bila sukses, 2 bila input salah (pesan jelas di stderr).
"""
import argparse
import csv
import difflib
import json
import re
import sys

KRITERIA = ["panjang", "suku_kata", "ejaan", "kemiripan", "aman_makna", "khas", "relevan"]
MANUAL = ["aman_makna", "khas", "relevan"]
BOBOT_AWAL = {"panjang": 10, "suku_kata": 10, "ejaan": 10, "kemiripan": 20,
              "aman_makna": 20, "khas": 15, "relevan": 15}
BATAS_SERI = 5.0
MAKS_NAMA = 100
VOKAL = set("aiueo")
DIFTONG = ("ai", "au", "oi", "eu")  # eu = vokal Sunda (Seulas = seu-las)
GENERIK_BAWAAN = ("kopi", "teh", "toko", "warung", "kedai", "depot", "rumah", "cafe", "kafe", "resto",
                  "restoran", "bengkel", "laundry", "salon", "studio", "jaya", "abadi", "mandiri", "makmur")

# Kata umum bahasa Inggris yang berkonotasi buruk/vulgar. Nama yang bunyinya mirip (mis. "Sneakuy" ~ "sneaky" =
# licik) ditandai untuk diperiksa. Daftar sengaja ringkas; arti di bahasa daerah tetap dicek manual (aman_makna).
KATA_INGGRIS_BURUK = {
    "sneaky": "licik/diam-diam", "sly": "licik", "shady": "mencurigakan",
    "sketchy": "meragukan", "dodgy": "meragukan", "cheat": "curang", "scam": "penipuan", "fake": "palsu",
    "phony": "palsu", "bogus": "palsu", "liar": "pembohong", "fraud": "penipuan", "cheap": "murahan",
    "trash": "sampah", "junk": "rongsokan", "rotten": "busuk", "stinky": "bau busuk", "stink": "bau busuk",
    "smelly": "bau", "dirty": "kotor", "filthy": "jorok", "gross": "menjijikkan", "nasty": "menjijikkan",
    "messy": "berantakan", "sloppy": "asal-asalan", "lazy": "malas", "ugly": "jelek", "dumb": "bodoh",
    "stupid": "bodoh", "idiot": "bodoh", "loser": "pecundang", "broke": "bangkrut/rusak", "broken": "rusak",
    "sick": "sakit", "dead": "mati", "die": "mati", "kill": "membunuh", "killer": "pembunuh",
    "poison": "racun", "toxic": "beracun", "evil": "jahat", "devil": "setan", "hell": "neraka",
    "creepy": "seram/mesum", "greedy": "rakus", "sucks": "payah", "suck": "payah", "crap": "kotoran (kasar)",
    "poop": "tinja", "shit": "kotoran (kasar)", "piss": "air kencing (kasar)", "fart": "kentut",
    "vomit": "muntah", "puke": "muntah", "damn": "umpatan", "bitch": "umpatan kasar", "fuck": "umpatan kasar",
    "slut": "umpatan kasar", "porn": "pornografi", "drug": "narkoba", "weed": "ganja",
}
BATAS_BUNYI_BURUK = 0.85


class InputSalah(Exception):
    pass


def huruf(teks):
    return re.sub(r"[^a-z]", "", teks.lower())


def suku_kata_kata(kata):
    """Hitung suku kata satu kata. Tiap huruf vokal = 1 suku kata, kecuali diftong ai/au/oi/eu
    (dihitung 1). Kata tanpa vokal (singkatan mis. BCA) dibaca per huruf."""
    k = re.sub(r"[^a-z]", "", kata.lower())
    if not k:
        return 0
    if not any(c in VOKAL for c in k):
        return len(k)
    n, i = 0, 0
    while i < len(k):
        if k[i] in VOKAL:
            n += 1
            if k[i:i + 2] in DIFTONG:
                i += 1
        i += 1
    return n


def suku_kata(nama):
    return sum(suku_kata_kata(k) for k in re.split(r"\s+", nama.strip()) if k)


def skor_panjang(n):
    if n < 3:
        return 2
    if n <= 8:
        return 5
    if n <= 10:
        return 4
    if n <= 12:
        return 3
    if n <= 15:
        return 2
    return 1


def skor_suku(n):
    if n in (2, 3):
        return 5
    if n == 4:
        return 4
    if n == 1:
        return 3
    if n == 5:
        return 2
    return 1


def skor_ejaan(nama):
    """5 = mudah dieja. Kurangi: angka/simbol (-2), huruf sama 3x berturut (-1),
    3 konsonan berturut di luar ng/ny/sy/kh (-1), huruf q/x (-1). Minimum 1."""
    s, alasan = 5, []
    if re.search(r"[^A-Za-z\s]", nama):
        s -= 2
        alasan.append("ada angka/simbol")
    low = nama.lower()
    if re.search(r"([a-z])\1\1", low):
        s -= 1
        alasan.append("huruf sama 3x")
    bersih = re.sub(r"ng|ny|sy|kh|gh", "a", low)
    if re.search(r"[bcdfghjklmnpqrstvwxyz]{3}", re.sub(r"[^a-z]", " ", bersih)):
        s -= 1
        alasan.append("3 konsonan berturut")
    if re.search(r"[qx]", low):
        s -= 1
        alasan.append("huruf q/x")
    return max(s, 1), alasan


def tanpa_generik(teks, generik):
    """Buang kata generik (per kata utuh) dari teks; hasil huruf saja."""
    sisa = [k for k in re.split(r"\s+", teks.strip()) if huruf(k) not in generik]
    return huruf(" ".join(sisa))


def bunyi_kata(kata):
    """Normalisasi bunyi kira-kira satu kata (lintas ejaan Indonesia/Inggris), huruf saja."""
    k = huruf(kata).replace("z", "s")
    if len(k) > 3 and k.endswith("s") and k[-2] not in VOKAL and k[-2] != "s":
        k = k[:-1]                      # jamak Inggris: kicks/kickz -> kick (bukan "bagus", "gendis")
    for a, b in (("ph", "f"), ("ck", "k"), ("qu", "kw"), ("ee", "i"), ("ea", "i"), ("oo", "u"),
                 ("c", "k"), ("q", "k"), ("x", "ks"), ("v", "f")):
        k = k.replace(a, b)
    if len(k) > 2 and k.endswith("y") and k[-2] not in VOKAL:
        k = k[:-1] + "i"                # sneaky -> sniki
    elif len(k) > 2 and k.endswith("y"):
        k = k[:-1] + "i"                # -uy/-ay/-oy: sneakuy -> snikui
    k = re.sub(r"([a-z])\1+", r"\1", k)  # huruf ganda dirapatkan
    return k


def bunyi(teks):
    return "".join(bunyi_kata(w) for w in re.split(r"\s+", teks.strip()) if huruf(w))


def kata_khas(teks, generik):
    return [w for w in re.split(r"\s+", teks.strip()) if huruf(w) and huruf(w) not in generik]


def rasio_pasangan(a, b):
    r = difflib.SequenceMatcher(None, a, b).ratio()
    if min(len(a), len(b)) >= 4 and (a in b or b in a):
        r = max(r, 0.9)
    return r


def kemiripan(nama, merek, generik=()):
    """Kembalikan (skor 1-5, merek paling mirip, rasio, jenis). Rasio = difflib, nilai tertinggi dari
    (a) ejaan huruf saja dan (b) bunyi kira-kira (`bunyi`). Bila SEMUA kata khas merek muncul (bunyinya)
    sebagai kata di nama (mis. "Fresh Kickz" memuat "Kick"), rasio dianggap >= 0,9.
    Kata generik (kopi, toko, ...) dibuang dari kedua sisi sebelum dibandingkan; merek yang seluruhnya
    generik dilewati; nama yang seluruhnya generik dibandingkan apa adanya."""
    generik = {huruf(g) for g in generik}
    a = tanpa_generik(nama, generik) or huruf(nama)
    kata_a = kata_khas(nama, generik) or [nama]
    a_bunyi = "".join(bunyi_kata(w) for w in kata_a)
    set_a = {bunyi_kata(w) for w in kata_a}
    terbaik, rasio_max, jenis_max = "", 0.0, "ejaan"
    for m in merek:
        b = tanpa_generik(m, generik)
        if not a or not b:
            continue
        r_ejaan = rasio_pasangan(a, b)
        kata_b = kata_khas(m, generik)
        b_bunyi = "".join(bunyi_kata(w) for w in kata_b)
        # bunyi hanya dibandingkan utuh bila keduanya >= 4 huruf (bentuk pendek terlalu mudah "mirip")
        r_bunyi = rasio_pasangan(a_bunyi, b_bunyi) if min(len(a_bunyi), len(b_bunyi)) >= 4 else 0.0
        set_b = {bunyi_kata(w) for w in kata_b}
        if set_b and all(len(w) >= 3 for w in set_b) and set_b <= set_a:
            r_bunyi = max(r_bunyi, 0.9)
        r, jenis = (r_ejaan, "ejaan") if r_ejaan >= r_bunyi else (r_bunyi, "bunyi")
        if r > rasio_max:
            rasio_max, terbaik, jenis_max = r, m, jenis
    if rasio_max >= 0.85:
        s = 1
    elif rasio_max >= 0.75:
        s = 2
    elif rasio_max >= 0.65:
        s = 3
    elif rasio_max >= 0.5:
        s = 4
    else:
        s = 5
    return s, terbaik, rasio_max, jenis_max


def cek_kata_buruk(nama):
    """Cari kata Inggris berkonotasi buruk yang ejaan/bunyinya mirip nama (per kata dan nama utuh).
    Kembalikan daftar (kata, arti, rasio)."""
    kandidat = [w for w in re.split(r"\s+", nama.strip()) if huruf(w)]
    if len(kandidat) > 1:
        kandidat.append(nama)
    temuan = {}
    for w in kandidat:
        hw, bw = huruf(w), (bunyi(w) if " " in w else bunyi_kata(w))
        for kata, arti in KATA_INGGRIS_BURUK.items():
            bk = bunyi_kata(kata)
            r = max(difflib.SequenceMatcher(None, hw, kata).ratio(), difflib.SequenceMatcher(None, bw, bk).ratio())
            if hw == kata or bw == bk:
                r = 1.0
            elif len(kata) < 5:
                continue                # kata pendek (die, hell, sick): hanya bila sama persis ejaan/bunyinya
            if r >= BATAS_BUNYI_BURUK and min(len(hw), len(kata)) >= 3:
                if r > temuan.get(kata, (None, 0))[1]:
                    temuan[kata] = (arti, r)
    return sorted(((k, a, r) for k, (a, r) in temuan.items()), key=lambda x: -x[2])


def baca_bobot(teks):
    bobot = dict(BOBOT_AWAL)
    if not teks:
        return bobot
    for bagian in teks.split(","):
        if not bagian.strip():
            continue
        if "=" not in bagian:
            raise InputSalah(f"bobot '{bagian.strip()}' harus berbentuk kriteria=angka")
        k, v = (x.strip() for x in bagian.split("=", 1))
        if k not in KRITERIA:
            raise InputSalah(f"kriteria bobot '{k}' tidak dikenal. Pilihan: {', '.join(KRITERIA)}")
        try:
            angka = float(v)
        except ValueError:
            raise InputSalah(f"bobot '{k}' bukan angka: '{v}' (desimal pakai titik)")
        if angka != angka or angka in (float("inf"), float("-inf")) or angka < 0:
            raise InputSalah(f"bobot '{k}' harus angka 0 atau lebih")
        bobot[k] = angka
    if sum(bobot.values()) <= 0:
        raise InputSalah("jumlah bobot harus lebih dari 0")
    return bobot


def daftar_merek(teks, path):
    hasil = []
    if teks:
        hasil += [x.strip() for x in re.split(r"[,;\n]", teks) if x.strip()]
    if path:
        try:
            with open(path, encoding="utf-8-sig") as f:
                hasil += [x.strip() for x in f.read().splitlines() if x.strip()]
        except (OSError, UnicodeDecodeError) as e:
            raise InputSalah(f"tidak bisa membaca file merek '{path}': {e}")
    return hasil


def baca_csv(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            baris = list(csv.reader(f))
    except (OSError, UnicodeDecodeError) as e:
        raise InputSalah(f"tidak bisa membaca '{path}': {e} (simpan CSV sebagai UTF-8)")
    baris = [b for b in baris if any(c.strip() for c in b)]
    if not baris:
        raise InputSalah("file CSV kosong")
    kepala = [h.strip().lower() for h in baris[0]]
    if "nama" not in kepala:
        raise InputSalah("kolom 'nama' tidak ada di baris pertama CSV")
    for h in kepala:
        if h != "nama" and h not in MANUAL:
            raise InputSalah(f"kolom '{h}' tidak dikenal. Kolom boleh: nama, {', '.join(MANUAL)}")
    if len(set(kepala)) != len(kepala):
        raise InputSalah("ada kolom ganda di baris pertama CSV")
    data = []
    for no, b in enumerate(baris[1:], start=2):
        if len(b) > len(kepala):
            raise InputSalah(f"baris {no}: kolom lebih banyak dari judul (nama berkoma harus diberi tanda kutip)")
        b = b + [""] * (len(kepala) - len(b))
        r = dict(zip(kepala, (c.strip() for c in b)))
        if not r["nama"]:
            raise InputSalah(f"baris {no}: nama kosong")
        for k in MANUAL:
            v = r.get(k, "")
            if v == "":
                r[k] = None
                continue
            try:
                x = float(v)
            except ValueError:
                raise InputSalah(f"baris {no}: '{k}' bukan angka: '{v}'")
            if x != int(x) or not 1 <= x <= 5:
                raise InputSalah(f"baris {no}: '{k}' harus bilangan bulat 1-5, bukan '{v}'")
            r[k] = int(x)
        data.append(r)
    if not data:
        raise InputSalah("CSV tidak berisi nama (hanya judul kolom)")
    if len(data) > MAKS_NAMA:
        raise InputSalah(f"terlalu banyak nama ({len(data)}); maksimal {MAKS_NAMA}")
    lihat = {}
    for r in data:
        kunci = huruf(r["nama"]) or r["nama"].lower()
        if kunci in lihat:
            raise InputSalah(f"nama ganda: '{lihat[kunci]}' dan '{r['nama']}'")
        lihat[kunci] = r["nama"]
    return data


def nilai(data, merek, bobot, generik=()):
    hasil = []
    total_bobot = sum(bobot.values())
    for r in data:
        nama = r["nama"]
        if not huruf(nama):
            raise InputSalah(f"nama '{nama}' tidak berisi huruf; beri nama dengan huruf")
        nilai_k, catatan, tandai = {}, [], []
        nilai_k["panjang"] = skor_panjang(len(huruf(nama)))
        sk = suku_kata(nama)
        nilai_k["suku_kata"] = skor_suku(sk)
        e, alasan = skor_ejaan(nama)
        nilai_k["ejaan"] = e
        if alasan:
            catatan.append("ejaan: " + ", ".join(alasan))
        if merek:
            m, terdekat, rasio, jenis = kemiripan(nama, merek, generik)
            nilai_k["kemiripan"] = m
            if m <= 2:
                catatan.append(f"mirip '{terdekat}' ({rasio:.0%} {jenis})")
            if m == 1:
                tandai.append(f"terlalu mirip '{terdekat}'" + (" (bunyi)" if jenis == "bunyi" else ""))
        else:
            nilai_k["kemiripan"] = 3
            catatan.append("kemiripan belum diperiksa (tidak ada daftar merek)")
        for k in MANUAL:
            if r[k] is None:
                nilai_k[k] = 3
                catatan.append(f"{k} belum dinilai (dianggap 3)")
            else:
                nilai_k[k] = r[k]
        if nilai_k["aman_makna"] == 1:
            tandai.append("arti/konotasi negatif")
        buruk = cek_kata_buruk(nama)
        if buruk:
            k0, arti0, _ = buruk[0]
            tandai.append(f"bunyi/ejaan mirip kata Inggris '{k0}' ({arti0})")
        skor = sum(bobot[k] * nilai_k[k] for k in KRITERIA) / total_bobot * 20
        hasil.append({"nama": nama, "huruf": len(huruf(nama)), "suku_kata": sk, "nilai": nilai_k,
                      "skor": round(skor, 1), "tandai": tandai, "catatan": catatan})
    hasil.sort(key=lambda x: (-x["skor"], x["nama"].lower()))
    layak = [x for x in hasil if not x["tandai"]]
    seri = len(layak) >= 2 and (layak[0]["skor"] - layak[1]["skor"]) <= BATAS_SERI
    return hasil, seri


def cetak_teks(hasil, seri, bobot, merek, generik):
    print(f"Bobot: " + ", ".join(f"{k}={bobot[k]:g}" for k in KRITERIA))
    print(f"Merek pembanding: {', '.join(merek) if merek else '(tidak ada)'}")
    if generik and merek:
        print(f"Kata generik diabaikan saat cek kemiripan: {', '.join(generik)}")
    print()
    print(f"{'#':>2}  {'Nama':<24}{'Skor':>6}  {'Huruf':>5} {'Suku':>4}  Status / catatan")
    for i, x in enumerate(hasil, 1):
        st = "TANDAI: " + "; ".join(x["tandai"]) if x["tandai"] else "layak dicek"
        cat = ("; " + "; ".join(x["catatan"])) if x["catatan"] else ""
        print(f"{i:>2}  {x['nama'][:23]:<24}{x['skor']:>6.1f}  {x['huruf']:>5} {x['suku_kata']:>4}  {st}{cat}")
    layak = [x for x in hasil if not x["tandai"]]
    print()
    if not layak:
        print("Semua nama ditandai. Buat opsi baru.")
    elif seri:
        print(f"SETARA: '{layak[0]['nama']}' dan '{layak[1]['nama']}' selisih <= {BATAS_SERI:g} poin. "
              "Pilih lewat uji ucap ke 5 orang dan cek ketersediaan.")
    else:
        print(f"Teratas yang layak dicek: '{layak[0]['nama']}' ({layak[0]['skor']:.1f}/100).")
    print("Ingat: skor ini bukan bukti nama tersedia. Cek domain, handle, dan merek (PDKI) sendiri.")


def hitung_satu(nama):
    if not huruf(nama):
        raise InputSalah(f"nama '{nama}' tidak berisi huruf; beri nama dengan huruf")
    e, alasan = skor_ejaan(nama)
    print(f"Nama: {nama}")
    print(f"Huruf (tanpa spasi/simbol): {len(huruf(nama))}; suku kata: {suku_kata(nama)}")
    print(f"Skor panjang {skor_panjang(len(huruf(nama)))}, suku kata {skor_suku(suku_kata(nama))}, "
          f"ejaan {e}" + (f" ({', '.join(alasan)})" if alasan else ""))


def main(argv=None):
    p = argparse.ArgumentParser(description="Skor calon nama usaha/produk", allow_abbrev=False)
    p.add_argument("csv", nargs="?", help="file CSV calon nama")
    p.add_argument("--merek", default="", help="merek yang ingin dibandingkan, dipisah koma")
    p.add_argument("--merek-file", default="", help="file teks berisi satu merek per baris")
    p.add_argument("--generik", default="", help='kata umum tambahan yang diabaikan saat cek kemiripan, mis. "sambal,nasi"')
    p.add_argument("--tanpa-generik", action="store_true", help="matikan daftar kata generik bawaan (kopi, toko, warung, ...)")
    p.add_argument("--bobot", default="", help='mis. "kemiripan=30,khas=10"')
    p.add_argument("--format", choices=["teks", "json", "csv"], default="teks")
    p.add_argument("--hitung", default="", help="hitung panjang & suku kata satu nama")
    try:
        a = p.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code else 0
    try:
        if a.hitung:
            hitung_satu(a.hitung)
            return 0
        if not a.csv:
            raise InputSalah('sebutkan file CSV calon nama, atau pakai --hitung "nama"')
        bobot = baca_bobot(a.bobot)
        merek = daftar_merek(a.merek, a.merek_file)
        generik = ([] if a.tanpa_generik else list(GENERIK_BAWAAN)) + [x.strip().lower() for x in re.split(r"[,;]", a.generik) if x.strip()]
        hasil, seri = nilai(baca_csv(a.csv), merek, bobot, generik)
    except InputSalah as e:
        print(f"GAGAL: {e}", file=sys.stderr)
        return 2
    if a.format == "json":
        print(json.dumps({"bobot": bobot, "merek": merek, "generik": generik, "seri": seri, "hasil": hasil},
                         ensure_ascii=False, indent=2))
    elif a.format == "csv":
        w = csv.writer(sys.stdout, lineterminator="\n")
        w.writerow(["peringkat", "nama", "skor"] + KRITERIA + ["status"])
        for i, x in enumerate(hasil, 1):
            w.writerow([i, x["nama"], x["skor"]] + [x["nilai"][k] for k in KRITERIA]
                       + ["TANDAI: " + "; ".join(x["tandai"]) if x["tandai"] else "layak dicek"])
    else:
        cetak_teks(hasil, seri, bobot, merek, generik)
    return 0


if __name__ == "__main__":
    sys.exit(main())
