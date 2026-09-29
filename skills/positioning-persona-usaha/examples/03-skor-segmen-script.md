# Uji 03 — Skenario normal 3: keripik tempe Malang, bobot kustom, minta ringkas + uji data rusak

> Hasil uji independen (Tahap 6), 2026-09-29. Merek "Keripik Mbok Sri" fiktif. Semua perintah dijalankan sungguhan; angka diverifikasi ulang dengan hitungan pecahan eksak buatan penguji. Contoh bawaan pembuat dipertahankan di lampiran.

**Permintaan pengguna:**
"Aku produksi keripik tempe di Malang, cuma berdua sama adik, sehari maksimal 40 bungkus. Harga Rp 15 ribu (100 g) sampai Rp 45 ribu (toples 350 g). Jual di Shopee, TikTok Shop, dan titip di 3 toko oleh-oleh. Karena tenaga terbatas, tolong penilaian 'kemampuan melayani' dibikin lebih penting. Ringkas aja ya, yang penting target, positioning, tagline, bio."

## Langkah skor (script)
`segmen.csv`:
```
segmen,ukuran,daya_beli,kebutuhan,jangkauan_kanal,kecocokan_produk,persaingan,kemampuan_layani
Wisatawan pencari oleh-oleh Malang,5,3,3,3,5,1,4
Perantau rindu camilan kampung,3,4,3,4,5,3,5
Warung & reseller camilan,4,2,4,3,3,2,3
Kantor & komunitas (hampers/snack box),2,4,3,2,4,4,2
```
Perintah: `python3 scripts/skor_segmen.py segmen.csv --bobot "kemampuan_layani=15,ukuran=10"`
```
Bobot: ukuran 10, daya_beli 20, kebutuhan 20, jangkauan_kanal 15, kecocokan_produk 15, persaingan 10, kemampuan_layani 15
#  Segmen                              Skor  Saran
1  Perantau rindu camilan kampung      78.1  Utama (layani duluan)
2  Wisatawan pencari oleh-oleh Malan   68.6  Kandidat (uji kecil dulu)  [lemah: persaingan]
3  Kantor & komunitas (hampers/snack   61.0  Kandidat (uji kecil dulu)  [lemah: ukuran, jangkauan_kanal, kemampuan_layani]
4  Warung & reseller camilan           60.0  Kandidat (uji kecil dulu)  [lemah: daya_beli, persaingan]
```
Verifikasi independen (jumlah bobot 105, skor = Σ(bobot x nilai)/105 x 20):
| Segmen | Σ | Skor eksak | Script |
|---|---|---|---|
| Perantau | 410 | 78,095 | 78,1 ✔ |
| Wisatawan | 360 | 68,571 | 68,6 ✔ |
| Kantor | 320 | 60,952 | 61,0 ✔ |
| Warung | 315 | 60,000 | 60,0 ✔ |
Pembanding bobot awal (dihitung penguji): Perantau 15x3+20x4+20x3+15x4+15x5+10x3+5x5 = 375 → 75,0; Wisatawan 75+60+60+45+75+10+20 = 345 → 69,0. Bobot kustom tidak mengubah pemenang, hanya melebarkan jarak (6,0 → 9,5 poin). Script tidak memberi tahu bahwa jumlah bobot kini 105 (dinormalisasi otomatis, hasilnya tetap benar).

