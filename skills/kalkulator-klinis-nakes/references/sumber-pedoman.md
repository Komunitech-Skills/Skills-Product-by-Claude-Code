# Sumber pedoman, status verifikasi, dan lisensi instrumen

Diperiksa kurator: 2026-09-29. **Seluruh skill berstatus PERLU REVIEW tenaga medis** (keputusan
pemilik 2026-09-29) — dokter/bidan wajib meninjau ambang & kalimat tindak lanjut sebelum rilis.

## Daftar sumber (dikutip di output script)
| Kode | Sumber | Tahun | Dipakai untuk | Status verifikasi kurator |
|---|---|---|---|---|
| kia | Kemenkes RI, *Buku Kesehatan Ibu dan Anak* edisi terbaru — cetakan Ditjen Kesehatan Primer dan Komunitas **2025**, ISBN 978-623-301-149-5 (lembar skrining preeklampsia < 20 minggu; tanda bahaya ibu hamil) | 2025 | Daftar faktor sedang/tinggi, aturan ≥ 2 sedang dan/atau ≥ 1 tinggi, **MAP ≥ 90**, proteinuria = **sedang**, kalimat tindak lanjut (ANC/persalinan/nifas di RS, rujukan terencana) | **Primer dibaca penguji independen 2026-09-29** (PDF resmi ayosehat.kemkes.go.id, hlm. cetak 102–103). v1.0.1 disamakan: MAP ≥ 90 (bukan > 90), proteinuria sedang (bukan tinggi), label "Multipara dengan riwayat preeklampsia sebelumnya", kalimat tindak lanjut. PERLU REVIEW: cocokkan dengan cetakan yang dipakai fasilitas (sekunder 2024 menulis "> 90"). |
| nice | NICE NG133 *Hypertension in pregnancy: diagnosis and management* | 2019, diperbarui 2023 | Pembanding (opsi `--pedoman nice`), definisi hipertensi ≥ 140/90 & hipertensi berat ≥ 160/110 (lapisan tanda bahaya) | Rek. 1.1.2–1.1.3 dicek penguji (https://www.nice.org.uk/guidance/ng133/chapter/Recommendations). v1.0.1: hanya **DM tipe 1/2** yang tinggi (bukan diabetes gestasional); "hypertensive disease during a previous pregnancy" dipisah sebagai kode sendiri. |
| acog_pb222 | ACOG Practice Bulletin No. 222 *Gestational Hypertension and Preeclampsia* | 2020 | Rentang berat ≥ 160 sistolik atau ≥ 110 diastolik (lapisan tanda bahaya) | Dari pengetahuan kurator; belum dibaca ulang dari naskah (berbayar). PERLU REVIEW terhadap protokol fasilitas/PNPK. |
| map | Rumus MAP = (S + 2D)/3 | — | MAP | Rumus baku. |
| naegele | Aturan Naegele; penyesuaian siklus (siklus − 28) | — | HPL | Rumus baku; penyesuaian siklus = praktik umum, bukan rekomendasi ACOG. |
| acog | ACOG Committee Opinion No. 700 *Methods for Estimating the Due Date* | 2017, reaffirmed 2025 | Ambang penanggalan ulang USG | Tabel ambang dikonfirmasi (≤ 8 6/7: > 5 hr; 9 0/7–13 6/7: > 7; 14 0/7–15 6/7: > 7; 16 0/7–21 6/7: > 10; 22 0/7–27 6/7: > 14; ≥ 28 0/7: > 21). |
| iom | IOM & NRC, *Weight Gain During Pregnancy: Reexamining the Guidelines* | 2009 | Rekomendasi kenaikan BB | Tabel S-1 dicek penguji (nap.nationalacademies.org). Keterbatasan: IOM menyatakan pedoman tidak dimaksudkan untuk populasi yang jauh lebih pendek/kurus dari perempuan Amerika → script menampilkan catatan ini. |
| ap | WHO WPRO/IASO/IOTF, *The Asia-Pacific Perspective: Redefining Obesity and its Treatment* | 2000 | IMT Asia-Pasifik, lingkar perut ≥ 90/≥ 80 | Standar luas dipakai. |
| kemenkes_imt | Kemenkes RI, Pedoman Gizi Seimbang (Permenkes 41/2014) | 2014 | Batas ambang IMT Indonesia (< 17 / 17–18,4 / 18,5–25 / 25,1–27 / > 27) | Dikonfirmasi lewat materi turunan Kemenkes/RSUD; PERLU REVIEW terhadap naskah asli. |
| mmse | Folstein dkk. 1975; Tombaugh & McIntyre 1992 | 1975/1992 | Ambang 24 & rentang 24–30/18–23/0–17 | Standar literatur. |
| moca | Nasreddine dkk. 2005; Husein dkk. 2010 (MoCA-Ina, Neurona 27(4)) | 2005/2010 | Ambang ≥ 26, +1 bila pendidikan ≤ 12 th | Dikonfirmasi: studi MoCA-Ina 2010 **tidak** menetapkan titik potong Indonesia (hanya melaporkan sebaran dengan 26 dan 23) → alat memakai 26 dan menyebutkannya. |
| amt | Hodkinson 1972; formulir AMT Permenkes 67/2015 | 1972/2015 | Rentang 8–10 / 4–7 / 0–3 | Permenkes 67/2015 memuat AMT (dikonfirmasi); pembagian rentang **belum** dibaca dari naskah asli (BPK 403) → PERLU REVIEW. |

Primer yang belum terbaca langsung (hanya sekunder): Permenkes 67/2015 (AMT), Permenkes 41/2014
(IMT Kemenkes), WPRO 2000 (PDF hasil pindai). Status: **PERLU REVIEW**.

URL yang dipakai saat riset (2026-09-29):
- Buku KIA cetakan 2025 (primer, dibaca penguji):
  https://ayosehat.kemkes.go.id/buku-kia-kesehatan-ibu-dan-anak
- NICE NG133 rekomendasi: https://www.nice.org.uk/guidance/ng133/chapter/Recommendations
- Buku KIA 2023 (dikutip sekunder, versi lama): https://wpcpublisher.com/jurnal/index.php/HRJI/article/view/1012 ;
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
| MMSE | PAR Inc. (sejak 2001) — reproduksi/terjemahan/modifikasi butir wajib izin tertulis | **Hanya menafsirkan skor total yang dimasukkan nakes.** Tidak memuat/mereproduksi formulir, butir, instruksi. Pemakaian formulir = lisensi milik pengguna sendiri dari PAR. |
| MoCA / MoCA-Ina | Z. Nasreddine / MoCA Cognition — sejak 1 Sep 2019 pemeriksa wajib pelatihan & sertifikasi; entitas komersial wajib izin tertulis & perjanjian lisensi; halaman izin melarang pengembangan materi elektronik terkait MoCA tanpa lisensi | **Hanya menafsirkan skor total yang dimasukkan nakes.** Tidak memuat/mereproduksi formulir, butir, instruksi, penskoran per butir. Pemakaian formulir = lisensi/izin + pelatihan-sertifikasi milik pengguna sendiri. **PERLU REVIEW legal (T4):** apakah menyebut & menafsirkan skor MoCA dalam produk berbayar perlu izin tertulis MoCA Cognition. Opsi untuk pemilik: (a) minta izin tertulis (draf pesan disiapkan pemilik); (b) ubah fitur menjadi penafsir generik "skor total 0–30 dengan ambang yang dimasukkan pemeriksa" tanpa nama MoCA di nama fitur & materi jualan. Sampai diputuskan, jangan rilis/jual. |
| AMT | Hodkinson 1972, dipakai bebas & dimuat di Permenkes 67/2015 | Aman secara lisensi, tetapi v1 tetap hanya menerima skor total (klinik memakai formulir resmi). |

## Yang sengaja tidak disertakan di v1
- **Skor risiko kardiovaskular tanpa lab.** Kandidat terbaik (WHO CVD risk chart non-lab 2019,
  wilayah Asia Tenggara) berupa tabel/persamaan terkalibrasi per wilayah yang harus diambil
  persis dari sumber resmi; Framingham BMI-based (2008) tidak terkalibrasi untuk Indonesia.
  Menghitung dari ingatan berisiko salah → **dilewati**; arahkan ke WHO HEARTS risk chart resmi.
- Dosis obat apa pun (keputusan pemilik).
- Kalkulator untuk anak (z-score WHO) — butuh tabel LMS panjang; kandidat v2.

## Status verifikasi — daftar PERLU REVIEW (v1.0.1)
Peninjau: dokter SpOG/dokter umum + bidan (preeklampsia & kehamilan); dokter/neurolog/psikolog
klinis (kognitif); ahli gizi/dokter (IMT). Status v1.0.1 di kolom kanan.

| # | Butir yang wajib ditinjau | Status v1.0.1 |
|---|---|---|
| 1 | Ambang MAP ≥ 90 vs > 90 | Disamakan dengan Buku KIA cetakan 2025 (≥ 90); cocokkan dengan cetakan fasilitas |
| 2 | Proteinuria sedang vs tinggi | Disamakan dengan Buku KIA cetakan 2025 (sedang) |
| 3 | Daftar & kolom semua faktor KIA; "riwayat preeklampsia" vs "hipertensi pada kehamilan sebelumnya"; cakupan "Diabetes dalam kehamilan" (apakah termasuk DM pregestasional) | Kode dipisah (`riwayat-preeklampsia` / `riwayat-hipertensi-kehamilan`; `diabetes-pregestasional` / `diabetes-gestasional`); cakupan KIA untuk DM pregestasional = asumsi kurator |
| 4 | Kalimat tindak lanjut risiko (RS, rujukan terencana) | Mengikuti bunyi Buku KIA + "sesuai protokol fasilitas & keputusan dokter" |
| 5 | Perilaku TD ≥ 140/90 dan ≥ 160/110; daftar gejala bahaya | Lapisan tanda bahaya di script (NICE NG133, ACOG PB 222, Buku KIA) — perlu dicocokkan dengan PNPK/protokol fasilitas |
| 6 | Pemetaan bahasa sehari-hari → kode faktor/gejala | `references/preeklampsia.md` |
| 7 | Koreksi siklus Naegele (siklus − 28) & batas 21–45 hari | Tetap; di luar batas → pakai USG bila ada |
| 8 | Ambang penanggalan ulang ACOG vs praktik lokal (Buku KIA: selisih ≥ 3 minggu USG TM I/HPHT vs USG TM III) | Belum diubah; sebutkan bila fasilitas memakai aturan KIA |
| 9 | Rumus "perkiraan rentang kenaikan BB saat ini" (turunan) & relevansi IOM untuk ibu Indonesia | Catatan keterbatasan IOM ditambahkan |
| 10 | IMT Kemenkes vs Asia-Pasifik; LP ≥ 90/80 vs > 90/80 | Catatan kapan memakai masing-masing ditambahkan |
| 11 | Rentang AMT vs naskah Permenkes 67/2015 | Belum terbaca primer |
| 12 | MMSE tanpa koreksi pendidikan; batas MoCA 26 untuk MoCA-Ina | Catatan pendidikan & delirium/depresi ditambahkan |
| 13 | Semua kalimat baku untuk pengguna awam (ibu hamil bergejala) | Diubah: bergejala → periksa **hari ini** / IGD / 119 |
| L | **Legal:** lisensi MoCA (dan MMSE) untuk produk berbayar | Alat hanya menafsirkan skor total; keputusan pemilik diperlukan (lihat tabel lisensi) |
