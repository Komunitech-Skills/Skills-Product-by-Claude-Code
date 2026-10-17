#!/usr/bin/env python3
"""Olah masukan pelanggan dari BANYAK kanal (chat WhatsApp hasil ekspor, ulasan marketplace,
komentar IG/TikTok, survei) menjadi angka & daftar isu teratas.

Yang dilakukan (deterministik, bisa diulang, tanpa jaringan, Python 3.8+ standar):
1. Membaca: ekspor chat WhatsApp (.txt), CSV (ulasan/survei), atau teks tempelan (satu masukan per baris
   atau dipisah baris kosong). Encoding UTF-8, UTF-8 BOM, UTF-16 (ekspor "Unicode Text"), dan Windows-1252 dikenali.
2. MENYAMARKAN data pribadi otomatis SEBELUM analisis: nama pengirim chat, nomor HP & telepon rumah, email,
   tautan, @username, nomor pesanan/resi, alamat (jalan, gang, perumahan, blok, RT/RW), plat nomor, "a.n. Nama",
   "Saya Nama", sapaan+nama ("kak Budi", "makasih kak rina"). Kolom nama pembeli di CSV tidak pernah dicetak.
3. Menandai tema (rasa, kemasan, harga, pengiriman, layanan, fasilitas, waktu tunggu, ...) dan sentimen per klausa,
   termasuk negasi ("tidak enak", "kurang bersih", "belum datang", "tidak telat") dan slang/typo ringan.
4. Menghitung: jumlah per kanal, sentimen, NPS (bila ada nilai 0-10), keluhan/pujian/saran per tema,
   tren per bulan, skor prioritas = jumlah keluhan x dampak, dan tabel isu teratas.

Hasil script = SARINGAN PERTAMA. Agent/manusia wajib membaca & memverifikasi setiap tema lewat kutipan.

Contoh:
  python3 olah_masukan.py chat-wa.txt=WhatsApp ulasan.csv=Shopee komentar.txt=Instagram --staf "Admin,Dapur"
  python3 olah_masukan.py chat-wa.txt --daftar-pengirim
  python3 olah_masukan.py ulasan.csv --tema tema-saya.json --format json --simpan-anonim anonim.csv
"""
import argparse
import csv
import datetime
import io
import json
import os
import re
import sys
from collections import Counter, defaultdict

for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

VERSI = "1.0.14"


class Gagal(Exception):
    """Kesalahan yang dijelaskan ke pengguna (dicetak 'GAGAL: ...', kode keluar 2)."""


# ------------------------------------------------------------------ kamus bawaan
SLANG = {
    "brg": "barang", "bgt": "banget", "bngt": "banget", "bgtt": "banget", "bnget": "banget", "bangett": "banget",
    "gk": "tidak", "ga": "tidak", "gak": "tidak", "g": "tidak", "nggak": "tidak", "ngga": "tidak", "engga": "tidak",
    "enggak": "tidak", "tdk": "tidak", "kaga": "tidak", "kagak": "tidak", "ndak": "tidak", "nda": "tidak", "gx": "tidak",
    "tak": "tidak", "blm": "belum", "blum": "belum", "yg": "yang", "udh": "sudah", "udah": "sudah", "sdh": "sudah",
    "dah": "sudah", "krn": "karena", "karna": "karena", "sm": "sama", "ama": "sama", "dr": "dari", "jg": "juga",
    "lbh": "lebih", "dtg": "datang", "dateng": "datang", "tp": "tapi", "tpi": "tapi", "sy": "saya", "gw": "saya",
    "gue": "saya", "aku": "saya", "bgs": "bagus", "mantul": "mantap", "mantab": "mantap", "mantep": "mantap",
    "trims": "terima kasih", "makasih": "terima kasih", "makasi": "terima kasih", "thx": "terima kasih",
    "tks": "terima kasih", "terimakasih": "terima kasih", "thanks": "terima kasih",
    "kadaluarsa": "kedaluwarsa", "kadaluwarsa": "kedaluwarsa", "expired": "kedaluwarsa", "exp": "kedaluwarsa",
    "murmer": "murah", "rekomen": "recommended", "recomended": "recommended", "rekomended": "recommended",
    "recommend": "recommended", "rekomendasi": "recommended", "cs": "layanan", "adm": "admin", "gmn": "bagaimana",
    "gimana": "bagaimana", "kmrn": "kemarin", "kemaren": "kemarin", "org": "orang", "aja": "saja", "doang": "saja",
    "pesenan": "pesanan", "pesen": "pesan", "cepet": "cepat", "cpt": "cepat", "lg": "lagi", "lgi": "lagi",
    "jd": "jadi", "jdi": "jadi", "krg": "kurang", "krng": "kurang", "tlt": "telat", "lmbt": "lambat",
    "nyampe": "sampai", "nyampai": "sampai", "nyampek": "sampai", "sampe": "sampai", "smpe": "sampai", "smp": "sampai",
    "dibales": "dibalas", "bales": "balas", "balesnya": "balasnya", "ilang": "hilang", "ancur": "hancur",
    "trs": "terus", "bnyk": "banyak", "dpt": "dapat", "dapet": "dapat", "cakep": "cantik", "kece": "keren",
    "pedes": "pedas", "asem": "asam", "gede": "besar", "kegedean": "kebesaran", "dikit": "sedikit", "pake": "pakai",
    "dipake": "dipakai", "rapih": "rapi", "bersi": "bersih", "ramahh": "ramah", "lemot": "lambat", "lelet": "lambat",
    "lola": "lambat", "respon": "respons", "respond": "respons", "fastrespon": "responscepat", "fast": "cepat",
    "slow": "lambat", "ok": "oke", "okey": "oke", "okay": "oke", "good": "bagus", "nice": "bagus", "bad": "jelek",
    "jutek": "judes", "ketus": "judes", "dicuekin": "cuek", "dicuekkin": "cuek", "nyesel": "menyesal",
    "sobek": "robek", "sobekk": "robek", "resleting": "ritsleting", "sleting": "ritsleting", "pdhl": "padahal",
    "skrg": "sekarang", "td": "tadi", "tdi": "tadi", "bs": "bisa", "bsa": "bisa", "gabisa": "tidak bisa",
    "gaada": "tidak ada", "gada": "tidak ada", "gaenak": "tidak enak", "gasesuai": "tidak sesuai",
    "cacad": "cacat", "nunggu": "tunggu", "ditunggu": "tunggu", "menunggu": "tunggu", "antri": "antre",
    "antrian": "antrean", "restok": "restock", "smua": "semua", "sma": "sama", "utk": "untuk", "buat": "untuk",
    "kakk": "kak", "kaka": "kak", "ka": "kak", "gt": "begitu", "gitu": "begitu",
    # v1.0.3: slang/singkatan sehari-hari yang sering muncul di keluhan
    "belom": "belum", "blom": "belum", "belon": "belum", "blon": "belum", "abis": "habis", "mulu": "terus", "melulu": "terus",
    "trus": "terus", "trs2": "terus", "bosen": "bosan", "tetep": "tetap", "ttp": "tetap", "salkir": "salah kirim", "slh": "salah",
    "brng": "barang", "sz": "size", "wrn": "warna", "dikasi": "dikasih", "ngasih": "kasih", "ngasi": "kasih", "dikirimin": "dikirim",
    "kirimin": "kirim", "ngirim": "kirim", "ngirimnya": "kirimnya", "nganter": "antar", "nganterin": "antar", "anterin": "antar",
    "anter": "antar", "dianter": "diantar", "dianterin": "diantar", "orderan": "pesanan", "mateng": "matang", "rapet": "rapat",
    "ngular": "mengular", "sebel": "kesal", "kesel": "kesal", "bete": "kesal", "bt": "kesal", "males": "malas", "nungguin": "tunggu",
    "diread": "dibaca", "dicancel": "dibatalkan", "dicansel": "dibatalkan", "dicancelin": "dibatalkan", "dibatalin": "dibatalkan",
    "cancel": "batal", "cancelled": "batal", "canceled": "batal", "po": "preorder", "bulukan": "berjamur",
    "jamuran": "berjamur", "ngelupas": "mengelupas", "kelupas": "mengelupas", "copot": "lepas", "dpet": "dapat",
    "kerasa": "terlihat", "terasa": "terlihat", "gini": "begini", "ongkosnya": "ongkir", "readystock": "ready stock",
    "soldout": "habis", "gatel": "gatal", "gamau": "tidak mau", "gabakal": "tidak akan",
    # v1.0.5: "gpp/gapapa" = tidak apa-apa (penanda memaklumi)
    "gpp": "tidak apa apa", "gapapa": "tidak apa apa", "gakpapa": "tidak apa apa", "gapapah": "tidak apa apa", "nggakpapa": "tidak apa apa",
    "ngapapa": "tidak apa apa", "gppa": "tidak apa apa", "ndakpapa": "tidak apa apa", "tidakpapa": "tidak apa apa",
    # v1.0.6: chat didiamkan
    "dianggurin": "diabaikan", "dianggurkan": "diabaikan", "dikacangin": "diabaikan", "dikacangi": "diabaikan",
}
# Frasa -> satu token (diterapkan setelah slang, sebelum pecah klausa)
# v1.0.3: ketepatan pesanan berbasis POLA ("pesan/checkout X ... yang datang/dapat/dikasih Y"), bukan frasa hafalan.
_PESAN = r"(?:pesan|order|checkout|beli|minta|pilih|klik)\w*"
_TERIMA = r"(?:datang|sampai|dikirim|dikasih|diberi|dapat|diantar|nongol|muncul)(?:nya)?"
_DESKRIPTOR = (r"(?:yang|warna|ukuran|size|varian|rasa|level|no|nomor|model|motif|tipe|type|seri|paket|item|barang|produk|menu|"
               r"xs|s|m|l|xl|xxl|xxxl|\dxl|hitam|putih|merah|biru|hijau|kuning|coklat|cokelat|abu|ungu|pink|navy|cream|krem|maroon|tosca|"
               r"mocca|sage|original|ori|polos|bermotif|bukan)")
_JEDA = r"(?:(?:\w+|,)\s+){0,6}?"   # sampai 6 kata (boleh melewati koma) antara "pesan X" dan "yang datang Y"
_BUKAN_WAKTU_KATA = (r"(?:jam|hari|besok|lusa|minggu|bulan|tanggal|pagi|siang|sore|malam|telat|terlambat|lama|cepat|tepat|sesuai|pas|"
                     r"benar|lengkap|aman|sudah|juga|sama|persis|sesuaiharapan|tepatwaktu)$")
_BUKAN_WAKTU = (r"(?!\s+(?:jam|hari|besok|lusa|minggu|bulan|tanggal|pagi|siang|sore|malam|telat|terlambat|lama|cepat|tepat|sesuai|pas|"
                r"benar|lengkap|aman|sudah|juga|sama|persis|\d+\s*(?:hari|jam|menit|minggu))\b)")


def _angka_beda(m):
    """'beli 6 ... yang sampai 5' -> salah jumlah; 'beli 3 yang datang 3' dibiarkan (sesuai)."""
    a = re.findall(r"\d+", m.group(1))
    return m.group(0) if a and a[0] == m.group(2) else " salahpesanan "


_KATEGORI = {"yang", "warna", "ukuran", "size", "varian", "rasa", "model", "motif", "tipe", "type", "no", "nomor", "level", "seri", "paket",
             "item", "barang", "produk", "menu"}


def _beda_pesanan(m):
    """'pesan navy ... yang datang hitam' -> salah pesanan; 'pilih navy, yang sampai navy juga' / '... warna sesuai' dibiarkan."""
    awal = set(re.findall(r"[a-z0-9]+", m.group(1)))
    nilai = m.group(3) if m.group(2) in _KATEGORI else m.group(2)
    if (m.group(3) and re.match(_BUKAN_WAKTU_KATA, m.group(3))) or (nilai and nilai in awal):
        return m.group(0)
    return " salahpesanan "


def _gap(n):
    """v1.0.5: jendela 0..n kata antara dua bagian pola; tidak boleh melewati kata negasi ('segel masih utuh, belum pernah dibuka')."""
    return r"(?:(?!(?:tidak|belum|bukan|tanpa|jangan)\b)\w+\s+){0,%d}?" % n


# v1.0.5: "habis/abis" + kata berawalan di-/ter-/ke- = "sesudah" ("abis diservis", "abis ketiban", "abis terkena"), KECUALI kata kerja
# yang memang berarti stok habis dibeli orang ("habis diborong/dibeli/terjual") dan kata waktu berawalan ke- ("habis kemarin").
_HABIS_STOK_KK = r"(?:diborong\w*|dibeli\w*|dipesan\w*|dipesen\w*|dijual\w*|terjual|laku|diambil\w*|dibooking|dibook|keburu|kemarin|kemaren|kecuali|kebagian|ketika)\b"
# kata di klausa yang menandakan arti stok ("abis dibawa pulang, ga kebagian" tetap stok)
_HABIS_STOK_KONTEKS = r"(?![^.!?;,]*\b(?:kebagian|stok|stock|kosong|sold|restock|ready|preorder|kehabisan)\b)"
# v1.0.5: salah kirim UMUM "pesan/order/beli X ... (yang) datang/dikirim/dikasih Y" dengan Y berbeda dari X, untuk barang APA PUN
# (angka/satuan/pecahan/kata benda), bukan hanya deskriptor fashion. Y dianggap barang bila tidak berisi kata waktu/penilaian/orang.
_Y_BATAS = set("""tapi namun padahal karena dan dengan dalam ke di dari pada jadi sudah sih deh kok ya kak min nih dong lho loh banget sekali
juga lagi semua semuanya kondisi keadaan walau meski terus""".split())
_Y_BUKAN_BARANG = set("""jam hari besok lusa minggu bulan tahun tanggal pagi siang sore malam subuh kemarin tadi sekarang nanti kemudian
langsung duluan belakangan sesuai pas persis sama benar lengkap aman utuh selamat tepat cepat lambat lama telat terlambat kilat awal akhir
bonus gratis hadiah diskon promo cashback voucher poin free extra tambahan lebih kurang cuma hanya cuman sesuaiharapan tepatwaktu pasbanget
kurir driver ojol ojek abang bapak mas mbak orang orangnya pengantar satpam tetangga paket paketnya resi sampai datang dikirim dalamwaktu""".split())
_SATUAN = set("""porsi pcs pc buah biji lembar pasang dus box kotak bungkus pack pak botol kaleng kg kilo gram gr ons meter m cm mm inch inci
liter ml lusin kodi set unit ekor batang sak karung roll rol ikat sisir tangkai pot polybag yang nya""".split())
_X_BUKAN_BARANG = set("""di ke dari lewat via sama dengan untuk jam kemarin tadi hari minggu bulan pagi siang sore malam sekarang online disini
sini situ lagi sudah dulu""".split())
_TERIMA_TANPA_YANG = {"dikasih", "dikirim", "diberi", "dikasihnya", "dikirimnya", "diberinya"}


def _dasar(t):
    return re.sub(r"nya$", "", t) if len(t) > 5 else t


def _salah_barang(m):
    x = [t for t in re.findall(r"[a-z0-9]+", m.group(2))]
    if not x or x[0] in _X_BUKAN_BARANG:
        return m.group(0)
    if not m.group(3) and m.group(4) not in _TERIMA_TANPA_YANG:
        return m.group(0)
    y_semua = m.group(5).split()
    y = []
    for t in y_semua:
        if t in _Y_BATAS:
            break
        y.append(t)
    ekor = " ".join(y_semua[len(y):])
    if not y or any(t in _Y_BUKAN_BARANG or t in NEGATOR or t in POS or t in NEG or t in AKSI for t in y):
        return m.group(0)
    xs = {_dasar(t) for t in x}
    beda = [t for t in y if re.fullmatch(r"[a-z0-9]+", t) and _dasar(t) not in xs and t not in _SATUAN]
    if not beda:
        return m.group(0)
    return " salahpesanan " + ekor + " "


# v1.0.6: "takut/khawatir/ragu X, ternyata aman/utuh/sampai" = kekhawatiran yang TIDAK terjadi -> X bukan keluhan.
# Bila sesudah "ternyata" tidak ada kata lega ("takut telat, ternyata beneran telat"), X tetap dihitung.
_LEGA = (r"(?:aman|utuh|selamat|sampai|tiba|datang|bagus|baik|oke|mulus|sesuai\w*|tepat|cepat|lancar|enak|pas\w*|rapi|rapat|awet|kuat|"
         r"kokoh|original|ori|asli|beres|dibungkus|tidak\s+(?:ada\s+(?:yang\s+)?)?(?:pecah|rusak|telat|terlambat|bocor|penyok|lecet|retak|"
         r"luntur|palsu|kw|masalah|kenapa|lama))")
_KHAWATIR = (r"\b(?:takut|khawatir|kuatir|ragu|cemas|was(?:\s+was)?|deg\s*(?:-\s*)?(?:deg)?an|degdegan)\b[^.!?;]{0,60}?"
             r"(?=[,\s]+(?:(?:eh|tapi|namun|alhamdulillah|syukurlah|untungnya|untung)\s+)?(?:ternyata|alhamdulillah|syukurlah|untungnya|"
             r"eh)\s+(?:\S+\s+){0,4}?" + _LEGA + r"\b)")
# v1.0.6: "dingin" bernilai baik untuk AC/kulkas/minuman/ruangan ("AC nya tidak dingin" = keluhan), buruk untuk makanan (aturan lain).
_ANCHOR_DINGIN = r"(?:ac|kulkas|freezer|es|minuman|ruangan|ruang|kamar|kelas|mobil|kabin|showcase|pendingin)"


def _lama_wajar(m):
    """'telat 10 menit karena macet, wajar' -> alasan sesudah 'karena' tidak ikut dihitung ('macet' bukan keluhan produk)."""
    g = m.group(1)
    a = re.search(r"\b(?:karena|soalnya|gara\s+gara|akibat|sebab|mungkin|namanya)\b", g)
    return "lamawajar" + (g[:a.start()] if a else g)


# v1.0.4: konteks yang mengubah arti kata keluhan (dijalankan paling awal)
_HABIS_SESUDAH = (r"pakai|dipakai|memakai|pemakaian|makan|dimakan|minum|diminum|mandi|cuci|dicuci|mencuci|tidur|bangun|olahraga|kerja|"
                  r"pulang|gajian|lebaran|kena|dilindas|dilindes|dilindas|ditabrak|diinjak|dibanting|dilempar|dipukul|digebuk|digiling|"
                  r"jatuh|dijemur|disetrika|oles|dioles|operasi|melahirkan|nonton|main|belanja|itu|begitu")
