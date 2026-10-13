# Hasil Uji – surat-peringatan-karyawan

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** SKILL.md, README.md, ATTRIBUTION.md, `references/regulasi.md`, `references/proses-dan-proporsionalitas.md`, `references/template-sp.md`, `scripts/masa_berlaku.py`
- **Metode:** 5 skenario dijalankan dengan berperan sebagai agent yang memuat SKILL.md, ditambah 1 uji A/B (S1 tanpa skill). Script dijalankan sungguhan di `/tmp/uji-surat-peringatan-karyawan/`. Logika tanggal diverifikasi dengan script Python terpisah milik penguji (rumus bulan kalender sendiri), yang dibandingkan untuk **setiap tanggal 2025–2028 × masa berlaku 1–12 bulan (17.532 kasus): 0 selisih**. Nama hari dicek dengan `datetime`.

## Audit keamanan
`masa_berlaku.py` hanya memakai library standar (argparse, calendar, json, re, sys, datetime). Tidak ada akses jaringan, penulisan/penghapusan file, `subprocess`/`eval`, maupun pembacaan variabel lingkungan atau kredensial. SKILL.md dan referensi tidak memuat prompt injection. Skill mengingatkan kerahasiaan data karyawan (UU 27/2022 tentang PDP) dan melarang penyebaran SP di grup WA. **Aman.**

## Uji script (data tepi)
| Input | Hasil | Seharusnya | Status |
|---|---|---|---|
| `--terbit 23-09-2026` | s.d. 22 Maret 2027 (Senin) | sama | ✅ |
| `--terbit 14-07-2026 --cek 17-09-2026` | s.d. 13 Januari 2027, MASIH AKTIF (sisa 118 hari) | sama | ✅ |
| `--terbit "2 Januari 2026" --cek "18 September 2026"` | s.d. 1 Juli 2026, SUDAH BERAKHIR | sama | ✅ |
| `31-08-2026`, `30-08-2026`, `29-08-2026` | semua s.d. 28 Februari 2027 | sesuai aturan tertulis (akhir bulan) | ✅ |
| `28-08-2026` | 27 Februari 2027 | sama | ✅ |
| `29-02-2028` (kabisat) | 28 Agustus 2028 | sama | ✅ |
| `31-03-2026` | 30 September 2026 | sesuai aturan akhir bulan | ✅ |
| `31-12-2026` | 30 Juni 2027 | sama | ✅ |
| Format `23 Sept 2026`, `23 sep. 2026`, `2026/09/23`, `23.09.2026`, `31 Agt 2026` | terbaca | terbaca | ✅ |
| `31-02-2026`, `23/13/2026` | ERROR "tidak ada di kalender" | error jelas | ✅ |
| kosong, `kemarin`, `23 Septembar 2026` | ERROR jelas + contoh format | error jelas | ✅ |
| `Sept 23, 2026` (gaya Inggris) | ERROR "format tidak dikenali" | idealnya terbaca | ⚠️ ringan |
| `--bulan 0`, `13`, `abc`, `1.5` | ERROR jelas | error | ✅ |
| `--cek` = hari terakhir (22-03-2027) | MASIH AKTIF (sisa 0 hari) | benar; kalimat "sisa 0 hari" agak janggal | ⚠️ ringan |
| `--cek` sebelum terbit | "sebelum SP terbit" | benar | ✅ |

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B: S1 tanpa skill | Tanpa skill: tanpa tanggal berakhir, ada ancaman PHK, tanpa saksi/tanggal terima, status SP1 tidak dicek. Dengan skill **jelas lebih baik**. |
| 01 | SP2 staf packing, SP1 masih aktif | Sangat baik. Script dipakai, fakta terukur, ada BA dan catatan proses. |
| 02 | "bikinin dong SP2", padahal SP1 sudah habis | Sangat baik. Skill mengoreksi ke SP1 berdasarkan script dan menjelaskan pengecualiannya. |
| 03 | Pemilik emosi minta langsung SP3/pecat | Sangat baik. Risiko dijelaskan, disarankan SP1, fakta netral, ada saran penanganan video viral. |
| 04 | "karyawan saya sering telat" | Sangat baik. Bertanya sekali (5 pertanyaan), tanpa tuduhan umum. |
| 05 | Surat PHK + pesangon | Baik. Menolak tegas tanpa angka, tetap menawarkan bantuan yang relevan. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description tepat) | 9 | Kata kunci SP1/2/3, teguran, telat/bolos, EN (warning letter). "Bukan untuk surat PHK" eksplisit. |
| Kemudahan awam | 8 | Satu kalimat cukup. Butuh Python untuk tanggal, tapi ada fallback manual yang jelas. |
| Kualitas output | 9 | SP + BA + catatan proses + disclaimer. Nada netral, harapan terukur. |
| Akurasi (angka/fakta) | 9 | Tanggal 100% cocok dengan verifikasi independen. Dasar PP 35/2021 Pasal 52 tepat dan bertanggal, bagian yang belum pasti ditandai ⚠️. |
| Penanganan input kurang | 9 | Tanya sekali, atau template + asumsi. |
| Penanganan di luar cakupan | 8 | PHK/pesangon ditolak dengan benar. Penjelasan prosedur PHK belum bersumber di referensi. |
| Keamanan | 10 | Lokal, library standar, menjaga kerahasiaan data karyawan. |

