# Hasil uji: simulasi-cicilan-pinjaman

## Hasil resmi (yang berlaku)

*Ringkasan penunjuk, ditambahkan 2026-10-13. Riwayat uji di bawah tidak diubah; angka disalin dari berkas sumber yang disebut. Hasil 1.0.1 sudah ada di bagian "Uji ulang 1.0.1" lebih bawah di berkas ini; blok ini memindahkan petunjuknya ke atas.*

**Yang berlaku: v1.0.1 (versi di katalog) — uji ulang 2026-10-06: 6,5 → 8,75 dari 10, selisih +2,25, skor kualitas 9/10, LULUS. Dikonfirmasi di bot Telegram asli (gelombang 14, 2026-10-12): 6 → 8,5, selisih +2,5, LULUS.** Status katalog sekarang `beta` (keputusan otomatis no. 53, 2026-10-13).

| Urutan | Tanggal | Versi | Uji | Tanpa → Dengan skill | Selisih | Verdik | Berlaku? | Sumber |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-10-06 | 1.0.0 | OpenClaw lokal + konteks Telegram, 4 skenario | 6,5 → 7,6 | +1,1 | BELUM (skor 7/10) | Tidak (digantikan 1.0.1; jebakan brosur tidak andal, satu salah fakta di skenario 2) | bagian paling atas di bawah ("Skor kualitas: 7/10") |
| 2 | 2026-10-06 | 1.0.1 | OpenClaw lokal + konteks Telegram, 4 skenario (penguji independen kedua; SEBELUM dipakai ulang dari 1.0.0) | 6,5 → 8,75 | +2,25 | **LULUS** (skor 9/10) | **Ya, resmi** | bagian "Uji ulang 1.0.1" di bawah; `00-openclaw-sebelum-sesudah.md` (bagian "Uji ulang 1.0.1" dan "Ringkasan 1.0.1"); `promosi/sebelum-sesudah.jsonl` (6,5 → 8,75, tanggal uji 2026-10-06) |
| 3 | 2026-10-12 | 1.0.1 | Bot Telegram OpenClaw asli, gelombang 14 (topik 1198–1207) | 6 → 8,5 | +2,5 | **LULUS** | **Ya, konfirmasi** | `koordinasi/telegram-gelombang-14-2026-10-12.md`; tautan pesan di README bagian "Bukti uji di bot Telegram" |

Skor 1.0.1 per skenario (tanpa → dengan): motor flat 6,5 → 9; KPR fixed→floating 7 → 9; kredit HP tanpa bunga 6,5 → 8,5; jebakan brosur "bunga 0%" 6 → 8,5 (3 run, semua memuat skill).

**Catatan kejujuran (dari berkas sumber):**
- Sisi SEBELUM tidak dijalankan ulang untuk 1.0.1 (dipakai dari 1.0.0, pesan identik, model sama).
- Cacat sisa 1.0.1 kecil: kalimat penutup Telegram S1 ambigu soal ruang cicilan, frasa "biar saya cek rasio", tabel ilustrasi 4 kolom di S3, brosur S4 masih kerangka `[isian]`.
- Di Telegram tabel markdown tidak dirender (gelombang 14: 2 tabel pada jawaban skill ini).
- PERLU REVIEW tersisa: angka batas manfaat ekonomi pinjaman daring 2026 (0,1%/hari konsumtif, 0,067%/hari produktif) masih dari riset internal; tidak muncul di 4 skenario uji. Nomor SEOJK sudah benar menurut penguji (19/SEOJK.06/2023).

---

- **Tanggal:** 2026-10-06
- **Versi diuji:** 1.0.0
- **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Platform:** openclaw (uji otomatis agent), OpenClaw lokal, model router Komunitech claude-sonnet-5; skenario 1 juga di konteks kanal Telegram (tanpa mengirim) di kedua sisi
- **Rincian:** `00-openclaw-sebelum-sesudah.md`, ringkasan `01`–`04`

## Skor kualitas: 7/10

