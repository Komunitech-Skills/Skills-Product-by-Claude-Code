"""Set berlabel v1.0.7 buatan pembuat (kalimat BARU; domain yang belum dipakai set pembuat sebelumnya: fotografer/WO, MC & dekorasi
acara, kursus musik & les privat, skincare/krim, cleaning service, servis AC, jasa desain, sewa sound system, pijat panggilan, tur,
depo air, bunga papan, sewa kamera).
Ditulis SEBELUM kode 1.0.7 diubah; label tidak diubah sesudahnya. Dipakai tests/uji_regresi_107.py.

TEMA_DEV / TEMA_HOLDOUT: (teks, bintang, label, terlarang)
  label None = bukan keluhan; set = keluhan dengan tema yang wajib tertandai (set() = cukup masuk tabel keluhan ATAU "Perlu dibaca");
  terlarang = tema yang TIDAK boleh menghitung keluhan baris ini (mis. "pengiriman" untuk keterlambatan usaha jasa, "krim" != "kirim").
SINDIR_DEV / SINDIR_HOLDOUT: (teks, sindiran) - sindiran True = wajib masuk tabel keluhan atau [KELUHAN?] di "Perlu dibaca";
  False = pujian tulus yang memuat "baru/akhirnya/cuma/sampai N" (tidak boleh jadi keluhan/[KELUHAN?]).
SAMAR_DEV / SAMAR_HOLDOUT: (teks, kata, harus_tersamar).
DEV     = dipakai selama perbaikan (risiko overfitting: aturan dirancang sambil melihat kalimat ini).
HOLDOUT = dijalankan SEKALI setelah aturan selesai; kegagalannya dicatat apa adanya (KNOWN_GAGAL_* di uji_regresi_107.py).
"""
TEMA_DEV = [
    # usaha jasa: datang/telat/dikirim = jadwal/layanan, bukan pengiriman barang
    ("fotografernya datang telat 1 jam, sesi foto jadi mepet", None, {"waktu_tunggu"}, {"pengiriman"}),
    ("MC-nya datang terlambat, acara molor setengah jam", None, {"waktu_tunggu"}, {"pengiriman"}),
    ("kelas gitar sering mulai telat, gurunya baru datang 20 menit kemudian", None, {"waktu_tunggu"}, {"pengiriman"}),
    ("desain logo yang dikirim tidak sesuai brief", None, set(), {"pengiriman"}),
    ("laporan perkembangan anak jarang dikirim tutornya", None, set(), {"pengiriman"}),
    ("revisi mockup baru dikirim setelah 5 hari", None, {"waktu_tunggu"}, {"pengiriman"}),
    ("teknisi AC dijadwalkan jam 9, datang jam 1 siang", None, set(), {"pengiriman"}),
    ("tim cleaning service datang telat 2 jam", None, {"waktu_tunggu"}, {"pengiriman"}),
    # kebalikan: barang/paket/makanan tetap pengiriman walau ada kata acara
    ("paketnya telat 4 hari, kurir tidak ada kabar", None, {"pengiriman"}, set()),
    ("kue pesanan untuk acara ulang tahun datang telat 2 jam", None, {"pengiriman"}, set()),
    ("undangan yang dicetak dikirim lewat ekspedisi, sampai telat seminggu", None, {"pengiriman"}, set()),
    ("sound system untuk acara nikahan diantar telat, kurirnya nyasar", None, {"pengiriman"}, set()),
    ("katering untuk acara kantor datang telat 45 menit", None, {"pengiriman"}, set()),
    # typo/slang tidak boleh mengubah kata sah
    ("krimnya meleleh dan ada rambut di krimnya", None, {"keamanan"}, {"pengiriman"}),
    ("krim wajahnya bikin kulit perih", None, {"kualitas_produk"}, {"pengiriman"}),
    ("krim malamnya lengket di kulit", None, set(), {"pengiriman"}),
    ("buttercream dan krimnya enak, tidak terlalu manis", None, None, set()),
    ("sebelah kirinya penyok, kardusnya juga sobek", None, {"kemasan"}, {"pengiriman"}),
    ("anak saya kelas 2 SMP, tutornya sabar dan jelas", None, None, set()),
    ("les untuk anak SMA kurang interaktif", None, set(), {"pengiriman"}),
]

