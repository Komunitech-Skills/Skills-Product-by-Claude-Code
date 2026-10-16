> **Sumber keluaran:** penguji independen Akun B, 2026-10-13, Claude Code (simulasi agent), data fiktif; menggantikan contoh lama yang memuat atribut/angka tanpa sumber.

# Uji 03 — Skenario normal: jasa renovasi rumah (B2C, tiket besar)

## Input pengguna
"Saya kontraktor renovasi rumah di Depok (dapur, kamar mandi, tambah kamar). Rata-rata nilai proyek 35 juta, modal material + tukang ± 26,5 juta. Survei & bikin RAB keluar biaya sekitar 250 ribu per kunjungan, biasanya 1 dari 4 survei yang jadi. Sekarang dapat proyek 5 per bulan, hampir semua dari mulut ke mulut. Budget promosi 5 juta per bulan. Mau rencana marketing Okt-Des, target 20 proyek."

## Output

**Perilaku agent:** info wajib lengkap (usaha, harga, modal, periode, tujuan, anggaran), jadi tidak ada pertanyaan balik. Info yang tidak diberikan pengguna (kondisi Google Maps, jumlah klien lama, kapasitas tukang, profil klien, laba minimum per proyek, besaran komisi referral) tidak ditebak: ditulis "DATA BELUM ADA" atau `[isi: ...]`, dan dijadikan pekerjaan minggu 1. Biaya survei yang gagal dimasukkan ke biaya per proyek: 4 survei x Rp 250.000 = **Rp 1.000.000 per proyek jadi**.

---

# Rencana Marketing Jasa Renovasi Rumah Depok — Oktober-Desember 2026

Disusun: 13 Okt 2026 | Pemilik rencana: pemilik usaha | **Asumsi yang dipakai (ganti dengan angka Anda bila berbeda):**
1. Periode 13 Okt-31 Des 2026 (mulai hari rencana ini disusun).
2. Laju 5 proyek per bulan (= 15 per kuartal) bertahan bila tidak ada perubahan (asumsi, ganti dengan angka Anda).
3. Biaya platform 0% (jasa, tidak lewat marketplace); tempat jualan WhatsApp + Instagram (bawaan skill, karena Anda hanya menyebut mulut ke mulut).
4. Dikerjakan 1 orang, 5 jam per minggu (bawaan skill).
5. Laba minimum per proyek belum Anda tentukan, jadi CAC target dan ROAS target tidak dihitung.
6. Pembagian dana per kanal = usulan mengikuti aturan 70/20/10 (asumsi, ganti dengan angka Anda).
7. Angka corong B memakai batas bawah `references/patokan-angka.md` (asumsi, ganti dengan data Anda).

## 0. Ringkasan
- Tujuan: proyek deal Okt-Des **15 -> 20** (omzet ± Rp 700 juta bila nilai rata-rata tetap Rp 35 juta), tenggat 31 Des 2026.
- Segmen: pemilik rumah di Depok yang butuh renovasi dapur, kamar mandi, atau tambah kamar. Profil lebih rinci: DATA BELUM ADA (tugas minggu 1).
- Kanal utama (3): referral + WA pelanggan lama, Google Maps + ulasan, konten sebelum-sesudah di Instagram/Facebook Group. Iklan berbayar hanya eksperimen kecil.
- Anggaran Rp 15.000.000 (Rp 5 juta x 3 bulan), cadangan eksperimen 10% = Rp 1.500.000.
- Margin Rp 7,5 juta per proyek (21,4%, status **TIPIS**); CAC titik impas Rp 7.500.000 (batas atas, bukan perkiraan biaya).
- Minggu ini: catat sumber setiap chat baru, cek profil Google Business, minta ulasan dan izin foto dari klien lama.

