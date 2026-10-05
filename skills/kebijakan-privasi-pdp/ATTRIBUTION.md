# Atribusi

Skill ini adalah karya **orisinal** Komunitech (komunitech.com), ditulis dari nol: SKILL.md, template, checklist, script `scripts/cek_kebijakan.py`, dan tes regresinya.

Tidak mengandung materi skill atau template pihak ketiga.

Rujukan hukum yang dipakai adalah **peraturan perundang-undangan Republik Indonesia** (UU 27/2022 tentang Pelindungan Data Pribadi, PP 33/2026, PP 71/2019, Permenkominfo 5/2020, UU 1/2024, UU KUP, Permenkes 24/2022) dan Putusan MK 151/PUU-XXII/2024. Peraturan perundang-undangan dan putusan pengadilan bukan objek hak cipta (UU 28/2014 Pasal 42). Daftar sumber beserta URL dan tanggal pengecekan ada di `references/dasar-hukum.md`.

Penggunaan tunduk pada `LISENSI.txt` yang disertakan dalam paket pembelian.

## Riwayat versi
- **1.0.2 (2026-09-25)** — revisi berdasarkan uji ulang (`examples/06-uji-ulang-v1.0.1.md`, B-1..B-8): pola deteksi & polaritas per klausa di `scripts/cek_kebijakan.py`, `references/checklist-uu-pdp.md`, `references/dasar-hukum.md` (definisi anak: UU 35/2014 Ps. 1 angka 1), SKILL.md (urutan status, usia anak). Data uji baru: `tests/data/set-penguji-v101.json` + `tests/data/penguji-d*.md` (disalin dari set uji penguji internal Komunitech) dan `tests/data/set-kontrol-v102.json` (ditulis perevisi). Semua tetap karya orisinal Komunitech.
- **1.0.1 (2026-09-25)** — revisi berdasarkan `examples/HASIL-UJI.md`: `scripts/cek_kebijakan.py` ditulis ulang bagian deteksinya (negasi & polaritas tingkat kalimat, pola jual data ID/EN, pola unsur, penalti isian kosong, HTML, UTF-16 tanpa BOM, kinerja linier, rujukan pasal); `templates/pemberitahuan-persetujuan.md` bagian D + D-online; `references/dasar-hukum.md` (Ps. 5, 31, 46, 68; status PP 33/2026) dan `references/checklist-uu-pdp.md`; tes regresi + set kalimat berlabel (`tests/data/`). Kalimat uji di `tests/data/kalimat-berlabel.json` dan `tests/data/contoh*.md` berasal dari hasil uji internal Komunitech (bukan materi pihak ketiga). Semua tetap karya orisinal Komunitech.
- **1.0.0 (2026-09-25)** — versi pertama.
