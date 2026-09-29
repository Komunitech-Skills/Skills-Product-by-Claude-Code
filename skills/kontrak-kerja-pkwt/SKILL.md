---
name: kontrak-kerja-pkwt
description: Menyusun draf kontrak kerja PKWT (Perjanjian Kerja Waktu Tertentu / karyawan kontrak) siap cetak, memeriksa draf PKWT yang ada dengan checklist berisiko (masa percobaan, pekerjaan tetap, lebih dari 5 tahun, upah di bawah UMK, tanpa BPJS, penalti berlebihan), serta menghitung uang kompensasi akhir PKWT dan ganti rugi pengakhiran dini lewat script. Dasar UU 13/2003 jo. UU 6/2023, PP 35/2021, Putusan MK 168/PUU-XXI/2023. Gunakan saat pengguna minta "buat kontrak kerja karyawan", "PKWT", "kontrak kerja harian lepas", "cek kontrak karyawan", "kompensasi habis kontrak", "karyawan kontrak diputus sebelum waktunya", atau fixed-term employment contract, employment agreement Indonesia, contract worker severance. Bukan untuk perjanjian bisnis umum (pakai perjanjian-sederhana) atau PHK karyawan tetap.
---

# Kontrak Kerja PKWT (Karyawan Kontrak)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Membantu pemilik usaha dan HR membuat kontrak karyawan kontrak yang **sesuai aturan**, **menemukan klausul berbahaya** di draf yang sudah ada, dan **menghitung uang kompensasi akhir kontrak** serta **ganti rugi** bila kontrak diputus lebih cepat, dengan angka yang dihitung script (bukan dikira-kira).

## Kapan digunakan
- "Buatkan kontrak kerja 1 tahun untuk barista baru." / "Bikin PKWT tukang proyek 6 bulan."
- "Tolong cek kontrak karyawan ini, aman nggak?" (pengguna menempel/melampirkan draf)
- "Kontrak habis bulan depan, kompensasinya berapa?" / "Karyawan kontrak mau saya berhentikan bulan ini, harus bayar apa?"
- "Kontrak sudah diperpanjang 3 kali, masih boleh?"

## Kapan TIDAK digunakan
- Perjanjian bisnis (reseller, sewa, freelance, NDA) → `perjanjian-sederhana`. Freelance yang pada praktiknya penuh perintah, jam kerja tetap, dan upah rutin → jelaskan bahwa itu cenderung hubungan kerja, lalu tawarkan PKWT.
- **Karyawan tetap (PKWTT)**, PHK/pesangon karyawan tetap, perjanjian bersama PHK → di luar cakupan; arahkan ke Disnaker/konsultan hukum. Boleh jelaskan singkat bedanya.
- Tenaga kerja asing (TKA), outsourcing/alih daya, PKB serikat pekerja, magang → arahkan ke konsultan.
- Surat peringatan → `surat-peringatan-karyawan`. THR → `hitung-thr`. Slip gaji & iuran BPJS → `slip-gaji-bpjs`. Lowongan → `lowongan-kerja`.

## Tiga mode
| Mode | Pemicu | Hasil |
|---|---|---|
| **Susun** | "buat/bikin kontrak kerja/PKWT" | Draf PKWT lengkap siap cetak + catatan pengisian + checklist tanda tangan |
| **Periksa** | pengguna memberi draf | Tabel temuan berisiko (🔴/🟠/🟢) + usulan perbaikan siap tempel |
| **Hitung** | "kompensasi", "ganti rugi", "sisa kontrak", "sudah berapa tahun" | Rincian kompensasi per periode, cek batas 5 tahun, ganti rugi Pasal 62 |

Satu permintaan bisa memakai beberapa mode (mis. Susun selalu menyertakan perkiraan kompensasi dari mode Hitung).

