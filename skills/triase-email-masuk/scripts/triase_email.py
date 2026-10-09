#!/usr/bin/env python3
"""Pra-pilah email untuk skill triase-email-masuk. Python standar saja, tanpa jaringan.

Pakai: python3 scripts/triase_email.py <folder|berkas> [--format json|ringkas] [--sekarang YYYY-MM-DD]
                                        [--keluar laporan.json]
Windows: python atau py. Input: folder berisi .eml/.txt, satu .eml/.mbox, atau CSV
(kolom from/dari, subject/subjek, date/tanggal, body/isi). Hanya membaca; tidak membuka tautan,
tidak mengirim apa pun. Hasilnya dugaan kata kunci: agent tetap harus membaca emailnya sendiri.
"""
import argparse
import csv
import email
import json
import mailbox
import re
import sys
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
from email import policy
from email.utils import parseaddr, parsedate_to_datetime
from pathlib import Path
from urllib.parse import urlparse

BULAN = {"januari": 1, "jan": 1, "februari": 2, "feb": 2, "maret": 3, "mar": 3, "april": 4, "apr": 4,
         "mei": 5, "juni": 6, "jun": 6, "juli": 7, "jul": 7, "agustus": 8, "agu": 8, "agt": 8, "ags": 8,
         "september": 9, "sep": 9, "sept": 9, "oktober": 10, "okt": 10, "november": 11, "nov": 11,
         "desember": 12, "des": 12,
         "january": 1, "february": 2, "march": 3, "may": 5, "june": 6, "july": 7, "august": 8,
         "aug": 8, "october": 10, "oct": 10, "december": 12, "dec": 12}
HARI = {"senin": 0, "selasa": 1, "rabu": 2, "kamis": 3, "jumat": 4, "jum'at": 4, "sabtu": 5, "minggu": 6}
BATAS_ISI = 200_000  # karakter per email yang dibaca

KATA_MENDESAK = ["segera", "urgent", "asap", "mendesak", "hari ini juga", "secepatnya", "paling lambat",
                 "batas akhir", "deadline", "jatuh tempo", "terakhir", "sebelum jam"]
KATA_TAGIHAN = ["invoice", "faktur", "tagihan", "pembayaran", "bayar", "jatuh tempo", "transfer",
                "outstanding", "overdue", "kwitansi", "bukti bayar", "nomor rekening", "pelunasan", "dp "]
KATA_PROMO = ["diskon", "promo", "flash sale", "newsletter", "unsubscribe", "berhenti berlangganan",
              "webinar", "penawaran spesial", "cashback", "gratis ongkir", "voucher", "hadiah"]
KATA_MINTA = ["mohon", "tolong", "bisa", "apakah", "konfirmasi", "kabari", "balas", "tanggapan",
              "dikirimkan", "mohon dikirim", "minta", "?", "please", "could you", "kindly"]
KATA_INFO = ["fyi", "untuk informasi", "pemberitahuan", "notifikasi", "pengumuman", "laporan otomatis"]
KATA_DATA_SENSITIF = ["password", "kata sandi", "otp", "kode verifikasi", "pin ", "cvv", "nomor kartu",
                      "data rekening", "ktp", "login", "masuk ke akun", "verifikasi akun", "konfirmasi akun"]
KATA_ANCAMAN = ["diblokir", "ditangguhkan", "dinonaktifkan", "dibekukan", "akan ditutup", "suspended",
                "locked", "terkunci", "denda", "tindakan hukum", "kedaluwarsa"]
KATA_TRANSFER_MENDESAK = ["transfer ke rekening", "ganti rekening", "rekening baru", "rekening berubah",
                          "pindah rekening", "ubah nomor rekening", "bayar ke rekening", "gift card",
                          "voucher google play", "pulsa"]
PEMENDEK = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "cutt.ly", "is.gd", "rb.gy", "s.id", "shorturl.at",
            "ow.ly", "tiny.cc", "rebrand.ly"}
MEREK = {"bca": ["bca.co.id", "klikbca.com"], "mandiri": ["bankmandiri.co.id", "livin.co.id"],
         "bri": ["bri.co.id"], "bni": ["bni.co.id"], "paypal": ["paypal.com"], "google": ["google.com"],
         "shopee": ["shopee.co.id", "shopee.com"], "tokopedia": ["tokopedia.com"],
         "tiktok": ["tiktok.com"], "microsoft": ["microsoft.com"], "dhl": ["dhl.com"],
         "jne": ["jne.co.id"], "gojek": ["gojek.com"], "grab": ["grab.com"],
         "djp": ["pajak.go.id"], "pajak": ["pajak.go.id"], "bpjs": ["bpjs-kesehatan.go.id", "bpjsketenagakerjaan.go.id"]}