## 1. Kondisi sekarang
| Hal | Kondisi | Data / "DATA BELUM ADA" |
|---|---|---|
| Proyek per bulan | 5, hampir semua dari mulut ke mulut | Pemilik |
| Nilai proyek rata-rata | Rp 35.000.000 | Pemilik |
| Omzet per bulan | ± Rp 175.000.000 (5 x Rp 35 juta) | Hitungan dari data pemilik |
| Modal per proyek | ± Rp 26.500.000 | Pemilik |
| Biaya survei per proyek jadi | Rp 1.000.000 (4 survei x Rp 250.000) | Hitungan dari data pemilik |
| Margin | Rp 7.500.000 (21,4%) | Script |
| Survei yang jadi | 1 dari 4 (25%) | Pemilik |
| Jumlah klien lama yang bisa dihubungi | DATA BELUM ADA | — |
| Profil Google Business dan jumlah ulasan | DATA BELUM ADA | — |
| Akun Instagram/Facebook aktif | DATA BELUM ADA | — |
| Proyek maksimal per bulan yang sanggup dikerjakan | DATA BELUM ADA | — |

## 2. Tujuan SMART
| Tujuan | Angka awal | Angka target | Tenggat | Cara ukur |
|---|---|---|---|---|
| Utama: proyek deal Okt-Des | 15 (asumsi laju 5/bulan) | 20 | 31 Des 2026 | Rekap proyek; "deal" = [isi: definisi deal, mis. kontrak atau DP] |
| Pendukung 1: survei yang jadi | 25% | ≥ 25% | Dicek tiap bulan | Catatan survei vs deal |
| Pendukung 2: chat baru yang tercatat sumbernya | DATA BELUM ADA | 100% | Mulai minggu 1 | Kolom "tahu dari mana?" di catatan chat |

## 3. Target pasar
Segmen prioritas: pemilik rumah di Depok yang meminta renovasi dapur, kamar mandi, atau tambah kamar (jenis pekerjaan dari Anda). Masalah yang dipecahkan, momen beli, dan tempat mereka berada: **DATA BELUM ADA**. Cara mengisinya: tanyakan ke 5 klien terakhir "kenapa memilih kami dan dari mana tahu kami?" (arahkan ke `riset-calon-pelanggan`). Usia, jenis rumah, dan wilayah selain Depok tidak ditebak di sini.

## 4. Pesan kunci
- Janji utama (1 kalimat): `[isi: satu janji yang benar-benar bisa Anda penuhi, ambil dari alasan klien lama memilih Anda]`.
- Bukti (pakai yang benar-benar ada): foto sebelum-sesudah proyek asli (dengan izin pemilik rumah, tanpa alamat), ulasan klien asli, contoh RAB tertulis milik sendiri.
- Ajakan: "Chat WhatsApp untuk jadwal survei dan RAB."
- Jangan klaim yang tidak bisa dibuktikan (mis. "termurah", "pasti selesai N hari"), dan jangan memakai testimoni rekaan.

## 5. Kanal
| Kanal | Peran di corong | Alasan | Pemilik | Jam/minggu |
|---|---|---|---|---|
| Referral + WA pelanggan lama | Rekomendasi, Beli lagi | Kanal yang sudah jalan: hampir semua proyek sekarang dari mulut ke mulut (data Anda). WA hanya ke orang yang pernah chat atau jadi klien, tanpa blast. | Pemilik | 2 |
| Google Maps / Google Business + ulasan | Kenal, Tertarik | Orang yang mencari jasa renovasi di sekitar Depok; gratis. Status profil sekarang: DATA BELUM ADA. | Pemilik | 1,5 |
| Konten sebelum-sesudah (Instagram, Facebook Group/grup WA perumahan) | Kenal, Tertarik | Renovasi mudah ditunjukkan lewat foto. Patuhi aturan grup, jangan spam. Iklan kecil (eksperimen) memakai bahan ini. | Pemilik | 1,5 |
Follow-up calon klien setelah survei -> `pengingat-follow-up`; penawaran/RAB -> `surat-penawaran-harga`; balasan ulasan -> `balas-ulasan-pelanggan`.

