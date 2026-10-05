# Uji 06 (Akun B) — Input tidak lengkap: hanya omzet & laba

> Penguji independen (Akun B), 2026-09-26. Skenario input tidak lengkap.

**Permintaan pengguna:** "Usaha saya sehat nggak? Omzet 20 juta sebulan, untung bersih 3 juta."

## Respons agent sesuai SKILL.md (simulasi mengikuti bagian "Input")
Data wajib untuk likuiditas & solvabilitas belum ada, jadi agent bertanya **sekali** dalam satu pesan:

> Supaya bisa saya nilai dengan angka pasti, boleh lengkapi 5 hal ini (perkiraan juga boleh):
> 1. Penjualan 20 jt dan laba bersih 3 jt itu untuk 1 bulan, ya? Berapa HPP (modal barang/bahan yang terjual) di bulan itu?
> 2. Di akhir bulan: uang kas + bank, piutang pelanggan, nilai stok, nilai peralatan/kendaraan usaha?
> 3. Utang: ke pemasok, ke bank (berapa pokok yang dibayar 12 bulan ke depan), lainnya? Modal pemilik?
> 4. Jenis usahanya: dagang, jasa, atau produksi/kuliner?
> 5. Ada angka bulan/tahun lalu untuk dibandingkan? Berencana pinjam? Cicilan per bulan berapa?
>
> Kalau lebih mudah, isi tabel `templates/isian-rasio.csv`. Yang bisa saya sampaikan sekarang: margin laba bersih 15% (dari tiap Rp 100.000 penjualan, laba Rp 15.000). Rasio lain belum bisa dinilai.

Pertanyaan sesuai daftar di SKILL.md, maksimal 5, satu pesan, dan menawarkan template. ✔

## Bila pengguna minta "langsung saja" (script dijalankan dengan data minim)
```bash
python3 scripts/rasio.py --penjualan "20 juta" --laba-bersih 3jt --bulan 1
```
# Analisis Rasio Keuangan — [Nama Usaha]
Jenis usaha: Umum (jenis usaha tidak disebut) · Periode dianalisis: periode ini · Status data: **SEMENTARA**

## Ringkasan untuk pemilik
Pada periode ini, usaha UNTUNG Rp 3.000.000 (15,0% dari penjualan). Dari 1 rasio yang dinilai terhadap ambang usaha umum: 1 baik, 0 waspada, 0 bahaya. Semua rasio yang bisa dihitung berada di rentang wajar — pertahankan.

## Likuiditas — sanggup bayar tagihan jangka pendek? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Rasio lancar (current ratio) | — | aset lancar ÷ utang lancar | ≥ 1,50x baik · 1,00x–1,50x waspada · < 1,00x bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Total aset lancar, Total utang lancar (≤ 1 tahun) |
| Rasio cepat (quick ratio) | — | (aset lancar − persediaan) ÷ utang lancar | ≥ 0,80x baik · 0,50x–0,80x waspada · < 0,50x bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Total aset lancar, Total utang lancar (≤ 1 tahun) |
| Rasio kas (cash ratio) | — | kas & bank ÷ utang lancar | ≥ 0,20x baik · 0,10x–0,20x waspada · < 0,10x bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Kas & bank, Total utang lancar (≤ 1 tahun) |

## Profitabilitas — seberapa untung? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Margin laba kotor | — | laba kotor ÷ penjualan × 100 | ≥ 20,0% baik · 10,0%–20,0% waspada · < 10,0% bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Harga pokok penjualan (HPP) |
| Margin laba bersih | 15,0% | laba bersih ÷ penjualan × 100 | ≥ 8,0% baik · 3,0%–8,0% waspada · < 3,0% bahaya | 🟢 Baik | Dari tiap Rp 100.000 penjualan, laba bersih Rp 15.000. |
| ROA disetahunkan (laba ÷ aset) | — | laba bersih ÷ total aset × 100 × (365 ÷ 30 hari) | ≥ 10,0% baik · 5,0%–10,0% waspada · < 5,0% bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Total aset |
| ROE disetahunkan (laba ÷ modal) | — | laba bersih ÷ modal akhir × 100 × (365 ÷ 30 hari) | ≥ 15,0% baik · 6,0%–15,0% waspada · < 6,0% bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Modal / ekuitas akhir |

