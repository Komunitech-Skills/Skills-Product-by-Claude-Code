---
name: hitung-thr
description: Menghitung THR Keagamaan per karyawan sesuai Permenaker 6/2016 dan SE Menaker THR 2026 (1 bulan upah untuk masa kerja ≥12 bulan, proporsional masa kerja/12 bila kurang, harian lepas & satuan hasil pakai rata-rata upah), batas bayar H-7, tambahan potongan PPh 21 TER di bulan THR dibayar, total THR, dan draf pengumuman untuk karyawan. Gunakan saat pengguna tanya "hitung THR", "THR Lebaran/Natal", "THR karyawan baru/kontrak/harian", atau holiday allowance, THR calculation Indonesia. Untuk slip gaji bulanan pakai slip-gaji-bpjs; untuk PPh 21 setahun pakai pph21-ter.
---

# Hitung THR Keagamaan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menghitung THR setiap karyawan dengan benar menurut aturan, termasuk karyawan baru, kontrak, dan harian lepas; menunjukkan batas bayar H-7 dan tambahan potongan PPh 21-nya; lalu menyiapkan pengumuman THR yang siap dikirim.

## Kapan digunakan
- "Hitung THR Lebaran untuk 8 karyawan saya."
- "Karyawan baru masuk Juni, THR-nya berapa?" / "Masa kerja 11 bulan dapat THR penuh?"
- "THR tukang harian yang upahnya beda-beda tiap bulan?"
- "Kapan paling lambat bayar THR? Buatkan pengumumannya."

## Kapan TIDAK digunakan
- Slip gaji bulanan lengkap → `slip-gaji-bpjs`. PPh 21 setahun/Desember → `pph21-ter`.
- Bonus/insentif kinerja, THR ASN/PNS, pesangon/PHK → jelaskan di luar cakupan dan arahkan ke Disnaker/konsultan.
- Menentukan tanggal hari raya → minta pengguna menyebutkan tanggal resmi (SKB libur nasional); skill tidak menebak tanggal.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Tanggal hari raya & namanya (Idul Fitri, Natal, Nyepi, Waisak, Imlek) | Ya | — (tanyakan) |
| Per karyawan: nama, tanggal mulai kerja (atau masa kerja dalam bulan) | Ya | — (tanyakan) |
| Gaji pokok + tunjangan tetap (tetap/kontrak) atau upah tiap bulan (harian lepas/satuan hasil) | Ya | — (tanyakan) |
| Status: tetap (PKWTT), kontrak (PKWT), harian, satuan | Tidak | Tetap |
| Status PTKP (untuk PPh 21) | Tidak | PPh 21 tidak dihitung — sebutkan |
| Total gaji bruto bulan THR dibayar (gaji + tunjangan + premi BPJS perusahaan) | Tidak | Perkiraan gaji pokok + tunjangan tetap, beri peringatan |
| Rencana tanggal bayar | Tidak | Batas H-7 |
| THR menurut kebijakan perusahaan (bila lebih besar) | Tidak | Minimum aturan |
| Tanggal berhenti (bila keluar sebelum hari raya) | Tidak | Masih bekerja |
| Sektor/KLU untuk PPh 21 DTP 2026 | Hanya bila THR dibayar tahun 2026 dan gaji tetap ≤ Rp 10 jt | Tanyakan; jangan diasumsikan |
| Bruto tetap & teratur Januari 2026/bulan pertama kerja (`bruto_tetap_januari`, syarat DTP ≤ Rp 10 jt) | Bila `dtp=ya` | Gaji pokok + tunjangan tetap, dengan peringatan |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna ingin cepat, pakai default dan sebutkan asumsinya.

## Langkah kerja
1. Susun data karyawan (lihat `templates/karyawan-thr-contoh.csv`; pemisah `;` atau `,`). Kolom: `nama` (wajib), `jenis`, `ptkp`, `gaji_pokok`, `tunjangan_tetap`, `tanggal_mulai` atau `masa_kerja_bulan`, `upah_bulanan` (harian/satuan: upah tiap bulan urut dari terlama, dipisah `+`, mis. `3jt+3,2jt+2,8jt`), `bruto_bulan_bayar`, `thr_kebijakan`, `tanggal_berhenti`, `dtp` (ya/tidak; script menolak otomatis bila THR tidak dibayar di tahun 2026 atau `bruto_tetap_januari` > Rp 10 jt), `bruto_tetap_januari`, `jabatan`.
   **Data gaji = data pribadi sensitif:** tulis CSV karyawan dan `--csv` rekap di **folder kerja yang disepakati dengan pengguna** (mis. folder kerja OpenClaw/agent atau folder yang ia sebut), **bukan `/tmp`** atau folder sementara lain; sebutkan path lengkapnya.
