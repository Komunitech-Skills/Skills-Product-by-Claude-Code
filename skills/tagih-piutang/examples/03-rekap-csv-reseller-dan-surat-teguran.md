# 03 — Rekap umur piutang dari CSV + surat teguran dengan denda tertulis

**Skenario:** S3 — banyak tagihan (CSV), tentukan prioritas, lalu surat teguran (tahap 6) untuk yang terlama dengan denda yang tercantum di syarat invoice.

**Input pengguna:**
> Saya toko bahan kue Sumber Manis Fiktif di Medan. Ini daftar piutang reseller saya (file piutang.csv). Mana yang harus ditagih duluan? Terus buatin surat teguran buat yang paling parah. Di setiap invoice kami ada syarat tertulis "denda 2% per bulan dari sisa tagihan, maksimal 10%" dan invoice-nya ditandatangani pembeli saat terima barang. Rekening BRI 0000-00-000000-00-0 a.n. Sumber Manis Fiktif.

**Isi `piutang.csv`:**
```
pelanggan,no_invoice,nominal,jatuh_tempo,dibayar
Toko Kue Melati Fiktif,INV-BK-0612,"Rp 4.750.000",2026-07-10,"Rp 1.000.000"
Reseller Bu Ani Fiktif,INV-BK-0701,2.300.000,2026-08-15,
Dapur Cake Fiktif,INV-BK-0705,3.150.000,2026-09-12,
Roti Sehat Fiktif,INV-BK-0710,1.800.000,2026-09-30,
Kue Nusantara Fiktif,INV-BK-0615,950.000,2026-07-20,950.000
```

**Perintah script:**
```bash
python3 scripts/hitung_telat.py --file piutang.csv --tanggal 2026-09-23 --format teks
python3 scripts/hitung_telat.py --nominal "Rp 4.750.000" --dibayar "Rp 1.000.000" --jatuh-tempo 2026-07-10 \
  --tanggal 2026-09-23 --denda-persen 2 --denda-per bulan --denda-maks 10% \
  --dasar-denda "Syarat pembayaran pada Invoice INV-BK-0612 yang ditandatangani pembeli" --format teks
```

## Output

### Rekap umur piutang per 23 September 2026 – total Rp 11.000.000

| Umur | Jumlah invoice | Total |
|---|---|---|
| Belum jatuh tempo | 1 | Rp 1.800.000 |
| 1–30 hari | 1 | Rp 3.150.000 |
| 31–60 hari | 1 | Rp 2.300.000 |
| 61–90 hari | 1 | Rp 3.750.000 |
| > 90 hari | 0 | Rp 0 |

### Urutan prioritas penagihan
| # | Pelanggan | Invoice | Sisa | Jatuh tempo | Terlambat | Tindakan |
|---|---|---|---|---|---|---|
| 1 | Toko Kue Melati Fiktif | INV-BK-0612 | Rp 3.750.000 | 10 Juli 2026 | 75 hari | **Surat teguran (tahap 6)** — di bawah |
| 2 | Reseller Bu Ani Fiktif | INV-BK-0701 | Rp 2.300.000 | 15 Agustus 2026 | 39 hari | Tahap 6 menurut umur; **jika belum pernah ditagih, mulai dari pemberitahuan resmi tahap 5 dulu** |
| 3 | Dapur Cake Fiktif | INV-BK-0705 | Rp 3.150.000 | 12 September 2026 | 11 hari | Tahap 4: WA tegas-sopan, minta tanggal pasti |
| 4 | Roti Sehat Fiktif | INV-BK-0710 | Rp 1.800.000 | 30 September 2026 | – | Pengingat halus tanggal 27 September (H-3) |

Kue Nusantara Fiktif (INV-BK-0615) sudah lunas → kirim ucapan terima kasih saja.

### Ringkasan tagihan – Toko Kue Melati Fiktif
Tagihan Rp 4.750.000 · sudah dibayar Rp 1.000.000 · **sisa Rp 3.750.000** · jatuh tempo 10 Juli 2026 · terlambat 75 hari · Tahap 6.
Denda: **Rp 225.000** = Rp 3.750.000 × 2% × 3 bulan (75 hari = 3 periode 30 hari atau bagiannya; batas maksimal 10% = Rp 375.000 tidak terlampaui). Dasar: syarat pembayaran pada Invoice INV-BK-0612 yang ditandatangani pembeli.
**Total: Rp 3.975.000.**

