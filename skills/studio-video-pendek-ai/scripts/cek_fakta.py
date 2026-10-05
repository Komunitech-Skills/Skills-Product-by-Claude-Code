#!/usr/bin/env python3
"""Cek-silang hasil tulisan (caption/naskah/proposal) terhadap FAKTA DARI PENGGUNA.
(Disalin dari skill caption-sosmed-umkm, milik Komunitech; dipakai untuk naskah video pendek: menangkap fakta/klaim
produk yang dikarang dan tidak disebut pengguna.)
Diadaptasi dari pola skill naskah-live-jualan. Teks di bawah ini deskripsi asli (klaim kesehatan pangan/jamu/kosmetik
yang dilarang aturan iklan BPOM: meredakan, mengatasi, pengganti obat, detox, melangsingkan, dst.)

Tujuan: menangkap fakta yang dikarang AI — hal yang terdengar wajar tetapi tidak pernah disebut pengguna:
- JAM      : jam (19:00, 19.00) padahal pengguna tidak menyebut jam.
- ASAL     : asal/produksi/panen ("diambil langsung dari Pekanbaru", "khas Surabaya") padahal pengguna
             hanya menyebut kota itu untuk hal lain (mis. "kirim dari Pekanbaru").
- UKURAN   : ukuran/berat/isi (250ml, 500 gr, 1 kg) yang tidak ada di fakta.
- KLAIM    : reputasi ("sudah dikenal", "favorit", "terlaris", "tren terus diminati"), label resmi (halal,
             BPOM), sifat produk ("murni", "tanpa pengawet", "homemade"), manfaat kesehatan, urgensi
             ("stok terbatas", "besok harga naik"), dan layanan ("gratis ongkir", "tanpa minimal").
- ANGKA    : angka kredibilitas ("500 pelanggan", "sejak 2019", "3 cabang") yang tidak ada di fakta.

Teks di dalam kurung siku ([isi: ...], [tunjukkan tekstur]) dan kalimat tanya diabaikan.
Klaim reputasi yang disebut pengguna tetap ditandai CEK bila barisnya tidak memuat [isi: bukti].

Hasil: GAGAL (wajib diperbaiki: hapus, ganti [isi: ...], atau tanyakan ke pengguna) / CEK (periksa) / LULUS.
Kode keluar: 0 = tidak ada GAGAL, 2 = ada GAGAL, 1 = input salah.

Hanya library standar Python 3.8+. Tidak ada akses jaringan. Contoh:
  python3 cek_fakta.py --teks-file naskah.md --fakta-file fakta.txt
  python3 cek_fakta.py --teks-file proposal.md --fakta "kopi susu literan Kopi Pakde, Rp20.000/botol, BPOM"
"""
import argparse
import json
import re
import sys

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

KATEGORI = ("jam", "asal", "ukuran", "klaim", "angka")
KATA_NEGASI = r"\b(?:tidak|tak|bukan|tanpa|jangan|belum|nggak|ngga|gak|ga|enggak|ndak|tdk)\b"

# ---------- JAM ----------
POLA_JAM = re.compile(r"(?<![\d:.,])([01]?\d|2[0-3])[:.]([0-5]\d)(?![\d.,]?\d)")
POLA_JAM_FAKTA = re.compile(r"\b(?:jam|pukul|pkl\.?)\s*\d{1,2}\b|(?<![\d:.,])(?:[01]?\d|2[0-3])[:.][0-5]\d(?![\d.,]?\d)",
                            re.IGNORECASE)

# ---------- ASAL ----------
KATA_ASAL = (r"diambil|dipanen|dipetik|panen|berasal|asalnya|asal|asli|khas|dibuat|diproduksi|produksi|didatangkan"
             r"|diimpor|impor|langsung\s+dari\s+(?:hutan|kebun|petani|peternak)")
