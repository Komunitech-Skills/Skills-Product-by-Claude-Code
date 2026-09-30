---
name: kalkulator-klinis-nakes
description: Alat bantu hitung & skrining untuk TENAGA KESEHATAN (dokter, bidan, perawat) di klinik/praktik mandiri/puskesmas — skrining faktor risiko preeklampsia (Buku KIA edisi terbaru cetakan 2025 / NICE NG133) + MAP dengan lapisan tanda bahaya (TD rentang berat → segera evaluasi/rujuk), kalkulator kehamilan (HPL Naegele, usia kehamilan dari HPHT/USG, penanggalan ulang ACOG), IMT pra-hamil & rekomendasi kenaikan BB (IOM 2009), IMT dewasa (Asia-Pasifik & Kemenkes) + lingkar perut, tafsir skor total MMSE/MoCA/AMT yang dimasukkan nakes, dan template catatan sesi stimulasi kognitif. Gunakan saat nakes minta hitung HPL, usia kehamilan, MAP, skrining preeklampsia, IMT, kenaikan berat badan hamil, atau tafsir skor total kognitif. Setiap hasil memuat sumber pedoman + tahun; tanpa dosis obat, tanpa diagnosis — clinical calculator for health professionals, preeclampsia risk screening, due date calculator, gestational age, BMI Asia-Pacific, pregnancy weight gain, cognitive screening total score interpretation.
---

# Kalkulator Klinis untuk Tenaga Kesehatan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

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
- IMT dewasa (kategori Asia-Pasifik & Kemenkes) + lingkar perut, satu pasien atau banyak (CSV).
- Menafsirkan **skor total** MMSE / MoCA / AMT yang sudah didapat pemeriksa.
- Menyusun catatan sesi stimulasi kognitif (template, tanpa diagnosis).

## Kapan TIDAK digunakan (tolak dengan sopan, beri alternatif)
- **Dosis obat apa pun** (termasuk aspirin/kalsium pencegahan preeklampsia, MgSO4,
  antihipertensi): "Dosis mengikuti PNPK/pedoman dan resep dokter — di luar cakupan alat ini."
- Diagnosis pasti ("pasien ini preeklampsia/demensia"), interpretasi lab/USG/CTG, tata laksana
  gawat darurat. Bila ada tanda bahaya, alat hanya menandai **"SEGERA evaluasi/rujuk sesuai
  protokol fasilitas"** (lihat "Lapisan tanda bahaya").
- Skor risiko kardiovaskular: **tidak disediakan di v1** (lihat `references/sumber-pedoman.md`
  bagian "Yang sengaja tidak disertakan") — arahkan ke WHO/HEARTS risk chart resmi.
- IMT anak/remaja (< 18 tahun) → pakai grafik pertumbuhan WHO/Kemenkes (z-score), bukan alat ini.
- Menampilkan, menulis ulang, menerjemahkan, atau memandu **pelaksanaan** MMSE/MoCA (formulir,
  butir soal, instruksi, cara skor per butir). Lihat "Instrumen kognitif" di bawah.

## Langkah 0 — WAJIB: pastikan peran pengguna
Jika peran belum jelas, tanyakan sekali: *"Sebelum mulai: Anda tenaga kesehatan (dokter, bidan,
perawat, ahli gizi, psikolog klinis) yang menangani pasien ini?"*
- **Ya (nakes)** → lanjut langkah kerja.
- **Bukan / pasien / keluarga** → **jangan** jalankan skrining atau menafsirkan skor. Beri
  edukasi umum singkat, sarankan konsultasi, dan **bila ibu hamil sedang bergejala** (pusing/sakit
  kepala hebat, pandangan kabur, nyeri ulu hati, bengkak mendadak, perdarahan, kejang) minta
  periksa **hari ini** ke bidan/puskesmas/IGD atau 119. Kalimat baku:
  `references/batasan-dan-kalimat-baku.md`.
- Pertanyaan umum tanpa pasien (mis. mahasiswa kebidanan belajar rumus) → boleh jelaskan rumus
  & sumber, tetap dengan penafian.

