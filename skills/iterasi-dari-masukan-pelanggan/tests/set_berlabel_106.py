"""Set berlabel v1.0.6 buatan pembuat (kalimat BARU, domain yang belum dipakai set sebelumnya: gym, villa/hotel, rental mobil/motor,
jasa pindahan, apotek, servis laptop/AC, renovasi, travel, antar-jemput sekolah, laundry koin, tur, percetakan).
Ditulis SEBELUM kode 1.0.6 diubah; label tidak diubah sesudahnya. Dipakai tests/uji_regresi_106.py.

(teks, bintang 1-5 atau None, label): label None = bukan keluhan; set = keluhan dengan tema yang wajib tertandai (set() = cukup
tertangkap sebagai keluhan ATAU masuk "Perlu dibaca agent" - tidak boleh hilang diam-diam).
Semua kalimat tanpa bintang/NPS (teks saja) - kelemahan terbesar yang terukur di uji buta 1.0.5.
DEV     = dipakai selama perbaikan (risiko overfitting: aturan dirancang sambil melihat kalimat ini).
HOLDOUT = dijalankan SEKALI setelah aturan selesai; kegagalannya dicatat apa adanya (KNOWN_GAGAL_HOLDOUT di uji_regresi_106.py).
SAMAR_DEV / SAMAR_HOLDOUT = (teks, kata, harus_tersamar) untuk penyamaran.
"""
DEV = [
    # frekuensi / kekurangan
    ("handuk di villa jarang diganti", None, set()),
    ("toilet di gym jarang dibersihkan", None, {"kebersihan"}),
    ("admin jarang balas chat kalau weekend", None, {"layanan"}),
    ("lantai kamar jarang disapu", None, set()),
    ("kurirnya jarang telat, paket selalu aman", None, None),
    ("jarang banget nemu apotek selengkap ini", None, None),
    # keterlambatan berangka
    ("tukang pindahan datang telat 3 jam tapi kerjanya cepat", None, {"pengiriman"}),
    ("jadwal check in molor 2 jam, resepsionis ramah sih", None, set()),
    ("terlambat 45 menit dari jam janjian, supirnya sopan", None, {"pengiriman"}),
    ("sampai lebih cepat 2 hari dari estimasi", None, None),
    ("telat 10 menit karena macet, wajar kok", None, None),
    # negasi atas kata positif
    ("tidak ada satu pun obat yang sesuai resep", None, set()),
    ("dari 5 lampu tidak ada yang terang", None, set()),
    ("kipas angin di kamar tidak ada yang nyala", None, set()),
    ("AC mobil rentalnya ga dingin sama sekali", None, {"fasilitas"}),
    ("kamarnya ber-AC tapi AC nya tidak dingin", None, {"fasilitas"}),
    ("es teh nya dingin segar, AC ruangan juga dingin", None, None),
    ("tidak ada yang ramah di meja resepsionis", None, {"layanan"}),
    ("tidak ada yang rusak, semua sesuai", None, None),
    ("kurang dingin AC nya", None, {"fasilitas"}),
    # takut X, ternyata aman
    ("awalnya takut kacanya pecah, ternyata aman sampai rumah", None, None),
    ("khawatir telat karena hujan, eh ternyata datang lebih awal", None, None),
    ("sempat ragu barangnya palsu, ternyata original", None, None),
    ("takut telat, ternyata beneran telat 2 jam", None, {"pengiriman"}),
    ("was was kardusnya penyok ternyata utuh semua", None, None),
    # keluhan bertema tanpa kata keluhan jelas
    ("3 minggu servis laptop belum selesai", None, set()),
    ("dijanjikan 2 hari, sudah seminggu belum kelar", None, set()),
    ("biaya parkir tidak dijelaskan dari awal", None, set()),
    # sindiran tanpa nilai
    ("Mantap, pesanan baru dikirim setelah 5 hari 🙏", None, set()),
    ("Keren, chat saya dianggurin 2 hari 👍", None, set()),
    # pujian (penjaga keluhan palsu)
    ("pelatihnya sabar, jadwal selalu tepat", None, None),
    ("proses cepat, 2 hari sudah beres", None, None),
    ("tidak ada biaya tersembunyi, semua dijelaskan di awal", None, None),
    ("belum pernah kecewa belanja di sini", None, None),
    ("kamar bersih, handuk diganti tiap hari", None, None),
]

HOLDOUT = [
    ("kolam renangnya jarang dikuras, airnya keruh", None, set()),
    ("CS nya jarang ngangkat telepon", None, set()),
    ("sopir travel telat 90 menit jemputnya", None, {"pengiriman"}),
    ("pengerjaan renovasi molor 2 minggu dari kontrak", None, set()),
    ("tidak ada satupun kursi yang nyaman di ruang tunggu", None, {"fasilitas"}),
    ("air panas di kamar mandi gak panas", None, set()),
    ("kulkas di kamar gak dingin", None, set()),
    ("takut barangnya lecet, ternyata dibungkus rapi banget", None, None),
    ("sempat khawatir ukurannya kekecilan, ternyata pas", None, None),
    ("ragu awalnya karena murah, ternyata awet", None, None),
    ("jarang telat, admin juga fast respon", None, None),
    ("sudah 10 hari laporan kerusakan belum ditindaklanjuti", None, set()),
    ("kamar hotel jarang dirapikan selama kami menginap", None, set()),
    ("antar jemput sekolah terlambat 30 menit hampir tiap hari", None, set()),
    ("mantul, datang lebih cepat 1 hari 👍", None, None),
    ("tidak ada yang bisa dipakai dari 3 charger itu", None, set()),
    ("Wah hebat, refund saya diproses setelah 3 minggu 🙏", None, set()),
    ("stafnya tidak pernah senyum", None, {"layanan"}),
    ("kasurnya empuk, tidak ada kutu", None, None),
    ("pemandu tur jarang menjelaskan, lebih banyak main hp", None, set()),
    ("hasil cetak tidak ada yang rapi", None, set()),
    ("was-was pengiriman lama, ternyata 2 hari sudah sampai", None, None),
    ("rental motor datang telat 1 jam tanpa kabar", None, {"pengiriman"}),
    ("tidak ada kendala sama sekali, admin ramah", None, None),
    ("mesin cuci di laundry koin jarang berfungsi", None, set()),
]

SAMAR_DEV = [
    ("anaknya dimarahi di depan teman2nya", "teman2nya", False),
    ("harganya ga dimahal2in", "dimahal2in", False),
    ("mantap pak lanjutkan", "lanjutkan", False),
    ("siap bu kirimkan", "kirimkan", False),
    ("makasih mas dibantu", "dibantu", False),
    ("anak2ku suka banget", "anak2ku", False),
    ("oke kak diproses", "diproses", False),
    ("makasih bu ratna", "ratna", True),
    ("halo mas bimo", "bimo", True),
    ("pesanan kode ORD2026XY99 belum datang", "ORD2026XY99", True),
    ("resi JX1234567890 belum gerak", "JX1234567890", True),
]

SAMAR_HOLDOUT = [
    ("hati2 ya kak, barangnya pecah belah", "hati2", False),
    ("mainannya dibanting2in anak saya", "dibanting2in", False),
    ("sip mbak teruskan", "teruskan", False),
    ("makasih pak arkan", "arkan", True),
    ("bu melati mohon dicek", "melati", True),
    ("kode booking BK88TRX21 tidak muncul", "BK88TRX21", True),
]