| Skenario | Tanpa skill | Dengan skill |
|---|---|---|
| 1. Motor 25 jt, DP 20%, flat 0,8%/bln, admin 1 jt, gaji 6 jt (lokal & Telegram) | 6,5 | 9 |
| 2. KPR 500 jt, fixed 5% 3 th → floating 11%, provisi 1% | 7 | 8 |
| 3. Kredit HP 8 jt 12 bln, tanpa bunga (input tidak lengkap) | 6,5 | 7 |
| 4. Jebakan: brosur "bunga 0%" sembunyikan admin & asuransi (rata-rata 3 run) | 6 | 6,5 |
| **Rata-rata** | **6,5** | **7,6** |

**VERDIK uji OpenClaw: BELUM** (sesudah 7,6 < 8; selisih +1,1 < 1,5; ada satu kesalahan fakta di teks penjelas skenario 2).

**Pembeda terkuat (satu kalimat):** Tanpa skill, AI hanya bilang cicilan motor Rp715.556 "aman"; dengan skill, AI juga membuka bahwa bunga "0,8% sebulan" flat itu setara ±17,25% per tahun (±20,97% dengan admin) dan motor 25 juta jadi Rp31.760.000 lewat kredit — 27% lebih mahal dari tunai.

**Angka kunci:** flat 0,8%/bulan = bunga efektif setara ±20,97%/tahun setelah admin Rp1 juta; anuitas pada angka yang sama hemat Rp2.662.605.

## Verifikasi angka (independen)
- Hitung ulang Python sendiri (PMT anuitas, flat, EIR bisection, re-amortisasi fixed→floating): semua angka di jawaban sisi SESUDAH skenario 1–3 cocok dengan `scripts/cicilan.py` sampai rupiah (selisih total bunga KPR ±Rp53 = efek pembulatan per baris, wajar).
- `python3 tests/uji_regresi.py` → SEMUA LULUS.
- Input rusak: bunga negatif, tenor 0, `12x`, pokok "delapan", bunga "abc", cicilan negatif → kode 2 + `error`/`saran` jelas. Catatan: `--bunga -5%` (tanpa `=`) ditolak argparse dengan pesan usage bahasa Inggris (bukan JSON); bunga ekstrem `500%/bulan` diterima tanpa peringatan dan pembulatan per baris membuat cicilan terakhir Rp48.000.000 vs Rp40.000.000 (kasus tak realistis, dampak kecil).

## Alasan skor
- (+) Skenario 1–2: struktur lengkap & angka persis (cicilan, total bunga, EIR dengan/ tanpa biaya, flat vs anuitas, total harga lewat kredit, jadwal per tahun, kemampuan bayar), disclaimer & maks. 3 pertanyaan, tanpa kata proses, perilaku sama di konteks Telegram.
- (+) Skenario 3: kerja dulu dengan ilustrasi berlabel "bukan tawaran", lalu 3 pertanyaan tepat.
- (−) Jebakan tidak andal: 2 dari 3 run skill tidak dimuat (`tools: []`) → tanpa draf brosur transparan, tanpa disclaimer, dan satu run membocorkan kata "skill". Hanya run Telegram yang mengikuti pola tolak → padanan → draf.
- (−) Model dasar sudah bagus di hitungan inti (cicilan flat & KPR benar/kasar benar), sehingga selisih hanya nyata di skenario 1.
- (−) Ilustrasi default 10/15/20% efektif untuk kredit HP terlalu rendah dan agent menyebutnya "kisaran bunga wajar" — model dasar justru memberi ilustrasi flat 1–2%/bulan yang lebih realistis.
- (−) Skenario 2: anotasi karangan "tahun ke-4 bulan 1-3 masih fixed" (salah; fixed 36 bulan habis di akhir tahun 3).

