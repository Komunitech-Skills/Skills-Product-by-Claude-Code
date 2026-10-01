# Uji OpenClaw Asli — Solusi VIP Toko Online

**Tanggal:** 2026-10-01 (Asia/Jakarta) · **Penguji:** agent penguji independen (bukan pembuat skill)

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), memakai **model router Komunitech yang sama dengan bot member** (`ninerouter/komunitech`; jawaban dilayani `claude-sonnet-5` di kedua sisi).
- **SEBELUM** = home `kosong-toko-online` (skill dimatikan: folder `~/.openclaw/skills` kosong). **SESUDAH** = home `sol-toko-online` (paket skill Toko Online + skill tambahan VIP terpasang di `~/.openclaw/skills`). Workspace awal identik.
- 5 pesan identik ditulis seperti pemilik toko online awam mengetik di WA/Telegram (singkat, santai, salah ketik). Skenario 04 sengaja info kurang; jawaban member dikirim sekali, identik di kedua sisi, di sesi yang sama.
- Skenario 02 memakai file fiktif `penjualan-september.csv` (72 baris gaya ekspor Shopee, tanpa nama/nomor pembeli) yang disalin identik ke kedua workspace.
- Pemakaian skill dicek dari daftar tool di JSON keluaran (`successfulToolNames`) + format keluaran yang identik dengan keluaran script skill. Argumen tool call **tidak** diperiksa (lihat "Masalah teknis").
- Semua angka dihitung ulang penguji dengan Python secara independen. Rincian lengkap (balasan utuh, verifikasi, alasan nilai): folder [`uji-openclaw/`](uji-openclaw/).

## Skor

| # | Skenario | Skill terpakai (SESUDAH) | Sebelum | Sesudah |
|---|---|---|---|---|
| 01 | Harga jual Shopee, target untung 25% | `harga-jual-marketplace` (read + script) | 6.5 | 8.5 |
| 02 | Rekap penjualan sebulan dari CSV Shopee | `rekap-penjualan-csv` (read + exec) | 7.5 | 8.5 |
| 03 | Balas ulasan bintang 1 (telat, warna beda, admin lambat) | `balas-ulasan-pelanggan` (read + `cek_balasan.py`) | 6 | 8.5 |
| 04 | Deskripsi produk Shopee, **info kurang** | `listing-marketplace` (read; lalu read + `cek_listing.py`) | 5.5* | 8.5 |
| 05 | Promo 11.11 diskon 30%: masih untung? + rencana | `promo-kalender` (read + `cek_promo.py`) | 6.5 | 8 |
| | **Rata-rata** | | **6.4** | **8.4** |

\* Skenario 04 SEBELUM hanya dinilai dari giliran 2; balasan giliran 1 tidak terbaca penguji (lihat "Masalah teknis").

**Skor keseluruhan solusi (SESUDAH): 8/10.** Skill yang tepat terpicu di 5/5 skenario tanpa perlu disebut namanya, dan semua angka di sisi SESUDAH cocok dengan hitung ulang penguji. Nilai tambah terbesar: **(1)** aturan Indonesia yang dilewatkan model polos (PPh 22 marketplace 0,5%), **(2)** tidak mengarang klaim produk/layanan (listing & ulasan), **(3)** keluaran siap tempel dengan panjang karakter tercek. Untuk rekap CSV (02), model tanpa skill sudah hampir sama tepat angkanya — jangan dijual sebagai pembeda besar; bedanya di kelengkapan & konsistensi format.

**Cakupan:** hanya 5 dari 21 skill paket yang diuji. Jadwal otomatis (laporan harian 21.00, `laporan-otomatis-terjadwal`, `buku-stok`, `kas-umkm`, `buku-piutang`), `karyawan-ai-mulai`, `cek-privasi-openclaw`, dan `agen-cs-toko` **belum** diuji di sini (butuh gateway/cron; sengaja tidak dijalankan).

**Perilaku berisiko agent TANPA skill (SEBELUM) yang tercatat:**
- 01: tidak memasukkan PPh 22 marketplace 0,5% → laba dilaporkan lebih tinggi dari kenyataan (Rp 15.574 vs seharusnya Rp 15.262 di harga yang sama) dan klaim "persis 25%" padahal 24,998%.
- 03: mengarang fakta toko di balasan publik ("sudah sesuai SLA", "pencahayaan studio"), nada membantah ("bukan karena produknya tidak sesuai"), panjang 924 karakter (di atas batas aman 500 karakter yang dipakai skill).
- 04: menambah 6 klaim yang tidak pernah diberikan pemilik ("Dikirim cepat & packing aman", "Barang sesuai foto & deskripsi", "Banyak pelanggan repeat order!", dll.) — berisiko UU Perlindungan Konsumen dan justru memancing ulasan buruk seperti skenario 03.
- 05: target "173 botol" membandingkan promo 1–3 hari dengan laba **sebulan penuh**; klaim pasar tanpa dasar ("11.11 lonjakan 2–4x", jam puncak iklan); anjuran teaser "stok terbatas" tanpa kuota nyata.

## Cacat per skill (temuan penguji)

