# HASIL UJI — analisis-rasio-keuangan-usaha v1.0.0

- **Tanggal:** 2026-09-26
- **Penguji:** agent penguji independen Akun B (bukan pembuat), Claude Code. Hanya membaca folder skill + sumber pesaing.
- **Folder kerja uji:** salinan skill di scratchpad sesi (bukan `.claude/skills/` repo).
- **Tes bawaan:** `python3 tests/uji_regresi.py` → **56 uji, 0 gagal, SEMUA UJI LULUS**.
- **Validator repo:** `python3 scripts/validate.py --skill analisis-rasio-keuangan-usaha` → **✅ 1 skill valid, 87 baris katalog sesuai**.
- **Skenario:** 03 warung 2 tahun · 04 laundry + utang bank · 05 konveksi stok & piutang besar + tren + KUR · 06 input kurang · 07 luar cakupan (saham/kripto & "pastikan disetujui"). Ditambah A/B (`00-pembanding-tanpa-skill.md`) dan banding pesaing (`00-banding-pesaing.md`).
- **uji_openclaw.sh:** tidak dijalankan (sesuai instruksi tugas).

## 1. Verifikasi angka independen (Decimal)
Script `verif.py` ditulis penguji dari rumus buku teks. Tidak mengimpor `rasio.py`, hanya memakai angka mentah. Presisi Decimal 40 digit, dibandingkan dengan `nilai` JSON script (4 desimal, toleransi 0,0001). Rasio cicilan dibandingkan ke 1 desimal.

| Kasus | Nilai dicek | Cocok |
|---|---:|---:|
| S1 warung 2024 (saldo akhir) | 17 | 17 |
| S1 warung 2025 (rata-rata saldo + cicilan) | 18 | 18 |
| S2 laundry (cakupan bunga dari laba usaha, cicilan) | 20 | 20 |
| S3 konveksi Sem-1 (6 bulan disetahunkan, penjualan tempo) | 18 | 18 |
| S3 konveksi Sem-2 (rata-rata saldo + cicilan) | 19 | 19 |
| E2 modal negatif + rugi | 15 | 15 |
| **Total** | **107** | **107 (100%)** |

Rasio yang dicek: rasio lancar, cepat, kas; modal kerja; margin kotor/usaha/bersih; ROA; ROE; DER; DAR; cakupan bunga; perputaran persediaan + umur stok; perputaran piutang + lama piutang; lama bayar pemasok; siklus kas; perputaran aset; rasio cicilan. Tabel lengkap ada di Lampiran A.

## 2. Uji tepi & data rusak
| Kasus | Hasil | Nilai |
|---|---|---|
| Utang lancar 0 | 3 rasio likuiditas "tidak dihitung — tidak ada utang jangka pendek (kondisi aman)", status info | ✔ |
| Penjualan 0 | margin "tidak dihitung — penjualan Rp 0"; lama piutang "penjualan Rp 0" | ✔ |
| HPP 0 | umur stok "HPP Rp 0 — tidak bisa dihitung" | ✔ |
| Modal −20 jt (`--modal -20jt`) | ROE & DER "tidak bermakna" 🔴; DAR 211,1% 🔴; saran "Modal habis/negatif" #2; KUR ✗ | ✔ |
| Laba negatif `(6.000.000)` / `--laba-bersih -2jt` / `=-2jt` | margin/ROA negatif + "Usaha RUGI"; saran rugi #1 | ✔ |
| Kas negatif di tabel | "mustahil", rasio kas & rasio lancar tidak dihitung | ✔ |
| Sel "sepuluh juta" | peringatan "tidak terbaca → dianggap tidak diisi", status SEMENTARA | ✔ |
| Baris tak dikenal ("Utang pemilik ke istri") | dilewati + dilaporkan di "Perlu dicek" | ✔ |
| Laba kotor ≠ penjualan − HPP | peringatan, dipakai penjualan − HPP | ✔ |
| Neraca tidak seimbang (selisih 20 jt) | peringatan + KUR ✗ "rapikan dulu" | ✔ |
| File kosong / .xlsx / PDF / JSON rusak / tidak ada / tanpa data / semua tak terbaca | `GALAT: …` jelas, kode keluar 2 | ✔ |
| Jenis usaha tak dikenal ("konter pulsa", "apotek") | GALAT + pilihan jenis | ✔ |
| Output EMKM (`laporan_emkm.py --format json`) | terbaca; utang bank dipecah; periode 31 hari | ✔ (lihat temuan ringan) |
| Format: `1.250.000`, `Rp 2,5 jt`, `(500.000)`, `Rp 1.500.000,50`, `1,2 M`, `15.000,-`, `500.000-`, `IDR 10,000,000`, `2 juta`, `150rb`, `(Rp 2 jt)`, `Rp -500.000`, `−3.000` | semua benar | ✔ |
| `1.234.56`, `Rp 1.2.3`, `10%`, `1e6`, `seratus ribu` | None → peringatan (tidak ditebak) | ✔ |
| `minus 2jt` | tidak terbaca → peringatan (tidak salah hitung, tetapi tidak dikenali) | ringan |
| CSV koma **tanpa tanda kutip**: `Kas,1,250,000` | terbaca **kas = Rp 1** tanpa peringatan | ✘ sedang |

