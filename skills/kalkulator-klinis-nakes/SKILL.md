---
name: kalkulator-klinis-nakes
description: Alat bantu hitung & skrining untuk TENAGA KESEHATAN (dokter, bidan, perawat) di klinik/praktik mandiri/puskesmas — skrining faktor risiko preeklampsia (Buku KIA 2023 / NICE NG133) + MAP, kalkulator kehamilan (HPL Naegele, usia kehamilan dari HPHT/USG, penanggalan ulang ACOG), IMT pra-hamil & rekomendasi kenaikan BB (IOM 2009), IMT dewasa (Asia-Pasifik & Kemenkes) + lingkar perut, interpretasi skor total MMSE/MoCA-Ina/AMT, dan template catatan sesi stimulasi kognitif. Gunakan saat nakes minta hitung HPL, usia kehamilan, MAP, skrining preeklampsia, IMT, kenaikan berat badan hamil, atau tafsir skor MoCA/MMSE/AMT. Setiap hasil memuat sumber pedoman + tahun; tanpa dosis obat, tanpa diagnosis — clinical calculator for health professionals, preeclampsia risk screening, due date calculator, gestational age, BMI Asia-Pacific, pregnancy weight gain, cognitive screening score interpretation.
---

# Kalkulator Klinis untuk Tenaga Kesehatan

> **Status: PERLU REVIEW tenaga medis sebelum rilis.** Alat bantu keputusan, bukan pengganti
> penilaian klinis. Keputusan tetap pada dokter/bidan yang memeriksa.

## Tujuan
Memberi tenaga kesehatan hasil hitung yang **pasti dan bersumber** (angka dari script, bukan
perkiraan) untuk pekerjaan rutin ANC, gizi, dan skrining kognitif — lengkap dengan kutipan
pedoman + tahun, sehingga bisa langsung dicatat di rekam medis klinik sendiri.

## Kapan digunakan
- Skrining faktor risiko preeklampsia pada ANC (idealnya < 20 minggu) + hitung MAP.
- HPL (Naegele & HPHT+280), usia kehamilan dari HPHT atau USG, cek perlu penanggalan ulang.
- IMT pra-hamil & rekomendasi kenaikan berat badan selama hamil.
- IMT dewasa (kategori Asia-Pasifik & Kemenkes) + lingkar perut (obesitas sentral).
- Menafsirkan **skor total** MMSE / MoCA-Ina / AMT yang sudah diberikan pemeriksa.
- Menyusun catatan sesi stimulasi kognitif (template, tanpa diagnosis).

## Kapan TIDAK digunakan (tolak dengan sopan, beri alternatif)
- **Dosis obat apa pun** (termasuk aspirin/kalsium pencegahan preeklampsia, MgSO4,
  antihipertensi): "Dosis mengikuti PNPK/pedoman dan resep dokter — di luar cakupan alat ini."
- Diagnosis pasti ("pasien ini preeklampsia/demensia"), interpretasi lab/USG/CTG, triase gawat
  darurat. Tanda bahaya (TD ≥ 160/110, kejang, nyeri kepala hebat, pandangan kabur, nyeri ulu
  hati, perdarahan) → "Tangani/rujuk segera sesuai protokol kegawatdaruratan fasilitas Anda."
- Skor risiko kardiovaskular: **tidak disediakan di v1** (lihat `references/sumber-pedoman.md`
  bagian "Yang sengaja tidak disertakan") — arahkan ke WHO/HEARTS risk chart resmi.
- IMT anak/remaja (< 18 tahun) → pakai grafik pertumbuhan WHO/Kemenkes (z-score), bukan alat ini.
- Menampilkan/menulis ulang **butir soal** MMSE atau MoCA (berhak cipta) — alat ini hanya
  menerima skor total.

