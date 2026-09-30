# Uji 06 - Normal 1: Toko skincare lokal, Rp3 juta/bulan, tujuan penjualan

Penguji independen, 2026-09-30, simulasi agent (claude-code) mengikuti SKILL.md v1.0.0.

## Permintaan pengguna
"Saya jual skincare lokal (serum & sunscreen, sudah BPOM) di Shopee dan IG, kadang TikTok. Anggaran iklan Rp3 juta sebulan, tujuannya jualan. Harga rata-rata per pesanan Rp120.000, margin setelah admin Shopee & ongkir subsidi sekitar 45%. Minggu ke-4 ada gajian + 10.10. Bagi anggarannya dan bikin strategi kontennya."

## Perintah script
```
python3 scripts/alokasi_anggaran.py --anggaran 3jt --tujuan penjualan --aov 120rb --margin 45% \
  --kanal meta,tiktok,shopee --bobot-minggu 1 1 1 2 --kategori skincare
```
## Keluaran script (apa adanya)
```
# Rencana Alokasi Anggaran Iklan - Rp3.000.000 / bulan
Tujuan: **penjualan** | 4 minggu x 7 hari = 28 hari tayang (sisa hari bulan dipakai evaluasi tanpa menambah anggaran).

## Target dari margin (batas impas, bukan prediksi)
- Harga rata-rata per pesanan: Rp120.000; margin kotor 45% -> laba kotor per pesanan Rp54.000
- **Titik impas ROAS = 1/margin = 2,23x** (di bawah ini iklan merugi); CPA impas Rp54.000
- **Target aman** (sisakan 30% laba kotor): CPA maks Rp37.800, ROAS minimal 3,18x
- Agar anggaran bulan ini sekadar impas dibutuhkan minimal 56 pesanan (= omzet Rp6.720.000); ini syarat impas, BUKAN perkiraan hasil.

## Anggaran per kanal
| Kanal | Anggaran | % | Aman 70% | Uji 30% |
|---|---:|---:|---:|---:|
| Meta (IG/FB) | Rp1.909.091 | 63,6% | Rp1.336.364 | Rp572.727 |
| Shopee Ads | Rp1.090.909 | 36,4% | Rp763.636 | Rp327.273 |
| **Total** | **Rp3.000.000** | 100% | | |

## Rencana per minggu
| Kanal | Minggu 1 | Minggu 2 | Minggu 3 | Minggu 4 | Jumlah |
|---|---:|---:|---:|---:|---:|
| Meta (IG/FB) | Rp381.818 | Rp381.818 | Rp381.818 | Rp763.637 | Rp1.909.091 |
| Shopee Ads | Rp218.182 | Rp218.182 | Rp218.182 | Rp436.363 | Rp1.090.909 |
| **Total** | **Rp600.000** | **Rp600.000** | **Rp600.000** | **Rp1.200.000** | **Rp3.000.000** |

## Batas uji (aturan praktis Komunitech, bukan syarat platform; cek minimum di Ads Manager)
| Kanal | Rata-rata per hari | Min. per iklan/hari | Iklan aktif maks |
|---|---:|---:|---:|
| Meta (IG/FB) | Rp68.182 | Rp25.000 | 2 |
| Shopee Ads | Rp38.961 | Rp10.000 | 3 |

Kanal tidak dipakai: TikTok Ads (bagian anggarannya di bawah batas uji).
Sisa pembulatan: Meta (IG/FB) antar minggu Rp1; Shopee Ads antar minggu -Rp1. Total tetap sama dengan anggaran.

## Catatan
- Kategori 'skincare': cek dulu apakah termasuk kategori terbatas di kebijakan iklan resmi tiap platform.

Angka pembagian ini titik awal yang bisa diubah, bukan janji hasil. Tidak ada jaminan penjualan.
```
Catatan penguji: `--kategori skincare` hanya memberi catatan umum; `--kategori "kesehatan (skincare)"` memberi catatan TERBATAS kesehatan/kosmetik (alokasi identik). Agent mengikuti `references/pilar-konten.md` (skincare = TERBATAS) dan menulis catatan kepatuhan kosmetik secara manual.

## Dokumen yang dihasilkan agent (ringkas)
**1. Ringkasan & asumsi:** skincare lokal ber-BPOM, Rp3.000.000/bulan, penjualan, 4 minggu (minggu 4 = gajian + 10.10, bobot 2). Margin 45% sudah bersih admin & ongkir (pengakuan pengguna).

**2. Angka kunci (script):** laba kotor/pesanan Rp54.000; ROAS impas 2,23x, target aman 3,18x; CPA impas Rp54.000, target maks Rp37.800; minimal 56 pesanan agar anggaran impas (syarat, bukan perkiraan).