## 3. Ambang "wajar", tafsiran, disclaimer
- **Sumber ambang tercatat** di `references/ambang-wajar.md`: Kasmir (lewat jurnal pengutip), tolok ukur `interpret_ratios.py` cookbook, dan bunga KUR 6% (Permenko 1/2026, konsisten dengan `pengajuan-kur/references/regulasi.md` yang sudah dicek fakta penguji lain). Penguji mengecek:
  - Nilai Kasmir (CR 200%, QR 150%, DER ≤ 90%, DAR ≤ 35%) sesuai hasil pencarian jurnal pengutip (UBP Karawang, JENSI Unsam). Teks PDF tidak bisa diekstrak di lingkungan uji (tanpa pdftotext), jadi kutipan persis per halaman **belum diverifikasi**.
  - Angka tolok ukur retail/manufacturing cookbook yang dikutip (CR 1,0/1,5; DER 1,5; GM 20%/30%; manufaktur CR 1,3, DER 1,2, GM 18%/25%) **cocok persis** dengan `interpret_ratios.py` commit 813fbee, termasuk label *"simplified for demonstration"*.
- **Tidak disajikan sebagai kepastian:** references bagian 1 ("pedoman praktis Komunitech… bukan standar resmi OJK/BI/IAI/bank"), setiap output mencantumkan "Ambang 'wajar' = pedoman praktis…", disclaimer akhir, dan FAQ README. ✔
- **Tafsiran awam:** setiap rasio punya kalimat "Artinya" ("Dari tiap Rp 100.000 penjualan, laba bersih Rp 4.000"; "Barang rata-rata diam ±42 hari"). ✔
- **Disclaimer bukan nasihat investasi/kredit:** di SKILL.md (format output + checklist), output script, dan README. Bagian KUR selalu ditutup "bukan keputusan kredit… SLIK OJK, agunan…". ✔

## 4. Atribusi MIT (anthropics/claude-cookbooks)
- `LICENSE-MIT` **identik byte-per-byte** dengan `LICENSE` root repo pada commit `813fbeec…` (dicek dengan `diff`). ✔
- Path sumber `skills/custom_skills/analyzing-financial-statements/` (SKILL.md, calculate_ratios.py 346 baris, interpret_ratios.py 377 baris), hash & tanggal commit: **benar**. ✔
- Klaim bahwa sumber memakai `safe_divide` yang mengembalikan 0 dan hanya mengimpor `json`/`typing`: **benar** (dicek di kode). ✔
- Bagian yang tidak dipakai (valuasi P/E, DCF, pembuatan Excel/API) memang tidak ada di skill. `rasio.py` tidak menyalin kode sumber (struktur, nama, dan logika berbeda total). ✔
- Kesimpulan: atribusi **benar dan lengkap**.

