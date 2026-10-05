# 01 — Normal: kopi susu literan, naik harga + reseller + kantor

> Uji independen Tahap 6 (2026-09-29). Penguji: agent terpisah dari pembuat. Output agent dihasilkan oleh sesi `claude -p` baru (Claude Code, simulasi agent) dengan skill terpasang di folder sementara `.claude/skills/` (tanpa folder `examples/`). Nama usaha fiktif.

## Input pengguna

> Aku jualan kopi susu gula aren literan (botol 1 liter) di Semarang, namanya Kopi Teras. Modal per botol 22 ribu udah sama botol & stiker. Sekarang aku jual 45 ribu, laku sekitar 400 botol sebulan. Biaya tetap (sewa dapur, gaji 1 orang, listrik) 5,2 juta sebulan. Pesaing di sekitar jual 35rb, 42rb, 55rb. Banyak yang minta jadi reseller, ada kantor juga mau ambil 100 botol per minggu. Terus aku kepikiran naikin ke 49.900 karena gula aren naik. Gimana strategi harganya?

## Output agent (dengan skill, apa adanya)

**Ringkasan**
- **Harga eceran:** naik ke Rp47.900 dulu, bukan langsung Rp49.900. Kalau nanti mau Rp49.900, naikkan bertahap setelah 4–6 minggu.
- **Strategi:** berbasis nilai (kamu di tengah pesaing: 35rb, 42rb, 55rb), ditambah tangga harga reseller dan kantor.
- **Alasan utama:** kenaikan Rp49.900 secara hitungan aman, tapi kenaikannya 10,9% sekaligus. Pelanggan eceran sensitif dengan lonjakan sebesar itu, dan volume dari reseller dan kantor lebih berharga untuk dijaga.

**Asumsi**
- HPP Rp22.000 per botol sudah termasuk botol dan stiker. Angka ini belum memasukkan kenaikan gula aren.
- Target margin minimum 40%, default untuk minuman.
- Penjualan langsung tanpa potongan marketplace.
- Non-PKP.

**Kondisi sekarang (dihitung script)**
- Laba Rp23.000 per botol, margin 51,1%.
- Titik impas 227 botol per bulan. Dengan 400 botol, laba kotor setelah biaya tetap sekitar Rp4 juta per bulan.
- Harga terendah yang masih aman (margin 40%) adalah Rp36.667. Harga 45rb sudah jauh di atasnya.

**Kalau naik ke Rp49.900**
- Laba per botol jadi Rp27.900, margin 55,9%.
- Volume impas: selama penjualan tidak turun di bawah 330 botol (turun sampai 17,5%), laba tetap sama atau lebih baik. Ini hitungan pasti.
- Perkiraan (ESTIMASI, bukan kepastian):

| Kepekaan pembeli | Volume | Laba/bulan | Selisih |
|---|---|---|---|
| Tidak peka | 378 | Rp5,35 juta | +Rp1,35 juta |
| Sedang | 356 | Rp4,73 juta | +Rp0,73 juta |
| Sangat peka | 313 | Rp3,53 juta | −Rp0,47 juta |

- Jadi naik harga hampir pasti menguntungkan kecuali pembelimu sangat peka harga. Karena itu uji dulu, jangan langsung naik penuh.
- **Soal gula aren naik:** kalau HPP naik jadi Rp24.000, laba sekarang turun ke Rp3,2 juta. Dengan harga Rp49.900, labanya kembali ke sekitar Rp4 juta pada 356 botol (kepekaan sedang, estimasi). Jadi kenaikan ini memang wajar. Tolong cek HPP terbarumu, karena angka Rp22.000 itu belum termasuk kenaikan gula.

**Tabel harga yang disarankan**
Semua angka pakai HPP Rp22.000. Baris Rp47.900, Rp43.000, dan Rp42.500 saya hitung manual. Baris lainnya dihitung script.

| Kanal | Syarat | Harga/botol | Laba/botol | Margin | Status |
|---|---|---|---|---|---|
| Eceran (baru) | 1 botol | Rp47.900 | Rp25.900 | 54,1% | OK |
| Reseller | min. 10 botol | Rp43.000 | Rp21.000 | 48,8% | OK |
| Kantor (langganan mingguan) | 100 botol/minggu | Rp42.500 | Rp20.500 | 48,2% | OK |

Untuk perbandingan, dengan harga eceran tetap Rp45.000, tangga script menghasilkan reseller Rp40.500 dan kantor Rp38.500 (margin 45,7% dan 42,9%, keduanya OK).

