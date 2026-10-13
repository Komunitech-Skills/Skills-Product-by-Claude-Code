# InvenTree Gudang: Asisten AI Stok & Opname Tanpa Langganan

**Tanya "stok singkong berapa, di rak mana?", "barang apa yang hampir habis?", atau "bahan cukup untuk produksi 300 bungkus?" — AI Anda langsung membaca InvenTree, aplikasi gudang gratis yang jalan di komputer sendiri. Stock opname dan penerimaan barang dari supplier jadi rapi, tercatat, dan selalu minta persetujuan Anda dulu.**

> Komunitech **tidak berafiliasi** dengan proyek InvenTree. InvenTree adalah software open-source (lisensi MIT) milik komunitas pengembangnya; skill dan panduan ini adalah karya orisinal Komunitech untuk memudahkan pemakaiannya oleh usaha Indonesia.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan: Inventree (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tanpa biaya bulanan per gudang/pengguna.** InvenTree gratis dan jalan di komputer/server Anda sendiri; data stok tidak dititipkan ke aplikasi pihak lain.
- ✅ **Cukup ngobrol.** "Stok minyak goreng?", "isi Rak A apa saja?", "PO mana yang belum datang?" — jawaban lengkap per lokasi dan per batch, angka gaya Indonesia (1.200 / 12,5).
- ✅ **Stock opname tanpa drama.** AI membuatkan lembar hitung (bisa dibuka di Excel), petugas mengisi, AI menunjukkan selisih per barang, baru disimpan setelah Anda setuju. Kalau ada barang keluar-masuk di tengah opname, AI **berhenti** alih-alih menimpa angka yang benar.
- ✅ **Barang datang, langsung tercatat.** Terima barang dari PO lengkap dengan kode batch & tanggal kedaluwarsa; kelebihan dari jumlah pesanan ditolak otomatis.
- ✅ **Tahu bisa produksi berapa.** Dari BOM (resep/daftar bahan), AI menghitung kebutuhan bahan untuk N unit, bahan mana yang kurang dan berapa, serta maksimal unit yang bisa dibuat dari stok sekarang — dihitung script, bukan dikira.
- ✅ **Laporan gudang tiap pagi di Telegram** (lewat OpenClaw): stok menipis, PO terbuka/terlambat, produksi terbuka.

## Cocok untuk siapa
- Usaha **manufaktur kecil–menengah** (makanan ringan, konveksi, sabun/kosmetik rumahan, percetakan, bengkel rakit) yang punya bahan baku, resep/BOM, dan perintah produksi.
- **Distributor / grosir / toko bangunan** dengan beberapa gudang atau rak, barang ber-batch/kedaluwarsa, dan pembelian rutin ke supplier.
- Admin gudang yang ingin stock opname dan penerimaan barang lebih tertib tanpa belajar menu aplikasi yang rumit.

**Kurang cocok:** seller marketplace solo tanpa komputer yang menyala terus (pakai skill `buku-stok`, lebih sederhana); yang butuh akuntansi/nilai rupiah persediaan (InvenTree fokus jumlah barang; pasangkan dengan `frappe-books-usaha`/`hitung-hpp`); yang ingin AI membuat PO/mengirim pesanan ke supplier otomatis (sengaja tidak didukung).

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** AI hanya bisa memberi saran umum cara opname, atau menebak alamat API dan format data InvenTree — tanpa membaca stok Anda yang sebenarnya, tanpa pengaman sebelum mengubah data.

**Sesudah:** ketik *"Bahan cukup untuk produksi 300 bungkus keripik balado?"*
```
KEBUTUHAN BAHAN: 300 unit Keripik Singkong Balado 250g [PJ-001]
- Singkong Kupas [BB-001]: butuh 90 kg, tersedia 85 -> KURANG 5 kg; sedang dipesan 200
- Minyak Goreng [BB-002]: butuh 15 L, tersedia 28 -> CUKUP
- Bumbu Balado [BB-003]: butuh 6 kg, tersedia 12,5 -> CUKUP
- Standing Pouch 250g [KM-001]: butuh 300, tersedia 1.200 -> CUKUP
- Label Stiker Sumber Rasa [KM-002]: butuh 300, tersedia 300 -> CUKUP

Kesimpulan: BAHAN BELUM CUKUP untuk 300 unit. Maksimal dari stok sekarang: 283 unit.
```
Ketik *"Singkong 150 kg dan minyak 40 liter dari CV Tani Makmur sudah datang, batch SK-2909"*:
```
PRATINJAU TERIMA BARANG PO-0001 dari CV Tani Makmur (fiktif)
Masuk ke lokasi: Gudang Utama/Rak A
Kode batch: SK-2909
- Singkong Kupas [BB-001]: terima 150 kg (sisa pesanan 200)
- Minyak Goreng [BB-002]: terima 40 L (sisa pesanan 40)

Belum disimpan. Cocokkan dengan surat jalan/nota pemasok. Bila benar, ulangi perintah + --ya.
```
(Contoh nyata dari uji dengan InvenTree 1.5.6 asli dan data fiktif — lihat `examples/`.)

## Cara pakai
Setelah InvenTree terpasang dan tersambung, cukup ketik:
- "Cek InvenTree saya sudah nyambung belum"
- "Stok bumbu balado berapa?", "Isi Rak B apa saja?"
- "Barang apa yang perlu dibeli minggu ini?"
- "Buatkan lembar stock opname Rak A" → (isi) → "Ini hasil hitungnya, cek selisihnya"
- "PO apa yang belum datang?", "Barang dari supplier X datang, ..."
- "Bahan produk PJ-001 apa saja?", "Bisa produksi berapa bungkus?"
- "Ekspor stok ke Excel"
- "Kirim laporan gudang ke Telegram saya tiap jam 7 pagi" (OpenClaw)

## Instalasi singkat
1. **InvenTree** sudah terpasang dan menyala. Belum? Ikuti `docs/panduan-inventree.md` di paket (Docker resmi, ±30–60 menit), **termasuk langkah pengamanan wajib** (hanya bisa dibuka dari komputer sendiri) dan setelan mata uang Rupiah — atau pakai **jasa setup Komunitech**.
2. Salin folder `inventree-gudang` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

(Rincian & verifikasi lokasi ada di `docs/instalasi.md`.)

3. Buat akun khusus + token API di InvenTree (panduan §6), lalu simpan sekali di terminal Anda sendiri (bukan di chat): `python3 ~/.openclaw/skills/inventree-gudang/scripts/inventree.py simpan-kunci` (Windows: `python` / `py`).
4. Coba: "Cek InvenTree saya sudah nyambung belum?"

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.6), skor 1–10: tanpa skill **4,5** → dengan skill **9,0** (LULUS). Jebakan token admin + "hapus semua stok": dengan skill **0 permintaan** ke API, minta cabut token; stok menipis dengan angka produksi maksimal **60 bungkus** (data contoh). Sumber: `examples/00-openclaw-sebelum-sesudah.md`, `promosi/sebelum-sesudah.jsonl`.

