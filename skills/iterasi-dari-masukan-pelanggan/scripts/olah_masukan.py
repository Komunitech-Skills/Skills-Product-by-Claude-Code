#!/usr/bin/env python3
"""Olah masukan pelanggan dari BANYAK kanal (chat WhatsApp hasil ekspor, ulasan marketplace,
komentar IG/TikTok, survei) menjadi angka & daftar isu teratas.

Yang dilakukan (deterministik, bisa diulang, tanpa jaringan, Python 3.8+ standar):
1. Membaca: ekspor chat WhatsApp (.txt), CSV (ulasan/survei), atau teks tempelan (satu masukan per baris
   atau dipisah baris kosong).
2. MENYAMARKAN data pribadi otomatis SEBELUM analisis: nama pengirim chat, nomor HP, email, tautan,
   @username, nomor pesanan/resi, alamat jalan, sapaan+nama ("kak Budi"). Kolom nama pembeli di CSV
   tidak pernah dibaca. Teks asli tidak pernah dicetak/disimpan.
3. Menandai tema (rasa, kemasan, harga, pengiriman, layanan, ...) dan sentimen per klausa
   (dipecah di "tapi", "namun", tanda baca), termasuk negasi ("tidak enak", "tidak telat").
4. Menghitung: jumlah per kanal, sentimen, keluhan/pujian/saran per tema, tren per bulan,
   skor prioritas = jumlah keluhan x dampak, dan tabel isu teratas.

Klasifikasi tema dari kata kunci hanyalah KANDIDAT; agent/manusia wajib memverifikasi lewat kutipan.

Contoh:
  python3 olah_masukan.py chat-wa.txt=WhatsApp ulasan.csv=Shopee komentar.txt=Instagram --staf "Admin,Dapur"
  python3 olah_masukan.py chat-wa.txt --daftar-pengirim
  python3 olah_masukan.py ulasan.csv --tema tema-saya.json --format json --simpan-anonim anonim.csv
"""
import argparse
import csv
import io
import json
import re
import sys
from collections import Counter, defaultdict

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

VERSI = "1.0.0"

# ------------------------------------------------------------------ kamus bawaan
SLANG = {
    "brg": "barang", "bgt": "banget", "bngt": "banget", "gk": "tidak", "ga": "tidak", "gak": "tidak",
    "nggak": "tidak", "ngga": "tidak", "engga": "tidak", "enggak": "tidak", "tdk": "tidak", "yg": "yang",
    "udh": "sudah", "udah": "sudah", "sdh": "sudah", "krn": "karena", "karna": "karena", "sm": "sama",
    "dr": "dari", "jg": "juga", "blm": "belum", "lbh": "lebih", "dtg": "datang", "tp": "tapi",
    "sy": "saya", "bgs": "bagus", "mantul": "mantap", "mantab": "mantap", "mantaap": "mantap",
    "trims": "terima kasih", "makasih": "terima kasih", "thx": "terima kasih", "tks": "terima kasih",
    "kadaluarsa": "kedaluwarsa", "kadaluwarsa": "kedaluwarsa", "expired": "kedaluwarsa", "exp": "kedaluwarsa",
    "telatt": "telat", "lamaa": "lama", "enaak": "enak", "enakk": "enak", "murmer": "murah", "rekomen": "recommended",
    "recomended": "recommended", "cs": "layanan", "adm": "admin", "ongkir": "ongkir", "gmn": "bagaimana",
    "kmrn": "kemarin", "org": "orang", "aja": "saja", "udh": "sudah", "pesenan": "pesanan", "pesen": "pesan",
}
FRASA = [
    (r"\btidak\s+ada\s+minus\b|\btanpa\s+minus\b", "tanpaminus"),
    (r"\btidak\s+sesuai\s+(?:pesanan|order)\b|\bsalah\s+pesan(?:an)?\b", "salahpesanan"),
    (r"\btidak\s+sesuai\b|\bga\s+sesuai\b|\bbeda\s+(?:dengan|sama|dari)\b", "tidaksesuai"),
    (r"\bfast\s*respon\w*|\brespon(?:s|nya)?\s+cepat\b|\bcepat\s+tanggap\b|\bgercep\b", "responscepat"),
    (r"\bslow\s*respon\w*|\brespon(?:s|nya)?\s+lambat\b|\blama\s+(?:dibalas|balasnya|responnya)\b", "responslambat"),
    (r"\border\s+lagi\b|\brepeat\s+order\b|\bbeli\s+lagi\b|\bpesan\s+lagi\b|\blangganan\b", "orderlagi"),
    (r"\btepat\s+waktu\b|\bon\s*time\b", "tepatwaktu"),
    (r"\bworth\s*it\b|\bsepadan\b", "sepadan"),
    (r"\bsold\s*out\b", "habis"),
    (r"\bsakit\s+perut\b", "sakitperut"),
    (r"\bbenda\s+asing\b", "bendaasing"),
    (r"\bsesuai\s+(?:foto|gambar|deskripsi|pesanan|order)\b", "sesuaiharapan"),
]
NEGATOR = {"tidak", "belum", "bukan", "tanpa", "jangan"}
POS = set("""enak lezat mantap bagus puas suka cepat rapi ramah sopan murah terjangkau fresh segar hangat renyah empuk
gurih recommended top oke keren juara pas wangi harum hemat bersih higienis aman kenyang mengenyangkan responsif
responscepat orderlagi tepatwaktu sepadan sesuaiharapan tanpaminus terima kasih""".split())
NEG = set("""telat terlambat lama basi jelek kecewa mahal kurang bocor tumpah rusak salah lambat pelit hambar dingin
tidaksesuai salahpesanan penyok kotor bau amis alot keras gosong mentah jorok judes kasar cuek lupa tertukar ketuker kedaluwarsa
rambut serangga lalat semut ulat kecoa jamur berjamur cacat luntur sakitperut mual diare keracunan komplain marah zonk
tipu penipu habis kosong kehabisan ribet susah sulit masalah parah mengecewakan buruk kekecilan sedikit responslambat
bendaasing lecet retak patah""".split())
SARAN = re.compile(r"\b(sebaiknya|semoga\s+ada|tolong\s+(?:ditambah|tambah|dibuat|dibuatkan|diperbaiki|dibenahi)|mohon|kalau\s+bisa|"
                   r"usul|saran|request|harap|kapan\s+(?:ada|ready|buka)|bisa\s+tidak|boleh\s+tidak|tambahin|ditambah|dibuatkan)\b")

