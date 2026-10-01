---
name: laporan-iklan-mingguan
description: Membuat SATU laporan mingguan bahasa awam dari ekspor CSV iklan Meta/Facebook/Instagram Ads Manager, TikTok Ads Manager, Shopee Ads, TikTok Shop Ads (dulu Tokopedia Ads), atau Google Ads - total belanja, klik, pesan/lead/pembelian, CPC, CPM, CTR, biaya per hasil (CPA/CPL), ROAS, perbandingan % vs minggu lalu, 3 kampanye terbaik & terburuk, dan saran berbasis angka. Gunakan saat pengguna minta "laporan iklan mingguan", "rekap Meta Ads/TikTok Ads/Shopee Ads/Google Ads", "berapa biaya per lead iklan saya", ads report, weekly ads summary, ROAS report. Bukan untuk laporan penjualan dari kasir/marketplace (rekap-penjualan-csv), menentukan harga jual (harga-jual-marketplace), atau menjadwalkan pengiriman rutin (laporan-otomatis-terjadwal, dipakai SETELAH laporan ini terbukti benar).
---

# Laporan Iklan Mingguan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

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
- Menarik data otomatis dari Ads Manager (login/scraping, atau API resmi dengan token akses) →
  **tidak didukung dan tidak akan dibuat** (keputusan pemilik Komunitech). Ekspor **selalu
  manual** oleh pemilik/admin iklan, 1-2 menit per platform per minggu.
- Pengguna **menempelkan password/kode OTP/token** akun iklan di chat → jangan diulang, disimpan,
  atau dipakai. Minta ia segera mengganti password dan menyalakan verifikasi 2 langkah, lalu
  lanjutkan dengan file ekspor saja.
- Iklan crypto/kesehatan dengan klaim menyembuhkan/untung pasti → skill ini hanya menghitung
  angka biaya-hasil, tidak menilai/menyetujui isi materi iklan.

## Input
| Info | Wajib? | Default |
|---|---|---|
| File CSV ekspor minggu ini (1 per platform) | Ya | — (minta pengguna ekspor & kirim) |
| File CSV minggu lalu (platform sama) | Tidak | Tanpa perbandingan; sebutkan itu ke pengguna |
| Nama/label hasil (mis. "pesan WA", "pembelian", "leads") | Tidak | Nama kolom hasil apa adanya (mis. "Results", "Konversi") |
| Omzet penjualan periode ini (angka penuh atau "20 juta"/"20jt"/"750 rb") | Tidak | Tidak dihitung % terhadap omzet |
| Pemetaan kolom manual (bila deteksi otomatis gagal) | Tidak | Deteksi otomatis dari nama kolom |

Jika hanya 1 file dikirim tanpa disebut platformnya, jalankan saja — platform terdeteksi otomatis
dari nama kolom (lihat `references/sumber-kolom.md`). Jika pengguna ingin cepat ("langsung aja"),
jalankan dengan default di atas dan sebutkan di akhir laporan bahwa tidak ada pembanding minggu
lalu / omzet bila memang tidak diberikan — **jangan mengarang angka pembanding**.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
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
- **Mata uang bukan Rupiah?** Script berhenti (kode 2), tidak pernah menghitungnya sebagai Rupiah.
  Mata uang dikenali dari label kolom (`Amount spent (USD)`), kolom `Currency`/`Currency code`/
  `Mata uang`, dan simbol di sel (`$`, `US$`, `RM`, `€`, kode `USD`...). Tanyakan kurs ke pengguna
  lalu tambahkan `--kurs <angka>` (boleh `--kurs-sumber`/`--kurs-tanggal`), atau `--mata-uang IDR`
  bila angkanya memang sudah Rupiah. File yang mencampur dua mata uang selalu ditolak.
- **Tidak perlu merapikan file dulu.** Script sendiri menangani: baris judul/info toko di atas
  tabel (dicari dalam 15 baris pertama), CSV UTF-16 bertab ("Excel CSV" Google Ads), sel kosong/
  `-`/`--`/`—` (dihitung 0 + dicatat), dan baris "Total"/"Total: Account"/"Total of 3 campaigns"/
  "Totals"/"Total Akun"/"Grand Total" di kolom teks mana pun (dilewati + ⚠️ nama & biayanya). File `.xlsx`
  ditolak dengan petunjuk Save As CSV.
