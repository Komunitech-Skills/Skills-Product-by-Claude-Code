# Riwayat perubahan — tagih-piutang

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.8 (2026-10-15)
- Verifikasi rujukan aturan (C31, 2026-10-15) — somasi: `references/regulasi.md` bagian 1 kini menyebut bahwa bila perjanjian/invoice sudah menetapkan jatuh tempo & akibat lalai, somasi terpisah bisa tidak wajib (Pasal 1238: "berdasarkan kekuatan dari perikatan sendiri") — advokat yang menilai. Klaim tentang yurisprudensi Mahkamah Agung soal somasi tidak dicantumkan karena sumbernya (URL/nomor putusan) tidak bisa dibuka dan ditelusuri. Batasan SKILL.md dan FAQ README diselaraskan; surat teguran tahap 6 tetap disarankan sebagai bukti.
- UU Perlindungan Konsumen: bagian baru `references/regulasi.md` bagian 4 (UU 8/1999 Pasal 18 — klausula baku terlarang batal demi hukum; relevan bila debitur konsumen perorangan/B2C, B2B umumnya KUHPerdata wanprestasi). FAQ README dan baris Batasan/Catatan hukum SKILL.md ditambah. Bagian "Jalur lanjutan" menjadi bagian 5.
- Bea meterai: catatan "perlu review" UU 10/2020 diganti hasil cek teks resmi PDF pajak.go.id: Pasal 3 ayat (2) huruf a & g, **Pasal 5** (tarif tetap Rp10.000), Pasal 8 ayat (1) huruf a angka 1 (terutang saat ditandatangani).
- Pasal 1250 KUHPerdata kini dikutip dari transkripsi naskah KUHPerdata di Wikisource (transkripsi komunitas, bukan terbitan resmi; halaman 226): bunga moratoir "baru wajib dibayar sejak diminta di muka Pengadilan, kecuali bila undang-undang menetapkan bahwa hal itu berlaku demi hukum". Frasa lama "kecuali para pihak menyepakati lain" dihapus karena tidak ada di pasal itu. Angka 6% per tahun dipisah sebagai klaim sumber sekunder (hukumonline: Staatsblad 1848 No. 22) bertanda *perlu review*; SKILL.md melarang menyebut angka 6% di pesan. Aturan "denda hanya bila disepakati tertulis" kini ditulis sebagai kebijakan skill, bukan bunyi Pasal 1250. README menambah Pasal 1250 di daftar dasar hukum.
- Gugatan sederhana: batas Rp500 juta (PERMA 2/2015 jo. 4/2019, Pasal 1 & 3) dicek lewat MARINews Mahkamah Agung (artikel 12 November 2025); naskah PERMA di JDIH MA tidak bisa dibuka otomatis, jadi tetap bertanda *perlu review naskah resmi* + saran memastikan ke advokat/pengadilan negeri.
- UU 8/1999 Pasal 18: kalimat di Batasan SKILL.md dan FAQ README diperhalus — yang batal demi hukum hanya klausula baku jenis yang disebut ayat (1) huruf a–h dan ayat (2), bukan semua syarat yang disiapkan penjual. `references/regulasi.md` bagian 4 menyebut contoh huruf g & ayat (2) dan rujukan Wikisource (transkripsi komunitas).
- Logika hitung tidak berubah; `VERSI` script → 1.0.8.

## Catatan revisi 1.0.7 (2026-10-10)
- Dari laporan uji OpenClaw v1.0.6: kolom pembayaran dengan judul bebas ("sdh bayar", "sudah dibayar", "terbayar", "DP", "uang muka", "cicilan", "paid", dan sejenisnya) kini dikenali; beberapa kolom pembayaran dijumlahkan; kolom "lunas" / "status bayar" menandai nota lunas. Dulu kolom itu diabaikan diam-diam sehingga nota yang sudah lunas tampil menunggak. Nota lunas masuk blok "Sudah lunas, TIDAK ditagih".
- Peringatan di baris paling atas keluaran bila judul mirip pembayaran tidak dikenali, isi pembayaran tak terbaca, tanggal bayar terisi padahal masih ada sisa, atau kolom sisa di file berbeda dari hitungan. Jumlah pengingat sebelumnya dibaca dari kolom keterangan ("sudah WA 2x").
- SKILL.md: bila input kurang, kerjakan dulu lalu tanyakan maksimal 3 hal di akhir; bahasa tanpa istilah teknis (script, file, folder); penolakan permintaan yang melanggar hukum singkat dengan alternatif; batas maksimal denda ditulis dalam rupiah dan baris rekening ada di semua pesan. Uji regresi menjadi 33 tes.