## Langkah 0 — WAJIB: pastikan peran pengguna
Jika peran belum jelas, tanyakan sekali: *"Sebelum mulai: Anda tenaga kesehatan (dokter, bidan,
perawat, ahli gizi, psikolog klinis) yang menangani pasien ini?"*
- **Ya (nakes)** → lanjut langkah kerja.
- **Bukan / pasien / keluarga** → **jangan** jalankan skrining atau menafsirkan skor. Beri
  edukasi umum singkat (mis. "Preeklampsia adalah tekanan darah tinggi dalam kehamilan; periksa
  tekanan darah di setiap kunjungan hamil"), sarankan konsultasi ke bidan/dokter, dan untuk HPL
  cukup sebutkan bahwa bidan/dokter akan memastikannya. Lihat
  `references/batasan-dan-kalimat-baku.md`.
- Pertanyaan umum tanpa pasien (mis. mahasiswa kebidanan belajar rumus) → boleh jelaskan rumus
  & sumber, tetap dengan penafian.

## Input
| Kalkulator | Wajib | Opsional / default |
|---|---|---|
| Preeklampsia | daftar faktor yang ada (bahasa bebas → petakan ke kode) | TD sistolik/diastolik, usia ibu, IMT; pedoman `kia` (default) atau `nice` |
| Kehamilan | HPHT **atau** (tanggal USG + usia saat USG) | siklus (default 28 hari), tanggal periksa (default hari ini) |
| BB hamil | tinggi, BB pra-hamil | BB sekarang, usia kehamilan (minggu), kembar |
| IMT dewasa | tinggi (cm atau m), berat (kg) | lingkar perut (cm) + jenis kelamin L/P |
| Kognitif | instrumen (mmse/moca/amt), skor total | lama pendidikan (tahun) — **wajib untuk MoCA** |

**Data minimal:** tidak perlu nama pasien. Pakai inisial/nomor RM klinik bila perlu label.
Jangan minta NIK, alamat, atau nomor HP. Jika pengguna menempel nama lengkap, pakai inisial di
output.

Jika input wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan).

## Langkah kerja
1. Langkah 0 (peran). 2. Kenali kalkulator yang diminta (bisa lebih dari satu).
3. Petakan bahasa bebas ke kode faktor preeklampsia (daftar: `python3 scripts/klinis.py
   faktor-preeklampsia`, atau `references/preeklampsia.md`). Faktor yang **tidak disebut** →
   anggap tidak ada, tapi tulis "belum ditanyakan" untuk faktor penting yang tidak dibahas.
4. **Jalankan script** (Windows: `python` atau `py`):
   ```
   python3 scripts/klinis.py preeklampsia --faktor nullipara,riwayat-keluarga --sistolik 118 --diastolik 82 --usia-ibu 36
   python3 scripts/klinis.py kehamilan --hpht 2026-03-10 --siklus 30 --tanggal-periksa 2026-09-29 --usg-tanggal 2026-05-02 --usg-minggu 7 --usg-hari 3
   python3 scripts/klinis.py bb-hamil --tinggi 155 --bb-prahamil 62 --bb-sekarang 68 --usia-minggu 24
   python3 scripts/klinis.py imt --tinggi 165 --berat 72 --lingkar-perut 92 --jk L
   python3 scripts/klinis.py kognitif --instrumen moca --skor 24 --pendidikan-tahun 9
   ```
   Tambah `--json` bila perlu data terstruktur. Kode keluar 1 = input tidak valid → sampaikan
   pesannya apa adanya dan minta data yang benar; **jangan menebak angka**.
5. Jika Python tidak bisa dijalankan: hitung manual dengan rumus di `references/` dan tulis
   "dihitung manual — verifikasi ulang". Tanggal wajib dihitung per hari kalender (kabisat!).
6. Susun output sesuai format di bawah. Salin angka **persis** dari script.
7. Periksa checklist sebelum mengirim.

## Format output
```
🩺 [Nama kalkulator] — [inisial/ID pasien bila diberikan] — [tanggal periksa]

Hasil:
- [angka/kategori dari script]

Arti untuk tindak lanjut:
- [kalimat "pertimbangkan ..." dari script; tanpa dosis, tanpa diagnosis pasti]

Catatan: [catatan script: asumsi, batas, pembulatan]
Sumber: [pedoman + tahun, persis dari script]
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap
pada dokter/bidan yang memeriksa.
```
Untuk catatan sesi stimulasi kognitif pakai `templates/catatan-sesi-stimulasi-kognitif.md`;
untuk ringkasan ANC pakai `templates/ringkasan-anc.md`.

