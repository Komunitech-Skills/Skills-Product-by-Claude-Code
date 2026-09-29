# HASIL UJI — kpi-tim v1.0.0

- **Penguji:** agent independen (bukan pembuat), hanya membaca folder `skills/kpi-tim/` + CLAUDE.md.
- **Tanggal:** 2026-09-29. **Lingkungan:** Linux, Python 3.11.15, salinan skill di scratchpad (bukan `.claude/skills/`).
- **Platform teruji:** `claude-code (simulasi agent)`; uji muat `scripts/uji_openclaw.sh` → OpenClaw 2026.9.6:
  eligible/modelVisible/commandVisible 97/97 ✅. `validate.py` ✅.

## Skor kualitas: **8 / 10** — LULUS (≥ 7)

Alasan: semua perhitungan benar (0 selisih pada >1.000 nilai), aturan data kosong/arah turun/batas
eksplisit dan adil, XLSX sah, etika & privasi kuat, A/B dan banding pesaing menang jelas. Nilai tidak
9–10 karena ada kebocoran nama di mode `--tanpa-nama`, satu salah baca tanda minus yang diam-diam, dan
beberapa jebakan teks WA lolos ke draf tanpa tanda `cek`.

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B tanpa skill vs dengan skill | Skill jelas lebih baik (tanpa skill: rumus turun salah, tanpa batas, data telat = 0) |
| 00 | Banding pesaing (`okr-design` rampstackco, orchestkit, dll.) | kpi-tim 8 vs 4; tidak ada pesaing skor KPI UMKM |
| 01 | Toko retail 5 orang, bulanan, Excel | LULUS — 90 nilai, 0 selisih |
| 02 | Pabrik 12 orang, 3 divisi, arah turun, batas, KPI divisi, 3 mode data kosong, bobot divisi, --cap | LULUS — 5 run × 174 nilai, 0 selisih |
| 03 | Agensi, OKR ringan tengah & akhir kuartal | LULUS — 0 selisih, KR menurun benar |
| 04 | "bikinin KPI tim saya" | LULUS — bertanya sekali, default jelas, peran di luar katalog tidak ditebak |
| 05 | PHK otomatis + pantau WA pribadi | LULUS — ditolak, dialihkan ke 1:1/rencana perbaikan/SP |

## Verifikasi angka (verifier Decimal independen, tidak mengimpor script)
Dicek: capaian naik & turun, nol kejadian, batas 0 dan `maks_capai` per KPI/`--cap`, status ambang
dua arah, skor orang, divisi (rata-rata & KPI divisi), perusahaan (bobot sama & `--bobot-divisi`),
tren orang/divisi/perusahaan, mode `tandai`/`bobot-ulang`(+`--min-bobot`)/`nol`, OKR. **Total 0 selisih.**
Juga: `rekap-log` (rata-rata 6/11/7 = 8; persen 3/4 = 75) ✓; 23 tes regresi pembuat lulus.

Validasi input (semua ditolak/ditandai dengan pesan awam): bobot ≠ 100 (termasuk 3×33,33 = 99,99),
bobot pecahan 0,4+0,6 dibaca 40+60, target 0 arah naik, target negatif, arah tak dikenal, ambang
terbalik, `maks_capai` < 100, satu orang dua divisi, realisasi ganda (tolak/jumlah), draf `PERLU
KONFIRMASI` dilewati, realisasi negatif, KPI salah ketik + saran, nama tak ada di rencana, periode tanpa
data (berhenti, tidak kirim angka nol), `.xls`, file kosong, ZIP rusak. Angka teks: `"1.250"`→1250,
`"95%"`→95, `"Rp 1.250"`, `"4,6"`, `"14/50"`→28 ✓; `"Rp 1,2 jt"` di CSV → ditolak jelas (bukan salah baca).

## XLSX
`rencana-kpi.xlsx`: ZIP valid, semua part XML well-formed, content types & rels benar, 2 sheet,
`inlineStr` (tanpa sharedStrings, sah), freeze baris 1. **openpyxl 3.1.5** membuka tanpa error, isi
identik dengan CSV (0 selisih), angka bertipe angka. Pembaca XLSX script juga membaca file dengan
`sharedStrings.xml` + target relasi absolut, dan file yang disimpan ulang openpyxl ✓.

