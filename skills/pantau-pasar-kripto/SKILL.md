---
name: pantau-pasar-kripto
description: Memantau harga kripto (BTC/ETH/dll) terhadap ambang naik/turun % atau harga Rp/USD yang DITETAPKAN MEMBER SENDIRI, mengirim ringkasan pagi (harga + berita bertautan sumber), checklist riset proyek (due diligence, TANPA kesimpulan beli/jual), dan merapikan + menghitung P/L jurnal trading milik member sendiri. TIDAK ADA auto-trading, TIDAK ADA rekomendasi beli/jual/tahan, TIDAK menyimpan API key exchange. Gunakan saat pengguna minta "pantau harga BTC/ETH", "kabari kalau kripto turun/naik X%", "ringkasan berita kripto pagi", "riset koin ini", "cek proyek kripto", "rapikan jurnal trading saya", crypto price alert, crypto watchlist, DYOR checklist, trading journal. JANGAN dipakai untuk eksekusi order, sinyal trading, target harga, atau alokasi portofolio -- skill ini menolak permintaan itu.
---

# Pantau Pasar Kripto

## Tujuan
Membantu member memantau harga & berita kripto, meriset proyek secara terstruktur, dan
merapikan jurnal trading -- **semua berbasis fakta bersumber, tanpa satu pun rekomendasi
beli/jual/tahan**. Skill ini adalah alat informasi & pencatatan, bukan bot trading.

## BATAS TEGAS (baca sebelum mulai -- berlaku di SETIAP langkah di bawah)
1. **Tidak ada rekomendasi beli/jual/tahan, target harga, sinyal "entry/exit", atau
   alokasi portofolio**, dalam bentuk apa pun (termasuk "kelihatannya bagus untuk masuk").
   Kalau pengguna memaksa minta itu, jelaskan alasan penolakan (lihat "Batasan" di bawah)
   dan tawarkan yang boleh: data, checklist riset, atau jurnal.
2. **Tidak pernah meminta atau menyimpan API key/secret exchange** (Indodax, Binance, dll.)
   dan **tidak pernah mengeksekusi order**. Kalau pengguna minta auto-trading atau minta
   skill "beli otomatis kalau turun X%", **tolak** dan jelaskan alasannya (lihat Batasan).
3. **Disclaimer wajib** di SETIAP keluaran (ringkasan pagi, notifikasi ambang, riset, jurnal):
   *"Informasi, bukan nasihat investasi. Keputusan & risiko sepenuhnya milik Anda."*
4. **Tidak pernah mengarang harga atau berita.** Kalau sumber data gagal, katakan itu apa
   adanya (lihat script `cek_ambang.py`). Kalau tidak ada akses pencarian web, katakan jujur
   bahwa ringkasan berita tidak bisa dibuat saat itu -- jangan menulis berita dari ingatan
   tanpa tautan sumber.
5. **Waspada skema penipuan/pump.** Kalau riset menemukan tanda klasik skema penipuan
   (janji imbal hasil tetap, tekanan "buru-buru sebelum kehabisan", token baru tanpa audit/
   tim jelas, grup yang melarang bertanya kritis), sebutkan ini secara **netral & edukatif**
   di bagian riset -- bukan sebagai "sinyal jual", tapi sebagai fakta yang perlu diketahui.
   Sebutkan juga bahwa dugaan penipuan/skema ilegal bisa dilaporkan ke **OJK (kontak 157)**
   atau **Satgas PASTI** (satgas pemberantasan aktivitas keuangan ilegal) -- ini info kanal
   resmi, bukan tuduhan atas proyek tertentu.
6. **Kalau member sudah menempel/membagikan API key exchange ke chat ini** (disengaja atau
   tidak), **jangan menyimpannya, jangan mengulanginya kembali di keluaran mana pun** (juga
   jangan ditulis ke file skill ini), dan **segera sarankan member mencabut (revoke) key itu
   di exchange lalu membuat yang baru** -- key yang pernah terlihat di riwayat chat/log
   harus dianggap bocor, terlepas dari niat awal member.

## Kapan digunakan
- "Pantau BTC dan ETH, kabari kalau turun lebih dari 5%."
- "Kirim ringkasan harga & berita kripto tiap jam 7 pagi."
- "Riset proyek [nama koin] ini, saya mau tahu fakta-faktanya."
- "Rapikan jurnal trading saya, hitung untung/rugi saya bulan ini."
- "Ingatkan saya sesuai rencana yang saya tulis di jurnal."

