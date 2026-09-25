---
name: laporan-iklan-mingguan
description: Membuat SATU laporan mingguan bahasa awam dari ekspor CSV iklan Meta/Facebook/Instagram Ads Manager, TikTok Ads Manager, Shopee Ads, TikTok Shop Ads (dulu Tokopedia Ads), atau Google Ads - total belanja, klik, pesan/lead/pembelian, CPC, CPM, CTR, biaya per hasil (CPA/CPL), ROAS, perbandingan % vs minggu lalu, 3 kampanye terbaik & terburuk, dan saran berbasis angka. Gunakan saat pengguna minta "laporan iklan mingguan", "rekap Meta Ads/TikTok Ads/Shopee Ads/Google Ads", "berapa biaya per lead iklan saya", ads report, weekly ads summary, ROAS report. Bukan untuk laporan penjualan dari kasir/marketplace (rekap-penjualan-csv), menentukan harga jual (harga-jual-marketplace), atau menjadwalkan pengiriman rutin (laporan-otomatis-terjadwal, dipakai SETELAH laporan ini terbukti benar).
---

# Laporan Iklan Mingguan

## Tujuan
Pemilik usaha yang beriklan (Meta/Instagram, TikTok, Shopee, Tokopedia/TikTok Shop, Google)
cukup mengekspor CSV dari Ads Manager masing-masing lalu dapat **satu laporan mingguan** bahasa
awam: berapa habis, hasilnya apa, mahal/murah dibanding minggu lalu, iklan mana yang layak
dimatikan atau dinaikkan anggarannya — tanpa menghitung manual atau menebak-nebak istilah CPC/CPM/
ROAS. Semua angka dihitung `scripts/laporan_iklan.py`, bukan diperkirakan.

## Kapan digunakan
- "Buatkan laporan iklan minggu ini", "rekap Meta Ads saya", "berapa ROAS TikTok Ads minggu ini?"
- Pengguna mengirim 1+ file CSV/Excel-disimpan-sebagai-CSV hasil unduh dari Ads Manager.
- "Bandingkan biaya iklan minggu ini vs minggu lalu", "iklan mana yang harus dimatikan?"

## Kapan TIDAK digunakan
- Data penjualan dari kasir/marketplace (bukan data iklan) → `rekap-penjualan-csv`.
- Menentukan harga jual produk → `harga-jual-marketplace`.
- Ingin laporan ini **terkirim otomatis tiap minggu** ke Telegram/WA → jalankan skill ini dulu
  sampai hasilnya benar, baru serahkan resepnya ke `laporan-otomatis-terjadwal` (lihat
  `references/openclaw-jadwal.md`). Skill ini sendiri **tidak** membuat jadwal.
- Laporan gabungan semua alat usaha (bukan cuma iklan) → `laporan-harian-usaha`.
- File Excel `.xlsx` asli → minta pengguna *Save As → CSV* dulu (bukan sekadar ganti nama file).
- Menarik data otomatis dari Ads Manager (login/scraping) → **tidak didukung dan tidak akan
  dibuat** (keputusan pemilik Komunitech). Ekspor **selalu manual** oleh pemilik/admin iklan,
  1-2 menit per platform per minggu.
- Iklan crypto/kesehatan dengan klaim menyembuhkan/untung pasti → skill ini hanya menghitung
  angka biaya-hasil, tidak menilai/menyetujui isi materi iklan.

## Input
| Info | Wajib? | Default |
|---|---|---|
| File CSV ekspor minggu ini (1 per platform) | Ya | — (minta pengguna ekspor & kirim) |
| File CSV minggu lalu (platform sama) | Tidak | Tanpa perbandingan; sebutkan itu ke pengguna |
| Nama/label hasil (mis. "pesan WA", "pembelian", "leads") | Tidak | Nama kolom hasil apa adanya (mis. "Results", "Konversi") |
| Omzet penjualan periode ini (dari `rekap-penjualan-csv`/kasir) | Tidak | Tidak dihitung % terhadap omzet |
| Pemetaan kolom manual (bila deteksi otomatis gagal) | Tidak | Deteksi otomatis dari nama kolom |

Jika hanya 1 file dikirim tanpa disebut platformnya, jalankan saja — platform terdeteksi otomatis
dari nama kolom (lihat `references/sumber-kolom.md`). Jika pengguna ingin cepat ("langsung aja"),
jalankan dengan default di atas dan sebutkan di akhir laporan bahwa tidak ada pembanding minggu
lalu / omzet bila memang tidak diberikan — **jangan mengarang angka pembanding**.

## Langkah kerja
Path script relatif terhadap folder SKILL.md ini. Windows: ganti `python3` dengan `python`/`py`.

### 1. Satu platform, satu minggu
```bash
python3 <folder-skill-ini>/scripts/laporan_iklan.py analisis "<ekspor-minggu-ini.csv>" \
  --sebelumnya "<ekspor-minggu-lalu.csv>" \
  --omzet 20000000 \
  --json
```
- Tanpa `--sebelumnya` bila pengguna tidak punya data minggu lalu (laporan tetap dibuat, tanpa
  bagian "VS MINGGU LALU").
