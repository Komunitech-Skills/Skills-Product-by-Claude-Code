# Sumber data harga (publik, tanpa API key)

Diverifikasi lewat `curl` sungguhan pada 2026-09-24 (bukan hanya dibaca dari dokumentasi).
Kalau salah satu sumber berubah format/berhenti gratis di kemudian hari, `cek_ambang.py`
akan gagal untuk sumber itu dan tetap melapor jujur (lihat penanganan "sumber gagal" di
`SKILL.md`) -- tidak pernah mengarang angka sebagai gantinya.

## 1. CoinGecko `simple/price`
- Dokumentasi resmi: https://docs.coingecko.com/reference/simple-price
- Endpoint: `https://api.coingecko.com/api/v3/simple/price`
- Contoh permintaan (dijalankan sungguhan):
  ```
  GET https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd,idr&include_24hr_change=true&include_last_updated_at=true
  ```
- Contoh respons nyata (dipotong):
  ```json
  {"bitcoin":{"usd":84364,"usd_24h_change":-2.4579829146579724,"idr":1504614412,
    "idr_24h_change":-2.415759695487968,"last_updated_at":1790209410},
   "ethereum":{"usd":2686.37,"usd_24h_change":-2.664466860385994,"idr":47910861,
    "idr_24h_change":-2.6223330223581622,"last_updated_at":1790209410}}
  ```
- **Tanpa API key** untuk tingkat gratis (Demo/Public API), tapi **ada batas laju
  permintaan** (rate limit) yang bisa berubah sewaktu-waktu dan tidak dijamin publik
  angka pastinya -- karena itu `cek_ambang.py` memakai timeout + percobaan ulang
  terbatas, bukan polling sangat sering. Untuk automation berkala (mis. tiap jam), ini
  jauh di bawah batas wajar.
- `ids` memakai **id CoinGecko** (bukan kode ticker), mis. `bitcoin` untuk BTC, `ethereum`
  untuk ETH, `solana` untuk SOL. Cari id yang benar di halaman koin di coingecko.com
  (bagian URL) sebelum menulis `konfigurasi.json` -- id yang salah bikin API tidak
  mengembalikan data sama sekali untuk koin itu (jadi "sumber gagal", bukan galat diam).
- `include_24hr_change=true` memberi field `<mata_uang>_24h_change` -- inilah yang dipakai
  `cek_ambang.py` sebagai dasar ambang persen kalau member **tidak** mengisi `harga_acuan`
  sendiri di `PANTAU.md`.
- `last_updated_at` adalah unix timestamp (UTC) kapan CoinGecko terakhir memperbarui harga
  itu -- dipakai script untuk menghitung `usia_data_jam` dan `jam_data` (dikonversi ke
  WIB).

## 2. Indodax `ticker/<pair>` (opsional, harga pasar lokal Rupiah)
- Dokumentasi resmi (repo GitHub Indodax):
  https://github.com/btcid/indodax-official-api-docs/blob/master/Public-REST-API.md
- Endpoint: `https://indodax.com/api/ticker/<pair>`, mis. `btcidr`, `ethidr`.
- Contoh permintaan & respons nyata:
  ```
  GET https://indodax.com/api/ticker/btcidr
  {"ticker":{"buy":"1506509000","high":"1550001000","last":"1506510000","low":"1491453000",
    "sell":"1506510000","server_time":1790209499,"vol_btc":"34.50828039","vol_idr":"52561459230"}}
  ```
- **Tanpa API key** untuk endpoint publik ini (harga saja, bukan trading).
- **Tidak menyediakan persentase perubahan 24 jam** di endpoint ini (tidak ada field
  "open"/harga 24 jam lalu) -- karena itu kalau `sumber: indodax` dipakai TANPA
  `harga_acuan` yang diisi member, `cek_ambang.py` tidak bisa menghitung ambang persen
  (hanya ambang harga absolut yang tetap bisa dicek). Ini disebutkan jelas ke member lewat
  field `peringatan`/`detail_pemicu`, bukan didiamkan.
- `server_time` (unix timestamp, UTC) dipakai sebagai `jam_data`.
- Cocok dipakai sebagai "harga pasar lokal Indodax" pembanding di ringkasan pagi, di
  samping harga CoinGecko (yang lebih ke harga pasar global).

## 3. Kalau kedua sumber di atas berubah/berhenti
`cek_ambang.py` tidak punya sumber cadangan pihak ketiga bawaan (menghindari menambah
dependensi paket luar standar Python). Kalau salah satu URL berubah format:
1. Cek ulang dokumentasi resmi di atas (URL bisa berubah seiring waktu).
2. Kalau format respons berubah, `_ambil_url_json`/`ambil_harga_coingecko`/
   `ambil_harga_indodax` di `cek_ambang.py` perlu disesuaikan -- fungsi-fungsi itu
   sengaja dipisah supaya mudah ditambal tanpa mengubah logika ambang/state.
3. Sambil menunggu perbaikan, gunakan mode `--harga-file` untuk tetap bisa menghitung
   ambang dari harga yang dimasukkan manual oleh member.
