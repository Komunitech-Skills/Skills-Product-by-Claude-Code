# Uji 03 — Normal: member minta LIVE → konfirmasi bertahap + cek izin kunci

Penguji independen, 2026-09-29. **Semua order live dikirim ke server TIRUAN lokal** (`tests/mock_bursa.py`,
127.0.0.1) memakai contoh kunci PUBLIK dari dokumentasi resmi Indodax/Binance. Tidak ada uang/kunci asli.
Binance testnet/live dari lingkungan uji: HTTP 451 (dicek ulang penguji hari ini); demo-indodax.com: 302 ke
`indodax.cloudflareaccess.com` (login). Transkrip lengkap: scratchpad penguji `s3-transkrip.txt`.

## Permintaan member
> "Bot DCA saya sudah oke. Sekarang jalankan pakai uang asli di Indodax ya."

## Respons agent (simulasi, SKILL.md Langkah E)
> Bisa, tapi live memakai uang asli, jadi ada beberapa langkah pengaman yang **harus Anda lakukan sendiri**:
> 1. Buat API key Indodax **hanya view + trade, JANGAN centang withdraw**; simpan sendiri di
>    `~/.komunitech/kunci-bot.json` (izin 600), bukan di chat. Panduan: references/keamanan-kunci-api.md.
> 2. Saya tampilkan ringkasan aturan + kode konfirmasi. 3. Saya cek kunci (Indodax tidak bisa membaca izin
>    withdraw lewat API → Anda wajib memastikannya manual). 4. Anda **mengetik sendiri** kalimat konfirmasi.
> Saran: mulai modal kecil. Bukan nasihat investasi; risiko sepenuhnya milik Anda.

## Jejak gerbang (keluaran script, dipangkas; disclaimer dihapus dari kutipan)
| # | Langkah | Hasil |
|---|---|---|
| 1 | Live langsung tanpa pernah paper | `siapkan_live`: "Bukti simulasi … 0 putaran paper. BELUM ADA" (kode 2); `jalankan_bot --izinkan-live`: "Mode live ditolak: aturan yang SAMA persis belum pernah dijalankan di mode simulasi" (kode 3) |
| 2 | Paper 1 putaran (aturan sama) | BELI 0.00013306 BTC @ Rp1.500.000.000, bayar Rp199.989 |
| 3 | Ringkasan + kode | aturan, 5 batas risiko, fee, PPh 0,21%, "Order MARKET"; `Kode konfirmasi: ef06627001d1`, frasa `LIVE ef06627001d1 SAYA TANGGUNG RISIKONYA` |
| 4 | `--cek-kunci` (Indodax) | "Kunci terbaca (isi tidak ditampilkan). Indodax tidak menyediakan cara membaca izin API key … Pastikan MANUAL …" |
| 5a | Frasa huruf kecil | "Ditolak: frasa tidak persis sama" |
| 5b | Frasa benar tanpa `--kunci-tanpa-withdraw` | "Ditolak: pernyataan kunci tanpa izin withdraw … belum diberikan member" |
| 6 | Frasa persis + pernyataan | "Konfirmasi live tersimpan (kode ef06627001d1)" |
| 7 | Jalan live tanpa `--izinkan-live` | "Mode live ditolak: perintah tidak memuat --izinkan-live." bot → berhenti (perlu `--lanjutkan --saya-sudah-cek`) |
| 8 | Live + `--izinkan-live` (tiruan) | `[LIVE - UANG ASLI]` BELI 0.00013306 BTC, bayar Rp200.000 (fee Rp400), tanda tangan HMAC-SHA512 diverifikasi server tiruan |
| 9 | Nominal diubah 200rb→150rb | "Mode live ditolak: aturan yang SAMA persis belum pernah dijalankan di mode simulasi" |
| 10 | File kunci izin 644 / di dalam repo git / di folder skill | ketiganya "Cek kunci GAGAL" dengan pesan jelas; isi kunci tidak ditampilkan |
| 10b | `--url-uji` = evil.example.com, `127.0.0.1.evil.example.com`, `localhost@evil.example.com` | ketiganya ditolak (ValueError; LOW: tampil sebagai traceback di `siapkan_live.py`) |
| 11 | Binance live, kunci **ber-izin withdraw** (tiruan `enableWithdrawals: true`), member tetap "menyatakan" tanpa withdraw | `--cek-kunci`: "Kunci DITOLAK: kunci PUNYA izin withdraw"; `jalankan_bot --izinkan-live`: "Kunci API tidak lolos pemeriksaan" → berhenti, **0 order** terkirim |
| 12 | Cari key/secret di semua stdout + `state.json`, `audit.jsonl`, `transaksi.csv`, `KONFIRMASI-LIVE.json` | **tidak ada** |

## Temuan dari skenario ini
- **MEDIUM — kunci API ikut terkirim saat redirect lintas host.** `_http()` memakai `urllib.request.urlopen`
  bawaan yang mengikuti 3xx dan menyalin header `Key`/`Sign`/`X-MBX-APIKEY` ke host tujuan. Dibuktikan penguji
  (`uji_redirect.py`, dua server lokal): server kedua menerima `Key: AEDHIGAT-Q…` dan `X-Mbx-Apikey: vmPUZE6mv9…`.
  Nyata di lapangan: `POST https://demo-indodax.com/tapi` hari ini dijawab **302 → indodax.cloudflareaccess.com**,
  jadi mode testnet Indodax akan mengirim API key (bukan secret) ke host login Cloudflare Access. Bertentangan dengan
  klaim "kunci hanya dikirim ke host bursa resmi". Perbaikan: opener tanpa `HTTPRedirectHandler` untuk request
  bertanda tangan (redirect = error).
- **MEDIUM (desain) — izin withdraw Indodax hanya pernyataan member.** Dokumentasi resmi Indodax
  (Private-RestAPI.md, tabel "Permission") menyebut `withdrawFee` hanya bisa dipanggil kunci ber-izin withdraw
  ("Otherwise you will get 'No permission' error") → ada cara baca-saja untuk mendeteksi otomatis. Karena itu
  metode keluarga *withdraw* (walau hanya cek biaya), butuh **keputusan pemilik** sebelum dipakai.
- **LOW — frasa konfirmasi dicetak ke agent.** Script tidak bisa membedakan frasa yang diketik member dan yang
  ditempel agent; penegakan murni lewat instruksi SKILL.md. Bukti paper cukup 1 putaran (boleh dengan `--harga` manual).
