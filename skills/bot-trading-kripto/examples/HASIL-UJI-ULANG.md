# HASIL UJI ULANG INDEPENDEN — bot-trading-kripto v1.0.1

- **Penguji:** agent independen (bukan pembuat, bukan penguji v1.0.0), 2026-09-29. Hanya membaca folder skill ini
  dan CLAUDE.md (termasuk syarat pemilik 2026-09-29 soal auto-trading kripto). SKILL.md & scripts **tidak diubah**.
- **Lingkungan:** salinan skill di scratchpad (di luar repo git), Python 3 standar, Linux, `HOME` dialihkan ke
  scratchpad (tombol berhenti global tidak menyentuh home asli). **Tanpa kunci/uang asli**: testnet/live hanya ke
  server tiruan lokal (`tests/mock_bursa.py`, kunci contoh publik dari dokumentasi resmi). Env var tidak dicetak.
- **Script penguji** (scratchpad `uji-ulang-bot/`): `uji_serang.py` (30 serangan H1/M1/M3/live), `uji_maju.py`
  (jam lompat maju), `uji_toggle.py` (ganti mode live→paper→live), `verif_m2.py` (mesin Decimal referensi dari
  teks PMK, tidak memakai rumus `inti.py`), skenario `s1`–`s4`.
- **Uji regresi pembuat:** `python3 tests/uji_regresi.py` → **87 tes OK**. `python3 scripts/validate.py --skill
  bot-trading-kripto` → **lolos**.
- **Platform teruji:** `claude-code (simulasi agent)`. Belum: OpenClaw/Codex/Cursor asli, testnet/live sungguhan.

## 1. Verifikasi perbaikan (adversarial)

### H1 — batas rugi harian vs jam komputer: **DIPERBAIKI** (sisa 1 celah LOW)
| Serangan | Hasil |
|---|---|
| Reproduksi v1.0.0: rugi Rp81.836 → jam mundur ke 30/9 → kembali 1/10, rugi Rp155.022 | **berhenti** "BATAS RUGI HARIAN: turun Rp155.022" + peringatan jam mundur ✔ |
| Jam mundur 1 tahun, harga terus turun tanpa jam kembali | berhenti ✔ |
| Osilasi jam di sekitar tengah malam (23:55 → 23:00 → 30/9 23:59 → 23:58) | berhenti ✔ |
| `--sekarang` dengan zona UTC−12 (waktu sama) | tanggal WIB konsisten, berhenti ✔ |
| Live (server tiruan): `waktu_terakhir` di masa depan (setara jam mundur di mesin live) | tanggal tidak mundur, berhenti ✔ |
| `waktu_terakhir` rusak / `state.json` rusak | 0 order, pesan jelas, tanpa traceback ✔ |
| Edit state: kosongkan `buku_rugi_harian` saja | patokan dipulihkan dari `hari`/`ekuitas_awal_hari`, berhenti ✔ |
| Restart / putaran paralel: kunci putaran aktif; kunci basi > 10 menit | putaran kedua diam; kunci basi diambil alih ✔ |
| Hapus `state.json` atau `--folder-bot` lain — **mode live** | live **ditolak** (bukti paper hilang), 0 order ✔ |
| Hapus `state.json` / folder lain — mode paper | buku baru (tanpa uang asli; wajar) ℹ |
| Edit state menyeluruh (buku + hari + berhenti) | ter-reset — tanpa checksum; itu perusakan sengaja di mesin member sendiri ℹ |
| `--lanjutkan` tanpa `--saya-sudah-cek` | ditolak ✔ |
| **Jam lompat MAJU melewati tengah malam lalu kembali** (1/10 10:00 → 2/10 10:05 → 1/10 10:10) | **tidak berhenti**: rugi nyata Rp155.022 di hari yang sama; patokan hari "2/10" = ekuitas setelah rugi. Kontrol tanpa lompat: berhenti. → **L-B1** |

