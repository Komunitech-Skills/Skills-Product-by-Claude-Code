# HASIL UJI — foto-produk-brief

- **Tanggal:** 2026-09-23
- **Penguji:** agent penguji independen (simulasi, Claude Code)
- **Jenis skill:** instruksi + referensi + template (tidak ada script)

## Ringkasan pengujian
| Uji | Hasil |
|---|---|
| Audit keamanan | Hanya file Markdown. Tidak ada script, perintah, jaringan, kredensial, atau prompt injection ✅ |
| S1 hijab 4 warna, Android tanpa tripod, jendela timur | Brief lengkap & bisa dieksekusi; keluhan "warna beda" dijawab spesifik |
| S2 minuman, malam hari, LED + tripod | Jalur tanpa jendela (LED dipantulkan) & backlight botol bening dipakai |
| S3 malas (lilin) | Default + asumsi, shot list 9 foto |
| S4 tanpa info produk | 5 pertanyaan + jalur cepat + 3 tips langsung |
| S5 edit foto, before-after, foto brand lain, deskripsi | Ditolak/diarahkan dengan benar (`listing-marketplace`) |
| Klaim platform | SKILL.md, `teknik-hp.md` §5, dan checklist mengarahkan jumlah slot, ukuran file & durasi ke Seller Center ✅. Yang disebut hanya praktik umum (1:1, 3:4 "sebagian kategori", ≥ 1080 px "aman", tanpa nomor WA di foto) dengan kata "umum/cek ketentuan terbaru" ✅ |
| Eksekusi dengan HP | Semua alat gratis/murah (karton, gorden, styrofoam, buku, timer). Tidak mewajibkan alat mahal ✅ |
| Uji A/B | Skill jelas lebih baik (agent umum menyarankan menaikkan saturasi dan mengarang angka platform) |
| Banding pesaing | Menang vs `product-shots` (motiful, MIT) |

## Skor
| Kriteria | Skor (1–10) | Alasan |
|---|---|---|
| Pemicu (description) | 9 | Jelas; batas dengan listing/caption/live tegas |
| Kemudahan awam | 9 | Bahasa sederhana, sketsa teks, alat rumahan |
| Kualitas output | 9 | Lembar kerja lengkap: shot list tabel, storyboard per detik, checklist, penamaan file |
| Akurasi (fakta) | 8 | Tidak mengarang aturan platform. Detail kecil: AE/AF lock ditulis "berlaku umum iPhone & Android" |
| Penanganan input kurang | 9 | Sekali tanya, maks. 5, dengan default |
| Penanganan di luar cakupan | 9 | Edit foto, before-after, hak cipta, listing: benar |
| Keamanan | 10 | – |

## SKOR AKHIR: **8 / 10 — LULUS**

## Daftar cacat & saran perbaikan

### Berat
- Tidak ada.

### Sedang
- Tidak ada.

### Ringan
1. `references/teknik-hp.md` §3 butir 4 ("tekan lama untuk mengunci fokus & pencahayaan (AE/AF Lock), geser ikon matahari") ditulis "berlaku umum iPhone & Android". Pada banyak kamera bawaan Android, fitur ini berbeda atau hanya ada di mode Pro. **Perbaikan:** tambahkan "(nama & letaknya beda per merek; di sebagian Android pakai mode Pro/Manual → kecerahan/EV)".
2. `references/teknik-hp.md` §1 jam "pagi ±08.00–10.30" tanpa kaitan arah jendela. Untuk jendela **timur**, pagi adalah saat sinar matahari langsung masuk. Tambahkan tabel kecil: jendela timur → siang/sore; barat → pagi–siang; utara/selatan → hampir sepanjang hari.
3. `references/shot-list-kategori.md` tidak punya catatan keselamatan untuk produk api/listrik (lilin, diffuser, elektronik menyala saat difoto): jangan tinggalkan menyala tanpa diawasi, jauhkan dari kain/karton. Tambahkan di "Rumah tangga" dan "Elektronik".
4. Tidak ada panduan singkat "tes warna" (bandingkan layar dengan barang asli + kertas putih sebagai acuan) di SKILL.md langkah 3, padahal keluhan "warna beda" adalah pemicu umum skill ini (disebut di "Kapan digunakan"). Pindahkan poin dari `teknik-hp.md` §6 ke langkah kerja/checklist utama.
5. SKILL.md bagian Format output belum meminta **urutan prioritas slot** bila jumlah slot platform lebih sedikit dari shot list. Tambahkan satu baris "jika slot terbatas, prioritaskan: utama → varian → ukuran → dipakai → detail".

## Verifikasi angka
Tidak ada script. Tidak ada angka platform yang ditetapkan skill; angka yang muncul di contoh (ukuran 115 × 115 cm, 1 L, dll.) berasal dari pengguna dan selalu diberi syarat "setelah diukur ulang".