- **Ekspor bertingkat** (mis. Meta `Campaign name` + `Ad set name` + `Ad name`, TikTok `Ad group
  name`, Google `Ad group`): script otomatis merinci per level **paling rinci** (iklan) agar iklan
  boros tidak tersembunyi di total kampanye, dan menulis levelnya di Catatan. Pakai
  `--kolom-nama "Campaign name"` **hanya** bila pengguna minta rincian per kampanye.
- Simpan hasil `--json` ke file sementara bila akan dipakai Langkah 2 (gabung) atau dipakai lagi
  minggu depan sebagai `--sebelumnya` (opsional).

### 2. Lebih dari satu platform (gabungkan jadi satu laporan)
Jalankan Langkah 1 (dengan `--json`) untuk **tiap** file platform, simpan tiap keluaran sebagai
file JSON, lalu:
```bash
python3 <folder-skill-ini>/scripts/laporan_iklan.py gabung meta.json tiktokads.json shopee.json \
  --omzet 20000000
```
Aturan mode gabung (v1.0.1):
- **Jenis hasil berbeda** (mis. Meta "pesan WA" vs Shopee "pesanan") → jumlah hasil & biaya per
  hasil gabungan **tidak dihitung**; hanya angka per platform. Samakan label dengan `--nama-hasil`
  hanya bila hasilnya memang sejenis.
- **Nama hasil sama tapi beda platform** (mis. TikTok & Google sama-sama "Conversions") → tetap
  dijumlah, dengan peringatan bahwa atribusi tiap platform berbeda (perkiraan kasar).
- **ROAS gabungan** hanya dari platform yang punya kolom nilai penjualan, dan disebut platformnya.
- JSON yang sama dua kali → ditolak. Catatan kurs tiap platform ikut tampil. Saran diambil
  bergiliran per platform (maks. 6).
Sampaikan semua peringatan ke pengguna; jangan disembunyikan.

### 3. Ekspor rincian per kampanye (opsional)
Tambahkan `--csv-keluaran "<nama-file>.csv"` pada Langkah 1 untuk file CSV rincian per kampanye
(nama kampanye yang diawali `=`/`+`/`-`/`@` otomatis diberi tanda kutip agar tidak dieksekusi
sebagai formula). Angka ditulis mentah: tanpa pemisah ribuan, desimal titik (`1245600`, `1.6`).
Nama file keluaran tidak boleh sama dengan file ekspor asli (ditolak agar tidak tertimpa).

### 4. Tulis laporan ke pengguna
Kirim field `teks` (dari `--json`) atau keluaran teks langsung **apa adanya**: boleh menambah
1-2 kalimat pembuka, tapi **jangan mengubah angka/persen**. Blok `⚠️ PERLU DICEK SEBELUM DIPAKAI`
(di atas) dan `Catatan` (di bawah, termasuk sel kosong yang dihitung 0, baris total yang
dilewati, dan kolom yang dibaca) wajib ikut terkirim. Bila ada ⚠️, sebutkan di kalimat pembuka.

### 5. (Lanjutan, opsional) Jadwalkan otomatis
Setelah pengguna puas dengan hasil laporan manual di atas selama minimal 1 minggu, tawarkan
menjadwalkannya lewat `laporan-otomatis-terjadwal` mengikuti pola di
`references/openclaw-jadwal.md`. **Ekspor dari Ads Manager tetap manual** — OpenClaw tidak login/
menarik data dari Meta/TikTok/Shopee/Google secara otomatis (keputusan pemilik Komunitech, lihat
`references/openclaw-jadwal.md`).

