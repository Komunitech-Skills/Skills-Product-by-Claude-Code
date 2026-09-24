# Kasir Toko Tanpa Langganan, Cukup Lewat Chat

**Catat penjualan, cetak struk, tutup kasir, dan terima rekap harian di Telegram — semua data tetap di komputer Anda sendiri.**

## Manfaat
- ✅ **Tanpa biaya bulanan.** Pengganti fitur dasar aplikasi kasir berlangganan (Moka, Majoo, Olsera, dsb.) untuk satu toko. Data tersimpan di satu file di komputer Anda, bukan di server orang lain.
- ✅ **Cukup ketik seperti biasa.** "2 kopi susu, 1 roti bakar, diskon 10%, bayar tunai 100rb" → nota bernomor, total, dan kembalian langsung jadi. Produk yang tidak jelas ditanyakan, bukan ditebak.
- ✅ **Struk rapi 58 mm / 80 mm** siap dicetak ke printer thermal dari browser, atau dikirim sebagai teks ke WhatsApp pembeli.
- ✅ **Uang laci jelas.** Buka kasir dengan modal, tutup kasir dengan hitungan uang fisik: kelihatan pas, lebih, atau kurang berapa, plus setoran ke pemilik. Salah catat dibatalkan dengan alasan, tidak dihapus diam-diam.
- ✅ **Rekap siap kirim & siap pajak.** Omzet, diskon, retur, per metode bayar, produk terlaris, jam ramai; file CSV untuk Excel; omzet bulanan untuk PPh final 0,5%; opsi PPN 12% (DPP 11/12) untuk toko PKP.

## Cocok untuk siapa
- Warung, toko kelontong, kedai kopi, toko kue, kios, toko oleh-oleh, butik kecil — **satu outlet, satu komputer kasir**.
- Pemilik yang ingin laporan penjualan harian masuk ke Telegram tanpa buka aplikasi.
- Toko yang sudah memakai skill **Buku Stok** dan ingin stoknya terpotong dari penjualan kasir.

**Kurang cocok:** banyak cabang, banyak kasir di perangkat berbeda sekaligus, atau yang butuh aplikasi kasir di HP/tablet.

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
- "Kirim rekap kasir ke Telegram saya tiap jam 9 malam" (OpenClaw)

**Mencetak struk ke printer thermal:** agent membuat file struk (HTML). Buka file itu di browser (Chrome/Edge) → tekan **Ctrl+P** (Mac: Cmd+P) → pilih printer thermal → ukuran kertas 58 mm atau 80 mm → Margin: **None/Tidak ada** → Skala **100%** → matikan **Header dan footer** → Cetak. Pastikan driver printer thermal sudah terpasang di komputer. Pengaturan ini cukup sekali; browser biasanya mengingatnya.

## Instalasi singkat
Salin folder `kasir-lokal` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

Butuh **Python 3.8+** (gratis di python.org; Mac/Linux biasanya sudah ada). Tidak butuh internet, akun, atau API key. Data tersimpan di `KomunitechData/kasir/` di folder pengguna Anda; backup otomatis dibuat saat tutup kasir.

## Yang perlu Anda tahu (jujur)
- **Bukan mesin pembayaran.** Kasir hanya *mencatat* bahwa pembeli membayar tunai/QRIS/transfer/debit. Tidak membuat QRIS dinamis, tidak menarik kartu, tidak mengecek uang masuk. Cocokkan QRIS/transfer dengan mutasi bank Anda (angkanya ada di laporan tutup kasir).
- **Satu outlet, satu komputer.** Jangan membuka file database yang sama dari dua komputer (mis. lewat Google Drive).
- **Pajak:** PPN hanya untuk toko yang sudah **PKP**. Warung makan/kafe/restoran umumnya kena **pajak daerah (PBJT)**, bukan PPN — versi ini belum menghitung PBJT; tanyakan ke Bapenda setempat. PPh final 0,5% tidak dicetak di struk; kasir menyiapkan omzetnya dan skill **PPh Final UMKM** yang menghitung. Pembulatan PPN belum dicocokkan dengan Coretax. Ini alat bantu catat, bukan nasihat pajak.
- Kecepatan: setiap transaksi dikonfirmasi dulu lewat chat, jadi cocok untuk toko dengan antrean santai, bukan kasir supermarket yang memindai barcode tiap detik.

## FAQ
**Apakah data saya dikirim ke internet?**
Tidak. Script kasir tidak memakai internet sama sekali; semua tersimpan di satu file di komputer Anda. Yang terkirim hanya teks rekap yang Anda minta dikirim ke Telegram (lewat OpenClaw).

**Kalau salah catat atau pembeli mengembalikan barang?**
Bilang saja "batalkan nota N-… karena salah input" atau "retur 1 es teh dari nota N-…, tumpah". Kasir membuat catatan pembalik dengan alasan; nota asli tetap tersimpan sehingga riwayat tidak bisa dihapus diam-diam dan uang laci tetap cocok.

**Printer saya thermal 80 mm / hanya punya printer biasa, bisa?**
Bisa. Pilih struk 80 mm untuk printer 80 mm. Untuk printer biasa (A4), struk tetap bisa dicetak, atau kirim struk sebagai teks/foto ke WhatsApp pembeli. Yang penting printer terpasang di komputer dan bisa mencetak dari browser.
