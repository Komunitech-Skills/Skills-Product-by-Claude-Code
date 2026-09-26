# Skenario 01 — Kafe, laporan harian dengan keempat alat (normal)

**Penguji:** agent independen (bukan pembuat skill), 2026-09-24. Semua nama fiktif.

## Permintaan pengguna
> "Laporan usaha hari ini dong." (dikirim pemilik jam 21.30 WIB, Kamis 24 September 2026)

## Data uji (dibuat dengan script RESMI tiap alat, bukan meniru skema)
Folder sementara `<uji>/kafe/` dengan HOME palsu, `KOMUNITECH_DATA=<uji>/kafe/data`, folder kerja `<uji>/kafe/kerja`. Skill disalin ke `<uji>/skills/` (bukan `.claude/skills` repo). Script pembuat data: `siapkan_kafe.py` (scratchpad penguji).

| Alat | Isi data "Kedai Kopi Senja" |
|---|---|
| kasir-lokal | `init --pajak pbjt-belum --tarif-pbjt 10 --stok buku-stok`; 8 produk (Kopi Susu Aren 20rb, Americano 18rb, Cafe Latte 24rb, Matcha 25rb, Es Teh Lemon 10rb, Pisang Goreng Keju 15rb, Roti Bakar Srikaya 16rb, Air Mineral 5rb). 18 nota 8–24 Sep. Hari ini: buka kasir 07.00 modal 300rb, 7 nota (diskon 10%, bayar campur QRIS+tunai, transfer), **void** N-260924-0006 (salah input), **retur** 1 es teh dari N-260924-0004 (tumpah), kas keluar 25rb (es batu), tutup kasir 21.00 dengan uang fisik **kurang Rp 12.000** |
| buku-stok | 8 SKU; hanya penjualan kasir **23 Sep** yang diimpor (`ekspor --format buku-stok` → `impor-pesanan`); RTB keluar 9 porsi rusak (berjamur) `--izinkan-minus` |
| absensi-lokal | 6 karyawan pola 6 hari (Dimas, Lala, Yoga, Nisa, Fajar, Tari); file mesin 7–23 Sep diimpor; hari ini: Dimas 07.58–19.10 + lembur disetujui 2 jam, Lala masuk 08.17, Yoga 08.05–19.40 (tanpa lembur disetujui), Nisa sakit, Fajar alpa, Tari tanpa catatan |
| pengingat-follow-up | 5 item lewat `tambah`: piutang Bu Wulan 1,75 jt jatuh tempo 18/9, piutang CV Rekaan Jaya 3,2 jt hari ini, janji Supplier Susu hari ini, prospek Mas Rendi besok, piutang PLG-12 450rb tgl 30/9 |

## Perintah
```bash
cd <uji>/kafe/kerja && HOME=<uji>/kafe/home KOMUNITECH_DATA=<uji>/kafe/data TZ=Asia/Jakarta \
  python3 <uji>/skills/laporan-harian-usaha/scripts/laporan.py --sekarang 2026-09-24T21:30+07:00
```
(`--sekarang` hanya untuk mengunci waktu uji.) Kode keluar 0, waktu 0,6 detik.

## Output nyata
```
LAPORAN HARIAN USAHA
Kamis, 24 September 2026
Dibuat 2026-09-24 21:30 WIB

PENJUALAN
Omzet bersih: Rp 346.400
Uang diterima: Rp 381.040 (selisih Rp 34.640 = pajak/service yang dicatat kasir)
Nota: 6 (+1 dibatalkan) | rata-rata Rp 57.733
vs kemarin (Rab 23/9): Rp 96.000 -> naik 260,8%
vs Kamis lalu (17/9): Rp 77.000 -> naik 349,9%
Per metode bayar:
- Tunai Rp 203.100
- QRIS Rp 125.140
- Transfer Rp 52.800
Terlaris:
1. Kopi Susu Aren: 5 terjual, Rp 100.000
2. Americano: 3 terjual, Rp 48.600
3. Cafe Latte: 2 terjual, Rp 48.000
4. Pisang Goreng Keju: 3 terjual, Rp 45.000
5. Roti Bakar Srikaya: 3 terjual, Rp 44.800
Retur 1 | void 1 (-Rp 30.000)

STOK
Posisi per 2026-09-24 21:30 WIB
Minus 1 | habis 1 | menipis 1
- RTB Roti Bakar Srikaya: stok -5 (min 8) MINUS
- TEH Es Teh Lemon: stok 0 (min 10) HABIS
- MCH Matcha Latte: stok 4 (min 6) MENIPIS
Perlu restock (sampai batas minimum): RTB 13, TEH 10, MCH 2
Pesanan belum dikemas: 0

KEHADIRAN
Hadir 3 dari 6 terjadwal
Terlambat (2): Lala 08.17 (17 mnt), Yoga 08.05 (5 mnt)
Izin/sakit/cuti/dinas (1): Nisa (sakit)
Alpa: 1 (Fajar)
Belum absen (1): Tari
Lembur disetujui: Dimas 2 jam
Lembur perlu keputusan (belum disetujui):
- Yoga 24/09: pulang 19.40, 2 jam 40 menit setelah jadwal, tanpa lembur disetujui

TAGIHAN & FOLLOW-UP
Terlambat 1 | hari ini 2 | besok 1
Piutang tertunggak (terlambat + hari ini): Rp 4.950.000
- #1 piutang Rp 1.750.000, lewat 6 hari
- #2 piutang Rp 3.200.000, hari ini
- #5 janji, hari ini
- #3 prospek, besok
Nama & draf pesan: ketik "rekap pengingat".

PERLU PERHATIAN
1. Selisih kas saat tutup kasir 2026-09-24 21:00: KURANG Rp 12.000 (seharusnya Rp 478.100, dihitung Rp 466.100).
2. Ada 1 void & 1 retur (-Rp 30.000). Cek alasannya di kasir.
3. Penjualan kasir tanggal 2026-09-24 belum diimpor ke buku-stok (stok belum terpotong).
4. Stok MINUS 1 barang (RTB). Lakukan stock opname.
5. 1 kejadian pulang lewat jadwal/masuk hari libur tanpa lembur disetujui. Putuskan: catat lembur atau abaikan.
6. 1 tagihan/follow-up terlambat, piutang Rp 1.750.000.

Sumber: kasir-lokal, buku-stok, absensi-lokal, pengingat-follow-up (hanya dibaca).
```
Jawaban agent yang disimulasikan (mengikuti Langkah A): teks di atas apa adanya + "Besok: restock Roti Bakar & Es Teh, impor penjualan kasir hari ini ke buku stok, tanyakan Tari kenapa tidak masuk, putuskan jam pulang Yoga."