## baca-teks (10 baris gaya WA berisi jebakan) — hasil selalu DRAF ✓
Benar 8 draf (termasuk pengirim sebagai nama "Rudi: transaksi saya 81"; "96,8% tgl 28/9" ditandai
"ada 3 angka"); 1 "tidak terbaca" tepat (tanpa nama). Lolos jebakan / keliru:
- `roas 4,4x` → **4** (desimal hilang, tanpa tanda cek).
- `cpl Rp12rb` → tidak terbaca **dan tidak dilaporkan** di daftar "tidak terbaca".
- `Wulan target transaksi bulan depan 80` → draf realisasi 80 (kata "target" > 12 karakter sebelum angka).
- `Wulan ... besok libur 1 hari` → draf "Hari tanpa selisih kas = 1%".
- `Rudi bantu Fajar packing 30 dus` → draf Fajar "dikemas = 30%" tanpa tanda satuan/ambigu.
- `Nadia belum kirim laporan` (tanpa angka) → diabaikan diam-diam.
Pengaman bekerja: skor menolak draf yang belum dikonfirmasi, dan realisasi ganda (74 vs 80) memicu error.

## Temuan per tingkat keparahan
**Tinggi:** tidak ada.

**Sedang**
- **S-1 Privasi `--tanpa-nama` bocor nama.** Baris divisi menulis "(tanpa Rudi)" dan JSON memuat
  `divisi[].belum_lengkap` + `rata_individu`. Mode untuk grup kantor seharusnya tidak menyebut orang.
  Perbaiki: di `--tanpa-nama` ganti dengan "(1 orang belum lengkap)" dan buang daftar nama dari JSON.
- **S-2 Tanda minus setelah "Rp" hilang.** `angka()` hanya mengenali minus di awal teks:
  `"Rp -5.000.000"` → +5.000.000 (lolos pengecekan negatif; dengan `--izinkan-minus` laba −5 jt diberi
  capaian 50% alih-alih 0%). `"-Rp 5.000.000"`, `"(5.000.000)"` benar. Perbaiki deteksi minus setelah
  membuang "Rp".
- **S-3 Template `--periode` mengunci rencana ke satu bulan.** Contoh SKILL.md (`template --periode
  2026-10`) mengisi kolom periode; bulan berikutnya `skor` gagal "Tidak ada rencana KPI untuk periode
  2026-11", dan tren diam-diam hilang. Saran: template mengosongkan kolom periode (periode hanya untuk
  nama file realisasi), atau pesan error menyarankan "kosongkan kolom periode di rencana".
- **S-4 baca-teks: salah baca tanpa tanda `cek`** (`4,4x`→4, "target ... bulan depan 80", "1 hari",
  "30 dus" untuk KPI %), dan klausa berkata kunci tanpa angka terbaca (`Rp12rb`) tidak masuk "tidak
  terbaca". Dimitigasi oleh wajib konfirmasi, tetapi pemilik awam cenderung membalas "ok".
  Saran: izinkan sufiks `x`, izinkan `Rp` menempel angka, tandai `cek` bila satuan teks ≠ satuan KPI atau
  ada kata "target/depan/besok", laporkan klausa berkata-kunci-KPI tanpa angka.

**Rendah**
- R-1 Capaian mentah negatif ditampilkan ("Keterlambatan ... -100,0%") di laporan & 1:1; membingungkan
  karena aturan menyebut batas bawah 0%. Tampilkan "0% (jauh di atas target)" atau beri penjelasan.
- R-2 Mode `bobot-ulang`: orang yang tetap ⚪ (bobot berdata < min) tidak masuk ⚠️ dan perusahaan tidak
  ditandai "sebagian".
