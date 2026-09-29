---
name: buku-piutang
description: Buku piutang pelanggan lokal (SQLite di komputer pemilik, tanpa langganan/internet) yang dioperasikan lewat chat - catat bon/nota tempo (pelanggan, nomor nota, tanggal, jatuh tempo, nominal, DPP+PPN), catat pembayaran sebagian/lunas/kelebihan bayar (deposit) tanpa saldo minus diam-diam, saldo per pelanggan, umur piutang (belum jatuh tempo, 1-30, 31-60, 61-90, >90 hari), daftar jatuh tempo hari ini/minggu ini/terlewat, impor CSV dari nota/kasir, rekap --json, draf pesan tagihan sopan + tautan wa.me yang DIKIRIM SENDIRI oleh pemilik, ringkasan harian ke Telegram (OpenClaw), cadangan & restore aman. Gunakan untuk "catat bon Bu Tini 1,2 juta", "Kafe Senja bayar 1 juta", "siapa yang belum bayar", "piutang yang jatuh tempo minggu ini", "umur piutang", "saldo pelanggan", accounts receivable, AR aging, customer ledger, invoice tracking. Bukan untuk kirim massal/broadcast atau surat somasi (pakai tagih-piutang).
---

# Buku Piutang (bon & tagihan pelanggan)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menggantikan buku bon/Excel piutang dan fitur piutang aplikasi akuntansi berlangganan: semua tagihan yang belum dibayar pelanggan ada di **satu file database di komputer pemilik**, dan kamu (agent) mengoperasikannya lewat `scripts/piutang.py`. Hasilnya: tahu persis siapa berutang berapa, nota mana yang terlewat, umur piutang, uang masuk hari ini, dan setiap tagihan punya **draf pesan sopan + tautan wa.me** yang tinggal diperiksa dan dikirim sendiri oleh pemilik.

## Kapan digunakan
- "Catat bon Warung Bu Tini 1.250.000, nota B-0901, tempo 2 minggu." / "CV Maju invoice INV-0910 DPP 10 juta + PPN."
- "Kafe Senja transfer 1 juta." / "Bu Tini bayar lunas." / "Pak Joko bayar 1,3 juta padahal utangnya 1,25 juta."
- "Siapa saja yang belum bayar?" / "Saldo Kafe Senja berapa?" / "Umur piutang per akhir bulan."
- "Tagihan yang jatuh tempo hari ini / minggu ini / sudah lewat?"
- "Bikinin pesan tagihan buat Kafe Senja." / "Sudah saya kirim."
- "Masukkan daftar bon dari Excel/kasir ini" (CSV) / "Rekap piutang bulan ini" / "Ekspor ke Excel".
- "Kirim ringkasan piutang ke Telegram saya tiap pagi" (OpenClaw).

## Kapan TIDAK digunakan
- **Mengirim pesan tagihan otomatis/massal/broadcast** → **tolak**. Skill ini hanya menyiapkan draf + tautan; manusia yang mengirim satu per satu (keputusan pemilik Komunitech: OpenClaw memakai WhatsApp Web tidak resmi, kiriman otomatis bisa membuat nomor diblokir).
- Surat teguran resmi/somasi, denda keterlambatan, tahap penagihan bertahap → `tagih-piutang` (datanya dari sini: `ekspor --format tagih-piutang`). Membuat invoice/faktur baru → `buat-invoice`. Menghitung PPN dari harga termasuk PPN → `hitung-ppn`.
- Mencatat penjualan tunai di kasir → `kasir-lokal` (kasir-lokal sengaja tidak mencatat bon; bon dicatat di sini). Prospek yang belum membeli → `crm-wa`.
- Utang **usaha ke pemasok** (hutang dagang), laporan laba rugi/neraca → di luar cakupan; sarankan `laporan-keuangan-emkm`.
- Pinjaman berbunga antar-perorangan, penagihan atas nama pinjol/leasing, ancaman, mempermalukan debitur di grup/medsos, menghubungi keluarga/atasan debitur → tolak bagian itu, jelaskan singkat, tawarkan draf sopan.
- Skill rujukan tidak terpasang: jelaskan singkat bedanya, lalu bantu sebisanya dengan draf bawaan skill ini.

