---
name: rencana-marketing-usaha
description: Menyusun rencana marketing kuartalan/tahunan untuk UMKM sampai usaha mapan Indonesia siap pakai — tujuan SMART, target pasar, pesan kunci, pilihan kanal (WhatsApp, Instagram, TikTok, marketplace, Google Maps), kalender momen (gajian, Ramadan, Harbolnas), anggaran per kanal, target CAC/ROAS/titik impas dari margin (dihitung script), KPI dan corong penjualan. Gunakan saat diminta rencana marketing, marketing plan, go-to-market/GTM plan, strategi promosi, atau alokasi anggaran iklan. Marketing plan, budget allocation, quarterly plan, KPI, funnel.
---

# Rencana Marketing Usaha

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah "saya mau usaha saya lebih laku" menjadi **satu dokumen rencana 1-3 bulan (atau 12 bulan)** yang bisa langsung dijalankan: tujuan terukur, siapa yang dibidik, apa pesannya, kanal mana, kapan, berapa uangnya, dan angka apa yang dipantau. Semua angka anggaran, CAC, ROAS, dan corong **dihitung script**, bukan dikira.

## Kapan digunakan
- "Bikin rencana marketing kuartal 4 untuk kedai kopi saya", "rencana promosi setahun", "GTM plan produk baru".
- "Anggaran iklan Rp 5 juta enaknya dibagi ke mana?", "berapa maksimal saya boleh keluar buat dapat 1 pelanggan?"
- Meluncurkan produk/cabang baru dan butuh urutan langkah + target.

## Kapan TIDAK digunakan (arahkan ke skill lain)
- Jadwal posting dan tulis konten mingguan -> `konten-mingguan`.
- Mekanisme diskon/promo momen + cek margin promo -> `promo-kalender`.
- Audit iklan yang sedang jalan -> `audit-akun-iklan`; laporan hasil iklan -> `laporan-iklan-mingguan`.
- Riset dan wawancara calon pelanggan -> `riset-calon-pelanggan`; harga jual -> `hitung-hpp` / `harga-jual-marketplace`.
- Target KPI tim/karyawan -> `kpi-tim`.
- Bukan janji hasil: skill ini tidak menjamin omzet dan tidak mengelola iklan.

## Input
| Info | Wajib? | Bila tidak diberikan |
|---|---|---|
| Usaha & produk utama (apa, harga jual, HPP/modal per unit) | Ya | Tanyakan; HPP belum tahu -> tawarkan `hitung-hpp`, jangan mengarang |
| Periode rencana (kuartal / tahun) & tanggal mulai | Ya | Default: 3 bulan ke depan dari hari ini (sebutkan asumsi) |
| Tujuan utama (omzet, jumlah pesanan, pelanggan baru, pengunjung toko) | Ya | Usulkan 1 tujuan dari kondisi usaha, minta konfirmasi |
| Anggaran marketing total periode (Rp) | Ya | Tanyakan; jawaban "belum tahu" -> pakai 5-10% dari target omzet, sebutkan asumsi, tampilkan skenario Rp 0 (tanpa iklan) |
| Tempat jualan (toko fisik, WA, IG, TikTok Shop, marketplace, Maps) & biaya platform % | Disarankan | Anggap WA + Instagram; biaya platform 0% (sebut) |
| Kondisi sekarang: omzet/bulan, pelanggan lama, kanal yang sudah jalan | Tidak | Tulis "belum ada data" dan jadikan pekerjaan minggu 1 (catat data dasar) |
| Siapa yang mengerjakan (sendiri, 1-2 staf) & jam per minggu | Tidak | Asumsi 1 orang, 5 jam/minggu; rencana dibuat sesuai kapasitas |

Aturan tanya: jika ada info **wajib** yang kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan pendek bernomor. Jika pengguna minta cepat, pakai default dan tulis asumsinya di bagian atas rencana.

