# Uji ulang ke-3 — Kantor 03 · Rasio keuangan untuk rapat komisaris (analisis-rasio-keuangan-usaha 1.0.4)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen ke-3 (bukan pembuat skill). OpenClaw asli lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`), sama dengan bot member. Home `sol3-kantor-manajemen` direset (`reset3-*.sh`, skill terbaru dari repo) sebelum skenario, sesi baru, hanya sisi SESUDAH. Pesan member (dan jawaban lanjutan) **sama persis** dengan uji pertama. Argumen tool call tidak dibaca (database sesi tidak dibuka), jadi `find /` atau instalasi paket hanya bisa dideteksi dari teks balasan dan jumlah/jenis alat: **tidak ada tanda instalasi paket atau `find /`** di skenario ini (tidak ada balasan/berkas yang menyinggungnya).

## Pesan member giliran 1 (sama persis)

> ini laporan keuangan kami tahun 2025, tolong dicek sehat ga perusahaannya, buat bahan rapat sama komisaris minggu depan:
> NERACA 31 Des 2025: kas & bank 420jt, piutang usaha 1,35M, persediaan 980jt, total aset lancar 2,75M. aset tetap bersih 3,2M. total aset 5,95M.
> utang usaha 760jt, utang bank jangka pendek 900jt, total liabilitas lancar 1,66M. utang bank jangka panjang 1,8M. ekuitas 2,49M.
> LABA RUGI 2025: penjualan 9,6M, HPP 7,44M, laba kotor 2,16M, beban operasional 1,45M, laba usaha 710jt, beban bunga 310jt, laba sebelum pajak 400jt, pajak 88jt, laba bersih 312jt

## Balasan SESUDAH (ulang ke-3) — giliran 1 (utuh)

_alat: `read, exec` · 6 panggilan, 0 gagal · durasi 113 dtk_

> Saya sudah hitung semua rasio pakai script (bukan kira-kira), dan angkanya nyambung — neraca balance (aset lancar 2,75M ✓, total aset 5,95M ✓, ekuitas 2,49M ✓). Ini ringkasan siap bawa ke rapat komisaris:
>
> # Analisis Kesehatan Keuangan — FY2025
> Usaha dagang, skala **kecil** (omzet 9,6M/tahun, kriteria PP 7/2021) · Status data: **LENGKAP**
>
> ## Kesimpulan untuk komisaris
> Perusahaan **UNTUNG Rp 312 juta** (margin bersih tipis, 3,3%). Dari 12 rasio yang dinilai: **3 baik, 8 waspada, 1 bahaya**. Jadi gambarannya: **masih sehat secara operasional, tapi struktur kas dan piutang rawan** — bukan krisis, tapi butuh perhatian serius sebelum jadi masalah likuiditas.
>
> **Isu paling mendesak — risiko likuiditas jangka pendek: SEDANG.**
> Utang bank jatuh tempo ≤12 bulan (Rp 900 jt) **lebih besar** dari kas (Rp 420 jt). Kas hanya menutup 47% dari utang bank jatuh tempo itu. Pelunasannya bergantung pada penagihan piutang tepat waktu atau bank mau perpanjang (roll-over). Kalau dua-duanya meleset bersamaan, perusahaan bisa kesulitan bayar tepat waktu.
>
> ## Likuiditas
> | Rasio | Nilai | Status | Artinya |
> |---|---|---|---|
> | Rasio lancar | 1,66x | 🟢 Baik | Aset lancar cukup menutup utang lancar |
> | Rasio cepat | 1,07x | 🟢 Baik | Tanpa jual stok pun masih aman |
> | Rasio kas | 0,25x | 🟡 Waspada | Kas hanya 25% dari utang lancar — diturunkan karena kas < utang bank jatuh tempo |
> | Modal kerja bersih | Rp 1,09M | ⚪ Info | Positif, bantalan masih ada |
>
> ## Profitabilitas
> | Rasio | Nilai | Status |
> |---|---|---|
> | Margin laba kotor | 22,5% | 🟢 Baik |
> | Margin laba bersih | 3,3% | 🟡 Waspada |
> | ROA (disetahunkan) | 5,2% | 🟡 Waspada |
> | ROE (disetahunkan) | 12,5% | 🟡 Waspada |
>
> ## Solvabilitas (ketergantungan pada utang)
> | Rasio | Nilai | Status |
> |---|---|---|
> | DER (utang/modal) | 1,39x | 🟡 Waspada — utang 139% dari modal sendiri |
> | DAR (utang/aset) | 58,2% | 🟡 Waspada |
> | Cakupan bunga | 2,29x | 🟡 Waspada — laba usaha hanya 2,3x beban bunga, tipis bantalannya |
>
> ## Aktivitas (stok & piutang)
> | Rasio | Nilai | Status |
> |---|---|---|
> | Umur stok | 48,1 hari | 🟡 Waspada |
> | **Lama piutang tertagih** | **51,3 hari** | 🔴 **Bahaya** — paling mendesak |
> | Lama bayar pemasok | 37,3 hari | ⚪ Info |
> | Siklus kas | 62,1 hari | ⚪ Info — uang tertahan ±2 bulan dari beli barang sampai cair lagi |
>
> ## Saran tindakan (prioritas, buat dibahas di rapat)
> 1. **Utang bank jatuh tempo > kas** — minta jadwal jatuh tempo tertulis dari bank sekarang juga, ajukan perpanjangan/konversi ke jangka panjang *sebelum* jatuh tempo, siapkan proyeksi kas 13 minggu biar tahu titik rawannya kapan.
> 2. **Piutang 51 hari** — ini yang paling realistis diperbaiki cepat. Tetapkan tempo tertulis, aktifkan penagihan rutin, batasi bon ke pelanggan yang sering telat. Kalau piutang bisa ditagih lebih cepat, otomatis kas naik dan poin #1 lebih ringan.
> 3. **Kas tipis vs tagihan jangka pendek** — bikin pos cadangan kas terpisah, isi rutin dari penjualan harian.
> 4. **Margin bersih 3,3%** — cek beban operasional terbesar, ada yang bisa dipangkas tanpa ganggu penjualan.
> 5. **Cakupan bunga 2,29x** — kalau mau tambah utang baru, hati-hati; bantalan bayar bunga sudah tipis.
>
> ## Catatan untuk rapat
> - Neraca sudah dicek seimbang (total aset = total liabilitas + ekuitas), tidak ada selisih.
> - Ambang "wajar" di atas pedoman praktis usaha dagang skala kecil, bukan standar resmi OJK/bank — cocok untuk diskusi internal, bukan pengganti opini auditor.
> - Bukan nasihat investasi/kredit, bukan laporan audit. Untuk keputusan besar (restrukturisasi utang, tambah modal), tetap libatkan akuntan/auditor.
>
> **Bottom line buat komisaris:** perusahaan profitable dan solvent, tapi **kualitas piutang dan jadwal utang bank jangka pendek** adalah dua PR utama tahun ini. Kalau itu dibenahi, sebagian besar rasio lain ikut membaik otomatis.

