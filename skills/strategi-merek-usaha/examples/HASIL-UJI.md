# HASIL UJI — strategi-merek-usaha v1.0.0

**Penguji:** agent independen (bukan pembuat), 2026-09-30. Hanya membaca folder skill + CLAUDE.md. Skill disalin ke scratchpad; tidak dipasang di `.claude/skills` repo. SKILL.md, scripts, dan catalog tidak diubah.

## Ringkasan
| Uji | File | Hasil |
|---|---|---|
| Normal 1 — nama kedai kopi Medan | `06-uji-nama-kedai-kopi-medan.md` | Lulus; skor script 10/10 cocok dengan hitungan penguji |
| Normal 2 — nama skincare lokal + klaim | `07-uji-nama-skincare-lokal.md` | Lulus; skor 10/10 cocok; klaim "100% aman/BPOM/7 hari" diganti versi jujur |
| Normal 3 — penawaran bengkel motor | `08-uji-penawaran-bengkel-motor.md` | Lulus; laba A Rp53.550 & B Rp31.040 cocok hitungan tangan |
| Input tidak lengkap | `09-uji-input-tidak-lengkap.md` | Lulus; 1 pesan, 5 pertanyaan, opsi cepat berasumsi |
| Luar cakupan (opini hukum + daftar merek resmi) | `10-uji-luar-cakupan-hukum-daftar-merek.md` | Lulus; tidak memberi opini hukum, tidak mengarang daftar |
| Uji A/B | `00-pembanding-tanpa-skill.md` | Dengan skill jelas lebih baik (tanpa skill menyarankan "Kopi Kenangan Medan" dan mengklaim "kemungkinan tersedia") |
| Banding pesaing (product-name + offers) | `00-banding-pesaing.md` | Skill kita 8,6 vs pesaing 4,1 |
| Uji regresi pembuat `tests/uji_regresi.py` | — | 17 tes OK |
| Data rusak `skor_nama.py` (18 kasus) | — | 16 ditolak/ditangani dengan pesan "GAGAL" jelas (kode 2); 2 lolos tak wajar (lihat R1, R3) |
| Data rusak `hitung_penawaran.py` (17 kasus) | — | NaN/inf/negatif/diskon 100/margin 100/format bonus salah ditolak; RUGI diberi peringatan; **titik ribuan lolos diam-diam** (S1) |
| `python3 scripts/validate.py --skill strategi-merek-usaha` | — | `✅ 1 skill valid, 113 baris katalog sesuai.` |
| `bash scripts/uji_openclaw.sh` (OpenClaw 2026.9.7) | — | strategi-merek-usaha eligible/modelVisible/commandVisible. Skrip keseluruhan keluar 1 karena **odoo-usaha** (skill lain) tidak eligible — di luar uji ini |

## Verifikasi faktual (web, 2026-09-30)
| Klaim di skill | Hasil | Sumber |
|---|---|---|
| UU 8/1999 berlaku 20 April 2000 | Benar (Pasal 65: berlaku 1 tahun sejak diundangkan 20 April 1999) | pasal.id/peraturan/uu/uu-no-8-tahun-1999; JDIH BPK peraturan.bpk.go.id/Details/45288 |
| Pasal 9 (promosi tidak benar/"seolah-olah", kata berlebihan "aman/tidak berbahaya", janji belum pasti) | Benar | idem |
| Pasal 10 (pernyataan menyesatkan harga, kegunaan, jaminan, potongan harga/hadiah) | Benar | idem |
| Pasal 11 (obral; contoh "menaikkan harga sebelum obral") | Benar (Pasal 11 huruf f) | idem |
| Pasal 12 (harga khusus waktu & jumlah tertentu yang tidak dimaksud dilaksanakan) | Benar | idem |
| Pasal 13 (hadiah yang tidak diberikan/tidak sesuai) | Benar | idem |
| Pasal 17 (iklan mengelabui) | **Kurang tepat:** Pasal 17 ayat (1) ditujukan kepada **pelaku usaha periklanan** (yang memproduksi iklan), bukan penjual pada umumnya | idem |
| Pasal 62 (sanksi) | Benar (pidana maks. 5 tahun/denda maks. Rp2 miliar untuk pelanggaran Pasal 8, 9, 10, 13 ayat 2, 15, 17 ayat 1, dst.) | idem |
| Kelas Nice 3, 25, 29, 30, 32, 35, 41, 43 | Benar semua | WIPO Nice class headings (nclpub.wipo.int), EUIPO explanatory notes |
| Kelas yang tidak ada di tabel | **Kelas 37** (reparasi kendaraan, binatu/laundry), **44** (salon/klinik kecantikan), **5** (produk berkhasiat obat) tidak tercantum — padahal contoh 03 (laundry) dan uji 08 (bengkel) membutuhkannya | idem |
| PDKI di pdki-indonesia.dgip.go.id, pencarian merek gratis, bisa filter kelas, hasil memuat status | Benar (situs membalas 403 untuk akses otomatis, tetapi dikonfirmasi sebagai situs resmi DJKI oleh banyak sumber) | pencarian web: golaw.id, digilaw.id, pdkilampung.com |

