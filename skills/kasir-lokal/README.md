# Kasir Toko Tanpa Langganan, Cukup Lewat Chat

**Catat penjualan, cetak struk, tutup kasir, dan siapkan rekap harian untuk dikirim ke Telegram (lewat OpenClaw) — data kasir disimpan di komputer Anda sendiri.**

Diuji AI penguji independen di OpenClaw: 6,5 → 8,5 dari 10 (pajak resto diluruskan sebagai PBJT, bukan PPN, dan nota bernomor urut tersimpan di komputer Anda).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tanpa biaya bulanan.** Pengganti fitur dasar aplikasi kasir berlangganan (Moka, Majoo, Olsera, dsb.) untuk satu toko. Data tersimpan di satu file di komputer Anda, bukan di server orang lain.
- ✅ **Cukup ketik seperti biasa.** "2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb" → nota bernomor, total, dan kembalian langsung jadi. Produk yang tidak jelas ditanyakan, bukan ditebak.
- ✅ **Struk rapi 58 mm / 80 mm** siap dicetak ke printer thermal (printer struk kecil di kasir) dari browser, atau dikirim sebagai teks ke WhatsApp pembeli.
- ✅ **Uang laci jelas.** Buka kasir dengan modal, tutup kasir dengan hitungan uang fisik: kelihatan pas, lebih, atau kurang berapa, plus setoran ke pemilik. Salah catat dibatalkan dengan alasan, tidak dihapus diam-diam.
- ✅ **Rekap siap kirim & bahan untuk pajak.** Omzet, diskon, retur, per metode bayar, produk terlaris, jam ramai; file CSV (file tabel yang bisa dibuka di Excel); omzet bulanan untuk PPh final 0,5%; opsi **PBJT (pajak resto/kafe)** sesuai tarif Perda daerah Anda + biaya layanan (service charge), atau PPN 12% (DPP nilai lain 11/12) untuk toko PKP (Pengusaha Kena Pajak).

## Cocok untuk siapa
- Warung, toko kelontong, kedai kopi, kafe, warung makan, toko kue, toko bangunan (sak, m3, meter), kios, butik kecil — **satu outlet, satu komputer kasir**.
- Pemilik yang ingin laporan penjualan harian masuk ke Telegram tanpa buka aplikasi (lewat OpenClaw; jadwal terjadwal sudah diuji langsung di Telegram, Oktober 2026).
- Toko yang sudah memakai skill **Buku Stok** dan ingin stoknya terpotong dari penjualan kasir.

**Kurang cocok:** banyak kasir di perangkat berbeda sekaligus, atau yang butuh aplikasi kasir di HP/tablet. Punya beberapa cabang? Bisa dengan satu file data (database) per cabang lalu laporan digabung manual (bukan sinkron otomatis).

## Contoh sebelum & sesudah
**Sebelum:** penjualan dicatat di buku tulis, total dihitung kalkulator, malam hari uang laci selisih dan tidak tahu sebabnya. Rekap bulanan untuk pajak dikerjakan akhir bulan sambil membongkar nota.

**Sesudah (cukup ketik):** "2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb"
→
```
Nota N-260924-0001 (belum disimpan):
1. Kopi Susu Gula Aren 2 x Rp 18.000 = Rp 36.000
2. Roti Bakar Coklat 1 x Rp 15.000 = Rp 15.000
Subtotal Rp 51.000 | Diskon 10% -Rp 5.100
TOTAL Rp 45.900 | Tunai Rp 100.000 | Kembalian Rp 54.100
Simpan? Balas "ya".
```
Malamnya: "tutup kasir, uang di laci 225 ribu, setor 125 ribu" → "Seharusnya Rp 225.900, dihitung Rp 225.000, SELISIH KURANG Rp 900."

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Pakai kasir untuk toko saya, ini daftar produknya" (kirim file Excel/CSV)
- "Buka kasir, modal 200 ribu"
- "3 es teh, 1 nasi goreng, bayar QRIS"
- "Cetak struk nota tadi, kertas 58"
- "Batalkan nota terakhir, salah input"
- "Tutup kasir, uang di laci 1.250.000"
- "Rekap kasir hari ini" / "rekap bulan September" / "omzet tahun ini untuk pajak"
- "Kirim rekap kasir ke Telegram saya tiap jam 9 malam" (OpenClaw; jadwal terjadwal sudah diuji langsung di Telegram)
- "Ini nota hari ini (tempel daftar nota), rekap + cocokkan laci + bikinin laporan buat grup karyawan" — tanpa perlu menyimpan data dulu: nota batal tidak dihitung, porsi & jumlah nota dipisah, dan ringkasan untuk grup tidak memuat nama/nomor pelanggan atau bon per orang

**Mencetak struk ke printer thermal:** agent membuat file struk (berformat HTML, bisa dibuka di browser). Buka file itu di browser (Chrome/Edge) → tekan **Ctrl+P** (Mac: Cmd+P) → pilih printer thermal → ukuran kertas 58 mm atau 80 mm → Margin: **None/Tidak ada** → Skala **100%** → matikan **Header dan footer** → Cetak. Pastikan driver printer thermal sudah terpasang di komputer. Pengaturan ini cukup sekali; browser biasanya mengingatnya.

## Instalasi singkat
Salin folder `kasir-lokal` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex (belum diuji langsung) | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor (belum diuji langsung) | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

