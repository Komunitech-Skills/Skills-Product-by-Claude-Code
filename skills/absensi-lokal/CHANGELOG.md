# Riwayat perubahan — absensi-lokal

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

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
- Teks yang bisa sampai ke pemilik usaha dibersihkan dari jargon: "tap" menjadi "catatan scan/jam masuk-pulang", "perintah lembur" dan "--gaji-pokok/--catatan" dihapus dari pesan PERLU DICEK dan catatan lembur, pesan "belum ada data absen" tanpa istilah impor/tap, dan teks pembuatan buku absensi tidak lagi memuat alamat folder. Ditambah uji regresi (`tests/uji_regresi.py`: kelas `UjiRekapCepat` dan `UjiBahasaChat`; kini 64 uji).

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