## Langkah Kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Cek kondisi (bagian 1 rencana).** Ringkas usaha, produk andalan, margin kotor, pelanggan sekarang, kanal yang sudah jalan. Tandai angka yang belum ada sebagai "DATA BELUM ADA".
2. **Uji layak dulu:** hitung margin per pesanan lewat script `target` (lihat Script). Jika status **RUGI** atau margin di bawah 15% (status TERLALU TIPIS), hentikan rencana iklan berbayar: sarankan perbaiki harga/HPP dulu (`hitung-hpp`, `harga-jual-marketplace`) dan buat rencana organik saja.
3. **Tujuan SMART.** Satu tujuan utama + maksimal 2 pendukung: angka, tenggat, cara ukur. Contoh: "Naikkan pesanan online dari 120 ke 200 per bulan pada 31 Desember, dihitung dari rekap pesanan."
4. **Target pasar.** Pilih **satu segmen prioritas** (mis. pekerja kantor sekitar toko, ibu muda di kota X), bukan "semua orang". Tulis masalahnya, momen beli, dan tempat mereka menghabiskan waktu. Bila belum kenal pelanggan, arahkan ke `riset-calon-pelanggan`.
5. **Pesan kunci.** Satu kalimat janji utama + 3 bukti (ulasan, foto hasil, angka nyata) + 1 ajakan bertindak (chat WA, kunjungi, klik keranjang). Jangan melebih-lebihkan klaim.
6. **Pilih kanal (maksimal 3 utama).** Pakai matriks di `references/kanal-umkm-indonesia.md`: cocokkan kanal dengan segmen, kapasitas orang, dan anggaran. Kanal gratis dulu (WA pelanggan lama, Google Maps, konten organik), berbayar hanya bila margin sehat. Aturan 70/20/10: 70% dana ke kanal yang sudah terbukti, 20% ke kanal berikutnya, 10% eksperimen.
7. **Kalender.** Petakan momen yang jatuh di periode (gajian tanggal 25-1, 9.9/10.10/11.11/12.12, Ramadan-Lebaran, tahun ajaran baru, musim hujan, dll.) memakai `references/kalender-momen.md`; **verifikasi tanggal bergerak (Ramadan, Lebaran) ke kalender resmi**. Buat linimasa per minggu: apa, siapa, kanal. Detail promo -> `promo-kalender`; jadwal konten -> `konten-mingguan`.
8. **Anggaran.** Jalankan script `alokasi`. Tampilkan Rp per kanal, per bulan, plus cadangan eksperimen 10%.
9. **Target angka.** Jalankan `target` (CAC titik impas, CAC & ROAS target, batas atas anggaran iklan dari target omzet) dan `funnel` (berapa jangkauan/klik/chat yang dibutuhkan untuk target pesanan). Konversi funnel dari data nyata; tanpa data pakai angka contoh di `references/patokan-angka.md` dan **beri label "asumsi, ganti dengan data Anda"**.
10. **KPI & rutinitas pantau.** Per tahap corong (Kenal, Tertarik, Beli, Beli lagi, Rekomendasi) 1-2 KPI, sumber datanya, dan pemilik. Rutinitas: catat mingguan 10 menit, evaluasi bulanan, aturan "hentikan" (mis. kanal dihentikan bila 4 minggu CAC > CAC titik impas). Hubungkan ke `laporan-iklan-mingguan` / `kpi-tim`.
11. **Risiko & keputusan terbuka.** Daftar hal yang belum diketahui dan rencana bila target meleset (rencana B).
12. **Sajikan** memakai `templates/rencana-marketing.md`; ringkasan eksekutif di paling atas (maks 6 baris). Tutup dengan 3 langkah minggu ini.