### Pesan tahap 6 · Surat (PDF + email + kurir bertanda terima) · kirim 23 September 2026
```
TOKO BAHAN KUE SUMBER MANIS FIKTIF
[Alamat], Medan · WA [nomor] · [email]

Nomor   : 001/SP/IX/2026
Lampiran: Salinan Invoice INV-BK-0612 & bukti serah terima barang
Perihal : Surat Teguran Pertama – Pembayaran Invoice INV-BK-0612

Medan, 23 September 2026

Kepada Yth.
Pemilik Toko Kue Melati Fiktif
[Alamat]

Dengan hormat,
1. Pada [tanggal] kami telah mengirimkan barang sesuai pesanan Bapak/Ibu dan menerbitkan Invoice No. INV-BK-0612 senilai Rp 4.750.000 dengan jatuh tempo 10 Juli 2026. Invoice tersebut telah ditandatangani saat barang diterima.
2. Pengingat pembayaran telah kami sampaikan pada [tanggal-tanggal pengingat] melalui [WA/telepon].
3. Pembayaran yang telah kami terima sebesar Rp 1.000.000, sehingga sisa kewajiban adalah Rp 3.750.000.
4. Sesuai syarat pembayaran yang tercantum pada Invoice INV-BK-0612 (denda 2% per bulan dari sisa tagihan, maksimal 10%), denda keterlambatan per 23 September 2026 adalah Rp 225.000. Total yang perlu diselesaikan: Rp 3.975.000.

Dengan surat ini kami meminta Bapak/Ibu menyelesaikan kewajiban tersebut paling lambat 30 September 2026 ke rekening BRI 0000-00-000000-00-0 a.n. Sumber Manis Fiktif, atau menghubungi kami sebelum tanggal tersebut untuk menyepakati jadwal pembayaran secara tertulis.

Apabila hingga batas waktu tersebut tidak ada pembayaran maupun tanggapan, dengan menyesal kami akan menempuh langkah penyelesaian sesuai peraturan perundang-undangan yang berlaku.

Demikian surat teguran ini kami sampaikan. Atas perhatiannya kami ucapkan terima kasih.

Hormat kami,

[Nama]
Pemilik – Toko Bahan Kue Sumber Manis Fiktif
```

**WA pengantar:** Selamat siang, Bapak/Ibu. Kami kirimkan surat teguran terkait Invoice INV-BK-0612 (sisa Rp 3.750.000 + denda sesuai syarat invoice). Jika ada kendala, kami terbuka membahas jadwal pembayaran sebelum 30 September 2026. Terima kasih.

### Tahap berikutnya (jika belum dibayar)
- 1 Oktober 2026 → hubungi via telepon; bila tidak ada tanggapan, teguran kedua 7–14 hari kemudian dengan tenggat lebih pendek.

### Saran tindakan
- Isi tanggal pengiriman barang dan tanggal pengingat sebelumnya — surat teguran harus berisi fakta, bukan perkiraan.
- Jika Toko Kue Melati menawar cicilan: buat kesepakatan tertulis (jumlah & tanggal tiap termin), ditandatangani kedua pihak dan dibubuhi meterai Rp10.000.
- Untuk sisa Rp 3.750.000, gugatan sederhana di pengadilan negeri dimungkinkan bila semua upaya gagal — konsultasikan ke advokat sebelum menempuh jalur ini.
- Hentikan pengiriman barang baru dengan tempo ke pelanggan ini sampai tagihan beres (boleh tetap jual dengan bayar di muka).

### Catatan hukum
Bukan nasihat hukum. Denda hanya ditagih karena ada syarat tertulis pada invoice yang ditandatangani pembeli; jika pembeli membantah pernah menyetujui syarat itu, prioritaskan pokok utang dan konsultasikan ke advokat. Dasar: KUHPerdata (wanprestasi/somasi), UU ITE, UU PDP, UU Bea Meterai — per 2026-09-23.

## Catatan penguji
- Angka diverifikasi independen: 10 Juli → 23 September = 75 hari; ⌈75/30⌉ = 3; 3.750.000 × 2% × 3 = 225.000; batas 10% = 375.000; total 3.975.000. Rekap CSV: total 11.000.000 (3.750.000 + 2.300.000 + 3.150.000 + 1.800.000), invoice lunas dikeluarkan dengan benar.
- **Temuan (sedang):** script dan SKILL.md menetapkan tahap hanya dari umur piutang. Reseller Bu Ani (39 hari) langsung "Tahap 6 – somasi" walau mungkin belum pernah ditagih; SKILL.md tidak punya aturan untuk menurunkan tahap bila riwayat penagihan kosong. Agent penguji menambahkan catatan secara inisiatif.
- Denda dari syarat pada invoice yang ditandatangani: skill menganggapnya "kesepakatan tertulis" (SKILL.md Input). Masuk akal, tetapi lebih lemah daripada klausul kontrak; catatan hukum di atas menambahkan kehati-hatian itu.
