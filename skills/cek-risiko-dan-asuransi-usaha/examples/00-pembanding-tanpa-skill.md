# Uji A/B: tanpa skill vs dengan skill (skenario normal 1)

- Tanggal: 2026-10-09
- Penguji: agent independen (bukan pembuat skill), hanya membaca folder skill ini
- Platform: `claude-code (simulasi agent)`. Tidak ada akses OpenClaw/kunci model di sesi ini, jadi kedua sisi disimulasikan oleh agent penguji; sisi "tanpa skill" ditulis sebagai jawaban model dasar yang wajar tanpa membaca folder skill.
- Angka sisi "dengan skill" diambil dari `scripts/cek_risiko.py` dan dihitung ulang terpisah (`examples/data/verifikasi-independen.py`): semua cocok.

## Pesan uji (identik di kedua sisi)
> kak sy punya kafe kecil di ruko 2 lt deket kali di bekasi, karyawan 3 (blm ikut bpjs tk, cuma bpjs kes yg mandiri masing2). sewa 4,5jt/bln, gaji @2,8jt, listrik+gas 1,7jt, cicilan mesin espresso 1,2jt. kas cadangan cuma 8jt. thn 2020 pernah kebanjiran semata kaki. perlu asuransi apa ya? dana darurat brp?

## SEBELUM (tanpa skill)
> Halo Kak! Untuk kafe kecil di Bekasi dekat kali, berikut risiko utama dan asuransi yang bisa dipertimbangkan:
>
> **Risiko utama**
> 1. **Banjir** – karena dekat kali dan pernah kebanjiran. Simpan peralatan di tempat tinggi.
> 2. **Kebakaran** – dapur dengan gas dan listrik. Sediakan APAR.
> 3. **Kecelakaan kerja** – karyawan bisa terluka.
> 4. **Pencurian.**
> 5. **Keracunan makanan** pelanggan.
>
> **Asuransi yang disarankan**
> - **Asuransi properti/kebakaran** dengan perluasan banjir. Beberapa perusahaan yang punya produk UMKM misalnya asuransi dari bank BUMN atau perusahaan asuransi umum besar.
> - **BPJS Ketenagakerjaan** untuk karyawan (wajib). Iurannya sekitar 0,24%–1,74% untuk JKK, 0,3% JKM, dan JHT 5,7%.
> - **Asuransi tanggung gugat** (opsional).
>
> **Dana darurat**
> Biaya bulanan Kakak: 4,5 jt + 8,4 jt + 1,7 jt + 1,2 jt = **15,8 jt**. Idealnya dana darurat usaha 3–6 bulan, jadi **Rp47,4 jt – Rp94,8 jt**. Kas sekarang 8 jt, jadi masih kurang cukup banyak. Coba sisihkan 10–20% laba tiap bulan.
>
> Semoga membantu! Sebaiknya konsultasikan dengan agen asuransi.

**Nilai: 6,5/10.** Angka biaya & target benar, risiko utama tepat. Kurang: tidak ada skor/prioritas, tidak ada kolom "perlu asuransi atau tidak" per risiko, kekurangan kas tidak dihitung, tidak ada cicilan menabung konkret, menyebut tarif iuran BPJS dari ingatan tanpa tanggal/sumber (berisiko keliru), menyinggung "bank BUMN/perusahaan besar" (mendekati rekomendasi merek), tidak ada daftar pertanyaan ke agen, tidak ada cek izin OJK.