## 5. Skor
| Kriteria | Skor (1–10) | Catatan |
|---|---:|---|
| Pemicu (description) | 9 | Spesifik, ID/EN, batas dengan laporan-keuangan-emkm & pengajuan-kur jelas; 801 karakter |
| Kemudahan awam | 9 | Tafsiran sehari-hari, emoji status, tabel siap tempel; 5 pertanyaan sekali kirim |
| Kualitas output | 8 | Lengkap (4 kelompok, tren, KUR, saran urut). Minus: tren campur basis, saran rasio cepat tak kontekstual |
| Akurasi angka | 9 | 107/107 cocok; pembagi nol/negatif benar. Minus: CSV koma tanpa kutip terbaca salah tanpa peringatan |
| Penanganan input kurang | 7 | Pertanyaan tepat, tetapi mode "langsung saja" menyimpulkan "pertahankan" dari 1 rasio |
| Penanganan luar cakupan | 10 | Saham/kripto/P/E ditolak; memoles angka ditolak; tidak menjanjikan kredit |
| Keamanan | 10 | Tanpa jaringan/subprocess/eval; hanya membaca file input; tanpa data pribadi |
| Uji A/B | ✔ | Dengan skill 33/35 vs tanpa skill 17/35, jelas lebih baik |
| Banding pesaing | ✔ | 8,8 vs 3,6 (cookbook) & 4,0 (financial-analyst); pesaing memberi "ROE excellent" untuk modal negatif |
| **SKOR AKHIR** | **8** | |

**Status: LULUS** (≥ 7). Perbaikan tingkat sedang disarankan sebelum `beta`.

## 6. Temuan
### Berat
- Tidak ada.

### Sedang
1. **Tren antarperiode membandingkan basis berbeda** (`rasio.py` `analisis()` baris ~999–1004 mengisi `*_awal` dari periode sebelumnya, sehingga periode terakhir memakai rata-rata saldo sedangkan periode pertama memakai saldo akhir; `tren()` lalu membandingkan keduanya). Dampak nyata:
   - Uji 03: ROA tampil **membaik** 22,2% → 23,7%, padahal dengan basis sama (saldo akhir) 2025 = 21,9% (**memburuk**). Umur stok tampil 41,7 → 41,9 hari, padahal saldo akhir 48,5 hari.
   - Uji 05: lama piutang tampil 60,8 → 61,2 hari, padahal saldo akhir 75,1 hari; umur stok 64,5 vs 75,3 hari.
   **Saran:** hitung tren dengan basis yang sama untuk semua periode (mis. saldo akhir untuk kolom tren, sedangkan tabel utama tetap rata-rata), atau beri catatan "periode pertama memakai saldo akhir". Tambahkan tes regresi untuk kasus ini.
2. **CSV koma tanpa tanda kutip** (`Kas,1,250,000`) → sel terpotong, kas = Rp 1 **tanpa peringatan** (`baca_tabel`: sel melebihi jumlah kolom judul diabaikan diam-diam). **Saran:** bila jumlah sel sebuah baris > jumlah kolom judul, beri peringatan "angka memakai koma sebagai pemisah ribuan; beri tanda kutip atau pakai `;`", atau gabungkan kembali sel angka yang pecah.
3. **Data minim → kesimpulan "pertahankan"** (Uji 06): dari 1 rasio yang dinilai, ringkasan menulis "Semua rasio… wajar — pertahankan", saran "Pertahankan", dan Asumsi "Tidak ada — semua angka diisi pengguna". **Saran:** bila rasio yang dinilai < 5, ganti dengan "data belum cukup" dan daftar pos kosong di Asumsi.
4. **Saran rasio cepat tidak kontekstual** (Uji 04, laundry): "Aset lancar terlalu banyak tertahan di stok" padahal stok hanya 1,2 jt dan penyebabnya utang lancar besar. **Saran:** bila persediaan < ±30% aset lancar, pakai saran versi utang lancar/kas.

