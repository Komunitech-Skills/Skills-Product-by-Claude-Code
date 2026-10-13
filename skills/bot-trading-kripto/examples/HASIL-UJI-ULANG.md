# HASIL UJI ULANG INDEPENDEN — bot-trading-kripto v1.0.1

- **Penguji:** agent independen (bukan pembuat, bukan penguji v1.0.0), 2026-09-29. Hanya membaca folder skill ini
  dan pedoman kurasi Komunitech (termasuk syarat pemilik 2026-09-29 soal auto-trading kripto). SKILL.md & scripts **tidak diubah**.
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

## Catatan revisi 1.0.3 (pembuat, 2026-09-29 — belum diuji ulang independen)
Versi 1.0.2 di catalog.csv dipakai revisi lintas-library `allow_abbrev=False` (dipertahankan); revisi ini = 1.0.3.
Status tetap `uji`. Uji ulang oleh penguji independen tetap diperlukan sebelum naik status.

| Temuan | Perbaikan | Uji regresi (`tests/uji_regresi.py`) |
|---|---|---|
| **N1** live→paper→live mengosongkan buku live & memakai ulang konfirmasi (297 USDT > batas 200) | (a) Buku **per mode** (`KOLOM_BUKU` di `inti.py`): ganti mode menyimpan buku mode lama di `buku_per_mode` dan memulihkan buku mode baru; buku live (posisi, modal terpakai, patokan rugi, saldo awal bursa) tidak pernah di-reset. (b) `KONFIRMASI-LIVE.json` **sekali pakai**: berisi `id`, `hash_konfigurasi` (SHA-256 penuh), `waktu`, `segel` = SHA-256(id+hash+waktu); wajib dipakai ≤ 24 jam; saat dipakai menjadi `sesi_live` dan id dicatat di `konfirmasi_live_dipakai` + file ditandai `dipakai`. Sesi batal saat ganti mode **atau** hash konfigurasi berubah (walau lalu dikembalikan). Konfirmasi format 1.0.1 (tanpa segel) ditolak. (c) Sebelum setiap order BELI live: modal terpakai = max(buku live, (saldo koin bursa − saldo awal live) × harga) lewat endpoint baca-saja (Binance `GET /api/v3/account`, Indodax `getInfo`); saldo gagal dibaca → tidak ada order beli. (d) Keluar dari live dengan posisi → peringatan; `berhenti.py --status` & `siapkan_live.py` menampilkan buku live tersimpan | `N1BukuLiveDanKonfirmasi`: reproduksi 297 vs 200 (2 BELI, bukan 3; konfirmasi lama "SUDAH DIPAKAI"; beli ke-3 "BATAS MODAL TOTAL"), segel disunting/kedaluwarsa/konfigurasi diubah-lalu-dikembalikan ditolak, rekonsiliasi saldo bursa saat buku live terhapus, saldo gagal → tanpa beli, status buku live |
| **L-B2** rekap pajak menjumlahkan USDC/BTC sebagai rupiah | `hitung_pajak_biaya.py --transaksi`: rekap per bulan **per mata uang kutipan** + `total_per_mata_uang`; tidak pernah menjumlahkan mata uang berbeda; rupiah hanya dengan `--kurs KUTIPAN=angka` dari pengguna (boleh berulang; `--kurs-idr` lama = kurs USDT) di blok `perkiraan_rupiah` berlabel PERKIRAAN; PPh dibulatkan ke bawah; kutipan tak dikenal → baris bermasalah | `LB2RekapPajakPerMataUang` (3 tes) + tes M2 lama disesuaikan |
| **L-B4** backtest tanpa disclaimer | Keluaran teks memuat `DISCLAIMER: ...`; JSON punya field `disclaimer` | `LB4DisclaimerBacktest` |
| **L-B1** jam lompat maju lalu kembali = jatah rugi tambahan | (a) Batas rugi juga **24 jam bergulir** (patokan = sampel ekuitas tertua dalam 24 jam menurut jam komputer, `jejak_ekuitas`, sampel tiap 15 menit); (b) selama jam tidak monoton, patokan hari = yang tertinggi dari tanggal jam komputer s.d. tanggal efektif. Catatan: 24 jam bergulir lebih ketat dari per tanggal (rugi yang melewati tengah malam ikut dihitung) — didokumentasikan di SKILL.md & references | `LB1JamMaju`: skenario penguji (1/10 10:00 → 2/10 10:05 → 1/10 10:10) kini berhenti "turun Rp155.022"; patokan tertinggi tanpa jejak; rugi melewati tengah malam; kontrol jam normal |

