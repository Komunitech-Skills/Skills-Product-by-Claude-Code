#!/usr/bin/env python3
"""Siapkan daftar kirim broadcast WhatsApp yang patuh izin (UU PDP) dari file kontak CSV.

Yang dilakukan:
1. Membaca kontak CSV (pemisah , ; atau tab dideteksi otomatis).
2. HANYA memakai kontak yang kolom persetujuannya "ya/setuju/1/opt-in", dan membuang kontak yang
   minta berhenti (kolom berhenti/opt-out atau file --daftar-berhenti).
3. Merapikan nomor ke format 628xxx, membuang nomor tidak valid & duplikat.
4. Mengisi {nama}, {sapaan}, dan kolom lain (mis. {kota}) ke beberapa variasi pesan, bergiliran.
5. Mewajibkan teks cara berhenti (mis. "balas STOP") di SETIAP variasi.
6. Membuat jadwal kirim bertahap (per batch, jeda, jam kirim, maks. per hari) dan link wa.me
   untuk dikirim manual satu per satu.

Script TIDAK mengirim pesan dan tidak mengakses internet. File output berisi data pribadi: simpan
di komputer sendiri, jangan dibagikan.

Hanya library standar Python 3.8+. Contoh:
  python3 siapkan_broadcast.py --kontak pelanggan.csv --pesan pesan.txt --mulai "2026-09-28 10:00" \
      --output broadcast_siap.csv
"""
import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, time, timedelta
from urllib.parse import quote

# Windows: pastikan teks Indonesia/emoji tercetak tanpa error encoding
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

KOLOM_NAMA = ["nama", "name", "nama pelanggan", "nama kontak", "customer"]
KOLOM_NOMOR = ["nomor", "no hp", "no. hp", "nohp", "hp", "no wa", "nomor wa", "whatsapp", "wa", "telepon",
               "telp", "phone", "no telepon", "nomor hp", "handphone"]
KOLOM_SETUJU = ["persetujuan", "setuju", "izin", "opt-in", "optin", "opt in", "consent", "bersedia",
                "setuju broadcast", "boleh dihubungi", "setuju promo", "izin promo", "boleh promo", "terima promo"]
KOLOM_SAPAAN = ["sapaan", "panggilan", "sapa", "salam", "sebutan", "sapaan pelanggan", "title", "salutation"]
KOLOM_BERHENTI = ["berhenti", "opt-out", "optout", "opt out", "stop", "unsubscribe", "tolak"]
YA = {"ya", "y", "iya", "yes", "setuju", "1", "true", "opt-in", "optin", "ok", "oke", "sudah", "v", "✓", "bersedia", "boleh"}
# Teks berhenti WAJIB berupa instruksi tindakan: balas/ketik/kirim + STOP/BERHENTI (atau setara).
# Frasa seperti "tidak mau dapat diskon" atau "untuk berhenti pusing" tidak dihitung.
POLA_OPTOUT = re.compile(
    r"\b(?:balas|ketik|kirim|reply|send)\b\s*:?\s*(?:\w+\s+){0,4}?[\"'“‘*_:]?\s*"
    r"(?:stop|berhenti|unreg|unsubscribe|batal\s+langganan)(?![-\w])", re.IGNORECASE)


def ada_optout(teks):
    """True bila ada instruksi berhenti yang sah (balas/ketik/kirim ... STOP), bukan "jangan balas STOP"."""
    for m in POLA_OPTOUT.finditer(teks):
        sebelum = teks[max(0, m.start() - 25):m.start()].lower()
        if re.search(r"\bjangan(?:\s+sampai)?\s*$", sebelum):
            continue
        return True
    return False


# Isi kolom Berhenti yang berarti "TIDAK berhenti". Isi lain yang tidak kosong (ya, STOP, x, tanggal, ...) = berhenti.
BUKAN_BERHENTI = {"tidak", "tdk", "no", "n", "0", "-", "false", "belum", "aktif", "nggak", "gak", "enggak"}
# Nilai baku untuk laporan: nilai lain tetap diperlakukan AMAN (tidak dikirimi) tetapi dilaporkan sebagai "tidak baku".
TIDAK_SETUJU_BAKU = {"", "tidak", "tdk", "no", "n", "0", "-", "false", "belum", "nggak", "gak", "enggak", "tolak"}
BERHENTI_BAKU = {"ya", "y", "iya", "yes", "1", "true", "stop", "berhenti", "x", "v", "✓", "unsubscribe", "unsub", "unreg",
                 "opt-out", "optout"}