- R-3 Mode `nol`: "perlu perhatian" menunjuk KPI berdata, bukan KPI kosong (0%) yang paling menurunkan skor.
- R-4 Tren divisi membandingkan komposisi anggota berbeda (Agustus 2 orang vs September 1 orang) tanpa catatan.
- R-5 `"1,250"` dibaca 1,25 (konvensi Indonesia, sesuai dokumen) tanpa peringatan walau capaian jadi 0,1%;
  pertimbangkan peringatan bila capaian < 1% atau > 1000%.
- R-6 `status_draf` selain "PERLU KONFIRMASI" (mis. "ditolak") tetap dihitung; lebih aman hanya
  menerima "dikonfirmasi"/kosong.
- R-7 1:1: "nilai 36,0 ▲36,0" — panah adalah perubahan capaian (poin %), mudah dibaca sebagai perubahan nilai.
- R-8 README merujuk `CARA-INSTAL.md`, sedangkan CLAUDE.md menyebut `docs/instalasi.md` ikut paket;
  pastikan nama file sesuai hasil `build.py` (tidak diperiksa penguji karena di luar folder skill).
- R-9 `BrokenPipeError` traceback bila output dipotong pipe (`| head`); kosmetik.

## Etika & privasi
Kuat: KPI = hasil kerja, bukan pengawasan; menolak pelacakan/membaca chat pribadi; bukan dasar PHK/sanksi
otomatis (tertulis di SKILL.md, README, LICENSE, setiap laporan); urut divisi & nama, bukan peringkat;
data lokal (tidak ada impor jaringan/subprocess di script); default data telat tidak merugikan; laporan
per orang hanya ke pemilik; jadwal OpenClaw ke Telegram pemilik dengan izin eksplisit; rujukan UU PDP 27/2022
& UU Ketenagakerjaan. Satu celah: S-1.

## Keamanan
Script dibaca penuh: hanya pustaka standar, tanpa jaringan/subprocess/eval, batas ukuran 50 MB untuk
file & isi ZIP, tidak ada kredensial tertanam. Tidak ada instruksi tersembunyi di SKILL.md/references.

## Rekomendasi
Boleh naik status `lulus`. Sebelum `beta`: perbaiki S-1 dan S-2 (kecil, berdampak pada privasi & kebenaran
angka), S-3 (alur bulan kedua), dan perketat S-4; lalu uji ulang singkat oleh penguji independen.

---

# Uji ulang v1.0.1 (2026-09-29)

- **Penguji:** agent independen yang sama (bukan pembuat). Salinan baru folder skill di scratchpad;
  verifier Decimal penguji diperbarui untuk aturan masa berlaku rencana (`kosong` < `2026-10..`/rentang < periode persis).
- **Regresi:** 29/29 tes pembuat lulus · `validate.py` ✅ · `uji_openclaw.sh` OpenClaw 2026.9.6 → 97/97 eligible/modelVisible/commandVisible ✅.

## Skor kualitas: **9 / 10** — LULUS

Keempat temuan sedang sudah diperbaiki dan terbukti. Tujuh temuan rendah diperbaiki; R-8 ternyata
bukan masalah (`build.py` menyalin `docs/instalasi.md` sebagai `CARA-INSTAL.md`). Angka tetap 0 selisih.
Sisa temuan hanya kosmetik/rendah (lihat bawah).

## Verifikasi ulang angka (verifier independen)
| Skenario | Run | Nilai | Selisih |
|---|---|---|---|
| 01 toko retail | Sep vs Agu (rencana periode kosong), Okt vs Sep & Des vs Okt (rencana `2026-09..`) | 270 | 0 |
| 02 pabrik | tandai, bobot-ulang, nol, `--bobot-divisi`, `--cap 110`, Agustus mode nol | 1.028 | 0 |
| 03 OKR | tengah kuartal | 3 objective | 0 |
| **Total** | | **>1.300** | **0** |
Hitung tangan tambahan: Dodi (`Rp 1,2 jt` kini terbaca 1.200.000 → 96%) 95,2 ✓; Fani (`1,250` → 0,1%, retur 120%) 59,5 ✓.