## Hasil (versi ringkas, urutan format tetap)
**Ringkasan**
- Target 90 hari: **Perantau asal Malang/Jatim yang rindu camilan kampung** (78,1). Wisatawan tetap dilayani lewat toko oleh-oleh (kanal yang sudah jalan), tidak dikejar online.
- Persona: **Fajar, 29, asal Malang, kerja di Bekasi**; beli 2-3 toples tiap akhir bulan di Shopee, sering untuk dibagi ke teman kos. Anti-persona: pencari camilan termurah < Rp 10 ribu. [H — cek dari alamat kirim pesanan]
- Positioning publik: "Keripik tempe Malang yang digoreng tiap pagi, dikirim buat kamu yang jauh dari rumah."
- Tagline: (1) "Rasa Malang, sampai ke perantauan." (5 kata) (2) "Digoreng pagi, dikirim hari ini." (5) (3) "Camilan kampung, buat yang merantau." (5) (4) "Kriuknya dari Malang." (3) (5) "Tempe asli, rasa rumah." (4). **Rekomendasi (1)** — langsung menyebut siapa & kenapa. "Dikirim hari ini" hanya dipakai bila benar (kapasitas 40 bungkus/hari).
- **Bio (123 karakter):** `Keripik tempe Malang, digoreng tiap pagi. Rasa rumah buat kamu yang merantau. Kirim se-Indonesia via Shopee & TikTok Shop 👇`
- **Judul listing:** `Keripik Tempe Malang Renyah 350 g — Digoreng Tiap Pagi, Oleh-oleh Khas` + poin: toples 350 g Rp 45 ribu / bungkus 100 g Rp 15 ribu; digoreng tiap pagi [F bila benar]; [isi: tanggal produksi di label].
- Uji 7 hari: cek kota tujuan 30 pesanan terakhir — bila ≥ 40% di luar Jawa Timur, target perantau dipertahankan.
- **Ceklis klaim:** produk pangan olahan → cek izin PIRT dan kewajiban sertifikasi halal ke sumber resmi sebelum menulis "halal"/"PIRT" di listing; jangan tulis "tanpa pengawet" tanpa dasar.

## Uji data rusak (script)
| Kasus | Hasil | Nilai |
|---|---|---|
| Nilai 6 / 0 / "tinggi" / sel kosong | `GAGAL: Baris 2 (A): 'ukuran' harus 1-5 ...`, kode 2 | ✔ |
| File kosong, hanya judul, kolom kurang, nama ganda, file hilang, bukan UTF-8 | Pesan GAGAL jelas, kode 2 | ✔ |
| `nan` di sel nilai | Ditolak (harus 1-5) | ✔ |
| Pemisah `;` (CSV Excel Indonesia) dan desimal `4,5` | Terbaca benar | ✔ |
| Nama segmen berisi koma **tanpa tanda kutip** (`Ibu muda, pengajian,3,3,4,4,4,3,5`) | **Traceback `AttributeError: 'list' object has no attribute 'strip'`, kode 1** | ✘ BUG |
| `--bobot ukuran=inf` atau `ukuran=nan` | Skor `nan`, label "Tunda", kode 0 | ✘ bug kecil |
| Kolom `ukuran` muncul dua kali | Diam-diam memakai kolom terakhir (82 jadi 73) | ✘ bug kecil |
| `--bobot "ukuran=1,5"` (desimal koma) | GAGAL "Bobot '5' salah format" — koma bentrok dengan pemisah; kode `replace(",", ".")` untuk bobot tak pernah terpakai | ✘ kecil (dokumentasi) |
| Kolom tambahan `alasan` | Diabaikan, skor benar | ✔ |
| File pemisah tab | GAGAL "Kolom 'segmen' tidak ada" (kurang jelas) | ~ |
| `scripts/uji_skor_segmen.py` bawaan | "Semua uji lulus" | ✔ |

### Catatan penguji
- Permintaan "ringkas" dipenuhi dengan memangkas bagian, urutan tetap (sesuai "Format output").
- Nama segmen di tabel dipotong 33 karakter ("...oleh-oleh Malan"); bila agent menyalin tabel apa adanya, nama segmen tampil terpotong.

---
## Lampiran: contoh bawaan pembuat (fiktif, dipertahankan)
```
segmen,ukuran,daya_beli,kebutuhan,jangkauan_kanal,kecocokan_produk,persaingan,kemampuan_layani
Karyawati muda kantoran,4,4,4,5,5,2,4
Ibu muda pengajian/arisan,3,3,4,4,4,3,5
Mahasiswi,5,2,3,5,3,2,4
Reseller kecil,3,3,3,4,4,2,2
```
Hasil: Karyawati 82,0 (Utama, lemah: persaingan); Ibu muda 72,0; Mahasiswi 67,0 (lemah: daya_beli, persaingan); Reseller 63,0 (lemah: persaingan, kemampuan_layani). Cek manual segmen 2: 360/100 x 20 = 72,0. Penguji menghitung ulang keempatnya: 410, 360, 335, 315 → 82,0 / 72,0 / 67,0 / 63,0 ✔.
Data rusak (nilai 6): `GAGAL: Baris 2 (A): 'ukuran' harus 1-5, ditemukan 6`, kode 2.
