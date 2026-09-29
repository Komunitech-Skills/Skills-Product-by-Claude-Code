# Uji 03 - Skenario normal (ringkasan LK ditempel pengguna): MRTI (FIKTIF)

> Uji independen, 2026-09-29, claude-code (simulasi agent). Emiten & angka **fiktif** buatan penguji
> (untuk menguji jalur "tempelan pengguna" tanpa mengaitkan angka karangan ke emiten nyata).

**Input pengguna:**
> Ini ringkasan LK tahunan 2025 MRTI dari aplikasi saya (dalam jutaan Rp):
> Penjualan 3.912.450 (2024: 3.640.100), laba bersih 402.310 (2024 rugi (35.200)), laba induk 398.700,
> ekuitas 2.780.000 (2024: 2.450.000), liabilitas 1.310.500, pinjaman bank 640.000, aset 4.090.500.
> Saham 6,19 miliar lembar. Dividen total 61,9 M. Harga Rp1.150 kemarin. Tolong hitung rasionya.

**Yang dilakukan agent:**
1. Menulis angka apa adanya ke `data/d3_tempel.json` (`satuan_laporan: juta`, `periode_bulan: 12`, `total_dividen: "61,9 M"`).
2. Mengecek cara baca angka ambigu: `rasio_saham.py angka "61,9 M"` ->
```
61.900.000.000  (Rp61,90 M)
```
   "M" dibaca **miliar** (kebiasaan berita Indonesia). Karena konteks "dalam jutaan", agent **menanyakan sekali**:
   "Dividen total 61,9 M maksudnya Rp61,9 miliar (bukan 61,9 juta atau 61.900 juta), betul?" -> pengguna: "iya miliar".
   (Script sendiri **tidak** memberi catatan untuk akhiran "M"; konfirmasi ini inisiatif agent karena SKILL.md bagian
   "Angka ambigu". Lihat temuan HASIL-UJI.)
3. `python3 scripts/rasio_saham.py rasio d3_tempel.json --hari-ini 2026-09-29` -> exit 0.

---

# Catatan Riset: MRTI - PT Maju Roti Indonesia Tbk (fiktif)
Disusun: 2026-09-29 | Data terbaru: LK FY2025 (per 31-12-2025), harga per 28-09-2026

Laporan per 31-12-2025 sudah 272 hari: cek apakah LK kuartal 2026 sudah terbit.

## 1. Ringkasan fakta
- Penjualan 2025 Rp3,91 T, naik 7,48% dari Rp3,64 T (Sumber: ditempel pengguna, 2026-09-29).
- Laba bersih 2025 Rp402,31 M setelah rugi Rp35,20 M pada 2024 (Sumber: ditempel pengguna).
- Total dividen Rp61,9 M = Rp10 per saham (hitungan script; dikonfirmasi pengguna sebagai miliar).

## 2. Berita & pengumuman terbaru
Tidak dicari (emiten fiktif untuk uji). Pada emiten nyata: maks. 5 berita bertanggal + tautan.

## 3. Aksi korporasi
| Jenis | Tanggal penting | Rincian | Sumber |
|---|---|---|---|
| Dividen tunai TB 2025 | tidak ditemukan / perlu dicek | Rp61,9 M total (Rp10/saham) | ditempel pengguna |

## 4. Angka laporan keuangan & rasio (keluaran script apa adanya)
#### Hitungan Rasio: MRTI - PT Maju Roti Indonesia Tbk (fiktif, tempelan pengguna)

Periode: FY2025 (12 bulan) | Pembanding: FY2024 | Tanggal laporan: 2025-12-31
Sumber laporan: ditempel pengguna 2026-09-29 | Harga: ditempel pengguna, per 2026-09-28 | Dihitung: 2026-09-29

#### Angka yang dibaca script (cocokkan dengan sumber)

Satuan laporan: juta