TEMA_HOLDOUT = [
    ("pemandu tur datang terlambat ke hotel, jadwal jadi berantakan", None, {"waktu_tunggu"}, {"pengiriman"}),
    ("materi kursus yang dikirim mentornya kurang lengkap", None, set(), {"pengiriman"}),
    ("tukang pijat panggilan telat 40 menit", None, {"waktu_tunggu"}, {"pengiriman"}),
    ("hasil edit video baru dikirim seminggu setelah acara", None, set(), {"pengiriman"}),
    ("dekorasi pelaminan telat dipasang, tamu sudah datang", None, set(), {"pengiriman"}),
    ("barang pesanan telat sampai 3 hari, resi tidak update", None, {"pengiriman"}, set()),
    ("galon air dari depo diantar telat terus", None, {"pengiriman"}, set()),
    ("nasi kotak untuk rapat datang telat setengah jam", None, {"pengiriman"}, set()),
    ("kiriman bunga papan untuk acara pernikahan telat datang", None, {"pengiriman"}, set()),
    ("krim sup jamurnya kental dan gurih", None, None, set()),
    ("krim pelembabnya bikin jerawatan", None, {"kualitas_produk"}, {"pengiriman"}),
    ("tutor les privat anak SMP sering ganti jadwal mendadak", None, set(), {"pengiriman"}),
    ("korset pelangsingnya jahitannya lepas", None, {"kualitas_produk"}, set()),
]

SINDIR_DEV = [
    ("Hebat min, chat dari kemarin baru dibalas hari ini 👍", True),
    ("Keren banget, 5 hari baru dijawab 👏", True),
    ("Salut deh, akhirnya dibalas juga setelah ditagih tiga kali", True),
    ("Mantap, pesan 10 cuma datang 7 👍", True),
    ("Luar biasa, nunggu sampai 3 jam buat servis ganti oli 🙃", True),
    ("Mantap, baru pesan tadi pagi sudah sampai siang ini 👍", False),
    ("Keren, sepatu barunya nyaman dipakai 👍", False),
    ("Alhamdulillah akhirnya nemu katering seenak ini, mantap", False),
    ("Top, cuma 1 jam servis sudah beres 👍", False),
    ("Mantap, kuenya masih enak sampai 3 hari", False),
]

SINDIR_HOLDOUT = [
    ("Wah keren, teknisinya baru muncul jam 4 sore padahal janji jam 10 👏", True),
    ("Sip, dikabari 2 minggu kemudian baru dikerjakan 🙂", True),
    ("Top markotop, antre sampai 2 jam cuma buat potong rambut 👍", True),
    ("Terima kasih banyak, refund akhirnya masuk setelah sebulan", True),
    ("Keren min, pesan 3 porsi cuma dikasih 2 🙃", True),
    ("Mantap, baru buka paket langsung wangi 👍", False),
    ("Keren, akhirnya ada katering sehat di kota ini", False),
    ("Top banget, cuma sehari sudah sampai 👍", False),
    ("Hebat, baru dipakai sekali noda langsung hilang", False),
]

SAMAR_DEV = [
    ("Mas telaten banget ngajarin anak saya", "telaten", False),
    ("Terima kasih kak sigap.", "sigap", False),
    ("Makasih bu cekatan!", "cekatan", False),
    ("Terima kasih Mas Telaten", "Telaten", False),
    ("Sewa Canon EOS R6 II dan lensa RF 50", "R6", False),
    ("Sony A7 IV nya ada jamur di sensor", "A7", False),
    ("iPhone 15 Pro Max nya mulus", "15", False),
    ("motor RX-King saya diservis rapi", "RX-King", False),
    ("Honda Beat B 4521 KJT sudah dijemput", "4521", True),
    ("mobilnya plat AB 1234 XY", "1234", True),
    ("mobil D1234ABC ditabrak di parkiran", "D1234ABC", True),
    ("Terima kasih Pak Heru", "Heru", True),
    ("makasih mas bagas.", "bagas", True),
]

SAMAR_HOLDOUT = [
    ("Makasih mbak cekatan dan ramah!", "cekatan", False),
    ("Terima kasih Kak Sabar dan telaten", "Sabar", False),
    ("Nikon Z6 II bodinya lecet", "Z6", False),
    ("Galaxy S23 FE nya mulus", "S23", False),
    ("plat motornya L 3456 AB", "3456", True),
    ("Mobil box B 9012 UCD", "9012", True),
    ("Terima kasih Bu Ratih.", "Ratih", True),
    ("makasih bang gesit.", "gesit", False),
]