- Tes baru terbukti **gagal pada kode sebelum revisi** (9 gagal/error dari 10) dan lulus sesudahnya.
- `python3 tests/uji_regresi.py` → 109 tes OK (dijalankan 3× berturut-turut). `python3 scripts/validate.py --skill bot-trading-kripto` → lolos.
- Server tiruan (`tests/mock_bursa.py`) kini melacak saldo BTC akun tiruan (untuk uji rekonsiliasi). Tanpa kunci/uang asli.
- Sisa (belum dikerjakan): L-B3 (setelah modal total habis, TP/SL global tidak dipantau), L-B5, L-B6; M4 tetap PERLU REVIEW pemilik; rekonsiliasi saldo mengasumsikan saldo koin di luar bot tidak berubah selama bot live (pembelian manual di akun yang sama dihitung sebagai modal terpakai → bot berhenti lebih cepat, arah aman). Buku live yang sudah hilang di 1.0.1 tidak bisa dipulihkan; saldo awal live diambil saat putaran live pertama 1.0.3.

## Uji ulang 1.0.3

- **Penguji:** agent independen (bukan pembuat, bukan penguji sebelumnya), 2026-09-29. Hanya membaca folder skill ini dan
  pedoman kurasi Komunitech (termasuk syarat pemilik 2026-09-29 soal kripto). SKILL.md & scripts **tidak diubah**.
- **Lingkungan:** salinan skill di scratchpad (di luar repo), `HOME` dialihkan ke scratchpad, Python 3 standar, Linux.
  Testnet/live **hanya** ke server tiruan lokal `tests/mock_bursa.py` (kunci contoh publik dokumentasi). Tanpa kunci/uang
  asli. Env var tidak dicetak. Script penguji (scratchpad `uji-ulang-bot3/`): `serang_n1.py` (12 serangan modal total),
  `uji_jam.py` (11 skenario jam), `s3_regresi.py` (skenario 3 + H1/M1/M3/M4), CSV pajak buatan penguji.
- `python3 tests/uji_regresi.py` → **109 tes OK**. `python3 scripts/validate.py --skill bot-trading-kripto` → **lolos**.
- **Platform teruji:** `claude-code (simulasi agent)`. Belum: OpenClaw/Codex/Cursor asli, testnet/live bursa sungguhan.

### 1. N1: modal maksimal total (DCA 100 USDT, `modal_maks_total` 200, Binance live ke server tiruan)
| # | Serangan | Hasil |
|---|---|---|
| A1 | live→paper→live 5× dengan konfirmasi **baru yang sah** setiap kali | 2 BELI, ±199,98 USDT ≤ 200 ✔ (buku live dipulihkan) |
| A2 | live→**testnet**→live 3× | buku live ≤ 200 ✔ |
| A3 | Konfirmasi **dipalsukan** (id baru, segel dihitung sendiri; segel tanpa rahasia) + toggle 4× | tetap 2 BELI ≤ 200 ✔. Pemalsuan menembus gerbang frasa, tapi tidak menembus batas modal (buku live + saldo bursa) ℹ |
| A4 | Folder bot **diklon** (state + konfirmasi) ke `--folder-bot` lain, dijalankan **bergantian** 4 ronde | 2 BELI ≤ 200 ✔ (rekonsiliasi saldo bursa menahan) |
| A5 | `--folder-bot` baru tanpa state | live ditolak (tanpa bukti paper), 0 order ✔ |
| A6 | Hapus `state.json` saat live | live ditolak, 0 order ✔ |
| A7 | Hapus `state.json` → paper ulang (bukti 24 jam) → frasa & konfirmasi baru | **4 BELI ≈ 400 USDT** ✘: `saldo_koin_awal_bursa` baru = saldo sekarang, koin bot lama dianggap milik member → **N1-R2** |
| A8 | Sunting state: buang `buku_per_mode.live` saat paper, lalu live dengan konfirmasi baru | **4 BELI ≈ 400 USDT** ✘ (perusakan sengaja; akar sama dengan A7) |
| A9 | Sunting state: nolkan buku live, `saldo_koin_awal_bursa` utuh | 2 BELI ≤ 200 ✔ ("dicocokkan dengan saldo bursa") |
| A10 | Naikkan `modal_maks_total` saat memegang posisi live | bot berhenti "Aturan/konfigurasi berubah…", 0 order ✔ |
| A11 | 8 proses paralel, folder yang sama | 7× `NO_REPLY` (kunci putaran), total ≤ 200 ✔ |
| A12 | Folder diklon + kedua folder dijalankan **bersamaan** (mis. pindah ke VPS tanpa mematikan laptop, jadwal menit sama) | **3 BELI ≈ 300 USDT** pada 2 dari 4 percobaan ✘ (race: keduanya membaca saldo sebelum order lain terisi) → **N1-R1** |

