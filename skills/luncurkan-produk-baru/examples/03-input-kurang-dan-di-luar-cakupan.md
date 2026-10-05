# Contoh 3: Input kurang, dan permintaan di luar cakupan (fiktif)

**Input kurang.** Pengguna: "mau launching produk baru."
Agen (satu pesan, satu daftar): "Supaya rencananya pas, jawab singkat ya: 1) produknya apa & harganya? 2) tanggal launching (atau 'secepatnya')? 3) makanan/minuman, kosmetik, atau lainnya? 4) kontak WA/pengikut IG/toko marketplace yang sudah ada? 5) anggaran promo+iklan? Kalau mau cepat, balas 'pakai default': aku asumsikan produk non-makanan, tanggal 35 hari dari sekarang, dan hanya kanal gratis."

**Di luar cakupan.** Pengguna: "Bantu launching aplikasi saya di Product Hunt dan tulis kontrak investor."
Agen: skill ini untuk produk usaha UMKM; peluncuran aplikasi/Product Hunt dan kontrak investor di luar cakupan. Untuk kontrak, konsultasikan ke penasihat hukum. Bila ada produk fisik/jasa yang ikut diluncurkan, saya bisa bantu jadwalnya.

**Tanggal salah.** `python3 scripts/jadwal_peluncuran.py --tanggal 14/11/2026`
Keluaran: `Galat: tanggal '14/11/2026' tidak valid; pakai format TTTT-BB-HH, mis. 2026-11-14` (kode keluar 2).
