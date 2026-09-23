# 02 — Permintaan singkat: karyawan baru

**Skenario:** S2 — permintaan malas.

**Input pengguna (persis):**
> bikinin dong thr karyawan baru masuk 1 agustus 2026 gaji 4,5jt, lebaran 10 maret 2027

**Perintah:** `python3 scripts/thr.py --hari-raya 2027-03-10 --nama-hari-raya "Idul Fitri 1448 H" --nama "Contoh Karyawan Baru" --gaji-pokok 4,5jt --mulai 2026-08-01`

**Output:**

**Rincian THR Idul Fitri 1448 H — -**
Hari raya: Rabu, 10 Maret 2027 · **Batas bayar (H-7): Rabu, 3 Maret 2027** · Rencana bayar: Rabu, 3 Maret 2027

| Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR | PPh 21 karena THR | THR diterima |
|---|---|---:|---:|---|---:|---:|---:|
| Contoh Karyawan Baru | Tetap (PKWTT) | 7 bln | Rp 4.500.000 | 7/12 × upah | **Rp 2.625.000** | – | Rp 2.625.000 |
| **Total** | | | | | **Rp 2.625.000** | **Rp 0** | **Rp 2.625.000** |

- Contoh Karyawan Baru: Status PTKP tidak diisi — PPh 21 atas THR tidak dihitung.

Catatan:
- THR wajib dibayar penuh (tidak dicicil) paling lambat 7 hari sebelum hari raya. Terlambat: denda 5% dari total THR, dan THR tetap wajib dibayar (Permenaker 6/2016 Pasal 10).
- THR bukan dasar iuran BPJS (iuran dihitung dari upah pokok + tunjangan tetap).
- 'Tambahan PPh 21' = selisih PPh 21 bulan itu dengan dan tanpa THR (THR digabung ke bruto bulan dibayar, tarif TER bisa naik). Di Desember semua dihitung ulang setahun.
- Pembulatan: THR ke rupiah terdekat; PPh 21 ke bawah ke rupiah penuh (belum dicocokkan dengan Coretax).
- Masa kerja dihitung dalam bulan penuh sampai tanggal hari raya (asumsi skill; aturan tidak mengatur pecahan bulan). Ubah dengan kolom masa_kerja_bulan bila perusahaan memakai cara lain.

**Draf pengumuman untuk karyawan (siap kirim WA/email):**

```
Yth. Rekan-rekan karyawan kami,

Menyambut Idul Fitri 1448 H, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan pada Rabu, 3 Maret 2027 (paling lambat Rabu, 3 Maret 2027, yaitu 7 hari sebelum hari raya).

Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026):
• Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
• Masa kerja 1 bulan s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
• THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.

Rincian THR masing-masing akan disampaikan secara pribadi. Jika ada pertanyaan, silakan hubungi bagian HR/keuangan.

Selamat menyambut hari raya. Terima kasih atas kerja keras Bapak/Ibu.

Salam,
Manajemen
```

_Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Permenaker 6/2016, SE Menaker M/3/HK.04.00/III/2026, PP 58/2023 & PMK 168/2023 (PPh 21 TER), berlaku per 23 September 2026. Untuk sengketa/kasus khusus hubungi Disnaker setempat, Posko THR (poskothr.kemnaker.go.id), Kring Pajak 1500200, atau konsultan._

Asumsi: karyawan tetap/kontrak dengan gaji Rp 4,5 jt = gaji pokok tanpa tunjangan tetap; status PTKP tidak disebut sehingga potongan PPh 21 atas THR belum dihitung — kirim status PTKP (mis. TK/0) dan gaji bruto bulan Maret bila ingin sekalian dihitung.

**Catatan penguji:**
- 1 Agustus 2026 → 10 Maret 2027 = 7 bulan penuh (inklusif, v1.0.1) → 7/12 × Rp 4.500.000 = **Rp 2.625.000**. Cocok.
- Permintaan singkat langsung dikerjakan dengan asumsi yang disebut. Sesuai prinsip "instan".
- Uji lanjutan penguji: bila PTKP TK/0, tambahan PPh 21 bulan Maret = TER A 1,25% × Rp 7.125.000 = Rp 89.062 (script dengan `--ptkp TK/0` memberi angka yang sama).