POLA_ASAL = [
    re.compile(r"(?i:\b(?:diambil|dipanen|dipetik|panen|berasal|asalnya|asli|dibuat|diproduksi|produksi|didatangkan"
               r"|diimpor|impor)\s+(?:\w+\s+){0,2}?(?:dari|di)\s+(?:hutan\s+|kebun\s+|daerah\s+|kota\s+|pulau\s+)?)"
               r"(?P<t>[A-Z][\w-]+)"),
    re.compile(r"(?i:\b(?:khas|asal|asli)\s+)(?P<t>[A-Z][\w-]+)"),
]

# ---------- UKURAN ----------
SATUAN = {"ml": ("ml", 1), "l": ("ml", 1000), "lt": ("ml", 1000), "ltr": ("ml", 1000), "liter": ("ml", 1000),
          "litre": ("ml", 1000), "g": ("g", 1), "gr": ("g", 1), "gram": ("g", 1), "kg": ("g", 1000),
          "kilo": ("g", 1000), "cm": ("cm", 1), "mm": ("cm", 0.1), "oz": ("oz", 1)}
POLA_UKURAN = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)?)\s?(ml|liter|litre|ltr|lt|l|gram|gr|g|kg|kilo|cm|mm|oz)\b",
                         re.IGNORECASE)