POLA_TANGGAL = re.compile(r"(?<![\d\-./])(?:\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{1,2}[-/.]\d{1,2}(?:[-/.]\d{2,4})?)(?![\d\-./])")
# Gelar belakang: hanya dibuang bila di belakang nama (mis. "Andi, S.E."), tidak dilewati sebagai gelar depan.
GELAR_BELAKANG = {"se", "st", "sh", "mm", "msi", "mpd", "mt", "skom", "spd", "mkes", "ssos", "sag", "amd", "spsi",
                  "ssi", "mh", "mkom", "sked", "ak", "ssn", "sip"}
GELAR = {"h", "hj", "haji", "hajjah", "hjh", "dr", "drs", "dra", "ir", "prof", "sdr", "sdri", "st", "se", "sh", "ust",
         "ustadz", "ustazah", "ustadzah", "kh", "hm", "muh", "moh", "mhd"}
SAPAAN = {"bu": "Bu", "ibu": "Bu", "pak": "Pak", "bapak": "Pak", "kak": "Kak", "kakak": "Kak", "mas": "Mas",
          "mbak": "Mbak", "mba": "Mbak", "bang": "Bang", "abang": "Bang", "teh": "Teh", "teteh": "Teh",
          "aa": "Aa", "uda": "Uda", "uni": "Uni", "koh": "Koh", "cik": "Cik", "ci": "Ci", "om": "Om",
          "tante": "Tante", "ny": "Bu", "nyonya": "Bu", "tn": "Pak", "tuan": "Pak", "dek": "Dek", "sis": "Sis",
          "gan": "Gan", "bli": "Bli", "mbok": "Mbok"}


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def kunci(teks):
    return re.sub(r"[^a-z0-9]+", "_", teks.strip().lower()).strip("_")


def cari_kolom(header, pilihan, paksa=None, nama_arg=""):
    if paksa:
        for h in header:
            if h.strip().lower() == paksa.strip().lower():
                return h
        galat("Kolom '{}' ({}) tidak ada. Kolom yang tersedia: {}".format(paksa, nama_arg, ", ".join(header)))
    norm = {h.strip().lower(): h for h in header}
    for p in pilihan:
        if p in norm:
            return norm[p]
    return None


def baca_kontak(path):
    try:
        with open(path, newline="", encoding="utf-8-sig") as f:
            contoh = f.read(4096)
            f.seek(0)
            try:
                dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t")
            except csv.Error:
                dialek = csv.excel
            r = csv.DictReader(f, dialect=dialek)
            baris = list(r)
            return (r.fieldnames or []), baris
    except FileNotFoundError:
        galat("File kontak tidak ditemukan: {}".format(path))
    except UnicodeDecodeError:
        galat("File kontak bukan UTF-8. Di Excel: Simpan Sebagai → 'CSV UTF-8 (Comma delimited)'.")
    except OSError as e:
        galat("Gagal membaca {}: {}".format(path, e))


def rapikan_nomor(teks):
    d = re.sub(r"\D", "", teks or "")
    if d.startswith("00"):
        d = d[2:]
    if d.startswith("620"):
        d = "62" + d[3:]
    elif d.startswith("0"):
        d = "62" + d[1:]
    elif d.startswith("8"):
        d = "62" + d
    if not d.startswith("628") or not 10 <= len(d) <= 15:
        return None
    return d


def _bersih(k):
    return re.sub(r"[.,]", "", k).lower()


BULAN_TEKS = (r"jan(?:uari)?|feb(?:ruari)?|mar(?:et)?|apr(?:il)?|mei|jun(?:i)?|jul(?:i)?|agu(?:stus)?|agt|"
              r"sep(?:t(?:ember)?)?|okt(?:ober)?|nov(?:ember)?|des(?:ember)?")
