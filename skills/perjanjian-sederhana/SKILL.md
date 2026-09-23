---
name: perjanjian-sederhana
description: Menyusun draf surat perjanjian sederhana berbahasa Indonesia dengan struktur pasal standar (para pihak, ruang lingkup, hak & kewajiban, harga & pembayaran, jangka waktu, wanprestasi, keadaan memaksa, penyelesaian sengketa, tanda tangan & meterai Rp10.000) untuk reseller/distributor, supplier/pemasok, NDA/kerahasiaan, sewa tempat, sewa alat, kerja sama bagi hasil, dan jasa freelance, plus checklist sebelum tanda tangan. Gunakan saat pengguna minta surat perjanjian, kontrak, MoU (agreement, contract, NDA). Bukan untuk jual beli tanah, investasi, pihak asing, atau kontrak kerja karyawan.
---

# Perjanjian Sederhana

## Tujuan
Membantu pelaku usaha kecil dan profesional membuat draf perjanjian yang rapi, seimbang, dan mudah dipahami. Draf memakai struktur pasal yang lazim di Indonesia, angka dan terbilangnya dihitung script, pasal berisiko ditandai, dan disertai checklist sebelum tanda tangan. Ini draf, bukan nasihat hukum.

## Kapan digunakan
- "Buatkan surat perjanjian reseller / kerja sama supplier / NDA / sewa kios / sewa alat / bagi hasil / kontrak freelance."
- Pengguna punya kesepakatan lisan/chat dan ingin dituangkan jadi perjanjian tertulis.
- Pengguna ingin mengecek draf perjanjian buatannya (kelengkapan pasal, angka vs terbilang, meterai).

## Kapan TIDAK digunakan (tolak menyusun draf, rujuk ke profesional)
Rincian dan template jawaban penolakan ada di `references/batasan-rujukan.md`:
- Jual beli/hibah/balik nama **tanah, rumah, bangunan** (termasuk PPJB) → notaris/PPAT.
- **Investasi**, saham, pendirian PT/CV, imbal hasil tetap/pasti, menghimpun dana dari banyak orang → pengacara/notaris, cek aturan OJK.
- Pihak **asing**/valuta asing → pengacara (wajib dwibahasa, UU 24/2009 Ps. 31).
- Utang-piutang dengan **jaminan** (sertifikat, BPKB, fidusia), perjanjian **kerja karyawan**, waralaba/lisensi merek, kontrak **pemerintah/BUMN**, dan kasus yang **sudah bersengketa** → profesional terkait.
- Isi yang melanggar hukum → tolak.
- Surat non-perjanjian (surat kuasa, pernyataan, undangan) → skill `surat-resmi`. Penawaran harga → `surat-penawaran-harga`. Proposal kerja sama (belum mengikat) → `proposal-kerjasama`.

Saat menolak, tetap bantu: daftar dokumen yang perlu disiapkan, pertanyaan untuk dibawa ke notaris/pengacara, dan ringkasan kesepakatan (bukan perjanjian).

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Jenis perjanjian | Ya | — (tebak dari konteks, konfirmasi) |
| Identitas para pihak: nama, NIK, alamat (dan jabatan + nama badan usaha bila mewakili PT/CV) | Ya | Placeholder `[[...]]` untuk diisi tangan |
| Objek: produk/barang/tempat/alat/pekerjaan + rincian | Ya | — (tanyakan) |
| Harga, cara & jadwal bayar | Ya (kecuali NDA) | Sesuai default di template |
| Jangka waktu | Tidak | Default per template (mis. 12 bulan) |
| Kota penandatanganan & penyelesaian sengketa | Tidak | Musyawarah 30 hari → Pengadilan Negeri kota Pihak Pertama |
| Posisi pengguna (pihak mana) | Tidak | Peran PIHAK PERTAMA/KEDUA mengikuti template (mis. klien = PIHAK PERTAMA, freelancer = PIHAK KEDUA); sebutkan posisi pengguna di ringkasan |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan (maks 5 pertanyaan bernomor). Contoh untuk sewa kios:
1. Nama, NIK, dan alamat pemilik dan penyewa?
2. Alamat kios, luas, dan nomor sertifikatnya (atau dasar hak menyewakan)?
3. Harga sewa, lama sewa, dan dibayar sekaligus atau bertahap? Ada uang jaminan?
4. Siapa yang bayar listrik, air, dan iuran?
5. Kamu di posisi pemilik atau penyewa?
Jika pengguna ingin cepat, isi dengan default template, biarkan data pribadi sebagai `[[...]]`, dan cantumkan daftar asumsi.

