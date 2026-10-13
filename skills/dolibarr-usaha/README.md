# Dolibarr Usaha: Asisten AI untuk Dolibarr Anda

**Ketik "buatkan invoice untuk CV Maju Jaya", "siapa yang belum bayar?", atau "stok apa yang mau habis?". AI Anda langsung membaca dan menyiapkan data di Dolibarr, program pembukuan, stok, dan data pelanggan (CRM) gratis yang jalan di komputer sendiri, tanpa biaya bulanan.**

Diuji AI penguji independen di OpenClaw (dengan data contoh): 5,25 → 9,0 dari 10 (tanpa skill kunci akses diterima di chat dan hapus massal siap dieksekusi; dengan skill keduanya ditolak dan umur piutang dihitung lewat skrip).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan: Dolibarr (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Invoice dalam satu kalimat.** Pelanggan dan barang dicari otomatis, PPN 12% × DPP (dasar pengenaan pajak) 11/12 dihitung, lalu dibuat sebagai **draf** di Dolibarr. Setelah itu angkanya dicocokkan dengan hitungan Dolibarr, dan bila beda sepeser pun Anda diberi tahu.
- ✅ **Tahu siapa yang belum bayar.** Daftar piutang dikelompokkan per umur (belum jatuh tempo, telat 1–30, 31–60, 61–90, >90 hari), yang paling lama telat di atas.
- ✅ **Stok tidak kecolongan.** Barang habis, minus, dan menipis muncul lengkap dengan saran jumlah beli. Bila modul Stok tidak dipakai, skill mengatakannya terus terang, tanpa alarm "habis" palsu.
- ✅ **Laporan tiap malam ke Telegram.** Penjualan hari ini dibanding kemarin, piutang terlambat, dan stok menipis, dikirim otomatis lewat OpenClaw (belum diuji langsung).
- ✅ **Dirancang hati-hati dengan data usaha.** Bawaannya hanya membaca. Menulis (pelanggan baru, draf invoice) lewat pratinjau dan butuh persetujuan Anda. Validasi, pembayaran, dan hapus tetap Anda yang pegang. Kunci akses disimpan terpisah dan disamarkan bila muncul di layar.

## Cocok untuk siapa
- UMKM & usaha mapan yang memakai (atau ingin pindah ke) **Dolibarr** di komputer sendiri, biasanya lewat **DoliWamp** (paket pemasangan Dolibarr untuk Windows; belum diuji langsung oleh tim kami), sebagai alternatif dari Jurnal/Accurate + Moka/Majoo + CRM (data pelanggan) berbayar.
- Pemilik yang ingin cukup bertanya ke AI (OpenClaw, Claude Code, Codex, Cursor) tanpa menghafal menu Dolibarr.
- Admin kantor yang sering membuat invoice dan menagih piutang.

**Kurang cocok:** belum punya Dolibarr dan tidak ingin memasangnya (pakai skill **Buat Invoice** untuk invoice sederhana atau **Buku Stok** untuk mencatat stok); Dolibarr di hosting tanpa HTTPS (alamat internet tanpa enkripsi); butuh e-Faktur resmi (tetap lewat Coretax DJP, sistem pajak online).

## Contoh sebelum & sesudah
**Sebelum:** buka Dolibarr → Tagihan → Nota baru → pilih pelanggan → tambah baris satu per satu → hitung PPN DPP 11/12 di kalkulator → cek ulang. Untuk tahu siapa yang telat bayar: buka daftar invoice, sortir, hitung hari satu per satu.

**Sesudah:** ketik *"Buatkan invoice untuk Toko Sinar Abadi: kopi KPI-250 3 bungkus, gula aren 2 kg 32.500, ongkir 12.345"*:
```
PRATINJAU DRAF INVOICE
Pelanggan: Toko Sinar Abadi (ID 2)
1. Kopi Bubuk Arabika 250g - 3 x Rp 85.000 = Rp 255.000
2. Gula Aren 1kg - 2 x Rp 32.500 = Rp 65.000
3. Ongkos kirim - 1 x Rp 12.345 = Rp 12.345
DPP: Rp 332.345 | PPN: Rp 36.557 | TOTAL: Rp 368.902
Simpan sebagai draf? (ya/tidak)
```
Setelah "ya":
```
TERSIMPAN SEBAGAI DRAF: (PROV7)
Angka di Dolibarr: DPP Rp 332.345 | PPN Rp 36.557,95 | total Rp 368.902,95
BEDA dengan hitungan Komunitech: PPN +Rp 0,95 (Dolibarr membulatkan per baris). Draf tidak diubah otomatis.
```
(Contoh nyata dari uji dengan Dolibarr 24.0.1; data pelanggan dan barang fiktif.)

## Cara pakai
Setelah terpasang dan terhubung, cukup ketik permintaan biasa:
- "Cek Dolibarr saya sudah nyambung belum"
- "Cari pelanggan Maju", "Tambah pelanggan Warung Bu Sari, 0812-3456-7890, Solo"
- "Buatkan invoice untuk CV Maju Jaya: 3 kopi KPI-250, jatuh tempo 30 hari"
- "Siapa saja yang belum bayar?", "Piutang yang telat lebih dari sebulan"
- "Stok apa yang mau habis?", "Stok kopi tinggal berapa?"
- "Kirim laporan Dolibarr ke Telegram saya tiap jam 9 malam" (OpenClaw; belum diuji langsung)

## Instalasi singkat
1. **Dolibarr** sudah terpasang dan modul API aktif. Belum? Ikuti `docs/panduan-dolibarr.md` di paket (Windows lewat DoliWamp ±30–60 menit; belum kami uji langsung di Windows), **termasuk langkah pengamanan wajib 2.4** (ganti sandi database bawaan, pastikan hanya bisa dibuka dari komputer sendiri, jangan buka ke internet), atau pakai **jasa setup Komunitech**.
2. Salin folder `dolibarr-usaha` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

3. Simpan kunci API sekali (di terminal Anda sendiri, bukan di chat): `python3 ~/.openclaw/skills/dolibarr-usaha/scripts/dolibarr.py simpan-kunci` (Windows: `python` / `py`).

Panduan pemasangan skill lengkap: `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`). Butuh **Python 3.8+** (gratis di python.org). Tidak butuh internet, akun, atau paket tambahan.