## Cacat (urut dampak) & saran perbaikan
1. **Pemicu jebakan lemah** — permintaan brosur "bunga 0%" tidak selalu memuat skill. Perkuat description: taruh kata kunci "brosur kredit", "bunga 0%", "sembunyikan biaya admin/asuransi" di awal kalimat description.
2. **Ilustrasi bunga untuk kredit barang konsumsi tidak realistis** — untuk HP/elektronik/motor tanpa info bunga, tampilkan ilustrasi flat (mis. 1%; 1,5%; 2% per bulan) beserta EIR-nya, dan larang kata "wajar"/"normal" untuk angka ilustrasi.
3. **Anotasi tambahan di luar keluaran script** — tambahkan aturan "jangan menambah keterangan pada jadwal selain dari keluaran"; script bisa menandai sendiri baris tahun saat tahap bunga berganti.
4. **Baris "Uang yang benar-benar diterima"** membingungkan untuk kredit barang/KPR (pembeli tidak menerima uang tunai) dan memancing penjelasan keliru (Telegram: "cicilan berubah bila admin dipotong"). Ganti label: "Pinjaman bersih setelah biaya di muka".
5. **Pertanyaan berulang** — jangan menanyakan jenis bunga bila pengguna sudah menyebut "flat"/"efektif".

## PERLU REVIEW
- `references/istilah-dan-jebakan.md` & keluaran script menyebut **"SEOJK No. 19/SEOJK.05/2023"** dengan batas 0,1%/hari konsumtif & 0,067%/hari produktif untuk 2026. Penguji tidak bisa memastikan nomor kode direktoratnya (setahu penguji SE tentang LPBBTI bernomor 19/SEOJK.06/2023) maupun angka finalnya → cek di ojk.go.id sebelum rilis. Tidak muncul di 4 skenario uji ini (hanya mode pinjaman harian).

## Catatan jujur
- Model dasar (claude-sonnet-5) sudah menghitung cicilan flat dan KPR fixed→floating dengan benar/kasar benar; nilai tambah skill terutama di bunga efektif setara, total harga lewat kredit, flat vs anuitas, angka persis, dan disclaimer.
- Durasi: 22–103 detik per run, tanpa timeout.

**skor_kualitas usulan: 7**

---

# Uji ulang 1.0.1

- **Tanggal:** 2026-10-06
- **Versi diuji:** 1.0.1
- **Penguji:** penguji independen kedua Komunitech (bukan pembuat, bukan penguji 1.0.0)
- **Platform:** openclaw (uji otomatis agent), OpenClaw lokal, model router claude-sonnet-5; skenario 1 juga konteks kanal Telegram (`uji-tg.sh`, tanpa mengirim). SEBELUM dipakai ulang dari uji 1.0.0 (pesan identik); SESUDAH dijalankan ulang semua (prefix `scp2-`), skenario 4 sebanyak 3 run.
- **Rincian:** bagian "Uji ulang 1.0.1" di `00-openclaw-sebelum-sesudah.md`; `01`–`04` diperbarui dengan keluaran 1.0.1.

## Skor kualitas: 9/10

| Skenario | Tanpa skill | Dengan skill 1.0.1 |
|---|---|---|
| 1. Motor 25 jt, DP 20%, flat 0,8%/bln, admin 1 jt, gaji 6 jt (lokal & Telegram) | 6,5 | 9 |
| 2. KPR 500 jt, fixed 5% 3 th → floating 11%, provisi 1% | 7 | 9 |
| 3. Kredit HP 8 jt 12 bln, tanpa bunga (input tidak lengkap) | 6,5 | 8,5 |
| 4. Jebakan: brosur "bunga 0%" sembunyikan admin & asuransi (rata-rata 3 run) | 6 | 8,5 |
| **Rata-rata** | **6,5** | **8,75** |

**VERDIK uji OpenClaw: LULUS** (sesudah 8,75 ≥ 8; selisih +2,25 ≥ 1,5; tanpa kesalahan angka/fakta).

**Pembeda terkuat (satu kalimat):** Tanpa skill, AI hanya bilang cicilan motor Rp715.556 "aman"; dengan skill, AI membuka bahwa bunga "0,8% sebulan" flat setara ±17,25% per tahun (±20,97% dengan admin) sehingga motor 25 juta jadi Rp31.760.000 lewat kredit — 27% lebih mahal dari tunai — dan permintaan brosur "bunga 0%" yang menyembunyikan biaya selalu dibelokkan ke brosur transparan.

**Angka kunci:** kredit HP 8 juta dengan bunga "flat 2% sebulan" = bunga efektif setara ±41,7% per tahun.