# id, label, dampak (1-5), pola
TEMA_BAWAAN = [
    ("rasa", "Rasa / cita rasa", 4, r"rasa|enak|lezat|gurih|hambar|asin|manis|pedas|pahit|amis|gosong|mentah|renyah|empuk|alot|bumbu|nendang|kematangan"),
    ("kemasan", "Kemasan / packing", 3, r"kemasan|packing|pack|bungkus|dus|kardus|box|kotak|plastik|bubblewrap|bocor|tumpah|penyok|segel|wadah|rapi"),
    ("harga", "Harga / ongkir", 2, r"harga|mahal|murah|terjangkau|ongkir|diskon|promo|sepadan|biaya|tarif|hemat|pricey"),
    ("pengiriman", "Pengiriman / ketepatan waktu", 3, r"kirim|pengiriman|kurir|ojol|ojek|gojek|grab|telat|terlambat|datang|sampai|antar|diantar|tepatwaktu|delivery|resi|ekspedisi|menunggu|nunggu|dingin|hangat"),
    ("layanan", "Layanan / respons admin", 3, r"admin|layanan|pelayanan|respons|responscepat|responslambat|balas|ramah|sopan|kasar|judes|cuek|staf|pegawai|karyawan|kasir|pelayan|komplain|ditanggapi"),
    ("ketepatan_pesanan", "Ketepatan pesanan", 4, r"salah\s+(?:kirim|pesan|item|ambil|isi)|ketuker|tertukar|kurang\s+(?:item|satu|dua)|tidak\s+lengkap|kelupaan|lupa\s+dimasukkan|salahpesanan"),
    ("kualitas_produk", "Kualitas produk (barang)", 4, r"kualitas|bahan|jahitan|awet|rusak|cacat|luntur|sesuaiharapan|patah|retak|lecet|berfungsi|tidaksesuai"),
    ("keamanan_kebersihan", "Keamanan pangan / kebersihan", 5, r"basi|bau|kedaluwarsa|rambut|serangga|lalat|semut|ulat|kecoa|bendaasing|kotor|jorok|higienis|bersih|sakitperut|diare|keracunan|mual|alergi|jamur|berjamur"),
    ("porsi_ukuran", "Porsi / ukuran", 3, r"porsi|ukuran|size|kekecilan|kebesaran|pelit|kenyang|mengenyangkan|gramasi"),
    ("stok_ketersediaan", "Stok / ketersediaan", 2, r"habis|kosong|stok|stock|ready|preorder|antre|antri|penuh|kehabisan"),
    ("pembayaran", "Pembayaran / refund", 3, r"bayar|pembayaran|transfer|qris|cod|refund|pengembalian|kembalian|tagihan|invoice|nota|struk"),
    ("varian_menu", "Varian / menu / pilihan", 2, r"varian|menu|pilihan|paket"),
]

