# Uji 08 (Akun B) — Uji ulang independen v1.0.1

> Penguji independen Akun B, 2026-09-26. Bukan pembuat skill dan bukan penguji v1.0.0. Hanya membaca folder skill. Folder kerja: salinan skill di scratchpad sesi (bukan `.claude/skills/`). `rasio.py` versi_script **1.0.1** dijalankan apa adanya. Verifikasi angka memakai `verif.py` buatan penguji: rumus buku teks, Decimal 40 digit, **tidak mengimpor `rasio.py`**, dibandingkan dengan `nilai` JSON script (4 desimal, toleransi 0,00006).

Fokus: temuan sedang v1.0.0 (tren beda basis; CSV `Kas,1,250,000` terbaca Rp 1; data minim tetap "pertahankan"; saran rasio cepat tidak kontekstual) + 1 skenario regresi baru.

## Ringkasan hasil
| Bagian | Hasil |
|---|---|
| (a) Tren basis sama & tertulis | ✔ Diperbaiki. Warung: ROA 22,2% → 21,9% **memburuk**. Konveksi: lama piutang 60,8 → **75,1 hari**. Basis ditulis di output teks & JSON (`basis_tren`) |
| (b) Format CSV | ✔ 12 dari 14 kasus benar/ditolak jelas. ✘ 1 kasus tepi masih salah diam-diam (b14), 1 kasus sel kosong tidak diberi catatan (b7) |
| (c) Data minim | ✔ "DATA BELUM CUKUP" + daftar pos kosong di ringkasan, KUR, saran & asumsi. ⚠ Varian data sebagian (c2) menyimpulkan "modal habis" dari pos yang di-nol-kan, status LENGKAP |
| (d) Saran kontekstual | ✔ Laundry: saran rasio cepat versi utang/kas ("stok bukan penyebabnya"). Toko bangunan stok 160 hari: saran versi stok + umur stok |
| (e) Regresi bengkel motor 2 tahun | ✔ 57/57 nilai cocok + rasio cicilan cocok |
| Verifikasi Decimal total | **164/165 cocok**; 1 selisih 0,0001 hari (pembulatan, lihat catatan) |
| Tes bawaan `tests/uji_regresi.py` | **71 uji, 0 gagal, SEMUA UJI LULUS** (v1.0.0: 56) |
| `python3 scripts/validate.py --skill analisis-rasio-keuangan-usaha` | **✅ 1 skill valid, 89 baris katalog sesuai** |
| `uji_openclaw.sh` | Tidak dijalankan (sesuai instruksi tugas) |

---
## (a) Tren antarperiode — basis sama & tertulis

### Warung sembako (data sama dengan uji 03)
Perintah: `python3 scripts/rasio.py s1.csv --jenis dagang --nama-usaha "Warung Bu Tini" --cicilan-bulanan 750rb` → kode keluar 0.

Output memuat catatan basis di atas tabel tren:
> _Tren memakai basis SAMA untuk semua periode: saldo AKHIR tiap periode (persediaan, piutang, aset, modal). Tabel rasio periode terakhir di atas memakai rata-rata saldo awal-akhir bila tersedia, jadi angkanya bisa sedikit berbeda dari kolom terakhir tabel tren._

| Rasio (tren, saldo akhir) | 2024 | 2025 | Arah script | Hitung penguji (Decimal) | v1.0.0 |
|---|---|---|---|---|---|
| ROA | 22,2% | 21,9% | **memburuk (turun)** | 14,4/65 = 22,1538% → 16,8/76,7 = 21,9035% | 22,2% → 23,7% "membaik" (salah basis) |
| Umur stok | 41,7 hari | 48,5 hari | memburuk (naik) | 35/306×365 = 41,7484 → 48/361,2×365 = 48,5050 | 41,7 → 41,9 |
| ROE | 30,0% | 35,2% | membaik (naik) | 14,4/48 = 30,0000 → 16,8/47,7 = 35,2201 | 30,0 → 35,1 |
| Lama piutang | 2,0 hari | 3,7 hari | memburuk (naik) | 2,0278 → 3,6500 | 2,0 → 2,7 |