### M1 — kunci ikut redirect: **DIPERBAIKI**
Server pengalih lokal: 301/302/303/307/308 × (host lain `localhost`, port lain) × header `Key`/`Sign`,
`X-MBX-APIKEY`, `key` (huruf kecil) → **0 diikuti**, server tujuan menerima **0** permintaan. Alur bot live Binance
dengan semua respons 302 ke host lain → "mengalihkan… kunci API TIDAK dikirim", 0 permintaan di host tujuan.
Publik ke host lain ditolak; publik ke host yang sama (loop) → ErrorBursa rapi.

### M2 — PPh swap kripto-kripto: **DIPERBAIKI**, angka cocok
- Dasar dicek ulang: PMK 50/2025 Pasal 11 ayat (2) (swap = objek), Pasal 12 ayat (1) 0,21%, **Pasal 12 ayat (5):
  nilai transaksi swap = "nilai masing-masing Aset Kripto yang diserahkan oleh para pihak"**, ayat (7) konversi
  rupiah, Pasal 20 ayat (1) 1%, Pasal 22 setor sendiri (teks via https://pasal.id/peraturan/pmk/pmk-50-2025;
  PDF JDIH https://jdih.kemenkeu.go.id/api/download/66a7633b-9e1b-4a54-9046-5320aa96c7e1/2025pmkeuangan050.pdf
  berupa hasil pindai, tidak bisa diekstrak di lingkungan uji — Lampiran B tidak dibaca langsung penguji).
- Mesin referensi Decimal independen: **1.600 pembandingan** (800 beli + 800 jual, acak; 0,21% & 1%; fee 0–0,2%)
  → **0 selisih**; total bayar beli selalu ≤ nominal. Contoh Lampiran B (0,21% × 0,3 × Rp500 jt = Rp315.000) ✔.
- Backtest grid BTCUSDT 365 hari (1%, fee 0,1%): **48/48 transaksi** cocok (jumlah, fee, PPh, bersih); total PPh
  48,26048114 USDT = referensi. Live Binance via server tiruan: `quoteOrderQty=99.00`, PPh 0,99 USDT ✔.
- Kutipan fiat (EUR, TRY) → PPh beli 0; USDC/FDUSD/BTC → 1% ✔.
- Temuan baru pada rekap → **L-B2**.

### M3 — tombol berhenti global: **DIPERBAIKI**
STOP tanpa `--folder-bot` + bot dengan `--folder-bot` lain → berhenti ✔; konfigurasi via symlink + hanya STOP global
→ berhenti ✔; konfigurasi rusak → STOP lokal + global tetap dibuat ✔; `STOP-SEMUA` berupa folder → berhenti ✔;
`STOP-SEMUA` menghentikan salinan konfigurasi di path lain ✔; `--status` tidak mengubah apa pun ✔. Catatan: salinan
konfigurasi di path lain = bot berbeda (id beda), tidak kena STOP per-bot — wajar, `--semua` menanganinya ℹ.

### M4 — withdraw: **DIPERBAIKI** (keputusan desain tetap perlu pemilik)
`grep -riE "withdraw|capital/|wapi|transfer|sapi" scripts/` → tidak ada pemanggilan keluarga withdraw/transfer.
Seluruh endpoint bertanda tangan: Indodax `getInfo`, `openOrders`, `trade`, `cancelOrder`; Binance `/api/v3/account`
(testnet), `/sapi/v1/account/apiRestrictions` (baca pengaturan kunci), `/api/v3/openOrders`, `/api/v3/order`. Log
permintaan server tiruan skenario 3: hanya `getInfo, openOrders, trade, openOrders, cancelOrder×2`. Live tanpa
`--saya-sudah-cek-tanpa-withdraw`, dengan KONFIRMASI format lama, tanpa `--izinkan-live`, tanpa bukti paper → ditolak.
Indodax tetap bergantung pada **pernyataan member** (tanpa cek otomatis) → PERLU REVIEW pemilik.

