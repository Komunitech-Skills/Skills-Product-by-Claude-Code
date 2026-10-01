# Uji OpenClaw 03 — Rasio keuangan dari neraca + laba rugi 2025 (bahan rapat komisaris)

Tanggal: 2026-10-01 · Agent: OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot member), sesi baru per sisi, kedua home direset sebelum skenario. SEBELUM = home `kosong-kantor-manajemen` (tanpa skill), SESUDAH = home `sol-kantor-manajemen` (17 skill paket kantor-manajemen). Semua data fiktif.

## Pesan member (identik di kedua sisi)

> ini laporan keuangan kami tahun 2025, tolong dicek sehat ga perusahaannya, buat bahan rapat sama komisaris minggu depan:
> NERACA 31 Des 2025: kas & bank 420jt, piutang usaha 1,35M, persediaan 980jt, total aset lancar 2,75M. aset tetap bersih 3,2M. total aset 5,95M.
> utang usaha 760jt, utang bank jangka pendek 900jt, total liabilitas lancar 1,66M. utang bank jangka panjang 1,8M. ekuitas 2,49M.
> LABA RUGI 2025: penjualan 9,6M, HPP 7,44M, laba kotor 2,16M, beban operasional 1,45M, laba usaha 710jt, beban bunga 310jt, laba sebelum pajak 400jt, pajak 88jt, laba bersih 312jt

## SEBELUM (tanpa skill) — balasan utuh

> Sudah saya cek semua angkanya — neraca balance (aset = liabilitas + ekuitas = 5,95M) dan laba rugi nyambung semua runtutannya. Berikut analisis rasio keuangannya untuk bahan rapat komisaris:
>
> **RINGKASAN KESEHATAN KEUANGAN 2025**
> Status: **Cukup sehat tapi rentan** — profitable dan solvent, tapi likuiditas tunai tipis dan beban bunga mulai menggerus margin.
>
> ---
>
> **1. Likuiditas**
> - Current ratio = 2,75M / 1,66M = **1,66x** → aset lancar masih di atas liabilitas lancar, oke secara teknis
> - Quick ratio (tanpa persediaan) = 1,77M / 1,66M = **1,07x** → pas-pasan, likuiditas banyak "terkunci" di persediaan
> - Cash ratio = 420jt / 1,66M = **0,25x** → kas hanya nutup 25% kewajiban jangka pendek
> - Working capital = **+1,09M** (positif, tapi kualitasnya rendah karena didominasi piutang+persediaan, bukan kas)
>
> ⚠️ Catatan penting: utang bank jangka pendek 900jt jatuh tempo, sementara kas cuma 420jt. Kalau bank tidak perpanjang/roll-over, perusahaan harus cairkan piutang/persediaan cepat atau cari pendanaan tambahan.
>
> **2. Solvabilitas / Leverage**
> - Total liabilitas = 3,46M, Ekuitas = 2,49M
> - Debt to Equity (DER) = **1,39x** → utang 1,4x lebih besar dari modal sendiri, tergolong leverage sedang-tinggi
> - Debt to Asset = **58%** → lebih dari separuh aset dibiayai utang
> - Interest coverage ratio = Laba usaha / Beban bunga = 710jt / 310jt = **2,29x** → laba usaha masih nutup bunga, tapi marginnya tipis (idealnya >3x untuk aman). Kalau laba usaha turun ~15-20%, cakupan bunga bisa di bawah 2x.
>
> **3. Profitabilitas**
> - Gross margin = 2,16M / 9,6M = **22,5%**
> - Operating margin = 710jt / 9,6M = **7,4%**
> - Net margin = 312jt / 9,6M = **3,25%** → tipis untuk omzet sebesar 9,6M
> - ROA = 312jt / 5,95M = **5,2%**
> - ROE = 312jt / 2,49M = **12,5%** → lumayan, tapi ini terdorong oleh leverage (utang), bukan semata efisiensi operasional
>
> **4. Efisiensi Modal Kerja**
> - Perputaran piutang = 9,6M/1,35M = 7,1x → rata-rata **51 hari** piutang tertagih
> - Perputaran persediaan = 7,44M/980jt = 7,6x → rata-rata **48 hari** stok mengendap
> - Perputaran utang usaha ≈ **37 hari**
> - Cash Conversion Cycle ≈ 51+48-37 = **~62 hari** → butuh ~2 bulan uang "nyangkut" di piutang & stok sebelum balik jadi kas
>
> ---
>
> **KESIMPULAN**
> ✅ Positif: penjualan besar (9,6M), masih untung bersih (312jt), ekuitas positif, neraca balance dan sehat secara struktur.
> ⚠️ Perhatian utama:
> 1. **Risiko likuiditas jangka pendek** — kas tipis vs utang bank jangka pendek yang jatuh tempo (900jt)
> 2. **Margin bersih tipis (3,25%)** — sensitif terhadap kenaikan biaya/bunga/persaingan harga
> 3. **Leverage sedang-tinggi (DER 1,39x)**, cakupan bunga pas-pasan (2,29x)
> 4. **Siklus kas ~62 hari** — modal kerja banyak tertahan di piutang & persediaan
>
> **REKOMENDASI untuk dibahas di rapat:**
> 1. Negosiasi perpanjangan/refinancing utang bank jangka pendek 900jt sebelum jatuh tempo, atau siapkan fasilitas cadangan
> 2. Percepat penagihan piutang (target turun dari 51 → ~35-40 hari) dan tekan persediaan berlebih
> 3. Evaluasi struktur biaya HPP (77,5% dari penjualan) — cek apakah ada ruang efisiensi
> 4. Pertimbangkan apakah perlu suntikan modal/ekuitas tambahan untuk kurangi ketergantungan pada utang bank, mengingat DER sudah >1x
> 5. Buat proyeksi cash flow 2026 untuk pastikan cukup kas menutup kewajiban jangka pendek
>
> Mau saya buatkan ini jadi slide/PDF ringkas buat dibawa ke rapat komisaris, atau format tabel saja?