## 6. Kalender
Momen dari `references/kalender-momen.md` (pola umum, bukan jaminan tanggal):
| Minggu / tanggal | Momen | Kegiatan | Kanal |
|---|---|---|---|
| Minggu 1-2 (13-26 Okt) | Persiapan | Catat sumber chat, cek profil Google Business, kumpulkan daftar klien lama, minta izin foto proyek | Semua |
| Okt-Nov | Musim hujan kira-kira Okt-Mar, tergantung daerah | Uji topik konten yang berkaitan dengan musim; ukur apakah ada chat masuk (asumsi, belum terbukti) | Konten |
| Tiap tanggal 25-3 | Gajian (pola umum) | Kirim kabar/ucapan ke klien lama dan tanyakan rekan yang butuh renovasi | WA |
| 20 Des-1 Jan | Natal & Tahun Baru (pola umum) | Pastikan jadwal kerja tim saat libur; umumkan jadwal survei setelah libur | WA, Maps |
Ramadan-Lebaran bergeser lebih awal tiap tahun; bila ingin menjadwalkan proyek menjelang Lebaran 2027, tanggalnya DATA BELUM ADA, cek SKB Libur Nasional. 11.11/12.12 adalah momen marketplace dan tidak dipakai di rencana ini.

## 7. Anggaran (keluaran script)
```
python3 scripts/alokasi_anggaran.py alokasi --anggaran "Rp 15.000.000" --bulan 3 --kanal "Referral & WA pelanggan lama=75,Google Maps & ulasan=15,Konten sebelum-sesudah (IG/FB)=10"

ANGGARAN Rp 15.000.000 untuk 3 bulan
- Referral & WA pelanggan lama: Rp 10.125.000 total (67.5% dari anggaran), ~Rp 3.375.000/bulan
- Google Maps & ulasan: Rp 2.025.000 total (13.5% dari anggaran), ~Rp 675.000/bulan
- Konten sebelum-sesudah (IG/FB): Rp 1.350.000 total (9.0% dari anggaran), ~Rp 450.000/bulan
- Cadangan eksperimen (10%): Rp 1.500.000
Cek: jumlah semua = anggaran (OK). Sisa pembulatan Rp diserap kanal dengan sisa terbesar.
```
Dana referral dipakai untuk hadiah/komisi referral dan kabar ke klien lama; **besaran komisi per proyek diputuskan pemilik** (lihat bagian 11). Cadangan eksperimen Rp 1.500.000 dipakai untuk satu iklan berbayar kecil karena margin berstatus TIPIS. Pembagian ini mendekati aturan 70/20/10 (kira-kira 67,5% kanal terbukti, 22,5% kanal berikutnya, 10% eksperimen); persentase adalah usulan, ganti sesuai kondisi Anda.