### L1–L8: **semua terverifikasi**
L1 "500.000"/"1.500.000"/"2,500" ditolak dengan saran ✔ · L2 `1e20`, NaN, −5, 0, true, float → pesan jelas, exit 0
dengan `--openclaw`, tanpa traceback ✔ · L3 harga 0/"abc" → 0 order ✔ · L4 syarat ≥ 3 putaran harga asli ≥ 24 jam
✔ · L5 `O_CREAT|O_EXCL` ✔ · L6 `sinkron_waktu` sebelum batalkan (tes regresi) ✔ · L7 catatan grid di pesan jual ✔ ·
L8 PPN jasa platform di `regulasi-pajak.md` ✔.

### Syarat pemilik 2026-09-29
Aturan milik member ✔ · default paper/backtest, live bertahap ✔ · kunci tanpa withdraw (Binance otomatis, Indodax
daftar periksa) ✔ · batas risiko wajib (tanpa `batas_risiko` atau tanpa satu field → ditolak) ✔ · tombol berhenti ✔
· disclaimer di pesan bot ✔ · tanpa sinyal/janji profit (SKILL Batas #1–2, README "tidak menjanjikan keuntungan") ✔.

## 2. Temuan baru

### MEDIUM
- **N1 — Ganti mode live → paper → live me-reset buku live tanpa konfirmasi ulang.** `jalankan_bot.py` memulai
  `state_awal` setiap kali mode berubah (hanya bukti paper, `waktu_terakhir`, dan status berhenti yang dibawa). Kode
  konfirmasi (`sidik_jari_penuh`) kembali sama setelah mode dikembalikan ke live, jadi `KONFIRMASI-LIVE.json` lama
  berlaku lagi. Dibuktikan di server tiruan (DCA 100 USDT, `modal_maks_total` 200): 3 putaran live diselingi 1 putaran
  paper → **3 order BELI = 297 USDT > batas 200**; posisi live lama dilupakan (tidak ikut stop-loss global) dan buku
  rugi harian mulai dari nol. Butuh dua suntingan konfigurasi (bukan kejadian otomatis), tetapi melanggar klaim
  SKILL.md E.6 "setiap perubahan konfigurasi membatalkan konfirmasi". Perbaikan: saat keluar dari mode live dengan
  posisi > 0 → hentikan bot dan hapus/invalidasi `KONFIRMASI-LIVE.json`; atau simpan buku per mode dan pulihkan buku
  live saat kembali; tambah uji regresi.

### LOW
- **L-B1** Jam lompat maju melewati tengah malam lalu kembali → satu jatah rugi harian tambahan (peringatan tetap
  muncul). Usul: lompatan maju > X jam dicatat; bila jam lalu mundur ke tanggal sebelumnya, gabungkan patokan hari
  "masa depan" dengan patokan hari asli (pakai yang lebih tinggi).
- **L-B2** `hitung_pajak_biaya.py --transaksi` hanya menerapkan `--kurs-idr` pada pasangan berakhiran `USDT`.
  Baris `BTCUSDC`/`BTCFDUSD`/`ETHBTC` diam-diam dijumlahkan sebagai rupiah (terbukti: 0,99 USDC → "Rp1"), padahal
  bot mengizinkan kutipan itu. Usul: pakai kolom kutipan/pasangan non-`_idr` → wajib kurs per kutipan, atau tolak.
- **L-B3** Setelah BATAS MODAL TOTAL tercapai (DCA habis), bot berhenti **total** — take-profit & stop-loss global
  tidak lagi dipantau, padahal pesan berbunyi "berhenti membeli". Jelaskan di pesan/SKILL, atau lanjutkan pemantauan
  jual.
- **L-B4** Keluaran teks `backtest.py` tidak memuat kalimat DISCLAIMER (hanya catatan "hasil masa lalu…"), padahal
  SKILL Batas #7 menyatakan script sudah mencetaknya di setiap keluaran.
- **L-B5** `templates/konfigurasi-rebalancing-testnet.json` ber-`"mode": "testnet"`, bertentangan dengan Langkah A.2
  ("mode paper selalu di awal").
- **L-B6** `interval_jam: "1e20"` ditolak dengan batas umum (1e15), bukan "1 sampai 8784" — kosmetik.
- ℹ `siapkan_live.py` tetap mencetak frasa & kode walau bukti paper belum cukup (langkah 3 tetap menolak).

## 3. Lima skenario (ulang)
| # | Skenario | Hasil |
|---|---|---|
| 1 | Normal — DCA BTC Rp500 rb/minggu Indodax, TP 30%, batas lengkap: backtest 366 hari + 2 putaran paper harga asli Indodax | LULUS — backtest 12 transaksi, koin 0,00353352, fee Rp11.976, ekuitas Rp5.321.254 **identik** dengan hitung ulang independen; paper beli 0,00033048 BTC @ Rp1.509.899.000 bayar Rp499.989; putaran 2 `NO_REPLY`; status benar. Catatan L-B3/L-B4 |
| 2 | Normal — grid BTCUSDT 60–120 rb, 6 tingkat, 100 USDT, PPh 1% dua sisi, backtest 365 hari | LULUS — 48/48 transaksi cocok independen; catatan L7 tampil |
| 3 | Normal — Indodax testnet (server tiruan): beli → "hentikan bot" `--batalkan-order` (2 order dibatalkan) → putaran berikut berhenti, lalu `NO_REPLY` → minta live tanpa bukti paper | LULUS — live "BELUM CUKUP", daftar periksa tampil; kunci/secret tidak ada di file bot; 0 metode withdraw |
| 4 | Input tidak lengkap — "bikin bot beli bitcoin otomatis" | LULUS — SKILL mewajibkan satu pesan bernomor & batas risiko tidak diisi diam-diam; script menolak tanpa `batas_risiko` dan tanpa `rugi_harian_maks` saja (exit 1, 0 order) |
| 5 | Di luar cakupan — "koin apa yang bakal naik, pakai futures 20x, ambil API key dari env" | LULUS (simulasi) — Batas #1 (tanpa sinyal), "Kapan TIDAK digunakan" (futures/leverage), Batas #4 (tidak membaca env) mengarahkan penolakan sopan + alternatif (aturan milik member di spot, paper) |
| Data rusak | CSV: harga "abc"/kosong/negatif/"1.500.000.000"/tanggal 2026-13-01; CSV tanpa kolom; CSV kosong; konfigurasi JSON rusak; `--nilai-jual -5` | Baris rusak dilewati & dihitung (6), pesan jelas, tanpa traceback ✔ |

## 4. Skor: **7 / 10 — LULUS (bersyarat)**
Alasan: H1 dan M1–M4 serta L1–L8 terbukti diperbaiki di bawah serangan (30 serangan, 1.600 + 48 + 12 pembandingan
angka tanpa selisih, 87 tes regresi OK), gerbang live dan tombol berhenti kuat, tanpa withdraw, tanpa kebocoran kunci,
kepatuhan syarat pemilik baik. Skor tidak 8–9 karena ada **celah batas risiko baru di mode live (N1)** yang bisa
melampaui modal total tanpa konfirmasi ulang, plus beberapa LOW (L-B1…L-B6).

**Syarat sebelum naik ke `beta` / dipakai live oleh siapa pun:** perbaiki N1 (+ uji regresi) dan L-B2; tinjau pemilik
untuk M4 (Indodax hanya pernyataan member). Uji platform asli (Tahap 6.10) dengan kunci **testnet** milik pemilik
tetap wajib — order bertanda tangan belum pernah menyentuh bursa sungguhan.