## SESUDAH (paket skill kantor-manajemen) — balasan utuh

> Sudah saya hitung pakai script rasio keuangan (bukan kira-kira). Berikut ringkasannya — siap jadi bahan rapat komisaris.
>
> ## Kesimpulan Singkat
> **Perusahaan UNTUNG tapi tipis, dan cukup bergantung pada utang.** Dari 12 rasio yang dinilai: **4 baik 🟢, 7 waspada 🟡, 1 bahaya 🔴**. Laba bersih 2025 Rp 312 juta (3,3% dari penjualan Rp 9,6 M) — bukan rugi, tapi marginnya tipis dan ada beberapa titik yang perlu dibenahi sebelum ini jadi masalah serius.
>
> ## Likuiditas — aman bayar tagihan jangka pendek? 🟢
> | Rasio | Nilai | Status | Artinya |
> |---|---|---|---|
> | Rasio lancar | 1,66x | 🟢 Baik | Aset lancar cukup menutup utang lancar + buffer |
> | Rasio cepat | 1,07x | 🟢 Baik | Tanpa jual stok pun masih aman |
> | Rasio kas | 0,25x | 🟢 Baik | Kas langsung menutup 25% utang lancar |
>
> ➡️ Tidak ada risiko gagal bayar jangka pendek saat ini.
>
> ## Profitabilitas — seberapa untung? 🟡
> | Rasio | Nilai | Status | Artinya |
> |---|---|---|---|
> | Margin laba kotor | 22,5% | 🟢 Baik | Margin dasar bisnis sehat |
> | Margin laba bersih | 3,3% | 🟡 Waspada | Banyak "bocor" di beban operasional/bunga/pajak |
> | ROA (laba÷aset) | 5,2% | 🟡 Waspada | Aset Rp 5,95 M belum menghasilkan laba optimal |
> | ROE (laba÷modal) | 12,5% | 🟡 Waspada | Return ke pemegang saham masih di bawah ambang baik (≥15%) |
>
> ➡️ Masalah utamanya bukan di penjualan/margin kotor, tapi di efisiensi biaya operasional & beban bunga yang menggerus laba.
>
> ## Solvabilitas — seberapa bergantung pada utang? 🟡
> | Rasio | Nilai | Status | Artinya |
> |---|---|---|---|
> | DER (utang÷modal) | 1,39x | 🟡 Waspada | Utang 139% dari modal sendiri |
> | DAR (utang÷aset) | 58,2% | 🟡 Waspada | 58% aset dibiayai utang |
> | Cakupan bunga | 2,29x | 🟡 Waspada | Laba usaha hanya 2,3x beban bunga — ada ruang tapi tidak lega |
>
> ➡️ Struktur modal masih sehat secara teknis, tapi beban bunga (Rp 310 jt) sudah "memakan" hampir separuh laba usaha (Rp 710 jt). Ini akar masalah margin bersih tipis.
>
> ## Aktivitas — kecepatan stok & piutang jadi uang 🔴
> | Rasio | Nilai | Status | Artinya |
> |---|---|---|---|
> | Umur stok | 48,1 hari | 🟡 Waspada | Stok cukup lama mengendap |
> | **Lama piutang tertagih** | **51,3 hari** | 🔴 **Bahaya** | Uang dari penjualan baru masuk ±51 hari — paling mendesak |
> | Lama bayar ke pemasok | 37,3 hari | ⚪ Info | — |
> | Siklus kas | 62,1 hari | ⚪ Info | Uang tertahan ±62 hari dari beli barang sampai kembali jadi kas |
>
> ➡️ **Ini titik paling mendesak.** Piutang 51 hari + stok 48 hari, sementara bayar pemasok cuma 37 hari — perusahaan membiayai jarak itu pakai utang bank jangka pendek (Rp 900 jt), yang kemungkinan besar sumber beban bunga tadi.
>
> ## Benang Merah untuk Komisaris
> Likuiditas & margin kotor sehat → bisnis intinya oke. Tapi **piutang lambat tertagih → butuh pinjaman jangka pendek → beban bunga tinggi → laba bersih tergerus ke 3,3%**. Ini satu rantai masalah, bukan 7 masalah terpisah.
>
> ## Saran Prioritas (untuk dibahas)
> 1. **Percepat penagihan piutang** — target turun dari 51 hari ke ≤45 hari. Tetapkan tempo tertulis, kirim reminder sebelum jatuh tempo, batasi bon pelanggan telat.
> 2. **Tekan beban operasional & review struktur utang** — cek apakah utang bank jangka pendek (Rp 900 jt) bisa direstrukturisasi/diperpanjang untuk turunkan tekanan bunga.
> 3. **Percepat perputaran stok** — 48 hari cukup lama untuk bisnis dagang; cek SKU yang lambat laku.
> 4. **Jangan tambah utang baru dulu** sampai DER turun di bawah 1,0x — dahulukan efisiensi & percepatan kas dulu.
> 5. Setelah 2 poin di atas membaik, ROA/ROE otomatis akan ikut naik.
>
> ---
> ⚠️ **Catatan:** ini pembacaan rasio berdasarkan pedoman praktis (bukan standar resmi OJK/bank), bukan audit atau nasihat investasi. Untuk keputusan strategis besar (restrukturisasi utang, dsb.), tetap libatkan akuntan/auditor.
>
> Mau saya buatkan versi **1 halaman eksekutif / ringkasan 5 baris untuk WA / skrip bicara 2 menit** biar lebih enak dipresentasikan ke komisaris? Saya punya skill khusus untuk itu.