**Yang perlu diperhatikan**
- **Kantor 100 botol per minggu:** ini sekitar 400 botol per bulan, setara dengan seluruh penjualanmu sekarang. Pada harga Rp38.500 (laba Rp16.500 per botol), tambahan labanya sekitar Rp6,6 juta per bulan. Ini peluang terbesar, jauh lebih besar dari selisih Rp4.900 di eceran. Beri harga langganan Rp42.500 dengan syarat kontrak minimal 1 bulan dan bayar di muka atau tiap minggu. Kalau mereka menawar, turun sampai Rp38.500 boleh, jangan lebih rendah.
- **Cek kapasitas:** volume 800 botol per bulan berarti kapasitas dapur dan tenaga satu orang harus cukup. Kalau tidak, tambahan biaya tenaga akan menggerus laba.
- **Reseller:** harga eceran mereka harus tetap di atas harga eceranmu. Pesaing di 35rb dan 42rb ada di bawah, jadi sarankan mereka jual minimal Rp49.900.
- **Jangan diskon reseller lebih dari 18,5% dari Rp45.000:** di bawah Rp36.667 margin turun di bawah 40%.

**Langkah minggu ini**
1. Cek HPP terbaru setelah gula aren naik, lalu hitung ulang tabel di atas.
2. Umumkan kenaikan eceran ke Rp47.900 dan berlaku 1–2 minggu ke depan, dengan alasan jujur (harga gula aren naik). Beri kesempatan beli harga lama selama masa itu.
3. Kirim penawaran ke kantor: Rp42.500 per botol, 100 botol per minggu, minimal 1 bulan.
4. Buat daftar harga reseller (Rp43.000 untuk 10 botol ke atas) dan kirim lewat WA ke yang sudah minta.
5. Catat penjualan eceran per minggu selama 4 minggu. Kalau turun kurang dari 17%, lanjut naik ke Rp49.900.

**Teks pengumuman (siap tempel)**
> Halo kak, mulai [tanggal], harga Kopi Teras literan naik jadi Rp47.900 karena harga gula aren naik. Sampai [tanggal], masih bisa pesan dengan harga lama Rp45.000. Terima kasih sudah jadi langganan! ☕

Angka dihitung dengan script dari data yang kamu berikan, kecuali yang saya tandai hitung manual. Keputusan harga tetap di tanganmu.

## Verifikasi penguji

Dihitung ulang dengan Decimal/Fraction milik penguji (`scratchpad/uji-harga/verif.py` + hitung tangan):
- Laba/botol 45.000 − 22.000 = 23.000; margin 51,11% ✔. BEP 5.200.000 ÷ 23.000 = 226,09 → **227** ✔. Laba 400 × 23.000 − 5,2 jt = Rp4.000.000 ✔.
- Lantai margin 40%: 22.000 ÷ 0,6 = 36.666,67 → **Rp36.667** (ke atas) ✔; diskon maks 1 − 36.667/45.000 = 18,52% ✔.
- Naik ke 49.900: laba 27.900; volume impas 400 × 23.000 ÷ 27.900 = 329,7 → **330** ✔ (turun 17,5%) ✔.
- ESTIMASI (Δ = 10,889%): e −0,5 → 378,2 → 378, laba 378 × 27.900 − 5,2 jt = Rp5.346.200 ✔; e −1 → 356 → Rp4.732.400 ✔; e −2 → 313 → Rp3.532.700 ✔ (label "ESTIMASI" ada ✔).
- HPP 24.000: laba 400 × 21.000 − 5,2 jt = Rp3.200.000 ✔; 356 × 25.900 − 5,2 jt = Rp4.020.400 ✔.
- Baris "hitung manual" (agent tidak menjalankan `tangga` untuk harga yang direkomendasikan): 47.900 → 25.900 / 54,07% ✔; 43.000 → 21.000 / 48,84% ✔; 42.500 → 20.500 / 48,24% ✔. Angka benar, tetapi **melanggar aturan "script wajib untuk semua angka uang"** — padahal `tangga --harga-ecer 47900 --level Reseller:10:=43000 --level Kantor:100:=42500` tersedia.

**Catatan kualitas:** (1) Tidak konsisten: eceran toko disarankan Rp47.900, tetapi reseller "disarankan jual minimal Rp49.900" — reseller kalah harga dari toko sendiri. (2) "100 botol/minggu ≈ 400 botol/bulan" (lebih tepat ±433) — wajar sebagai perkiraan. (3) Tambahan laba kantor dihitung pada Rp38.500, padahal harga yang disarankan Rp42.500 — membingungkan.

**Nilai: 7,5/10** — struktur lengkap (ringkasan, asumsi, tabel, estimasi berlabel, langkah, teks siap tempel), angka benar, tetapi ada inkonsistensi saran & angka manual.
