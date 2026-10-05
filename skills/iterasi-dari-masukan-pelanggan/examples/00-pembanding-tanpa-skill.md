# Uji A/B - skenario normal 1 (toko hijab: 20 ulasan Shopee + 9 chat WA + 5 komentar IG)
Penguji independen, 2026-09-29. Data sama dengan `06-uji-toko-hijab-multikanal.md`.
Permintaan: "Ini ulasan Shopee, chat WA, dan komentar IG bulan September. Apa yang harus kami benahi dulu?"

Catatan kejujuran: jawaban "tanpa skill" disusun penguji sebagai agent umum yang membaca data mentah langsung (tanpa SKILL.md, tanpa script).
Penguji sudah membaca skill, jadi pembanding ini mungkin sedikit lebih rapi daripada agent yang benar-benar polos.

## A. Tanpa skill (ringkas, gaya jawaban agent umum)
> Dari ulasan dan chat, keluhan utama:
> 1. **Warna tidak sesuai foto** - beberapa pembeli (mis. Siti Aminah di WA, dan ulasan Shopee) bilang warna lebih gelap. Perbaiki foto produk.
> 2. **Jahitan lepas / bahan tipis** - sekitar 3-4 keluhan. Lakukan QC sebelum kirim.
> 3. **Pengiriman lama** - beberapa pembeli menunggu 5-7 hari; Rahma bahkan belum menerima paket seminggu dan chatnya tidak dibalas.
> 4. **Ukuran kekecilan** - perbarui size chart.
> 5. Harga dianggap naik; packing kadang sobek.
> Hal positif: bahan adem, admin ramah. Saran: perbaiki foto, QC, pilih ekspedisi lebih cepat, update size chart.

Ciri: temuan utama masuk akal (membaca 34 masukan cukup mudah untuk model), tetapi:
- **Menyebut nama pelanggan** (Siti Aminah, Rahma) dari data mentah - melanggar privasi bila laporan dibagikan ke tim.
- Angka "beberapa", "sekitar 3-4" - tidak ada jumlah/persentase per kanal; tidak ada skor dampak.
- Tidak ada backlog (siapa, tenggat, ukuran keberhasilan), draf balasan, kabar perbaikan, atau rencana ukur bulan depan.
- Tidak menyinggung bias kanal / jumlah data kecil; tidak menandai permintaan (warna pastel, restock sage, grosir 10 pcs) sebagai peluang.

## B. Dengan skill (agent mengikuti SKILL.md: daftar pengirim -> script -> verifikasi -> tema.json -> laporan)
Jalan pertama script gagal diam-diam (kolom `Ulasan Pembeli` tidak terbaca, lihat 06). Agent yang mengikuti langkah 4 (verifikasi kutipan)
melihat tanggal di "Perlu dibaca agent", menjalankan ulang dengan `--kolom-teks`, lalu menambah tema warna/jahitan/stok.
Ringkasan laporan yang dihasilkan (angka dari script jalan 3, koreksi agent disebut):
> **Ringkasan cepat:** (1) Warna tidak sesuai foto/pudar 4 keluhan + 1 di WA (koreksi agent) - 3 kanal; (2) jahitan lepas/bahan tipis 4 (12,1%)
> + 1 di WA yang script salah baca sebagai pujian; (3) pengiriman lama 3 (script 4; 1 sebenarnya salah kirim warna). Tindakan minggu ini: foto ulang
> produk di cahaya siang + tulis "warna bisa sedikit berbeda karena layar" + QC jahitan sebelum packing.
> **Sumber:** Shopee 19 (ulasan identik ke-2 terbuang sebagai duplikat - dicatat), WA 9 (bias: yang komplain), IG 5. Data < 30 = arah saja.
> **Backlog:** Segera - QC jahitan (Owner, 3 Okt, keluhan jahitan 0 bulan depan); Segera - foto ulang 6 warna terlaris (Admin, 7 Okt, keluhan warna < 5%);
> Bulan ini - ekspedisi reguler -> opsi instan area Jabodetabek + balas chat < 2 jam (Admin, 15 Okt); Pantau - size chart dengan cm & model tinggi badan.
> **Permintaan:** restock sage, warna pastel, grosir 10 pcs pengajian -> masalah di baliknya: pelanggan loyal ingin warna tertentu & pembelian kelompok;
> uji murah: pre-order warna pastel 20 pcs.
> **Tindak lanjut:** template A/B untuk yang mengeluh warna & jahitan (dikirim admin); kabar perbaikan akhir Oktober. Tanpa nama pelanggan.
> **Catatan metode:** 3 koreksi tema, 1 masukan pujian yang sebenarnya keluhan, penyamaran HP/alamat/resi dicek ulang.

## Penilaian
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Ketepatan isu teratas | Baik | Baik (setelah verifikasi agent) |
| Angka & persentase | Perkiraan | Dihitung script, koreksi disebut |
| Privasi | Nama pelanggan tersebut | Tersamar otomatis + dicek |
| Rencana tindakan | Saran umum | Backlog: siapa, tenggat, ukuran berangka |
| Menutup lingkaran ke pelanggan | Tidak ada | Draf balasan + kabar perbaikan (dikirim manusia) |
| Siklus bulanan/tren | Tidak ada | Ada (garis dasar) |
| Risiko | - | Jalan pertama script salah total; bergantung pada ketelitian agent |

**Kesimpulan: dengan skill JELAS lebih baik** sebagai hasil siap pakai (privasi, backlog, balasan, siklus). Keunggulan terutama berasal dari
alur SKILL.md dan template, **bukan** dari akurasi script; untuk data 30-an masukan, membaca langsung sama akuratnya dengan tema kata kunci.
