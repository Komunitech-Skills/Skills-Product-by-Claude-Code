# Kalkulator Klinis Nakes: Hitungan Jelas, Bersumber Jelas

**HPL, usia kehamilan, skrining preeklampsia, IMT, dan skor kognitif — dihitung skrip, lengkap
dengan kutipan pedoman. Untuk dokter, bidan, dan perawat.**

Diuji AI penguji independen di OpenClaw: 6,1 → 9,0 dari 10 (pada pertanyaan ibu hamil awam yang minta dosis aspirin, jawaban AI tanpa skill berubah-ubah dan sekali menyebut dosis; dengan skill konsisten tanpa nama obat atau dosis, dan mengarahkan ke bidan/IGD/119).

> ⚠️ **Belum direview tenaga medis.** Ambang dan kalimat tindak lanjut perlu ditinjau dokter/bidan
> sebelum dipakai klinis (lihat `references/sumber-pedoman.md`). Alat bantu keputusan khusus
> tenaga kesehatan: bukan diagnosis, bukan pengganti penilaian klinis, tanpa dosis obat.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **HPL & usia kehamilan dihitung skrip, bukan dikira** — Naegele dan HPHT+280 hari, tahun kabisat,
  siklus ≠ 28 hari, plus cek otomatis "perlu penanggalan ulang dengan USG?" (ACOG 2017).
- ✅ **Skrining preeklampsia sesuai Buku KIA terbaru (cetakan 2025)** — isi faktor dengan
  bahasa biasa, MAP dihitung tepat tanpa dibulatkan dulu (110/80 = 90,0 → memenuhi ambang
  MAP ≥ 90; 109/80 = 89,7 → belum), keluar kategori risiko + sumber. Opsi NICE NG133 dengan
  aturan yang disebut sumbernya — tidak dicampur.
- ✅ **Tanda bahaya diperiksa lebih dulu** — TD ≥ 160/110 atau gejala bahaya langsung
  ditandai "SEGERA evaluasi/rujuk sesuai protokol fasilitas"; TD ≥ 140/90 "evaluasi/rujuk hari
  ini". Pada kasus seperti ini hasil tidak diarahkan ke "ANC rutin".
- ✅ **IMT & kenaikan BB hamil** — kategori Asia-Pasifik **dan** Kemenkes sekaligus, lingkar
  perut, rekomendasi IOM 2009 (termasuk kembar), plus mode banyak pasien dari tabel CSV (file Excel yang disimpan sebagai .csv) untuk posbindu (pos pembinaan terpadu).
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

**Sesudah (cukup ketik):** "Saya bidan. Bu R, G1P0A0, 36 th, hamil 14 minggu, TD 120/80, IMT sebelum hamil 31, ibunya dulu preeklampsia. Skrining preeklampsia ya."

Cuplikan balasan (dipotong; contoh dengan data fiktif dari `examples/01-skrining-preeklampsia.md`):
```
🩺 Skrining faktor risiko preeklampsia — Bu R — 29 September 2026

Tanda bahaya: tidak ada (TD 120/80 < 140/90; …)

Hasil:
- MAP 93,3 mmHg (≥ 90)
- Kategori (Buku KIA cetakan 2025): BERISIKO PREEKLAMPSIA — perlu rujukan terencana
  (≥ 2 faktor risiko sedang)
  Faktor sedang (5): nullipara; usia ≥ 35 tahun; riwayat preeklampsia pada ibu;
  obesitas pra-hamil (IMT > 30); MAP ≥ 90. Faktor tinggi: tidak ada.
- Belum ditanyakan: diabetes, penyakit ginjal, autoimun/APS, proteinuria — mohon dilengkapi
  bila belum diperiksa.
…
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap
pada dokter/bidan yang memeriksa.
```
Bila TD 170/115: hasil diawali **TANDA BAHAYA — segera evaluasi/rujuk sesuai protokol
fasilitas** (sumber NICE NG133/ACOG), bukan "ANC rutin". Siap disalin ke rekam medis.

## Cara pakai
Setelah terpasang, ketik permintaan biasa, misalnya:
- "HPHT 10 Maret 2026, siklus 30 hari, USG 2 Mei usia 7 minggu 3 hari. HPL dan usia kehamilan
  hari ini?"
- "TB 155, BB sebelum hamil 62, sekarang 68 di usia 24 minggu. Kenaikannya sesuai?"
- "IMT dan lingkar perut: laki-laki, 165 cm, 72 kg, LP 92."
- "Skor MoCA-Ina 24, pendidikan 9 tahun. Interpretasinya?"
- "Buatkan catatan sesi stimulasi kognitif untuk peserta L-07 hari ini: ..."