Kesimpulan N1: jalur asli (ganti mode, konfirmasi dipakai ulang, restart, paralel satu folder, sunting buku) **tertutup**.
Masih bisa lewat batas bila (R1) salinan buku yang sama jalan bersamaan di dua folder/mesin, atau (R2) buku live hilang lalu
member membangun ulang bukti paper 24 jam + mengetik frasa baru. Keduanya butuh tindakan manusia yang disengaja.

### 2. Rekap pajak per mata uang kutipan (L-B2): **DIPERBAIKI**
CSV uji: IDR, USDT, USDC, ETHBTC, FDUSD, pasangan tak dikenal, angka rusak. Tanpa `--kurs`: 5 blok terpisah (IDR/USDT/USDC/
BTC/FDUSD), **0** angka rupiah untuk non-IDR, peringatan "TIDAK dijumlahkan sebagai rupiah"; `BTCXYZ` & `bruto "xx"` →
`baris_bermasalah`. Dengan `--kurs USDT=16500 --kurs usdc=16400`: blok `perkiraan_rupiah` hanya untuk kutipan berkurs,
berlabel "PERKIRAAN - dikonversi dengan kurs yang ANDA masukkan…"; angka dicek tangan (USDT 60 → Rp990.000, PPh 0,6 →
Rp9.900; USDC 61 → Rp1.000.400, PPh Rp10.004) ✔. `--kurs-idr` lama = USDT ✔. Kurs negatif/NaN/IDR/tanpa `=` → error rapi ✔.
Temuan kecil → **R3**: `--kurs USDT=16.500` diterima sebagai 16,5 (rupiah 1.000× terlalu kecil, walau label menampilkan
"Rp16.5"); `--kurs USDT=1e400` → traceback `InvalidOperation`.

### 3. Disclaimer backtest (L-B4): **DIPERBAIKI**
Keluaran teks diakhiri "DISCLAIMER: Bot ini hanya menjalankan aturan yang ANDA tetapkan…"; JSON memuat field `disclaimer` ✔.

### 4. Batas rugi 24 jam bergulir vs jam komputer (L-B1): **DIPERBAIKI** — 11/11 sesuai harapan
Posisi 1 jt IDR, batas rugi Rp100.000 (paper, `--harga/--sekarang`). Rugi Rp121.755 dicek tangan (0,00066533 BTC × 1,32 M +
kas Rp9). Kontrol normal berhenti; rugi ±60 rb tidak berhenti. Jam **maju** +26 j / +3 hari / +10 hari lalu kembali → berhenti;
jam **mundur** −24 j lalu kembali → berhenti; osilasi maju-mundur 5× → berhenti; rugi melewati tengah malam dan rugi pelan
10:00→22:00→09:00 → berhenti "dalam 24 jam terakhir"; rugi 60 rb, pulih, lalu turun 60 rb setelah 25 jam → **tidak** berhenti
(tanpa positif palsu). ℹ Dari kode: bila jam mundur > 24 jam, patokan 24 jam = sampel tertua (bisa ±4 hari) → bisa berhenti
lebih awal (arah aman).

### 5. Regresi H1 / M1 / M2 / M3 / M4: **tetap baik**
H1 jam mundur 400 menit → "BATAS RUGI HARIAN" ✔ · M1 redirect 302 ke server lain → ditolak, **0** permintaan di host tujuan ✔
· M2 grid BTCUSDT 365 hari: **48/48** transaksi cocok dengan hitung ulang independen (jumlah, fee, PPh 1% dua sisi, bersih),
total PPh 48,26048114 USDT ✔ · M3 STOP tanpa `--folder-bot`, bot dengan folder lain → berhenti ✔ · M4 metode Indodax yang
dipanggil hanya `getInfo, openOrders, trade, cancelOrder`; grep tanpa pemanggilan withdraw/transfer ✔ (Indodax tetap
pernyataan member → PERLU REVIEW pemilik).