## Input
| Kalkulator | Wajib | Opsional / default |
|---|---|---|
| Preeklampsia | daftar faktor yang ada (bahasa bebas → petakan ke kode) | TD sistolik/diastolik, usia ibu, IMT, **gejala bahaya**; pedoman `kia` (default) atau `nice` |
| Kehamilan | HPHT **atau** (tanggal USG + usia saat USG) | siklus (default 28 hari), tanggal periksa (default hari ini) |
| BB hamil | tinggi, BB pra-hamil | BB sekarang, usia kehamilan (minggu), kembar |
| IMT dewasa | tinggi (cm atau m), berat (kg) | lingkar perut (cm) + jenis kelamin L/P; banyak pasien → CSV |
| Kognitif | instrumen (mmse/moca/amt), skor total | lama pendidikan (tahun) — **wajib untuk MoCA** |

**Data minimal:** tidak perlu nama pasien. Pakai inisial/nomor RM klinik bila perlu label.
Jangan minta NIK, alamat, atau nomor HP. Jika pengguna menempel nama lengkap, pakai inisial di
output. Jika input wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5).

## Lapisan tanda bahaya (diperiksa SEBELUM saran rutin apa pun)
Script `map` dan `preeklampsia` selalu memeriksa ini dulu:
- **TD ≥ 160 sistolik atau ≥ 110 diastolik**, atau ada **gejala bahaya** (`--gejala`) →
  `TANDA BAHAYA - SEGERA EVALUASI/RUJUK` sesuai protokol kegawatdaruratan fasilitas.
- **TD ≥ 140 sistolik atau ≥ 90 diastolik** → `TD RENTANG HIPERTENSI - EVALUASI/RUJUK HARI INI`.
- **TD < 90 sistolik atau < 60 diastolik** → `TD RENDAH - EVALUASI KLINIS SESUAI PROTOKOL`
  (ambang konservatif, sumber NHLBI < 90/60; **PERLU REVIEW medis**).
- **TD hanya satu angka** (mis. "170, diastolik lupa"): jalankan dengan angka yang ada saja
  (`--sistolik 170`) — ambang tetap dinilai, MAP tidak dihitung, script menulis angka yang
  kurang. Tanpa TD sama sekali, script menulis "Tanda bahaya (TD/gejala) belum diperiksa" —
  sampaikan apa adanya, jangan simpulkan "ANC rutin".
- **Setiap kali TD atau gejala disebut** di permintaan apa pun (HPL, BB hamil, IMT), jalankan
  juga `map` (dengan `--gejala`) agar lapisan ini selalu diperiksa.
- Sumber ambang: NICE NG133 (2019, diperbarui 2023) & ACOG Practice Bulletin 222 (2020);
  gejala: Buku KIA (cetakan 2025) & NICE NG133. Keduanya **tidak pernah** berakhir dengan
  "Lanjutkan ANC rutin". Tulis baris tanda bahaya **paling atas** di jawaban.
- Bila pengguna menyebut gejala dalam kalimat biasa, petakan ke kode `--gejala` (daftar:
  `python3 scripts/klinis.py faktor-preeklampsia`). Ragu → tetap masukkan (lebih aman).

## Langkah kerja
1. Langkah 0 (peran). 2. Kenali kalkulator yang diminta (bisa lebih dari satu).
3. Petakan bahasa bebas ke kode faktor & gejala (`python3 scripts/klinis.py
   faktor-preeklampsia`, atau `references/preeklampsia.md`). Faktor yang **tidak disebut** →
   anggap tidak ada, tapi tulis "belum ditanyakan" untuk faktor penting yang tidak dibahas.
