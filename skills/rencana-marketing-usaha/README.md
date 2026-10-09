# Rencana Marketing Usaha — dari "bingung mulai" jadi rencana siap jalan

**Tagline:** Satu kalimat dari Anda, satu rencana marketing lengkap dengan angka anggarannya.

## Manfaat
- **Rencana lengkap dalam satu dokumen:** tujuan terukur, target pasar, pesan, kanal, kalender, anggaran, KPI.
- **Angka dihitung, bukan dikira:** pembagian anggaran per kanal, batas biaya per pelanggan (CAC), ROAS impas, dan anggaran iklan maksimal dihitung script dari margin Anda.
- **Cocok untuk modal kecil:** mulai dari WhatsApp, Google Maps, Instagram, TikTok, marketplace; iklan berbayar hanya bila margin sehat.
- **Kalender Indonesia:** gajian, 11.11/12.12, Ramadan-Lebaran, tahun ajaran baru, akhir tahun.
- **Terhubung ke skill lain:** kalender konten, promo, audit iklan, laporan iklan, KPI tim, riset pelanggan.

## Cocok untuk siapa
Pemilik warung/kedai/toko online, jasa lokal, reseller, freelancer, dan usaha mapan yang belum punya rencana marketing tertulis. Tidak butuh istilah teknis.

## Sebelum / sesudah
**Sebelum:** "Budget iklan Rp 6 juta saya taruh di mana ya? Posting kalau sempat saja."
**Sesudah:** rencana 12 bagian: tujuan 120 -> 200 pesanan/bulan, 5 kanal dengan Rp per kanal, kalender gajian/11.11/12.12, batas CAC Rp 10.000, KPI mingguan, aturan berhenti bila iklan tidak menguntungkan. Lihat `examples/01-kedai-kopi-q4.md`.

## Cara pakai
Ketik contoh: *"Bikin rencana marketing 3 bulan untuk toko hijab saya, budget Rp 5 juta, target omzet Rp 40 juta."* Skill akan bertanya sekali soal harga, HPP, tempat jualan, dan waktu luang, lalu menyusun rencana. Jika Anda buru-buru, ia memakai asumsi yang disebut di awal dokumen.

## Instalasi singkat
Salin folder `rencana-marketing-usaha` ke lokasi skill di platform Anda (OpenClaw, OpenAI Codex, Claude Code, Cursor). Lokasi lengkap dan langkah per platform: `docs/instalasi.md` di paket ini. Script memakai Python standar (tanpa pemasangan paket); di Windows pakai `python` atau `py`. Skill tetap berguna bila script tidak bisa dijalankan.

## FAQ
1. **Apakah harus punya data penjualan?** Tidak wajib. Tanpa data, skill memakai angka contoh berlabel "asumsi" dan menjadikan pencatatan data sebagai tugas minggu pertama.
2. **Apakah ini menjamin omzet naik?** Tidak. Target adalah tujuan kerja; hasil tergantung produk, harga, dan eksekusi.
3. **Apakah skill menjalankan iklan untuk saya?** Tidak. Skill menyusun rencana dan angka batasnya; pemasangan iklan dikerjakan Anda/tim. Untuk audit iklan pakai `audit-akun-iklan`.

## Skill pendamping
`kalender-konten-30hari`, `promo-kalender`, `audit-akun-iklan`, `laporan-iklan-mingguan`, `kpi-tim`, `riset-calon-pelanggan`, `hitung-hpp`, `harga-jual-marketplace`.

## Asal-usul
Diadaptasi dan diperluas dari dua skill berlisensi MIT (marketing-plan oleh Corey Haines; gtm-strategy oleh Pawel Huryn); rincian di `ATTRIBUTION.md`. Tidak berafiliasi dengan para pembuat sumber.