## Solvabilitas — seberapa besar bergantung pada utang? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| DER (utang ÷ modal) | — | total utang ÷ modal | ≤ 1,00x baik · 1,00x–2,00x waspada · > 2,00x bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Total utang (liabilitas), Modal / ekuitas akhir |
| DAR (utang ÷ aset) | — | total utang ÷ total aset × 100 | ≤ 50,0% baik · 50,0%–67,0% waspada · > 67,0% bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Total utang (liabilitas), Total aset |

## Aktivitas — seberapa cepat stok & piutang jadi uang? (periode ini)
| Rasio | Nilai | Rumus | Wajar untuk jenis usaha ini | Status | Artinya |
|---|---|---|---|---|---|
| Umur stok (hari) | — | persediaan akhir × hari periode ÷ HPP | ≤ 45,0 hari baik · 45,0 hari–90,0 hari waspada · > 90,0 hari bahaya | — Tidak dihitung | Tidak dihitung: data belum ada: Harga pokok penjualan (HPP), Persediaan / stok |

## Kesiapan pengajuan KUR/kredit (dari sisi angka)
**PERLU PERBAIKAN/DATA TAMBAHAN — lihat poin ⚠/?**
- ✓ Usaha UNTUNG Rp 3.000.000 pada periode ini.
- ? Modal/ekuitas belum diketahui atau dihitung dari angka mustahil.
- Laba bersih rata-rata per bulan: Rp 3.000.000.
- Cicilan belum diisi. Untuk cek kemampuan bayar, sebutkan total cicilan per bulan (lama + rencana) → --cicilan-bulanan.
_Ini pembacaan angka, bukan keputusan kredit. Bank juga menilai karakter, riwayat SLIK OJK, agunan, legalitas, dan prospek usaha. Simulasi cicilan & dokumen KUR: skill pengajuan-kur._

## Saran tindakan (urut prioritas)
1. **—** — Pertahankan: hitung ulang rasio ini tiap bulan/kuartal dan bandingkan trennya; sisihkan sebagian laba sebagai dana cadangan.

## Perlu dicek
- [periode ini] Periode pendek (1,0 bulan): angka yang disetahunkan (ROA, ROE, perputaran aset) bisa meleset karena musim ramai/sepi.

## Asumsi yang dipakai
- Tidak ada — semua angka diisi pengguna.
- Ambang 'wajar' = pedoman praktis untuk jenis usaha umum (references/ambang-wajar.md).

_Disclaimer: Analisis angka untuk membantu pemilik usaha memahami kondisi keuangan. Bukan nasihat investasi, bukan penilaian kredit, bukan laporan audit. Ambang wajar adalah pedoman praktis (lihat references/ambang-wajar.md), bukan standar resmi OJK/bank. Untuk keputusan besar, konsultasikan dengan akuntan atau pendamping UMKM._

## Penilaian penguji
- ✔ Rasio yang datanya kurang ditulis "Tidak dihitung: data belum ada: …", tidak diganti 0. Status data SEMENTARA. Peringatan periode pendek muncul. Tidak ada galat.
- ✔ Kesiapan KUR: "PERLU PERBAIKAN/DATA TAMBAHAN" dengan "? Modal/ekuitas belum diketahui".
- ✘ **Temuan (sedang) — kesimpulan menyesatkan saat data minim:** ringkasan berbunyi "Dari 1 rasio… Semua rasio yang bisa dihitung berada di rentang wajar — **pertahankan**", dan saran satu-satunya "Pertahankan". Padahal 10 dari 11 rasio belum dihitung. Bagian Asumsi juga menulis "**Tidak ada — semua angka diisi pengguna**", padahal hampir semua pos kosong. Usul perbaikan: bila rasio yang dinilai < ±5, ringkasan & saran jadi "Data belum cukup untuk menilai kesehatan; lengkapi …", dan Asumsi mendaftar pos yang kosong.
- Agent yang mengikuti SKILL.md akan bertanya dulu, jadi risikonya muncul hanya bila pengguna memaksa "langsung saja".
