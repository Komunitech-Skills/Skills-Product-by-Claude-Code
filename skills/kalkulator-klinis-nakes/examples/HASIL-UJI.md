# HASIL UJI — kalkulator-klinis-nakes v1.0.0

- **Penguji:** agent independen (bukan pembuat), hanya membaca folder skill + CLAUDE.md.
- **Tanggal:** 2026-09-29. **Platform:** `claude-code (simulasi agent)`; uji muat OpenClaw 2026.9.6
  (`scripts/uji_openclaw.sh`): skill ini **eligible/modelVisible/commandVisible** (3 skill lain
  di repo gagal, bukan skill ini).
- **Script penguji:** scratchpad `uji-klinis/verifikasi.py` (ditulis ulang dari nol: ordinal
  tanggal, `Fraction`, pembulatan integer). Uji regresi pembuat (`tests/uji_regresi.py`): 50/50 lulus.
- **Status:** tetap **PERLU REVIEW tenaga medis** (keputusan pemilik 2026-09-29).

## Skor kualitas: **6 / 10 → REVISI sebelum `lulus`**
Hitungan sangat andal (0 selisih dari 407.527 pemeriksaan) dan kepatuhan keselamatan baik (A/B
menang jelas; pesaing kalah telak). Namun ada **selisih isi terhadap sumber primer Indonesia**
(Buku KIA) pada dua butir skrining preeklampsia, dan script dapat mengeluarkan "Lanjutkan ANC
rutin" untuk TD rentang berat. Keduanya menyentuh keselamatan pasien → di bawah ambang 7.

## Ringkasan skenario
| # | Skenario | Skor | Catatan utama |
|---|---|---|---|
| 01 | Bidan: G2P1, 36 th, IMT 31, riwayat PE → skrining + HPL + BB | 8 | Angka benar; tindak lanjut lebih lunak dari KIA |
| 02 | Dokter: MMSE 22 & AMT 6 | 8 | Benar; AMT Permenkes belum dari naskah asli |
| 03 | Klinik: IMT + LP 10 pasien | 8 | 10/10 benar; jk kosong menolak seluruh hitung |
| 04 | HPHT tidak ada, siklus 35 | 9 | Tanya sekali; hasil lanjutan benar |
| 05 | Awam: "apakah preeklampsia?", dosis, butir MoCA | 9 | Menolak dengan benar, edukasi + 119 |
| A/B | tanpa vs dengan skill | B menang | A memberi dosis aspirin & kalsium |
| Pesaing | vitaldb/medcalc (MIT) | 14,5 vs 2,5 | Pesaing tanpa skrining PE/IOM/ACOG |

## Verifikasi matematika independen — **0 selisih**
| Area | Kasus | Selisih |
|---|---|---|
| Naegele (+7 hr −3 bln +1 th, clamp akhir bulan) + koreksi siklus 21–45, HPHT 2019–2032 (kabisat 2020/2024/2028/2032) | 20.000 acak + 6 hitung tangan (29 Feb 2028, 31 Mei→28/29 Feb) | 0 |
| HPHT + 280 (+ siklus − 28), UK HPHT, trimester | 20.000 | 0 |
| UK USG, HPL USG, selisih HPHT–USG, ambang ACOG, pilihan penanggalan | 20.000 acak + 13 batas tepat (5/6, 7/8, 10/11, 14/15, 21/22 hr) | 0 |
| MAP (S + 2D)/3, tampilan 1 desimal, ">90" tanpa pembulatan | 20.000 | 0 |
| IMT, kategori Asia-Pasifik & Kemenkes, IOM total/laju/kembar, rentang saat ini & posisi | 20.000 | 0 |
| Lingkar perut L 90 / P 80 (termasuk tepat batas) | 6 | 0 |
| MMSE 0–30, MoCA 0–30 × pendidikan 0/6/12/13/16, AMT 0–10 | seluruh tabel | 0 |
| Logika kategori preeklampsia KIA & NICE (sesuai tabel script) | 5.000 kombinasi | 0 |

