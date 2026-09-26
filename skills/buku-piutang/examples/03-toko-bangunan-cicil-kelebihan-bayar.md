# Uji 03 — Toko bangunan: bayar sebagian, cicilan, kelebihan bayar, deposit, batal bayar (normal)

- **Penguji:** agent independen Akun B. Acuan 26 Sep 2026 (WIB). Data rekaan.
- **Permintaan:** "TB Kokoh Jaya. Pak Joko Mandor ambil semen & besi 12,75 juta tgl 3/8, lalu 4.333.333,50 tgl 20/8. Bu Lina Kontraktor bon 2,5 juta tgl 3 Apr 26 tempo 60 hari. Joko nyicil 5 juta (10/9), 7,75 juta (20/9), lalu transfer 4,5 juta (25/9) padahal sisa utangnya 4,33 juta. Lina nyicil 300rb, 300rb, 450.500 (15/9; yang 450.500 ternyata transfernya gagal), 250rb (16/9), lalu lunas hari ini."

## Output script (inti)
```
TB-115 ... Rp 4.333.334  Catatan: Nominal 'Rp4.333.333,50' berisi pecahan sen; dibulatkan ke rupiah terdekat: Rp 4.333.334.
TB-120 ... tanggal 3 Apr 2026 | JT 2 Juni 2026   Catatan: Tahun '3 Apr 26' ditulis 2 angka; dibaca 2026.
B0001 Rp 5.000.000 → TB-101 (sisa Rp 7.750.000)
B0002 Rp 7.750.000 → TB-101 (LUNAS)
bayar yang sama diulang → GAGAL: ... sudah tercatat (B0002). Tidak dicatat dobel ... --izinkan-dobel
bayar 4,5jt → ok:false, kelebihan: 166666, "TIDAK dicatat, supaya saldo tidak minus diam-diam. Tanyakan ke pengguna ..."
(agent bertanya; pengguna: "simpan jadi deposit") → --kelebihan kredit
→ TB-115 LUNAS; Kelebihan Rp 166.666 disimpan sebagai DEPOSIT ... saldo bersih: DEPOSIT milik pelanggan Rp 166.666
catat TB-130 Rp 1.000.000 → Catatan: ... punya deposit Rp 166.666. Tawarkan: pakai-kredit
pakai-kredit → TB-130 sisa Rp 833.334, deposit Rp 0
Lina: 2.500.000 → 2.200.000 → 1.900.000 → 1.449.500 → 1.199.500
batal-bayar --bayar B0006 --alasan "transfer gagal" → TB-120 +Rp 450.500 → saldo Rp 1.650.000
bayar --jumlah lunas → Rp 1.650.000, TB-120 LUNAS
Joko bayar 900rb (--kelebihan kredit) → deposit 66.666 → kembalikan --jumlah semua → deposit Rp 0
saldo --per 15/09/2026 → Joko 12.083.334 (terlewat 7.750.000, 13 hari); Lina 1.900.000 (105 hari)
rekap --periode semua → nota 4 (Rp 20.583.334), pembayaran 8 kali Rp 20.650.000, dikembalikan Rp 66.666, piutang Rp 0
```

## Verifikasi independen (Decimal)
| Pos | Hitung manual | Script |
|---|---|---|
| 4.333.333,50 ROUND_HALF_UP | 4.333.334 | ✅ |
| 1.234.567,49 (uji tambahan) | 1.234.567 | ✅ |
| Total Joko setelah 2 nota | 17.083.334 | ✅ |
| Kelebihan: 4.500.000 − 4.333.334 | 166.666 | ✅ |
| TB-130 setelah deposit: 1.000.000 − 166.666 | 833.334 | ✅ |
| Lina setelah batal B0006: 2.500.000 − 300.000 − 300.000 − 250.000 | 1.650.000 | ✅ |
| Posisi 15/09 (tanpa B0006 yang dibatalkan): Joko 12.750.000 − 5.000.000 + 4.333.334; Lina 2.500.000 − 600.000 | 12.083.334; 1.900.000 | ✅ |
| Hari lewat per 15/09: 15/09 − 02/09; 15/09 − 02/06 | 13; 105 | ✅ |
| Rekonsiliasi: bayar aktif 5.000.000+7.750.000+4.500.000+300.000+300.000+250.000+1.650.000+900.000 | 20.650.000 = nota 20.583.334 + dikembalikan 66.666 → piutang 0, deposit 0 | ✅ |

Alokasi tanpa `--nota` = JT paling awal dulu (TB-101 sebelum TB-115) ✅. Invarian "tidak ada saldo minus" terjaga di semua langkah.

## Catatan
- `batal-bayar` punya pratinjau; di uji ini penguji langsung `--ya` (menguji script, bukan perilaku agent).
- Pembayaran tanpa tagihan terbuka ditolak dengan saran `--kelebihan kredit` untuk uang muka — jelas.

**Nilai skenario: lulus.**
