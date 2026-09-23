# 01 — Bengkel las, KUR Mikro Rp 100 juta 5 tahun (paket lengkap)

**Skenario:** S1 — permintaan normal lengkap. Semua nama/nomor fiktif.

**Input pengguna (persis):**
> Saya punya bengkel las "Las Contoh Jaya" di Bekasi, udah jalan 4 tahun, punya NIB, karyawan 3 orang. Laba bersih sekitar 6 juta sebulan. Mau ajukan KUR BRI 100 juta 5 tahun buat beli mesin las & mesin bending 70 juta sama stok besi 30 juta. Tolong siapin semua yang perlu, sama cicilannya berapa, kuat nggak saya?

Perintah yang dijalankan (langkah 1):
```bash
python3 scripts/simulasi_kur.py --plafon 100jt --tenor 60 --kur --sektor produksi --akad-ke 1 \
  --penggunaan investasi --laba-bersih "6 juta" --rincian-dana "Mesin las & bending=70jt; Stok besi=30jt"
```

## Output (mengikuti SKILL.md)

## Persiapan Pengajuan KUR — Las Contoh Jaya
⚠️ Suku bunga **6% efektif/tahun = ACUAN Permenko Perekonomian 1/2026 Pasal 37** (KUR Mikro, sektor produksi — bengkel las termasuk sektor produksi karena bukan perdagangan) — **konfirmasi ke bank penyalur**.

### 1. Simulasi cicilan (Rp 100.000.000, 60 bulan)
| | Anuitas (efektif) — yang berlaku untuk KUR | Flat 6% (ilustrasi) |
|---|---:|---:|
| Cicilan/bulan | **Rp 1.933.280** | Rp 2.166.667 |
| Total bunga | Rp 15.996.809 | Rp 30.000.000 |
| Total dibayar | Rp 115.996.809 | Rp 130.000.000 |

Anuitas: cicilan tetap, bunga dihitung dari **sisa** pinjaman sehingga porsi bunga makin kecil. Kalau angka 6% itu dihitung **flat** (bunga selalu dari 100 juta), total bunganya Rp 30 juta — **Rp 14.003.191 lebih mahal**, setara bunga efektif ±10,85%. Untuk KUR, bunga flat yang setara dengan 6% efektif (60 bulan) hanya **±3,2%/tahun**. Jadi kalau petugas menyebut "flat 6%", minta penjelasan dan **tabel angsuran resmi**.

### 2. Kemampuan bayar
Laba bersih Rp 6.000.000/bulan → cicilan **32,2%** dari laba → 🟡 **BERAT, perlu hati-hati**. Sisa laba Rp 4.066.720/bulan.

⚠️ Cicilan sedikit di atas batas aman 30% yang dipakai skill ini (panduan umum, bukan aturan bank). Pilihan:
- **Turunkan plafon ke ± Rp 93.106.000** (cicilan ≤ 30% laba), mis. mesin 70 jt + stok 23 jt.
- Ajukan stok besi belakangan / bertahap setelah mesin baru menambah omzet.
- Pastikan laba 6 juta itu **sudah dikurangi** kebutuhan rumah tangga yang diambil dari bengkel; kalau belum, hitung ulang — hasilnya bisa lebih berat.
- Tenor tidak bisa diperpanjang lagi: 60 bulan sudah batas awal KUR Mikro investasi (Pasal 38).

### 3. Rencana penggunaan dana
| Pos | Nominal | % | Jenis |
|---|---:|---:|---|
| Mesin las & mesin bending | Rp 70.000.000 | 70,0% | Investasi |
| Stok besi | Rp 30.000.000 | 30,0% | Modal kerja |
| **Total** | **Rp 100.000.000** | 100% | = plafon ✔ |

⚠️ Stok besi adalah **modal kerja**; batas awal tenor KUR Mikro modal kerja **3 tahun (36 bulan)**, investasi 5 tahun (Pasal 38). Tanyakan ke bank apakah pinjaman dipecah (investasi 60 bulan + modal kerja ≤ 36 bulan) atau digabung. Siapkan penawaran harga/proforma mesin.

