# Riset sumber: bot trading kripto (untuk skill `bot-trading-kripto`) — 2026-09-29

Dasar: keputusan pemilik 2026-09-29 (CLAUDE.md §1, jalur 3 "Kripto"): auto-trading
diizinkan dengan aturan milik member sendiri, default simulasi/paper & testnet, API key
tanpa izin tarik dana, batas risiko wajib, disclaimer; tanpa sinyal/rekomendasi & tanpa
janji profit.

Status: **T** = dicek langsung (API/file resmi dibaca atau endpoint dipanggil sungguhan
pada tanggal ini). **L** = dari pemberitaan/rangkuman pihak ketiga. **S** = terdokumentasi
tapi belum bisa diuji dari lingkungan kurator.

## 1. Proyek open-source bersumber kuat (dicek lewat GitHub API, 2026-09-29)

| Proyek | URL | Bintang | Fork | Lisensi (file LICENSE dibaca) | Dirawat? | Catatan |
|---|---|---|---|---|---|---|
| Freqtrade | https://github.com/freqtrade/freqtrade | 54.907 | 11.374 | **GPL-3.0** (T) | Ya, push hari ini; sejak 2017 | Bot lengkap: backtest, dry-run, Telegram, hyperopt. Butuh instalasi (pip/Docker, TA-Lib, pandas). |
| ccxt | https://github.com/ccxt/ccxt | 44.206 | 8.877 | **MIT** (T) | Ya | Pustaka API terpadu >100 bursa (termasuk Indodax, Tokocrypto). Butuh `pip install`. |
| Hummingbot | https://github.com/hummingbot/hummingbot | 20.259 | 4.971 | **Apache-2.0** (T) | Ya | Fokus market making/HFT; berat (Docker/conda). |
| Jesse | https://github.com/jesse-ai/jesse | 8.595 | 1.249 | **MIT** (T) | Ya | Framework riset & backtest; butuh Postgres/Redis. |
| OctoBot | https://github.com/Drakkar-Software/OctoBot | 6.662 | 1.282 | **GPL-3.0** (T) | Ya | Grid/DCA dengan UI; berat. |
| Superalgos | https://github.com/Superalgos/Superalgos | 5.668 | 6.019 | Apache-2.0 (dari metadata, tidak dibaca) | Ya | Node.js, visual, berat. |

Semua lolos ≥3 sinyal bukti (bintang, umur >5 tahun, komunitas/fork, perawatan aktif).

## 2. Keputusan arsitektur: **runner tipis Python standar buatan sendiri** (bukan wrapper Freqtrade)

Alasan:
1. **Prinsip "tanpa setup" CLAUDE.md**: Freqtrade/Hummingbot/Jesse/OctoBot semuanya butuh
   instalasi paket (pandas, TA-Lib, Docker, database). Mayoritas member awam; skill
   harus jalan dengan Python standar saja.
2. **Cakupan yang dibutuhkan kecil & tertutup**: hanya 4 aturan milik member (DCA,
   grid, TP/SL, rebalancing) + batas risiko. Tidak butuh indikator teknikal (yang justru
   mendorong ke arah "sinyal").
3. **Lisensi bersih**: tidak ada satu baris pun kode Freqtrade/OctoBot (GPL-3.0) yang
   disalin atau dibaca untuk ditiru, jadi hasil tetap **Proprietary Komunitech**. ccxt
   (MIT) juga tidak dipakai/disalin; adapter bursa ditulis dari **dokumentasi API resmi
   bursa** (Binance spot docs, Indodax official API docs).
4. **Keamanan lebih mudah diaudit**: ±2.000 baris stdlib yang bisa dibaca utuh, tanpa
   dependensi pihak ketiga (Tahap 3).
5. **Jalur lanjutan**: untuk member teknis yang ingin indikator/hyperopt, skill hanya
   **merujuk** ke Freqtrade sebagai program terpisah yang dipasang sendiri oleh member dari
   situs resminya (tidak dibundel, tidak disalin) — lihat
   `skills/bot-trading-kripto/references/jalur-lanjutan-freqtrade.md`.

## 3. Bursa: API & testnet (dicek 2026-09-29)