### Ringan
5. Tebakan jenis usaha memakai substring dengan urutan dagang dulu: "jasa fotokopi" → **dagang** ("toko" di dalam "fotokopi"), "jasa katering" → jasa (SKILL.md: katering = produksi), "warung kopi"/"toko kue" → dagang (SKILL.md: kuliner/kue = produksi). **Saran:** cocokkan kata utuh, dahulukan alias yang lebih spesifik (katering, kue, kopi, makan), dan SKILL.md meminta agent mengirim `--jenis dagang|jasa|manufaktur` yang sudah dipetakan.
6. `--bagian-lancar-utang-bank` lebih besar dari utang bank dipotong diam-diam (999 jt → 11 jt). Beri peringatan.
7. Status **SEMENTARA** juga dipicu peringatan informatif "periode pendek < 3 bulan", sehingga laporan bulanan dari EMKM selalu "SEMENTARA" walau datanya lengkap. Pisahkan peringatan data dari peringatan informatif.
8. Ringkasan "Paling mendesak" diurutkan menurut urutan kelompok, bukan keparahan. Pada modal negatif (E2), ringkasan menyebut rasio lancar/cepat/kas, bukan "modal habis". Ringkasan juga tidak memuat satu kalimat tren (mis. "laba turun 21,4%").
9. `minus 2jt` tidak dikenali (hanya diberi peringatan). Pertimbangkan menerima kata "minus"/"rugi".
10. Kutipan Kasmir hanya dicek lewat jurnal pengutip (sudah diakui di references). Bila memungkinkan, cantumkan halaman/edisi buku.

## 7. Yang sudah bagus
- Semua perhitungan Decimal. Pembulatan hanya di tampilan (rasio 2 desimal, %/hari 1 desimal, rupiah bulat). 107/107 cocok.
- Pembagi nol, modal ≤ 0, laba negatif, dan pos mustahil ditangani jujur. Dua pesaing publik gagal di kasus yang sama.
- Ambang per jenis UMKM masuk akal dan bersumber. Warung tidak dicap bahaya karena stok.
- Input Indonesia sangat luwes (Rp, jt, rb, M, kurung, minus di belakang, tabel Markdown/TAB/`;`, EMKM JSON).
- Kesiapan KUR konsisten dengan `pengajuan-kur` (≤ 30/50/100%) dan tidak pernah menjanjikan persetujuan.

## 8. Rekomendasi katalog (untuk kurator; katalog TIDAK diubah penguji)
- `skor_kualitas`: 8 · `status`: `lulus` · `platform_teruji`: `claude-code (simulasi agent)`.

---
## Lampiran A — Tabel verifikasi lengkap (keluaran `verif.py`)

### S1 warung 2024
| Rasio | Verifikasi (Decimal, 4 desimal) | Script | Cocok |
|---|---:|---:|---|
| rasio_lancar | 2.6471 | 2.6471 | cocok |
| rasio_cepat | 0.5882 | 0.5882 | cocok |
| rasio_kas | 0.4706 | 0.4706 | cocok |
| modal_kerja | 28000000 | 28000000 | cocok |
| margin_kotor | 15.0000 | 15 | cocok |
| margin_bersih | 4.0000 | 4 | cocok |
| roa | 22.1538 | 22.1538 | cocok |
| roe | 30.0000 | 30 | cocok |
| der | 0.3542 | 0.3542 | cocok |
| dar | 26.1538 | 26.1538 | cocok |
| perputaran_persediaan | 8.7429 | 8.7429 | cocok |
| hari_persediaan | 41.7484 | 41.7484 | cocok |
| perputaran_piutang | 180.0000 | 180 | cocok |
| hari_piutang | 2.0278 | 2.0278 | cocok |
| hari_utang | 17.8922 | 17.8922 | cocok |
| siklus_kas | 25.8840 | 25.884 | cocok |
| perputaran_aset | 5.5385 | 5.5385 | cocok |

### S1 warung 2025
| Rasio | Verifikasi (Decimal, 4 desimal) | Script | Cocok |
|---|---:|---:|---|
| rasio_lancar | 2.0241 | 2.0241 | cocok |
| rasio_cepat | 0.3690 | 0.369 | cocok |
| rasio_kas | 0.2241 | 0.2241 | cocok |
| modal_kerja | 29700000 | 29700000 | cocok |
| margin_kotor | 14.0000 | 14 | cocok |
| margin_bersih | 4.0000 | 4 | cocok |
| roa | 23.7121 | 23.7121 | cocok |
| roe | 35.1097 | 35.1097 | cocok |
| der | 0.6080 | 0.608 | cocok |
| dar | 37.8096 | 37.8096 | cocok |
| perputaran_persediaan | 8.7036 | 8.7036 | cocok |
| hari_persediaan | 41.9366 | 41.9366 | cocok |
| perputaran_piutang | 135.4839 | 135.4839 | cocok |
| hari_piutang | 2.6940 | 2.694 | cocok |
| hari_utang | 26.2735 | 26.2735 | cocok |
| siklus_kas | 18.3571 | 18.3571 | cocok |
| perputaran_aset | 5.9280 | 5.928 | cocok |
| rasio cicilan % | 53.6 | 53.6 | cocok |