# ------------------------------------------------------------------ penyamaran
RE_URL = re.compile(r"(?:https?://|www\.)\S+|\b(?:wa\.me|bit\.ly|shp\.ee|tokopedia\.link|vt\.tiktok\.com)/\S+", re.I)
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
RE_HP = re.compile(r"(?<![\w/])(?:\+?62|0)[\s.-]?8\d{1,2}[\s.-]?\d{3,4}[\s.-]?\d{2,5}(?!\d)")
RE_USER = re.compile(r"(?<![\w.])@[A-Za-z0-9_.]{2,}")
RE_NOPESAN = re.compile(r"\b(?:inv|invoice|order|pesanan|resi|no\.?\s*(?:pesanan|order|resi|inv))\s*[:#.\-]?\s*(?=[A-Za-z0-9\-/]*\d)[A-Za-z0-9\-/]{5,}\b", re.I)
RE_KODE = re.compile(r"\b(?=[A-Za-z0-9\-]*\d)(?=[A-Za-z0-9\-]*[A-Za-z])[A-Za-z0-9\-]{8,}\b|\b\d{9,}\b")
RE_ALAMAT = re.compile(r"\b(?:jl|jln|jalan|gg|gang)\.?\s+[^,;\n]{3,40}", re.I)
SAPAAN = r"(?i:kak|kakak|ka|bu|ibu|pak|bapak|mas|mba|mbak|bang|om|tante|bro|sis)"
RE_SAPAAN_NAMA = re.compile(r"\b(" + SAPAAN + r")\s+([A-Z][A-Za-z]{2,})\b")
BUKAN_NAMA = {"Admin", "Seller", "Toko", "Min", "Kasir", "Owner", "Saya", "Aku", "Tolong", "Mau", "Ini", "Itu", "Yang", "Kok", "Bisa",
              "Boleh", "Apakah", "Minta", "Terima", "Terimakasih", "Makasih", "Halo", "Hai", "Selamat", "Maaf", "Pesanan", "Order",
              "Barang", "Paket", "Dapur", "Warung", "Kedai", "Bakery", "Katering", "Kurir", "Driver", "Sudah", "Belum", "Untuk", "Dari", "Pesan", "Kirim", "Nanti", "Besok", "Sama"}
RE_PENGIRIM_MEDIA = re.compile(r"<media[^>]*>|<attached[^>]*>|\(file attached\)|gambar tidak disertakan|video tidak disertakan|stiker tidak disertakan|audio tidak disertakan|dokumen tidak disertakan", re.I)
RE_SISTEM_TEKS = re.compile(r"pesan ini dihapus|you deleted this message|this message was deleted|pesan dihapus|end-to-end|terenkripsi|"
                            r"bergabung menggunakan tautan|telah ditambahkan|meninggalkan grup|mengubah (?:ikon|subjek|deskripsi)|null$", re.I)


def samarkan(teks, nama_pengirim=()):
    t = teks
    for n in sorted(set(nama_pengirim), key=len, reverse=True):
        if len(n) >= 3:
            t = re.sub(r"(?<!\w)" + re.escape(n) + r"(?!\w)", "[nama]", t, flags=re.I)
    t = RE_URL.sub("[tautan]", t)
    t = RE_EMAIL.sub("[email]", t)
    t = RE_HP.sub("[hp]", t)
    t = RE_USER.sub("[akun]", t)
    t = RE_NOPESAN.sub("[nomor]", t)
    t = RE_KODE.sub("[nomor]", t)
    t = RE_ALAMAT.sub("[alamat]", t)
    t = RE_SAPAAN_NAMA.sub(lambda m: m.group(0) if m.group(2) in BUKAN_NAMA else m.group(1) + " [nama]", t)
    return re.sub(r"\s+", " ", t).strip()


# ------------------------------------------------------------------ tanggal
BULAN = {"jan": 1, "januari": 1, "feb": 2, "februari": 2, "mar": 3, "maret": 3, "apr": 4, "april": 4, "mei": 5, "may": 5,
         "jun": 6, "juni": 6, "jul": 7, "juli": 7, "agu": 8, "agt": 8, "agustus": 8, "aug": 8, "sep": 9, "sept": 9, "september": 9,
         "okt": 10, "oktober": 10, "oct": 10, "nov": 11, "november": 11, "des": 12, "desember": 12, "dec": 12}


def bulan_dari(s):
    """Kembalikan 'YYYY-MM' dari string tanggal (dd/mm/yyyy, yyyy-mm-dd, '12 Sep 2026'), atau None."""
    if not s:
        return None
    s = str(s).strip()
    m = re.match(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
    else:
        m = re.match(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})", s)
        if m:
            mo, y = int(m.group(2)), int(m.group(3))
            if y < 100:
                y += 2000
        else:
            m = re.match(r"(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{2,4})", s)
            if not m or m.group(2).lower() not in BULAN:
                return None
            mo, y = BULAN[m.group(2).lower()], int(m.group(3))
            if y < 100:
                y += 2000
    if not (1 <= mo <= 12 and 2000 <= y <= 2100):
        return None
    return "%04d-%02d" % (y, mo)