## Input (mode Susun)
Tanyakan **sekali** dalam satu pesan bernomor, maksimal 8 butir, contoh:
```
Supaya kontraknya tepat, mohon isi yang Anda tahu (yang kosong akan saya beri tanda [isi: ...]):
1. Nama usaha, jenis usaha, alamat, dan nama + jabatan penanda tangan. Apakah usaha Anda **usaha mikro/kecil**? (mis. warung, kedai, bengkel kecil; bila ragu, sebutkan omzet setahun kira-kira)
2. Nama pekerja (NIK/alamat boleh diisi sendiri nanti)
3. Jabatan & tugas utamanya
4. Kenapa pekerjaan ini kontrak, bukan tetap? (proyek, musiman, produk baru, pengganti sementara, dll.)
5. Tanggal mulai & lama kontrak (atau "sampai proyek X selesai"); apakah ini perpanjangan? sejak kapan kontrak pertama?
6. Gaji pokok + tunjangan tetap per bulan (atau upah harian), tanggal gajian
7. Hari & jam kerja
8. Kota/kabupaten tempat kerja dan UMK-nya tahun ini (bila tahu)
```
Jika pengguna ingin cepat ("langsung buatin aja"), buat dengan data yang ada, isi sisanya `[isi: ...]`, dan sebutkan asumsinya. **Jangan pernah mengarang** nama, NIK, alamat, nomor BPJS, tanggal, atau angka UMK.

- **Beberapa pekerja sekaligus:** PKWT dibuat **per orang**. Buat satu draf (bagian yang sama untuk semua) + tabel identitas per pekerja (nama, jabatan, upah, tanggal mulai). Jalankan script **satu kali per pekerja** bila upah/tanggalnya berbeda (sekali saja bila semuanya sama), lalu tampilkan tabel per orang dan total = jumlah per orang.
- **Usaha mikro/kecil (UMK):** menurut PP 35/2021 Pasal 16 ayat (6), **besaran** uang kompensasi bagi pekerja di usaha mikro dan usaha kecil diberikan **berdasarkan kesepakatan** pengusaha dan pekerja; rumus umum (n ÷ 12 × upah) tidak wajib bagi mereka. Bila pengguna UMK (atau belum menjawab tetapi jelas usaha kecil), tetap jalankan script dengan `--usaha-mikro-kecil`: rumus umum ditampilkan sebagai **acuan praktik baik** (bukan batas bawah wajib; besaran kesepakatan di bawah acuan sah bila tertulis jelas, sejalan dengan checklist B4a), dan kontrak memakai klausul kompensasi versi kesepakatan (lihat template Pasal 7 ayat (2)). Jangan menyebut rumus umum sebagai kewajiban bagi UMK, dan jangan menyimpulkan kompensasi boleh Rp0. Status usaha mikro/kecil tidak dinilai skill: bila ragu, sarankan cek ke Dinas Koperasi & UKM/Disnaker. Tanpa jawaban, pakai rumus umum dan sebutkan asumsinya ("dianggap bukan usaha mikro/kecil").
- **Tanggal mulai belum diketahui:** tanyakan dulu. Bila pengguna tetap ingin draf sekarang, tulis `[isi: tanggal mulai]` / `[isi: tanggal akhir]`, jangan mengarang tanggal. Script butuh tanggal, jadi hitung kompensasi dengan rumus (12 bulan = 1 × upah; n bulan = n ÷ 12 × upah) dan beri label "dihitung manual, tanggal belum diisi". Batas 5 tahun ditulis sebagai "5 tahun sejak tanggal mulai kontrak pertama".

