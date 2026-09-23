# 06 — Data berisik: nama depan sama, nominal sama beda orang, gabungan, termin 3×, nama badan usaha mirip (v1.1.0)

**Skenario:** uji tambahan (stress test) untuk mencari pasangan palsu. Semua data fiktif.

Kasus yang sengaja dimasukkan ke data:
- Dua pelanggan bernama depan **Andi**, masing-masing Rp 200.000 di hari yang sama.
- **Rudi** dan **Sinta** sama-sama Rp 500.000. Hanya Sinta yang transfer; ada transfer lain Rp 500.000 dari orang yang tidak dikenal (SURYA KENCANA).
- **Lestari** membayar 2 invoice sekaligus.
- **Bambang** mencicil 3× Rp 300.000 (tanggal 10, 17, dan 24; transfer ke-3 terjadi 15 hari setelah invoice).
- **CV Maju Jaya** vs transfer dari **PT JAYA MAJU MOTOR** dengan nominal & tanggal sama.
- **Kartika** membayar dengan no. invoice di berita transfer, terpotong Rp 5.000.
- **Heru Prasetyo** vs **Hermawan** (sama-sama Rp 400.000; hanya "HERU" yang transfer).

**Input pengguna (persis):**
> Tolong cocokin mutasi BCA November (berisik-bank.csv) sama invoice (berisik-catatan.csv). Pelanggan saya banyak yang namanya mirip, hati-hati ya.

## Output (mengikuti SKILL.md, script v1.1.0)

> 🔒 Data rekening hanya dibaca di komputer ini; jangan tempel PIN/OTP.

(Kolom dikonfirmasi seperti format BCA pada contoh 01.)

## Rekonsiliasi BCA — November 2026
Total catatan: **Rp 5.950.000** · Total uang masuk bank: **Rp 5.545.000** · Selisih: **Rp 405.000**

| Kelompok | Jumlah | Nilai catatan | Nilai bank |
|---|---:|---:|---:|
| ✅ Cocok | 6 | Rp 3.050.000 | Rp 3.050.000 |
| 🟡 Cocok parsial (perlu dicek) | 3 | Rp 2.500.000 | Rp 1.895.000 |
| ❌ Ada di catatan, tidak ada di bank | 1 | Rp 400.000 | — |
| ❓ Ada di bank, tidak ada di catatan | 2 | — | Rp 600.000 |

### Penjelasan selisih Rp 405.000
+ Rp 400.000 − Rp 600.000 + Rp 605.000 = **Rp 405.000** (angka seimbang; tetap cek pasangan 🟡 dan yang saya tandai ⚠)

### Hasil pemeriksaan nama oleh agent (langkah 5 SKILL.md)
Dari 6 pasangan "cocok" versi script, hanya **2 yang pasti**:
- INV-0034 Sinta Dewi ↔ SINTA DEWI
- INV-0043 Heru Prasetyo ↔ HERU

Empat lainnya **perlu dicek**:

| Catatan | Bank | Masalah |
|---|---|---|
| INV-0031 **Andi Wijaya** | 03/11 **ANDI SAPUTRA** Rp 200.000 | Tertukar: nama belakang berbeda. Seharusnya ↔ ANDI WIJAYA |
| INV-0032 **Andi Saputra** | 03/11 **ANDI WIJAYA** Rp 200.000 | Tertukar (pasangan kebalikannya) |
| INV-0033 **Rudi Hartono** | 06/11 **SURYA KENCANA** Rp 500.000 | Pengirim bukan Rudi ("nama tidak terlihat"). Tanyakan apakah Surya membayar untuk Rudi; kalau tidak, INV-0033 belum dibayar |
| INV-0038 **CV Maju Jaya** | 12/11 **PT JAYA MAJU MOTOR** Rp 1.250.000 | Kata "Jaya" dan "Maju" sama, tetapi badan usahanya berbeda (CV vs PT, ada "Motor"). Konfirmasi |

🟡 Parsial:
- Lestari (INV-0035 + INV-0036 = 1 transfer Rp 750.000) ✔
- Kartika (INV-2026-0042 ada di berita, bank Rp 845.000, kurang Rp 5.000, kemungkinan biaya transfer) ✔
- Bambang INV-0037 Rp 900.000 ↔ transfer 10/11 Rp 300.000: script menyebut "baru bayar sebagian". Namun transfer BAMBANG ARIF tanggal 17/11 dan 24/11 (masing-masing Rp 300.000) masuk kelompok "tidak ada di catatan". **Kemungkinan besar ketiganya adalah cicilan INV-0037 dan sudah lunas.**

❌ Belum di bank: INV-0044 Hermawan Rp 400.000. Transfer "HERU" sudah tepat dipasangkan ke Heru Prasetyo, bukan ke Hermawan.

## Catatan penguji (verifikasi independen dengan `verif_v110.py`)
- Total dan rincian selisih benar secara aritmetika:
  - Catatan: 200.000 + 200.000 + 500.000 + 500.000 + 300.000 + 450.000 + 900.000 + 1.250.000 + 850.000 + 400.000 + 400.000 = 5.950.000
  - Bank: 5.545.000
  - Rincian: 400.000 − 600.000 + 605.000 = 405.000 ✔
- ✅ **Berhasil:**
  - Heru ≠ Hermawan (kecocokan kata utuh bekerja)
  - Sinta dipilih, bukan Rudi
  - Lestari (pembayaran gabungan) dan Kartika (no. invoice di berita + potong biaya) benar
- ❌ **Andi Wijaya/Andi Saputra tertukar, dan berlabel ✅ COCOK "nama ada di keterangan bank".**
  - Penyebab: `cocok_nama` (script baris 524–530) sudah menganggap cocok bila **satu kata** nama sama ("andi"), lalu tahap 0 memilih pasangan menurut tanggal/urutan baris, bukan menurut jumlah kata nama yang cocok. `konflik()` juga tidak mendeteksinya, karena "ANDI SAPUTRA" memang memuat kata "andi".
  - Varian lebih berbahaya (diuji dengan `andi-cat2.csv`): hanya ANDI SAPUTRA yang transfer (04/11), tetapi invoice **Andi Wijaya** tertanggal 04/11 yang mendapat ✅ COCOK, sementara Andi Saputra tercatat **belum dibayar**. Akibatnya orang yang salah bisa ditagih.
- ⚠ Rudi ↔ SURYA KENCANA tetap berstatus COCOK ("nama tidak terlihat — cek sekilas") dan ikut dihitung di baris ✅.
- ⚠ CV Maju Jaya ↔ PT JAYA MAJU MOTOR dianggap "nama ada di keterangan", karena untuk nama yang seluruhnya kata umum cukup semua katanya muncul.
- ⚠ Cicilan ke-3 Bambang (15 hari setelah invoice) berada di luar jendela `--maks-hari-parsial 14` pada tahap 2c. Jendela `--maks-hari-nama` (31) tidak dipakai untuk kombinasi transfer yang namanya cocok.
- Pada semua kasus di atas, pemeriksaan nama yang diwajibkan SKILL.md langkah 5 membuat agent tetap menandai pasangan bermasalah. Laporan akhir jadi benar, tetapi bergantung pada ketelitian agent.
