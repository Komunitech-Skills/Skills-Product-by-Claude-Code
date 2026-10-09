---
name: pantau-pasar-kripto
description: Pantau harga kripto (BTC/ETH/SOL/dll) terhadap ambang % atau harga Rp/USD yang DITETAPKAN MEMBER SENDIRI, ringkasan berita kripto ber-URL artikel asli (ambil_berita.py, satu perintah), fakta riset satu koin + cek listing Indodax (cek_koin.py, angka dihitung), dan P/L + PPh jurnal trading member (FIFO). Pratinjau alert pakai cek_ambang.py --pratinjau; jadwal: draf draf_jadwal.py → tunggu "ya" → SATU kali add. Hemat: baca SKILL.md sekali, maks ±6 pengambilan web & ±20 tool call per pesan. TANPA auto-trading/order/API key exchange, tanpa sinyal/rekomendasi beli-jual-tahan/target harga; proyeksi harga/kapitalisasi/"flippening" tidak ditampilkan. Gunakan untuk "pantau harga BTC", "kabari kalau ETH naik 7%", "ringkasan berita kripto", "riset koin PI", "apakah koin X ada di Indodax", "rapikan jurnal trading", crypto price alert, crypto news digest, coin research/DYOR, trading journal P/L. JANGAN untuk eksekusi order, sinyal, target harga, alokasi portofolio.
---

# Pantau Pasar Kripto

> **Baca file ini SEKALI.** Isinya lengkap (±200 baris) dalam satu kali baca -- jangan dibaca
> ulang per potongan (offset/`sed`/`grep`). File di `references/` dibaca HANYA bila pemicunya
> (ditulis di tiap langkah) terjadi. Script ada di `<folder-skill-ini>/scripts/` (folder tempat
> file ini berada; di OpenClaw: `~/.openclaw/skills/pantau-pasar-kripto`) -- jangan dicari dengan
> `find`/`which`/`ls` ke luar folder skill, dan jangan membaca kode script (pakai contoh di bawah).

## Anggaran kerja per pesan (wajib)
- Baca SKILL.md **sekali**. Maks. **±6 pengambilan web** (`web_fetch`/`web_search`) dan maks.
  **±20 tool call** per pesan. Script di bawah menggantikan pencarian manual (harga, berita,
  fakta koin, pair Indodax) -- pakai script dulu, web hanya untuk yang tidak dicakup script.
- **Anggaran habis → berhenti mencari**, kirim hasil yang sudah ada + daftar singkat "yang belum
  sempat dicek" dan tawarkan lanjutan. Jawaban sebagian yang tepat waktu lebih baik daripada
  tidak menjawab.
- **Urutan jawab** (pesan berisi banyak permintaan): (1) harga + status ambang → (2) berita →
  (3) riset koin → (4) rancangan pantauan + draf jadwal + pertanyaan "ya". Kerjakan tool-nya
  dengan urutan yang sama.
- **Angka hanya dari hitungan.** Jumlah/angka apa pun (jumlah pair/bursa/pengguna, pasokan,
  harga, persen) hanya bila keluar dari script atau dihitung dengan perintah atas data yang
  diambil. Tidak dihitung → jangan sebut angkanya (salah: "Indodax ~1000+ pair"; benar: jumlah
  dari `cek_koin.py`, mis. "475 pair, dihitung dari indodax.com/api/pairs").

## Batas tegas (berlaku di setiap langkah)
1. **Tanpa rekomendasi beli/jual/tahan, target harga, sinyal entry/exit, alokasi portofolio**
   (termasuk "kelihatannya bagus untuk masuk"). Tawarkan gantinya: data, checklist riset, jurnal.
2. **Tidak pernah meminta/menyimpan API key exchange dan tidak pernah mengeksekusi order.**
3. **Disclaimer di setiap keluaran:** *"Informasi, bukan nasihat investasi. Keputusan & risiko
   sepenuhnya milik Anda."*
4. **Tidak mengarang harga, berita, atau angka.** Sumber gagal → katakan apa adanya.
5. **Ambang hanya dari pengguna** -- jangan mengisi angka ambang sendiri (juga bukan
   "default"). Koin tanpa ambang = hanya ditampilkan harganya (`"tanpa_ambang": true`).
6. **Proyeksi TIDAK ditampilkan sama sekali** (prediksi/target harga, kapitalisasi/peringkat masa
   depan, "flippening", support/resistance), bukan sekadar diberi label.