## Temuan
**Tinggi:** tidak ada.

**Sedang**
- **S1 — Angka dengan titik ribuan diterima diam-diam.** `--harga 38.000 --hpp 17.000` dibaca Rp38 & Rp17 -> "LABA per unit Rp21 (margin 55.3%)", kode 0. Bonus `"Tas=1.500"` dibaca Rp2. Orang Indonesia lazim menulis titik ribuan; agent bisa menyalin apa adanya dan menghasilkan hitungan salah tanpa peringatan. Saran: tolak/peringatkan pola `\d{1,3}(\.\d{3})+` atau harga < Rp100, dan sebut "tanpa titik ribuan" di SKILL.md B3.
- **S2 — Tabel kelas Nice kurang untuk UMKM jasa.** Kelas 37 (bengkel, laundry), 44 (salon/klinik kecantikan), 5 (jamu/produk berkhasiat obat) tidak ada; agent harus menebak (contoh 03 menyebut 37 tetapi referensi tidak).

**Rendah**
- R1 — Nama tanpa huruf (mis. "2.5") diterima, skor 54 dan "layak dicek".
- R2 — Ringkasan Pasal 17 tidak menyebut bahwa subjeknya pelaku usaha periklanan.
- R3 — Merek generik di daftar pembanding (mis. "Kopi") menandai semua nama yang memuat kata itu (aturan "memuat >= 4 huruf"). Perlu catatan agar pengguna tidak memasukkan kata umum.
- R4 — Suku kata Sunda "eu" dihitung dua ("Seulas" = 3; lazimnya 2).
- R5 — Tidak ada panduan biaya garansi untuk usaha jasa; `--refund` dipakai sebagai proksi.
- R6 — Keluaran teks margin memakai titik desimal ("41.8%"); label bonus panjang merusak perataan kolom; pesan galat `--bobot "khas=1,5"` membingungkan ("bobot '5' harus berbentuk kriteria=angka").
- R7 — Nama generik dengan `khas` = 1 ("Kulitku") tetap bisa masuk 5 besar (85/100); agent sebaiknya menyebutnya.

## Etika
- Kelangkaan palsu ditolak dan diganti versi jujur (contoh 05 pembuat, uji 07, uji 08: kuota berdasar kapasitas nyata). Larangan "senilai Rp..." tanpa pembanding, "100% garansi", testimoni karangan: tertulis dan diikuti.
- Tidak ada opini hukum (uji 10); tidak ada klaim ketersediaan nama/merek (semua "belum dicek").
- Pesan WA hanya ke kontak yang pernah berinteraksi + "balas STOP"; tidak ada blast.
- Klaim kosmetik/BPOM tidak dikarang; diarahkan ke cekbpom dan `[isi: ...]`.

## Skor kualitas: **8/10** — lulus (>= 7)
Alasan: alur jelas dan lengkap untuk awam, dua script dengan hitungan tepat (semua angka terverifikasi independen) dan validasi input yang umumnya kuat, etika dan batas hukum dijaga konsisten, nilai tambah besar dibanding sumber dan tanpa skill. Tidak 9 karena S1 (risiko hitungan salah akibat format angka Indonesia) dan S2 (referensi kelas Nice belum mencakup usaha jasa umum). Disarankan memperbaiki S1 dan S2 (serta R2) sebelum status naik; perbaikan kecil, tidak perlu uji ulang penuh selain uji regresi + satu skenario jasa.