# ---------- KLAIM ----------
# (jenis, pola, cara cek). cara: "k" = kata inti grup k (akar) harus ada di fakta; "semua" = semua kata isi frasa
# harus ada di fakta; "selalu" = selalu GAGAL kecuali dinegasikan (klaim medis).
POLA_KLAIM = [
    ("reputasi", r"\b(?P<k>dikenal|terkenal|ternama|legendaris|terfavorit|terlaris|laris|best\s*seller"
                 r"|viral|populer|diminati|digemari|terpercaya|terbaik|nomor\s+satu|peringkat\s+(?:1|satu|pertama)|juara)\b",
     "k"),
    ("reputasi", r"\b(?:jadi|paling|menjadi|salah\s+satu|sudah)\s+(?P<k>favorit)\b", "k"),
    ("reputasi", r"\b(?P<k>favorit)\s+(?:pelanggan|warga|banyak|orang|pembeli|konsumen|semua)\b", "k"),
    ("reputasi", r"\b(?P<k>favorit)\b(?!\s*(?:-?mu|kamu|kalian|kakak|kak|anda)\b)", "cek"),
    ("reputasi", r"\b(?P<k>tren)\b[^.!?\n|]{0,40}?\b(?:diminati|naik|meningkat|berkembang|populer|tumbuh)\b", "k"),
    ("reputasi", r"\b(?:ratusan|ribuan|puluhan|banyak)\s+(?:pelanggan|pembeli|reseller|outlet|mitra|follower"
                 r"|pengikut|testimoni|ulasan)\b", "semua"),
    ("reputasi", r"\b(?:dulu|sebelumnya)\s+(?:aku|saya|gue|gw)\s+(?:juga\s+)?(?:sering|suka|pernah|sempat|susah|bingung)\b", "semua"),
    ("label resmi", r"\b(?P<k>halal(?!\s*-?\s*bi\s*-?\s*halal)|bpom|sni|pirt|p-irt|organik|bersertifikat|sertifikasi)\b", "k"),
    ("sifat produk", r"\b(?P<k>murni|homemade|rumahan|fresh|higienis|premium|alami|natural|lebah\s+liar"
                     r"|pilihan|melimpah|wangi|harum|renyah|gurih|segar|spesial)\b", "k"),
    ("sifat produk", r"\b100%\s*(?P<k>asli|murni|alami|original)\b", "k"),
    ("sifat produk", r"\b(?P<k>asli)\b(?!\s+(?:dari|di)\b)", "k"),
    ("sifat produk", r"\btanpa\s+(?:bahan\s+)?(?P<k>pengawet|msg|pewarna|pemanis|gula\s+tambahan|campuran)\b", "k"),
    ("kesehatan", r"\b(?:menyembuhkan|sembuhkan|nyembuhin|mengobati|ngobatin|berkhasiat|khasiat)\b", "selalu"),
    ("kesehatan", r"\b(?:jaga|menjaga|meningkatkan|tingkatkan|menambah|nambah|memperkuat|perkuat|mencegah|cegah"
                  r"|menurunkan|turunkan|mengontrol|melancarkan|baik\s+untuk|bagus\s+untuk|bagus\s+buat|baik\s+buat)"
                  r"\s+(?:\w+\s+){0,3}?(?P<k>stamina|daya\s+tahan|imun\w*|kekebalan|kolesterol|gula\s+darah"
                  r"|tekanan\s+darah|metabolisme|pencernaan|kesehatan|lambung|jantung)\b", "k"),
    ("kesehatan", r"\b(?:meredakan|redakan|mengatasi|atasi|menghilangkan|hilangkan|melegakan|menetralkan|detoks|detox"
                  r"|melangsingkan|pelangsing|memutihkan|peluntur|anti\s*(?:kanker|diabetes|maag|asam\s+urat)"
                  r"|obat\s+(?:alami|herbal|kuat|maag|diabetes|batuk)|pengganti\s+obat|menggantikan\s+obat"
                  r"|ganti\s+obat|terapi|menyuburkan|awet\s+muda|menumbuhkan\s+rambut|mengencangkan)\b", "selalu"),
    ("kesehatan", r"\b(?:bantu|membantu)\s+(?:\w+\s+){0,3}?(?:kembung|asam\s+lambung|maag|pencernaan|tidur\s+nyenyak"
                  r"|diet|turun\s+berat|kolesterol|gula\s+darah|tekanan\s+darah|imun\w*|stamina|nyeri|pegal|batuk|flu"
                  r"|masuk\s+angin|jerawat|flek)\b", "selalu"),
    ("kesehatan", r"\b(?:asam\s+lambung|kembung|maag|diabetes|kolesterol|hipertensi|asam\s+urat|jerawat)\s+"
                  r"(?:naik|kambuh|reda|hilang|sembuh|turun)\b", "selalu"),
    ("kesehatan", r"\b(?P<k>menyehatkan|antioksidan|bergizi\s+tinggi|kaya\s+(?:vitamin|nutrisi|gizi))\b", "k"),
    ("urgensi", r"\b(?:stok|kuota|barang|jumlah|slot)\s+(?:tinggal\s+\w+|terbatas|menipis|sedikit|hampir\s+habis)\b",
     "semua"),
    ("urgensi", r"\b(?:hari\s+terakhir|cuma\s+hari\s+ini|hanya\s+hari\s+ini|sebelum\s+kehabisan|batch\s+terakhir"
                r"|siapa\s+cepat|harga\s+(?:akan\s+)?naik|besok\s+(?:sudah\s+|udah\s+)?(?:balik|naik|kembali|normal|habis))\b",
     "semua"),
    ("layanan", r"\b(?:gratis|free)\s+(?:ongkir|ongkos\s+kirim|antar|jemput|sampel|sample|tester|pengiriman)\b"
                r"|\bongkir\s+gratis\b|\btanpa\s+minimal\w*\b|\bsame\s*day\b|\bexpress\b|\bkilat\b"
                r"|\b(?:dikirim|pengiriman|kirim)\s+(?:cepat|hari\s+ini|di\s+hari\s+yang\s+sama)\b"
                r"|\b(?:antar|jemput|ongkir|pengiriman|kirim)\s+(?:\S+\s+){0,2}?gratis\b", "semua"),
    ("layanan", r"\b(?P<k>garansi|dijamin|jaminan\s+uang\s+kembali)\b", "k"),
    # Kelangkaan/urgensi & janji pengiriman: GAGAL kecuali pengguna sendiri menyebutnya (kata kuncinya ada di fakta).
    ("urgensi", r"\bstok(?:nya)?\s+(?:\w+\s+){0,3}?(?:terbatas|menipis|sedikit|hampir\s+habis|tinggal)\b"
                r"|\b(?:jumlah|kuota)\s+terbatas\b|\b(?:ready\s+)?terbatas\b(?=[^.!?\n]{0,20}\bstok)", "semua"),
    ("urgensi", r"\b(?:kehabisan|keabisan|ludes|sold\s*out|habis\s+duluan|buruan|buruan\s+order"
                r"|promo\s+(?:cuma\s+|hanya\s+)?hari\s+ini(?:\s+saja)?|hari\s+ini\s+saja|jangan\s+sampai\s+(?:telat|ketinggalan|terlewat)"
                r"|mumpung\s+(?:masih\s+)?ada|selagi\s+(?:masih\s+)?ada|periode\s+terbatas|waktu\s+terbatas)\b", "semua"),
    ("layanan", r"\b(?:siap|bisa|melayani|layanan)\s+(?:antar|kirim|delivery|pengiriman|ongkir)\b"
                r"|\b(?:diantar|dianterin|diantarkan|dikirim|dikirimkan|nyampe|sampai\s+(?:di\s+)?rumah|sampai\s+depan\s+pintu"
                r"|antar\s+(?:ke|sampai)|kirim\s+ke\s+(?:seluruh|semua|mana)|ke\s+seluruh\s+indonesia|delivery|cod|bayar\s+di\s+tempat"
                r"|secepatnya|langsung\s+(?:sampai|diantar|dikirim))\b", "semua"),
]
POLA_ATRIBUSI = re.compile(r"\b(?:sesuai|seperti|sebagaimana|persis)\s+(?:yang\s+|apa\s+yang\s+)?(?:kakak|kak|anda|kamu|bapak|ibu"
                           r"|pengguna|klien)\s+(?:\w+\s+)?(?:sebut\w*|minta\w*|bilang|katakan|inginkan|tulis\w*)\b", re.IGNORECASE)
