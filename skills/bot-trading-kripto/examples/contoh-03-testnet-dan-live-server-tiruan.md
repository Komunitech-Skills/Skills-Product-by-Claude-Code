# Contoh 03 — Testnet & gerbang LIVE terhadap SERVER TIRUAN lokal

> **Label jujur:** semua order di contoh ini dikirim ke `tests/mock_bursa.py` (127.0.0.1), server tiruan yang meniru contoh respons di dokumentasi resmi Binance Spot. **Bukan** Binance testnet/live sungguhan: testnet.binance.vision menolak lokasi lingkungan uji (HTTP 451) dan kunci testnet butuh login GitHub pemilik. Kunci yang dipakai = contoh kunci publik dari dokumentasi Binance. Dijalankan pembuat skill 2026-09-29.

> **Catatan versi:** bagian A–C direkam pada versi 1.0.0. Mulai 1.0.1: flag `--kunci-tanpa-withdraw` diganti
> `--saya-sudah-cek-tanpa-withdraw` (daftar periksa wajib), live butuh bukti paper harga asli ≥ 3 putaran/≥ 24 jam,
> PPh 1% juga dipotong di sisi beli pasangan kripto-kripto (BTCUSDT), dan redirect tidak diikuti. Keluaran versi
> 1.0.1 ada di **bagian D** (angka A–C untuk BTCUSDT tidak lagi sama).

## A. Testnet Binance (server tiruan), strategi rebalancing 50%
```
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan>
Bot kripto [TESTNET - uang mainan] BTCUSDT
BELI 0.00332667 BTC @ 60000 USDT | bayar 199.8 USDT (fee 0.1998 USDT)
  Aturan Anda: rebalancing: porsi koin 0% < target 50%
Ringkasan bot: kas 800.2 USDT, koin 0.00332667 BTC, nilai total 999.8002 USDT (harga 60000 USDT), untung/rugi terealisasi 0 USDT.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 2]

# (harga tiruan dinaikkan ke 70000)
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan>
Bot kripto [TESTNET - uang mainan] BTCUSDT
BELI 0.00284715 BTC @ 70000 USDT | bayar 199.5 USDT (fee 0.1995 USDT)
  Aturan Anda: rebalancing: porsi koin 22.54% < target 50%
Ringkasan bot: kas 600.7 USDT, koin 0.00617382 BTC, nilai total 1032.8674 USDT (harga 70000 USDT), untung/rugi terealisasi 0 USDT.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 2]

```
Urutan permintaan yang diterima server tiruan (semua bertanda tangan HMAC-SHA256 diverifikasi server):
`GET /api/v3/time, GET /api/v3/account, GET /api/v3/exchangeInfo, GET /api/v3/ticker/price, GET /api/v3/openOrders, POST /api/v3/order, GET /api/v3/time, GET /api/v3/exchangeInfo, GET /api/v3/ticker/price, GET /api/v3/openOrders, POST /api/v3/order`

Kunci/secret muncul di audit.jsonl/state.json/transaksi.csv? **tidak**

