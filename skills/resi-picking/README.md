# Picking List & Urutan Resi dari File Pesanan

**Ratusan pesanan Shopee/Tokopedia/TikTok Shop, satu file, langsung jadi daftar ambil barang dan urutan resi siap cetak.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Cocokkan barang dengan resi dalam hitungan detik.** Cukup kirim file ekspor pesanan, admin gudang langsung dapat daftar ambil per SKU dan urutan kemas per kurir - tidak perlu mencocokkan satu per satu di Excel.
- ✅ **Diurutkan per rak kalau kamu punya data lokasinya.** Ambil barang jadi satu jalur, tidak bolak-balik gudang.
- ✅ **Pesanan dengan catatan khusus (minta bungkus kado, warna tertentu, dll.) ditandai jelas** di bagian paling atas supaya tidak terlewat.
- ✅ **Peringatan jujur:** SKU yang belum kamu kenal, jumlah 0/aneh, baris data yang dobel, dan pesanan tanpa nomor resi semuanya disebutkan - bukan diam-diam dilewati.
- ✅ **Tanpa setup.** Tidak perlu akun, API key, atau install aplikasi tambahan - hanya file CSV yang sudah kamu unduh sendiri dari Seller Center.

## Cocok untuk siapa
- Seller Shopee/Tokopedia/TikTok Shop dengan puluhan sampai ratusan pesanan per hari
- Admin gudang/packing yang selama ini mencocokkan pesanan dan resi secara manual
- Toko yang belum (atau belum mau) pakai aplikasi inventori penuh - cukup jalankan setiap hari dari file pesanan

## Contoh sebelum & sesudah
**Sebelum:** Setiap sore kamu buka file pesanan di Excel, hitung manual berapa kaos hitam M yang harus diambil, lalu tulis ulang urutan resi per kurir di kertas supaya admin gudang tidak salah kirim. Kalau ada 150 pesanan, ini bisa makan waktu 30-60 menit dan gampang salah hitung.

**Sesudah (cukup ketik):** "Ini file pesanan hari ini, buatkan daftar ambil barang dan urutan resinya."
→ Dalam beberapa detik keluar dua dokumen: daftar ambil per SKU (diurutkan per rak bila ada datanya) dan urutan kemas per kurir, lengkap dengan pesanan yang punya catatan khusus dan peringatan untuk data yang mencurigakan (jumlah 0, SKU asing, resi kosong, pesanan dobel).

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Ini file pesanan Shopee hari ini, buatkan picking list"
- "Buatkan urutan resi per kurir dari file TikTok Shop ini"
- "Ini file pesanan, file lokasi rak, dan file stok - cocokkan semuanya"
- "Kolom SKU-nya ternyata di kolom 'Kode Barang', coba lagi"

Setiap hasil selalu menunjukkan dulu pemetaan kolom yang dipakai (No. pesanan, SKU, Jumlah, dst.) dan daftar peringatan, supaya kamu bisa cek sebelum dicetak.

## Syarat
- Python 3.8 atau lebih baru (biasanya sudah ada di Mac/Linux; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, atau API key.
- File ekspor pesanan dalam format **CSV** (kalau file aslinya .xlsx, simpan ulang sebagai CSV dari Excel/Google Sheets terlebih dulu).
- File lokasi rak dan file stok bersifat opsional dan bisa ditambahkan kapan saja untuk hasil yang lebih lengkap.

## Beda dengan skill lain
- **`buku-stok`** juga punya fitur picking list, tapi itu bagian dari aplikasi inventori penuh (menyimpan database stok, memotong stok otomatis, mengingat pesanan yang sudah dikemas). **resi-picking** tidak menyimpan apa pun - cocok kalau kamu cuma butuh daftar ambil & urutan resi cepat tanpa mengurus stok penuh.
- **`pdf-lokal`** merapikan file PDF resi (gabung, susun 4 per lembar) untuk dicetak. **resi-picking** membuat DAFTAR barangnya, bukan mengolah file PDF resinya - keduanya saling melengkapi.

## Instalasi singkat
Salin folder `resi-picking` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1 Okt 2026 (v1.0.4), skor 1–10 penguji independen: tanpa skill **6,5** → dengan skill **8,5** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dengan skill: script `resi.py`, file siap cetak, peringatan No. pesanan rusak Excel; tanpa skill di jebakan Excel: picking tetap terisi tapi kerusakan nomor pesanan diremehkan.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung.

## FAQ
**Filenya harus format apa?**
CSV. Kalau file ekspor dari Seller Center-nya .xlsx, buka di Excel/Google Sheets lalu simpan ulang sebagai CSV - baru unggah ke sini.

**Kalau nama kolom di file saya beda dari biasanya, gimana?**
Alat ini mendeteksi nama kolom secara fleksibel (banyak sinonim), dan selalu menunjukkan pemetaan yang dipakai supaya bisa dicek. Kalau salah tebak, cukup bilang ke AI agent nama kolom yang benar, atau minta jalankan ulang dengan opsi `--kolom-...`.

**Apakah ini bisa otomatis ambil pesanan dari Shopee/Tokopedia/TikTok Shop tanpa saya unduh manual?**
Tidak. Skill ini sengaja tidak melakukan scraping atau login otomatis ke marketplace - kamu tetap yang mengekspor file pesanan dari Seller Center, alat ini hanya mengolahnya jadi picking list & urutan resi.
