# Riwayat perubahan — kasir-lokal

Catatan teknis per versi.

## Catatan revisi 1.1.8 (2026-10-17)
Temuan uji di bot Telegram asli (17 Okt 2026): skor tanpa skill 7,5 dan dengan skill 6,5 (belum lulus). Angka sudah benar; yang kurang adalah cara hasilnya sampai ke pemilik toko di chat.
- Struk tidak sampai ke chat (hanya file di komputer bot) -> setelah nota tersimpan, hasil `jual --ya` selalu memuat `struk_teks` (blok kode, 32 kolom untuk kertas 58 mm, 48 untuk 80 mm; isinya sama persis dengan `struk --teks`). Teks `jual --ya` kini ringkas (nomor nota, total, kembalian, catatan) lalu struknya. Pratinjau `jual` juga membawa `struk_teks` agar nomor dan isi struk bisa dicek sebelum disimpan. File struk siap cetak (HTML) hanya bila pengguna minta cetak atau memakai komputer yang sama; di kanal chat tanpa menyebut lokasi file.
- Hasil baru muncul di giliran kedua dan asumsi tampil seperti fakta -> perintah baru `mulai` (pemakaian pertama): daftar produk + pengaturan toko + penjualan pertama dalam SATU pesan konfirmasi, lengkap dengan struk teks; pengguna cukup membalas "ya" sekali. Pengaturan yang belum disebut pengguna (pajak, ukuran kertas, stok, zona jam, alamat/telepon) ditampilkan sebagai "Saya anggap - koreksi bila beda" (`asumsi` di JSON), bukan sebagai fakta. Pratinjau dan penyimpanan dicoba lebih dulu di salinan sementara: bila ada yang gagal (produk tak dikenal, pembayaran kurang), buku kasir asli tidak tersentuh.
- Istilah teknis ke pengguna ("database", "dipetakan", "sistem kasir", "struk HTML", "file lokal") -> SKILL.md kini mewajibkan bahasa awam ("buku kasir", "daftar produk", "struk siap cetak"); pengingat kasir belum dibuka dipersingkat dan tidak lagi menyebut nama perintah atau opsi.
- Kata "struk" tidak pernah dibuang dari nama barang -> permintaan struk di kalimat penjualan ("terus bikinin struknya ya") kini dibuang hanya bila seluruh segmen/kalimat penutupnya permintaan struk, atau sebagai ekor di segmen bayar/diskon, atau ekor dengan kata kerja berimbuhan (bikinin/buatin/cetakin/kirimin) di segmen barang. Toko perlengkapan kasir/ATK yang menjual "kertas struk" atau "printer struk" tetap mendapat produk yang benar (ini regresi di draf 1.1.8 yang belum dirilis; 1.1.7 tidak terdampak). Ucapan penutup yang lebih beragam ikut diterima ("kirim struknya ke sini ya", "struknya kirim ya", "... bayar tunai 100rb. Bikinin struknya ya", titik di akhir kalimat). "Struk 58mm" di dalam `--pesan` tetap ditolak jelas; ukuran kertas lewat `--kertas`.
- Awalan "Tolong catat penjualan:" / "catat penjualan" / "Penjualan:" di `--pesan` kini diabaikan (sebelumnya dibaca sebagai nama barang dan ditolak dengan saran "Kopi Hitam; Kopi Susu" yang membingungkan). SKILL.md menegaskan bahwa `--pesan` hanya berisi barang, diskon, dan bayar.
- Pesan "buku kasir belum ada" kini menunjuk ke `mulai --produk FILE` (pemakaian pertama dengan file produk) dan baru `init` bila tanpa file produk, agar agent tidak kembali ke alur bertahap lama. Kata "database" tidak lagi dipakai di pesan itu.
- SKILL.md langkah A.3: jawaban yang hanya membenarkan asumsi dan minta simpan ("tanpa pajak, 58mm, ..., simpan aja") berarti setuju, jalankan perintah sama + `--ya` tanpa pratinjau ketiga; pratinjau baru hanya bila ada yang berbeda dari asumsi.
- Pengingat "kasir belum dibuka" kini satu kalimat dan tidak lagi berkata "nota tetap tersimpan" (pratinjau berbunyi "belum ada yang disimpan"); begitu pula pengingat "kasir sudah ditutup".
- Ditambah uji regresi `UjiV118` (19 uji): struk teks ikut hasil `jual`, lebar 32/48 kolom, `mulai` (pratinjau tidak menulis apa pun, asumsi, simpan sama dengan pratinjau, gagal tidak meninggalkan buku setengah jadi, tanpa pesanan), pengingat singkat, kesamaan nomor versi di semua berkas, "struk" di nama barang (katalog Kertas/Kertas Struk/Printer Struk/Printer Inkjet), ucapan penutup struk, awalan "catat penjualan", petunjuk buku belum ada, pengingat satu kalimat, jawaban sama dengan asumsi, dan kecocokan jumlah uji di CHANGELOG. Total 84 uji di `uji_regresi.py` (ditambah 7 di `uji_rekap_nota.py`).

## Catatan revisi 1.1.7 (2026-10-03)
- Jalur baru "rekap dari nota yang DITEMPEL di chat" (tanpa database kasir): script `scripts/rekap_nota.py` menghitung omzet, porsi per menu, jumlah nota per menu, rincian per cara bayar, dan mencocokkan uang laci. Nota bertanda BATAL/void dikecualikan, bon dipisah dari uang masuk.
- Ada "RINGKASAN SIAP TEMPEL untuk grup karyawan" yang hanya berisi angka gabungan, tanpa nama/nomor pelanggan dan tanpa bon per orang. Ini draf: pemilik yang mengirim ke grup.
- Pemicu baru di SKILL.md ("ini nota hari ini, rekap + cocokkan laci + bikinin laporan buat grup"), uji `tests/uji_rekap_nota.py`, dan rujukan di `references/perintah.md`.

## Catatan revisi 1.1.6 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.1.5 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.1.4 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.1.3 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan; bila kanal belum siap atau perintah ditolak, agent berhenti dan memberi langkah persiapan.

## Catatan revisi 1.1.2 (2026-09-26)
- Pembeli yang belum bayar (bon/utang) kini diarahkan ke skill `buku-piutang`, karena kasir hanya mencatat penjualan yang sudah dibayar. Bila `buku-piutang` belum terpasang, cara lama (buat tagihan dengan `buat-invoice`) tetap bisa dipakai. Diperbarui di SKILL.md, README, dan `references/perintah.md`.

## Catatan revisi 1.1.1 (2026-09-24)
- Menutup celah "formula injection" CSV: teks yang diawali tanda minus tidak lagi bisa dibaca spreadsheet sebagai rumus. Ditambah uji regresi.
- Uji ulang v1.1.1: skor 9/10, mode PBJT diverifikasi pada 900 nota.

## Catatan revisi 1.1.0 (2026-09-24)
- Mode pajak PBJT (Pajak Barang dan Jasa Tertentu, UU 1/2022); dukungan satuan barang; penanganan zona waktu; dan larangan memanipulasi nota.

## Catatan revisi 1.0.0 (2026-09-24)
- Rilis awal (uji internal): kasir UMKM satu outlet di komputer pemilik dengan database lokal, dioperasikan lewat chat.