4. **Jalankan script** (Windows: `python` atau `py`):
   ```
   python3 scripts/klinis.py preeklampsia --faktor nullipara,riwayat-keluarga --sistolik 118 --diastolik 82 --usia-ibu 36 [--gejala pandangan-kabur]
   python3 scripts/klinis.py kehamilan --hpht 2026-03-10 --siklus 30 --tanggal-periksa 2026-09-29 --usg-tanggal 2026-05-02 --usg-minggu 7 --usg-hari 3
   python3 scripts/klinis.py bb-hamil --tinggi 155 --bb-prahamil 62 --bb-sekarang 68 --usia-minggu 24
   python3 scripts/klinis.py imt --tinggi 165 --berat 72 --lingkar-perut 92 --jk L
   python3 scripts/klinis.py imt-batch --file pasien.csv     # kolom: id,tinggi,berat[,lingkar_perut,jk]
   python3 scripts/klinis.py kognitif --instrumen moca --skor 24 --pendidikan-tahun 9
   ```
   Tambah `--json` (letakkan **sebelum** sub-perintah: `klinis.py --json imt ...`) bila perlu
   data terstruktur. Kode keluar 1 = input tidak valid → sampaikan pesannya apa adanya dan minta
   data yang benar; **jangan menebak angka**. Khusus kode gejala/faktor tak dikenal: hasil
   (termasuk ‼️ tanda bahaya) tetap tercetak dulu, lalu daftar kode tak dikenal + kode valid di
   stderr (exit 1) → sampaikan tanda bahaya lebih dulu, lalu petakan ulang kodenya dan jalankan
   lagi.
5. Jika Python tidak bisa dijalankan: hitung manual dengan rumus di `references/`, tulis
   "dihitung manual — verifikasi ulang", dan **tetap** terapkan lapisan tanda bahaya dulu.
   Tanggal wajib dihitung per hari kalender (kabisat!).
6. Susun output sesuai format di bawah. Salin angka & kalimat tindak lanjut **persis** dari script.
7. Periksa checklist sebelum mengirim.

## Format output
```
🩺 [Nama kalkulator] — [inisial/ID pasien bila diberikan] — [tanggal periksa]

[Bila ada] ‼️ TANDA BAHAYA: [alasan dari script] → [tindak lanjut dari script]

Hasil:
- [angka/kategori dari script, dengan nama pedoman yang dipakai]

Arti untuk tindak lanjut:
- [kalimat dari script; tanpa dosis, tanpa diagnosis pasti]

Catatan: [catatan script: aturan & sumbernya, asumsi, batas, pembulatan]
Sumber: [pedoman + tahun, persis dari script]
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap
pada dokter/bidan yang memeriksa.
```
Catatan sesi stimulasi kognitif: `templates/catatan-sesi-stimulasi-kognitif.md`; ringkasan ANC:
`templates/ringkasan-anc.md`.

## Contoh
**Input:** "Saya bidan. Bu R, G1P0A0, 36 th, hamil 14 minggu, TD 120/80, IMT sebelum hamil 31,
ibunya dulu preeklampsia. Skrining preeklampsia ya."

**Proses:** faktor = nullipara, riwayat-keluarga; angka → `--sistolik 120 --diastolik 80
--usia-ibu 36 --imt 31`. Tidak ada tanda bahaya (TD < 140/90, tidak ada gejala disebut).

**Output (ringkas):**
```
🩺 Skrining faktor risiko preeklampsia — Bu R — 29 September 2026
Hasil:
- MAP 93,3 mmHg (≥ 90)
- Kategori (Buku KIA cetakan 2025): RISIKO SEDANG (≥ 2 faktor sedang) — 5 faktor sedang:
  nullipara, usia ≥ 35, riwayat preeklampsia pada ibu, obesitas pra-hamil (IMT > 30),
  MAP ≥ 90. Faktor tinggi: tidak ada.
- Belum ditanyakan: diabetes, penyakit ginjal, autoimun/APS, proteinuria.
Arti untuk tindak lanjut:
- Memenuhi kriteria ibu berisiko preeklampsia menurut Buku KIA: pemeriksaan kehamilan,
  persalinan, dan nifas di Rumah Sakit; rujukan terencana (tidak perlu menunggu inpartu).
  Pelaksanaan sesuai protokol fasilitas & keputusan dokter. Obat pencegahan/dosis bukan
  bagian alat ini.
Sumber: Kemenkes RI, Buku KIA edisi terbaru (cetakan 2025) — lembar skrining preeklampsia
< 20 minggu; rumus MAP, ambang MAP ≥ 90.
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis.
```
Contoh TD 170/115: hasil diawali `‼️ TANDA BAHAYA — SEGERA evaluasi/rujuk sesuai protokol
kegawatdaruratan fasilitas` (sumber NICE NG133/ACOG PB 222), skrining faktor hanya pelengkap.
Contoh lengkap lain: `examples/`.