## SKOR AKHIR: 8 / 10 → **LULUS**

Skill ini matang. Script akurat di semua kasus tepi yang diuji, dan skill benar-benar mencegah kesalahan yang umum dilakukan pemilik UMKM: SP tanpa tanggal berakhir, loncat ke SP3, ancaman PHK, dan menaikkan tingkat dari SP yang sudah kedaluwarsa. Uji A/B menunjukkan nilai tambah yang jelas. Tidak ada cacat berat atau sedang.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- Tidak ada.

### Ringan
- **R1 – Tidak ada pedoman tanggal mana yang dicek untuk pelanggaran berulang** (SKILL.md langkah 3). Contoh 01 punya 5 tanggal pelanggaran. *Saran:* ubah menjadi `--cek "<tanggal pelanggaran baru PERTAMA>"`, plus kalimat "Jika pelanggaran berulang, cek tanggal pertama; bila sebagian terjadi setelah SP lama berakhir, jelaskan ke pengguna."
- **R2 – SP yang sudah berakhir: boleh disebut atau tidak?** (SKILL.md, *Batasan*). *Saran:* tambahkan "SP yang sudah berakhir boleh disebut sebagai riwayat, tetapi tidak menjadi dasar menaikkan tingkat."
- **R3 – Kalimat "sisa 0 hari" pada hari terakhir berlaku** (`scripts/masa_berlaku.py`, fungsi `hitung`, cabang `masih_aktif`). *Saran:* bila `sisa == 0`, tulis "hari ini adalah hari terakhir SP berlaku".
- **R4 – Format tanggal gaya Inggris ("Sept 23, 2026") belum didukung** (`parse_tanggal`). Error-nya jelas, jadi hanya ringan. *Saran:* tambahkan pola `([A-Za-z]+)\.?\s+(\d{1,2}),?\s+(\d{4})`.
- **R5 – Matriks proporsionalitas tidak membedakan ringan vs sedang** (`references/proses-dan-proporsionalitas.md` bagian B), padahal langkah 2 SKILL.md menyarankan teguran lisan untuk "pelanggaran ringan pertama". *Saran:* tambahkan kolom "Tingkat keseriusan (ringan/sedang/berat)".
- **R6 – Penjelasan singkat alur PHK tidak bersumber** (untuk menjawab S5). *Saran:* tambahkan 2–3 baris alur umum (pemberitahuan tertulis → bipartit → mediasi Disnaker) dengan sumber di `references/regulasi.md`, bertanda ⚠️ PERLU VERIFIKASI setelah UU baru.
- **R7 – Contoh nomor di SKILL.md (`001/SP/TB-MAJU/IX/2026`) tidak konsisten dengan pola di template (`001/SP-1/[SINGKATAN]/...`).** *Saran:* samakan menjadi `001/SP-1/TB-MAJU/IX/2026`.
- **R8 – README merujuk `CARA-INSTAL.md`** dan ATTRIBUTION merujuk `LISENSI.txt`, dan keduanya tidak ada di folder skill. Pastikan keduanya ikut dalam paket rilis.