2. Jalankan (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/thr.py --hari-raya 2027-03-10 --nama-hari-raya "Idul Fitri 1448 H" --perusahaan "CV Maju Jaya" --data karyawan.csv --csv rekap-thr.csv
   ```
   Satu karyawan: `--nama Budi --ptkp K/1 --gaji-pokok 5jt --tunjangan-tetap 500rb --mulai 2026-06-15`. Opsi: `--tanggal-bayar`, `--format json`.
3. Tampilkan tabel rincian dari script, batas bayar H-7, catatan per karyawan, semua ⚠️ peringatan, lalu draf pengumuman. Rincian nominal per orang bersifat pribadi — jangan dimasukkan ke pengumuman grup. Sebutkan lokasi file rekap; bila CSV input dibuat oleh agent dari data chat, **tawarkan untuk menghapusnya** setelah selesai (hapus hanya bila pengguna setuju). Jangan menawarkan kirim lewat WA/email bila kanal itu belum diatur pengguna.
4. Bila THR dibayar di **Desember** (mis. Natal) atau bulan karyawan berhenti, PPh 21 dihitung ulang setahun — jelaskan dan sarankan skill `pph21-ter`/`slip-gaji-bpjs`.
5. **Fallback tanpa Python:** hitung manual dengan rumus di bawah (tabel TER di `references/tabel-ter.md`), tulis langkahnya, dan beri tahu pengguna bahwa hasil dihitung manual.

## Rumus (untuk hitung manual)
Dasar: Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026, berlaku per 2026-09-23 (rincian: `references/regulasi.md`).
- Masa kerja = bulan penuh dari tanggal mulai sampai tanggal hari raya, **inklusif** (hari mulai dan hari raya ikut dihitung): 11 Mar 2026 s.d. 10 Mar 2027 = 12 bulan; 12 Mar 2026 s.d. 10 Mar 2027 = 11 bulan (script memberi ⚠️ bila kurang ≤ 3 hari dari bulan berikutnya). Ini konvensi skill karena aturan tidak mengatur pecahan bulan.
- < 1 bulan: tidak wajib · 1 s.d. < 12 bulan: **masa kerja ÷ 12 × upah 1 bulan** · ≥ 12 bulan: **1 × upah 1 bulan**.
- Upah 1 bulan: gaji pokok + tunjangan tetap (atau upah bersih bila tanpa tunjangan). Harian lepas: rata-rata upah 12 bulan terakhir (≥ 12 bulan) atau rata-rata per bulan selama masa kerja. Satuan hasil: rata-rata 12 bulan terakhir.
- Batas bayar = tanggal hari raya − 7 hari. Terlambat: denda 5% dari total THR (THR tetap wajib dibayar).
- PPh 21: THR digabung ke gaji bulan dibayar → PPh 21 = TER(gaji + THR) × (gaji + THR). Tambahan karena THR = hasil itu − TER(gaji) × gaji.
- Karyawan yang sudah berhenti (PHK ≤ 30 hari sebelum hari raya) dan THR dibayar **setelah bulan berhenti** berstatus Mantan Pegawai: PPh 21 = tarif Pasal 17 (5% s.d. Rp 60 jt, 15% berikutnya, dst.) × THR, bukan TER (PMK 168/2023 Pasal 16 ayat 6).
- PPh 21 DTP (PMK 105/2025) hanya bila THR dibayar di tahun 2026, sektor/KLU dikonfirmasi, dan bruto tetap Januari 2026/bulan pertama kerja ≤ Rp 10 jt.
- Pembulatan: THR ke rupiah terdekat; PPh 21 ke bawah (belum dicocokkan dengan Coretax).

## Format output
```
**Rincian THR <Hari Raya> — <Perusahaan>**
Hari raya: <tanggal> · Batas bayar (H-7): <tanggal> · Rencana bayar: <tanggal>
| Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR | Tambahan PPh 21 | THR diterima |
| **Total** | ... |
Catatan per karyawan (PHK ≤30 hari, tidak berhak, rincian PPh 21)
⚠️ Peringatan · Asumsi
**Draf pengumuman untuk karyawan** (tanpa nominal pribadi)
_Disclaimer + dasar aturan + tanggal berlaku_
```

## Contoh
**Input pengguna:** "Lebaran 10 Maret 2027. Budi (K/1) gaji pokok 5 juta + tunjangan tetap 500 ribu, kerja sejak 2019, bruto gaji Maret 5.960.000. Rina (TK/0) kontrak gaji 4,8 juta, masuk 15 Juni 2026."

**Output (ringkas, dari script):** Batas bayar Rabu, 3 Maret 2027. Budi 92 bulan → THR Rp 5.500.000; PPh 21 Maret TER B 2,5% × Rp 11.460.000 = Rp 286.500 (tanpa THR Rp 0) → tambahan Rp 286.500. Rina 8 bulan → 8/12 × Rp 4.800.000 = Rp 3.200.000; tambahan PPh 21 Rp 120.000 (TER A 1,5% × Rp 8.000.000). Total THR Rp 8.700.000. Lalu draf pengumuman.

## Checklist sebelum mengirim hasil
- [ ] Angka dari script (atau ditandai "dihitung manual").
- [ ] Masa kerja 11 vs 12 bulan dicek teliti (12 bulan = THR penuh).
- [ ] Komponen upah hanya gaji pokok + tunjangan tetap (bukan uang makan/transport harian yang tidak tetap).
- [ ] Batas H-7 disebut; peringatan keterlambatan/denda bila relevan.
- [ ] PPh 21 Desember diarahkan ke hitung ulang setahun; mantan pegawai memakai Pasal 17 × THR.
- [ ] DTP hanya bila dibayar tahun 2026, sektor dikonfirmasi, dan bruto tetap Januari ≤ Rp 10 jt.
- [ ] Pengumuman tanpa nominal pribadi; disclaimer ada.

## Batasan & penanganan error
- Kode keluar 2 + `ERROR:` untuk tanggal salah format, tanggal mulai setelah hari raya, jenis pekerja tak dikenal, angka rusak, PTKP salah, atau upah harian kosong. Sampaikan dengan bahasa sederhana.
- Perusahaan yang memakai cara hitung masa kerja lain (mis. per hari) dapat mengisi `masa_kerja_bulan` sendiri (boleh desimal).
- Pekerja pindahan grup dengan masa kerja berlanjut, THR bagi pekerja yang cuti panjang/diskors, dan sengketa THR → arahkan ke Disnaker atau Posko THR (poskothr.kemnaker.go.id).
- Uji otomatis: `python3 <folder-skill-ini>/scripts/test_thr.py`.