Butuh **Python 3.8+** (gratis di python.org; Mac/Linux biasanya sudah ada). Tidak butuh internet, akun, atau API key. Data tersimpan di `KomunitechData/kasir/` di folder pengguna Anda; backup otomatis dibuat saat tutup kasir.

**Hasil uji (angka nyata):** uji di OpenClaw, 1 Okt 2026 (v1.1.7), skor 1–10 dari agen penguji independen: tanpa skill 6,5 → dengan skill 8,5.
- Tugas: "2 kopi susu dan 1 roti bakar, diskon 10%, bayar tunai 100 ribu, buatkan struknya" (harga menu di uji ini berbeda dari contoh di atas). Tanpa skill, angkanya benar tetapi pajak resto 10% disebut PPN (jenis pajaknya salah) dan catatannya tidak terstruktur. Dengan skill: total Rp 35.100, kembalian Rp 64.900, nota bernomor urut tersimpan di komputer Anda, struk 58 mm siap cetak, dan pajak resto diluruskan sebagai PBJT, bukan PPN.
- Jujur: untuk satu transaksi saja, hasil tanpa skill juga benar. Nilai tambahnya ada di penyimpanan data yang rapi, nomor nota urut, tutup kasir, rekap, dan jenis pajak yang tepat.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis oleh agen AI, bukan oleh manusia) dan Claude Code (simulasi agen penguji). Codex dan Cursor memakai format SKILL.md yang sama, tetapi belum kami uji langsung. Jadwal kirim otomatis ke Telegram: diuji langsung di Telegram (Oktober 2026; rekap harian one-shot ~5 menit, angka Rp 51.000 cocok; rincian di `examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`).

## Yang perlu Anda tahu (jujur)
- **Bukan mesin pembayaran.** Kasir hanya *mencatat* bahwa pembeli membayar tunai/QRIS/transfer/debit. Tidak membuat QRIS dinamis, tidak menarik kartu, tidak mengecek uang masuk. Cocokkan QRIS/transfer dengan mutasi bank Anda (angkanya ada di laporan tutup kasir).
- **Satu outlet, satu komputer.** Jangan membuka file database yang sama dari dua komputer (mis. lewat Google Drive).
- **Pajak:** restoran/kafe/warung makan yang sudah terdaftar di Bapenda (Badan Pendapatan Daerah) memungut **PBJT** (pajak daerah, UU 1/2022), bukan PPN — kasir bisa menghitung dan mencetaknya, tetapi **tarifnya Anda isi sendiri** sesuai Perda daerah (paling tinggi 10%), dan penyetoran/pelaporan tetap Anda lakukan ke Bapenda. PPN hanya untuk toko non-kuliner yang sudah **PKP**. Pembulatan PBJT belum dicocokkan dengan sistem Bapenda. PPh final 0,5% tidak dicetak di struk; kasir menyiapkan omzetnya dan skill **PPh Final UMKM** yang menghitung. Pembulatan PPN belum dicocokkan dengan Coretax (sistem pajak DJP). Ini alat bantu catat, bukan nasihat pajak.
- Kecepatan: setiap transaksi dikonfirmasi dulu lewat chat, jadi cocok untuk toko dengan antrean santai, bukan kasir supermarket yang memindai barcode tiap detik.
- **Dasar aturan & tanggal berlaku:** PBJT mengikuti UU 1/2022 (HKPD); PPN 12% dengan DPP nilai lain 11/12 mengikuti UU HPP dan PMK 131/2024; PPh final 0,5% mengikuti PP 55/2022 jo. PP 20/2026. Semuanya berlaku per 24 September 2026. Aturan pajak bisa berubah, jadi cek ke DJP (Kring Pajak 1500200), Bapenda, atau konsultan pajak untuk kasus khusus.

## FAQ
**Apakah data saya dikirim ke internet?**
Tidak. Script (program kecil) kasir tidak memakai internet; data penjualan tersimpan di satu file di komputer Anda. Yang terkirim hanya teks rekap yang Anda minta dikirim ke Telegram (lewat OpenClaw). Percakapan dengan AI agent Anda tetap diproses oleh penyedia AI yang Anda pakai.

**Kalau salah catat atau pembeli mengembalikan barang?**
Bilang saja "batalkan nota N-… karena salah input" atau "retur 1 es teh dari nota N-…, tumpah". Kasir membuat catatan pembalik dengan alasan; nota asli tetap tersimpan sehingga riwayat tidak dihapus diam-diam dan hitungan uang laci tetap konsisten.

**Printer saya thermal 80 mm / hanya punya printer biasa, bisa?**
Bisa. Pilih struk 80 mm untuk printer 80 mm. Untuk printer biasa (A4), struk tetap bisa dicetak, atau kirim struk sebagai teks/foto ke WhatsApp pembeli. Yang penting printer terpasang di komputer dan bisa mencetak dari browser.

**Ada pembeli yang belum bayar (ngutang/bon)?**
Kasir ini sengaja hanya mencatat penjualan yang sudah dibayar. Kalau ada pelanggan bon, catat di skill **Buku Piutang** — nanti kelihatan siapa berutang berapa, kapan jatuh temponya, dan ada draf pesan tagihan siap kirim. Belum pasang Buku Piutang? Cara lama masih bisa: buat tagihannya dengan skill **Buat Invoice**, lalu kalau sudah lewat jatuh tempo, susun pesan penagihannya dengan skill **Tagih Piutang**.

## Riwayat perubahan

Versi terkini: **1.1.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