### 4. Profil usaha (siap salin)
```
PROFIL USAHA
Nama usaha      : Las Contoh Jaya
Pemilik         : [isi: nama pemilik]
Alamat usaha    : [isi: alamat lengkap], Bekasi
Bidang usaha    : Produksi/jasa — bengkel las
Mulai berjalan  : ± 4 tahun ([isi: bulan/tahun mulai])
Legalitas       : NIB [isi: nomor NIB]
Karyawan        : 3 orang

Gambaran usaha
Las Contoh Jaya adalah bengkel las di Bekasi yang melayani [isi: jenis pekerjaan, mis. pagar, kanopi, teralis] untuk pelanggan [isi: rumah tangga/kontraktor/toko]. Pesanan diterima melalui [isi: datang langsung/WhatsApp/kontraktor]. Omzet rata-rata [isi: Rp … per bulan] dengan laba bersih sekitar Rp 6.000.000 per bulan (berdasarkan [isi: catatan/pembukuan …]).

Keunggulan & peluang
[isi: pelanggan tetap, pesanan yang tertunda karena alat terbatas, dsb.]

Kebutuhan dana
Pinjaman Rp 100.000.000 untuk mesin las & mesin bending (Rp 70.000.000) dan stok besi (Rp 30.000.000). Pemilik memperkirakan dana ini meningkatkan [isi: kapasitas/pesanan] sebesar [isi: perkiraan].

Kemampuan membayar
Dengan laba bersih Rp 6.000.000 per bulan dan perkiraan cicilan Rp 1.933.280 (simulasi anuitas 6% efektif, 60 bulan), porsi cicilan sekitar 32,2% dari laba bersih.
```

### 5. Checklist dokumen
**Syarat inti [Permenko 1/2026 Pasal 34]**
- [ ] KTP-el pemohon (NIK)
- [ ] NIB (sudah ada ✔) atau surat keterangan usaha
- [ ] Usaha berjalan ≥ 6 bulan (4 tahun ✔)
- [ ] **NPWP — wajib**, karena pinjaman > Rp50 juta (Pasal 34 ayat 1 huruf d)
- [ ] Belum pernah menerima kredit **komersial** produktif (kecuali yang dikecualikan: kredit konsumsi rumah tangga, ultra mikro ≤ Rp20 jt, pinjaman fintech)

**Umum diminta bank (cek ke bank penyalur):** Kartu Keluarga; KTP pasangan & surat nikah (bila menikah); pas foto; foto bengkel & hasil kerja; catatan penjualan 6–12 bulan; mutasi rekening 3–6 bulan; penawaran harga mesin.

**Hak Anda:** plafon ≤ Rp100 juta → bank **tidak boleh** meminta agunan tambahan di luar usaha/objek yang dibiayai (Pasal 20 ayat 1). Uang yang cair harus **sama** dengan nilai di akad (Pasal 13 ayat 2). Tolak siapa pun yang menjanjikan "pasti cair" dengan imbalan.

### 6. Langkah berikutnya
1. Cek SLIK OJK Anda sendiri (layanan resmi OJK), pastikan kolektibilitas lancar.
2. Lengkapi NPWP & dokumen di atas, datangi unit BRI (atau bank penyalur lain) terdekat.
3. Minta **tabel angsuran resmi** dan rincian biaya (asuransi, materai, notaris); tanyakan skema investasi vs modal kerja.
4. Pertimbangkan plafon ± Rp 93 juta agar cicilan tetap di zona aman.

Catatan: Simulasi ini bukan penawaran atau jaminan persetujuan kredit. Keputusan & angka final ada di bank.
Dasar: Permenko Perekonomian 1/2026 (dicek per 2026-09-23). Ketentuan dapat berubah — konfirmasi ke bank penyalur.

## Catatan penguji
- ✅ Angka diverifikasi independen (`/tmp/uji-pengajuan-kur/verif.py`, rumus float terpisah): anuitas 1.933.280,15 → Rp 1.933.280; total bunga Rp 15.996.809; flat Rp 2.166.667; efektif setara flat 10,85%; flat setara acuan 3,20%; rasio 32,2%; plafon maks Rp 93.106.000 — **semua cocok**.
- ✅ Fakta Permenko dicek ke teks Pasal 20, 34, 37, 38 (DDTC) — benar.
- ✅ Tidak ada janji persetujuan; label bunga "acuan … konfirmasi ke bank" ada.
- ⚠ Penggunaan campuran (investasi + modal kerja) tidak ditangani script (`--penggunaan` hanya satu nilai); peringatan tenor modal kerja di atas ditambahkan agent dari `regulasi.md`, bukan otomatis.
