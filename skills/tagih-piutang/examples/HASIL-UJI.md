# HASIL UJI — tagih-piutang

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja sementara `/tmp/uji-tagih-piutang/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (`00-pembanding-tanpa-skill.md`) + banding pesaing (`00-banding-pesaing.md`)

## Audit keamanan
- `scripts/hitung_telat.py`: hanya `argparse, csv, json, math, re, sys, datetime, decimal`. Tidak ada jaringan, subprocess, penulisan file, kredensial; hanya membaca CSV dari `--file`.
- SKILL.md/README/references: tidak ada prompt injection. Pengaman kuat: menolak ancaman/mempermalukan/menghubungi keluarga, denda hanya bila tertulis, tidak menyebut polisi untuk utang dagang. **Aman.**

## Verifikasi angka (independen)
- Script terpisah (`verif.py`) membandingkan 400 kasus acak (pembayaran sebagian, tenggang 0–7, denda harian/bulanan/proporsional/tetap, batas % dan nominal, tanggal sebelum/sesudah jatuh tempo) dengan perhitungan Decimal independen untuk hari terlambat, sisa, denda, total, dan kode tahap → **0 selisih**.
- Contoh SKILL.md/README (sisa Rp 10.000.000, 30 hari, denda Rp 270.000, total Rp 10.270.000) → benar.
- Mode CSV: rekap umur piutang, urutan prioritas, baris lunas dikeluarkan, baris rusak dilewati dengan alasan, file kosong & kolom hilang → ditolak dengan pesan jelas.
- Data rusak/tepi yang ditangani baik: nominal 0, dibayar > nominal, tanggal 2026-13-01, tenggang negatif, denda persen + tetap sekaligus, "Rp 1.500.000,50", "23/09/2026", lunas.
- **Temuan:** `--denda-persen 0,100` → dibaca 100% per hari → denda Rp 110.000.000 atas pokok Rp 5.000.000 tanpa peringatan; `--denda-maks 5` (tanpa %) → batas Rp 5 tanpa peringatan.

## Verifikasi dasar hukum (`references/regulasi.md`)
- KUHPerdata 1238 (pernyataan lalai), 1243 (ganti rugi setelah lalai), 1250 (bunga moratoir, umumnya sejak dituntut di pengadilan) — ringkasan **masuk akal dan sesuai**. Kesimpulan "denda hanya bila disepakati tertulis" tepat.
- UU 1/2024 (perubahan kedua UU ITE) Pasal 27A (menyerang kehormatan, delik aduan) dan 27B (ancaman kekerasan / ancaman pencemaran atau membuka rahasia untuk memaksa memberi barang, membuat pengakuan utang, dsb.; ancaman pidana hingga 6 tahun dan/atau Rp1 miliar) — **sesuai**. Catatan: unsur 27B mensyaratkan maksud menguntungkan diri "secara melawan hukum"; ringkasan menyederhanakan, tetapi sebagai pagar risiko tetap tepat.
- KUHP baru (UU 1/2023) berlaku 2 Januari 2026 — **benar**; nomor pasal diberi label *(perlu review)* — **label verifikasi jujur**.
- Gugatan sederhana ≤ Rp500 juta (PERMA 2/2015 jo. PERMA 4/2019) — benar, berlabel *(perlu review)*.
- UU PDP 27/2022 — relevan.
- **Tidak tepat:** bea meterai — lihat cacat sedang #2.

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | Kata kunci ID/EN lengkap; batas dengan invoice & follow-up prospek jelas |
| Kemudahan awam | 9 | Satu kalimat cukup; CSV untuk banyak tagihan |
| Kualitas output | 9 | 6 tahap sampai somasi, surat resmi siap kirim, saran tindakan konkret |
| Akurasi (angka/fakta) | 8 | Hitungan 0 selisih; dasar hukum umumnya benar & berlabel; meterai kurang tepat; tidak ada uji kewajaran denda |
| Penanganan input kurang | 9 | Tanya sekali, default "tanpa denda" |
| Penanganan di luar cakupan | 9 | Menolak ancaman/sebar di grup dengan alasan & alternatif sah |
| Keamanan | 10 | Bersih, pengaman hukum kuat |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: skill jelas lebih baik (versi tanpa skill mengancam denda yang tidak pernah disepakati dan penghentian layanan sepihak). Banding pesaing: `invoice-chaser` (Ootto-AI/claude-invoice-skills, MIT) menghasilkan email yang cukup baik untuk S1 tetapi tanpa kalkulasi, tanpa tahap somasi, dan tanpa pagar hukum Indonesia — skill kita menang. Tidak ada cacat berat.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Tahap ditentukan hanya dari umur piutang** (script `tahap()` baris 88; SKILL.md langkah 2 baris 48). Invoice 39 hari yang belum pernah ditagih langsung "Tahap 6 – somasi", padahal Input baris 34 punya "Riwayat penagihan" (default "belum pernah ditagih") yang tidak dipakai. **Saran:** di SKILL.md langkah 2 tambahkan: "Jika belum pernah ada pengingat, mulai maksimal dari tahap 4 (atau 5 bila ≥ 30 hari), dan naikkan tahap setelah 7 hari tanpa respons"; opsional argumen `--sudah-diingatkan N` di script.
2. **Ambang meterai kurang tepat** — SKILL.md baris 62 ("surat pengakuan utang > Rp5.000.000 perlu meterai"), `references/regulasi.md` baris 22, `references/template-penagihan.md` baris 68. Menurut UU 10/2020 Pasal 3 ayat (2), surat perjanjian/pernyataan (termasuk kesepakatan cicilan & surat pengakuan utang) adalah objek bea meterai **tanpa ambang nilai**; ambang > Rp5.000.000 berlaku untuk dokumen penerimaan uang atau pernyataan utang telah dilunasi. Tulisan saat ini bisa membuat pengguna mengira kesepakatan cicilan Rp 3 juta tidak perlu meterai. **Saran:** "Kesepakatan cicilan/pengakuan utang yang akan dijadikan alat bukti sebaiknya bermeterai Rp10.000 (berapa pun nilainya); kuitansi/tanda terima pelunasan > Rp5.000.000 wajib bermeterai." Beri label *(perlu review)* bila belum dicek ke teks resmi.
3. **Tidak ada uji kewajaran denda** (`hitung_denda()` baris 117–150). `--denda-persen 0,100` → 100%/hari → denda 22× pokok tanpa peringatan; `--denda-maks 5` tanpa "%" → batas Rp 5. **Saran:** PERINGATAN bila persen harian > 1% atau denda > sisa pokok; tolak `--denda-maks` berupa angka ≤ 100 tanpa "Rp"/"%" dengan pesan "maksud Anda 5% atau Rp 5?".

### Ringan
4. Script tidak mencetak tanggal tahap berikutnya (agent menghitung +7/+14/+30 manual). **Saran:** tambah `tahap_berikutnya: {tahap, tanggal}` di output.
5. "Kapan TIDAK digunakan" tidak menyebut pinjaman uang berbunga antar-perorangan (hanya lembaga keuangan/pinjol). **Saran:** tambah satu baris: tagih pokok, bunga tanpa perjanjian tertulis jangan dihitung, sarankan advokat/LBH.
6. Pelanggan langganan yang masih dilayani (katering, jasa bulanan) belum punya panduan — mis. jangan menghentikan layanan sepihak tanpa pemberitahuan tertulis. **Saran:** satu butir di Saran tindakan.
7. Dari banding pesaing (ide): dua opsi subjek email untuk tahap 4–5, batas panjang email pengingat, dan template kesepakatan cicilan ringkas.
