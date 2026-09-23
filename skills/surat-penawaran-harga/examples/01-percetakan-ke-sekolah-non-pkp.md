# 01 — Percetakan (bukan PKP) ke sekolah, diskon total 5%

**Skenario:** S1 — permintaan normal, penjual bukan PKP, 3 item, diskon persen atas total, gratis ongkir.

**Input pengguna:**
> Tolong bikinin surat penawaran harga dari usaha saya Percetakan Sinar Jaya Fiktif (Jl. Kaliurang Km 7, Yogyakarta, WA 0812-0000-1101, email sinarjaya.fiktif@contoh.id). Saya belum PKP. Buat SMA Harapan Bangsa Fiktif, ke Bu Wati bendahara. Isinya 500 buku tulis custom logo sekolah @7.500, 20 banner 3x1 m @150rb, 1000 kartu pelajar PVC @12rb. Kasih diskon 5% dari total ya, ongkir gratis karena masih dalam kota. Nomor surat 45.

**Perintah script yang dijalankan:**
```bash
python3 scripts/hitung_sph.py \
  --item "Buku tulis custom logo sekolah (38 lbr)|500|pcs|7.500" \
  --item "Banner 3x1 m|20|lembar|150rb" \
  --item "Kartu pelajar PVC|1000|pcs|12rb" \
  --diskon-total 5% --nomor-urut 45 --kode "SPH/PSJ" --tanggal 2026-09-23 --format teks
```
Hasil script: Subtotal Rp 18.750.000; diskon 5% −Rp 937.500; TOTAL Rp 17.812.500; nomor 045/SPH/PSJ/IX/2026; berlaku s.d. 7 Oktober 2026.

## Output

### (A) Surat penawaran

**PERCETAKAN SINAR JAYA FIKTIF**
Jl. Kaliurang Km 7, Yogyakarta · WA 0812-0000-1101 · sinarjaya.fiktif@contoh.id

---

Nomor    : 045/SPH/PSJ/IX/2026
Lampiran : -
Perihal  : Penawaran Harga Buku Tulis Custom, Banner, dan Kartu Pelajar

Yogyakarta, 23 September 2026

Kepada Yth.
Ibu Wati – Bendahara
SMA Harapan Bangsa Fiktif
di tempat

Dengan hormat,
Menindaklanjuti kebutuhan perlengkapan sekolah yang Ibu sampaikan, bersama ini kami sampaikan penawaran harga sebagai berikut:

| No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
|---|---|---|---|---|---|---|
| 1 | Buku tulis custom logo sekolah (38 lbr) | 500 | pcs | Rp 7.500 | - | Rp 3.750.000 |
| 2 | Banner 3x1 m | 20 | lembar | Rp 150.000 | - | Rp 3.000.000 |
| 3 | Kartu pelajar PVC | 1.000 | pcs | Rp 12.000 | - | Rp 12.000.000 |

| | |
|---|---|
| Subtotal | Rp 18.750.000 |
| Diskon tambahan (5%) | −Rp 937.500 |
| Ongkos kirim | Gratis (dalam kota Yogyakarta) |
| **TOTAL** | **Rp 17.812.500** |

Terbilang: *Tujuh Belas Juta Delapan Ratus Dua Belas Ribu Lima Ratus Rupiah*

**Syarat & ketentuan**
1. Harga tidak dikenakan PPN.
2. Penawaran berlaku sampai 7 Oktober 2026.
3. Pembayaran: DP 50% saat pesanan (PO/SPK) diterima, pelunasan 50% sebelum barang dikirim, ke [Bank – No. Rek – a.n. Percetakan Sinar Jaya Fiktif].
4. Pengiriman: 3–7 hari kerja setelah DP diterima dan desain disetujui; diantar gratis ke sekolah (dalam kota Yogyakarta).

Demikian penawaran ini kami sampaikan. Besar harapan kami dapat mendukung kebutuhan SMA Harapan Bangsa Fiktif. Untuk konfirmasi pesanan atau pertanyaan, Ibu dapat menghubungi kami di WA 0812-0000-1101.

Hormat kami,

[Nama]
[Jabatan] – Percetakan Sinar Jaya Fiktif

**Asumsi yang dipakai**
- Penjual bukan PKP → tanpa PPN (sesuai keterangan Bapak/Ibu).
- Masa berlaku 14 hari; pembayaran DP 50%/pelunasan sebelum kirim; pengiriman 3–7 hari kerja (default, tidak disebutkan).
- Nama penanda tangan & rekening belum diberikan → ditandai `[isi]`.

**Catatan:** Perhitungan angka memakai kalkulator bawaan skill. Bukan nasihat pajak.

### (B) Teks WhatsApp
```
Selamat siang, Bu Wati 🙏
Berikut penawaran harga dari Percetakan Sinar Jaya Fiktif untuk kebutuhan sekolah:
• Buku tulis custom logo – 500 pcs × Rp 7.500
• Banner 3x1 m – 20 lembar × Rp 150.000
• Kartu pelajar PVC – 1.000 pcs × Rp 12.000
Total: *Rp 17.812.500* (sudah diskon 5%, tanpa PPN, gratis antar dalam kota)
Berlaku s.d. 7 Oktober 2026. DP 50% saat pesan, pelunasan sebelum kirim.
Surat penawaran resmi (PDF) terlampir. Jika ada yang ingin disesuaikan, kabari saja ya, Bu.
```

## Catatan penguji
- Angka diverifikasi independen: 3.750.000 + 3.000.000 + 12.000.000 = 18.750.000; 5% = 937.500; total 17.812.500. Terbilang benar.
- Bagus: nomor surat otomatis, PPN tidak muncul untuk non-PKP, total tabel = WA = terbilang, rekening tidak dikarang.
- Kurang (ringan): SKILL.md tidak punya aturan menampilkan ongkir "Gratis" (script tidak menampilkan baris ongkir bila 0); agent menambahkannya sendiri agar jelas bagi pembeli. Untuk sekolah negeri/BOS, pembeli mungkin butuh NPWP penjual — skill menyebutnya hanya di tabel "nada per jenis pembeli".
