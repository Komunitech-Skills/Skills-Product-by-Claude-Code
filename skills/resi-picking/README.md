# Picking List & Urutan Resi dari File Pesanan

**Ratusan pesanan Shopee/Tokopedia/TikTok Shop, satu file, langsung jadi daftar ambil barang dan urutan resi siap cetak.**

Diuji AI penguji independen di OpenClaw: 6,5 → 8,5 dari 10 (nomor pesanan yang rusak karena Excel ditandai dan ditahan, bukan diremehkan; pada pesanan biasa, AI tanpa skill sudah hampir sama bagusnya).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Cocokkan barang dengan resi dalam waktu singkat.** Cukup kirim file ekspor pesanan, admin gudang langsung dapat daftar ambil per SKU (kode barang) dan urutan kemas per kurir - tidak perlu mencocokkan satu per satu di Excel.
- ✅ **Diurutkan per rak kalau Anda punya data lokasinya.** Ambil barang jadi satu jalur, tidak bolak-balik gudang.
- ✅ **Pesanan dengan catatan khusus (minta bungkus kado, warna tertentu, dll.) ditandai jelas** di bagian paling atas supaya tidak terlewat.
- ✅ **Peringatan jujur:** SKU yang belum Anda kenal, jumlah 0/aneh, baris data yang dobel, dan pesanan tanpa nomor resi disebutkan di daftar peringatan, tidak dilewati diam-diam.
- ✅ **Tanpa setup.** Tidak perlu akun, API key, atau install aplikasi tambahan - hanya file CSV (file tabel yang bisa dibuka di Excel) yang sudah Anda unduh sendiri dari Seller Center.

## Cocok untuk siapa
- Seller Shopee/Tokopedia/TikTok Shop dengan puluhan sampai ratusan pesanan per hari
- Admin gudang/packing yang selama ini mencocokkan pesanan dan resi secara manual
- Toko yang belum (atau belum mau) pakai aplikasi inventori penuh - cukup jalankan setiap hari dari file pesanan

## Contoh sebelum & sesudah
**Sebelum:** Setiap sore Anda buka file pesanan di Excel, hitung manual berapa kaos hitam M yang harus diambil, lalu tulis ulang urutan resi per kurir di kertas supaya admin gudang tidak salah kirim. Kalau ada 150 pesanan, ini bisa makan waktu 30-60 menit dan gampang salah hitung.

**Sesudah (cukup ketik):** "Ini file pesanan hari ini, buatkan daftar ambil barang dan urutan resinya."

Cuplikan hasil (contoh dengan data fiktif: 10 baris pesanan contoh; dipotong dari `examples/01-picking-dasar/output-daftar-ambil.md`):
> # Daftar Ambil Barang (Picking)
>
> …
>
> **Total: 4 pesanan aktif, 4 jenis barang, 12 pcs.**
>
> ## Pesanan dengan catatan khusus (baca dulu sebelum packing)
> - Pesanan #240901A1: "Tolong dibungkus rapi ya kak"
>
> ## Ambil di rak
>
> ### A1
> - [ ] **KAOS-HT-M** Kaos Polos Pria - Hitam - M x 3 pcs (2 pesanan)
>
> ### A2
> - [ ] **KAOS-HT-L** Kaos Polos Pria - Hitam - L x 3 pcs (1 pesanan)
>
> …
>
> ## Peringatan
> - SKU tidak ada di file stok (input-stok-buku-stok.csv): GANTUNGAN-X. Kemungkinan salah ketik atau produk baru.
> - 1 baris 'jumlah tidak terbaca' dilewati (baris 9).

Hasil lengkapnya juga memuat urutan kemas per kurir.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Ini file pesanan Shopee hari ini, buatkan picking list"
- "Buatkan urutan resi per kurir dari file TikTok Shop ini"
- "Ini file pesanan, file lokasi rak, dan file stok - cocokkan semuanya"
- "Kolom SKU-nya ternyata di kolom 'Kode Barang', coba lagi"

Setiap hasil menampilkan dulu pemetaan kolom yang dipakai (No. pesanan, SKU, Jumlah, dst.) dan daftar peringatan, supaya Anda bisa cek sebelum dicetak.