TLD_RISIKO = (".xyz", ".top", ".click", ".icu", ".work", ".zip", ".mov", ".tk", ".ml", ".ga", ".cf", ".gq", ".buzz")
DOMAIN_UMUM = {"gmail.com", "yahoo.com", "yahoo.co.id", "outlook.com", "hotmail.com", "icloud.com", "ymail.com"}

RE_URL = re.compile(r"https?://[^\s<>\")\]]+|www\.[^\s<>\")\]]+", re.I)
RE_RP = re.compile(r"(?:rp\.?|idr)\s*([0-9][0-9\.,]*)\s*(juta|jt|ribu|rb|k|miliar|m)?\b|"
                   r"\b([0-9][0-9\.,]*)\s*(juta|jt|ribu|rb)\b", re.I)
RE_TGL_TEKS = re.compile(r"\b(\d{1,2})\s+([A-Za-z]{3,9})\.?\s*(\d{4})?\b")
RE_TGL_ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
RE_TGL_SLASH = re.compile(r"\b(\d{1,2})[/-](\d{1,2})[/-](\d{4})\b")
RE_RELATIF = re.compile(r"\b(hari ini|besok lusa|besok|lusa|minggu depan|akhir pekan|akhir bulan|"
                        r"dalam\s+\d+\s+hari|\d+\s+hari lagi|(?:hari\s+)?(?:senin|selasa|rabu|kamis|jum'?at|sabtu)"
                        r"(?:\s+depan|\s+ini)?|jam\s+\d{1,2}[.:]\d{2}|pukul\s+\d{1,2}[.:]\d{2})\b", re.I)


def angka_rupiah(angka, satuan):
    s = angka.strip(".,")
    if not s:
        return None
    satuan = (satuan or "").lower()
    try:
        if satuan in ("juta", "jt", "miliar", "m") and re.fullmatch(r"\d+[.,]\d{1,2}", s):
            v = Decimal(s.replace(",", "."))
        elif re.fullmatch(r"\d{1,3}([.,]\d{3})+[.,]\d{1,2}", s):
            v = Decimal(re.sub(r"[.,]", "", s[:s.rfind(s[-3] if s[-3] in ".," else s[-2])]))
        elif re.fullmatch(r"\d{1,3}([.,]\d{3})+", s):
            v = Decimal(re.sub(r"[.,]", "", s))
        elif re.fullmatch(r"\d+[.,]\d{1,2}", s):
            v = Decimal(s.replace(",", "."))
        else:
            v = Decimal(re.sub(r"[.,]", "", s))
    except InvalidOperation:
        return None
    kali = {"juta": 10**6, "jt": 10**6, "ribu": 10**3, "rb": 10**3, "k": 10**3, "miliar": 10**9, "m": 10**9}
    v *= kali.get(satuan, 1)
    return int(v)


def cari_nominal(teks):
    hasil = []
    for m in RE_RP.finditer(teks):
        v = angka_rupiah(m.group(1) or m.group(3), m.group(2) or m.group(4))
        if v and v >= 1000 and v not in hasil:
            hasil.append(v)
    return hasil


def cari_tenggat(teks, acuan):
    """Tanggal eksplisit (ISO) + ungkapan relatif apa adanya. Tahun kosong dianggap tahun acuan."""
    tgl = []
    for m in RE_TGL_ISO.finditer(teks):
        _tambah(tgl, m.group(1), m.group(2), m.group(3))
    for m in RE_TGL_SLASH.finditer(teks):
        _tambah(tgl, m.group(3), m.group(2), m.group(1))
    for m in RE_TGL_TEKS.finditer(teks):
        bln = BULAN.get(m.group(2).lower())
        if bln:
            _tambah(tgl, m.group(3) or acuan.year, bln, m.group(1))
    rel = []
    for m in RE_RELATIF.finditer(teks):
        s = re.sub(r"\s+", " ", m.group(0).lower())
        if s not in rel:
            rel.append(s)
    return sorted(set(tgl)), rel[:6]


