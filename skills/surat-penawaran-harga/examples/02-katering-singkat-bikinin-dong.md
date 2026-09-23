# 02 — Permintaan singkat "bikinin dong" (katering, bukan PKP)

**Skenario:** S2 — permintaan normal tapi malas/singkat. Data inti (penjual, pembeli, item, harga) ada; sisanya pakai default + asumsi.

**Input pengguna:**
> bikinin dong sph dari Dapur Berkah Fiktif bekasi ke panitia seminar PT Fiktif Jaya Abadi, 200 snack box 18rb, 200 kopi/teh 8rb, diskon 5%. aku ga pkp

**Perintah script yang dijalankan:**
```bash
python3 scripts/hitung_sph.py \
  --item "Snack box (3 kue + air mineral)|200|box|18rb" \
  --item "Kopi/teh sachet + gelas|200|cup|8rb" \
  --diskon-total 5% --nomor-urut 1 --kode "SPH/DB" --tanggal 2026-09-23 --format teks
```
Hasil: Subtotal Rp 5.200.000; diskon 5% −Rp 260.000; TOTAL Rp 4.940.000.

## Output

### (A) Surat penawaran

**DAPUR BERKAH FIKTIF**
[Alamat], Bekasi · WA [nomor] · [email]

---

Nomor    : 001/SPH/DB/IX/2026
Lampiran : -
Perihal  : Penawaran Harga Konsumsi Seminar

Bekasi, 23 September 2026

Kepada Yth.
[Nama PIC] – Panitia Seminar
PT Fiktif Jaya Abadi
di tempat

Dengan hormat,
Menindaklanjuti permintaan Bapak/Ibu, bersama ini kami sampaikan penawaran harga konsumsi untuk kegiatan seminar sebagai berikut:

| No | Uraian | Qty | Satuan | Harga Satuan | Diskon | Jumlah |
|---|---|---|---|---|---|---|
| 1 | Snack box (3 kue + air mineral) | 200 | box | Rp 18.000 | - | Rp 3.600.000 |
| 2 | Kopi/teh sachet + gelas | 200 | cup | Rp 8.000 | - | Rp 1.600.000 |

| | |
|---|---|
| Subtotal | Rp 5.200.000 |
| Diskon tambahan (5%) | −Rp 260.000 |
| **TOTAL** | **Rp 4.940.000** |

Terbilang: *Empat Juta Sembilan Ratus Empat Puluh Ribu Rupiah*

**Syarat & ketentuan**
1. Harga tidak dikenakan PPN.
2. Penawaran berlaku sampai 7 Oktober 2026.
3. Pembayaran: DP 50% saat pesanan dikonfirmasi, pelunasan sebelum pesanan dikirim, ke [Bank – No. Rek – a.n.].
4. Pengiriman: [isi tanggal & jam acara]; harga belum termasuk ongkos kirim.

Demikian penawaran ini kami sampaikan. Besar harapan kami dapat melayani kebutuhan konsumsi seminar PT Fiktif Jaya Abadi. Untuk konfirmasi pesanan, Bapak/Ibu dapat menghubungi kami di WA [nomor].

Hormat kami,

[Nama]
[Jabatan] – Dapur Berkah Fiktif

**Asumsi yang dipakai**
- "snack box 18rb" & "kopi/teh 8rb" dibaca sebagai harga per box/cup; isi snack box ditulis contoh — mohon sesuaikan.
- Diskon 5% dihitung dari total semua item.
- Nomor urut 001, masa berlaku 14 hari, DP 50%, ongkir belum termasuk (default karena tidak disebutkan).
- Alamat, WA, nama PIC, penanda tangan, rekening belum ada → `[isi]`.

### (B) Teks WhatsApp
```
Selamat siang, Bapak/Ibu 🙏
Berikut penawaran harga dari Dapur Berkah Fiktif untuk konsumsi seminar:
• Snack box – 200 box × Rp 18.000
• Kopi/teh – 200 cup × Rp 8.000
Total: *Rp 4.940.000* (sudah diskon 5%, tanpa PPN, belum ongkir)
Berlaku s.d. 7 Oktober 2026. DP 50% saat konfirmasi, pelunasan sebelum kirim.
Surat penawaran resmi (PDF) terlampir. Jika ada yang ingin disesuaikan, kabari saja ya.
```

Mau saya isi alamat/WA/rekening sekalian, atau ongkirnya dimasukkan ke total?

## Catatan penguji
- Angka benar (5.200.000 × 95% = 4.940.000).
- Bagus: tidak bertanya berulang-ulang untuk permintaan singkat; asumsi disebut jelas; placeholder `[isi]` rapi.
- Kurang (ringan): isi snack box tidak diberikan pengguna — agent harus hati-hati tidak mengarang spesifikasi (checklist SKILL.md sudah melarang klaim yang tidak diberikan; di sini ditandai "contoh — mohon sesuaikan"). Idealnya uraian cukup "Snack box".
