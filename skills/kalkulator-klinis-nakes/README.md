# Kalkulator Klinis Nakes: Hitung Pasti, Bersumber Jelas

**HPL, usia kehamilan, skrining preeklampsia, IMT, dan skor kognitif — dihitung script, lengkap
dengan kutipan pedoman. Untuk dokter, bidan, dan perawat.**

> ⚠️ **Status: PERLU REVIEW tenaga medis — belum untuk dijual.** Ambang & kalimat tindak lanjut
> wajib ditinjau dokter/bidan sebelum rilis (lihat `references/sumber-pedoman.md`, bagian
> "Status verifikasi"). Alat bantu keputusan untuk tenaga kesehatan, **bukan** pengganti
> penilaian klinis, **bukan** alat diagnosis, dan **tidak memberi dosis obat**.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **HPL & usia kehamilan tanpa salah hitung** — Naegele dan HPHT+280 hari, tahun kabisat,
  siklus ≠ 28 hari, plus cek otomatis "perlu penanggalan ulang dengan USG?" (ACOG 2017).
- ✅ **Skrining preeklampsia sesuai Buku KIA terbaru (cetakan 2025)** — isi faktor dengan
  bahasa biasa, MAP dihitung tepat tanpa dibulatkan dulu (110/80 = 90,0 → memenuhi ambang
  MAP ≥ 90; 109/80 = 89,7 → belum), keluar kategori risiko + sumber. Opsi NICE NG133 dengan
  aturan yang disebut sumbernya — tidak dicampur.
- ✅ **Tanda bahaya diperiksa lebih dulu** — TD ≥ 160/110 atau gejala bahaya langsung
  ditandai "SEGERA evaluasi/rujuk sesuai protokol fasilitas"; TD ≥ 140/90 "evaluasi/rujuk hari
  ini". Tidak pernah keluar saran "ANC rutin" untuk kasus seperti ini.
- ✅ **IMT & kenaikan BB hamil** — kategori Asia-Pasifik **dan** Kemenkes sekaligus, lingkar
  perut, rekomendasi IOM 2009 (termasuk kembar), plus mode banyak pasien dari CSV (posbindu).
- ✅ **Tafsir skor total kognitif (MMSE / MoCA / AMT)** yang Anda masukkan — alat tidak memuat
  formulir atau butir tes.
- ✅ **Catatan sesi stimulasi kognitif** rapi, siap tempel ke rekam medis — tanpa label
  diagnosis.

## Cocok untuk siapa
Dokter umum & dokter praktik mandiri, bidan (praktik mandiri, klinik, puskesmas), perawat klinik
lansia, ahli gizi, dan psikolog klinis/terapis yang menjalankan stimulasi kognitif. **Bukan untuk
pasien/awam** — bila yang bertanya bukan tenaga kesehatan, skill hanya memberi edukasi umum dan
menyarankan konsultasi.

## Contoh sebelum & sesudah
**Sebelum:** bidan menghitung HPL dengan kalender putar; siklus 35 hari tidak disesuaikan; MAP
dihitung kalkulator HP dan dibulatkan sebelum dibandingkan; faktor risiko preeklampsia dicentang
dari ingatan; sumber tidak tercatat.

**Sesudah (cukup ketik):** "Saya bidan. Bu R, G1, 36 th, hamil 14 minggu, TD 120/80, IMT 31,
ibunya dulu preeklampsia. Skrining preeklampsia."
→ MAP 93,3; **5 faktor sedang** (nullipara, usia ≥ 35, riwayat keluarga, IMT > 30, MAP ≥ 90) →
**BERISIKO PREEKLAMPSIA — Buku KIA: ANC/persalinan/nifas di RS, rujukan terencana**; daftar faktor yang
belum ditanyakan; sumber + penafian. Siap disalin ke rekam medis.
Bila TD 170/115: hasil diawali **‼️ TANDA BAHAYA — segera evaluasi/rujuk sesuai protokol
fasilitas** (sumber NICE NG133/ACOG), bukan "ANC rutin".

## Cara pakai
Setelah terpasang, ketik permintaan biasa, misalnya:
- "HPHT 10 Maret 2026, siklus 30 hari, USG 2 Mei usia 7 minggu 3 hari. HPL dan usia kehamilan
  hari ini?"
