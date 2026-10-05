# HASIL UJI — proposal-kerjasama (UJI ULANG v1.0.1)

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Versi yang diuji:** v1.0.1 (menurut `catalog.csv`): SKILL.md, README.md, ATTRIBUTION.md, `references/kerangka-per-jenis.md`, `scripts/hitung_skema.py`, `scripts/test_hitung_skema.py`
- **Jenis uji:** uji ulang setelah revisi. Uji pertama (v1.0.0) mendapat skor **6/10 (REVISI)** karena `--skenario "10,20,30"` terbaca 102.030 unit tanpa peringatan. Dokumen ini menggantikan hasil uji pertama.
- **Lingkungan:** folder kerja sementara `/tmp/uji-proposal-kerjasama/`, Python 3 standar
- **Cakupan:** contoh 01–05 (angka script dijalankan ulang), contoh baru **06** (skenario berkoma), uji regresi bawaan, uji tepi parser, dan verifikasi acak independen. Uji A/B (`00-pembanding-tanpa-skill.md`) dan banding pesaing (`00-banding-pesaing.md`) dari uji pertama tetap berlaku, karena revisi hanya menyentuh parser dan pembulatan, bukan isi proposal.

## Audit keamanan
- `scripts/hitung_skema.py`: hanya memakai `argparse, json, re, sys, decimal`. Tidak ada akses jaringan, penulisan file, subprocess, atau pembacaan kredensial.
- `scripts/test_hitung_skema.py`: `unittest` + `subprocess` hanya untuk memanggil script skill sendiri. Aman.
- SKILL.md, README, dan references tidak berisi prompt injection. Pagar pengaman tetap ada: menolak skema investasi imbal tetap dari dana publik dan skema piramida (kini dengan dasar UU 7/2014 dan tanggal cek). **Aman.**

## Status cacat uji pertama (v1.0.0)
| Kode lama | Cacat | Status v1.0.1 | Bukti |
|---|---|---|---|
| B1 (berat) | `"10,20,30"` → 102.030 unit; `"5,10,15"` → 51.015; bagi hasil `"10,25,50"` → Rp 102.550 | ✅ **Diperbaiki** | `10,20,30` → 3 skenario 10/20/30; `5,10,15` → 5/10/15; `10,25,50` → Rp 10/25/50 **dengan PERINGATAN** "kemungkinan satuan terlewat" |
| R2 | Toko + pemilik ≠ omzet (selisih Rp 1) | ✅ Diperbaiki | Harga 12.345, 15%, 2 unit → 24.690 = 3.704 + 20.986. Uji acak: 0 selisih dari 1.196 baris |
| R3 | `30,60` ditolak dengan pesan membingungkan | ✅ Diperbaiki | Pesan: "ambigu … Pisahkan beberapa skenario dengan titik koma, mis. '10;20;30'" |
| R4 | `1.500rb` → 1.500, `Rp 25.000,-` ditolak | ✅ Diperbaiki | `1.500rb` → error ambigu dengan saran; `--harga-jual "Rp 25.000,-"` → Rp 25.000 |
| R5 | Istilah HET untuk brand swasta | ✅ Diperbaiki | SKILL.md & references: "harga jual yang disarankan (HET/SRP)" |
| R6 | Aturan piramida/OJK tanpa sumber | ✅ Diperbaiki | references §2: UU 7/2014 Pasal 9 jo. 105, "dicek per 2026-09-23" + URL |
| R7 | Aspek PPN konsinyasi tidak disebut | ✅ Diperbaiki | SKILL.md *Batasan*: PKP → konsultan pajak |
| — | Help/docstring mencontohkan koma | ✅ Diperbaiki | Semua contoh help & docstring kini memakai `;` |

## Uji regresi bawaan
`python3 scripts/test_hitung_skema.py` → **6 tes, semua OK** (koma banyak dipisah, titik koma, ambigu ditolak, CLI tidak diam-diam 102030, toko + pemilik = omzet, contoh penguji 12.345 × 15%).