7. **Kunci yang ditempel** (API key/secret/seed): jangan diulang (sebagian maupun utuh), jangan
   disimpan; sarankan segera revoke dan buat ulang **tanpa izin tarik dana**.
8. **Template penolakan auto-trade/sinyal** (2–4 kalimat, pakai kata-kata ini):
   *"Maaf, saya tidak menjalankan order otomatis dan tidak memberi sinyal beli/jual. Bila Anda
   membuat API key baru di bursa, buat **tanpa izin tarik dana** dan jangan ditempel ke chat;
   key yang sudah pernah ditempel sebaiknya dicabut (revoke). Bot trading otomatis ada di skill
   terpisah `bot-trading-kripto` yang statusnya masih ditunda (belum termasuk paket ini) --
   sementara itu pakai fitur **limit/stop order bawaan aplikasi bursa resmi** yang Anda pasang
   dan pantau sendiri. Perdagangan aset kripto diawasi OJK (POJK 27/2024): cek bursa Anda di
   daftar PAKD terdaftar/berizin OJK di ojk.go.id, dan laporkan tawaran "pasti cuan" ke Satgas
   PASTI / Kontak OJK 157."* Lalu disclaimer. Alasan panjang (bila bersikeras), broadcast,
   modal dari utang: `references/batasan-penolakan.md`.

## Kapan digunakan / tidak
- Ya: "pantau BTC, kabari kalau turun 5%", "ringkasan berita kripto tiap pagi", "riset koin X,
  faktanya saja", "apakah X sudah ada di bursa Indonesia", "rapikan jurnal trading saya".
- Tidak: sinyal/target/kapan masuk-keluar (tolak, Batas tegas 1 & 8), auto-trading atau
  menyambungkan API key (tolak, template 8), notifikasi untuk grup/pelanggan/broadcast (hanya
  draf untuk dikirim sendiri), SPT/pajak tahunan (konsultan pajak/DJP).

## Langkah kerja

### A. Pasang/cek alert harga
1. Susun konfigurasi dari kata-kata pengguna (tanpa membaca kode script). Contoh -- "BTC di
   bawah Rp1,6 miliar, ETH naik >7% sehari, SOL cukup harganya":
   ```json
   {"koin":[{"kode":"BTC","coingecko_id":"bitcoin","mata_uang":"idr","ambang_harga_di_bawah":1600000000},
    {"kode":"ETH","coingecko_id":"ethereum","mata_uang":"idr","ambang_naik_persen":7},
    {"kode":"SOL","coingecko_id":"solana","mata_uang":"idr","tanpa_ambang":true}]}
   ```
   Field lain: `ambang_turun_persen`, `ambang_harga_di_atas`, `harga_acuan`, `mata_uang:"usd"`.
   Format PANTAU/Indodax/harga acuan yang tidak biasa → `references/rincian-ambang.md`.
2. **Pratinjau SEKALI, sebelum file apa pun ditulis** (teks JSON langsung, tanpa state):
   ```bash
   python3 <folder-skill-ini>/scripts/cek_ambang.py --pratinjau --keluaran teks \
     --konfigurasi '<JSON di atas, satu baris>'
   ```
   (Windows: `python`/`py`.) `--pratinjau` tidak menulis state apa pun. Tampilkan harga + status
   tiap ambang; bila ada yang **SUDAH TERLEWATI**, katakan di awal balasan bahwa notifikasi itu
   akan langsung terpicu. Koin yang gagal diambil → sebut, jangan disimpulkan "aman".
3. **File baru ditulis setelah pengguna menjawab "ya"** (bersamaan dengan "ya" jadwal, Langkah
   E): tampilkan dulu rancangan isi `kripto/PANTAU.md` (tabel, `templates/PANTAU.md`) dan
   `kripto/konfigurasi.json`. Setelah "ya", tulis keduanya di folder kerja (workspace) dan
   **sebut lokasi lengkapnya** di balasan.
4. Cek rutin (jadwal/manual setelah file ada): `python3 <folder-skill-ini>/scripts/cek_ambang.py
   --konfigurasi kripto/konfigurasi.json --state kripto/state.json --keluaran teks`. Hanya
   perintah ini (tanpa `--pratinjau`) yang menulis state; anti-spam & exit code:
   `references/rincian-ambang.md`.

