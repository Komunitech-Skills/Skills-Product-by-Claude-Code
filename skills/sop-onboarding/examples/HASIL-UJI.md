# HASIL UJI — sop-onboarding (Tahap 6, penguji independen)

Tanggal uji: 25 September 2026 · Penguji: agent terpisah dari pembuat (hanya membaca folder skill; `skills/sop-writer`
dicek sekilas untuk batas cakupan) · Script dijalankan dari salinan di scratchpad · Versi diuji: 1.0.0 (status `draft`).

## 1. Ringkasan skenario
| # | File | Skenario | Hasil |
|---|---|---|---|
| 00 | `00-pembanding-tanpa-skill.md` | A/B skenario 01 | Dengan skill **17/18** vs tanpa skill 5/18 → jelas lebih baik |
| 00 | `00-banding-pesaing.md` | vs `team-onboarding-playbook` (rampstackco) | Skill kita **15/20** vs pesaing 9/20 → menang; kalah di panduan buddy, ritme check-in, target per peran, retrospektif |
| 01 | `01-kafe-yogyakarta-2-barista-pkwtt.md` | Kafe, 2 barista PKWTT, 6 hari, shift | ✅ lengkap, tanggal benar |
| 02 | `02-klinik-gigi-perawat-pkwt.md` | Klinik gigi, perawat PKWT 1 th, 1 Des 2026 | ✅ tanpa masa percobaan; ⚠️ libur Natal hanya terhitung karena penguji menyiapkan file libur sendiri |
| 03 | `03-kantor-konsultan-admin-cepat.md` | "Cepat saja": WA + 30-60-90 | ✅ ringkas; ⚠️ evaluasi 90 hari jatuh tepat di hari terakhir percobaan; default `pkwtt` memunculkan asumsi percobaan |
| 04 | `04-input-tidak-lengkap.md` | "bikin onboarding karyawan" | ✅ tanya sekali, 8 butir, tidak mengarang tanggal |
| 05 | `05-di-luar-cakupan-berisiko.md` | Percobaan 6 bln untuk PKWT + gaji < UMK + data KTP/rekening keluarga | ✅ ditolak dengan dasar hukum & alternatif; ⚠️ nuansa upah usaha mikro/kecil tidak ada di skill |

Tes bawaan `python3 tests/uji_regresi.py` → **LULUS semua 46 cek** (tidak mencakup akhir bulan, H1 di hari libur,
atau evaluasi 90 hari yang melewati batas percobaan).

## 2. Verifikasi tanggal independen
Penguji menulis kalkulator sendiri **tanpa membaca kode script** (`verif_mandiri.py` di scratchpad), memakai aturan
SKILL.md: minggu 1 = mulai+6, hari 30/60/90 = mulai+29/59/89, akhir percobaan = tanggal sama 3 bulan kemudian −1;
hari kerja 5 (Sabtu+Minggu libur) atau 6 (Minggu libur); tanggal evaluasi digeser **maju**, evaluasi akhir percobaan
digeser **mundur** (aturan geser disimpulkan dari contoh, karena tidak ditulis di teks SKILL.md).
Libur uji (SKB 3 Menteri 2026 & 2027): 24–25 Des 2026, 1 & 5 Jan 2027, 5–6 Feb 2027, 8–12 & 15 Mar 2027.