## Catatan revisi 1.0.6 (2026-10-02)
- Ringkasan aman untuk grup/tim: hanya jumlah faktur dan total (termasuk yang lewat jatuh tempo dan keterlambatan terlama), tanpa nama pelanggan, nomor invoice, nomor HP, atau sisa per pelanggan (JSON: `ringkasan_grup`). Tabel per pelanggan diberi judul "khusus pemilik/admin keuangan". Ditambah tes ringkasan grup anonim dan butir daftar periksa.

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: pesan menulis "kami lampirkan surat" padahal tidak ada file.
- Kini lampiran hanya disebut bila pengguna menyatakan ada; selain itu ditulis `[lampirkan: …]` dengan catatan pengguna yang membuat/melampirkan. Catatan pemilik di luar blok pesan.

## Catatan revisi 1.0.4 (2026-10-01)
Perbaikan dari uji OpenClaw asli (paket kantor-manajemen, konsultan, usaha-offline):
- File piutang dengan judul kolom umum langsung terbaca: `no_faktur`, `nilai_faktur`, `sudah_dibayar`, `customer`, `due_date`, `amount`, `paid`, kolom `sisa`/`outstanding`, judul berkurung seperti "Nilai Faktur (Rp)". Kolom lain (no. WA, tanggal faktur) diabaikan. Angka format Indonesia dan tanggal "25 Sep 2026" diterima. Bila kolom tidak dikenali, pesan error menyebut nama kolom yang diterima dan kolom yang ada di file.
- Rekap kini menampilkan total yang sudah lewat jatuh tempo.
- Script menulis kalimat jadwal yang jelas (tenggat bayar + kapan tahap berikutnya). Opsi `--hubungan dekat` (tetangga/kenalan/keluarga) memakai jeda 14 hari dan menyarankan bicara langsung dulu. Tidak ada lagi saran naik ke tahap tegas dalam 2 hari.
- Rincian yang diberikan pengguna (per bulan/per invoice) wajib masuk ke pesan tagihan.
- UU ITE/UU PDP hanya disebut bila relevan, dengan alasannya. Bila pengguna minta tahap 5 lewat WA: versi WA singkat + saran surat resmi.
- Path script ditulis jelas (subfolder `scripts/` di folder skill); agent dilarang mencari ke seluruh disk.

## Catatan revisi 1.0.3 (2026-09-29)
- Pengaman: singkatan opsi baris perintah tidak lagi diterima (mis. opsi `--konfirmasi-denda` tidak bisa dipicu dengan tulisan singkat), sehingga konfirmasi tidak terpicu tanpa sengaja. Ditambah uji regresi.

## Catatan revisi 1.0.2 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).
- Sumber data hanya yang diberikan pengguna: bila data tagihan tidak disebut, agent bertanya dan tidak menjelajah folder untuk "menemukan" piutang.
- File Excel `.xlsx` kini bisa dibaca langsung oleh script (`--file piutang.xlsx`, opsi `--sheet`) tanpa memasang paket tambahan; file `.xls`/`.ods` atau yang terkunci/rusak ditolak dengan pesan agar disimpan sebagai CSV. Uji regresi bertambah.

## Catatan revisi 1.0.1 (2026-09-24)
- Versi saat skill pertama masuk repo (lolos uji muat OpenClaw). Perbaikan kecil; rincian di riwayat git.

## Catatan revisi 1.0.0 (sebelum 2026-09-24)
- Rilis awal (uji internal).
