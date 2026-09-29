# Membuat & menyimpan API key dengan aman (dikerjakan MEMBER sendiri)

> Agent **tidak** membuat, membaca, menampilkan, atau menyalin kunci. Agent hanya
> menunjukkan panduan ini. Kalau kunci/secret pernah ditempel ke chat mana pun, anggap bocor:
> **cabut (revoke) sekarang** di bursa, lalu buat yang baru.

## Aturan emas
1. **Izin: hanya "trade" (dan "view/baca").** **JANGAN** centang *withdraw / tarik dana /
   transfer*. Dengan begitu, jika kunci bocor, pencuri tidak bisa memindahkan dana keluar.
2. **Batasi IP** bila bursa menyediakan (isi IP publik mesin bot). Binance mendukung ini.
3. **Satu kunci untuk satu bot.** Mudah dicabut tanpa mengganggu yang lain.
4. **Simpan di luar folder skill & di luar folder repo git**, mis. `~/.komunitech/kunci-bot.json`
   (Windows: `C:\Users\<nama>\.komunitech\kunci-bot.json`). Script **menolak** file kunci yang
   berada di dalam folder skill atau di dalam repo git.
5. **Izin file 600** (macOS/Linux): `chmod 600 ~/.komunitech/kunci-bot.json`. Script menolak
   file yang bisa dibaca pengguna lain. (Windows: pastikan folder hanya bisa diakses akun Anda.)

## Format file kunci
Salin `templates/kunci-contoh.json` ke lokasi di atas, lalu **Anda sendiri** menempelkan isinya
dengan editor teks (bukan lewat chat):
```json
{"api_key": "…", "api_secret": "…"}
```
Lalu di `bot/konfigurasi.json`: `"kunci": {"file": "~/.komunitech/kunci-bot.json"}`.

Alternatif: variabel lingkungan yang Anda set sendiri di mesin bot:
`KOMUNITECH_BOT_API_KEY` dan `KOMUNITECH_BOT_API_SECRET`, lalu `"kunci": {"env": true}`.

## Indodax (PAKD berizin OJK — cek ulang daftar di ojk.go.id)
- Buat kunci di menu pengaturan API Trade di akun Indodax (nama menu dapat berubah; ikuti
  tampilan terbaru). Pilih izin **view + trade saja**, jangan withdraw.
- **Penting:** API Indodax tidak menyediakan cara membaca izin kunci, jadi bot **tidak bisa
  memeriksa otomatis** apakah withdraw dimatikan. Anda wajib memastikannya sendiri; pernyataan
  Anda dicatat di `bot/KONFIRMASI-LIVE.json`.
- Demo/latihan: dokumentasi resmi Indodax menyebut **demo-indodax.com** (saldo demo, tidak bisa
  ditarik). Status di skill ini: **belum teruji** (situs demo meminta login saat diuji
  2026-09-29). Kunci demo dibuat di situs demo, bukan di akun asli.
- Sumber: https://github.com/btcid/indodax-official-api-docs (Private-RestAPI.md)

## Binance Spot Testnet (latihan, uang mainan)
- Buka https://testnet.binance.vision → login dengan akun GitHub → "Generate HMAC_SHA256 Key".
  Secret hanya tampil sekali; simpan langsung ke file kunci Anda.
- Testnet tidak punya endpoint izin kunci; dana testnet bukan uang asli.
- Binance dapat memblokir akses dari lokasi tertentu (HTTP 451). Kalau itu terjadi di mesin
  Anda, testnet Binance tidak bisa dipakai dari sana.

## Binance live (tidak disarankan untuk member Indonesia)
- Binance global tidak tercantum di daftar PAKD berizin OJK (cek ojk.go.id); PPh 1% dan bila
  platform tidak ditunjuk DJP, Anda menyetor sendiri. Bot mewajibkan
  `"saya_paham_binance_bukan_pakd_ojk": true` bila tetap dipilih.
- Bot memeriksa izin lewat `GET /sapi/v1/account/apiRestrictions` dan **menolak** kunci yang
  `enableWithdrawals: true`, tidak punya izin spot, atau punya izin margin/futures/transfer.

## Kalau curiga kunci bocor
1. Jalankan tombol berhenti: `python3 scripts/berhenti.py --konfigurasi bot/konfigurasi.json --batalkan-order`
2. Cabut kunci di bursa. 3. Periksa riwayat transaksi di aplikasi bursa. 4. Buat kunci baru.