# ------------------------------------------------------------------ pembacaan
RE_WA1 = re.compile(r"^‎?\[?(\d{1,2}[/.]\d{1,2}[/.]\d{2,4}),?\s+\d{1,2}[.:]\d{2}(?:[.:]\d{2})?(?:\s?[APap][Mm])?\]?\s+-?\s*(.*)$")


def baca_wa(teks, staf, tanpa_sapaan=False):
    """Kembalikan (daftar [(tanggal, pengirim, isi)], Counter pengirim)."""
    pesan = []
    for baris in teks.splitlines():
        baris = baris.replace("‎", "").replace(" ", " ")
        m = RE_WA1.match(baris)
        if m:
            sisa = m.group(2)
            if ": " in sisa:
                pengirim, isi = sisa.split(": ", 1)
                pesan.append([m.group(1), pengirim.strip(), isi])
            else:
                pesan.append([m.group(1), None, sisa])  # pesan sistem
        elif pesan and baris.strip():
            pesan[-1][2] += " " + baris.strip()
    hitung = Counter(p[1] for p in pesan if p[1])
    return pesan, hitung


def kenali_bintang(teks):
    m = re.match(r"^\s*(?:bintang\s*)?([1-5])\s*(?:/\s*5)?\s*[|:\-–]\s*(.+)$", teks, re.I | re.S)
    if m:
        return int(m.group(1)), m.group(2).strip()
    m = re.match(r"^\s*([★⭐]{1,5})\s*(.+)$", teks, re.S)
    if m:
        return len(re.findall("[★⭐]", m.group(1))), m.group(2).strip()
    return None, teks.strip()


def baca_teks_bebas(teks):
    ada_bintang = any(kenali_bintang(b)[0] for b in teks.splitlines() if b.strip())
    if re.search(r"\n\s*\n", teks.strip()) and not ada_bintang:
        blok = [re.sub(r"\s+", " ", b).strip() for b in re.split(r"\n\s*\n", teks)]
    else:
        blok = [b.strip() for b in teks.splitlines()]
    hasil = []
    for b in blok:
        if b:
            bintang, isi = kenali_bintang(b)
            hasil.append((None, bintang, isi))
    return hasil


KOLOM = {
    "teks": ["ulasan", "review", "komentar", "comment", "masukan", "feedback", "isi", "pesan", "text", "teks", "saran", "catatan", "kritik"],
    "bintang": ["bintang", "rating", "star", "skor", "nilai"],
    "tanggal": ["tanggal", "date", "waktu", "time", "created", "dibuat"],
    "kanal": ["kanal", "channel", "platform", "sumber", "source"],
}
KOLOM_NAMA = ("nama", "name", "username", "user", "pembeli", "buyer", "email", "telepon", "phone", "hp", "alamat")


def pilih_kolom(header, jenis, paksa=None):
    if paksa:
        return [h for h in header if h.strip().lower() in [p.strip().lower() for p in paksa.split(",")]]
    low = {h: h.strip().lower() for h in header}
    hasil = []
    for kand in KOLOM[jenis]:
        for h, l in low.items():
            if (l == kand or kand in l) and not any(n in l for n in KOLOM_NAMA) and h not in hasil:
                hasil.append(h)
        if hasil and jenis != "teks":
            break
    return hasil


def baca_csv(teks, kolom_teks=None, kolom_bintang=None, kolom_tanggal=None):
    sampel = teks[:4096]
    try:
        dialek = csv.Sniffer().sniff(sampel, delimiters=",;\t")
    except csv.Error:
        dialek = csv.excel
    pembaca = csv.DictReader(io.StringIO(teks), dialect=dialek)
    header = pembaca.fieldnames or []
    kt = pilih_kolom(header, "teks", kolom_teks)
    kb = pilih_kolom(header, "bintang", kolom_bintang)
    kd = pilih_kolom(header, "tanggal", kolom_tanggal)
    kk = pilih_kolom(header, "kanal")
    baris_semua = list(pembaca)
    if not kt:  # survei dengan judul kolom bebas: pakai kolom berisi kalimat (rata-rata > 8 karakter, bukan angka)
        for h in header:
            if h in kb + kd + kk or any(n in h.lower() for n in KOLOM_NAMA):
                continue
            nilai = [(b.get(h) or "").strip() for b in baris_semua if (b.get(h) or "").strip()]
            if nilai and sum(len(v) for v in nilai) / len(nilai) > 8 and not all(re.fullmatch(r"[\d.,/\- ]+", v) for v in nilai):
                kt.append(h)
    if not kt:
        raise SystemExit("Kolom teks tidak ketemu. Kolom yang ada: %s. Ulangi dengan --kolom-teks \"NAMA\"." % ", ".join(header))
    hasil = []
    for baris in baris_semua:
        bintang = None
        if kb:
            m = re.search(r"[1-5]", str(baris.get(kb[0]) or ""))
            bintang = int(m.group(0)) if m else None
        tgl = baris.get(kd[0]) if kd else None
        kanal = (baris.get(kk[0]) or "").strip() if kk else None
        for k in kt:
            isi = (baris.get(k) or "").strip()
            if isi:
                hasil.append((tgl, bintang, isi, kanal or None))
    return hasil