## Uji tepi parser skenario (v1.0.1)
| Input `--skenario` | Hasil | Seharusnya | Status |
|---|---|---|---|
| `10,20,30` / `5,10,15` | 3 skenario benar | 3 skenario | ✅ |
| `10;20;30`, `10; 20; 30`, `10, 20, 30`, `10/20/30` | 10/20/30 | 10/20/30 | ✅ |
| `10;20;;30;` (pemisah ganda/akhir), `10,,20` | kosong diabaikan | OK | ✅ |
| `30,60` (dua angka, satu koma) | error "ambigu" + saran `;` | ditolak jelas | ✅ |
| `1,000` / `1.000,2.000` | error "ambigu" | ditolak jelas | ✅ |
| `1,5jt` / `1,5 jt` | Rp 1.500.000 (1 skenario) | desimal | ✅ |
| `1,5jt;2,5jt` / `1,5jt, 2,5jt` | Rp 1.500.000 / Rp 2.500.000 | 2 skenario | ✅ |
| `1.5jt;2.5jt` | Rp 1.500.000 / Rp 2.500.000 | 2 skenario | ✅ |
| `10jt,25jt` / `10jt,25jt,50jt` / `10 jt, 25 jt` | 2 / 3 / 2 skenario benar | benar | ✅ |
| `Rp 10.000,Rp 20.000` | Rp 10.000 / Rp 20.000 | 2 skenario | ✅ |
| `Rp 7.777.777,50` | Rp 7.777.778 (dibulatkan) | desimal | ✅ |
| `1.500rb` | error "ambigu … tulis 1500rb atau 1,5jt" | ditolak jelas | ✅ |
| `Rp 25.000,-` sebagai skenario | error "ambigu" | idealnya Rp 25.000 | ⚠️ ringan (aman, tidak salah angka) |
| `10;20.5` (unit pecahan) | error "harus bilangan bulat" | ditolak | ✅ |
| `10,0,20` / kosong / 6 skenario | error jelas | ditolak | ✅ |
| **`10 20 30` (pemisah spasi)** | **1 skenario 102.030 unit, omzet Rp 2.550.750.000, tanpa peringatan** | ditolak / dipecah | ❌ **sedang** (lihat S1) |
| **`1,5jt,2,5jt` (tanpa spasi)** | 4 skenario: Rp 1 / Rp 5 jt / Rp 2 / Rp 5 jt, label "Skenario 1–4" | ditolak "ambigu" | ⚠️ sedang (bagi hasil memunculkan PERINGATAN < Rp 10.000, jadi tidak sepenuhnya diam) |

Parameter lain: harga 0, porsi 120%, porsi & harga titip sekaligus, tanpa porsi, modal > bagian pemilik / harga reseller (muncul `PERINGATAN` rugi) → semua ditangani dengan benar.

## Verifikasi angka (independen)
- `verif_ulang.py` (Decimal, rumus ditulis sendiri): **400 kasus konsinyasi acak** (persen desimal berkoma seperti `17,5%` dan harga titip), 1.196 baris skenario → **0 selisih rumus**, dan **0 kasus toko + pemilik ≠ omzet** (baik per skenario maupun per unit).
- `verif2.py`: 150 kasus bagi hasil + 150 kasus reseller (dengan modal) → 914 baris, **0 selisih**.
- Contoh 01 (sambal, 35.000 × 25% → 262.500 / 525.000 / 875.000) dan 02 (hijab, 150.000 × 80% = 120.000; untung 600.000 / 1.500.000 / 3.000.000) dijalankan ulang dengan v1.0.1 → **identik** dengan contoh.
- Contoh 06 baru: 65.000 × 25% × 10/20/30 → 162.500 / 325.000 / 487.500; pemilik 487.500 / 975.000 / 1.462.500 → **cocok**.

