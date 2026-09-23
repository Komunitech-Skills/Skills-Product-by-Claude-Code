# 03 — Penjual PKP, barang + jasa pasang + ongkir (PPN 12% × DPP 11/12)

**Skenario:** S3 — permintaan normal, penjual PKP, ada ongkir dan jasa pasang, masa berlaku 7 hari, tempo pembayaran berbeda dari default.

**Input pengguna:**
> Saya CV Teknik Mandiri Fiktif, Surabaya, sudah PKP. Mau kirim penawaran ke Klinik Sehat Sentosa Fiktif, Pak dr. Budi (pemilik). 5 unit AC split 1 PK @4.250.000, jasa pasang + pipa 3 meter 350rb per titik, ongkir 200rb. Harga belum PPN. Berlaku seminggu aja karena harga AC naik terus. Pembayaran 30% DP, sisanya setelah terpasang. Nomor surat 7.

**Perintah script yang dijalankan:**
```bash
python3 scripts/hitung_sph.py \
  --item "AC split 1 PK|5|unit|4.250.000" \
  --item "Jasa pasang + pipa 3 m|5|titik|350rb" \
  --ongkir 200rb --ppn pkp --nomor-urut 7 --kode "SPH/TMF" \
  --tanggal 2026-09-23 --berlaku-hari 7 --format teks
```
Hasil: Subtotal Rp 23.000.000; ongkir Rp 200.000; DPP Rp 23.200.000; DPP nilai lain Rp 21.266.667; PPN Rp 2.552.000; TOTAL Rp 25.752.000; berlaku s.d. 30 September 2026.

## Output

### (A) Surat penawaran

**CV TEKNIK MANDIRI FIKTIF**
[Alamat], Surabaya · WA [nomor] · [email]

---

Nomor    : 007/SPH/TMF/IX/2026
Lampiran : -
Perihal  : Penawaran Harga Pengadaan dan Pemasangan AC Split

Surabaya, 23 September 2026

Kepada Yth.
dr. Budi – Pemilik
Klinik Sehat Sentosa Fiktif
di tempat

Dengan hormat,
Menindaklanjuti permintaan Bapak, bersama ini kami sampaikan penawaran harga pengadaan dan pemasangan AC split untuk Klinik Sehat Sentosa Fiktif sebagai berikut:

| No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
|---|---|---|---|---|---|---|
| 1 | AC split 1 PK | 5 | unit | Rp 4.250.000 | - | Rp 21.250.000 |
| 2 | Jasa pasang + pipa 3 m | 5 | titik | Rp 350.000 | - | Rp 1.750.000 |

| | |
|---|---|
| Subtotal | Rp 23.000.000 |
| Ongkos kirim | Rp 200.000 |
| DPP | Rp 23.200.000 |
| PPN 12% (DPP nilai lain 11/12 = Rp 21.266.667) | Rp 2.552.000 |
| **TOTAL** | **Rp 25.752.000** |

Terbilang: *Dua Puluh Lima Juta Tujuh Ratus Lima Puluh Dua Ribu Rupiah*

**Syarat & ketentuan**
1. Harga sudah termasuk PPN (rincian di atas).
2. Penawaran berlaku sampai 30 September 2026 mengingat fluktuasi harga unit AC.
3. Pembayaran: DP 30% saat PO diterima, pelunasan 70% setelah seluruh unit terpasang, ke [Bank – No. Rek – a.n. CV Teknik Mandiri Fiktif].
4. Pengiriman & pemasangan: [isi estimasi] setelah DP diterima; ongkos kirim sudah termasuk dalam penawaran.

Demikian penawaran ini kami sampaikan. Besar harapan kami dapat bekerja sama dengan Klinik Sehat Sentosa Fiktif. Untuk konfirmasi pesanan, Bapak dapat menghubungi kami di WA [nomor].

Hormat kami,

[Nama]
[Jabatan] – CV Teknik Mandiri Fiktif

**Asumsi yang dipakai**
- Ongkos kirim dan jasa pasang ditagihkan oleh CV sendiri sehingga **ikut dihitung dalam DPP (dikenai PPN)**. Jika ongkir hanya titipan biaya kurir pihak ketiga yang ditagihkan terpisah, beri tahu saya — PPN akan dihitung tanpa ongkir.
- Merek/tipe AC, garansi, dan estimasi waktu pasang belum diberikan → tidak dicantumkan / `[isi]`.

**Catatan:** Perhitungan PPN mengikuti PMK 131/2024 (berlaku per 2026-09-23): 12% × DPP nilai lain 11/12 (efektif 11%). Nilai di faktur pajak Coretax bisa selisih Rp 1 karena pembulatan. Bukan nasihat pajak; kasus khusus konsultasikan ke konsultan pajak/KPP.

### (B) Teks WhatsApp
```
Selamat siang, dr. Budi 🙏
Berikut penawaran harga dari CV Teknik Mandiri Fiktif untuk AC klinik:
• AC split 1 PK – 5 unit × Rp 4.250.000
• Jasa pasang + pipa 3 m – 5 titik × Rp 350.000
Total: *Rp 25.752.000* (sudah termasuk PPN & ongkir)
Berlaku s.d. 30 September 2026. DP 30%, pelunasan setelah terpasang.
Surat penawaran resmi (PDF) terlampir. Jika ada yang ingin disesuaikan, kabari saja ya, Pak.
```

## Catatan penguji
- Verifikasi independen: 21.250.000 + 1.750.000 + 200.000 = 23.200.000; 23.200.000 × 11/12 = 21.266.666,67; × 12% = 2.552.000; total 25.752.000. Benar.
- Ongkir masuk DPP secara default: **masuk akal** (ongkir yang ditagih penjual lazimnya bagian dari harga jual/penggantian yang menjadi DPP). Namun SKILL.md **tidak menyuruh agent memberi tahu** pengguna soal ini; penguji menambahkannya ke "Asumsi" secara inisiatif. Perlu dijadikan instruksi eksplisit (lihat HASIL-UJI).
- Bagus: syarat custom (7 hari, DP 30%) dipakai, label PPN jelas, disclaimer pajak dengan tanggal.