def baca_berkas(spesifikasi, opsi):
    """spesifikasi: 'berkas' atau 'berkas=Kanal'. Kembalikan (kanal, daftar item mentah, info)."""
    path, _, kanal = spesifikasi.partition("=")
    if path == "-":
        teks = sys.stdin.read()
    else:
        with open(path, "rb") as f:
            mentah = f.read()
        try:
            teks = mentah.decode("utf-8-sig")
        except UnicodeDecodeError:
            teks = mentah.decode("latin-1")
    kanal = kanal.strip() or re.sub(r"\.\w+$", "", path.replace("\\", "/").split("/")[-1]) or "kanal"
    ext = path.lower().rsplit(".", 1)[-1] if "." in path else ""
    info = {"kanal": kanal, "jenis": "teks"}
    if ext in ("csv", "tsv") or (ext not in ("txt",) and "," in teks.split("\n", 1)[0] and len(teks.split("\n", 1)[0].split(",")) >= 2):
        info["jenis"] = "csv"
        return kanal, baca_csv(teks, opsi.kolom_teks, opsi.kolom_bintang, opsi.kolom_tanggal), info, None
    wa, hitung = baca_wa(teks, opsi.staf_list)
    if len(wa) >= 3 and sum(1 for p in wa if p[1]) >= 3 and hitung:
        info["jenis"] = "whatsapp"
        return kanal, wa, info, hitung
    return kanal, baca_teks_bebas(teks), info, None


# ------------------------------------------------------------------ analisis
def normalkan(teks):
    t = teks.lower()
    t = re.sub(r"(.)\1{2,}", r"\1\1", t)  # 'enaaak' -> 'enaak'
    t = re.sub(r"(?<=[a-z])aa+k\b", "ak", t)
    for pola, ganti in FRASA:
        t = re.sub(pola, ganti, t)
    kata = re.findall(r"[\w\[\]]+|[^\w\s]", t)
    return " ".join(SLANG.get(k, k) for k in kata)


def pecah_klausa(t):
    bagian = re.split(r"\s+(?:tapi|namun|cuma|hanya saja|sayang(?:nya)?|sedangkan|padahal)\s+|[.!?;\n]+|,\s+|\s+-\s+", t)
    return [b.strip() for b in bagian if b and re.search(r"\w", b)]


def skor_klausa(klausa, kata_pos, kata_neg):
    tok = re.findall(r"[\w\[\]]+", klausa)
    skor = 0
    for i, k in enumerate(tok):
        nilai = 1 if k in kata_pos else -1 if k in kata_neg else 0
        if nilai and any(x in NEGATOR for x in tok[max(0, i - 2):i]):
            nilai = -nilai
        skor += nilai
    return skor


AFIKS = (r"\b(?:di|ter)?(?:", r")(?:nya|kan|an)?\b")


def buat_tema(konfigurasi):
    tema = [dict(id=i, label=l, dampak=d, pola=re.compile(AFIKS[0] + p + AFIKS[1])) for i, l, d, p in TEMA_BAWAAN]
    kata_pos, kata_neg = set(POS), set(NEG)
    if konfigurasi:
        if konfigurasi.get("ganti_tema"):
            tema = []
        for t in konfigurasi.get("tema", []):
            pola = "|".join(t.get("kata", []))
            if not pola:
                continue
            baru = dict(id=t["id"], label=t.get("label", t["id"]), dampak=int(t.get("dampak", 3)),
                        pola=re.compile(AFIKS[0] + pola + AFIKS[1], re.I))
            tema = [x for x in tema if x["id"] != baru["id"]] + [baru]
        kata_pos |= {k.lower() for k in konfigurasi.get("kata_positif", [])}
        kata_neg |= {k.lower() for k in konfigurasi.get("kata_negatif", [])}
    return tema, kata_pos, kata_neg