## Kapan TIDAK digunakan
- Minta rekomendasi beli/jual, target harga, atau "kapan waktu terbaik masuk/keluar" →
  **tolak**, jelaskan Batas Tegas #1, tawarkan data & checklist riset sebagai gantinya.
- Minta auto-trading, bot eksekusi order, atau menyambungkan API key exchange → **tolak**,
  jelaskan Batas Tegas #2. Arahkan ke fitur limit/stop order **bawaan aplikasi exchange
  resmi** (dieksekusi & dipantau manual oleh pengguna sendiri, bukan lewat skill ini).
- Minta clone suara/wajah untuk konten promosi koin → di luar cakupan skill ini, dan
  library Komunitech menolak permintaan itu di skill mana pun.
- Laporan/notifikasi untuk **grup/pelanggan/broadcast** → di luar cakupan; notifikasi
  hanya untuk pemilik/member sendiri.
- Kebutuhan pajak transaksi kripto (PPh/PPN kripto) → skill ini tidak menghitung pajak;
  arahkan ke konsultan pajak/DJP untuk kepastian kewajiban pajak individu.

## Input

### 1. Daftar pantau (`kripto/PANTAU.md`)
File markdown yang **ditulis/diubah oleh member** (lihat `templates/PANTAU.md`). Tabel:

| Koin | Ambang naik | Ambang turun | Harga acuan | Kata kunci berita | Jam ringkasan pagi |
|---|---|---|---|---|---|
| BTC | 8% | 5% | (kosong = pakai 24 jam terakhir) | bitcoin, ETF, halving | 07:00 WIB |

- **Ambang naik/turun**: persen perubahan. Kalau "Harga acuan" kosong, dihitung dari
  perubahan 24 jam (data bawaan sumber). Kalau diisi (mis. harga beli member), dihitung
  dari acuan itu -- tetap tetap sampai member mengubahnya sendiri.
  Boleh juga menulis ambang sebagai **harga absolut**, mis. "di atas Rp 1,6 M" / "US$ 3.000".
- **Kata kunci berita**: dipakai agent saat mencari berita (Langkah 3).
- **Jam ringkasan pagi**: default 07:00 WIB kalau tidak diisi.

Kalau member belum punya `kripto/PANTAU.md`, **tanyakan sekali** (bernomor, maks 5):
1. Koin apa saja? (kode, mis. BTC, ETH)
2. Mau dikabari kalau naik/turun berapa persen? Atau di harga berapa (Rp/USD)?
3. Ada harga acuan sendiri (mis. harga beli), atau cukup dibandingkan 24 jam terakhir?
4. Kata kunci berita yang ingin dipantau? (boleh kosong = nama koin saja)
5. Ringkasan pagi dikirim jam berapa & lewat kanal apa (Telegram/WhatsApp)?

Kalau pengguna ingin cepat: pakai default **ambang ±5% (naik & turun) dari 24 jam
terakhir, ringkasan jam 07:00 WIB, kanal Telegram**, dan sebutkan bahwa ini cuma titik
awal yang masuk akal -- angka ambang sepenuhnya **diatur sendiri oleh member**, kapan pun
bisa diubah dengan mengedit `kripto/PANTAU.md` lalu minta diterjemahkan ulang.

### 2. Jurnal trading (`kripto/JURNAL.csv`)
Milik member, format di `templates/JURNAL.csv` (lihat juga docstring
`scripts/hitung_pl_jurnal.py`). Member menulis alasan/rencananya sendiri di kolom
`alasan_rencana` dan `tinjau_ulang_syarat` -- skill **tidak pernah mengisi kolom ini
dengan opini sendiri**, hanya merapikan & menghitung.

## Langkah kerja

### A. Cek ambang (dipicu manual atau lewat automation OpenClaw)
1. Kalau `kripto/konfigurasi.json` belum ada atau lebih lama dari `kripto/PANTAU.md`,
   **terjemahkan** tabel `PANTAU.md` ke `kripto/konfigurasi.json` (format lihat
   docstring/`--help` `cek_ambang.py`): satu objek per koin dengan `kode`, `coingecko_id`
   (untuk USD atau default IDR; cari id resmi CoinGecko, mis. `bitcoin`, `ethereum`),
   opsional `indodax_pair` (untuk sumber IDR lokal, mis. `btcidr`), `mata_uang`
   (`idr`/`usd`), `ambang_naik_persen`/`ambang_turun_persen`, `harga_acuan` (kalau member
   mengisi), dan/atau `ambang_harga_di_atas`/`ambang_harga_di_bawah`. File ini yang
   nantinya dipanggil otomatis oleh jadwal -- **tunjukkan isinya ke member** untuk
   dikonfirmasi sebelum lanjut, supaya salah terjemahan ketahuan.
