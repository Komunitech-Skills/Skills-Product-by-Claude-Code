# 01 - Normal utama: 3 balasan WA pemasok tepung (600 kg, tenggat 5 hari)

- **Tanggal:** 2026-10-14 · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw 2026.10.2 lokal, model `claude-sonnet-5`, home berisi hanya skill ini. Hasil SEBELUM/SESUDAH utuh: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna)
> Tolong bandingin 3 supplier tepung ini ya. Saya punya toko bahan kue, butuh terigu protein sedang 600 kg, harus sudah sampai paling lambat 5 hari lagi soalnya stok tinggal dikit. Ini balasan WA mereka:
>
> [Toko Tepung Sentosa] Siang bu 🙏 terigu protein sedang ready. hrg 118rb/dus isi 10kg. kalo ambil diatas 50 dus kami kasih disc 5% bu. ongkir ke tempat ibu 100rb. kirim 2-3 hari stlh order. bayar cash pas barang dtg ya bu
>
> [PT Mitra Pangan Jaya] Selamat siang Ibu. Penawaran kami: Tepung terigu protein sedang Rp11.200/kg, harga belum termasuk PPN (kami PKP, faktur pajak tersedia). Minimal order 300 kg. Ongkir Rp150.000 ditagihkan di invoice. Estimasi kirim 3-4 hari. Pembayaran tempo 30 hari setelah barang diterima.
>
> [CV Berkah Gandum] bu harga 11.900/kg udh franco sampai gudang ibu ya, kami blm PKP jadi ga ada ppn. kirim 5-7 hari soalnya nunggu stok masuk. bayar transfer full dulu baru kami kirim
>
> Mana yang paling untung?

## Output SESUDAH (skill aktif) - konteks uji lokal
> **Perbandingan 3 penawaran terigu protein sedang: 600 kg, butuh tiba dalam 5 hari**
> Toko Tepung Sentosa termurah sekaligus skor tertinggi — direkomendasikan, tapi hampir seri dengan PT Mitra Pangan Jaya (beda cuma 0,7 poin). CV Berkah Gandum **tidak disarankan** karena lead time 5-7 hari (dibaca 7 hari) melewati tenggat 5 hari Anda.
>
> | Pemasok | Total bayar (per kg) | Selisih vs termurah | Skor (peringkat) |
> |---|---|---|---|
> | Toko Tepung Sentosa | Rp6.826.000 (Rp11.377) | termurah | 86,5 (1) |
> | PT Mitra Pangan Jaya | Rp7.625.700 (Rp12.710) | +Rp799.700 (+11,7%) | 85,8 (2) |
> | CV Berkah Gandum | Rp7.140.000 (Rp11.900) | +Rp314.000 (+4,6%) | 63,0 (3) — telat |
>
> **Rekomendasi: Toko Tepung Sentosa**
> 1. **Biaya:** total paling murah, Rp6.826.000 untuk 600 kg (60 dus x Rp118rb, dapat diskon 5% karena di atas 50 dus → harga efektif Rp11.210/kg) + ongkir Rp100rb.
> 2. **Waktu:** kirim 2-3 hari, aman di dalam tenggat 5 hari Anda.
> 3. **Catatan:** termin cash saat barang datang — ringan untuk negosiasi tapi tidak menahan kas Anda lebih lama; status PKP/PPN-nya belum disebutkan, ini yang paling menentukan apakah posisinya tetap #1 (lihat di bawah).
>
> **Rincian singkat:**
> - **Toko Tepung Sentosa:** Rp11.800/kg → diskon 5% jadi Rp11.210/kg (>50 dus), beli 600 kg, ongkir Rp100rb, status PKP belum jelas (potensi PPN tambahan Rp750.860 jika ternyata PKP & harga belum termasuk PPN), kirim 2-3 hari, bayar cash saat barang tiba.
> - **PT Mitra Pangan Jaya:** Rp11.200/kg, MOQ 300kg (terpenuhi), ongkir Rp150rb, PKP dengan harga belum termasuk PPN → PPN Rp755.700 ditambahkan, kirim 3-4 hari, tempo 30 hari (ringan untuk kas).
> - **CV Berkah Gandum:** Rp11.900/kg sudah franco (ongkir 0), non-PKP jadi tanpa PPN, tapi kirim 5-7 hari (melewati tenggat 5 hari Anda) dan harus transfer lunas dulu sebelum barang dikirim (risiko ke pemasok baru).
>
> **Kalau kondisinya berubah:**
> - Kebutuhan jadi 1.200 kg: Toko Tepung Sentosa tetap termurah & direkomendasikan (Rp13.552.000, Rp11.293/kg).
> - Bila Toko Tepung Sentosa ternyata telat jadi 10 hari (melewati tenggat): rekomendasi pindah ke PT Mitra Pangan Jaya, dengan selisih hemat Rp314.000 dibanding CV Berkah Gandum.
> - Bagi pesanan 70/30 (Sentosa 420 kg + Mitra Pangan Jaya 180 kg, MOQ Mitra naik beli jadi 300 kg): tambahan biaya Rp2.126.100 (+31,1%) — kurang efisien karena MOQ Mitra Pangan Jaya memaksa beli lebih dari kebutuhan.
>
> **Risiko yang perlu dijaga:**
> - Status PKP Toko Tepung Sentosa belum jelas — kalau ternyata PKP dan harga belum termasuk PPN, totalnya naik ke Rp7.576.860, hampir menyamai Mitra Pangan Jaya. Ini bisa mengubah peringkat #1.
> - Jangan bergantung ke satu pemasok untuk stok sekritis ini; dengan jarak skor tipis, ada baiknya tetap jalin komunikasi dengan PT Mitra Pangan Jaya sebagai cadangan.
> - CV Berkah Gandum minta transfer lunas di muka sebelum kirim — risiko untuk pemasok yang belum punya rekam jejak dengan toko Anda, dan tetap tidak memenuhi tenggat Anda.
> - Harga di atas berlaku untuk pesanan ini; belum ada info "harga berlaku sampai kapan" dari ketiganya — minta dikonfirmasi tertulis bila Anda rutin order bulanan.
>
> **Pesan WA ke pemasok (siap kirim):**
>
> Ke Toko Tepung Sentosa:
> > Terima kasih atas penawarannya. Sebelum kami putuskan, mohon konfirmasi: toko ini PKP atau bukan? Kalau PKP, harga Rp118rb/dus itu sudah termasuk PPN atau belum, dan bisa terbit faktur pajak? Terima kasih.
>
> Ke PT Mitra Pangan Jaya:
> > Terima kasih atas penawarannya, Pak/Bu. Apakah ongkir Rp150.000 itu sekali kirim untuk 600 kg atau per dus? Dan apakah ada kemungkinan kirim dipercepat jadi maksimal 5 hari dari sekarang? Mohon konfirmasi, terima kasih.
>
> **Data yang belum ada:**
> - [isian: status PKP Toko Tepung Sentosa & apakah harga sudah termasuk PPN] — bila PKP & belum termasuk PPN, total naik jadi Rp7.576.860
> - [isian: konfirmasi ongkir Rp150.000 PT Mitra Pangan Jaya itu untuk 600 kg sekali kirim, bukan per satuan lain]
>
> **Asumsi:** pembeli (toko Anda) bukan PKP sehingga PPN dihitung sebagai biaya; bobot skor default (biaya 40, lead time 20, termin 15, kualitas 15, MOQ 10); harga bertingkat berlaku untuk seluruh jumlah yang dibeli; kualitas ketiganya belum dinilai jadi dianggap netral (3/5); lead time ditulis rentang dibaca angka terlama ("2-3 hari" → 3, "3-4 hari" → 4, "5-7 hari" → 7).
>
> Catatan: alat bantu keputusan pembelian, bukan nasihat pajak/hukum; pastikan harga & status PPN tertulis di penawaran/faktur sebelum bayar.
>
> Tiga hal yang paling mengubah hasil ini:
> 1. Toko Tepung Sentosa itu PKP atau bukan, dan kalau PKP apakah harganya sudah termasuk PPN?
> 2. Mau saya hitung ulang kalau Anda sudah dapat kepastian jawaban itu dari Sentosa?
> 3. Apakah Anda ingin tetap simpan CV Berkah Gandum sebagai cadangan untuk order berikutnya (di luar kebutuhan mendesak 5 hari ini)?

