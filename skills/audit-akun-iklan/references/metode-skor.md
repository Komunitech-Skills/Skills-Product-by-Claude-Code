# Metode Skor Kesehatan Akun Iklan

Sumber kebenaran angka: `scripts/skor_audit.py`, `scripts/daftar_cek.csv`, `scripts/bobot_kategori.csv`.
Dokumen ini menjelaskan rumusnya supaya bisa dicek ulang manual (atau dipakai bila Python tidak
tersedia; tulis langkah hitungnya di jawaban dan sebut bahwa hitungan manual).

Metode diadaptasi dari claude-ads (MIT, lihat `ATTRIBUTION.md`): status empat nilai, bobot
keparahan, bobot kategori yang dinormalkan ulang, dan cakupan bukti. Komunitech menambahkan status
`sebagian`, label skor bahasa awam, prioritas dampak × kemudahan, kenaikan skor per perbaikan,
rencana 7 hari, serta cek khusus Shopee/TikTok Shop/Tokopedia dan konteks Indonesia.

## 1. Status tiap cek
| Status | Arti | Kredit |
|---|---|---|
| `lulus` | Bukti menunjukkan cek terpenuhi | 1 |
| `sebagian` | Terpenuhi sebagian (mis. 2 dari 3 kampanye benar) | 0,5 |
| `gagal` | Bukti menunjukkan cek tidak terpenuhi | 0 |
| `tidak_tahu` | Berlaku, tapi bukti belum ada | tidak dihitung ke skor, **menurunkan cakupan** |
| `tidak_berlaku` | Tidak relevan (lihat kolom `tidak_berlaku_jika`) | dibuang dari semua perhitungan |

Cek yang tidak dijawab sama sekali = `tidak_tahu`. **Jangan pernah menebak `lulus`** tanpa bukti.

## 2. Bobot keparahan (dampak bila gagal)
| Keparahan | Bobot | Contoh |
|---|---:|---|
| kritis | 5 | Pelacakan salah, akun bisa dibajak, iklan ditolak |
| tinggi | 3 | Anggaran bocor, tujuan kampanye salah, materi lemah |
| sedang | 1 | Perbaikan berguna tapi tidak mendesak |

## 3. Rumus
Per kategori (hanya cek yang statusnya diketahui):

    skor_kategori = 100 × Σ(bobot × kredit) / Σ(bobot cek lulus/sebagian/gagal)

Per platform (kategori tanpa cek diketahui dibuang, bobot sisanya dinormalkan ulang):

    skor_platform = Σ(skor_kategori × bobot_kategori) / Σ(bobot_kategori yang dipakai)

Cakupan bukti per platform:

    cakupan = 100 × Σ(bobot cek diketahui) / Σ(bobot cek yang berlaku)

| Cakupan | Status | Aturan laporan |
|---|---|---|
| ≥ 80% | final | Skor boleh disampaikan sebagai nilai akun |
| 60–79,99% | sementara | Wajib ditulis "sementara" |
| < 60% | bukti kurang | Skor **tidak** disampaikan sebagai nilai akun; minta bukti dulu |

Skor gabungan beberapa platform = rata-rata tertimbang **porsi belanja** (bila belanja semua
platform layak diketahui) atau rata-rata biasa (ditandai sementara). Platform berstatus bukti
kurang dikeluarkan dari gabungan dan disebutkan.

Label: 85–100 Sehat · 70–84,9 Cukup, ada yang perlu dibenahi · 50–69,9 Perlu perbaikan · < 50 Kritis.
Tampilan dibulatkan 1 desimal (setengah ke atas); perhitungan memakai angka penuh.

## 4. Bobot kategori per platform (total 100)
| Kategori | Meta | TikTok | Google | Shopee | TikTok Shop/Tokopedia |
|---|---:|---:|---:|---:|---:|
| Pelacakan & konversi | 20 | 20 | 25 | 10 | 15 |
| Struktur & akses akun | 15 | 10 | 15 | 15 | 10 |
| Target & audiens | 10 | 10 | 10 | 10 | - |
| Anggaran & bidding | 15 | 15 | 15 | 20 | 20 |
| Materi iklan | 15 | 25 | 10 | 15 | 25 |
| Halaman tujuan / etalase | 10 | 10 | 10 | 20 | 20 |
| Frekuensi & kelelahan materi | 10 | 5 | - | - | - |
| Pengecualian | 5 | 5 | 15 | 10 | 10 |

Alasan singkat: TikTok & TikTok Shop sangat bergantung pada video (materi 25). Marketplace
(Shopee/TikTok Shop) menang/kalah di halaman produk & ROAS impas (etalase 20, anggaran 20), dan
pelacakannya sudah disediakan platform (pelacakan lebih rendah). Google Ads paling sering bocor lewat
pencarian tidak relevan (pengecualian 15) dan konversi yang salah (pelacakan 25).
Bobot ini adalah **keputusan produk Komunitech versi 1.0.0**, bukan standar resmi platform.

## 5. Prioritas perbaikan
    prioritas = bobot_keparahan × nilai_kemudahan      (mudah = 3, sedang = 2, sulit = 1)

Rentang 1–15. Urutan: prioritas tertinggi → kenaikan skor platform terbesar → keparahan → platform → ID.
`naik` = skor platform bila cek itu menjadi `lulus` dikurangi skor sekarang (dihitung ulang penuh).
Cek **kritis** berstatus `tidak_tahu` masuk daftar "CEK DULU" dan dikerjakan paling awal.

## 6. Rencana 7 hari
- Hari 1–5: antrean (CEK DULU lalu prioritas) diisi berurutan, kapasitas 3 unit/hari
  (mudah = 1, sedang = 2, sulit = 3 unit ≈ 1–2 jam kerja). Sisa masuk "antrean minggu berikutnya".
- Hari 6: tidak mengubah pengaturan besar; biarkan iklan belajar.
- Hari 7: ekspor data, buat laporan dengan `laporan-iklan-mingguan`, audit ulang.

## 7. ROAS/ROI impas (`roas-impas`)
    biaya_platform = harga × persen / 100   (dibulatkan ke rupiah terdekat)
    laba_kotor     = harga − modal − biaya_platform − biaya_lain
    biaya iklan maks per pesanan (impas) = laba_kotor
    ROAS impas     = harga / laba_kotor     (dibulatkan KE ATAS 2 desimal, supaya target tidak di bawah impas)

Bila laba_kotor ≤ 0 → produk sudah rugi sebelum iklan; script menolak dan menyarankan membenahi
harga/modal dulu. Persen biaya marketplace berubah-ubah per kategori & program; pakai angka dari
rincian pesanan/penghasilan di Seller Centre milik pengguna, bukan tebakan.