- Tanpa `--json` untuk langsung dapat teks siap kirim (dipakai bila hanya 1 platform).
- `--nama-hasil "pesan WA"` bila kolom hasil generik (mis. "Results" Meta yang sebenarnya berarti
  pesan WhatsApp/Messenger) — pakai istilah yang pengguna sendiri sebutkan.
- **Kolom tidak terdeteksi?** Script keluar kode 2 dan menyebutkan kolom apa yang hilang serta
  daftar kolom yang ada di file. Tanyakan ke pengguna kolom mana yang dimaksud, lalu jalankan
  ulang dengan `--kolom-biaya`, `--kolom-tayangan`, `--kolom-klik`, `--kolom-hasil`,
  `--kolom-nilai-hasil`, `--kolom-nama` sesuai nama kolom **persis** di file (lihat pesan error).
- **Mata uang bukan Rupiah?** Script menolak diam-diam. Ikuti pesan errornya: tanyakan ke
  pengguna kurs yang mau dipakai lalu tambahkan `--kurs <angka>` (boleh `--kurs-sumber`/
  `--kurs-tanggal` untuk dicatat), atau `--mata-uang IDR` bila label file memang keliru dan
  angkanya sudah Rupiah.
- Simpan hasil `--json` ke file sementara bila akan dipakai Langkah 2 (gabung) atau dipakai lagi
  minggu depan sebagai `--sebelumnya` (opsional).

### 2. Lebih dari satu platform (gabungkan jadi satu laporan)
Jalankan Langkah 1 (dengan `--json`) untuk **tiap** file platform, simpan tiap keluaran sebagai
file JSON, lalu:
```bash
python3 <folder-skill-ini>/scripts/laporan_iklan.py gabung meta.json tiktokads.json shopee.json \
  --omzet 20000000
```
Bila platform yang digabung mengukur "hasil" secara berbeda (mis. Meta "Results" vs Shopee
"Konversi Langsung"), script tetap menjumlahkan tapi **wajib** menampilkan peringatan bahwa
biaya-per-hasil/ROAS gabungan hanya perkiraan kasar — sampaikan peringatan itu ke pengguna, jangan
disembunyikan, dan tunjukkan juga rincian per platform (selalu ada di keluaran).

### 3. Ekspor rincian per kampanye (opsional)
Tambahkan `--csv-keluaran "<nama-file>.csv"` pada Langkah 1 untuk file CSV rincian per kampanye
yang aman dibuka di Excel (nama kampanye yang diawali `=`/`+`/`-`/`@` otomatis diberi tanda kutip
agar tidak dieksekusi sebagai formula).

### 4. Tulis laporan ke pengguna
Kirim field `teks` (dari `--json`) atau keluaran teks langsung **apa adanya** — boleh menambah
1-2 kalimat pembuka, tapi **jangan mengubah angka/persen**. Sebutkan semua `peringatan` dan
`catatan_mata_uang` dari hasil, termasuk baris "Total/Jumlah" yang dilewati agar tidak dihitung
dua kali.

### 5. (Lanjutan, opsional) Jadwalkan otomatis
Setelah pengguna puas dengan hasil laporan manual di atas selama minimal 1 minggu, tawarkan
menjadwalkannya lewat `laporan-otomatis-terjadwal` mengikuti pola di
`references/openclaw-jadwal.md`. **Ekspor dari Ads Manager tetap manual** — OpenClaw tidak login/
menarik data dari Meta/TikTok/Shopee/Google secara otomatis (keputusan pemilik Komunitech, lihat
`references/openclaw-jadwal.md`).

## Rumus (dipakai script, untuk hitung manual bila Python tak tersedia)
Per baris kampanye setelah baris "Total/Jumlah" dibuang: `biaya`, `tayangan`, `klik`, `hasil`,
`nilai_hasil` (opsional, untuk ROAS) dijumlah per nama kampanye (menangani ekspor dengan baris
harian per kampanye), lalu:
```
CPC              = biaya ÷ klik                (klik = 0 → "-")
CPM              = biaya ÷ tayangan × 1000      (tayangan = 0 → "-")
CTR              = klik ÷ tayangan × 100%       (tayangan = 0 → "-")
Biaya per hasil  = biaya ÷ hasil                (hasil = 0 → "-", ditandai "tanpa hasil")
ROAS             = nilai_hasil ÷ biaya          (hanya bila kolom nilai/omzet iklan ada)
Biaya vs omzet   = total biaya ÷ omzet × 100%   (hanya bila --omzet diisi)
```
**Pembulatan (sama untuk seluruh library, lihat `CLAUDE.md`):** nominal Rupiah dibulatkan ke
rupiah terdekat, 0,5 menjauhi nol (mis. Rp100,5 → Rp101). Persen & ROAS dibulatkan 1 desimal,
0,05 menjauhi nol (mis. 91,65% → 91,7%). Perbandingan minggu lalu memakai rumus yang sama seperti
`laporan-harian-usaha`: `(sekarang − lalu) ÷ lalu × 100`; pembanding Rp0 → "naik dari Rp 0 (persen
tidak dihitung)"; keduanya Rp0 → "sama-sama Rp 0". *Pembulatan di sini belum dicocokkan dengan
Coretax (tidak relevan untuk laporan iklan, tapi mengikuti standar pembulatan library ini).*

