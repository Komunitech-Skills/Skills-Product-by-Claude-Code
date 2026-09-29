# Kalkulator kehamilan, IMT, dan kenaikan berat badan — rumus manual

Pakai bila script tidak bisa dijalankan. Tulis "dihitung manual — verifikasi ulang".

## HPL & usia kehamilan
- **Naegele:** HPHT + 7 hari, lalu + 9 bulan kalender (= − 3 bulan + 1 tahun). Bila tanggal
  hasil tidak ada (mis. 31 Feb), pakai tanggal terakhir bulan itu.
- **HPHT + 280 hari:** dihitung per hari kalender (perhatikan tahun kabisat: 2028, 2032).
  Naegele dan +280 bisa beda 1–3 hari; keduanya ditampilkan.
- **Siklus ≠ 28 hari (21–45):** geser HPL dan kurangi usia kehamilan sebesar (siklus − 28) hari.
  Di luar 21–45 hari atau tidak teratur → HPHT tidak andal; bila ada USG, script tetap menghitung
  dengan USG (HPHT diabaikan dan ditandai), tanpa USG → minta data USG.
- **Usia kehamilan (HPHT)** = (tanggal periksa − HPHT) − (siklus − 28) hari → minggu + hari.
- **Usia kehamilan (USG)** = usia saat USG + (tanggal periksa − tanggal USG).
- **Trimester:** T1 ≤ 13 mg 6 hr; T2 14 mg 0 hr – 27 mg 6 hr; T3 ≥ 28 mg 0 hr (ACOG).

### Penanggalan ulang dengan USG (ACOG CO 700, 2017, reaffirmed 2025)
Hitung selisih usia kehamilan HPHT vs USG **pada tanggal USG**. Pakai USG bila selisih melebihi:

| Usia kehamilan saat USG | Selisih yang memicu penanggalan ulang |
|---|---|
| ≤ 8 mg 6 hr | > 5 hari |
| 9 mg 0 hr – 13 mg 6 hr | > 7 hari |
| 14 mg 0 hr – 15 mg 6 hr | > 7 hari |
| 16 mg 0 hr – 21 mg 6 hr | > 10 hari |
| 22 mg 0 hr – 27 mg 6 hr | > 14 hari |
| ≥ 28 mg 0 hr | > 21 hari |

Tanpa HPHT → USG dipakai. Catatan lokal (PERLU REVIEW): Buku KIA memakai selisih ≥ 3 minggu
antara UK USG TM I/HPHT dan USG TM III untuk trimester 3 — sebutkan bila fasilitas memakai
aturan KIA. Kehamilan bayi tabung: ACOG memakai tanggal transfer embrio — alat ini
belum mendukung; hitung dari data USG/klinik fertilitas.

## IMT
IMT = berat (kg) / tinggi (m)². Dibulatkan 1 desimal (setengah ke atas), baru dikategorikan.

| Asia-Pasifik (WPRO 2000) | | Kemenkes (Pedoman Gizi Seimbang 2014) | |
|---|---|---|---|
| < 18,5 | BB kurang | < 17,0 | Kurus berat |
| 18,5–22,9 | Normal | 17,0–18,4 | Kurus ringan |
| 23,0–24,9 | BB lebih/berisiko | 18,5–25,0 | Normal |
| 25,0–29,9 | Obesitas I | 25,1–27,0 | Gemuk ringan |
| ≥ 30,0 | Obesitas II | > 27,0 | Gemuk berat/obesitas |

**Lingkar perut** (obesitas sentral, WPRO 2000): laki-laki ≥ 90 cm, perempuan ≥ 80 cm.
Materi Kemenkes menulis "lebih dari 90/80"; tepat 90/80 → ukur ulang dan catat.

## Kenaikan berat badan selama hamil (IOM 2009)
Kategori IMT pra-hamil memakai batas **WHO internasional** (bukan Asia-Pasifik).

| IMT pra-hamil | Total (janin tunggal) | Laju T2–T3 (kg/minggu) | Total (kembar, provisional) |
|---|---|---|---|
| < 18,5 | 12,5–18 kg | 0,44–0,58 | tidak ada rekomendasi |
| 18,5–24,9 | 11,5–16 kg | 0,35–0,50 | 17–25 kg |
| 25,0–29,9 | 7–11,5 kg | 0,23–0,33 | 14–23 kg |
| ≥ 30,0 | 5–9 kg | 0,17–0,27 | 11–19 kg |

**Perkiraan rentang saat ini (turunan, bukan tabel resmi):** untuk usia > 13 minggu,
bawah = 0,5 + laju_bawah × (minggu − 13); atas = 2 + laju_atas × (minggu − 13); kedua batas
dan kenaikan dibulatkan 1 desimal **sebelum** dibandingkan (agar posisi konsisten dengan angka
yang ditampilkan). Usia ≤ 13 minggu: dibandingkan dengan asumsi IOM trimester 1 = 0,5–2 kg.

**Keterbatasan:** IOM 2009 menyatakan pedomannya tidak dimaksudkan untuk populasi yang jauh
lebih pendek/kurus dari perempuan Amerika — untuk ibu Indonesia pakai sebagai acuan umum.

## Kapan memakai kategori IMT Asia-Pasifik vs Kemenkes
IMT 23,0–27,0 bisa berbeda kategori (mis. 25,0 = Obesitas I menurut Asia-Pasifik, Normal
menurut Kemenkes). Asia-Pasifik lazim untuk penilaian risiko metabolik individu; ambang
Kemenkes lazim untuk laporan gizi/posbindu sesuai format dinas. Pakai yang diminta fasilitas
dan sebutkan acuannya (PERLU REVIEW).

## IMT banyak pasien (posbindu)
`python3 scripts/klinis.py imt-batch --file data.csv` — kolom `id,tinggi,berat` (opsional
`lingkar_perut,jk`). Baris rusak ditandai "TIDAK DIHITUNG", baris lain tetap dihitung. Pakai
ID/inisial, bukan nama lengkap.