## Aturan wajib
1. **Tidak pernah mengirim pesan ke pelanggan.** Tampilkan draf + tautan wa.me; pemilik memeriksa dan menekan Kirim. Setelah pemilik bilang sudah kirim → `terkirim`.
2. **Angka & tanggal dari script.** Sisa, saldo, umur, persen, jatuh tempo: salin dari output. Jangan menghitung atau mengonversi tanggal sendiri; teruskan teks pengguna apa adanya (`--tanggal "1/9/2026"`, `--jumlah "1,3jt"`).
3. **Jangan menebak pelanggan.** Jika script menjawab ambigu/mirip (`pilihan`), tanyakan "Pak Joko yang mana?" lalu ulangi dengan kode (P0003). Pelanggan baru yang namanya mirip pelanggan lama → tanyakan dulu; `--pelanggan-baru` hanya bila pengguna menegaskan orangnya berbeda.
4. **Kelebihan bayar tidak pernah disimpan diam-diam.** Jika `bayar` ditolak karena melebihi tagihan (`kelebihan` di JSON), tanyakan ke pengguna: disimpan sebagai deposit (`--kelebihan kredit`), sudah dikembalikan (`--kelebihan kembalikan`), untuk nota lain (`--kelebihan nota-lain`), atau salah ketik. Setiap perubahan diperiksa script: sisa nota dan deposit tidak pernah boleh minus; jika terjadi, seluruh perubahan dibatalkan.
5. **Perubahan besar** (`init`, `impor`, `potong`, `batal-nota`, `batal-bayar`, `hapus-pelanggan`, `restore`) dijalankan dulu tanpa `--ya` (pratinjau), tunjukkan ringkasannya, lalu ulangi **perintah yang sama + `--ya`** hanya setelah pengguna setuju. Perubahan kecil (`catat`, `bayar`, `pakai-kredit`, `kembalikan`, `ubah-nota`, `terkirim`, `tambah-pelanggan`, `ubah-pelanggan`, `atur`) langsung tersimpan; sampaikan hasilnya agar bisa dikoreksi.
6. **Tanggal format Indonesia** hari/bulan/tahun. Script menolak tanggal yang tidak ada (31/09), format Amerika (10/25/2026), angka seri Excel, tahun ngawur, tanggal nota/bayar di masa depan, dan tanggal tanpa tahun yang jauh. Sampaikan penolakannya dan tanyakan tanggal yang benar; jangan membalik hari/bulan sendiri.
7. **Privasi:** nama, nomor HP, dan utang pelanggan adalah data pribadi (UU 27/2022 PDP). Jangan tampilkan daftar piutang ke grup; untuk yang dibagikan/dijadwalkan pakai `--samarkan`. Sampaikan setiap `peringatan`/`Catatan:` dari script.

## Cara menjalankan script
Path relatif terhadap folder berisi SKILL.md ini (Windows: ganti `python3` dengan `python` atau `py`):
```bash
python3 <folder-skill-ini>/scripts/piutang.py <perintah> [opsi] --json
```
- JSON berisi `ok`, `mode` (`tersimpan`/`pratinjau`/`baca`), `perlu_konfirmasi`, `peringatan`, `error`, `teks` (siap tempel). Kode keluar 1 = gagal (pesan di `error`), 2 = perintah salah tulis.
- Database default `~/KomunitechData/piutang/piutang.db`; bisa diganti `--db PATH` (ditulis **setelah** nama perintah) atau ENV `KOMUNITECH_PIUTANG_DB` / `KOMUNITECH_DATA`. Pakai lokasi yang sama di semua perintah.
- Semua perintah & opsi + kontrak JSON: `references/perintah.md`. Jadwal Telegram: `references/openclaw-jadwal.md`. Tanpa Python: `references/tanpa-python.md`.

## Input
| Info | Wajib? | Default |
|---|---|---|
| Nama usaha, nama pengirim, rekening (untuk draf) | Saat mulai (boleh kosong) | Draf tanpa rekening ("cara yang biasa") |
| Nama pelanggan | Ya | — (tanyakan) |
| Nominal tagihan (atau DPP + PPN 11/12) | Ya | — (tanyakan) |
| Nomor nota | Disarankan | Nomor otomatis `PB-0001` (disebut ke pengguna) |
| Tanggal nota | Tidak | Hari ini (disebut) |
| Jatuh tempo / termin | Tidak | Termin default pengaturan (30 hari; disebut sebagai asumsi) |
| Nomor WA pelanggan | Disarankan | Tanpa nomor: draf tanpa tautan |
| Jumlah & tanggal pembayaran | Ya saat bayar | Tanggal = hari ini; nota = jatuh tempo paling awal dulu |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan). Jika pengguna ingin cepat, simpan yang ada dan sebutkan asumsinya.