## Batasan yang perlu Anda tahu (jujur)
- **Verifikasi sumber:** lembar preeklampsia Buku KIA cetakan 2025
  sudah dicocokkan dengan naskah resmi; rentang AMT Permenkes 67/2015, tabel IMT Kemenkes, dan
  WPRO 2000 baru dikonfirmasi lewat sumber sekunder — rinciannya di
  `references/sumber-pedoman.md`. Cocokkan dengan cetakan Buku KIA yang dipakai fasilitas Anda.
- **Tanpa dosis obat** apa pun, termasuk aspirin/kalsium pencegahan preeklampsia.
- **Tanpa diagnosis** — hasil berupa kategori risiko/hasil skrining.
- **Alat ini hanya menafsirkan skor total MMSE/MoCA yang Anda masukkan** — tidak memuat,
  mereproduksi, atau memandu formulir, butir, maupun instruksinya. Memakai formulir **MoCA**
  memerlukan lisensi/izin dan pelatihan-sertifikasi milik Anda sendiri dari MoCA Cognition;
  formulir **MMSE** memerlukan lisensi milik Anda sendiri dari PAR Inc. Nama instrumen hanya
  penyebut; Komunitech tidak berafiliasi dengan pemegang hak cipta. (PERLU REVIEW legal.)
- **MoCA-Ina:** studi validasi 2010 belum menetapkan titik potong khusus Indonesia; alat memakai
  batas asli 26 dan menyebutkannya.
- **Skor risiko kardiovaskular tidak disertakan di v1** — agar tidak salah hitung; pakai WHO
  HEARTS risk chart resmi.
- Tidak untuk anak/remaja (< 18 tahun) dan kehamilan bayi tabung (tanggal transfer embrio).
- Data minimal: cukup inisial/ID pasien. Skill tidak menyimpan data apa pun.

## Instalasi singkat
Salin folder `kalkulator-klinis-nakes` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket (di dalam paket bernama `CARA-INSTAL.md`).

Butuh Python 3 untuk perhitungan (sudah ada di kebanyakan komputer; Windows: `python`/`py`).
Tanpa Python, agent menghitung manual dengan rumus di `references/` dan memberi tanda
"verifikasi ulang".

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.5), skor 1–10: tanpa skill **6,1** → dengan skill **9,0** (hasil uji: lulus). Contoh bidan TD 128/86: **MAP 100,0**, 5 faktor sedang Buku KIA 2025, **HPL 19 Maret 2027**, tanpa dosis obat. Sumber skor: `examples/00-openclaw-sebelum-sesudah.md`. Hasil uji di bot Telegram asli ada di bagian berikutnya.

**Status uji (jujur):** sudah uji OpenClaw otomatis + bot Telegram asli (5 Okt 2026). MoCA/MMSE hanya tafsir skor total (lisensi formulir milik pengguna). Codex/Cursor belum uji platform asli.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech) pada 5 Okt 2026, skill versi 1.0.6. Pesan yang sama dikirim ke dua kondisi, tanpa skill dan dengan skill: seorang bidan meminta skrining preeklampsia dan HPL untuk satu pasien fiktif (tekanan darah 128/86, kehamilan kedua). Skor 1–10 dari penilai independen: tanpa skill **6** → dengan skill **8,5** (selisih +2,5, lulus acuan kami). Dengan skill, bot menghitung tekanan arteri rata-rata (MAP) 100,0 dan mengenali pasien berisiko preeklampsia (usia 35 tahun ke atas plus MAP 90 ke atas, dua faktor sedang) sehingga perlu rujukan terencana sesuai Buku KIA; tanpa skill, MAP tidak dihitung, hanya satu faktor yang ditemukan, dan kesimpulannya cuma "pantau". Catatan jujur: skill ini belum direview tenaga medis, dan hasil uji kami bukan review medis. Pada balasan dengan skill, daftar "belum ditanyakan" masih menyebut "nullipara" padahal pasiennya sudah pernah melahirkan. Uji sebelumnya (OpenClaw di komputer penguji, v1.0.5): 6,1 → 9,0.

## FAQ
**Apakah hasilnya bisa langsung jadi dasar rujukan?**
Hasil adalah alat bantu. Kategori risiko mengikuti pedoman yang dikutip, tetapi keputusan
rujukan dan tata laksana tetap penilaian klinis dokter/bidan yang memeriksa.

**Kenapa HPL Naegele dan HPHT+280 hari bisa beda 1–3 hari?**
Naegele memakai bulan kalender yang panjangnya berbeda-beda; +280 hari menghitung hari persis.
Keduanya ditampilkan agar sesuai kebiasaan praktik Anda, dan catatan menjelaskan selisihnya.

**Pasien saya bertanya langsung ke agent, apa yang terjadi?**
Skill menanyakan peran penanya. Bila bukan tenaga kesehatan, skill tidak menjalankan skrining
atau menafsirkan angka — hanya edukasi umum, anjuran konsultasi, dan kalimat tanda bahaya
(IGD/119).

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
