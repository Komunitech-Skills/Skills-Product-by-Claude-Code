# 02 — HPL, usia kehamilan (siklus 35 hari + USG) dan kenaikan BB

> Contoh dari pembuat skill (data fiktif). Belum uji independen.

**Input:** "Dokter di sini. Pasien ID 0412, HPHT 20 Feb 2026, siklus 35 hari, USG 18 April 2026
usia 7 minggu 0 hari. TB 152, BB sebelum hamil 44, sekarang 47. Hari ini 29 Sep 2026. Hitung HPL,
usia kehamilan, dan kenaikan BB-nya."

**Perintah:**
```
python3 scripts/klinis.py kehamilan --hpht 2026-02-20 --siklus 35 --tanggal-periksa 2026-09-29 --usg-tanggal 2026-04-18 --usg-minggu 7 --usg-hari 0
python3 scripts/klinis.py bb-hamil --tinggi 152 --bb-prahamil 44 --bb-sekarang 47 --usia-minggu 30
```
**Output script (v1.0.1):**
```
Tanggal periksa: 29 September 2026 (2026-09-29)
HPHT: 20 Februari 2026 (2026-02-20)
Siklus (hari): 35
HPL (Naegele): 4 Desember 2026 (2026-12-04)
HPL (HPHT + 280 hari): 4 Desember 2026 (2026-12-04)
Usia kehamilan menurut HPHT: 30 minggu 4 hari
USG: 18 April 2026 (2026-04-18), usia 7 minggu 0 hari
HPL (USG): 5 Desember 2026 (2026-12-05)
Usia kehamilan menurut USG: 30 minggu 3 hari
Selisih HPHT vs USG (hari): 1
Ambang ACOG (hari): 5
Penanggalan dipakai: HPHT
USIA KEHAMILAN DIPAKAI: 30 minggu 4 hari
Trimester: Trimester 3
Catatan: Siklus 35 hari: HPL & usia kehamilan digeser +7 hari (modifikasi umum Naegele; bukan bagian ACOG CO 700).
Catatan: Selisih HPHT vs USG 1 hari; ambang ACOG untuk USG usia 7 minggu 0 hari adalah > 5 hari -> HPHT tetap dipakai.
Sumber: Aturan Naegele (HPHT + 7 hari - 3 bulan + 1 tahun); penyesuaian siklus = modifikasi umum (siklus - 28 hari)
Sumber: ACOG Committee Opinion No. 700 Methods for Estimating the Due Date (2017, reaffirmed 2025)
PENTING: Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap pada dokter/bidan yang memeriksa.

IMT pra-hamil (kg/m2): 19.0
Kategori IMT (IOM): Normal (18,5-24,9)
Rekomendasi kenaikan total: 11,5-16 kg
Laju trimester 2-3 (kg/minggu): 0,35-0,50
Kenaikan sejauh ini (kg): 3.0
Usia kehamilan (minggu): 30
Perkiraan rentang saat ini (kg): 6.5-10.5
Posisi: Kenaikan 3.0 kg di bawah perkiraan rentang 6.5-10.5 kg
Catatan: IOM memakai batas IMT WHO internasional (bukan Asia-Pasifik).
Catatan: Keterbatasan: IOM 2009 menyatakan pedomannya tidak dimaksudkan untuk populasi yang jauh lebih pendek/kurus dari perempuan Amerika; untuk ibu Indonesia pakai sebagai acuan umum, bukan target mutlak.
Catatan: Perkiraan rentang saat ini = turunan: trimester 1 0,5-2 kg + laju IOM x (minggu - 13). Bukan tabel resmi; pakai sebagai gambaran kasar.
Sumber: Institute of Medicine & National Research Council, Weight Gain During Pregnancy: Reexamining the Guidelines (2009)
PENTING: Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis. Keputusan klinis tetap pada dokter/bidan yang memeriksa.
```
**Verifikasi manual:**
- Naegele: 20 Feb + 7 = 27 Feb → + 9 bulan = 27 Nov 2026 → + 7 (siklus 35) = 4 Des 2026 ✓.
- +280+7 = 287 hari: sisa Feb 8 + Mar–Nov 275 = 283 → 4 Des 2026 ✓.
- Usia: 20 Feb→29 Sep = 221 hari − 7 = 214 = 30 mg 4 hr ✓.
- Pada tanggal USG: 57 − 7 = 50 hari (HPHT) vs 49 (USG) → selisih 1, ambang > 5 → HPHT ✓.
- IMT 44 / 1,52² = 44 / 2,3104 = 19,04 → 19,0 normal → 11,5–16 kg ✓.
- 30 minggu: 0,5 + 0,35×17 = 6,45 → 6,5 ; 2 + 0,50×17 = 10,5 → kenaikan 3 kg di bawah rentang ✓.

**Jawaban agent (ringkas):** HPL 4 Desember 2026 (Naegele disesuaikan siklus = HPHT+280
disesuaikan), USG konsisten (selisih 1 hari) → penanggalan HPHT dipakai; usia kehamilan 30 minggu
4 hari (trimester 3). IMT pra-hamil 19,0 (normal): rekomendasi total 11,5–16 kg; kenaikan 3,0 kg
di bawah perkiraan rentang kasar 6,5–10,5 kg → pertimbangkan evaluasi asupan/status gizi sesuai
penilaian Anda. Sumber: Naegele; ACOG CO 700 (2017, reaffirmed 2025); IOM 2009 (acuan umum — IOM tidak dirancang khusus untuk ibu bertubuh lebih pendek/kurus). ⚠️ Alat bantu, bukan pengganti
penilaian klinis.
