# Riwayat perubahan — cv-lamaran-ats

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi singkat
- **1.1.3** (2026-10-01) — petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill; agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).
- **1.1.2** (2026-09-29) — baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).
- **1.1.1** (2026-09-28) — revisi rendah: `scripts/skor_kecocokan.py` menambah daftar kata pengisi lowongan ("dipersilakan", "jujur", "melamar", "silakan", dan sejenisnya) agar tidak dihitung sebagai kata kunci; `references/evaluasi-kecocokan.md` menjelaskan bahwa bila satu dimensi skor tidak bisa dinilai, bobotnya dikeluarkan dan dibagi proporsional ke dimensi lain (bukan dianggap 0). Uji regresi baru `tests/uji_regresi.py` (2 skenario).
- **1.1.0** — tambah profil pengalaman induk, evaluasi kecocokan lowongan (skor+alasan+celah), dan latihan wawancara STAR.
- **1.0.1** — versi awal: CV ramah ATS, surat lamaran, skor kecocokan kata kunci.