2. Jalankan:
   ```bash
   python3 <folder-skill-ini>/scripts/cek_ambang.py \
     --konfigurasi kripto/konfigurasi.json --state kripto/state.json
   ```
   (Windows: `python`/`py`. Uji tanpa jaringan: tambahkan `--harga-file <file-harga-uji>`,
   lihat docstring script untuk formatnya.)
3. Baca field `pesan_singkat` di hasil JSON -- itu sudah siap kirim apa adanya (sudah
   memuat sumber, jam data, peringatan data basi/tua, dan disclaimer per koin). Untuk
   keluaran teks langsung tanpa JSON, tambahkan `--keluaran teks`.
4. Kalau `perlu_lapor_sekarang: true`, itulah yang dikirim/ditunjukkan ke member sebagai
   notifikasi. Kalau `ada_koin_gagal_total: true`, beri tahu member koin mana yang gagal
   diambil datanya (jangan diam-diam disembunyikan) -- `pesan_singkat` sudah menyebutnya
   secara eksplisit, jangan pernah menyimpulkan "tidak ada ambang terlewati" kalau
   sebagian koin justru TIDAK BISA dicek sama sekali.
5. **Anti-spam bawaan:** `cek_ambang.py` menyimpan status "sudah dilaporkan" per koin/
   ambang di `kripto/state.json`. Selama ambang masih terlewati tapi belum berubah,
   `perlu_lapor_sekarang` akan `false` pada giliran berikutnya (diredam) sampai jeda
   `--jeda-ulang-jam` (default 6 jam) habis, atau sampai kondisinya pulih dulu lalu
   terpicu lagi. Field `ambang_terlewati` (beda dari `perlu_lapor_sekarang`) selalu
   menunjukkan fakta apa adanya, terlepas dari sudah dilaporkan atau belum.
6. Exit code script: `0` = tidak ada yang PERLU dilaporkan sekarang, `2` = ADA yang perlu
   dilaporkan (ambang baru terlewati, atau jeda lapor-ulang habis -- dipakai automation
   untuk memutuskan kapan perlu memanggil agent/mengirim pesan, lihat
   `references/openclaw-jadwal.md`), `3` = sukses sebagian (ada koin gagal total, tetap
   perlu diberitahukan lewat wrapper `scripts/cek_dan_lapor.py`), `1` = error input/
   konfigurasi.

### B. Ringkasan pagi
1. Jalankan `cek_ambang.py` (Langkah A.2) untuk bagian harga & perubahan 24 jam.
2. Untuk berita: **kalau agent punya akses pencarian web** (`web_search`/`web_fetch` di
   OpenClaw, atau alat browsing di platform lain), cari berita terbaru untuk tiap kata
   kunci di `PANTAU.md`, ambil **maksimal 3-5 judul paling relevan hari itu**, dan
   **selalu sertakan tautan sumber asli** per judul. Kalau **tidak ada** akses pencarian
   web, katakan itu jujur: *"Ringkasan berita tidak bisa dibuat -- agent ini tidak punya
   akses pencarian web saat ini. Harga & ambang tetap di bawah."* -- jangan menulis
   ringkasan berita dari ingatan tanpa tautan.
   **Jangan pernah meneruskan target harga, level support/resistance, prediksi angka, atau
   rekomendasi analis dari isi artikel** (berita kripto sering memuat ini, mis. "resistance
   US$120-130") -- itu sama saja memberi sinyal trading lewat jalur belakang, melanggar
   Batas Tegas #1. Ringkas hanya **peristiwa yang sudah terjadi** (rilis, regulasi,
   kemitraan, listing/delisting, dst.); kalau sebuah artikel memuat proyeksi/target harga,
   cukup tulis **"artikel ini juga memuat proyeksi analis -- tidak ditampilkan di sini"**
   tanpa mengutip angkanya.
3. Kalender peristiwa (listing/delisting bursa lokal, jadwal rilis regulasi OJK, dst.)
   **hanya** ditulis kalau ditemukan lewat pencarian dengan sumber jelas. Kalau tidak
   ditemukan, jangan ditulis sama sekali (jangan mengarang "kemungkinan ada rilis X").
4. Susun pesan: harga & perubahan 24 jam (dari Langkah B.1) → berita bertautan (atau
   pernyataan jujur tidak tersedia) → kalender peristiwa (kalau ada) → disclaimer.