FRASA_104 = [
    (_KHAWATIR, "semularagu"),
    (r"\b(" + _ANCHOR_DINGIN + r"(?:\s*nya)?\s+(?:(?!(?:tapi|namun|padahal)\b)[a-z]+\s+){0,5}?)dingin\b", r"\1sejuk"),
    (r"\bdingin\b(?=\s+(?:[a-z]+\s+)?(?:ac|kulkas|freezer|ruangan)\b)", "sejuk"),
    # "abis/habis" = sesudah/seperti sesudah ("abis pake ini muka merah", "kayak abis dilindes truk"), bukan stok habis
    (r"\b(kayak|kaya|kyk|kek|seperti|bagai|bagaikan|macam|mirip|kayaknya)\s+habis\b", r"\1 sesudah"),
    (r"\bhabis\s+(?=(?:" + _HABIS_SESUDAH + r"|ini|\d+\s*(?:x|kali|hari|minggu|bulan)\s+(?:di)?(?:pakai|cuci|oles|minum))\b)", "sesudah "),
    (r"\bhabis\s+" + _HABIS_STOK_KONTEKS + r"(?=(?!" + _HABIS_STOK_KK + r")(?:di|ter|ke)[a-z]{3,}\b)", "sesudah "),
    # "jual/kirim stok lama" = barang lama/kedaluwarsa (keamanan), bukan stok kosong
    (r"\b(?:jual|kirim|dikirim|dikasih|dapat|diberi)\w*\s+(?:\w+\s+){0,2}?(?:stok|stock)\s+lama\b"
     r"|\bini\s+(?:stok|stock)\s+lama\b|\b(?:stok|stock)\s+lama\b(?=\s*(?:(?:ya|kah|nih|deh|sih|kak|min|kayaknya|sepertinya)\s*)*(?:[?.!]|$))",
     "stoklama"),
    # "lama/telat ..., wajar/maklum" = pelanggan memaklumi -> netral (bukan keluhan, bukan pujian)
    (r"\b(?:lama|telat|terlambat|lambat|molor|ngaret)(?:\s+(?:sedikit|banget|sekali|juga))?\b([^.!?;]{0,50}?)[,\s]+(?:masih\s+|cukup\s+|sangat\s+|jadi\s+)?(?:wajar|maklum|"
     r"dimaklumi|dimaklum|bisa\s+dimaklumi|dimengerti|bisa\s+dimengerti|tidak\s+apa(?:\s+apa)?|tidak\s+masalah)\b", _lama_wajar),
    # v1.0.6 "cuma/hanya telat 5 menit" = pelanggan mengecilkan keterlambatan menit -> dimaklumi
    (r"\b(?:cuma|hanya|cuman)\s+(?:telat|terlambat|lambat)\s+(?:\d+\s*|se|beberapa\s+)menit\b", "lamawajar"),
    (r"\b(?:wajar|maklum|dimaklumi|tidak\s+apa\s+apa|tidak\s+masalah)\s+(?:(?:kalau|kalo|jika|bila|sih|lah|saja|kok|kak|ya|min|mas|mbak|"
     r"bu|pak|deh|kalaupun|walau|meski)\s+){0,2}(?:agak\s+|sedikit\s+)?(?:lama|telat|terlambat|lambat)\b", "lamawajar"),
    # "di read doang", "cuma dibaca" = chat diabaikan (layanan)
    (r"\b(?:(?:cuma|hanya|cuman)\s+dibaca|dibaca\s+saja)\b(?=\s*(?:$|[,.!?;]|tidak|belum|tanpa|terus|lagi|sampai|dari))", r"\g<0> diabaikan"),
    # segel terbuka/rusak = kemasan (dan bisa keamanan) - keluhan
    (r"\bsegel\w*\s+" + _gap(8) + r"(?:terbuka|kebuka|dibuka|rusak|robek|lepas|hilang|bolong|putus|tidak\s+ada)\b", "segelrusak"),
    # permukaan lengket = kebersihan; tekstur produk lengket BUKAN kebersihan (tanpa kata meja/lantai/dll.)
    (r"\b((?:meja|lantai|kursi|piring|gelas|sendok|garpu|mangkok|mangkuk|nampan|gagang|pegangan|toilet|wastafel|karpet|sofa|menu|"
     r"tempat\s+duduk)(?:nya)?\s+" + _gap(4) + r")lengket\b", r"\1lengket kotor"),
    # v1.0.6: keterlambatan BERANGKA ("telat 2 jam", "molor 3 hari") = keluhan kuat walau klausa yang sama memuji hal lain;
    # "cuma/hanya telat 5 menit" dibiarkan (pelanggan mengecilkan). Dijalankan sesudah aturan "wajar/maklum".
    (r"(?<!cuma )(?<!hanya )(?<!cuman )\b(?:telat|terlambat|molor|ngaret|mundur|diundur|kelamaan)\s+(?:(?:sampai|hingga|lebih|dari|hampir|"
     r"sekitar|kurang|sudah)\s+){0,2}(?:\d+\s*|se|(?:satu|dua|tiga|empat|lima|setengah)\s+)(?:menit|jam|hari|minggu|bulan)\b", "telatlama"),
    # v1.0.7: "baru dikirim/dibalas setelah 5 hari" = keterlambatan berangka (kata kerjanya tetap ada untuk tema)
    (r"\bbaru\s+(?:\w+\s+){0,3}?(?:setelah|sesudah)\s+(?:\d+\s*|se|(?:satu|dua|tiga|empat|lima|setengah)\s+)(?:menit|jam|hari|minggu|bulan)\b",
     r"\g<0> sudahlama"),
]
FRASA_103 = [
    (r"(?:^|(?<=[,.!?] ))(?:jujur|sejujurnya)(?:\s+(?:saja|ya|sih|deh|nih))?\b", "sejujurnya"),  # "jujur, ..." = pembuka, bukan pujian
    (r"\bongkos\s+(?:kirim|antar)\w*", "ongkir"),
    # pengiriman: nyasar / tidak diterima
    (r"\b(?:diterima|dikirim|diantar|antar|sampai|nyasar)\w*\s+(?:ke\s+)?(?:orang|alamat|rumah|tempat|kota)\s+(?:lain|yang\s+salah|tetangga)\b"
     r"|\bsalah\s+alamat\b|\b(?:muter|mutar|putar|keliling)\s+(?:\w+\s+)?(?:sejam|lama|\d+\s*(?:jam|menit|hari|minggu)|berjam\s+jam|berhari\s+hari)\b", "nyasar"),
    (r"\b(?:tidak|belum)\s+(?:pernah|juga|kunjung)\s+(?:(?:saya|kami|aku)\s+)?(?:di)?terima\b|\bbelum\s+(?:(?:saya|kami|aku)\s+)?(?:di)?terima\b"
     r"|\btidak\s+(?:saya|kami|aku)\s+terima\b", "belumsampai"),
    # ketepatan pesanan
    (r"\b(?:beda|berbeda|lain|tidak\s+sesuai|tidak\s+sama)\s+(?:dengan\s+|sama\s+|dari\s+)?(?:apa\s+)?yang\s+(?:saya\s+|aku\s+|kami\s+|sudah\s+)?"
     r"(?:di)?(?:pesan|order|pilih|klik|checkout|beli|minta|tulis|catat)\w*|\btidak\s+sesuai\s+(?:dengan\s+)?(?:catatan|request|permintaan|"
     r"pesanan|checkout)\b", "salahpesanan"),
    (r"\b" + _PESAN + r"\s+" + _JEDA + r"(?:malah|kok|justru|eh|tapi)\s+(?:yang\s+|malah\s+)?" + _TERIMA + r"\b" + _BUKAN_WAKTU,
     "salahpesanan"),
    (r"\b(" + _PESAN + r"\s+" + _JEDA + r")yang\s+" + _TERIMA + r"\s+(\d+)\b", _angka_beda),
    (r"\b((?:pesan|order|beli|bayar|dibayar)\w*\s+\d+\s+(?:\w+\s+){0,3}?)(?:cuma|hanya|cuman)\s+(?:di)?(?:kirim|datang|dapat|sampai|kasih|isi|bungkus|antar|terima|"
     r"masuk|hitung|ada)\w*\s+(\d+)\b", _angka_beda),
    (r"\b(" + _PESAN + r"\s+" + _JEDA + r")(?:yang\s+)?" + _TERIMA + r"\s+(?:malah\s+|justru\s+|kok\s+)?(" + _DESKRIPTOR +
     r")\b(?:\s+([a-z0-9]+)\b)?", _beda_pesanan),
    (r"\b(" + _PESAN + r")\s+((?:(?:[a-z0-9]+|,|/)\s+){1,7}?)(?:(yang)\s+)?(" + _TERIMA + r")\s+([a-z0-9/]+(?:\s+[a-z0-9/]+){0,5})",
     _salah_barang),
    (r"\b" + _TERIMA + r"\s+(?:yang|warna|ukuran|size|varian|model|motif)\s+(?:\w+\s+){0,2}?(?:padahal|harusnya|seharusnya|bukannya)\s+"
     r"(?:\w+\s+){0,3}?" + _PESAN, "salahpesanan"),
    (r"\b(?:datang|dikirim|sampai|dapat|dikasih)\w*\s+bukan\s+(?:yang|barang|warna|ukuran|varian|model|pesanan)\b", "salahpesanan"),
    (r"\bbukan\s+(?:yang|barang|warna|ukuran|varian|model)\s+(?:\w+\s+){0,2}?(?:saya\s+|aku\s+|kami\s+)?(?:di)?" + _PESAN, "salahpesanan"),
    (r"\b(?:varian|warna|ukuran|size|model|motif|menu|item|barang|isi|isinya|topping|pesanan|produk|tipe|level)(?:nya)?\s+(?:yang\s+)?"
     r"(?:(?:datang|dikirim|dikasih|sampai|diberi|diantar)(?:nya)?\s+)?salah\b", "salahpesanan"),
    (r"\b(?:catatan|note|notes|request|permintaan)\w*\s+(?:(?:\w+|,)\s+){0,10}?(?:diabaikan|dicuekin|cuek|tidak\s+(?:dibaca|diikuti|"
     r"dituruti|diperhatikan|digubris)|tetap\s+(?:saja\s+)?(?!dilayani|ramah|enak|bagus|mantap|oke|cepat)[a-z]+)\b", "salahpesanan"),
    (r"\b(?:dikirim|dikasih|diberi|dapat|datang|diantar)(?:nya)?\s+(?:yang|barang|produk|item|warna|ukuran|model)\s+(?:lain|beda|berbeda|salah)\b",
     "salahpesanan"),
    (r"\b(?:cuma|hanya|cuman)\s+(?:di)?(?:kirim|datang|dapat|sampai|kasih|isi|bungkus|antar|terima|masuk|hitung)\w*\s+\d+\b|\bkurang\s+(?:item|barang|pcs|biji|satu|sebiji)\b"
     r"|\b(?:jumlah|jumlahnya|item|itemnya)\s+(?:\w+\s+)?kurang\b"
     r"|\b(?:bonus|hadiah|gift|freebie\w*|gratisan|merchandise|merch|souvenir|kelengkapan|aksesori\w*)\s+(?:\w+\s+){0,5}?(?:tidak|belum)\s+"
     r"(?:pernah\s+|juga\s+)?(?:ada|dikasih|dikirim|dimasukkan|dimasukin|datang|sampai|diberi|termasuk)\b"
     r"|\btidak\s+(?:pernah|juga)\s+(?:dikasih|dimasukkan|dimasukin|disertakan|diberi)\b", "kurangjumlah"),
    # stok
    (r"\b(?:selalu|sering|sudah|lagi|terus)\s+sold\b|\b(?:ternyata|malah|tapi|eh)\s+(?:harus\s+|mesti\s+|jadi\s+|masih\s+)?(?:preorder|indent|inden)\b"
     r"|\btidak\s+pernah\s+ada\s+lagi\b|\btidak\s+(?:pernah\s+)?(?:dijual|diproduksi|tersedia|dibuat|restock)\s+lagi\b"
     , "habis"),
    (r"\bkapan\s+(?:\w+\s+){0,2}?(?:diisi|dibuat|dijual|diproduksi|produksi|stok)\s+lagi\b"
     r"|\bkapan\s+(?:\w+\s+){3,4}?(?:restock|ready|tersedia)\b", "tanyarestock"),
    (r"\b(?:masih|belum)\s+(?:juga\s+)?(?:di)?(?:kemas|proses|packing|pack|pick\s*up|pickup)\w*", "belumdikirim"),
    (r"\b(?:makin|semakin|tambah)\s+(?:kecil|sedikit|tipis|dikit)\b", "sedikit"),
    # kualitas / rasa / nada kecewa
    (r"\bdead\s*pixel\b", "deadpixel"),
    (r"\bmasih\s+(?:merah|berdarah)\b", "mentah"),
    (r"\b(?:sudah|baru\s+dibuka\s+sudah)\s+(?:asam|berlendir|menggumpal|bau\s+asam)\b", "basi"),
    (r"\btidak\s+(?:terlalu\s+|begitu\s+)?rapat\b", "tidakrapat"),
    (r"\bkok\s+(?:jadi\s+)?(?:begini|begitu)\b", "mengecewakan"),
    (r"\b\d+\s*menit\s+baru\b", "sudahlama"),
    (r"\b(?:sampai|hingga)\s+(?:sekarang|saat\s+ini|hari\s+ini|detik\s+ini|kini)\b", "hinggakini"),
    # v1.0.5: "tidak sampai sejam/2 hari sudah ..." = kurang dari (cepat), bukan "belum sampai"
    (r"\btidak\s+(?:sampai|hingga)\s+(?=(?:\d+\s*(?:menit|jam|hari|minggu)|se(?:jam|hari|minggu|menit)|setengah\s+(?:jam|hari))\b)", "dalamwaktu "),  # bukan tema pengiriman
]
# v1.0.8 (temuan uji OpenClaw toko kue): tekstur kue gagal, jamur tanpa kata "jamur", keterlambatan tanpa kata "telat"
_HARI_JAM = (r"(?:senin|selasa|rabu|kamis|jumat|sabtu|minggu|besok\w*|lusa|pagi|siang|sore|malam|subuh|tengah\s+malam|tanggal\s+\d+|"
             r"tgl\s+\d+|jam\s+\d+|pukul\s+\d+|\d+\s*(?:jam|hari|minggu))")
FRASA_108 = [
    # "roti sobek" = nama produk, bukan barang robek
    (r"\broti\s+robek(nya)?\b", r"rotisobek\1"),
    # bintik hijau/putih berbulu di makanan = jamur awal (keamanan), bukan kualitas biasa
    (r"\b(?:ber)?bintik\w*\s+(?:\w+\s+)?(?:hijau|biru|putih\s+berbulu|hitam\s+berbulu)\b|\bberbulu\s+(?:hijau|putih|halus)\b", "berjamur"),
    # tekstur kue/roti gagal: "bantat", "tengahnya (masih) basah/mentah/lembek"
    (r"\b(?:tengah|dalam|bagian\s+dalam)(?:nya)?\s+(?:masih\s+|agak\s+|sedikit\s+|kok\s+)?(?:basah|mentah|lembek|bantat|belum\s+matang)\b",
     "tengahbasah"),
    # "nyampe jam 4 padahal janjinya jam 10" = terlambat (tanpa kata telat)
    (r"\b((?:sampai|datang|tiba|diantar|dikirim|diterima)\w*\s+(?:\w+\s+){0,5}?)(?=,?\s*padahal\s+(?:\w+\s+){0,2}?(?:di)?janji)", r"\1telatlama "),
    (r"\b((?:sampai|datang|tiba|diantar|dikirim)\w*\s+)(?=(?:\w+\s+){0,2}?(?:lewat|melewati|lebih\s+dari)\s+(?:jam\s+)?(?:janji|estimasi|jadwal))",
     r"\1telatlama "),
    # "acara sudah bubar/selesai" saat barang datang = terlambat
    (r"\bacara\w*(?:\s+[a-z]+)?\s+(?:sudah\s+|telah\s+)?bubar\b|\bacara\w*(?:\s+[a-z]+)?\s+(?:sudah|telah)\s+(?:selesai|kelar|usai)\b",
     "telatlama acara"),
    # "baru nyampe hari jumat, padahal pesan senin" / "pesan senin baru sampai jumat"
    (r"\b(baru\s+(?:sampai|datang|tiba|diterima|dikirim)\w*\s+(?:hari\s+)?" + _HARI_JAM + r")\b(?=[^.!?]{0,30}?\bpadahal\b)", r"\1 sudahlama"),
    (r"\b((?:pesan|order|checkout|beli|bayar|transfer)\w*\s+(?:(?:dari|sejak|hari|tanggal|tgl)\s+)*" + _HARI_JAM +
     r"\b[^.!?]{0,40}?\bbaru\s+(?:sampai|datang|tiba|diterima|dikirim)\w*)", r"\1 sudahlama"),
    # "lama banget pesanannya" / "paket saya kok lama" = pengiriman lambat (bukan "tahan lama")
    (r"\b(?:lama|lambat)\b(?=\s+(?:banget\s+|sekali\s+|amat\s+)?(?:\w+\s+){0,2}?(?:pesanan|paket|kiriman)\w*\b)", "lama telatlama"),
    (r"\b((?:pesanan|paket|kiriman)\w*\s+(?:(?!tahan\b)\w+\s+){0,3}?)(?<!tahan )(?:lama|lambat)\b(?!\s+(?:sekali\s+)?(?:dipakai|awet|tahan))",
     r"\1lama telatlama"),
]
FRASA = FRASA_108 + FRASA_104 + FRASA_103 + [
    (r"\bkurang\s+lebih\b", "kuranglebih"),
    (r"(?:\btidak\s+ada\s+(?:yang\s+)?(?:minus|masalah|kendala|keluhan|kekurangan|komplain|cacat|lecet|kurang)(?:nya)?\b"
     r"|\btanpa\s+(?:minus|cacat|kendala|masalah)\b|\bno\s+minus\b)(?:\s+(?:sedikit\s*pun|satu\s*pun|sama\s+sekali|apa\s*pun))?", "tanpaminus"),
    (r"\bkurang\s+(?:\d+|satu|dua|tiga|empat|lima|se(?:biji|bungkus|kotak|porsi|potong|pcs|buah|lembar|pasang))\b|\b(?:yang\s+)?(?:datang|sampai|dikirim|dapat|isinya?)\s+(?:cuma|hanya|cuman)\s+\d+\b|\btidak\s+lengkap\b"
     r"|\b(?:datang|sampai|dikirim|dapat)\s+(?:cuma\s+|hanya\s+)?(?:1|satu)\s+(?:biji|buah|pcs|pasang|lembar|potong)?\s*(?:saja)?(?=\s*(?:$|[,.!?;]))"
     r"|\btidak\s+(?:dimasukkan|dimasukin|dimasukan|disertakan|dibungkus|dibawakan|dikasih|dikasi|termasuk)\b"
     r"|\blupa\s+(?:dimasukkan|dimasukin|dimasukan|dikirim|dibungkus)\b", "kurangjumlah"),
    (r"\b\d+\s*(?:x|kali)\s+(?:pesan\w*|order)\s+\d+\s*(?:x|kali)\s+salah\b|\bsalah\s+(?:terus|lagi|melulu)\b"
     r"|\b(?:pesan\w*|order)\s+(?:\w+\s+){0,5}?(?:tapi\s+|malah\s+|kok\s+)?(?:dikasih|dikirim|diberi)\s+(?:yang|item|warna|ukuran|size|rasa|varian|model|barang\s+lain)\b"
     r"|\b(?:pesan\w*|order)\s+(?:\w+\s+){0,3}?(?:tapi|malah|kok)\s+(?:dapat|datang)\b", "salahpesanan"),
    (r"\b(?:pas|waktu|saat|begitu)\s+(?:datang|sampai|tiba|diterima)\s+(?:sudah\s+|udah\s+)?(?:dingin|kempes|melempem)\b", "makanandingin"),
    (r"\bkapan\s+(?:\w+\s+){0,2}?(?:restock|ready|ada\s+lagi|tersedia|masuk\s+lagi|balik|kembali\s+ada)\b|\b(?:restock|ready)\s+kapan\b",
     "tanyarestock"),
    (r"\btidak\s+kebagian\b|\bout\s+of\s+stock\b|\boos\b|\bludes\b|\b(?:sering|selalu)\s+(?:habis|kosong)\b|\b(?:habis|kosong)\s+terus\b", "habis"),
    (r"\b(?:dikirim|dikasih|diberi)\s+salah(?:\s+(?:warna|ukuran|size|varian|model|barang|menu|produk|item))?\b|\btidak\s+sesuai\s+(?:pesanan|order)\b|\bsalah\s+(?:pesan(?:an)?|kirim|item|ambil|isi|warna|ukuran|size|varian|"
     r"model|barang|menu|produk|alamat|hitung)\b", "salahpesanan"),
    (r"\btidak\s+sesuai\b|\bbeda\s+(?:jauh|banget|sekali|warna|ukuran|bahan|model|dengan|sama|dari)\b|\btidak\s+(?:kayak|seperti|mirip)\s+"
     r"(?:di\s+)?(?:foto|gambar|deskripsi|iklan|contoh)", "tidaksesuai"),
    (r"\bresponscepat\b|\bcepat\s+respons\w*|\brespons\w*\s+cepat\b|\bcepat\s+tanggap\b|\bgercep\b|\bcepat\s+dibalas\b", "responscepat"),
    (r"\blambat\s+respons\w*|\brespons\w*\s+lambat\b|\blama\s+(?:dibalas|balas\w*|respons\w*|direspons\w*)\b"
     r"|\bbalas(?:nya)?\s+lama\b", "responslambat"),
    (r"\border\s+lagi\b|\brepeat\s+order\b|\bbeli\s+lagi\b|\bpesan\s+lagi\b|\blangganan\b|\bsudah\s+lama\s+(?:langganan|beli|pakai|order)\b",
     "orderlagi"),
    (r"\btepat\s+waktu\b|\bon\s*time\b|\bdengan\s+selamat\b|\bsampai\s+aman\b|\baman\s+sampai\b", "tepatwaktu"),
    (r"\bworth\s*it\b|\bsepadan\b", "sepadan"),
    (r"\bsold\s*out\b", "habis"),
    (r"\bantr[ei]\w*\s+(?:\w+\s+)?(?:panjang|mengular|lama|penuh)\b", "tunggulama"),
    (r"\bsakit\s+perut\b", "sakitperut"),
    (r"\bbenda\s+asing\b|\b(?:nemu|menemukan|ketemu|ditemukan|temukan|ada)\s+(?:plastik|kerikil|batu|staples|stapler|kawat|"
     r"kaca|beling|belatung|kuku|isolasi)\b", "bendaasing"),
    (r"\bsesuai\s+(?:foto|gambar|deskripsi|pesanan|order|harapan|ekspektasi)\b", "sesuaiharapan"),
    (r"\bpas\s+(?:banget|sekali|di\s*badan|di\s*kaki|ukuran\w*)\b|\b(?:ukuran|size|porsi|harga|rasa)(?:nya)?\s+(?:sudah\s+)?pas\b",
     "pasbanget"),
    (r"\bharga(?:nya)?\s+(?:\w+\s+){0,2}naik\b|\bnaik\s+(?:terus|lagi)\b|\bnaik\s+harga\b", "harganaik"),
    (r"\bsudah\s+(?:\d+\s*(?:hari|minggu|bulan|jam)|seminggu|sebulan|berhari\s+hari|berminggu\s+minggu)\b"
     r"|\b\d+\s*(?:hari|minggu|jam)\s+baru\b", "sudahlama"),
    (r"\btunggu\w*\s+(?:\w+\s+)?(?:\d+\s*(?:menit|jam|hari)|lama|kelamaan|sejam|berjam\s+jam|setengah\s+jam)\b", "tunggulama"),
    (r"\bcepat\s+(?:rusak|pudar|luntur|robek|basi|lepas|kusut|lecek|rontok|patah|mati|jebol|berjamur|melar)\b", "cepatrusak"),
    (r"\b(?:ac|wifi|wi\s*fi|lampu|kipas|listrik|colokan|toilet|wc|air|lift|mesin)(?:\s*nya)?\s+(?:\w+\s+)?"
     r"(?:mati|rusak|lambat|putus|error|macet|mampet|bocor|kotor|bau|panas)\b", "fasilitasrusak"),
    (r"\b(?:musik|suara|lagu|speaker)(?:\s*nya)?\s+(?:\w+\s+)?(?:keras|kencang|kenceng|berisik)\b", "musikkeras"),
    (r"\b(?:makanan|nasi|lauk|kuah|sup|soto|bakso|mie|mi|pizza|ayam|burger|kopi|teh)(?:\s*nya)?\s+(?:\w+\s+)?"
     r"(?:dingin|sudah\s+dingin)\b", "makanandingin"),
    (r"\bmasih\s+(?:panas|hangat|anget)\b", "masihhangat"),
]
NEGATOR = {"tidak", "belum", "bukan", "tanpa", "jangan"}
# kata "aksi netral": setelah negasi berarti keluhan ("belum datang", "tidak dibalas", "tidak berfungsi")
AKSI = set("""datang sampai dikirim kirim balas dibalas respons direspons diproses proses berfungsi nyala menyala jalan masuk cair gerak
bergerak diangkat dihubungi bisa dikembalikan diganti ditanggapi update dikabari kabar dapat dicek diantar diterima terima jadi ada
ready tersedia jawab dijawab digubris dikonfirmasi konfirmasi diurus dilayani
pemberitahuan info informasi penjelasan kejelasan kepastian izin permisi balasan jawaban tanggapan dihubungi
selesai kelar beres rampung dijelaskan diinfokan diinformasikan diberitahu diberitahukan dikabarkan ditindaklanjuti dikerjakan
diselesaikan diperbaiki""".split())
# v1.0.5 cakupan negasi eksistensial: "tidak/belum ada (yang) X", "tanpa X", "bebas X", "anti X" dengan X kata masalah = pernyataan
# positif/netral ("tidak ada yang retak", "bebas noda", "gak ada bau apek"). Jendela beberapa kata, boleh melewati kata pengisi.
NEG_EKSIS_AWAL = {"tanpa", "bebas", "anti"}
NEG_EKSIS_ISI = set("""yang satupun satu pun sedikitpun sedikit sama sekali apapun apa pun lagi tanda kok sih ya kak min dan atau maupun ataupun
serta juga the""".split())
JENDELA_EKSIS = 4
JENDELA_HILANG = 5
# masalah yang "hilang/sembuh" = hasil baik ("noda membandel bisa hilang", "jerawat hilang"), bukan barang hilang
PENGHILANG = {"hilang", "lenyap", "sembuh", "berkurang", "teratasi", "minggat", "rontok"}
MASALAH_HILANG = set("""noda bau apek amis anyir pesing tengik busuk kotor kotoran debu berdebu jerawat jerawatan iritasi gatal perih kusam
karat karatan jamur berjamur lengket kerak flek ketombe sakit nyeri pegal pegel mual lecet kusut breakout keringat gores goresan baret kerut
keriput bengkak demam batuk pilek pusing bintik bruntusan komedo lumut kerak""".split())
POS = set("""enak lezat nikmat mantap bagus puas suka cepat rapi ramah sopan murah terjangkau fresh segar hangat renyah empuk gurih
recommended top oke keren juara wangi harum hemat bersih higienis aman kenyang mengenyangkan responsif adem nyaman cozy cantik lembut halus
awet kokoh kuat sesuai amanah sabar informatif jujur sigap tanggap perfect sempurna best love lucu mulus kilat ori original asli bersahabat
akurat lumayan senang cinta memuaskan istimewa teliti profesional helpful membantu tebal wow matang
responscepat orderlagi tepatwaktu sepadan sesuaiharapan tanpaminus pasbanget masihhangat terima kasih
terang sejuk lancar stabil jernih semularagu utuh""".split())
NEG = set("""telat terlambat lama basi jelek kecewa mahal bocor tumpah rusak salah lambat pelit hambar anyep lembek pera keras alot gosong
mentah tidaksesuai salahpesanan penyok kotor jorok dekil kumuh berdebu lengket bau amis apek tengik anyir pesing busuk judes kasar cuek galak sombong lupa tertukar ketuker
kedaluwarsa rambut serangga lalat semut ulat kecoa belatung tikus jamur berjamur cacat luntur pudar kusam lepas robek tipis nerawang
sakitperut mual muntah diare keracunan jijik komplain marah zonk tipu penipu bohong kapok menyesal habis kehabisan ribet susah sulit masalah
parah mengecewakan buruk kekecilan kebesaran kesempitan kepanjangan kependekan sedikit responslambat bendaasing lecet lecek retak patah
hancur remuk pecah penyok macet error mati panas gerah pengap berisik bising sempit hilang ketinggalan kelupaan nyasar ngaret molor kelamaan
kemahalan kemanisan keasinan kepedasan kepahitan keasaman kusut noda jerawat jerawatan iritasi gatal perih breakout jebol melar rontok
berantakan php kosong harganaik sudahlama tunggulama cepatrusak fasilitasrusak musikkeras makanandingin kurangjumlah
kesal jengkel sebal rugi dirugikan bosan malas batal dibatalkan rembes merembes stuck nyangkut tertahan mandek belumsampai mengelupas
bolong bengkok karatan konslet korslet longgar kendor deadpixel diabaikan tidakrapat belumdikirim berlendir menggumpal stoklama segelrusak
tersembunyi telatlama bantat tengahbasah""".split())
KELUHAN_KUAT = {"salahpesanan", "kurangjumlah", "bendaasing", "sakitperut", "belumsampai", "belumdikirim", "nyasar", "tidaksesuai",
                "keracunan", "basi", "kedaluwarsa", "telatlama"}
PENGUAT = {"begitu", "terlalu", "banget", "sekali", "agak", "sangat", "amat", "cukup", "sih", "juga"}
PERANTARA = {"pernah", "ada", "yang", "juga", "sama", "begitu", "terlalu", "sangat", "pula", "kunjung", "mau", "bisa", "jadi", "lagi", "sih",
             "dong", "kok", "terus", "cukup", "sampai", "dapat", "dikasih", "segera", "bikin", "membuat", "menimbulkan",
             "menyebabkan"}
BERLEBIH = {"terlalu", "kelewat", "kebanyakan", "kelewatan"}
# v1.0.6 "jarang + <kata sesudahnya>": kata kelangkaan (pujian "jarang nemu seller seramah ini") tidak dinilai sebagai keluhan
JARANG_LANGKA = {"ada", "nemu", "menemukan", "ketemu", "dapat", "lihat", "melihat", "liat", "dijumpai", "ditemukan", "ditemui", "terjadi"}
# v1.0.6 "belum + kata kerja di-" = harapan belum dipenuhi ("belum ditindaklanjuti"), kecuali kegiatan pembeli sendiri ("belum dicoba")
BELUM_WAJAR = {"dipakai", "dicoba", "dibuka", "dimakan", "diminum", "dites", "ditest", "dirasakan", "dirasa", "dicicipi", "dicuci", "dipasang",
               "dicek", "dibaca", "direview", "diulas", "dinilai", "dihitung", "dipakainya", "dicobain"}
_BUKAN_KK = set("""dingin dinding diri dirinya diam dimana dini dinas diet diskon dikit dia dian mereka member memang mentah menu menit mesin
meja merah mesjid mewah mending mendingan""".split())


def _kata_kerja(w):
    """v1.0.6: bentuk kata kerja dari imbuhannya (di-/me-/ng-), bukan dari daftar: 'dikuras', 'disapu', 'menjelaskan', 'ngangkat'."""
    if w in _BUKAN_KK or not w.isalpha():
        return False
    return ((len(w) >= 5 and w.startswith("di")) or (len(w) >= 6 and bool(re.match(r"me(?:m|n|ng|ny)?[a-z]{3,}$", w)))
            or (len(w) >= 5 and w.startswith("ng")))
SARAN = re.compile(r"\b(sebaiknya|semoga\s+ada|tolong\s+(?:ditambah|tambah|dibuat|dibuatkan|diperbaiki|dibenahi|diadakan)|mohon|"
                   r"kalau\s+bisa|usul\w*|saran\w*|request|harap|kapan\s+(?:ada|ready|buka|restock)|tanyarestock|bisa\s+tidak|boleh\s+tidak|"
                   r"tambahin|ditambah|dibuatkan|next|pengen|ingin|mau\s+dong)\b")
