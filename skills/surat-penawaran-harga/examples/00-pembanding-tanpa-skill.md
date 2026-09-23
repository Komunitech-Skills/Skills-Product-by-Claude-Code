# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Tolong bikinin surat penawaran harga dari usaha saya Percetakan Sinar Jaya Fiktif (Jl. Kaliurang Km 7, Yogyakarta, WA 0812-0000-1101, email sinarjaya.fiktif@contoh.id). Saya belum PKP. Buat SMA Harapan Bangsa Fiktif, ke Bu Wati bendahara. Isinya 500 buku tulis custom logo sekolah @7.500, 20 banner 3x1 m @150rb, 1000 kartu pelajar PVC @12rb. Kasih diskon 5% dari total ya, ongkir gratis karena masih dalam kota. Nomor surat 45.

## Berdampingan

| Aspek | TANPA skill (AI agent biasa) | DENGAN skill |
|---|---|---|
| Nomor surat | `No: 45/SPH/IX/2026` (tanpa kode usaha, tanpa 3 digit) | `045/SPH/PSJ/IX/2026` (pola baku, dari script) |
| Tabel & total | Benar (hitung di kepala): Rp 17.812.500 | Benar, dihitung script & diverifikasi |
| Terbilang | Ada: "tujuh belas juta delapan ratus dua belas ribu lima ratus rupiah" | Ada, dari script |
| PPN | "Harga di atas belum termasuk pajak." (ambigu; bisa dikira pembeli akan ditagih PPN, padahal penjual bukan PKP) | "Harga tidak dikenakan PPN." (tepat untuk non-PKP) |
| Masa berlaku | "Penawaran berlaku 14 hari" (tanpa tanggal) | "berlaku sampai 7 Oktober 2026" (tanggal pasti) |
| Syarat bayar & rekening | "Pembayaran dapat didiskusikan" | DP 50%/pelunasan + placeholder rekening `[isi]` |
| Versi WhatsApp | Tidak ada | Ada, ≤ 15 baris, total sama dengan surat |
| Asumsi | Tidak disebut | Blok "Asumsi yang dipakai" |

### Output TANPA skill (lengkap)
```
PERCETAKAN SINAR JAYA FIKTIF
Jl. Kaliurang Km 7, Yogyakarta | WA 0812-0000-1101 | sinarjaya.fiktif@contoh.id

No      : 45/SPH/IX/2026
Hal     : Surat Penawaran Harga

Yogyakarta, 23 September 2026

Kepada Yth.
Ibu Wati
Bendahara SMA Harapan Bangsa Fiktif

Dengan hormat,
Bersama surat ini kami menawarkan produk sebagai berikut:

No | Produk                        | Jumlah | Harga    | Total
1  | Buku tulis custom logo sekolah| 500    | 7.500    | 3.750.000
2  | Banner 3x1 m                  | 20     | 150.000  | 3.000.000
3  | Kartu pelajar PVC             | 1000   | 12.000   | 12.000.000
   | Subtotal                      |        |          | 18.750.000
   | Diskon 5%                     |        |          | (937.500)
   | TOTAL                         |        |          | 17.812.500
Terbilang: tujuh belas juta delapan ratus dua belas ribu lima ratus rupiah

Keterangan:
- Harga di atas belum termasuk pajak.
- Gratis ongkos kirim dalam kota Yogyakarta.
- Penawaran berlaku 14 hari.
- Pembayaran dapat didiskusikan.

Demikian penawaran kami, atas perhatiannya kami ucapkan terima kasih.

Hormat kami,
Percetakan Sinar Jaya Fiktif
```

### Output DENGAN skill
Lihat `01-percetakan-ke-sekolah-non-pkp.md` (surat lengkap + teks WhatsApp + asumsi).

## Penilaian
- **Lebih baik berkat skill:** (1) kalimat PPN yang benar untuk non-PKP — versi tanpa skill menulis "belum termasuk pajak" yang menyesatkan dan bisa memicu pertanyaan/komplain pembeli; (2) tanggal masa berlaku pasti; (3) syarat bayar konkret + rekening tidak dikarang; (4) teks WhatsApp siap kirim; (5) asumsi transparan; (6) angka dijamin script (pada kasus PKP dengan diskon per baris & ongkir, AI biasa rawan salah memakai 12% penuh atau 11% tanpa penjelasan DPP 11/12).
- **Setara:** aritmetika sederhana dan terbilang pada kasus ini sama-sama benar.
- **Kesimpulan:** hasil dengan skill **jelas lebih baik** dan lebih siap kirim; selisih paling besar muncul pada kasus PKP (lihat 03).
