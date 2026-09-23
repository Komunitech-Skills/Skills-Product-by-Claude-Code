# Contoh 06 – Titip jual pomade ke barbershop, skenario ditulis dengan koma (uji ulang v1.0.1)

## Skenario
Skenario tambahan uji ulang v1.0.1. Pengguna menulis perkiraan penjualan dengan koma ("10,20,30"), pola input yang pada v1.0.0 terbaca sebagai 102.030 unit. Tujuannya membuktikan cacat berat lama sudah beres, baik saat agent mengikuti SKILL.md (memakai `;`) maupun saat agent menyalin koma apa adanya. Semua nama usaha fiktif.

## Input pengguna
```
aku punya pomade "Klimis Jaya" (fiktif) mau titip jual di barbershop Cukur Rapi (fiktif), 3 cabang. harga jual 65rb, barbershop dapet 25%. modal aku 30rb. perkiraan laku 10,20,30 pcs per cabang sebulan. bikinin proposal singkat ya
```

## Proses (dijalankan agent, sesuai SKILL.md langkah 3)
```
$ python3 scripts/hitung_skema.py konsinyasi --harga-jual 65rb --porsi-toko 25% --modal 30rb --skenario "10;20;30" --format teks

Per unit: harga jual Rp 65.000 | toko Rp 16.250 (25%) | pemilik barang Rp 48.750
Modal Rp 30.000 -> laba kotor pemilik Rp 18.750/unit

| Skenario | Terjual | Omzet | Bagian toko | Bagian pemilik barang | Laba kotor pemilik |
|---|---|---|---|---|---|
| Pesimis | 10 | Rp 650.000 | Rp 162.500 | Rp 487.500 | Rp 187.500 |
| Realistis | 20 | Rp 1.300.000 | Rp 325.000 | Rp 975.000 | Rp 375.000 |
| Optimis | 30 | Rp 1.950.000 | Rp 487.500 | Rp 1.462.500 | Rp 562.500 |
```
Perintah yang sama dengan `--skenario "10,20,30"` (koma disalin apa adanya) menghasilkan output **identik** (md5 sama). Pada v1.0.0 input ini menjadi 1 skenario 102.030 unit.

**Hanya untuk kamu (tidak masuk proposal):** tiap pomade terjual, kamu terima Rp 48.750. Setelah dikurangi modal Rp 30.000, laba kotormu Rp 18.750 per pcs, atau Rp 187.500 sampai Rp 562.500 per cabang per bulan. Angka ini belum termasuk ongkos antar barang.

## Output

# Proposal Kerja Sama Titip Jual – Klimis Jaya × Cukur Rapi

**Ringkasan:** Klimis Jaya adalah pomade lokal yang ingin dititipkan di 3 cabang Cukur Rapi. Cukur Rapi mendapat 25% dari setiap pomade terjual, tanpa modal stok. Pelanggan juga bisa langsung membeli produk penata rambut setelah dicukur.

**Peluang untuk Cukur Rapi:** Pelanggan barbershop sering bertanya "pakai pomade apa tadi?" setelah rambutnya ditata. Dengan produk tersedia di meja kasir, pertanyaan itu langsung menjadi penjualan tambahan bagi Cukur Rapi, tanpa perlu menyetok atau membayar di muka.

**Yang kami tawarkan:**
- Stok awal [isi] pcs per cabang, diisi ulang sesuai penjualan.
- Display kecil untuk meja kasir.
- Tester untuk dipakai kapster saat menata rambut pelanggan.

**Skema kerja sama:**
- Harga jual ke pelanggan Rp 65.000 per pcs. Cukur Rapi mendapat Rp 16.250 (25%) per pcs terjual.
- Barang tetap milik kami sampai terjual. Barang yang tidak laku atau rusak kemasannya kami tarik tanpa biaya.
- Rekap stok dan pembayaran setiap akhir bulan: [transfer / tunai saat isi ulang].
- Harga jual sama di semua cabang agar tidak membingungkan pelanggan.

*Simulasi pendapatan Cukur Rapi per cabang per bulan (perkiraan, bukan jaminan):*

| Terjual per cabang/bulan | 10 pcs | 20 pcs | 30 pcs |
|---|---|---|---|
| Pendapatan Cukur Rapi per cabang | Rp 162.500 | Rp 325.000 | Rp 487.500 |

**Manfaat untuk Cukur Rapi:**
- Pemasukan tambahan tanpa modal dan tanpa risiko stok tidak laku.
- Layanan terasa lebih lengkap: potong, tata, dan pelanggan bisa membawa pulang produknya.
- Kerja tambahan minimal: cukup mencatat penjualan, isi ulang stok kami yang urus.

**Langkah berikutnya:** Uji coba 3 bulan di 3 cabang mulai [tanggal], lalu evaluasi bersama. Kami ingin mampir 15 menit untuk menunjukkan produk dan tester. Kapan waktu yang cocok?

Kontak: [Nama] – Pemilik Klimis Jaya – WA 0812-0000-xxxx – [email]

---

**Pesan pengantar WA**
```
Halo Kak [nama], saya [nama] dari Klimis Jaya, pomade lokal.
Kami ingin menawarkan titip jual di 3 cabang Cukur Rapi: Cukur Rapi dapat 25% (Rp 16.250) dari setiap pomade terjual, tanpa modal stok. Barang tidak laku kami tarik.
Proposal singkatnya saya lampirkan ya.
Boleh saya mampir 15 menit minggu ini untuk menunjukkan produk dan tester? Terima kasih 🙏
```

**Email**
- Subjek: Penawaran Titip Jual Pomade Klimis Jaya untuk Cukur Rapi (Uji Coba 3 Bulan)
- Isi: Yth. Bapak/Ibu [nama], perkenalkan saya [nama] dari Klimis Jaya. Terlampir proposal singkat titip jual pomade di 3 cabang Cukur Rapi. Cukur Rapi memperoleh 25% dari setiap produk terjual tanpa modal stok, dan barang tidak laku kami tarik. Kami mengusulkan uji coba 3 bulan dan ingin berdiskusi singkat di waktu yang Bapak/Ibu tentukan. Hormat kami, [nama] – WA 0812-0000-xxxx.

**Asumsi:** stok awal, cara bayar, dan tanggal mulai belum disebut, jadi ditulis `[isi]`. Uji coba 3 bulan adalah default skill. Klaim BPOM/notifikasi kosmetik tidak dicantumkan karena tidak disebut. Pomade termasuk kosmetik, jadi pastikan izin edarnya sudah ada sebelum menitipkan. Setelah sepakat, tuangkan dalam perjanjian tertulis (bermeterai Rp10.000).

## Catatan penguji
- **Cacat berat v1.0.0 sudah beres:** `"10,20,30"` kini dibaca sebagai 3 skenario (10/20/30). Output identik dengan pemisah `;`.
- **Verifikasi independen** (python terpisah, bilangan bulat): 65.000 × 25% = 16.250. Untuk 10/20/30 pcs, bagian toko 162.500 / 325.000 / 487.500 dan bagian pemilik 487.500 / 975.000 / 1.462.500. Bagian toko + bagian pemilik = omzet (650.000 / 1.300.000 / 1.950.000). Laba kotor 18.750 × q. **Cocok 100%.**
- Bagus: modal dan laba tidak masuk proposal. Izin edar kosmetik diingatkan di Asumsi, bukan diklaim.
- Catatan: agent tetap sebaiknya menulis `;` sesuai SKILL.md. Pemisah spasi (`"10 20 30"`) masih terbaca 102.030 unit (lihat HASIL-UJI.md, cacat S1).