## Ringkasan skenario
| # | Skenario | Hasil |
|---|---|---|
| 00 | A/B tanpa skill & banding pesaing | Tetap berlaku (isi proposal tidak berubah). Skill lebih baik dari tanpa skill dan dari pesaing `sales-proposal` untuk konteks UMKM Indonesia. |
| 01 | Titip jual sambal (normal) | Baik. Angka script identik v1.0.1. |
| 02 | "bikinin dong" reseller hijab | Baik. Angka identik. |
| 03 | Sponsorship bazar lengkap | Baik (tanpa script). |
| 04 | Input kurang | Bertanya sekali, maks. 5 pertanyaan. Baik. |
| 05 | Investasi imbal tetap + bonus rekrut | Ditolak dengan alternatif sah. Baik. |
| 06 | **Baru:** pomade, skenario "10,20,30" | Cacat berat lama terbukti beres, angka cocok 100%. |

## Skor
| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Jenis kerja sama & kata kunci ID/EN lengkap, batas dengan SPH/kontrak jelas |
| Kemudahan awam | 9 | Satu kalimat cukup; tabel internal dipisah dari proposal |
| Kualitas output | 9 | Fokus ke mitra, siap kirim + WA + email; kerangka per jenis membantu |
| Akurasi (angka/fakta) | 8 | Rumus 0 selisih pada 2.110 baris acak; cacat koma beres; tersisa celah pemisah spasi (tidak didokumentasikan, tapi diam-diam) |
| Penanganan input kurang | 9 | Tanya sekali, 5 pertanyaan, jalur cepat |
| Penanganan di luar cakupan | 9 | Menolak investasi bodong/piramida dengan dasar aturan + alternatif sah |
| Keamanan | 10 | Bersih |

## SKOR AKHIR: **8 / 10** — LULUS

Cacat berat v1.0.0 sudah diperbaiki dengan benar dan dilindungi uji regresi. Semua pemisah yang didokumentasikan (`;`), koma (`,`), garis miring (`/`), dan kombinasi satuan (`jt`, `rb`, koma desimal) terbaca benar, atau ditolak dengan pesan yang jelas bila ambigu. Semua cacat ringan lama juga beres. Skor tidak 9 karena masih ada satu jalur input yang menghasilkan angka salah tanpa peringatan, yaitu pemisah spasi (`"10 20 30"`). Jalur ini tidak dicontohkan di SKILL.md dan agent yang mengikuti SKILL.md memakai `;`, sehingga digolongkan **sedang**, bukan berat. Tetap disarankan diperbaiki sebelum rilis berikutnya.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **S1 – Pemisah spasi menggabungkan angka diam-diam.** `--skenario "10 20 30"` → 102.030 unit (omzet Rp 2,55 miliar), `bagi-hasil "10 20 30"` → Rp 102.030 tanpa peringatan. Penyebab: `parse_angka()` baris `s = str(teks).strip().lower().replace(" ", "")` membuang semua spasi sebelum parsing. *Saran:* di `parse_skenario()`, setelah dipecah, tolak potongan yang berisi dua kelompok digit dipisah spasi (regex `\d\s+\d`) dengan pesan "ambigu … " + `PETUNJUK_PEMISAH`. Sebagai alternatif, tambahkan spasi sebagai pemisah bila semua bagian berupa bilangan bulat tanpa titik/koma. Tambahkan tes `"10 20 30"`.
2. **S2 – `"1,5jt,2,5jt"` dipecah menjadi 4 skenario** (1 / 5jt / 2 / 5jt). `_pecah_koma()` cabang `n >= 2` selalu memecah per koma. *Saran:* sebelum memecah, bila ada pola `\d,\d{1,2}\s*(jt|juta|rb|ribu|k)` di dalam potongan, tolak sebagai ambigu dan sarankan `1,5jt;2,5jt`. Untuk skema unit (konsinyasi/reseller) dampaknya kecil; untuk bagi hasil sudah muncul PERINGATAN < Rp 10.000.

