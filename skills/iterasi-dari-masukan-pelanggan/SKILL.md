---
name: iterasi-dari-masukan-pelanggan
description: Mengubah masukan pelanggan dari SEMUA kanal (chat WhatsApp hasil ekspor, ulasan Shopee/Tokopedia/Google Maps, komentar Instagram/TikTok, survei) menjadi rencana perbaikan berurutan - data pribadi disamarkan otomatis, tema (rasa, kemasan, harga, pengiriman, layanan), sentimen, tren bulanan, skor jumlah x dampak, backlog perbaikan, template balasan ke pelanggan, kabar perbaikan, dan siklus bulanan. Gunakan saat pengguna minta olah masukan/feedback/komplain/saran pelanggan, "apa yang harus kami perbaiki dulu", rencana perbaikan produk/layanan, atau menutup lingkaran ke pelanggan (customer feedback synthesis, voice of customer, improvement backlog, close the loop). Hanya ulasan marketplace: analisis-ulasan. Membalas satu ulasan publik: balas-ulasan-pelanggan.
---

# Iterasi dari Masukan Pelanggan

## Tujuan
Menyatukan masukan yang tercecer di banyak tempat menjadi satu daftar "perbaiki ini dulu, begini caranya, begini cara mengabarkannya ke pelanggan", lalu mengulanginya tiap bulan agar terlihat apakah perbaikan berhasil. Angka dihitung script; tema dan prioritas diverifikasi agent dengan bukti kutipan.

## Kapan digunakan
- "Ini chat WA pelanggan + ulasan Shopee bulan ini, apa yang harus kami benahi?"
- Masukan datang dari lebih dari satu kanal, atau dari chat/komentar/survei (bukan hanya ulasan bintang).
- Perlu rencana perbaikan, balasan tindak lanjut, kabar perbaikan ke pelanggan, atau rekap bulanan.

## Kapan TIDAK digunakan
- Hanya ulasan marketplace/Google Maps dan ingin laporan bintang + ide konten -> `analisis-ulasan`.
- Membalas SATU ulasan publik -> `balas-ulasan-pelanggan`; membalas chat komplain -> `balas-chat-cs`.
- Masukan dari karyawan (bukan pelanggan), atau kurang dari ±8 masukan: baca langsung, beri saran singkat tanpa statistik.
- Meminta membuat ulasan/komentar palsu, mengambil nomor pelanggan untuk promosi, atau mengirim pesan massal otomatis: tolak (lihat Batasan).

## Input
| Info | Wajib? | Default |
|---|---|---|
| Masukan: file ekspor chat WA (.txt), CSV ulasan/survei, atau teks tempelan (IG/TikTok/DM) | Ya, minimal satu kanal | Minta sekali (lihat bawah) |
| Nama usaha & jenis usaha | Tidak | Ditebak dari isi; sebut asumsinya |
| Nama pemilik/admin di chat WA (agar pesan tim tidak dihitung) | Tidak | Jalankan `--daftar-pengirim`, tanya pengguna siapa tim |
| Tanggal per masukan | Tidak | Tren tidak dihitung; sebut "garis dasar" |
| Kapasitas (siapa & berapa jam sebulan) | Tidak | Asumsikan pemilik + 1 staf, maks. 3 perbaikan per bulan |

Bila belum ada data, tanyakan **sekali**: (1) kanal apa saja & bagaimana mengambil datanya (`templates/cara-ekspor-chat-whatsapp.txt`; ulasan: ekspor CSV atau salin-tempel; komentar IG/TikTok: salin-tempel satu per baris), (2) periode, (3) jenis usaha. Teks tempelan disimpan ke `.txt` di folder kerja (satu masukan per baris, boleh diawali `5 | ...`).

