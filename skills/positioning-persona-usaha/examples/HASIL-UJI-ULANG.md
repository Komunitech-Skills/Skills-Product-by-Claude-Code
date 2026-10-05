# Hasil Uji Ulang: positioning-persona-usaha v1.0.1

- Penguji: agent independen kedua (bukan pembuat, bukan penguji pertama). Hanya membaca folder skill + CLAUDE.md. Tanggal: 2026-09-29.
- Platform: `claude-code (simulasi agent)`. Belum diuji di OpenClaw/Codex/Cursor asli.
- `python3 scripts/validate.py --skill positioning-persona-usaha` → ✅ "1 skill valid". `python3 scripts/uji_skor_segmen.py` → "Semua uji lulus".
- Skor diverifikasi penguji dengan hitungan sendiri (jumlah bobot x nilai ÷ 5, pecahan eksak), bukan kode skill.

## 1. Verifikasi perbaikan

| Butir | Cek penguji | Hasil |
|---|---|---|
| B1 koma tanpa kutip | `Ibu muda, pengajian,3,3,4,4,5,3,4` → `GAGAL: Baris 2: jumlah kolom lebih banyak dari judul. Nama segmen yang berisi koma harus diberi tanda kutip "..." atau ganti komanya dengan '/'`, exit 2, **tanpa traceback**. Versi berkutip diterima, nama utuh "Ibu muda, pengajian" 74,0 (independen 370/5 = 74 ✅). | ✅ |
| B2 inf/nan | `--bobot ukuran=inf / nan / -inf / 1e999` → semua `GAGAL: Bobot 'ukuran' harus angka biasa`, exit 2. Bonus: sel CSV `nan`/`inf` juga ditolak ("harus 1-5"). | ✅ |
| B3 judul ganda | dua `ukuran` → `GAGAL: Judul kolom ganda: ukuran`; varian beda huruf/spasi (`Ukuran`, `ukuran `) juga tertangkap. | ✅ |
| B4 desimal bobot | `ukuran=1,5` → GAGAL dengan petunjuk "Desimal pakai titik: ukuran=1.5"; `ukuran=1.5` jalan. Terdokumentasi di SKILL Langkah 3. | ✅ |
| B5 nama terpotong | Nama 40 karakter ("Karyawan perantau & anak kos yang kerja") tampil utuh; kolom melebar. | ✅ |
| B6 tab | CSV bertab terbaca benar (skor 78,0 cocok). | ✅ |
| 6 Aturan seri | Selisih 1 poin (79 vs 78) dan 4 poin (78 vs 74) → baris "SETARA ..." di tabel dan kunci `seri` di JSON; selisih 7 poin (81 vs 74) → tidak ada SETARA. SKILL Langkah 3 memberi urutan dasar pilihan (FAKTA pembeli → termurah diuji → termudah dilayani) dan wajib menulis dasarnya. | ✅ |
| 7 Dasar hukum | Diverifikasi terhadap teks resmi (lihat bagian 2). | ✅ dengan catatan kecil |
| 8 Mode chat | Aturan ada di Format output (Ringkasan 5 baris + teks siap tempel, maks. ±25 baris, tawaran "Balas: lengkap"). Diuji di R1: 19 baris. | ✅ |
| 9 Tema ulasan ≠ pelanggan | Ada di Langkah 1. | ✅ |
| 10 Hitung karakter | `--hitung` benar: 127 code point / 128 UTF-16 untuk bio berisi 🍱 (independen: `len` 127, UTF-16 128 ✅); 122 untuk bio tanpa emoji ✅. | ✅ |
| 11 Nama contoh fiktif | `examples/contoh-fiktif-toko-hijab.md` ada; tidak ada rujukan tersisa ke `01-toko-hijab...` selain di HASIL-UJI.md (rekaman). | ✅ |