## 8. Target angka (keluaran script)
> **Disegarkan ke v1.0.7 (2026-10-16):** keluaran dijalankan ulang dengan perintah yang sama. Karena laba minimum per proyek belum ditentukan (tanpa `--laba-target-per-pesanan`), label "Minimal pesanan agar balik modal iklan" tetap dipakai — minimal di sini memang sama dengan titik impas iklan, jadi baris "Titik impas iklan" tidak muncul. Yang bertambah hanya baris "Batas atas anggaran iklan, sesuai target laba" (sama dengan batas impas, Rp 150.000.000, karena tidak ada laba target) dan kalimat penutup tentang pesanan organik.
```
python3 scripts/alokasi_anggaran.py target --harga-jual 35000000 --hpp 26500000 --biaya-platform 0 --biaya-per-pesanan 1000000 --anggaran-iklan 1500000 --target-omzet 700000000

Harga jual Rp 35.000.000 | HPP Rp 26.500.000 | biaya platform Rp 0 | biaya/pesanan Rp 1.000.000
Margin kontribusi per pesanan: Rp 7.500.000 (21.4%)  STATUS: TIPIS
- CAC titik impas (pesanan pertama): Rp 7.500.000
- ROAS titik impas: 4.67
- Minimal pesanan agar balik modal iklan (bukan perkiraan): 1
- Omzet minimal dari iklan (bukan perkiraan): Rp 35.000.000
- Jumlah pesanan yang dibutuhkan untuk target omzet: 20
- Batas atas anggaran iklan, impas (hanya bila SEMUA pesanan dari iklan; bukan saran belanja): Rp 150.000.000
- Batas atas anggaran iklan, sesuai target laba (hanya bila SEMUA pesanan dari iklan; bukan saran belanja): Rp 150.000.000
Cara baca: angka 'minimal' = syarat agar iklan tidak rugi, BUKAN perkiraan hasil iklan.
Kalau 'tanpa iklan' sebagian pesanan tetap datang (organik), iklan cukup menutup sisanya: kurangi pesanan_dibutuhkan dengan perkiraan pesanan organik.
```
Cara membaca (penting untuk jasa bernilai besar):
- "Minimal pesanan: 1" artinya iklan Rp 1,5 juta cukup balik modal bila menghasilkan 1 proyek. Itu syarat minimum, **bukan perkiraan hasil**.
- "Batas atas Rp 150 juta" hanya plafon teoretis bila semua 20 proyek berasal dari iklan. **Bukan saran belanja**; rencana ini hanya memakai Rp 1,5 juta untuk iklan.
- CAC target dan ROAS target: DATA BELUM ADA karena laba minimum per proyek belum Anda tentukan (lihat bagian 11).
- Margin 21,4% berstatus TIPIS (15% - < 25%): iklan berbayar hanya kecil dan dipantau ketat; utamakan referral dan Maps.

Corong A (data Anda: 1 dari 4 survei jadi):
```
python3 scripts/alokasi_anggaran.py funnel --target-pesanan 20 --tahap "Survei>Proyek jadi=25"
Target 20 pesanan -> perlu 80 di awal corong (Survei)
- Survei -> Proyek jadi: konversi 25% -> butuh 80 untuk dapat 20
```
Corong B (asumsi, ganti dengan data Anda; angka dari batas bawah `references/patokan-angka.md`), untuk 5 proyek tambahan di atas laju 15:
```
python3 scripts/alokasi_anggaran.py funnel --target-pesanan 5 --tahap "Klik>Chat=10" --tahap "Chat>Proyek jadi=15"
Target 5 pesanan -> perlu 340 di awal corong (Klik)
- Klik -> Chat: konversi 10% -> butuh 340 untuk dapat 34
- Chat -> Proyek jadi: konversi 15% -> butuh 34 untuk dapat 5
```
Corong B hanya contoh hitungan sampai Anda punya data chat dan klik sendiri.

## 9. KPI & rutinitas pantau
| Tahap | KPI | Target | Sumber | Dicek | Aturan hentikan/ubah |
|---|---|---|---|---|---|
| Kenal | Penelusuran dan kunjungan profil Google Business | DATA BELUM ADA (catat dasar 2 minggu) | Insight Google Business | Mingguan | — |
| Tertarik | Chat WA baru beserta sumbernya | 100% tercatat | Catatan chat | Mingguan | Bila sumber tidak tercatat, perbaiki pencatatan dulu |
| Beli | Survei yang jadi | ≥ 25% | Catatan survei vs deal | Bulanan | Bila di bawah 25% selama 4 minggu, periksa RAB dan penawaran |
| Beli | Proyek deal kumulatif | 20 pada 31 Des | Rekap proyek | Mingguan | — |
| Beli | Biaya iklan kecil per proyek jadi | ≤ Rp 7.500.000 (CAC titik impas) | Dasbor iklan + rekap | Mingguan | Hentikan iklan bila 4 minggu berturut-turut di atas Rp 7.500.000 |
| Beli lagi | Klien lama yang minta pekerjaan tambahan | [isi: target] | Rekap proyek | Bulanan | — |
| Rekomendasi | Proyek dari referral dan ulasan baru | [isi: target setelah tahu jumlah sekarang] | Catatan sumber, Google Business | Bulanan | — |
Rutinitas: 10 menit tiap minggu mengisi catatan, evaluasi bulanan di akhir Okt, Nov, Des.