### C. Riset proyek terstruktur (checklist due diligence)
1. Gunakan checklist di `references/checklist-riset.md` (tim, tokenomics, audit kontrak,
   likuiditas, status legal Indonesia). **Isi HANYA fakta yang punya sumber** (tautan
   resmi: whitepaper, situs proyek, explorer blockchain, laporan audit, OJK). Kolom yang
   tidak ditemukan sumbernya ditulis **"tidak ditemukan / perlu dicek"**, bukan diisi
   perkiraan.
2. Untuk status legal Indonesia: cek `references/regulasi.md` untuk dasar hukum yang
   sudah terverifikasi (per tanggal referensi doc itu). Kalau member menanyakan status
   terkini yang mungkin sudah berubah, arahkan verifikasi ke ojk.go.id /
   peraturan.bpk.go.id, jangan mengutip angka/tanggal dari ingatan tanpa cek ulang.
3. Kalau ditemukan tanda skema penipuan/pump klasik, tulis di bagian "Perhatian" secara
   netral (lihat Batas Tegas #5).
4. **Tutup dengan disclaimer, dan JANGAN tambahkan kesimpulan "layak dibeli" atau
   sejenisnya** -- checklist berhenti di fakta, keputusan sepenuhnya di tangan member.

### D. Jurnal trading (rapikan + hitung P/L)
1. Jalankan:
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_pl_jurnal.py --jurnal kripto/JURNAL.csv
   ```
   (`--hari-ini YYYY-MM-DD` opsional, untuk mencocokkan pengingat pada tanggal tertentu.
   `--periode bulan-ini|tahun-ini` atau `--dari YYYY-MM-DD --sampai YYYY-MM-DD` opsional,
   untuk membatasi transaksi JUAL yang dijumlahkan ke `realized_per_koin`/
   `total_realized_pl` -- mis. saat member minta "untung/rugi bulan ini"; FIFO & cost
   basis tetap dihitung dari SELURUH riwayat 'beli', filter hanya membatasi tampilan.)
2. Tunjukkan `realized_per_koin` (untung/rugi transaksi yang sudah dijual, sudah
   memperhitungkan biaya) dan `posisi_tersisa` (rata-rata harga perolehan yang masih
   dipegang) apa adanya dari hasil JSON -- **jangan dihitung ulang manual**, angka
   sudah lewat script (FIFO).
3. Kalau ada `baris_bermasalah` (baris rusak atau jual melebihi stok tercatat), sampaikan
   ke member supaya jurnalnya diperbaiki -- jangan diam-diam mengabaikannya.
4. Kalau ada `tinjau_ulang_jatuh_tempo` (rencana yang member tulis sendiri dan sudah jatuh
   tempo), sampaikan **persis seperti yang member tulis** di `syarat` -- **jangan** ditambah
   opini baru soal apakah rencana itu masih relevan atau tidak.
5. **Info pajak (bukan nasihat, sekadar info):** transaksi kripto di platform PAKD
   (Pedagang Aset Keuangan Digital) berizin OJK dalam negeri dikenai PPh final 0,21% dari
   nilai transaksi (biasanya sudah dipotong otomatis oleh exchange -- lihat
   `references/regulasi.md`). Kalau member menanyakan ini, sebutkan info ini dan sarankan
   memasukkan potongan pajak itu ke kolom `biaya` di `JURNAL.csv` supaya P/L yang dihitung
   sudah bersih (setelah pajak), lalu tetap arahkan ke konsultan pajak/DJP untuk kepastian
   kewajiban pajak individu member (skill ini tidak menghitung SPT/pelaporan pajak).

### E. Membuat jadwal otomatis (opsional, setelah A/B pertama kali berhasil manual)
Lihat `references/openclaw-jadwal.md` untuk perintah `openclaw automations` yang
**terbukti** jalan di Gateway uji (bukan cuma `--help`): pola utama memakai `--command`
menjalankan `scripts/cek_dan_lapor.py` (wrapper Python lintas OS yang menerjemahkan exit
code `cek_ambang.py` jadi pesan siap kirim atau `NO_REPLY`, dan SELALU keluar dengan kode
0 supaya Gateway tidak salah mencatatnya sebagai job gagal), dan kanal pengiriman
(Telegram default; WhatsApp hanya nomor terpisah + persetujuan risiko tertulis, sama
seperti aturan skill `laporan-otomatis-terjadwal`). **Selalu minta konfirmasi eksplisit
("Lanjut? ya/tidak") sebelum menjalankan perintah pembuatan jadwal.** Untuk menguji
sebelum mengaktifkan, ikuti cara di `references/openclaw-jadwal.md` §3 -- **JANGAN**
mengandalkan `automations run --wait` untuk menyimpulkan bahwa trigger otomatis bekerja
(perintah itu memaksa job jalan, mengabaikan trigger); itu hanya valid untuk menguji pola
`--command` (job SELALU jalan, wrapper yang membedakan tenang/terpicu).

## Format output
Semua keluaran (ringkasan pagi, notifikasi ambang, hasil riset, hasil jurnal) diakhiri
dengan baris disclaimer: *"Informasi, bukan nasihat investasi. Keputusan & risiko
sepenuhnya milik Anda."* Notifikasi ambang & ringkasan pagi selalu mencantumkan **sumber
data & jam data** (dari field `sumber`/`jam_data` hasil `cek_ambang.py`), termasuk kalau
sedang memakai data cache/basi.

## Contoh
**Input pengguna:** "Pantau BTC dan ETH, kabari kalau turun lebih dari 5%, dan kirim
ringkasan berita tiap jam 7 pagi ke Telegram saya."

**Alur:** tanyakan sisanya (harga acuan? kata kunci berita?) dalam satu pesan bernomor →
member jawab/pakai default → buat `kripto/PANTAU.md` + `kripto/konfigurasi.json` →
tunjukkan contoh hasil `cek_ambang.py` (Langkah A) → tunjukkan contoh ringkasan pagi
(Langkah B, dengan tautan berita nyata atau pernyataan jujur tak ada akses web) → minta
konfirmasi → buat 2 jadwal (ringkasan pagi harian, cek ambang tiap jam) mengikuti
`references/openclaw-jadwal.md` → uji sekali → jelaskan cara jeda/hapus.

## Batasan & penanganan error
- **Tidak ada API key exchange, tidak ada eksekusi order.** Kalau pengguna bersikeras
  minta ini, jelaskan: (1) berita/web yang dipakai agent bisa disusupi instruksi
  tersembunyi (*prompt injection*) yang mencoba memicu transaksi, (2) kesalahan model AI
  soal auto-trading = kerugian uang nyata dan tidak bisa dibatalkan, (3) kredensial
  exchange yang tersimpan di mesin yang juga membaca konten dari luar adalah risiko
  keamanan. Alternatif aman: fitur limit/stop order **bawaan aplikasi exchange resmi**
  (dieksekusi manual oleh member sendiri).
- **Sumber harga gagal/data basi:** `cek_ambang.py` tidak pernah mengarang angka. Kalau
  sumber langsung gagal, dipakai cache terakhir dengan peringatan jelas + jam datanya;
  kalau tidak ada cache sama sekali, koin itu ditandai "gagal_total" tanpa angka apa pun.
  Selalu tunjukkan status ini ke member, jangan disembunyikan demi pesan yang "rapi".
- **Tidak ada akses pencarian web:** ringkasan berita & kalender peristiwa dilewati dengan
  pernyataan jujur, bagian harga & ambang tetap jalan (tidak saling bergantung).
- **Python tidak bisa dijalankan:** untuk cek ambang, hitung manual: persen = (harga
  sekarang - harga acuan) / harga acuan × 100, lalu bandingkan ke ambang; beri tahu member
  hasil ini belum diverifikasi script. Untuk jurnal, jangan menghitung P/L manual dengan
  banyak baris (rawan salah) -- sampaikan bahwa perhitungan perlu Python dan tawarkan
  membantu memasang Python, atau hitung 1-2 baris paling sederhana saja secara manual
  sambil menyebut ini belum diverifikasi script.
- **Regulasi kripto Indonesia bisa berubah.** `references/regulasi.md` berisi fakta yang
  sudah diverifikasi ke sumber resmi PER TANGGAL referensi di file itu. Untuk kebutuhan
  yang butuh kepastian hukum terkini (mis. legalitas suatu penawaran investasi), arahkan
  ke ojk.go.id / peraturan.bpk.go.id langsung atau konsultan hukum, jangan menjamin
  kebenaran info yang mungkin sudah usang.
- **Data pribadi:** `kripto/PANTAU.md`, `konfigurasi.json`, `state.json`, dan
  `JURNAL.csv` berisi data finansial pribadi member. Semua tersimpan lokal di komputer
  member; skill ini tidak mengirim isinya ke server mana pun selain penyedia model AI
  (untuk membaca instruksi, sama seperti percakapan biasa) dan API harga publik (yang
  hanya menerima kode koin, bukan data member).
