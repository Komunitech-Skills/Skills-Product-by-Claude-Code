# Arsip Nota Otomatis, Tanpa Langganan

**Nota & struk yang berantakan di HP jadi arsip rapi di komputer sendiri - cukup ngobrol.**

## Manfaat
- ✅ File foto/PDF nota diberi nama baku (`2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg`) dan tersusun otomatis per folder tahun/bulan - tidak perlu klik-klik Explorer/Finder satu-satu.
- ✅ Semua nota tercatat di satu indeks lokal: cari nota vendor tertentu atau rentang tanggal dalam hitungan detik, tanpa scroll ratusan foto.
- ✅ Ketahuan kalau ada nota yang kebetulan diarsipkan dua kali (isi file sama persis maupun kemungkinan dobel).
- ✅ Rekap pengeluaran per kategori/vendor sekali ketik, dan bisa diekspor langsung ke buku kas (`kas-umkm`).
- ✅ Data 100% di komputer sendiri, tidak ada langganan bulanan, tidak ada upload ke internet. File nota asli **tidak pernah dihapus**.

## Cocok untuk siapa
- Pemilik UMKM/toko yang notanya menumpuk di galeri HP dan sulit dicari saat butuh (klaim garansi, cek harga beli, laporan pajak).
- Freelancer/pemilik usaha kecil yang ingin arsip pengeluaran rapi tanpa berlangganan aplikasi arsip dokumen berbayar.
- Siapa pun yang sudah pakai `ekstrak-nota-faktur` untuk membaca isi nota, dan ingin hasilnya langsung tersimpan rapi.

## Contoh sebelum & sesudah
**Sebelum:** folder unduhan/galeri berisi `IMG_20260920_1.jpg`, `WhatsApp Image 2026-09-21.jpeg`, `Scan001.pdf` — tidak jelas nota siapa, tanggal berapa, atau sudah pernah dicatat belum.

**Sesudah (cukup ketik):** "Arsipkan nota-nota ini, dari Toko Sembako Bu Yati tanggal 20 September 150 ribu, dan dari Toko C tanggal 22 September 50 ribu."
→ Agent menunjukkan pratinjau nama file barunya, minta konfirmasi, lalu menyimpan ke `arsip/2026/09/2026-09-20_Toko-Sembako-Bu-Yati_150000.jpg` dan `arsip/2026/09/2026-09-22_Toko-C_50000.jpg`, tercatat di indeks, dan file lama tetap ada.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Rapikan nota-nota ini, tanggal dan nominalnya begini: ..."
- "Cari nota Toko Sembako Bu Yati bulan lalu"
- "Rekap pengeluaran per kategori bulan September"
- "Ada nota yang keinput dobel nggak?"

Untuk membaca angka dari foto nota (bukan sekadar arsip nama file), gunakan bersama skill `ekstrak-nota-faktur` (hasilnya diarsipkan otomatis oleh skill ini).

## Instalasi singkat
Salin folder `arsip-nota` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**File nota asli saya bisa hilang/terhapus?**
Tidak. Mode bawaan adalah **salin** — file asli tetap di tempatnya, hanya salinannya yang diarsipkan dan diberi nama baku. Ada juga mode "pindah" (opsional) yang hanya memindahkan file ke lokasi baru, tetap tidak pernah menghapus.

**Skill ini bisa membaca angka di foto nota (OCR)?**
Tidak. arsip-nota khusus merapikan file & mencatat data yang sudah ada. Untuk membaca subtotal/PPN/total dari foto, pakai skill `ekstrak-nota-faktur`, lalu hasilnya diarsipkan otomatis oleh skill ini.

**Data saya dikirim ke internet?**
Tidak. Semua data (foto nota dan indeksnya) tersimpan di file di komputer kamu sendiri (SQLite), tidak ada langganan bulanan dan tidak ada yang diunggah.