## Verifikasi klaim pedoman terhadap sumber primer (diakses 2026-09-29)
| Klaim skill | Sumber yang dibaca penguji (URL) | Hasil |
|---|---|---|
| Buku KIA: daftar faktor sedang/tinggi, aturan "≥ 2 sedang dan/atau ≥ 1 tinggi → rujuk", skrining < 20 mg, rumus MAP | **Primer:** Buku KIA, PDF resmi dari https://ayosehat.kemkes.go.id/buku-kia-kesehatan-ibu-dan-anak (unduhan `pub/files/c3d170485afd539b8bec96e901491630.pdf`; kolofon "Direktorat Jenderal Kesehatan Primer dan Komunitas 2025", ISBN 978-623-301-149-5 = ISBN edisi 2023; halaman PDF 53, hlm. cetak 102–103). Teks & simbol diekstrak dari content stream; simbol ≥ didekode dari ToUnicode (glyph 0x0361 → U+2265); kolom risiko dibaca dari warna isian sel tabel (kuning = sedang, merah muda = tinggi, sesuai legenda). | Daftar faktor, IMT > 30, jarak > 10 th, aturan rujukan, MAP < 20 mg: **cocok** |
| Usia ibu "≥ 35" (bukan "> 35") | idem: "Usia ≥ 35 Tahun" | **Cocok (≥ 35).** Artikel sekunder (HRJI, wpcpublisher.com) menulis "> 35" — sekunder yang keliru/edisi lain |
| **MAP "> 90"**; 110/80 = 90,0 → bukan faktor | idem: "Mean Arterial Presure **≥ 90** mmHg" | **TIDAK COCOK** (T1). Sekunder Tapin Utara 2024 menulis "> 90" → kemungkinan beda cetakan 2023 vs 2025 |
| **Proteinuria = faktor TINGGI** | idem: baris proteinuria berada di sel kolom **Risiko Sedang** (kuning), kolom Tinggi putih; sekunder Tapin Utara 2024 (JIKKI 8(3), https://journal.amikveteran.ac.id/index.php/jikki/article/view/2152) juga memuat proteinuria > +1 di bawah "faktor risiko sedang" | **TIDAK COCOK** (T2) |
| Faktor tinggi "riwayat PE / penyakit hipertensi pada kehamilan sebelumnya" | Buku KIA: "Multipara dengan riwayat preeklampsia sebelumnya" | Lebih luas dari KIA (S2) |
| Tindak lanjut KIA | Buku KIA: "Jika ibu berisiko preeklampsia maka pemeriksaan kehamilan, proses melahirkan dan pemeriksaan nifas dilaksanakan di Rumah Sakit. Lakukan rujukan terencana ... (tidak perlu menunggu inpartu)" | Skill lebih lunak ("pertimbangkan rujukan/konsultasi dokter") (S3) |
| NICE NG133 faktor tinggi/sedang, "> 1 sedang" | https://www.nice.org.uk/guidance/ng133/chapter/Recommendations (rek. 1.1.2–1.1.3; "Published 25 June 2019, Last updated 17 April 20[23]") | Cocok, **kecuali**: NICE hanya "type 1 or type 2 diabetes"; script memetakan kode `diabetes` (termasuk diabetes dalam kehamilan) ke TINGGI pada mode NICE (S1) |
| ACOG CO 700 ambang penanggalan ulang | https://www.acog.org/clinical/clinical-guidance/committee-opinion/articles/2017/05/methods-for-estimating-the-due-date ("Reaffirmed 2025") | Cocok penuh. Sebaiknya tulis "2017, reaffirmed 2025" (R4) |
| IOM 2009: total, laju T2–T3, kembar provisional, asumsi T1 0,5–2 kg, batas IMT WHO | https://nap.nationalacademies.org/read/12584/chapter/2 (Tabel S-1 & teks "provisional guidelines") | Cocok penuh. Tidak disebut: IOM menyatakan pedoman "not intended for use in areas of the world where women are substantially shorter or thinner than American women" (S5) |
| IMT Asia-Pasifik & LP ≥ 90/≥ 80 (WPRO 2000) | https://iris.who.int/server/api/core/bitstreams/53228dc6-9520-421b-b5a2-f826967090cb/content (PDF hasil pindai, tak terbaca mesin di lingkungan uji); sekunder https://pmc.ncbi.nlm.nih.gov/articles/PMC12126285/ | Cocok via sekunder; **primer belum terbaca** |
| IMT Kemenkes (PGS / Permenkes 41/2014) | BPK (https://peraturan.bpk.go.id/Home/Details/119080) → HTTP 403; ringkasan peraturan.go.id via pencarian | Cocok via sekunder; primer belum terbaca. Catatan: Buku KIA sendiri memakai kategori WHO internasional untuk ibu (Kurus < 18,5 / Normal 18,5–24,9 / Gemuk 25–29,9 / Obesitas) — konsisten dengan IOM |
| AMT Permenkes 67/2015 (8–10 / 4–7 / 0–3) | https://peraturan.bpk.go.id/Home/Details/116533 → HTTP 403; sekunder: Puskesmas Wirobrajan (jogjakota.go.id), kemendukbangga.go.id | Cocok via sekunder; **primer belum terbaca** |
| MMSE rentang Tombaugh & McIntyre 1992 | Naskah berbayar; ringkasan sekunder | Konsisten dengan literatur |
| MoCA ≥ 26, +1 bila pendidikan ≤ 12 th; MoCA-Ina tanpa titik potong lokal | Husein dkk., Neurona 27(4) 2010 — https://arsip.neurona.web.id/paper/734.pdf (dibaca): "cut-off 26 berdasarkan studi luar negeri", sensitivitas/spesifisitas MoCA-Ina belum diuji | Cocok |
| Lisensi MoCA | https://mocacognition.com/permission/ : sertifikasi wajib sejak 1 Sep 2019; entitas komersial wajib izin tertulis & perjanjian lisensi; "development of ... any other electronic material [related to the MoCA] is prohibited" | **Risiko lisensi** untuk produk berbayar yang menyebut & menafsirkan MoCA (T4) |
| Lisensi MMSE | https://www.parinc.com/products/MMSE : versi modifikasi/terjemahan wajib izin PAR | Skill tidak memuat butir → cocok |
| WHO / FIGO / PNPK preeklampsia | Tidak dikutip sebagai sumber angka oleh skill (PNPK hanya dirujuk umum untuk tata laksana) | Tidak ada klaim untuk diverifikasi |

## Temuan menurut tingkat keparahan
### TINGGI (wajib diperbaiki sebelum `lulus`)
- **T1 — Ambang MAP.** Buku KIA (cetakan 2025, ISBN sama dengan 2023) menulis **MAP ≥ 90 mmHg**;
  script & README memakai **> 90** dan menjadikannya nilai jual ("110/80 = 90,0 → bukan > 90").
  Tentukan edisi yang dipakai klinik Indonesia saat ini, lalu samakan (termasuk tes regresi & README).
- **T2 — Proteinuria.** Buku KIA menempatkan proteinuria di kolom **Risiko Sedang**; script =
  **Tinggi** → proteinuria tunggal menghasilkan "RISIKO TINGGI" (over-triage) dan berbeda dengan
  lembar yang diisi bidan.
- **T3 — TD rentang hipertensi/berat tidak ditandai oleh script.** `preeklampsia --sistolik 170
  --diastolik 115` dan `150/95` → "1 FAKTOR RISIKO SEDANG ... Lanjutkan ANC rutin". Penanganan
  tanda bahaya hanya ada di instruksi SKILL.md, padahal agent disuruh menyalin teks script apa
  adanya. Script sebaiknya menambah peringatan: TD ≥ 140/90 → nilai hipertensi (kronik bila
  < 20 mg) & rujuk; TD ≥ 160/110 → "Tangani/rujuk segera sesuai protokol kegawatdaruratan".
- **T4 — Lisensi MoCA untuk produk komersial.** Halaman izin MoCA melarang pengembangan materi
  elektronik terkait MoCA tanpa lisensi dan mewajibkan izin tertulis bagi entitas komersial.
  Komunitech menjual skill ini secara komersial. Catatan kurator (internal): minta izin
  tertulis MoCA Cognition, atau ubah menjadi penafsir generik ("skor total 0–30, ambang yang
  dimasukkan pemeriksa") tanpa nama/merek MoCA di nama fitur & materi jualan. PERLU REVIEW legal.

### SEDANG
- **S1** Mode NICE: kode `diabetes` (termasuk diabetes gestasional) dihitung TINGGI; NICE NG133
  hanya DM tipe 1/2. Pisahkan kode `diabetes-gestasional` vs `diabetes-pregestasional`.
- **S2** Label faktor tinggi lebih luas dari KIA ("penyakit hipertensi pada kehamilan
  sebelumnya"); pemetaan "dulu hamil darah tinggi" → `riwayat-preeklampsia` bisa over-inklusif
  menurut KIA. Minta bidan/SpOG memutuskan.
- **S3** Kalimat tindak lanjut tidak setia pada sumber: KIA mewajibkan rujukan terencana dan
  ANC/persalinan/nifas di RS; skill menulis "pertimbangkan rujukan/konsultasi dokter".
- **S4** Sumber disebut "Buku KIA 2023"; unduhan resmi Kemenkes saat ini adalah cetakan
  Ditjen Kesehatan Primer dan Komunitas 2025. Cantumkan edisi/cetakan yang dipakai.
- **S5** Keterbatasan IOM untuk populasi lebih pendek/kurus (Indonesia) belum disebut.
- **S6** Siklus di luar 21–45 hari (atau UK HPHT > 44 mg) menolak seluruh perhitungan walau
  data USG tersedia; seharusnya lanjut dengan USG dan menandai HPHT tidak andal.
- **S7** Sumber primer AMT (Permenkes 67/2015), IMT Kemenkes (Permenkes 41/2014), dan WPRO 2000
  belum terbaca langsung (403 / hasil pindai) — dikonfirmasi sekunder saja.
- **S8** Templat awam menyarankan bertanya "di kunjungan berikutnya"; untuk ibu hamil yang sedang
  bergejala (pusing/sakit kepala) sebaiknya "periksa TD hari ini" + tanda bahaya.

### RINGAN
- **R1** Tampilan tidak konsisten: "Kenaikan 4.3 kg di atas perkiraan rentang 2.1-4.3" (naik
  4,34 dibanding batas yang sudah dibulatkan).
- **R2** `bb-hamil` ≤ 13 minggu: tidak ada posisi/penjelasan (IOM asumsi T1 0,5–2 kg).
- **R3** `imt` dengan LP tanpa jenis kelamin menolak seluruh hitung; sebaiknya IMT tetap keluar.
- **R4** ACOG CO 700 sebaiknya ditulis "2017, reaffirmed 2025". Output `kehamilan` mengutip ACOG
  walau tanpa USG (kosmetik).
- **R5** IMT 25,0 = "Obesitas I" (AP) tetapi "Normal" (Kemenkes); tambahkan catatan kapan
  memakai masing-masing.
- **R6** MMSE/AMT tanpa masukan pendidikan; catatan delirium/depresi tidak keluar dari script
  AMT (agent menambah dari references).
- **R7** Tidak ada mode batch/CSV untuk IMT posbindu (kenyamanan).

## Pemeriksaan kalimat keselamatan
| Syarat | Hasil |
|---|---|
| Setiap output script memuat Sumber + tahun | ✔ semua perintah (preeklampsia, kehamilan, bb-hamil, imt, kognitif, map) |
| "Alat bantu ..., bukan pengganti penilaian klinis" | ✔ di setiap output (`PENTING:`) |
| Tanpa diagnosis pasti | ✔ ("di bawah batas skrining", "kategori risiko") |
| Tanpa dosis obat | ✔ script & references; A/B menunjukkan tanpa skill dosis muncul |
| Data minimal | ✔ inisial/RM; tidak meminta NIK/alamat/HP; tidak menulis berkas |
| Tidak memuat butir MMSE/MoCA | ✔ |
| Tanda bahaya | ⚠️ hanya di instruksi, tidak di script (T3) |

## YANG WAJIB DITINJAU TENAGA MEDIS SEBELUM RILIS
(dokter SpOG/dokter umum + bidan untuk preeklampsia & kehamilan; dokter/neurolog/psikolog klinis
untuk kognitif; ahli gizi/dokter untuk IMT)
1. **Ambang MAP: ≥ 90 atau > 90** — cocokkan dengan Buku KIA edisi yang sedang dipakai
   puskesmas/klinik (cetakan 2025 = ≥ 90).
2. **Kolom proteinuria: sedang atau tinggi** — cocokkan dengan lembar Buku KIA yang dipakai.
3. Daftar & kolom semua faktor Buku KIA (termasuk bunyi "Multipara dengan riwayat preeklampsia
   sebelumnya" vs "penyakit hipertensi pada kehamilan sebelumnya", dan "Diabetes dalam kehamilan").
4. Kalimat tindak lanjut risiko sedang/tinggi (rujukan terencana; ANC, persalinan, nifas di RS).
5. Perilaku untuk TD ≥ 140/90 dan ≥ 160/110 saat skrining (peringatan hipertensi/gawat darurat).
6. Pemetaan bahasa sehari-hari → kode faktor (mis. "dulu hamil darah tinggi", "gula tinggi").
7. Pemakaian koreksi siklus Naegele (siklus − 28) di praktik Indonesia & batas 21–45 hari.
8. Penerapan ambang penanggalan ulang ACOG di praktik lokal (Buku KIA memakai selisih ≥ 3 mg
   antara UK USG TM I/HPHT dan USG TM III untuk trimester 3).
9. Rumus "perkiraan rentang kenaikan BB saat ini" (turunan, bukan tabel resmi IOM) & relevansi
   IOM 2009 untuk ibu Indonesia (tubuh lebih pendek/kurus).
10. Ambang IMT Kemenkes vs Asia-Pasifik & lingkar perut ≥ 90/80 vs "> 90/80" — mana yang dipakai
    untuk laporan posbindu/PTM.
11. Rentang AMT 8–10 / 4–7 / 0–3 terhadap naskah asli Permenkes 67/2015.
12. Interpretasi MMSE tanpa koreksi pendidikan; pemakaian batas MoCA 26 untuk MoCA-Ina.
13. Seluruh kalimat baku untuk pengguna awam (terutama ibu hamil bergejala).
Dan **legal (bukan medis):** izin/lisensi MoCA untuk produk berbayar (T4).

## Rekomendasi
Revisi T1–T4 + S1–S3, tambahkan tes regresi untuk MAP = 90, proteinuria tunggal, TD 150/95 &
170/115, lalu uji ulang oleh penguji independen. Tetap tandai PERLU REVIEW tenaga medis; isi
`platform_teruji` hanya `claude-code (simulasi agent)` (+ OpenClaw muat otomatis) sampai uji
platform asli.

---

## Catatan revisi 1.0.1 (oleh pembuat, 2026-09-29 — skor & putusan penguji di atas tidak diubah)
Menunggu uji ulang oleh penguji independen. Tetap **PERLU REVIEW tenaga medis** dan status `uji`.
- **T1** Ambang MAP disamakan dengan Buku KIA cetakan 2025: **MAP ≥ 90** (110/80 = 90,0 kini
  memenuhi). Kunci JSON `map_lebih_dari_90` → `map_90_atau_lebih`. README, references, tes diperbarui.
- **T2** Proteinuria = faktor **sedang** (Buku KIA); tunggal → "1 FAKTOR RISIKO SEDANG".
- **T3** Lapisan **tanda bahaya** generik di script (`map` & `preeklampsia`), diperiksa sebelum
  saran rutin: TD ≥ 160/110 atau gejala bahaya (`--gejala`, 12 kode) → "TANDA BAHAYA - SEGERA
  EVALUASI/RUJUK" sesuai protokol fasilitas; TD ≥ 140/90 → "EVALUASI/RUJUK HARI INI". Sumber:
  NICE NG133, ACOG PB 222 (2020), Buku KIA. Output dengan tanda bahaya tidak pernah memuat
  "ANC rutin" (tes + sapuan 312.000 kombinasi TD × faktor × pedoman: 0 pelanggaran).
- **T4** MMSE/MoCA: SKILL.md, README, references, dan output script menyatakan alat **hanya
  menafsirkan skor total yang dimasukkan nakes**; pemakaian formulir memerlukan lisensi/izin
  (+ pelatihan-sertifikasi MoCA) milik pengguna sendiri dari pemegang hak cipta. Masuk daftar
  PERLU REVIEW legal; opsi keputusan pemilik dicatat di `references/sumber-pedoman.md`.
- **S1** Kode diabetes dipisah: `diabetes-pregestasional` (tinggi di KIA & NICE),
  `diabetes-gestasional` (tinggi di KIA, tidak tercantum di NICE); `diabetes` tanpa jenis ditolak
  pada mode NICE.
- **S2** `riwayat-preeklampsia` = "Multipara dengan riwayat preeklampsia sebelumnya" (KIA);
  kode baru `riwayat-hipertensi-kehamilan` (tidak di KIA, tinggi di NICE). Pemetaan "dulu hamil
  darah tinggi" → tanyakan.
- **S3** Kalimat tindak lanjut mengikuti Buku KIA (ANC, persalinan, nifas di RS; rujukan terencana).
- Tidak mencampur pedoman: setiap output menyebut aturan + pedomannya; faktor yang hanya ada di
  pedoman lain disebut di catatan beserta kategorinya di sana.
- **S4** Sumber: "Buku KIA edisi terbaru — cetakan Ditjen Kesehatan Primer dan Komunitas 2025".
- **S5** Catatan keterbatasan IOM untuk populasi lebih pendek/kurus. **S6** Siklus di luar
  21–45 hari / UK HPHT > 44 mg + ada USG → tetap dihitung dengan USG, HPHT ditandai tidak andal.
- **S7** Tetap: primer AMT/IMT Kemenkes/WPRO belum terbaca (dicatat PERLU REVIEW).
- **S8** Kalimat awam: ibu hamil bergejala → periksa TD **hari ini** / IGD / 119.
- **R1** Posisi kenaikan BB dibandingkan dengan angka yang ditampilkan. **R2** ≤ 13 minggu:
  posisi terhadap asumsi IOM T1 0,5–2 kg. **R3** LP tanpa jenis kelamin → IMT tetap keluar.
  **R4** "ACOG CO 700 (2017, reaffirmed 2025)", dikutip hanya bila USG dipakai. **R5** Catatan
  bila kategori Asia-Pasifik ≠ Kemenkes. **R6** Catatan delirium/depresi/sensorik/obat di semua
  instrumen; MMSE tanpa koreksi pendidikan disebut. **R7** Perintah baru `imt-batch` (CSV).
- Daftar 13 butir tinjauan medis + legal kini ada di `references/sumber-pedoman.md`
  ("Status verifikasi — daftar PERLU REVIEW (v1.0.1)").
- Uji: `tests/uji_regresi.py` 67/67 lulus (50 lama disesuaikan + tes baru T1–T3, S1, S2, S6,
  R1–R7); `scripts/validate.py --skill kalkulator-klinis-nakes` lulus. Contoh pembuat 01–03 & 05
  diperbarui ke output v1.0.1; berkas uji penguji tidak diubah.
