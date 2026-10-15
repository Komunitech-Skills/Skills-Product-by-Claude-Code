# Riwayat perubahan — crm-wa

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.11 (2026-10-15)
- Tindak lanjut verifikasi rujukan aturan (dicek 15 Oktober 2026; sumber yang dibuka: Kebijakan WhatsApp Business https://www.whatsapp.com/legal/business-policy, dialihkan ke https://whatsappbusiness.com/policy/, tertulis diperbarui 23 Sep 2026; teks UU 27/2022 PDP Pasal 20–21 di JDIH Kemkomdigi https://jdih.komdigi.go.id/produk_hukum/view/id/832/t/undangundang+nomor+27+tahun+2022; halaman JDIH BPK https://peraturan.bpk.go.id/Details/229798/uu-no-27-tahun-2022 menolak akses otomatis/HTTP 403 saat dicek). Logika script tidak berubah (hanya konstanta VERSI disamakan ke 1.0.11). Perilaku agent bertambah di aturan 10 (menanyakan tanggal & sumber persetujuan sebelum memasang `setuju-promo`); perilaku ini belum diuji ulang di OpenClaw.
- README "Yang perlu Anda tahu": dipertegas **mode Copilot** (AI menyiapkan draf, pemilik yang mengirim satu per satu; bukan bot balas otomatis, bukan auto-blast) dan beda **daftar tautan wa.me untuk dikirim sendiri** dengan **WhatsApp Business Platform (API) resmi** (kiriman otomatis/massal resmi tersedia lewat Platform itu, dengan template pesan disetujui, opt-in penerima, permintaan berhenti dihormati; bukan lewat WhatsApp Web/OpenClaw). Baris "Kurang cocok" dan FAQ kirim massal ikut menyebut jalur resmi itu tanpa mengklaim itu satu-satunya jalur resmi.
- README: catatan label `setuju-promo` = catatan persetujuan promo; simpan tanggal & sumber persetujuan di catatan kontak (UU 27/2022 Pasal 20–21), dengan disclaimer bukan nasihat hukum.
- Koreksi klaim melebihi sumber: frasa "(biasanya) melalui penyedia resmi" dihapus dari README (butir wa.me vs Platform, FAQ kirim massal), SKILL.md (Kapan TIDAK digunakan) dan catatan ini, karena Kebijakan WhatsApp Business tidak menyatakan usaha umum wajib lewat penyedia. Kalimat README "agent akan menanyakannya" dilunakkan menjadi "skill ini mengarahkan agent untuk menanyakannya" karena perilaku itu belum diuji ulang. Tanggal cek sumber ditambahkan pada rujukan kebijakan dan UU di README/SKILL.md.
- SKILL.md: "Kapan TIDAK digunakan" menjelaskan bahwa kiriman otomatis/massal resmi tersedia lewat WhatsApp Business Platform (bukan lewat WhatsApp Web/OpenClaw) bila pengguna memintanya; aturan 10 meminta agent menanyakan tanggal & sumber persetujuan sebelum memasang `setuju-promo`; Batasan menyebut "WhatsApp Business API (Platform resmi Meta)".

## Catatan revisi 1.0.10 (2026-10-02)
- Revisi putaran 2 pada aturan promo (SKILL.md butir 10): chat broadcast/blast di dalam marketplace ke pembeli yang belum opt-in ikut dilarang karena berisiko melanggar kebijakan platform. Yang masih boleh hanya voucher toko atau fitur promo resmi platform yang berbasis pengikut/opt-in, atau ajakan opt-in di kemasan.

## Catatan revisi 1.0.9 (2026-10-02)
- Temuan uji gabungan paket Toko Online: permintaan "daftar pelanggan buat promo" tidak memicu skill ini, dan rujukan ke `broadcast-wa` (tidak ada di paket Toko Online) membingungkan.
- Pemicu baru: "daftar pelanggan buat promo", "data pelanggan", "kontak pembeli". Aturan 10: promo hanya ke kontak berlabel `setuju-promo`; pembeli marketplace default belum setuju; tanpa broadcast (termasuk WhatsApp Business) ke kontak yang belum setuju.

## Catatan revisi 1.0.8 (2026-10-02)
- Temuan rendah dari uji ulang OpenClaw: kalimat pembuka draf perkenalan kini bervariasi (stabil per kontak) agar tidak terdengar kaku.
- Draf untuk banyak kontak ("semua kontak", "semua prospek") hanya untuk kontak yang aktif. Kontak tahap `batal` (termasuk yang catatannya "minta jangan dihubungi") dikecualikan dan alasannya disebut. Tetap satu draf per kontak, tidak pernah kirim massal. Versi script naik ke 1.0.8.

## Catatan revisi 1.0.7 (2026-10-02)
- Revisi identitas usaha: satu database untuk satu usaha. Di awal sesi agent menjalankan `info` dan mencatat profil aktif (nama usaha dan pengirim). Bila pengguna menyebut usaha atau pemilik yang berbeda, agent berhenti sebelum mencatat apa pun dan menanyakan pilihan (database terpisah atau tetap). `info` kini menampilkan baris Usaha dan Pengirim.

## Catatan revisi 1.0.6 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.5 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.4 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).
- Uji pengamanan: gerbang konfirmasi terverifikasi (catatan di `examples/HASIL-UJI.md`).

## Catatan revisi 1.0.3 (2026-09-29)
- Gerbang konfirmasi dipertegas: perubahan besar (`init`, `impor`, `hapus`, `gabung`, `restore`) hanya ditampilkan sebagai pratinjau (untuk `init` beserta lokasi file database), lalu agent berhenti dan baru melanjutkan setelah pengguna membalas "ya" di pesan berikutnya. Agent tidak menampilkan sintaks perintah ke pengguna awam.
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan. Versi script naik ke 1.0.3.

## Catatan revisi 1.0.2 (2026-09-25)
- Perawatan temuan rendah dari uji ulang v1.0.1 (9/10): draf pesan kini memotong di titik, mengenali "sejuta", tidak salah memotong koma desimal ("1,5 juta"), dan membuang kata "rupiah"; kutip (`"`) yang tak tertutup di CSV tidak lagi menelan baris berikutnya tanpa kabar; kontak impor tanpa tanggal masuk disebut di pratinjau; pesan "jadwal prospek lama diganti" tidak lagi muncul pada kontak yang baru dibuat. 57 tes lulus.

## Catatan revisi 1.0.1 (2026-09-24)
- Revisi dari uji independen pertama (6/10): pemulihan (`restore`) kini aman saat database rusak (tahan 9 jenis kerusakan pada uji ulang 8/10), deal tidak lagi dianggap "telat", dan nama yang ambigu ditanyakan dengan daftar pilihan (kode, nama, 4 digit akhir nomor, tahap).
- Kolom kebutuhan hanya berisi nama produk/jasa; angka rupiah dan teks setelah koma dibuang dari draf dan pengguna diperingatkan. Rujukan laporan keuangan diarahkan ke `laporan-keuangan-emkm`.

## Catatan revisi 1.0.0 (2026-09-24)
- Rilis awal (uji internal): CRM lokal berbasis chat WhatsApp (prospek, ditawar, deal) dengan database SQLite, draf pesan dan tautan wa.me yang dikirim manusia, rekap, dan jadwal ringkasan pagi.