## 10. Risiko & rencana B
| Risiko | Tanda | Tindakan |
|---|---|---|
| Banyak survei tidak jadi | Survei yang jadi di bawah 25% | Saring calon klien lewat chat sebelum survei; periksa RAB |
| Proyek bertambah tetapi kapasitas tim terbatas | Jadwal molor; kapasitas maksimal DATA BELUM ADA | Tentukan batas proyek per bulan; tawarkan jadwal setelah libur akhir tahun |
| Sumber chat tidak tercatat | Kolom "tahu dari mana?" kosong | Jadikan pertanyaan wajib di chat pertama |
| Iklan kecil tidak menghasilkan | 4 minggu di atas CAC titik impas | Hentikan; pindahkan dana ke referral dan Maps |

## 11. Keputusan terbuka
- Definisi "deal" (kontrak atau DP) untuk hitungan proyek.
- Laba minimum per proyek (agar CAC target dan ROAS target bisa dihitung).
- Besaran hadiah/komisi referral per proyek (dana tersedia Rp 10.125.000 untuk kuartal ini).
- Janji utama yang bisa dibuktikan, dan izin foto proyek dari klien lama.
- Kapasitas maksimal proyek per bulan.

## 12. Langkah minggu ini
1. Mulai catat "tahu dari mana?" di setiap chat baru. 2. Cek profil Google Business Anda dan hitung ulasan yang ada. 3. Buat daftar klien lama yang boleh dihubungi, lalu minta ulasan dan izin foto proyek.

*Bukan jaminan hasil. Target adalah tujuan kerja, bukan prediksi; tanggal momen dan aturan platform perlu dicek ke sumber resmi.*

---

## Catatan penguji
- **Karangan di contoh lama (dihapus):** "Kanal yang sudah terbukti (70% usaha datang dari sini)" (input hanya "hampir semua dari mulut ke mulut"; "70%" kemungkinan tertukar dengan aturan alokasi 70/20/10), komisi referral "Rp 500 rb per proyek jadi", laba target "Rp 3 jt/proyek", "pemilik 4 jam/minggu + admin", "Google Maps belum dikelola", wilayah "Cinere, Cibubur", segmen "30-50 th, rumah 5-20 tahun", "Lebaran 2027 sekitar Maret 2027", target "+25 ulasan", "50 chat/kuartal", serta aturan "bila < 15%" dan konversi "Chat -> Survei 40%" tanpa dasar.
- **Sekarang:** semua fakta usaha berasal dari input (nilai proyek, modal, biaya survei, 1 dari 4, 5 proyek/bulan, mulut ke mulut, Rp 5 juta/bulan, target 20, Depok); sisanya "DATA BELUM ADA", `[isi: ...]`, atau asumsi bertanda. Tidak ada angka pasar atau persentase kanal dari luar input.
- **Verifikasi independen:** margin 35.000.000 - 26.500.000 - 1.000.000 = 7.500.000 (21,43%); ROAS impas 35/7,5 = 4,67 (dibulatkan ke atas); iklan Rp 1,5 juta / margin 7,5 juta -> 1 proyek; alokasi 13.500.000 x 75% / 15% / 10% = 10.125.000 / 2.025.000 / 1.350.000 (jumlah + cadangan 1.500.000 = 15.000.000); corong 20/0,25 = 80, 5/0,15 = 33,3 -> 34, 34/0,10 = 340. Semua cocok dengan keluaran script.
- **Beda dari contoh lama:** status margin 21,4% kini TIPIS (contoh lama menulis AMAN, memakai ambang lama), sehingga iklan berbayar dibatasi pada eksperimen kecil.
- Hasil: PASS.