RE_OPTATIF = re.compile(r"\b(?:semoga|jangan|harap|mohon|tolong|supaya|biar|agar)\b")
TANYA_MINTA = re.compile(r"\b(kapan|bisa|boleh|ada|tolong|mohon|apakah|mau)\b")

# id, label, dampak (1-5), pola (bagian regex; imbuhan di-/ter-/ke-/ber- dan -nya/-kan/-an/-in/-ya dikenali)
TEMA_BAWAAN = [
    ("rasa", "Rasa / cita rasa", 4, r"rasa|enak|lezat|nikmat|gurih|hambar|anyep|asin|manis|pedas|pahit|asam|amis|gosong|mentah|renyah|empuk|"
     r"alot|keras|lembek|pera|bumbu|nendang|kematangan|matang|kemanisan|keasinan|kepedasan|kepahitan|keasaman|makanandingin|masihhangat|bantat|tengahbasah|tekstur"),
    ("kemasan", "Kemasan / packing", 3, r"kemasan|kemas|packing|packaging|pack|bungkus|dus|kardus|box|kotak|plastik|bubble|bubblewrap|bocor|"
     r"tumpah|penyok|segel|wadah|botol|toples|lakban|kresek|rembes|merembes|tidakrapat|segelrusak"),
    ("harga", "Harga / ongkir", 2, r"harga|mahal|murah|terjangkau|ongkir|diskon|promo|sepadan|biaya|tarif|hemat|pricey|kemahalan|harganaik"),
    ("pengiriman", "Pengiriman / ketepatan waktu", 3, r"kirim|pengiriman|kurir|ojol|ojek|gojek|grab|shopeefood|gofood|telat|terlambat|datang|"
     r"sampai|antar|tepatwaktu|delivery|resi|ekspedisi|jne|jnt|sicepat|anteraja|nyasar|kilat|ngaret|molor|dijemput|jemput|"
     r"pengantaran|kiriman|terkirim|estimasi|paket|lacak|tracking|tiba|keterlambatan|lamban|dititipkan|titip|satpam|belumsampai|belumdikirim|nyangkut|telatlama|"
     r"stuck|tertahan|mandek|manifest|transit|gudang\s+transit|spx|ninja|lion\s+parcel|wahana|idexpress|lalamove|paxel|gosend|grabexpress|"
     r"same\s*day|instan|instant|driver"),
    ("layanan", "Layanan / respons admin & staf", 3, r"admin|layanan|pelayanan|pelayan|respons|responscepat|responslambat|balas|chat|ramah|"
     r"sopan|judes|galak|cuek|diabaikan|jawab|staf|pegawai|karyawan|kasir|barista|waiter|waitress|teknisi|montir|mekanik|seller|penjual|ditanggapi|"
     r"tanggap|sabar|informatif|amanah|dilayani|melayani"),
    ("ketepatan_pesanan", "Ketepatan pesanan", 4, r"ketuker|ketukar|tertukar|kelupaan|lupa\s+dimasukkan|salahpesanan|kurangjumlah|ketinggalan|zonk|salah\s+item"),
    ("kualitas_produk", "Kualitas produk / sesuai foto", 4, r"kualitas|bahan|jahitan|jahit|awet|rusak|cacat|luntur|pudar|kusam|"
     r"warna(?=(?:nya)?\s+(?:\w+\s+)?(?:luntur|pudar|beda|berbeda|bagus|cantik|kusam|jelek|cerah|pucat|belang|keren|sesuai|"
     r"tidaksesuai|sesuaiharapan|cepatrusak|kalem|elegan))|"
     r"sesuaiharapan|tidaksesuai|patah|retak|lecet|berfungsi|robek|lepas|tipis|nerawang|ritsleting|kancing|macet|mati|ori|original|palsu|kw|"
     r"jerawat|jerawatan|iritasi|gatal|perih|breakout|kusut|noda|hasil|mulus|cepatrusak|jebol|melar|rontok|hancur|pecah|mengelupas|bolong|"
     r"bengkok|karat|karatan|konslet|korslet|longgar|kendor|deadpixel|layar|baterai|ngecas|dicas|nyala|menyala|sol|lem"),
    ("keamanan", "Keamanan produk (benda asing, basi, sakit)", 5, r"basi|kedaluwarsa|rambut|serangga|lalat|semut|ulat|belatung|kecoa|tikus|"
     r"bendaasing|sakitperut|diare|keracunan|mual|muntah|alergi|jamur|berjamur|jijik|berlendir|menggumpal|stoklama"),
    ("kebersihan", "Kebersihan", 3, r"kotor|jorok|higienis|bersih|kebersihan|debu|berdebu"),
    ("bau_aroma", "Bau / aroma", 3, r"bau|apek|tengik|anyir|pesing|busuk|wangi|harum|aroma"),
    ("porsi_ukuran", "Porsi / ukuran / size", 3, r"porsi|ukuran|size|kekecilan|kebesaran|kesempitan|kepanjangan|kependekan|pelit|kenyang|"
     r"mengenyangkan|gramasi|isian|pasbanget"),
    ("stok_ketersediaan", "Stok / ketersediaan", 2, r"habis|kosong|stok|stock|restock|tanyarestock|ready|preorder|kehabisan|persediaan|langka|indent|inden|kebagian|tersedia"),
    ("pembayaran", "Pembayaran / refund", 3, r"bayar|pembayaran|transfer|qris|cod|refund|pengembalian|kembalian|tagihan|invoice|nota|struk|"
     r"cashback|saldo"),
    ("varian_menu", "Varian / menu / pilihan", 2, r"varian|menu|pilihan|model|motif|koleksi|rasa\s+baru|warna\s+baru|warna\s+lain"),
    ("fasilitas", "Tempat / fasilitas", 3, r"tempat|wifi|wi\s*fi|ac|parkir|parkiran|toilet|wc|kamar\s+mandi|colokan|stopkontak|musik|kursi|"
     r"mushola|musala|ruangan|ruang|suasana|lampu|fasilitas|fasilitasrusak|musikkeras|berisik|bising|gerah|pengap"),
    ("waktu_tunggu", "Waktu tunggu / jadwal / antrean", 3, r"antre|antrean|antri|antrian|tunggu|tunggulama|kelamaan|disajikan|penyajian|selesai|kelar|"
     r"rampung|diselesaikan|dikerjakan|pengerjaan"),
]
AFIKS = (r"\b(?:di|ter|ke|ber)?(?:", r")(?:nya|kan|an|in|ya|ny|lah)?(?:nya)?\b")

# kata umum yang tidak pernah "dikoreksi" typo dan tidak dianggap nama
KATA_UMUM = set("""yang dan di ke dari untuk dengan ini itu saya kami kita kak ya nya juga sudah tidak tapi atau ada pada saja lagi sama
karena jadi bisa mau akan sih deh dong kok banget terima kasih nama nomor tautan akun email alamat harus segera kelas rumah motor mobil
gambar dinding sampah kabar lewat pasar catat kerang mantan merah putih hitam biru hijau kuning coklat cokelat ungu abu pink navy cream
krem maroon tosca mocca sage pastel emas perak bulan minggu hari jam menit tahun kemarin besok tadi pagi siang sore malam sekarang nanti
semua banyak besar kecil baru lama sekali masih belum pernah selalu sering jarang kadang langsung akhirnya ternyata padahal semoga
makan minum beli pesan pesanan order barang produk toko teman temen anak istri suami ibu bapak orang pembeli penjual pelanggan kantor
sekolah kerja nugas kuliah acara pengajian seragam grosir retur tukar ganti cuci dicuci setrika jemput antar ambil kirim bawa pakai
coba dicoba minta tanya ditanya jawab bilang kata cerita lihat liat foto video gambar kamera sama lain sebelah seperti kayak mirip
berapa kapan dimana mana siapa kenapa mengapa bagaimana apa apakah tolong mohon maaf halo hai selamat pagi salam permisi kalau jika
kalo biar supaya agar sebelum sesudah setelah waktu saat ketika pas sedang lagi baru mulai selesai habis sekitar hampir cuma hanya
paling lebih kurang sangat agak cukup terlalu begitu memang emang juga pula lalu terus kemudian akhir awal tengah atas bawah depan
belakang dalam luar samping sini situ sana nih tuh deh kok sih yah dong lah kah pun toh jangan boleh perlu wajib bakal akan hendak
ingin pengen suka senang sedih takut kira pikir rasa tahu kenal ingat lupa dengar tunggu tahan jual bayar harga ongkir diskon promo
kilo kiloan pcs buah biji lembar botol bungkus porsi gelas cup piring mangkok paket kardus plastik kertas nasi ayam ikan telur sayur
roti kue kopi susu teh gula garam minyak sambal bumbu kuah mie bakso soto sate martabak croissant latte matcha pastry donat brownies
baju kaos kemeja celana rok jilbab hijab gamis sepatu sandal tas dompet jam kacamata topi kaos kaki mukena sarung jaket hoodie dress
bahan kain jahitan warna ukuran model motif size ritsleting kancing laundry cucian pakaian kamar tamu tempat meja kursi pintu jendela
kasir admin kurir driver ojol seller owner bos mbak mas kakak adik abang bang tante om bro sis pak bu mba teh aa neng dek kang uda
servis service montir bengkel oli ban mesin rem aki charger baterai layar casing hp ponsel laptop printer kabel
tangga teknis kencang kenceng kentang bawang masak malah kecap bambu karang kurung pesaing berisiko
namax hpx teleponx emailx tautanx akunx nomorx alamatx platx""".split())
# sapaan & gelar, untuk penyamaran nama
SAPAAN_KATA = ["kak", "kakak", "ka", "bu", "ibu", "pak", "bapak", "mas", "mba", "mbak", "bang", "abang", "om", "tante", "bro", "sis", "teh",
               "aa", "neng", "dek", "kang", "uda", "cici", "koh", "ci", "ko", "bunda", "mama", "papa", "ayah", "umi", "abi", "haji", "hj",
               "bpk", "sdr", "sdri"]
SAPAAN = r"(?i:" + "|".join(sorted(SAPAAN_KATA, key=len, reverse=True)) + r")"
GELAR = r"(?:RT|RW|Haji|H\.|Hj\.?|dr\.?|Dr\.?|drg\.?|Ir\.?|Ustadz|Ustadzah|Ust\.?)"


# ------------------------------------------------------------------ penyamaran
RE_URL = re.compile(r"(?:https?://|www\.)\S+|\b(?:wa\.me|bit\.ly|shp\.ee|tokopedia\.link|vt\.tiktok\.com)/\S+", re.I)
RE_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
RE_HP = re.compile(r"(?<![\w/])(?:\+?62|0)[\s.-]?8\d{1,2}[\s.-]?\d{3,4}[\s.-]?\d{2,5}(?!\d)")
RE_TELP = re.compile(r"(?<![\w/.,])(?:\(0[2-7]\d{1,2}\)|0[2-7]\d{1,2}|\+62[\s.-]?[2-7]\d{1,2})[\s.-]?\d{3,4}[\s.-]?\d{3,5}(?![\d.,]*\d)")
RE_USER = re.compile(r"(?<![\w.])@[A-Za-z0-9_.]{2,}")
RE_NOPESAN = re.compile(r"\b(?:inv|invoice|order|pesanan|resi|no\.?\s*(?:pesanan|order|resi|inv))\s*[:#.\-]?\s*(?=[A-Za-z0-9\-/]*\d)[A-Za-z0-9\-/]{5,}\b", re.I)
# v1.0.6: kata berulang ber-angka 2 + akhiran ("teman2nya", "dimahal2in", "anak2ku") bukan kode/nomor
RE_KODE = re.compile(r"\b(?![a-z]{2,}2[a-z]{0,4}\b)(?=[A-Za-z0-9\-]*\d)(?=[A-Za-z0-9\-]*[A-Za-z])[A-Za-z0-9\-]{8,}\b|\b\d{9,}\b")
# v1.0.5: alamat dikenali per kata (nama jalan + nomor/blok/RT), berhenti di kata biasa -> kalimat keluhan sesudahnya tidak ikut tertelan.
# "jalan"/"gang" huruf kecil hanya dianggap alamat bila diikuti huruf besar/angka ("di jalan tol" bukan alamat).
RE_ALAMAT = re.compile(r"\b(?:(?i:jl|jln)\b\.?|(?i:gg)\.|(?i:gg)(?=\s+[A-Z0-9])|(?i:jalan|gang)(?=\s+[A-Z0-9]))\s*")
RE_ALAMAT2 = re.compile(r"\b(?i:perum(?:ahan)?|komplek|kompleks|komp|cluster|apartemen|apart|griya|villa|residence)\b\.?\s*")
RE_KATA_ALAMAT = re.compile(r"(?:[A-Z][\w'-]*\.?|\d+[A-Za-z]?(?:/\d+)?\.?|[A-Za-z]\d+[A-Za-z]?|(?i:no|nomor|nmr|blok|blk|rt|rw|gg|gang|kav|"
                            r"kavling|lt|lantai|raya|dalam|timur|barat|utara|selatan|ujung|indah|asri|permai)\.?|[A-Za-z]\.?|/)$")
RE_BLOK = re.compile(r"\b(?:blok|blk|rt|rw|kav)\.?\s*[A-Za-z]?\d{1,4}[A-Za-z]?\b(?:\s*/\s*\d{1,3})?", re.I)
RE_PLAT = re.compile(r"\b([A-Z]{1,2})(\s?)(\d{1,4})(\s?)([A-Z]{1,3})\b")
# v1.0.7: plat nomor = kode wilayah Indonesia + 1-4 angka + 1-3 huruf, dengan spasi KONSISTEN ("B 1234 XYZ" atau "B1234XYZ").
# Kode model produk ("A7 III", "R6 II", "S23 FE": huruf menempel angka, seri berspasi) dan kode ringkas pendek ("A7S") bukan plat.
KODE_WILAYAH = set("""A B D E F G H K L M N P R S T W Z AA AB AD AE AG BA BB BD BE BG BH BK BL BM BN BP DA DB DC DD DE DG DH DK DL DM DN DP
DR DS DT DW EA EB ED KB KH KT KU PA PB PG PT""".split())


def _plat(m):
    wil, s1, angka, s2, seri = m.groups()
    if wil not in KODE_WILAYAH or s1 != s2 or (not s1 and len(angka) < 3):
        return m.group(0)
    if re.search(r"(?i)\b(?:tipe|type|seri|series|model|versi|varian)\s*$", m.string[:m.start()]):
        return m.group(0)
    return "[plat]"
RE_AN = re.compile(r"((?i:\b(?:a\.\s?n\.?|a/n|an\.|atas\s+nama)))\s+((?:\[nama\]|[A-Za-z][A-Za-z']*)(?:\s+(?:\[nama\]|[A-Za-z][A-Za-z']*)){0,4})")
RE_SAYA = re.compile(r"\b((?i:nama\s+(?:saya|sy|aku)|namaku))\s+([A-Za-z][A-Za-z']{1,})(?:\s+([A-Z][A-Za-z']{2,}))?"
                     r"|\b((?i:saya|aku|sy))\s+([A-Z][a-z']{2,})(?:\s+([A-Z][a-z']{2,}))?")
RE_SAPAAN_NAMA = re.compile(r"\b(" + SAPAAN + r")\.?\s+(?:(" + GELAR + r")\s+)?([A-Z][A-Za-z']{2,})(?:\s+([A-Z][A-Za-z']{2,}))?")
# v1.0.5: kata umum sehari-hari yang sering muncul sesudah sapaan ("gpp kak maklum", "iya mas siap") - BUKAN nama
STOPWORD_SAPAAN = set("""maklum siap oke okay okey sip siip gpp gapapa gakpapa ngapapa santai aman sehat semangat amin aamiin iya iyaa yaa
betul benar bener setuju ditunggu tunggu dulu lho loh sekalian lancar beres kelar noted baik baiklah punten nuhun suwun nuwun matur tq ty
makasi makasii mksh mks trimakasih trims hehe wkwk haha hihi btw sama kembali selalu terus banget sekali dong nih tuh lah kah pun doang
aja saja semua semuanya semoga cepat sukses berkah barokah mantul mantap sabar ramah juga kok sih deh nya kan ok pagi siang sore malam
selamat permisi maaf mohon tolong salam met happy good nice thanks thank sorry please yes nope bisa boleh udah sudah belum blm udh sdh
ready kirim kirimin order pesan cek mampir datang balik lagi kapan dimana mana gimana berapa apa bantu lanjut gas proses dicek""".split())
# v1.0.7: kata sifat untuk orang/pelayanan sesudah sapaan ("Mas telaten", "kak sigap", "bu cekatan") BUKAN nama. Kata sifat yang juga
# lazim sebagai nama (Bagus, Indah, Ayu, Setia, Tulus, Budi, Jaya, Mulia, Wangi, Suci) sengaja TIDAK dimasukkan.
SIFAT_ORANG = set("""telaten sigap cekatan gesit tangkas tanggap sopan santun jujur amanah teliti rajin tekun ulet gercep helpful informatif
komunikatif responsif solutif profesional kompeten terampil handal andal jago cakap baik hebat keren top joss asik asyik seru humble
perhatian detail rapi tegas lembut halus ramah sabar cepat fast friendly kooperatif telitian sabaran""".split())
STOPWORD_SAPAAN |= SIFAT_ORANG


def _kata_umum_sapaan(k):
    k = (k or "").lower()
    if k in STOPWORD_SAPAAN or re.sub(r"(.)\1+", r"\1", k) in STOPWORD_SAPAAN:
        return True
    # v1.0.6 bentuk kata kerja dari imbuhan, bukan daftar tertutup: "lanjutkan", "kirimkan", "teruskan" (akhiran -kan),
    # "dibantu", "diproses", "ditunggu" (awalan + kata dasar yang dikenal). Akhiran -in/-lah TIDAK dipakai (nama: Paimin, Abdullah).
    if len(k) >= 6 and k.endswith("kan"):
        return True
    if len(k) >= 6 and k.endswith("nya"):   # v1.0.8 "kak kuenya", "kak rotinya" = benda, bukan nama
        return True
    kamus = STOPWORD_SAPAAN | AKSI | set(POS) | set(NEG)   # kata dasar >= 4 huruf: "dimas" (mas), "dinda" (nda) tetap nama
    for awal in ("di", "me", "ter", "ber"):
        if k.startswith(awal) and len(k) - len(awal) >= 4 and k[len(awal):] in kamus:
            return True
    return False


RE_SAPAAN_KECIL = re.compile(r"\b(" + SAPAAN + r")\s+([a-z]{3,12})(?=\s*(?:[,.!?)~]|$))")
BUKAN_NAMA = {"Admin", "Seller", "Toko", "Min", "Kasir", "Owner", "Saya", "Aku", "Tolong", "Mau", "Ini", "Itu", "Yang", "Kok", "Bisa",
              "Boleh", "Apakah", "Minta", "Terima", "Terimakasih", "Makasih", "Halo", "Hai", "Selamat", "Maaf", "Pesanan", "Order",
              "Barang", "Paket", "Dapur", "Warung", "Kedai", "Bakery", "Katering", "Kurir", "Driver", "Sudah", "Belum", "Untuk", "Dari",
              "Pesan", "Kirim", "Nanti", "Besok", "Sama", "Juga", "Tapi", "Dan", "Atau", "Kalau", "Kapan", "Gimana", "Bagaimana", "Apa",
              "Sangat", "Suka", "Senang", "Puas", "Kecewa", "Beli", "Pakai", "Harus", "Sedang", "Lagi", "Baru", "Masih", "Tidak", "Ga",
              "Gak", "Enggak", "Nggak", "Punya", "Pernah", "Selalu", "Langganan", "Pelanggan", "Customer", "Cs", "Mohon", "Silakan"}
# v1.0.5: penanda media WhatsApp Android/iOS, bahasa Indonesia & Inggris ("image omitted", "<Media tidak disertakan>", "stiker dihilangkan")
RE_PENGIRIM_MEDIA = re.compile(
    r"<media[^>]*>|<attached[^>]*>|\(file attached\)|(?:[^\s<>]+\s+•\s+(?:\d+\s+\w+\s+)?)?(?:document|dokumen)\s+omitted|"
    r"\b(?:image|video|audio|sticker|gif|contact\s+card|photo|voice\s+message)\s+omitted\b|"
    r"\b(?:gambar|foto|video|stiker|audio|dokumen|gif|kartu\s+kontak|pesan\s+suara)\s+(?:tidak\s+disertakan|dihilangkan|dihapus)\b", re.I)
# v1.0.12 teks sistem WA hanya dibuang bila SELURUH isi pesan adalah teks sistem (dicocokkan dengan fullmatch). Sebelumnya dicari di tengah pesan,
# sehingga pesan pelanggan yang diikuti baris "Pesan ini dihapus" ikut terbuang seluruhnya.
_SISTEM_HAPUS = r"(?:pesan ini dihapus|pesan dihapus|you deleted this message|this message was deleted)(?:\s+oleh\s+\S+(?:\s+\S+){0,2})?"
_SISTEM_ENKRIPSI = (r"(?:pesan dan panggilan|pesan yang dikirim ke chat ini|messages and calls|messages to this chat)\b.*"
                    r"(?:end-to-end|terenkripsi|enkripsi|encrypt).*")
_SISTEM_GRUP = (r"(?:\S+\s+){0,6}(?:bergabung menggunakan tautan|telah ditambahkan|meninggalkan grup|mengubah (?:ikon|subjek|deskripsi))"
                r"(?:\s+\S+){0,8}")
RE_SISTEM_TEKS = re.compile(r"[\W_]*(?:" + _SISTEM_HAPUS + r"|" + _SISTEM_ENKRIPSI + r"|" + _SISTEM_GRUP + r"|null)[\W_]*", re.I)


def _bukan_nama(kata):
    return (kata is None or kata in BUKAN_NAMA or kata.lower() in KATA_UMUM or kata.lower() in POS or kata.lower() in NEG
            or kata.lower() in SLANG)


def token_nama(nama_pengirim):
    """Token nama dari nama pengirim WA: tanpa sapaan/gelar ('Kak Yanti' -> 'Yanti'), tanpa angka/kata umum."""
    hasil = set()
    sap = {s.lower() for s in SAPAAN_KATA} | {"rt", "rw", "h", "dr", "drg", "ir", "ust", "ustadz", "ustadzah"}
    for n in nama_pengirim:
        n = (n or "").strip()
        if not n:
            continue
        hasil.add(n)
        kata = [k for k in re.findall(r"[A-Za-z']+", n) if len(k) >= 3 and k.lower() not in sap and not _bukan_nama(k.capitalize())]
        hasil.update(kata)
    return hasil


def _samarkan_an(m):
    """Kata sesudah 'a.n.' / 'atas nama' = nama. Kata pertama selalu; berikutnya bila berhuruf besar/[nama] atau bukan kata umum."""
    kata = m.group(2).split()
    maks = 4 if kata[0].lower() in {s.lower() for s in SAPAAN_KATA} else 3
    dipakai = 1
    for k in kata[1:maks]:
        nama_besar = k[:1].isupper() and k not in BUKAN_NAMA and k.lower() not in KATA_UMUM
        nama_kecil = k[:1].islower() and not _bukan_nama(k) and k not in VOCAB and len(k) >= 3
        if k == "[nama]" or nama_besar or nama_kecil:
            dipakai += 1
        else:
            break
    sisa = " ".join(kata[dipakai:])
    return re.sub(r"\s+", " ", m.group(1)) + " [nama]" + ((" " + sisa) if sisa else "")


def _umum(k):
    k = k.lower().strip(".")
    return (k in KATA_UMUM or k in POS or k in NEG or k in AKSI or k in NEGATOR or k in SLANG or k in STOPWORD_SAPAAN
            or re.sub(r"(nya|lah)$", "", k) in KATA_UMUM | set(SLANG))


def _samarkan_alamat(t, awal):
    """Ganti '<kata kunci alamat> <nama jalan> [No 5] [RT 04] ...' dengan [alamat]; berhenti pada kata biasa/tanda baca."""
    hasil, pos = [], 0
    for m in awal.finditer(t):
        if m.start() < pos:
            continue
        sisa = t[m.end():]
        kata = re.match(r"[^\s,;!?()\[\]]+(?:\s+[^\s,;!?()\[\]]+){0,7}", sisa)
        if not kata:
            continue
        token = kata.group(0).split()
        pakai, kecil = 0, 0
        singkatan = {"no", "gg", "blk", "kav", "lt", "rt", "rw", "jl", "jln", "komp"}
        for n, k in enumerate(token):
            if n and token[n - 1].endswith(".") and token[n - 1][:-1].lower() not in singkatan and len(token[n - 1]) > 2:
                break   # titik akhir kalimat: kata sesudahnya bukan alamat
            if n == 0:
                if k[:1].islower() and _umum(k):
                    break
                pakai = 1
                continue
            if k[:1].islower() and not re.match(r"\d", k) and not RE_KATA_ALAMAT.match(k):
                if _umum(k) or kecil >= 2 or len(k) < 3:
                    break
                kecil += 1
            elif not RE_KATA_ALAMAT.match(k):
                break
            elif k[:1].isupper() and any(re.match(r"\d", x) for x in token[:n]) and _umum(k):
                break   # "Jl. Melati No 5 Kurirnya telat": sesudah nomor, kata umum berhuruf besar bukan alamat
            pakai = n + 1
        if not pakai:
            continue
        panjang = len(" ".join(token[:pakai]))
        akhir = m.end() + sisa.index(token[0]) + panjang
        ujung = token[pakai - 1]
        if ujung.endswith(".") and ujung[:-1].lower() not in singkatan and len(ujung) > 2:
            akhir -= 1   # titik akhir kalimat tidak ikut disamarkan
        hasil.append(t[pos:m.start()] + "[alamat]")
        pos = akhir
    return "".join(hasil) + t[pos:]