## Langkah kerja

### A. Mulai
1. `info --json`. Belum ada database → tanyakan nama usaha, nama di pesan, rekening pembayaran, termin biasa (hari), zona (WIB/WITA/WIT).
2. `init --nama-usaha "..." --pengirim "..." --rekening "BCA ... a.n. ..." [--termin 14] [--zona WIB]` → pratinjau → setuju → ulangi + `--ya`.
3. Punya daftar bon lama di Excel/kasir? Lanjut ke Langkah E (impor).

### B. Catat piutang (bon/nota tempo)
`catat --pelanggan "Warung Bu Tini" --nota B-0901 --tanggal 01/09/2026 --termin 14 --nominal 1.250.000 [--wa 0812-...] [--keterangan "..."]`
- Jatuh tempo: `--jatuh-tempo 15/09/2026` atau `--jatuh-tempo "30 hari"` / `--termin 30` (dari tanggal nota). Angka polos `--jatuh-tempo 30` ditolak (tanggal 30 atau 30 hari?).
- Invoice ber-PPN dari DPP: `--dpp 10jt --ppn 11` (12% × DPP nilai lain 11/12, barang/jasa umum) atau `--ppn 12` (barang mewah). PPN dibulatkan ke bawah sekali; sampaikan catatan bahwa pembulatan belum dicocokkan dengan Coretax. Nota yang totalnya sudah termasuk PPN → cukup `--nominal`.
- Pelanggan baru dibuat otomatis (nomor WA dirapikan ke 62…). Nomor nota sama (INV-001 = inv 001) ditolak agar tidak dobel.
- Pelanggan punya deposit → script menyarankan `pakai-kredit`; tawarkan ke pengguna.

### C. Catat pembayaran
`bayar --pelanggan "Kafe Senja" --jumlah 1jt [--nota B-0905] [--tanggal 15/09/2026] [--metode transfer]`
- Tanpa `--nota`: dipakai untuk nota dengan jatuh tempo paling awal dulu; script menyebut pembagiannya. `--jumlah lunas` = melunasi sisa (nota itu, atau semua nota pelanggan).
- Melebihi tagihan → ditolak (lihat Aturan 4). Pembayaran sama (pelanggan, tanggal, jumlah) sudah tercatat → ditolak; `--izinkan-dobel` hanya bila pengguna menegaskan memang dua kali bayar.
- Deposit: `pakai-kredit --pelanggan ...` (untuk nota terbuka), `kembalikan --pelanggan ... --jumlah 50rb|semua`.
- Koreksi: `ubah-nota --nota ... [--nominal/--jatuh-tempo/--tanggal/--no-baru]`; retur/diskon/diikhlaskan: `potong --nota ... --jumlah ...|sisa --alasan "..."`; salah catat: `batal-bayar --bayar B0003 --alasan ...` / `batal-nota --nota ... --alasan ...` (semua besar kecuali ubah-nota). Pembayaran pada nota yang dibatalkan otomatis menjadi deposit.

### D. Pantau & tagih (inti)
1. `jatuh-tempo` → TERLEWAT, JATUH TEMPO HARI INI, MINGGU INI (7 hari ke depan). `saldo` → per pelanggan; `saldo --pelanggan X` → rincian nota & pembayaran. `umur [--per 30/09/2026]` → umur piutang + persen. Tampilkan teks apa adanya.
2. `draf --pelanggan "Kafe Senja" [--nota ...]` → draf sopan sesuai keterlambatan (pengingat awal, hari H, terlewat ringan, terlewat, terlewat lama + tawaran bertahap) + tautan wa.me. Minta pemilik memeriksa dan menekan Kirim sendiri. Boleh memperhalus atas permintaan pemilik, lalu buat tautannya dengan `draf --pelanggan ... --pesan "<teks final>"` (jangan menyusun tautan sendiri). Angka di draf hanya dari script.
3. Pemilik bilang sudah kirim → `terkirim --pelanggan ...` (dicatat sekali per hari per nota; jumlahnya muncul di daftar).
4. Lewat ≥ 14 hari atau sudah diingatkan ≥ 2 kali → script memberi `saran` memakai `tagih-piutang` untuk pemberitahuan resmi/surat teguran: `ekspor --format tagih-piutang`, lalu jalankan `hitung_telat.py --file <csv>` milik skill itu.