POLA_ANGKA = [
    re.compile(r"\b(?P<n>\d[\d.]*)\s*\+?\s*(?:pelanggan|pembeli|reseller|follower|pengikut|testimoni|ulasan"
               r"|terjual|tahun\s+berdiri|tahun\s+pengalaman)\b", re.IGNORECASE),
    re.compile(r"\b(?:sejak|berdiri)\s+(?:tahun\s+)?(?P<n>(?:19|20)\d\d)\b", re.IGNORECASE),
]
# Kalimat yang membicarakan label/bukti (bukan menyatakannya): "info sertifikasi cek deskripsi", "kalau ada".
KONTEKS_NETRAL = re.compile(r"\b(?:kalau|jika|bila|apabila)\s+(?:ada|punya|sudah)\b|\b(?:cek|info|pastikan|lampirkan"
                            r"|lengkapi|perlu|butuh|tanyakan|nomor|no\.)\b", re.IGNORECASE)
URUTAN_ETALASE = re.compile(r"(?:\b(?:pilih|pin|produk|keranjang|kuning|etalase|link|varian)\s+|\()$", re.IGNORECASE)
KATA_SAMBUNG = {"dan", "atau", "di", "ke", "dari", "yang", "untuk", "buat", "sudah", "udah", "sangat", "lebih",
                "akan", "hari", "ini", "harga", "sebelum"}


def galat(pesan):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(1)


def baca_file(path):
    try:
        with open(path, encoding="utf-8-sig") as f:
            return f.read()
    except FileNotFoundError:
        galat("File tidak ditemukan: {}".format(path))
    except UnicodeDecodeError:
        galat("File {} bukan teks UTF-8. Simpan ulang sebagai .txt (UTF-8).".format(path))
    except OSError as e:
        galat("Gagal membaca {}: {}".format(path, e))


def bersihkan(teks):
    """Buang isi kurung siku (placeholder & arahan aksi) dan kode inline berisi placeholder."""
    return re.sub(r"\[[^\]\n]*\]", " ", teks)


def kalimat(baris):
    """Pecah baris jadi kalimat/sel; kembalikan (teks, diakhiri_tanda_tanya)."""
    hasil = []
    for bag in re.split(r"(?<=[.!?])\s+|\|", baris):
        b = bag.strip().strip('"“”*_` ')
        if b:
            hasil.append((b, b.rstrip('"“”*_` ').endswith("?")))
    return hasil