## Script (opsional, Python standar)
Semua perintah dari folder skill. Windows: `python` atau `py`. Jika script tidak bisa dijalankan, hitung dengan rumus di bawah dan tulis "dihitung manual".
```
python3 scripts/alokasi_anggaran.py alokasi --anggaran "Rp 6.000.000" --bulan 3 --kanal "Meta Ads=30,TikTok=25,WA=15,Konten=20,Google Maps=10"
python3 scripts/alokasi_anggaran.py target --harga-jual 45000 --hpp 18000 --biaya-platform 8 --biaya-per-pesanan 1500 --laba-target-per-pesanan 5000 --anggaran-iklan 2000000 --target-omzet 30000000
python3 scripts/alokasi_anggaran.py funnel --target-pesanan 300 --tahap "Jangkauan>Klik=2" --tahap "Klik>Chat=20" --tahap "Chat>Pesanan=30"
```
- Ambang margin (satu set, dipakai di seluruh skill): < 15% TERLALU TIPIS (jangan iklan berbayar); 15% - < 25% TIPIS (iklan kecil, pantau ketat); >= 25% AMAN.
- Cara baca keluaran `target`: angka berlabel "Minimal ..." adalah **syarat** agar iklan tidak rugi (jumlah pesanan minimal dibulatkan ke ATAS, jadi benar-benar menutup anggaran), dan "Batas atas ..." adalah plafon teoretis bila semua pesanan dari iklan. **Bukan perkiraan hasil dan bukan saran belanja.** Tulis begitu di rencana.
- `--bulan` harus bilangan bulat >= 1; nilai lain ditolak dengan pesan GAGAL.
- Persen kanal harus total 100; cadangan eksperimen (default 10%) diambil dulu dari total, sisanya dibagi ke kanal.
- Rumus: margin = harga - HPP - (harga x biaya platform%) - biaya per pesanan. **CAC titik impas = margin** (dibulatkan ke bawah). **ROAS titik impas = harga / margin** (dibulatkan ke atas). ROAS/CAC target memakai margin dikurangi laba target per pesanan.
- Input rusak (persen tak 100, angka negatif, harga 0) -> pesan ERROR jelas; sampaikan ke pengguna dan minta perbaikan, jangan menebak.
- Biaya platform dan tarif iklan **tidak** ditanam di script: minta dari Seller Center/dasbor iklan.

## Format Output
Dokumen mengikuti `templates/rencana-marketing.md` (12 bagian: ringkasan, kondisi, tujuan SMART, target pasar, pesan kunci, kanal, kalender, anggaran, target angka, KPI, risiko, langkah minggu ini). Bahasa sehari-hari, tabel untuk kalender/anggaran/KPI, angka dalam Rupiah dengan titik ribuan. Bagian atas selalu memuat **asumsi** yang dipakai.

## Contoh singkat
Masukan: "Rencana marketing Q4 kedai kopi saya, budget 6 juta, target 200 pesanan online/bulan." -> Tanyakan sekali: harga & HPP menu andalan, tempat jualan, biaya platform, jam luang per minggu. Lalu hasil: tujuan SMART, segmen pekerja kantor radius 3 km, kanal WA + Instagram + Maps + sedikit iklan Meta, kalender gajian/11.11/12.12/Natal, tabel anggaran, CAC impas Rp 10.000 (harga Rp 25.000, margin Rp 10.000), funnel, KPI. Contoh lengkap: `examples/01-kedai-kopi-q4.md`.

## Batasan & Penanganan Error
- Ini alat perencanaan, **bukan jaminan hasil**; angka target adalah tujuan, bukan prediksi. Konversi/CAC nyata bervariasi antar usaha dan musim.
- Jangan mengarang spesifikasi produk, bahan, ukuran, angka pasar/kanal, atau klaim hasil; yang tidak diberikan pengguna ditulis `[isi: ...]` atau ditandai asumsi.
- Tidak memakai data pribadi pelanggan. Jangan menyarankan broadcast massal/spam WA (risiko nomor diblokir); WA dipakai untuk pelanggan yang sudah pernah chat/beli.
- Klaim iklan harus jujur (UU Perlindungan Konsumen); jangan menyarankan testimoni palsu atau klaim kesehatan/medis. Iklan produk teregulasi (obat, kosmetik, makanan) wajib memenuhi aturan BPOM/platform: arahkan ke profesional.
- Tanggal momen dan aturan platform berubah: sebutkan "dicek per <tanggal>" dan minta pengguna memastikan di sumber resmi.
- Anggaran Rp 0 atau data nol: tetap buat rencana organik + langkah mengumpulkan data.
- Pertanyaan di luar cakupan (menjalankan iklan, desain kreatif, strategi investasi/pendanaan): jelaskan batasnya dan arahkan ke skill yang relevan.