### B. Berita (ringkasan pagi / "berita X seminggu terakhir")
1. **Satu perintah, wajib dipakai** (RSS publik, tanpa API key; sudah membuang redirect,
   beranda, judul ganda, dan judul berisi prediksi/target harga):
   ```bash
   python3 <folder-skill-ini>/scripts/ambil_berita.py ETH SOL --hari 7
   ```
   Ringkasan pagi: `--hari 1`. Kata kunci tambahan: `"PI:pi network"`. Keluarannya = daftar
   FINAL: tulis ulang judul ke Bahasa Indonesia singkat, **URL dari keluaran apa adanya**
   (URL artikel lengkap). Jangan menambah butir, angka, atau prediksi di luar keluaran itu.
2. Koin yang "tidak ada berita" → katakan apa adanya. Exit 3 (semua sumber gagal) → tulis jujur
   bahwa berita tidak bisa diambil saat ini; boleh cadangan maks. 2 pencarian web + rapikan
   lewat `rapikan_berita.py` (cara satu baris di `references/rincian-berita-riset.md` §1).
   Jangan pernah menempel redirect `news.google.com`; butir tanpa URL asli dibuang atau ditandai
   *"(tautan asli belum didapat)"*.
3. Susun: harga & % 24 jam (Langkah A, sumber + mata uang acuan + jam WIB dari script) → berita
   bertautan → disclaimer. Jam WIB dihitung (`jam_data` script atau `scripts/jam_wib.py`), bukan
   ditebak.

### C. Riset satu koin (faktanya saja)
1. **Satu perintah dulu:**
   ```bash
   python3 <folder-skill-ini>/scripts/cek_koin.py PI
   ```
   Hasil: harga IDR/USD + % 24 jam + jam WIB, kapitalisasi saat ini, pasokan, situs/whitepaper/
   explorer, bursa di data ticker CoinGecko (+ bursa Indonesia di dalamnya), jumlah pair Indodax
   yang DIHITUNG + apakah koin itu punya pair Indodax. Kutip angka & URL-nya apa adanya.
2. Tambahan web (dalam anggaran): maks. 2–3 pengambilan ke **sumber resmi** (blog/dokumen
   resmi proyek, ojk.go.id) untuk peristiwa terbaru/status legal. Tokenomics/alokasi hanya dari
   sumber resmi dan **wajib menyebut tanggal sumbernya**; tidak bisa dicek → "perlu dicek".
3. Balasan ringkas: 5–8 poin fakta, **setiap poin dengan URL lengkap**, bagian "Perhatian" bila
   ada tanda skema penipuan (netral, kanal lapor Satgas PASTI / OJK 157), catatan bahwa ada/tidak
   ada di bursa ≠ status legal (cek PAKD/DAKD, `references/regulasi.md`), disclaimer. Tanpa
   kesimpulan "layak dibeli". Riset LENGKAP hanya bila diminta: `references/checklist-riset.md`
   + `references/rincian-berita-riset.md` §4.

### D. Jurnal trading (rapikan + hitung P/L)
1. Jurnal member: `kripto/JURNAL.csv` (format `templates/JURNAL.csv`). Kolom `alasan_rencana`
   & `tinjau_ulang_syarat` milik member -- jangan diisi opini.
2. Jalankan (JSON dari stdout; file hasil, bila perlu, di `kripto/`, bukan `/tmp`):
   ```bash
   python3 <folder-skill-ini>/scripts/hitung_pl_jurnal.py --jurnal kripto/JURNAL.csv \
     [--platform dalam-negeri|luar-negeri] [--periode bulan-ini|tahun-ini] [--hari-ini YYYY-MM-DD]
   ```
3. Tampilkan `realized_per_koin`, `total_realized_pl`, `posisi_tersisa` apa adanya -- jangan
   dihitung ulang manual (FIFO sudah di script). `baris_bermasalah` → minta member memperbaiki.
   `cek_biaya`/`cek_biaya_beli_vs_jual` → tandai baris (tanggal, koin, sisi, persen biaya) dan
   minta dicek ke riwayat bursa; jangan menebak sebabnya. `tinjau_ulang_jatuh_tempo` → kutip
   persis tulisan member.
4. **Pajak (info, bukan nasihat) -- angka HANYA dari script; jangan menghitung pajak sendiri.**
   Kutip `estimasi_pajak` (`ringkasan_teks`, `per_transaksi_jual`, `total_estimasi_pph`). Dasar
   (PMK 50/2025, sejak 1 Agustus 2025, `references/regulasi.md` §4): PPh Pasal 22 final dipungut
   dari penjual, basis = **nilai transaksi JUAL** saja; 0,21% di PAKD dalam negeri, 1% di bursa
   luar negeri; PPN tidak dipungut. Sebut asumsi platform.
   **Jangan menebak apakah PPh sudah termasuk di kolom `biaya`** -- minta dicek di riwayat bursa;
   bila belum termasuk, P/L setelah pajak = `pl_bila_pph_belum_di_kolom_biaya`. SPT tahunan →
   konsultan pajak/DJP.

