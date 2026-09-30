# Audit format angka Indonesia di script skill (2026-09-30)

Auditor hanya membaca dan menguji di salinan scratchpad (`.../scratchpad/audit-angka`). Tidak ada file repo yang diubah dan tidak ada commit.

Dilewati sesuai perintah: strategi-merek-usaha, program-referral-loyalitas, odoo-usaha.

Cakupan:
- 143 script (di luar tiga skill yang dilewati) diperiksa.
- Semua fungsi pembaca angka (sekitar 85 fungsi di ±70 skill) diuji dengan `38.000`, `1.500`, `1.250.000`, `Rp38.000`, `Rp 1.250.000`, `1.250.000,50`, `1,5`, `38000`, `38.000,00`.
- Script yang tidak punya fungsi pembaca bernama, tetapi memanggil `Decimal(...)` atau `float(...)` langsung pada teks pengguna, diperiksa lewat kode dan CLI.
- Semua argumen argparse `type=int/float` diperiksa. Semuanya menolak `1.500` untuk int dengan pesan jelas. Untuk float, `1.500` terbaca 1,5; ini hanya soal untuk `--wpm`/`--target` di studio-video-pendek-ai (bukan uang, tingkat aman/rendah).

Legenda perilaku: BENAR / GAGAL JELAS (aman) / SALAH DIAM-DIAM (bug).
Tingkat: tinggi = salah baca diam-diam pada uang. sedang = salah baca diam-diam pada jumlah/harga aset. aman = benar atau gagal jelas.

## A. Temuan bug (tingkat tinggi dan sedang)

| skill | script | argumen | perilaku | tingkat |
|---|---|---|---|---|
| presentasi-data-ke-atasan | scripts/hitung_perubahan.py | `--pasangan "Omzet:38.000:45.000"` | SALAH DIAM-DIAM: `Decimal(teks)` mentah. 38.000 terbaca 38 dan 45.000 terbaca 45, sehingga selisih 7 dan +18,4% (yang benar 7.000). `1.250.000` gagal jelas. Pesan galat bilang "jangan pakai titik ribuan", tetapi `38.000` lolos begitu saja. `--daftar "Jual=1.500,2.000"` juga salah (1,5 dan 2). | tinggi |
| klon-diri-konten | scripts/rencana_konten_avatar.py | `--kurs 16.500` (juga `--anggaran`, dan angka di paket.json bila ditulis teks) | SALAH DIAM-DIAM: `dec()` hanya mengganti koma dengan titik. `16.500` terbaca 16,5 sehingga biaya jadi Rp479 (benar Rp478.500). Nilai bertitik dua atau lebih (`1.500.000`) gagal jelas. | tinggi |
| laporan-otomatis-terjadwal | scripts/susun_pesan.py | JSON `{"label":"Omzet","nilai":"38.000","rupiah":true}` | SALAH DIAM-DIAM: `round(float(nilai))`. "38.000" tercetak "Rp 38" dan "1.500" tercetak "Rp 2". "1.250.000" gagal jelas. Aman bila `nilai` berupa angka JSON, tetapi teks berformat Indonesia tidak diperingatkan. | tinggi |
| arsip-nota | scripts/arsip.py | `tambah --nominal 150,50` atau `--nominal 1,5` | SALAH DIAM-DIAM pada koma desimal tanpa satuan: `150,50` menjadi Rp15.050 dan `1,5` menjadi Rp15, dengan `peringatan: []`. `38.000` dan `Rp38.000` benar. | tinggi (jarang terjadi) |
| frappe-books-usaha | scripts/frappe_books.py | fungsi `baca_jumlah`, dipakai impor CSV kolom jumlah | SALAH DIAM-DIAM: `1.500` terbaca 1,5 dan `38.000` terbaca 38. `1.250.000` gagal jelas. Jumlah, bukan rupiah. Pembaca harga `baca_rupiah` di file yang sama benar. | sedang |
| bot-trading-kripto | scripts/backtest.py | fungsi `parse_harga`, dipakai CSV candle harga | SALAH DIAM-DIAM: `38.000` terbaca 38 dan `1.500` terbaca 1,5. `1.250.000` gagal jelas. Wajar untuk CSV bursa berformat titik desimal, tetapi tidak ada peringatan untuk pasangan IDR (harga bertitik ribuan). | sedang |

Catatan tingkat rendah (bukan pola titik ribuan):
- gaji-umkm (`uang`) dan kontrak-kerja-pkwt (`parse_rupiah`): `1,5` dan `1.250.000,50` dibulatkan ke rupiah tanpa peringatan. buku-piutang dan pengingat-follow-up memperingatkan.
- Tidak ada temuan tinggi atau sedang di skill pajak, gaji, keuangan, atau harga utama (lihat bagian B).