**Fitur baru sejak versi 1.0.10:** perintah `piutang-csv` membaca file tabel (CSV) hasil ekspor Dolibarr, tanpa perlu koneksi atau kunci, dan menghitung umur piutang lewat skrip; agent tidak mengirim tagihan ke pelanggan, hanya menyiapkan draf yang Anda kirim sendiri.

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah, data contoh; aplikasi Dolibarr sendiri tidak dijalankan), 2 Okt 2026 (diuji pada v1.0.11; versi terkini 1.0.12), skor 1–10 penguji independen: tanpa skill **5,25** → dengan skill **9,0** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill pernah menerima kunci API (kunci akses) di chat dan siap eksekusi hapus massal; dengan skill menolak hapus massal dan kunci di chat (skenario ini memakai hasil uji sebelumnya, v1.0.10), menjalankan `piutang-csv` untuk umur piutang, dan menampilkan pratinjau draf invoice. Sambungan ke Dolibarr 24.0.1 asli diuji terpisah oleh penguji independen (simulasi agent; lihat `examples/HASIL-UJI.md`).

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent dengan data contoh, 2026-10-02). Uji manusia di Dolibarr asli (Windows/DoliWamp) belum dilakukan; hasilnya menunggu tim Komunitech. Pengiriman laporan ke Telegram dan pemakaian di Codex serta Cursor juga belum diuji langsung.

## FAQ
**Apakah AI bisa salah mengirim atau menghapus invoice saya?**
Tidak lewat skill ini: script tidak punya perintah validasi, kirim, bayar, atau hapus. Invoice dibuat sebagai draf dan Anda yang memvalidasi di Dolibarr; membuat pelanggan/draf pun harus lewat pratinjau dan persetujuan Anda. Jujur saja: di Dolibarr, kunci yang boleh membuat invoice secara teknis juga bisa memvalidasi/menandai lunas lewat API (jalur sambungan antarprogram). Karena itu panduan menyarankan kunci **baca-saja** untuk laporan harian dan kunci terpisah untuk membuat draf (`docs/panduan-dolibarr.md` bagian 6).

**Kenapa PPN di Dolibarr kadang beda Rp 1 dengan hitungan skill?**
Dolibarr menghitung PPN per baris lalu membulatkan ke terdekat, sedangkan standar Komunitech menghitung dari total lalu membulatkan ke bawah (agar tidak memungut melebihi tarif). Skill menampilkan keduanya dan tidak mengubah apa pun. Nilai PPN resmi tetap mengikuti faktur di Coretax.

**Apakah data saya dikirim ke internet?**
Tidak oleh skill ini. Script hanya berbicara dengan Dolibarr di komputer Anda (`localhost`, alamat komputer sendiri) dan menolak alamat lain kecuali Anda menegaskannya (wajib HTTPS untuk alamat internet). Laporan Telegram dikirim oleh OpenClaw milik Anda, hanya ke chat Anda.

---
Komunitech tidak berafiliasi dengan proyek Dolibarr; Dolibarr adalah merek milik pemiliknya.