| Kasus | Tahap | Hitung penguji | Script | Cocok? |
|---|---|---|---|---|
| 01: 5 Okt 2026, 6 hari, PKWTT | H1 / mg1 / 30 / 60 / 90 | 5 Okt / 11→12 Okt / 3 Nov / 3 Des / 2 Jan 2027 | sama | ✅ |
| | Akhir percobaan (hukum → evaluasi) | 4 Jan 2027 → 4 Jan 2027 | sama | ✅ |
| 02: 1 Des 2026, 6 hari, PKWT + libur | 30 / 60 / 90 | 30 Des / 29 Jan / 28 Feb (Min) → 1 Mar 2027 | sama; tanpa baris percobaan | ✅ |
| 03: 12 Okt 2026, 5 hari, PKWTT | 90 / akhir percobaan | 9 Jan (Sab) → 11 Jan / 11 Jan 2027 | sama | ✅ |
| Mulai 31 Jan 2027 (Minggu), 5 hari | H1 | 31 Jan (Minggu) → mestinya 1 Feb | **31 Jan, "Tidak" digeser** | ❌ temuan P2-1 |
| | Akhir percobaan | rumus fallback SKILL.md: 30 Apr (klip) −1 = **29 Apr**; alternatif akhir bulan ke-3 = 30 Apr | **30 Apr 2027** | ⚠️ script lebih masuk akal; fallback manual beda |
| Mulai 29 Feb 2028, 5 hari | Akhir percobaan | 28 Mei 2028 (Min) → evaluasi Jum 26 Mei | sama | ✅ |
| | Evaluasi 90 | 28 Mei → Sen 29 Mei 2028 (**setelah** batas 28 Mei) | sama | ⚠️ P1-1 |
| Mulai 30 Nov 2027 | Akhir percobaan | fallback: 28 Feb 2028; alternatif 29 Feb | **29 Feb 2028** | ⚠️ fallback beda |
| Mulai Minggu 4 Okt 2026, 5 hari, libur 1 Jan | H1 | → 5 Okt | **4 Okt (Minggu), tidak digeser** | ❌ P2-1 |
| | 90 / akhir percobaan | 1 Jan (libur) → 4 Jan / 3 Jan (Min) → 31 Des | sama | ✅ hitungan; ⚠️ evaluasi 90 **setelah** batas |
| Mulai 14 Des 2026 + libur Lebaran 2027 | 90 | 13 Mar (Sab) → maju melewati 15 Mar → **16 Mar** | sama | ✅ |
| | Akhir percobaan | 13 Mar → mundur melewati 8–12 Mar → **5 Mar** | sama | ✅ (evaluasi 90 = 11 hari setelah batas hukum) |
| Mulai 10 Feb 2027 + libur | 30 / 90 / akhir | 11 Mar→16 Mar / 10 Mei / 9 Mei (Min) → 7 Mei | sama | ✅ hitungan; ⚠️ evaluasi 90 setelah batas |