## Instrumen kognitif (MMSE, MoCA, AMT)
- Alat ini **hanya menafsirkan skor total yang dimasukkan nakes**. Alat ini **tidak memuat,
  mereproduksi, menerjemahkan, atau memandu** formulir, butir, instruksi, atau penskoran per
  butir MMSE/MoCA.
- Memakai formulir **MoCA** memerlukan **lisensi/izin dan pelatihan-sertifikasi milik pengguna
  sendiri** dari pemegang hak cipta (MoCA Cognition). Memakai formulir **MMSE** memerlukan
  **lisensi milik pengguna sendiri** dari PAR Inc. Nama instrumen disebut hanya sebagai penyebut
  produk; Komunitech tidak berafiliasi dengan pemegang hak cipta mana pun.
- Status: **PERLU REVIEW** (klinis: ambang; legal: pemakaian nama & tafsir skor dalam produk
  berbayar — lihat `references/sumber-pedoman.md`).

## Checklist sebelum mengirim
- [ ] Peran nakes sudah dipastikan (atau jawaban edukasi umum untuk awam).
- [ ] Tanda bahaya diperiksa lebih dulu; bila ada, baris ‼️ di paling atas dan **tidak ada**
      kalimat "ANC rutin".
- [ ] Semua angka dari script (atau ditandai "dihitung manual — verifikasi ulang").
- [ ] Nama pedoman yang dipakai disebut untuk setiap aturan (Buku KIA vs NICE tidak dicampur).
- [ ] Ada baris **Sumber** (pedoman + tahun) dan baris penafian ⚠️.
- [ ] Tidak ada dosis obat, nama obat sebagai anjuran, atau diagnosis pasti.
- [ ] Tidak ada nama lengkap/NIK/alamat/no. HP pasien.
- [ ] Tidak menulis butir/instruksi MMSE/MoCA.

## Batasan & penanganan error
- **Angka tidak masuk akal** (TD 80/120, tinggi 16 cm, HPHT di masa depan): script menolak
  dengan pesan jelas → minta pengguna cek ulang/satuan.
- **CSV `imt-batch`:** pemisah koma atau titik koma (;) dikenali otomatis. Koma desimal pada
  CSV berpemisah koma tanpa tanda kutip → baris itu "GAGAL - TIDAK DIHITUNG" + petunjuk
  (pakai titik desimal, tanda kutip, atau pemisah ;); baris lain tetap dihitung.
- **Satuan:** tinggi ≥ 3 dianggap cm, < 3 dianggap meter; berat kg; TD mmHg; koma desimal
  boleh ("1,65"). Pon/inci → minta dikonversi dulu oleh pengguna (jangan tebak).
- **Siklus di luar 21–45 hari atau UK HPHT > 44 minggu:** bila ada data USG, script tetap
  menghitung dengan USG dan menandai "HPHT TIDAK ANDAL"; tanpa USG → minta data USG.
- **Skrining preeklampsia > 20 minggu:** tetap bisa dihitung; sebutkan bahwa lembar Buku KIA
  dirancang untuk < 20 minggu. TD ≥ 140/90 pada usia berapa pun → lapisan tanda bahaya.
- **Faktor ambigu:** "dulu hamil darah tinggi" → tanyakan: didiagnosis preeklampsia
  (`riwayat-preeklampsia`) atau hanya hipertensi tanpa preeklampsia
  (`riwayat-hipertensi-kehamilan`; tidak ada di lembar KIA, tinggi di NICE). "Gula tinggi
  waktu hamil" → `diabetes-gestasional`; DM sejak sebelum hamil → `diabetes-pregestasional`.
- **Dua pedoman berbeda** (Buku KIA vs NICE: kembar tinggi vs sedang; usia 35 vs 40; IMT > 30
  vs ≥ 35; proteinuria & MAP hanya di KIA; diabetes gestasional hanya di KIA): default Buku KIA;
  script menyebut pedoman untuk setiap aturan dan mencatat faktor yang hanya ada di pedoman lain.
- **MoCA tanpa lama pendidikan:** script menolak — tanyakan lama sekolah (tahun).
- **Batas yang PERLU REVIEW tenaga medis:** `references/sumber-pedoman.md` bagian "Status
  verifikasi". Alat ini belum boleh dijual sebelum ditinjau dokter/bidan.
