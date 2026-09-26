# Uji 01 — Distributor sembako, 30 pelanggan tempo (normal)

- **Penguji:** agent independen Akun B (hanya membaca folder skill; kode tidak dibaca untuk verifikasi angka).
- **Tanggal uji / acuan:** Sabtu, 26 September 2026 (WIB). Salinan skill di scratchpad, `KOMUNITECH_PIUTANG_DB` ke folder uji. Data rekaan.
- **Permintaan pengguna:** "Saya distributor sembako UD Sumber Pangan, ini daftar bon warung dari Excel (CSV). Masukkan semua, lalu kasih tahu siapa yang belum bayar, umur piutangnya, dan bikinin pesan tagihan untuk yang paling lama."

## Data
`sembako.csv` (pemisah `;`, 49 baris, 30 pelanggan, nominal dengan pecahan ratusan rupiah seperti 5.875.750, jatuh tempo campur tanggal & "N hari", kolom `dibayar` untuk DP/cicilan, status `lunas`/`belum lunas`/`tempo`/`bon`). 11 baris lunas.

## Langkah agent (mengikuti SKILL.md)
1. `info` → belum ada DB → tanya nama usaha, pengirim, rekening, termin → `init ... --termin 14` (pratinjau) → `--ya`.
2. `impor sembako.csv` (pratinjau):
```
Kolom dikenali: pelanggan='pelanggan', nota='no nota', tanggal='tanggal', jatuh_tempo='jatuh tempo', nominal='nominal', dibayar='dibayar', wa='no wa', keterangan='keterangan', status='status'
Akan dicatat: 38 nota, total Rp 119.962.250, sisa piutang Rp 110.811.250, untuk 26 pelanggan (26 pelanggan baru)
Dilewati: 0 sudah ada di buku, 11 sudah lunas, 0 batal/void
```
   Setuju → `impor ... --ya` (cadangan `...-sebelum-impor.db` dibuat dulu).
3. `umur`, `saldo --semua`, `jatuh-tempo`, `draf --pelanggan "Toko Makmur"`, `ringkasan --samarkan`.

## Output script (dipotong)
```
UMUR PIUTANG - per Sabtu, 26 September 2026
Total piutang: Rp 110.811.250 (38 nota)
Belum jatuh tempo Rp 14.951.875 (13,5%) | 1-30 hari Rp 15.588.500 (14,1%) | 31-60 hari Rp 16.140.125 (14,6%) | 61-90 hari Rp 48.505.000 (43,8%) | >90 hari Rp 15.625.750 (14,1%)

JATUH TEMPO PIUTANG - Sabtu, 26 September 2026 (WIB)
Terlewat: Rp 95.859.375 (33 nota) | Hari ini: Rp 0 (0) | 7 hari ke depan: Rp 7.901.000 (2)
1. SP-0005 | Toko Makmur (P0002) | sisa Rp 3.625.000 | JT 14 Jun 2026 (lewat 104 hari)
...
MINGGU INI (besok s.d. 3 Okt 2026) (2 nota, Rp 7.901.000)
1. SP-0022 | Warung Bu Siti (P0013) | sisa Rp 4.125.500 | JT 27 Sep 2026 (1 hari lagi)
2. SP-0012 | Kios Bu Ani (P0006) | sisa Rp 3.775.500 | JT 1 Okt 2026 (5 hari lagi)
```
Draf Toko Makmur (jenis `terlewat-lama`): sapaan "Bapak/Ibu di Toko Makmur", 2 nota + total Rp 9.750.000, rekening, tawaran bertahap, tanpa denda/ancaman, tautan `https://wa.me/6281200003001?text=...`, baris `Setelah terkirim: piutang.py terkirim --pelanggan P0002`, dan `Saran` (untuk pemilik) memakai `tagih-piutang` karena lewat 104 hari. Draf Warung Bu Siti = `pengingat-awal` ("Halo Bu Siti ... Izin mengingatkan ... akan jatuh tempo"). `ringkasan --samarkan` menampilkan "Toko M. (P0002)", tanpa nomor WA.

## Verifikasi angka independen (Decimal, dari CSV mentah, tanpa membaca kode)
Skrip verifikasi sendiri (`verif.py`: lewati status lunas, sisa = nominal − dibayar, JT = tanggal + N hari atau tanggal, hari lewat = 26/09/2026 − JT, bucket ≤0 / 1–30 / 31–60 / 61–90 / >90, persen ROUND_HALF_UP 1 desimal):

| Pos | Verifikasi | Script | Cocok |
|---|---|---|---|
| Nota terbuka / pelanggan | 38 / 26 | 38 / 26 | ✅ |
| Total nominal / sisa | 119.962.250 / 110.811.250 | sama | ✅ |
| Belum JT | 5 nota, 14.951.875 (13,5%) | 14.951.875 (13,5%) | ✅ |
| 1–30 | 8, 15.588.500 (14,1%) | sama | ✅ |
| 31–60 | 7, 16.140.125 (14,6%) | sama | ✅ |
| 61–90 | 15, 48.505.000 (43,8%) | sama | ✅ |
| >90 | 3, 15.625.750 (14,1%) | sama | ✅ |
| Terlewat = jumlah 4 bucket | 95.859.375 | 95.859.375 | ✅ |
| 7 hari ke depan | 4.125.500 + 3.775.500 = 7.901.000 | sama | ✅ |
| Saldo 26 pelanggan (mis. RM Padang 11.500.500, Toko Makmur 9.750.000, Bu Tini 8.475.750, Warung Kopi Asik 150.500) | semua 26 baris | sama persis | ✅ |

Pembanding silang: skrip pesaing (`accounts-receivable`, lihat `00-banding-pesaing.md`) pada data yang sama menghasilkan bucket & total identik.

**Batas bucket** (DB terpisah, nota dengan JT lewat 0/1/30/31/60/61/90/91 hari dan 7/8 hari lagi): 0 → "hari ini"; 1 & 30 → 1–30; 31 & 60 → 31–60; 61 & 90 → 61–90; 91 → >90; 7 hari lagi → MINGGU INI; 8 hari lagi → belum JT. Semua ✅.

## Catatan temuan
- `ringkasan`: "Pembayaran masuk kemarin: Rp 1.087.500 (1)" berasal dari kolom `dibayar` impor pada nota bertanggal 25/09 (DP dicatat bertanggal nota). Benar secara aturan, tapi bisa terbaca sebagai uang masuk baru hari itu (P3).
- Urutan daftar `umur` tidak menurut total (mis. RM Padang Rp 11,5 jt di nomor 5) — tampaknya menurut umur terberat; tidak dijelaskan di teks (kosmetik).

**Nilai skenario: lulus.** Angka 100% cocok, alur pratinjau → setuju → simpan berjalan, draf sopan dan tidak terkirim otomatis.