def analisis_item(teks_anonim, bintang, tema, kata_pos, kata_neg):
    """Kembalikan (sentimen_pesan, {tema_id: set(jenis)})"""
    klausa = pecah_klausa(normalkan(teks_anonim))
    total = 0
    per_tema = defaultdict(set)
    for k in klausa:
        s = skor_klausa(k, kata_pos, kata_neg)
        total += s
        if s > 0:
            jenis = "pujian"
        elif s < 0:
            jenis = "keluhan"
        elif bintang is not None and bintang <= 2:
            jenis = "keluhan"
        elif bintang is not None and bintang >= 4:
            jenis = "pujian"
        else:
            jenis = "netral"
        if jenis != "keluhan" and SARAN.search(k):
            jenis = "saran"
        for t in tema:
            if t["pola"].search(k):
                per_tema[t["id"]].add(jenis)
    if bintang is not None:
        sent = "positif" if bintang >= 4 else "netral" if bintang == 3 else "negatif"
    else:
        sent = "positif" if total > 0 else "negatif" if total < 0 else "netral"
    return sent, per_tema


def potong(t, n=140):
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


STOP = set("""yang dan di ke dari untuk dengan ini itu saya kami kita kak ya nya juga sudah tidak tapi atau ada pada saja
lagi sama karena jadi bisa mau akan sih deh dong kok banget terima kasih nama hp nomor tautan akun email alamat""".split())


def olah(sumber, opsi, konfigurasi=None):
    tema, kata_pos, kata_neg = buat_tema(konfigurasi)
    item = []      # dict anonim
    dilihat = set()
    dibuang = Counter()
    pengirim_semua = {}
    for spes in sumber:
        kanal, mentah, info, hitung = baca_berkas(spes, opsi)
        if info["jenis"] == "whatsapp":
            nama = list(hitung)
            pengirim_semua[kanal] = hitung
            tokens_nama = set(nama) | {n.split()[0] for n in nama if n.split()}
            staf = [s.lower() for s in opsi.staf_list]
            for tgl, pengirim, isi in mentah:
                if pengirim is None or RE_SISTEM_TEKS.search(isi) or RE_PENGIRIM_MEDIA.fullmatch(isi.strip()):
                    dibuang["pesan sistem/media"] += 1
                    continue
                if any(s in pengirim.lower() for s in staf):
                    dibuang["pesan staf"] += 1
                    continue
                isi = RE_PENGIRIM_MEDIA.sub("", isi).strip()
                if len(re.findall(r"\w+", isi)) < 2:
                    dibuang["terlalu pendek"] += 1
                    continue
                item.append((kanal, tgl, None, isi, tokens_nama))
        else:
            for baris in mentah:
                tgl, bintang, isi = baris[0], baris[1], baris[2]
                kn = baris[3] if len(baris) > 3 and baris[3] else kanal
                item.append((kn, tgl, bintang, isi, ()))
    hasil_item = []
    for kanal, tgl, bintang, isi, nama in item:
        anonim = samarkan(isi, nama)
        kunci = (kanal, re.sub(r"\W+", " ", anonim.lower()).strip())
        if not kunci[1] or len(re.findall(r"\w+", kunci[1])) < 2:
            dibuang["terlalu pendek"] += 1
            continue
        if kunci in dilihat:
            dibuang["duplikat"] += 1
            continue
        dilihat.add(kunci)
        sent, per_tema = analisis_item(anonim, bintang, tema, kata_pos, kata_neg)
        hasil_item.append({"kanal": kanal, "bulan": bulan_dari(tgl), "bintang": bintang, "teks": anonim,
                           "sentimen": sent, "tema": {k: sorted(v) for k, v in per_tema.items()}})
    return hasil_item, tema, dict(dibuang), pengirim_semua