**Status uji (jujur):** diuji OpenClaw sebelum/sesudah dengan **server tiruan** InvenTree 1.5.6 (2026-10-02), bukan instalasi Docker asli di sesi uji otomatis. InvenTree asli diuji pembuat secara terpisah (`examples/`). Codex/Cursor belum uji platform asli.

## FAQ
**Apakah data stok saya dikirim ke Komunitech atau pihak lain?**
Tidak. Script hanya menghubungi InvenTree **milik Anda sendiri** (biasanya `localhost`). Tidak ada data ke Komunitech atau internet, kecuali Anda sendiri mengatur laporan ke Telegram.

**Bisakah AI salah mengubah stok saya?**
Setiap perubahan (opname, terima barang) selalu ditampilkan dulu sebagai pratinjau dan baru disimpan setelah Anda menjawab "ya". Untuk chat harian dan laporan otomatis disarankan memakai akun InvenTree yang **hanya bisa melihat** — InvenTree sendiri akan menolak perubahan dari akun itu. Semua perubahan tercatat di riwayat stok InvenTree.

**Saya belum pernah pakai InvenTree. Apakah sulit?**
Pemasangan butuh komputer/mini PC yang menyala terus dan Docker; panduan langkah demi langkah ada di paket, atau Komunitech bisa memasangkan (jasa berbayar). Data awal (daftar barang, lokasi, BOM, supplier) diisi sekali di layar InvenTree atau diimpor dari Excel; setelah itu pekerjaan harian cukup lewat chat.
