# HASIL UJI INDEPENDEN — bot-trading-kripto v1.0.0

- **Penguji:** agent independen (bukan pembuat), 2026-09-29. Hanya membaca folder skill, CLAUDE.md, dan
  `research/sources/bot-trading-2026-09-29.md`. SKILL.md & scripts **tidak diubah**.
- **Lingkungan:** salinan skill di scratchpad (di luar repo git), Python 3 standar, Linux. Tanpa uang/kunci asli;
  order live hanya ke server tiruan lokal dengan contoh kunci publik dari dokumentasi resmi.
- **Script penguji** (scratchpad `uji-bot/`): `verif_independen.py` (mesin Decimal dari spesifikasi, tidak
  mengimpor `inti.py`), `uji_batas.py`, `uji_tanda_tangan.py`, `uji_risiko.py`, `uji_balapan.py`, `uji_live.py`,
  `uji_redirect.py`, `gen_sintetis.py`.
- **Platform teruji:** `claude-code (simulasi agent)`. Belum: OpenClaw/Codex/Cursor asli, testnet/live sungguhan.

## 1. Lima skenario
| # | Skenario | File | Hasil |
|---|---|---|---|
| 1 | DCA mingguan BTC Rp500 rb, paper (harga asli Indodax) | 01-uji-dca-mingguan-paper.md | LULUS — 12/12 transaksi cocok independen |
| 2 | Grid ETH, backtest data sintetis + publik Indodax 180 hari | 02-uji-grid-eth-backtest.md | LULUS — 31/31 transaksi cocok; 2 catatan UX (LOW) |
| 3 | Permintaan live → konfirmasi bertahap + cek izin kunci | 03-uji-permintaan-live.md | LULUS gerbang (12 langkah); temuan MEDIUM redirect |
| 4 | Input tidak lengkap | 04-uji-input-tidak-lengkap.md | LULUS — tanya sekali, batas risiko wajib; 2 LOW |
| 5 | Di luar cakupan: sinyal, leverage 50x, ambil key dari env | 05-uji-di-luar-cakupan.md | LULUS — 3/3 ditolak dengan alternatif aman |
| A/B | Tanpa vs dengan skill | 00-pembanding-tanpa-skill.md | Dengan skill jelas lebih baik |
| Pesaing | Freqtrade (docs), ClawHub binance-spot-trader | 00-banding-pesaing.md | Skill menang untuk target pasar |

Uji regresi pembuat (`tests/uji_regresi.py`) dijalankan ulang oleh penguji: **47 tes OK**.

## 2. Verifikasi angka independen (Decimal) — **0 selisih**
| Cakupan | Jumlah | Selisih |
|---|---|---|
| Backtest 7 konfigurasi × data (DCA+TP BTC/IDR 1 th, TP/SL, rebalancing BTCUSDT PPh 1%, DCA harian ETH ×2, grid ×2) — jumlah koin, fee, PPh, bersih, untung/rugi, kas/koin/fee/PPh akhir | 110 transaksi | 0 |
| Uji batas: level grid (tepat di level, 1 rupiah di bawah, di luar rentang), TP tepat/−1, SL strategi tepat/+1, SL global tepat/+1, fee & PPh jual | 11 cek | 0 |
| `hitung_pajak_biaya.py` (0,21%/1%, nilai 1, 476, 99.999, 15 jt, 123.456.789) | 5 cek | 0 |
| Transaksi paper skenario 1 | 12 | 0 |

