# Riwayat perubahan — cek-privasi-openclaw

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.1.5 (2026-10-15)
- Tindak lanjut verifikasi rujukan aturan (dicek 15 Oktober 2026): `references/uu-pdp.md` kini mencantumkan **PP 33/2026** tentang Peraturan Pelaksanaan UU 27/2022 (diundangkan 16 Juli 2026, mulai berlaku 16 Januari 2027) menggantikan catatan "PP belum diverifikasi", serta dasar berlaku penuh UU PDP sejak Oktober 2024 (Pasal 74).
- Pemberitahuan kebocoran data: frasa "dalam hitungan hari" diganti "**paling lambat 72 jam (3×24 jam)** secara tertulis kepada pemilik data dan lembaga" dengan rujukan UU 27/2022 Pasal 46 ayat (1); SKILL.md langkah 5 & checklist ikut diperbarui.
- Tambah satu pengingat sanksi administratif UU PDP (Pasal 57) di `references/uu-pdp.md` dan FAQ README.
- Penolakan permintaan menyadap chat kini merujuk UU ITE lengkap: UU 11/2008 jo. UU 1/2024 (perubahan kedua), Pasal 31 — di SKILL.md dan bagian baru `references/uu-pdp.md`.
- README: manfaat UU PDP menyebut nomor & tahun aturan; versi terkini 1.1.5. Cara kerja audit OpenClaw tidak berubah.

## Catatan revisi 1.1.4 (2026-10-01)
- Uji OpenClaw 2026-10-01: agent sempat menjalankan `chmod` sebelum menampilkan daftar perbaikan. Kini semua perubahan (config, `chmod`/izin file, `--fix`) hanya dijalankan setelah daftar lengkap ditampilkan dan pemilik menjawab "ya"; "gak usah nanya" sebelum melihat daftar bukan persetujuan.
- Permintaan menyadap/memata-matai chat orang lain: penolakan kini wajib ditulis lengkap & sopan di balasan itu sendiri (alasan UU ITE Pasal 31 & UU PDP + alternatif sah), bukan hanya "tetap saya tolak".
