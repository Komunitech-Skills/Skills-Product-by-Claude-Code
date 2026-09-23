# 01 — Titip jual (konsinyasi) sambal ke toko oleh-oleh, versi singkat

**Skenario:** S1 — permintaan normal, konsinyasi dengan porsi toko %, modal diberikan (tidak boleh bocor ke proposal).

**Input pengguna:**
> Saya punya usaha sambal botol "Sambal Bu Tatik Fiktif" di Malang, sudah jalan 2 tahun, jualan online dan di CFD. Mau titip jual di Toko Oleh-oleh Pusaka Fiktif yang punya 3 cabang di Batu. Harga jual di toko 35rb per botol, toko ambil 25%. Modal saya 18rb per botol. Tolong buatkan proposalnya, singkat aja 1 halaman.

**Perintah script:**
```bash
python3 scripts/hitung_skema.py konsinyasi --harga-jual 35rb --porsi-toko 25% --modal 18rb --skenario "30;60;100" --format teks
```
Hasil (per cabang per bulan): toko Rp 8.750/botol → 30 botol Rp 262.500 · 60 botol Rp 525.000 · 100 botol Rp 875.000. Laba kotor pemilik Rp 8.250/botol (hanya untuk pengguna).

## Output

### Untuk Anda (tidak masuk proposal)
| Skenario/cabang/bulan | Terjual | Bagian toko | Bagian Anda | Laba kotor Anda (modal Rp 18.000) |
|---|---|---|---|---|
| Pesimis | 30 | Rp 262.500 | Rp 787.500 | Rp 247.500 |
| Realistis | 60 | Rp 525.000 | Rp 1.575.000 | Rp 495.000 |
| Optimis | 100 | Rp 875.000 | Rp 2.625.000 | Rp 825.000 |

Laba kotor Anda Rp 8.250/botol (belum termasuk ongkos antar & botol yang rusak/tidak laku). Skema aman (tidak rugi).

---

### Proposal (siap kirim)

# Proposal Kerja Sama Titip Jual – Sambal Bu Tatik Fiktif × Toko Oleh-oleh Pusaka Fiktif

**Ringkasan:** Sambal Bu Tatik Fiktif adalah sambal botol rumahan dari Malang yang sudah berjalan 2 tahun. Kami ingin menitipkan produk di 3 cabang Toko Oleh-oleh Pusaka Fiktif di Batu. Toko mendapat 25% dari setiap botol terjual, tanpa modal stok dan tanpa risiko barang tidak laku.

**Peluang untuk Pusaka:** Wisatawan di Batu mencari oleh-oleh khas Malang yang praktis dibawa pulang. Sambal botol melengkapi rak camilan dan kerupuk, dan cocok dibeli bersamaan.

**Yang kami tawarkan:**
- Sambal botol siap jual dengan label lengkap, harga jual Rp 35.000/botol.
- Stok awal [isi] botol per cabang, diisi ulang setiap minggu oleh kami.
- Display/rak kecil kami sediakan bila dibutuhkan.

**Skema kerja sama:**
- Sistem titip jual (konsinyasi): Pusaka membayar hanya botol yang terjual.
- Pusaka mendapat **Rp 8.750 (25%)** per botol terjual.
- Rekap stok & pembayaran setiap akhir bulan melalui transfer, berdasarkan nota titip.
- Produk rusak atau mendekati kedaluwarsa kami tarik dan ganti tanpa biaya.

*Simulasi pendapatan Pusaka per cabang per bulan (perkiraan, bukan jaminan):*

| Terjual per cabang/bulan | 30 botol | 60 botol | 100 botol |
|---|---|---|---|
| Pendapatan Pusaka | Rp 262.500 | Rp 525.000 | Rp 875.000 |

**Manfaat untuk Pusaka:**
- Tambahan produk oleh-oleh tanpa modal dan tanpa risiko stok mati.
- Pengisian ulang & perawatan display kami yang urus.
- Pembayaran sederhana, sekali sebulan.

**Langkah berikutnya:** Uji coba 3 bulan mulai [tanggal] di 1–2 cabang dulu, lalu evaluasi bersama. Kami siap mengantar sampel dan menjelaskan langsung 15 menit di waktu yang Bapak/Ibu tentukan.

Kontak: [Nama] – Pemilik Sambal Bu Tatik Fiktif – WA 0812-0000-2201 – [email]

---

### Pesan pengantar WhatsApp
```
Selamat siang, Pak/Bu [Nama] 🙏
Saya [nama] dari Sambal Bu Tatik Fiktif, sambal botol rumahan dari Malang. Kami ingin mengajukan kerja sama titip jual di Pusaka: toko mendapat 25% per botol terjual, tanpa modal stok.
Proposal singkatnya saya lampirkan (1 halaman). Kalau berkenan, boleh saya minta waktu 15 menit minggu ini untuk mengantar sampel?
Terima kasih, Pak/Bu.
```

### Email
**Subjek:** Proposal Kerja Sama Titip Jual – Sambal Bu Tatik Fiktif × Toko Oleh-oleh Pusaka Fiktif

Yth. Bapak/Ibu [Nama],
Perkenalkan, saya [nama] dari Sambal Bu Tatik Fiktif, sambal botol rumahan dari Malang yang sudah berjalan 2 tahun. Kami ingin menawarkan kerja sama titip jual di 3 cabang Pusaka: toko mendapat 25% per botol terjual, tanpa modal stok, dan barang rusak kami ganti. Proposal singkat terlampir.
Jika berkenan, kami ingin menjadwalkan diskusi 15–20 menit sekaligus mengantar sampel.
Hormat saya,
[Nama] – WA 0812-0000-2201

**Asumsi:** skenario 30/60/100 botol per cabang per bulan dipilih sebagai simulasi; stok awal, isi ulang mingguan, display, dan uji coba 3 bulan adalah usulan standar — mohon dikonfirmasi. Klaim halal/PIRT/BPOM tidak dicantumkan karena tidak disebutkan; jika sudah punya, sebaiknya ditambahkan (toko oleh-oleh biasanya menanyakannya). Setelah sepakat, tuangkan dalam perjanjian tertulis (bermeterai Rp10.000).

## Catatan penguji
- Angka diverifikasi manual: 35.000 × 25% = 8.750; × 30/60/100 = 262.500/525.000/875.000. Benar.
- Bagus: fokus ke untung mitra; data modal/laba dipisah dan tidak masuk proposal; label "perkiraan, bukan jaminan"; tidak mengarang izin PIRT/halal.
- Panjang proposal ± 300 kata (sesuai batas ±350).