def akar(kata):
    k = re.sub(r"\s+", " ", kata.lower().strip())
    for awalan in ("ter", "di"):
        if k.startswith(awalan) and len(k) > len(awalan) + 3 and k not in ("dijamin",):
            sisa = k[len(awalan):]
            if sisa in ("kenal", "laris", "favorit", "percaya", "minati", "gemari", "nama"):
                return sisa
    return {"best seller": "best", "bestseller": "best", "no 1": "1", "no.1": "1", "no. 1": "1",
            "nomor 1": "1", "p-irt": "irt", "pirt": "irt", "bersertifikat": "sertifikat",
            "sertifikasi": "sertifikat"}.get(k, k)


def ada(kata, fakta_l):
    return re.search(r"(?<![a-z])" + re.escape(kata), fakta_l) is not None


def dinegasikan(teks, posisi, jarak=30):
    """True bila ada kata negasi (tidak/bukan/tanpa/...) paling jauh `jarak` karakter sebelum posisi."""
    return re.search(KATA_NEGASI + r"[^.!?\n|]{0,%d}$" % jarak, teks[max(0, posisi - jarak - 12):posisi],
                     re.IGNORECASE) is not None


def ukuran_set(teks):
    hasil = set()
    for m in POLA_UKURAN.finditer(teks):
        try:
            n = float(m.group(1).replace(",", "."))
        except ValueError:
            continue
        dasar, kali = SATUAN[m.group(2).lower()]
        hasil.add((dasar, round(n * kali, 3)))
    return hasil


