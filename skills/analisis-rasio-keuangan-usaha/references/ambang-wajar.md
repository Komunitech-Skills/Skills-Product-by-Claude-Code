# Rumus & Ambang Wajar Rasio: Dasar dan Sumber

**Dicek per: 2026-09-26.** Tinjau ulang minimal setahun sekali, atau saat bunga KUR berubah.

## 1. Sifat ambang ini (baca dulu)
Ambang "baik / waspada / bahaya" di skill ini adalah **pedoman praktis Komunitech untuk UMKM**. Ambang ini **bukan standar resmi** OJK, Bank Indonesia, IAI, atau bank mana pun. Bank punya penilaian internal sendiri yang tidak dipublikasikan. Tidak ada tolok ukur rasio resmi per sektor untuk usaha mikro di Indonesia yang bisa diakses publik (dicari 2026-09-26). Ambang ini disusun dari tiga pijakan:

1. **Buku teks yang paling banyak dikutip di Indonesia.** Kasmir, *Analisis Laporan Keuangan* (Rajawali Pers; edisi 2016/2018). Buku ini memuat "standar rata-rata industri" untuk **perusahaan umum**, antara lain rasio lancar 2 kali (200%), rasio cepat 1,5 kali (150%), DER maksimal 90%, dan DAR maksimal 35%. Angka ini **dicek lewat jurnal yang mengutipnya**, tidak dari buku aslinya, misalnya https://ejurnalunsam.id/index.php/jensi/article/download/403/296 dan https://journal.ubpkarawang.ac.id/mahasiswa/index.php/JMMA/article/download/190/124. Angka Kasmir dipakai sebagai **batas atas "ideal"**. Untuk usaha mikro ambangnya diturunkan, karena warung dan toko memang menaruh sebagian besar aset lancar di stok. Menuntut rasio cepat 1,5 berarti hampir semua warung akan dinilai "bahaya" padahal sehat.
2. **Contoh tolok ukur di sumber kurasi.** File `interpret_ratios.py` di anthropics/claude-cookbooks (MIT, commit `813fbee`) memuat angka untuk *retail*: rasio lancar dianggap cukup mulai 1,0 dan baik mulai 1,5; DER cukup sampai 1,5; margin kotor cukup mulai 20% dan baik mulai 30%. Untuk *manufacturing*: rasio lancar cukup mulai 1,3; DER cukup sampai 1,2; margin kotor cukup mulai 18% dan baik mulai 25%. Sumber itu sendiri menyebut angkanya *"simplified for demonstration"*, jadi dipakai hanya sebagai pembanding arah, bukan acuan.
3. **Logika biaya modal di Indonesia.** Bunga KUR Mikro/Kecil adalah **6% efektif per tahun** untuk akad pertama (Permenko Perekonomian 1/2026 Pasal 37 & 44; lihat `skills/pengajuan-kur/references/regulasi.md`). Karena itu ROE di bawah 6% berarti modal pemilik menghasilkan lebih kecil dari bunga pinjaman termurah, sehingga masuk "bahaya". ROE ≥ 15% dianggap "baik", karena memberi ruang untuk risiko usaha dan inflasi.

Rasio cicilan terhadap laba bersih memakai ambang yang sama dengan skill `pengajuan-kur`: ≤ 30% aman, > 30–50% berat, > 50% terlalu berat, ≥ 100% laba tidak cukup. Itu pun **panduan skill, bukan aturan bank**.

## 2. Tabel ambang per jenis usaha
Format: **baik / waspada**. Nilai yang lebih buruk dari batas waspada = bahaya. Panah ↑ berarti makin tinggi makin baik, ↓ makin rendah makin baik.

| Rasio | Dagang (warung, toko) | Jasa | Produksi/manufaktur kecil (termasuk kuliner & katering) | Umum | Alasan singkat |
|---|---|---|---|---|---|
| Rasio lancar ↑ | ≥1,5 / ≥1,0 | ≥1,2 / ≥1,0 | ≥1,5 / ≥1,1 | ≥1,5 / ≥1,0 | Di bawah 1 berarti utang ≤1 tahun lebih besar dari aset lancar. Kasmir 2,0 untuk perusahaan umum |
| Rasio cepat ↑ | ≥0,5 / ≥0,2 | ≥1,0 / ≥0,7 | ≥0,8 / ≥0,5 | ≥0,8 / ≥0,5 | Aset warung memang kebanyakan stok. Usaha jasa hampir tanpa stok, jadi harus lebih tinggi |
| Rasio kas ↑ | ≥0,2 / ≥0,1 | ≥0,3 / ≥0,15 | ≥0,2 / ≥0,1 | ≥0,2 / ≥0,1 | Kas minimal untuk tagihan mendadak |
| Margin kotor ↑ (%) | ≥15 / ≥8 | ≥40 / ≥25 | ≥25 / ≥15 | ≥20 / ≥10 | Sembako margin tipis. Jasa hampir tanpa modal barang. Cookbook: manufaktur 18–25% |
| Margin bersih ↑ (%) | ≥5 / ≥2 | ≥15 / ≥8 | ≥8 / ≥4 | ≥8 / ≥3 | Setelah semua biaya |
| ROA ↑ (%/tahun) | ≥10 / ≥5 | ≥15 / ≥7 | ≥8 / ≥4 | ≥10 / ≥5 | Manufaktur padat alat, jadi lebih rendah |
| ROE ↑ (%/tahun) | ≥15 / ≥6 | sama | sama | sama | 6% = bunga KUR (Permenko 1/2026) |
| DER ↓ (x) | ≤1,0 / ≤2,0 | sama | sama | sama | Kasmir ≤0,9. Cookbook retail cukup sampai 1,5 |
| DAR ↓ (%) | ≤50 / ≤67 | sama | sama | sama | Setara DER 1 dan 2. Kasmir ≤35% |
| Cakupan bunga ↑ (x) | ≥3 / ≥1,5 | sama | sama | sama | Di bawah 1,5 bunga menggerus sebagian besar laba usaha |
| Umur stok ↓ (hari) | ≤30 / ≤60 | tidak dinilai | ≤60 / ≤90 | ≤45 / ≤90 | Barang dagang cepat basi/usang. Produksi termasuk bahan & barang setengah jadi |
| Lama piutang ↓ (hari) | ≤30 / ≤45 | ≤45 / ≤60 | ≤45 / ≤60 | ≤45 / ≤60 | Tempo umum pemasok & B2B 30 hari |