def samarkan(teks, nama_pengirim=()):
    t = teks
    for n in sorted(token_nama(nama_pengirim) if nama_pengirim else (), key=len, reverse=True):
        if len(n) >= 3:
            t = re.sub(r"(?<!\w)" + re.escape(n) + r"(?!\w)", "[nama]", t, flags=re.I)
    t = RE_URL.sub("[tautan]", t)
    t = RE_EMAIL.sub("[email]", t)
    t = RE_HP.sub("[hp]", t)
    t = RE_TELP.sub("[telepon]", t)
    t = RE_USER.sub("[akun]", t)
    t = RE_NOPESAN.sub("[nomor]", t)
    t = RE_KODE.sub("[nomor]", t)
    t = _samarkan_alamat(t, RE_ALAMAT)
    t = _samarkan_alamat(t, RE_ALAMAT2)
    t = RE_BLOK.sub("[alamat]", t)
    t = RE_PLAT.sub(_plat, t)
    t = RE_AN.sub(_samarkan_an, t)

    def _saya(m):
        if m.group(1):  # "nama saya X" -> selalu disamarkan
            return m.group(1) + " [nama]" + ((" " + m.group(3)) if m.group(3) and _bukan_nama(m.group(3)) else "")
        if _bukan_nama(m.group(5)):
            return m.group(0)
        return m.group(4) + " [nama]" + ((" " + m.group(6)) if m.group(6) and _bukan_nama(m.group(6)) else "")
    t = RE_SAYA.sub(_saya, t)

    def _sapaan(m):
        if m.group(3) in BUKAN_NAMA or (m.group(2) is None and (_bukan_nama(m.group(3)) or _kata_umum_sapaan(m.group(3)))):
            return m.group(0)
        ekor = (" " + m.group(4)) if m.group(4) and _bukan_nama(m.group(4)) else ""
        return m.group(1) + (" " + m.group(2) if m.group(2) else "") + " [nama]" + ekor
    t = RE_SAPAAN_NAMA.sub(_sapaan, t)
    t = RE_SAPAAN_KECIL.sub(lambda m: m.group(0) if _bukan_nama(m.group(2)) or m.group(2) in VOCAB or _kata_umum_sapaan(m.group(2))
                            else m.group(1) + " [nama]", t)
    return re.sub(r"\s+", " ", t).strip()


# ------------------------------------------------------------------ tanggal
BULAN = {"jan": 1, "januari": 1, "feb": 2, "februari": 2, "mar": 3, "maret": 3, "apr": 4, "april": 4, "mei": 5, "may": 5,
         "jun": 6, "juni": 6, "jul": 7, "juli": 7, "agu": 8, "agt": 8, "agustus": 8, "aug": 8, "sep": 9, "sept": 9, "september": 9,
         "okt": 10, "oktober": 10, "oct": 10, "nov": 11, "november": 11, "des": 12, "desember": 12, "dec": 12}