def periksa(teks, fakta, abaikan=()):
    """Kembalikan list (level, kategori, frasa, pesan)."""
    fakta_l = fakta.lower()
    temuan, lihat = [], set()

    def tambah(level, kat, frasa, pesan):
        kunci = (kat, frasa.lower())
        if kunci not in lihat:
            lihat.add(kunci)
            temuan.append({"level": level, "kategori": kat, "frasa": frasa, "pesan": pesan})

    fakta_ukuran = ukuran_set(fakta)
    fakta_punya_jam = POLA_JAM_FAKTA.search(fakta) is not None
    for baris_asli in teks.splitlines():
        ada_bukti = re.search(r"\[\s*isi\b[^\]]*\]", baris_asli, re.IGNORECASE) is not None
        baris = bersihkan(baris_asli)
        # Jam dicek pada baris yang hanya dibuang placeholder [isi: ...]-nya: label rundown [19:00–19:03] ikut diperiksa.
        baris_jam = re.sub(r"\[\s*isi\b[^\]\n]*\]", " ", baris_asli, flags=re.IGNORECASE)
        baris_asumsi = re.search(r"\basumsi\b", baris, re.IGNORECASE) is not None
        # JAM
        if "jam" not in abaikan and not fakta_punya_jam:
            for m in POLA_JAM.finditer(baris_jam):
                if m.group(1) in ("0", "00"):
                    continue  # menit relatif 00:03
                jam = "{}:{}".format(m.group(1).zfill(2), m.group(2))
                if baris_asumsi:
                    tambah("CEK", "jam", jam, "Jam {} disebut sebagai asumsi — pastikan pengguna menyetujuinya, atau "
                                              "pakai menit relatif / [isi: jam mulai].".format(jam))
                else:
                    tambah("GAGAL", "jam", jam, "Jam {} tidak disebut pengguna. Pakai menit relatif (menit 0–3) atau "
                                                "[isi: jam mulai], dan sebut di Asumsi.".format(jam))
        # ASAL
        if "asal" not in abaikan:
            for pola in POLA_ASAL:
                for m in pola.finditer(baris):
                    tempat = m.group("t")
                    if dinegasikan(baris, m.start()):
                        continue
                    t_l = tempat.lower()
                    didukung = re.search(r"(?:" + KATA_ASAL + r")\W+(?:[\w-]+\W+){0,4}?" + re.escape(t_l), fakta_l)
                    if didukung:
                        continue
                    frasa = m.group(0).strip()
                    if t_l in fakta_l:
                        pesan = ("'{}' — pengguna menyebut {} untuk hal lain (mis. kota toko/kirim), bukan asal/produksi "
                                 "produk. Tulis persis kata pengguna (mis. 'dikirim dari {}') atau [isi: asal produk]."
                                 .format(frasa, tempat, tempat))
                    else:
                        pesan = "'{}' — asal/produksi tidak disebut pengguna. Hapus atau [isi: asal produk].".format(frasa)
                    tambah("GAGAL", "asal", frasa, pesan)
        # UKURAN
        if "ukuran" not in abaikan:
            for m in POLA_UKURAN.finditer(baris):
                n = float(m.group(1).replace(",", "."))
                dasar, kali = SATUAN[m.group(2).lower()]
                angka_di_fakta = re.search(r"(?<![\d.,])" + re.escape(m.group(1)) + r"(?![\d]|[.,]\d)", fakta)
                if (dasar, round(n * kali, 3)) not in fakta_ukuran and not angka_di_fakta:
                    tambah("GAGAL", "ukuran", m.group(0), "Ukuran/isi '{}' tidak disebut pengguna. Pakai "
                                                          "[isi: ukuran/isi kemasan].".format(m.group(0)))
        # ANGKA kredibilitas
        if "angka" not in abaikan:
            for pola in POLA_ANGKA:
                for m in pola.finditer(baris):
                    n = m.group("n").rstrip(".")
                    if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?![\d])", fakta):
                        tambah("GAGAL", "angka", m.group(0), "Angka '{}' tidak ada di fakta pengguna. Hapus atau "
                                                             "[isi: angka sebenarnya].".format(m.group(0)))
        # ATRIBUSI: dilarang mengaku pengguna menyebut/meminta sesuatu (selalu GAGAL; pengguna tak bisa dikutip lewat naskah)
        if "klaim" not in abaikan:
            for m in POLA_ATRIBUSI.finditer(baris):
                tambah("GAGAL", "klaim", m.group(0).strip(), "'{}' — jangan mengaku pengguna menyebut/meminta sesuatu. "
                       "Hapus kalimatnya; tulis hanya fakta yang benar-benar dari pengguna.".format(m.group(0).strip()))
        # KLAIM
        if "klaim" not in abaikan:
            for kal, tanya in kalimat(baris):
                if tanya:
                    continue
                for jenis, pola, cara in POLA_KLAIM:
                    for m in re.finditer(pola, kal, flags=re.IGNORECASE):
                        frasa = m.group(0).strip()
                        if dinegasikan(kal, m.start(), 30 if jenis == "kesehatan" else 15):
                            continue
                        if re.search(r"\b(?:klaim|tanya|bertanya|nanya)\b", kal[:m.start()], re.IGNORECASE):
                            continue  # kalimat membahas klaim (mis. catatan "klaim X tidak ditulis"), bukan menyatakannya
                        if re.match(r"(?:nomor|no)", frasa, re.IGNORECASE) and URUTAN_ETALASE.search(kal[:m.start()]):
                            continue  # "pilih nomor 1" = nomor etalase, bukan klaim
                        if frasa.lower() == "asli" and re.search(
                                r"\b(?:testimoni|ulasan|foto|kutipan|data|bukti|angka|stok|rekam\w*|nama|akun|pelanggan"
                                r"|pembeli|harga)\s+(?:\w+\s+)?$", kal[:m.start()], re.IGNORECASE):
                            continue  # "testimoni asli", "stok asli" = keaslian data, bukan klaim produk
                        if cara == "selalu":
                            tambah("GAGAL", "klaim", frasa, "'{}' — klaim {} (menyembuhkan/khasiat) tidak boleh ditulis, "
                                                            "walau diminta pengguna.".format(frasa, jenis))
                            continue
                        if cara == "k" and m.groupdict().get("k"):
                            kunci = [akar(m.group("k"))]
                        else:
                            kunci = [w for w in re.findall(r"[a-z0-9]+", frasa.lower()) if w not in KATA_SAMBUNG]
                        if cara == "cek" and not all(ada(k, fakta_l) for k in kunci):
                            tambah("CEK", "klaim", frasa, "'{}' — pastikan bukan klaim reputasi produk (mis. 'favorit "
                                                          "pelanggan') yang tidak disebut pengguna.".format(frasa))
                            continue
                        if all(ada(k, fakta_l) for k in kunci):
                            if jenis == "reputasi" and not ada_bukti:
                                tambah("CEK", "klaim", frasa, "'{}' — disebut pengguna tetapi belum ada bukti; tulis "
                                                              "versi lunak + [isi: bukti].".format(frasa))
                            continue
                        if jenis == "label resmi" and KONTEKS_NETRAL.search(kal):
                            tambah("CEK", "klaim", frasa, "'{}' — label resmi disebut sebagai info/syarat; pastikan tidak "
                                                          "terbaca sebagai klaim bahwa produk sudah {}.".format(frasa, frasa))
                            continue
                        tambah("GAGAL", "klaim", frasa, "'{}' — klaim {} yang tidak ada di fakta pengguna. Hapus, ganti "
                                                        "[isi: ...], atau tanyakan ke pengguna.".format(frasa, jenis))
    return temuan


