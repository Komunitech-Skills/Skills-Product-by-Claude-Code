# Riwayat perubahan — kasir-lokal

Catatan teknis per versi.

## Catatan revisi 1.1.13 (2026-10-27)
Uji Telegram gelombang 29 pada 1.1.12: 6,5 → 7,5 (BELUM); satu pesan internal ("jalankan dengan argumen identik plus --ya") bocor lagi setelah balasan "ya". `CATATAN_PRATINJAU` kini diawali penanda "CATATAN INTERNAL, jangan dikutip" dan tanpa kalimat perintah. Angka tidak diubah. BELUM diuji ulang di bot asli.

## Catatan revisi 1.1.12 (2026-10-27)
Memperbaiki temuan verifikator atas 1.1.11. BELUM diuji ulang di bot Telegram asli; hanya uji otomatis. Angka tidak diubah.
- `kasir.py`: `CATATAN_PRATINJAU` dan catatan pemakaian pertama ditulis netral (tanpa "setuju" dan tanpa kalimat "jalankan perintah sama persis + --ya") karena catatan itu dikirim di setiap pratinjau dan bisa ditiru model.
- SKILL.md: aturan keamanan poin 2, langkah A.3, dan alur penjualan tidak lagi memuat kalimat perintah yang bisa disalin. Balasan setelah "ya" = `teks` (struk sudah di dalamnya); `struk_teks` hanya bila `teks` tidak memuatnya, tidak dua kali.
- Uji baru: `test_120` (varian frasa di SKILL.md), `test_121` (catatan_agent bebas frasa), `test_122` (struk tidak dua kali). Versi 1.1.12 di script dan dokumen. Kelas `UjiV1111` (9 uji). Total 116 uji di `uji_regresi.py` (ditambah 7 di `uji_rekap_nota.py`).

## Catatan revisi 1.1.11 (2026-10-27)
Perbaikan dari uji bot Telegram gelombang 28 pada 1.1.10 (skor dengan skill 7,5; tanpa skill 6,5). Angka benar dan tidak diubah (subtotal 39.000, diskon 3.900, total 35.100, kembalian 64.900). Yang bocor: saat pemilik membalas "ya", bot menulis satu pesan terpisah berisi narasi proses dan opsi perintah (campuran bahasa Inggris) ke chat. Versi ini BELUM diuji ulang di bot Telegram asli; yang sudah dijalankan hanya uji otomatis.
- SKILL.md, bagian "Cara bicara", poin 6 baru: setelah pemilik membalas "ya", penyimpanan dikerjakan diam-diam dan satu-satunya balasan adalah `teks` hasil dan `struk_teks`. Kalimat tentang perintah, opsi, persetujuan, proses, atau instruksi kerja tidak pernah ditulis ke chat. Aturannya ditulis netral, tanpa mengutip kalimat contoh yang bisa ditiru model.
- SKILL.md langkah A.3: "hasil singkat" diganti "hanya hasilnya (`teks` + `struk_teks`)" agar tidak bertentangan dengan poin 6.
- Ditambah uji regresi `UjiV1111` (6 uji): aturan ada, SKILL.md tanpa kalimat bocor yang bisa disalin dan tanpa aturan lama yang bertentangan, poin baru tanpa opsi teknis, hasil simpan tanpa bahasa proses, versi dan dokumen sama. Total 113 uji di `uji_regresi.py` (ditambah 7 di `uji_rekap_nota.py`).

