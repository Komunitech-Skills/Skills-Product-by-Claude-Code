# Riwayat perubahan — absensi-lokal

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.11 (2026-10-27)
- Dari pra-cek Telegram 1.0.10 (skor 8,5 / 9,5 / 5; angka dan "ya = simpan" selalu benar): 1 dari 3 run membuka dengan narasi yang mengutip SKILL.md ("Sesuai instruksi A0, kirim isi pesan apa adanya..."). Dugaan pemicu: kalimat larangan narasi dan label "A0". Kalimat larangan dihapus, label "A0" dihapus dan diganti judul netral "Rekap langsung dari file mesin" di SKILL.md/contoh/uji; rujukan antar-langkah ("langkah 4", "alur C", "bagian D", "A langkah 1(b)") diganti uraian biasa ("saat pengguna membalas ya atas tawaran simpan"), nama field `pesan` tidak lagi disebut di aturan balasan/daftar periksa, aturan balasan ditulis ringkas dan deklaratif ("Jawaban pertama = teks rekap...", "Jawaban = kalimat jumlah tersimpan persis bentuk ini"), balasan sesudah "ya" maks. dua kalimat (kedua hanya libur/izin atau orang tak dikenal). Uji: `UjiTanpaNarasiProses`, `UjiBalasanPenutupDanTanggalTelat`. Belum diuji ulang di bot asli.

## Catatan revisi 1.0.10 (2026-10-27)
- Dari pra-cek Telegram G28 (skor 7, TIDAK SIAP): setelah satu "ya", balasan bot dibuka dengan teks instruksi yang bocor ("Semua berhasil tersimpan sesuai alur A0 langkah 4. Balas sesuai skill: ..."), baru kalimat jumlah catatan. SKILL.md A0 langkah 4 kini memberi templat kalimat persis dan menyatakan itu seluruh balasan, tanpa menyebut nama langkah/alur/aturan/instruksi. Hanya teks SKILL.md yang berubah untuk temuan ini (script tidak punya field penutup); kepatuhan agent baru terbukti lewat uji bot asli, belum diuji ulang.
- Rekap kini menambah baris "Tanggal telat: 02/09, 15/09, ..." per karyawan bila telatnya 1-5 kali (lebih banyak: baris dilewati agar tetap ringkas). Field JSON baru `tanggal_terlambat`; hitungan tidak berubah. `examples/06` diperbarui.
- Setelah pra-cek G28 (27 Okt, 1 dari 2 run membuka balasan dengan narasi Inggris tentang proses): aturan A0 langkah 2 ditegaskan, balasan HANYA teks rekap lengkap siap kirim dari kalimat pertamanya, tanpa pembuka atau narasi proses. Uji: `UjiTanpaNarasiProses`. Belum diuji ulang di bot asli.
- Putaran verifikator berikutnya (tetap 1.0.10, belum dirilis; tidak dinaikkan lagi): aturan balasan penutup bertentangan dengan contoh. Kini satu kalimat jumlah + opsional satu kalimat kedua (libur/izin atau orang tak dikenal), maks. dua kalimat; `examples/06` diseragamkan ("sudah tersimpan", versi 1.0.10); contoh lama `examples/01` & `03` dan SKILL.md diberi keterangan baris "Tanggal telat". Uji: `test_06`-`test_08` kelas `UjiBalasanPenutupDanTanggalTelat`. Kepatuhan di bot asli belum diuji ulang.
- Versi dinaikkan dari 1.0.9 (sudah di HEAD) ke 1.0.10 (patch). Uji regresi: kelas `UjiBalasanPenutupDanTanggalTelat`.