Yang tidak diberi status, cukup "info": modal kerja, margin usaha, perputaran (persediaan, piutang, aset), lama bayar pemasok, dan siklus kas. Rasio-rasio ini hanya bermakna bila dibandingkan antarperiode.

**Catatan jenis usaha**
- Warung makan, katering, dan kue dimasukkan ke **produksi**, karena mereka mengolah bahan. Margin kotornya biasanya jauh di atas warung sembako.
- Toko fashion atau aksesori bermargin tinggi tetap "dagang". Margin kotor 30–50% di sana wajar dan akan tampil "baik".
- Jika usaha campuran (mis. bengkel yang juga jual suku cadang), pakai jenis yang menyumbang omzet terbesar, atau `umum`.

## 3. Rumus (untuk fallback manual)
Semua nilai memakai angka **akhir periode**. Bila saldo awal tersedia (dari laporan periode sebelumnya atau `saldo_awal` EMKM), dipakai **rata-rata (awal + akhir) ÷ 2** untuk persediaan, piutang, total aset, dan modal.

- Aset lancar = kas + piutang + persediaan + aset lancar lain
- Utang lancar = utang usaha + utang jatuh tempo ≤ 12 bulan (termasuk bagian cicilan pokok bank 12 bulan ke depan, titipan pajak)
- Total aset = aset lancar + aset tetap (nilai buku); modal = total aset − total utang
- Rasio lancar = aset lancar ÷ utang lancar
- Rasio cepat = (aset lancar − persediaan) ÷ utang lancar
- Rasio kas = kas ÷ utang lancar
- Margin kotor = (penjualan − HPP) ÷ penjualan × 100
- Margin bersih = laba bersih ÷ penjualan × 100
- ROA/tahun = laba bersih ÷ total aset × 100 × (365 ÷ jumlah hari periode)
- ROE/tahun = laba bersih ÷ modal × 100 × (365 ÷ hari)
- DER = total utang ÷ modal; DAR = total utang ÷ total aset × 100
- Cakupan bunga = laba usaha ÷ beban bunga (tanpa laba usaha: laba bersih + bunga + pajak)
- Umur stok (hari) = persediaan × hari periode ÷ HPP; perputaran = HPP ÷ persediaan
- Lama piutang (hari) = piutang × hari ÷ penjualan tempo (bila tidak ada: total penjualan; hasilnya jadi terlalu optimis)
- Lama bayar pemasok (hari) = utang usaha × hari ÷ HPP
- Siklus kas = umur stok + lama piutang − lama bayar pemasok
- Laba per bulan = laba bersih ÷ jumlah bulan; rasio cicilan = cicilan per bulan ÷ laba per bulan × 100
- Jumlah hari: 12 bulan = 365 hari; n bulan = 365 × n ÷ 12.

**Aturan pembagian nol & angka negatif (wajib diikuti juga saat manual):**
- Pembagi 0: jangan tulis 0 atau ∞. Tulis "tidak dihitung" beserta alasannya. Contoh: utang lancar 0 berarti tidak ada tagihan dekat (aman); penjualan 0 berarti margin tidak ada.
- Modal ≤ 0: ROE dan DER **tidak bermakna**. Tulis "modal habis/negatif", status bahaya.
- Laba negatif: margin/ROA/ROE ditulis negatif dan disebut **rugi**.
- Kas, piutang, persediaan, aset, atau utang bernilai negatif: **mustahil**. Rasio yang memakainya tidak dihitung, lalu tanyakan angkanya.
- Pembulatan tampilan: rasio 2 desimal, persen & hari 1 desimal, rupiah ke rupiah terdekat (setengah ke atas). Hitung dengan angka penuh, bulatkan hanya saat menampilkan.