| Skill | Bukti | Saran perbaikan |
|---|---|---|
| `harga-jual-marketplace` | Script mencetak blok "Catatan & asumsi" lengkap (PMK 37/2025, berlaku 1 Agustus 2026, "Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak."), tetapi agent meringkasnya menjadi "berlaku per PMK terbaru" — nomor aturan, tanggal berlaku, dan disclaimer hilang (01). | Di Langkah kerja 4 / Format output tulis tegas: "salin baris PPh 22 dan baris 'Berlaku per … bukan nasihat pajak' dari script **apa adanya**, jangan diringkas". Tambah butir checklist "nomor PMK + tanggal berlaku tampil". |
| `listing-marketplace` | Deskripsi menambah "tepi lasercut … **ga gampang buyar**" — pemilik hanya menyebut "tepi lasercut"; `cek_listing.py` tetap LULUS (04). Pelanggaran kecil terhadap aturan skill sendiri ("tanpa klaim baru"). | Tambah langkah cek mandiri: bandingkan setiap poin keunggulan dengan daftar fakta dari pengguna; frasa sifat/ketahanan ("tidak mudah …", "awet", "anti …") yang tidak disebut pengguna → hapus atau tanyakan. Bila memungkinkan, `cek_listing.py` menerima daftar fakta pengguna dan menandai frasa sifat yang tidak ada di daftar. |
| `promo-kalender` | Asumsi periode 3 hari (10–12 Nov, normal ±6 botol, target 18 botol) tetapi rencana & S&K memakai periode 1 hari (11 Nov 00.00–23.59) dengan target tetap 18 (05). | Tambah butir checklist: "periode di linimasa & S&K = periode yang dipakai untuk `--unit-normal`/target; bila berbeda, hitung ulang". |
| `promo-kalender` | S&K draf memuat janji "Dikirim maks 2 hari kerja setelah bayar" yang tidak diberikan pemilik (05). | Di langkah 6 (S&K): butir yang belum diketahui (waktu kirim, kuota) ditulis sebagai isian `[isi: …]`, bukan dikarang. |
| `rekap-penjualan-csv` | Member bertanya "hari paling rame" — SESUDAH hanya menjawab dari sisi omzet; SEBELUM (tanpa skill) menjawab omzet **dan** jumlah pesanan (02). | Minor: tambah ke format "Tren harian" baris "Hari dengan transaksi terbanyak" (script sudah punya data per tanggal). |
| `balas-ulasan-pelanggan` | Tidak ada cacat berarti. Balasan publik memuat komitmen ("kami pakai untuk perbaiki hasil fotonya", "sedang membenahi respon tim CS"), tetapi agent sendiri mengingatkan pemilik agar tidak jadi janji kosong (03). | Tidak wajib. Pertimbangkan versi default tanpa komitmen spesifik bila pemilik tidak menyebut rencana perbaikan. |

Pola yang diwaspadai kurator (nama contoh dari file skill bocor ke balasan, tahun/tanggal salah): **tidak ditemukan** di 5 skenario ini. Tanggal & nama hari di rencana 11.11 (Rabu 11 Nov 2026; H-14 = 28 Okt) benar.

## Masalah teknis alat uji
- **Argumen tool call tidak bisa diperiksa.** `uji.sh` hanya menyimpan nama tool (`successfulToolNames`), bukan perintah yang dijalankan. Riwayat sesi ada di SQLite agent; upaya penguji membaca salinannya diblokir pengaman sesi penguji (auto-mode classifier, alasan "Credential Exploration") dan tidak diteruskan. Bukti pemakaian script disimpulkan dari format keluaran yang identik dengan keluaran script. Saran: `uji.sh` ikut mengekspor daftar tool call + argumen (tanpa isi konfigurasi/kredensial) ke `hasil/<nama>.tools.json`.
- **Balasan giliran 1 skenario 04 SEBELUM tidak terbaca.** Agent tanpa skill memakai `tool_search, memory_search, tool_call, ls, read` (menjelajah workspace/memori); saat penguji membuka file balasannya, pembacaan diblokir oleh pengaman yang sama. Penguji tidak mencoba jalan lain; file mentahnya tetap ada di `hasil/toko-04-sebelum.txt` untuk diperiksa pemilik.
- Log `.err` berisi peringatan `SQLite reclamation Worker failed … database owner is no longer current` setelah setiap giliran — tidak memengaruhi balasan.
- Durasi per giliran 13–127 detik; tidak ada timeout.

## Cuplikan jualan (sebelum/sesudah, jujur)

**1. "Harga jual di Shopee berapa biar untung 25%?" (01)**
- Tanpa skill: "HJ ≈ Rp 62.300 … Untung bersih Rp 15.574 → persis 25%" — lupa potongan PPh 22 marketplace 0,5% yang berlaku sejak Agustus 2026.
- Dengan paket Toko Online: "Harga minimal biar ga rugi: Rp 44.858 · Harga rekomendasi: Rp 63.000 … PPh 22 marketplace (0,5%) −Rp 315 … Laba bersih Rp 15.875 (margin 25,2%)" — dihitung script, lengkap dengan catatan pengecualian omzet ≤ Rp500 juta.

**2. "Bikinin deskripsi produk hijab voal" (04)**
- Tanpa skill: langsung menulis "🚚 Dikirim cepat & packing aman · 💯 Barang sesuai foto & deskripsi · ⭐ Banyak pelanggan repeat order!" — tidak satu pun pernah dikatakan pemilik.
- Dengan paket: bertanya sekali ("biar nggak ngarang spek", 5 pertanyaan), lalu memberi judul untuk Shopee/Tokopedia/TikTok (68/100, 47/70, 63/100 karakter, tercek) dan deskripsi hanya dari fakta pemilik.

**3. Balas ulasan bintang 1 (03)**
- Tanpa skill: 924 karakter, mengklaim "packing & kirim sudah sesuai SLA" dan "bukan karena produknya tidak sesuai".
- Dengan paket: balasan publik 469 karakter (tercek script) yang menjelaskan ekspedisi & cahaya foto tanpa membantah pembeli, plus pesan chat pribadi yang meminta nomor pesanan & foto barang.
