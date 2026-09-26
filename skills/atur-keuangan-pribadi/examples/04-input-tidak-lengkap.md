# Uji 04 — Input tidak lengkap

> Penguji independen, 2026-09-26. Menguji aturan SKILL.md "Tanyakan **sekali** dalam satu pesan, hanya yang relevan" dan default bila pengguna ingin cepat.

## Input pengguna
"gimana cara atur keuangan saya?"

## Perilaku agent (mengikuti SKILL.md)
Tidak ada angka sama sekali dan tidak jelas kebutuhannya (anggaran/dana darurat/utang/target). Agent **tidak menjalankan script** (tidak ada data), **tidak memberi saran umum panjang**, dan bertanya sekali:

---
Siap bantu! Supaya hasilnya langsung berupa angka (bukan teori), jawab yang Anda tahu saja — perkiraan juga boleh:

1. **Pemasukan bersih per bulan** (setelah potongan). Kalau suami-istri, sebut masing-masing. Ada THR/bonus tahunan?
2. **Pengeluaran rutin** per bulan: tempat tinggal (kos/kontrakan/KPR), makan, transport, listrik/air, pulsa/internet, sekolah anak, kiriman orang tua, dll.
3. **Utang/cicilan** (kalau ada): nama, sisa, bunga (per bulan/tahun, flat atau bukan), cicilan per bulan — termasuk paylater & pinjol.
4. **Tabungan/dana darurat** yang sudah ada.
5. **Status**: lajang / menikah / punya anak atau tanggungan / pekerja lepas-usaha / PNS.
6. **Tujuan terdekat** (opsional): DP rumah, sekolah anak, umrah, lunas utang, dll. + berapa tahun lagi.

Kalau mau cepat, cukup kirim contoh seperti: *"gaji 6 jt, kos 1,5 jt, makan 2 jt, cicilan motor 800 rb, tabungan 3 jt, lajang"* — sisanya saya pakai asumsi umum (pola 50/30/20, inflasi 4%/tahun) dan saya sebutkan asumsinya.

⚠️ Bukan nasihat keuangan/investasi.
---

## Lanjutan (pengguna menjawab singkat, ingin cepat)
"gaji 6 jt, kos 1,5 jt, makan 2 jt, cicilan motor 800 rb, tabungan 3 jt, lajang"

Agent menjalankan:
```
python3 scripts/keuangan.py anggaran --pemasukan "Gaji=6jt" --pos "Kos=1,5jt" --pos "Makan=2jt" --pos "Cicilan motor=800rb"
python3 scripts/keuangan.py dana-darurat --pengeluaran-pokok 4,3jt --status lajang --saldo 3jt --setoran 700rb
```
Inti keluaran (asli, dipotong):
```
| Kos | Kebutuhan wajib (tebakan) | Rp1.500.000 | 25,0% |
| Makan | Kebutuhan wajib (tebakan) | Rp2.000.000 | 33,3% |
| Cicilan motor | Kebutuhan wajib (tebakan) | Rp800.000 | 13,3% |
| **Belum dialokasikan** | | **Rp1.700.000** | harus dijadikan 0 |
| 3 bulan | Rp12.900.000 | Rp9.900.000 | 15 bulan (~1 th 3 bln) | ...
| 6 bulan | Rp25.800.000 | Rp22.800.000 | 33 bulan (~2 th 9 bln) | ...
```
Agent lalu menyarankan pembagian sisa Rp1.700.000 (mis. transport/pulsa yang belum disebut Rp600.000, keinginan Rp400.000, dana darurat Rp700.000) sambil **menyebut asumsinya** dan meminta koreksi bila transport/pulsa sudah termasuk.

## Penilaian penguji
- Satu pesan, daftar singkat, bahasa awam, ada contoh jawaban cepat ✓ (sesuai prinsip "instan" CLAUDE.md).
- Tidak mengarang angka sebelum ada data ✓. Setelah data ada, pos tanpa label ditandai "(tebakan)" ✓.
- Cek angka: 9.900.000 ÷ 700.000 = 14,14 → 15 ✓; 22.800.000 ÷ 700.000 = 32,57 → 33 ✓.
- **Hasil: LULUS.**