## Verifikasi angka independen (query SQLite read-only sendiri + hitung manual)
| Angka | Dari data mentah | Script | Cocok |
|---|---|---|---|
| Omzet bersih 24/9 | Σ `nota.netto` jual 376.400 − void 20.000 − retur 10.000 = **346.400** | 346.400 | ✅ |
| Uang diterima | Σ `nota.total` (jual 414.040, void −22.000, retur −11.000) = **381.040**; PBJT 10% = 34.640 | 381.040 / 34.640 | ✅ |
| Nota sah / rata-rata | 7 jual − 1 void = 6; 346.400 ÷ 6 = 57.733,33 → **57.733** | 6 / 57.733 | ✅ |
| Kemarin 23/9 | 2×20.000 + 2×16.000 + 24.000 = **96.000** | 96.000 | ✅ |
| Kamis lalu 17/9 | 2×18.000 + 16.000 + 20.000 + 5.000 = **77.000** | 77.000 | ✅ |
| % vs kemarin | 250.400 ÷ 96.000 × 100 = 260,833… → **260,8** | 260,8% | ✅ |
| % vs Kamis lalu | 269.400 ÷ 77.000 × 100 = 349,870… → **349,9** | 349,9% | ✅ |
| Per metode | Tunai: 60.500+33.000+37.000+22.000+83.600−22.000−11.000 = **203.100**; QRIS 85.140+40.000 = **125.140**; Transfer **52.800** | sama | ✅ |
| Terlaris RTB | 2×16.000 − diskon 10% = 28.800 + 16.000 = **44.800** | 44.800 | ✅ |
| Selisih kas | 300.000 + 203.100 − 25.000 = 478.100; fisik 466.100 → **−12.000** (tabel `sesi`) | KURANG 12.000 | ✅ |
| Stok RTB | 6 − 2 (impor 23/9) − 9 rusak = **−5**; restock 8 − (−5) = **13** | −5 / 13 | ✅ |
| TEH / MCH | 0 (min 10) → 10; 4 (min 6) → 2; LTE 11 > min 10 tidak masuk | sama | ✅ |
| Belum diimpor | tabel `pesanan` hanya `N-260923-000x`; tidak ada `N-260924-%` | ditandai | ✅ |
| Kehadiran | shift REG 08.00: Lala 17 mnt, Yoga 5 mnt (toleransi 0); Yoga pulang 19.40 = 2 j 40 m lewat 17.00 | sama | ✅ |
| Tagihan | Bu Wulan 18/9 → lewat 6 hari; 1.750.000 + 3.200.000 = **4.950.000**; PLG-12 (30/9) hanya dihitung di `tujuh_hari_ke_depan` = 1 | sama | ✅ |

## Keamanan & privasi
- **File asli tidak berubah:** sha256 9 file (`kasir.db`, `stok.db`, `absensi.db`, `DAFTAR.csv`, 5 backup) sebelum = sesudah, dicek lagi setelah ±15 kali menjalankan laporan (termasuk uji DB terkunci). Tidak ada file baru di folder data; folder sementara `/tmp/laporan-usaha-*` terhapus (0 tersisa).
- **Nama/perihal pelanggan tidak bocor:** grep teks & JSON untuk `Wulan`, `Rekaan`, `Rendi`, `PLG-12`, `Supplier`, `INV-`, `arisan`, `sewa tempat`, `harga baru`, catatan lembur `Hendra`, catatan sakit `demam` → **0** kemunculan.
- **`--samarkan`:** nama menjadi `L.`, `Y.`, `N.`, `F.`, `T.`, `D.`; grep 6 nama karyawan di JSON → 0.
- **Tengah malam WIB:** mesin TZ=UTC, `--sekarang 2026-09-24T17:30Z` → laporan "Jumat, 25 September 2026, Dibuat 2026-09-25 00:30 WIB" + peringatan "Jam komputer ini bukan Asia/Jakarta (selisih 7 jam)". `--tanggal kemarin` pada jam itu → Kamis 24/9 dengan angka identik. `--tz WITA` pada 16:30Z → 25/9 00.30 WITA. ✅

## Catatan penguji
- "Belum absen (1): Tari" pada laporan jam 21.30 (jam pulang sudah lewat) tidak masuk PERLU PERHATIAN — lihat cacat R1 di `HASIL-UJI.md`.
- Per metode bayar menjumlah uang termasuk PBJT (381.040), sedangkan omzet tanpa PBJT (346.400). Benar, tetapi tidak diberi label (kosmetik).

**Hasil: LULUS** — semua angka cocok 100%.
