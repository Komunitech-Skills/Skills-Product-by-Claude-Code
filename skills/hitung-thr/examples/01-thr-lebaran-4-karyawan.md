# 01 — THR Lebaran untuk 4 karyawan campuran (diperbarui v1.0.1)

**Skenario:** S1 — permintaan normal: karyawan tetap lama, kontrak baru, tukang harian lepas, dan karyawan yang di-PHK 18 hari sebelum Lebaran.

**Input pengguna (persis):**
> Lebaran tahun depan 10 Maret 2027 (Idul Fitri 1448 H). Tolong hitung THR karyawan CV Contoh Maju Jaya:
> - Budi, tetap, K/1, gapok 5 jt + tunjangan tetap 500 rb, kerja sejak Juli 2019. Gaji bruto bulan Maret biasanya 5.960.000.
> - Rina, kontrak, TK/0, gaji 4,8 jt, masuk 15 Juni 2026.
> - Joko, tukang harian lepas sejak 5 Januari 2026, upah per bulan beda-beda (data 12 bulan terakhir saya lampirkan).
> - Wati, tetap, TK/1, gaji 5,2 jt, kerja sejak Februari 2021, kena PHK tanggal 20 Februari 2027.
> Sekalian buatin pengumumannya.

**Langkah agent:** menyusun CSV:
```
nama;jabatan;jenis;ptkp;gaji_pokok;tunjangan_tetap;tanggal_mulai;bruto_bulan_bayar;upah_bulanan;tanggal_berhenti
Contoh Budi;Staf Gudang;tetap;K/1;5.000.000;500.000;2019-07-01;5.960.000;;
Contoh Rina;Admin;kontrak;TK/0;4.800.000;;2026-06-15;;;
Contoh Joko;Tukang;harian;TK/0;;;2026-01-05;;3jt+3,2jt+2,8jt+3jt+3,1jt+2,9jt+3jt+3jt+3,2jt+3jt+2,9jt+3jt;
Contoh Wati;Kasir;tetap;TK/1;5.200.000;;2021-02-01;;;2027-02-20
```
Perintah: `python3 scripts/thr.py --hari-raya 2027-03-10 --nama-hari-raya "Idul Fitri 1448 H" --perusahaan "CV Contoh Maju Jaya" --data karyawan.csv --csv rekap-thr.csv`

**Output (script v1.0.1):**

**Rincian THR Idul Fitri 1448 H — CV Contoh Maju Jaya**
Hari raya: Rabu, 10 Maret 2027 · **Batas bayar (H-7): Rabu, 3 Maret 2027** · Rencana bayar: Rabu, 3 Maret 2027

| Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR | PPh 21 karena THR | THR diterima |
|---|---|---:|---:|---|---:|---:|---:|
| Contoh Budi | Tetap (PKWTT) | 92 bln | Rp 5.500.000 | masa kerja ≥ 12 bulan → 1 × upah | **Rp 5.500.000** | Rp 286.500 | Rp 5.213.500 |
| Contoh Rina | Kontrak (PKWT) | 8 bln | Rp 4.800.000 | 8/12 × upah | **Rp 3.200.000** | Rp 120.000 | Rp 3.080.000 |
| Contoh Joko | Harian lepas | 14 bln | Rp 3.008.333 | masa kerja ≥ 12 bulan → 1 × upah | **Rp 3.008.333** | – | Rp 3.008.333 |
| Contoh Wati | Tetap (PKWTT) | 72 bln | Rp 5.200.000 | masa kerja ≥ 12 bulan → 1 × upah | **Rp 5.200.000** | Rp 260.000 | Rp 4.940.000 |
| **Total** | | | | | **Rp 16.908.333** | **Rp 666.500** | **Rp 16.241.833** |

- Contoh Budi: PPh 21 bulan THR dibayar (TER B) = 2,5% × (Rp 5.960.000 + THR Rp 5.500.000) = Rp 286.500; tanpa THR 0% × Rp 5.960.000 = Rp 0 → tambahan Rp 286.500.
- Contoh Rina: PPh 21 bulan THR dibayar (TER A) = 1,5% × (Rp 4.800.000 + THR Rp 3.200.000) = Rp 120.000; tanpa THR 0% × Rp 4.800.000 = Rp 0 → tambahan Rp 120.000.
- Contoh Joko: Pekerja harian/satuan: PPh 21 memakai aturan pegawai tidak tetap (TER harian atau TER bulanan bila dibayar bulanan) — hitung dengan skill pph21-ter.
- Contoh Wati: PHK 18 hari sebelum hari raya (≤ 30 hari) — tetap berhak THR (Permenaker 6/2016 Pasal 7 ayat 1).
- Contoh Wati: THR dibayar setelah bulan berhenti bekerja → berstatus Mantan Pegawai: PPh 21 = tarif Pasal 17 × bruto THR = Rp 260.000 (PMK 168/2023 Pasal 16 ayat 6), bukan TER.

