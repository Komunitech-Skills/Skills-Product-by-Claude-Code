# Riwayat perubahan — program-referral-loyalitas

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## 1.0.6 (2026-10-13) — rujukan ke skill arsip (`caption-sosmed-umkm`) diganti `konten-mingguan` (`SKILL.md`). Script tidak berubah.

## Riwayat versi
- **1.0.5 (2026-10-02):** temuan uji gabungan paket klinik (S3): pengecualian faskes kini menyebut eksplisit merchandise, voucher, dan layanan gratis (mis. "cek tensi gratis") sebagai imbalan rujukan yang tidak dirancang. Script tidak berubah. Tetap PERLU REVIEW tenaga medis/hukum.
- **1.0.2 (2026-09-30):** temuan uji ulang: kartu info klinik kini untuk pasien sendiri; klinik tidak meminta/mendorong pasien membagikannya (KODEKGI 2020 Pasal 3 butir 1.2.4 & Pasal 5, KODEKI Pasal 3). Tetap PERLU REVIEW tenaga medis/hukum.
- **1.0.1 (2026-09-30):** script menerima angka format Indonesia di semua isian (uang dan jumlah: `40.000`, `1.500.000`, `Rp38.000`, `38rb`, `1,5jt`, desimal koma `0,25`/`12,5`); angka yang bisa dibaca dua arah ditolak dengan pesan jelas, tidak ditebak. Fasilitas kesehatan: tidak lagi merancang hadiah/diskon untuk merujuk pasien (Permenkes 1787/2010 Pasal 5, kode etik profesi); diganti edukasi, pengingat kontrol, dan kartu info tanpa imbalan. Status `impas` tidak lagi "AMAN" bila pesanan pertama rugi (status `RUGI DI PESANAN PERTAMA`); batas hadiah pemberi diberi label BATAS ATAS (bukan anjuran) plus hadiah SARAN yang lebih konservatif. Tes regresi 26 -> 43.
- **1.0.0 (2026-09-30):** rilis awal.