- "TB 155, BB sebelum hamil 62, sekarang 68 di usia 24 minggu. Kenaikannya sesuai?"
- "IMT dan lingkar perut: laki-laki, 165 cm, 72 kg, LP 92."
- "Skor MoCA-Ina 24, pendidikan 9 tahun. Interpretasinya?"
- "Buatkan catatan sesi stimulasi kognitif untuk peserta L-07 hari ini: ..."

Butuh Python 3 untuk perhitungan (sudah ada di kebanyakan komputer; Windows: `python`/`py`).
Tanpa Python, agent menghitung manual dengan rumus di `references/` dan memberi tanda
"verifikasi ulang".

## Batasan yang jujur perlu kamu tahu
- **Belum ditinjau dokter/bidan** (PERLU REVIEW). Lembar preeklampsia Buku KIA cetakan 2025
  sudah dicocokkan dengan naskah resmi; rentang AMT Permenkes 67/2015, tabel IMT Kemenkes, dan
  WPRO 2000 baru dikonfirmasi lewat sumber sekunder — rinciannya di
  `references/sumber-pedoman.md`. Cocokkan dengan cetakan Buku KIA yang dipakai fasilitas Anda.
- **Tanpa dosis obat** apa pun, termasuk aspirin/kalsium pencegahan preeklampsia.
- **Tanpa diagnosis** — hasil berupa kategori risiko/hasil skrining.
- **Alat ini hanya menafsirkan skor total MMSE/MoCA yang kamu masukkan** — tidak memuat,
  mereproduksi, atau memandu formulir, butir, maupun instruksinya. Memakai formulir **MoCA**
  memerlukan lisensi/izin dan pelatihan-sertifikasi milikmu sendiri dari MoCA Cognition;
  formulir **MMSE** memerlukan lisensi milikmu sendiri dari PAR Inc. Nama instrumen hanya
  penyebut; Komunitech tidak berafiliasi dengan pemegang hak cipta. (PERLU REVIEW legal.)
- **MoCA-Ina:** studi validasi 2010 belum menetapkan titik potong khusus Indonesia; alat memakai
  batas asli 26 dan menyebutkannya.
- **Skor risiko kardiovaskular tidak disertakan di v1** — agar tidak salah hitung; pakai WHO
  HEARTS risk chart resmi.
- Tidak untuk anak/remaja (< 18 tahun) dan kehamilan bayi tabung (tanggal transfer embrio).
- Data minimal: cukup inisial/ID pasien. Skill tidak menyimpan data apa pun.

## Instalasi singkat
Salin folder `kalkulator-klinis-nakes` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 8, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/790/813 — skor 6
- Dengan skill: https://t.me/c/4407409583/791/816 — skor 8,5
Verdik gelombang: LULUS — DENGAN menghitung MAP 100,0 dan mengklasifikasi pasien BERISIKO PREEKLAMPSIA (2 faktor sedang: usia ≥35 + MAP ≥90 → rujukan terencana sesuai Buku KIA); TANPA tidak menghitung MAP sehingga hanya menemukan 1 faktor dan menyimpulkan "pantau", padahal menurut Buku KIA pasien memenuhi kriteria rujukan terencana. Belum direview tenaga medis.

## FAQ
**Apakah hasilnya bisa langsung jadi dasar rujukan?**
Hasil adalah alat bantu. Kategori risiko mengikuti pedoman yang dikutip, tetapi keputusan
rujukan dan tata laksana tetap penilaian klinis dokter/bidan yang memeriksa.

**Kenapa HPL Naegele dan HPHT+280 hari bisa beda 1–3 hari?**
Naegele memakai bulan kalender yang panjangnya berbeda-beda; +280 hari menghitung hari persis.
Keduanya ditampilkan agar sesuai kebiasaan praktikmu, dan catatan menjelaskan selisihnya.

**Pasien saya bertanya langsung ke agent, apa yang terjadi?**
Skill memastikan peran penanya. Bila bukan tenaga kesehatan, skill tidak menjalankan skrining
atau menafsirkan angka — hanya edukasi umum, anjuran konsultasi, dan kalimat tanda bahaya
(IGD/119).