### S2 laundry
| Rasio | Verifikasi (Decimal, 4 desimal) | Script | Cocok |
|---|---:|---:|---|
| rasio_lancar | 0.4188 | 0.4188 | cocok |
| rasio_cepat | 0.3675 | 0.3675 | cocok |
| rasio_kas | 0.2350 | 0.235 | cocok |
| modal_kerja | -13600000 | -13600000 | cocok |
| margin_kotor | 77.9570 | 77.957 | cocok |
| margin_bersih | 10.3226 | 10.3226 | cocok |
| margin_usaha | 14.1935 | 14.1935 | cocok |
| roa | 15.0235 | 15.0235 | cocok |
| roe | 47.5248 | 47.5248 | cocok |
| der | 2.1634 | 2.1634 | cocok |
| dar | 68.3881 | 68.3881 | cocok |
| cakupan_bunga | 3.6667 | 3.6667 | cocok |
| perputaran_persediaan | 34.1667 | 34.1667 | cocok |
| hari_persediaan | 10.6829 | 10.6829 | cocok |
| perputaran_piutang | 60.0000 | 60 | cocok |
| hari_piutang | 6.0833 | 6.0833 | cocok |
| hari_utang | 21.3659 | 21.3659 | cocok |
| siklus_kas | -4.5996 | -4.5997 | cocok |
| perputaran_aset | 1.4554 | 1.4554 | cocok |
| rasio cicilan % | 146.9 | 146.9 | cocok |

### S3 konveksi Sem-1
| Rasio | Verifikasi (Decimal, 4 desimal) | Script | Cocok |
|---|---:|---:|---|
| rasio_lancar | 3.0889 | 3.0889 | cocok |
| rasio_cepat | 1.5333 | 1.5333 | cocok |
| rasio_kas | 0.2000 | 0.2 | cocok |
| modal_kerja | 94000000 | 94000000 | cocok |
| margin_kotor | 30.0000 | 30 | cocok |
| margin_bersih | 7.0000 | 7 | cocok |
| roa | 21.1055 | 21.1055 | cocok |
| roe | 33.8710 | 33.871 | cocok |
| der | 0.6048 | 0.6048 | cocok |
| dar | 37.6884 | 37.6884 | cocok |
| cakupan_bunga | 15.0000 | 15 | cocok |
| perputaran_persediaan | 3.0000 | 3 | cocok |
| hari_persediaan | 60.8333 | 60.8333 | cocok |
| perputaran_piutang | 3.0000 | 3 | cocok |
| hari_piutang | 60.8333 | 60.8333 | cocok |
| hari_utang | 30.4167 | 30.4167 | cocok |
| siklus_kas | 91.2500 | 91.2499 | cocok |
| perputaran_aset | 3.0151 | 3.0151 | cocok |

### S3 konveksi Sem-2
| Rasio | Verifikasi (Decimal, 4 desimal) | Script | Cocok |
|---|---:|---:|---|
| rasio_lancar | 2.6053 | 2.6053 | cocok |
| rasio_cepat | 1.3158 | 1.3158 | cocok |
| rasio_kas | 0.0658 | 0.0658 | cocok |
| modal_kerja | 122000000 | 122000000 | cocok |
| margin_kotor | 28.0000 | 28 | cocok |
| margin_bersih | 5.0000 | 5 | cocok |
| roa | 14.5374 | 14.5374 | cocok |
| roe | 25.0951 | 25.0951 | cocok |
| der | 0.8345 | 0.8345 | cocok |
| dar | 45.4902 | 45.4902 | cocok |
| cakupan_bunga | 8.8571 | 8.8571 | cocok |
| perputaran_persediaan | 2.8286 | 2.8286 | cocok |
| hari_persediaan | 64.5202 | 64.5202 | cocok |
| perputaran_piutang | 2.9806 | 2.9806 | cocok |
| hari_piutang | 61.2284 | 61.2284 | cocok |
| hari_utang | 39.9411 | 39.9411 | cocok |
| siklus_kas | 85.8075 | 85.8075 | cocok |
| perputaran_aset | 2.9075 | 2.9075 | cocok |
| rasio cicilan % | 65.5 | 65.5 | cocok |

