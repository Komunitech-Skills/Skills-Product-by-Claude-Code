# Riwayat perubahan — tagih-piutang

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

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