## Langkah kerja — mode Susun
1. **Uji kelayakan PKWT dulu** (pertanyaan no. 4). Jika pekerjaannya jelas **bersifat tetap** (mis. kasir tetap toko, admin tetap, koki tetap) dan tidak ada alasan waktu tertentu: jelaskan dengan sopan bahwa PKWT untuk pekerjaan tetap berisiko **demi hukum menjadi karyawan tetap (PKWTT)**. Tawarkan: (a) tetap membuat PKWT bila memang ada alasan sementara yang jujur, dengan alasan itu ditulis di Pasal 1 ayat (3); atau (b) memakai PKWTT dengan masa percobaan maks. 3 bulan (di luar cakupan template ini; arahkan ke konsultan).
2. **Tentukan varian jangka waktu** di `templates/kerangka-pkwt.md`: A (jangka waktu), B (selesainya pekerjaan), atau C (harian lepas, < 21 hari/bulan).
3. **Hitung dengan script** (lihat bagian Hitung): total jangka waktu termasuk kontrak sebelumnya (≤ 5 tahun), tanggal akhir, dan perkiraan kompensasi. Jika melebihi 5 tahun → hentikan penyusunan PKWT baru, jelaskan risikonya, sarankan PKWTT.
4. **Cek upah**: bandingkan dengan UMK yang diisi pengguna. Jika pengguna tidak tahu UMK: tulis `[isi: UMK {kota} {tahun} — cek situs Disnaker]` dan ingatkan. Jika di bawah UMK → tandai 🔴 (untuk usaha mikro/kecil, jelaskan ada pengecualian: upah berdasarkan kesepakatan dengan batas bawah, PP 36/2021 Pasal 36, dan sarankan cek Disnaker).
5. **Cek jam kerja** (PP 35/2021 Pasal 21): 6 hari kerja = 7 jam/hari dan 40 jam/minggu (mis. 5 × 7 jam + 1 × 5 jam), 5 hari kerja = 8 jam/hari dan 40 jam/minggu. Bila jam yang diminta lebih dari 40 jam/minggu, koreksi atau tulis kelebihannya sebagai lembur berbayar (maks. 18 jam/minggu).
6. **Isi template** pasal demi pasal. Angka rupiah selalu dengan terbilang. **Tidak ada masa percobaan**, denda, atau penahanan dokumen.
7. Tambahkan **Catatan pengisian** (daftar `[isi: ...]` yang tersisa), **Checklist tanda tangan**, dan **disclaimer** (lihat Format Output).

## Langkah kerja — mode Periksa
1. Baca seluruh draf. Jika draf tidak ditempel/dilampirkan, minta sekali.
2. Periksa terhadap `references/checklist-periksa.md` bagian A–D. Temuan utama yang selalu dicek:
   - 🔴 masa percobaan di PKWT (batal demi hukum, masa kerja tetap dihitung)
   - 🔴 pekerjaan bersifat tetap dikontrak PKWT → risiko menjadi PKWTT
   - 🔴 total jangka waktu > 5 tahun termasuk perpanjangan (hitung dengan script)
   - 🔴 hanya berbahasa asing / tidak tertulis
   - 🔴 upah di bawah UMK (angka UMK dari pengguna; jangan dikarang)
   - 🔴 tanpa BPJS Ketenagakerjaan & Kesehatan, atau iuran perusahaan dibebankan ke pekerja
   - 🔴 tanpa uang kompensasi / "hangus bila resign"; THR dikecualikan (mis. "THR hanya untuk karyawan tetap"). THR yang sekadar tidak disebut → 🟠 (checklist B5)
   - 🔴 penalti berlebihan ke pekerja (denda berkali-kali gaji, gaji terakhir hangus, penahanan ijazah)
   - 🔴 pengusaha boleh memutus kapan saja tanpa ganti rugi
   - Usaha mikro/kecil: kompensasi dengan **besaran kesepakatan** yang tertulis jelas (di bawah rumus umum) **bukan** pelanggaran (PP 35/2021 Pasal 16 ayat (6)) → paling tinggi 🟢 dengan saran menyebut dasar kesepakatan; bila kompensasi dihapus sama sekali tetap 🔴 (checklist B4). Bila status usaha tidak diketahui, tanyakan dalam satu pesan bersama pertanyaan lain.
   - 🟠 isi minimal tidak lengkap, tidak dicatatkan, lembur/jam kerja/cuti tidak sesuai, upah pokok < 75%