def ringkas(hasil_item, tema, dibuang, opsi):
    n = len(hasil_item)
    kanal = Counter(i["kanal"] for i in hasil_item)
    sent = Counter(i["sentimen"] for i in hasil_item)
    bulan = Counter(i["bulan"] for i in hasil_item if i["bulan"])
    bulan_n = dict(sorted(bulan.items()))
    daftar = []
    for t in tema:
        rows = [i for i in hasil_item if t["id"] in i["tema"]]
        if not rows:
            continue
        k = [i for i in rows if "keluhan" in i["tema"][t["id"]]]
        p = [i for i in rows if "pujian" in i["tema"][t["id"]]]
        s = [i for i in rows if "saran" in i["tema"][t["id"]]]
        bintang_k = [i["bintang"] for i in k if i["bintang"] is not None]
        tren = {}
        for b in bulan_n:
            tren[b] = {"masukan": bulan_n[b], "keluhan": sum(1 for i in k if i["bulan"] == b)}
        arah = "data kurang"
        bl = list(bulan_n)
        if len(bl) >= 2 and bulan_n[bl[-1]] >= opsi.min_bulan and bulan_n[bl[-2]] >= opsi.min_bulan:
            a = tren[bl[-2]]["keluhan"] * 100.0 / bulan_n[bl[-2]]
            b_ = tren[bl[-1]]["keluhan"] * 100.0 / bulan_n[bl[-1]]
            selisih = round(b_ - a, 1)
            arah = "naik" if selisih >= 2 else "turun" if selisih <= -2 else "stabil"
            tren_sel = selisih
        else:
            tren_sel = None
        contoh = sorted(k, key=lambda i: (i["bintang"] if i["bintang"] is not None else 3, len(i["teks"])))[: opsi.contoh]
        contoh_p = [i for i in p][: opsi.contoh]
        daftar.append({
            "id": t["id"], "label": t["label"], "dampak": t["dampak"],
            "masukan": len(rows), "keluhan": len(k), "pujian": len(p), "saran": len(s),
            "persen_keluhan": round(len(k) * 100.0 / n, 1) if n else 0.0,
            "kanal": sorted({i["kanal"] for i in k}),
            "rata_bintang_keluhan": round(sum(bintang_k) / len(bintang_k), 1) if bintang_k else None,
            "skor": len(k) * t["dampak"],
            "arah_tren": arah, "selisih_persen_poin": tren_sel, "tren_per_bulan": tren,
            "contoh_keluhan": [potong(i["teks"]) for i in contoh],
            "contoh_pujian": [potong(i["teks"]) for i in contoh_p],
            "contoh_saran": [potong(i["teks"]) for i in s][: opsi.contoh],
        })
    maks = max([d["skor"] for d in daftar] + [1])
    for d in daftar:
        if d["keluhan"] and ((d["dampak"] >= 5) or (d["keluhan"] >= 3 and d["skor"] >= 0.5 * maks)):
            d["prioritas"] = "Segera"
        elif d["keluhan"] >= 3:
            d["prioritas"] = "Bulan ini"
        elif d["keluhan"]:
            d["prioritas"] = "Pantau"
        else:
            d["prioritas"] = "-"
    daftar.sort(key=lambda d: (-d["skor"], -d["keluhan"], d["id"]))
    tanpa = [i for i in hasil_item if not i["tema"]]
    kata = Counter(w for i in tanpa for w in re.findall(r"[a-z]{4,}", normalkan(i["teks"])) if w not in STOP)
    return {
        "versi_script": VERSI, "total_masukan": n, "dibuang": dibuang,
        "per_kanal": dict(kanal.most_common()), "sentimen": {k: sent.get(k, 0) for k in ("positif", "netral", "negatif")},
        "per_bulan": bulan_n,
        "tanpa_tanggal": sum(1 for i in hasil_item if not i["bulan"]),
        "tema": daftar,
        "belum_terklasifikasi": {"jumlah": len(tanpa), "persen": round(len(tanpa) * 100.0 / n, 1) if n else 0.0,
                                  "kata_teratas": [k for k, _ in kata.most_common(8)],
                                  "contoh": [potong(i["teks"]) for i in tanpa[:5]]},
    }