## B. Skill uang/pajak/gaji/harga: benar untuk semua input uji (aman)

Semua benar untuk `38.000`, `1.500`, `1.250.000`, `Rp38.000` (kecuali dicatat), dan koma desimal:
- hitung-ppn, buat-invoice, hitung-hpp, pph-final-umkm, pph21-ter, slip-gaji-bpjs, hitung-thr, gaji-umkm
- harga-jual-marketplace, strategi-harga-produk, katalog-reseller, promo-kalender
- surat-penawaran-harga, tender-checklist, proposal-kerjasama, validasi-ide-produk-baru
- kasir-lokal, kas-umkm, buku-piutang, tagih-piutang, buku-stok, crm-wa
- laporan-keuangan-emkm, analisis-rasio-keuangan-usaha, arus-kas-13minggu, rekonsiliasi-bank
- pengajuan-kur, perjanjian-sederhana, kontrak-kerja-pkwt, riset-harga-kompetitor
- ekstrak-nota-faktur, laporan-iklan-mingguan, audit-akun-iklan, rekap-penjualan-csv
- resi-picking, atur-keuangan-pribadi, absensi-lokal, analisis-excel, grist-usaha
- naskah-live-jualan (`hitung_promo.py`), peringatan-dini-operasional, kpi-tim
- brainstorming-ide-usaha, spesifikasi-produk-usaha, inventree-gudang, dolibarr-usaha (`parse_item`)

Gagal jelas, tetapi `Rp38.000` (tanpa spasi) ditolak (aman, hanya kurang ramah):
- absensi-lokal (`angka_wajib`), actual-budget-usaha (`parse_nominal`), atur-keuangan-pribadi (`_angka_polos`), inventree-gudang.

Sengaja ketat, menolak pola ribuan dengan pesan jelas (aman):
- bot-trading-kripto (`inti.angka`), hledger-usaha (jurnal wajib "Rp"), kalender-pajak, uji-pasar-produk-cepat (`angka_bulat`, `angka_desimal`), proposal-kerjasama (`parse_persen`).

Titik atau koma di situ memang berarti desimal, dan ini terdokumentasi (bukan uang, aman):
- pantau-pasar-kripto (`parse_jumlah_koin`)
- perjanjian-sederhana, strategi-harga-produk (`parse_persen`)
- analisis-pesaing-strategis, riset-calon-pelanggan (skor)
- studio-video-pendek-ai (`--wpm`, `--target`)

Bukan pembaca uang (hanya pemformat, tidak diaudit): fider `angka`, umami `angka`.

## C. Perintah reproduksi (jalankan dari folder `skills/`)

```bash
# presentasi-data-ke-atasan (tinggi): 38.000 -> 38
python3 presentasi-data-ke-atasan/scripts/hitung_perubahan.py --pasangan "Omzet:38.000:45.000"
#   benar: selisih 7000, +18,4%. Keluaran: nilai_lama 38, nilai_baru 45, selisih 7

# klon-diri-konten (tinggi): kurs 16.500 -> 16,5 (Rp479 vs Rp478.500)
python3 klon-diri-konten/scripts/rencana_konten_avatar.py \
  --paket klon-diri-konten/examples/contoh-paket.json --video 12 --menit 0.75 --kurs 16.500
python3 klon-diri-konten/scripts/rencana_konten_avatar.py \
  --paket klon-diri-konten/examples/contoh-paket.json --video 12 --menit 0.75 --kurs 16500   # pembanding benar

# laporan-otomatis-terjadwal (tinggi): "38.000" -> "Rp 38"
echo '{"judul":"T","baris":[{"label":"Omzet","nilai":"38.000","rupiah":true}]}' \
  | python3 laporan-otomatis-terjadwal/scripts/susun_pesan.py

# arsip-nota (tinggi, jarang): 150,50 -> 15050. Butuh --db dari `init --ya` dan berkas JPEG asli (bukan 0 byte)
python3 arsip-nota/scripts/arsip.py tambah --db /tmp/x.db --file nota.jpg --tanggal 01/09/2026 \
  --vendor X --nominal "150,50" --json

# frappe-books-usaha (sedang) dan bot-trading-kripto backtest (sedang): lewat fungsi
python3 -c "import sys;sys.path.insert(0,'frappe-books-usaha/scripts');import frappe_books as f;print(f.baca_jumlah('1.500'))"   # Decimal('1.500') = 1,5
python3 -c "import sys;sys.path.insert(0,'bot-trading-kripto/scripts');import backtest as b;print(b.parse_harga('38.000'))"      # Decimal('38.000') = 38
```

## D. Saran perbaikan singkat (belum dikerjakan)

Pakai kembali pola parser yang sudah teruji di hitung-ppn / kasir-lokal: `\d{1,3}(\.\d{3})+` dibaca sebagai ribuan, `,` sebagai desimal, awalan `Rp` dengan atau tanpa spasi, dan akhiran `rb/jt`.

