# 02 — Normal + potongan marketplace: diskon 11.11 di Shopee

> Uji independen Tahap 6 (2026-09-29). Penguji: agent terpisah dari pembuat. Output agent dihasilkan oleh sesi `claude -p` baru (Claude Code, simulasi agent) dengan skill terpasang di folder sementara `.claude/skills/` (tanpa folder `examples/`). Nama usaha fiktif.

## Input pengguna

> Aku jual pashmina ceruti di Shopee, toko Hijab Aruna. Modal 38 ribu per pcs udah sama packing. Harga jual sekarang 89.900. Total potongan Shopee (admin + gratis ongkir xtra + layanan) kata kalkulator harga-jual-marketplace sekitar 17% dari harga jual. Sebulan laku kira-kira 300 pcs. Mau ikut 11.11 diskon 30%, masih untung nggak? Atau mending beli 2 gratis 1? Aku pengen margin minimal 25%.

## Output agent (dengan skill, apa adanya)

**Ringkasan:** Diskon 30% masih untung, tapi margin turun ke 22,6%, di bawah target 25% kamu. Beli 2 gratis 1 lebih buruk, marginnya 19,6%. Saranku ikut 11.11 dengan diskon maksimal 25%, atau paket beli 2 diskon 25%.

**Asumsi:** Modal Rp38.000 sudah termasuk packing. Potongan Shopee 17% dari harga jual (angkamu dari kalkulator). Margin dihitung dari harga jual, bukan markup. Voucher toko dan biaya iklan belum masuk hitungan.

**Kondisi sekarang (Rp89.900):**
- Potongan Shopee Rp15.283, laba Rp36.617 per pcs.
- Margin 40,73%.
- Laba kotor sebulan sekitar Rp10,99 juta (300 pcs).

**Perbandingan promo:**

| Promo | Harga efektif/pcs | Laba/pcs | Margin | Target 25% | Penjualan minimal agar laba kotor sama |
|---|---|---|---|---|---|
| Normal | 89.900 | 36.617 | 40,7% | OK | 300 pcs |
| Diskon 15% | 76.415 | 25.424 | 33,3% | OK | 433 pcs (+44%) |
| Diskon 30% | 62.930 | 14.232 | 22,6% | Di bawah | 772 pcs (+157%) |
| Beli 2 gratis 1 | 59.933 | 11.745 | 19,6% | Di bawah | 936 pcs (+212%) |

**Batas aman:**
- Diskon maksimal supaya margin tetap 25% adalah 27,12%, atau harga terendah Rp65.518. Kalau mau angka cantik, pakai diskon 25% (sekitar Rp67.425).
- Untuk diskon 30% dan beli 2 gratis 1, penjualan harus naik lebih dari 2,5 kali lipat supaya total laba tidak turun. Untuk pashmina yang biasanya laku 300 pcs, itu target berat. Kalau tidak tercapai, kamu kerja lebih banyak untuk laba lebih kecil.
- Pada beli 2 gratis 1, kamu memberi diskon efektif 33% dan tetap kena potongan Shopee di tiap pcs.

**Simulasi (perkiraan, bukan kepastian):** Kalau 11.11 bikin penjualan naik 2 sampai 3 kali lipat (600 sampai 900 pcs), diskon 30% bisa menutup laba bulan normal, tapi margin per pcs tetap di bawah targetmu. Diskon 25% butuh kenaikan penjualan 103,85% (dari 300 jadi minimal 612 pcs) untuk menyamai laba kotor normal, dan marginnya tetap di atas 25% (26,64%).

**Langkah minggu ini:**
1. Pilih promo: diskon 25% atau paket "beli 2 diskon 25%". Paket ini menaikkan jumlah pcs per pesanan.
2. Kalau tetap mau 30%, batasi kuotanya (mis. 100 pcs, atau hanya 1 varian warna) supaya kerugian margin terbatas.
3. Cek stok dan modal. Kalau penjualan naik 2 sampai 3 kali lipat, stok harus siap.
4. Cek biaya di luar hitungan tadi (voucher toko, iklan, ongkir yang kamu tanggung). Kalau ada, margin sebenarnya lebih rendah dari angka di atas.
5. Setelah 11.11, catat pcs terjual dan laba nyata, lalu bandingkan dengan tabel ini.

Kalau mau, aku bisa hitung paket "beli 2" dengan harga spesifik, atau kuota untuk diskon 30%.

Angka dihitung dengan script dari data yang kamu berikan. Keputusan harga tetap di tanganmu.

## Verifikasi penguji

Script dijalankan penguji: `diskon --harga 89.900 --hpp 38rb --diskon 30 --volume 300 --margin-min 25 --biaya-persen 17`, `--beli-gratis 2:1`, `margin`, `cantik --harga 65518 --hpp 38000 --margin-min 25 --biaya-persen 17`.
- Normal: potongan 17% = 15.283; laba 89.900 × 0,83 − 38.000 = **36.617**; margin 40,73%, markup 96,36% ✔.
- Diskon 30%: harga 62.930; laba 62.930 × 0,83 − 38.000 = 14.231,90; margin 22,62%; faktor 2,5729 → +157,29%; 300 → ceil(771,9) = **772** ✔.
- Beli 2 gratis 1: harga efektif 59.933,33; laba 11.744,67; margin 19,6%; +211,78% → **936** ✔.
- Diskon 15% (agent): 76.415; laba 25.424,45; margin 33,27%; 300 × 1,4402 = 432,07 → **433** ✔.
- Lantai 25%: 38.000 ÷ 0,58 = 65.517,24 → **Rp65.518**; diskon maks 27,12% ✔. Diskon 25% → Rp67.425 ✔ (margin 26,64% — penguji).
- Diskon 25%: angka dihitung ulang skrip 2026-10-13 (`diskon --harga 89.900 --hpp 38rb --diskon 25 --volume 300 --margin-min 25 --biaya-persen 17`): harga promo Rp67.425, margin 26,64%, penjualan harus naik **103,85%** → minimal **612 pcs**. Script menandai kenaikan > 100% sebagai TIDAK DISARANKAN; angka ini pasti, bukan perkiraan.
- Harga cantik di sekitar lantai: Rp64.900 di bawah batas, Rp65.900 OK (25,34%) ✔ — sesuai aturan "kandidat di bawah lantai tidak boleh dipilih".

**Catatan penguji:** angka dihitung ulang skrip 2026-10-13; angka diskon 25% di output di atas sudah memakai hasil skrip. Tampilan script "laba Rp14.231,90/unit" bersen, sementara laba normal dibulatkan (inkonsisten tampilan, ringan).

**Nilai: 8/10** — jawaban langsung ("masih untung, tapi di bawah target"), batas diskon maksimal, alternatif, langkah konkret.