Tabel utama 2025 tetap memakai rata-rata saldo (ROA 23,71% = 16,8 ÷ ((65+76,7)/2)), dan rumusnya menyebut "rata-rata total aset". Keduanya cocok dengan hitungan penguji. Kesimpulan: **ROA memburuk, sesuai harapan.** ✔

### Konveksi (data sama dengan uji 05, 2 semester, penjualan tempo)
| Rasio (tren, saldo akhir) | Sem-1 | Sem-2 | Arah | Hitung penguji |
|---|---|---|---|---|
| Lama piutang tertagih | 60,8 hari | **75,1 hari** | memburuk (naik) | 95 × 182,5 ÷ 231 = 75,0541 |
| Umur stok | 60,8 hari | 75,3 hari | memburuk (naik) | 98 × 182,5 ÷ 237,6 = 75,2736 |
| ROA disetahunkan | 21,1% | 12,9% | memburuk (turun) | 16,5/255×2 = 12,9412% |
| Siklus kas | 91,2 hari | 110,4 hari | "naik" | 75,2736 + 75,0541 − 39,9411 = 110,3866 |

Tabel utama Sem-2 (rata-rata): lama piutang 61,2 hari (= 77,5 × 182,5 ÷ 231 = 61,2284) ✔. Ringkasan "Paling mendesak … Lama piutang tertagih 61,2 hari" memakai tabel utama, sesuai aturan SKILL.md ("jangan membandingkan angka tabel utama dengan kolom tren"). ✔

---
## (b) CSV dengan berbagai format angka
Semua file tabel 1 kolom pos + 1–2 periode, `--jenis dagang --format json`, lalu dicek nilai `data` yang terbaca.

| # | Kasus | Hasil script | Penilaian |
|---|---|---|---|
| b1 | Koma pemisah kolom, `Kas,1,250,000` tanpa kutip | Kode 2, `GALAT: … memakai koma sebagai pemisah kolom, tetapi angkanya juga memakai koma … (baris 5: Kas \| 1 \| 250 \| 000). Angka TIDAK ditebak. Perbaiki: (a) Kas;1.250.000, (b) Kas,"1,250,000", (c) Kas,1250000` | ✔ (v1.0.0: Rp 1 diam-diam) |
| b2 | Koma dikutip `"1,250,000"` | kas 1.250.000, LENGKAP | ✔ |
| b3 | Titik ribuan `1.250.000` dengan `;` | kas 1.250.000 | ✔ |
| b4 | Spasi di sekitar sel, `Rp 1.250.000 `, `Rp12.000.000`, `Rp  80.000.000`, `Rp 3 000 000` | semua benar | ✔ |
| b5 | Kurung negatif `(6.000.000)` laba, `(2.000.000)` modal | −6 jt, −2 jt; neraca tak seimbang dilaporkan, SEMENTARA | ✔ |
| b6 | Kolom berlebih (`HPP;80.000.000;99` pada tabel 1 periode) | Kode 2, `GALAT: … kolom lebih banyak dari judulnya … Angka TIDAK ditebak` | ✔ |
| b7 | Kolom kurang (`HPP;70.000.000` pada tabel 2 periode) | HPP 2025 = kosong → margin kotor & umur stok 2025 "Tidak dihitung: data belum ada: HPP". Status **LENGKAP**, tanpa catatan "baris HPP hanya 1 dari 2 periode" | ⚠ ringan (tidak ada angka salah) |
| b8 | Koma tanpa kutip di tabel 2 periode (`Kas,1,250,000`) | Kode 2, GALAT sama dengan b1 | ✔ |
| b9 | `Kas;1,250,000` di tabel `;` | 1.250.000 | ✔ |
| b10 | `Kas;1.250` (maksud mungkin 1,25 jt) | dibaca Rp 1.250 (benar menurut format Indonesia); neraca tak seimbang −Rp 1.248.750 dilaporkan, SEMENTARA | ✔ (tertangkap lewat neraca) |
| b11 | Tab + koma ribuan tanpa kutip | benar semua (koma bukan pemisah kolom) | ✔ |
| b12 | Desimal `1.250.000,50` | 1.250.000,5; neraca "selisih Rp 1" → SEMENTARA | ✔ (catatan: selisih sebenarnya Rp 0,50 ditampilkan "Rp 1") |
| b13 | Koma, 2 periode, `Kas,250,000` (sel pecah **pas** 3 kolom), ada baris Modal | 2024 kas = Rp 250, 2025 kas = Rp 0. Tertangkap tidak langsung: neraca tak seimbang → SEMENTARA | ⚠ |
| b14 | Sama dengan b13 tetapi **tanpa baris Modal** | kas 2024 = Rp 250, 2025 = Rp 0; modal dihitung = aset − utang, jadi neraca selalu seimbang. Status **LENGKAP**, tanpa peringatan. Ringkasan: "Paling mendesak: Rasio kas 0,00x", saran #1 dana cadangan | ✘ **angka salah diam-diam** (kasus tepi) |

