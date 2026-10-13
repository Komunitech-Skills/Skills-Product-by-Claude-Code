# Riwayat perubahan — tagih-piutang

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

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