def _tambah(daftar, y, mth, d):
    try:
        daftar.append(date(int(y), int(mth), int(d)).isoformat())
    except ValueError:
        pass


def domain_dari_url(u):
    if not u.lower().startswith("http"):
        u = "http://" + u
    try:
        host = (urlparse(u).hostname or "").lower().strip(".")
    except ValueError:
        return ""
    return host


def induk(host):
    bagian = host.split(".")
    if len(bagian) >= 3 and ".".join(bagian[-2:]) in {"co.id", "or.id", "go.id", "ac.id", "web.id", "my.id", "com.au", "co.uk"}:
        return ".".join(bagian[-3:])
    return ".".join(bagian[-2:]) if len(bagian) >= 2 else host


def periksa_phishing(pengirim_nama, pengirim_alamat, balas_ke, subjek, isi):
    alasan, skor = [], 0
    dom = pengirim_alamat.split("@")[-1].lower() if "@" in pengirim_alamat else ""
    dom_induk = induk(dom) if dom else ""
    nama_l = (pengirim_nama + " " + subjek).lower()
    for kunci, sah in MEREK.items():
        if re.search(r"\b" + re.escape(kunci) + r"\b", pengirim_nama.lower()) and dom_induk and not any(
                dom_induk == induk(s) for s in sah):
            alasan.append(f"nama pengirim menyebut '{kunci}' tetapi alamatnya dari {dom}")
            skor += 3
            break
    if dom in DOMAIN_UMUM and re.search(r"\b(bank|pajak|djp|bpjs|admin|support|security|keamanan|layanan)\b", pengirim_nama.lower()):
        alasan.append(f"mengaku lembaga/layanan tetapi memakai alamat gratis ({dom})")
        skor += 2
    if dom.endswith(TLD_RISIKO):
        alasan.append(f"domain pengirim berakhiran tidak lazim ({dom})")
        skor += 1
    if dom.startswith("xn--") or ".xn--" in dom:
        alasan.append("domain pengirim memakai penulisan huruf menyerupai (punycode)")
        skor += 2
    if balas_ke and "@" in balas_ke and induk(balas_ke.split("@")[-1].lower()) != dom_induk:
        alasan.append(f"alamat balasan ({balas_ke.split('@')[-1].lower()}) berbeda dari pengirim")
        skor += 2
    tautan = []
    for u in RE_URL.findall(isi):
        h = domain_dari_url(u.rstrip(".,;)"))
        if h and h not in [t["domain"] for t in tautan]:
            tautan.append({"domain": h})
    for t in tautan:
        h = t["domain"]
        t["catatan"] = []
        if h in PEMENDEK:
            t["catatan"].append("tautan dipendekkan, tujuan asli tidak terlihat")
            skor += 1
        if re.fullmatch(r"\d{1,3}(\.\d{1,3}){3}", h):
            t["catatan"].append("berupa alamat angka (IP), bukan nama situs")
            skor += 2
        if h.endswith(TLD_RISIKO):
            t["catatan"].append("akhiran domain tidak lazim")
            skor += 1
        if "xn--" in h:
            t["catatan"].append("penulisan huruf menyerupai (punycode)")
            skor += 2
        if h.count("-") >= 2 or h.count(".") >= 4:
            t["catatan"].append("nama domain panjang/berlapis, mudah menyamar")
            skor += 1
        for kunci, sah in MEREK.items():
            if kunci in h.replace("-", "") and not any(induk(h) == induk(s) for s in sah):
                t["catatan"].append(f"memuat nama '{kunci}' tetapi bukan situs resminya")
                skor += 3
                break
        if dom_induk and induk(h) != dom_induk and h not in PEMENDEK and not t["catatan"]:
            t["catatan"].append("berbeda dari domain pengirim")
    isi_l = (subjek + " " + isi).lower()
    if any(k in isi_l for k in KATA_DATA_SENSITIF):
        alasan.append("meminta data sensitif (kata sandi/OTP/PIN/data akun)")
        skor += 3
    if any(k in isi_l for k in KATA_ANCAMAN) and any(k in isi_l for k in KATA_MENDESAK + ["klik", "tautan", "link"]):
        alasan.append("ancaman akun/layanan ditutup disertai tekanan waktu")
        skor += 2
    if any(k in isi_l for k in KATA_TRANSFER_MENDESAK):
        alasan.append("meminta transfer/mengubah rekening pembayaran (verifikasi lewat telepon ke nomor yang sudah dikenal)")
        skor += 4 if any(k in isi_l for k in ("rekening baru", "ganti rekening", "pindah rekening", "ubah nomor rekening", "rekening berubah")) else 2
    if re.search(r"\b(klik|buka|tekan)\b.{0,30}\b(tautan|link|di sini|disini|tombol)\b", isi_l) and any(
            k in isi_l for k in KATA_DATA_SENSITIF + KATA_ANCAMAN):
        skor += 1
    for t in tautan:
        for c in t["catatan"]:
            if c != "berbeda dari domain pengirim":
                alasan.append(f"tautan ke {t['domain']}: {c}")
    return skor, list(dict.fromkeys(alasan)), tautan