**Catatan b14:** Terjadi hanya bila pemisah kolom = koma, jumlah sel setelah pecah **tepat sama** dengan jumlah kolom judul, dan modal tidak diisi. Jarang, tetapi mungkin terjadi pada tabel 2 periode dengan satu nilai di bawah Rp 1 juta (mis. `Kas,250,000` atau `Utang lain,750,000`). Saran: pada tabel berpemisah koma, beri peringatan bila sebuah sel berisi tepat 3 digit (`000`, `250`) dan sel sebelumnya 1–3 digit, atau bila ada sel angka < 1.000 di tabel yang angka lainnya jutaan.

---
## (c) Data minim
**c1** `--penjualan "20 juta" --laba-bersih 3jt --bulan 1` (sama dengan uji 06):
- Status: **DATA BELUM CUKUP** (v1.0.0: LENGKAP).
- Ringkasan: "… Dari 1 rasio yang dinilai … DATA BELUM CUKUP untuk menyimpulkan kondisi usaha. Yang belum ada: HPP, Kas & bank, Persediaan / stok, Total aset, Total utang lancar, Total utang, Modal." Tidak ada kata "pertahankan". ✔
- KUR: "DATA BELUM CUKUP untuk menilai kesiapan — lengkapi: …" ✔
- Saran: satu butir "Lengkapi data — Baru 1 rasio yang bisa dinilai …" ✔
- Asumsi: "Pos tidak diisi (rasio yang memakainya tidak dihitung): …" (v1.0.0: "Tidak ada — semua angka diisi"). ✔
- Kosmetik: judul bagian Likuiditas/Solvabilitas/Aktivitas tetap tercetak walau tabelnya kosong (ringan).

**c2 (varian penguji)** data sebagian: `--jenis dagang --penjualan 240jt --hpp 200jt --laba-bersih 12jt --kas 5jt --utang-usaha 8jt` (piutang, stok, aset tetap, modal tidak disebut):
- Pos kosong di-nol-kan sesuai SKILL.md ("Pos rincian yang kosong = Rp 0, ditulis di Asumsi"), lalu modal dihitung = 5 − 8 = **−Rp 3.000.000**.
- Status **LENGKAP**, 9 rasio dinilai, 4 bahaya. Saran #1 "**Modal habis/negatif** … pertimbangkan konsultasi ke pendamping UMKM", KUR "BELUM SIAP ✗ Modal sendiri −Rp 3.000.000 habis/negatif".
- Asumsi mencantumkan semua pos yang dianggap Rp 0 dan "Modal dihitung = −Rp 3.000.000", jadi tidak sepenuhnya diam-diam. Namun untuk toko dengan HPP 200 jt, stok & aset Rp 0 hampir pasti data belum diisi, bukan kondisi nyata. Kesimpulan "modal habis" dari angka turunan tersebut berisiko menakutkan pemilik.
- Mitigasi di SKILL.md: agent wajib bertanya dulu bila kas/piutang/persediaan/aset tetap kosong (tabel Input). Jadi risiko hanya muncul bila agent melewati langkah bertanya atau pengguna meminta "langsung saja".
- Saran: bila modal **dihitung** (bukan diisi) dan persediaan/aset tetap tidak diisi, jadikan status SEMENTARA dan ganti saran "Modal habis" dengan "Modal dihitung dari data belum lengkap — lengkapi stok & aset dulu".

