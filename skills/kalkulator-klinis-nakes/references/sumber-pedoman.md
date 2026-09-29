# Sumber pedoman, status verifikasi, dan lisensi instrumen

Diperiksa kurator: 2026-09-29. **Seluruh skill berstatus PERLU REVIEW tenaga medis** (keputusan
pemilik 2026-09-29) — dokter/bidan wajib meninjau ambang & kalimat tindak lanjut sebelum rilis.

## Daftar sumber (dikutip di output script)
| Kode | Sumber | Tahun | Dipakai untuk | Status verifikasi kurator |
|---|---|---|---|---|
| kia | Kemenkes RI, *Buku Kesehatan Ibu dan Anak* (lembar skrining preeklampsia < 20 minggu) | 2023 | Daftar faktor sedang/tinggi, aturan ≥ 2 sedang atau ≥ 1 tinggi, MAP > 90 | **Sebagian.** Daftar 16 butir & aturan dikonfirmasi lewat artikel sekunder yang mengutip Buku KIA (lihat URL di bawah); naskah Buku KIA asli belum dibaca langsung. PERLU REVIEW: bunyi persis "usia ≥ 35" vs "> 35", letak "proteinuria" (merah), dan kalimat tindak lanjut. |
| nice | NICE NG133 *Hypertension in pregnancy: diagnosis and management* | 2019, diperbarui 2023 | Pembanding (opsi `--pedoman nice`) | Daftar faktor dari pengetahuan kurator + ringkasan resmi; halaman NICE memblokir pengambilan otomatis. PERLU REVIEW. |
| map | Rumus MAP = (S + 2D)/3 | — | MAP | Rumus baku. |
| naegele | Aturan Naegele; penyesuaian siklus (siklus − 28) | — | HPL | Rumus baku; penyesuaian siklus = praktik umum, bukan rekomendasi ACOG. |
| acog | ACOG Committee Opinion No. 700 *Methods for Estimating the Due Date* | 2017 | Ambang penanggalan ulang USG | Tabel ambang dikonfirmasi (≤ 8 6/7: > 5 hr; 9 0/7–13 6/7: > 7; 14 0/7–15 6/7: > 7; 16 0/7–21 6/7: > 10; 22 0/7–27 6/7: > 14; ≥ 28 0/7: > 21). |
| iom | IOM & NRC, *Weight Gain During Pregnancy: Reexamining the Guidelines* | 2009 | Rekomendasi kenaikan BB | Angka tabel standar IOM (termasuk kembar "provisional"). |
| ap | WHO WPRO/IASO/IOTF, *The Asia-Pacific Perspective: Redefining Obesity and its Treatment* | 2000 | IMT Asia-Pasifik, lingkar perut ≥ 90/≥ 80 | Standar luas dipakai. |
| kemenkes_imt | Kemenkes RI, Pedoman Gizi Seimbang (Permenkes 41/2014) | 2014 | Batas ambang IMT Indonesia (< 17 / 17–18,4 / 18,5–25 / 25,1–27 / > 27) | Dikonfirmasi lewat materi turunan Kemenkes/RSUD; PERLU REVIEW terhadap naskah asli. |
| mmse | Folstein dkk. 1975; Tombaugh & McIntyre 1992 | 1975/1992 | Ambang 24 & rentang 24–30/18–23/0–17 | Standar literatur. |
| moca | Nasreddine dkk. 2005; Husein dkk. 2010 (MoCA-Ina, Neurona 27(4)) | 2005/2010 | Ambang ≥ 26, +1 bila pendidikan ≤ 12 th | Dikonfirmasi: studi MoCA-Ina 2010 **tidak** menetapkan titik potong Indonesia (hanya melaporkan sebaran dengan 26 dan 23) → alat memakai 26 dan menyebutkannya. |
| amt | Hodkinson 1972; formulir AMT Permenkes 67/2015 | 1972/2015 | Rentang 8–10 / 4–7 / 0–3 | Permenkes 67/2015 memuat AMT (dikonfirmasi); pembagian rentang **belum** dibaca dari naskah asli → PERLU REVIEW. |

URL yang dipakai saat riset (2026-09-29):
- Buku KIA 2023 (dikutip sekunder): https://wpcpublisher.com/jurnal/index.php/HRJI/article/view/1012 ;
  https://fkkmk.ugm.ac.id/deteksi-dini-preeklamsia-dengan-penggunaan-buku-kia-versi-terbaru/ ;
  https://anyflip.com/trrop/fjqu/basic (salinan Buku KIA 2023)
- NICE NG133: https://www.nice.org.uk/guidance/ng133
- ACOG CO 700: https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2017/05/methods-for-estimating-the-due-date
- MoCA izin & sertifikasi: https://mocacognition.com/permission/ ; https://mocacognition.com/training-certification/
- MMSE hak cipta PAR: https://www.parinc.com/about/connect-with-us/licensing-team ;
  https://pmc.ncbi.nlm.nih.gov/articles/PMC4160306/
- MoCA-Ina: https://arsip.neurona.web.id/paper/734.pdf
- Permenkes 67/2015: https://peraturan.bpk.go.id/Home/Details/116533/permenkes-no-67-tahun-2015
- Lingkar perut Kemenkes (materi turunan): https://rsudmyamin.sumbarprov.go.id/blog/kenali-dan-cegah-obesitas

## Putusan lisensi instrumen kognitif
| Instrumen | Pemilik hak | Putusan untuk skill ini |
|---|---|---|
| MMSE | PAR Inc. (sejak 2001) — reproduksi/terjemahan butir wajib izin tertulis | **Butir tidak dimuat.** Hanya menerima skor total + ambang literatur. |
| MoCA / MoCA-Ina | Z. Nasreddine / MoCA Cognition — sejak 1 Sep 2019 pemeriksa wajib pelatihan & sertifikasi; entitas komersial wajib izin tertulis & perjanjian lisensi | **Butir tidak dimuat.** Hanya menerima skor total dari pemeriksa bersertifikat; skill mengingatkan kewajiban sertifikasi. |
| AMT | Hodkinson 1972, dipakai bebas & dimuat di Permenkes 67/2015 | Aman secara lisensi, tetapi v1 tetap hanya menerima skor total (klinik memakai formulir resmi). |

## Yang sengaja tidak disertakan di v1
- **Skor risiko kardiovaskular tanpa lab.** Kandidat terbaik (WHO CVD risk chart non-lab 2019,
  wilayah Asia Tenggara) berupa tabel/persamaan terkalibrasi per wilayah yang harus diambil
  persis dari sumber resmi; Framingham BMI-based (2008) tidak terkalibrasi untuk Indonesia.
  Menghitung dari ingatan berisiko salah → **dilewati**; arahkan ke WHO HEARTS risk chart resmi.
- Dosis obat apa pun (keputusan pemilik).
- Kalkulator untuk anak (z-score WHO) — butuh tabel LMS panjang; kandidat v2.
