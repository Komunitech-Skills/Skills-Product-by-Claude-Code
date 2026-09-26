# Contoh sesi (pembuat): toko bangunan 4 karyawan, gaji September 2026 + revisi

> Contoh dari pembuat skill, bukan hasil uji independen. Semua data fiktif. Perintah dijalankan sungguhan dengan
> `scripts/gaji.py` pada 26 September 2026 (database di folder sementara). Keluaran dipotong seperlunya; angka apa adanya.

## Data
`karyawan.csv` (pemisah `;`):
```
kode;nama;jabatan;jenis;ptkp;gaji_pokok;tunjangan_tetap;tunjangan_tidak_tetap;bpjs;hari_kerja;masuk;nik;bank;rekening;kode_absensi
K001;Andi Saputra;Kepala Gudang;tetap;K/1;6.000.000;750.000;400.000;kes,tk,jp;6;2019-03-01;3201010101010001;BCA;1234567890;A01
K002;Sari Wulandari;Kasir;tetap;TK/0;4.000.000;;300.000;kes,tk,jp;6;2024-02-01;;BRI;002101000123456;A02
K003;Joko Prasetyo;Sopir;kontrak;K/2;3.800.000;200.000;500.000;kes,tk;6;2026-01-05;;Mandiri;1300012345678;A03
K004;Rina Marlina;Admin;tetap;TK/1;5.000.000;500.000;;semua;5;2022-07-11;;BCA;9876543210;A04
```
`absensi-sep.csv` = file `rekap --csv-gaji` dari skill absensi-lokal (Andi lembur 2 + 1,5 jam hari kerja & 7 jam hari Minggu; Joko 3 jam; Sari alpa 2 hari).

## Percakapan
**Pemilik:** "Pakai aplikasi gaji untuk toko saya, UMK sini 3,5 juta, JKK kami 0,54%, gajian tiap tanggal 28. Ini data karyawannya."

**Agent:** `init --nama-usaha ... --ya` (setelah setuju), `atur --umk 3.500.000 --jkk 0,54 --tanggal-gajian 28`, `karyawan impor karyawan.csv` → pratinjau 4 karyawan (NIK tampil `************0001`, rekening `******7890`) → "ya" → `--ya`.

**Pemilik:** "Gaji September: Sari kasbon 250 ribu, Rina bonus sejuta. Lembur ambil dari file absensi ini."

**Agent:** `impor-absensi absensi-sep.csv --bulan 2026-09`:
```
PRATINJAU (belum disimpan):
Impor rekap absensi September 2026 (4 karyawan):
- Andi Saputra: lembur hari kerja 2+1,5 | hari libur 7 | hadir 25, alpa 0
- Sari Wulandari: lembur hari kerja - | hari libur - | hadir 23, alpa 2
- Joko Prasetyo: lembur hari kerja 3 | hari libur - | hadir 25, alpa 0
- Rina Marlina: lembur hari kerja - | hari libur - | hadir 21, alpa 0

Catatan: Sari Wulandari: 2 hari alpa TIDAK dipotong otomatis (aturan potongan belum diatur). ...
```
→ "ya" → `--ya`; `isi --bulan 2026-09 --karyawan Sari --kasbon 250rb`; `isi --bulan 2026-09 --karyawan K004 --bonus 1jt`; `hitung --bulan 2026-09`:
```
REKAP GAJI SEPTEMBER 2026 - Toko Bangunan Sumber Rejeki (fiktif)
Status: DRAF (belum final) | 4 karyawan

| Kode | Nama | Pendapatan | Potongan | PPh 21 | Gaji bersih | Biaya perusahaan |
|---|---|---:|---:|---:|---:|---:|
| K001 | Andi Saputra | Rp 7.930.347 | Rp 352.570 | Rp 82.570 | Rp 7.577.777 | Rp 8.641.797 |
| K002 | Sari Wulandari | Rp 4.300.000 | Rp 410.000 | Rp 0 | Rp 3.890.000 | Rp 4.721.600 |
| K003 | Joko Prasetyo | Rp 4.627.168 | Rp 120.000 | Rp 0 | Rp 4.507.168 | Rp 4.968.768 |
| K004 | Rina Marlina | Rp 6.500.000 | Rp 304.577 | Rp 84.577 | Rp 6.195.423 | Rp 7.079.700 |
| | **Total** | **Rp 23.357.515** | **Rp 1.187.147** | **Rp 167.147** | **Rp 22.170.368** | **Rp 25.411.865** |

Yang harus dibayar/disetor:
- Transfer gaji bersih ke karyawan: Rp 22.170.368
- Setor BPJS Kesehatan (4% perusahaan + 1% karyawan): Rp 1.012.500
- Setor BPJS Ketenagakerjaan (JHT, JKK, JKM, JP): Rp 1.811.850
- Setor PPh 21: Rp 167.147
- Total biaya gaji perusahaan: Rp 25.411.865
```
"Sudah benar? Kalau ya, saya kunci periode September."