## Catatan revisi 1.0.9 (2026-10-26)
- Dari uji Telegram asli gelombang A8 (skor 6,5 menjadi 7,5, verdik BELUM): rekap dan angkanya benar, tetapi saat pengguna membalas "ya" untuk menyimpan, bot bertanya ulang dan tidak menyimpan apa pun. Perbaikan ini hanya menutup penyebab itu; belum diuji ulang di bot Telegram asli. Putaran kedua (penilaian independen): butir "Buku belum ada" tidak lagi meminta "ya" kedua atas ringkasan baru; setelah tersimpan tidak ada rekap ulang atau pertanyaan baru (hanya bila diminta); orang tak dikenal di file tidak menghentikan penyimpanan (yang dikenal disimpan, orang itu disebut singkat); pertanyaan yang baru diajukan disebut "tadi", bukan "kemarin".
- Putaran ketiga (verifikator): `examples/06` ditulis ulang ke alur "satu ya = simpan" (tanpa ringkasan baru, tanpa "Betul?", tanpa rekap ulang); varian B memakai file Oktober sungguhan (`buat_csv_okt`, 128 catatan, Andi telat 41 menit; sebelumnya angka 121 salah). Pelanggan lama: satu "ya" atas tawaran memasukkan file langsung `impor-absen --ya`; orang tak dikenal tidak menghentikan simpan. Aturan WAJIB (no. 1-2) dan checklist diberi pengecualian eksplisit A0 langkah 4; alur C diberi catatan; "ya" bersama jawaban samping = simpan saat itu juga. Uji regresi: `test_07`-`test_10` (membaca SKILL.md dan examples/06 untuk aturan lama yang bertentangan) dan `test_14a`.
- SKILL.md A0 langkah 4: satu kata setuju ("ya", "iya", "boleh", "ok", "simpan") atas tawaran simpan berarti SIMPAN sekarang. Tidak boleh bertanya balik ("ya yang mana?") atau meminta persetujuan ulang; satu "ya" mencakup seluruh rangkaian simpan. Pertanyaan samping yang belum dijawab dibiarkan, hari kosong tetap "tanpa keterangan". Setelah selesai, balasan akhir satu kalimat berisi jumlah catatan dari script, tanpa lokasi file atau perintah.
- `rekap-cepat`: pertanyaan simpan kini memuat jumlah catatan dan berbunyi: Cukup balas "ya" bila mau; pertanyaan lain boleh dijawab nanti (berlaku untuk buku baru dan buku yang sudah ada). Hitungan rekap tidak diubah.
- Uji regresi: kelas `UjiYaTunggalSimpan` (jumlah catatan sama dengan yang dibaca script, kalimat penutup, satu pertanyaan simpan di akhir, aturan "ya" tunggal ada di SKILL.md, SKILL.md < 300 baris, frontmatter dua field). Aturan perilaku agent (tidak bertanya balik) hanya bisa dijaga lewat teks SKILL.md; kepatuhannya baru terbukti lewat uji bot asli.

## Catatan revisi 1.0.8 (2026-10-17)
- Dari pra-cek di bot Telegram asli (skor 7,0, angka sudah benar): balasan pertama dulu hanya berisi 5 pertanyaan dan menyebut alamat file database; rekap baru muncul setelah pengguna membalas "ya". Kini file mesin + permintaan rekap langsung dijawab dengan rekap di balasan pertama lewat perintah baru `rekap-cepat` (dihitung di memori, tidak membuat atau mengubah file apa pun): menampilkan asumsi yang dipakai (jam kerja, hari kerja, jam pulang Sabtu, kelonggaran telat, tanggal merah, daftar karyawan dari isi file), tanggal yang kosong untuk semua karyawan ("kemungkinan libur"), dan paling banyak 3 pertanyaan penutup (termasuk tawaran menyimpan). Opsi `--libur` untuk menjawab pertanyaan libur, `--pulang-hari-pendek` untuk Sabtu pulang lebih awal. Perhitungan telat/jam kerja/lembur tidak diubah.
- SKILL.md: bagian baru "Cara bicara di chat" (tanpa path, nama database/script, perintah, opsi, atau kode karyawan di chat; daftar pengganti istilah; pertanyaan maks. 3 di akhir; aturan memecah pesan panjang), A0 jalur cepat, langkah A.1 tidak lagi menanyakan lokasi simpan/kelonggaran telat/ID mesin di awal (maks. 3 pertanyaan bila belum ada data), persetujuan jadwal OpenClaw atas rencana berbahasa sederhana (bukan perintah teknis).
- Temuan verifikator independen (putaran 1) yang diperbaiki:
  - Pelanggan lama (buku absensi sudah ada): `rekap-cepat` kini memakai isi buku (karyawan, jadwal, kelonggaran telat, libur, izin/sakit/cuti, lembur disetujui; field `dari_buku`) alih-alih nilai bawaan, sehingga hasilnya sama dengan `rekap` dari buku; buku aslinya tidak diubah. Tawaran "simpan supaya bulan depan tinggal tambah file" diganti "masukkan file ini ke buku"; orang yang belum terdaftar ditanyakan.
  - Pola 6 hari dengan Sabtu pulang lebih awal: `--pulang-hari-pendek` masuk daftar opsi A0; baris "Sabtu dihitung hari kerja biasa" kini ditandai anggapan, dan bila hampir semua Sabtu pulang jauh lebih awal dari jadwal, script menanyakannya.
  - Contoh di SKILL.md dan `examples/06` memakai semua opsi yang disebut pengguna (`--hari-kerja 5 --masuk 08.00 --pulang 17.00 --istirahat 60`), sehingga hanya "tidak ada tanggal merah" yang ditulis anggapan.
  - Rute file mesin + lembur/upah/shift malam saat buku belum ada: A.1(a) hanya untuk rekap telat/bolong dengan satu jadwal; selebihnya satu pratinjau gabungan (A.1(b)).
  - Pesan panjang: field `pesan` (rekap-cepat, rekap, harian) memecah teks > 3.800 karakter di batas antar-karyawan; pertanyaan di pesan terakhir.
  - Istilah teknis di teks yang disalin: judul rekap "kelonggaran telat" (bukan "toleransi terlambat"), kode karyawan hanya tampil bila ada nama kembar, "Libur/tutup:" (bukan "Libur resmi: ... menurut Anda"), "(lihat CSV/JSON)" diganti kalimat biasa, teks rencana `init` dan `info` tanpa alamat folder atau nama field, pratinjau `catat`/`keterangan`/`lembur`/`hapus` tanpa kode karyawan, teks upah harian "6 hari kerja seminggu" (bukan "pola 6 hari").
  - `examples/01` ditulis ulang mengikuti alur baru (satu pratinjau gabungan, bahasa biasa, tanpa lokasi simpan, tanpa nama kolom/perintah); contoh 02–04 disesuaikan dengan teks rekap terbaru.
  - File yang mencakup lebih dari 62 hari (atau di luar bulan yang dipilih) kini diberi catatan "File berisi catatan dari ... sampai ..." di "Catatan dari file".