## Syarat
- Python 3.8 atau lebih baru (biasanya sudah ada di Mac/Linux; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, atau API key.
- File ekspor pesanan dalam format **CSV** (kalau file aslinya .xlsx, simpan ulang sebagai CSV dari Excel/Google Sheets terlebih dulu).
- File lokasi rak dan file stok bersifat opsional dan bisa ditambahkan kapan saja untuk hasil yang lebih lengkap.

## Beda dengan skill lain
- **`buku-stok`** (aplikasi pencatat stok Komunitech) juga punya fitur picking list (daftar ambil barang), tapi itu bagian dari aplikasi inventori penuh (menyimpan database stok, memotong stok otomatis, mengingat pesanan yang sudah dikemas). **resi-picking** tidak menyimpan apa pun - cocok kalau Anda cuma butuh daftar ambil & urutan resi cepat tanpa mengurus stok penuh.
- **`pdf-lokal`** (alat pengolah PDF Komunitech) merapikan file PDF resi (gabung, susun 4 per lembar) untuk dicetak. **resi-picking** membuat DAFTAR barangnya, bukan mengolah file PDF resinya - keduanya saling melengkapi.

## Instalasi singkat
Salin folder `resi-picking` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.0.4), skor 1–10 penguji independen: tanpa skill **6,5** → dengan skill **8,5** (selisih +2,0, lulus acuan kami). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Dengan skill: skrip hitung bawaan skill, file siap cetak, peringatan nomor pesanan yang rusak karena Excel; tanpa skill di jebakan Excel: picking tetap terisi tapi kerusakan nomor pesanan diremehkan.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis 2026-10-01) dan Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung. Semua uji memakai file pesanan contoh (data fiktif) dengan judul kolom yang meniru ekspor Shopee/Tokopedia/TikTok Shop, belum dengan ekspor toko asli.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech), 17 Oktober 2026, versi 1.0.5, dengan pesan yang sama untuk kedua sisi (tanpa skill dan dengan skill): ekspor pesanan Shopee hari ini dari sebuah toko gadget (campur kurir JNE, J&T, dan SiCepat, ada yang batal dan belum bayar), lengkap dengan file lokasi rak dan file stok, lalu minta daftar ambil barang per SKU dan urutan kemas/tempel resi per kurir. Skor 1–10 dari penilai independen: tanpa skill **7,5** → dengan skill **8,5** (selisih +1,0), **belum lulus acuan kami**: selisihnya masih di bawah 1,5.

Dengan skill, Anda langsung melihat totalnya (4 pesanan aktif, 4 jenis barang, 12 pcs), nomor pesanan yang dilewati beserta alasannya, dan stok setelah dikemas (kaos hitam M tinggal 0 dan ditandai habis). Namun kali ini versi tanpa skill juga menangkap semua baris bermasalah dengan benar, sehingga selisihnya kecil.

Catatan jujur: data uji ini ternyata cukup mudah bagi asisten tanpa skill. Jawaban dengan skill masih memuat bagian "Pemetaan kolom" yang agak teknis dan kalimat pembuka yang tidak perlu. Uji sebelumnya: 16 Oktober 2026 (versi 1.0.4), tanpa skill 6,5 → dengan skill 7,5; saat itu nomor pesanan yang dilewati dan sisa stok belum ditampilkan.

## FAQ
**Filenya harus format apa?**
CSV. Kalau file ekspor dari Seller Center-nya .xlsx, buka di Excel/Google Sheets lalu simpan ulang sebagai CSV - baru unggah ke sini.

**Kalau nama kolom di file saya beda dari biasanya, gimana?**
Alat ini mendeteksi nama kolom secara fleksibel (banyak sinonim), dan menunjukkan pemetaan yang dipakai supaya bisa dicek. Kalau salah tebak, cukup bilang ke AI agent nama kolom yang benar, lalu minta dijalankan ulang.

**Apakah ini bisa otomatis ambil pesanan dari Shopee/Tokopedia/TikTok Shop tanpa saya unduh manual?**
Tidak. Skill ini sengaja tidak mengambil data otomatis dari akun penjual Anda dan tidak login ke marketplace - Anda tetap yang mengekspor file pesanan dari Seller Center, alat ini hanya mengolahnya jadi picking list & urutan resi.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