## Langkah kerja
1. **Kumpulkan & simpan file** per kanal di folder kerja. Jangan tempel data mentah ke laporan.
2. **Cek pengirim WA** (bila ada chat): `python3 <folder-skill-ini>/scripts/olah_masukan.py chat.txt --daftar-pengirim` (Windows: `python` atau `py`). Nama hanya untuk Anda: **jangan salin nama itu ke laporan**. Tanyakan pengguna siapa yang tim; sebut di `--staf`.
3. **Jalankan script** (semua kanal sekaligus; nama kanal setelah `=`):
   ```bash
   python3 <folder-skill-ini>/scripts/olah_masukan.py chat.txt=WhatsApp ulasan.csv=Shopee komentar.txt=Instagram survei.csv=Survei --staf "Admin,Dapur" --simpan-anonim anonim-2026-09.csv
   ```
   - Data pribadi disamarkan **sebelum** analisis (nama pengirim, HP, email, tautan, @akun, nomor pesanan/resi, alamat, "kak Budi"). Kolom nama pembeli di CSV tidak dibaca. Detail & batasnya: `references/privasi-dan-etika.md`.
   - Kolom CSV dikenali otomatis (survei dengan judul kolom bebas juga). Jika gagal: `--kolom-teks "Komentar" --kolom-bintang "Rating" --kolom-tanggal "Tanggal"`.
   - Tema/kata khas usaha: salin `templates/tema-contoh.json` menjadi `tema.json`, lalu `--tema tema.json`.
   - Tambah `--format json` untuk data lengkap (tren per bulan per tema, kutipan pujian, saran).
4. **Verifikasi (wajib).** Hasil script = kandidat:
   - Baca kutipan tiap tema; koreksi yang salah kelompok dan sebut koreksinya di Catatan metode (jangan mengubah angka dengan tangan: perbaiki lewat `tema.json` lalu jalankan ulang).
   - Baca "Perlu dibaca agent" (masukan tanpa tema): bila ≥ 3 masukan atau ≥ 5% berpola sama, buat tema baru di `tema.json` dan jalankan ulang.
   - Periksa ulang kutipan untuk sisa data pribadi (nama tanpa sapaan, nama kantor, foto) sebelum dipakai.
   - Pujian bintang 4-5 yang tetap mengeluh = sinyal dini; sebut.
   - Bandingkan antarkanal: isu di ≥ 2 kanal lebih kuat. Sebut kanal yang bias (mis. WA didominasi pelanggan yang komplain).
5. **Susun prioritas** dengan `references/prioritas.md`: skor script + penyesuaian (keamanan selalu Segera, jangkauan kanal, tren, usaha). Pecah permintaan pelanggan ("tambah menu X") menjadi masalah di baliknya + 2-3 alternatif solusi + uji murah.
6. **Buat backlog perbaikan** (`templates/backlog-perbaikan.csv`): tiap baris punya bukti (jumlah + kutipan), tindakan konkret, penanggung jawab, tenggat, ukuran keberhasilan berangka. Maks. 3 perbaikan aktif sebulan (sesuaikan kapasitas).
7. **Tutup lingkaran ke pelanggan** (`templates/balasan-pelanggan.md`): draf balasan per situasi A-E untuk dikirim **manusia**; untuk balasan publik di ulasan arahkan ke `balas-ulasan-pelanggan`. Bila ada perbaikan selesai, tulis **kabar perbaikan** dengan `templates/catatan-perbaikan-pelanggan.md` (bahasa pelanggan, tanpa nama, tanpa janji yang belum pasti).
8. **Atur siklus bulanan** (`references/siklus-bulanan.md`): simpan `anonim-YYYY-MM.csv`; bulan berikutnya jalankan ulang seluruh file gabungan agar tren muncul; nilai apakah ukuran keberhasilan tercapai; tutup/lanjutkan.
9. Tulis laporan (format di bawah), lalu periksa checklist.
10. **Fallback tanpa Python:** hitung manual - jumlah masukan per kanal; kelompokkan tema dengan membaca; keluhan per tema = jumlah masukan yang mengeluh; skor = keluhan x dampak (tabel dampak di `references/prioritas.md`). Tulis "dihitung manual, belum diverifikasi script". Samarkan data pribadi dengan tangan.