## 2. Verifikasi UU No. 8 Tahun 1999 (teks resmi)
Sumber: teks lengkap JDIH Kemenkeu (https://jdih.kemenkeu.go.id/api/download/fulltext/1999/8TAHUN~1999UU.htm), dan halaman peraturan.go.id (https://peraturan.go.id/id/uu-no-8-tahun-1999) ditemukan lewat pencarian web. Diakses 2026-09-29.

| Ringkasan di SKILL | Teks resmi | Status |
|---|---|---|
| Berlaku 20 April 2000 | Diundangkan 20 April 1999 (LN 1999 No. 42); Pasal 65: "mulai berlaku setelah 1 (satu) tahun sejak diundangkan" → 20 April 2000 | ✅ |
| Pasal 9: melarang menawarkan/mempromosikan/mengiklankan secara tidak benar atau seolah-olah memenuhi standar mutu, mendapat persetujuan/sponsor, kata berlebihan "aman", "tanpa efek samping" tanpa keterangan lengkap, merendahkan barang/jasa lain | Pasal 9 ayat (1): "menawarkan, memproduksikan, mengiklankan ... secara tidak benar, dan/atau seolah-olah" huruf a (standar mutu), c (sponsor, persetujuan), i (merendahkan barang/jasa lain), j (kata berlebihan "aman, tidak berbahaya, tidak mengandung risiko atau efek sampingan tanpa keterangan yang lengkap") | ✅ akurat |
| Pasal 17: iklan yang mengelabui soal kualitas, kuantitas, bahan, kegunaan, harga, atau jaminan; informasi keliru/salah/tidak tepat; memakai orang tanpa izin | Pasal 17 ayat (1) huruf a (kualitas, kuantitas, bahan, kegunaan, harga, ketepatan waktu), b (jaminan/garansi), c (informasi keliru, salah, tidak tepat), e (mengeksploitasi kejadian/seseorang tanpa izin) | ✅ isi akurat; catatan: subjek Pasal 17 adalah **"pelaku usaha periklanan"** |
| Pasal 62: pelanggaran dapat dipidana | Pasal 62 ayat (1): pelanggaran Pasal 9 dan Pasal 17 ayat (1) huruf a, b, c, e → penjara maks. 5 tahun atau denda maks. Rp2 miliar; ayat (2): Pasal 17 ayat (1) huruf d, f → maks. 2 tahun / Rp500 juta | ✅ benar (tanpa rincian ancaman) |

Catatan (tidak memblokir): (a) Pasal 17 ditujukan ke pelaku usaha periklanan; untuk UMKM yang membuat iklan sendiri, dasar yang paling langsung adalah Pasal 9 (dan Pasal 10 tentang pernyataan tidak benar soal harga, kegunaan, jaminan, potongan harga). Ringkasan sebaiknya menyebut ini agar tidak terkesan Pasal 17 langsung mengikat penjual. (b) Boleh tambahkan ancaman maksimal Pasal 62 ayat (1) agar lebih konkret. Perlu review hukum tidak diwajibkan: ringkasan tidak keliru, dan skill sudah menyebut "bukan kutipan resmi" + tempat cek.

## 3. Skenario uji ulang

### R1 — Normal (baru), mode chat: laundry kiloan, Makassar, via Telegram/OpenClaw
**Pengguna (Telegram):** "Aku buka laundry kiloan antar-jemput di Tamalanrea Makassar, Rp8 ribu/kg, min 4 kg jemput gratis, selesai 2 hari. Pelanggan sekarang campur mahasiswa sama karyawan. Tolong bikin target & positioning, cepat aja ya."

Script (nilai 1-5 dengan alasan singkat oleh agent):
```
$ python3 scripts/skor_segmen.py laundry.csv
#  Segmen                                     Skor  Saran
1  Karyawan muda lajang (kos/kontrakan)       81.0  Utama (layani duluan)
2  Mahasiswa kos sekitar kampus Tamalanrea    74.0  Kandidat (uji kecil dulu)  [lemah: daya_beli, persaingan]
3  Keluarga, ibu bekerja                      71.0  Kandidat (uji kecil dulu)
4  Pemilik kos & homestay (langganan sprei)   62.0  Kandidat (uji kecil dulu)  [lemah: ukuran, kemampuan_layani]
```
Independen: 405/5 = 81, 370/5 = 74, 355/5 = 71, 310/5 = 62 ✅. Selisih 7 poin → tidak SETARA (benar). Nama berkoma dikutip di CSV dan tampil utuh.

Jawaban agent (mode chat, 19 baris, tanpa tabel):
> **Ringkasan**
> 1. Fokus 90 hari: **karyawan muda lajang yang ngekos/kontrak** (skor 81/100). Mahasiswa (74) = uji berikutnya.
> 2. Persona (fiktif): Rian, 25, staf kantor, ngekos di Tamalanrea, pulang malam, tak sempat nyuci.
> 3. Positioning: laundry kiloan antar-jemput yang dilipat rapi dan selesai sesuai janji, untuk yang pulang kerja sudah capek.
> 4. Tagline: **"Pulang kerja, baju sudah beres."**
> 5. Langkah pertama: tanya 5 pelanggan karyawan lewat WA kenapa pilih kamu; uji 2 tagline di status 3 hari.
>
> **Siap tempel**
> Bio (122 karakter, dihitung): Laundry kiloan antar-jemput Tamalanrea. Rapi dilipat, wangi, selesai 2 hari. Jemput gratis min. 4 kg. Chat WA: [isi nomor]
> Judul listing/WA katalog: Laundry Kiloan Antar-Jemput Tamalanrea – Rp8.000/kg, Selesai 2 Hari
> Sapaan WA: "Halo Kak, terima kasih sudah chat. Mau dijemput hari ini? Kirim alamat & jam yang pas ya, minimal 4 kg gratis jemput."
>
> Asumsi: skor 1-5 perkiraan saya dari cerita Kakak; "selesai 2 hari" harus benar-benar bisa ditepati. Hindari "paling bersih/termurah" (tak bisa dibuktikan).
> Mau versi lengkap (segmen & skor, persona, pembeda, message house, uji 7 hari)? Balas: **lengkap**.

**Vonis: LULUS.** Mode chat dipatuhi (≤ 25 baris, teks tempel di depan, tawaran versi lengkap), skor lewat script, bio dihitung script, klaim dijaga.

### R2 — Data rusak
Semua ditolak dengan pesan "GAGAL: ..." dan exit 2, **tanpa satu pun traceback**: koma tanpa kutip, judul ganda (2 varian), sel `nan`/`inf`, baris kurang kolom, file biner non-UTF-8, file kosong, file tidak ada, tanpa argumen, bobot `inf/nan/-inf/1e999/-1/1,5/foo=3/semua 0`.
**Vonis: LULUS** (bug B1 penguji pertama tuntas).

### R3 — Regresi skenario 1 penguji pertama (katering Rantang Bu Wulan, Semarang)
CSV dua segmen teratas dari `01-uji-katering-rantang-semarang.md` dijalankan ulang:
```
1  Karyawan perantau & anak kos yang kerja   79.0  Utama (layani duluan)  [lemah: persaingan]
2  Keluarga muda suami-istri bekerja         78.0  Utama (layani duluan)
SETARA: '...' dan '...' hanya selisih 1 poin (<= 5). Skor tidak cukup untuk memilih; ...
```
Skor sama dengan v1.0.0 (79,0 / 78,0; independen 395/5, 390/5 ✅). Nama kini utuh (dulu terpotong "...anak kos kerj"). Kasus seri yang dulu tanpa aturan kini ditandai SETARA, dan keputusan di contoh 01 (pilih segmen yang sudah terbukti membeli) sesuai urutan dasar yang sekarang tertulis di SKILL.
**Vonis: LULUS (tanpa regresi, lebih baik).**

## 4. Temuan baru (tidak memblokir)
| ID | Tingkat | Temuan |
|---|---|---|
| N1 | Kecil | Ringkasan Pasal 17 tidak menyebut subjeknya "pelaku usaha periklanan"; Pasal 10 (yang langsung mengikat penjual soal harga/kegunaan/jaminan) tidak disebut. Isi tidak salah. |
| N2 | Sangat kecil | Saat SETARA, kolom "Saran" bisa tetap "Utama" untuk keduanya (79/78) atau "Utama" vs "Kandidat" (78/74). Tidak salah karena baris SETARA menjelaskan, tapi agent harus membaca baris itu. |
| N3 | Sangat kecil | SKILL.md 125 baris (naik dari 117), masih jauh di bawah 300. |

## 5. Skor
**9/10 — LULUS.** Naik dari 8/10.
- (+) Crash B1 tuntas; semua bug kecil B2-B6 tuntas dengan tes; aturan seri jelas di script & SKILL; mode chat praktis untuk OpenClaw/Telegram; alat hitung karakter bio akurat (termasuk UTF-16 emoji).
- (+) Dasar hukum UU 8/1999 kini lengkap dan ringkasan Pasal 9/17/62 cocok dengan teks resmi.
- (−) Nuansa subjek Pasal 17 (N1); butir 12 opsional (file konteks lintas skill) belum dikerjakan.
- Rekomendasi: siap untuk uji platform asli / `beta`. N1 bisa dirapikan kapan saja tanpa uji ulang.
