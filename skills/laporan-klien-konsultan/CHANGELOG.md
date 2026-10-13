# Riwayat perubahan — laporan-klien-konsultan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.6 (2026-10-13)
- `references/openclaw-jadwal.md`: dua rujukan ke aturan pengujian internal diganti kalimat yang berdiri sendiri (pengujian independen oleh kurator Komunitech); konstanta VERSI skrip dan penanda versi di SKILL.md disamakan; cara kerja tidak berubah.

## Catatan revisi 1.0.5 (2026-10-01)
Perbaikan dari uji OpenClaw asli 2026-10-01 (skenario laporan progres dari file CSV):
- **Jam tidak lagi dibulatkan 1 desimal.** 3,25 jam tampil "3,25 jam" (sebelumnya "3,2"), total
  tampil "9,75 jam (9 jam 45 menit)" dan selalu sama persis dengan jumlah jam per pekerjaan.
- **File catatan Anda sendiri langsung terbaca** (`--file`): pemisah koma/titik koma/tab, desimal
  koma, "90 menit"/"1 jam 30 menit"/"1:30", tanggal 22/09/2026, header Indonesia/Inggris, file
  dari Excel (BOM, UTF-16, Windows-1252). Bila tetap gagal, pesan error menyebut baris & cara
  memperbaikinya.
- **Teks "Periode periode kustom" diperbaiki** -- rentang kustom cukup menampilkan tanggalnya.
- **"Rencana berikutnya" tidak lagi mengulang judul tugas.** Diisi dari rencana Anda (ucapan,
  `--rencana`, atau kolom Rencana di file); bila belum ada, muncul isian `[isi: ...]` untuk Anda
  lengkapi sebelum dikirim.
- Agent diarahkan memakai script di folder skill sendiri, tidak mencari file ke seluruh disk.
- Uji regresi: 45/45 lolos (termasuk file contoh skenario `tests/data/catatan-kerja.csv`).