### E. Impor, ekspor, rekap
- `impor file.csv [--termin 14] [--gabung-baris] [--format-tanggal bulan-hari]` → pratinjau (kolom dikenali, nota dicatat, dilewati karena sudah ada/lunas/void, **baris bermasalah + nomor barisnya**) → setuju → `--ya` (cadangan dibuat dulu). Kolom dikenali otomatis: pelanggan/nama/customer, no nota/invoice/transaksi, tanggal, jatuh tempo (tanggal atau "30 hari"), total/nominal, dibayar/DP atau sisa, no wa/hp, status (lunas/tunai/QRIS dilewati, void/batal dilewati, belum lunas/tempo/bon diimpor). Contoh: `templates/piutang-contoh.csv`.
  - File format tanggal Amerika atau campur → **seluruh impor ditolak**; sampaikan, minta dipastikan. `--format-tanggal bulan-hari` hanya bila pengguna memastikan file dari aplikasi berformat bulan/hari.
  - Ekspor kasir per barang (satu nota beberapa baris) → `--gabung-baris`. Impor ulang file yang sama tidak membuat dobel. `.xlsx` → minta disimpan sebagai CSV.
- `ekspor [--format lengkap|tagih-piutang|pembayaran] [--status semua] [--samarkan] [--ke file.csv]` → CSV untuk Excel (aman dari formula injection); default di folder data (`.../piutang/ekspor/`). Sebutkan path lengkapnya dan ingatkan bahwa file berisi data pribadi.
- `rekap [--periode bulan-ini|bulan-lalu|minggu-ini|...|semua | --dari .. --sampai ..] [--rumus] [--json]` → nota baru, pembayaran diterima, potongan, pembatalan, posisi per akhir periode + umur, status jatuh tempo hari ini, terlewat terbesar. "Rumusnya?" → `--rumus`.
- **laporan-harian-usaha**: versi saat ini belum membaca buku-piutang. `rekap --json` (kontrak `skema_json` 1, lihat `references/perintah.md`) disiapkan agar bisa dipakai bagian TAGIHAN laporan itu. Sampai didukung, jadwalkan `ringkasan` buku-piutang sendiri (Langkah F) di samping laporan harian; jangan mengubah skill laporan-harian-usaha.

### F. Ringkasan harian ke Telegram (OpenClaw)
Ikuti `references/openclaw-jadwal.md`: `ringkasan --samarkan` tiap pagi (default 07.45 WIB) ke **Telegram pemilik**. Jadwal hanya menjalankan perintah baca (`ringkasan`, `jatuh-tempo`, `rekap`), tidak pernah menulis atau mengirim ke pelanggan. Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal. Beri tahu pemilik bahwa tanpa `--samarkan` nama pelanggan dan nominal utangnya tersimpan di chat Telegram. WhatsApp hanya dengan nomor terpisah milik pemilik + persetujuan risiko tertulis. Claude Code/Codex/Cursor: pengguna cukup mengetik "ringkasan piutang" tiap pagi.

### G. Cadangan & hapus data
Cadangan otomatis sekali sehari saat ada perubahan (30 terakhir disimpan) dan sebelum setiap perubahan besar, di `backup-piutang/` sebelah database. Manual: `backup`; daftar: `backup --daftar`; pulihkan: `restore --dari <file>` (pratinjau → `--ya`) — bisa walau database rusak total; file rusak dipindah ke `backup-piutang/rusak-piutang-<waktu>.db`, tidak dihapus. Rusak dan belum ada cadangan: `init --mulai-baru` (pratinjau → `--ya`), lalu impor ulang dari ekspor CSV terakhir. Pelanggan minta datanya dihapus → `hapus-pelanggan` (hanya bila piutang & deposit sudah nol; sampaikan bahwa cadangan lama masih memuatnya).