### 6. Lima skenario
| # | Skenario | Hasil |
|---|---|---|
| 1 | Normal — DCA BTC Rp250 rb/minggu Indodax, TP 20%, modal 3 jt: backtest 366 hari + 2 putaran paper harga asli Indodax | LULUS — 12 transaksi, koin 0,00176674, fee Rp5.988, ekuitas Rp2.660.629 **identik** hitung ulang independen; paper BELI 0,00016536 @ Rp1.508.758.000 bayar Rp249.987 (fee Rp499) dicek tangan; putaran 2 `NO_REPLY`; status benar; disclaimer ada |
| 2 | Normal — grid BTCUSDT 60–120 rb, 6 tingkat, 100 USDT, PPh 1% | LULUS — 48/48 cocok, catatan grid & disclaimer tampil |
| 3 | Normal — Indodax testnet (server tiruan): BELI → "hentikan bot" `--batalkan-order` (2 dibatalkan) → berhenti → `NO_REPLY` → minta live tanpa bukti paper | LULUS — `siapkan_live` "BELUM CUKUP", live ditolak 0 order; kunci tidak ada di folder bot |
| 4 | Input tidak lengkap — konfigurasi tanpa `batas_risiko` / tanpa `rugi_harian_maks` + "1.000.000" | LULUS — ditolak, pesan jelas, 0 order, `--openclaw` exit 0; SKILL mewajibkan satu pertanyaan bernomor, batas risiko tidak diisi diam-diam |
| 5 | Di luar cakupan — "koin apa yang naik, futures 20x, ambil API key dari env" | LULUS (simulasi) — Batas #1, #4 dan "Kapan TIDAK digunakan" (futures/leverage) mengarahkan penolakan sopan + alternatif |

### 7. Temuan baru
- **N1-R1 (MEDIUM-rendah)** Dua salinan folder bot yang sama berjalan **bersamaan** (klon/migrasi mesin) bisa melewati
  `modal_maks_total` (race baca saldo; terbukti 300 > 200 pada 2/4 percobaan). Usul: kunci putaran global per akun+pasangan di
  `~/.komunitech/…` (tidak bergantung `--folder-bot`) dan/atau baca saldo ulang setelah order; sebut di SKILL "jangan salin
  folder bot yang sedang aktif".
- **N1-R2 (LOW)** Buku live hilang (hapus `state.json`/sunting) → setelah paper 24 jam + frasa baru, patokan saldo baru
  menganggap koin bot lama milik member → satu jatah modal penuh lagi. Usul: simpan `saldo_koin_awal_bursa` live di lokasi
  global per bot/akun, atau saat live mulai tanpa buku tampilkan saldo koin yang ada dan minta member menyatakannya.
- **R3 (LOW)** `hitung_pajak_biaya.py --kurs`: pola ribuan ("16.500") tidak ditolak; `1e400` → traceback.
- Sisa lama belum dikerjakan (sesuai catatan pembuat): L-B3, L-B5, L-B6; M4 PERLU REVIEW pemilik.

### 8. Skor: **8 / 10 — LULUS**
Alasan: N1 jalur asli (ganti mode, konfirmasi dipakai ulang/dipalsukan, restart, paralel, sunting buku) tertutup dan terbukti
di bawah 12 serangan; L-B1, L-B2, L-B4 diperbaiki (11/11 skenario jam, rekap per kutipan berlabel PERKIRAAN, disclaimer);
regresi H1/M1–M4 tetap; angka cocok independen (12 + 48 transaksi + paper). Tidak 9 karena batas modal masih bisa dilewati
lewat salinan bot yang jalan bersamaan (R1) atau buku live yang hilang (R2), plus LOW sisa.
**Syarat sebelum `beta`/live oleh siapa pun:** perbaiki atau dokumentasikan R1 (+ uji regresi), tinjau pemilik untuk M4, dan uji
platform asli (Tahap 6.10) dengan kunci **testnet** milik pemilik — order bertanda tangan belum pernah menyentuh bursa sungguhan.

## Catatan revisi 1.0.4 (pembuat, 2026-09-29)

Menutup temuan "Uji ulang 1.0.3". Status tetap `lulus`; **perlu uji ulang independen** sebelum skor diubah.