## Format output
```
# Rencana Perbaikan dari Masukan Pelanggan - <usaha> (<periode>, <N> masukan)

## Ringkasan cepat
- 3 temuan berangka + 1 tindakan terpenting minggu ini

## Sumber & kualitas data
| Kanal | Jumlah | Catatan bias |   (+ sentimen positif/netral/negatif, N tidak dihitung & alasannya)

## Isu teratas
| # | Tema | Keluhan (%) | Pujian | Dampak | Skor | Tren | Kanal | Prioritas |

## Bukti & analisis per isu utama (maks. 5)
- Kutipan tanpa nama, masalah di baliknya, penyebab dugaan (tandai "dugaan")

## Backlog perbaikan
| Prioritas | Perbaikan | Bukti | Tindakan | Siapa | Tenggat | Ukuran keberhasilan |

## Yang jangan diubah (pujian)
## Saran & permintaan pelanggan (masalah di baliknya, alternatif, uji murah)
## Tindak lanjut ke pelanggan
- Draf balasan (template terpilih) + kabar perbaikan
## Rencana bulan depan
- Jadwal ekspor, ukuran yang dicek, pertanyaan survei singkat (maks. 3)
## Catatan metode
- Koreksi tema, aturan penyamaran, batasan data
```
Bila pengguna minta cepat: tampilkan Ringkasan, Isu teratas, Backlog, dan sebut asumsinya.

## Contoh singkat
Masukan: 12 pesan WA + 26 ulasan Shopee + 5 komentar IG + 8 jawaban survei (katering harian).
Ringkasan: "Pengiriman telat = isu #1: 9 dari 51 masukan (17,6%), muncul di 4 kanal. Ada 3 laporan rambut/ulat di makanan (dampak 5) -> Segera. Kemasan bocor naik 6,4 poin bulan ini." Backlog: "Ganti kurir area kantor + jadwal kirim 30 menit lebih awal (Ibu Rini, 7 Okt; ukuran: keluhan telat < 10%)." Contoh lengkap: `examples/`.

## Batasan & penanganan error
- Tema dari kata kunci **belum** memahami sarkasme atau konteks panjang; itu sebabnya verifikasi kutipan wajib. Teks campur bahasa daerah/emoji: baca manual dan tambahkan kata ke `tema.json`.
- Data sedikit: < 30 masukan = arah saja, jangan menyimpulkan persentase; tren bulanan butuh ≥ 5 masukan per bulan (script menulis "data kurang").
- Masukan hanya dari pelanggan yang mau bicara (bias): jangan klaim mewakili semua pelanggan; saran tambah survei singkat 3 pertanyaan.
- Format tanggal ekspor WA diasumsikan hari/bulan (umum di Indonesia); bila bulan tampak terbalik, perbaiki lewat CSV.
- Ekspor chat berisi pelanggan tak sengaja dari chat pribadi: hentikan, minta hanya chat usaha.
- Berkas kosong/rusak: script berhenti dengan pesan jelas (kode 2) - minta ekspor ulang, jangan mengarang data.
- Keluhan berat (keracunan, sakit, ancaman hukum, penipuan): jangan dianalisis sebagai statistik saja; sarankan pemilik menanganinya langsung dan segera, dan konsultasi ke profesional bila perlu. Ini bukan nasihat hukum/medis.
- **Ditolak:** membuat/membeli ulasan palsu, menyalin nomor dari ekspor untuk promosi, kirim pesan massal otomatis (WhatsApp tidak resmi & berisiko blokir), scraping ulasan lewat login browser, mengidentifikasi pelanggan tertentu dari data yang sudah disamarkan.
- Skill tidak menjanjikan hasil penjualan; ia mengurutkan bukti agar keputusan lebih terarah.

## Checklist sebelum mengirim hasil
- [ ] Tidak ada nama, nomor HP, email, alamat, nomor pesanan di laporan (kutipan sudah dibaca ulang)
- [ ] Semua angka berasal dari script (atau ditandai manual)
- [ ] Tiap prioritas punya bukti, tindakan, siapa, tenggat, ukuran berangka
- [ ] Keamanan/kesehatan ditandai Segera
- [ ] Balasan ke pelanggan berupa draf untuk dikirim manusia; tidak ada kirim massal
- [ ] Asumsi & batas data (bias kanal, jumlah kecil) ditulis
