# Uji A/B — Tanpa skill vs dengan skill (skenario normal 1: warung bakso)

> Penguji independen, 2026-09-29. Permintaan sama persis dengan `01-uji-warung-bakso.md`. Keterbatasan: output "tanpa skill" disimulasikan oleh agent penguji dengan gaya jawaban umum model tanpa instruksi skill (bukan sesi terpisah yang benar-benar bersih); representatif untuk pola jawaban generik, namun dinilai konservatif.

## A. Tanpa skill (ringkasan keluaran agent umum)

> **Rencana Marketing 3 Bulan Warung Bakso**
> **Tujuan:** meningkatkan penjualan dan brand awareness, terutama malam hari.
> **Strategi:** 1) Optimasi media sosial (IG, TikTok, posting 1x sehari). 2) Google My Business. 3) Promo: diskon 20% jam 17-21, beli 2 gratis es teh. 4) GoFood/GrabFood: ikut promo platform. 5) **WhatsApp broadcast** ke pelanggan dan grup-grup perumahan. 6) Endorse food vlogger lokal.
> **Anggaran Rp 3 jt/bulan:** Iklan IG/FB Rp 1.000.000; Endorse Rp 1.000.000; Promo diskon Rp 500.000; Konten Rp 300.000; Lain-lain Rp 200.000.
> **KPI:** followers +1.000, omzet naik 20-30%, engagement rate 5%.
> **Timeline:** Bulan 1 branding, Bulan 2 promo, Bulan 3 evaluasi.

## B. Dengan skill
Lihat `01-uji-warung-bakso.md` (12 bagian lengkap).

## Perbandingan
| Aspek | Tanpa skill | Dengan skill |
|---|---|---|
| Tujuan | "naikkan penjualan & awareness", omzet +20-30% (tanpa dasar, tanpa tenggat) | SMART: +Rp 12 jt/bulan (≈ 1.800 nota/kuartal), nota malam +20/hari, tenggat 31 Des, cara ukur |
| Cek kelayakan margin | Tidak ada | Margin Rp 10.000/nota (50%); **GoFood dihitung terpisah: margin Rp 6.000, ROAS impas 3,34** |
| Diskon 20% | Disarankan tanpa cek; memotong 40% margin (Rp 4.000 dari Rp 10.000) | Promo dirujuk ke `promo-kalender` untuk cek margin dulu |
| Batas biaya iklan | Tidak ada | CAC impas Rp 10.000, target Rp 8.000, aturan hentikan 4 minggu |
| Anggaran | Angka bulat tanpa alasan, kuartal tidak dijumlah | Rp 9 jt dibagi per kanal & per bulan, cadangan 10%, jumlah dicek = anggaran (script) |
| Corong | Tidak ada | 300.000 jangkauan -> 4.500 klik -> 900 kunjungan -> 360 pembeli (berlabel asumsi) |
| WhatsApp | **"WA broadcast ke grup-grup perumahan"** (risiko spam/blokir) | Hanya ke pelanggan yang pernah chat/beli + kartu stempel |
| KPI | Followers & engagement (vanity) | Per tahap corong, sumber data, pemilik, jadwal cek |
| Kalender Indonesia | Umum (bulan 1-2-3) | Musim hujan, gajian 25, libur sekolah/tahun baru, tanggal diverifikasi |
| Langkah minggu ini | Tidak ada | 3 langkah konkret |
| Asumsi ditulis | Tidak | Ya, di bagian atas |

## Kesimpulan
Dengan skill **jelas lebih baik**: angka dihitung (bukan dikira), menghindari dua saran berisiko dari jawaban generik (diskon 20% tanpa cek margin, broadcast WA ke grup), dan hasilnya dokumen siap jalan. Syarat nilai tambah Tahap 6 butir 4 terpenuhi.
