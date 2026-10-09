---
name: analisis-ulasan
description: Meringkas puluhan sampai ribuan ulasan pelanggan (tempelan teks atau CSV ekspor Shopee/Tokopedia/TikTok Shop/Google Maps) menjadi sebaran bintang, tema keluhan & pujian teratas lengkap dengan jumlah dan kutipan singkat tanpa nama pelanggan, prioritas perbaikan produk/layanan, dan ide konten dari pujian; paham bahasa gaul seperti "brg", "bgt", "mantul", "ga sesuai". Gunakan saat pengguna minta analisis/rekap/rangkuman ulasan, review, rating, atau komplain pembeli (review analysis, customer feedback insights, sentiment summary). Membalas satu ulasan pakai balas-ulasan-pelanggan.
---

# Analisis Ulasan Pelanggan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah tumpukan ulasan menjadi laporan satu halaman: apa yang paling sering dikeluhkan, apa yang paling disukai, apa yang harus diperbaiki duluan, dan konten apa yang bisa dibuat dari pujian. Semua angka dihitung script; tema dipastikan agent dengan bukti kutipan.

## Kapan digunakan
- "Tolong rangkum 200 ulasan toko saya", "keluhan pembeli paling banyak apa?"
- Pengguna mengirim CSV ulasan, atau menempel banyak ulasan sekaligus (minimal ±10).
- Membandingkan ulasan antar-produk atau antar-bulan (jika ada kolom produk/tanggal).

## Kapan TIDAK digunakan
- Membalas satu/beberapa ulasan → skill `balas-ulasan-pelanggan`.
- Membalas chat komplain pribadi → `balas-chat-cs`.
- Rekap omzet/penjualan → `rekap-penjualan-csv`.
- Kurang dari ±5 ulasan: tidak perlu statistik; baca langsung dan beri saran singkat.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Ulasan: file CSV/TSV ekspor atau teks tempelan | Ya | — (minta tempel, satu ulasan per baris, format `bintang \| ulasan`) |
| Bintang per ulasan | Tidak | Dianalisis tanpa sebaran bintang; skor prioritas memakai bobot netral (sebutkan) |
| Nama toko/produk & jenis usaha | Tidak | Ditebak dari isi ulasan; sebut asumsinya |
| Periode ulasan | Tidak | "Periode sesuai data yang dikirim" |
| Tujuan khusus (mis. fokus produk X, siap rapat tim) | Tidak | Laporan lengkap 7 bagian |

