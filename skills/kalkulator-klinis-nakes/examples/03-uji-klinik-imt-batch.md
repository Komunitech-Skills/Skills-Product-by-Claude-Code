# Uji 03 — Normal: klinik, IMT & lingkar perut batch 10 pasien

Penguji independen, 2026-09-29, `claude-code (simulasi agent)`. Data fiktif (ID klinik saja).

## Input pengguna
> "Saya perawat klinik (posbindu karyawan). Tolong hitung IMT + lingkar perut 10 orang ini:
> K-01 L 165/72/LP92; K-02 P 1,58 m/54/79,5; K-03 P 152/58/80; K-04 L 170/66,5/90;
> K-05 P 160/58,8/86; K-06 L 175/95/104; K-07 P 148/40/66; K-08 L 168/70,6/88;
> K-09 (jk lupa) 162/60/85; K-10 P 155/62,5/81."

## Langkah agent
Script tidak punya mode batch → agent menjalankan `imt` 10 kali (`--json`). K-09 ditolak script
("isi jenis kelamin L atau P untuk menilai lingkar perut") → agent menjalankan ulang tanpa LP dan
menandai LP "perlu jenis kelamin".

## Output agent (dengan skill)
| ID | IMT | Asia-Pasifik (WPRO 2000) | Kemenkes (PGS 2014) | Lingkar perut |
|---|---|---|---|---|
| K-01 | 26,4 | Obesitas I | Gemuk ringan (25,1–27,0) | ≥ 90 → obesitas sentral |
| K-02 | 21,6 | Normal | Normal | < 80 |
| K-03 | 25,1 | Obesitas I | Gemuk ringan | **tepat 80** → ≥ 80 obesitas sentral; *ukur ulang* |
| K-04 | 23,0 | BB lebih/berisiko | Normal | **tepat 90** → ≥ 90; *ukur ulang* |
| K-05 | 23,0 | BB lebih/berisiko | Normal | ≥ 80 → obesitas sentral |
| K-06 | 31,0 | Obesitas II | Gemuk berat/obesitas | ≥ 90 → obesitas sentral |
| K-07 | 18,3 | BB kurang | Kurus ringan (17,0–18,4) | < 80 |
| K-08 | 25,0 | Obesitas I | **Normal** (18,5–25,0) | < 90 |
| K-09 | 22,9 | Normal | Normal | belum dinilai — jenis kelamin? |
| K-10 | 26,0 | Obesitas I | Gemuk ringan | ≥ 80 → obesitas sentral |

Catatan: IMT dibulatkan 1 desimal lalu dikategorikan; hanya untuk dewasa ≥ 18 th, tidak untuk
ibu hamil. Sumber: WHO WPRO/IASO/IOTF 2000; Kemenkes, Pedoman Gizi Seimbang (Permenkes 41/2014).
⚠️ Alat bantu untuk tenaga kesehatan, bukan pengganti penilaian klinis.

## Verifikasi independen
Hitung penguji (Fraction, pembulatan setengah ke atas): 72/1,65²=26,45→26,4; 54/1,58²=21,63;
58/1,52²=25,10; 66,5/1,70²=23,01; 58,8/1,60²=22,97→23,0; 95/1,75²=31,02; 40/1,48²=18,26→18,3;
70,6/1,68²=25,01→25,0; 60/1,62²=22,86→22,9; 62,5/1,55²=26,01 → **10/10 cocok**. Uji acak
20.000 pasangan TB/BB di `verifikasi.py` → 0 selisih untuk IMT, kategori AP, Kemenkes, IOM.

Sumber ambang: Asia-Pasifik & lingkar perut ≥ 90/≥ 80 — PDF WPRO 2000 di IRIS WHO berupa hasil
pindai (tidak bisa dibaca mesin di lingkungan uji); dikonfirmasi lewat sumber sekunder (PMC12126285:
23–24,9 overweight, ≥ 25 obesitas Asia). Tabel Kemenkes: naskah Permenkes 41/2014 di BPK →
HTTP 403; dikonfirmasi lewat ringkasan peraturan.go.id (< 17 / 17–<18,5 / 18,5–25,0 / >25,0–27,0 / > 27,0).

## Catatan penguji
- ✔ Tepat 80/90 cm ditandai "ukur ulang" (WPRO ≥ vs materi Kemenkes ">").
- ⚠️ K-08: IMT 25,0 = "Obesitas I" (AP) tapi "Normal" (Kemenkes) — output tidak menjelaskan
  kapan memakai yang mana (temuan R9).
- ⚠️ Satu nilai kurang (jk) membuat seluruh perhitungan ditolak; lebih baik IMT tetap dihitung
  dan LP ditandai (temuan R3). Tidak ada mode batch/CSV (kenyamanan, bukan kesalahan).

Skor skenario: 8/10.