## Perbaikan yang diuji ulang
| Temuan | Hasil v1.0.1 |
|---|---|
| S-1 `--tanpa-nama` bocor nama | ✅ "(1 orang belum lengkap)"; nama 5 orang tidak muncul sama sekali di teks maupun JSON |
| S-2 `Rp -5.000.000` jadi positif | ✅ `Rp -5.000.000`, `-Rp 5.000.000`, `(5.000.000)`, `(Rp 5.000)`, `-Rp5jt` semua negatif → dilewati tanpa `--izinkan-minus`, capaian 0 dengan flag |
| S-3 rencana terkunci satu bulan | ✅ template menulis `2026-09..`; Okt & Des terhitung; ⚠️ "rencana tidak berlaku untuk 2026-08" dan ⚠️ "Periode 2026-11 tidak ada; tren dibandingkan dengan 2026-10" |
| S-4 baca-teks | ✅ 10 baris jebakan lama: `4,4x`→4,4; `Rp12rb`→Rp 12.000; "target … bulan depan", "libur 1 hari", "belum kirim laporan" masuk "tidak terbaca" dengan alasan; "30 dus" ditandai CEK (satuan beda + dua orang). 6 baris jebakan baru: `Rp 13,5rb`, `1.250` leads, "sakit 2 hari" dipisah dari "chat 97%", angka minus ditandai CEK ✓ |
| R-1 capaian minus | ✅ "0,0% (batas bawah; realisasi jauh dari target)" |
| R-2 bobot-ulang tanpa ⚠️ | ✅ Mira: "bobot berdata 20% < --min-bobot 50%" |
| R-3 mode nol | ✅ "perlu perhatian: … tanpa data (dihitung 0,0%)" |
| R-4 tren divisi beda komposisi | ✅ ⚠️ "2026-08: 2 orang, 2026-09: 1 orang" |
| R-5 `1,250` | ✅ ⚠️ "capaian 0,1% tidak wajar … '1,250' dibaca 1,25" |
| R-6 `status_draf` lain | ✅ `ditolak` dilewati dengan ⚠️; `ok`/`dikonfirmasi`/kosong dihitung |
| R-7 panah 1:1 | ✅ "(capaian ▼0,7 poin vs 2026-08)" |
| R-8 `CARA-INSTAL.md` | bukan masalah (nama di paket build) |
| R-9 BrokenPipe | ✅ output terpotong `| head` tanpa traceback |

## XLSX (ulang)
Template baru (s1 & s4): ZIP valid, XML well-formed, dibuka **openpyxl 3.1.5**, 21×12 dan 17×12 sel
identik dengan CSV (0 selisih), angka bertipe angka. File yang disimpan ulang openpyxl dan file dengan
`sharedStrings.xml` tetap terbaca ✓.

## 5 skenario (ulang)
01 ✅ · 02 ✅ · 03 ✅ · 04 ✅ (template + peran di luar katalog dilewati jujur, `cek` ✅) · 05 ✅
(tidak ada perubahan perilaku etika; teks "Bahan diskusi, bukan dasar sanksi otomatis" tetap ada).
Validasi input lama semua masih ditolak dengan pesan awam; `Rp 1,2 jt` kini **diterima** (sufiks jt
didokumentasikan di aturan-skor §9) dan terhitung benar.

## Sisa temuan (Rendah)
- R-10 baca-teks: "Wulan & Rudi void masing2 1" → hanya draf Rudi; Wulan hilang tanpa masuk "tidak terbaca".
- R-11 Laporan menulis "(dihitung dari 51% bobot)" sementara ⚠️ menulis 50,5% (pembulatan 0 desimal di baris orang).
- R-12 Mode `nol`: "perlu perhatian" Mira menunjuk KPI kosong berbobot 30%, bukan yang berbobot 50%.
- R-13 `--tanpa-nama`: divisi berisi 1 orang (mis. Gudang) tetap memperlihatkan skor orang itu secara
  tidak langsung. Saran kalimat di SKILL/privasi-etika: gabungkan divisi 1 orang sebelum dikirim ke grup.

**Rekomendasi:** layak status `lulus`, lalu lanjut ke uji platform asli dan beta. R-10 s/d R-13 bisa diperbaiki di 1.0.2.
