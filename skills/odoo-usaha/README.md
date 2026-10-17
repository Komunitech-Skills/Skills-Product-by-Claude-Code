# Tanya Odoo Lewat Chat, Laporan Siap Pakai

**Tanya "penjualan hari ini berapa?", "siapa yang belum bayar?", atau "stok apa yang mau habis?" — AI Anda langsung membaca Odoo milik usaha Anda dan menjawab dengan angka yang dihitung, bukan dikira. Laporan harian bisa dikirim otomatis ke Telegram pemilik (jadwal otomatis belum diuji langsung), dan penawaran (quotation) bisa disiapkan sebagai draf tanpa membuka menu Odoo.**

Diuji AI penguji independen di OpenClaw (dengan server Odoo tiruan): rata-rata dua tugas 3,0 → 8,9 dari 10. Pada tugas jebakan (kunci admin ditempel di chat + "hapus penawaran"), AI tanpa skill langsung menghapus dan membatalkan lewat kunci itu; dengan skill tidak ada satu pun permintaan ke Odoo. Pada tugas penjualan & piutang, dengan skill angka penjualan tepat.

> Komunitech **tidak berafiliasi** dengan Odoo S.A. Odoo adalah software milik Odoo S.A. (edisi Community berlisensi LGPL-3.0). Skill dan panduan ini adalah karya orisinal Komunitech yang memakai **API eksternal resmi** (pintu sambungan data bawaan) Odoo milik Anda sendiri. Odoo tidak disertakan dalam paket.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Software tambahan: Odoo (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tanpa buka banyak menu.** Penjualan hari ini vs kemarin, produk terlaris, faktur terbit, piutang (tagihan yang belum dibayar pelanggan) per umur, dan stok kritis — cukup satu kalimat biasa.
- ✅ **Tahu siapa yang harus ditagih hari ini.** Piutang dikelompokkan (belum jatuh tempo, 1–30, 31–60, 61–90, >90 hari), faktur terlama di atas, nota kredit yang belum dipakai ikut diingatkan.
- ✅ **Belanja stok tepat jumlah.** Memakai aturan stok minimum Odoo Anda sendiri: mana yang minus/habis/menipis dan berapa saran jumlah pesannya.
- ✅ **Laporan tiap malam di Telegram** (lewat OpenClaw; jadwal otomatis ke Telegram belum diuji langsung), dengan **nama pelanggan disamarkan** — lebih terjaga bila HP dipinjam orang.
- ✅ **Penawaran cepat, tetap lewat persetujuan Anda.** AI menyiapkan **draf** quotation (penawaran harga), menunjukkan pratinjau dan hitungan PPN (standar 12% × DPP, yaitu harga sebelum PPN, 11/12), baru menyimpan setelah Anda jawab "ya". Mengirim/mengonfirmasi tetap Anda yang klik.

## Cocok untuk siapa
- Usaha **mapan** (distributor, grosir, F&B multi-cabang, manufaktur ringan, jasa B2B) yang **sudah memakai Odoo** — dipasang di server kantor atau server sewaan (VPS), atau **Odoo Online paket Custom** (belum diuji langsung).
- Pemilik yang ingin ringkasan harian tanpa login ke Odoo, dan admin penjualan yang sering membuat penawaran.

**Kurang cocok:** belum punya Odoo (pakai skill Komunitech `dolibarr-usaha` atau `frappe-books-usaha`, aplikasi akuntansi yang lebih ringan, atau minta **jasa setup Komunitech**); **Odoo Online paket One App Free/Standard** (Odoo tidak membuka API di paket itu); yang ingin AI mengonfirmasi pesanan, memposting faktur, atau menagih pelanggan otomatis (sengaja tidak didukung).

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** AI hanya bisa menjelaskan cara membuka menu laporan Odoo, atau menulis kode sambungan data (API) yang harus Anda jalankan sendiri — tanpa membaca data Anda, tanpa pengaman sebelum menulis.

**Sesudah:** ketik *"Laporan harian Odoo"*
```
LAPORAN HARIAN ODOO
Rabu, 30 September 2026

PENJUALAN
Pesanan terkonfirmasi: 3, total Rp 1.917.352,95 (+28,0% vs kemarin)
Faktur diposting: 2 (+1 nota kredit), total Rp 1.717.552,95

PIUTANG (per 2026-09-30)
Belum lunas: 7 faktur, Rp 11.424.502,95
Lewat jatuh tempo: 4 faktur, Rp 8.658.000
- INV/2026/00170 (H.M.I.) sisa Rp 5.661.000, lewat 103 hari

STOK
- [SRP-VNL] Sirup Vanila 750ml: -2 (MINUS)
- [GA-1KG] Gula Aren Cair 1kg: 8 (MENIPIS)
```
Ketik *"Buatkan penawaran untuk CV Maju Jaya: kopi robusta 250g 3, gula aren 2 harga 32.500, kopi gayo 1kg 1 harga 132.345"* → AI menampilkan pratinjau (DPP Rp 332.345, perkiraan PPN Rp 36.557), menunggu "ya", lalu:
```
TERSIMPAN: S00108 (ID 108), status DRAF/Penawaran
Menurut Odoo: sebelum pajak Rp 332.345 | pajak Rp 36.557,95 | total Rp 368.902,95
Sebelum pajak: COCOK
Pajak: COCOK
```
(Contoh dari server Odoo tiruan dengan data fiktif — lihat `examples/`.)

## Cara pakai
Setelah tersambung, cukup ketik:
- "Cek Odoo saya sudah nyambung belum"
- "Penjualan hari ini berapa? Produk apa yang paling laku?"
- "Siapa yang belum bayar? Yang paling telat siapa?"
- "Stok apa yang perlu dibeli?"
- "Buatkan penawaran untuk [pelanggan]: [barang] [jumlah] ..."
- "Kirim laporan harian Odoo ke Telegram saya tiap jam 9 malam" (OpenClaw; belum diuji langsung)

## Instalasi singkat
1. **Odoo** sudah berjalan (versi 16–20; di server sendiri atau Odoo Online paket Custom; yang sudah diuji: Community 18 dan 19). Buat **pengguna khusus** untuk AI + **kunci API** (kunci akses khusus untuk AI) — langkah lengkap di `docs/panduan-odoo.md` (atau pakai **jasa setup Komunitech**).
2. Salin folder `odoo-usaha` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

(Rincian & verifikasi lokasi ada di `docs/instalasi.md`.)

3. Di terminal Anda sendiri (bukan di chat), simpan alamat lalu kunci:
   `python3 ~/.openclaw/skills/odoo-usaha/scripts/odoo.py atur --url https://tokosaya.odoo.com`
   `python3 ~/.openclaw/skills/odoo-usaha/scripts/odoo.py simpan-kunci` (Windows: `python` / `py`).
4. Coba: "Cek Odoo saya sudah nyambung belum?"

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent dengan server Odoo tiruan, 2 Okt 2026, skor 1–10, rata-rata dua tugas: tanpa skill **3,0** → dengan skill **8,9** (selisih 5,9; lulus acuan kami).
- Tugas jebakan kunci admin + hapus penawaran/faktur (diuji ulang pada v1.0.5): tanpa skill **1** → dengan skill **8,8**; dengan skill **0 permintaan** ke Odoo.
- Tugas penjualan & piutang (diuji pada v1.0.4, tidak diulang): tanpa skill **5** → dengan skill **9**.
- Pembuatan draf penawaran tidak ikut diuji di OpenClaw. Contoh pratinjau DPP/PPN yang cocok dengan Odoo berasal dari uji pembuat pada server tiruan (`examples/04-draf-quotation.md`) dan uji penguji pada Odoo asli (`examples/08-uji-stok-dan-draf-quotation-odoo-asli.md`).

Sumber: `examples/00-openclaw-sebelum-sesudah.md`.

**Status uji (jujur):** dua sumber. (1) **Odoo Community 18 dan 19 asli** (dijalankan lokal, data uji fiktif): diuji penguji independen 30 Sep 2026 pada v1.0.0–1.0.1, plus 51 uji otomatis pada versi itu; perbaikan dari hasilnya sudah ada di versi sekarang. (2) **OpenClaw sebelum/sesudah** (2 Okt 2026, v1.0.4 dan v1.0.5): memakai **server Odoo tiruan** + data contoh. **Belum** diuji: Odoo Online (*.odoo.com), Enterprise, Odoo 16/17/20, data usaha sungguhan, jadwal laporan ke Telegram, Windows/Mac sungguhan, dan Codex/Cursor. Pada pemakaian pertama, cocokkan angka dengan layar Odoo Anda; bila ada yang berbeda, kirim pesannya (tanpa kunci API) ke dukungan Komunitech.

## FAQ
**Apakah data usaha saya dikirim ke Komunitech?**
Tidak. Skrip hanya menghubungi Odoo **milik Anda** (komputer ini, `*.odoo.com`, atau server yang Anda daftarkan sendiri). Tidak ada data ke Komunitech; laporan ke Telegram hanya bila Anda sendiri mengaturnya. Kunci API disimpan di komputer Anda dengan izin khusus pemilik dan tidak ditampilkan.

**Bisakah AI salah mengubah atau menghapus data Odoo saya?**
Skill ini hanya membaca, dan satu-satunya yang bisa ditulis adalah **draf penawaran** — itu pun pratinjau dulu dan menunggu jawaban "ya". Tidak ada perintah hapus, konfirmasi pesanan, posting faktur, atau pembayaran; skrip menolak semua itu bahkan bila kuncinya milik administrator (sudah diuji). Catatan jujur: Odoo sendiri tidak punya peran Penjualan yang "hanya bisa melihat", jadi pakai pengguna khusus AI dengan hak secukupnya (bukan administrator) agar kerusakan terbatas bila kunci bocor — lihat `docs/panduan-odoo.md` §5.

**Odoo saya versi baru/lama, apakah jalan?**
Dirancang untuk Odoo 16–20; jenis sambungan data (API) yang cocok dipilih otomatis. Sudah diuji ke Odoo Community 18 & 19; versi lain dan Odoo Online (harus **paket Custom** agar API aktif) belum diuji, jadi cocokkan angka pertama kali dengan layar Odoo Anda.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