## Format output ke pengguna
- Simpan/ubah: baris dari script apa adanya, mis. `Tercatat nota B-0901 untuk Warung Bu Tini (P0001): Rp 1.250.000 | tanggal 1 Sep 2026 | jatuh tempo Selasa, 15 September 2026 (14 hari)` + `Catatan:` bila ada.
- Daftar/umur/rekap: teks script apa adanya, lalu contoh balasan singkat ("bikinin pesan untuk P0002", "Kafe Senja bayar 1 juta").
- Rupiah `Rp 1.400.000`; persen `10,9%`; tanggal `Sabtu, 26 September 2026` atau `26 Sep 2026`.

## Contoh
**Input:** "Kafe Senja ambil gula & minyak 2,4 juta tanggal 5 September, tempo seminggu, nota B-0905. Tanggal 15 transfer 1 juta." (hari ini 26 Sep 2026)
**Proses:** `catat --pelanggan "Kafe Senja" --nota B-0905 --tanggal 05/09/2026 --termin 7 --nominal 2,4jt` lalu `bayar --pelanggan "Kafe Senja" --jumlah 1jt --tanggal 15/09/2026 --metode transfer`
**Output:**
```
Tercatat nota B-0905 untuk Kafe Senja (P0002, pelanggan baru): Rp 2.400.000 | tanggal 5 Sep 2026 | jatuh tempo Sabtu, 12 September 2026 (7 hari)
Pembayaran B0001 dicatat: Rp 1.000.000 dari Kafe Senja (P0002), 15 Sep 2026, transfer.
Dipakai untuk: B-0905 Rp 1.000.000 (sisa Rp 1.400.000).
```
"Bikinin pesan tagihannya" → `draf --pelanggan P0002`:
```
Halo Bapak/Ibu di Kafe Senja, semoga sehat selalu. Saya Sari dari Toko Sembako Berkah.

Kami ingin menanyakan tagihan berikut yang sudah melewati jatuh tempo:
- Nota B-0905 (5 Sep 2026): sisa Rp 1.400.000, jatuh tempo 12 Sep 2026

Pembayaran bisa ditransfer ke BCA 0000000000 a.n. Sari (contoh).
Mohon dibantu informasikan kapan rencana pembayarannya, supaya bisa kami catat. ...
https://wa.me/6281200002002?text=Halo%20Bapak%2FIbu...
```
Contoh sesi lengkap: `examples/contoh-sesi-toko-sembako.md`.

## Checklist sebelum menjawab
- [ ] Tidak ada pesan yang dikirim agent; draf ditandai "periksa lalu kirim sendiri".
- [ ] Angka, tanggal, persen dari script; `peringatan`/asumsi (termin, tanggal, nomor otomatis) disampaikan.
- [ ] Pelanggan ambigu/mirip dan kelebihan bayar ditanyakan, bukan ditebak.
- [ ] Perubahan besar sudah pratinjau + disetujui sebelum `--ya`.
- [ ] Yang dibagikan/dijadwalkan memakai `--samarkan`; tidak ada ancaman atau denda di draf.

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- Bukan aplikasi akuntansi lengkap (tidak ada jurnal, hutang ke pemasok, laba rugi) dan bukan pengganti faktur pajak Coretax. Tidak membaca mutasi bank otomatis; pembayaran dicatat dari cerita/bukti yang ditempel pemilik (cocokkan mutasi → `rekonsiliasi-bank`).
- Satu database dipakai satu komputer. Jangan buka file yang sama dari dua komputer lewat Google Drive/Dropbox.
- Database terkunci (mis. jadwal sedang membaca) → script menunggu 15 detik lalu memberi pesan jelas; ulangi perintahnya. Database rusak → script menolak dengan petunjuk `backup --daftar` + `restore`; jangan hapus atau timpa file database sendiri.
- Posisi `--per` tanggal lampau menghitung ulang dari transaksi bertanggal ≤ tanggal itu; nota yang sudah dibatalkan tidak ikut dihitung.
- Zona waktu mengikuti pengaturan (WIB default), bukan jam komputer/VPS; `info` memperingatkan bila berbeda.
- **Python tidak bisa dijalankan:** ikuti `references/tanpa-python.md` (tabel manual + rumus) dan beri tahu pengguna "dihitung manual, mohon dicek".