---
## (d) Saran kontekstual
**d1 Laundry** (data uji 04: stok 1,2 jt dari aset lancar 9,8 jt = 12%; utang lancar 23,4 jt):
> 3. **Rasio cepat (quick ratio)** — Kas + piutang tidak cukup menutup utang jangka pendek, dan stok bukan penyebabnya (stok kecil). Fokus ke utang & kas: minta tenor cicilan/tempo pemasok lebih panjang, tagih piutang, tahan prive & pembelian alat, dan sisihkan dana cadangan dari penjualan harian.

✔ (v1.0.0: "Aset lancar terlalu banyak tertahan di stok").

**d2 Toko bangunan, stok besar & lambat** (penjualan 600 jt, HPP 480 jt, stok 210 jt, kas 6 jt, piutang 10 jt, utang lancar 130 jt):
- Rasio cepat 0,12x 🔴, rasio kas 0,05x 🔴, umur stok 159,7 hari 🔴 (210 × 365 ÷ 480 = 159,6875 ✔).
- Saran #1 rasio cepat: "Aset lancar terlalu banyak tertahan di stok. Kurangi belanja stok yang lambat laku, jual/promo barang lama …" dan #3 umur stok (buku-stok, stop belanja barang tidak laku 30 hari). ✔ Versi stok dipakai karena stok = 93% aset lancar.

---
## (e) Skenario regresi baru — Bengkel motor 2 tahun (buatan penguji)
**Permintaan (simulasi):** "Bengkel motor saya (servis + jual sparepart, ada langganan ojek yang bayar tempo). Ini angka 2024 dan 2025. Mau ambil KUR, cicilan 2,5 juta sebulan. Membaik atau memburuk?"

**Data (`s5-bengkel.csv`, `;`, format campuran Rp/titik/jt):**
```
Pos;2024;2025
Pendapatan usaha;Rp 540.000.000;612jt
Penjualan tempo;60.000.000;96jt
HPP;297.000.000;348,8jt
Laba usaha;63.000.000;61,2jt
Beban bunga;6.000.000;8,4jt
Beban pajak;2.700.000;3,06jt
Laba bersih;54.300.000;49,74jt
Kas;18.000.000;11jt
Piutang;7.500.000;19jt
Persediaan;45.000.000;72jt
Aset tetap;85.000.000;110jt
Utang usaha;22.000.000;41jt
Utang lancar lain;12.000.000;18jt
Utang jangka panjang;36.000.000;60jt
Modal;85.500.000;93jt
Bulan;12;12
```
Neraca seimbang (2024: 155,5 = 70 + 85,5; 2025: 212 = 119 + 93). Laba bersih = laba usaha − bunga − pajak di kedua tahun.

**Perintah:** `python3 scripts/rasio.py s5-bengkel.csv --jenis "bengkel motor" --nama-usaha "Bengkel Jaya Motor" --cicilan-bulanan 2,5jt` → kode 0, jenis "bengkel motor" → **Jasa**, status LENGKAP.

**Inti output script:**
- Ringkasan: "Pada 2025, usaha UNTUNG Rp 49.740.000 (8,1% dari penjualan). Dari 11 rasio … usaha jasa: 5 baik, 5 waspada, 1 bahaya. Paling mendesak: Rasio cepat 0,51x."
- Tren (saldo akhir): rasio lancar 2,07x → 1,73x, rasio kas 0,53x → 0,19x, ROA 34,9% → 23,5%, DER 0,82x → 1,28x, cakupan bunga 10,50x → 7,29x, umur stok 55,3 → 75,3 hari, lama piutang 45,6 → 72,2 hari, penjualan +13,3%, laba −8,4%. Semua rasio yang punya ambang berlabel "memburuk"; penjualan "membaik"; perputaran, lama bayar pemasok, siklus kas & margin usaha berlabel netral (naik/turun).
- KUR: **BELUM SIAP** — "✗ Cicilan Rp 2.500.000/bulan = 60,3% dari laba bersih per bulan Rp 4.145.000 → 🔴 TERLALU BERAT", ⚠ DER 1,28x.
- Saran: 1 rencana cicilan (kecilkan plafon/tenor lebih panjang, rujuk pengajuan-kur) · 2 rasio cepat versi stok (stok 72 jt = 71% aset lancar, kontekstual ✔) · 3 kas · 4 margin bersih · 5 DER · 6 "Lainnya".
- Umur stok untuk jenis jasa ditampilkan sebagai ⚪ Info (tanpa ambang), sesuai references.