POLA_TANGGAL_TEKS = re.compile(r"\b\d{1,2}\s+(?:" + BULAN_TEKS + r")\b\.?(?:\s+\d{2,4})?|\b(?:" + BULAN_TEKS +
                               r")\b\.?\s+\d{4}\b", re.IGNORECASE)
POLA_NOMOR_URUT = re.compile(r"^\s*\d{1,3}\s*[.)]\s+")


def cari_nomor_di_teks(teks):
    """Cari nomor HP Indonesia di satu baris teks bebas (boleh ada nama/catatan/tanggal/nomor urut).
    Kembalikan (daftar nomor valid, daftar potongan angka panjang yang tidak terbaca).

    Aturan penggabungan grup angka (agar angka catatan tidak ikut tergabung):
    - nomor urut di awal baris ("5. ", "1) ") dan tanggal (12/09, 2026-09-01, 25 September, 12 Sept 2026) dibuang;
    - grup hanya digabung bila dipisah spasi/titik/tanda hubung tunggal (bukan " - ", huruf, koma, "/", "x");
    - grup berkurung "(2)" memutus nomor, kecuali di awal ("(0812)") atau "(0)" sesudah 62;
    - bila nomor sudah valid dan >= 12 digit (format 62), grup berikutnya yang <= 4 digit tidak digabung;
    - grup yang diawali 08/62/+62 memulai nomor baru bila nomor sebelumnya sudah valid."""
    t = POLA_NOMOR_URUT.sub(" ", teks)
    t = POLA_TANGGAL.sub(" ", t)
    t = POLA_TANGGAL_TEKS.sub(" ", t)
    valid, gagal = [], []
    grup = [(m.group(0), m.start(), m.end()) for m in re.finditer(r"\+?\d+|\(\d+\)", t)]
    buf, akhir_sblm = "", None

    def tutup():
        if not buf:
            return
        n = rapikan_nomor(buf)
        if n:
            valid.append(n)
        elif len(re.sub(r"\D", "", buf)) >= 7:
            gagal.append(buf)

    for g, mulai, akhir in grup:
        sep = t[akhir_sblm:mulai] if akhir_sblm is not None else ""
        berkurung = g.startswith("(")
        n_buf = rapikan_nomor(buf) if buf else None
        putus = False
        if buf:
            if not re.fullmatch(r"[ \t]*[.\-]?[ \t]*", sep) or re.search(r"\s-\s", sep):
                putus = True
            elif berkurung and not (g == "(0)" and re.sub(r"\D", "", buf) in ("62", "0062")):
                putus = True
            elif n_buf and len(n_buf) >= 12 and len(re.sub(r"\D", "", g)) <= 4:
                putus = True
            elif n_buf and re.match(r"^(?:\+?62|0062|08)", g):
                putus = True
            elif len(re.sub(r"\D", "", buf)) >= 15:
                putus = True
        if putus:
            tutup()
            buf = ""
        buf += g
        akhir_sblm = akhir
    tutup()
    return valid, gagal


def pecah_nama(nama, sapaan_default, nama_lengkap):
    # "Hj.Nurul" / "Dr.Rina" -> "Hj. Nurul" / "Dr. Rina" (gelar tanpa spasi)
    nama = re.sub(r"\b([A-Za-z]{1,4})\.(?=[A-Z][a-z]{2,})", r"\1. ", nama or "")
    kata = nama.strip().split()
    sapaan = None
    if kata and _bersih(kata[0]) in SAPAAN:
        sapaan = SAPAAN[_bersih(kata[0])]
        kata = kata[1:]
    # Lewati gelar depan (H., Hj., H.M., dr., Ir., Prof., Muh., ...).
    while kata and _bersih(kata[0]) in GELAR and _bersih(kata[0]) not in GELAR_BELAKANG:
        g = _bersih(kata[0])
        if sapaan is None and g in ("hj", "hjh", "hajjah", "ustazah", "ustadzah"):
            sapaan = "Bu"
        elif sapaan is None and g in ("h", "hm", "haji", "kh", "ust", "ustadz"):
            sapaan = "Pak"
        kata = kata[1:]
    sapaan = sapaan or sapaan_default
    # Buang gelar di mana pun (termasuk gelar belakang bertitik: S.E., M.Si., M.Pd.).
    kata = [k for k in kata if _bersih(k) not in GELAR and _bersih(k) not in GELAR_BELAKANG]
    if not kata:
        return sapaan, ""
    kata = [k.strip(",") for k in kata]
    kata = [k if (k.isupper() and len(k) <= 3 and len(kata) > 1) else k.capitalize() for k in kata]
    return sapaan, " ".join(kata) if nama_lengkap else kata[0]