def bersihkan_html(teks):
    if "<html" in teks.lower() or "<body" in teks.lower() or "<div" in teks.lower():
        teks = re.sub(r"(?is)<(script|style).*?</\1>", " ", teks)
        teks = re.sub(r"(?i)href=[\"']([^\"']+)[\"']", r" \1 ", teks)
        teks = re.sub(r"<[^>]+>", " ", teks)
    return re.sub(r"[ \t]+", " ", teks)


def baca_pesan(msg):
    nama, alamat = parseaddr(str(msg.get("From", "")))
    _, balas = parseaddr(str(msg.get("Reply-To", "")))
    tubuh = ""
    try:
        bagian = msg.get_body(preferencelist=("plain", "html")) if hasattr(msg, "get_body") else None
        tubuh = bagian.get_content() if bagian else (msg.get_payload(decode=True) or b"").decode("utf-8", "replace")
    except Exception:
        tubuh = str(msg.get_payload())
    lampiran = []
    if hasattr(msg, "iter_attachments"):
        lampiran = [p.get_filename() or "tanpa-nama" for p in msg.iter_attachments()]
    tgl = None
    try:
        tgl = parsedate_to_datetime(str(msg.get("Date"))).date().isoformat()
    except Exception:
        pass
    return {"nama": nama, "alamat": alamat.lower(), "balas_ke": balas.lower(), "subjek": str(msg.get("Subject", "")),
            "tanggal": tgl, "isi": bersihkan_html(tubuh)[:BATAS_ISI], "lampiran": lampiran}


def baca_csv(path):
    with open(path, "rb") as f:
        mentah = f.read()
    teks = None
    for enc in ("utf-8-sig", "utf-16", "cp1252"):
        try:
            teks = mentah.decode(enc)
            break
        except UnicodeError:
            continue
    if teks is None or "\x00" in teks:
        raise ValueError("berkas CSV tidak bisa dibaca sebagai teks")
    baris = list(csv.DictReader(teks.splitlines(), delimiter=";" if teks.split("\n")[0].count(";") > teks.split("\n")[0].count(",") else ","))
    if not baris:
        return []
    peta = {}
    alias = {"from": ["from", "dari", "pengirim", "sender"], "subject": ["subject", "subjek", "perihal"],
             "date": ["date", "tanggal", "tgl"], "body": ["body", "isi", "pesan", "content", "text"]}
    kolom = {k.strip().lower(): k for k in baris[0].keys() if k}
    for std, al in alias.items():
        for a in al:
            if a in kolom:
                peta[std] = kolom[a]
                break
    if "body" not in peta and "subject" not in peta:
        raise ValueError("CSV harus punya kolom from, subject, date, body (atau dari, subjek, tanggal, isi)")
    hasil = []
    for b in baris:
        nama, alamat = parseaddr(b.get(peta.get("from", ""), "") or "")
        hasil.append({"nama": nama, "alamat": alamat.lower(), "balas_ke": "", "subjek": b.get(peta.get("subject", ""), "") or "",
                      "tanggal": (b.get(peta.get("date", ""), "") or "")[:40] or None,
                      "isi": bersihkan_html(b.get(peta.get("body", ""), "") or "")[:BATAS_ISI], "lampiran": []})
    return hasil


def baca_teks_polos(path):
    teks = Path(path).read_bytes().decode("utf-8", "replace")
    if re.match(r"(?im)^(from|dari):", teks) or re.match(r"(?im)^(subject|subjek):", teks):
        msg = email.message_from_string(teks, policy=policy.default)
        if msg.get("From") or msg.get("Subject"):
            return baca_pesan(msg)
    return {"nama": "", "alamat": "", "balas_ke": "", "subjek": "", "tanggal": None,
            "isi": bersihkan_html(teks)[:BATAS_ISI], "lampiran": []}


