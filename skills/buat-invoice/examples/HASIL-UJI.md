# HASIL UJI — buat-invoice

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Lingkungan:** folder kerja `/tmp/uji-buat-invoice/`, Python 3 standar
- **Skenario:** 01–05 + uji A/B (00)

## Audit keamanan
- `scripts/buat_invoice.py` + `scripts/hitung_ppn.py` (identik dengan milik skill `hitung-ppn`, dicek `diff`): hanya library standar (`argparse, datetime, html, json, os, re, sys, decimal`). Menulis file **hanya** ke path `--html` / `--counter-file` yang diberikan; `sys.dont_write_bytecode` mencegah `__pycache__`. Tidak ada jaringan, subprocess, atau pembacaan kredensial.
- **HTML aman:** uji injeksi dengan `<script>`, `<img onerror>`, `<iframe>`, `<svg onload>`, `javascript:` di nama penjual/pembeli, alamat, item, satuan, catatan, rekening, tanda tangan, dan nomor → **tidak ada satu pun tag yang lolos**; semua di-escape (`html.escape`). CSS statis, tanpa script.
- Output Markdown tidak meng-escape HTML (nama berisi `<script>` tercetak apa adanya). Risiko rendah (antarmuka chat umumnya menyanitasi), dicatat sebagai ringan.
- SKILL.md/README/references: tidak ada prompt injection. **Aman.**

## Verifikasi angka (independen)
- **Terbilang:** implementasi independen (algoritma kelompok 3 digit) dibandingkan untuk 0–2.999, 20.000 angka acak s.d. 10^14, dan kasus khusus (seribu, sebelas, seratus, satu juta, 1.001.000, 1.000.001.000) → **0 selisih**. (Fungsi skill dipanggil hanya sebagai objek yang diuji; ekspektasi dihitung sendiri.)
- **Invoice acak:** 300 invoice (1–4 item, qty & harga acak termasuk pecahan ,333, diskon baris %/nominal, diskon total, ongkir, PKP umum/mewah, ongkir kena/tidak kena PPN, pembayaran acak termasuk tepat Rp5.000.000 / Rp5.000.001 / Rp4.999.999) dibandingkan dengan perhitungan `Fraction` independen → **0 selisih** pada subtotal, PPN, total, sisa, status meterai, dan terbilang.
- Contoh SKILL.md/README/template (total Rp6.750.000, sisa Rp3.750.000, terbilang "Tiga Juta Tujuh Ratus Lima Puluh Ribu Rupiah"): **benar**.
- Termin 40-30-30 atas Rp49.950.000 → 19.980.000 / 14.985.000 / 14.985.000 (termin terakhir = sisa agar pas): **benar**.

## Kepatuhan fokus khusus
- **Bea meterai:** penanda muncul bila penerimaan uang **> Rp5.000.000**; **tepat Rp5.000.000 tidak** ditandai (diuji). Benar.
- **PPN ditolak bila bukan PKP:** `"ppn": true` + `"pkp": false` → `ERROR` exit 2 (S5). Benar.
- **Terbilang benar:** lihat verifikasi.
- **HTML aman:** lihat audit.
- **Pembulatan PPN:** ke bawah (sama dengan hitung-ppn), **berbeda** dengan surat-penawaran-harga (ke terdekat) → penawaran dan invoice untuk transaksi yang sama bisa selisih Rp1 (contoh Rp1.000.005: SPH total Rp1.110.006, invoice Rp1.110.005). Rekomendasi standar: lihat HASIL-UJI `hitung-ppn` (satu modul bersama, PPN dibulatkan sekali ke bawah).

## Skor

| Kriteria | Skor (1–10) | Alasan singkat |
|---|---|---|
| Pemicu (description) | 9 | "buatkan invoice", "nota tagihan", "kuitansi DP/lunas" + EN; batas dengan tagih-piutang & SPH jelas |
| Kemudahan awam | 9 | Satu pesan cukup; agent menyusun JSON; HTML → PDF dijelaskan |
| Kualitas output | 8 | Lengkap & rapi; kuitansi DP membingungkan (lihat cacat) dan terbilang tanpa label |
| Akurasi (angka/fakta) | 9 | 0 selisih pada 300 invoice & 23.000 terbilang; meterai & PPN sesuai aturan; pembulatan PPN beda dengan SPH |
| Penanganan input kurang | 9 | Tanya sekali, 5 butir, default jelas |
| Penanganan di luar cakupan | 9 | PPN non-PKP ditolak oleh script; faktur pajak diarahkan ke Coretax |
| Keamanan | 9 | HTML aman; Markdown tidak di-escape (ringan) |

## SKOR AKHIR: **8 / 10** — LULUS

Uji A/B: dengan skill jelas lebih baik (terbilang, status, meterai, HTML siap cetak, pagar PPN non-PKP). Tidak ada cacat berat.

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
1. **Kuitansi DP/sebagian membingungkan.** Kuitansi dengan pembayaran Rp3.000.000 atas pesanan Rp10.000.000 menampilkan "Uang sejumlah Rp3.000.000 / Terbilang: Tiga Juta" di atas, lalu tabel dengan "TOTAL Rp10.000.000" dan "Terbilang: Sepuluh Juta" di bawah — tanpa baris "Sudah dibayar" atau "Sisa". Pembeli bisa mengira kuitansi menyatakan penerimaan Rp10 juta (juga berdampak ke penilaian meterai). Lokasi: `markdown()` dan `html_dok()`, cabang `jenis_dokumen == "kuitansi"`. Saran: untuk kuitansi, tampilkan "Nilai pesanan Rp…, diterima sekarang Rp…, sisa Rp…" dan hilangkan terbilang kedua (terbilang hanya untuk uang yang diterima).
2. **Pembulatan PPN tidak konsisten dengan `surat-penawaran-harga`** (lihat di atas). Saran: satukan standar di level library (SPH ikut `hitung_ppn.py`).

### Ringan
3. Invoice dengan pembayaran: baris "Terbilang" di bawah "SISA TAGIHAN" tidak menyebut bahwa itu terbilang sisa. Saran: "Terbilang (sisa tagihan): …".
4. Output Markdown tidak meng-escape karakter HTML pada nama/alamat/catatan. Saran: escape `<`, `>` (atau ganti dengan entitas) di `blok_pihak()` dan baris item, seperti pada HTML.
5. Interpretasi meterai untuk invoice yang **mencantumkan** DP > Rp5 juta (S1) masuk akal tetapi bisa diperdebatkan (DP biasanya sudah punya kuitansi sendiri). Saran: di pesan "Info untuk penjual", tambahkan alternatif "bila DP sudah dibuatkan kuitansi bermeterai, baris DP dapat dihapus dari invoice — konfirmasi ke konsultan".
6. `nomor_berikutnya()` mempertahankan bulan/tahun dari nomor terakhir (INV/2026/09/0012 → …/09/0013) walaupun tanggal invoice sudah bulan berikutnya. Saran: bila pola `PREFIX/YYYY/MM/NNNN` dan bulan berbeda dari tanggal dokumen, beri peringatan atau reset ke 0001.
7. Kuitansi: terbilang tercetak dua kali (blok penerimaan & bawah tabel). Saran: hilangkan yang di bawah untuk kuitansi lunas.