3. Untuk tiap temuan: kutip kalimat asli, beri risiko, dasar aturan, dan **usulan kalimat pengganti siap tempel**.
4. Sebutkan juga yang **sudah baik**, lalu kesimpulan: Aman ditandatangani / Perbaiki dulu / Konsultasikan dulu (bila ada ≥1 🔴 yang tidak bisa diperbaiki dengan menulis ulang klausul, mis. pekerjaan tetap atau > 5 tahun).
5. Jika pengguna mau, susun ulang draf yang sudah diperbaiki memakai mode Susun.

## Langkah kerja — mode Hitung
Jalankan script (path relatif terhadap folder SKILL.md ini; Windows: ganti `python3` dengan `python` atau `py`):
```bash
python3 <folder-skill-ini>/scripts/hitung_pkwt.py --periode "1 Januari 2026 s.d. 31 Desember 2026" --gaji-pokok 5jt --tunjangan-tetap 500rb
```
- Perpanjangan/kontrak berturut-turut: ulangi `--periode` untuk setiap kontrak (urut dari yang pertama).
- Diputus sebelum waktunya: tambah `--berhenti "<hari kerja terakhir>" --pihak-mengakhiri pengusaha|pekerja`.
- Opsi: `--upah` (bila upah tidak dipisah, atau rata-rata upah harian lepas per bulan) · `--upah-minimum <UMK>` · `--harian` · `--usaha-mikro-kecil` · `--format json`. (Opsi lama `--metode bulan-penuh` dihapus sejak v1.0.2: membuang sisa hari membuat masa dijalani + sisa kontrak ≠ panjang kontrak. Hanya ada satu metode, lihat Rumus no. 2.)
- Format tanggal yang diterima: `2026-01-01`, `01/01/2026` (hari/bulan/tahun), `1 Januari 2026`, `1 Jan 2026`. Upah: `Rp5.000.000`, `Rp 5.000.000,-`, `Rp5.000.000,00`, `5jt`, `5,5 juta`, `500rb`.
- Bila muncul **PERIKSA UPAH** (upah bulanan < Rp500.000, mis. "4.500" terbaca Rp4.500 atau "4,5" terbaca Rp5): tanyakan ke pengguna apakah maksudnya Rp4.500.000, lalu jalankan ulang. Jangan diam-diam memakai angka kecil itu.
- Bila muncul **PERLU REVIEW (kompensasi Rp0 pada periode pendek)**: sampaikan kedua tafsir (a) dan (b) beserta angkanya apa adanya, jangan memilih salah satunya; sarankan konfirmasi ke Disnaker/konsultan.
- **Usaha mikro/kecil:** tanyakan (sekali, bersama pertanyaan lain) bila belum jelas. Dengan `--usaha-mikro-kecil`, angka rupiah tidak berubah, tetapi label menjadi **ACUAN KOMPENSASI** (kolom tabel "Kompensasi (acuan)") dan muncul catatan PP 35/2021 Pasal 16 ayat (6): besaran sesuai kesepakatan. Sampaikan ke pengguna: angka itu acuan praktik baik, bukan jumlah wajib; yang dibayar adalah besaran yang disepakati dan ditulis di kontrak. Ganti rugi Pasal 62 tidak terpengaruh.
- Salin tabel & peringatan dari output apa adanya. Jika script error, baca pesannya (mis. tanggal tertukar, tanggal tidak ada), perbaiki input, jalankan ulang.

## Rumus (untuk hitung manual bila Python tidak bisa dijalankan)
1. **Upah 1 bulan** = gaji pokok + tunjangan tetap (bukan uang makan/transport harian yang tergantung kehadiran). Bila upah = upah pokok + tunjangan **tidak** tetap → upah pokok saja (PP 35/2021 Pasal 16 ayat (4)). Harian lepas: rata-rata upah per bulan (asumsi skill). Upah satuan hasil: naskah tidak mengatur rinci (aturan "rata-rata 12 bulan terakhir" di Pasal 33 ayat (2) hanya untuk upah lembur) → pakai rata-rata upah per bulan sebagai asumsi dan tandai PERLU REVIEW.
2. **Masa kerja** (asumsi skill, aturan tidak merinci): tanggal mulai dan akhir **ikut dihitung**. Hitung **bulan penuh** dengan tanggal ulang bulanan (1 Jan → 1 Feb = 1 bulan; bila tanggal tidak ada, pakai akhir bulan), lalu **sisa hari**. Bulan desimal = bulan penuh + sisa hari ÷ jumlah hari "bulan berjalan" (dari tanggal ulang terakhir ke tanggal ulang berikutnya).
   Contoh: 1 Januari–15 Maret 2026 = 2 bulan 15 hari = 2 + 15/31 = 2,4839 bulan.
