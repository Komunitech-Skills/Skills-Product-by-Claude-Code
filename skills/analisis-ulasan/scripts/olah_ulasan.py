#!/usr/bin/env python3
"""Olah puluhan/ratusan ulasan pelanggan menjadi statistik & kandidat tema (bahasa Indonesia).

Yang dilakukan script (deterministik, bisa diulang):
- Membaca CSV ekspor (kolom ulasan/bintang/produk/tanggal dideteksi otomatis) ATAU teks tempelan.
- Menghitung sebaran bintang, rata-rata, persen positif/netral/negatif.
- Menormalkan bahasa gaul & singkatan ("brg", "bgt", "gk", "mantul", "ga sesuai", huruf berulang).
- Menandai KANDIDAT tema keluhan & pujian per klausa (kalimat dipecah di "tapi", titik, dll.),
  lengkap dengan jumlah ulasan, sebaran bintang, skor prioritas, dan contoh kutipan singkat.
- Menyamarkan nomor HP, email, @username, nomor pesanan/resi, dan sapaan+nama di kutipan.
- Kolom nama/username pembeli TIDAK pernah dikeluarkan.

Klasifikasi akhir tetap dilakukan agent/manusia dengan membaca bukti kutipan.
Hanya library standar Python 3.8+. Tidak ada akses jaringan.

Contoh:
  python3 olah_ulasan.py ulasan.csv
  python3 olah_ulasan.py ulasan.txt --format teks
  python3 olah_ulasan.py ulasan.csv --kolom-ulasan "Komentar" --kolom-bintang "Rating"
  python3 olah_ulasan.py ulasan.csv --detail-tema k_pengiriman
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

VERSI = "1.0.4"

# --------------------------------------------------------------------------- kamus
# Frasa diganti SEBELUM normalisasi per kata (urutan penting).
FRASA = [
    (r"\bfast\s*(?:respon|respond|response|resp|res)\w*", "respons cepat"),
    (r"\bslow\s*(?:respon|respond|response|resp|res)\w*", "respons lambat"),
    (r"\bgerak\s*cepat\b|\bgercep\b", "cepat tanggap"),
    (r"\breal\s*pic\w*", "sesuai foto"),
    (r"\bworth\s*it\w*|\bworthit\w*", "sepadan"),
    (r"\bnot\s*worth\w*", "tidak sepadan"),
    (r"\bbubble\s*wrap\w*|\bbubblewrap\w*|\bbuble\s*wrap\w*", "bubblewrap"),
    (r"\bmurmer\b|\bmurah\s*meriah\b", "murah"),
    (r"\bsize\s*chart\w*", "tabel ukuran"),
    (r"\brepeat\s*order\w*|\bro\b", "order lagi"),
    (r"\bthank\s*you\s*card\b|\bkartu\s*ucapan\b", "bonus kartu"),
    (r"\bno\s*minus\b|\btanpa\s*minus\b", "tidak ada minus"),
    (r"\bke\s*-?\s*[2-9]\s*(?:x|kali)\w*|\bkesekian\s*kali\w*|\byang\s*ke\s*-?\s*[2-9]\b", "order lagi"),
    (r"\bgood\s*quality\b|\bhigh\s*quality\b", "kualitas bagus"),
    (r"\bbad\s*quality\b|\blow\s*quality\b", "kualitas jelek"),
    (r"\bfast\s*(?:delivery|shipping)\b", "pengiriman cepat"),
    (r"\bslow\s*(?:delivery|shipping)\b", "pengiriman lambat"),
    (r"\b(?:will|would)\s*(?:buy|order)\s*(?:again|more)\b|\bbuy\s*again\b|\border\s*again\b", "order lagi"),
    (r"\bnot\s*as\s*described\b|\bnot\s*as\s*(?:pictured|expected)\b", "tidak sesuai"),
    (r"\bexp(?:ired|ire)?\b|\bkadaluarsa\b|\bkadaluwarsa\b|\bkedaluarsa\b|\bdaluwarsa\b", "kedaluwarsa"),
]

SLANG = {
    # kata umum
    "brg": "barang", "brng": "barang", "barangnya": "barang", "brgnya": "barang",
    "bgt": "banget", "bngt": "banget", "bgtt": "banget", "bangett": "banget", "bet": "banget",
    "gk": "tidak", "ga": "tidak", "gak": "tidak", "nggak": "tidak", "ngga": "tidak", "enggak": "tidak",
    "engga": "tidak", "tdk": "tidak", "tak": "tidak", "kagak": "tidak", "ndak": "tidak",
    "gag": "tidak", "gada": "tidak ada", "gaada": "tidak ada", "ngak": "tidak", "nda": "tidak",
    "blm": "belum", "blum": "belum", "krg": "kurang", "krng": "kurang",
    "yg": "yang", "dg": "dengan", "dgn": "dengan", "sm": "sama", "sma": "sama",
    "sdh": "sudah", "udh": "sudah", "udah": "sudah", "dah": "sudah", "sudh": "sudah",
    "krn": "karena", "karna": "karena", "tp": "tapi", "tpi": "tapi", "tapii": "tapi",
    "jg": "juga", "aja": "saja", "aj": "saja", "bs": "bisa", "bsa": "bisa", "lg": "lagi", "lgi": "lagi",
    "sy": "saya", "sya": "saya", "aku": "saya", "gw": "saya", "gue": "saya",
    "pdhl": "padahal", "bnr": "benar", "bener": "benar", "emg": "memang", "emang": "memang",
    "utk": "untuk", "u/": "untuk", "trs": "terus", "trus": "terus", "dr": "dari", "dri": "dari",
    "jd": "jadi", "jdi": "jadi", "skrg": "sekarang", "kl": "kalau", "klo": "kalau", "kalo": "kalau",
    "bnyk": "banyak", "byk": "banyak", "sgt": "sangat", "bkn": "bukan", "msh": "masih", "masi": "masih",
    "dtg": "datang", "nyampe": "sampai", "nyampai": "sampai", "nympe": "sampai", "smp": "sampai",
    "sampe": "sampai", "nyampenya": "sampai", "sampainya": "sampai", "datangnya": "datang",
    # penilaian
    "bgs": "bagus", "bagu": "bagus", "baguss": "bagus", "mantul": "mantap", "mantab": "mantap",
    "mantep": "mantap", "mantaps": "mantap", "mntp": "mantap", "mantapp": "mantap", "mantav": "mantap",
    "joss": "mantap", "jos": "mantap", "josss": "mantap", "top": "mantap", "topp": "mantap",
    "rekomen": "rekomendasi", "rekomended": "rekomendasi", "recomended": "rekomendasi",
    "recommended": "rekomendasi", "recommend": "rekomendasi", "recomend": "rekomendasi",
    "rekom": "rekomendasi", "recommended!": "rekomendasi",
    "jlk": "jelek", "jlek": "jelek", "jelekk": "jelek", "ancur": "hancur", "rsk": "rusak",
    "cpt": "cepat", "cepet": "cepat", "cpet": "cepat", "kilat": "cepat", "express": "cepat",
    "lmbt": "lambat", "lelet": "lambat", "lemot": "lambat", "lamaa": "lama", "lamaaa": "lama",
    "ok": "oke", "okey": "oke", "okay": "oke", "okeh": "oke", "oce": "oke", "sip": "oke", "sipp": "oke",
    "enk": "enak", "uenak": "enak", "enaak": "enak", "endul": "enak", "enakk": "enak", "maknyus": "enak",
    "krispi": "renyah", "crispy": "renyah", "kriuk": "renyah", "garing": "renyah",
    "murmer": "murah", "mura": "murah", "murahh": "murah",
    "ori": "asli", "original": "asli", "orii": "asli", "kw": "palsu", "fake": "palsu",
    "rapih": "rapi", "rpi": "rapi",
    # obyek
    "packing": "kemasan", "packingnya": "kemasan", "paking": "kemasan", "pakingnya": "kemasan",
    "pengemasan": "kemasan", "pengemasannya": "kemasan", "packaging": "kemasan", "kemasannya": "kemasan",
    "bungkus": "kemasan", "bungkusnya": "kemasan", "bungkusan": "kemasan", "dus": "kardus", "dusnya": "kardus",
    "pack": "kemasan", "packingan": "kemasan",
    "respon": "respons", "respond": "respons", "response": "respons", "responnya": "respons",
    "responsnya": "respons", "balesnya": "balas", "bales": "balas", "dibales": "dibalas",
    "seller": "penjual", "sellernya": "penjual", "penjualnya": "penjual", "adminnya": "admin", "min": "admin",
    "cs": "admin", "csnya": "admin", "tokonya": "toko", "olshop": "toko",
    "size": "ukuran", "sizenya": "ukuran", "ukurannya": "ukuran", "uk": "ukuran", "sizes": "ukuran",
    "kegedean": "kebesaran", "kegedeaan": "kebesaran", "kekecilan": "kekecilan",
    "kirimnya": "kirim", "pengirimannya": "pengiriman", "pengirimanya": "pengiriman", "ngirim": "kirim",
    "ngirimnya": "kirim", "dikirimnya": "dikirim", "kurirnya": "kurir", "ekspedisinya": "ekspedisi",
    "paketnya": "paket", "pesenan": "pesanan", "pesananya": "pesanan", "pesanannya": "pesanan",
    "orderan": "pesanan", "pesen": "pesan", "order": "order", "ordernya": "order",
    "fotonya": "foto", "gambarnya": "gambar", "pic": "foto", "pict": "foto", "picture": "foto",
    "deskripsinya": "deskripsi", "desc": "deskripsi", "deskrip": "deskripsi",
    "kualitasnya": "kualitas", "quality": "kualitas", "qualitynya": "kualitas", "kwalitas": "kualitas",
    "bahannya": "bahan", "jahitannya": "jahitan", "warnanya": "warna", "rasanya": "rasa", "baunya": "bau",
    "harganya": "harga", "price": "harga", "hrg": "harga", "hrga": "harga",
    "bonusnya": "bonus", "free": "bonus", "fre": "bonus", "gift": "bonus", "hadiahnya": "hadiah",
    "refund": "refund", "return": "retur", "returnya": "retur", "komplen": "komplain", "complain": "komplain",
    "komplennya": "komplain", "garansinya": "garansi",
    "expired": "kedaluwarsa", "ed": "kedaluwarsa",
    "bocor": "bocor", "tumpah": "tumpah", "sobek": "sobek", "robek": "sobek",
    # tambahan (tempat makan, jasa, bahasa Inggris dasar)
    "tebel": "tebal", "tebell": "tebal", "ketagihan": "nagih", "nagihh": "nagih", "dateng": "datang", "dtng": "datang",
    "nunggu": "tunggu", "nungguin": "tunggu", "nunggunya": "tunggu", "menunggunya": "menunggu", "ngantri": "antri",
    "ngantre": "antri", "antrinya": "antri", "antriannya": "antrian",
    "pelayanannya": "pelayanan", "pelayanan2": "pelayanan", "servis": "pelayanan", "service": "pelayanan",
    "servicenya": "pelayanan", "tempatnya": "tempat", "suasananya": "suasana", "parkirannya": "parkir",
    "parkiran": "parkir", "parkirnya": "parkir", "toiletnya": "toilet", "wc": "toilet", "wcnya": "toilet",
    "musholanya": "mushola", "wifinya": "wifi", "acnya": "ac", "makanannya": "makanan", "minumannya": "minuman",
    "masakannya": "makanan", "menunya": "menu", "stafnya": "staf", "karyawannya": "staf", "pegawainya": "staf",
    "waiter": "staf", "waitress": "staf", "pelayannya": "staf", "mbaknya": "staf", "masnya": "staf",
    "nice": "bagus", "good": "bagus", "great": "bagus", "bad": "jelek", "slow": "lambat", "late": "telat",
    "broken": "rusak", "damaged": "rusak", "cheap": "murah", "expensive": "mahal", "delicious": "enak",
    "yummy": "enak", "tasty": "enak", "clean": "bersih", "dirty": "kotor", "friendly": "ramah", "fast": "cepat",
    "fragrant": "wangi", "cozy": "cozy", "comfy": "nyaman", "comfortable": "nyaman", "recomend": "rekomendasi",
}

INTENSIFIER = r"(?:terlalu|begitu|sangat|gitu|sama\s+sekali|pernah)"

# Setiap tema: id, label, jenis (keluhan/pujian), pihak (siapa yang bisa memperbaiki), daftar regex.
# Regex dijalankan pada teks klausa yang SUDAH dinormalisasi (huruf kecil, slang diganti,
# negasi digabung: "tidak sesuai" -> "tidak_sesuai", "tidak ada yang rusak" -> "tidak_ada_rusak").
DEKAT = r"\W+(?:\w+\W+){0,3}"  # jarak maks. 3 kata
DEKAT2 = r"\W+(?:\w+\W+){0,2}"  # jarak maks. 2 kata
TEMA = [
    # ---------------------------------------------------------------- keluhan
    {"id": "k_tidak_sesuai", "label": "Barang tidak sesuai deskripsi/foto", "jenis": "keluhan",
     "pihak": "produk & listing", "pola": [
         r"\btidak_sesuai\b(?!" + r"\W+(?:tabel\s+)?ukuran)", r"\bkurang_sesuai\b", r"\btidak_seperti\b",
         r"\bbeda\w*\W+(?:\w+\W+){0,2}(?:foto|gambar|deskripsi|iklan|video|etalase)",
         r"\b(?:foto|gambar)\w*\W+(?:\w+\W+){0,2}beda\b", r"\bzonk\b",
         r"\b(?:tertipu|penipuan|nipu|menipu|penipu|ketipu)\b"]},
    {"id": "k_kualitas", "label": "Kualitas buruk / cacat / cepat rusak", "jenis": "keluhan",
     "pihak": "produk", "pola": [
         r"(?<!_)\b(?:cacat|rusak|sobek|bolong|pecah|penyok|lecet|patah|luntur|retak|berjamur|jamuran|karatan|karat|hancur|remuk)\b",
         r"\bjahitan\w*" + DEKAT + r"(?:lepas|jelek|berantakan|tidak_rapi|kurang_rapi|keluar)",
         r"(?<!_)\b(?:jelek|buruk|murahan|ringkih|rapuh|abal)\b", r"\bbahan\w*" + DEKAT + r"tipis\b",
         r"\btidak_(?:awet|nyala|berfungsi|bisa_dipakai|jalan|hidup|kuat)\b", r"\bcepat\W+rusak\b",
         r"(?<!_)\bmati\b", r"(?<!_)\bpalsu\b", r"\b(?:tidak|bukan)_asli\b",
         r"\bkualitas\w*" + DEKAT + r"(?:jelek|buruk|kurang|menurun|turun|rendah|biasa)",
         r"\b(?:tidak|kurang)_bagus\b", r"\bkurang_berkualitas\b", r"\bkurang_(?:rapi|halus|kokoh|tebal|awet)\b"]},
    {"id": "k_ukuran", "label": "Ukuran tidak pas / info ukuran kurang jelas", "jenis": "keluhan",
     "pihak": "produk & listing", "pola": [
         r"\b(?:kekecilan|kebesaran|kesempitan|kepanjangan|kependekan|kelonggaran|kegedean)\b",
         r"\bterlalu\W+(?:kecil|besar|pendek|panjang|sempit|longgar|ketat)\b",
         r"\bukuran\w*" + DEKAT + r"(?:tidak_sesuai|beda|salah|kecil|besar|kurang_pas|tidak_pas|melenceng|kurang_sesuai)",
         r"\b(?:tidak|kurang)_pas\b", r"\btidak_sesuai\W+(?:tabel\s+)?ukuran"]},
    {"id": "k_pengiriman", "label": "Pengiriman/proses kirim lambat", "jenis": "keluhan",
     "pihak": "proses kirim & kurir", "pola": [
         r"\b(?:pengiriman|kirim|dikirim|sampai|datang|paket|proses|diproses|kurir|ekspedisi)\w*" + DEKAT +
         r"(?:lama|lambat|telat|terlambat|molor|berhari|seminggu|lemot)\b",
         r"\b(?:lama|lambat|telat|terlambat|molor)\w*" + DEKAT +
         r"(?:sampai|datang|dikirim|kirim|pengiriman|diproses|proses|pengemasan)\b",
         r"\bbelum_(?:sampai|datang|dikirim|diterima|dikemas|diproses)\b", r"\btidak_dikirim(?:_\w+)?\b",
         r"\btunggu\w*" + DEKAT + r"(?:seminggu|berhari|hari)\b"]},
    {"id": "k_kemasan", "label": "Kemasan kurang aman / rusak / bocor", "jenis": "keluhan",
     "pihak": "packing (gudang)", "pola": [
         r"\b(?:kemasan|kardus|plastik|segel)\w*" + DEKAT +
         r"(?:rusak|penyok|sobek|jelek|seadanya|asal|kurang_aman|tidak_aman|tipis|basah|bocor|terbuka|kurang_rapi|tidak_rapi|hancur|lecek|kurang_tebal)",
         r"(?<!_)\b(?:bocor|tumpah|rembes|merembes)\b", r"\btidak_(?:pakai|dikasih|ada|diberi)[ _]bubblewrap\b",
         r"\btanpa\W+(?:bubblewrap|kardus|dus)\b", r"\bsegel\w*" + DEKAT + r"(?:terbuka|rusak|sobek)",
         r"\btidak_(?:disegel|bersegel)\b"]},
    {"id": "k_salah_kirim", "label": "Salah kirim / barang kurang / varian keliru", "jenis": "keluhan",
     "pihak": "packing (gudang)", "pola": [
         r"\bsalah\W+(?:kirim|warna|ukuran|varian|barang|produk|model|tipe|motif|rasa|pesanan)\b",
         r"\bdikirim\w*" + DEKAT + r"(?:salah|beda|lain)\b",
         r"\bwarna\w*" + DEKAT + r"(?:beda|tidak_sesuai|salah|lain)\b(?!.*\b(?:foto|gambar|deskripsi|iklan)\b)",
         r"\btidak_lengkap\b", r"\bkurang_(?:satu|1|2|dua|tiga|3|lengkap|jumlah|isi)\b",
         r"\b(?:isi|jumlah)\w*" + DEKAT + r"(?:kurang|tidak_sesuai|beda)\b", r"\bhilang\b"]},
    {"id": "k_respons", "label": "Respons penjual/CS lambat atau kurang ramah", "jenis": "keluhan",
     "pihak": "layanan (admin/CS)", "pola": [
         r"\brespons\W+(?:lambat|lama|lemot)", r"\b(?:lambat|lama)\W+(?:respons|dibalas|balas)\b",
         r"\b(?:chat|dm|inbox|pesan(?!an)|pesen(?!an))\w*" + DEKAT + r"(?:tidak_dibalas|tidak_direspons|lama|dicuekin|diabaikan|tidak_ditanggapi)",
         r"\btidak_(?:dibalas|direspons|ditanggapi|responsif|ramah|sopan|membantu)\b", r"\btidak_ada_respons\b",
         r"\b(?:jutek|judes|ketus|kasar|cuek|galak|sombong)\b", r"\bkurang_(?:ramah|responsif|sopan)\b"]},
    {"id": "k_harga", "label": "Harga terasa mahal / tidak sepadan", "jenis": "keluhan",
     "pihak": "harga & nilai", "pola": [
         r"(?<!_)\b(?:mahal|kemahalan|overprice\w*)\b", r"\btidak_(?:sepadan|sebanding|worth|murah)\b",
         r"\bharga\w*" + DEKAT + r"(?:tidak_sesuai|tidak_sebanding|naik)\b", r"\brugi\b"]},
    {"id": "k_rasa", "label": "Rasa kurang enak / tidak konsisten", "jenis": "keluhan",
     "pihak": "produk", "pola": [
         r"\b(?:hambar|keasinan|kemanisan|kepedasan|keasaman|basi|anyep|tengik)\b",
         r"\bterlalu\W+(?:asin|manis|pedas|pahit|asam|keras|lembek|berminyak|kering)\b",
         r"\b(?:tidak|kurang)_(?:enak|gurih|renyah|segar|fresh|nikmat|lezat)\b",
         r"\brasa\w*" + DEKAT + r"(?:aneh|beda|berubah|hambar|pahit|tidak_sama|kurang|tidak_enak)",
         r"\b(?:alot|melempem|keras\W+banget)\b"]},
    {"id": "k_bau", "label": "Bau tidak sedap", "jenis": "keluhan",
     "pihak": "produk & penyimpanan", "pola": [
         r"(?<!_)\bbau\b(?!\W+(?:wangi|harum|enak|segar))", r"\b(?:menyengat|busuk|pesing)\b",
         r"\bbau\w*" + DEKAT + r"(?:apek|menyengat|aneh|busuk|kimia|lem|plastik|tidak_sedap)"]},
    {"id": "k_kedaluwarsa", "label": "Kedaluwarsa / tanggal expired dekat", "jenis": "keluhan",
     "pihak": "stok & penyimpanan", "pola": [r"\bkedaluwarsa\b", r"\bbasi\b"]},
    {"id": "k_retur", "label": "Komplain/retur/garansi dipersulit", "jenis": "keluhan",
     "pihak": "layanan (admin/CS)", "pola": [
         r"\b(?:retur|refund|pengembalian|garansi|komplain|klaim|tukar)\w*" + DEKAT +
         r"(?:susah|sulit|ribet|ditolak|lama|tidak_ditanggapi|dipersulit|tidak_diproses|tidak_bisa|tidak_dilayani|tidak_direspons)"]},
    {"id": "k_waktu_tunggu", "label": "Waktu tunggu/penyajian lama (tempat makan & jasa)", "jenis": "keluhan",
     "pihak": "layanan (dapur/kasir/staf)", "pola": [
         r"\b(?:pelayanan|layanan|penyajian|disajikan|dilayani|antri|antre|antrian|antrean|tunggu|menunggu|kasir|order|makanan|minuman)\w*" + DEKAT +
         r"(?:lama|lambat|lelet|telat|panjang|menit|jam)\b",
         r"\b(?:lama|lambat)\W+(?:\w+\W+)?(?:dilayani|disajikan|keluar|datangnya|nunggu|tunggu|menunggu)\b",
         r"\bantri\w*\W+(?:\w+\W+)?(?:panjang|lama|mengular)\b"]},
    {"id": "k_kebersihan", "label": "Kebersihan / benda asing (keamanan pangan)", "jenis": "keluhan",
     "pihak": "kebersihan & keamanan pangan", "pola": [
         r"(?<!_)\b(?:kotor|jorok|kumuh|berdebu|lengket|dekil|jijik)\b", r"\b(?:tidak|kurang)_(?:bersih|higienis|steril)\b",
         r"\b(?:ada|nemu|menemukan|ketemu|terdapat|dapat|dapet|isi)\W+(?:\w+\W+){0,3}(?:rambut|serangga|lalat|kecoa|semut|ulat|belatung|kutu|plastik|staples|kerikil|benda\W+asing)\b",
         r"\b(?:rambut|serangga|lalat|kecoa|belatung|ulat|benda\W+asing)\W+(?:\w+\W+){0,2}(?:di|dalam|dalem)\W+(?:\w+\W+){0,1}(?:makanan|minuman|nasi|kue|pastry|roti|mie|mi|sup|kuah|piring|gelas|produk|paket|kemasan)\b",
         r"\b(?:banyak|ada)\W+(?:lalat|kecoa|tikus|nyamuk)\b"]},
    {"id": "k_fasilitas", "label": "Fasilitas kurang (parkir, toilet, AC, wifi, tempat)", "jenis": "keluhan",
     "pihak": "fasilitas tempat", "pola": [
         r"\b(?:parkir|toilet|mushola|musala|ac|wifi|colokan|kursi|meja|tempat)\w*" + DEKAT +
         r"(?:sempit|susah|sulit|penuh|tidak_ada|mahal|kotor|bau|rusak|mati|panas|lemot|lambat|tidak_dingin|kurang|sedikit|terbatas|sesak)\b",
         r"\b(?:gerah|pengap|panas\W+banget|berisik|bising)\b", r"\btidak_ada_(?:parkir|toilet|mushola|musala|wifi|ac|colokan)\b"]},
    # ---------------------------------------------------------------- pujian
    {"id": "p_sesuai", "label": "Sesuai deskripsi/foto", "jenis": "pujian",
     "pihak": "produk & listing", "pola": [
         r"(?<!_)\bsesuai\b(?!\W+(?:tabel\s+)?ukuran)", r"\bpersis\b", r"(?<!beda )\bsama\W+(?:(?:dengan|di|kayak|kaya|seperti|persis)\W+)?(?:foto|gambar|deskripsi)\b",
         r"\bseperti\W+(?:di\W+)?(?:foto|gambar)\b", r"\btidak_ada_(?:beda|perbedaan)\b"]},
    {"id": "p_kualitas", "label": "Kualitas bagus / awet", "jenis": "pujian",
     "pihak": "produk", "pola": [
         r"(?<!_)\b(?:bagus|berkualitas|awet|kokoh|kuat|tebal|adem|lembut|halus|premium|solid|elegan|cantik|kece|kinclong|terang|jernih)\b",
         r"\bkualitas\w*" + DEKAT + r"(?:oke|mantap|premium|bagus|baik|juara|terbaik|tinggi)",
         r"\bjahitan\w*" + DEKAT + r"(?:rapi|kuat|bagus|halus)", r"(?<!_)\basli\b",
         r"\btidak_ada_(?:cacat|minus|kerusakan|rusak|lecet)\b", r"\bberfungsi\W+(?:baik|normal|dengan\W+baik)\b",
         r"\bnyala\b", r"\bjalan\W+normal\b"]},
    {"id": "p_pengiriman", "label": "Pengiriman/proses cepat", "jenis": "pujian",
     "pihak": "proses kirim & kurir", "pola": [
         r"\b(?:pengiriman|kirim|dikirim|sampai|datang|paket|proses|diproses|kurir|pengemasan)\w*" + DEKAT +
         r"(?:cepat|tidak_lama|tidak_lambat|kilat|sat\W*set|ngebut|tepat\W+waktu|on\W*time)\b",
         r"\b(?:cepat|sehari|besoknya|langsung)\W+(?:\w+\W+)?(?:sampai|datang|dikirim|diproses|kirim)\b",
         r"\b(?:tepat\W+waktu|on\W*time|sat\W*set)\b", r"\bpengiriman\W+cepat\b"]},
    {"id": "p_kemasan", "label": "Kemasan rapi & aman", "jenis": "pujian",
     "pihak": "packing (gudang)", "pola": [
         r"\b(?:kemasan|kardus)\w*" + DEKAT2 +
         r"(?:rapi|aman|tebal|bagus|cantik|lucu|mantap|oke|rapat|kuat|premium|berlapis|double|dobel|tebel)\b",
         r"(?<!_)\bbubblewrap\b(?!\W+(?:tipis|sedikit))", r"\b(?:double|dobel)\W+(?:bubblewrap|kardus|kemasan|plastik)\b",
         r"\b(?:sampai|datang|diterima)\W+(?:\w+\W+)?(?:aman|selamat)\b", r"\baman\W+(?:sampai|sentosa)\b",
         r"\btidak_ada_(?:bocor|pecah|penyok|tumpah)\b", r"\btidak_(?:bocor|pecah|penyok|tumpah|rusak)\b"]},
    {"id": "p_harga", "label": "Harga terjangkau / sepadan", "jenis": "pujian",
     "pihak": "harga & nilai", "pola": [
         r"(?<!_)\b(?:murah|terjangkau|sepadan|hemat|ekonomis|affordable)\b", r"\btidak_mahal\b",
         r"\bharga\w*" + DEKAT + r"(?:bersahabat|oke|pas|miring|murah|terjangkau|bersaing|masuk|sebanding)\b",
         r"\bdengan\W+harga\W+segini\b"]},
    {"id": "p_respons", "label": "Penjual/CS ramah & responsif", "jenis": "pujian",
     "pihak": "layanan (admin/CS)", "pola": [
         r"\b(?:respons|admin|penjual|toko|owner|pelayanan|layanan)\w*" + DEKAT +
         r"(?:cepat|ramah|baik|sabar|membantu|informatif|mantap|sigap|tanggap|responsif|oke|jujur|amanah|komunikatif)\b",
         r"(?<!_)\b(?:ramah|sabar|amanah|komunikatif|responsif)\b", r"\bcepat\W+tanggap\b",
         r"\b(?:chat|dm|inbox|pesan(?!an)|pesen(?!an))\w*" + DEKAT + r"(?:dibalas|direspons)\W+(?:\w+\W+)?cepat"]},
    {"id": "p_rasa", "label": "Rasa enak", "jenis": "pujian",
     "pihak": "produk", "pola": [
         r"(?<!_)\b(?:enak|lezat|nikmat|gurih|renyah|nagih|legit|fresh|segar|lumer|empuk|juicy)\b",
         r"\brasa\w*" + DEKAT + r"(?:pas|mantap|enak|oke|konsisten|juara|nendang)\b"]},
    {"id": "p_aroma", "label": "Aroma wangi", "jenis": "pujian",
     "pihak": "produk", "pola": [r"(?<!_)\b(?:wangi|harum)\w*", r"\bbau\W+(?:wangi|harum|enak|segar)\b",
                                 r"\btidak_(?:bau|menyengat|apek)\b"]},
    {"id": "p_ukuran", "label": "Ukuran pas / sesuai tabel ukuran", "jenis": "pujian",
     "pihak": "produk & listing", "pola": [
         r"\bukuran\w*" + DEKAT + r"(?:pas|sesuai|standar|akurat|tepat)\b",
         r"\bpas\W+(?:di\W+badan|dipakai|banget|di\W+kaki|di\W+tangan|ukuran)\b", r"\bsesuai\W+(?:tabel\s+)?ukuran\b"]},
    {"id": "p_repeat", "label": "Pembeli berulang / akan beli lagi", "jenis": "pujian",
     "pihak": "loyalitas", "pola": [
         r"\border\W+lagi\b", r"\b(?:beli|belanja|pesan|langganan|borong|nambah)\W+(?:\w+\W+)?lagi\b",
         r"\blangganan\b", r"\b(?:bakal|akan|pasti|mau)\W+(?:\w+\W+)?(?:beli|order|pesan|belanja)\b",
         r"\bkedua\W*kali\w*|\bketiga\W*kali\w*"]},
    {"id": "p_bonus", "label": "Bonus / hadiah kecil / sentuhan personal", "jenis": "pujian",
     "pihak": "packing & layanan", "pola": [
         r"(?<!_)\b(?:bonus|hadiah|stiker|sticker|permen)\b", r"\bdikasih\W+(?:\w+\W+)?(?:bonus|hadiah|permen|stiker|sample|sampel)\b",
         r"\bbonus\W+kartu\b", r"\bsurat\W+(?:kecil|tulisan)\b"]},
    {"id": "p_suasana", "label": "Suasana/tempat nyaman", "jenis": "pujian",
     "pihak": "fasilitas tempat", "pola": [
         r"\b(?:suasana|tempat|vibes|ambience|ambiance|interior|dekorasi|view|pemandangan)\w*" + DEKAT2 +
         r"(?:nyaman|cozy|asik|asyik|enak|adem|estetik|aesthetic|instagramable|tenang|luas|homey|bagus|keren|cantik|sejuk)\b",
         r"(?<!_)\b(?:nyaman|cozy|estetik|aesthetic|instagramable|homey|kekinian)\b"]},
    {"id": "p_kebersihan", "label": "Bersih & higienis", "jenis": "pujian",
     "pihak": "kebersihan & keamanan pangan", "pola": [r"(?<!_)\b(?:bersih|higienis|steril|wangi\W+bersih)\b"]},
    {"id": "p_fasilitas", "label": "Fasilitas lengkap (parkir, toilet, wifi)", "jenis": "pujian",
     "pihak": "fasilitas tempat", "pola": [
         r"\b(?:parkir|toilet|mushola|musala|wifi|colokan|ac)\w*" + DEKAT2 + r"(?:luas|mudah|gampang|bersih|kencang|lengkap|dingin|ada|banyak|aman|gratis)\b"]},
    {"id": "p_umum", "label": "Puas secara umum (tanpa detail)", "jenis": "pujian",
     "pihak": "umum", "pola": [
         r"(?<!_)\b(?:mantap|puas|suka|keren|oke|rekomendasi|terbaik|love|recommended|top|amanah|memuaskan|luar\W+biasa)\b",
         r"\btidak_(?:kecewa|nyesel|menyesal|rugi)\b", r"\b(?:terima\W*kasih|makasih|thanks|thx)\b"]},
]

# (menang, kalah): bila satu klausa cocok keduanya, tema kedua dibuang.
PRESEDEN = [
    ("k_kemasan", "k_kualitas"),      # "kemasan penyok" -> kemasan, bukan cacat produk
    ("k_kemasan", "p_kemasan"),
    ("k_tidak_sesuai", "p_sesuai"),
    ("k_tidak_sesuai", "k_salah_kirim"),  # "warna beda dengan foto" -> tidak sesuai foto
    ("k_ukuran", "p_ukuran"),
    ("k_kualitas", "p_kualitas"),
    ("k_pengiriman", "p_pengiriman"),
    ("k_respons", "p_respons"),
    ("k_rasa", "p_rasa"),
    ("k_bau", "p_aroma"),
    ("k_harga", "p_harga"),
    ("k_pengiriman", "k_waktu_tunggu"),   # "nunggu paket lama" -> pengiriman
    ("k_kebersihan", "p_kebersihan"),
    ("k_fasilitas", "p_fasilitas"),
    ("k_kebersihan", "k_kualitas"),
    ("k_fasilitas", "p_suasana"),
    ("k_kebersihan", "k_bau"),
]

STOPWORDS = set("""
yang dan di ke dari ini itu dengan untuk pada juga saja sudah belum ada adalah akan atau karena
jadi tapi kalau sama saya kamu kak kakak gan sis min kok sih deh dong ya yah nya lah pun lagi terus
banget sangat sekali udah aja nih tuh kan yg dgn utk buat bisa mau masih lebih paling semua
sebelum sesudah setelah waktu hari kali orang barang produk pesanan beli dibeli membeli order toko
penjual admin seller dapat dapet kasih semoga moga next time the and is it to of a in for good very
nya kah tah mah si oh wah eh aduh hmm hehe wkwk wkwkwk
disamarkan nama nomor kode akun email
""".split())

POLA_BINTANG_CHAR = re.compile(r"[★⭐]")
POLA_RATING_FRASA = [
    re.compile(r"(?i)\b(?:rating|bintang|nilai|skor|score|stars?)\s*[:=]?\s*([1-5])(?:[.,]0)?\b"),
    re.compile(r"(?i)\b([1-5])(?:[.,]0)?\s*(?:/\s*5|dari\s*5|bintang|stars?)\b"),
]
POLA_RATING_AWAL_PIPA = re.compile(r"^\s*([1-5])(?:[.,]0)?\s*\|\s*")
POLA_NOMOR_URUT = re.compile(r"^\s*(?:\d{1,4}[.)]|[-*•])\s+")

# Penyamaran data pribadi di kutipan
SAMARKAN = [
    (re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+"), "[email disamarkan]"),
    (re.compile(r"(?<!\w)@[\w.]{2,}"), "@[akun disamarkan]"),
    (re.compile(r"(?:\+?62|0)\s?8[\d\s-]{7,14}\d"), "[nomor disamarkan]"),
    (re.compile(r"\b(?=[A-Za-z0-9]*\d)(?=[A-Za-z0-9]*[A-Za-z])[A-Za-z0-9]{10,}\b"), "[kode disamarkan]"),
    (re.compile(r"\b\d{8,}\b"), "[nomor disamarkan]"),
    (re.compile(r"\b((?:[Kk]ak|[Kk]a|[Mm]ba|[Mm]bak|[Mm]as|[Bb]u|[Ii]bu|[Pp]ak|[Bb]apak|[Oo]m|[Tt]ante|[Ss]is|[Gg]an|[Bb]ang|[Tt]eh|[Cc]ici|[Kk]oko)\.?\s+)[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})?"),
     r"\1[nama]"),
]

KANDIDAT_KOLOM = {
    "ulasan": ["ulasan", "review", "komentar", "comment", "isi ulasan", "teks", "text", "feedback", "isi",
               "pesan", "testimoni", "content", "konten", "deskripsi ulasan", "review text", "ulasan pembeli"],
    "bintang": ["bintang", "rating", "star", "stars", "nilai", "skor", "score", "penilaian", "rate"],
    "produk": ["produk", "product", "nama produk", "product name", "item", "nama barang", "barang", "sku"],
    "tanggal": ["tanggal", "date", "waktu", "time", "tgl", "created", "tanggal ulasan", "review date"],
    "nama": ["nama", "name", "username", "user", "pembeli", "buyer", "pelanggan", "customer", "akun",
             "nama pembeli", "reviewer", "author"],
}

BULAN = {"jan": 1, "feb": 2, "peb": 2, "mar": 3, "apr": 4, "mei": 5, "may": 5, "jun": 6, "jul": 7,
         "agu": 8, "agt": 8, "aug": 8, "sep": 9, "okt": 10, "oct": 10, "nov": 11, "nop": 11,
         "des": 12, "dec": 12}


# --------------------------------------------------------------------------- util
class GalatInput(Exception):
    pass


def keluar_galat(pesan, kode=2):
    print("ERROR: " + pesan, file=sys.stderr)
    sys.exit(kode)


def baca_teks_file(path):
    if path == "-":
        data = sys.stdin.buffer.read() if hasattr(sys.stdin, "buffer") else sys.stdin.read().encode("utf-8")
    else:
        try:
            with open(path, "rb") as f:
                data = f.read()
        except OSError as e:
            raise GalatInput("file '{}' tidak bisa dibaca ({}). Periksa nama & lokasi file.".format(path, e.strerror))
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            return data.decode(enc), enc
        except UnicodeDecodeError:
            continue
    raise GalatInput("encoding file tidak dikenali")


def normalisasi(teks):
    s = teks.lower()
    s = s.replace(" ", " ").replace("’", "'").replace("`", "'")
    s = re.sub(r"https?://\S+", " ", s)
    s = re.sub(r"(\w)\1{2,}", r"\1", s)               # bagusss -> bagus, bangettt -> banget
    s = re.sub(r"\b([a-z]{3,})2\b", r"\1", s)          # barang2 -> barang
    s = re.sub(r"\b([a-z]{3,})-\1\b", r"\1", s)        # barang-barang -> barang
    for pola, ganti in FRASA:
        s = re.sub(pola, ganti, s)
    kata = re.findall(r"[a-z0-9_]+|[^\sa-z0-9_]", s)
    hasil = []
    for k in kata:
        hasil.append(SLANG.get(k, k))
    s = " ".join(hasil)
    for pola, ganti in FRASA:  # frasa bisa muncul setelah slang diganti (mis. 'order lg' -> 'order lagi')
        s = re.sub(pola, ganti, s)
    s = re.sub(r"\s+", " ", s).strip()
    # "tidak ada (yang)? X" / "tanpa X" -> tidak_ada_X (supaya "tidak ada yang rusak" bukan keluhan)
    s = re.sub(r"\b(?:tidak ada|tanpa|bebas)\s+(?:yang\s+|sedikit\s+pun\s+|satu\s*pun\s+)?([a-z]+)", r"tidak_ada_\1", s)
    # negasi: tidak/kurang/belum/bukan (+ intensifier) + kata -> tidak_kata
    s = re.sub(r"\b(tidak|kurang|belum|bukan)\s+(?:" + INTENSIFIER + r"\s+)?([a-z]+)", r"\1_\2", s)
    return s


def pecah_klausa(teks):
    """Pecah teks asli menjadi klausa (dipakai untuk kutipan & pencocokan tema)."""
    bagian = re.split(r"(?:[!?;\n]+|\.+(?!\d)|\s+-\s+|,?\s+(?=(?:tapi|tp|tpi|namun|cuma|cuman|sayangnya|padahal|untung|untungnya)\s))",
                      teks, flags=re.I)
    return [b.strip(" ,") for b in bagian if b and b.strip(" ,")]


def pecah_koma(kalimat):
    """Pecah satu kalimat di koma (bukan koma desimal) untuk pencocokan tema yang lebih ketat."""
    return [b.strip() for b in re.split(r"(?<!\d),(?!\d)", kalimat) if b.strip()]


def samarkan(teks):
    for pola, ganti in SAMARKAN:
        teks = pola.sub(ganti, teks)
    return teks


def potong(teks, maks=140):
    teks = re.sub(r"\s+", " ", teks).strip()
    if len(teks) <= maks:
        return teks
    return teks[: maks - 1].rsplit(" ", 1)[0] + "…"


def parse_bintang(nilai):
    if nilai is None:
        return None
    s = str(nilai).strip()
    if not s:
        return None
    jumlah_bintang = len(POLA_BINTANG_CHAR.findall(s))
    if jumlah_bintang:
        return jumlah_bintang if 1 <= jumlah_bintang <= 5 else "invalid"
    m = re.match(r"^\s*([0-9]+(?:[.,][0-9]+)?)\s*(?:/\s*5|dari\s*5|bintang|stars?)?\s*$", s, re.I)
    if m:
        v = float(m.group(1).replace(",", "."))
        if v != int(v) or not 1 <= v <= 5:
            return "invalid"
        return int(v)
    for pola in POLA_RATING_FRASA:
        m = pola.search(s)
        if m:
            return int(m.group(1))
    return "invalid"


def parse_tanggal(teks):
    s = (teks or "").strip()
    if not s:
        return None
    m = re.match(r"^(\d{4})[-/.](\d{1,2})[-/.](\d{1,2})", s)
    if m:
        y, mo = int(m.group(1)), int(m.group(2))
        return "{:04d}-{:02d}".format(y, mo) if 1 <= mo <= 12 else None
    m = re.match(r"^(\d{1,2})[-/.](\d{1,2})[-/.](\d{2,4})", s)
    if m:
        mo, y = int(m.group(2)), int(m.group(3))
        y = y + 2000 if y < 100 else y
        return "{:04d}-{:02d}".format(y, mo) if 1 <= mo <= 12 else None
    m = re.match(r"^(\d{1,2})\s+([A-Za-z]+)\.?\s+(\d{2,4})", s)
    if m:
        mo = BULAN.get(m.group(2)[:3].lower())
        y = int(m.group(3))
        y = y + 2000 if y < 100 else y
        return "{:04d}-{:02d}".format(y, mo) if mo else None
    return None


def cari_kolom(kolom, jenis, paksa=None):
    if paksa:
        for k in kolom:
            if k.strip().lower() == paksa.strip().lower():
                return k
        raise GalatInput("kolom '{}' tidak ditemukan. Kolom yang ada: {}".format(paksa, ", ".join(kolom)))
    kecil = {k: k.strip().lower() for k in kolom}
    for kandidat in KANDIDAT_KOLOM[jenis]:
        for k, kk in kecil.items():
            if kk == kandidat:
                return k
    for kandidat in KANDIDAT_KOLOM[jenis]:
        for k, kk in kecil.items():
            if kandidat in kk and len(kandidat) >= 4:
                if jenis == "ulasan" and any(x in kk for x in ("balas", "reply", "tanggapan", "respon")):
                    continue
                if jenis == "nama" and "produk" in kk:
                    continue
                return k
    return None


# --------------------------------------------------------------------------- baca input
def baca_csv(teks, args):
    contoh = teks[:4096]
    try:
        dialek = csv.Sniffer().sniff(contoh, delimiters=",;\t|")
    except csv.Error:
        dialek = csv.excel
    pembaca = csv.DictReader(io.StringIO(teks), dialect=dialek)
    kolom = [k for k in (pembaca.fieldnames or []) if k is not None]
    if not kolom:
        raise GalatInput("CSV tidak punya baris judul kolom")
    k_ulasan = cari_kolom(kolom, "ulasan", args.kolom_ulasan)
    k_bintang = cari_kolom(kolom, "bintang", args.kolom_bintang)
    k_produk = cari_kolom(kolom, "produk", args.kolom_produk)
    k_tanggal = cari_kolom(kolom, "tanggal", args.kolom_tanggal)
    k_nama = cari_kolom(kolom, "nama")
    if k_nama in (k_ulasan, k_produk):
        k_nama = None
    if not k_ulasan and not k_bintang:
        raise GalatInput("kolom ulasan/bintang tidak dikenali. Kolom yang ada: {}. Pakai --kolom-ulasan dan "
                         "--kolom-bintang untuk menunjuk kolomnya.".format(", ".join(kolom)))
    data = []
    for no, r in enumerate(pembaca, start=2):
        if r is None or not any((v or "").strip() for v in r.values() if isinstance(v, str)):
            continue
        data.append({
            "baris": no,
            "teks": (r.get(k_ulasan) or "").strip() if k_ulasan else "",
            "bintang_mentah": r.get(k_bintang) if k_bintang else None,
            "produk": (r.get(k_produk) or "").strip() if k_produk else None,
            "tanggal_mentah": r.get(k_tanggal) if k_tanggal else None,
        })
    info = {"format": "csv", "kolom_ulasan": k_ulasan, "kolom_bintang": k_bintang, "kolom_produk": k_produk,
            "kolom_tanggal": k_tanggal,
            "kolom_nama_diabaikan": k_nama}
    return data, info


def baca_teks(teks):
    baris = teks.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    ada_kosong = any(not b.strip() for b in baris[1:-1]) and sum(1 for b in baris if b.strip()) > 1
    blok = []
    if ada_kosong:
        kini, mulai = [], None
        for i, b in enumerate(baris, start=1):
            if b.strip():
                if not kini:
                    mulai = i
                kini.append(b.strip())
            elif kini:
                blok.append((mulai, " ".join(kini)))
                kini = []
        if kini:
            blok.append((mulai, " ".join(kini)))
    else:
        blok = [(i, b.strip()) for i, b in enumerate(baris, start=1) if b.strip()]
    data = []
    for no, isi in blok:
        isi = POLA_NOMOR_URUT.sub("", isi, count=1)
        bintang = None
        m = POLA_RATING_AWAL_PIPA.match(isi)
        if m:
            bintang = int(m.group(1))
            isi = isi[m.end():]
        else:
            n = len(POLA_BINTANG_CHAR.findall(isi))
            if 1 <= n <= 5:
                bintang = n
                isi = POLA_BINTANG_CHAR.sub("", isi).replace("☆", "")
            else:
                for pola in POLA_RATING_FRASA:
                    m = pola.search(isi)
                    if m:
                        bintang = int(m.group(1))
                        isi = (isi[: m.start()] + isi[m.end():])
                        break
        isi = re.sub(r"^\s*[|:\-–—]\s*", "", isi).strip(" |-–—")
        data.append({"baris": no, "teks": isi.strip(), "bintang_mentah": bintang, "produk": None,
                     "tanggal_mentah": None})
    return data, {"format": "teks", "pemisah_ulasan": "baris kosong" if ada_kosong else "per baris"}


def muat_kamus_tambahan(path):
    teks, _ = baca_teks_file(path)
    try:
        data = json.loads(teks)
    except ValueError as e:
        raise GalatInput("kamus tambahan bukan JSON yang valid: {}".format(e))
    if not isinstance(data, dict):
        raise GalatInput("kamus tambahan harus berupa objek JSON {\"slang\": {...}, \"tema\": [...]}")
    for k, v in (data.get("slang") or {}).items():
        SLANG[str(k).lower()] = str(v).lower()
    ada = {t["id"]: t for t in TEMA}
    for t in data.get("tema") or []:
        if not isinstance(t, dict) or "id" not in t or not (t.get("pola") or t.get("kecualikan")):
            raise GalatInput("setiap tema tambahan wajib punya 'id' dan 'pola' dan/atau 'kecualikan' (daftar regex)")
        for kunci in ("pola", "kecualikan"):
            if kunci in t and not isinstance(t[kunci], list):
                raise GalatInput("'{}' pada tema '{}' harus berupa daftar regex".format(kunci, t["id"]))
        t.setdefault("pola", [])
        for p in list(t["pola"]) + list(t.get("kecualikan", [])):
            try:
                re.compile(p)
            except re.error as e:
                raise GalatInput("regex tema '{}' tidak valid: {} ({})".format(t["id"], p, e))
        if t["id"] in ada:
            ada[t["id"]]["pola"] = list(ada[t["id"]]["pola"]) + list(t["pola"])
            ada[t["id"]]["kecualikan"] = list(ada[t["id"]].get("kecualikan", [])) + list(t.get("kecualikan", []))
        else:
            if not t["pola"]:
                raise GalatInput("tema baru '{}' wajib punya 'pola'".format(t["id"]))
            jenis = t.get("jenis", "keluhan")
            if jenis not in ("keluhan", "pujian"):
                raise GalatInput("jenis tema '{}' harus 'keluhan' atau 'pujian'".format(t["id"]))
            baru = {"id": t["id"], "label": t.get("label", t["id"]), "jenis": jenis,
                    "pihak": t.get("pihak", "lainnya"), "pola": list(t["pola"]),
                    "kecualikan": list(t.get("kecualikan", []))}
            TEMA.append(baru)
            ada[baru["id"]] = baru


# --------------------------------------------------------------------------- analisis
BOBOT = {1: 5, 2: 4, 3: 3, 4: 2, 5: 1, None: 3}


def parse_abaikan(daftar):
    """'k_respons:3,14' (bisa diulang / dipisah ';') -> {tema: {id,...}}"""
    hasil = defaultdict(set)
    ids_tema = {t["id"] for t in TEMA}
    for item in daftar or []:
        for bagian in str(item).split(";"):
            bagian = bagian.strip()
            if not bagian:
                continue
            if ":" not in bagian:
                raise GalatInput("--abaikan-id '{}' harus berformat tema:id,id (mis. k_respons:3,14)".format(bagian))
            tema, ids = bagian.split(":", 1)
            tema = tema.strip()
            if tema not in ids_tema:
                raise GalatInput("--abaikan-id: tema '{}' tidak dikenal".format(tema))
            for x in ids.split(","):
                x = x.strip()
                if not x.isdigit():
                    raise GalatInput("--abaikan-id: id ulasan '{}' harus angka".format(x))
                hasil[tema].add(int(x))
    return hasil


def analisis(data, info, args):
    pola_tema = [(t, [re.compile(p) for p in t["pola"]], [re.compile(p) for p in t.get("kecualikan", [])])
                 for t in TEMA]
    abaikan = parse_abaikan(getattr(args, "abaikan_id", None))
    ulasan = []
    bintang_invalid = 0
    dikecualikan = Counter()
    for d in data:
        b = d["bintang_mentah"]
        if info["format"] == "csv":
            b = parse_bintang(b)
        if b == "invalid":
            bintang_invalid += 1
            b = None
        # samarkan DULU (sebelum dipecah) agar email/nomor tidak terpotong jadi kutipan yang bocor
        teks = samarkan(d["teks"] or "")
        klausa = pecah_klausa(teks) if teks else []
        norm_klausa = []
        tema_hit = defaultdict(list)  # id -> [kutipan]
        id_ulasan = len(ulasan) + 1
        for kalimat in klausa:
            hit_kalimat = {}
            for bagian in pecah_koma(kalimat):
                norm = normalisasi(bagian)
                norm_klausa.append(norm)
                hit = []
                for t, pola, kecuali in pola_tema:
                    if any(p.search(norm) for p in pola):
                        if kecuali and any(k.search(norm) for k in kecuali):
                            dikecualikan[t["id"]] += 1
                            continue
                        hit.append(t["id"])
                for menang, kalah in PRESEDEN:
                    if menang in hit and kalah in hit:
                        hit.remove(kalah)
                kutipan = kalimat if len(kalimat) <= 140 else bagian
                for i in hit:
                    hit_kalimat.setdefault(i, kutipan)
            # presedensi antar-keluhan berlaku per kalimat ("ga sesuai deskripsi, warnanya beda" = 1 tema)
            for menang, kalah in PRESEDEN:
                if menang.startswith("k_") and kalah.startswith("k_") and menang in hit_kalimat and kalah in hit_kalimat:
                    del hit_kalimat[kalah]
            for i, kutipan in hit_kalimat.items():
                if kutipan not in tema_hit[i]:
                    tema_hit[i].append(kutipan)
        for i in list(tema_hit):
            if id_ulasan in abaikan.get(i, ()):
                del tema_hit[i]
                dikecualikan["abaikan_id:" + i] += 1
        # p_umum hanya dihitung bila tidak ada pujian spesifik
        spesifik = [i for i in tema_hit if i.startswith("p_") and i != "p_umum"]
        if spesifik and "p_umum" in tema_hit:
            del tema_hit["p_umum"]
        u = {"id": id_ulasan, "baris": d["baris"], "bintang": b, "teks": teks,
             "norm": " ".join(norm_klausa), "tema": dict(tema_hit), "produk": d.get("produk"),
             "bulan": parse_tanggal(d.get("tanggal_mentah")) if d.get("tanggal_mentah") else None}
        ulasan.append(u)
    info["dikecualikan"] = dict(dikecualikan)
    return ulasan, bintang_invalid


def pilih_contoh(entri, jenis, n):
    """entri: list of (ulasan, klausa). Pilih kutipan beragam, panjang sedang, bintang relevan."""
    def skor(e):
        u, k = e
        panjang = len(k)
        pas = 0 if 15 <= panjang <= 140 else 1
        b = u["bintang"] if u["bintang"] is not None else 3
        urut_b = b if jenis == "keluhan" else -b
        return (pas, urut_b, -min(panjang, 140), u["id"])
    hasil, sudah = [], set()
    for u, k in sorted(entri, key=skor):
        kunci = re.sub(r"\[[a-z ]+\]|\d+", "", normalisasi(samarkan(k))).strip()
        if kunci in sudah or u["id"] in {h["id_ulasan"] for h in hasil}:
            continue
        sudah.add(kunci)
        hasil.append({"id_ulasan": u["id"], "bintang": u["bintang"], "kutipan": potong(samarkan(k))})
        if len(hasil) >= n:
            break
    return hasil


def kata_teratas(teks_list, n=15):
    uni, bi = Counter(), Counter()
    for t in teks_list:
        kata = [k for k in re.findall(r"[a-z_]{3,}", t) if k not in STOPWORDS]
        uni.update(set(kata))
        bi.update(set(" ".join(p) for p in zip(kata, kata[1:])))
    return {"kata": [[k, v] for k, v in uni.most_common(n)],
            "pasangan_kata": [[k, v] for k, v in bi.most_common(n) if v >= 2]}


def sebaran(ulasan_list):
    c = Counter(u["bintang"] for u in ulasan_list)
    return {str(i): c.get(i, 0) for i in range(5, 0, -1)}


def rata(ulasan_list):
    nilai = [u["bintang"] for u in ulasan_list if u["bintang"] is not None]
    return round(sum(nilai) / len(nilai), 2) if nilai else None


def ringkas(ulasan, info, bintang_invalid, args):
    total = len(ulasan)
    berbintang = [u for u in ulasan if u["bintang"] is not None]
    berteks = [u for u in ulasan if u["teks"].strip()]
    n_b = len(berbintang)
    seb = sebaran(ulasan)
    pos = sum(1 for u in berbintang if u["bintang"] >= 4)
    net = sum(1 for u in berbintang if u["bintang"] == 3)
    neg = sum(1 for u in berbintang if u["bintang"] <= 2)

    def pct(a, b):
        return round(a / b * 100, 1) if b else 0.0

    tema_out = []
    for t in TEMA:
        entri = [(u, k) for u in ulasan if t["id"] in u["tema"] for k in u["tema"][t["id"]]]
        anggota = [u for u in ulasan if t["id"] in u["tema"]]
        if not anggota:
            continue
        item = {
            "id": t["id"], "label": t["label"], "jenis": t["jenis"], "pihak": t["pihak"],
            "jumlah_ulasan": len(anggota),
            "persen_dari_ulasan_berteks": pct(len(anggota), len(berteks)),
            "sebaran_bintang": sebaran(anggota), "rata_rata_bintang": rata(anggota),
            "contoh": pilih_contoh(entri, t["jenis"], args.contoh),
            "id_ulasan": [u["id"] for u in anggota][: args.maks_id],
        }
        if t["jenis"] == "keluhan":
            item["skor_prioritas"] = sum(BOBOT[u["bintang"]] for u in anggota)
            item["persen_dari_ulasan_negatif"] = pct(sum(1 for u in anggota if u["bintang"] is not None
                                                         and u["bintang"] <= 2), neg)
        tema_out.append(item)
    keluhan = sorted([t for t in tema_out if t["jenis"] == "keluhan"],
                     key=lambda t: (-t["skor_prioritas"], -t["jumlah_ulasan"], t["id"]))
    for i, t in enumerate(keluhan, 1):
        t["peringkat_prioritas"] = i
    pujian = sorted([t for t in tema_out if t["jenis"] == "pujian"],
                    key=lambda t: (t["id"] == "p_umum", -t["jumlah_ulasan"], t["id"]))

    ada_keluhan = lambda u: any(i.startswith("k_") for i in u["tema"])
    ada_pujian = lambda u: any(i.startswith("p_") for i in u["tema"])
    campur_tinggi = [u for u in berbintang if u["bintang"] >= 4 and ada_keluhan(u)]
    rendah_tanpa_keluhan = [u for u in berbintang if u["bintang"] <= 2 and u["teks"].strip() and not ada_keluhan(u)]
    belum = [u for u in berteks if not u["tema"]]
    singkat = [u for u in berteks if len(u["teks"].split()) <= 3]
    tanpa_teks = total - len(berteks)
    norm_c = Counter(u["norm"] for u in berteks if len(u["norm"]) > 0)
    duplikat = sum(v - 1 for v in norm_c.values() if v > 1)

    def daftar_kutipan(lst):
        return [{"id_ulasan": u["id"], "bintang": u["bintang"], "kutipan": potong(samarkan(u["teks"]), 160)}
                for u in lst[: args.maks_id]]

    hasil = {
        "versi_script": VERSI,
        "sumber": info,
        "ringkasan": {
            "total_ulasan": total, "ulasan_berbintang": n_b, "ulasan_tanpa_bintang": total - n_b,
            "bintang_tidak_valid_diabaikan": bintang_invalid,
            "ulasan_berteks": len(berteks), "ulasan_tanpa_teks": tanpa_teks,
            "ulasan_sangat_singkat_(<=3_kata)": len(singkat), "teks_duplikat_persis": duplikat,
            "rata_rata_bintang": rata(ulasan), "sebaran_bintang": seb,
            "persen_sebaran_bintang": {k: pct(v, n_b) for k, v in seb.items()},
            "positif_4_5": {"jumlah": pos, "persen": pct(pos, n_b)},
            "netral_3": {"jumlah": net, "persen": pct(net, n_b)},
            "negatif_1_2": {"jumlah": neg, "persen": pct(neg, n_b)},
            "ulasan_dengan_keluhan_terdeteksi": sum(1 for u in berteks if ada_keluhan(u)),
            "ulasan_dengan_pujian_terdeteksi": sum(1 for u in berteks if ada_pujian(u)),
        },
        "keluhan_berdasarkan_prioritas": keluhan,
        "pujian_terbanyak": pujian,
        "perlu_dibaca_agent": {
            "bintang_tinggi_tapi_ada_keluhan": {"jumlah": len(campur_tinggi), "contoh": daftar_kutipan(campur_tinggi)},
            "bintang_rendah_tanpa_keluhan_terdeteksi": {"jumlah": len(rendah_tanpa_keluhan),
                                                        "contoh": daftar_kutipan(rendah_tanpa_keluhan)},
            "belum_terklasifikasi": {"jumlah": len(belum), "contoh": daftar_kutipan(belum),
                                     "kata_teratas": kata_teratas([u["norm"] for u in belum])},
        },
        "kata_teratas_bintang_1_3": kata_teratas([u["norm"] for u in berteks if u["bintang"] is not None and u["bintang"] <= 3]),
        "kata_teratas_bintang_4_5": kata_teratas([u["norm"] for u in berteks if u["bintang"] is not None and u["bintang"] >= 4]),
        "rumus": {
            "rata_rata_bintang": "jumlah bintang / ulasan berbintang (2 desimal, pembulatan biasa)",
            "persen": "jumlah / pembagi x 100 (1 desimal); persen sebaran & positif/negatif dari ulasan berbintang",
            "skor_prioritas": "jumlah bobot per ulasan yang menyebut keluhan; bobot 1*=5, 2*=4, 3*=3, 4*=2, 5*=1, tanpa bintang=3",
        },
        "peringatan": [],
    }
    if any(u["produk"] for u in ulasan):
        per = defaultdict(list)
        for u in ulasan:
            per[u["produk"] or "(tanpa nama produk)"].append(u)
        hasil["per_produk"] = sorted([
            {"produk": p, "jumlah_ulasan": len(l), "rata_rata_bintang": rata(l),
             "negatif_1_2": sum(1 for u in l if u["bintang"] is not None and u["bintang"] <= 2),
             "keluhan_teratas": [k for k, _ in Counter(i for u in l for i in u["tema"] if i.startswith("k_")).most_common(3)]}
            for p, l in per.items()], key=lambda x: (-x["jumlah_ulasan"], x["produk"]))
    if any(u["bulan"] for u in ulasan):
        per = defaultdict(list)
        for u in ulasan:
            if u["bulan"]:
                per[u["bulan"]].append(u)
        hasil["per_bulan"] = [{"bulan": b, "jumlah_ulasan": len(l), "rata_rata_bintang": rata(l),
                               "negatif_1_2": sum(1 for u in l if u["bintang"] is not None and u["bintang"] <= 2)}
                              for b, l in sorted(per.items())]
        tak = sum(1 for u in ulasan if not u["bulan"])
        if tak:
            hasil["peringatan"].append("{} ulasan tanggalnya tidak terbaca, tidak masuk rekap per bulan.".format(tak))

    p = hasil["peringatan"]
    if total < 20:
        p.append("Sampel kecil ({} ulasan): persentase mudah berubah, sampaikan sebagai gambaran awal.".format(total))
    if n_b == 0:
        p.append("Tidak ada bintang terbaca: sebaran bintang & skor prioritas memakai bobot netral. "
                 "Minta pengguna menyertakan bintang (format 'bintang | ulasan').")
    elif total - n_b > 0:
        p.append("{} ulasan tanpa bintang (tidak masuk rata-rata & persen sebaran).".format(total - n_b))
    if bintang_invalid:
        p.append("{} nilai bintang tidak valid (bukan 1-5) diabaikan.".format(bintang_invalid))
    if berteks and len(belum) / len(berteks) > 0.3:
        p.append("{}% ulasan berteks belum masuk tema kamus: baca contohnya & kata teratasnya, "
                 "lalu buat tema tambahan bila perlu.".format(round(len(belum) / len(berteks) * 100)))
    if duplikat:
        p.append("{} ulasan berteks persis sama dengan ulasan lain (mungkin template/otomatis); tetap dihitung.".format(duplikat))
    if info.get("encoding") and info["encoding"] != "utf-8-sig":
        p.append("File dibaca dengan encoding {} (bukan UTF-8); cek huruf aneh di kutipan.".format(info["encoding"]))
    return hasil


def detail_tema(ulasan, id_tema):
    ids = {t["id"] for t in TEMA}
    if id_tema not in ids:
        raise GalatInput("tema '{}' tidak dikenal. Pilihan: {}".format(id_tema, ", ".join(sorted(ids))))
    out = []
    for u in ulasan:
        if id_tema in u["tema"]:
            out.append({"id_ulasan": u["id"], "baris_sumber": u["baris"], "bintang": u["bintang"],
                        "klausa_cocok": [potong(samarkan(k), 200) for k in u["tema"][id_tema]],
                        "ulasan_lengkap": potong(samarkan(u["teks"]), 400)})
    return {"tema": id_tema, "jumlah": len(out), "ulasan": out}


# --------------------------------------------------------------------------- output teks
def cetak_teks(h):
    r = h["ringkasan"]
    L = []
    L.append("RINGKASAN ULASAN")
    L.append("Total ulasan: {} (berbintang {}, berteks {})".format(r["total_ulasan"], r["ulasan_berbintang"], r["ulasan_berteks"]))
    if r["rata_rata_bintang"] is not None:
        L.append("Rata-rata bintang: {}".format(str(r["rata_rata_bintang"]).replace(".", ",")))
    for k in ("5", "4", "3", "2", "1"):
        n = r["sebaran_bintang"][k]
        L.append("  {}★ {:>4}  ({}%)  {}".format(k, n, str(r["persen_sebaran_bintang"][k]).replace(".", ","),
                                               "█" * int(round(r["persen_sebaran_bintang"][k] / 5))))
    L.append("Positif (4-5★): {}%  |  Netral (3★): {}%  |  Negatif (1-2★): {}%".format(
        *(str(r[x]["persen"]).replace(".", ",") for x in ("positif_4_5", "netral_3", "negatif_1_2"))))
    L.append("")
    L.append("KELUHAN (urut prioritas)")
    for t in h["keluhan_berdasarkan_prioritas"]:
        L.append("{}. {} — {} ulasan, skor {} [{}]".format(t["peringkat_prioritas"], t["label"], t["jumlah_ulasan"],
                                                          t["skor_prioritas"], t["pihak"]))
        for c in t["contoh"]:
            L.append('   - "{}" ({}★)'.format(c["kutipan"], c["bintang"] if c["bintang"] is not None else "?"))
    L.append("")
    L.append("PUJIAN TERBANYAK")
    for t in h["pujian_terbanyak"]:
        L.append("- {} — {} ulasan".format(t["label"], t["jumlah_ulasan"]))
        for c in t["contoh"]:
            L.append('   - "{}" ({}★)'.format(c["kutipan"], c["bintang"] if c["bintang"] is not None else "?"))
    x = h["perlu_dibaca_agent"]
    L.append("")
    L.append("PERLU DIBACA MANUAL: bintang tinggi+keluhan {}, bintang rendah tanpa keluhan terdeteksi {}, "
             "belum terklasifikasi {}".format(x["bintang_tinggi_tapi_ada_keluhan"]["jumlah"],
                                              x["bintang_rendah_tanpa_keluhan_terdeteksi"]["jumlah"],
                                              x["belum_terklasifikasi"]["jumlah"]))
    for p in h["peringatan"]:
        L.append("PERINGATAN: " + p)
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Olah ulasan pelanggan (CSV/teks) menjadi statistik & kandidat tema.")
    ap.add_argument("file", help="File .csv/.tsv (ekspor) atau .txt (tempelan). Pakai '-' untuk membaca dari stdin.")
    ap.add_argument("--jenis-input", choices=["auto", "csv", "teks"], default="auto")
    ap.add_argument("--kolom-ulasan")
    ap.add_argument("--kolom-bintang")
    ap.add_argument("--kolom-produk")
    ap.add_argument("--kolom-tanggal")
    ap.add_argument("--contoh", type=int, default=3, help="Jumlah contoh kutipan per tema (default 3)")
    ap.add_argument("--maks-id", type=int, default=30, help="Maks. id ulasan/contoh yang dicantumkan per daftar")
    ap.add_argument("--detail-tema", help="Tampilkan semua ulasan untuk satu id tema (mis. k_pengiriman)")
    ap.add_argument("--kamus-tambahan", help="File JSON berisi slang/tema tambahan/pola kecualikan")
    ap.add_argument("--abaikan-id", action="append",
                    help="Buang tema dari ulasan tertentu setelah dicek manual, mis. k_respons:3,14 (bisa diulang)")
    ap.add_argument("--format", choices=["json", "teks"], default="json")
    args = ap.parse_args()
    if args.contoh < 1 or args.maks_id < 1:
        keluar_galat("--contoh dan --maks-id minimal 1")
    try:
        if args.kamus_tambahan:
            muat_kamus_tambahan(args.kamus_tambahan)
        teks, enc = baca_teks_file(args.file)
        if not teks.strip():
            raise GalatInput("file kosong. Tempel ulasan (satu ulasan per baris, format 'bintang | ulasan') "
                             "atau kirim file CSV ekspor.")
        jenis = args.jenis_input
        if jenis == "auto":
            jenis = "csv" if args.file.lower().endswith((".csv", ".tsv")) else "teks"
        data, info = baca_csv(teks, args) if jenis == "csv" else baca_teks(teks)
        info["encoding"] = enc
        if not data:
            raise GalatInput("tidak ada ulasan yang terbaca (file hanya berisi judul kolom?)")
        ulasan, invalid = analisis(data, info, args)
        if args.detail_tema:
            print(json.dumps(detail_tema(ulasan, args.detail_tema), ensure_ascii=False, indent=2))
            return
        hasil = ringkas(ulasan, info, invalid, args)
    except GalatInput as e:
        keluar_galat(str(e))
    if args.format == "teks":
        print(cetak_teks(hasil))
    else:
        print(json.dumps(hasil, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
