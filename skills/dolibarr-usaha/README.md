# Dolibarr Usaha: Asisten AI untuk Dolibarr Anda

**Ketik "buatkan invoice untuk CV Maju Jaya", "siapa yang belum bayar?", atau "stok apa yang mau habis?". AI Anda langsung membaca dan menyiapkan data di Dolibarr, program pembukuan-stok-CRM gratis yang jalan di komputer sendiri, tanpa biaya bulanan.**

## Manfaat
- ✅ **Invoice dalam satu kalimat.** Pelanggan dan barang dicari otomatis, PPN 12% × DPP 11/12 dihitung, lalu dibuat sebagai **draf** di Dolibarr. Setelah itu angkanya dicocokkan dengan hitungan Dolibarr, dan bila beda sepeser pun Anda diberi tahu.
- ✅ **Tahu siapa yang belum bayar.** Daftar piutang dikelompokkan per umur (belum jatuh tempo, telat 1–30, 31–60, 61–90, >90 hari), yang paling lama telat di atas.
- ✅ **Stok tidak kecolongan.** Barang habis, minus, dan menipis muncul lengkap dengan saran jumlah beli. Bila modul Stok tidak dipakai, skill mengatakannya terus terang, tanpa alarm "habis" palsu.
- ✅ **Laporan tiap malam ke Telegram.** Penjualan hari ini dibanding kemarin, piutang terlambat, dan stok menipis, dikirim otomatis lewat OpenClaw.
- ✅ **Aman untuk data usaha.** Default hanya membaca. Menulis (pelanggan baru, draf invoice) selalu lewat pratinjau dan butuh persetujuan Anda. Validasi, pembayaran, dan hapus tetap Anda yang pegang. Kunci akses disimpan aman dan tidak pernah ditampilkan.

## Cocok untuk siapa
- UMKM & usaha mapan yang memakai (atau ingin pindah ke) **Dolibarr** di komputer sendiri, biasanya lewat **DoliWamp** di Windows, sebagai pengganti Jurnal/Accurate + Moka/Majoo + CRM berbayar.
- Pemilik yang ingin cukup bertanya ke AI (OpenClaw, Claude Code, Codex, Cursor) tanpa menghafal menu Dolibarr.
- Admin kantor yang sering membuat invoice dan menagih piutang.

**Kurang cocok:** belum punya Dolibarr dan tidak ingin memasangnya (pakai skill **Buat Invoice** atau **Buku Stok**); Dolibarr di hosting tanpa HTTPS; butuh e-Faktur resmi (tetap lewat Coretax DJP).

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
(Contoh nyata dari uji dengan Dolibarr 24.0.1.)

## Cara pakai
Setelah terpasang dan terhubung, cukup ketik permintaan biasa:
- "Cek Dolibarr saya sudah nyambung belum"
- "Cari pelanggan Maju", "Tambah pelanggan Warung Bu Sari, 0812-3456-7890, Solo"
- "Buatkan invoice untuk CV Maju Jaya: 3 kopi KPI-250, jatuh tempo 30 hari"
- "Siapa saja yang belum bayar?", "Piutang yang telat lebih dari sebulan"
- "Stok apa yang mau habis?", "Stok kopi tinggal berapa?"
- "Kirim laporan Dolibarr ke Telegram saya tiap jam 9 malam" (OpenClaw)

## Instalasi singkat
1. **Dolibarr** sudah terpasang dan modul API aktif. Belum? Ikuti `docs/panduan-dolibarr.md` di paket (Windows lewat DoliWamp ±30–60 menit), **termasuk langkah pengamanan wajib 2.4** (ganti sandi database bawaan, pastikan hanya bisa dibuka dari komputer sendiri, jangan buka ke internet), atau pakai **jasa setup Komunitech**.
2. Salin folder `dolibarr-usaha` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

3. Simpan kunci API sekali (di terminal Anda sendiri, bukan di chat): `python3 ~/.openclaw/skills/dolibarr-usaha/scripts/dolibarr.py simpan-kunci` (Windows: `python` / `py`).

Panduan pemasangan skill lengkap: `CARA-INSTAL.md` di paket. Butuh **Python 3.8+** (gratis di python.org). Tidak butuh internet, akun, atau paket tambahan.

**Status uji jujur (versi 1.0.3):** diuji dengan Dolibarr asli **24.0.1 dan 22.0.4** (versi DoliWamp terbaru) di Linux, uji independen v1.0.0 s.d. v1.0.2 (lulus 8/10; dua temuan sisa, pencegah draf dobel untuk harga bersen dan urutan kunci, diperbaiki di 1.0.3 dan menunggu uji ulang independen), uji otomatis, dan jadwal OpenClaw 2026.9.6 (tanpa pengiriman Telegram sungguhan). **Belum** diuji di DoliWamp Windows sungguhan; versi Dolibarr lain akan diberi tanda "belum diuji".

## FAQ
**Apakah AI bisa salah mengirim atau menghapus invoice saya?**
Tidak lewat skill ini: script tidak punya perintah validasi, kirim, bayar, atau hapus. Invoice selalu dibuat sebagai draf dan Anda yang memvalidasi di Dolibarr; membuat pelanggan/draf pun harus lewat pratinjau dan persetujuan Anda. Jujur saja: di Dolibarr, kunci yang boleh membuat invoice secara teknis juga bisa memvalidasi/menandai lunas lewat API. Karena itu panduan menyarankan kunci **baca-saja** untuk laporan harian dan kunci terpisah untuk membuat draf (`docs/panduan-dolibarr.md` bagian 6).

**Kenapa PPN di Dolibarr kadang beda Rp 1 dengan hitungan skill?**
Dolibarr menghitung PPN per baris lalu membulatkan ke terdekat, sedangkan standar Komunitech menghitung dari total lalu membulatkan ke bawah (agar tidak pernah memungut melebihi tarif). Skill menampilkan keduanya dan tidak mengubah apa pun. Nilai PPN resmi tetap mengikuti faktur di Coretax.

**Apakah data saya dikirim ke internet?**
Tidak oleh skill ini. Script hanya berbicara dengan Dolibarr di komputer Anda (`localhost`) dan menolak alamat lain kecuali Anda menegaskannya (wajib HTTPS untuk alamat internet). Laporan Telegram dikirim oleh OpenClaw milik Anda, hanya ke chat Anda.

---
Komunitech tidak berafiliasi dengan proyek Dolibarr; Dolibarr adalah merek milik pemiliknya.