def main():
    p = argparse.ArgumentParser(description="Cek-silang hasil tulisan terhadap fakta dari pengguna.")
    p.add_argument("--teks", help="teks hasil yang diperiksa")
    p.add_argument("--teks-file", help="file .md/.txt berisi hasil yang diperiksa")
    p.add_argument("--fakta", help="fakta dari pengguna (salin kata-kata pengguna, jangan ditambah)")
    p.add_argument("--fakta-file", help="file .txt berisi daftar 'Fakta dari pengguna'")
    p.add_argument("--abaikan", default="", help="kategori yang dilewati, dipisah koma: " + ",".join(KATEGORI))
    p.add_argument("--json", action="store_true", help="keluarkan JSON")
    a = p.parse_args()

    if (a.teks is None) == (a.teks_file is None):
        galat("Isi salah satu: --teks atau --teks-file.")
    if (a.fakta is None) == (a.fakta_file is None):
        galat("Isi salah satu: --fakta atau --fakta-file (daftar 'Fakta dari pengguna').")
    teks = a.teks if a.teks is not None else baca_file(a.teks_file)
    fakta = a.fakta if a.fakta is not None else baca_file(a.fakta_file)
    if not fakta.strip():
        galat("Fakta kosong. Tulis dulu daftar 'Fakta dari pengguna' (kata-kata pengguna).")
    if not teks.strip():
        galat("Teks yang diperiksa kosong.")
    abaikan = {x.strip().lower() for x in a.abaikan.split(",") if x.strip()}
    salah = abaikan - set(KATEGORI)
    if salah:
        galat("Kategori --abaikan tidak dikenal: {}. Pilihan: {}.".format(", ".join(sorted(salah)), ", ".join(KATEGORI)))

    temuan = periksa(teks, fakta, abaikan)
    gagal = sum(1 for t in temuan if t["level"] == "GAGAL")
    hasil = "GAGAL" if gagal else "LULUS"
    if a.json:
        print(json.dumps({"hasil": hasil, "temuan": temuan}, ensure_ascii=False, indent=2))
    else:
        for t in temuan:
            print("{}: [{}] {}".format(t["level"], t["kategori"], t["pesan"]))
        print("HASIL: {} ({} GAGAL, {} CEK)".format(hasil, gagal, len(temuan) - gagal))
        if gagal:
            print("Perbaiki semua GAGAL (hapus klaim, ganti [isi: ...], atau tanyakan ke pengguna), lalu jalankan ulang.")
    sys.exit(2 if gagal else 0)


if __name__ == "__main__":
    main()