Jika ulasan belum dikirim, minta **sekali**: (1) tempel ulasan atau kirim file CSV, (2) sertakan bintangnya bila ada, (3) nama produk/toko. Untuk teks tempelan, simpan dulu ke file `.txt` di folder kerja pengguna (satu ulasan per baris, atau pisahkan ulasan dengan baris kosong). Format bintang yang dikenali: `5 | teks`, `★★★★★ teks`, `⭐⭐⭐ teks`, `bintang 4 - teks`, `4/5 teks`, `Rating: 4 teks`. Contoh format: `templates/format-tempel.txt`.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Siapkan file.** CSV dipakai apa adanya (Excel `.xlsx` → minta simpan sebagai CSV). Teks tempelan → tulis ke `ulasan.txt`.
2. **Jalankan script** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/olah_ulasan.py ulasan.csv
   python3 <folder-skill-ini>/scripts/olah_ulasan.py ulasan.txt --format teks   # ringkasan cepat
   ```
   - Kolom ulasan/bintang/produk/tanggal dideteksi otomatis; kolom nama/username pembeli **diabaikan**. Jika deteksi gagal, script menampilkan daftar kolom → ulangi dengan `--kolom-ulasan "..." --kolom-bintang "..."` (juga `--kolom-produk`, `--kolom-tanggal`).
   - Untuk memeriksa satu tema: `--detail-tema k_pengiriman` (daftar id tema ada di `references/kamus-tema.md`).
   - Kata khas usaha yang tidak dikenali (mis. istilah produk) → buat `kamus.json` di folder kerja dan pakai `--kamus-tambahan kamus.json` (format di `references/kamus-tema.md`).
   - Kamus bawaan mencakup toko online **dan** tempat makan/jasa (waktu tunggu, kebersihan & benda asing, fasilitas parkir/toilet/AC/wifi, suasana).
3. **Verifikasi tema (wajib, jangan dilewati).** Hasil script adalah *kandidat*:
   - Baca `contoh` tiap tema. Jika kutipan tidak cocok dengan labelnya, pindahkan/koreksi dan sebut koreksinya di catatan metode.
   - Baca `perlu_dibaca_agent`: ulasan bintang rendah tanpa keluhan terdeteksi dan ulasan `belum_terklasifikasi` (plus `kata_teratas`-nya). Jika ada pola berulang (≥ 3 ulasan atau ≥ 5%), buat tema tambahan dan hitung jumlahnya dengan menjalankan ulang script memakai `--kamus-tambahan`, bukan dengan menebak.
   - Ulasan bintang 4–5 yang tetap mengeluh adalah sinyal dini — sebutkan.
   - **Salah tangkap?** Jangan mengoreksi angka dengan tangan. Hitung ulang lewat script: `--abaikan-id k_respons:3,14` (buang tema dari ulasan tertentu yang sudah dibaca) atau pola `"kecualikan"` per tema di `kamus.json` (mis. `{"tema":[{"id":"k_kualitas","kecualikan":["\\bmati\\W+lampu\\b"]}]}`). Sebut koreksinya di catatan metode.
   - Gabungkan tema yang sebenarnya sama bagi pengguna (mis. "salah kirim" + "barang kurang" untuk toko kecil) dan jelaskan.
4. **Susun prioritas perbaikan** dengan aturan di bawah dan `references/tindakan-per-tema.md`.
5. **Buat 3–5 ide konten** dari pujian terbanyak dengan aturan di `references/ide-konten.md`.
6. Tulis laporan dengan format di bawah, lalu periksa checklist.
7. **Fallback tanpa Python:** hitung manual — sebaran = jumlah ulasan per bintang; rata-rata = total bintang ÷ ulasan berbintang; persen = jumlah ÷ pembagi × 100 (1 desimal); skor prioritas keluhan = Σ bobot (1★=5, 2★=4, 3★=3, 4★=2, 5★=1, tanpa bintang=3). Kelompokkan tema dengan membaca tiap ulasan. Tulis di laporan: "dihitung manual, belum diverifikasi script".

### Aturan prioritas perbaikan
Urutan awal = `peringkat_prioritas` dari script (skor = seberapa sering × seberapa parah bintangnya). Lalu sesuaikan:
- **Segera (minggu ini):** skor tertinggi, ATAU menyangkut keamanan/kesehatan (basi, kedaluwarsa, **rambut/serangga/benda asing** di makanan, tempat kotor, bau aneh pada makanan/kosmetik, produk listrik bermasalah) walau jumlahnya sedikit, ATAU perbaikan murah yang bisa dikerjakan sendiri (deskripsi, tabel ukuran, cara packing).
- **Bulan ini:** perlu biaya/pemasok (bahan, kualitas jahitan, ganti kurir).
- **Pantau:** 1–2 ulasan saja, atau di luar kendali langsung (kurir) — tetap tuliskan langkah mitigasinya.
Setiap prioritas wajib punya: bukti (jumlah + kutipan), tindakan konkret (siapa, apa), dan ukuran keberhasilan yang bisa dicek (mis. "keluhan ukuran turun di bawah 5% ulasan bulan depan").

## Format output
```
# Analisis Ulasan — <produk/toko> (<periode>, <N> ulasan)

## Ringkasan cepat
- <temuan 1 dengan angka> - <temuan 2> - <1 tindakan paling penting>

## Sebaran bintang
| Bintang | Jumlah | % |   (+ rata-rata, % positif 4–5★ / netral 3★ / negatif 1–2★)

## Keluhan teratas
| # | Keluhan | Ulasan (%) | Rata-rata ★ | Contoh kutipan (tanpa nama) | Area |

## Pujian teratas
| # | Pujian | Ulasan (%) | Contoh kutipan |

## Prioritas perbaikan
| Prioritas | Masalah | Bukti | Tindakan konkret | Ukuran keberhasilan |