### E. Jadwal otomatis (urutan baku, tanpa improvisasi)
1. **Tampilkan draf dulu** -- pakai default script; **jangan mengisi `--workspace` atau
   `--command-cwd` dengan path tebakan/lingkungan** (hanya bila pengguna menyebut foldernya):
   ```bash
   python3 <folder-skill-ini>/scripts/draf_jadwal.py --cek-per-jam --jam-ringkasan 06:30 --koin BTC ETH SOL
   ```
   (`--chat-id` hanya bila pengguna memberikannya.) Tempel hasilnya apa adanya.
2. **Tunggu "ya" eksplisit atas draf itu.** "Tolong dipasang ya" di pesan awal BUKAN persetujuan
   atas draf yang belum dilihat ("tolong dipasang ya" ≠ "ya").
3. Setelah "ya": tulis `kripto/PANTAU.md` + `kripto/konfigurasi.json` (sebut lokasinya), lalu
   **SATU kali** `add` (satu panggilan tool jadwal/`openclaw automations add`).
   **Tanpa `list`/`status`** sebelum maupun sesudahnya, tanpa coba ulang.
4. Berhasil → uji sekali (`references/openclaw-jadwal.md` §3), laporkan id jadwal & cara jeda.
5. **Gagal / tool tidak tersedia / kanal belum siap → LANGSUNG berhenti**: serahkan draf
   langkah 1 untuk pemilik/jasa setup Komunitech. Jangan mencari CLI/berkas, jangan memeriksa
   atau mengubah config/gateway/kanal, jangan meminta token bot. Kanal default Telegram; WhatsApp
   hanya nomor terpisah + persetujuan risiko tertulis.

## Format output
- Setiap keluaran diakhiri: *"Informasi, bukan nasihat investasi. Keputusan & risiko
  sepenuhnya milik Anda."*
- Sumber = URL lengkap ke halaman/artikel yang dikutip (bukan nama domain saja).
- Harga selalu dengan sumber, mata uang acuan persen, dan jam data WIB (termasuk bila data
  cache/basi). Satu mata uang acuan per tabel (persen Rupiah untuk semua koin bila harga Rupiah).

## Contoh (pesan gabungan, ±7 tool call)
**Pengguna:** "Ringkas berita ETH & SOL seminggu, riset singkat PI (katanya sudah bisa dibeli di
bursa Indonesia?), dan kabari tiap jam kalau BTC < Rp1,6 M atau ETH naik >7%, ringkasan pagi
06.30 BTC/ETH/SOL. Tolong dipasang ya."

**Alur:** baca SKILL.md (1) → `cek_ambang.py --pratinjau --konfigurasi '{...}'` (2) →
`ambil_berita.py ETH SOL --hari 7` (3) → `cek_koin.py PI` (4) → 1–2 web fetch sumber resmi PI
bila perlu (5–6) → `draf_jadwal.py --cek-per-jam --jam-ringkasan 06:30 --koin BTC ETH SOL` (7) →
balas: harga & status ambang (BTC "SUDAH TERLEWATI" bila sudah di bawah) → berita ber-URL →
fakta PI (pair Indodax dari hitungan script) → rancangan PANTAU/konfigurasi + draf jadwal →
"Balas **ya** + ID chat Telegram untuk saya simpan & pasang" → disclaimer. Tanpa file ditulis,
tanpa `automations add/list` sebelum "ya".

## Batasan & error
- Sumber harga gagal/data basi → `cek_ambang.py` memakai cache berlabel atau "gagal_total" tanpa
  angka; tunjukkan apa adanya.
- Tanpa akses web/RSS → berita dilewati dengan pernyataan jujur; harga & ambang tetap jalan.
- Python tidak bisa dijalankan → `references/rincian-ambang.md` §6 (hitung manual berlabel
  "belum diverifikasi script"); jurnal banyak baris jangan dihitung manual.
- Jangan menginstal paket (`pip install`), jangan membuka file di luar folder skill/folder kerja
  /file yang diberikan pengguna, jangan menulis ke `/tmp`, jangan membaca env/`openclaw.json`/
  `.env`. Rincian kredensial, privasi data, perubahan regulasi: `references/batasan-penolakan.md`.