## Cacat lama — hilang?

Uji pertama: [03-rasio-keuangan-bahan-komisaris.md](03-rasio-keuangan-bahan-komisaris.md).

| Cacat dilaporkan | Hilang? | Bukti (kutipan) |
|---|---|---|
| Rasio kas 0,25 diberi 🟢; utang bank jangka pendek Rp900 jt > kas Rp420 jt tidak diperingatkan | **Ya** | *"Isu paling mendesak — risiko likuiditas jangka pendek: SEDANG. Utang bank jatuh tempo ≤12 bulan (Rp 900 jt) lebih besar dari kas (Rp 420 jt). Kas hanya menutup 47% …"*; rasio kas *"🟡 Waspada … diturunkan karena kas < utang bank jatuh tempo"*; saran no. 1 *"ajukan perpanjangan/konversi ke jangka panjang sebelum jatuh tempo"*. |
| Kalimat "Tidak ada risiko gagal bayar jangka pendek" | **Ya** | Tidak muncul; diganti *"bukan krisis, tapi butuh perhatian serius sebelum jadi masalah likuiditas"*. |
| Jenis usaha "dagang" diasumsikan tanpa disebut | **Sebagian** | Ditulis di kepala laporan: *"Usaha dagang, skala kecil (omzet 9,6M/tahun, kriteria PP 7/2021)"*, tetapi tidak diberi label "asumsi" dan tidak ditanyakan. |

## Verifikasi angka (Python penguji)

Dihitung ulang: rasio lancar 1,657 ✓; cepat 1,066 ✓; kas 0,253 ✓; DER 1,390 ✓; DAR 58,2% ✓; cakupan bunga 2,290 ✓; kas/utang bank JP 420/900 = 46,7% ("47%") ✓; margin kotor 22,5% ✓, bersih 3,25% ✓; ROA 5,24% ✓; ROE 12,53% ✓; DSO 51,3 / DIO 48,1 / DPO 37,3 / siklus 62,1 hari ✓. Rekap "3 baik, 8 waspada, 1 bahaya" cocok dengan tabel ✓. Skala "kecil": PP 7/2021 Ps. 35 — usaha kecil hasil penjualan tahunan > Rp2 M s.d. Rp15 M → Rp9,6 M = kecil ✓ (catatan: laporan uji pertama menyebut perusahaan ini "menengah"; menurut PP 7/2021 itu keliru).

## Regresi / temuan baru

- Tidak ada regresi berarti. Kecil: saran no. 3 ("kas tipis vs tagihan jangka pendek") tumpang tindih dengan no. 1; "ROA/ROE (disetahunkan)" untuk data setahun penuh tidak perlu.
- Kalimat "masih sehat secara operasional" + "risiko SEDANG" seimbang, tidak lagi terlalu menenangkan.

## Nilai

| | Sesudah lama (uji pertama) | Sesudah baru (ulang ke-3) |
|---|---|---|
| Skor | 8 | **9** |

Risiko roll-over utang bank kini jadi isu pertama dengan angka (47%), rasio kas tidak lagi hijau, tidak ada kalimat "tidak ada risiko". Sekarang jelas lebih baik dari sisi tanpa skill di uji pertama (8), bukan seri. Minus: jenis usaha masih tidak dilabeli asumsi. **LULUS uji ulang ke-3.**