def bulan_dari(s, urutan="hb"):
    """Kembalikan 'YYYY-MM' dari string tanggal (dd/mm/yyyy, yyyy-mm-dd, '12 Sep 2026'), atau None.
    urutan 'hb' = hari/bulan (Indonesia, bawaan); 'bh' = bulan/hari (format AS, mis. Google Form 8/15/2026)."""
    if not s:
        return None
    s = str(s).strip()
    m = re.match(r"(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
    else:
        m = re.match(r"(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})", s)
        if m:
            mo, y = int(m.group(1) if urutan == "bh" else m.group(2)), int(m.group(3))
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


RE_TGL_ANGKA = re.compile(r"^\s*(\d{1,2})[/.\-](\d{1,2})[/.\-](\d{2,4})(.*)$")
RE_AMPM = re.compile(r"\b[AP]\.?M\b", re.I)


def deteksi_urutan(daftar, paksa=None):
    """Tentukan urutan tanggal angka ('hb' hari/bulan atau 'bh' bulan/hari) dari SEMUA tanggal satu kolom/berkas.
    Kembalikan (urutan, daftar peringatan). Tanggal ambigu (semua bagian <= 12) ditandai; tanggal tak terbaca dihitung."""
    hb = bh = ambigu = ampm = tak = 0
    for v in daftar:
        v = (v or "").strip()
        if not v:
            continue
        m = RE_TGL_ANGKA.match(v)
        if not m:
            if bulan_dari(v) is None:
                tak += 1
            continue
        a, b = int(m.group(1)), int(m.group(2))
        if a > 12 and b > 12:
            tak += 1
        elif a > 12:
            hb += 1
        elif b > 12:
            bh += 1
        else:
            ambigu += 1
            if RE_AMPM.search(m.group(4)):
                ampm += 1
    pr = []
    if paksa:
        urutan = paksa
    elif hb and bh:
        urutan = "hb" if hb >= bh else "bh"
        pr.append("tanggal bercampur dua urutan (%d hari/bulan, %d bulan/hari) - dibaca %s; sebagian bulan bisa salah. Samakan format tanggal "
                  "di berkas, atau pakai --urutan-tanggal." % (hb, bh, "hari/bulan" if urutan == "hb" else "bulan/hari"))
    elif bh:
        urutan = "bh"
        pr.append("tanggal terbaca berformat bulan/hari (AS, mis. 8/15/2026) - bulan dihitung dengan urutan itu.")
    elif hb:
        urutan = "hb"
    elif ambigu and ampm >= 0.5 * ambigu:
        urutan = "bh"
        pr.append("%d tanggal ambigu (semua bagian <= 12) berpenanda AM/PM, khas format AS - dibaca bulan/hari. Periksa; bila salah pakai "
                  "--urutan-tanggal hari-bulan." % ambigu)
    else:
        urutan = "hb"
        if ambigu:
            pr.append("%d tanggal ambigu (mis. 03/04/2026 bisa 3 April atau 4 Maret) - dibaca hari/bulan (format Indonesia). Bila berkas dari "
                      "Google Form/Excel berformat AS, ulangi dengan --urutan-tanggal bulan-hari." % ambigu)
    if tak:
        pr.append("%d tanggal tidak terbaca (format tak dikenali) - masukan itu masuk 'tanpa tanggal', tren bulanan tidak lengkap." % tak)
    return urutan, pr


# ------------------------------------------------------------------ pembacaan berkas
def dekode(mentah, nama="berkas"):
    """Bytes -> (teks, catatan). Mengenali BOM UTF-8/UTF-16, UTF-16 tanpa BOM, UTF-8 campur Windows-1252."""
    catatan = []
    if mentah.startswith(b"\xef\xbb\xbf"):
        return mentah[3:].decode("utf-8", errors="replace"), catatan
    if mentah.startswith(b"\xff\xfe") or mentah.startswith(b"\xfe\xff"):
        catatan.append("encoding UTF-16 (BOM) dikenali")
        return mentah.decode("utf-16", errors="replace"), catatan
    sampel = mentah[:4000]
    if sampel.count(b"\x00") > len(sampel) * 0.25:
        genap, ganjil = sampel[0::2].count(0), sampel[1::2].count(0)
        if ganjil > 3 * max(genap, 1):
            catatan.append("encoding UTF-16 tanpa BOM dikenali")
            return mentah.decode("utf-16-le", errors="replace"), catatan
        if genap > 3 * max(ganjil, 1):
            catatan.append("encoding UTF-16 tanpa BOM dikenali")
            return mentah.decode("utf-16-be", errors="replace"), catatan
    if b"\x00" in sampel:
        raise Gagal("%s tampak berkas biner (bukan teks/CSV). Ekspor ulang sebagai .txt atau .csv (UTF-8)." % nama)
    try:
        teks = mentah.decode("utf-8")
    except UnicodeDecodeError:
        baris, cadangan = [], 0
        for b in mentah.split(b"\n"):
            try:
                baris.append(b.decode("utf-8"))
            except UnicodeDecodeError:
                cadangan += 1
                baris.append(b.decode("cp1252", errors="replace"))
        teks = "\n".join(baris)
        catatan.append("%d baris bukan UTF-8, dibaca sebagai Windows-1252" % cadangan)
    kendali = sum(1 for c in teks if (ord(c) < 32 and c not in "\t\r\n") or 0x7f <= ord(c) <= 0x9f or c == "\ufffd")
    if teks and kendali > max(3, len(teks) * 0.02):
        raise Gagal("%s tampak berkas biner/rusak (banyak karakter aneh). Ekspor ulang sebagai .txt atau .csv (UTF-8)." % nama)
    return teks, catatan


def baca_mentah(path):
    if path == "-":
        return sys.stdin.read(), []
    try:
        with open(path, "rb") as f:
            mentah = f.read()
    except FileNotFoundError:
        raise Gagal("berkas tidak ditemukan: %s. Periksa nama/lokasi berkas (huruf besar-kecil & ekstensi)." % path)
    except IsADirectoryError:
        raise Gagal("%s adalah folder, bukan berkas. Sebutkan nama berkasnya." % path)
    except OSError as e:
        raise Gagal("berkas %s tidak bisa dibuka (%s)." % (path, e.strerror or e))
    return dekode(mentah, os.path.basename(path))


RE_WA1 = re.compile(r"^\u200e?\[?(\d{1,2}[/.]\d{1,2}[/.]\d{2,4}),?\s+\d{1,2}[.:]\d{2}(?:[.:]\d{2})?(?:\s?[APap][Mm])?\]?\s+-?\s*(.*)$")


RE_WA_JAM = re.compile(r"^\[?\d{1,2}[/.]\d{1,2}[/.]\d{2,4},?\s+(\d{1,2})[.:](\d{2})(?:[.:]\d{2})?(?:\s?([APap])\.?[Mm])?")


def _jam_wa(baris):
    """Menit sejak tengah malam dari baris ekspor WA, atau None."""
    m = RE_WA_JAM.match(baris)
    if not m:
        return None
    j, mn = int(m.group(1)), int(m.group(2))
    if m.group(3):
        j = j % 12 + (12 if m.group(3).lower() == "p" else 0)
    return j * 60 + mn if j < 24 and mn < 60 else None


def _tanggal_wa(tgl, urutan="hb"):
    m = re.match(r"(\d{1,2})[/.](\d{1,2})[/.](\d{2,4})", tgl or "")
    if not m:
        return None
    a, b, y = int(m.group(1)), int(m.group(2)), int(m.group(3))
    y += 2000 if y < 100 else 0
    h, bl = (b, a) if urutan == "bh" else (a, b)
    try:
        return datetime.date(y, bl, h)
    except ValueError:
        return None


def baca_wa(teks, staf=None, tanpa_sapaan=False):
    """Kembalikan (daftar [(tanggal, pengirim, isi, menit_hari)], Counter pengirim)."""
    pesan = []
    akhir = None   # indeks pesan bertanggal terakhir: baris lanjutan tanpa tanggal ikut ke sana
    for baris in teks.splitlines():
        baris = baris.replace("\u200e", "").replace("\u202f", " ").replace("\xa0", " ")
        m = RE_WA1.match(baris)
        if m:
            sisa = m.group(2)
            jam = _jam_wa(baris)
            if ": " in sisa:
                pengirim, isi = sisa.split(": ", 1)
                pesan.append([m.group(1), pengirim.strip(), isi, jam])
            else:
                pesan.append([m.group(1), None, sisa, jam])  # pesan sistem
            akhir = len(pesan) - 1
        elif akhir is not None and baris.strip():
            if RE_SISTEM_TEKS.fullmatch(baris.strip()):
                # v1.0.12 baris tanpa tanggal yang seluruhnya teks sistem ("Pesan ini dihapus") = baris sistem tersendiri (dibuang),
                # BUKAN lanjutan pesan sebelumnya; pesan pelanggan di atasnya tetap utuh.
                pesan.append([pesan[akhir][0], None, baris.strip(), pesan[akhir][3]])
            else:
                pesan[akhir][2] += " " + baris.strip()
    hitung = Counter(p[1] for p in pesan if p[1])
    return pesan, hitung


def kenali_nilai(teks):
    """'5 | enak' / '★★ dingin' / '2/5 - x' / '8/10 - x' -> (nilai, skala, isi)."""
    m = re.match(r"^\s*(?:nilai\s*)?(10|\d)\s*/\s*10\s*[|:\-–]?\s*(.+)$", teks, re.I | re.S)
    if m:
        return int(m.group(1)), 10, m.group(2).strip()
    m = re.match(r"^\s*(?:bintang\s*)?([1-5])\s*(?:/\s*5)?\s*[|:\-–]\s*(.+)$", teks, re.I | re.S)
    if m:
        return int(m.group(1)), 5, m.group(2).strip()
    m = re.match(r"^\s*([★⭐]{1,5})\s*(.+)$", teks, re.S)
    if m:
        return len(re.findall("[★⭐]", m.group(1))), 5, m.group(2).strip()
    return None, None, teks.strip()


def baca_teks_bebas(teks):
    ada_nilai = any(kenali_nilai(b)[0] is not None for b in teks.splitlines() if b.strip())
    if re.search(r"\n\s*\n", teks.strip()) and not ada_nilai:
        blok = [re.sub(r"\s+", " ", b).strip() for b in re.split(r"\n\s*\n", teks)]
    else:
        blok = [b.strip() for b in teks.splitlines()]
    hasil = []
    for b in blok:
        if b:
            nilai, skala, isi = kenali_nilai(b)
            hasil.append({"tgl": None, "nilai": nilai, "skala": skala, "isi": isi, "identitas": None})
    return hasil


# ---- CSV: pengenalan kolom
def _tok(h):
    return re.findall(r"[a-z0-9]+", (h or "").lower())


KATA_TEKS = {"ulasan", "review", "reviews", "komentar", "comment", "comments", "masukan", "feedback", "saran", "kritik", "catatan", "text",
             "teks", "isi", "pesan", "message", "keluhan", "komplain", "testimoni", "testimonial", "pendapat", "tanggapan", "opini", "kesan",
             "content", "konten", "body", "jawaban", "answer", "note", "notes", "remarks"}
KATA_PENGHALANG = {"no", "nomor", "id", "kode", "order", "pesanan", "invoice", "resi", "sku", "tanggal", "tgl", "date", "waktu", "time",
                   "jam", "created", "timestamp", "dibuat", "rating", "bintang", "star", "stars", "skor", "score", "nilai", "jumlah", "qty",
                   "harga", "price", "total", "foto", "gambar", "image", "images", "video", "link", "url", "media", "like", "likes", "suka"}
KATA_BALASAN = {"balasan", "reply", "replies", "response"}
KATA_PENJUAL = {"penjual", "seller", "toko", "admin", "shop", "merchant", "owner", "store", "kami"}
KOLOM_NAMA = {"nama", "name", "username", "user", "pembeli", "buyer", "email", "telepon", "telp", "phone", "hp", "wa", "whatsapp",
              "alamat", "address", "akun", "account", "pelanggan", "customer", "reviewer", "penulis", "author", "pengirim"}
KATA_KATEGORI = {"kota", "domisili", "usia", "umur", "gender", "kelamin", "pekerjaan", "profesi", "cabang", "outlet", "produk", "variasi",
                 "varian", "kategori", "status", "jenis", "provinsi", "kecamatan", "kabupaten", "product", "variant", "sku", "kanal",
                 "channel", "platform", "sumber", "source"}
KATA_TANYA = {"apa", "bagaimana", "gimana", "kenapa", "mengapa", "menurut", "saran", "harapan", "usulan", "ingin", "mau", "perlu",
              "tambah", "ditambah", "diperbaiki", "perbaiki", "kurang", "kritik", "masukan"}
KATA_PERAN_SARAN = {"ditambah", "tambah", "ditambahkan", "ingin", "harapan", "usul", "usulan", "request", "permintaan", "keinginan",
                    "diinginkan", "inginkan", "dijual", "tersedia", "wishlist"}
KATA_PERAN_KELUHAN = {"perbaiki", "diperbaiki", "kurang", "keluhan", "kritik", "masalah", "kendala", "komplain"}
KOLOM_NILAI = {"bintang", "rating", "star", "stars", "skor", "score", "nilai", "nps", "rate", "penilaian"}
# judul survei yang lazim tanpa kata "nilai/skor" ("Seberapa besar kemungkinan Anda merekomendasikan ...?"); dipakai hanya bila ISINYA angka
KOLOM_NILAI_SAMAR = {"merekomendasikan", "rekomendasi", "rekomendasikan", "recommend", "kemungkinan", "likelihood", "kepuasan", "puas",
                     "satisfaction", "satisfied", "kepuasannya"}
KOLOM_TANGGAL = {"tanggal", "tgl", "date", "waktu", "time", "created", "dibuat", "timestamp", "cap"}
KOLOM_KANAL = {"kanal", "channel", "platform", "sumber", "source"}
KOSONG = {"", "-", "--", "—", ".", "..", "n/a", "na", "none", "null", "x", "tidak ada", "ga ada", "gak ada", "nggak ada", "belum ada",
          "tidak", "no", "nope", "nothing", "kosong"}
RE_BUKAN_TEKS = re.compile(r"[\d\s./:,\-+()#]+|(?=[A-Za-z0-9\-/]*\d)[A-Za-z0-9\-/]{5,}|\d{1,2}\s+[A-Za-z]{3,9}\.?\s+\d{2,4}(?:\s+[\d:.]+)?")


def _persen_bukan_teks(nilai):
    if not nilai:
        return 0.0
    return sum(1 for v in nilai if RE_BUKAN_TEKS.fullmatch(v.strip()) or bulan_dari(v) and len(v) <= 25) / len(nilai)


def _cocok_paksa(header, paksa, jenis):
    if not paksa:
        return None
    minta = [p.strip() for p in paksa.split(",") if p.strip()]
    hasil, hilang = [], []
    for p in minta:
        cocok = [h for h in header if h.strip().lower() == p.lower()]
        (hasil if cocok else hilang).extend(cocok or [p])
    if hilang:
        raise Gagal("kolom %s \"%s\" tidak ada. Kolom yang ada: %s." % (jenis, "\", \"".join(hilang), ", ".join('"%s"' % h for h in header)))
    return hasil


def pilih_kolom(header, jenis, paksa=None):
    """Kolom bintang/nilai, tanggal, atau kanal (berdasarkan judul kolom). Kolom teks: pilih_kolom_teks."""
    p = _cocok_paksa(header, paksa, jenis)
    if p is not None:
        return p
    kamus = {"bintang": KOLOM_NILAI | KOLOM_NILAI_SAMAR, "tanggal": KOLOM_TANGGAL, "kanal": KOLOM_KANAL}[jenis]
    hasil = []
    for h in header:
        tk = set(_tok(h))
        if tk & kamus and not (jenis != "tanggal" and tk & KOLOM_NAMA):
            if jenis == "tanggal" and tk & {"lahir"}:
                continue
            hasil.append(h)
    if jenis == "tanggal":  # utamakan kolom yang judulnya tepat "tanggal"/"waktu ulasan" dsb.
        hasil.sort(key=lambda h: (0 if set(_tok(h)) & {"tanggal", "tgl", "date", "timestamp"} else 1))
    return hasil


def pilih_kolom_teks(header, baris, paksa=None, kecuali=()):
    """Kembalikan (daftar (kolom, peran), peringatan). peran: 'ulasan' atau 'saran' (kolom pertanyaan permintaan)."""
    peringatan = []

    def nilai_kolom(h):
        return [(b.get(h) or "").strip() for b in baris if (b.get(h) or "").strip()]

    def peran(h):
        tk = set(_tok(h))
        return "saran" if tk & KATA_PERAN_SARAN and not tk & KATA_PERAN_KELUHAN else "ulasan"

    p = _cocok_paksa(header, paksa, "teks")
    if p is not None:
        for h in p:
            pb = _persen_bukan_teks(nilai_kolom(h))
            if pb > 0.5:
                peringatan.append("kolom teks \"%s\" berisi %.0f%% tanggal/angka/kode - apakah kolomnya benar?" % (h, pb * 100))
        return [(h, peran(h)) for h in p], peringatan
    hasil = []
    for h in header:
        if h in kecuali:
            continue
        tk = set(_tok(h))
        if not tk & KATA_TEKS:
            continue
        if tk & KATA_BALASAN or (tk & {"tanggapan", "respon", "respons"} and tk & KATA_PENJUAL):
            continue  # balasan penjual, bukan suara pelanggan
        if tk & KATA_PENGHALANG and not tk & {"isi"}:
            continue  # "Waktu Ulasan", "Foto Ulasan", "No. Pesanan"
        if _persen_bukan_teks(nilai_kolom(h)) > 0.5:
            peringatan.append("kolom \"%s\" dilewati: isinya mayoritas tanggal/angka/kode" % h)
            continue
        hasil.append((h, peran(h)))
    if hasil:
        return hasil, peringatan
    # survei dengan judul kolom bebas ("Apa yang perlu kami perbaiki?")
    for h in header:
        if h in kecuali:
            continue
        tk = set(_tok(h))
        if tk & (KOLOM_NAMA | KATA_PENGHALANG | KATA_KATEGORI) and not h.strip().endswith("?"):
            continue
        if tk & KOLOM_NAMA and not tk & KATA_TANYA:
            continue
        nilai = [v for v in nilai_kolom(h) if v.lower() not in KOSONG]
        if not nilai or _persen_bukan_teks(nilai) > 0.5:
            continue
        if sum(1 for v in nilai if re.search(r"[A-Za-z]{2,}", v)) < 0.5 * len(nilai):
            continue
        rata = sum(len(v) for v in nilai) / len(nilai)
        pertanyaan = h.strip().endswith("?") or bool(tk & KATA_TANYA)
        kategori = len(nilai) >= 6 and len({v.lower() for v in nilai}) <= 3
        if kategori or not (rata >= 8 or pertanyaan):
            continue
        hasil.append((h, peran(h)))
    return hasil, peringatan


def parse_nilai(v):
    """'4' / '4,5' / '4/5' / '8/10' / '★★★★' / '5 bintang' -> (angka, skala_petunjuk atau None)."""
    v = (v or "").strip()
    if not v:
        return None, None
    bintang = re.findall("[★⭐]", v)
    if bintang:
        return len(bintang), 5
    m = re.fullmatch(r"(\d{1,2}(?:[.,]\d+)?)\s*/\s*(5|10|100)", v)
    if m:
        return float(m.group(1).replace(",", ".")), int(m.group(2))
    m = re.fullmatch(r"(\d{1,3}(?:[.,]\d+)?)\s*(?:bintang|stars?|poin)?", v, re.I)
    if m:
        return float(m.group(1).replace(",", ".")), None
    return None, None


def tentukan_skala(judul, angka, paksa=None):
    """Kembalikan (skala 5 atau 10, peringatan atau None)."""
    if paksa:
        return int(paksa), None
    j = (judul or "").lower()
    if re.search(r"\b[01]\s*(?:-|–|s\.?/?d\.?|sampai|hingga|to)\s*10\b|/\s*10\b|\bnps\b|skala\s*10|rekomendasi|merekomendasikan|recommend", j):
        return 10, None
    if angka and (max(angka) > 5 or min(angka) == 0):
        if re.search(r"bintang|star|1\s*-\s*5|/\s*5\b", j):
            return 10, "kolom \"%s\" disebut bintang tetapi berisi nilai di atas 5/nol - dibaca sebagai skala 0-10; periksa." % judul
        return 10, None
    if re.search(r"bintang|star|rating|1\s*-\s*5|/\s*5\b", j):
        return 5, None
    return 5, ("skala kolom \"%s\" tidak pasti (semua nilai 1-5), dianggap bintang 1-5. Bila survei memakai 0-10, "
               "jalankan ulang dengan --skala 10." % judul) if angka else None


def nilai_ke_bintang(nilai, skala):
    """Setara bintang 1-5 untuk sentimen. Skala 0-10 mengikuti NPS: 9-10 promotor, 7-8 pasif, 0-6 detraktor."""
    if nilai is None:
        return None
    if skala == 10:
        n = round(nilai)
        return 1 if n <= 3 else 2 if n <= 6 else 3 if n <= 8 else 4 if n == 9 else 5
    return max(1, min(5, int(round(nilai))))


def _angka_kecil(baris, h):
    """Nilai kolom h yang bilangan bulat 0-10 (untuk mengenali kolom nilai dari isinya). Kembalikan (daftar angka, jumlah terisi)."""
    isi = [(b.get(h) or "").strip() for b in baris]
    isi = [v for v in isi if v]
    return [int(v) for v in isi if re.fullmatch(r"\d{1,2}", v) and int(v) <= 10], len(isi)


def baca_csv(teks, kolom_teks=None, kolom_bintang=None, kolom_tanggal=None, skala=None, nama="CSV", pemisah=None, urutan_tanggal=None):
    """Kembalikan (daftar item mentah, info kolom, peringatan)."""
    sampel = teks[:4096]
    if pemisah:
        dialek = csv.excel_tab if pemisah == "\t" else csv.excel
    else:
        try:
            dialek = csv.Sniffer().sniff(sampel, delimiters=",;\t")
        except csv.Error:
            dialek = csv.excel
    try:
        csv.field_size_limit(10 * 1024 * 1024)
        pembaca = csv.DictReader(io.StringIO(teks), dialect=dialek)
        header = [h for h in (pembaca.fieldnames or []) if h is not None]
        baris_semua = list(pembaca)
    except csv.Error as e:
        raise Gagal("%s tidak bisa dibaca sebagai CSV (%s). Buka di Excel/Google Sheets lalu simpan ulang sebagai CSV." % (nama, e))
    if not header:
        raise Gagal("%s kosong atau tanpa baris judul kolom." % nama)
    if teks.count('"') % 2 == 1 and any("\n" in (v or "") for b in baris_semua for v in b.values() if isinstance(v, str)):
        raise Gagal("%s: tanda kutip (\") tidak seimbang - beberapa baris tergabung jadi satu. Buka di Excel/Google Sheets lalu simpan "
                    "ulang sebagai CSV, atau hapus tanda kutip yang tidak berpasangan." % nama)
    kb = pilih_kolom(header, "bintang", kolom_bintang)
    if not kolom_bintang:  # judul samar ("...merekomendasikan...?", "Kepuasan") hanya dipakai bila isinya angka
        kb = [h for h in kb if set(_tok(h)) & KOLOM_NILAI or (lambda a: a[1] and len(a[0]) >= 0.6 * a[1])(_angka_kecil(baris_semua, h))]
    kd = pilih_kolom(header, "tanggal", kolom_tanggal)
    kk = pilih_kolom(header, "kanal")
    kt, peringatan = pilih_kolom_teks(header, baris_semua, kolom_teks, kecuali=set(kb[:1] + kd[:1] + kk[:1]))
    if not kt:
        raise Gagal("%s: kolom teks ulasan/komentar tidak ditemukan. Kolom yang ada: %s. Ulangi dengan --kolom-teks \"NAMA KOLOM\"."
                    % (nama, ", ".join('"%s"' % h for h in header)))
    kt_nama = [h for h, _ in kt]
    kb = [h for h in kb if h not in kt_nama]
    # kolom angka 0-10 yang judulnya tidak dikenali: pakai bila jelas skala 0-10 (ada 0 atau > 5), selain itu BERI PERINGATAN (jangan diam)
    dipakai_lain = set(kt_nama) | set(kb[:1]) | set(kd[:1]) | set(kk[:1])
    kandidat = []
    for h in header:
        tk = set(_tok(h))
        if h in dipakai_lain or tk & (KOLOM_NAMA | KATA_PENGHALANG | KATA_KATEGORI | KOLOM_TANGGAL | KOLOM_KANAL):
            continue
        a, n_isi = _angka_kecil(baris_semua, h)
        if n_isi >= 5 and len(a) >= 0.8 * n_isi and len(set(a)) >= 3:
            kandidat.append((h, a))
    if kandidat and not kb and not kolom_bintang and len(kandidat) == 1 and (min(kandidat[0][1]) == 0 or max(kandidat[0][1]) > 5):
        kb = [kandidat[0][0]]
        peringatan.append("kolom \"%s\" dikenali sebagai nilai 0-10 dari ISINYA (judulnya tidak menyebut nilai/skor). Bila bukan nilai "
                          "kepuasan/NPS, abaikan; bila salah kolom, pakai --kolom-bintang." % kb[0])
    else:
        for h, a in kandidat:
            peringatan.append("kolom \"%s\" berisi angka %d-%d tetapi TIDAK dipakai sebagai nilai/bintang. Bila itu nilai kepuasan/NPS, ulangi "
                              "dengan --kolom-bintang \"%s\" (dan --skala 10 bila 0-10)." % (h, min(a), max(a), h))
    # skala nilai
    sk, angka = None, []
    if kb:
        for b in baris_semua:
            a, petunjuk = parse_nilai(b.get(kb[0]))
            if a is not None:
                angka.append(a)
                if petunjuk:
                    sk = sk or petunjuk
        if sk == 100:
            sk = None
        if not angka:
            peringatan.append("kolom nilai \"%s\" tidak berisi angka - diabaikan" % kb[0])
            kb = []
        elif sk is None or skala:
            sk, pr = tentukan_skala(kb[0], angka, skala)
            if pr:
                peringatan.append(pr)
    kolom_identitas = [h for h in header if set(_tok(h)) & (KOLOM_NAMA | {"pesanan", "order", "invoice", "id"}) and h not in kt_nama]
    # v1.0.8 kolom balasan penjual (Shopee/Tokopedia/Google Maps): dipakai HANYA untuk menghitung ulasan yang belum dibalas
    k_balas = [h for h in header if h not in kt_nama and (set(_tok(h)) & KATA_BALASAN or
                                                          (set(_tok(h)) & {"tanggapan", "respon", "respons"} and set(_tok(h)) & KATA_PENJUAL))]
    urutan = "hb"
    if kd:
        urutan, pr_tgl = deteksi_urutan([b.get(kd[0]) for b in baris_semua], urutan_tanggal)
        peringatan += ["kolom tanggal \"%s\": %s" % (kd[0], x) for x in pr_tgl]
    hasil = []
    for baris in baris_semua:
        nilai = None
        if kb:
            nilai, _ = parse_nilai(baris.get(kb[0]))
        tgl = baris.get(kd[0]) if kd else None
        kanal = (baris.get(kk[0]) or "").strip() if kk else None
        if kolom_identitas:
            identitas = tuple((baris.get(h) or "").strip().lower() for h in kolom_identitas)
        else:
            identitas = tuple((baris.get(h) or "").strip() for h in header)  # tanpa kolom identitas: hanya baris identik
        for k, peran in kt:
            isi = (baris.get(k) or "").strip()
            if isi.lower() in KOSONG:
                if isi:
                    hasil.append({"kosong": True})
                continue
            dibalas = None
            if k_balas:
                dibalas = (baris.get(k_balas[0]) or "").strip().lower() not in KOSONG
            hasil.append({"tgl": tgl, "nilai": nilai, "skala": sk if nilai is not None else None, "isi": isi, "kanal": kanal or None,
                          "identitas": (k,) + identitas, "peran": peran, "kolom": k, "urutan": urutan, "dibalas": dibalas})
    nilai_baris = []
    if kb:
        for baris in baris_semua:
            a, _ = parse_nilai(baris.get(kb[0]))
            if a is not None:
                nilai_baris.append(a)
    responden = sum(1 for b in baris_semua if any((b.get(k) or "").strip().lower() not in KOSONG for k, _ in kt))
    info = {"kolom_teks": kt_nama, "kolom_nilai": kb[0] if kb else None, "nilai_baris": nilai_baris if sk == 10 else [],
            "responden": responden, "skala_nilai": ("0-10" if sk == 10 else "1-5") if kb else None,
            "kolom_tanggal": kd[0] if kd else None, "baris": len(baris_semua), "kolom_balasan": k_balas[0] if k_balas else None,
            "urutan_tanggal": ("bulan/hari" if urutan == "bh" else "hari/bulan") if kd else None}
    return hasil, info, peringatan


def baca_berkas(spesifikasi, opsi):
    """spesifikasi: 'berkas' atau 'berkas=Kanal'. Kembalikan (kanal, daftar item mentah, info, hitung_pengirim)."""
    path, _, kanal = spesifikasi.partition("=")
    if not os.path.exists(path) and "=" in path:
        path, _, kanal = spesifikasi.rpartition("=")
    teks, catatan = baca_mentah(path)
    nama = os.path.basename(path) if path != "-" else "stdin"
    kanal = kanal.strip() or re.sub(r"\.\w+$", "", path.replace("\\", "/").split("/")[-1]) or "kanal"
    ext = path.lower().rsplit(".", 1)[-1] if "." in path else ""
    info = {"berkas": nama, "kanal": kanal, "jenis": "teks", "peringatan": [], "catatan": catatan}
    if ext == "json":
        info["peringatan"].append("berkas .json dibaca sebagai teks tempelan (satu masukan per baris). Bila ini berkas tema, pakai --tema %s; "
                                  "bila data ulasan, ekspor sebagai CSV." % nama)
    baris1 = teks.lstrip("\ufeff").split("\n", 1)[0]
    # .txt berisi tabel bertab (ekspor Excel "Unicode Text"): baca sebagai tabel, bukan teks tempelan
    tab_tabel = False
    if ext == "txt":
        baris_isi = [b for b in teks.lstrip("\ufeff").splitlines() if b.strip()]
        jt = baris_isi[0].count("\t") if baris_isi else 0
        if jt >= 1 and len(baris_isi) >= 2 and not RE_WA1.match(baris_isi[0].strip("\ufeff")):
            cek = baris_isi[1:21]
            if sum(1 for b in cek if b.count("\t") == jt) >= 0.6 * len(cek):
                tab_tabel = True
                info["catatan"].append("berkas .txt bertab dibaca sebagai tabel (baris pertama = judul kolom)")
            else:
                info["peringatan"].append("berkas .txt punya karakter tab di baris pertama tetapi barisnya tidak seragam - dibaca sebagai teks "
                                          "biasa. Bila ini tabel Excel, simpan ulang sebagai CSV.")
    if tab_tabel or ext in ("csv", "tsv") or (ext not in ("txt",) and len(re.split(r"[,;\t]", baris1)) >= 2 and not RE_WA1.match(baris1)):
        info["jenis"] = "csv"
        mentah, kol, pr = baca_csv(teks, getattr(opsi, "kolom_teks", None), getattr(opsi, "kolom_bintang", None),
                                   getattr(opsi, "kolom_tanggal", None), getattr(opsi, "skala", None), nama,
                                   "\t" if tab_tabel else None, getattr(opsi, "urutan_tanggal", None))
        info.update(kol)
        info["peringatan"] += pr
        return kanal, mentah, info, None
    wa, hitung = baca_wa(teks, getattr(opsi, "staf_list", []))
    if len(wa) >= 3 and sum(1 for p in wa if p[1]) >= 3 and hitung:
        info["jenis"] = "whatsapp"
        urutan, pr = deteksi_urutan([p[0] for p in wa], getattr(opsi, "urutan_tanggal", None))
        info["urutan"] = urutan
        info["peringatan"] += ["tanggal chat: " + x for x in pr]
        return kanal, wa, info, hitung
    return kanal, baca_teks_bebas(teks), info, None


# ------------------------------------------------------------------ normalisasi & koreksi typo
# v1.0.7: kata sah (KBBI/umum) yang berjarak SATU huruf dari kata kamus - tidak pernah "dikoreksi" sebagai typo. Daftar ini hasil
# pemeriksaan menyeluruh semua bentuk hapus-1-huruf dari kamus (tests/uji_regresi_107.py memeriksa ulang setiap versi).
KATA_SAH = set("""krim kiri kenang kenangan mengenangkan korset menular menguar sasana susana dialas tracing pacing""".split())


def _kata_pola(pola):
    return set(re.findall(r"[a-z]{3,}", pola))


def _hapus1(w):
    return {w[:i] + w[i + 1:] for i in range(len(w))}


VOCAB = set(POS) | set(NEG) | AKSI | set(SLANG.values()) | NEGATOR | {"kurang"}
for _t in TEMA_BAWAAN:
    VOCAB |= _kata_pola(_t[3])
VOCAB = {v for v in VOCAB if " " not in v}
_HAPUS = {}


def _siapkan_typo(vocab):
    peta = defaultdict(set)
    for w in vocab:
        if len(w) >= 5 and w.isalpha():
            for d in _hapus1(w):
                peta[d].add(w)
    return peta


_HAPUS = _siapkan_typo(VOCAB)


def koreksi_typo(tok, vocab=None, peta=None):
    """Toleransi typo yang AMAN: huruf berulang ('lamaa', 'bgttt') dan SATU huruf hilang pada kata >= 6 huruf
    ('pengirimn', 'terlmbat'), hanya bila kandidatnya tunggal. Substitusi huruf sengaja tidak dikoreksi
    (terlalu sering salah: 'tanggal'->'tanggap', 'benar'->'besar')."""
    vocab = VOCAB if vocab is None else vocab
    peta = _HAPUS if peta is None else peta
    if tok in vocab or tok in KATA_UMUM or tok in KATA_SAH or len(tok) < 4 or not tok.isalpha():
        return tok
    tunggal = re.sub(r"(.)\1+", r"\1", tok)
    if tunggal in vocab:
        return tunggal
    # v1.0.7: akhiran klitik (-nya/-ku/-mu/-lah/-kah) tidak ikut dihitung panjang kata. Huruf hilang hanya dikoreksi bila KATA DASARNYA
    # >= 6 huruf dan bukan kata sah: 'krimnya' (krim) bukan 'kirimnya', 'kirinya' (kiri) bukan 'kirimnya'.
    dasar = tok
    for akhir in ("nya", "lah", "kah", "ku", "mu"):
        if tok.endswith(akhir) and len(tok) - len(akhir) >= 3:
            dasar = tok[:-len(akhir)]
            break
    if dasar != tok and (dasar in KATA_SAH or dasar in KATA_UMUM or dasar in vocab):
        return tok
    if len(dasar) >= 6:
        # huruf pertama sama; huruf terakhir yang hilang tidak dikoreksi ('berisi' bukan 'berisik')
        kand = {w for w in peta.get(tok, ()) if w[0] == tok[0] and w[:-1] != tok}
        if len(kand) == 1:
            return kand.pop()
        if dasar != tok:   # 'dikirmnya' -> 'dikirim' + 'nya'
            kand = {w for w in peta.get(dasar, ()) if w[0] == dasar[0] and w[:-1] != dasar}
            if len(kand) == 1:
                return kand.pop() + tok[len(dasar):]
    return tok


def _slang(k):
    """Cari slang juga dalam bentuk huruf-berulang ('gaaa', 'blmm') dan ber-akhiran -nya ('nyampenya', 'dapetnya')."""
    if k in SLANG:
        return SLANG[k]
    tunggal = re.sub(r"(.)\1+", r"\1", k)
    if tunggal != k and tunggal in SLANG and tunggal not in VOCAB:
        return SLANG[tunggal]
    for akhir in ("nya", "ny"):
        dasar = k[:-len(akhir)]
        if k.endswith(akhir) and len(dasar) >= 3 and dasar in SLANG and " " not in SLANG[dasar]:
            return SLANG[dasar] + "nya"
    return None


def normalkan(teks, vocab=None, peta=None):
    # v1.0.7: jenjang sekolah bukan slang ('SMP' bukan 'sampai', 'SMA' bukan 'sama'): huruf besar, atau sesudah kelas/anak/siswa
    t = re.sub(r"\b(?:SMA|SMP|SMK|MTs)\b", " sekolah ", teks)
    t = re.sub(r"(?i)\b(kelas|anak|siswa|murid|lulusan|jenjang|tingkat|les|bimbel)(\s+(?:\d+\s+)?)(?:sma|smp|smk|sd)\b", r"\1\2sekolah", t)
    t = t.lower()
    t = re.sub(r"\[(nama|hp|telepon|email|tautan|akun|nomor|alamat|plat)\]", r" \1x ", t)
    t = re.sub(r"(.)\1{2,}", r"\1\1", t)                  # 'enaaak' -> 'enaak'
    t = re.sub(r"\b([a-z]{3,})2([a-z]{0,4})\b", r"\1\2", t)  # 'anak2' -> 'anak', v1.0.6 'teman2nya' -> 'temannya', 'dimahal2in'
    t = re.sub(r"\b([a-z]{3,})-\1\b", r"\1", t)          # 'gerak-gerak'
    t = re.sub(r"\b(di|ke|ter|ber)-(?=[a-z]{3,})", r"\1", t)  # 'di-read' -> 'diread', 'di-cancel'
    t = re.sub(r"\bdi\s+read\b", "diread", t)               # v1.0.4: 'di read' = 'diread'
    t = re.sub(r"\bj\s*&\s*t\b", "jnt", t)
    t = re.sub(r"\bg(?:a|ak|k)(?=(?:enak|sesuai|bisa|ada|jelas|dibalas|dibales|datang|dateng|nyampe|sampai|bagus|ramah|rapi|bersih|awet|"
               r"adem|nyaman|mau|respon|fresh|sopan|cocok)\b)", "tidak ", t)
    kata = re.findall(r"[a-z]+|\d+|[^\w\s]", t)
    keluar = []
    for k in kata:
        s = _slang(k) if k.isalpha() else None
        if s is not None:
            keluar.append(s)
        elif k.isalpha():
            keluar.append(koreksi_typo(k, vocab, peta))
        else:
            keluar.append(k)
    t = " ".join(keluar)
    for pola, ganti in FRASA:
        t = re.sub(pola, ganti, t)
    return t


def pecah_klausa(t):
    """Kembalikan daftar (klausa, tanya) - tanya=True bila kalimatnya diakhiri '?'."""
    hasil = []
    for kal, tanda in re.findall(r"([^.!?;\n]+)([.!?;\n]*)", t):
        tanya = "?" in tanda
        for b in re.split(r"\s+(?:tapi|namun|cuma|hanya saja|sayang(?:nya)?|sedangkan|padahal|cuman|tetapi)\s+|\s,\s|,|\s+-\s+", " " + kal + " "):
            b = b.strip()
            if b and re.search(r"\w", b):
                hasil.append((b, tanya))
    return hasil


def polaritas(k, kata_pos, kata_neg):
    for cal in (k, re.sub(r"(?:nya|ya|in|kan|lah)$", "", k), re.sub(r"^di", "", re.sub(r"(?:nya|in|kan)$", "", k)),
                re.sub(r"^ke(\w{3,})an(?:nya)?$", r"\1", k)):   # v1.0.5 "kerusakan" -> "rusak"
        if cal and len(cal) >= 3:
            if cal != k and cal in {"terima", "kasih"}:
                continue   # v1.0.5: "diterima" bukan "terima kasih"
            if cal in kata_neg:
                return -1
            if cal in kata_pos:
                return 1
    return 0


def _masalah(t):
    return t in MASALAH_HILANG or re.sub(r"(?:nya|ny)$", "", t) in MASALAH_HILANG


def _cakupan_negasi(tok, kata_pos, kata_neg, neg_kustom=frozenset()):
    """v1.0.5: aturan cakupan negasi UMUM (jendela kata), dikembalikan sebagai {indeks: nilai}.
    1. Negasi eksistensial "tidak/belum ada (yang) X" / "tanpa X" / "bebas X" / "anti X": kata masalah X dalam JENDELA_EKSIS kata
       (melewati kata pengisi 'yang', 'satupun', 'sama sekali', dll.) dibalik jadi positif; X berikutnya yang disambung 'dan/atau' ikut.
       "ada" sendiri tidak lagi dihitung keluhan bila yang dinegasi ternyata kata masalah. Bila kata pertama yang ditemui adalah aksi
       ("tidak ada yang bisa dihubungi", "tidak ada yang balas") -> keluhan. Kata benda biasa ("ga ada parkiran") -> aturan lama (keluhan).
    2. Masalah + hilang/sembuh/berkurang dalam JENDELA_HILANG kata ("noda tinta bisa hilang", "jerawat hilang") = hasil baik: masalah 0, hilang +1;
       "noda tidak hilang" tetap keluhan (hilang dinegasi)."""
    tetap = {}
    n = len(tok)
    for i, k in enumerate(tok):
        if k in NEG_EKSIS_AWAL or (k in {"ada", "terdapat", "ditemukan", "kelihatan", "terlihat"} and i >= 1 and tok[i - 1] in {"tidak", "belum"}):
            j, dilihat, balik = i + 1, 0, []
            while j < n and dilihat < JENDELA_EKSIS:
                t = tok[j]
                if t in NEG_EKSIS_ISI:
                    j += 1
                    continue
                p = polaritas(t, kata_pos, kata_neg)
                if p < 0 or t in neg_kustom or _masalah(t):
                    balik.append(j)
                    j += 1
                    continue
                if p > 0 and not balik and k in {"ada", "terdapat"}:
                    # v1.0.6 negasi atas kata POSITIF: "tidak ada (satupun) yang sesuai/ramah/terang" = keluhan
                    tetap[i] = 0
                    tetap[j] = -1
                    break
                if balik or t in NEGATOR or p > 0:
                    break
                if t in AKSI and k not in NEG_EKSIS_AWAL - {"tanpa"} and not balik:
                    if tok[i] in {"ada", "terdapat"}:
                        tetap[i] = 0
                        tetap[j] = -1          # "tidak ada yang bisa dihubungi", "tidak ada yang balas"
                    break
                dilihat += 1
                j += 1
            if balik:
                for b in balik:
                    tetap[b] = 1
                if k not in NEG_EKSIS_AWAL:
                    tetap[i] = 0               # "ada" pada "tidak ada noda" bukan keluhan
                    tetap[i - 1] = 0
                else:
                    tetap[i] = 0
    for j, k in enumerate(tok):
        if k in PENGHILANG and j not in tetap:
            for b in range(j - 1, max(-1, j - 1 - JENDELA_HILANG), -1):
                if _masalah(tok[b]):
                    tetap.setdefault(b, 0)
                    negasi = (j >= 1 and tok[j - 1] in NEGATOR) or (j >= 2 and tok[j - 2] in NEGATOR and tok[j - 1] in PERANTARA)
                    tetap[j] = -1 if negasi else 1
                    break
    return tetap


def skor_klausa(klausa, kata_pos, kata_neg, tanya=False, neg_kustom=frozenset()):
    tok = re.findall(r"[a-z0-9_\[\]]+", klausa)
    tetap = _cakupan_negasi(tok, kata_pos, kata_neg, neg_kustom)   # v1.0.5: indeks -> nilai yang sudah pasti
    skor, i = 0, 0
    terpakai = -1   # indeks kata terakhir yang sudah "dimakan" negasi ("belum sampai" -> kata sesudahnya tidak ikut dinegasi)
    while i < len(tok):
        k = tok[i]
        if i in tetap:
            skor += 0 if (tanya and tetap[i] > 0) else tetap[i]
            i += 1
            continue
        # negasi hanya untuk kata tepat sesudahnya, atau dengan satu kata antara ("tidak pernah telat", "belum juga datang")
        dinegasi = (i >= 1 and tok[i - 1] in NEGATOR) or (i >= 2 and tok[i - 2] in NEGATOR and tok[i - 1] in PERANTARA
                                                           and terpakai != i - 1)
        if k == "kurang":
            j = i + 1
            while j < len(tok) and tok[j] in PENGUAT:
                j += 1
            if dinegasi:
                nilai = 0
            else:
                nilai = -2   # "kurang bersih", "kurang ramah", "colokan kurang"
            if j < len(tok) and polaritas(tok[j], kata_pos, kata_neg):
                i = j        # kata sesudahnya ikut "dimakan"
            skor += nilai
            i += 1
            continue
        if k == "jarang" and not dinegasi and i + 1 < len(tok):
            # v1.0.6 frekuensi: "jarang dibersihin/dibalas/berfungsi" = keluhan; "jarang telat" = pujian ringan;
            # "jarang (banget) nemu/ada seller seramah ini" = pujian kelangkaan -> kata sesudahnya dinilai biasa
            j = i + 1
            while j < len(tok) and tok[j] in PENGUAT:
                j += 1
            if j < len(tok) and tok[j] not in JARANG_LANGKA:
                p = polaritas(tok[j], kata_pos, kata_neg)
                if p < 0:
                    nilai = 1
                elif p > 0 or tok[j] in AKSI or _kata_kerja(tok[j]):
                    nilai = -1
                else:
                    nilai = 0
                if nilai:
                    skor += 0 if (tanya and nilai > 0) else nilai
                    i = j + 1
                    continue
        if k in BERLEBIH:
            j = i + 1
            if j < len(tok):
                p = polaritas(tok[j], kata_pos, kata_neg)
                if dinegasi:
                    nilai = -1 if p > 0 else 0         # "tidak terlalu enak" = keluhan ringan; "tidak terlalu mahal" = netral
                else:
                    nilai = 1 if p > 0 else -1         # "terlalu kencang/manis/lama"
                skor += 0 if (tanya and nilai > 0) else nilai
                i = j + 1
                continue
        nilai = polaritas(k, kata_pos, kata_neg)
        if dinegasi:
            if nilai > 0:
                nilai = -1
            elif nilai < 0:
                nilai = -1 if k in neg_kustom else 1   # kata keluhan kustom tetap keluhan ("tidak dibales")
            elif k in AKSI and not (k == "ada" and (i + 1 >= len(tok) or tok[i + 1] in PENGUAT | {"kak", "ya", "yang", "lagi", "nih", "dong"})):
                nilai = -1   # "belum datang", "tidak berfungsi", "tidak ada kabar"
            elif (tok[i - 1] if tok[i - 1] in NEGATOR else tok[i - 2]) == "belum" and _kata_kerja(k) and k.startswith("di") \
                    and k not in BELUM_WAJAR:
                nilai = -1   # v1.0.6 "belum ditindaklanjuti/dikerjakan/dirapikan" (bukan "belum dicoba")
            if nilai:
                terpakai = i
        if nilai < 0 and k in KELUHAN_KUAT:
            nilai = -2       # "salah kirim ... original": kata positif sesudahnya tidak menetralkan keluhan yang jelas
        if tanya and nilai > 0:
            nilai = 0        # pertanyaan bukan pujian ("sesuai foto tidak?")
        skor += nilai
        i += 1
    return skor


RE_PEMISAH_KLAUSA = re.compile(r"[.!?;,]|\s-\s|\b(?:tapi|namun|cuma|hanya\s+saja|sayang(?:nya)?|sedangkan|padahal|cuman|tetapi)\b")


def _pola_kata(kata, konteks="tema.json", peringatan=None):
    """Kata/frasa tema.json -> regex. Kata ikut dinormalkan seperti teks ('dibales' -> 'dibalas', 'fast respon' -> 'responscepat').
    v1.0.6: entri yang tidak mungkin cocok (bukan teks, tanpa huruf/angka, berisi pemisah klausa) diberi PERINGATAN, tidak diam-diam."""
    bentuk = []
    for k in kata:
        if not isinstance(k, str) or not k.strip():
            if peringatan is not None:
                peringatan.append("%s: entri %r bukan kata/teks - diabaikan. Tulis sebagai \"kata\" dalam tanda kutip." % (konteks, k))
            continue
        n = normalkan(k).strip()
        if not re.search(r"[a-z0-9]", n):
            if peringatan is not None:
                peringatan.append("%s: \"%s\" tidak berisi huruf/angka (mis. emoji/tanda baca) - tidak bisa dicocokkan, diabaikan. "
                                  "Tulis kata biasa." % (konteks, k))
            continue
        if peringatan is not None and RE_PEMISAH_KLAUSA.search(n):
            peringatan.append("%s: frasa \"%s\" berisi pemisah kalimat (koma/titik/'tapi'/'padahal'...) - teks dipecah di situ, jadi frasa "
                              "ini tidak akan pernah cocok. Pecah menjadi dua kata/frasa terpisah." % (konteks, k))
        for v in {k.lower().strip(), n}:
            if v:
                bentuk.append(r"\s+".join(re.escape(b) for b in v.split()))
    return "|".join(sorted(set(bentuk), key=len, reverse=True))


def _kata_sentimen(daftar, konteks="kata_negatif", peringatan=None):
    """v1.0.6: kembalikan (kata tunggal, {token_frasa: regex}). Frasa ('belum kelar', 'pelan banget') dicocokkan pada teks yang SUDAH
    dinormalkan lalu digabung menjadi satu token ('belum_kelar') sebelum sentimen dihitung. Entri yang tidak bisa dipakai -> PERINGATAN."""
    peringatan = [] if peringatan is None else peringatan
    hasil, frasa = set(), {}
    if daftar is None:
        return hasil, frasa
    if isinstance(daftar, str):
        peringatan.append("tema.json: %s harus daftar [\"...\", \"...\"], bukan satu teks - dibaca sebagai satu entri." % konteks)
        daftar = [daftar]
    elif not isinstance(daftar, list):
        peringatan.append("tema.json: %s harus daftar [\"...\"] - diabaikan." % konteks)
        return hasil, frasa
    for k in daftar:
        if not isinstance(k, str) or not k.strip():
            peringatan.append("tema.json: %s berisi entri %r yang bukan kata - diabaikan." % (konteks, k))
            continue
        if re.fullmatch(r"[\d\s.,:/+\-%]+", k.strip()):
            # v1.0.7: angka saja tidak pernah menandai nada ("123", "5") - diabaikan dengan PERINGATAN
            peringatan.append("tema.json: %s \"%s\" hanya berisi angka - tidak bisa menandai nada, diabaikan. Tulis kata, "
                              "mis. \"telat 2 jam\" sebagai frasa." % (konteks, k.strip()))
            continue
        if re.search(r"[,;.!?]", k.strip().rstrip(".!?")):
            # v1.0.7: koma/titik di tengah entri = kemungkinan dua kata digabung ("telat banget, kecewa")
            peringatan.append("tema.json: %s \"%s\" berisi koma/titik - dibaca sebagai SATU frasa yang hanya cocok bila tulisannya persis "
                              "berurutan begitu. Bila maksudnya beberapa kata, tulis sebagai entri terpisah: %s." % (
                                  konteks, k, ", ".join('"%s"' % x.strip() for x in re.split(r"[,;.!?]", k) if x.strip())))
        kata = re.findall(r"[a-z0-9]+", normalkan(k))
        if not kata:
            peringatan.append("tema.json: %s \"%s\" tidak berisi huruf/angka (mis. emoji) - tidak bisa dipakai, diabaikan. Tulis kata biasa."
                              % (konteks, k))
            continue
        if len(kata) == 1:
            hasil.add(kata[0])
            if re.fullmatch(r"[a-z0-9]+", k.lower().strip()):
                hasil.add(k.lower().strip())
            continue
        token = "_".join(kata)
        frasa[token] = re.compile(r"(?<![a-z0-9_])" + r"(?:\s+[^\w\s])*\s+".join(re.escape(x) for x in kata) + r"(?![a-z0-9_])")
        hasil.add(token)
    return hasil, frasa


def gabung_frasa(norm, frasa=None):
    """v1.0.6: frasa kata_positif/kata_negatif -> satu token ('belum kelar' -> 'belum_kelar'); frasa terpanjang lebih dulu."""
    frasa = buat_tema.frasa if frasa is None else frasa
    for token in sorted(frasa, key=len, reverse=True):
        norm = frasa[token].sub(token, norm)
    return norm


def buat_tema(konfigurasi):
    """Tema bawaan (+ tema.json). Kunci tema.json: tema, tambah_kata, hapus_tema, ganti_tema, kata_positif, kata_negatif."""
    tema = [dict(id=i, label=l, dampak=d, pola=re.compile(AFIKS[0] + p + AFIKS[1])) for i, l, d, p in TEMA_BAWAAN]
    kata_pos, kata_neg = set(POS), set(NEG)
    neg_kustom = set()
    frasa = {}
    peringatan = []
    buat_tema.peringatan = peringatan
    if konfigurasi:
        if not isinstance(konfigurasi, dict):
            raise Gagal("tema.json harus berupa objek {...}; lihat templates/tema-contoh.json.")
        if konfigurasi.get("ganti_tema"):
            tema = []
        hapus = konfigurasi.get("hapus_tema", []) or []
        if not isinstance(hapus, list):
            hapus = [hapus]
        hapus = set(str(h) for h in hapus)
        dikenal = {t["id"] for t in tema}
        for h in sorted(hapus - dikenal):
            peringatan.append("tema.json: hapus_tema \"%s\" tidak dikenal - diabaikan. Id bawaan: %s." % (h, ", ".join(sorted(dikenal))))
        tema = [t for t in tema if t["id"] not in hapus]
        for tid, kata in (konfigurasi.get("tambah_kata", {}) or {}).items():
            if not isinstance(kata, list):
                raise Gagal("tema.json: tambah_kata[\"%s\"] harus daftar kata, mis. [\"dibales\", \"fast respon\"]." % tid)
            for t in tema:
                if t["id"] == tid:
                    pola = _pola_kata(kata, "tema.json tambah_kata[\"%s\"]" % tid, peringatan)
                    if pola:
                        t["pola"] = re.compile(t["pola"].pattern[:-len(AFIKS[1])] + "|" + pola + AFIKS[1], re.I)
                    break
            else:
                raise Gagal("tema.json: tambah_kata memakai id \"%s\" yang tidak ada. Id bawaan: %s." % (tid, ", ".join(t[0] for t in TEMA_BAWAAN)))
        daftar = konfigurasi.get("tema", []) or []
        if not isinstance(daftar, list):
            raise Gagal("tema.json: \"tema\" harus daftar [...].")
        for t in daftar:
            if not isinstance(t, dict) or not t.get("id") or not isinstance(t.get("kata", []), list):
                raise Gagal("tema.json: setiap tema perlu \"id\" dan \"kata\" (daftar). Contoh: templates/tema-contoh.json.")
            pola = _pola_kata(t.get("kata", []), "tema.json tema \"%s\"" % t["id"], peringatan)
            if not pola:
                peringatan.append("tema.json: tema \"%s\" tidak punya kata yang bisa dipakai - tema ini diabaikan." % t["id"])
                continue
            try:
                dampak = int(t.get("dampak", 3))
            except (TypeError, ValueError):
                raise Gagal("tema.json: dampak tema \"%s\" harus angka 1-5." % t["id"])
            baru = dict(id=str(t["id"]), label=t.get("label", t["id"]), dampak=max(1, min(5, dampak)),
                        pola=re.compile(AFIKS[0] + "(?:" + pola + ")" + AFIKS[1], re.I))
            tema = [x for x in tema if x["id"] != baru["id"]] + [baru]
        pos_kustom, frasa_pos = _kata_sentimen(konfigurasi.get("kata_positif"), "kata_positif", peringatan)
        neg_kustom, frasa_neg = _kata_sentimen(konfigurasi.get("kata_negatif"), "kata_negatif", peringatan)
        kata_pos |= pos_kustom
        kata_neg |= neg_kustom
        kata_pos -= neg_kustom
        frasa = dict(frasa_pos, **frasa_neg)
    buat_tema.neg_kustom = frozenset(neg_kustom)
    buat_tema.frasa = frasa
    buat_tema.frasa_kata = frozenset(w for t in frasa for w in t.split("_") if w.isalpha())
    return tema, kata_pos, kata_neg


buat_tema.neg_kustom = frozenset()
buat_tema.peringatan = []
buat_tema.frasa = {}
buat_tema.frasa_kata = frozenset()


# v1.0.7 konteks pengiriman. Kata seperti "dikirim/datang/telat/sampai" dipakai juga oleh usaha JASA (EO, fotografer, bimbel, servis,
# desain): "MC datang terlambat", "mockup yang dikirim", "kelas mulai telat". Tanpa kata barang/logistik di kalimat, dan dengan kata jasa,
# itu bukan Pengiriman barang: keterlambatan -> Waktu tunggu / jadwal; kiriman hasil kerja tanpa tema lain -> Layanan.
RE_KIRIM_SAMAR = re.compile(r"\b(?:\w*kirim(?!an\b)\w*|\w*datang\w*|telat\w*|terlambat\w*|keterlambatan|sampai\w*|tiba\w*|molor\w*|ngaret\w*|"
                            r"estimasi\w*|lamban\w*|kilat|instan|instant|tepatwaktu|telatlama)\b")
RE_KONTEKS_BARANG = re.compile(
    r"\b(?:paket\w*|kurir\w*|resi|ekspedisi\w*|ongkir\w*|barang\w*|pesanan\w*|kiriman\w*|pengiriman\w*|pengantaran\w*|kardus\w*|dus|"
    r"gudang|transit|manifest|tracking|lacak\w*|nyasar|belumsampai|belumdikirim|delivery|driver\w*|supir\w*|sopir\w*|ojol|ojek|gojek|grab|"
    r"gosend|grabexpress|shopeefood|gofood|jne|jnt|sicepat|anteraja|spx|ninja|wahana|idexpress|lalamove|paxel|pindahan|truk|produk\w*|"
    r"katering\w*|catering\w*|makanan\w*|nasi|kue\w*|snack\w*|minuman\w*|checkout|order\w*)\b")
RE_KONTEKS_JASA = re.compile(
    r"\b(?:acara\w*|event\w*|sesi\w*|kelas\w*|les|kursus\w*|bimbel\w*|guru\w*|tutor\w*|mentor\w*|pengajar\w*|instruktur\w*|pelatih\w*|"
    r"coach\w*|mc|fotografer\w*|videografer\w*|pemandu\w*|guide\w*|terapis\w*|teknisi\w*|montir\w*|mekanik\w*|tukang\w*|tim\w*|kru\w*|"
    r"crew\w*|rapat\w*|meeting\w*|jadwal\w*|dijadwalkan|janji\w*|booking\w*|reservasi\w*|konsultasi\w*|servis\w*|service\w*|desain\w*|"
    r"dekorasi\w*|cleaning)\b")
# hasil kerja jasa yang "dikirim" (bukan barang fisik): "mockup yang dikirim", "laporan jarang dikirim"
RE_KONTEKS_HASIL = re.compile(r"\b(?:desain\w*|logo\w*|mockup\w*|revisi\w*|laporan\w*|rapor\w*|file\w*|materi\w*|modul\w*|draf\w*|"
                              r"draft\w*|editan\w*|edit\w*|foto\w*|video\w*|jadwal\w*|link\w*|tautan\w*|email\w*|soal\w*|tugas\w*)\b")
RE_TELAT_JASA = re.compile(r"\b(?:telat\w*|terlambat\w*|keterlambatan|molor\w*|ngaret\w*|lama|kelamaan|lambat|lamban\w*|baru|setelah|sesudah|"
                           r"tunggu\w*|telatlama|belum)\b|\d+\s*(?:menit|jam|hari|minggu)")


def _pengiriman_usaha_jasa(k, norm, cocok, tema):
    """Klausa k cocok tema pengiriman. Bila cocoknya HANYA lewat kata samar (kirim/datang/telat/sampai...), kalimatnya tanpa kata
    barang/logistik dan ada kata jasa -> ganti pengiriman dengan waktu_tunggu (terlambat) atau layanan (hasil kerja dikirim)."""
    pola_kirim = next((t["pola"] for t in tema if t["id"] == "pengiriman"), None)
    if pola_kirim is None or pola_kirim.search(RE_KIRIM_SAMAR.sub(" ", k)):
        return cocok   # ada kata pengiriman yang jelas (kurir, resi, ekspedisi, paket ...)
    if RE_KONTEKS_BARANG.search(norm):
        return cocok
    # "dikirim/kirimnya" tetap pengiriman kecuali yang dikirim jelas hasil kerja (desain, laporan, file ...);
    # "datang/telat/molor/sampai" cukup dengan kata jasa (MC, fotografer, kelas, sesi, teknisi ...)
    if re.search(r"\b\w*kirim\w*", k):
        if not RE_KONTEKS_HASIL.search(norm):
            return cocok
    elif not (RE_KONTEKS_JASA.search(norm) or RE_KONTEKS_HASIL.search(norm)):
        return cocok
    ada = {t["id"] for t in tema}
    baru = [c for c in cocok if c != "pengiriman"]
    if RE_TELAT_JASA.search(k) and "waktu_tunggu" in ada:
        if "waktu_tunggu" not in baru:
            baru.append("waktu_tunggu")
    elif not baru and "layanan" in ada:
        baru.append("layanan")
    return baru


# v1.0.13 "paket" dan "instan" ambigu: paket barang kiriman ("paketnya penyok") vs paket produk/menu ("semoga ada paket hemat",
# "paket nasi box untuk arisan") dan makanan instan ("mie instan"). Kata kunci pengiriman yang lemah ini tidak boleh menang atas arti
# produk/menu: bila HANYA kata itu yang membuat klausa cocok Pengiriman dan konteksnya produk/menu, Pengiriman dilepas. Kata kuat
# (kirim, kurir, telat, sampai, resi ...) tetap menang: "paket hemat tapi telat" tetap keluhan Pengiriman.
RE_PENGIRIMAN_LEMAH = re.compile(r"\b(?:paket\w*|instan\w*|instant\w*)\b")
_BUNDEL = (r"hemat|murah|promo|bundling|bundle|combo|reguler|ramadan|ramadhan|lebaran|keluarga|arisan|nasi|box|tumpeng|diet|vegetarian|"
           r"vegan|tanpa|langganan|mingguan|bulanan|harian|premium|spesial|istimewa|sehat|isi\s+\d+")
# paket + kata bundel ("paket hemat", "paket tanpa daging")
RE_PAKET_BUNDEL = re.compile(r"\b(?P<w>paket)(?:an)?\s+(?:\w+\s+)?(?:%s)\w*\b" % _BUNDEL)
# permintaan menawarkan paket ("semoga ada paket", "tolong tambah paket"); hanya untuk klausa saran. "paketnya" (barang) tidak cocok.
RE_PAKET_MINTA = re.compile(r"\b(?:ada|adakan|adain|tambah\w*|bikin\w*|buat\w*|sedia\w*|menyediakan|jual\w*|menjual|tawar\w*|punya|rilis\w*|"
                            r"luncurkan|keluarkan)\s+(?:\w+\s+)?(?P<w>paket)\b")
RE_INSTAN_PRODUK = re.compile(r"\b(?:mie|mi|kopi|bumbu|bubur|susu|teh|minuman|makanan|sambal|kuah|soto|sop|bihun|oat\w*|jus|cokelat|coklat|"
                              r"puding|nasi)\s+(?P<w>instan\w*|instant\w*)\b")


def _pengiriman_hanya_kata_produk(k, jenis, tema):
    """Kembalikan (True, ada_paket_produk) bila Pengiriman di klausa k hanya berasal dari kata lemah (paket/instan) yang jelas berarti
    produk/menu. ada_paket_produk=True bila yang dimaksud paket produk (bukan makanan instan)."""
    pola_kirim = next((t["pola"] for t in tema if t["id"] == "pengiriman"), None)
    if pola_kirim is None or pola_kirim.search(RE_PENGIRIMAN_LEMAH.sub(" ", k)):
        return False, False   # ada kata pengiriman yang kuat -> tetap Pengiriman
    lemah = {m.start() for m in RE_PENGIRIMAN_LEMAH.finditer(k)}
    produk = {m.start("w") for m in RE_PAKET_BUNDEL.finditer(k)}
    if jenis == "saran":
        produk |= {m.start("w") for m in RE_PAKET_MINTA.finditer(k)}
    instan = {m.start("w") for m in RE_INSTAN_PRODUK.finditer(k)}
    if not lemah or not lemah <= (produk | instan):
        return False, False   # ada "paket"/"instan" yang bisa berarti barang kiriman -> perilaku lama
    return True, bool(produk)


_CACHE_TYPO = {}
_TERAKHIR = {}   # hasil normalisasi analisis_item terakhir (dipakai ulang oleh nada_keluhan agar tidak dihitung dua kali)


def analisis_item(teks_anonim, bintang, tema, kata_pos, kata_neg, peran="ulasan", tema_kolom=()):
    """Kembalikan (sentimen_pesan, {tema_id: set(jenis)}). bintang = setara 1-5 (lihat nilai_ke_bintang) atau None."""
    neg_kustom = buat_tema.neg_kustom
    vocab_tambah = frozenset(({w for w in kata_pos | kata_neg if "_" not in w} | buat_tema.frasa_kata) - VOCAB)
    if vocab_tambah:
        if _CACHE_TYPO.get("kunci") != vocab_tambah:
            vocab = VOCAB | vocab_tambah
            _CACHE_TYPO.update(kunci=vocab_tambah, vocab=vocab, peta=_siapkan_typo(vocab))
        vocab, peta = _CACHE_TYPO["vocab"], _CACHE_TYPO["peta"]
    else:
        vocab = peta = None
    norm = normalkan(teks_anonim, vocab, peta)
    klausa = pecah_klausa(gabung_frasa(norm) if buat_tema.frasa else norm)   # v1.0.6 frasa kata_positif/kata_negatif = satu token
    _TERAKHIR.clear()
    _TERAKHIR.update(teks=teks_anonim, norm=norm, skor=[])
    total = 0
    per_tema = defaultdict(set)
    tanpa_tema_keluhan = False
    restock_keluhan = None
    if "tanyarestock" in norm:
        restock_keluhan = _restock_keluhan(teks_anonim, norm, bintang)
    for k, tanya in klausa:
        s = skor_klausa(k, kata_pos, kata_neg, tanya, neg_kustom)
        k = k.replace("_", " ")   # tema & penanda lain dicocokkan pada kata aslinya (frasa tidak menyembunyikan kata tema)
        _TERAKHIR["skor"].append(s)
        optatif = bool(s > 0 and RE_OPTATIF.search(k) and set(re.findall(r"[a-z]+", k)) & NEGATOR)
        if optatif:
            s = 0   # "semoga lain kali tidak telat" = harapan, bukan pujian
        total += s
        if s > 0:
            jenis = "pujian"
        elif s < 0:
            jenis = "keluhan"
        elif bintang is not None and bintang <= 2 and not tanya:
            jenis = "keluhan"
        elif bintang is not None and bintang >= 4 and not tanya:
            jenis = "pujian"
        else:
            jenis = "netral"
        if jenis != "keluhan" and (optatif or SARAN.search(k) or (tanya and TANYA_MINTA.search(k)) or peran == "saran"
                                   or (s == 0 and re.search(r"\bsemoga\b", k))):   # v1.0.6 "semoga stoknya segera ada" = harapan
            jenis = "saran"
        if s == 0 and "lamawajar" in k:
            jenis = "netral"   # "telat karena tanggal merah, wajar" = dimaklumi pelanggan: bukan keluhan, bukan pujian
        if s == 0 and restock_keluhan is not None and "tanyarestock" in k:
            # "kapan restock?" = keluhan hanya bila ada nada kecewa/bintang <= 3; bernada senang/bintang 4-5 = permintaan (saran)
            jenis = "keluhan" if restock_keluhan else "saran"
            if restock_keluhan and bintang is None:
                total -= 1
        cocok = [t["id"] for t in tema if t["pola"].search(k)]
        # salah kirim/jumlah kurang = ketepatan pesanan, bukan keterlambatan: kata "dikirim/datang" saja tidak cukup untuk tema pengiriman
        if "ketepatan_pesanan" in cocok and "pengiriman" in cocok and not re.search(
                r"pengiriman|kurir|ekspedisi|telat|terlambat|lambat|lama|kilat|ngaret|molor|resi|nyasar|belumsampai", k):
            cocok.remove("pengiriman")
        # "datang" saja (pelanggan datang ke toko, menu datang) tidak cukup untuk tema pengiriman bila tema lain sudah cocok
        if "pengiriman" in cocok and len(cocok) > 1:
            pola_kirim = next(t["pola"] for t in tema if t["id"] == "pengiriman")
            if not pola_kirim.search(re.sub(r"\b\w*datang\w*\b", " ", k)):
                cocok.remove("pengiriman")
        if "pengiriman" in cocok:
            produk_saja, paket_produk = _pengiriman_hanya_kata_produk(k, jenis, tema)
            if produk_saja:   # v1.0.13 "semoga ada paket hemat" / "mie instan" = produk/menu, bukan pengiriman
                cocok.remove("pengiriman")
                if paket_produk and jenis == "saran" and "varian_menu" not in cocok and any(t["id"] == "varian_menu" for t in tema):
                    cocok.append("varian_menu")   # permintaan paket = permintaan menu/produk
        if "pengiriman" in cocok:
            cocok = _pengiriman_usaha_jasa(k, norm, cocok, tema)
        for tid in cocok:
            per_tema[tid].add(jenis)
        if jenis == "keluhan" and not cocok:
            tanpa_tema_keluhan = True
    if tanpa_tema_keluhan:  # "kecewa." tanpa tema -> ikut tema netral di pesan yang sama
        for tid, j in per_tema.items():
            if j == {"netral"}:
                j.discard("netral")
                j.add("keluhan")
    for tid in tema_kolom:
        per_tema[tid].add("saran" if peran == "saran" else "netral")
    if bintang is not None:
        sent = "positif" if bintang >= 4 else "netral" if bintang == 3 else "negatif"
    elif peran == "saran" and total >= 0:
        sent = "netral"
    else:
        sent = "positif" if total > 0 else "negatif" if total < 0 else "netral"
    return sent, per_tema


RE_RESTOCK_KECEWA = re.compile(
    r"\b(?:lama|kelamaan|sudahlama|tunggulama|terus|lagi\s+lagi|sering|selalu|kecewa|mengecewakan|berkali|habis|kosong|kehabisan|"
    r"tidak\s+pernah|belum\s+juga|hinggakini|capek|bosan|php|kesal|dari\s+(?:bulan|minggu|kemarin|dulu|lama)|sudah\s+\d+|kok|masa)\b")
RE_RESTOCK_SENANG = re.compile(
    r"\b(?:orderlagi|mau\s+(?:\w+\s+)?(?:order|beli|pesan|ambil|checkout|borong|coba)|pengen|ingin|suka|naksir|incar\w*|favorit|"
    r"langganan|terima\s+kasih|recommended|bagus|enak|cantik|mantap|keren|love|lucu|cocok)\b")
RE_EMOJI_SENANG = re.compile(r"[\U0001F60D\U0001F970\u2764\U0001F60A\u263A\U0001F929\U0001F495\U0001F496\u2728\U0001F917\U0001F618"
                             r"\U0001F64F\U0001F601\U0001F604\U0001F973]")


def _restock_keluhan(teks, norm, bintang):
    """Pertanyaan restock/ready: True = keluhan stok, False = permintaan (catatan saran)."""
    if bintang is not None and bintang <= 3:
        return True
    if RE_RESTOCK_KECEWA.search(norm) or RE_EMOJI_KELUHAN.search(teks):
        return True
    if bintang is not None and bintang >= 4:
        return False
    return not (RE_RESTOCK_SENANG.search(norm) or RE_EMOJI_SENANG.search(teks))


# Jaring pengaman: penanda nada keluhan umum (dibaca pada teks yang sudah dinormalkan). Hanya untuk daftar "Perlu dibaca agent",
# tidak pernah menambah angka tabel keluhan.
RE_NADA_KELUHAN = re.compile(
    r"\b(?:kok|masa|padahal|kecewa|mengecewakan|komplain|kapok|menyesal|rugi|dirugikan|kesal|jengkel|sebal|zonk|parah|php|tipu|penipu|"
    r"bohong|batal|dibatalkan|refund|retur|harusnya|seharusnya|terus\s+menerus|berkali|lagi\s+lagi|bagaimana\s+sih|tolong\s+dong|"
    r"mending|kapan\s+lagi\s+tidak|tidak\s+lagi|tidak\s+akan|sayang\s+sekali|sayangnya|marah|kesel|bosan|biasa\s+saja|jelek|buruk|"
    r"bukan\s+(?:yang|barang|pesanan)|tetap\s+saja|(?:cuma|hanya|cuman)\s+(?:\w+\s+)?\d+|yang\s+(?:datang|dikirim|sampai|dapat|dikasih)\w*|"
    r"masih\s+(?:di)?(?:kemas|proses)\w*|belum\s+juga|sampai\s+sekarang|hinggakini|ternyata\s+(?:tetap|masih|malah)|"
    r"katanya\b[^.!?]{0,60}\bternyata|(?:sesudah|setelah)\b[^.!?]{0,60}\bmalah)\b"
    r"|[\U0001F620\U0001F621\U0001F92C\U0001F624\U0001F612\U0001F644\U0001F44E\U0001F61E\U0001F614\U0001F622\U0001F62D\U0001F494\U0001F611]")
RE_EMOJI_KELUHAN = re.compile(r"[\U0001F620\U0001F621\U0001F92C\U0001F624\U0001F612\U0001F644\U0001F44E\U0001F61E\U0001F614\U0001F622"
                              r"\U0001F62D\U0001F494\U0001F611]")


# v1.0.4 sindiran: pujian/emoji ironi + konteks buruk ("keren, belum dijawab dari minggu lalu 👍", "hebat, datang pas sudah selesai 😂")
RE_SINDIR_PUJI = re.compile(r"\b(?:hebat|keren|mantap|salut|luar\s+biasa|wow|top|juara|pintar|pinter|bagus|sip|the\s+best|good\s+job|"
                            r"terima\s+kasih\s+(?:loh|lho|ya|banyak|sekali)|makasih\s+(?:loh|lho))\b")
RE_SINDIR_EMOJI = re.compile(r"[\U0001F643\U0001F644\U0001F44F\U0001F642]")   # 🙃 🙄 👏 🙂
# v1.0.5: konteks buruk dibagi dua. KUAT = jelas buruk apa pun kalimatnya (waktu molor, acara sudah bubar, tidak ada kabar).
# LEMAH ("belum", "rusak", "malah", "tidak bisa") hanya dihitung bila klausanya memang bernilai negatif - "keren, tidak ada yang rusak 👏",
# "hebat, noda bisa hilang 👏", "mantap, malah dapat bonus 👏" bukan sindiran.
RE_SINDIR_KONTEKS = re.compile(
    r"\b(?:hinggakini|sudahlama|tunggulama|nyasar|kelamaan|selesai\s+makan|"
    r"sudah\s+(?:selesai|bubar|lewat|tutup|pulang|kelar|berangkat)(?!\s+(?:di|ter)\w{3,})|dari\s+(?:minggu|bulan)\s+(?:lalu|kemarin)|tidak\s+ada\s+kabar|"
    r"(?:sampai|baru)\s+\d+\s*(?:hari|minggu|bulan)|\d+\s*(?:hari|minggu|bulan)\s+baru|"
    # v1.0.6: hasil yang baru datang sesudah N hari ("dikirim setelah 6 hari", "refund diproses setelah 3 minggu")
    r"(?:dikirim|datang|sampai|dibalas|diproses|direspons|dikerjakan|selesai|kelar|diantar|dicairkan|refund\w*)\s+(?:\w+\s+){0,2}?"
    r"(?:setelah|sesudah|baru)\s+(?:\d+|se)\s*(?:hari|minggu|bulan))\b")
RE_SINDIR_KONTEKS_LEMAH = re.compile(r"\b(?:belum(?!\s+pernah)|tidak\s+bisa|muter|remuk|penyok|hancur|rusak|mati|malah|hilang)\b")
# v1.0.4 pertanyaan menagih: "kok belum dikirim?", "sudah transfer dari pagi, belum lunas kak?"
RE_TAGIH_KOK = re.compile(r"\b(?:kok|masa|kenapa|mengapa)\b(?:\s+\w+){0,4}?\s+(?:belum|tidak|masih)\b")
RE_TAGIH_BELUM = re.compile(r"\bbelum\s+(?:juga\s+)?(?!(?:pernah|kak|ya|sih|min|nih|dong|kah|gan|sis|bang|mas|mbak|ada\s+yang)\b)[a-z]{3,}")
RE_TAGIH_KONTEKS = re.compile(r"\b(?:sudah|transfer|bayar|dibayar|checkout|pesan|order|dari|kemarin|tadi|hinggakini|sudahlama|kok|masa)\b")


# v1.0.7 penanda keterlambatan/kekurangan untuk sindiran TANPA kata negatif: "baru dibalas sore", "3 hari baru jawab", "akhirnya dibalas
# juga", "pesan 10 cuma datang 7", "sampai 3 jam". Dipakai hanya bersama kata pujian di klausa pertama (atau emoji ironi) dan hanya bila
# klausa lain tidak berisi pujian nyata ("masih enak sampai 3 hari", "baru dipakai noda hilang" bukan sindiran).
_AKSI_TELAT = (r"(?:di\w{3,}|datang|sampai|tiba|jawab|balas|respons|muncul|nongol|kelar|selesai|beres|jadi|cair|masuk|kirim|bisa|mau|"
               r"ada\s+kabar|dikabari|ditanggapi|diproses|dikerjakan)")
RE_SINDIR_TANDA = re.compile(
    r"\bbaru\s+(?:\w+\s+){0,1}?" + _AKSI_TELAT + r"\b"
    r"|\b(?:\d+|se|satu|dua|tiga|empat|lima)\s*(?:menit|jam|hari|minggu|bulan)\s+(?:\w+\s+){0,2}?baru\b"
    r"|\b(?:dari|sejak)\s+(?:pagi|siang|sore|malam|kemarin|tadi|minggu\s+lalu|bulan\s+lalu|jam\s+\d+)\b[^.!?]{0,40}?\bbaru\b"
    r"|\bakhirnya\s+(?:\w+\s+){0,2}?" + _AKSI_TELAT + r"\b"
    r"|\b(?:cuma|hanya|cuman)\s+(?:di\w{3,}|datang|dapat|sampai|ada|isi(?:nya)?)\s+(?:\w+\s+)?\d+\b"
    r"|\b(?:pesan|order|beli|minta)\w*\s+\d+\s+(?:\w+\s+){0,2}?(?:cuma|hanya|cuman)\s+(?:\w+\s+)?\d+\b"
    r"|\b(?:sampai|hingga)\s+(?:\d+\s*|se|satu\s+|dua\s+|tiga\s+)(?:jam|hari|minggu|bulan)\b"
    r"|\b(?:setelah|sesudah)\s+(?:di\w{3,}|\d+\s*(?:jam|hari|minggu|bulan)|se(?:jam|hari|minggu|bulan)|(?:\w+\s+)?acara\w*)\b")


def _sindiran_tanda(norm):
    """Pujian di awal + penanda keterlambatan/kekurangan, tanpa pujian nyata di klausa lain."""
    klausa = pecah_klausa(norm)
    if not klausa or not RE_SINDIR_TANDA.search(norm):
        return False
    awal = klausa[0][0]
    puji = RE_SINDIR_PUJI.search(awal) or re.search(r"\b(?:mantap|salut|keren|hebat|top|juara)\w*", awal)
    if not puji:
        return False
    sisa = [(RE_SINDIR_PUJI.sub(" ", k), t) for k, t in klausa]
    sisa = [(re.sub(r"\b(?:mantap|keren|hebat|salut|top|juara|sekali|banget|min|kak|deh|sih|dong|wah|markotop|mantul)\b", " ", k), t)
            for k, t in sisa]
    return all(skor_klausa(k, POS, NEG, t) <= 0 for k, t in sisa if k.strip())


def sindiran_atau_tagih(teks_anonim, norm):
    """True bila kalimat mirip sindiran atau pertanyaan menagih (hanya untuk 'Perlu dibaca agent', tidak menambah tabel)."""
    if _sindiran_tanda(norm):
        return True
    if RE_SINDIR_PUJI.search(norm) or RE_SINDIR_EMOJI.search(teks_anonim):
        for k, tanya in pecah_klausa(norm):
            m = RE_SINDIR_KONTEKS.search(k)
            # v1.0.7: "masih enak sampai 3 hari" = daya tahan (pujian), bukan waktu tunggu
            if m and not (re.match(r"(?:sampai|baru)\b", m.group(0)) and skor_klausa(k, POS, NEG, tanya) > 0):
                return True
        for k, tanya in pecah_klausa(norm):
            if RE_SINDIR_KONTEKS_LEMAH.search(k) and skor_klausa(k, POS, NEG, tanya) < 0:
                return True
    for k, tanya in pecah_klausa(norm):
        if tanya and (RE_TAGIH_KOK.search(k) or (RE_TAGIH_BELUM.search(k) and RE_TAGIH_KONTEKS.search(norm))):
            return True
    return False


def nada_keluhan(teks_anonim, bintang, kata_pos=None, kata_neg=None):
    """True bila masukan bernada keluhan: bintang/nilai rendah, ada klausa negatif, atau penanda keluhan umum tanpa nada positif."""
    if bintang is not None and bintang <= 2:
        return True
    if _TERAKHIR.get("teks") == teks_anonim:
        norm, skor = _TERAKHIR["norm"], _TERAKHIR["skor"]
    else:
        kata_pos = POS if kata_pos is None else kata_pos
        kata_neg = NEG if kata_neg is None else kata_neg
        norm = normalkan(teks_anonim)
        skor = [skor_klausa(k, kata_pos, kata_neg, tanya, buat_tema.neg_kustom)
                for k, tanya in pecah_klausa(gabung_frasa(norm) if buat_tema.frasa else norm)]
    if any(x < 0 for x in skor):
        return True
    if sindiran_atau_tagih(teks_anonim, norm):
        return True
    return bool(RE_NADA_KELUHAN.search(norm) or RE_NADA_KELUHAN.search(teks_anonim)) and sum(skor) <= 0


def perlu_dibaca(i, kata_pos=None, kata_neg=None):
    """Alasan masukan wajib dibaca agent, atau None. Tidak ada keluhan yang boleh hilang diam-diam:
    - 'tanpa tema': tidak cocok tema mana pun;
    - 'keluhan tanpa tabel': bernada keluhan tetapi tidak dihitung sebagai keluhan di tema mana pun."""
    if i.get("koreksi") and i["tema"]:
        return None   # v1.0.8 sudah diputuskan agent lewat --koreksi
    if not i["tema"]:
        return "tanpa tema"
    if any("keluhan" in j for j in i["tema"].values()):
        return None
    nada = i.get("nada_keluhan")
    b = i.get("bintang_setara", i.get("bintang"))
    if nada is None:
        nada = nada_keluhan(i["teks"], b, kata_pos, kata_neg)
    if nada:
        return "keluhan tanpa tabel"
    # v1.0.6 invarian: tema yang hanya "netral" (tanpa keluhan/pujian/saran) + tanpa nilai tinggi = nada belum terbaca. Masukan seperti ini
    # dulu hanya tertangkap sebagai "tanpa tema"; menambah kata tema TIDAK BOLEH mengeluarkannya dari daftar baca.
    jenis = set().union(*i["tema"].values())
    if (jenis <= {"netral"} and i.get("peran") != "saran" and (b is None or b == 3) and i.get("sentimen") != "positif"
            and not re.search(r"\?[\s\W]*$", i["teks"])):
        return "tema tanpa nada"
    return None


def potong(t, n=140):
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


STOP = set("""yang dan di ke dari untuk dengan ini itu saya kami kita kak ya nya juga sudah tidak tapi atau ada pada saja
lagi sama karena jadi bisa mau akan sih deh dong kok banget terima kasih namax hpx nomorx tautanx akunx emailx alamatx platx teleponx""".split())


def olah(sumber, opsi, konfigurasi=None):
    tema, kata_pos, kata_neg = buat_tema(konfigurasi)
    item = []
    dibuang = Counter()
    meta = {"pengirim": {}, "sumber": [], "peringatan": list(buat_tema.peringatan)}
    buang_teks_sama = getattr(opsi, "buang_teks_sama", False)
    staf = [s.lower() for s in getattr(opsi, "staf_list", [])]
    for spes in sumber:
        kanal, mentah, info, hitung = baca_berkas(spes, opsi)
        n_awal = len(item)
        if info["jenis"] == "whatsapp":
            meta["pengirim"][kanal] = hitung
            nama = list(hitung)
            balas = _balasan_wa(mentah, staf, info.get("urutan", "hb"), getattr(opsi, "batas_balas_jam", 24))
            if staf and not any(any(s_ in (p[1] or "").lower() for s_ in staf) for p in mentah):
                meta["peringatan"].append("%s: tidak ada pesan dari staf (%s) - nama --staf tidak cocok dengan pengirim? Balasan admin TIDAK "
                                          "dihitung. Cek dengan --daftar-pengirim." % (info["berkas"], ", ".join(getattr(opsi, "staf_list", []))))
                balas = {}
            for idx, (tgl, pengirim, isi, _jam) in enumerate(mentah):
                if pengirim is None or RE_SISTEM_TEKS.fullmatch(isi.strip()) or RE_PENGIRIM_MEDIA.fullmatch(isi.strip()):
                    dibuang["pesan sistem/media"] += 1
                    continue
                if any(s in pengirim.lower() for s in staf):
                    dibuang["pesan staf"] += 1
                    continue
                ada_media = bool(RE_PENGIRIM_MEDIA.search(isi))
                isi = RE_PENGIRIM_MEDIA.sub("", isi).strip()
                if ada_media and not re.search(r"\w", isi) and not RE_EMOJI_KELUHAN.search(isi):
                    dibuang["pesan sistem/media"] += 1
                    continue
                dibalas, jeda = balas.get(idx, (None, None))
                item.append(dict(kanal=kanal, tgl=tgl, nilai=None, skala=None, isi=isi, nama=nama, peran="ulasan", urutan=info.get("urutan", "hb"),
                                 identitas=(info["berkas"], pengirim.lower(), tgl), berkas=info["berkas"], min_kata=2,
                                 dibalas=dibalas, jeda_balas=jeda, sumber_balas="wa"))
        else:
            for b in mentah:
                if b.get("kosong"):
                    dibuang["jawaban kosong ('-', 'tidak ada')"] += 1
                    continue
                item.append(dict(kanal=b.get("kanal") or kanal, tgl=b["tgl"], nilai=b["nilai"], skala=b["skala"], isi=b["isi"], nama=(),
                                 peran=b.get("peran", "ulasan"), kolom=b.get("kolom"), urutan=b.get("urutan", "hb"),
                                 identitas=(info["berkas"],) + b["identitas"] if b.get("identitas") else None, berkas=info["berkas"],
                                 # ulasan 1 kata tetap dihitung bila ada nilai/bintang ("basi" + bintang 1) atau dari kolom permintaan
                                 min_kata=1 if b.get("peran") == "saran" or b["nilai"] is not None else 2,
                                 dibalas=b.get("dibalas"), jeda_balas=None, sumber_balas="csv"))
        info["masukan_mentah"] = len(item) - n_awal
        meta["sumber"].append(info)
        for p in info["peringatan"]:
            meta["peringatan"].append("%s: %s" % (info["berkas"], p))
        for c in info.get("catatan", []):
            if "Windows-1252" in c:
                meta["peringatan"].append("%s: %s (periksa huruf/emoji yang aneh)" % (info["berkas"], c))
    hasil_item = []
    dilihat = set()
    teks_sama = Counter()
    pendek_per_berkas = Counter()
    for it in item:
        anonim = samarkan(it["isi"], it["nama"])
        bersih = re.sub(r"\W+", " ", anonim.lower()).strip()
        # jaring pengaman: "😡😡" atau "zonk" dengan bintang 1-2 tetap dihitung (bukan dibuang sebagai 'terlalu pendek')
        b_setara = None if it["peran"] == "saran" else nilai_ke_bintang(it["nilai"], it["skala"])
        pendek_keluhan = bool(anonim.strip()) and ((b_setara is not None and b_setara <= 2) or RE_EMOJI_KELUHAN.search(anonim))
        if pendek_keluhan and not bersih:
            bersih = anonim.strip()
        elif not pendek_keluhan and (not bersih or len(re.findall(r"\w+", bersih)) < it["min_kata"] or not re.search(r"[a-z]", bersih)):
            dibuang["terlalu pendek"] += 1
            pendek_per_berkas[it["berkas"]] += 1
            continue
        if buang_teks_sama:
            kunci = (it["kanal"], bersih)
        elif it["identitas"] is not None:
            kunci = (it["identitas"], it["nilai"], bersih)
        else:
            kunci = None
        if kunci is not None and kunci in dilihat:
            dibuang["duplikat (baris identik)" if not buang_teks_sama else "teks sama (--buang-teks-sama)"] += 1
            continue
        if kunci is not None:
            dilihat.add(kunci)
        teks_sama[(it["kanal"], bersih)] += 1
        # kolom permintaan ("Menu apa yang ingin ditambah?"): nilai baris tidak dipakai untuk menebak keluhan
        bintang_setara = None if it["peran"] == "saran" else nilai_ke_bintang(it["nilai"], it["skala"])
        tema_kolom = []
        if it["peran"] == "saran" and it.get("kolom"):
            kolom_norm = normalkan(it["kolom"])
            tema_kolom = [t["id"] for t in tema if t["pola"].search(kolom_norm)]
        sent, per_tema = analisis_item(anonim, bintang_setara, tema, kata_pos, kata_neg, it["peran"], tema_kolom)
        nada = it["peran"] != "saran" and nada_keluhan(anonim, bintang_setara, kata_pos, kata_neg)
        hasil_item.append({"nada_keluhan": nada, "bintang_setara": bintang_setara,
                           "kanal": it["kanal"], "bulan": bulan_dari(it["tgl"], it.get("urutan", "hb")),
                           "bintang": int(round(it["nilai"])) if it["nilai"] is not None and it["skala"] == 5 else None,
                           "nilai_0_10": it["nilai"] if it["skala"] == 10 else None, "peran": it["peran"],
                           "teks": anonim, "sentimen": sent, "tema": {k: sorted(v) for k, v in per_tema.items()},
                           "dibalas": it.get("dibalas"), "jeda_balas_menit": it.get("jeda_balas"), "sumber_balas": it.get("sumber_balas")})
    sekarang = datetime.date.today()
    depan = sorted({i["bulan"] for i in hasil_item if i["bulan"] and i["bulan"] > "%04d-%02d" % (sekarang.year, sekarang.month)})
    if depan:
        meta["peringatan"].append("ada masukan bertanggal di masa depan (bulan %s) - kemungkinan urutan hari/bulan tertukar atau tanggal salah; "
                                  "periksa dengan --urutan-tanggal." % ", ".join(depan))
    sama = sum(c - 1 for c in teks_sama.values() if c > 1)
    if sama:
        meta["peringatan"].append("%d masukan bertulisan sama dari pengirim/baris berbeda tetap dihitung (bukan duplikat). "
                                  "Bila itu tempelan ganda, hapus di berkas atau pakai --buang-teks-sama." % sama)
    for info in meta["sumber"]:
        n = info.get("masukan_mentah", 0)
        p = pendek_per_berkas.get(info["berkas"], 0)
        if n >= 5 and p > 0.3 * n:
            kol = (" (kolom dipakai: %s)" % ", ".join(info["kolom_teks"])) if info.get("kolom_teks") else ""
            meta["peringatan"].append("%s: %d dari %d masukan terlalu pendek/kosong%s - periksa apakah kolom/berkasnya benar." % (
                info["berkas"], p, n, kol))
    if getattr(opsi, "koreksi", None):
        meta["koreksi"] = terapkan_koreksi(hasil_item, opsi.koreksi, tema, meta["peringatan"])
    return hasil_item, tema, dict(dibuang), meta


def _balasan_wa(pesan, staf, urutan="hb", batas_jam=24):
    """v1.0.8 {indeks pesan pelanggan: (dibalas_dalam_batas, jeda_menit)}. Pesan pelanggan dianggap dibalas bila pesan BERIKUTNYA dari
    pengirim lain adalah staf, dalam batas jam. Pesan beruntun dari pelanggan yang sama ikut dibalas oleh balasan yang sama.
    Paling akurat untuk ekspor per pelanggan; di ekspor grup/campuran, balasan untuk orang lain bisa terhitung. Tanpa --staf: {}."""
    if not staf:
        return {}
    hasil = {}
    n = len(pesan)
    for i, (tgl, pengirim, isi, jam) in enumerate(pesan):
        if pengirim is None or any(s_ in pengirim.lower() for s_ in staf):
            continue
        j = i + 1
        while j < n and (pesan[j][1] is None or pesan[j][1] == pengirim):
            j += 1
        if j >= n or not any(s_ in pesan[j][1].lower() for s_ in staf):
            hasil[i] = (False, None)
            continue
        t1, t2 = _tanggal_wa(tgl, urutan), _tanggal_wa(pesan[j][0], urutan)
        jeda = None
        if t1 and t2 and jam is not None and pesan[j][3] is not None:
            jeda = (t2 - t1).days * 1440 + pesan[j][3] - jam
        hasil[i] = (jeda is None or jeda <= batas_jam * 60, jeda)
    return hasil


KOLOM_KOREKSI = ("cuplikan", "tema", "jenis", "sentimen", "catatan")


def terapkan_koreksi(hasil_item, path, tema, peringatan):
    """v1.0.8 koreksi agent yang TERCATAT: CSV kolom cuplikan,tema,jenis,sentimen,catatan. Masukan yang teks (sudah disamarkan) memuat
    cuplikan diberi tema/jenis/sentimen baru; '-tema' membuang tema. Hitungan lalu dihitung ulang script (bukan diubah tangan)."""
    teks, _ = baca_mentah(path)
    try:
        baris = list(csv.DictReader(io.StringIO(teks.lstrip("\ufeff"))))
    except csv.Error as e:
        raise Gagal("berkas koreksi %s tidak bisa dibaca sebagai CSV (%s)." % (path, e))
    if not baris or "cuplikan" not in {(h or "").strip().lower() for h in baris[0]}:
        raise Gagal("berkas koreksi %s harus CSV dengan judul kolom: %s (lihat templates/koreksi-contoh.csv)." % (path, ",".join(KOLOM_KOREKSI)))
    ids = {t["id"] for t in tema}
    catat = []
    for no, b in enumerate(baris, 2):
        b = {(k or "").strip().lower(): (v or "").strip() for k, v in b.items()}
        cup = re.sub(r"\s+", " ", b.get("cuplikan", "")).lower()
        if len(cup) < 5:
            peringatan.append("koreksi baris %d: cuplikan kosong/terlalu pendek (min. 5 huruf) - dilewati." % no)
            continue
        jenis = (b.get("jenis") or "keluhan").lower()
        sent = (b.get("sentimen") or "").lower()
        if jenis not in ("keluhan", "pujian", "saran", "netral") or sent not in ("", "positif", "netral", "negatif"):
            peringatan.append("koreksi baris %d: jenis harus keluhan/pujian/saran/netral dan sentimen positif/netral/negatif - dilewati." % no)
            continue
        tambah, buang, salah = [], [], []
        for t in re.split(r"[;,]", b.get("tema", "")):
            t = t.strip().lower()
            if not t:
                continue
            (buang if t.startswith("-") else tambah).append(t.lstrip("-"))
            if t.lstrip("-") not in ids:
                salah.append(t.lstrip("-"))
        if salah:
            peringatan.append("koreksi baris %d: tema tidak dikenal: %s (pakai id tema, mis. %s) - dilewati." % (
                no, ", ".join(salah), ", ".join(sorted(ids)[:6])))
            continue
        kena = [i for i in hasil_item if cup in re.sub(r"\s+", " ", i["teks"]).lower()]
        if not kena:
            peringatan.append("koreksi baris %d: cuplikan \"%s\" tidak ditemukan di masukan (cocokkan dengan teks yang SUDAH disamarkan) - "
                              "tidak diterapkan." % (no, b.get("cuplikan")))
            continue
        if len(kena) > 1:
            peringatan.append("koreksi baris %d: cuplikan \"%s\" cocok dengan %d masukan - semuanya dikoreksi; perpanjang cuplikan bila "
                              "hanya satu yang dimaksud." % (no, b.get("cuplikan"), len(kena)))
        for i in kena:
            for t in buang:
                i["tema"].pop(t, None)
            for t in tambah:
                i["tema"][t] = [jenis]
            if sent:
                i["sentimen"] = sent
            if jenis == "keluhan":
                if tambah:
                    i["nada_keluhan"] = True
            else:
                # v1.0.10: koreksi "bukan keluhan" berlaku untuk SEMUA hitungan (tabel tema, respons staf, perlu dibaca)
                i["nada_keluhan"] = False
                for t_, js in list(i["tema"].items()):
                    js2 = [j for j in js if j != "keluhan"]
                    i["tema"][t_] = js2 or [jenis]
            i["koreksi"] = b.get("catatan") or "koreksi agent"
        catat.append({"baris": no, "cuplikan": b.get("cuplikan"), "tema": b.get("tema", ""), "jenis": jenis, "sentimen": sent,
                      "catatan": b.get("catatan", ""), "masukan": len(kena)})
    return catat


RINCIAN_KEAMANAN = [
    ("jamur", r"\b(?:jamur|berjamur|jamuran|bulukan|berbulu)\b"),
    ("hewan/serangga", r"\b(?:semut|lalat|ulat|kecoa|belatung|tikus|serangga|kutu|cicak)\b"),
    ("basi/kedaluwarsa", r"\b(?:basi|kedaluwarsa|kadaluarsa|expired|berlendir)\b"),
    ("benda asing", r"\b(?:rambut|kerikil|pecahan|bendaasing|benda\s+asing|staples|paku)\b"),
    ("sakit (diare/mual/alergi)", r"\b(?:sakit\s*perut|diare|keracunan|mual|muntah|alergi)\b"),
]


def rincian_keamanan(rows):
    """v1.0.10 pecah keluhan tema Keamanan per jenis (jamur vs hewan/serangga dst.). Satu pesan dihitung ke jenis PERTAMA yang cocok,
    jadi jumlah rincian = jumlah keluhan tema."""
    c = Counter()
    for i in rows:
        t = (i["teks"] + " " + normalkan(i["teks"])).lower()
        c[next((n for n, pola in RINCIAN_KEAMANAN if re.search(pola, t)), "lainnya")] += 1
    urut = [n for n, _ in RINCIAN_KEAMANAN] + ["lainnya"]
    return {n: c[n] for n in urut if c[n]}


def _persen_id(a, b):
    if not b:
        return "0%"
    v = "%.1f" % (a * 100.0 / b)
    return v.replace(".", ",").replace(",0", "") + "%"


def kalimat_siap_salin(r):
    """v1.0.10 kalimat ringkasan berangka yang dicetak script supaya agent CUKUP MENYALIN (tidak menulis/menghitung angka sendiri)."""
    n = r["total_masukan"]
    out = ["Total %d masukan dari %s." % (n, ", ".join("%s %d" % kv for kv in r["per_kanal"].items()))]
    for k, v in r.get("respons_staf", {}).items():
        a = v["keluhan_tanpa_balasan"]
        tb = v["tanpa_balasan"]
        kal = "Keluhan tanpa balasan (%s): %d dari %d keluhan (%s); pesan tanpa balasan: %d dari %d pesan (%s)" % (
            k, a, v["keluhan"], _persen_id(a, v["keluhan"]), tb, v["masukan"], _persen_id(tb, v["masukan"]))
        if v["keluhan_dibalas_lambat"]:
            kal += "; keluhan dibalas lewat %d jam: %d" % (r.get("batas_balas_jam", 24), v["keluhan_dibalas_lambat"])
        out.append(kal + ".")
    if len(r.get("sentimen_per_kanal", {})) > 1:
        out.append("Sentimen per kanal: " + "; ".join("%s: positif %d, netral %d, negatif %d" % (k, v["positif"], v["netral"], v["negatif"])
                                                      for k, v in r["sentimen_per_kanal"].items()) + ".")
    for d in [d for d in r["tema"] if d["keluhan"]][:6]:
        kal = "%s: %d keluhan (%s dari semua masukan; prioritas %s)" % (d["label"], d["keluhan"], _persen_id(d["keluhan"], n), d["prioritas"])
        if d.get("rincian"):
            kal += "; rincian: " + ", ".join("%s %d" % kv for kv in d["rincian"].items())
        out.append(kal + ".")
    return out


def ringkas(hasil_item, tema, dibuang, opsi, meta=None):
    meta = meta or {}
    n = len(hasil_item)
    kanal = Counter(i["kanal"] for i in hasil_item)
    sent = Counter(i["sentimen"] for i in hasil_item)
    bulan = Counter(i["bulan"] for i in hasil_item if i["bulan"])
    bulan_n = dict(sorted(bulan.items()))
    min_bulan = getattr(opsi, "min_bulan", 5)
    n_contoh = getattr(opsi, "contoh", 3)
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
        arah, tren_sel, indikatif = "data kurang", None, False
        bl = list(bulan_n)
        if len(bl) >= 2 and bulan_n[bl[-1]] >= min_bulan and bulan_n[bl[-2]] >= min_bulan:
            if tren[bl[-1]]["keluhan"] + tren[bl[-2]]["keluhan"] < 3:
                arah = "keluhan terlalu sedikit"
            else:
                a = tren[bl[-2]]["keluhan"] * 100.0 / bulan_n[bl[-2]]
                b_ = tren[bl[-1]]["keluhan"] * 100.0 / bulan_n[bl[-1]]
                tren_sel = round(b_ - a, 1)
                arah = "naik" if tren_sel >= 2 else "turun" if tren_sel <= -2 else "stabil"
                indikatif = n < 30 or bulan_n[bl[-1]] < 10 or bulan_n[bl[-2]] < 10
        contoh = sorted(k, key=lambda i: (i["bintang"] if i["bintang"] is not None else 3, len(i["teks"])))[:n_contoh]
        daftar.append({
            "id": t["id"], "label": t["label"], "dampak": t["dampak"],
            "masukan": len(rows), "keluhan": len(k), "pujian": len(p), "saran": len(s),
            "persen_keluhan": round(len(k) * 100.0 / n, 1) if n else 0.0,
            "kanal": sorted({i["kanal"] for i in k}),
            "rata_bintang_keluhan": round(sum(bintang_k) / len(bintang_k), 1) if bintang_k else None,
            "skor": len(k) * t["dampak"],
            "arah_tren": arah, "selisih_persen_poin": tren_sel, "tren_indikatif": indikatif, "tren_per_bulan": tren,
            "contoh_keluhan": [potong(i["teks"]) for i in contoh],
            "contoh_pujian": [potong(i["teks"]) for i in p][:n_contoh],
            "contoh_saran": [potong(i["teks"]) for i in s][:n_contoh],
        })
        if t["id"] == "keamanan" and k:
            daftar[-1]["rincian"] = rincian_keamanan(k)
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
    # tema yang menghitung keluhan yang sama (mis. tema kustom "bau_apek" + bawaan "bau_aroma") -> peringatan dobel
    peringatan = list(meta.get("peringatan", []))
    set_k = {t["id"]: {n_ for n_, i in enumerate(hasil_item) if "keluhan" in i["tema"].get(t["id"], [])} for t in tema}
    label = {t["id"]: t["label"] for t in tema}
    ids = [d["id"] for d in daftar if d["keluhan"] >= 2]
    for x in range(len(ids)):
        for y in range(x + 1, len(ids)):
            a_, b_ = set_k[ids[x]], set_k[ids[y]]
            if len(a_ & b_) >= 2 and len(a_ & b_) >= 0.8 * len(a_ | b_):
                peringatan.append("tema \"%s\" dan \"%s\" menghitung %d keluhan yang sama - kemungkinan dobel; hapus salah satu lewat "
                                  "\"hapus_tema\" di tema.json atau sebut sekali di laporan." % (label[ids[x]], label[ids[y]], len(a_ & b_)))
    tanpa = [i for i in hasil_item if not i["tema"]]
    daftar_baca = []
    for i in hasil_item:
        if i.get("nada_keluhan") is None:
            i["nada_keluhan"] = i.get("peran") != "saran" and nada_keluhan(i["teks"], i.get("bintang_setara", i.get("bintang")))
        alasan = perlu_dibaca(i)
        if alasan:
            daftar_baca.append({"teks": potong(i["teks"]), "alasan": alasan, "nada_keluhan": bool(i["nada_keluhan"]),
                                "tema": {k: v for k, v in i["tema"].items()}})
    # yang bernada keluhan ditaruh paling atas (dan selalu dicetak semua)
    daftar_baca.sort(key=lambda d: (not d["nada_keluhan"], d["alasan"] != "keluhan tanpa tabel"))
    # v1.0.7: token internal hasil FRASA ('semularagu', 'tanpaminus', 'sudahlama') tidak ditampilkan sebagai "kata teratas"
    internal = {g for pola, g in FRASA if isinstance(g, str) and re.fullmatch(r"[a-z]+", g) and not re.search(r"\b%s\b" % g, pola)}
    kata = Counter(w for i in tanpa for w in re.findall(r"[a-z]{4,}", normalkan(i["teks"]))
                   if w not in STOP and (w not in internal or w in i["teks"].lower()))
    sent_kanal = {}
    for i in hasil_item:
        sent_kanal.setdefault(i["kanal"], {"positif": 0, "netral": 0, "negatif": 0})[i["sentimen"]] += 1
    respons = {}
    for i in hasil_item:
        if i.get("dibalas") is None:
            continue
        r_ = respons.setdefault(i["kanal"], {"sumber": "chat WhatsApp" if i.get("sumber_balas") == "wa" else "kolom balasan penjual",
                                             "masukan": 0, "dibalas": 0, "keluhan": 0, "keluhan_tanpa_balasan": 0,
                                             "keluhan_dibalas_lambat": 0, "tanpa_balasan": 0, "contoh_tanpa_balasan": []})
        keluhan = any("keluhan" in v for v in i["tema"].values()) or bool(i.get("nada_keluhan"))
        r_["masukan"] += 1
        r_["dibalas"] += bool(i["dibalas"])
        if not i["dibalas"] and i.get("jeda_balas_menit") is None:
            r_["tanpa_balasan"] += 1
        if keluhan:
            r_["keluhan"] += 1
            if not i["dibalas"]:
                if i.get("jeda_balas_menit") is not None:
                    r_["keluhan_dibalas_lambat"] += 1
                else:
                    r_["keluhan_tanpa_balasan"] += 1
                    r_["contoh_tanpa_balasan"].append(potong(i["teks"], 90))
    nps = None
    nilai10 = [v for s_ in meta.get("sumber", []) for v in s_.get("nilai_baris", [])]
    if not nilai10 and not meta.get("sumber"):
        nilai10 = [i["nilai_0_10"] for i in hasil_item if i.get("nilai_0_10") is not None]
    if nilai10:
        pro = sum(1 for v in nilai10 if v >= 9)
        det = sum(1 for v in nilai10 if v <= 6)
        nps = {"responden": len(nilai10), "promotor_9_10": pro, "pasif_7_8": len(nilai10) - pro - det, "detraktor_0_6": det,
               "nps": round((pro - det) * 100.0 / len(nilai10), 1), "indikatif": len(nilai10) < 30}
    hasil_r = {
        "versi_script": VERSI, "total_masukan": n, "dibuang": dibuang,
        "sumber": [{k: v for k, v in s.items() if k in ("berkas", "kanal", "jenis", "kolom_teks", "kolom_nilai", "skala_nilai",
                                                          "kolom_tanggal", "baris", "responden", "catatan", "urutan_tanggal")} for s in meta.get("sumber", [])],
        "peringatan": peringatan,
        "per_kanal": dict(kanal.most_common()), "sentimen": {k: sent.get(k, 0) for k in ("positif", "netral", "negatif")},
        "sentimen_per_kanal": {k: sent_kanal[k] for k, _ in kanal.most_common()},
        "respons_staf": respons, "batas_balas_jam": getattr(opsi, "batas_balas_jam", 24),
        "koreksi": meta.get("koreksi", []),
        "nps": nps,
        "per_bulan": bulan_n,
        "tanpa_tanggal": sum(1 for i in hasil_item if not i["bulan"]),
        "data_kecil": n < 30,
        "tema": daftar,
        "belum_terklasifikasi": {"jumlah": len(tanpa), "persen": round(len(tanpa) * 100.0 / n, 1) if n else 0.0,
                                  "kata_teratas": [k for k, _ in kata.most_common(8)],
                                  "contoh": [potong(i["teks"]) for i in tanpa]},
        "perlu_dibaca": {"tidak_terklasifikasi": len(daftar_baca),
                         "tanpa_tema": sum(1 for d in daftar_baca if d["alasan"] == "tanpa tema"),
                         "keluhan_tanpa_tabel": sum(1 for d in daftar_baca if d["alasan"] == "keluhan tanpa tabel"),
                         "tema_tanpa_nada": sum(1 for d in daftar_baca if d["alasan"] == "tema tanpa nada"),
                         "bernada_keluhan": sum(1 for d in daftar_baca if d["nada_keluhan"]),
                         "daftar": daftar_baca},
    }
    hasil_r["ringkasan_siap_salin"] = kalimat_siap_salin(hasil_r)
    return hasil_r


def _fmt_tren(d):
    if d["selisih_persen_poin"] is None:
        return d["arah_tren"]
    s = "%s (%+.1f poin" % (d["arah_tren"], d["selisih_persen_poin"])
    return s + (", indikatif: data kecil)" if d.get("tren_indikatif") else ")")


def cetak_teks(r, opsi, maks_tanpa_tema=20):
    out = []
    n = r["total_masukan"]
    out.append("# Rekap Masukan Pelanggan (%d masukan)\n" % n)
    if r.get("peringatan"):
        out.append("PERINGATAN (baca dulu):")
        out += ["- " + p for p in r["peringatan"]]
        out.append("")
    for s in r.get("sumber", []):
        if s["jenis"] == "csv":
            out.append("Sumber %s (%s): CSV %d baris (%d berisi jawaban); kolom teks: %s; nilai: %s; tanggal: %s" % (
                s["berkas"], s["kanal"], s.get("baris", 0), s.get("responden", 0), ", ".join('"%s"' % k for k in s.get("kolom_teks", [])),
                ('"%s" (skala %s)' % (s["kolom_nilai"], s["skala_nilai"])) if s.get("kolom_nilai") else "-",
                (('"%s"' % s["kolom_tanggal"]) + (" (dibaca %s)" % s["urutan_tanggal"] if s.get("urutan_tanggal") else "")) if s.get("kolom_tanggal") else "-"))
        else:
            out.append("Sumber %s (%s): %s" % (s["berkas"], s["kanal"], "chat WhatsApp" if s["jenis"] == "whatsapp" else "teks tempelan"))
    out.append("Kanal: " + ", ".join("%s %d" % (k, v) for k, v in r["per_kanal"].items()))
    s = r["sentimen"]
    if n:
        out.append("Sentimen: positif %d (%.1f%%), netral %d (%.1f%%), negatif %d (%.1f%%)" % (
            s["positif"], s["positif"] * 100.0 / n, s["netral"], s["netral"] * 100.0 / n, s["negatif"], s["negatif"] * 100.0 / n))
    if len(r.get("sentimen_per_kanal", {})) > 1:
        out.append("Sentimen per kanal: " + "; ".join("%s: positif %d, netral %d, negatif %d" % (k, v["positif"], v["netral"], v["negatif"])
                                                      for k, v in r["sentimen_per_kanal"].items()))
    if r.get("nps"):
        x = r["nps"]
        out.append("Nilai 0-10 (NPS): %d responden - promotor %d, pasif %d, detraktor %d -> NPS %+.1f%s" % (
            x["responden"], x["promotor_9_10"], x["pasif_7_8"], x["detraktor_0_6"], x["nps"], " (indikatif, < 30 responden)" if x["indikatif"] else ""))
    if r["per_bulan"]:
        out.append("Per bulan: " + ", ".join("%s: %d" % kv for kv in r["per_bulan"].items())
                   + ("; %d tanpa tanggal" % r["tanpa_tanggal"] if r["tanpa_tanggal"] else ""))
    if r["dibuang"]:
        out.append("Tidak dihitung: " + ", ".join("%s %d" % kv for kv in r["dibuang"].items()))
    if r.get("data_kecil"):
        out.append("Data < 30 masukan: pakai sebagai arah saja, bukan persentase pasti.")
    if r.get("koreksi"):
        out.append("Koreksi agent diterapkan (--koreksi): %d baris, %d masukan - angka di bawah SUDAH termasuk koreksi ini." % (
            len(r["koreksi"]), sum(k["masukan"] for k in r["koreksi"])))
        out += ["- \"%s\" -> tema %s, %s%s%s" % (k["cuplikan"], k["tema"] or "-", k["jenis"], (", sentimen " + k["sentimen"]) if k["sentimen"] else "",
                                             (" (%s)" % k["catatan"]) if k["catatan"] else "") for k in r["koreksi"]]
    out.append("\n## Kalimat ringkasan siap salin (angka sudah dihitung script - SALIN apa adanya, jangan hitung/tulis ulang)\n")
    out += ["- " + k for k in r.get("ringkasan_siap_salin", [])]
    jenis_wa = [s_ for s_ in r.get("sumber", []) if s_["jenis"] == "whatsapp"]
    if r.get("respons_staf"):
        out.append("\n## Respons staf / penjual\n")
        for k, v in r["respons_staf"].items():
            out.append("- %s (%s): %d dari %d masukan dibalas%s; keluhan TANPA balasan: %d dari %d%s" % (
                k, v["sumber"], v["dibalas"], v["masukan"], (" <= %d jam" % r.get("batas_balas_jam", 24)) if v["sumber"] == "chat WhatsApp" else "",
                v["keluhan_tanpa_balasan"], v["keluhan"],
                (", dibalas > %d jam: %d" % (r.get("batas_balas_jam", 24), v["keluhan_dibalas_lambat"])) if v["keluhan_dibalas_lambat"] else ""))
            out += ["  - belum dibalas: \"%s\"" % c for c in v["contoh_tanpa_balasan"][:10]]
    if any(s_["kanal"] not in r.get("respons_staf", {}) for s_ in jenis_wa):
        out.append("\nRespons admin WhatsApp belum dihitung: jalankan dengan --staf \"Nama Admin\" (lihat --daftar-pengirim).")
    out.append("\n## Isu teratas (skor = jumlah keluhan x dampak 1-5) - KANDIDAT, verifikasi tiap tema\n")
    out.append("| # | Tema | Keluhan (% dari semua) | Pujian | Saran | Dampak | Skor | Tren | Kanal | Prioritas |")
    out.append("|---|---|---|---|---|---|---|---|---|---|")
    for i, d in enumerate([d for d in r["tema"] if d["keluhan"]], 1):
        out.append("| %d | %s | %d (%.1f%%) | %d | %d | %d | %d | %s | %s | %s |" % (
            i, d["label"], d["keluhan"], d["persen_keluhan"], d["pujian"], d["saran"], d["dampak"], d["skor"], _fmt_tren(d),
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
    pd = r.get("perlu_dibaca") or {"tidak_terklasifikasi": 0, "tanpa_tema": 0, "keluhan_tanpa_tabel": 0, "bernada_keluhan": 0, "daftar": []}
    out.append("\n## Perlu dibaca agent\n")
    ttn = pd.get("tema_tanpa_nada", 0)
    out.append("Tidak terklasifikasi: %d masukan (%d tanpa tema + %d bernada keluhan tetapi tidak masuk tabel keluhan%s). "
               "Di antaranya %d bernada keluhan - WAJIB dibaca & dimasukkan ke tema yang tepat (lewat tema.json atau koreksi bertanda)." % (
                   pd["tidak_terklasifikasi"], pd["tanpa_tema"], pd["keluhan_tanpa_tabel"],
                   (" + %d bertema tetapi nadanya belum terbaca" % ttn) if ttn else "", pd["bernada_keluhan"]))
    out.append("Tanpa tema terdeteksi: %d (%.1f%%). Kata teratas: %s" % (b["jumlah"], b["persen"], ", ".join(b["kata_teratas"]) or "-"))
    keluhan = [d for d in pd["daftar"] if d["nada_keluhan"]]
    lain = [d for d in pd["daftar"] if not d["nada_keluhan"]]
    if keluhan:
        out.append("\nBernada keluhan (semua ditampilkan):")
        for d in keluhan:
            ket = "tanpa tema" if d["alasan"] == "tanpa tema" else "tema: " + ", ".join(
                "%s (%s)" % (k, "/".join(v)) for k, v in sorted(d["tema"].items()))
            out.append("- [KELUHAN? %s] \"%s\"" % (ket, d["teks"]))
    if lain:
        out.append("\nTanpa tema / bertema tanpa nada (netral) - bisa keluhan tersirat, baca:")
        out += ["- %s\"%s\"" % ("[tema: %s] " % ", ".join(sorted(d["tema"])) if d["tema"] else "", d["teks"]) for d in lain[:maks_tanpa_tema]]
        if len(lain) > maks_tanpa_tema:
            out.append("- ... +%d lainnya: lihat --format json atau CSV --simpan-anonim (kolom perlu_dibaca)" % (len(lain) - maks_tanpa_tema))
    out.append("\nCatatan: hasil ini SARINGAN PERTAMA dari kata kunci. Baca kutipan tiap tema & koreksi lewat tema.json. "
               "Nama, nomor HP, dll. sudah disamarkan otomatis (tidak sempurna - baca ulang).")
    return "\n".join(out)


def muat_tema(path):
    try:
        with open(path, "rb") as f:
            teks, _ = dekode(f.read(), os.path.basename(path))
    except FileNotFoundError:
        raise Gagal("berkas tema tidak ditemukan: %s" % path)
    except OSError as e:
        raise Gagal("berkas tema %s tidak bisa dibuka (%s)." % (path, e.strerror or e))
    try:
        return json.loads(teks)
    except ValueError as e:
        raise Gagal("berkas tema %s bukan JSON yang valid (%s). Bandingkan dengan templates/tema-contoh.json "
                    "(tanda kutip ganda, koma antar-item, kurung tutup)." % (path, e))


def main(argv=None):
    ap = argparse.ArgumentParser(description="Olah masukan pelanggan multi-kanal (anonim, tema, sentimen, tren).")
    ap.add_argument("sumber", nargs="+", help="berkas atau berkas=NamaKanal (.txt chat WhatsApp / tempelan, .csv). '-' = stdin")
    ap.add_argument("--staf", default="", help="Nama pengirim WhatsApp yang dianggap staf/pemilik (dipisah koma); pesannya dilewati")
    ap.add_argument("--daftar-pengirim", action="store_true", help="Tampilkan pengirim chat WhatsApp + jumlah pesan, lalu berhenti")
    ap.add_argument("--kolom-teks", help="Nama kolom teks CSV (boleh beberapa, pisah koma)")
    ap.add_argument("--kolom-bintang", help="Nama kolom nilai/bintang CSV")
    ap.add_argument("--kolom-tanggal", help="Nama kolom tanggal CSV")
    ap.add_argument("--urutan-tanggal", choices=["hari-bulan", "bulan-hari"],
                    help="Paksa urutan tanggal angka: hari-bulan (Indonesia, 15/08/2026) atau bulan-hari (AS/Google Form, 8/15/2026)")
    ap.add_argument("--skala", choices=["5", "10"], help="Paksa skala kolom nilai: 5 (bintang 1-5) atau 10 (nilai 0-10/NPS)")
    ap.add_argument("--buang-teks-sama", action="store_true",
                    help="Buang teks yang sama persis per kanal walau dari pembeli berbeda (bawaan: hanya baris identik yang dibuang)")
    ap.add_argument("--tema", help="File JSON tema/kata tambahan (lihat templates/tema-*.json)")
    ap.add_argument("--contoh", type=int, default=3)
    ap.add_argument("--min-bulan", type=int, default=5, help="Minimal masukan per bulan agar tren dihitung (default 5)")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    ap.add_argument("--koreksi", help="CSV koreksi agent (cuplikan,tema,jenis,sentimen,catatan) - lihat templates/koreksi-contoh.csv")
    ap.add_argument("--batas-balas-jam", type=float, default=24, help="Batas jam agar pesan WA dianggap dibalas staf (default 24)")
    ap.add_argument("--simpan-anonim", help="Simpan data yang SUDAH disamarkan ke CSV ini (kanal,bulan,bintang,nilai_0_10,sentimen,tema,teks,keluhan_tema,perlu_dibaca)")
    opsi = ap.parse_args(argv)
    opsi.staf_list = [s.strip() for s in opsi.staf.split(",") if s.strip()]
    opsi.urutan_tanggal = {"hari-bulan": "hb", "bulan-hari": "bh"}.get(opsi.urutan_tanggal)
    try:
        konfigurasi = muat_tema(opsi.tema) if opsi.tema else None
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
        hasil_item, tema, dibuang, meta = olah(opsi.sumber, opsi, konfigurasi)
        if not hasil_item:
            raise Gagal("tidak ada masukan yang bisa dibaca (berkas kosong atau semua baris terlalu pendek). Periksa format berkas / "
                        "kolom teks, lalu ekspor ulang.")
        r = ringkas(hasil_item, tema, dibuang, opsi, meta)
        if opsi.simpan_anonim:
            try:
                with open(opsi.simpan_anonim, "w", encoding="utf-8", newline="") as f:
                    w = csv.writer(f)
                    w.writerow(["kanal", "bulan", "bintang", "nilai_0_10", "sentimen", "tema", "teks", "keluhan_tema", "perlu_dibaca",
                                "dibalas", "koreksi"])
                    for i in hasil_item:
                        n10 = i.get("nilai_0_10")
                        w.writerow([i["kanal"], i["bulan"] or "", i["bintang"] or "",
                                    "" if n10 is None else ("%g" % n10), i["sentimen"], ";".join(sorted(i["tema"])), i["teks"],
                                    ";".join(sorted(k for k, v in i["tema"].items() if "keluhan" in v)), perlu_dibaca(i) or "",
                                    {True: "ya", False: "tidak"}.get(i.get("dibalas"), ""), i.get("koreksi", "")])
            except OSError as e:
                raise Gagal("tidak bisa menulis %s (%s)." % (opsi.simpan_anonim, e.strerror or e))
    except Gagal as e:
        print("GAGAL: %s" % e, file=sys.stderr)
        return 2
    except (UnicodeError, csv.Error, ValueError) as e:
        print("GAGAL: berkas tidak bisa diproses (%s: %s). Ekspor ulang sebagai .txt/.csv UTF-8, atau pakai fallback manual di SKILL.md."
              % (type(e).__name__, e), file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=2) if opsi.format == "json" else cetak_teks(r, opsi))
    return 0


if __name__ == "__main__":
    sys.exit(main())
