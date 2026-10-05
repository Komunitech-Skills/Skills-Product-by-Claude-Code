# Skenario 04: input buruk

- **Penguji:** agent penguji independen (simulasi, Claude Code), 2026-09-25. Semua file dibuat penguji di scratchpad, dengan data fiktif.
- Tujuan: script tidak boleh crash atau menampilkan traceback mentah, dan tidak boleh menghasilkan angka salah secara diam-diam. Pesannya harus bisa dipakai agent untuk bertanya ke pengguna.

| # | Kasus | Hasil | Nilai |
|---|---|---|---|
| 1 | File 0 byte | `{"error": "File kosong"}` rc=2 | ✅ |
| 2 | Hanya baris judul | `File kosong atau hanya berisi judul kolom` rc=2 | ✅ |
| 3 | Kolom tak dikenal (`Uang Keluar, Dilihat Orang, Pencet, Chat Masuk`) | rc=2, menyebut kolom yang hilang + daftar kolom di file. Setelah `--kolom-*` diisi: Rp 100.000, CPC 833, CPM 20.000, CTR 2,4%, 25.000/chat (cocok) | ✅ |
| 4 | Meta `Amount spent (USD)` tanpa `--kurs` | Ditolak rc=2, pesan jelas (kurs / `--mata-uang IDR`) | ✅ |
| 5 | Sama, `--kurs 16350 --kurs-sumber … --kurs-tanggal 2026-09-19` | Rp 4.302.012, CPC 1.337, CPM 17.819, 30.296/pesan WA. Catatan kurs + sumber + tanggal tampil | ✅ (0 beda dengan hitung ulang) |
| 6 | `--kurs 0` | Ditolak (dianggap tidak diisi) | ✅ |
| 7 | `--kurs -16350` | **Diterima**: "Total belanja iklan: Rp -49.976…", saran "naikkan anggaran" untuk iklan terburuk | ❌ rendah |
| 8 | **TikTok `Currency`=USD, kolom `Cost` tanpa label** (angka 111.84 dst.) | **Diterima sebagai Rupiah**: "Total belanja iklan: Rp 299", CPC Rp 0, CPM Rp 1. Hanya ada catatan "diasumsikan IDR" | ❌ **tinggi** |
| 9 | **Nilai `$111.84`** (simbol dolar di sel) + `Currency`=USD | Simbol `$` dibuang diam-diam (`:111-113`), hasilnya **Rp 299** | ❌ **tinggi** |
| 10 | Baris rusak: `lima ratus ribu` | Baris dilewati + peringatan (bentuk `dict` mentah) | ✅/kosmetik |
| 11 | Sel `Conversions` kosong (iklan tanpa konversi, Rp 120.000) | **Seluruh baris dibuang**, biayanya hilang dari total (sama dengan skenario 01) | ❌ **tinggi** |
| 12 | `"250.000,00;x"` (sampah di sel angka) | Dibaca Rp 250.000 tanpa peringatan | ❌ rendah |
| 13 | Biaya `(15000)` (negatif) | Diterima: "Iklan Negatif: Rp -15.000 terpakai" di PERLU PERHATIAN tanpa peringatan | ❌ rendah |
| 14 | Tanggal campur: `2026-09-14`, `15/09/2026`, `09/16/2026`, `17 Sep 2026`, `18-09-26`, `2026-08-20`, `kemarin` | Tidak crash. `09/16/2026` dan `kemarin` diam-diam tidak masuk rentang. Periode "2026-08-20 s.d. 2026-09-18" (**30 hari**) diberi judul "LAPORAN IKLAN MINGGUAN" **tanpa peringatan** bahwa file bukan 1 minggu | ❌ sedang-rendah |
| 15 | `.xlsx` diganti nama `.csv` (header `PK…`) | `File kosong atau hanya berisi judul kolom`: tidak crash, tetapi pesannya menyesatkan (tidak menyebut Excel/Save As CSV) | ❌ rendah |
| 16 | CSV UTF-16 bertab (format "Excel CSV" unduhan Google Ads) | rc=2 dengan daftar kolom rusak `ÿþC\x00a\x00m…` | ❌ rendah |
| 17 | File tidak ada | `[Errno 2] No such file or directory: 'tidakada.csv'` (bahasa Inggris teknis) | kosmetik |
| 18 | `--omzet "20 juta"` / `"20jt"` | **Dibaca Rp 20**: "Biaya iklan vs omzet: 24521000,0% dari omzet Rp 20" | ❌ sedang |
| 19 | `--sebelumnya` = file yang sama | "tetap (0,0%)" di semua baris, tanpa peringatan "file minggu lalu sama dengan minggu ini" | ❌ rendah |
| 20 | `gabung` dengan JSON yang bukan hasil `analisis` | `Terjadi kesalahan tak terduga: 'total'` (tidak ramah) | kosmetik |
| 21 | `gabung` dengan file CSV (bukan JSON) | Pesan jelas: "jalankan dulu 'analisis --json'" | ✅ |
| 22 | `--csv-keluaran` = path file input | **File ekspor asli ditimpa** tanpa peringatan (sha256 berubah) | ❌ rendah |
| 23 | Google mentah (2 baris judul) / Shopee dengan baris info toko | rc=2 "Kolom yang ada di file: ['Campaign report']", tanpa petunjuk menghapus baris judul (lihat 03) | ❌ sedang |