## B. Gerbang live bertahap (server tiruan)
```
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan> --izinkan-live
Bot kripto [LIVE - UANG ASLI] BTCUSDT
Mode live ditolak: aturan yang SAMA persis belum pernah dijalankan di mode simulasi (paper). Jalankan dulu dengan "mode": "paper" minimal satu putaran, lalu siapkan live lagi.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 3]

# (member menjalankan aturan yang sama di mode paper dulu)
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan>
Bot kripto [SIMULASI - bukan uang asli] BTCUSDT
BELI 0.00285 BTC @ 70000 USDT | bayar 199.6995 USDT (fee 0.1995 USDT)
  Aturan Anda: rebalancing: porsi koin 0% < target 50%
Ringkasan bot: kas 800.3005 USDT, koin 0.00285 BTC, nilai total 999.8005 USDT (harga 70000 USDT), untung/rugi terealisasi 0 USDT.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 2]

$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json
=== PERSIAPAN MODE LIVE (UANG ASLI) ===
Bursa: binance | pasangan: BTCUSDT | strategi: rebalancing
Aturan strategi (milik Anda): {"target_persen_koin": "50", "ambang_deviasi_persen": "5"}
Batas modal per order: 200 USDT
Batas modal total: 1000 USDT
Stop-loss global: 20% di bawah harga rata-rata -> jual semua & berhenti
Batas rugi harian: 100 USDT -> berhenti
Order terbuka maks: 2
Fee dipakai: 0.1% | PPh jual: 1% (PMK 50/2025 (berlaku 1 Agustus 2025): PPh 22 final 0,21% (PAKD dalam negeri) / 1% (platform luar negeri) dari nilai jual, dipungut dari penjual. Dicek 2026-09-29 di pajak.go.id. Pembulatan belum dicocokkan dengan Coretax.)
Order yang dipakai: MARKET (harga saat eksekusi bisa berbeda dari harga terakhir).

Bukti simulasi aturan yang sama: 1 putaran paper.

Kode konfirmasi: e81352e23aff
Agar live aktif, MEMBER SENDIRI harus mengetik persis kalimat ini di chat:
  LIVE e81352e23aff SAYA TANGGUNG RISIKONYA
dan menyatakan bahwa API key TIDAK punya izin withdraw (tarik dana).

# (kunci tiruan diset PUNYA izin withdraw)
$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json --cek-kunci --url-uji <server-tiruan>
Kunci DITOLAK: kunci PUNYA izin withdraw (tarik dana) -- WAJIB dimatikan
Buat kunci baru dengan izin HANYA trading spot (tanpa withdraw), lalu ulangi.
[kode keluar 2]

# (member membuat kunci baru tanpa withdraw)
$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json --cek-kunci --url-uji <server-tiruan>
Kunci terbaca (isi tidak ditampilkan). Izin diperiksa otomatis: tanpa withdraw, spot trading aktif.
Disarankan batasi IP kunci ke IP mesin bot.
[kode keluar 0]

# (member mengetik frasa dengan kode salah)
$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json --frasa LIVE 123456789abc SAYA TANGGUNG RISIKONYA --kunci-tanpa-withdraw
Ditolak: frasa tidak persis sama (kode mungkin berubah karena konfigurasi diubah). Jalankan langkah 1 lagi.
[kode keluar 2]

# (member mengetik frasa persis + menyatakan kunci tanpa withdraw)
$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json --frasa LIVE e81352e23aff SAYA TANGGUNG RISIKONYA --kunci-tanpa-withdraw
Konfirmasi live tersimpan (kode e81352e23aff). Jadwal/perintah live wajib memakai --izinkan-live.
[kode keluar 0]

# (jadwal lupa memuat --izinkan-live)
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan>
Bot kripto [LIVE - UANG ASLI] BTCUSDT
Mode live ditolak: perintah tidak memuat --izinkan-live.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 3]

$ python3 scripts/berhenti.py --konfigurasi bot/konfigurasi.json --lanjutkan --saya-sudah-cek
Bot dilanjutkan. Alasan berhenti sebelumnya: Mode live dipanggil tanpa --izinkan-live.. Batas rugi harian dihitung ulang dari sekarang.
[kode keluar 0]

$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan> --izinkan-live
Bot kripto [LIVE - UANG ASLI] BTCUSDT
BELI 0.00284715 BTC @ 70000 USDT | bayar 199.5 USDT (fee 0.1995 USDT)
  Aturan Anda: rebalancing: porsi koin 0% < target 50%
Ringkasan bot: kas 800.5 USDT, koin 0.00284715 BTC, nilai total 999.8005 USDT (harga 70000 USDT), untung/rugi terealisasi 0 USDT.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 2]

```
## C. Tombol berhenti + status order tidak pasti
```
$ python3 scripts/berhenti.py --konfigurasi bot/konfigurasi.json --batalkan-order --url-uji <server-tiruan>
Tombol berhenti AKTIF (file STOP dibuat). Bot tidak akan membuat order baru mulai putaran berikutnya.
Order terbuka yang dibatalkan: 1.
Koin yang sudah dibeli bot TIDAK dijual otomatis. Cek posisi di aplikasi bursa.
[kode keluar 0]

$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan> --izinkan-live --openclaw
Bot kripto [LIVE - UANG ASLI] BTCUSDT
BOT BERHENTI. Alasan: Tombol berhenti (file STOP) aktif.
Tidak ada order baru. Untuk melanjutkan, tinjau dulu lalu minta agen menjalankan berhenti.py --lanjutkan.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 0]

$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan> --izinkan-live --openclaw
NO_REPLY
[kode keluar 0]

$ python3 scripts/berhenti.py --konfigurasi bot/konfigurasi.json --lanjutkan --saya-sudah-cek
Bot dilanjutkan. Alasan berhenti sebelumnya: Tombol berhenti (file STOP) aktif.. Batas rugi harian dihitung ulang dari sekarang.
[kode keluar 0]

# (server tiruan memutus koneksi saat menerima order; harga naik -> aturan rebalancing ingin menjual)
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan> --izinkan-live
Bot kripto [LIVE - UANG ASLI] BTCUSDT
BOT BERHENTI. Alasan: STATUS ORDER TIDAK PASTI: Tidak ada jawaban bursa saat mengirim order (RemoteDisconnected). Order MUNGKIN sudah masuk -- cek manual di aplikasi bursa.
Tidak ada order baru sampai Anda meninjau dan melanjutkan (berhenti.py --lanjutkan).
Ringkasan bot: kas 800.5 USDT, koin 0.00284715 BTC, nilai total 1056.7435 USDT (harga 90000 USDT), untung/rugi terealisasi 0 USDT.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 3]

```

