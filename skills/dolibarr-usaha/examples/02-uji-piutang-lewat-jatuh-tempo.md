# 02 (uji independen) — Piutang lewat jatuh tempo + umur piutang

**Penguji:** agent independen, 2026-09-24. Dolibarr **24.0.1 asli** (lingkungan sama dengan 01). Data fiktif dibuat penguji lewat API admin: 10 invoice (8 tervalidasi belum lunas, 1 lunas, 1 draf), 1 bayar sebagian Rp 200.000, harga bersen (83.333,33).

## Permintaan
> "Siapa saja yang belum bayar? Yang telat urutkan paling lama."

## Keluaran `piutang`
```
PIUTANG BELUM LUNAS per 2026-09-24
Total sisa tagihan: Rp 18.968.192,16 (8 invoice)

UMUR PIUTANG (dihitung dari tanggal jatuh tempo)
- belum jatuh tempo: 3 invoice, Rp 1.935.812,25
- lewat 1-30 hari: 2 invoice, Rp 11.660.550
- lewat 31-60 hari: 1 invoice, Rp 324.475
- lewat 61-90 hari: 1 invoice, Rp 75.480
- lewat > 90 hari: 1 invoice, Rp 4.971.874,91

RINCIAN (paling lama terlambat di atas)
- IN2606-0001 | CV Maju Jaya Konstruksi | sisa Rp 4.971.874,91 | tempo 2026-06-25 (lewat 91 hari)
- IN2606-0009 | Pak Budi Santoso | sisa Rp 75.480 | tempo 2026-06-26 (lewat 90 hari)
- IN2608-0002 | Pak Budi Santoso | sisa Rp 324.475 (sudah dibayar Rp 200.000) | tempo 2026-08-15 (lewat 40 hari)
- IN2607-0008 | PT Griya Asri Properti | sisa Rp 6.937.500 | tempo 2026-08-25 (lewat 30 hari)
- IN2608-0003 | PT Griya Asri Properti | sisa Rp 4.723.050 | tempo 2026-09-19 (lewat 5 hari)
- IN2609-0004 | Bu Rina Wati | sisa Rp 79.920 | tempo 2026-09-24 (jatuh tempo hari ini)
- IN2609-0007 | CV Maju Jaya Konstruksi | sisa Rp 230.325 | tempo 2026-10-07 (jatuh tempo 13 hari lagi)
- IN2609-0005 | Toko Maju Jaya Makmur | sisa Rp 1.625.567,25 | tempo 2026-10-08 (jatuh tempo 14 hari lagi)
```
`piutang --samarkan --maks 3` → nama jadi `C.M.J.`, `P.B.S.`, lalu "... dan 5 invoice lainnya (pakai --maks)" ✅.

## Verifikasi independen (query SQL langsung ke `llx_facture` + `llx_paiement_facture`, `DATEDIFF('2026-09-24', date_lim_reglement)`)
| Invoice | total_ttc | dibayar | sisa (SQL) | lewat (SQL) | Script |
|---|---|---|---|---|---|
| IN2606-0001 | 4.971.874,91 | 0 | 4.971.874,91 | 91 | ✅ >90 |
| IN2606-0009 | 75.480 | 0 | 75.480 | 90 | ✅ 61–90 (batas) |
| IN2608-0002 | 524.475 | 200.000 | 324.475 | 40 | ✅ |
| IN2607-0008 | 6.937.500 | 0 | 6.937.500 | 30 | ✅ 1–30 (batas) |
| IN2608-0003 | 4.723.050 | 0 | 4.723.050 | 5 | ✅ |
| IN2609-0004 | 79.920 | 0 | 79.920 | 0 | ✅ "hari ini", kelompok belum jatuh tempo |
| IN2609-0007 / -0005 | 230.325 / 1.625.567,25 | 0 | sama | −13 / −14 | ✅ |
| IN2609-0006 (lunas) | 138.750 | 138.750 | 0 | – | ✅ tidak muncul |
| (PROV8) draf | 11.100 | – | – | – | ✅ tidak dihitung |
Total 18.968.192,16 dan kelima kelompok = penjumlahan penguji (0 beda).

## Uji zona waktu server (PHP `date.timezone` diganti, DB sama)
| PHP tz | `--tz` | IN2606-0001 | IN2609-0004 |
|---|---|---|---|
| Asia/Jakarta, UTC (default DoliWamp `php.ini.install:688`), Europe/Paris, America/New_York | WIB | tempo 25/06, 91 hari ✅ | hari ini ✅ |
| **Asia/Makassar** | WIB (default) | tempo **24/06, 92 hari** ❌ | "**lewat 1 hari**" ❌ |
| Asia/Makassar | WITA | ✅ | ✅ |
| **Asia/Tokyo** | WIB | 24/06, 92 hari ❌ | lewat 1 hari ❌ |
Sebab: `tanggal_dari_ts` (dolibarr.py:168-176) mengubah timestamp tengah malam zona **server** memakai offset `--tz`; bila zona server lebih ke timur dari `--tz`, semua tanggal mundur 1 hari (IN2607-0008 pindah dari 1–30 ke 31–60). DoliWamp default (UTC) aman; risiko pada Dolibarr Linux/DoliDeb/Docker di Bali/Sulawesi/Kalimantan Timur/Papua yang mengikuti zona sistem tanpa `--tz`. SKILL.md tidak menyebut `--tz` untuk pemakaian interaktif (hanya di references/openclaw-jadwal.md:39). → cacat **R3**.

**Hasil skenario: LULUS** (angka 100% cocok pada konfigurasi DoliWamp default), catatan R3.