⚠️ Peringatan:
- Contoh Rina: bruto gaji bulan THR dibayar tidak diisi; dipakai gaji pokok + tunjangan tetap (belum termasuk lembur, tunjangan tidak tetap, premi JKK/JKM/BPJS Kesehatan). Isi bruto_bulan_bayar agar PPh 21 tepat.

Catatan:
- THR wajib dibayar penuh (tidak dicicil) paling lambat 7 hari sebelum hari raya. Terlambat: denda 5% dari total THR, dan THR tetap wajib dibayar (Permenaker 6/2016 Pasal 10).
- THR bukan dasar iuran BPJS (iuran dihitung dari upah pokok + tunjangan tetap).
- 'Tambahan PPh 21' = selisih PPh 21 bulan itu dengan dan tanpa THR (THR digabung ke bruto bulan dibayar, tarif TER bisa naik). Di Desember semua dihitung ulang setahun.
- Pembulatan: THR ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax).
- Masa kerja dihitung dalam bulan penuh sampai tanggal hari raya (asumsi skill; aturan tidak mengatur pecahan bulan). Ubah dengan kolom masa_kerja_bulan bila perusahaan memakai cara lain.

File rekap: rekap-thr.csv

**Draf pengumuman untuk karyawan (siap kirim WA/email):**

```
Yth. Rekan-rekan karyawan CV Contoh Maju Jaya,

Menyambut Idul Fitri 1448 H, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan pada Rabu, 3 Maret 2027 (paling lambat Rabu, 3 Maret 2027, yaitu 7 hari sebelum hari raya).

Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026):
• Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
• Masa kerja 1 bulan s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
• THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.

Rincian THR masing-masing akan disampaikan secara pribadi. Jika ada pertanyaan, silakan hubungi bagian HR/keuangan.

Selamat menyambut hari raya. Terima kasih atas kerja keras Bapak/Ibu.

Salam,
Manajemen CV Contoh Maju Jaya
```

_Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Permenaker 6/2016, SE Menaker M/3/HK.04.00/III/2026, PP 58/2023 & PMK 168/2023 (PPh 21 TER), berlaku per 23 September 2026. Untuk sengketa/kasus khusus hubungi Disnaker setempat, Posko THR (poskothr.kemnaker.go.id), Kring Pajak 1500200, atau konsultan._

**Catatan penguji:**
- Besaran THR diverifikasi dengan kalkulator independen penguji (dari teks Permenaker 6/2016 Pasal 2–4 & 7 dan SE Menaker M/3/HK.04.00/III/2026 yang dibaca langsung dari pindaian JDIH): Budi Rp 5.500.000, Rina 8/12 × 4,8 jt = Rp 3.200.000, Joko rata-rata 12 bulan terakhir Rp 3.008.333 (masa kerja 14 bulan ≥ 12), Wati Rp 5.200.000 (PHK ≤ 30 hari, PKWTT) — **cocok**.
- Tambahan PPh 21 Budi Rp 286.500 dan Rina Rp 120.000 benar (TER B 2,5% × 11,46 jt; TER A 1,5% × 8 jt).
- v1.0.1: Wati sudah berhenti 20 Februari dan THR dibayar 3 Maret, jadi saat dibayar ia **Mantan Pegawai**. Script kini memakai tarif Pasal 17 × bruto THR (PMK 168/2023 Pasal 12 ayat 8 & Pasal 16 ayat 6; contoh resmi Tuan O) = 5% × Rp 5,2 jt = **Rp 260.000**, bukan TER + gaji fiktif. Diverifikasi: kasus gaji Rp 20 jt kini Rp 1.000.000 (v1.0.0: Rp 4.600.000); analog Tuan O (Rp 60 jt) Rp 3.000.000 sama dengan contoh resmi.
- Pengumuman tanpa nominal pribadi, siap kirim. Bagus.