## D. Versi 1.0.1 — daftar periksa withdraw, bukti paper, PPh sisi beli, redirect (server tiruan)
Direkam pembuat 2026-09-29 (revisi 1.0.1). Home diarahkan ke folder sementara; kunci = contoh publik docs Binance; secret dicari di semua keluaran & file bot: **tidak ada**.
```
$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan>
Bot kripto [SIMULASI - bukan uang asli] BTCUSDT
BELI 0.00329 BTC @ 60000 USDT | bayar 199.5714 USDT (fee 0.1974 USDT, PPh 1.974 USDT)
  Aturan Anda: rebalancing: porsi koin 0% < target 50%
Ringkasan bot: kas 800.4286 USDT, koin 0.00329 BTC, nilai total 997.8286 USDT (harga 60000 USDT), untung/rugi terealisasi 0 USDT.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 2]

$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json
=== PERSIAPAN MODE LIVE (UANG ASLI) ===
Bursa: binance | pasangan: BTCUSDT | strategi: rebalancing
Aturan strategi (milik Anda): {"target_persen_koin": "50", "ambang_deviasi_persen": "5"}
Batas modal per order: 200 USDT
Batas modal total: 1000 USDT
Stop-loss global: 20% di bawah harga rata-rata -> jual semua & berhenti
Batas rugi harian: 100 USDT -> berhenti
Order terbuka maks: 2
Fee dipakai: 0.1% | PPh jual: 1% | PPh beli (swap kripto-kripto): 1% (PMK 50/2025 (berlaku 1 Agustus 2025): PPh 22 final 0,21% (PAKD dalam negeri) / 1% (platform luar negeri) dari nilai transaksi. Pasangan rupiah: dipungut dari penjual. Pasangan kripto-kripto (mis. BTCUSDT) = tukar-menukar (swap): PPh atas nilai MASING-MASING aset yang diserahkan, jadi sisi beli juga kena (Pasal 11 ayat (2) huruf b, Pasal 12 ayat (5) huruf b). Dicek 2026-09-29 di teks resmi JDIH Kemenkeu. Pembulatan belum dicocokkan dengan Coretax.)
Order yang dipakai: MARKET (harga saat eksekusi bisa berbeda dari harga terakhir).

Bukti simulasi aturan yang sama: 0 putaran paper dengan harga asli selama 0.0 jam (syarat: minimal 3 putaran dalam rentang minimal 24 jam). BELUM CUKUP -> biarkan jadwal paper berjalan dulu. Live belum bisa aktif.

DAFTAR PERIKSA WAJIB (dikerjakan MEMBER SENDIRI di layar binance, bukan oleh agent):
  [ ] 1. Login ke binance.com, buka API Management.
  [ ] 2. Pastikan 'Enable Withdrawals' TIDAK dicentang; aktifkan hanya 'Enable Reading' dan 'Enable Spot & Margin Trading'.
  [ ] 3. Margin, futures, universal transfer TIDAK aktif; batasi IP ke IP mesin bot bila bisa.
  [ ] 4. Bot juga memeriksa ini otomatis (endpoint baca-saja apiRestrictions) dan menolak kunci ber-withdraw.

Kode konfirmasi: e81352e23aff
Agar live aktif, MEMBER SENDIRI harus mengetik persis kalimat ini di chat:
  LIVE e81352e23aff SAYA TANGGUNG RISIKONYA
dan menyatakan sudah menyelesaikan SEMUA butir daftar periksa di atas (izin withdraw MATI).
[kode keluar 2]

# (penguji menyuntik bukti 3 putaran paper harga asli selama 25 jam ke state.json -- uji tidak menunggu 24 jam)

$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json
=== PERSIAPAN MODE LIVE (UANG ASLI) ===
Bursa: binance | pasangan: BTCUSDT | strategi: rebalancing
Aturan strategi (milik Anda): {"target_persen_koin": "50", "ambang_deviasi_persen": "5"}
Batas modal per order: 200 USDT
Batas modal total: 1000 USDT
Stop-loss global: 20% di bawah harga rata-rata -> jual semua & berhenti
Batas rugi harian: 100 USDT -> berhenti
Order terbuka maks: 2
Fee dipakai: 0.1% | PPh jual: 1% | PPh beli (swap kripto-kripto): 1% (PMK 50/2025 (berlaku 1 Agustus 2025): PPh 22 final 0,21% (PAKD dalam negeri) / 1% (platform luar negeri) dari nilai transaksi. Pasangan rupiah: dipungut dari penjual. Pasangan kripto-kripto (mis. BTCUSDT) = tukar-menukar (swap): PPh atas nilai MASING-MASING aset yang diserahkan, jadi sisi beli juga kena (Pasal 11 ayat (2) huruf b, Pasal 12 ayat (5) huruf b). Dicek 2026-09-29 di teks resmi JDIH Kemenkeu. Pembulatan belum dicocokkan dengan Coretax.)
Order yang dipakai: MARKET (harga saat eksekusi bisa berbeda dari harga terakhir).

Bukti simulasi aturan yang sama: 3 putaran paper dengan harga asli selama 25.0 jam (syarat: minimal 3 putaran dalam rentang minimal 24 jam).

DAFTAR PERIKSA WAJIB (dikerjakan MEMBER SENDIRI di layar binance, bukan oleh agent):
  [ ] 1. Login ke binance.com, buka API Management.
  [ ] 2. Pastikan 'Enable Withdrawals' TIDAK dicentang; aktifkan hanya 'Enable Reading' dan 'Enable Spot & Margin Trading'.
  [ ] 3. Margin, futures, universal transfer TIDAK aktif; batasi IP ke IP mesin bot bila bisa.
  [ ] 4. Bot juga memeriksa ini otomatis (endpoint baca-saja apiRestrictions) dan menolak kunci ber-withdraw.

Kode konfirmasi: e81352e23aff
Agar live aktif, MEMBER SENDIRI harus mengetik persis kalimat ini di chat:
  LIVE e81352e23aff SAYA TANGGUNG RISIKONYA
dan menyatakan sudah menyelesaikan SEMUA butir daftar periksa di atas (izin withdraw MATI).
[kode keluar 0]

$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json --frasa "LIVE e81352e23aff SAYA TANGGUNG RISIKONYA"
Ditolak: daftar periksa izin withdraw belum dinyatakan selesai oleh member (--saya-sudah-cek-tanpa-withdraw). Daftar periksa:
  [ ] 1. Login ke binance.com, buka API Management.
  [ ] 2. Pastikan 'Enable Withdrawals' TIDAK dicentang; aktifkan hanya 'Enable Reading' dan 'Enable Spot & Margin Trading'.
  [ ] 3. Margin, futures, universal transfer TIDAK aktif; batasi IP ke IP mesin bot bila bisa.
  [ ] 4. Bot juga memeriksa ini otomatis (endpoint baca-saja apiRestrictions) dan menolak kunci ber-withdraw.
[kode keluar 2]

$ python3 scripts/siapkan_live.py --konfigurasi bot/konfigurasi.json --frasa "LIVE e81352e23aff SAYA TANGGUNG RISIKONYA" --saya-sudah-cek-tanpa-withdraw
Konfirmasi live tersimpan (kode e81352e23aff). Jadwal/perintah live wajib memakai --izinkan-live.
[kode keluar 0]

$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan> --izinkan-live
Bot kripto [LIVE - UANG ASLI] BTCUSDT
BELI 0.0032967 BTC @ 60000 USDT | bayar 199.98 USDT (fee 0.198 USDT, PPh 1.98 USDT)
  Aturan Anda: rebalancing: porsi koin 0% < target 50%
Ringkasan bot: kas 800.02 USDT, koin 0.0032967 BTC, nilai total 997.822 USDT (harga 60000 USDT), untung/rugi terealisasi 0 USDT.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 2]

# (server tiruan kini menjawab semua permintaan dengan 302 ke host lain)

$ python3 scripts/jalankan_bot.py --konfigurasi bot/konfigurasi.json --url-uji <server-tiruan> --izinkan-live
Bot kripto [LIVE - UANG ASLI] BTCUSDT
Tidak bisa mengambil data bursa: Bursa mengalihkan permintaan (HTTP 302) dari 127.0.0.1 ke localhost. Demi keamanan, pengalihan ke host lain tidak diikuti. Kemungkinan situs sedang maintenance/butuh login atau alamat API berubah; cek pengumuman bursa. Tidak ada order dijalankan putaran ini.

Bot ini hanya menjalankan aturan yang ANDA tetapkan. Bukan nasihat investasi, bukan sinyal, tanpa jaminan untung. Aset kripto berisiko tinggi; Anda bisa kehilangan seluruh modal. Keputusan & risiko sepenuhnya milik Anda.
[kode keluar 2]
```