## Reproduksi kasus penting
```bash
# 8: kolom Currency=USD diabaikan
printf 'Campaign name,Cost,Impressions,Clicks (destination),Conversions,Currency\nA,111.84,186020,4450,57,USD\n' > usd.csv
python3 scripts/laporan_iklan.py analisis usd.csv   # → "Total belanja iklan: Rp 112"
# 9: simbol $ dibuang
printf 'Campaign name,Cost,Impressions,Clicks (destination),Conversions\nA,"$1,234.56",100000,1000,10\n' > dolar.csv
python3 scripts/laporan_iklan.py analisis dolar.csv  # → "Total belanja iklan: Rp 1.235"
# 11: sel hasil kosong → baris hilang
printf 'Campaign name,Cost,Impressions,Clicks (destination),Conversions\nA,500000,40000,900,20\nB,120000,9000,150,\n' > kosong.csv
python3 scripts/laporan_iklan.py analisis kosong.csv  # → total Rp 500.000 (seharusnya Rp 620.000)
# 18: omzet dengan kata "juta"
python3 scripts/laporan_iklan.py analisis tiktok.csv --omzet "20 juta"   # → "... dari omzet Rp 20"
```

## Uji pembulatan persen di titik tepi (x,x5%)
Fungsi `bandingkan_persen` dibandingkan dengan rumus acuan `Fraction` (0,05 menjauhi nol): 20.000 pasangan acak + 20.000 CPC/biaya-per-hasil acak + 20.000 CTR acak menghasilkan **0 beda**. Namun **202 kasus tepi** berbeda karena pembagian `float` sebelum `Decimal` (`:547-548`). Contoh: biaya Rp 103.000 vs Rp 80.000 = tepat **28,75%**, sehingga seharusnya **naik 28,8%**, tetapi skill menulis **naik 28,7%**. Selisihnya 0,1 poin pada kasus langka, tetapi melanggar aturan pembulatan yang ditulis di SKILL.md.

## Kesimpulan
Tidak ada crash atau traceback mentah (pembungkus `main()` bekerja). Penolakan mata uang dari label kolom `(USD)` bekerja baik. Namun **tiga kasus menghasilkan angka salah diam-diam** (8, 9, 11), padahal README menjanjikan "Menolak diam-diam kalau file ternyata mata uang asing". Beberapa pesan juga belum ramah pengguna awam (dict mentah, errno, `'total'`).

**Hasil skenario: GAGAL sebagian** (3 cacat tinggi, 2 sedang).