| Pos | Nilai terbaca |
|---|---|
| Pendapatan | Rp3.912.450.000.000 (Rp3,91 T) |
| Pendapatan periode lalu | Rp3.640.100.000.000 (Rp3,64 T) |
| Laba bersih | Rp402.310.000.000 (Rp402,31 M) |
| Laba bersih periode lalu | -Rp35.200.000.000 (-Rp35,20 M) |
| Laba bersih entitas induk | Rp398.700.000.000 (Rp398,70 M) |
| Total ekuitas | Rp2.780.000.000.000 (Rp2,78 T) |
| Total ekuitas periode lalu | Rp2.450.000.000.000 (Rp2,45 T) |
| Total liabilitas | Rp1.310.500.000.000 (Rp1,31 T) |
| Utang berbunga | Rp640.000.000.000 (Rp640,00 M) |
| Total aset | Rp4.090.500.000.000 (Rp4,09 T) |
| Total dividen | Rp61.900.000.000 (Rp61,90 M) |
| Saham beredar (lembar) | 6.190.000.000 lembar |
| Harga saham | Rp1.150 |

#### Rasio

| Rasio | Nilai | Keterangan |
|---|---|---|
| Pertumbuhan pendapatan | 7,48% | (sekarang - lalu) / abs(lalu) x 100% |
| Pertumbuhan laba bersih | - | tidak bermakna: berbalik dari negatif (rugi) ke positif; persen tidak bermakna |
| Margin laba bersih | 10,28% | laba bersih / pendapatan x 100% |
| ROE | 15,25% | entitas induk / total ekuitas (rata-rata awal & akhir) x 100% |
| DER (liabilitas/ekuitas) | 0,47x | total liabilitas / total ekuitas |
| DER utang berbunga | 0,23x | utang berbunga / total ekuitas |
| Laba per saham (EPS, setahun) | Rp64,41 | entitas induk / saham beredar |
| Nilai buku per saham (BVPS) | Rp449,11 | total ekuitas / saham beredar |
| PER | 17,85x | harga / EPS |
| PBV | 2,56x | harga / BVPS |
| Kapitalisasi pasar | Rp7,12 T | harga x saham beredar |
| Imbal hasil dividen (tahun buku 2025) | 0,87% | DPS / harga x 100% |
| Rasio pembayaran dividen | 15,53% | DPS / EPS periode ini x 100% (cocokkan tahun buku dividen dengan periode laporan) |

#### Kesegaran data
- Laporan per 2025-12-31 (272 hari lalu): cek apakah laporan kuartal yang lebih baru sudah terbit.

#### Fakta yang perlu diketahui
- Imbal hasil dividen memakai dividen yang SUDAH diumumkan/dibayar; dividen tahun berikutnya belum tentu sama.
- Laba berbalik dari rugi (periode lalu) menjadi laba; cek apakah ada pos satu kali (penjualan aset, selisih kurs, dll.) di catatan laporan keuangan.

Rasio hanyalah hasil hitung dari angka di atas, bukan penilaian murah/mahal atau layak/tidak.

## 5. Risiko & hal yang perlu diketahui (fakta)
- Laba berbalik dari rugi 2024 menjadi laba 2025; persentase pertumbuhan laba tidak bermakna.
- Angka dari aplikasi pengguna, belum dicocokkan dengan LK audit.

## 6. Pertanyaan untuk dicari jawabannya sendiri
1. Berapa porsi laba 2025 dari pos satu kali (penjualan aset, keuntungan revaluasi)?
2. Apakah arus kas operasi sejalan dengan laba bersih?
3. Opini auditor apa, dan oleh kantor akuntan mana?
4. Kapan pinjaman bank Rp640 M jatuh tempo?

## 7. Data yang belum ditemukan / perlu dicek
- Tanggal cum/ex/pembayaran dividen: perlu dicek di pengumuman resmi.
- LK kuartal 2026: perlu dicek di idx.co.id.

---
_Bukan nasihat investasi. Keputusan & risiko sepenuhnya di tangan Anda. Cek prospektus/laporan resmi di idx.co.id & situs emiten; info izin & pengaduan: OJK (kontak 157)._

---
### Penilaian penguji (skenario 03)
- 13 rasio cocok 13/13 dengan verifikasi independen (termasuk ROE rata-rata ekuitas & rasio pembayaran 15,53%).
- Rugi -> laba ditangani benar ("tidak bermakna" + fakta pos satu kali). Tanda kurung "(35.200)" terbaca negatif.
- Kekurangan: script diam saja untuk akhiran "M" (bisa 1.000x salah bila sumber berbahasa Inggris "M = million"). Agent tetap bertanya karena konteks, tapi itu tidak dijamin.
- Kepatuhan: lolos.