3. **Kompensasi** (PP 35/2021 Pasal 15–16): diberikan bila masa kerja **paling sedikit 1 bulan secara terus-menerus**; < 1 bulan → tidak berhak (bila beberapa periode pendek berurutan tanpa jeda, lihat peringatan PERLU REVIEW di atas). 12 bulan → 1 × upah. Selain itu → **masa kerja (bulan) ÷ 12 × upah 1 bulan**. Dihitung **per periode kontrak** (kontrak awal dan tiap perpanjangan dibayar saat periodenya selesai). **Usaha mikro/kecil:** besaran sesuai kesepakatan (Pasal 16 ayat (6)); angka rumus ini hanya acuan.
4. **Diputus lebih cepat**: kompensasi dihitung dari masa yang sudah dijalani (PP 35/2021 Pasal 17), **ditambah** ganti rugi Pasal 62 UU 13/2003 = **sisa masa kontrak (bulan) × upah 1 bulan**, dibayar oleh pihak yang mengakhiri kepada pihak lain. **Sisa (bulan) = panjang periode berjalan (bulan) − masa yang sudah dijalani di periode itu (bulan)**, keduanya dihitung dengan cara no. 2, sehingga dijalani + sisa = panjang kontrak persis. Contoh: kontrak 1 Jan–31 Mar 2026 (3 bulan), berhenti 15 Feb → dijalani 1 + 15/28 = 1,5357; sisa 3 − 1,5357 = 1,4643 bulan. Jangan menghitung sisa dari tanggal sisa ("16 Feb–31 Mar = 1 bulan 16 hari" = 1,5161, angka lain); jumlah hari kalender sisa hanya informasi. Bila berhenti tepat di hari terakhir periode berjalan, sisa = 0 (tidak ada ganti rugi di periode itu). Tidak berlaku bila berakhir karena pekerja meninggal, putusan pengadilan, atau pekerjaan (varian B) sudah selesai.
5. **Batas 5 tahun**: tanggal akhir terakhir ≤ (tanggal mulai kontrak pertama + 60 bulan − 1 hari).
6. **Pembulatan**: hasil akhir dibulatkan ke rupiah terdekat (setengah ke atas).
Tulis langkahnya dan beri label "dihitung manual".

## Format output
**Mode Susun:**
```
[DRAF PKWT lengkap dari templates/kerangka-pkwt.md, sudah terisi]

---
CATATAN PENGISIAN (jangan dicetak)
- Masih kosong: [daftar [isi: ...]]
- Asumsi: [mis. varian A, 6 hari kerja]
- Hitungan script: total PKWT ..., batas 5 tahun s.d. ..., perkiraan kompensasi Rp... (rumus; bila usaha mikro/kecil: "acuan, besaran sesuai kesepakatan")
- Peringatan: [dari script & pengecekan upah/jenis pekerjaan]

CHECKLIST SEBELUM TANDA TANGAN
[ ] Pekerja membaca seluruh isi & diberi waktu bertanya   [ ] Semua [isi: ...] sudah terisi
[ ] Upah ≥ UMK [kota] [tahun] (dicek di situs Disnaker)     [ ] Paraf tiap halaman, 2 rangkap asli, meterai Rp10.000
[ ] Daftarkan BPJS TK & Kesehatan                            [ ] Catatkan PKWT daring maks. 3 hari kerja
[ ] Simpan salinan KTP/NIK secara terbatas (data pribadi)

DISCLAIMER (teks baku di references/dasar-hukum.md bagian 6)
```
**Mode Periksa:** pakai format laporan di `references/checklist-periksa.md`.
**Mode Hitung:** tabel dari script + penjelasan 2–4 kalimat bahasa awam (siapa bayar siapa, kapan dibayar) + disclaimer.