## Catatan revisi 1.1.10 (2026-10-26)
Memperbaiki temuan verifikator independen atas draf 1.1.9 (1.1.9 tidak pernah dirilis; isinya tetap tercatat di bawah). Versi ini BELUM diuji ulang di bot Telegram asli; yang sudah dijalankan hanya uji otomatis. Angka tidak diubah.
- Galat `error` yang masih memuat nama perintah dibersihkan: "Kasir belum dibuka" (`kas`) dan "Kasir sudah dibuka" (`buka-kasir` dua kali) kini berbahasa awam; petunjuk perintahnya pindah ke `catatan_agent`.
- Galat `error` yang masih memuat jalur berkas dibersihkan: daftar produk tidak ketemu/kosong, cadangan tidak ketemu, dan "bukan buku kasir" (yang juga tidak lagi memakai kata "database"). Jalurnya pindah ke `berkas_csv_produk`, `berkas_backup`, `lokasi_buku`.
- Regresi frasa diperbaiki: kata kerja catat/input/rekam/masuk dibuang lagi bila diikuti angka ("catat 2 kopi hitam"), angka kata ("catat dua kopi hitam, bayar pas"), atau nama barang yang hanya cocok bila kata kerja dibuang ("catat kopi hitam 2, bayar pas"; dicoba hanya bila bacaan biasa tidak cocok ke produk mana pun). "masuk angin=2" dan "input data 1" tetap dibaca sebagai barang. Ini menggantikan catatan konsekuensi di 1.1.9 di bawah.
- Bunyi klaim diluruskan: pratinjau `jual`, `void`, `retur`, `restore` berakhir `Simpan? Balas "ya".`; pratinjau `mulai` berakhir `Balas "ya" kalau sudah sesuai.` (SKILL.md, README, CHANGELOG).
- Dokumen: `references/perintah.md` (`info` tidak lagi dikatakan menampilkan lokasi), checklist SKILL.md disamakan dengan poin 2, dan petunjuk "masuk --jenis retur-pembeli" di ekspor buku-stok dipindah ke `catatan_agent` (hanya bila ada retur sebagian).
- Galat database selain "terkunci" (mis. skema rusak) kini tidak berkata "sementara" dan detail teknisnya ada di `catatan_agent`, bukan di `error`.
- Ditambah uji regresi `UjiV1110` (12 uji). Total 107 uji di `uji_regresi.py` (ditambah 7 di `uji_rekap_nota.py`).

## Catatan revisi 1.1.9 (2026-10-26)
Perbaikan dari temuan uji bot Telegram 17 Okt 2026 pada 1.1.8 (balasan bot masih menempelkan instruksi agent dan jalur berkas ke chat pemilik). Versi ini BELUM diuji ulang di bot asli; yang sudah dijalankan hanya uji otomatis. Angka (total, pajak, kembalian, kas, rekap) tidak diubah dan sama dengan 1.1.8.
- Field yang ditempel ke chat (`teks`, `struk_teks`, pratinjau, `error`, `peringatan`) tidak lagi memuat instruksi agent, nama perintah/opsi (`--ya`, `--izinkan-duplikat`, `produk impor`, `kasir.py`, ...), atau jalur berkas. Pratinjau penjualan/void/retur/restore berakhir `Simpan? Balas "ya".` (pratinjau `mulai` berakhir `Balas "ya" kalau sudah sesuai.`)
- Instruksi untuk agent pindah ke field `catatan_agent` (mis. "jalankan perintah yang sama + --ya"). Jalur berkas pindah ke field terpisah yang TIDAK boleh ditempel ke chat kecuali pemilik memintanya: `lokasi_buku` (juga `db`), `berkas_struk` (juga `struk`/`file`), `berkas_backup` (juga `backup`), `berkas_csv`, `berkas_csv_produk`. Teks ke pemilik cukup berkata "tersimpan di komputer ini".
- Galat `mulai` saat buku sudah ada kini berbahasa awam (tanpa "produk impor"/"jual"); galat lain (alasan void/retur kosong, tarif pajak restoran, PKP, service charge, kas, stok tidak cukup, nota dobel, buku belum dibuat/bukan buku kasir/terkunci) juga dibersihkan dari nama opsi, petunjuknya pindah ke `catatan_agent`. Info, backup, restore, ekspor, dan rekap tidak lagi mencetak jalur berkas di `teks`.
- SKILL.md: satu aturan penyebutan berkas (di chat cukup "tersimpan di komputer ini"; jalur hanya bila pemilik minta atau jelas di komputer yang sama; file Word/struk dilampirkan bila kanal bisa); aturan di bagian "Cara bicara", langkah C, dan checklist disamakan.
- `POLA_AWALAN`: kata kerja "catat/input/rekam/masuk" hanya dibuang bila diikuti frasa dikenal ("catat penjualan", "input transaksi", dst.) atau titik dua ("catat: ..."). Produk seperti "Masuk Angin" atau "Input Data" ("masuk angin 2", "input data 1") tidak lagi dipotong. (Konsekuensi di draf ini, "catat 2 kopi susu" tidak lagi dipahami, dibalik di 1.1.10.)
- Ditambah uji regresi `UjiV119` (11 uji): pratinjau tanpa instruksi, jual/struk/mulai tanpa jalur, galat `mulai`, sapuan galat, backup/info/ekspor/rekap, awalan, produk "Masuk Angin"/"Input Data", angka sama dengan 1.1.8, jumlah uji di CHANGELOG, dan SKILL.md (satu aturan berkas, frontmatter). Total 95 uji di `uji_regresi.py` (ditambah 7 di `uji_rekap_nota.py`).

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