def rapikan_teks(t):
    t = re.sub(r"[ \t]{2,}", " ", t)
    t = re.sub(r" +([,.!?])", r"\1", t)
    return "\n".join(b.rstrip() for b in t.split("\n")).strip()


def baca_variasi(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            isi = f.read()
    except FileNotFoundError:
        galat("File pesan tidak ditemukan: {}".format(path))
    except UnicodeDecodeError:
        galat("File pesan harus teks UTF-8 (.txt).")
    bagian = re.split(r"^\s*-{3,}\s*$", isi, flags=re.MULTILINE)
    return [b.strip() for b in bagian if b.strip()]


def parse_jam(teks):
    try:
        a, b = [datetime.strptime(x.strip().replace(".", ":"), "%H:%M").time() for x in teks.split("-")]
    except ValueError:
        galat("--jam-kirim harus seperti 09:00-20:00.")
    if a >= b:
        galat("--jam-kirim: jam mulai harus sebelum jam selesai.")
    return a, b


def main():
    p = argparse.ArgumentParser(description="Siapkan daftar kirim broadcast WA yang patuh izin.", allow_abbrev=False)
    p.add_argument("--kontak", required=True, help="file CSV kontak (kolom nama, nomor, persetujuan)")
    p.add_argument("--pesan", required=True, help="file .txt berisi variasi pesan, dipisah baris '---'")
    p.add_argument("--output", default="broadcast_siap.csv", help="file CSV hasil (default broadcast_siap.csv)")
    p.add_argument("--mulai", help="waktu mulai kirim 'YYYY-MM-DD HH:MM'. Tanpa ini, kolom jadwal dikosongkan")
    p.add_argument("--jam-kirim", default="09:00-20:00", help="jendela jam kirim, default 09:00-20:00")
    p.add_argument("--per-batch", type=int, default=20, help="jumlah pesan per batch, default 20")
    p.add_argument("--jeda-pesan-detik", type=int, default=60, help="jeda antar pesan dalam batch, default 60 detik")
    p.add_argument("--jeda-batch-menit", type=int, default=30, help="jeda antar batch, default 30 menit")
    p.add_argument("--maks-per-hari", type=int, default=100, help="maks. pesan per hari, default 100 (saran konservatif)")
    p.add_argument("--sapaan-default", default="Kak", help="sapaan bila nama tidak diawali Bu/Pak/dll. Default Kak")
    p.add_argument("--nama-lengkap", action="store_true", help="pakai nama lengkap (default: nama depan saja)")
    p.add_argument("--kirim-saat-jumatan", action="store_true",
                   help="jangan lewati Jumat 11.30–13.00 (default: dilewati, digeser ke 13.00)")
    p.add_argument("--daftar-berhenti", help="file .txt/.csv berisi nomor yang minta berhenti (satu per baris)")
    p.add_argument("--kolom-nama")
    p.add_argument("--kolom-nomor")
    p.add_argument("--kolom-persetujuan")
    p.add_argument("--kolom-berhenti")
    p.add_argument("--kolom-sapaan", help="kolom sapaan (Bu/Pak/Kak...). Otomatis terdeteksi: Sapaan, Panggilan, dll.")
    p.add_argument("--fakta", help="kata-kata pengguna tentang promo (salin persis) untuk cek klaim karangan")
    p.add_argument("--fakta-file", help="file .txt berisi kata-kata pengguna tentang promo (salin persis)")
    p.add_argument("--saya-pastikan-semua-setuju", action="store_true",
                   help="HANYA jika file tidak punya kolom persetujuan dan kamu yakin semua kontak sudah setuju")
    a = p.parse_args()

    for nama, nilai, minimal in (("--per-batch", a.per_batch, 1), ("--jeda-pesan-detik", a.jeda_pesan_detik, 0),
                                 ("--jeda-batch-menit", a.jeda_batch_menit, 0), ("--maks-per-hari", a.maks_per_hari, 1)):
        if nilai < minimal:
            galat("{} minimal {}.".format(nama, minimal))
    jam_awal, jam_akhir = parse_jam(a.jam_kirim)

    variasi = baca_variasi(a.pesan)
    if not variasi:
        galat("File pesan kosong. Tulis minimal 1 variasi pesan.")
    tanpa_optout = [str(i + 1) for i, v in enumerate(variasi) if not ada_optout(v)]
    if tanpa_optout:
        galat("Variasi ke-{} belum punya teks cara berhenti. Tambahkan, mis.: "
              "\"Tidak ingin menerima info promo lagi? Balas STOP.\"".format(", ".join(tanpa_optout)))

    # Anti-karang: klaim (stok terbatas, terlaris, halal, gratis ongkir, ...) hanya boleh dari fakta pemilik.
    cek_klaim = "belum"
    if a.fakta is not None or a.fakta_file is not None:
        if a.fakta is not None and a.fakta_file is not None:
            galat("Isi salah satu: --fakta atau --fakta-file.")
        if a.fakta_file is not None:
            try:
                with open(a.fakta_file, encoding="utf-8-sig") as f:
                    fakta = f.read()
            except (OSError, UnicodeDecodeError) as e:
                galat("Gagal membaca --fakta-file: {}".format(e))
        else:
            fakta = a.fakta
        if not fakta.strip():
            galat("Fakta kosong. Salin kata-kata pengguna tentang promo ke --fakta/--fakta-file.")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import cek_fakta
        karang = []
        for i, v in enumerate(variasi, start=1):
            for t in cek_fakta.periksa(re.sub(r"\{[^{}]+\}", " ", v), fakta, abaikan={"jam"}):
                if t["level"] == "GAGAL":
                    karang.append("Variasi {}: {}".format(i, t["pesan"]))
        if karang:
            galat("Ada klaim yang tidak disebut pemilik (jangan dikarang):\n- " + "\n- ".join(karang) +
                  "\nHapus klaim itu atau tanyakan ke pemilik, lalu jalankan ulang.")
        cek_klaim = "lulus"

    header, baris = baca_kontak(a.kontak)
    if not baris:
        galat("File kontak tidak berisi data.")
    k_nama = cari_kolom(header, KOLOM_NAMA, a.kolom_nama, "--kolom-nama")
    k_nomor = cari_kolom(header, KOLOM_NOMOR, a.kolom_nomor, "--kolom-nomor")
    k_setuju = cari_kolom(header, KOLOM_SETUJU, a.kolom_persetujuan, "--kolom-persetujuan")
    k_berhenti = cari_kolom(header, KOLOM_BERHENTI, a.kolom_berhenti, "--kolom-berhenti")
    k_sapaan = cari_kolom(header, KOLOM_SAPAAN, a.kolom_sapaan, "--kolom-sapaan")
    if k_nama:
        tanpa_nama = [str(i + 1) for i, v in enumerate(variasi) if not re.search(r"\{\s*nama\s*\}", v, re.IGNORECASE)]
        if tanpa_nama:
            galat("Variasi ke-{} tidak memuat {{nama}}. Versi tanpa nama (untuk daftar siaran WhatsApp Business) jangan "
                  "dimasukkan ke file pesan untuk kontak personal — tampilkan terpisah di chat saja.".format(
                      ", ".join(tanpa_nama)))
    if not k_nomor:
        galat("Kolom nomor WA tidak ditemukan. Kolom tersedia: {}. Pakai --kolom-nomor \"Nama Kolom\".".format(
            ", ".join(header)))
    if not k_setuju and not a.saya_pastikan_semua_setuju:
        galat("Kolom persetujuan (mis. 'Persetujuan' berisi ya/tidak) tidak ditemukan. UU PDP mensyaratkan dasar "
              "pemrosesan seperti persetujuan. Tambahkan kolom itu, atau pakai --kolom-persetujuan. Jika kamu "
              "YAKIN semua kontak sudah setuju, jalankan ulang dengan --saya-pastikan-semua-setuju.")

    # placeholder yang tersedia
    tersedia = {"nama", "sapaan"} | {kunci(h) for h in header}
    dipakai = set()
    for v in variasi:
        dipakai |= set(re.findall(r"\{([^{}]+)\}", v))
    asing = sorted(x for x in dipakai if kunci(x) not in tersedia)
    if asing:
        galat("Placeholder tidak dikenal: {}. Yang tersedia: {}.".format(
            ", ".join("{" + x + "}" for x in asing), ", ".join("{" + x + "}" for x in sorted(tersedia))))

    berhenti, stop_tak_terbaca, asal_stop, digit_stop = set(), [], {}, []
    if a.daftar_berhenti:
        try:
            with open(a.daftar_berhenti, encoding="utf-8-sig") as f:
                isi_stop = f.read()
        except (OSError, UnicodeDecodeError) as e:
            galat("Gagal membaca --daftar-berhenti: {}".format(e))
        for no_b, t in enumerate(isi_stop.splitlines(), start=1):
            # Huruf O/o yang diapit angka hampir pasti salah ketik nol (0812-OOOO-0332)
            t = re.sub(r"(?<=[\dOo\s.\-])[Oo](?=[Oo\d\s.\-]*\d)", "0", t) if re.search(r"\d", t) else t
            nomor_b, sisa = cari_nomor_di_teks(t)
            # Baris berisi teks tapi tanpa nomor terbaca (mis. "Bu Tuti minta stop") tidak boleh diabaikan
            # diam-diam; hanya baris judul pertama tanpa angka yang dilewati.
            if not nomor_b and not sisa and t.strip() and not (no_b == 1 and not re.search(r"\d", t)):
                stop_tak_terbaca.append({"baris": no_b, "teks": t.strip()[:80]})
            berhenti.update(nomor_b)
            for n in nomor_b:
                asal_stop.setdefault(n, []).append(no_b)
            digit_baris = re.sub(r"\D", "", t)
            if len(digit_baris) >= 9:
                digit_stop.append(digit_baris)
            if sisa:
                stop_tak_terbaca.append({"baris": no_b, "teks": t.strip()[:80]})

    siap, dilewati, terlihat = [], {}, set()

    def tanda_berhenti(b):
        if not k_berhenti:
            return False
        v = (b.get(k_berhenti) or "").strip().lower()
        return bool(v) and v not in BUKAN_BERHENTI

    def tanda_tolak(b):
        return bool(k_setuju) and (b.get(k_setuju) or "").strip().lower() not in YA

    # Lintasan pertama: kumpulkan SEMUA nomor yang minta berhenti / tidak setuju di baris mana pun,
    # supaya baris duplikat tanpa tanda tidak "menimpa" permintaan berhenti.
    ditolak_di_baris_lain = set()
    for b in baris:
        n = rapikan_nomor(b.get(k_nomor))
        if n and (tanda_berhenti(b) or tanda_tolak(b)):
            ditolak_di_baris_lain.add(n)

    def lewati(alasan, no):
        dilewati.setdefault(alasan, []).append(no)

    for no, b in enumerate(baris, start=2):  # nomor baris sesuai tampilan spreadsheet (baris 1 = judul)
        nomor = rapikan_nomor(b.get(k_nomor))
        if tanda_tolak(b):
            v = (b.get(k_setuju) or "").strip()
            if v.lower() in TIDAK_SETUJU_BAKU:
                lewati("belum/tidak setuju menerima broadcast", no)
            else:
                lewati("nilai persetujuan tidak baku '{}' (dianggap belum setuju; rapikan jadi ya/tidak)".format(v), no)
            continue
        if tanda_berhenti(b):
            v = (b.get(k_berhenti) or "").strip()
            if v.lower() in BERHENTI_BAKU or POLA_TANGGAL.fullmatch(v):
                lewati("minta berhenti (kolom berhenti)", no)
            else:
                lewati("nilai kolom berhenti tidak baku '{}' (dianggap berhenti; kosongkan bila masih aktif)".format(v), no)
            continue
        if not nomor:
            lewati("nomor kosong/tidak valid", no)
            continue
        if nomor in berhenti:
            lewati("ada di daftar berhenti", no)
            continue
        # Jaring pengaman: nomor kontak (bentuk 08.., 8.., 62..) muncul sebagai deretan angka di baris stop mana pun.
        bentuk = ("0" + nomor[2:], nomor[2:], nomor)
        if any(b in d for d in digit_stop for b in bentuk):
            lewati("nomor ada di baris daftar berhenti (cocok sebagian — periksa baris itu)", no)
            continue
        if nomor in ditolak_di_baris_lain:
            lewati("nomor ini minta berhenti/tidak setuju di baris lain", no)
            continue
        if nomor in terlihat:
            lewati("nomor duplikat", no)
            continue
        sapaan, nama = pecah_nama(b.get(k_nama) if k_nama else "", a.sapaan_default, a.nama_lengkap)
        nilai = {kunci(h): (b.get(h) or "").strip() for h in header}
        # Kolom Sapaan milik pemilik (Bu/Pak/Kak...) diutamakan; baru jatuh ke awalan nama/gelar/--sapaan-default.
        isi_sapaan = (b.get(k_sapaan) or "").strip() if k_sapaan else ""
        if isi_sapaan:
            sapaan = SAPAAN.get(_bersih(isi_sapaan), isi_sapaan[:1].upper() + isi_sapaan[1:])
        nilai["nama"], nilai["sapaan"] = nama, sapaan
        kosong = [x for x in dipakai if kunci(x) not in ("nama", "sapaan") and not nilai.get(kunci(x))]
        if kosong:
            lewati("kolom {} kosong".format(", ".join("{" + x + "}" for x in sorted(kosong))), no)
            continue
        terlihat.add(nomor)
        siap.append({"baris_asal": no, "nama": nama, "sapaan": sapaan, "nomor": nomor, "nilai": nilai})

    if not siap:
        galat("Tidak ada kontak yang lolos. Rincian: " + json.dumps(
            {k: len(v) for k, v in dilewati.items()}, ensure_ascii=False))

    mulai = None
    if a.mulai:
        try:
            mulai = datetime.strptime(a.mulai.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            galat("--mulai harus 'YYYY-MM-DD HH:MM', mis. \"2026-09-28 10:00\".")

    jumat_awal, jumat_akhir = time(11, 30), time(13, 0)

    def geser_ke_jendela(t):
        for _ in range(3):
            if t.time() < jam_awal:
                t = t.replace(hour=jam_awal.hour, minute=jam_awal.minute, second=0)
            elif t.time() > jam_akhir:
                t = (t + timedelta(days=1)).replace(hour=jam_awal.hour, minute=jam_awal.minute, second=0)
            # Jumat (weekday 4) 11.30–13.00: jeda salat Jumat, geser ke 13.00
            if not a.kirim_saat_jumatan and t.weekday() == 4 and jumat_awal <= t.time() < jumat_akhir:
                t = t.replace(hour=13, minute=0, second=0)
                continue
            break
        return t

    jadwal_list = [""] * len(siap)
    if mulai:
        t = geser_ke_jendela(mulai)
        hari, hitung_hari, dalam_batch = t.date(), 0, 0
        for i in range(len(siap)):
            if hitung_hari >= a.maks_per_hari:
                t = (t + timedelta(days=1)).replace(hour=jam_awal.hour, minute=jam_awal.minute, second=0)
            t = geser_ke_jendela(t)
            if t.date() != hari:
                hari, hitung_hari, dalam_batch = t.date(), 0, 0
            jadwal_list[i] = t.strftime("%Y-%m-%d %H:%M")
            hitung_hari += 1
            dalam_batch += 1
            t = t + timedelta(seconds=a.jeda_pesan_detik)
            if dalam_batch >= a.per_batch:
                t = t + timedelta(minutes=a.jeda_batch_menit)
                dalam_batch = 0

    hasil, jumlah_varian = [], [0] * len(variasi)
    for i, k in enumerate(siap):
        idx = i % len(variasi)
        jumlah_varian[idx] += 1

        def ganti(m):
            return k["nilai"].get(kunci(m.group(1)), "")
        teks = rapikan_teks(re.sub(r"\{([^{}]+)\}", ganti, variasi[idx]))
        jadwal = jadwal_list[i]
        hasil.append({"no": i + 1, "jadwal_kirim": jadwal, "nama": k["nama"], "nomor": k["nomor"],
                      "varian": idx + 1, "pesan": teks,
                      "link_wa": "https://wa.me/{}?text={}".format(k["nomor"], quote(teks, safe=""))})

    try:
        with open(a.output, "w", newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=["no", "jadwal_kirim", "nama", "nomor", "varian", "pesan", "link_wa"])
            w.writeheader()
            w.writerows(hasil)
    except OSError as e:
        galat("Gagal menyimpan {}: {}".format(a.output, e))

    peringatan = []
    nomor_kontak = {rapikan_nomor(b.get(k_nomor)) for b in baris} - {None}
    stop_tak_cocok = [{"nomor": "0" + n[2:], "baris": asal_stop[n]} for n in sorted(berhenti)
                      if n in asal_stop and n not in nomor_kontak]
    if stop_tak_cocok:
        peringatan.append(
            "{} nomor di daftar berhenti tidak cocok dengan kontak mana pun (baris: {}). Bisa jadi memang bukan "
            "pelanggan di file ini, TAPI bisa juga salah baca. Cocokkan dulu baris itu sebelum mengirim.".format(
                len(stop_tak_cocok), ", ".join(str(b) for x in stop_tak_cocok for b in x["baris"])))
    if stop_tak_terbaca:
        peringatan.append(
            "Ada {} baris di daftar berhenti yang nomornya TIDAK terbaca (baris: {}). JANGAN kirim dulu: rapikan "
            "baris itu (satu nomor per baris, mis. 0812-3456-7890) lalu jalankan ulang, karena orang di baris itu "
            "bisa tetap terkirimi.".format(len(stop_tak_terbaca), ", ".join(str(x["baris"]) for x in stop_tak_terbaca)))
    if len(variasi) < 2:
        peringatan.append("Hanya 1 variasi pesan. Disarankan 3–5 variasi agar pesan terasa personal.")
    for i, v in enumerate(variasi, start=1):
        if len(v) > 700:
            peringatan.append("Variasi {} cukup panjang ({} karakter); pesan singkat lebih jarang dilaporkan spam.".format(i, len(v)))
        if len(re.findall(r"https?://|www\.", v)) > 1:
            peringatan.append("Variasi {} berisi lebih dari 1 link; cukup 1 link.".format(i))
    if cek_klaim == "belum":
        peringatan.append("Klaim di pesan belum dicek terhadap kata-kata pemilik. Jalankan ulang dengan "
                          "--fakta-file fakta.txt agar klaim karangan (stok terbatas, terlaris, halal, ...) tertangkap.")
    if a.saya_pastikan_semua_setuju and not k_setuju:
        peringatan.append("Kolom persetujuan tidak ada; pengguna menyatakan semua kontak sudah setuju. "
                          "Simpan bukti persetujuan masing-masing kontak.")
    ringkasan = {
        "file_output": a.output,
        "total_baris_kontak": len(baris),
        "siap_kirim": len(hasil),
        "dilewati": {k: {"jumlah": len(v), "baris": v[:30]} for k, v in dilewati.items()},
        "sebaran_varian": {"varian_{}".format(i + 1): n for i, n in enumerate(jumlah_varian)},
        "jadwal_pertama": hasil[0]["jadwal_kirim"] or None,
        "jadwal_terakhir": hasil[-1]["jadwal_kirim"] or None,
        "kolom_terdeteksi": {"nama": k_nama, "nomor": k_nomor, "persetujuan": k_setuju, "berhenti": k_berhenti,
                             "sapaan": k_sapaan},
        "cek_klaim_terhadap_fakta": cek_klaim,
        "daftar_berhenti_terbaca": len(berhenti),
        "daftar_berhenti_tidak_terbaca": stop_tak_terbaca,
        "daftar_berhenti_tidak_cocok_kontak": stop_tak_cocok,
        "status": "PERIKSA DULU" if (stop_tak_terbaca or stop_tak_cocok) else "SIAP",
        "peringatan": peringatan,
        "catatan": "File output berisi data pribadi pelanggan. Simpan di komputer sendiri, jangan dibagikan.",
    }
    print(json.dumps(ringkasan, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