**Verifikasi Decimal (57 nilai + cicilan):** `tren[0]` = 2024 saldo akhir, `tren[1]` = 2025 saldo akhir, `utama` = tabel 2025 dengan rata-rata saldo (aset (155,5+212)/2, modal (85,5+93)/2, stok (45+72)/2, piutang (7,5+19)/2).

| Nilai | Penguji (Decimal) | Script | Cocok |
|---|---:|---:|---|
| tren[0] rasio_lancar | 2.0735 | 2.0735 | cocok |
| tren[1] rasio_lancar | 1.7288 | 1.7288 | cocok |
| tren[0] rasio_cepat | 0.7500 | 0.75 | cocok |
| tren[1] rasio_cepat | 0.5085 | 0.5085 | cocok |
| tren[0] rasio_kas | 0.5294 | 0.5294 | cocok |
| tren[1] rasio_kas | 0.1864 | 0.1864 | cocok |
| tren[0] modal_kerja | 36500000.0000 | 36500000 | cocok |
| tren[1] modal_kerja | 43000000.0000 | 43000000 | cocok |
| tren[0] margin_kotor | 45.0000 | 45 | cocok |
| tren[1] margin_kotor | 43.0065 | 43.0065 | cocok |
| tren[0] margin_usaha | 11.6667 | 11.6667 | cocok |
| tren[1] margin_usaha | 10.0000 | 10 | cocok |
| tren[0] margin_bersih | 10.0556 | 10.0556 | cocok |
| tren[1] margin_bersih | 8.1275 | 8.1275 | cocok |
| tren[0] roa | 34.9196 | 34.9196 | cocok |
| tren[1] roa | 23.4623 | 23.4623 | cocok |
| tren[0] roe | 63.5088 | 63.5088 | cocok |
| tren[1] roe | 53.4839 | 53.4839 | cocok |
| tren[0] der | 0.8187 | 0.8187 | cocok |
| tren[1] der | 1.2796 | 1.2796 | cocok |
| tren[0] dar | 45.0161 | 45.0161 | cocok |
| tren[1] dar | 56.1321 | 56.1321 | cocok |
| tren[0] cakupan_bunga | 10.5000 | 10.5 | cocok |
| tren[1] cakupan_bunga | 7.2857 | 7.2857 | cocok |
| tren[0] perputaran_persediaan | 6.6000 | 6.6 | cocok |
| tren[1] perputaran_persediaan | 4.8444 | 4.8444 | cocok |
| tren[0] hari_persediaan | 55.3030 | 55.303 | cocok |
| tren[1] hari_persediaan | 75.3440 | 75.344 | cocok |
| tren[0] perputaran_piutang | 8.0000 | 8 | cocok |
| tren[1] perputaran_piutang | 5.0526 | 5.0526 | cocok |
| tren[0] hari_piutang | 45.6250 | 45.625 | cocok |
| tren[1] hari_piutang | 72.2396 | 72.2396 | cocok |
| tren[0] hari_utang | 27.0370 | 27.037 | cocok |
| tren[1] hari_utang | 42.9042 | 42.9042 | cocok |
| tren[0] siklus_kas | 73.8910 | 73.891 | cocok |
| tren[1] siklus_kas | 104.6794 | 104.6794 | cocok |
| tren[0] perputaran_aset | 3.4727 | 3.4727 | cocok |
| tren[1] perputaran_aset | 2.8868 | 2.8868 | cocok |
| utama rasio_lancar | 1.7288 | 1.7288 | cocok |
| utama rasio_cepat | 0.5085 | 0.5085 | cocok |
| utama rasio_kas | 0.1864 | 0.1864 | cocok |
| utama modal_kerja | 43000000.0000 | 43000000 | cocok |
| utama margin_kotor | 43.0065 | 43.0065 | cocok |
| utama margin_bersih | 8.1275 | 8.1275 | cocok |
| utama margin_usaha | 10.0000 | 10 | cocok |
| utama roa | 27.0694 | 27.0694 | cocok |
| utama roe | 55.7311 | 55.7311 | cocok |
| utama der | 1.2796 | 1.2796 | cocok |
| utama dar | 56.1321 | 56.1321 | cocok |
| utama cakupan_bunga | 7.2857 | 7.2857 | cocok |
| utama perputaran_persediaan | 5.9624 | 5.9624 | cocok |
| utama hari_persediaan | 61.2170 | 61.217 | cocok |
| utama perputaran_piutang | 7.2453 | 7.2453 | cocok |
| utama hari_piutang | 50.3776 | 50.3776 | cocok |
| utama hari_utang | 42.9042 | 42.9042 | cocok |
| utama siklus_kas | 68.6904 | 68.6904 | cocok |
| utama perputaran_aset | 3.3306 | 3.3306 | cocok |
| rasio cicilan % | 2.500.000 ÷ (49.740.000 ÷ 12) = 60,3136 → 60,3 | 60,3 | cocok |