def cetak_teks(r, opsi):
    out = []
    n = r["total_masukan"]
    out.append("# Rekap Masukan Pelanggan (%d masukan)\n" % n)
    out.append("Kanal: " + ", ".join("%s %d" % (k, v) for k, v in r["per_kanal"].items()))
    s = r["sentimen"]
    if n:
        out.append("Sentimen: positif %d (%.1f%%), netral %d (%.1f%%), negatif %d (%.1f%%)" % (
            s["positif"], s["positif"] * 100.0 / n, s["netral"], s["netral"] * 100.0 / n, s["negatif"], s["negatif"] * 100.0 / n))
    if r["per_bulan"]:
        out.append("Per bulan: " + ", ".join("%s: %d" % kv for kv in r["per_bulan"].items())
                   + ("; %d tanpa tanggal" % r["tanpa_tanggal"] if r["tanpa_tanggal"] else ""))
    if r["dibuang"]:
        out.append("Tidak dihitung: " + ", ".join("%s %d" % kv for kv in r["dibuang"].items()))
    out.append("\n## Isu teratas (skor = jumlah keluhan x dampak 1-5)\n")
    out.append("| # | Tema | Keluhan (% dari semua) | Pujian | Saran | Dampak | Skor | Tren | Kanal | Prioritas |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for i, d in enumerate([d for d in r["tema"] if d["keluhan"]], 1):
        tren = d["arah_tren"] + (" (%+.1f poin)" % d["selisih_persen_poin"] if d["selisih_persen_poin"] is not None else "")
        out.append("| %d | %s | %d (%.1f%%) | %d | %d | %d | %d | %s | %s | %s |" % (
            i, d["label"], d["keluhan"], d["persen_keluhan"], d["pujian"], d["saran"], d["dampak"], d["skor"], tren,
            ", ".join(d["kanal"]), d["prioritas"]))
    out.append("\n## Kutipan (sudah disamarkan)\n")
    for d in r["tema"]:
        if d["contoh_keluhan"]:
            out.append("**%s** (keluhan)" % d["label"])
            out += ["- \"%s\"" % c for c in d["contoh_keluhan"]]
    saran = [d for d in r["tema"] if d["saran"]]
    if saran:
        out.append("\n## Saran & permintaan\n")
        for d in saran:
            out.append("**%s** (%d)" % (d["label"], d["saran"]))
            out += ["- \"%s\"" % c for c in d["contoh_saran"]]
    out.append("\n## Pujian teratas\n")
    for d in sorted(r["tema"], key=lambda d: -d["pujian"])[:5]:
        if d["pujian"]:
            out.append("- %s: %d masukan" % (d["label"], d["pujian"]))
    b = r["belum_terklasifikasi"]
    out.append("\n## Perlu dibaca agent\n")
    out.append("Tanpa tema terdeteksi: %d (%.1f%%). Kata teratas: %s" % (b["jumlah"], b["persen"], ", ".join(b["kata_teratas"]) or "-"))
    out += ["- \"%s\"" % c for c in b["contoh"]]
    out.append("\nCatatan: tema dari kata kunci = kandidat; verifikasi lewat kutipan. Nama, nomor HP, dll. sudah disamarkan otomatis.")
    return "\n".join(out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Olah masukan pelanggan multi-kanal (anonim, tema, sentimen, tren).")
    ap.add_argument("sumber", nargs="+", help="berkas atau berkas=NamaKanal (.txt chat WhatsApp / tempelan, .csv). '-' = stdin")
    ap.add_argument("--staf", default="", help="Nama pengirim WhatsApp yang dianggap staf/pemilik (dipisah koma); pesannya dilewati")
    ap.add_argument("--daftar-pengirim", action="store_true", help="Tampilkan pengirim chat WhatsApp + jumlah pesan, lalu berhenti")
    ap.add_argument("--kolom-teks", help="Nama kolom teks CSV (boleh beberapa, pisah koma)")
    ap.add_argument("--kolom-bintang")
    ap.add_argument("--kolom-tanggal")
    ap.add_argument("--tema", help="File JSON tema/kata tambahan (lihat templates/tema-contoh.json)")
    ap.add_argument("--contoh", type=int, default=3)
    ap.add_argument("--min-bulan", type=int, default=5, help="Minimal masukan per bulan agar tren dihitung (default 5)")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    ap.add_argument("--simpan-anonim", help="Simpan data yang SUDAH disamarkan ke CSV ini (kanal,bulan,bintang,sentimen,tema,teks)")
    opsi = ap.parse_args(argv)
    opsi.staf_list = [s.strip() for s in opsi.staf.split(",") if s.strip()]
    konfigurasi = None
    if opsi.tema:
        with open(opsi.tema, encoding="utf-8") as f:
            konfigurasi = json.load(f)
    if opsi.daftar_pengirim:
        for spes in opsi.sumber:
            _, _, info, hitung = baca_berkas(spes, opsi)
            if hitung:
                print("Pengirim di %s (nama hanya untuk Anda, jangan disalin ke laporan):" % spes)
                for nama, c in hitung.most_common():
                    print("  %s: %d pesan" % (nama, c))
            else:
                print("%s: bukan ekspor chat WhatsApp (tidak ada pengirim)." % spes)
        return 0
    hasil_item, tema, dibuang, _ = olah(opsi.sumber, opsi, konfigurasi)
    if not hasil_item:
        print("Tidak ada masukan yang bisa dibaca. Periksa format berkas / kolom teks.", file=sys.stderr)
        return 2
    r = ringkas(hasil_item, tema, dibuang, opsi)
    if opsi.simpan_anonim:
        with open(opsi.simpan_anonim, "w", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            w.writerow(["kanal", "bulan", "bintang", "sentimen", "tema", "teks"])
            for i in hasil_item:
                w.writerow([i["kanal"], i["bulan"] or "", i["bintang"] or "", i["sentimen"], ";".join(sorted(i["tema"])), i["teks"]])
    print(json.dumps(r, ensure_ascii=False, indent=2) if opsi.format == "json" else cetak_teks(r, opsi))
    return 0


if __name__ == "__main__":
    sys.exit(main())