## Contoh
**Input:** "Bikinin kontrak kerja buat Dimas, barista kedai kopi saya di Bandung, 1 tahun mulai 1 Oktober 2026, gaji 3,8 juta + tunjangan transport tetap 300 ribu. Tiga bulan pertama masa percobaan ya."

**Output (ringkas):**
- Sampaikan dulu: *"Masa percobaan tidak boleh ada di kontrak PKWT. Kalau tetap ditulis, masa percobaan itu batal demi hukum dan masa kerja Dimas tetap dihitung sejak 1 Oktober. Jadi saya tidak memasukkannya. Kalau ingin menilai Dimas dulu, pilihannya adalah mengangkatnya sebagai karyawan tetap dengan masa percobaan maksimal 3 bulan."*
- Tanya satu hal kritis (alasan kontrak): barista di kedai yang buka setiap hari umumnya pekerjaan tetap. Jika pengguna menjawab "cabang baru masih uji coba 1 tahun", tulis alasan itu di Pasal 1 ayat (3) dan tandai sebagai risiko 🟠 untuk dikonsultasikan.
- Script: `--periode "1 Oktober 2026 s.d. 30 September 2027" --gaji-pokok 3,8jt --tunjangan-tetap 300rb` menghasilkan 12 bulan, kompensasi **Rp4.100.000**, dengan batas 5 tahun s.d. 30 September 2031.
- Draf 12 pasal: upah Rp4.100.000 (empat juta seratus ribu rupiah), UMK Kota Bandung 2026 ditulis `[isi: cek situs Disnaker]`, BPJS, THR, cuti 12 hari setelah 12 bulan, kompensasi, ganti rugi Pasal 62 dua arah. Diakhiri catatan pengisian, checklist, dan disclaimer.

## Batasan & penanganan error
- **Status hukum berubah:** Putusan MK 168/PUU-XXI/2023 memerintahkan UU Ketenagakerjaan baru paling lambat ±31 Oktober 2026. Per 26 September 2026, RUU Pelindungan Ketenagakerjaan **belum disahkan**. Selalu sebutkan ini di disclaimer. Jika pengguna menyebut UU baru sudah berlaku, katakan bahwa skill ini belum diperbarui untuk UU tersebut dan sarankan cek Disnaker.
- Detail dasar hukum & status verifikasi: `references/dasar-hukum.md`.
- Jangan menulis klausul yang merugikan pekerja di bawah standar minimum, meskipun diminta (masa percobaan, denda berlebihan, penahanan ijazah, "tanpa BPJS"). Jelaskan alasannya dan tawarkan alternatif yang sah.
- Jangan menentukan apakah suatu PHK sah atau menghitung pesangon karyawan tetap.
- Angka UMK tidak disimpan di skill. Minta pengguna mengisi atau mengecek sendiri.
- Kasus rumit (kontrak berulang dengan jeda, sengketa, pekerja hamil diputus kontrak, TKA, kontrak > Rp50 jt/bulan dengan non-compete) → beri gambaran umum, lalu arahkan ke Disnaker setempat atau konsultan hukum ketenagakerjaan.
- Data pekerja (NIK, alamat, gaji) bersifat pribadi. Jangan disimpan atau disebar di luar percakapan.
- Disclaimer wajib di setiap output: bukan nasihat hukum; dasar UU 13/2003 jo. UU 6/2023, PP 35/2021, Putusan MK 168/PUU-XXI/2023 (dicek 26 September 2026); UU baru belum disahkan; konsultasikan ke Disnaker/konsultan hukum.
