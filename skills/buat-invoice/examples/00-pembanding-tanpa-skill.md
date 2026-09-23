# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Buatin invoice dari Konveksi Maju Fiktif (Jl. Contoh Raya No. 10 Sukoharjo, WA 0812-0000-2201) ke SMP Contoh Nusantara (Jl. Pendidikan No. 5 Surakarta): 120 kaos olahraga @85rb, 120 celana @70rb diskon 5%, sablon nama 120 x 10rb, ongkir 150rb. DP 6 juta udah ditransfer tgl 15 September. Jatuh tempo 30 hari. Rekening BRI 0000-01-000000-50-0 a.n. Konveksi Maju Fiktif. Nomor terakhir INV/2026/09/0012. Saya belum PKP. Yang tanda tangan Sri Contoh, pemilik.

## Output TANPA skill (AI agent biasa, tanpa membaca skill)
```
INVOICE
No: INV/2026/09/0013
Tanggal: 23 September 2026
Jatuh Tempo: 23 Oktober 2026

Dari: Konveksi Maju Fiktif, Jl. Contoh Raya No. 10 Sukoharjo, WA 0812-0000-2201
Kepada: SMP Contoh Nusantara, Jl. Pendidikan No. 5 Surakarta

No | Item               | Qty | Harga   | Total
1  | Kaos olahraga      | 120 | 85.000  | 10.200.000
2  | Celana olahraga    | 120 | 70.000  | 8.400.000
   | Diskon 5% celana   |     |         | -420.000
3  | Sablon nama        | 120 | 10.000  | 1.200.000
   | Ongkir             |     |         | 150.000
   | TOTAL              |     |         | 19.530.000
   | DP (15/09/2026)    |     |         | -6.000.000
   | SISA               |     |         | 13.530.000

Pembayaran: BRI 0000-01-000000-50-0 a.n. Konveksi Maju Fiktif

Hormat kami,
Sri Contoh (Pemilik)
```

## Output DENGAN skill
Lihat `01-konveksi-seragam-dp.md`: invoice Markdown dengan status "SEBAGIAN DIBAYAR", tabel item + kolom diskon, subtotal/ongkir/total/DP/sisa, **terbilang**, rekening, catatan, kota & tanggal, **tempat meterai**, plus **file HTML siap cetak/PDF**, dan catatan terpisah untuk penjual (meterai wajib karena menyatakan penerimaan DP > Rp5 juta, kuitansi pelunasan nanti juga wajib meterai, non-PKP tanpa PPN).

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Angka total & sisa | Benar | Benar, dihitung script & diverifikasi |
| Nomor lanjutan | Benar | Benar (otomatis dari nomor terakhir) |
| Terbilang | Tidak ada | Ada (diverifikasi 23.000+ angka) |
| Bea meterai | **Tidak disinggung** | Ditandai + penjelasan + pengingat untuk kuitansi pelunasan |
| Status pembayaran | Tidak ada | "SEBAGIAN DIBAYAR" |
| Versi cetak/PDF | Tidak ada | File HTML siap cetak (A4) |
| Pemisahan info internal vs dokumen untuk pembeli | Tidak ada | Ada ("Info untuk penjual — jangan ikut dikirim") |
| Penolakan PPN non-PKP (S5) | Agent biasa cenderung menuruti permintaan menambah PPN | Ditolak oleh script + penjelasan |

## Penilaian
Skill **jelas lebih baik**: dokumen siap cetak, terbilang, status, penanda meterai, dan pagar pengaman PPN untuk non-PKP — hal-hal yang tidak muncul pada jawaban tanpa skill walaupun aritmetikanya sama.