### E2 modal negatif
| Rasio | Verifikasi (Decimal, 4 desimal) | Script | Cocok |
|---|---:|---:|---|
| rasio_lancar | 0.7222 | 0.7222 | cocok |
| rasio_cepat | 0.1667 | 0.1667 | cocok |
| rasio_kas | 0.0556 | 0.0556 | cocok |
| modal_kerja | -5000000 | -5000000 | cocok |
| margin_kotor | 16.6667 | 16.6667 | cocok |
| margin_bersih | -5.0000 | -5 | cocok |
| roa | -33.3333 | -33.3333 | cocok |
| dar | 211.1111 | 211.1111 | cocok |
| perputaran_persediaan | 10.0000 | 10 | cocok |
| hari_persediaan | 36.5000 | 36.5 | cocok |
| perputaran_piutang | 60.0000 | 60 | cocok |
| hari_piutang | 6.0833 | 6.0833 | cocok |
| hari_utang | 54.7500 | 54.75 | cocok |
| siklus_kas | -12.1667 | -12.1667 | cocok |
| perputaran_aset | 6.6667 | 6.6667 | cocok |

TOTAL: 107/107 cocok

---
## Uji ulang independen v1.0.1 (Akun B, 2026-09-26)
- **Penguji:** agent Akun B, bukan pembuat skill dan bukan penguji v1.0.0. Hanya membaca folder skill. Salinan di scratchpad (bukan `.claude/skills/`). Rincian lengkap: `examples/08-uji-ulang-v101-akun-b.md`.
- **Tes bawaan:** `tests/uji_regresi.py` → **71 uji, 0 gagal, SEMUA UJI LULUS**.
- **Validator:** `python3 scripts/validate.py --skill analisis-rasio-keuangan-usaha` → **✅ 1 skill valid, 89 baris katalog sesuai**.
- **uji_openclaw.sh:** tidak dijalankan (sesuai instruksi tugas).
- **Verifikasi Decimal independen** (`verif.py` tanpa impor `rasio.py`): warung, konveksi, dan skenario baru bengkel motor 2 tahun, mencakup tren saldo akhir, tabel utama rata-rata, dan rasio cicilan → **164/165 cocok**. Satu selisih 0,0001 hari (siklus kas dijumlah dari komponen 4 desimal), tampilan sama.

### Status temuan v1.0.0
| # | Temuan v1.0.0 | Status v1.0.1 | Bukti |
|---|---|---|---|
| 1 | Tren beda basis | ✔ Diperbaiki | Basis "saldo AKHIR" ditulis di output & JSON `basis_tren`. Warung ROA 22,2% → 21,9% **memburuk**; konveksi lama piutang 60,8 → **75,1 hari**, umur stok 75,3 hari. Tabel utama tetap rata-rata (ROA 23,71%, piutang 61,2 hari) |
| 2 | `Kas,1,250,000` → Rp 1 | ✔ Diperbaiki | GALAT kode 2 + tiga cara perbaikan. Kolom berlebih pada `;` juga ditolak. Titik ribuan, spasi, "Rp", kurung negatif, koma dikutip, TAB+koma: benar |
| 3 | Data minim → "pertahankan" | ✔ Diperbaiki | Status **DATA BELUM CUKUP** + daftar pos kosong di ringkasan, KUR, saran & asumsi |
| 4 | Saran rasio cepat tak kontekstual | ✔ Diperbaiki | Laundry: "stok bukan penyebabnya … fokus ke utang & kas". Toko bangunan stok 160 hari: saran versi stok |
| 5, 7 | Tebak jenis substring; periode pendek → SEMENTARA | ✔ Diperbaiki | Uji G15, G14; "bengkel motor" → jasa |
| 8 | Ringkasan tanpa kalimat tren | ⏳ Belum | — |