- Teks yang bisa sampai ke pemilik usaha dibersihkan dari jargon: "tap" menjadi "catatan scan/jam masuk-pulang", "perintah lembur" dan "--gaji-pokok/--catatan" dihapus dari pesan PERLU DICEK dan catatan lembur, pesan "belum ada data absen" tanpa istilah impor/tap, dan teks pembuatan buku absensi tidak lagi memuat alamat folder. Ditambah uji regresi (`tests/uji_regresi.py`: kelas `UjiRekapCepat` dan `UjiBahasaChat`; kini 64 uji; 1.0.9 menambah kelas UjiYaTunggalSimpan, total 76 setelah 1.0.9 diperbaiki lagi).

## Catatan revisi 1.0.7 (2026-10-03)
- Jalur baru "upah pekerja harian lepas" tanpa database (SKILL.md bagian F, `scripts/upah_harian.py`): menghitung upah mingguan/periode dari hari kerja, setengah hari, lembur, tambahan, dan potongan/kasbon yang diketik di chat. Tidak menyimpan apa pun.
- Lembur dicek terhadap minimum PP 35/2021 (upah sebulan = tarif harian x 25 untuk pola 6 hari atau x 21 untuk pola 5 hari, dibagi 173 per jam). Bila pemilik memakai tarif lembur sendiri yang lebih rendah dari minimum, script memberi peringatan dan menampilkan total versi minimum. `gaji-umkm` tetap untuk gaji bulanan. Uji `tests/uji_upah_harian.py`.

## Catatan revisi 1.0.6 (2026-10-01)
- Dari uji OpenClaw sebelum/sesudah: kini data karyawan selalu ditampilkan sebagai pratinjau dan baru disimpan setelah Anda membalas "ya"; tanggal yang kosong untuk semua karyawan ditandai "kemungkinan libur — konfirmasi" (bukan dianggap bolong per orang).

## Catatan revisi 1.0.5 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.0.4 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. `--y` tidak bisa dibaca sebagai `--ya`), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.3 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.0.2 (2026-09-29)
- Aturan kredensial & jadwal (SKILL.md dan `references/openclaw-jadwal.md`): agent tidak pernah mencari, membaca, atau menampilkan token/API key dari environment, file konfigurasi, atau riwayat. Jadwal hanya dibuat setelah pengguna membalas "ya" atas perintah dan jam yang ditunjukkan.

## Catatan revisi 1.0.1 (2026-09-24)
- Versi saat skill pertama masuk repo (lolos uji muat OpenClaw). Perbaikan kecil; rincian di riwayat git.

## Catatan revisi 1.0.0 (sebelum 2026-09-24)
- Rilis awal (uji internal).
