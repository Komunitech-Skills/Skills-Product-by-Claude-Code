# 00 — Uji banding pesaing: skenario 01

> Tahap 6 butir 5. Pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pesaing yang dicari
| Sumber | Kandidat | Catatan |
|---|---|---|
| skills.sh | `coreyhaines31/marketingskills` → `pricing` (tercatat di skills.sh sebagai pricing-strategy, ±62,0 rb instal) | Terpopuler; snapshot commit `5b2c000` (2026-09-04). Fokus SaaS (value metric, tier, freemium, Van Westendorp), tanpa hitungan |
| GitHub | `phuryn/pm-skills` → `pm-product-strategy/skills/pricing-strategy` (85 baris) | Kerangka PM/SaaS, tanpa hitungan; commit `8607e3b` |
| skills.sh | `kostja94/marketing-skills` → pricing-strategy (±834 instal) | SaaS/tools, tanpa hitungan |
| ClawHub (clawhub.ai, cari "pricing", 2026-09-29) | Terbanyak untuk harga umum: `Pricing` @ivangdavila ±2,9 rb unduh; `pricing-strategy` @phuryn ±2,8 rb; `ecommerce-pricing-strategy` @thcjp ±306 (lainnya khusus Azure/App Store/Amazon/freight) | Semua jauh di bawah ±62 rb instal marketingskills; tidak ada yang untuk UMKM/Rupiah. Hanya daftar yang dibaca, isi tidak diunduh |

Dipilih pesaing terkuat: **marketingskills `pricing`** (instal & bintang tertinggi, pembuat kredibel). Catatan: skill kita mengadaptasi kerangka dari sumber ini (MIT), jadi uji ini sekaligus menguji nilai tambahnya.

Cara uji: sesi `claude -p` baru, folder sementara berisi hanya skill pesaing di `.claude/skills/pricing/`, prompt identik dengan skenario 01.

## Output DENGAN skill pesaing (apa adanya)

Menurutku 49.900 masuk akal, tapi jangan jadikan itu satu-satunya keputusan. Deal kantor dan reseller nilainya jauh lebih besar daripada kenaikan harga.

## Hitungan kondisi sekarang
- Margin per botol: 45.000 − 22.000 = **23.000**
- Laba bersih: 400 × 23.000 − 5,2 jt = **±4,0 jt/bulan**

## Kalau naik ke 49.900
- Margin per botol jadi **27.900**, naik 21%.
- Laba tetap 4 jt kalau volume turun sampai **±330 botol**, yaitu boleh hilang 70 botol (17%). Titik impas ini jadi batas aman untuk uji harga.
- Kalau volume tetap 400, laba jadi ±5,96 jt.
- 49.900 masih di bawah pesaing yang jual 55rb. Kamu juga sudah di atas dua pesaing di 35rb dan 42rb, dan tetap laku 400 botol. Banyaknya yang minta reseller dan kantor mau ambil rutin menandakan harga 45rb belum terasa berat.
- Alasan "gula aren naik" itu wajar dan bisa kamu pakai saat memberi tahu pelanggan. Coba hitung kenaikan modalnya. Kalau modal jadi 24rb, margin di 45rb tinggal 21rb, jadi kenaikan ke 49.900 sebagian cuma menutup biaya.

## Struktur harga yang kusarankan
| Jalur | Harga | Margin/botol | Catatan |
|---|---|---|---|
| Eceran / langsung | **49.900** | 27.900 | Ini harga acuan. Reseller tidak boleh jual di bawahnya. |
| Reseller | **±39.900** (diskon ~20%) | ±17.900 | Minimal order 10–20 botol. Reseller untung ±10rb, cukup untuk mereka. |
| Kantor 100 botol/minggu | **±42.000** (atau 40.000 kalau kontrak 3 bulan) | 18.000–20.000 | Bayar di muka atau termin maksimal 7 hari. |