def kumpulkan(sumber):
    p = Path(sumber)
    if p.is_dir():
        berkas = sorted(x for x in p.iterdir() if x.suffix.lower() in (".eml", ".txt", ".mbox", ".csv"))
        hasil = []
        for b in berkas:
            hasil.extend(kumpulkan(b))
        return hasil
    if not p.is_file():
        raise FileNotFoundError(f"tidak ada: {sumber}")
    s = p.suffix.lower()
    if s == ".csv":
        return baca_csv(p)
    if s == ".mbox":
        return [baca_pesan(email.message_from_bytes(m.as_bytes(), policy=policy.default)) for m in mailbox.mbox(str(p))]
    if s == ".eml":
        return [baca_pesan(email.message_from_bytes(p.read_bytes(), policy=policy.default))]
    return [baca_teks_polos(p)]


def kategori_dan_prioritas(e, acuan, isi):
    isi_l = (e["subjek"] + " " + isi).lower()
    sinyal = []
    skor_p = 0
    if e["phishing_skor"] >= 4:
        return "phishing dicurigai", "P1-waspada", ["dugaan phishing: jangan klik tautan, jangan balas"]
    mendesak = [k for k in KATA_MENDESAK if k in isi_l]
    if mendesak:
        sinyal.append("kata mendesak: " + ", ".join(mendesak[:3]))
        skor_p += 2
    keluhan = [k for k in ("komplain", "refund", "belum sampai", "kecewa", "batalkan", "lapor", "bintang 1") if k in isi_l]
    if keluhan:
        sinyal.append("nada keluhan: " + ", ".join(keluhan[:3]))
        skor_p += 2
    ada_tenggat = bool(e["tenggat_tanggal"] or e["tenggat_relatif"])
    terdekat = None
    for t in e["tenggat_tanggal"]:
        d = date.fromisoformat(t)
        if terdekat is None or d < terdekat:
            terdekat = d
    if terdekat is not None:
        sel = (terdekat - acuan).days
        if sel < 0:
            sinyal.append(f"tanggal {terdekat.isoformat()} sudah lewat {-sel} hari dari acuan")
            skor_p += 2
        elif sel <= 2:
            sinyal.append(f"tenggat {terdekat.isoformat()} dalam {sel} hari")
            skor_p += 3
        elif sel <= 7:
            sinyal.append(f"tenggat {terdekat.isoformat()} dalam {sel} hari")
            skor_p += 2
        else:
            sinyal.append(f"tanggal disebut {terdekat.isoformat()}")
            skor_p += 1
    elif e["tenggat_relatif"]:
        sinyal.append("tenggat disebut: " + ", ".join(e["tenggat_relatif"][:3]))
        skor_p += 1
    if e["nominal_rp"]:
        sinyal.append("nominal Rp" + f"{max(e['nominal_rp']):,}".replace(",", "."))
        if max(e["nominal_rp"]) >= 10_000_000:
            skor_p += 2
        elif max(e["nominal_rp"]) >= 1_000_000:
            skor_p += 1
    tagihan = any(k in isi_l for k in KATA_TAGIHAN)
    promo = sum(k in isi_l for k in KATA_PROMO)
    minta = any(k in isi_l for k in KATA_MINTA)
    info = any(k in isi_l for k in KATA_INFO)
    if e["phishing_skor"] >= 2:
        sinyal.append("ada tanda mencurigakan ringan; cek sebelum klik")
    if promo >= 2 and not tagihan:
        kat = "promosi/spam"
        skor_p = 0
    elif tagihan and (e["nominal_rp"] or ada_tenggat or "invoice" in isi_l or "tagihan" in isi_l):
        kat = "tagihan/pembayaran"
        skor_p += 1
    elif skor_p >= 4 and (mendesak or terdekat is not None):
        kat = "mendesak"
    elif minta and not info:
        kat = "perlu balasan"
    elif info or not minta:
        kat = "info saja"
    else:
        kat = "perlu balasan"
    if kat == "info saja":
        skor_p = min(skor_p, 1)
    if kat == "promosi/spam":
        pri = "P4"
    elif skor_p >= 5 or kat == "mendesak":
        pri = "P1"
    elif skor_p >= 3:
        pri = "P2"
    elif skor_p >= 1 or kat in ("perlu balasan", "tagihan/pembayaran"):
        pri = "P3"
    else:
        pri = "P4"
    return kat, pri, sinyal