**Penilaian definisi "3 bulan":** script memakai (mulai − 1 hari) + 3 bulan kalender, bila tanggal tidak ada → akhir
bulan (31 Jan → 30 Apr; 30 Nov 2027 → 29 Feb 2028; 29 Feb 2028 → 28 Mei). Ini masuk akal dan tidak pernah melebihi 3
bulan. Tetapi **tidak dijelaskan** di SKILL.md, dan rumus fallback manual di SKILL.md ("tanggal sama 3 bulan
kemudian dikurangi 1 hari") memberi hasil berbeda di akhir bulan (29 Apr, 28 Feb). Pergeseran **mundur** untuk
evaluasi akhir percobaan tepat (keputusan harus sebelum batas), dan catatan script menjelaskan tanggal hukum tidak
digeser. Namun aturan geser (maju/mundur) tidak ditulis di teks SKILL.md.

### Uji data rusak
| Input | Hasil |
|---|---|
| `--mulai 31/02/2026`, `2026-13-01`, `abc`, kosong | ✅ pesan ERROR ramah, exit code 2 |
| `5 Okt 2026`, `05-10-2026`, `Senin, 5 Oktober 2026`, `10/05/2026` (=10 Mei, DD/MM) | ✅ terbaca benar |
| `--mulai 9999-12-31` | ❌ Traceback (overflow) — P3 |
| `--mulai 1900-01-01` | ⚠️ diterima tanpa peringatan — P3 |
| `--libur` baris teks rusak / file tidak ada | ✅ ERROR ramah dengan nomor baris |
| `--libur` file kosong | ✅ dianggap tanpa libur |
| `--libur` CSV titik-koma ekspor Excel ID (`tgl;keterangan` / `25/12/2026;Natal`) | ❌ gagal di baris 1 — P3 |
| `--hari-kerja 7` | ✅ ditolak argparse |

## 3. Pemeriksaan hukum (web search, 25 Sep 2026)
| Poin | Status | Sumber |
|---|---|---|
| PKWT tidak boleh masa percobaan, batal demi hukum, masa kerja tetap dihitung (Ps. 58 jo. UU 6/2023 Ps. 81 angka 14; PP 35/2021 Ps. 12) | ✅ benar | hukumonline.com/klinik/a/masa-percobaan-karyawan-kontrak-lt62a8cadf0ce0d ; bplawyers.co.id/2025/08/11/pkwt-tidak-boleh-memuat-klausul-masa-percobaan… ; wageindicator.org (PKWT) |
| PKWTT percobaan maks. 3 bulan, upah tidak di bawah upah minimum (Ps. 60) | ✅ benar | pasal.id/peraturan/uu/uu-no-13-tahun-2003/pasal-60 ; hukumonline.com/berita/a/landasan-hukum-masa-probation-lt63b3f6a60c1ec |
| BPJS TK & Kesehatan wajib; 30 hari sejak mulai kerja | ✅ benar (dasar pasal 30 hari sebaiknya dirinci) | hukumonline.com/klinik/a/wajibkah-pengusaha-mendaftarkan-pekerjanya-di-bpjs…; wageindicator.org (jaminan sosial) |
| UU PDP minimisasi / pembatasan tujuan (Ps. 16 ayat 2) | ✅ benar | hukumonline.com/berita/a/kenali-prinsip-prinsip-pemrosesan-data-pribadi-dalam-uu-pdp-lt66c6947421f2b |
| Pengecualian upah minimum usaha mikro & kecil (Ps. 90B jo. UU 6/2023; PP 36/2021 Ps. 36: kesepakatan, min. 50% rata-rata konsumsi & 25% di atas garis kemiskinan) | ❌ **tidak disebut** | hukumonline.com/klinik/a/upah-minimum-usaha-kecil-lt50c7d16e6ea32 ; literasihukum.com/upah-minimum-umkm |
| Libur nasional & cuti bersama 2026/2027 (SKB 3 Menteri) | tidak dimuat skill | kemenkopmk.go.id (2026: cuti bersama Natal 24 Des); SKB No. 1205/2026 (2027: Lebaran 9–15 Mar, Nyepi 8 Mar) |
| Disclaimer & tanggal cek | ✅ ada (SKILL.md, referensi, formulir) | — |
| Angka UMK karangan | ✅ tidak ada | — |

## 4. Temuan berprioritas
**P1 (wajib diperbaiki sebelum lulus)**
1. **Evaluasi 90 hari sering jatuh SETELAH batas masa percobaan** tanpa peringatan (3 bulan = 89–92 hari). Contoh:
   mulai 4 Okt 2026 (evaluasi 4 Jan vs batas 3 Jan), 14 Des 2026 (16 Mar vs 13 Mar), 10 Feb 2027 (10 Mei vs 9 Mei),
   29 Feb 2028 (29 Mei vs 28 Mei). Baris itu berlabel "akhir orientasi (isi formulir evaluasi)" sehingga pemilik bisa
   memutuskan kelulusan setelah karyawan otomatis tetap. *Lokasi:* `scripts/jadwal_onboarding.py` (tahap `hari90`),
   SKILL.md langkah 6. *Usul:* untuk PKWTT, bila hari90 > tanggal evaluasi akhir percobaan, gunakan tanggal evaluasi
   akhir percobaan untuk formulir (atau tambahkan catatan/peringatan eksplisit), dan tambah tes regresinya.
2. **Contoh di SKILL.md & README salah/tidak konsisten.** Tabel contoh SKILL.md berlabel "6 hari" tetapi berisi output
   `--hari-kerja 5` (hari 90 → 28 Des; evaluasi percobaan → **25 Des 2026 = Hari Natal**). Output 6 hari yang benar:
   26 Des / 26 Des (lihat `uji-pembuat-01`). README menulis "akhir masa percobaan 25 Desember 2026" — batas hukum yang
   benar **27 Desember 2026**; 25 Des hanya tanggal evaluasi (dan itu libur nasional). *Lokasi:* SKILL.md bagian Contoh;
   README "Sebelum & sesudah". *Usul:* salin ulang output script yang benar dan bedakan "batas hukum" vs "evaluasi".

**P2**
1. **H1 di hari libur tidak digeser/diperingatkan** (mulai Minggu 31 Jan 2027 / 4 Okt 2026 → "Tidak" digeser). *Usul:* beri
   peringatan "tanggal mulai jatuh di hari libur" atau geser maju + catatan.
2. **Tidak ada daftar libur nasional bawaan**; SKILL.md hanya memakai `--libur` bila pengguna punya daftar → evaluasi
   bisa jatuh di Natal/Lebaran. *Usul:* sertakan `references/libur-nasional-2026-2027.csv` (SKB 3 Menteri, bertanggal cek)
   dan jadikan default, dengan catatan verifikasi tahunan.
3. **Aturan geser & definisi 3 bulan tidak tertulis**, dan rumus fallback manual berbeda dengan script di akhir bulan
   (31 Jan → 29 Apr vs 30 Apr). *Lokasi:* SKILL.md langkah 3. *Usul:* tulis "akhir percobaan = (mulai − 1 hari) + 3 bulan;
   bila tanggal tidak ada → akhir bulan; evaluasi digeser maju, evaluasi akhir percobaan digeser mundur".
4. **Upah minimum usaha mikro & kecil** tidak dijelaskan; kalimat "tidak boleh di bawah upah minimum" absolut, padahal
   audiens UMKM. Upah minimum di luar masa percobaan (PKWT) juga tidak ada di referensi. *Lokasi:*
   `references/dasar-hukum-onboarding.md` §1, checklist, formulir. *Usul:* tambah poin Ps. 88E/90B + PP 36/2021 Ps. 36
   bertanda PERLU REVIEW, arahkan ke Disnaker.
5. **Formulir evaluasi untuk PKWT** memakai istilah masa percobaan, opsi "Lanjut sebagai karyawan tetap" dan "Perpanjang
   masa pemantauan" — tidak ada instruksi adaptasi di SKILL.md; agent harus berimprovisasi. *Usul:* varian PKWT di
   template + catatan risiko pemutusan PKWT sebelum waktunya (ganti rugi, Ps. 62).

**P3**
1. SKILL.md menyebut contoh "varian bengkel, karyawan PKWT, input tidak lengkap" di `examples/` — belum ada saat diuji
   (PKWT & input tidak lengkap kini tercakup file uji 02 & 04; bengkel belum).
2. Default `--jenis pkwtt` diam-diam memunculkan baris masa percobaan saat pengguna tidak menyebut jenis (uji 03).
   *Usul:* SKILL.md: bila jenis tidak diketahui, sebut asumsi atau jalankan tanpa baris percobaan.
3. Mode cepat tanpa tanggal mulai: fallback tidak dijelaskan (tanya tanggal atau tabel relatif H+29).
4. Script: overflow `9999-12-31` → Traceback; tahun tak wajar diterima; CSV titik-koma/kolom kedua tidak didukung.
5. Kegiatan di tabel script generik; tidak ada target 30/60/90 per jabatan, panduan buddy, ritme check-in, retrospektif
   (kelebihan pesaing, lihat `00-banding-pesaing.md`).
6. "Akhir minggu 1" yang jatuh Minggu digeser ke Senin minggu ke-2; lebih wajar mundur ke hari kerja terakhir minggu 1.

## 5. Skor
**6 / 10 — REVISI, belum lulus.**
Alasan: inti skill kuat (A/B jelas lebih baik, menang dari pesaing, dasar hukum benar dan bertanggal, script teruji,
penolakan permintaan berisiko baik, tidak mengarang aturan/UMK). Namun nilai jual utama "tanggal pasti" tercederai
oleh P1: evaluasi 90 hari yang dapat jatuh setelah batas masa percobaan tanpa peringatan, dan contoh unggulan di
SKILL.md/README yang menampilkan tanggal salah (termasuk menyebut 25 Des 2026 — Hari Natal — sebagai "akhir masa
percobaan"). Keduanya mudah diperbaiki. Setelah P1 + P2-1..P2-3 beres dan tes regresi ditambah, skor realistis 8.
Uji ulang oleh penguji independen setelah revisi.