## Verifikasi & pemakaian skill

- **Pemakaian skill:** SESUDAH membaca `analisis-rasio-keuangan-usaha/SKILL.md` dan menjalankan `scripts/rasio.py` (jenis `dagang`, angka diketik). SEBELUM tanpa script (hanya `tool_search`).
- **Angka (dihitung ulang penguji, Python):** rasio lancar 1,657; cepat 1,066; kas 0,253; DER 1,390; DAR 58,2%; cakupan bunga 2,290; margin kotor 22,5%; usaha 7,40%; bersih 3,25%; ROA 5,24%; ROE 12,53%; DSO 51,3 hr; DIO 48,1 hr; DPO 37,3 hr; siklus kas 62,1 hr. **Semua angka di kedua sisi benar.** Hitungan rangkuman SESUDAH "4 baik, 7 waspada, 1 bahaya" juga cocok dengan tabelnya.
- **Kelebihan SEBELUM:** memeriksa neraca seimbang, dan menangkap **risiko paling penting untuk komisaris**: utang bank jangka pendek Rp900 jt vs kas Rp420 jt (risiko roll-over), plus uji sensitivitas cakupan bunga (laba usaha −15% → 710×0,85/310 = 1,95x ✓).
- **Kelemahan SESUDAH:** menyimpulkan "**Tidak ada risiko gagal bayar jangka pendek saat ini**" dan memberi rasio kas 0,25x status 🟢 — ambang skill dibuat untuk UMKM (rasio kas ≥0,2 = baik) dan tidak punya aturan "utang bank jangka pendek > kas". Untuk perusahaan dengan Rp900 jt pinjaman jangka pendek, kalimat itu terlalu yakin. Jenis usaha "dagang" diasumsikan tanpa ditanyakan/disebut eksplisit sebagai asumsi.
- **Kelebihan SESUDAH:** tabel bertanda 🟢🟡🔴 dengan arti bahasa awam, "benang merah" (piutang lambat → pinjaman → bunga → laba tipis) yang bagus untuk komisaris, disclaimer bukan audit.
- **Keamanan:** tidak ada isu di kedua sisi.

## Nilai

| | Sebelum | Sesudah |
|---|---|---|
| Skor (1–10) | 8 | 8 |

SEBELUM 8: semua angka benar tanpa script, cek neraca seimbang, dan menangkap risiko roll-over utang bank jangka pendek. SESUDAH 8: angka dari script (lebih bisa dipercaya untuk data yang lebih berantakan), penyajian lebih siap rapat, disclaimer; tetapi salah menenangkan soal likuiditas. **Seri — untuk input rapi seperti ini, model tanpa skill sudah sama bagusnya.**