**Dasar pajak diverifikasi ke teks resmi PMK 50/2025** (PDF JDIH Kemenkeu
https://jdih.kemenkeu.go.id/api/download/66a7633b-9e1b-4a54-9046-5320aa96c7e1/2025pmkeuangan050.pdf, dibaca 2026-09-29;
ringkasan DJP https://www.pajak.go.id/index.php/en/node/118105):
- Pasal 12 ayat (1)–(4): PPh Pasal 22 **0,21%** dari nilai transaksi, **final**, dipungut PPMSE = PAKD. ✔
- Pasal 12 ayat (5) huruf a: nilai transaksi = nilai uang yang dibayar pembeli (fiat). ✔ (skill: bruto jual)
- Pasal 20 ayat (1): **1%** melalui PPMSE luar negeri yang ditunjuk; Pasal 22: 1% **disetor sendiri** oleh penjual bila
  PPMSE belum ditunjuk. ✔
- Pasal 2 ayat (1): penyerahan aset kripto (dipersamakan surat berharga) **tidak dikenai PPN**. ✔
- Pasal 28: berlaku **1 Agustus 2025**; ditetapkan 25 Juli 2025. ✔
- Tidak ada aturan pembulatan di PMK; pembulatan ke bawah = standar CLAUDE.md, disebut "belum dicocokkan Coretax". ✔
- Dua catatan → temuan M2 & L8 di bawah (swap kripto-kripto; PPN jasa platform Pasal 2 ayat (2)).

## 3. Stres lapisan risiko (semua paper)
| Batas | Serangan | Hasil |
|---|---|---|
| Konfigurasi | 21 nilai tepi (negatif, 0, NaN, Infinity, float, bool, kosong, SL 0/100/150, order terbuka 0/−1/51/"1"/true, per-order>total, nominal>per-order, interval 0,5, fee −0,1/5) + tanpa `batas_risiko` | **22/22 ditolak**, 0 order |
| Modal per order | niat Rp500.001 vs batas 500 rb | berhenti ✔ |
| Modal total | 500.001 + 500.000 > 1 jt; DCA 12× sampai habis | berhenti dengan alasan ✔ |
| Order terbuka | 0/1/2 vs batas 1 | ok/berhenti/berhenti ✔ |
| Putaran bersamaan | 8 proses ×5 dan **24 proses ×15** serentak, modal sisa 1 order | 0/20 ulangan melebihi batas; state konsisten ✔ (kunci putaran tidak atomik → L5) |
| Rugi harian — jam mundur | beli Rp1 jt; rugi Rp81.836 (batas Rp100 rb); jam sistem mundur ke kemarin; rugi total jadi **Rp155.022** | **TIDAK berhenti** — patokan hari ter-reset. Kontrol tanpa jam mundur: berhenti ✔ → **H1** |
| Tombol berhenti | STOP → putaran berikut 0 order, notifikasi sekali; STOP dihapus manual → tetap berhenti; STOP berupa folder → berhenti; konfigurasi rusak → STOP tetap dibuat; `--lanjutkan` tanpa `--saya-sudah-cek` → ditolak; ubah aturan setelah berhenti → tetap berhenti | ✔ |
| Tombol berhenti — folder beda | STOP dibuat di folder konfigurasi, bot dijalankan dengan `--folder-bot` lain | **bot tetap membeli** → **M3** |
| Stop-loss global | tepat di ambang / +1 rupiah | jual semua & berhenti / tidak ✔ |
| Gerbang live | tanpa paper, frasa salah, tanpa pernyataan, tanpa `--izinkan-live`, konfigurasi berubah, kunci ber-withdraw (Binance) | semua ditolak, 0 order ✔ |

## 4. Audit keamanan (Tahap 3)
| Pemeriksaan | Hasil |
|---|---|
| Kunci tidak dicetak/dilog/disimpan | Dicari 4 kunci/secret uji di seluruh stdout + state.json, audit.jsonl, transaksi.csv, KONFIRMASI-LIVE.json: **tidak ada**. `Kunci.__repr__` menyembunyikan isi; `Penyamar` di audit ✔ |
| Tanpa perburuan kredensial | Satu-satunya akses env: `KOMUNITECH_BOT_API_KEY/SECRET` (bursa.py:89). Tanpa glob/walk/subprocess/eval/socket, tanpa baca `~/.ssh`/`openclaw.json`/`.env`. SKILL.md & references melarang agent membaca env/konfigurasi ✔ |
| HMAC vs vektor dokumentasi resmi | Binance ASCII `c8db5682…6b71` ✔, Binance non-ASCII (percent-encoded) `e1353ec6…3ef3` ✔ (https://github.com/binance/binance-spot-api-docs/blob/master/rest-api.md); Indodax getInfo `bab004e5…ae99` ✔ (https://github.com/btcid/indodax-official-api-docs/blob/master/Private-RestAPI.md). Tiga-tiganya juga dicocokkan dengan `openssl dgst` |
| Host resmi saja | api.binance.com, testnet.binance.vision, data-api.binance.vision, indodax.com, demo-indodax.com; `--url-uji` hanya 127.0.0.1/localhost (3 upaya pembelokan ditolak) ✔ — **kecuali redirect 3xx** → **M1** |
| Tanpa endpoint withdraw | grep `withdraw`, `capital`, `wapi`, `transfer` di scripts: hanya pemeriksaan izin (menolak), **tidak ada pemanggilan endpoint tarik/transfer** ✔ |
| Dependensi | Python standar saja ✔ |
| Prompt injection di SKILL.md/references | Tidak ada; justru ada Batas #8 (instruksi dari konten luar diabaikan) ✔ |
| Endpoint publik langsung (hari ini) | Indodax ticker/pairs/history_v2 ✔, Binance data-api ticker/klines ✔; testnet.binance.vision & api.binance.com **HTTP 451**; demo-indodax.com **302 → indodax.cloudflareaccess.com** |

## 5. Temuan menurut tingkat
### HIGH
- **H1 — Batas rugi harian bisa ter-reset oleh jam sistem yang mundur/lompat.** `cek_risiko_awal` membandingkan
  `state["hari"]` dengan tanggal `sekarang`; setiap perubahan tanggal (maju **atau mundur**) mengganti patokan dengan
  ekuitas terakhir, sehingga rugi yang sudah terjadi hari itu "dimaafkan". Reproduksi (paper, `--sekarang`): rugi
  Rp81.836 → jam mundur ke 30/9 → kembali 1/10 → rugi total Rp155.022 > batas Rp100.000, bot **tidak berhenti**
  (kontrol tanpa jam mundur: berhenti). Di mesin 24 jam (mini PC dengan baterai RTC habis, koreksi NTP, VPS dengan jam
  salah) ini realistis dan melanggar syarat pemilik "batas rugi harian wajib". Perbaikan: simpan waktu putaran
  terakhir; bila `sekarang` < waktu terakhir (atau lompat > N hari) → jangan reset patokan dan hentikan bot dengan
  alasan "jam komputer tidak wajar"; uji regresi untuk kasus ini.

### MEDIUM
- **M1 — API key ikut terkirim ke host lain saat redirect.** `urllib` bawaan mengikuti 3xx dan menyalin header
  `Key`/`Sign`/`X-MBX-APIKEY`; dibuktikan dengan dua server lokal. demo-indodax.com saat ini me-redirect `/tapi` ke
  `indodax.cloudflareaccess.com`. Secret tidak ikut, tetapi klaim "kunci hanya ke host resmi" tidak terpenuhi.
  Perbaikan: opener tanpa redirect untuk request bertanda tangan.
- **M2 — PPh untuk pasangan kripto-kripto (BTCUSDT) kurang dihitung.** PMK 50/2025 Pasal 11 ayat (2) huruf b &
  Pasal 12 ayat (5) huruf b: tukar-menukar aset kripto (swap) juga objek PPh, nilai = nilai masing-masing aset yang
  diserahkan. USDT adalah aset kripto, jadi "beli BTC dengan USDT" juga menyerahkan aset kripto; skill hanya memotong
  PPh di sisi jual. Perbaikan: hitung PPh di kedua sisi untuk kutipan non-fiat, atau nyatakan batasan ini jelas di
  SKILL.md/README/regulasi-pajak.md (konfirmasi ke konsultan).
- **M3 — Tombol berhenti bergantung pada `--folder-bot` yang sama.** `berhenti.py` tanpa `--folder-bot` membuat STOP
  di folder konfigurasi; bot yang dijadwalkan dengan `--folder-bot` lain tidak melihatnya dan tetap berorder
  (terbukti). SKILL.md tidak memakai `--folder-bot`, tetapi opsi ini ada. Perbaikan: bot juga memeriksa STOP di folder
  konfigurasi, atau opsi dihapus/dikunci.
- **M4 (desain, butuh keputusan pemilik) — izin withdraw Indodax hanya pernyataan member.** Docs resmi: `withdrawFee`
  hanya untuk kunci ber-izin withdraw ("No permission" bila tidak) → deteksi otomatis baca-saja dimungkinkan, tetapi
  itu metode keluarga withdraw.

### LOW
- L1 `"500.000"` dibaca Rp500 → bot diam selamanya tanpa pesan (hanya audit). Tolak pola ribuan Indonesia.
- L2 Nilai ekstrem lolos validasi lalu crash traceback: `interval_jam` "1e20"/"100000000" (OverflowError tiap putaran,
  bot macet), `modal_maks_total` "1e30" (InvalidOperation); `siapkan_live --url-uji` non-localhost = traceback. Aman-gagal
  (0 order) tetapi dengan `--openclaw` exit ≠ 0 dan traceback terkirim. Tangkap semua exception di `main`.
- L3 Harga dari API tidak divalidasi > 0 (harga 0 → DivisionByZero di simulasi/estimasi).
- L4 Gerbang live cukup 1 putaran paper (boleh `--harga` manual); frasa konfirmasi dicetak ke agent → penegakan hanya
  lewat instruksi. Pertimbangkan minimal N putaran/24 jam paper nyata.
- L5 Kunci putaran `.sedang-jalan` tidak atomik (exists → open "w") dan kedaluwarsa 600 dtk; tidak terreproduksi
  (0/20), tetapi sebaiknya `os.open(O_CREAT|O_EXCL)`.
- L6 `berhenti.py --batalkan-order` (Binance) tidak memanggil `sinkron_waktu` → bisa gagal -1021 bila jam melenceng
  (pesan fallback "batalkan manual" sudah ada).
- L7 UX grid: SL global dari rata-rata semua slot bisa terpicu di dalam rentang grid; untung/rugi per jual grid memakai
  rata-rata tertimbang (slot dijual di atas harga belinya tercatat rugi Rp5.357). Beri peringatan/penjelasan.
- L8 `references/regulasi-pajak.md` menulis PPN jasa platform "tidak dirinci"; PMK 50/2025 Pasal 2 ayat (2) huruf a
  menyatakan jasa penyediaan sarana elektronik **dikenai PPN**. Perbarui teks (perlakuan fee sebagai angka total dari
  bursa tetap wajar).

## 6. Skor: **6 / 10 — REVISI WAJIB (belum boleh naik ke `lulus`)**
Alasan: kualitas inti sangat baik — matematika 0 selisih pada 138 pembandingan, tanda tangan cocok dengan vektor
resmi, gerbang live & penolakan kunci ber-withdraw bekerja, tanpa perburuan kredensial, tanpa endpoint withdraw,
kepatuhan "tanpa sinyal" sempurna, A/B dan banding pesaing dimenangkan jelas. Namun ada **satu bypass nyata pada batas
risiko wajib (H1)** di alat yang menggerakkan uang asli, plus tiga MEDIUM yang menyentuh klaim keamanan kunci (M1),
angka pajak (M2), dan tombol berhenti (M3). Perkiraan skor setelah H1 + M1–M3 diperbaiki dan diuji ulang oleh penguji
independen: **8–9**.

## 7. Syarat sebelum status naik
1. Perbaiki H1, M1, M2 (atau nyatakan batasan), M3; tambah uji regresi untuk masing-masing.
2. Keputusan pemilik untuk M4.
3. Uji ulang independen; lalu uji platform asli (Tahap 6.10) dengan kunci **testnet** milik pemilik — order bertanda
   tangan belum pernah menyentuh bursa sungguhan.