## Rumus (dipakai script, untuk hitung manual bila Python tak tersedia)
Per baris kampanye setelah baris total dibuang: `biaya`, `tayangan`, `klik`, `hasil`,
`nilai_hasil` (opsional, untuk ROAS) dijumlah per nama kampanye (menangani ekspor dengan baris
harian per kampanye). Sel metrik kosong/`-`/`--` = 0 (dicatat); baris yang **biayanya** tidak
terbaca tidak dihitung dan disebut namanya di ⚠️. Lalu:
```
CPC              = biaya ÷ klik                (klik = 0 → "-")
CPM              = biaya ÷ tayangan × 1000      (tayangan = 0 → "-")
CTR              = klik ÷ tayangan × 100%       (tayangan = 0 → "-")
Biaya per hasil  = biaya ÷ hasil                (hasil = 0 → "-", ditandai "tanpa hasil")
ROAS             = nilai_hasil ÷ biaya          (hanya bila kolom nilai/omzet iklan ada)
Biaya vs omzet   = total biaya ÷ omzet × 100%   (hanya bila --omzet diisi)
Rata-rata saran  = total biaya ÷ total hasil    (= "Biaya per hasil" di laporan)
```
Semua hitungan memakai `Decimal` (tanpa float). Kampanye berbiaya Rp 0 (dijeda) tidak dinilai.
TERBAIK = biaya per hasil termurah; PERLU PERHATIAN = tanpa hasil (biaya terbesar dulu) lalu
biaya per hasil termahal; keduanya **tidak pernah beririsan**. Saran "matikan" = biaya per hasil
> 2× rata-rata; "naikkan" = ≤ ½ rata-rata; di bawah 5 hasil diberi catatan "sampel kecil".
**Pembulatan (sama untuk seluruh library, lihat `CLAUDE.md`):** skill ini tidak menghitung PPN;
nominal Rupiah dibulatkan ke rupiah terdekat, 0,5 menjauhi nol (mis. Rp100,5 → Rp101). Persen & ROAS dibulatkan 1 desimal,
0,05 menjauhi nol (mis. 91,65% → 91,7%). Perbandingan minggu lalu memakai rumus yang sama seperti
`laporan-harian-usaha`: `(sekarang − lalu) ÷ lalu × 100`; pembanding Rp0 → "naik dari Rp 0 (persen
tidak dihitung)"; keduanya Rp0 → "sama-sama Rp 0". *Pembulatan di sini belum dicocokkan dengan
Coretax (tidak relevan untuk laporan iklan, tapi mengikuti standar pembulatan library ini).*

## Format output
```
LAPORAN IKLAN MINGGUAN — <Platform>
Periode: <awal> s.d. <akhir>             (dari kolom tanggal/Reporting starts-ends/baris judul)

⚠️ PERLU DICEK SEBELUM DIPAKAI:          (hanya bila ada)
- ...

Total belanja iklan: Rp ...
Tayangan: ... | Klik: ... | <Hasil>: ...
CPC: Rp ... | CPM: Rp ... | CTR: ...%
Biaya per <hasil>: Rp ...
ROAS: ...x                              (bila ada data nilai/omzet iklan)
Biaya iklan vs omzet: ...%  dari omzet Rp ...   (bila --omzet diisi)

VS MINGGU LALU                           (bila --sebelumnya diisi)
Biaya iklan: Rp ... (naik/turun ...% dari minggu lalu Rp ...)
Hasil: ... (naik/turun ...% dari minggu lalu ...)
Biaya per hasil: Rp ... (naik/turun ...% dari minggu lalu Rp ...)

TERBAIK (biaya per hasil termurah)        (maks. 3)
1. <nama>: Rp .../hasil (... hasil, Rp ...)

PERLU PERHATIAN (tanpa hasil / biaya per hasil termahal)   (maks. 3, tanpa irisan)
1. <nama>: Rp ... terpakai, 0 hasil

SARAN
1. ...
(Saran berdasarkan angka minggu ini, bukan jaminan hasil. Keputusan tetap di tangan Anda.)

Catatan:
- ... (mata uang/kurs, sel kosong = 0, baris total dilewati, PPN bila --omzet, kolom dibaca)
```