## Catatan penguji
- **Nilai SESUDAH 7,5** (SEBELUM 6). Konteks Telegram: SESUDAH **6** (SEBELUM 6,5).
- Angka diverifikasi independen (lihat `05-...md` bagian A): semua angka tabel, PPN Rp755.700 (DPP termasuk ongkir yang ditagih di invoice), skor, 2x, bagi 70/30 benar.
- Pembeda nyata vs tanpa skill: harga Rp11.200/kg yang "kelihatan termurah" ternyata termahal setelah PPN (+Rp799.700); status PKP Sentosa yang belum disebut ditandai dengan dampaknya; pemasok yang melewati tenggat tidak direkomendasikan; pesan WA siap kirim.
- **Cacat:** kalimat "rekomendasi pindah ke PT Mitra..., dengan selisih hemat Rp314.000 dibanding CV Berkah" salah subjek (Rp314.000 = selisih Sentosa vs Berkah; Mitra justru lebih mahal Rp485.700 dari Berkah). Di konteks Telegram kesalahan ini lebih parah: agent menyimpulkan sendiri "bila Sentosa PKP, Mitra jadi lebih murah" (salah: 7.576.860 < 7.625.700). Akar masalah: kalimat sensitivitas script ("rekomendasi X (BERUBAH). Hemat vs Y: Rp...") tidak menyebut siapa yang hemat, dan script tidak menghitung peringkat baru bila potensi PPN benar terjadi.
- Mapping "di atas 50 dus": run ini memakai `50: 5%` (≥ 50 dus), run Telegram `51: 5%`; untuk 60 dus hasilnya sama.
- Agent membaca ±700 baris kode script untuk memahami mengapa `harga_termasuk_ppn: "belum"` masuk "data belum ada" (cacat script no. 1 di `05`), sehingga durasi 2,5 menit.