---
## Verifikasi Decimal total
| Kasus | Nilai dicek | Cocok |
|---|---:|---:|
| Warung (tren 2024 & 2025 saldo akhir + tabel utama 2025 rata-rata + cicilan 53,6%) | 52 | 52 |
| Konveksi (tren Sem-1 & Sem-2 + tabel utama Sem-2 + cicilan 65,5%) | 55 | 54 |
| Bengkel (tren 2024 & 2025 + tabel utama 2025 + cicilan 60,3%) | 58 | 58 |
| **Total** | **165** | **164** |

Satu selisih: konveksi tren Sem-1 siklus kas, penguji 91,2500 vs script 91,2499 (script menjumlah komponen yang sudah dibulatkan 4 desimal: 60,8333 + 60,8333 − 30,4167). Selisih 0,0001 hari, tampilan sama (91,2 hari). Diabaikan (sama dengan temuan v1.0.0 yang ditandai "cocok" pada toleransi 0,0001).

## Temuan baru / tersisa
| # | Tingkat | Temuan | Saran |
|---|---|---|---|
| 1 | Sedang (tepi) | b14: CSV koma, sel pecah tepat sejumlah kolom judul (`Kas,250,000` di tabel 2 periode) + modal tidak diisi → kas salah (Rp 250 / Rp 0) tanpa peringatan, status LENGKAP | Deteksi pola sel 3 digit setelah sel 1–3 digit pada tabel berpemisah koma; minta kutip/`;` |
| 2 | Sedang | c2: modal **dihitung** dari pos yang di-nol-kan → "Modal habis/negatif", KUR ✗, status LENGKAP | Bila modal dihitung dan stok/aset tetap tidak diisi → SEMENTARA + saran "lengkapi data" |
| 3 | Ringan | b7: baris dengan sel kurang (HPP hanya 1 dari 2 periode) tidak dicatat di "Perlu dicek"; status LENGKAP | Catat "baris X kosong untuk periode Y" |
| 4 | Ringan | Label tren netral "naik" untuk siklus kas & margin usaha, padahal siklus kas naik = memburuk dan margin usaha turun = memburuk | Beri arah baik/buruk seperti rasio lain |
| 5 | Ringan (sisa v1.0.0 #8) | Ringkasan belum memuat satu kalimat tren (mis. "laba turun 8,4% dan utang naik") | Tambah 1 kalimat tren di ringkasan bila > 1 periode |
| 6 | Ringan | Neraca selisih Rp 0,50 (b12) ditampilkan "selisih Rp 1" dan membuat SEMENTARA | Toleransi < Rp 1 |
| 7 | Ringan | Data minim: judul bagian kosong tetap dicetak; saran 6 butir ("Lainnya") sementara SKILL.md menulis "maks. 5" | Sembunyikan bagian kosong; tulis "maks. 5 + 1 ringkasan" di SKILL.md |

Temuan sedang v1.0.0 #1–#4 dan ringan #5 (tebak jenis kata utuh, uji G15), #7 (periode pendek tidak membuat SEMENTARA, uji G14) **sudah diperbaiki dan terbukti ulang**.