## SESUDAH (dengan skill)
> **Asumsi:** kafe di ruko 2 lantai dekat kali, Bekasi; 3 karyawan; nilai alat & stok belum disebut (`[isian: nilai aset]`).
>
> | No | Risiko | Kemungkinan | Dampak | Skor/Tingkat | Langkah murah minggu ini | Perlu asuransi? |
> |---|---|---|---|---|---|---|
> | 1 | Banjir (dekat kali, pernah 2020) | 3 | 4 | 12 TINGGI | Stok, mesin kecil & dokumen di rak tinggi/lantai 2; palet; salinan digital dokumen | Ya, pertimbangkan |
> | 2 | Kebakaran dapur (gas, korsleting) | 2 | 5 | 10 TINGGI | APAR + cek tanggal isi ulang, cek selang & regulator gas, ganti colokan bertumpuk | Ya, pertimbangkan |
> | 3 | Barista kunci keluar mendadak | 3 | 3 | 9 SEDANG | Tulis resep & takaran (SOP), latih 1 cadangan | Tidak perlu |
> | 4 | Karyawan cedera kerja (luka bakar, terpeleset) | 3 | 3 | 9 SEDANG | Keset antislip, sarung tangan panas; daftarkan BPJS Ketenagakerjaan | Tidak perlu (BPJS dibahas terpisah) |
> | 5 | Mesin espresso rusak / listrik padam | 3 | 3 | 9 SEDANG | Nomor teknisi cadangan, stabilizer/UPS | Tidak perlu |
> | 6 | Pelanggan sakit perut/keracunan | 2 | 4 | 8 SEDANG | Catat tanggal bahan, kulkas di bawah 5°C, cuci tangan | Ya, pertimbangkan |
> | 7 | Pencurian kas/stok | 3 | 2 | 6 SEDANG | Setor kas harian, hitung stok mingguan | Tidak perlu |
> | 8 | Gempa bumi | 1 | 4 | 4 RENDAH | Ikat rak tinggi ke dinding | Tidak |
> | 9 | Bukti transfer palsu | 2 | 2 | 4 RENDAH | Cek mutasi sebelum kopi diserahkan | Tidak |
>
> **Dana darurat (3 bulan)**
> - Biaya tetap per bulan: Rp15.800.000 (sewa 4,5 jt + gaji 3 × 2,8 jt + listrik/gas 1,7 jt + cicilan 1,2 jt)
> - Target: **Rp47.400.000**
> - Kas sekarang: Rp8.000.000 (cukup ±0,5 bulan)
> - Kekurangan: **Rp39.400.000** → bila dikejar 12 bulan, sisihkan Rp3.283.334/bulan.
>
> **Jenis perlindungan umum (tanpa merek)**
> - Asuransi kebakaran/properti untuk isi & alat: tanyakan perluasan banjir (biasanya terpisah per polis).
> - Tanggung gugat umum: bila pelanggan sakit/cedera dan menuntut.
> - BPJS Ketenagakerjaan (JKK, JKM, JHT, JP) & BPJS Kesehatan: kewajiban pemberi kerja dan iuran cek di sumber resmi BPJS per hari ini.
> Asuransi mengalihkan kerugian besar yang jarang; tetap ada premi, pengecualian, dan batas klaim. Cek izin perusahaan & agen di OJK; jangan bayar ke rekening pribadi.
>
> **3 prioritas minggu ini:** (1) naikkan stok & alat dari lantai dasar; (2) APAR + cek gas; (3) tanyakan pendaftaran BPJS Ketenagakerjaan karyawan.
>
> *Ini alat bantu awam, bukan nasihat asuransi/keuangan/hukum.*
> Pertanyaan: 1) Berapa kira-kira nilai mesin, alat, dan stok? 2) Ruko milik sendiri atau sewa (bangunan diasuransikan pemilik?) 3) Mau target 3 atau 6 bulan?

**Nilai: 8/10.** Prioritas jelas lewat skor, kekurangan kas & cicilan dihitung pasti, tanpa merek, BPJS tanpa tarif karangan, ada cek OJK. Kekurangan: gempa (kemungkinan 1, dampak 4) otomatis "Tidak" asuransi padahal kerugian besar-jarang adalah kasus klasik asuransi (aturan script: skor ≤ 4 selalu "Terima"); baris cedera kerja "Tidak perlu" bersebelahan dengan BPJS yang wajib bisa membingungkan.

## Kesimpulan A/B
Dengan skill jelas lebih baik (+1,5): tabel berprioritas, keputusan asuransi per risiko, kekurangan dana dan cicilan dihitung, tanpa tarif BPJS dari ingatan. Selisih tidak dramatis karena model dasar sudah menjawab cukup baik.

### Kalimat sebelum/sesudah untuk README
Tanpa skill: daftar risiko umum dan "dana darurat 47–95 juta". Dengan skill: 9 risiko diberi skor & keputusan asuransi masing-masing, plus "kurang Rp39.400.000, sisihkan Rp3.283.334/bulan selama 12 bulan".