| Bursa | Status Indonesia | API trading | Testnet/demo | Hasil uji dari lingkungan kurator |
|---|---|---|---|---|
| **Indodax** (PT Indodax Nasional Indonesia) | PAKD berizin OJK (daftar per Mei 2026, **L** — cek ulang ojk.go.id) | Private REST `POST https://indodax.com/tapi`, header `Key` + `Sign` = HMAC-SHA512(body, secret), `timestamp`+`recvWindow` (T, docs resmi https://github.com/btcid/indodax-official-api-docs) | **demo-indodax.com** (disebut di docs resmi: saldo demo otomatis ~1 menit setelah daftar, tidak bisa ditarik) | Publik **T**: `/api/ticker/btcidr`, `/api/pairs`, `/api/server_time`, `/tradingview/history_v2` merespons data nyata. demo-indodax.com **S**: terhalang Cloudflare Access (302 ke login) dari lingkungan uji (IP AS). getInfo **tidak** menampilkan izin API key → izin withdraw tidak bisa dicek otomatis. Contoh tanda tangan di docs (getInfo) dicocokkan: HMAC hasil Python = `bab004e5…ae99` (sama dengan docs, T). |
| **Binance Spot Testnet** | Binance global **tidak** ada di daftar PAKD berizin OJK (L) — dipakai di skill ini untuk latihan testnet | REST `https://testnet.binance.vision/api`, header `X-MBX-APIKEY`, `signature` = HMAC-SHA256(query+body) hex (T, docs https://github.com/binance/binance-spot-api-docs/blob/master/testnet/rest-api.md) | Ya; API key dibuat setelah **login GitHub** di testnet.binance.vision → **tidak bisa dibuat tanpa akun pemilik** | testnet.binance.vision & api.binance.com: **HTTP 451 / "restricted location"** dari lingkungan uji. Data pasar publik lewat `data-api.binance.vision` **T** (ticker, klines, exchangeInfo). Contoh tanda tangan docs (`c8db5682…6b71`) dicocokkan dengan Python (T). Endpoint bertanda tangan diuji terhadap **server tiruan lokal** yang meniru respons terdokumentasi. |
| Binance (mainnet) izin key | — | `GET /sapi/v1/account/apiRestrictions` → `enableWithdrawals`, `enableSpotAndMarginTrading`, `ipRestrict` (T, docs https://developers.binance.com/docs/wallet/account/api-key-permission) | — | Dipakai untuk menolak key yang punya izin withdraw (diuji di mock). |
| Tokocrypto | PAKD berizin OJK (L) | Konvensi mirip Binance (HMAC-SHA256, `X-MBX-APIKEY`) di path `open/v1` (https://www.tokocrypto.com/apidocs/) | Tidak ditemukan testnet publik | `www.tokocrypto.com/open/v1/common/time` mengembalikan halaman "not-support" dari lingkungan uji. **Belum didukung** skill v1.0.0 (kandidat v1.1). |
| Pintu, Reku, Pluang, dll. | PAKD berizin OJK (L) | Tidak ditemukan API trading publik untuk ritel | — | Tidak didukung. |

## 4. Regulasi & pajak (dicek 2026-09-29)
- Pengawasan aset kripto oleh **OJK** (peralihan dari Bappebti sejak 10 Jan 2025, transisi
  berakhir 20 Jan 2026) — rincian & sumber sudah diverifikasi di
  `skills/pantau-pasar-kripto/references/regulasi.md` (dipakai ulang, tidak ditulis ulang).
- **Daftar PAKD berizin**: 26 PAKD per Mei 2026 menurut pemberitaan (L) —
  https://coinvestasi.com/berita/daftar-exchange-kripto-berizin-ojk-di-indonesia ;
  sumber resmi yang wajib dicek member: https://ojk.go.id/id/Fungsi-Utama/ITSK/Perizinan-ITSK-Aset-Keuangan-Digital-Aset-Kripto/
- **PMK 50/2025** (berlaku 1 Agustus 2025), https://www.pajak.go.id/index.php/en/node/118105
  & https://www.pajak.go.id/en/node/117774 (T):
  - PPh Pasal 22 **final 0,21%** dari nilai transaksi, dipungut dari **penjual** oleh
    PPMSE dalam negeri.
  - **1%** untuk PPMSE luar negeri (dipungut bila ditunjuk DJP; bila tidak ditunjuk,
    penjual menyetor sendiri).
  - Penyerahan aset kripto **tidak dikenai PPN** (Pasal 2 ayat (1) PMK 50/2025,
    dipersamakan dengan surat berharga). PPN atas jasa/fee platform **tidak dihitung**
    skill (rinciannya tidak ditemukan di sumber yang dibaca; fee bursa diperlakukan
    sebagai angka total dari bursa).
- Pembulatan PPh di skill: dibulatkan **ke bawah** ke rupiah (tidak pernah melebihi tarif),
  searah standar CLAUDE.md; **belum dicocokkan dengan Coretax**.

## 5. Pesaing (untuk uji banding nanti)
Freqtrade (dry-run + backtest) adalah pembanding terkuat, tapi bukan skill agent.
Kata kunci yang dicari untuk skill agent: "crypto trading bot skill", "DCA bot SKILL.md",
"grid trading agent skill" (ClawHub/skills.sh/GitHub) — penguji Tahap 6 perlu mencari
ulang dan menjalankan banding sesuai aturan.

## 6. Keputusan lisensi
**Proprietary Komunitech.** Tidak ada kode pihak ketiga yang disalin. Contoh API key/secret
pada tes adalah **nilai contoh publik dari dokumentasi resmi** Binance & Indodax (dipakai
untuk mencocokkan algoritma tanda tangan), bukan kredensial siapa pun.