## Contoh
**Input pengguna:** "Ini ekspor Meta Ads minggu ini sama minggu lalu, tolong buatin laporannya.
Omzet toko minggu ini 20 juta."

**Alur:** jalankan `analisis meta_minggu_ini.csv --sebelumnya meta_minggu_lalu.csv --omzet
20000000` → platform terdeteksi "Meta Ads (Facebook/Instagram)", 1 baris "Total" dilewati → kirim
`teks` apa adanya. Contoh lengkap hasil nyata: `examples/uji-pembuat-01-meta-mingguan-vs-lalu.md`
dan catatan revisi `examples/uji-pembuat/UJI-PEMBUAT-v1.0.1.md` & `UJI-PEMBUAT-v1.0.2.md`.

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- **Nama kolom bisa berbeda** menurut bahasa/versi UI Ads Manager. **Belum semua nama kolom
  terverifikasi dari ekspor asli**: nama kolom Meta Ads dan perilaku sel `Results` kosong,
  bentuk ekspor Google Ads (baris judul, `Total: Account`), dan beberapa kolom TikTok bersandar
  pada ringkasan/sumber pihak ketiga (status per platform di `references/sumber-kolom.md`).
  Karena itu laporan selalu mencetak "Kolom dibaca: ..." di Catatan: cocokkan sekali dengan file
  pengguna. Deteksi gagal → script memberi daftar kolom + cara mengisi manual (`--kolom-...`);
  jangan menebak sendiri.
- **Baris total (v1.0.3)** dikenali dari kata kepala di awal sel ("Total", "Totals", "Jumlah",
  "Grand Total", "Subtotal", "Summary", "Ringkasan", "Overall"...) yang sisanya **hanya** tanda
  baca atau kata cakupan ("Total:", "Total (5 iklan)", "Total: Account", "Total 4 kampanye",
  "Total of 3 campaigns", "Total Akun") → dilewati. Nama kampanye seperti "Total Look Hijab",
  "Total 12.12 Flash Sale", "Jumlah 2 Pcs Bundling", atau "Total 12.12" (sisa hanya angka) **tetap
  dihitung**. Label total di kolom lain sementara kolom nama berisi nama biasa juga tetap dihitung.
- **Setiap baris yang dikecualikan sebagai total/subtotal selalu diberi ⚠️** berisi nama/label +
  biayanya (plus jumlah baris lain bila angkanya tidak cocok). Sampaikan ⚠️ ini ke pengguna.