## Format output
```
LAPORAN IKLAN MINGGUAN — <Platform>
Periode: <awal> s.d. <akhir>

Total belanja iklan: Rp ...
Tayangan: ... | Klik: ... | <Hasil>: ...
CPC: Rp ... | CPM: Rp ... | CTR: ...%
Biaya per <hasil>: Rp ...
ROAS: ...x                              (bila ada data nilai/omzet iklan)
Biaya iklan vs omzet: ...%  dari omzet Rp ...   (bila --omzet diisi)

VS MINGGU LALU                           (bila --sebelumnya diisi)
Biaya iklan: Rp ... (naik/turun ...% dari minggu lalu)
Hasil: ... (naik/turun ...%)
Biaya per hasil: Rp ... (naik/turun ...%)

3 TERBAIK (biaya per hasil termurah)
1. <nama>: Rp .../hasil (... hasil, Rp ... terpakai)
...

3 PERLU PERHATIAN (biaya per hasil termahal / tanpa hasil)
1. <nama>: Rp ... terpakai, 0 hasil
...

SARAN
1. ...
(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)

Catatan: ...      ⚠️ ...
```

## Contoh
**Input pengguna:** "Ini ekspor Meta Ads minggu ini sama minggu lalu, tolong buatin laporannya.
Omzet toko minggu ini 20 juta."

**Alur:** jalankan `analisis meta_minggu_ini.csv --sebelumnya meta_minggu_lalu.csv --omzet
20000000` → platform terdeteksi "Meta Ads (Facebook/Instagram)", 1 baris "Total" dilewati → kirim
`teks` apa adanya. Contoh lengkap hasil nyata: `examples/uji-pembuat-01-meta-mingguan-vs-lalu.md`.

## Batasan & penanganan error
- **Nama kolom bisa berbeda** menurut bahasa/versi UI Ads Manager (lihat sumber &
  keterbatasannya di `references/sumber-kolom.md`). Deteksi gagal → script memberi daftar kolom
  yang ada + cara mengisi manual (`--kolom-...`); jangan menebak sendiri kolom mana yang dipakai.
- **Baris "Total"/"Jumlah"** di ekspor otomatis dilewati (dicocokkan lewat nama baris, bukan
  dijumlah dua kali) — jumlahnya dilaporkan di `catatan`.
- **Pembagi nol** (0 klik/0 tayangan/0 hasil) → ditampilkan `-`, bukan error atau angka mengada-ada.
- **Mata uang bukan IDR** → ditolak sampai pengguna memberi `--kurs` (dicatat sumber & tanggal
  kursnya) atau menegaskan `--mata-uang IDR`. Tidak pernah dikonversi diam-diam.
- **Minggu tanpa data pembanding** → laporan tetap dibuat tanpa bagian "VS MINGGU LALU"; jangan
  mengarang angka minggu lalu.
- **Bandingkan platform/jenis hasil yang beda** (mis. minggu ini Meta, minggu lalu Google Ads) →
  script tetap menghitung tapi menambahkan peringatan eksplisit bahwa perbandingan mungkin tidak
  setara; sampaikan peringatan itu ke pengguna.
- **File kosong/rusak/bukan CSV** → pesan error jelas (kode keluar 2), tidak pernah traceback
  mentah; sarankan cek ulang hasil ekspor.
- **Formula injection saat buka di Excel**: bila memakai `--csv-keluaran`, nama kampanye yang
  diawali `=`/`+`/`-`/`@` otomatis diberi awalan kutip tunggal agar tidak dieksekusi sebagai
  formula (diuji di `tests/uji_regresi.py`).
- **Saran bukan jaminan hasil.** Semua saran dihasilkan dari ambang angka sederhana (biaya tanpa
  hasil, biaya-per-hasil 2× rata-rata, ROAS < 1x) berdasarkan data minggu itu saja — bukan
  prediksi, bukan audit strategi iklan penuh, dan tidak menilai kualitas materi/target iklan.
- **Python tidak bisa dijalankan:** hitung manual dengan rumus di atas per kampanye, jumlahkan
  baris (kecuali baris Total), dan beri tahu pengguna hasil belum diverifikasi script.
- **Privasi:** hanya angka performa iklan (biaya, tayangan, klik, hasil, nilai). Tidak ada data
  pelanggan/nomor kontak yang diproses atau dikirim ke layanan eksternal.
