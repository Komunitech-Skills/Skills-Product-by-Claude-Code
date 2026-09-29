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

VERSI = "1.0.1"


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
}
# Frasa -> satu token (diterapkan setelah slang, sebelum pecah klausa)
FRASA = [
    (r"\bkurang\s+lebih\b", "kuranglebih"),
    (r"\btidak\s+ada\s+(?:yang\s+)?(?:minus|masalah|kendala|keluhan|kekurangan|komplain|cacat|lecet|kurang)(?:nya)?\b"
     r"|\btanpa\s+(?:minus|cacat|kendala|masalah)\b|\bno\s+minus\b", "tanpaminus"),
    (r"\bkurang\s+\d+\b|\b(?:yang\s+)?(?:datang|sampai|dikirim)\s+(?:cuma|hanya|cuman)\s+\d+\b|\btidak\s+lengkap\b", "kurangjumlah"),
    (r"\b(?:dikirim|dikasih|diberi)\s+salah(?:\s+(?:warna|ukuran|size|varian|model|barang|menu|produk|item))?\b|\btidak\s+sesuai\s+(?:pesanan|order)\b|\bsalah\s+(?:pesan(?:an)?|kirim|item|ambil|isi|warna|ukuran|size|varian|"
     r"model|barang|menu|produk|alamat)\b", "salahpesanan"),
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
    (r"\bpas\s+(?:banget|sekali|di\s*badan|di\s*kaki|dipakai|ukuran\w*)\b|\b(?:ukuran|size|porsi|harga|rasa)(?:nya)?\s+(?:sudah\s+)?pas\b",
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
bergerak diangkat dihubungi bisa dikembalikan diganti ditanggapi update dikabari kabar dapat dicek diantar diterima terima jadi ada""".split())
POS = set("""enak lezat nikmat mantap bagus puas suka cepat rapi ramah sopan murah terjangkau fresh segar hangat renyah empuk gurih
recommended top oke keren juara wangi harum hemat bersih higienis aman kenyang mengenyangkan responsif adem nyaman cozy cantik lembut halus
awet kokoh kuat sesuai amanah sabar informatif jujur sigap tanggap perfect sempurna best love lucu mulus kilat ori original asli bersahabat
akurat lumayan senang cinta memuaskan istimewa teliti profesional helpful membantu tebal wow
responscepat orderlagi tepatwaktu sepadan sesuaiharapan tanpaminus pasbanget masihhangat terima kasih""".split())
NEG = set("""telat terlambat lama basi jelek kecewa mahal bocor tumpah rusak salah lambat pelit hambar anyep lembek pera keras alot gosong
mentah tidaksesuai salahpesanan penyok kotor bau amis apek tengik anyir pesing busuk judes kasar cuek galak sombong lupa tertukar ketuker
kedaluwarsa rambut serangga lalat semut ulat kecoa belatung tikus jamur berjamur cacat luntur pudar kusam lepas robek tipis nerawang
sakitperut mual muntah diare keracunan jijik komplain marah zonk tipu penipu bohong kapok menyesal habis kehabisan ribet susah sulit masalah
parah mengecewakan buruk kekecilan kebesaran kesempitan kepanjangan kependekan sedikit responslambat bendaasing lecet lecek retak patah
hancur remuk pecah penyok macet error mati panas gerah pengap berisik bising sempit hilang ketinggalan kelupaan nyasar ngaret molor kelamaan
kemahalan kemanisan keasinan kepedasan kepahitan keasaman kusut noda jerawat jerawatan iritasi gatal perih breakout jebol melar rontok
berantakan php kosong harganaik sudahlama tunggulama cepatrusak fasilitasrusak musikkeras makanandingin kurangjumlah""".split())
PENGUAT = {"begitu", "terlalu", "banget", "sekali", "agak", "sangat", "amat", "cukup", "sih", "juga"}
BERLEBIH = {"terlalu", "kelewat", "kebanyakan", "kelewatan"}
SARAN = re.compile(r"\b(sebaiknya|semoga\s+ada|tolong\s+(?:ditambah|tambah|dibuat|dibuatkan|diperbaiki|dibenahi|diadakan)|mohon|"
                   r"kalau\s+bisa|usul\w*|saran\w*|request|harap|kapan\s+(?:ada|ready|buka|restock)|bisa\s+tidak|boleh\s+tidak|"
                   r"tambahin|ditambah|dibuatkan|next|pengen|ingin|mau\s+dong)\b")
TANYA_MINTA = re.compile(r"\b(kapan|bisa|boleh|ada|tolong|mohon|apakah|mau)\b")

# id, label, dampak (1-5), pola (bagian regex; imbuhan di-/ter-/ke-/ber- dan -nya/-kan/-an/-in/-ya dikenali)
TEMA_BAWAAN = [
    ("rasa", "Rasa / cita rasa", 4, r"rasa|enak|lezat|nikmat|gurih|hambar|anyep|asin|manis|pedas|pahit|asam|amis|gosong|mentah|renyah|empuk|"
     r"alot|keras|lembek|pera|bumbu|nendang|kematangan|matang|kemanisan|keasinan|kepedasan|kepahitan|keasaman|makanandingin|masihhangat"),
    ("kemasan", "Kemasan / packing", 3, r"kemasan|kemas|packing|packaging|pack|bungkus|dus|kardus|box|kotak|plastik|bubble|bubblewrap|bocor|"
     r"tumpah|penyok|segel|wadah|botol|toples|lakban|kresek"),
    ("harga", "Harga / ongkir", 2, r"harga|mahal|murah|terjangkau|ongkir|diskon|promo|sepadan|biaya|tarif|hemat|pricey|kemahalan|harganaik"),
    ("pengiriman", "Pengiriman / ketepatan waktu", 3, r"kirim|pengiriman|kurir|ojol|ojek|gojek|grab|shopeefood|gofood|telat|terlambat|datang|"
     r"sampai|antar|tepatwaktu|delivery|resi|ekspedisi|jne|jnt|sicepat|anteraja|nyasar|kilat|ngaret|molor|dijemput|jemput"),
    ("layanan", "Layanan / respons admin & staf", 3, r"admin|layanan|pelayanan|pelayan|respons|responscepat|responslambat|balas|chat|ramah|"
     r"sopan|judes|galak|cuek|staf|pegawai|karyawan|kasir|barista|waiter|waitress|teknisi|montir|mekanik|seller|penjual|ditanggapi|"
     r"tanggap|sabar|informatif|amanah|dilayani|melayani"),
    ("ketepatan_pesanan", "Ketepatan pesanan", 4, r"ketuker|tertukar|kelupaan|lupa\s+dimasukkan|salahpesanan|kurangjumlah|ketinggalan"),
    ("kualitas_produk", "Kualitas produk / sesuai foto", 4, r"kualitas|bahan|jahitan|jahit|awet|rusak|cacat|luntur|pudar|kusam|warna|"
     r"sesuaiharapan|tidaksesuai|patah|retak|lecet|berfungsi|robek|lepas|tipis|nerawang|ritsleting|kancing|macet|mati|ori|original|palsu|kw|"
     r"jerawat|jerawatan|iritasi|gatal|perih|breakout|kusut|noda|hasil|mulus|cepatrusak|jebol|melar|rontok|hancur|pecah"),
    ("keamanan", "Keamanan produk (benda asing, basi, sakit)", 5, r"basi|kedaluwarsa|rambut|serangga|lalat|semut|ulat|belatung|kecoa|tikus|"
     r"bendaasing|sakitperut|diare|keracunan|mual|muntah|alergi|jamur|berjamur|jijik"),
    ("kebersihan", "Kebersihan", 3, r"kotor|jorok|higienis|bersih|kebersihan|debu|berdebu|lengket"),
    ("bau_aroma", "Bau / aroma", 3, r"bau|apek|tengik|anyir|pesing|busuk|wangi|harum|aroma"),
    ("porsi_ukuran", "Porsi / ukuran / size", 3, r"porsi|ukuran|size|kekecilan|kebesaran|kesempitan|kepanjangan|kependekan|pelit|kenyang|"
     r"mengenyangkan|gramasi|sedikit|pasbanget"),
    ("stok_ketersediaan", "Stok / ketersediaan", 2, r"habis|kosong|stok|stock|restock|ready|preorder|kehabisan"),
    ("pembayaran", "Pembayaran / refund", 3, r"bayar|pembayaran|transfer|qris|cod|refund|pengembalian|kembalian|tagihan|invoice|nota|struk|"
     r"cashback|saldo"),
    ("varian_menu", "Varian / menu / pilihan", 2, r"varian|menu|pilihan|model|motif|koleksi|rasa\s+baru|warna\s+baru|warna\s+lain"),
    ("fasilitas", "Tempat / fasilitas", 3, r"tempat|wifi|wi\s*fi|ac|parkir|parkiran|toilet|wc|kamar\s+mandi|colokan|stopkontak|musik|kursi|"
     r"mushola|musala|ruangan|ruang|suasana|lampu|fasilitas|fasilitasrusak|musikkeras|berisik|bising|gerah|pengap"),
    ("waktu_tunggu", "Waktu tunggu / antrean", 3, r"antre|antrean|antri|antrian|tunggu|tunggulama|kelamaan|disajikan|penyajian|selesai"),
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
RE_KODE = re.compile(r"\b(?=[A-Za-z0-9\-]*\d)(?=[A-Za-z0-9\-]*[A-Za-z])[A-Za-z0-9\-]{8,}\b|\b\d{9,}\b")
RE_ALAMAT = re.compile(r"\b(?:jl|jln|jalan|gg|gang)\.?\s+[^,;\n]{3,40}", re.I)
RE_ALAMAT2 = re.compile(r"\b(?:perum(?:ahan)?|komplek|kompleks|komp|cluster|apartemen|apart|griya|villa|residence)\.?\s+[^,;\n]{2,40}", re.I)
RE_BLOK = re.compile(r"\b(?:blok|blk|rt|rw|kav)\.?\s*[A-Za-z]?\d{1,4}[A-Za-z]?\b(?:\s*/\s*\d{1,3})?", re.I)
RE_PLAT = re.compile(r"\b[A-Z]{1,2}\s?\d{1,4}\s?[A-Z]{1,3}\b")
RE_AN = re.compile(r"(?i:\b(?:a\.\s?n\.?|a/n|an\.|atas\s+nama))\s+[A-Za-z][A-Za-z']+(?:\s+[A-Z][A-Za-z']+){0,2}")
RE_SAYA = re.compile(r"\b((?i:nama\s+(?:saya|sy|aku)|namaku))\s+([A-Za-z][A-Za-z']{1,})(?:\s+([A-Z][A-Za-z']{2,}))?"
                     r"|\b((?i:saya|aku|sy))\s+([A-Z][a-z']{2,})(?:\s+([A-Z][a-z']{2,}))?")
RE_SAPAAN_NAMA = re.compile(r"\b(" + SAPAAN + r")\.?\s+(?:(" + GELAR + r")\s+)?([A-Z][A-Za-z']{2,})(?:\s+([A-Z][A-Za-z']{2,}))?")
RE_SAPAAN_KECIL = re.compile(r"\b(" + SAPAAN + r")\s+([a-z]{3,12})(?=\s*(?:[,.!?)~]|$))")
BUKAN_NAMA = {"Admin", "Seller", "Toko", "Min", "Kasir", "Owner", "Saya", "Aku", "Tolong", "Mau", "Ini", "Itu", "Yang", "Kok", "Bisa",
              "Boleh", "Apakah", "Minta", "Terima", "Terimakasih", "Makasih", "Halo", "Hai", "Selamat", "Maaf", "Pesanan", "Order",
              "Barang", "Paket", "Dapur", "Warung", "Kedai", "Bakery", "Katering", "Kurir", "Driver", "Sudah", "Belum", "Untuk", "Dari",
              "Pesan", "Kirim", "Nanti", "Besok", "Sama", "Juga", "Tapi", "Dan", "Atau", "Kalau", "Kapan", "Gimana", "Bagaimana", "Apa",
              "Sangat", "Suka", "Senang", "Puas", "Kecewa", "Beli", "Pakai", "Harus", "Sedang", "Lagi", "Baru", "Masih", "Tidak", "Ga",
              "Gak", "Enggak", "Nggak", "Punya", "Pernah", "Selalu", "Langganan", "Pelanggan", "Customer", "Cs", "Mohon", "Silakan"}
RE_PENGIRIM_MEDIA = re.compile(r"<media[^>]*>|<attached[^>]*>|\(file attached\)|gambar tidak disertakan|video tidak disertakan|stiker tidak disertakan|audio tidak disertakan|dokumen tidak disertakan", re.I)
RE_SISTEM_TEKS = re.compile(r"pesan ini dihapus|you deleted this message|this message was deleted|pesan dihapus|end-to-end|terenkripsi|"
                            r"bergabung menggunakan tautan|telah ditambahkan|meninggalkan grup|mengubah (?:ikon|subjek|deskripsi)|null$", re.I)


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
    t = RE_ALAMAT.sub("[alamat]", t)
    t = RE_ALAMAT2.sub("[alamat]", t)
    t = RE_BLOK.sub("[alamat]", t)
    t = RE_PLAT.sub("[plat]", t)
    t = RE_AN.sub(lambda m: re.match(r"\S+(?:\s+nama)?", m.group(0)).group(0) + " [nama]", t)

    def _saya(m):
        if m.group(1):  # "nama saya X" -> selalu disamarkan
            return m.group(1) + " [nama]" + ((" " + m.group(3)) if m.group(3) and _bukan_nama(m.group(3)) else "")
        if _bukan_nama(m.group(5)):
            return m.group(0)
        return m.group(4) + " [nama]" + ((" " + m.group(6)) if m.group(6) and _bukan_nama(m.group(6)) else "")
    t = RE_SAYA.sub(_saya, t)

    def _sapaan(m):
        if m.group(3) in BUKAN_NAMA or (m.group(2) is None and _bukan_nama(m.group(3))):
            return m.group(0)
        ekor = (" " + m.group(4)) if m.group(4) and _bukan_nama(m.group(4)) else ""
        return m.group(1) + (" " + m.group(2) if m.group(2) else "") + " [nama]" + ekor
    t = RE_SAPAAN_NAMA.sub(_sapaan, t)
    t = RE_SAPAAN_KECIL.sub(lambda m: m.group(0) if _bukan_nama(m.group(2)) or m.group(2) in VOCAB else m.group(1) + " [nama]", t)
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


def baca_wa(teks, staf=None, tanpa_sapaan=False):
    """Kembalikan (daftar [(tanggal, pengirim, isi)], Counter pengirim)."""
    pesan = []
    for baris in teks.splitlines():
        baris = baris.replace("\u200e", "").replace("\u202f", " ").replace("\xa0", " ")
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
    kamus = {"bintang": KOLOM_NILAI, "tanggal": KOLOM_TANGGAL, "kanal": KOLOM_KANAL}[jenis]
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


def baca_csv(teks, kolom_teks=None, kolom_bintang=None, kolom_tanggal=None, skala=None, nama="CSV"):
    """Kembalikan (daftar item mentah, info kolom, peringatan)."""
    sampel = teks[:4096]
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
    kd = pilih_kolom(header, "tanggal", kolom_tanggal)
    kk = pilih_kolom(header, "kanal")
    kt, peringatan = pilih_kolom_teks(header, baris_semua, kolom_teks, kecuali=set(kb[:1] + kd[:1] + kk[:1]))
    if not kt:
        raise Gagal("%s: kolom teks ulasan/komentar tidak ditemukan. Kolom yang ada: %s. Ulangi dengan --kolom-teks \"NAMA KOLOM\"."
                    % (nama, ", ".join('"%s"' % h for h in header)))
    kt_nama = [h for h, _ in kt]
    kb = [h for h in kb if h not in kt_nama]
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
            hasil.append({"tgl": tgl, "nilai": nilai, "skala": sk if nilai is not None else None, "isi": isi, "kanal": kanal or None,
                          "identitas": (k,) + identitas, "peran": peran, "kolom": k})
    nilai_baris = []
    if kb:
        for baris in baris_semua:
            a, _ = parse_nilai(baris.get(kb[0]))
            if a is not None:
                nilai_baris.append(a)
    responden = sum(1 for b in baris_semua if any((b.get(k) or "").strip().lower() not in KOSONG for k, _ in kt))
    info = {"kolom_teks": kt_nama, "kolom_nilai": kb[0] if kb else None, "nilai_baris": nilai_baris if sk == 10 else [],
            "responden": responden, "skala_nilai": ("0-10" if sk == 10 else "1-5") if kb else None,
            "kolom_tanggal": kd[0] if kd else None, "baris": len(baris_semua)}
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
    baris1 = teks.lstrip("\ufeff").split("\n", 1)[0]
    if ext in ("csv", "tsv") or (ext not in ("txt",) and len(re.split(r"[,;\t]", baris1)) >= 2 and not RE_WA1.match(baris1)):
        info["jenis"] = "csv"
        mentah, kol, pr = baca_csv(teks, getattr(opsi, "kolom_teks", None), getattr(opsi, "kolom_bintang", None),
                                   getattr(opsi, "kolom_tanggal", None), getattr(opsi, "skala", None), nama)
        info.update(kol)
        info["peringatan"] += pr
        return kanal, mentah, info, None
    wa, hitung = baca_wa(teks, getattr(opsi, "staf_list", []))
    if len(wa) >= 3 and sum(1 for p in wa if p[1]) >= 3 and hitung:
        info["jenis"] = "whatsapp"
        return kanal, wa, info, hitung
    return kanal, baca_teks_bebas(teks), info, None


# ------------------------------------------------------------------ normalisasi & koreksi typo
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
    if tok in vocab or tok in KATA_UMUM or len(tok) < 4 or not tok.isalpha():
        return tok
    tunggal = re.sub(r"(.)\1+", r"\1", tok)
    if tunggal in vocab:
        return tunggal
    if len(tok) >= 6:
        # huruf pertama sama; huruf terakhir yang hilang tidak dikoreksi ('berisi' bukan 'berisik')
        kand = {w for w in peta.get(tok, ()) if w[0] == tok[0] and w[:-1] != tok}
        if len(kand) == 1:
            return kand.pop()
    return tok


def normalkan(teks, vocab=None, peta=None):
    t = teks.lower()
    t = re.sub(r"\[(nama|hp|telepon|email|tautan|akun|nomor|alamat|plat)\]", r" \1x ", t)
    t = re.sub(r"(.)\1{2,}", r"\1\1", t)                  # 'enaaak' -> 'enaak'
    t = re.sub(r"\b([a-z]{3,})2\b", r"\1", t)            # 'anak2' -> 'anak'
    t = re.sub(r"\b([a-z]{3,})-\1\b", r"\1", t)          # 'gerak-gerak'
    t = re.sub(r"\bg(?:a|ak|k)(?=(?:enak|sesuai|bisa|ada|jelas|dibalas|dibales|datang|dateng|nyampe|sampai|bagus|ramah|rapi|bersih|awet|"
               r"adem|nyaman|mau|respon|fresh|sopan|cocok)\b)", "tidak ", t)
    kata = re.findall(r"[a-z]+|\d+|[^\w\s]", t)
    keluar = []
    for k in kata:
        if k in SLANG:
            keluar.append(SLANG[k])
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
    for cal in (k, re.sub(r"(?:nya|ya|in|kan|lah)$", "", k), re.sub(r"^di", "", re.sub(r"(?:nya|in|kan)$", "", k))):
        if cal and len(cal) >= 3:
            if cal in kata_neg:
                return -1
            if cal in kata_pos:
                return 1
    return 0


def skor_klausa(klausa, kata_pos, kata_neg, tanya=False, neg_kustom=frozenset()):
    tok = re.findall(r"[a-z0-9\[\]]+", klausa)
    skor, i = 0, 0
    while i < len(tok):
        k = tok[i]
        sebelum = tok[max(0, i - 2):i]
        dinegasi = any(x in NEGATOR for x in sebelum)
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
        if tanya and nilai > 0:
            nilai = 0        # pertanyaan bukan pujian ("sesuai foto tidak?")
        skor += nilai
        i += 1
    return skor


def _pola_kata(kata):
    return "|".join(r"\s+".join(re.escape(b) for b in k.lower().split()) for k in kata if k and k.strip())


def buat_tema(konfigurasi):
    """Tema bawaan (+ tema.json). Kunci tema.json: tema, tambah_kata, hapus_tema, ganti_tema, kata_positif, kata_negatif."""
    tema = [dict(id=i, label=l, dampak=d, pola=re.compile(AFIKS[0] + p + AFIKS[1])) for i, l, d, p in TEMA_BAWAAN]
    kata_pos, kata_neg = set(POS), set(NEG)
    neg_kustom = set()
    if konfigurasi:
        if not isinstance(konfigurasi, dict):
            raise Gagal("tema.json harus berupa objek {...}; lihat templates/tema-contoh.json.")
        if konfigurasi.get("ganti_tema"):
            tema = []
        hapus = set(konfigurasi.get("hapus_tema", []) or [])
        tema = [t for t in tema if t["id"] not in hapus]
        for tid, kata in (konfigurasi.get("tambah_kata", {}) or {}).items():
            if not isinstance(kata, list):
                raise Gagal("tema.json: tambah_kata[\"%s\"] harus daftar kata, mis. [\"dibales\", \"fast respon\"]." % tid)
            for t in tema:
                if t["id"] == tid and _pola_kata(kata):
                    t["pola"] = re.compile(t["pola"].pattern[:-len(AFIKS[1])] + "|" + _pola_kata(kata) + AFIKS[1], re.I)
                    break
            else:
                raise Gagal("tema.json: tambah_kata memakai id \"%s\" yang tidak ada. Id bawaan: %s." % (tid, ", ".join(t[0] for t in TEMA_BAWAAN)))
        daftar = konfigurasi.get("tema", []) or []
        if not isinstance(daftar, list):
            raise Gagal("tema.json: \"tema\" harus daftar [...].")
        for t in daftar:
            if not isinstance(t, dict) or not t.get("id") or not isinstance(t.get("kata", []), list):
                raise Gagal("tema.json: setiap tema perlu \"id\" dan \"kata\" (daftar). Contoh: templates/tema-contoh.json.")
            pola = _pola_kata(t.get("kata", []))
            if not pola:
                continue
            try:
                dampak = int(t.get("dampak", 3))
            except (TypeError, ValueError):
                raise Gagal("tema.json: dampak tema \"%s\" harus angka 1-5." % t["id"])
            baru = dict(id=str(t["id"]), label=t.get("label", t["id"]), dampak=max(1, min(5, dampak)),
                        pola=re.compile(AFIKS[0] + "(?:" + pola + ")" + AFIKS[1], re.I))
            tema = [x for x in tema if x["id"] != baru["id"]] + [baru]
        kata_pos |= {k.lower() for k in konfigurasi.get("kata_positif", []) or []}
        neg_kustom = {k.lower() for k in konfigurasi.get("kata_negatif", []) or []}
        kata_neg |= neg_kustom
        kata_pos -= neg_kustom
    buat_tema.neg_kustom = frozenset(neg_kustom)
    return tema, kata_pos, kata_neg


buat_tema.neg_kustom = frozenset()


_CACHE_TYPO = {}


def analisis_item(teks_anonim, bintang, tema, kata_pos, kata_neg, peran="ulasan", tema_kolom=()):
    """Kembalikan (sentimen_pesan, {tema_id: set(jenis)}). bintang = setara 1-5 (lihat nilai_ke_bintang) atau None."""
    neg_kustom = buat_tema.neg_kustom
    vocab_tambah = frozenset((kata_pos | kata_neg) - VOCAB)
    if vocab_tambah:
        if _CACHE_TYPO.get("kunci") != vocab_tambah:
            vocab = VOCAB | vocab_tambah
            _CACHE_TYPO.update(kunci=vocab_tambah, vocab=vocab, peta=_siapkan_typo(vocab))
        vocab, peta = _CACHE_TYPO["vocab"], _CACHE_TYPO["peta"]
    else:
        vocab = peta = None
    klausa = pecah_klausa(normalkan(teks_anonim, vocab, peta))
    total = 0
    per_tema = defaultdict(set)
    tanpa_tema_keluhan = False
    for k, tanya in klausa:
        s = skor_klausa(k, kata_pos, kata_neg, tanya, neg_kustom)
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
        if jenis != "keluhan" and (SARAN.search(k) or (tanya and TANYA_MINTA.search(k)) or peran == "saran"):
            jenis = "saran"
        cocok = [t["id"] for t in tema if t["pola"].search(k)]
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


def potong(t, n=140):
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


STOP = set("""yang dan di ke dari untuk dengan ini itu saya kami kita kak ya nya juga sudah tidak tapi atau ada pada saja
lagi sama karena jadi bisa mau akan sih deh dong kok banget terima kasih namax hpx nomorx tautanx akunx emailx alamatx platx teleponx""".split())


def olah(sumber, opsi, konfigurasi=None):
    tema, kata_pos, kata_neg = buat_tema(konfigurasi)
    item = []
    dibuang = Counter()
    meta = {"pengirim": {}, "sumber": [], "peringatan": []}
    buang_teks_sama = getattr(opsi, "buang_teks_sama", False)
    staf = [s.lower() for s in getattr(opsi, "staf_list", [])]
    for spes in sumber:
        kanal, mentah, info, hitung = baca_berkas(spes, opsi)
        n_awal = len(item)
        if info["jenis"] == "whatsapp":
            meta["pengirim"][kanal] = hitung
            nama = list(hitung)
            for tgl, pengirim, isi in mentah:
                if pengirim is None or RE_SISTEM_TEKS.search(isi) or RE_PENGIRIM_MEDIA.fullmatch(isi.strip()):
                    dibuang["pesan sistem/media"] += 1
                    continue
                if any(s in pengirim.lower() for s in staf):
                    dibuang["pesan staf"] += 1
                    continue
                isi = RE_PENGIRIM_MEDIA.sub("", isi).strip()
                item.append(dict(kanal=kanal, tgl=tgl, nilai=None, skala=None, isi=isi, nama=nama, peran="ulasan",
                                 identitas=(info["berkas"], pengirim.lower(), tgl), berkas=info["berkas"], min_kata=2))
        else:
            for b in mentah:
                if b.get("kosong"):
                    dibuang["jawaban kosong ('-', 'tidak ada')"] += 1
                    continue
                item.append(dict(kanal=b.get("kanal") or kanal, tgl=b["tgl"], nilai=b["nilai"], skala=b["skala"], isi=b["isi"], nama=(),
                                 peran=b.get("peran", "ulasan"), kolom=b.get("kolom"),
                                 identitas=(info["berkas"],) + b["identitas"] if b.get("identitas") else None, berkas=info["berkas"],
                                 min_kata=1 if b.get("peran") == "saran" else 2))
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
        if not bersih or len(re.findall(r"\w+", bersih)) < it["min_kata"] or not re.search(r"[a-z]", bersih):
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
        hasil_item.append({"kanal": it["kanal"], "bulan": bulan_dari(it["tgl"]),
                           "bintang": int(round(it["nilai"])) if it["nilai"] is not None and it["skala"] == 5 else None,
                           "nilai_0_10": it["nilai"] if it["skala"] == 10 else None, "peran": it["peran"],
                           "teks": anonim, "sentimen": sent, "tema": {k: sorted(v) for k, v in per_tema.items()}})
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
    return hasil_item, tema, dict(dibuang), meta


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
    kata = Counter(w for i in tanpa for w in re.findall(r"[a-z]{4,}", normalkan(i["teks"])) if w not in STOP)
    nps = None
    nilai10 = [v for s_ in meta.get("sumber", []) for v in s_.get("nilai_baris", [])]
    if not nilai10 and not meta.get("sumber"):
        nilai10 = [i["nilai_0_10"] for i in hasil_item if i.get("nilai_0_10") is not None]
    if nilai10:
        pro = sum(1 for v in nilai10 if v >= 9)
        det = sum(1 for v in nilai10 if v <= 6)
        nps = {"responden": len(nilai10), "promotor_9_10": pro, "pasif_7_8": len(nilai10) - pro - det, "detraktor_0_6": det,
               "nps": round((pro - det) * 100.0 / len(nilai10), 1), "indikatif": len(nilai10) < 30}
    return {
        "versi_script": VERSI, "total_masukan": n, "dibuang": dibuang,
        "sumber": [{k: v for k, v in s.items() if k in ("berkas", "kanal", "jenis", "kolom_teks", "kolom_nilai", "skala_nilai",
                                                          "kolom_tanggal", "baris", "responden", "catatan")} for s in meta.get("sumber", [])],
        "peringatan": peringatan,
        "per_kanal": dict(kanal.most_common()), "sentimen": {k: sent.get(k, 0) for k in ("positif", "netral", "negatif")},
        "nps": nps,
        "per_bulan": bulan_n,
        "tanpa_tanggal": sum(1 for i in hasil_item if not i["bulan"]),
        "data_kecil": n < 30,
        "tema": daftar,
        "belum_terklasifikasi": {"jumlah": len(tanpa), "persen": round(len(tanpa) * 100.0 / n, 1) if n else 0.0,
                                  "kata_teratas": [k for k, _ in kata.most_common(8)],
                                  "contoh": [potong(i["teks"]) for i in tanpa]},
    }


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
                ('"%s"' % s["kolom_tanggal"]) if s.get("kolom_tanggal") else "-"))
        else:
            out.append("Sumber %s (%s): %s" % (s["berkas"], s["kanal"], "chat WhatsApp" if s["jenis"] == "whatsapp" else "teks tempelan"))
    out.append("Kanal: " + ", ".join("%s %d" % (k, v) for k, v in r["per_kanal"].items()))
    s = r["sentimen"]
    if n:
        out.append("Sentimen: positif %d (%.1f%%), netral %d (%.1f%%), negatif %d (%.1f%%)" % (
            s["positif"], s["positif"] * 100.0 / n, s["netral"], s["netral"] * 100.0 / n, s["negatif"], s["negatif"] * 100.0 / n))
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
    out.append("\n## Perlu dibaca agent\n")
    out.append("Tanpa tema terdeteksi: %d (%.1f%%). Kata teratas: %s" % (b["jumlah"], b["persen"], ", ".join(b["kata_teratas"]) or "-"))
    out += ["- \"%s\"" % c for c in b["contoh"][:maks_tanpa_tema]]
    if len(b["contoh"]) > maks_tanpa_tema:
        out.append("- ... +%d lainnya: lihat --format json atau CSV --simpan-anonim" % (len(b["contoh"]) - maks_tanpa_tema))
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
    ap.add_argument("--skala", choices=["5", "10"], help="Paksa skala kolom nilai: 5 (bintang 1-5) atau 10 (nilai 0-10/NPS)")
    ap.add_argument("--buang-teks-sama", action="store_true",
                    help="Buang teks yang sama persis per kanal walau dari pembeli berbeda (bawaan: hanya baris identik yang dibuang)")
    ap.add_argument("--tema", help="File JSON tema/kata tambahan (lihat templates/tema-*.json)")
    ap.add_argument("--contoh", type=int, default=3)
    ap.add_argument("--min-bulan", type=int, default=5, help="Minimal masukan per bulan agar tren dihitung (default 5)")
    ap.add_argument("--format", choices=["teks", "json"], default="teks")
    ap.add_argument("--simpan-anonim", help="Simpan data yang SUDAH disamarkan ke CSV ini (kanal,bulan,bintang,nilai_0_10,sentimen,tema,teks)")
    opsi = ap.parse_args(argv)
    opsi.staf_list = [s.strip() for s in opsi.staf.split(",") if s.strip()]
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
                    w.writerow(["kanal", "bulan", "bintang", "nilai_0_10", "sentimen", "tema", "teks"])
                    for i in hasil_item:
                        n10 = i.get("nilai_0_10")
                        w.writerow([i["kanal"], i["bulan"] or "", i["bintang"] or "",
                                    "" if n10 is None else ("%g" % n10), i["sentimen"], ";".join(sorted(i["tema"])), i["teks"]])
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
