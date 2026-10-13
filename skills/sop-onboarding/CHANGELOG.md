# Riwayat perubahan — sop-onboarding

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
- **Catatan revisi 1.0.6 (2026-10-05):** uji bot Telegram asli (DENGAN 8, tepat di batas): tabel 6 kolom tampil sebagai teks berpipa, urutan evaluasi keputusan vs batas percobaan membingungkan, kata "skill" bocor. Kini jadwal di chat berupa daftar bernomor kronologis (tabel maks. 2 kolom hanya untuk dokumen), evaluasi keputusan selalu ditulis sebelum batas percobaan, kata proses (skill, script, file, path, cek) dilarang di balasan. Menunggu uji ulang independen.
- **Catatan revisi 1.0.5 (2026-10-05):** pra-cek Telegram G9: untuk "paket onboarding kasir minimarket, karyawan tetap, 3 bulan, mulai Senin 12 Oktober 2026" bot hanya mengajukan 6 pertanyaan dan membocorkan "sudah saya cek". Kini wajib "kerjakan dulu, tanya di akhir": paket utuh di chat (jadwal minggu 1, checklist, SOP kasir ringkas, evaluasi masa percobaan dengan tanggal, catatan PP 35/2021 & cek UMK) dengan [isian], maks. 3 pertanyaan di akhir, tanpa kata proses. Menunggu uji ulang independen.
- **1.0.2** (lulus) — Perbaikan kecil hasil uji ulang independen: batas 3 bulan akhir masa percobaan kini
  dinyatakan tegas sebagai **tafsir** (bukan kepastian hukum), dengan saran konfirmasi ke Disnaker/konsultan
  bila ragu (SKILL.md, script, `references/dasar-hukum-onboarding.md`); kalimat contoh di SKILL.md diperbaiki
  (libur Natal 24–25 Des memundurkan evaluasi dari 22 ke 19 Desember, bukan "tidak ada libur di rentang ini");
  definisi "5 hari kerja sebelum batas" diperjelas (hari kerja terakhir ≤ batas = hari kerja ke-1); cuti
  bersama kini disebut eksplisit fakultatif bagi swasta, dengan opsi `--cuti-bersama-hari-kerja` untuk
  menganggapnya hari kerja; tanggal tahun di luar 1900–9900 (termasuk 9999) kini memberi pesan ramah, bukan
  Traceback; file `--libur` berpemisah titik-koma (ekspor Excel Indonesia) kini terbaca; tambahan contoh
  lengkap varian bengkel (PKWT, tanggal mulai di hari libur) di `references/varian-jenis-usaha.md`.
- **1.0.1** (draft) — Perbaikan hasil uji independen: batas hukum akhir masa percobaan PKWTT & tanggal evaluasi keputusannya kini dipisah dari checkpoint 90 hari (evaluasi selalu terjadwal sebelum batas hukum; peringatan eksplisit bila checkpoint 90 hari melewati batas); contoh di SKILL.md/README diperbaiki agar sama persis dengan hasil script; libur nasional & cuti bersama 2026/2027 dimuat otomatis; peringatan bila tanggal mulai jatuh di hari libur/Minggu; catatan pengecualian upah usaha mikro/kecil; formulir evaluasi versi PKWT; tambahan panduan buddy, jadwal check-in mingguan, target per jabatan, dan retrospektif onboarding.
- **1.0.0** — Rilis awal (draft).