def proses(sumber, acuan):
    mentah = kumpulkan(sumber)
    hasil = []
    for i, m in enumerate(mentah, 1):
        skor, alasan, tautan = periksa_phishing(m["nama"], m["alamat"], m["balas_ke"], m["subjek"], m["isi"])
        teks = m["subjek"] + "\n" + m["isi"]
        tgl, rel = cari_tenggat(teks, acuan)
        e = {"id": f"E{i}", "dari_nama": m["nama"], "dari_alamat": m["alamat"], "subjek": m["subjek"],
             "tanggal_kirim": m["tanggal"], "lampiran": m["lampiran"], "tenggat_tanggal": tgl,
             "tenggat_relatif": rel, "nominal_rp": cari_nominal(teks), "tautan": tautan,
             "phishing_skor": skor, "phishing_alasan": alasan, "isi_awal": re.sub(r"\s+", " ", m["isi"]).strip()[:300]}
        e["kategori_dugaan"], e["prioritas_dugaan"], e["sinyal"] = kategori_dan_prioritas(e, acuan, m["isi"])
        e["isi_kosong"] = len(e["isi_awal"]) < 5 and not m["subjek"]
        hasil.append(e)
    urut = {"P1-waspada": 0, "P1": 1, "P2": 2, "P3": 3, "P4": 4}
    hasil_urut = sorted(hasil, key=lambda x: (urut.get(x["prioritas_dugaan"], 5), x["id"]))
    ringkas = {}
    for e in hasil:
        ringkas[e["kategori_dugaan"]] = ringkas.get(e["kategori_dugaan"], 0) + 1
    return {"tanggal_acuan": acuan.isoformat(), "jumlah_email": len(hasil), "sebaran_dugaan": ringkas,
            "urutan_dugaan": [e["id"] for e in hasil_urut], "email": hasil,
            "UNTUK_AGENT_SAJA": "Ini pra-pilah kata kunci, bukan putusan. Baca tiap email sendiri sebelum menulis "
                                "ringkasan; jangan sebut script/berkas ini ke pengguna; jangan buka tautan."}


def cetak_ringkas(lap):
    print(f"Acuan {lap['tanggal_acuan']} | {lap['jumlah_email']} email | {lap['sebaran_dugaan']}")
    for e in sorted(lap["email"], key=lambda x: lap["urutan_dugaan"].index(x["id"])):
        print(f"{e['id']} [{e['prioritas_dugaan']}] {e['kategori_dugaan']} | {e['dari_nama'] or e['dari_alamat']} | "
              f"{e['subjek'][:60]} | {'; '.join(e['sinyal'][:3])}")
        for a in e["phishing_alasan"][:3]:
            print(f"    ! {a}")
    print("UNTUK AGENT SAJA: " + lap["UNTUK_AGENT_SAJA"])


def main(argv=None):
    ap = argparse.ArgumentParser(description="Pra-pilah email (kata kunci); agent tetap membaca isinya.")
    ap.add_argument("sumber")
    ap.add_argument("--format", choices=["json", "ringkas"], default="json")
    ap.add_argument("--sekarang", help="tanggal acuan YYYY-MM-DD (default hari ini)")
    ap.add_argument("--keluar", help="simpan JSON ke berkas ini (mis. laporan.json)")
    a = ap.parse_args(argv)
    try:
        acuan = datetime.strptime(a.sekarang, "%Y-%m-%d").date() if a.sekarang else date.today()
    except ValueError:
        print("Tanggal --sekarang harus berbentuk YYYY-MM-DD", file=sys.stderr)
        return 2
    try:
        lap = proses(a.sumber, acuan)
    except (FileNotFoundError, ValueError, OSError) as ex:
        print(f"Gagal membaca: {ex}", file=sys.stderr)
        return 1
    if lap["jumlah_email"] == 0:
        print("Tidak ada email yang bisa dibaca (butuh .eml/.txt/.mbox/.csv).", file=sys.stderr)
        return 1
    if a.keluar:
        Path(a.keluar).write_text(json.dumps(lap, ensure_ascii=False, indent=2), encoding="utf-8")
    if a.format == "ringkas":
        cetak_ringkas(lap)
    elif not a.keluar:
        print(json.dumps(lap, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
