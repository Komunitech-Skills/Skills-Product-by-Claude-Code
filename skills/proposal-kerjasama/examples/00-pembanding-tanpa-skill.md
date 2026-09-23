# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama dengan S1):**
> Saya punya usaha sambal botol "Sambal Bu Tatik Fiktif" di Malang, sudah jalan 2 tahun, jualan online dan di CFD. Mau titip jual di Toko Oleh-oleh Pusaka Fiktif yang punya 3 cabang di Batu. Harga jual di toko 35rb per botol, toko ambil 25%. Modal saya 18rb per botol. Tolong buatkan proposalnya, singkat aja 1 halaman.

## Output TANPA skill (AI agent biasa, lengkap)
```
PROPOSAL KERJA SAMA KONSINYASI
Sambal Bu Tatik – Toko Oleh-oleh Pusaka

I. Pendahuluan
Sambal Bu Tatik merupakan usaha sambal botol dari Malang yang telah berdiri selama 2 tahun
dengan cita rasa khas, dibuat dari bahan-bahan alami pilihan tanpa pengawet, dan telah
dipercaya ratusan pelanggan.

II. Tujuan
Menjalin kerja sama konsinyasi untuk memperluas pemasaran produk di 3 cabang Toko Oleh-oleh Pusaka.

III. Profil Produk
- Sambal bawang, sambal cumi, sambal teri (varian dapat disesuaikan)
- Harga jual: Rp 35.000/botol

IV. Skema Kerja Sama
- Sistem konsinyasi dengan pembagian 75% untuk kami dan 25% untuk toko.
- Harga modal Rp 18.000, sehingga keuntungan kami per botol Rp 8.250 dan toko Rp 8.750.
- Pembayaran dilakukan setiap bulan.

V. Keuntungan bagi Toko
- Tidak perlu modal
- Produk berkualitas dan diminati

VI. Penutup
Demikian proposal ini kami buat. Besar harapan kami agar kerja sama ini dapat terwujud.
```

## Output DENGAN skill
Lihat `01-titip-jual-sambal-ke-toko-oleh-oleh.md` (proposal 1 halaman + tabel simulasi pendapatan toko + WA + email + tabel internal untuk pengguna).

## Perbandingan

| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Fokus | Memuji produk sendiri, "tujuan kami" | Untung & risiko **mitra** di setiap bagian |
| Data internal | **Bocor**: modal Rp 18.000 & laba Rp 8.250 ditulis di proposal (melemahkan posisi tawar) | Modal/laba hanya ditunjukkan ke pengguna |
| Klaim | **Dikarang**: "tanpa pengawet", "ratusan pelanggan", 3 varian yang tidak disebut | Tidak ada klaim yang tidak diberikan; izin PIRT/halal disarankan ditambah bila ada |
| Simulasi angka | Tidak ada simulasi pendapatan toko per bulan | Tabel 30/60/100 botol per cabang, dihitung script, berlabel perkiraan |
| Mekanisme | Tidak ada isi ulang stok, retur/kedaluwarsa, nota | Isi ulang mingguan, tarik & ganti barang rusak, rekap bulanan |
| Langkah berikutnya | "Semoga terwujud" | Uji coba 3 bulan di 1–2 cabang + ajakan antar sampel 15 menit |
| Pesan pengantar | Tidak ada | WA ≤ 8 baris + email subjek & isi |

## Penilaian
Hasil dengan skill **jelas lebih baik**: tidak membocorkan modal, tidak mengarang klaim (risiko hukum untuk klaim pangan), menjawab pertanyaan utama toko ("dapat berapa, repot tidak, kalau tidak laku bagaimana"), dan langsung siap kirim beserta pesan pengantarnya.