## Langkah kerja
1. **Saring batasan** (daftar "Kapan TIDAK digunakan"). Nilai ≥ Rp500 juta atau jangka > 5 tahun: boleh dibuat, tetapi beri judul "DRAF BAHAN DISKUSI, WAJIB DITINJAU PENGACARA".
2. **Pilih template** di `templates/`: `reseller-distributor.md`, `supplier-pemasok.md`, `nda-kerahasiaan.md`, `sewa-tempat.md`, `sewa-alat.md`, `bagi-hasil.md`, `jasa-freelance.md`. Baca blok PANDUAN AGENT di atasnya (info wajib, default, peringatan). Kombinasi (mis. reseller + NDA) → gabungkan pasal dari `references/klausul-pilihan.md`.
3. **Hitung semua angka lewat script** (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/perjanjian.py tanggal 2026-09-23            # kalimat "Pada hari ini, Rabu, tanggal ..."
   python3 <folder-skill-ini>/scripts/perjanjian.py terbilang "Rp 7.500.000"      # Rp 7.500.000 (tujuh juta lima ratus ribu rupiah)
   python3 <folder-skill-ini>/scripts/perjanjian.py termin --total "Rp 7.500.000" --persen 50,50 --nama "Uang muka,Pelunasan"
   python3 <folder-skill-ini>/scripts/perjanjian.py bagihasil --persen 60,40 --pihak "Pemodal,Pengelola" --contoh "Rp 10.000.000"
   python3 <folder-skill-ini>/scripts/perjanjian.py denda --nilai "Rp 5.000.000" --persen-per-hari 0,1 --hari 30 --maks-persen 5
   python3 <folder-skill-ini>/scripts/perjanjian.py meterai --rangkap 2
   ```
   Pembulatan: ke rupiah terdekat (0,5 ke atas). Sisa pembulatan termin/bagi hasil masuk ke baris terakhir agar total tepat.
4. **Isi template.** Ganti setiap `[[...]]` dengan data pengguna. Data yang belum diketahui biarkan `[[...]]` agar terlihat. Hapus blok PANDUAN AGENT. Pertahankan tanda `> ⚠ TINJAU PENGACARA` pada pasal berisiko. Jangan menambah klaim (halal, BPOM, izin) yang tidak diberikan pengguna. Seimbangkan hak kedua pihak. Jangan membuat pasal yang hanya menguntungkan pengguna secara tidak wajar.
5. **Periksa draf:** simpan ke file lalu jalankan `python3 <folder-skill-ini>/scripts/perjanjian.py cek draf.md`. Perbaiki semua temuan "Harus diperbaiki" (angka vs terbilang, penomoran pasal, meterai, bagian standar). Temuan "Rujuk profesional" → kembali ke langkah 1.
6. **Sajikan** sesuai format output, lalu tawarkan versi .docx/PDF atau penyesuaian pasal.

### Fallback jika Python tidak bisa dijalankan
Beri tahu pengguna bahwa angka dihitung manual. Aturan: terbilang ditulis per kelompok tiga digit (triliun, miliar, juta, ribu); "seribu" dan "seratus" untuk angka 1; 11 = "sebelas", 12–19 = "... belas". Termin = total × persen, dibulatkan ke rupiah, termin terakhir = total − jumlah termin lain. Denda = nilai × persen/hari × hari, maksimal batas yang disepakati. Meterai = Rp10.000 × jumlah rangkap asli. Cek kelengkapan pasal dengan daftar di "Checklist" di bawah secara manual.

## Format output
```
**⚠ Draf ini bukan nasihat hukum.** [ringkas 1 kalimat + status: SIAP DITINJAU / PERLU DILENGKAPI]

--- (draf perjanjian lengkap: judul, nomor, pembuka tanggal, para pihak, latar belakang, Pasal 1..n, penutup, tabel tanda tangan + [Meterai Rp10.000], lampiran) ---

### Yang masih perlu dilengkapi
- [[...]] yang tersisa (dari hasil `cek`)

### Pasal yang sebaiknya ditinjau pengacara
- Pasal X: alasan singkat

### Syarat sah perjanjian (Pasal 1320 KUHPerdata)
Sepakat · Cakap · Hal tertentu · Sebab halal → 1 baris status masing-masing untuk draf ini

### Checklist sebelum tanda tangan (8–12 poin relevan, dari references/checklist-tanda-tangan.md)

### Catatan meterai
Surat perjanjian wajib bermeterai Rp10.000 berapa pun nilainya (UU 10/2020); 2 rangkap asli = 2 meterai. Meterai bukan syarat sah, tetapi diperlukan bila dokumen dipakai sebagai alat bukti.

_Disclaimer: Draf ini disusun otomatis berdasarkan informasi dari Anda, mengacu pada ketentuan yang berlaku per 23 September 2026. Ini bukan nasihat hukum dan tidak menggantikan pengacara/notaris. Untuk nilai besar atau kasus kompleks, mintalah peninjauan profesional._
```

## Contoh
**Input pengguna:** "Buatin kontrak freelance desain logo buat klien toko kue, harga 7,5 juta, DP 50%, revisi 2x, selesai 3 minggu. Aku desainernya."

**Output (dipotong):**
```
⚠ Draf ini bukan nasihat hukum. Status: PERLU DILENGKAPI (identitas & rekening).
# PERJANJIAN JASA DESAIN LOGO
...
## Pasal 3 — Biaya Jasa dan Pembayaran
(1) Biaya jasa untuk seluruh Pekerjaan adalah Rp 7.500.000 (tujuh juta lima ratus ribu rupiah).
(2) a. uang muka 50% sebesar Rp 3.750.000 (tiga juta tujuh ratus lima puluh ribu rupiah) ...
...
Pasal yang sebaiknya ditinjau pengacara: Pasal 6 (Hak atas Hasil Karya) bila logo akan didaftarkan sebagai merek.
```

**Di luar cakupan:** "Bikinin perjanjian jual beli tanah kavling 300 juta" → tolak menyusun draf, jelaskan perlunya akta PPAT, beri daftar dokumen (sertifikat, PBB, KTP/KK, surat nikah/persetujuan pasangan) dan pertanyaan untuk notaris.

## Checklist sebelum mengirim hasil
- [ ] Jenis perjanjian tidak termasuk daftar tolak; nilai besar diberi peringatan.
- [ ] Ada: judul & nomor, pembuka tanggal, identitas para pihak, latar belakang, ruang lingkup, hak & kewajiban, harga & pembayaran (kecuali NDA), jangka waktu, wanprestasi, keadaan memaksa, penyelesaian sengketa, lain-lain, tanda tangan + meterai.
- [ ] Semua nominal ditulis `Rp 1.250.000 (terbilang)` dari output script; `cek` tidak melaporkan ketidakcocokan.
- [ ] Pasal berisiko bertanda ⚠ dan dirangkum; daftar `[[...]]` tersisa disebutkan.
- [ ] Checklist sebelum tanda tangan, catatan meterai, dan disclaimer tercantum.
- [ ] Bahasa Indonesia baku tetapi mudah dipahami; tidak ada klaim/izin karangan.

## Batasan & penanganan error
- Script keluar dengan kode ≠ 0 dan pesan `GALAT: ...` (nominal tak terbaca, persen tidak 100%, file kosong/.docx, tanggal salah). Perbaiki input sesuai pesan.
- `cek` hanya pemeriksa bantu (pola teks), bukan penilaian hukum.
- Dasar hukum & tanggal berlaku: `references/regulasi.md`. Aturan bisa berubah; sarankan cek peraturan.bpk.go.id atau konsultasi.
- Data pribadi (NIK, alamat) hanya dipakai untuk draf. Jangan disimpan atau dikirim ke tempat lain.