| Temuan | Perbaikan | Regresi (`tests/uji_regresi.py`) |
|---|---|---|
| **N1-R1** salinan folder jalan bersamaan (300 > 200) | `scripts/buku_global.py`: **kunci akun** OS (`fcntl.flock` POSIX / `msvcrt.locking` Windows) di `~/.komunitech/bot-trading-kripto/akun/akun-<sidik>.lock`, sidik = SHA-256(bursa + API key **publik**)[:16], tanpa secret. Dipegang sepanjang putaran live (baca saldo → putuskan → order → catat), lepas otomatis bila proses mati. Tunggu maks 120 detik, lalu putaran dilewati tanpa order. | `test_r1_salinan_folder_berjalan_bersamaan`: 6 proses serentak (asli + 5 salinan, state + konfirmasi ikut tersalin), order tiruan diperlambat 0,3 detik → **2 BELI ≤ 200 USDT**. `test_r1_kunci_akun_eksklusif_lintas_proses` |
| **N1-R2** hapus `state.json` → paper ulang → frasa baru (400 > 200) | **Buku live global** per akun/pasangan (`akun-<sidik>.json`): patokan saldo koin milik member sebelum live pertama + posisi & modal terpakai gabungan semua bot, diperbarui segera setelah setiap isi order. Sebelum **setiap** beli live: modal terpakai = max(buku folder, buku global, (saldo koin bursa − patokan) × harga + nilai order BELI terbuka). Buku global rusak → tanpa beli. Migrasi: entri baru diisi dari buku live folder 1.0.3, patokan diambil yang lebih rendah (lebih ketat). | `test_r2_hapus_state_paper_ulang_frasa_baru` (tetap 2 BELI, patokan tetap 0), `test_r2_folder_baru_total_dan_buku_global_tanpa_rahasia` (folder bot dibuang total → folder baru tetap 1 jatah; buku global tanpa key/secret), `test_order_beli_terbuka_dihitung` (150 USDT order limit terbuka + 100 > 200 → berhenti), `test_buku_global_rusak_tanpa_beli`, `test_migrasi_buku_folder_lama_ke_global`, `test_catat_isi_jual_mengurangi_modal`, `test_indodax_nilai_order_beli_terbuka` |
| **R3** `--kurs USDT=16.500` terbaca 16,5; `1e400` traceback | `angka_kurs()`: format Indonesia (`16.500` = 16500, `1.500.000.000`, desimal koma `16500,25`); **ditolak** ambigu `16,500` (pesan "AMBIGU"), `16500.5`, `16.5`, `16,500.00`, `1.50.000`, notasi ilmiah, negatif, 0. Semua angka dibatasi ≤ 10^15; `ArithmeticError` ditangkap → `{"status":"error","pesan":"GAGAL: ..."}`, exit 1. | `R3KursFormatIndonesia` (3 tes; `1e400` di `--kurs`, `--kurs-idr`, `--nilai-jual`, dan kurs 10^15 × bruto 10^15 lewat subprocess: tanpa traceback) |

- **Uji kontrol (membuktikan tes bermakna):** di salinan scratchpad, kunci akun dimatikan → tes paralel gagal **7 BELI (≈700 USDT) ≠ 2** (3/3 kali); buku global dimatikan → 4 tes N1R1R2 gagal. Kode repo tidak memuat saklar pematian apa pun.
- **Hasil:** `python3 tests/uji_regresi.py` **3× berturut-turut: 128 tes OK** (109 lama + 19 baru); tes paralel diulang 5× tambahan: 5/5 OK. `python3 scripts/validate.py --skill bot-trading-kripto` → lolos. Semua uji memakai `HOME` sementara & server tiruan lokal dengan kunci contoh publik dokumentasi; tanpa kunci asli, env var tidak dicetak.
- **Dokumentasi:** SKILL.md (E.6 + Batasan), README (bagian batas modal), `references/strategi-dan-konfigurasi.md`, `references/regulasi-pajak.md`.
- **Batas jujur yang TIDAK bisa dicegah script** (tertulis di SKILL.md & README): pengguna dengan akses shell menghapus/menyunting `~/.komunitech/bot-trading-kripto/akun/` **sekaligus** state bot; kunci API **baru** untuk akun yang sama (buku global baru); dua **mesin** berbeda (kunci file OS hanya berlaku di satu komputer). Saat patokan saldo baru dibuat dengan saldo koin > 0, bot menampilkan catatan agar member memeriksanya. Kunci `msvcrt` (Windows) dan macOS belum diuji di mesin asli.
- **Sisa:** L-B3, L-B5, L-B6; M4 PERLU REVIEW pemilik; uji platform asli + testnet milik pemilik tetap syarat sebelum `beta`.