- **Pengaman silang angka:** baris berbiaya terbesar dibandingkan dengan jumlah semua baris lain.
  Biaya, tayangan, dan klik sama persis atau selisih ≤ 2% → dianggap total, dibuang, dan diberi ⚠️
  (satu-satunya jalan nama seperti "Total 12.12 Flash Sale" dibuang). Hanya biayanya yang dalam
  ±5% dari jumlah baris lain → **tetap dihitung** tapi diberi ⚠️ sopan ("mohon dicek… mungkin
  terjumlah dua kali") beserta total yang benar bila baris itu ternyata total.
- **Subtotal buatan admin:** kolom nama kosong + kolom lain berbunyi mirip total ("Subtotal Kamp
  A") → dibuang hanya bila biaya, tayangan & klik ≈ (±2%) jumlah baris-baris tepat di atas/
  bawahnya; bila tidak cocok, tetap dihitung + ⚠️ agar pengguna mengecek.
- **Subtotal di kolom nama (v1.0.4):** baris berawalan "Subtotal"/"Sub total"/"Sub-total"/
  "Jumlah sementara" ("Subtotal: Retarget Video") → selalu dikecualikan + ⚠️ nama & biaya (⚠️
  menyebut apakah angkanya cocok dengan baris di sekitarnya). Nama = nama kampanye di atasnya +
  kata total ("Retarget Video Total", "Total: Retarget Video") → dikecualikan bila biayanya ≈ (±2%)
  jumlah baris kampanye itu tepat di atasnya; bila tidak cocok, **tetap dihitung** + ⚠️. Nama sama
  persis → dikecualikan hanya bila baris itu tanpa tanggal (baris di atasnya bertanggal) dan biaya,
  tayangan & klik semuanya ≈ jumlahnya. Kampanye sungguhan tidak pernah dibuang tanpa ⚠️.
- **Cek kewajaran:** CPC < Rp 10 atau ROAS > 50x → ⚠️ "tidak wajar" (tanda kolom/mata uang salah).
- **Rentang data > 7 hari**, tanggal tak terbaca, atau file minggu lalu = file minggu ini → ⚠️.
- **Pembagi nol** (0 klik/0 tayangan/0 hasil) → ditampilkan `-`, bukan error atau angka mengada-ada.
- **Mata uang bukan IDR** (label kolom, kolom Currency, atau simbol di sel) → ditolak sampai
  pengguna memberi `--kurs` > 0 (dicatat sumber & tanggal kursnya) atau menegaskan `--mata-uang
  IDR`. Tidak pernah dikonversi diam-diam.
- **PPN:** biaya di file ekspor biasanya belum termasuk PPN yang ditagihkan platform ke akun
  Indonesia; bila `--omzet` diisi, laporan mengingatkan untuk cek invoice platform.
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
  hasil, biaya-per-hasil 2× rata-rata, ROAS < 1x) berdasarkan data minggu itu saja: bukan
  prediksi, bukan audit strategi iklan penuh, dan tidak menilai kualitas materi/target iklan.
  Hasil < 5 diberi catatan "sampel kecil".
- **Python tidak bisa dijalankan:** hitung manual dengan rumus di atas per kampanye, jumlahkan
  baris (kecuali baris Total), dan beri tahu pengguna hasil belum diverifikasi script.
- **Privasi:** hanya angka performa iklan (biaya, tayangan, klik, hasil, nilai). Tidak ada data
  pelanggan/nomor kontak yang diproses atau dikirim ke layanan eksternal.

## Riwayat versi
- **1.0.8** (2026-09-29): aturan kerja standar library: tidak menginstal paket, tidak membuka/mencari file di luar yang diberikan, lokasi file baru disebut, hasil di folder kerja yang disepakati (bukan /tmp).
- **1.0.7** (2026-09-29): pada file bertingkat (kampanye > grup iklan), baris yang kolom grup iklannya kosong padahal kampanye itu punya baris grup iklan bernama diperiksa: bila biaya, tayangan & kliknya sama dengan jumlah baris grup iklan (total kampanye tanpa label) baris itu tidak dihitung dua kali dan diberi ⚠️; bila tidak sama tetap dihitung dengan ⚠️ "mohon cek". Baris Performance Max tanpa saudara tidak terkena. Tes regresi 94.
- **1.0.5** (2026-09-29): baris Google Performance Max tanpa grup iklan tidak lagi tampil
  "(tanpa nama, baris N)", melainkan memakai nama grup aset (bila ada kolom "Asset group") atau nama
  kampanye + "(tanpa grup iklan)" (P-3); ⚠️ subtotal/total yang meragukan kini menyebut total belanja
  sekarang dan total alternatif bila baris itu dihitung/tidak dihitung (P-4). Tes regresi 91.
- **1.0.4** (2026-09-28): subtotal buatan admin di kolom nama ("Subtotal: Retarget Video",
  "Retarget Video Total", "Jumlah sementara") tidak lagi terhitung dua kali dan selalu diberi ⚠️
  nama + biaya (N3); kalimat ⚠️ "biaya hampir sama dengan jumlah baris lain" dilunakkan. Tes regresi
  bertambah jadi 87.
- **1.0.3** (2026-09-26): nama kampanye berawalan "Total"/"Jumlah" tidak lagi dibuang; setiap baris
  total yang dikecualikan diberi ⚠️; ⚠️ ±5% (M2); subtotal dengan kolom nama kosong (M3).
- **1.0.2** (2026-09-26): ekspor bertingkat dirinci per iklan (N1); label total umum + cek silang (N2).
- **1.0.1** (2026-09-26): sel kosong, baris total varian, pemilihan kolom Google Ads, mata uang non-IDR.
- **1.0.0**: rilis draf pertama.