Skill yang perlu diperbaiki: presentasi-data-ke-atasan, klon-diri-konten, laporan-otomatis-terjadwal, arsip-nota. Opsional: frappe-books-usaha dan bot-trading-kripto (peringatan bila pola ribuan muncul di harga IDR).

Setiap perbaikan perlu ditambah tes regresi untuk `38.000`, `1.500`, dan `Rp38.000`.

## Verifikasi perbaikan (2026-09-30)

Penguji independen, di salinan scratchpad (`.../scratchpad/verif-angka`). Tidak ada file skill yang diubah, tidak ada commit.

| skill | hasil | bukti singkat |
|---|---|---|
| presentasi-data-ke-atasan 1.0.3 | OK | Repro `Omzet:38.000:45.000` → 38000/45000, selisih 7000, +18,4% (dihitung ulang: 7000/38000 = 18,42%). `Rp38.000`, `Rp 45.000`, `rp 1.000.000`, `Rp.2.000.000`, `38rb`, `1,5jt`, `1.5jt`, `-1.500` benar. `38.5`, `1,500`, dan kosong ditolak dengan pesan jelas. `--daftar "Jual=1.500,2.000"` → 1500+2000 = 3500. `1,5jt,2jt` ditolak dengan saran titik-koma. 13 tes lulus. |
| klon-diri-konten 1.0.3 | OK | `--kurs 16.500` hasilnya sama persis dengan `16500`: A Rp478.500 (29×16.500), B Rp957.000, C Rp855.000 (480.000 + 6,25×60.000), per menit Rp42.533/85.067/76.000, semua dicek ulang. `Rp 16.500` dan `16,5rb` benar. `16.5`, `16,500`, `-16500`, kosong, dan `abc` ditolak. paket.json teks `"480.000"`, `"Rp60.000"`, USD `"29,99"` → Rp494.835 (benar). IDR `"480,5"` ditolak. `--menit 1.500` ditolak. 19 tes lulus. |
| laporan-otomatis-terjadwal 1.1.4 | OK | `"38.000"` → Rp 38.000, `"1.500"` → Rp 1.500, `"1.250.000"`, `"Rp 38.000"`, `38rb`, `1,5jt`, `38k` benar. `"38.5"`, `"1,5"`, `"1,500"`, `""`, `true`, dan `null` → exit 1 dengan pesan. Half-up: 2.5 → 3, 3.5 → 4, -2.5 → -Rp 3. Ini sesuai standar "rupiah terdekat" di CLAUDE.md dan ROUND_HALF_UP di skill lain. Tidak menyangkut PPN (aturan floor tidak berlaku di sini). JSON angka bulat identik dengan versi lama. 6 tes lulus. |
| arsip-nota 1.0.5 | OK | Repro CLI `--nominal "150,50"` → `ok:false`, exit 1, nota tidak tersimpan. `1,5`, `1,500`, dan `38.5` ditolak. 22 input yang dulu benar (`38.000`, `Rp 1.250.000`, `4,5 jt`, `1,5jt`, `25000.50`, `1,250,000`, `Rp. 38.000,-`, dan lainnya) hasilnya identik dengan 9d626a5. Uji regresi: SEMUA LULUS (55). |
| frappe-books-usaha 1.0.6 | OK | `baca_jumlah('1.500')` = 1500, `38.000` = 38000, `1.250.000` dan `1.500,5` sekarang terbaca. `1,500` ditolak karena ambigu. `3`, `1,5`, `2.5`, `0.500`, `1500.5`, `10,25` identik dengan versi lama. qty ≤ 0 tetap ditolak di impor. 47 tes lulus. |
| bot-trading-kripto 1.0.5 | OK | Backtest lama (9d626a5) vs baru, 4 konfigurasi × 4 CSV (btcidr, btcusdt, harga 5 desimal, harga 1 desimal): 16/16 output IDENTIK byte demi byte. CSV IDR bertitik ribuan (`1.908.238.000`) kini sama persis dengan CSV polos; versi lama menolak semua barisnya. Kolom yang semuanya ambigu (`100.500`) atau campur gaya ditolak dengan pesan jelas. Repro `parse_harga('38.000')` → ValueError ambigu. 135 tes lulus. Hanya backtest.py yang berubah. |

Catatan kecil, bukan regresi (sudah ada sebelumnya): di presentasi-data-ke-atasan, `--daftar "Rating=4,5,3,5"` terbaca 4 nilai (4, 5, 3, 5) karena koma dipakai sebagai pemisah. Hal ini sudah didokumentasikan (pakai `;`). Keluaran dibulatkan ke bilangan bulat, sehingga `2,5 → 3,75` tampil sebagai selisih 1 (persen 50,0 tetap benar).