## Contoh
**Input:** "Saya bidan. Bu R, G1P0A0, 36 th, hamil 14 minggu, TD 120/80, IMT sebelum hamil 31,
ibunya dulu preeklampsia. Skrining preeklampsia ya."

**Proses:** faktor = nullipara, riwayat-keluarga; angka → `--sistolik 120 --diastolik 80
--usia-ibu 36 --imt 31`.

**Output (ringkas):**
```
🩺 Skrining faktor risiko preeklampsia — Bu R — 29 September 2026
Hasil:
- MAP 93,3 mmHg (> 90)
- Kategori: RISIKO SEDANG (≥ 2 faktor sedang) — 5 faktor sedang: nullipara, usia ≥ 35,
  riwayat preeklampsia pada ibu, obesitas pra-hamil (IMT > 30), MAP > 90. Faktor tinggi: tidak ada.
Arti untuk tindak lanjut:
- Sesuai Buku KIA 2023 memenuhi kriteria rujukan/konsultasi dokter; pertimbangkan tindak
  lanjut sesuai PNPK/pedoman. Keputusan terapi/obat pencegahan (termasuk dosis) bukan bagian
  alat ini.
Sumber: Kemenkes RI, Buku KIA 2023 — lembar skrining preeklampsia < 20 minggu; rumus MAP.
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis.
```
Contoh lengkap lain: `examples/`.

## Checklist sebelum mengirim
- [ ] Peran nakes sudah dipastikan (atau jawaban edukasi umum untuk awam).
- [ ] Semua angka dari script (atau ditandai "dihitung manual — verifikasi ulang").
- [ ] Ada baris **Sumber** (pedoman + tahun) dan baris penafian ⚠️.
- [ ] Tidak ada dosis obat, nama obat sebagai anjuran, atau diagnosis pasti
      ("pasien menderita ..."). Pakai "kategori risiko", "di bawah batas skrining",
      "pertimbangkan ...".
- [ ] Tidak ada nama lengkap/NIK/alamat/no. HP pasien.
- [ ] Tidak menulis butir soal MMSE/MoCA.

## Batasan & penanganan error
- **Angka tidak masuk akal** (TD 80/120, tinggi 16 cm, HPHT di masa depan, usia kehamilan
  > 44 minggu): script menolak dengan pesan jelas → minta pengguna cek ulang/satuan.
- **Satuan:** tinggi ≥ 3 dianggap cm, < 3 dianggap meter; berat kg; TD mmHg; koma desimal
  boleh ("1,65"). Pon/inci → minta dikonversi dulu oleh pengguna (jangan tebak).
- **Siklus tidak teratur / di luar 21–45 hari / lupa HPHT:** HPHT kurang andal → sarankan
  penanggalan USG (idealnya trimester 1).
- **Skrining preeklampsia > 20 minggu:** tetap bisa dihitung, sebutkan bahwa lembar Buku KIA
  dirancang untuk < 20 minggu.
- **Faktor ambigu** (mis. "pernah darah tinggi waktu hamil dulu"): petakan ke
  `riwayat-preeklampsia` dan tulis asumsinya; bila ragu, tanyakan.
- **Dua pedoman berbeda** (Buku KIA vs NICE: kembar = tinggi vs sedang; usia 35 vs 40; IMT > 30
  vs ≥ 35): default Buku KIA (Indonesia); tampilkan NICE hanya bila diminta.
- **MoCA tanpa lama pendidikan:** script menolak — tanyakan lama sekolah (tahun).
- **Batas yang PERLU REVIEW tenaga medis:** lihat `references/sumber-pedoman.md` bagian
  "Status verifikasi". Alat ini belum boleh dijual sebelum ditinjau dokter/bidan.
