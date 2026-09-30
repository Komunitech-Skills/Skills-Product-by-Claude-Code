# Hasil Uji Ulang - strategi-konten-iklan

## Uji ulang 1.0.1 (2026-09-30)

Penguji independen (bukan pembuat), salinan di scratchpad, input baru buatan penguji. Platform: `claude-code (simulasi agent)`.

### Skor: 9/10
Semua temuan sedang (S1-S4) dan rendah yang dijanjikan (R1-R5) terbukti teratasi; tidak ada regresi. Sisa catatan kecil di bawah.

### Verifikasi temuan 1.0.0
| Temuan | Hasil | Bukti |
|---|---|---|
| S1 saringan kanal vs iklan aktif maks | Beres | Fuzz 300 kasus (tujuan tunggal & campuran, 1-5 minggu, bobot acak, jenis, margin): 0 kasus "0 - DI BAWAH BATAS" tanpa catatan "DI BAWAH batas uji"; hari tayang terbiayai tidak melebihi hari rencana (Rp500rb Google: 20 hari) |
| S2 prioritas kanal `--jenis` | Beres | Rp500rb/Rp1jt: marketplace penjualan -> Shopee; jasa-lokal -> Google; umum -> Meta; leads + marketplace -> Meta (Shopee tidak cocok leads). Rp500rb jasa-lokal leads: Google tetap di bawah batas, tetapi ada catatan jelas |
| S3 tujuan campuran | Beres | `awareness:30,penjualan:70` Rp8jt bobot 1 1 2 3 jalan; total 90/110 ditolak, kata tak dikenal ditolak, porsi 0 ditolak |
| S4 tumpang tindih | Tercatat di README 1.0.1 (deskripsi/rujukan tidak diuji ulang mendalam) |
| R1 margin | Beres | 12% tanpa peringatan, 11%->0; <=10% (10/8/3/1%) ada PERINGATAN; 0%, -10%, 150% GAGAL dengan penjelasan rugi |
| R2 kategori | Beres | skincare, kosmetik, suplemen, klinik, obat, jamu herbal, pinjaman, investasi, asuransi, kripto memicu catatan TERBATAS; "makanan" catatan cek kebijakan |
| R3 alias/format | Beres | ig, instagram, fb, facebook, tiktok shop, tokopedia, google ads; `Rp 3.000.000,-`, `IDR 3jt`, `rp 3jt` diterima; `3,000,000`, `1.5jt`, `3000000.00` tetap ditolak jelas |

### Hitung ulang independen
Fuzz 300 kasus (parser terpisah pada keluaran): total alokasi = anggaran, jumlah per baris minggu = anggaran kanal, jumlah kolom = total minggu, ROAS impas = ceil(100/margin)/100: 0 selisih. Kasus Rp8jt campuran dicek tangan: impas 2,50x, CPA impas Rp40.000, aman Rp28.000 / 3,58x, 200 pesanan; bagian minggu 1/1/2/3 dan iklan aktif maks (2/1/2/1) benar.

### Regresi
Contoh 01-03 dan 06-08, 10 dijalankan ulang: semua nominal keluaran baru ada di dokumen lama (0 selisih); 09 tidak berisi perintah. `tests/uji_regresi.py` 43 tes OK. `validate.py --skill strategi-konten-iklan` lolos.

### Catatan sisa (rendah)
- `--jenis jasa-lokal` dengan tujuan awareness tetap memilih Google Ads (kurang cocok untuk awareness); pertimbangkan Meta.
- Alias `tokopedia` dipetakan ke TikTok Shop Ads (masuk akal, tetapi sebaiknya disebut di README).
- Peringatan margin baru muncul di <=10%; 11-15% tidak diberi catatan (ambang wajar, hanya info).