## Ide konten dari pujian
1. <format + platform> — Hook: "..." — Kutipan yang dipakai: "..." — CTA

## Catatan metode
Jumlah ulasan dibaca/dilewati, koreksi tema oleh agent, peringatan script, batasan.
```
Tabel Markdown, Rupiah (bila ada) format `Rp 1.250.000`, persen memakai koma desimal (`12,5%`).

## Contoh
**Input pengguna:** "Ini 120 ulasan keripik pedas saya dari Shopee (file ulasan.csv). Apa yang harus saya benahi?"

**Output (dipersingkat):**
```
## Ringkasan cepat
- Rata-rata 4,3★; 78,3% ulasan positif, 11,7% negatif (1–2★).
- Keluhan terbesar: kemasan bocor/remuk (9 ulasan, 7,5%; rata-rata 1,9★) — paling merusak bintang.
- Pujian terbesar: rasa pedas gurih (41 ulasan) → bahan konten testimoni.

## Keluhan teratas
| # | Keluhan | Ulasan (%) | Rata ★ | Contoh kutipan | Area |
| 1 | Kemasan bocor/remuk | 9 (7,5%) | 1,9 | "keripiknya remuk semua, plastik sobek" | Packing |
| 2 | Terlalu pedas / rasa berubah | 6 (5%) | 2,5 | "level 3 kok kayak level 5, beda sama kemarin" | Produk |

## Prioritas perbaikan
| Segera | Kemasan remuk | 9 ulasan, rata 1,9★ | Tambah kardus + bubble wrap; foto isi paket sebelum dikirim | Keluhan kemasan < 2% ulasan bulan depan |
```

## Checklist sebelum mengirim hasil
- [ ] Semua angka (jumlah, %, rata-rata, skor) berasal dari output script atau hitung manual yang disebut.
- [ ] Tidak ada nama, username, nomor HP, nomor pesanan/resi pelanggan di laporan (kutipan sudah disamarkan; periksa ulang).
- [ ] Kutipan asli, pendek (≤ 1 kalimat), tidak diubah maknanya; tanda "…" jika dipotong.
- [ ] Tema sudah diverifikasi dengan membaca kutipan; ulasan "belum terklasifikasi" & bintang rendah tanpa keluhan sudah dibaca.
- [ ] Tiap prioritas punya bukti + tindakan konkret + ukuran keberhasilan.
- [ ] Ide konten tidak memakai nama pelanggan tanpa izin & tanpa klaim yang tidak ada di ulasan.
- [ ] Peringatan script (sampel kecil, bintang tidak valid, encoding) disampaikan.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` bila file tidak ada/kosong, hanya berisi judul kolom, kolom tidak dikenali, atau kamus tambahan rusak — sampaikan pesan itu dengan bahasa sederhana dan minta perbaikan.
- Kamus kata kunci tidak paham sarkasme ("mantap, 2 minggu baru sampai") dan konteks yang sangat khusus; karena itu verifikasi agent di langkah 3 wajib.
- Sampel < 20 ulasan: sebut sebagai gambaran awal, jangan menyimpulkan tren.
- Ulasan palsu/spam tidak bisa dipastikan; script hanya menandai teks duplikat persis.
- **Permintaan membuat/menulis ulasan palsu, membeli ulasan, atau menghapus/menyembunyikan ulasan pembeli asli → tolak** (menyesatkan konsumen, UU 8/1999 Pasal 10, dan melanggar aturan platform). Tawarkan gantinya: analisis ulasan yang ada, perbaikan masalahnya, dan cara meminta ulasan jujur dari pembeli asli (tanpa imbalan bersyarat bintang). Ulasan yang diduga palsu dari pesaing → laporkan lewat fitur platform, balas dengan skill `balas-ulasan-pelanggan`.
- UU PDP: jangan menyimpan atau menampilkan data pribadi pembeli. Laporan memakai kutipan anonim. Untuk memakai ulasan sebagai testimoni iklan, sarankan meminta izin pembeli dan menyamarkan identitas.
- Jangan mengarang penyebab ("pasti karena kurir X") tanpa bukti di ulasan; tulis sebagai dugaan yang perlu dicek.