### Temuan baru
**Sedang**
1. **CSV koma, sel pecah tepat sejumlah kolom judul** (`Kas,250,000` di tabel 2 periode) → kas 2024 = Rp 250, 2025 = Rp 0. Bila modal tidak diisi (modal dihitung sehingga neraca selalu seimbang): status LENGKAP **tanpa peringatan**, dan "Rasio kas 0,00x" jadi masalah paling mendesak. Bila modal diisi, kesalahan tertangkap lewat "neraca tidak seimbang". Kasus tepi, tetapi tetap angka salah diam-diam. **Saran:** pada tabel berpemisah koma, beri peringatan untuk sel 3 digit yang mengikuti sel 1–3 digit, atau sel angka < 1.000 di tabel yang angka lainnya jutaan.
2. **Modal dihitung dari pos yang di-nol-kan** (`--penjualan 240jt --hpp 200jt --kas 5jt --utang-usaha 8jt`, tanpa stok/aset) → modal −3 jt, "Modal habis/negatif", KUR ✗, status LENGKAP. Asumsi mencatatnya dan SKILL.md menyuruh agent bertanya dulu, jadi risiko hanya muncul pada mode "langsung saja". **Saran:** bila modal dihitung dan stok/aset tetap kosong → SEMENTARA + saran "lengkapi data", bukan "modal habis".

**Ringan**
3. Baris dengan sel kurang (HPP hanya 1 dari 2 periode) tidak dicatat di "Perlu dicek". Rasio terkait memang "tidak dihitung", jadi tidak ada angka salah.
4. Label tren netral untuk siklus kas ("naik") dan margin usaha ("turun"), padahal arahnya jelas memburuk.
5. Selisih neraca Rp 0,50 ditampilkan "Rp 1" dan membuat SEMENTARA.
6. Data minim: judul bagian kosong tetap tercetak. Saran bisa 6 butir ("Lainnya") sementara SKILL.md menulis "maks. 5".

### Skor v1.0.1
| Kriteria | Skor | Catatan |
|---|---:|---|
| Kualitas output | 9 | Tren jujur & basis tertulis, saran kontekstual |
| Akurasi angka | 9 | 164/165 Decimal. Minus: kasus tepi CSV b14 |
| Penanganan input kurang | 8 | DATA BELUM CUKUP benar. Minus: modal turunan dari pos nol |
| Penanganan luar cakupan, keamanan | 10 | Tidak berubah dari v1.0.0 (tanpa jaringan/subprocess) |
| **SKOR AKHIR** | **9** | Naik dari 8. Keempat temuan sedang v1.0.0 tertutup; dua temuan sedang baru bersifat tepi dan tercakup langkah bertanya di SKILL.md |

**Status: LULUS** (≥ 7). Rekomendasi untuk kurator (katalog tidak diubah penguji): `skor_kualitas` 9, status `lulus`, `platform_teruji` tetap `claude-code (simulasi agent)`. Perbaiki temuan baru #1–#2 sebelum `beta` bila memungkinkan.

---
## Uji ulang v1.0.5 (2026-10-13, penguji independen, OpenClaw sebelum/sesudah)
- OpenClaw 2026.10.2 lokal dengan skenario rapat komisaris yang sama (neraca + laba rugi 2025, pesan identik). SEBELUM tanpa skill, SESUDAH hanya skill ini. Rincian ada di `00-openclaw-sebelum-sesudah.md`.
- Skor tanpa skill **7** → dengan skill **9** (selisih +2,0), jadi **LULUS** acuan (sesudah ≥ 8 dan selisih ≥ 1,5).
- Angka di kedua sisi cocok dengan hitung ulang Python (Decimal) penguji. Pembeda: hanya sisi dengan skill yang membandingkan kas Rp420 jt dengan utang bank jatuh tempo Rp900 jt (risiko likuiditas SEDANG).
- Perbaikan v1.0.5 terbukti: jenis dan skala usaha ditulis dengan label "Asumsi:". Sisa temuan ringan: ambang piutang di ringkasan (≤30–45 hari) berbeda dari tabel (≤30 hari), dan disclaimer menyebut "referensi internal".