- **Kantor:** 400 botol/bulan × 20.000 = **+8 jt/bulan** kalau kapasitas dapur dan tenaga kerja cukup. Ini lebih dari dua kali lipat laba sekarang, jauh di atas tambahan ±2 jt dari kenaikan harga. Pastikan dulu produksi 800 botol/bulan sanggup, dan hitung ongkos antar. Kalau perlu tambah tenaga part-time, biayanya masih tertutup.
- **Reseller:** kalau eceran tetap 45rb, diskon 20% jadi 36rb dan margin kamu tinggal 14rb. Harga eceran 49.900 membuat jalur reseller lebih sehat. Mulai dengan 3–5 reseller terbaik supaya kualitas dan harga tetap terkontrol.
- **Bundling:** jual 2 botol 95rb (47.500/botol). Ini mendorong orang beli lebih banyak tanpa menurunkan harga acuan.

## Cara menaikkan harga
1. Pakai harga baru untuk pelanggan baru dan kanal baru (reseller, kantor) lebih dulu, supaya dapat pembacaan yang bersih.
2. Beri tahu pelanggan lama 1–2 minggu sebelumnya, misalnya: "Harga gula aren naik, mulai tanggal X harga jadi 49.900." Kalau perlu, beri satu kali promo beli 2 lebih murah.
3. Pantau 3–4 minggu. Kalau volume eceran tetap di atas ±330 botol, harganya aman. Kalau turun jauh di bawah itu, turunkan ke 47.500.
4. Naik bertahap 45 → 47.500 → 49.900 juga boleh kalau kamu takut. Tapi karena permintaan kuat, langsung 49.900 lebih efisien.

## Yang perlu kamu cek
- Berapa modal gula aren sekarang per botol, dan apakah 22rb itu sudah naik?
- Kapasitas maksimal dapur per bulan.
- Kenapa pelanggan beli: rasa, kemasan, atau kebiasaan? Kalau alasannya jelas, kamu bisa memposisikan produkmu sebagai premium.

Kalau kamu kirim angka modal gula aren yang baru dan kapasitas produksi, aku bisa hitung ulang skenario laba dan harga untuk kantor dan reseller.

## Output DENGAN skill kita
Lihat `01-kopi-literan-naik-harga-reseller.md`.

## Penilaian berdampingan (1–10)
| Kriteria | Pesaing (`pricing`) | Kita (`strategi-harga-produk`) |
|---|---|---|
| Ketepatan angka | 7 — yang dihitung benar (5,96 jt; impas 330); "titik impas" dipakai untuk volume impas (istilah keliru); laba kantor 8 jt pada asumsi 400 botol × 20 rb | 8 — semua benar, sebagian dihitung manual |
| Kelengkapan hitungan | 4 — tanpa BEP, tanpa lantai margin, tanpa % margin | 9 — BEP, lantai, diskon maksimal, volume impas, estimasi 3 tingkat |
| Relevansi konteks UMKM Indonesia | 6 — model tetap berpikir tier/"pembacaan bersih" gaya SaaS; bahasa baik | 9 — reseller, harga eceran anjuran, teks WA, asumsi non-PKP |
| Kejujuran estimasi | 6 — "langsung 49.900 lebih efisien" tanpa label estimasi | 9 — label ESTIMASI, uji kecil |
| Siap pakai | 6 — tabel + langkah, tanpa teks siap tempel | 8 — tabel + langkah + teks pengumuman |
| Konsistensi saran | 8 | 6 — harga reseller anjuran bertentangan dengan harga toko |
| **Rata-rata** | **6,2** | **8,2** |

## Kesimpulan
**Skill kita menang** atas pesaing terpopuler. Pesaing unggul pada satu hal yang patut ditiru dengan cara kita sendiri: satu harga acuan yang konsisten untuk semua kanal (reseller "tidak boleh jual di bawah harga acuan"). Tambahan pesaing yang tidak ada di output kita: ide paket "2 botol" untuk menaikkan nilai transaksi (skill kita punya perintah `bundel`, tapi agent tidak menawarkannya).
