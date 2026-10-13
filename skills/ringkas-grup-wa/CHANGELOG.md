# Riwayat perubahan — ringkas-grup-wa

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.6 (2026-10-13)
- `references/openclaw-grup.md`: rujukan ke catatan riset dan aturan kerja internal diganti kalimat yang berdiri sendiri (kebijakan Komunitech). Tidak ada perubahan perilaku.

## Catatan revisi 1.0.5 (2026-10-01)
- Temuan uji ulang OpenClaw: jumlah butir salah hitung ("(6)" padahal 5; "tiga lainnya" padahal 4) dan pelanggan tertulis "vendor".
- Kini jumlah butir wajib dihitung ulang dari daftar final / keluaran script, dan peran pihak disalin dari chat.

## Catatan revisi 1.0.4 (2026-10-01)
Perbaikan dari uji OpenClaw asli (ringkasan grup WA gudang):
- Tenggat yang sudah lewat kini ditandai **"⏰ LEWAT TENGGAT — cek status"**. Script membaca tanggal di pesan (29/9, 5 Okt, hari ini/besok/lusa, nama hari) dan membandingkannya dengan tanggal hari ini; rencana yang tanggalnya sudah lewat tidak lagi ditulis "sudah beres".
- Ringkasan menyebut tanggal chat terakhir dan tanggal hari ini.
- Path script ditulis jelas (subfolder `scripts/`); AI dilarang mencari file ke seluruh disk.