**3. Pilar konten (4 pilar, 4 konten/minggu, promosi 25%)**
| Pilar | Tahap | Tujuan | 3 sudut | Format | 5 judul contoh |
|---|---|---|---|---|---|
| Edukasi kulit tropis | Awareness | Dikenal karena berguna | "cocok iklim lembap", "hemat langkah", "salah kaprah" | Reels/TikTok 20 dtk, carousel | "3 salah pakai sunscreen di cuaca panas"; "Urutan serum yang benar untuk pemula"; "Berapa banyak sunscreen yang cukup?"; "Kulit berminyak tetap perlu pelembap?"; "Cara baca komposisi di kemasan" |
| Bahan & legalitas | Pertimbangan | Membangun percaya | "BPOM terdaftar", "bahan dicantumkan", "produksi lokal" | Carousel, foto kemasan | "Cara cek nomor BPOM produk kami"; "Isi serum kami, dijelaskan satu per satu"; "Di balik layar pengemasan"; "Kenapa kami tidak pakai pewangi"; "Tanggal kedaluwarsa & cara simpan" |
| Ulasan asli & jawab keberatan | Pertimbangan-beli | Hilangkan alasan menunda | "tekstur", "cocok kulit sensitif? (uji tempel)", "harga per pemakaian" | Tangkapan ulasan asli (izin), video tekstur | "Ulasan asli minggu ini (tanpa edit)"; "Serum ini habis berapa lama?"; "Bisa dipakai bareng retinol?"; "Cara uji tempel sebelum pakai"; "Beda ukuran 20ml vs 30ml" |
| Penawaran & momen | Beli | Ajak beli sekarang | "paket gajian", "10.10 voucher toko", "bundling" | Foto produk, live Shopee | "Paket gajian serum+sunscreen"; "Voucher 10.10 berlaku 10 Okt saja"; "Bundling hemat ... "; "Gratis ongkir s/d ..."; "Stok batch baru" |

**4. Rencana anggaran:** tabel di atas disalin apa adanya. TikTok Ads tidak dipakai: "uangnya terlalu tipis untuk diuji di sana; fokus Meta & Shopee dulu, TikTok tetap organik".
**5. Kreatif & uji:** M1 sudut "cocok iklim lembap" vs "hemat langkah" (Meta, 2 iklan); M2 hook; M3 visual; M4 penawaran gajian/10.10 dengan batas waktu asli.
**6. Kalender momen:** gajian ±25, 10.10 (tanggal tetap; syarat voucher cek Seller Center).
**7. Aturan keputusan:** dari `references/aturan-keputusan.md` (hentikan di bawah 2,23x setelah ≥ Rp54.000 terpakai per iklan; naikkan maks +20% bila > 3,18x stabil 2 minggu).
**8. Kepatuhan:** kosmetik = kategori terbatas; tanpa klaim "menyembuhkan jerawat/memutihkan permanen", tanpa foto sebelum-sesudah bernuansa medis, klaim sesuai penandaan BPOM; musik berlisensi; label AI bila memakai model AI.
**9. 3 langkah hari ini:** salin 10 pertanyaan DM tersering; pilih 2 konten organik terbaik 30 hari terakhir sebagai kandidat iklan Meta; rapikan foto/judul/ulasan 3 produk teratas di Shopee sebelum Shopee Ads.

## Verifikasi angka independen (penguji, Fraction)
- 3.000.000 x 35/55 = 1.909.090,9 -> 1.909.091; x 20/55 = 1.090.909,1 -> 1.090.909; jumlah 3.000.000. OK.
- Meta per minggu 1:1:1:2 -> 381.818,2 x3 + 763.636,4 -> pembulatan 381.818 x3 + 763.636 = 1.909.090 -> sisa +1 ke minggu 4 = 763.637. OK. Shopee 218.182 x3 + 436.364 = 1.090.910 -> sisa -1 -> 436.363. OK. Total per minggu 600.000/600.000/600.000/1.200.000. OK.
- Uji 30%: 572.727,3 -> 572.727; aman 1.336.364. Shopee 327.272,7 -> 327.273; aman 763.636. OK.
- ROAS impas 1/0,45 = 2,222 -> 2,23 (ke atas). ROAS target 1/(0,45x0,7)=3,1746 -> 3,18. CPA target 54.000x0,7 = 37.800. Pesanan 3.000.000/54.000 = 55,6 -> 56. OK.
- TikTok dibuang: bagian 3.000.000x20/75 = 800.000 < 28 x 30.000 = 840.000. OK. Iklan maks Meta 381.818 // 175.000 = 2; Shopee 218.182 // 70.000 = 3. OK.

**Penilaian:** lengkap, angka benar, pilar dari kebutuhan pembeli, kepatuhan kosmetik ada. Kekurangan: kata "skincare" tidak otomatis memicu catatan TERBATAS di script (agent harus ingat dari referensi).
