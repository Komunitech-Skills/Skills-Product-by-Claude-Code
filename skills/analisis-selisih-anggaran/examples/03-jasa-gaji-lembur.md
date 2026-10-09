# 03 — Jasa kebersihan, bulanan, gaji & lembur (efek jumlah vs tarif)

> Contoh pembuat skill (v1.0.0). Angka dari `scripts/selisih.py --file examples/data/03-jasa-kebersihan-agustus.csv --periode "Agustus 2026" --format teks`; diverifikasi ulang terpisah di `tests/uji_selisih.py` kasus E1–E4 (lembur: 260 jam × Rp25.000 = Rp6.500.000; Rp1.500 × 410 jam = Rp615.000).

## Pesan pengguna
"Usaha cleaning service saya, Agustus. Pendapatan kontrak 145 jt jadi 152 jt, jasa panggilan 20 jt jadi 14,5 jt. Gaji petugas tetap 20 orang @3,4 jt, sekarang 21 orang. Lembur rencana 150 jam @25 rb, realisasi 410 jam total Rp10.865.000. Bahan chemical 12 jt jadi 13,9 jt, transport 6 jt jadi 7,2 jt, BPJS 4,76 jt jadi 5 jt, sewa 4 jt. Kenapa laba turun padahal kontrak naik?"

## Contoh balasan chat
**Rekap Agustus 2026: laba Rp54.135.000 vs rencana Rp66.490.000 (−Rp12.355.000, −18,6%)**
Pendapatan justru lebih Rp1,5 jt (+0,9%), tetapi biaya naik Rp13,855 jt (+14,1%). Penyebab terbesar: lembur +Rp7,115 jt dan tambahan 1 petugas +Rp3,4 jt; jasa panggilan juga kurang Rp5,5 jt.

| Pos | Selisih | Keterangan |
|---|---|---|
| Lembur petugas | +Rp7.115.000 (+189,7%) | merugikan; terbesar |
| Pendapatan kontrak kantor | +Rp7.000.000 (+4,8%) | menguntungkan |
| Pendapatan jasa panggilan | −Rp5.500.000 (−27,5%) | merugikan |
| Gaji petugas tetap | +Rp3.400.000 (+5,0%) | merugikan; 1 orang tambahan |
| Bahan & chemical | +Rp1.900.000 (+15,8%) | merugikan |
| Transport petugas | +Rp1.200.000 (+20,0%) | merugikan |
| BPJS & tunjangan | +Rp240.000 (+5,0%) | ikut jumlah petugas |
| **Laba** | **−Rp12.355.000 (−18,6%)** | margin 40,3% → 32,5% |

**Kenapa angkanya begitu**
- **Lembur +Rp7.115.000** = jam lembur naik 150 → 410 jam (**+Rp6.500.000**) + tarif per jam naik Rp25.000 → Rp26.500 (**+Rp615.000**). Jadi masalah utamanya **jumlah jam**, bukan tarif.
- **Gaji +Rp3.400.000** = seluruhnya karena tambah 1 orang (gaji per orang tetap Rp3.400.000).
- Bahan chemical: setelah disesuaikan pendapatan (+0,9%), kelebihannya Rp1.790.909 (+14,8%).
- Catatan: lembur dan petugas tambahan naik bersamaan, padahal biasanya petugas tambahan mengurangi lembur.

**Yang perlu dicek**
1. Lembur 410 jam: untuk kontrak baru (pendapatan kontrak +Rp7 jt), petugas absen/cuti yang digantikan, atau jadwal shift yang belum pas? Apakah lembur sudah disetujui atasan per kejadian?
2. Petugas ke-21: menggantikan orang yang keluar (tumpang tindih sementara) atau penambahan permanen?
3. Jasa panggilan −27,5%: order yang turun, atau tim panggilan dipakai menutup kontrak (sehingga order ditolak)?
4. Chemical +14,8% di atas wajar: harga beli naik, atau pemakaian per lokasi naik?

**Tindakan bulan depan**
- Batas lembur, mis. maks. 200 jam/bulan, dan setiap lembur di atas 4 jam/orang/minggu perlu persetujuan.
- Susun ulang jadwal shift untuk kontrak baru sebelum menambah lembur; bandingkan biaya 1 petugas tambahan (±Rp3,4 jt + BPJS) dengan 260 jam lembur (Rp6,5 jt).
- Catat pemakaian chemical per lokasi selama 2 minggu.
- Bila kontrak baru memang butuh tenaga lebih, revisi anggaran gaji/lembur dan cek apakah harga kontrak masih menutup biayanya.

**Pesan untuk tim (siap kirim)**
> Rekap Agustus: pendapatan sesuai rencana, tapi laba kurang Rp12,4 jt karena lembur 410 jam (rencana 150) dan biaya bahan naik.
> Mulai minggu depan lembur perlu persetujuan supervisor. Supervisor tolong kirim rekap jam lembur per lokasi & alasannya sebelum Rabu.
> Terima kasih atas kerja kerasnya bulan ini.

**Asumsi:** ambang 5% atau Rp500 rb; bahan chemical dianggap ikut naik-turun dengan pendapatan (unit layanan tidak ada, jadi kenaikan harga kontrak ikut terhitung); pajak tidak dihitung.
Catatan: analisis untuk manajemen, bukan audit/nasihat keuangan; penyebab perlu dicek ke nota, rekening, dan catatan absensi.

Pertanyaan: berapa jam lembur yang terjadi di lokasi kontrak baru? Dengan itu saya bisa pisahkan lembur karena kontrak baru vs karena jadwal.