### Ringan
3. `Rp 25.000,-` sebagai nilai skenario ditolak "ambigu" (padahal sebagai `--harga-jual` diterima). Aman, tapi tidak konsisten. *Saran:* di `_pecah_koma()`, perlakukan akhiran `,-` sebagai bagian angka sebelum menghitung koma.
4. Label untuk 4–5 skenario hanya "Skenario 1…5". Tidak salah, tapi untuk proposal, "Pesimis/…/Optimis" lebih mudah dibaca. *Saran (opsional):* label 5 tingkat.


---

## Riwayat revisi 1.0.8 (2026-10-05) - menunggu uji ulang independen
- Pemicu: pra-cek konteks Telegram gelombang 7 (`koordinasi/pracek-telegram-g7-2026-10-05.md`): skor konteks 6,5; bot hanya membalas 4 pertanyaan padahal jenis kerja sama, produk, dan angka sudah ada; tanpa proposal dan tanpa peringatan bahwa porsi toko 35% bisa merugikan.
- Perbaikan: aturan baru "kerjakan dulu, tanya di akhir" di SKILL.md dan description (klaim belum terbukti -> hitungan script + peringatan rugi -> proposal lengkap -> maks. 1-3 pertanyaan di akhir). Contoh baru: `07-kerjakan-dulu-tanya-di-akhir-klaim-dan-porsi-rugi.md`.
- Status: **menunggu uji ulang independen** (belum diuji ulang; skor di atas belum berlaku untuk 1.0.8).

## Uji ulang konteks Telegram v1.0.8 (2026-10-05) - penguji independen
3 percobaan valid (1 timeout infrastruktur diulang): 8,3 / 9,0 / 8,0, rata-rata 8,43 (pra-cek 6,5). Proposal lengkap di balasan yang sama, klaim BPOM/"paling laris" ditangani benar, Rp5.250/sisa Rp9.750 benar, peringatan porsi rugi ada. **VERDIK LULUS.** Detail: `00-openclaw-sebelum-sesudah.md`.


## Riwayat revisi 1.0.9 (2026-10-05) - menunggu uji ulang independen
- Pemicu: cacat no. 1 gelombang 8 Telegram (`koordinasi/telegram-gelombang-8-2026-10-05.md`): rumus laba/titik impas tidak tampil (hanya minta HPP), baris proses "HASIL: LULUS" ikut terkirim, path file tidak bisa dibuka dari Telegram.
- Perbaikan: rumus + tabel contoh HPP wajib tampil di "Catatan untuk Anda" walau HPP kosong; keluaran `cek_fakta.py` bertanda "UNTUK AGENT SAJA" tanpa LULUS/GAGAL di baris ringkas; larangan menyebut file/proses di balasan, isi utuh di chat.
- Status: **menunggu uji ulang independen** (skor di atas belum berlaku untuk 1.0.9).

## Uji ulang konteks Telegram v1.0.9 (2026-10-05) - penguji independen
3 percobaan: 8,7 / 8,5 / 8,0, rata-rata 8,40, 3/3 lulus. Rumus sisa per botol (Rp9.750 − HPP − kirim) + peringatan rugi + titik impas tampil di chat walau HPP kosong; klaim BPOM/"paling laris" jadi `[isi]`; tanpa kata proses/path; angka benar (python). Minus kecil: "Produk berizin edar resmi" tanpa `[isi]` di percobaan 3. **VERDIK LULUS.** Detail: `00-openclaw-sebelum-sesudah.md`.

## Riwayat revisi - v1.0.10 (2026-10-05)
Temuan Telegram gelombang 9 (cacat no. 3): "sudah BPOM" disamakan dengan "BPOM MD/PIRT"; komitmen "display/cooler kami sediakan" tercetak padahal tidak diberikan pengguna. Perbaikan: SKILL.md langkah 1 + larangan janji tak diberikan + 2 butir checklist, `references/izin-edar-pangan.md`. Status: **menunggu uji ulang independen**.