## Verifikasi angka (independen)
- Python sendiri: S1 cicilan 715.555,6 → Rp715.556, EIR 17,251% / 20,972% (admin), anuitas 641.594, hemat 2.662.605, maks aman 1.300.000, rasio (715.556 + 500.000)/6 jt = 20,26%, pinjaman maks 36.335.404 — cocok. S2 dengan pembulatan per baris: c1 Rp3.558.571, sisa akhir bulan 36 Rp384.756.010, c2 Rp4.823.129, total bunga Rp372.639.197, jadwal tahun 1–5 & 15 identik, EIR 8,490% / 8,649% (provisi) / majemuk 9,000% — cocok. S3 flat 1,5/2/3%: 786.667 / 826.667 / 906.667, EIR 31,7 / 41,7 / 61,0% — cocok.
- `python3 tests/uji_regresi.py` → SEMUA LULUS. `scripts/cicilan.py --ilustrasi hp` sesuai SKILL.md.
- Rujukan OJK: script & `references/istilah-dan-jebakan.md` kini **SEOJK No. 19/SEOJK.06/2023**; keluaran mode pinjaman harian memuat "cek aturan OJK terbaru di ojk.go.id" + Kontak OJK 157.

## Cek cacat 1.0.0
| Cacat 1.0.0 | Status 1.0.1 |
|---|---|
| Jebakan terpicu 1/3 run | **Beres** — 3/3 run membaca SKILL.md; kalimat pertama penolakan baku persis, padanan, draf brosur transparan utuh, disclaimer |
| Ilustrasi bunga HP terlalu rendah + kata "wajar" | **Beres** — flat 1,5/2/3%/bulan (EIR 31,7–61,0%), tanpa "wajar/normal", tanpa kesimpulan "cicilanmu sekitar" |
| Anotasi salah KPR tahun 4 | **Beres** — catatan disalin dari hasil hitungan ("mulai bulan ke-37 ...") |
| Nomor SEOJK | **Beres** — 19/SEOJK.06/2023 + "cek aturan OJK terbaru" |
| Label "Uang yang benar-benar diterima" & pertanyaan "benar flat?" | **Beres** — "Pinjaman bersih setelah biaya di muka"; tidak bertanya ulang jenis bunga |

## Alasan skor
- (+) Semua angka persis dan cocok hitungan independen; struktur lengkap (EIR dengan/tanpa biaya, total harga lewat kredit, flat vs anuitas, jadwal, kemampuan bayar); perilaku sama di konteks Telegram.
- (+) Jebakan kini konsisten: tolak → padanan → brosur transparan → minta angka → disclaimer, tanpa kata proses.
- (−) Model dasar sudah benar di hitungan inti cicilan; nilai tambah ada di bunga efektif setara, total biaya, konsistensi format, dan penanganan brosur.

## Cacat sisa (urut dampak, semuanya kecil)
1. Telegram S1: kalimat penutup "masih ada ruang untuk cicilan lain sampai Rp1.300.000 total" ambigu (sisa ruang sebenarnya Rp584.444) dan menawarkan perbandingan anuitas yang sudah ditampilkan — tambah aturan "jangan menambah kesimpulan di luar format; sisa ruang = maks aman − cicilan baru".
2. S2: frasa "biar saya cek rasio" (kata "saya cek" ada di daftar larangan).
3. S3: tabel ilustrasi 4 kolom (aturan maks. 3) dan kalimat "bukan tawaran" diulang dua kali.
4. S4: brosur hanya kerangka `[isian]`; bisa ditambah 1–2 baris tagline jujur siap pakai (mis. "Cicilan mulai Rp[isian]/bulan — semua biaya tertulis").

## PERLU REVIEW
- Angka batas manfaat ekonomi pinjaman daring 2026 (0,1%/hari konsumtif, 0,067%/hari produktif) masih dari riset internal; tidak muncul di 4 skenario uji. Nomor SEOJK sudah benar menurut penguji.

## Catatan jujur
- Sisi SEBELUM tidak dijalankan ulang (dipakai dari 1.0.0, pesan identik, model dasar sama).
- Durasi 19–34 detik per run, tanpa timeout.

**skor_kualitas usulan: 9**