**Pemilik:** "Ya, kunci. Buatkan slip dan file transfernya."

**Agent:** `final --bulan 2026-09 --ya`, `slip --bulan 2026-09` (4 file `slip-2026-09-K00x.md`), `transfer --bulan 2026-09` → `transfer-gaji-2026-09.csv`, 4 penerima, total Rp 22.170.368, nomor rekening disamarkan. "Kirim slip ke masing-masing karyawan, jangan ke grup."

**Pemilik (3 hari kemudian):** "Bonus Andi 500 ribu kelupaan."

**Agent:** "September sudah dikunci; perubahan harus lewat revisi tercatat." `revisi --bulan 2026-09 --alasan "bonus Andi Rp 500.000 terlewat"` → pratinjau → "ya" → `--ya`; `isi --bulan 2026-09 --karyawan Andi --bonus 500rb`; `hitung`; `final --ya`:
```
Perubahan dibanding versi final sebelumnya (revisi ke-0):
- K001 Andi Saputra: gaji bersih Rp 7.577.777 -> Rp 8.072.777 (+Rp 495.000); pph21 Rp 82.570 -> Rp 87.570 (+Rp 5.000); biaya perusahaan Rp 8.641.797 -> Rp 9.141.797 (+Rp 500.000); ...
```
`transfer --bulan 2026-09` → `transfer-selisih-2026-09-rev1.csv`: 1 penerima, Rp 495.000 ("Kekurangan gaji September 2026 (revisi 1)").

**Pemilik:** "Oktober nanti ingatkan saya setoran-setorannya."

**Agent:** `pengingat --hari-ini 2026-10-08 --rentang 14` (untuk jadwal harian lihat `references/openclaw-jadwal.md`):
```
- Sab 10/10/2026: Batas setor iuran BPJS Kesehatan (tgl 10 setiap bulan, Perpres 82/2018 Pasal 39): perkiraan Rp 1.012.500 ...
- Kam 15/10/2026: Batas setor iuran BPJS Ketenagakerjaan masa September 2026 (...): Rp 1.811.850 (periode September 2026 final)
- Kam 15/10/2026: Batas setor PPh 21 masa September 2026 (...): Rp 172.147 (periode September 2026 final)
- Sel 20/10/2026: Batas lapor SPT Masa PPh 21 masa September 2026 (...)
```

## Cek angka manual (pembuat)
- **Andi** (pola 6 hari): upah lembur = gaji pokok + tunjangan tetap Rp 6.750.000 (tunjangan tidak tetap Rp 400.000; 75% dari total Rp 7.150.000 lebih kecil, jadi tidak dipakai). Jam setara: 2 jam → 1,5 + 2 = 3,5; 1,5 jam → 1,5 + 2 × 0,5 = 2,5; 7 jam hari Minggu → 7 × 2 = 14; total 20 × 6.750.000 ÷ 173 = 780.346,8 → **Rp 780.347**. Bruto pajak = 7.930.347 + JKK 36.450 + JKM 20.250 + BPJS Kes 4% 270.000 = 8.257.047; TER B 1% → **Rp 82.570**.
- **Joko** (tanpa JP): 3 jam → 1,5 + 2 + 2 = 5,5 × 4.000.000 ÷ 173 = 127.167,6 → Rp 127.168; potongan = BPJS Kes 1% 40.000 + JHT 2% 80.000 = **Rp 120.000**; bruto pajak 4.820.768 → TER B 0%.
- **Rina**: bruto pajak 6.500.000 + 29.700 + 16.500 + 220.000 = 6.766.200 → TER A 1,25% = 84.577,5 → **Rp 84.577** (dibulatkan ke bawah).

Semua cocok dengan keluaran script.
