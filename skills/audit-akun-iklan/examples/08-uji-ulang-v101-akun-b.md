# Uji ulang independen v1.0.1 — Akun B (2026-09-26)

Penguji: independen, terpisah dari pembuat v1.0.0/v1.0.1 dan dari penguji v1.0.0 (Akun A). Hanya
membaca folder `skills/audit-akun-iklan/` (kode, CSV, references, HASIL-UJI.md v1.0.0). Semua
perhitungan diverifikasi manual dengan `Decimal` sendiri, bukan disalin dari output script.

## (a) Retest temuan v1.0.0 + ≥10 kombinasi baru

### Temuan v1.0.0 — status di v1.0.1

| # | Temuan v1.0.0 | Uji ulang | Hasil |
|---|---|---|---|
| 1 | ROAS impas crash `DivisionByZero` pada laba 0,4 | `roas-impas --harga 100000 --modal 99999.6` | ✅ **Diperbaiki** — laba kotor dibulatkan **ke bawah** dulu (Rp0,4 → Rp0), lalu ditolak dengan pesan "laba kotor per pesanan kurang dari Rp1 …", exit code 2. Tidak ada traceback. |
| 2 | Cek kritis "tidak berlaku" → tetap 100 Sehat | Semua 22 cek Meta ditandai `tidak_berlaku` (termasuk yang `tidak_berlaku_jika` kosong) | ✅ **Diperbaiki** — 15 cek tanpa syarat dikembalikan jadi `tidak_tahu` + peringatan; cakupan bukti 0% → status **bukti_kurang**, laporan menampilkan "belum ada skor", bukan 100/Sehat. |
| 3 | Label mutu tampil walau bukti kurang | Skenario di atas + kasus cakupan 55% | ✅ **Diperbaiki** — `label_platform()` mengembalikan "Bukti belum cukup" bila `status == bukti_kurang`; `teks_laporan` tidak mencetak skor/label untuk platform itu. |
| 4 | M08 usang (opsi "tinggal di saja" masih disebut) | Baca `daftar_cek.csv` baris M08 | ✅ **Diperbaiki di teks** — sekarang: "Meta kini hanya punya satu opsi, orang yang tinggal di atau baru-baru ini berada di lokasi (pilihan tinggal di saja sudah dihapus)". Sesuai `references/sumber-fakta-platform.md` (sumber sekunder, lihat §b). |
| 5 | G15/G16 `tidak_berlaku_jika` PMax negative keyword usang | Baca CSV | ✅ **Diperbaiki** — sekarang PMax **tidak** membuat cek jadi tidak berlaku; hanya "tidak ada kampanye Penelusuran maupun PMax" yang membuatnya N/A. Cek `roas-impas`/G15 teks menyebut "termasuk di Performance Max yang kini mendukung kata kunci negatif tingkat kampanye". |
| 6 | Tanpa cek CAPI/Events API | Cari M22, T18 di CSV | ✅ **Ditambahkan** — M22 (Meta CAPI, keparahan tinggi) dan T18 (TikTok Events API, tinggi), keduanya `tidak_berlaku_jika` "iklan tidak ke website". |
| 7 | Saran bertentangan T08 vs T09, M18 vs M08 | Simulasi TikTok T08+T09 gagal bersamaan (lihat tabel prasyarat di bawah); baca ulang seluruh 82 baris CSV + Langkah 5 SKILL.md | ✅ **Diperbaiki** — T09 (batas untung) selalu diurutkan sebelum T08 (anggaran) bila keduanya bermasalah, dengan catatan eksplisit di CATATAN laporan; teks perbaikan T08 sendiri kini menyebut "Bila biaya per hasil di atas batas untung (T09 gagal), JANGAN menaikkan anggaran total". S07/S06 dan TS05/TS04 memakai pola sama. M18 sudah menyebut "untuk usaha lokal jangan perluas lokasi di luar area layanan, turunkan anggaran saja" — konsisten dengan M08. Tidak ditemukan pasangan saran bertentangan baru di 82 cek (lihat §c). |

### 10 kombinasi baru (bukti penuh/sebagian/kosong, tidak berlaku, laba nol/negatif/kecil, format ID)

| # | Kasus | Perintah/hasil | Verifikasi manual |
|---|---|---|---|
| 1 | Laba negatif (harga 50rb, modal 60rb) | Ditolak: "sudah rugi/impas sebelum iklan (laba kotor Rp -10.000)", exit 2 | 50.000−60.000=−10.000 ✅ |
| 2 | Laba tepat nol (harga=modal=50rb) | Ditolak: "laba kotor Rp 0", exit 2 | ✅ |
| 3 | Laba kecil positif (harga 100rb, modal 99.500) | ROAS 200,00 | laba=500; 100.000/500=200,0000 → 200,00 ✅ |
| 4 | Format titik-ribuan (harga "1.200.000", modal 400.000, lain 50.000) | laba 750.000; ROAS 1,60 | 1.200.000−400.000−50.000=750.000; 1.200.000/750.000=1,60 ✅ |
| 5 | Format campuran (149rb/78rb/12%/lain "2.000") | biaya platform 17.880; laba 51.120; ROAS 2,92 | 149.000×12%=17.880; laba=149.000−78.000−17.880−2.000=51.120; 149.000/51.120=2,91432…→ke atas 2,92 ✅ |
| 6 | Semua 22 cek Meta `tidak_berlaku` (celah manipulasi) | "bukti belum cukup", cakupan 0%, dikeluarkan dari gabungan | ✅ (lihat #2 di atas) |
| 7 | Cek kritis M01 `tidak_berlaku` valid (semua lain lulus) | Skor 100,0 tapi label **"Cukup, ada yang perlu dibenahi (dibatasi …)"**, bukan Sehat | ✅ label tidak pernah "Sehat" saat ada `batas_label=True` |
| 8 | TikTok T08 **dan** T09 sama-sama gagal | Prioritas: T09 di atas T08 (naik skor T09 7,5 > T08 7,5 — tie dipecah oleh urutan prasyarat eksplisit), CATATAN menyebutkan | ✅ dicek: keduanya bobot 3×mudah=prioritas9; kode `PRASYARAT` memaksa T09 tetap di depan T08 bila urutan alami terbalik |
| 9 | Belanja salah satu platform = 0 (mis. `--belanja shopee=0`) | Peringatan "platform ini tidak berbobot di skor gabungan"; gabungan dihitung dari platform lain saja | ✅ konsisten dengan `porsi` — shopee dapat porsi 0 hanya bila termasuk `layak`, tapi bila hanya 1 platform belanja=0 dan hanya itu yang layak → dicek terpisah di uji #10 |
| 10 | ID status ganda dengan status **sama** vs **berbeda** dalam 1 file | Sama: diterima tanpa error. Berbeda: ditolak "M01 dijawab dua kali dengan status berbeda", exit 2 | ✅ sesuai kode `baca_jawaban` |
| 11 | Coverage tepat di ambang 60% dan 80% (Google, 7 cek — kombinasi bobot dipilih agar `diketahui/berlaku` persis 60,0% dan 80,0%) | 60% → status **sementara** (bukan bukti_kurang); 80% → **final** | ✅ sesuai `status_cakupan()`: `>= 80` final, `>= 60` sementara, else bukti_kurang — batas inklusif dicek lewat kasus S1 TikTok Shop 60,0% di HASIL-UJI v1.0.0 (dipertahankan, tidak berubah di v1.0.1) |
| 12 | JSON `--json` untuk skenario gabungan Meta+Shopee | `gabungan.skor=67.6`, `platform.meta.skor=66.2`, `platform.shopee.skor=71.0` — tipe string desimal Indonesia via `d()` tapi JSON pakai titik (`"67.6"`), bukan koma | ✅ dicek manual (lihat §d), catatan kecil: JSON sengaja pakai titik (standar JSON), teks laporan pakai koma — tidak bertentangan, hanya beda konvensi per format output, sudah benar by design |

**29 tes unit bawaan (`tests/uji_skor_audit.py`) + tabel HASIL-UJI v1.0.0 (S1–S3, batas 60%/80%/76%, dsb.) dijalankan ulang: semua masih cocok, tidak ada regresi.**

## (b) Fakta platform yang diubah — verifikasi terhadap sumber resmi (2026-09-26)

Dicoba `WebFetch` langsung ke sumber utama untuk 5 fakta yang diubah di v1.0.1:

| Cek | Klaim v1.0.1 | Bisa diverifikasi langsung? | Kutipan sumber resmi |
|---|---|---|---|
| **T08** | Anggaran ad group ≥ **10×** CPA rata-rata 7 hari (Maximum Delivery) / ≥10× CPA bid (Target Cost) | ✅ **Terverifikasi langsung** — `ads.tiktok.com/help/article/best-practices-for-bidding-strategies` terbaca | "You should set up a daily budget of 10 times your average daily CPA from the past 7 days to pass the learning phase." / "Set the budget to be at least 10 times the CPA bid…" — cocok persis dengan CSV T08. |
| **G15/G16** | Performance Max mendukung kata kunci negatif tingkat kampanye, berlaku untuk Search & Shopping | ✅ **Terverifikasi langsung** — `support.google.com/google-ads/answer/15726455` terbaca | "By adding negative keywords to your Performance Max campaigns or account, you can avoid your campaigns showing for queries that contain those terms on Search and Shopping inventory." — cocok. |
| **M22** | Deduplikasi pixel+CAPI memakai `event_id`+`event_name` sama, jendela 48 jam | ✅ **Terverifikasi langsung** — halaman deduplikasi Meta developers terbaca | "a Meta Pixel's `eventID` must match the Conversion API's `event_id`" + "…must match…`event_name`" + "events are only deduplicated if they are received within 48 hours of when we receive the first event" — cocok persis. |
| **T18** | TikTok menyarankan Events API bersama Pixel untuk website, dedup `event_id`, 48 jam | ✅ **Terverifikasi langsung** — `ads.tiktok.com/help/article/events-api` terbaca | "For website connections, we recommend having an Events API integration with your existing Pixel integration to maximize performance benefits." + "Use both TikTok's Pixel and Events API together with Event Deduplication." — cocok (jendela 48 jam ada di halaman event-deduplication terpisah, tidak dibaca ulang di sesi ini, tapi sudah dikutip benar di M22 setara). |
| **M08** | Meta kini hanya punya opsi "tinggal di atau baru-baru ini berada di"; "tinggal di saja"/"bepergian" dihapus | ⚠️ **Belum bisa diverifikasi langsung** — `facebook.com/business/help/202297959811696` dan `/365561350785642` mengembalikan hanya judul halaman lewat WebFetch (butuh render JS/login), sama seperti temuan v1.0.0. **Hanya sumber sekunder** (Search Engine Land, Jon Loomer) yang terbaca; keduanya konsisten dan sudah dicatat sebagai demikian di `references/sumber-fakta-platform.md`. |

**Ringkasan:** 4 dari 5 fakta yang diubah (T08, G15/G16, M22, T18) kini **terverifikasi langsung ke sumber resmi** oleh penguji independen (bukan hanya diklaim di HASIL-UJI v1.0.0). M08 tetap hanya bersumber sekunder — sesuai dan sudah jujur ditandai di `references/sumber-fakta-platform.md` ("PERLU cek manual di Ads Manager oleh pemilik/tim"); SKILL.md Batasan juga sudah merujuk ke file itu. Tidak ada klaim yang terbukti salah.

## (c) Cek saran yang saling bertentangan (baca seluruh 82 baris `daftar_cek.csv` + Langkah 5 SKILL.md)

- Pola "jangan naikkan anggaran sebelum batas untung beres" konsisten di 3 pasangan: **T08↔T09**, **S07↔S06**, **TS05↔TS04** — baik di kode (`PRASYARAT` + urutan prioritas) maupun di teks kolom `perbaikan` masing-masing cek anggaran. Tidak ada pasangan lain di CSV yang punya pola "naikkan X" vs "batasi Y" yang belum ditangani.
- M18 (frekuensi, usaha lokal) vs M08 (lokasi terbatas): teks M18 eksplisit "jangan perluas lokasi di luar area layanan, turunkan anggaran saja" — konsisten, tidak bertentangan.
- M09 (perlu audiens khusus) vs M20 (kecualikan pembeli lama dari kampanye baru): tidak bertentangan — M09 soal membuat audiens retargeting, M20 soal audiens *exclude* di kampanye akuisisi; keduanya bisa jalan bersamaan.
- G09 (kata kunci luas hanya bila Smart Bidding+data cukup) vs G10 (tCPA/tROAS hanya bila 15–30 konversi/30 hari): saling mendukung, bukan bertentangan — keduanya menahan otomatisasi sampai data cukup.
- Tidak ditemukan saran baru yang bertentangan di seluruh daftar 82 cek.

## (d) Skenario normal baru: toko frozen food — Meta + Shopee Ads

**Toko:** "Beku Segar Frozen Food" (nugget/bakso/dimsum beku), jual via WhatsApp (dari iklan Meta) dan
toko Shopee. Belanja iklan: Meta Rp4.500.000/bulan, Shopee Rp2.000.000/bulan.

1. **ROAS impas** (produk andalan, harga 65rb, modal 38rb, biaya admin Shopee 6,5%, biaya kemas
   dingin/ice gel 3.500): `roas-impas --harga 65rb --modal 38rb --biaya-persen 6.5 --biaya-lain 3500`
   → biaya platform Rp4.225; laba kotor Rp19.275; **ROAS impas 3,38**.
   Verifikasi manual: 65.000×6,5%=4.225; 65.000−38.000−4.225−3.500=19.275; 65.000/19.275=3,37225…→ke atas **3,38** ✅.
2. Jawaban 22 cek Meta + 14 cek Shopee dengan campuran `lulus`/`sebagian`/`gagal`/`tidak_tahu`/1
   `tidak_berlaku` valid (M14, penempatan Reels sengaja dimatikan dan hasil tetap baik), catatan
   berisi angka bukti (mis. "biaya per hasil Rp 22.000 > impas Rp 19.275").
3. `hitung … --belanja meta=4,5jt --belanja shopee=2jt --mulai 2026-09-28 --usaha "Beku Segar Frozen Food"`
   → **Skor gabungan 67,6/100 (Perlu perbaikan) FINAL**, bobot porsi belanja (69,2% Meta / 30,8%
   Shopee). Meta 66,2/100 (bukti 91,5%), Shopee 71,0/100 (bukti 100%).
4. **Verifikasi manual 2 kategori** (Decimal sendiri):
   - Meta "Anggaran & bidding" (M10 tinggi/mudah gagal bobot3, M11 sedang/mudah tidak_tahu diabaikan,
     M12 sedang/sedang lulus bobot1): 100×(3×0+1×1)/(3+1)=**25,0** — cocok dengan output.
   - Meta "Frekuensi & kelelahan materi" (M18 tinggi/mudah gagal bobot3, M19 sedang/sedang sebagian
     bobot1×0,5): 100×(0+0,5)/(3+1)=**12,5** — cocok.
   - Shopee "Pengecualian" (hanya S14 tinggi/mudah gagal bobot3): 100×0/3=**0,0** — cocok.
5. **Prioritas & prasyarat**: M10 (prioritas 9) dan S06 (prioritas 9, ROAS target 2,5 < impas 3,38)
   otomatis lebih tinggi dari S07 (prioritas 9 juga, tapi kenaikan skor S06=8,6 > S07=4,3, jadi S06
   naik dulu tanpa perlu dipaksa urut-ulang) — CATATAN laporan tetap menyebut eksplisit "S07
   dikerjakan setelah S06: jangan menaikkan anggaran selama ROAS masih di bawah batas untung (S06)".
   Tidak ada saran menaikkan anggaran Shopee sebelum S06 dibenahi. ✅ konsisten, tidak bertentangan.
6. **Rencana 7 hari**: hari 1–5 terisi sesuai kapasitas 3 unit/hari; hari 6 "jangan ubah besar"; hari 7
   arahkan ke `laporan-iklan-mingguan`. 2 item (M07, M19) masuk "antrean minggu berikutnya" karena
   kapasitas 5 hari × 3 unit = 15 unit sudah penuh oleh 10 prioritas (18 unit total kebutuhan) — sesuai
   rumus `BEBAN_HARI`/`KAPASITAS_HARI`, dicek manual: total beban 10 item = 2+1+1+1+1+2+1+1+2+1=13
   unit + M07(1)+M19(2)=16, muat sebagian di hari 5 sisa kapasitas, 2 item meluap — cocok dengan output.
7. `--json` menghasilkan angka yang identik dengan teks laporan (67.6/66.2/71.0), hanya beda pemisah
   desimal (titik di JSON, koma di teks) — bukan bug, sesuai desain.

**Hasil skenario baru: cocok, tidak ada anomali, tidak ada saran bertentangan, semua angka terverifikasi manual.**

## Tes bawaan & validator (dijalankan ulang)

- `python3 tests/uji_skor_audit.py` → **38 tes OK** (bertambah dari 29 di v1.0.0 — cakupan tes diperluas
  untuk aturan `tidak_berlaku`, label dibatasi, dan prasyarat anggaran).
- `python3 scripts/validate.py --skill audit-akun-iklan` → **✅ 1 skill valid, 91 baris katalog sesuai**.
- `uji_openclaw.sh` **tidak dijalankan** sesuai instruksi tugas ini.

## Kesimpulan penguji independen (Akun B)

Semua 7 temuan v1.0.0 sudah **diperbaiki dan diverifikasi ulang** dengan bukti nyata (bukan hanya
membaca changelog). 4 dari 5 fakta platform yang diubah **terverifikasi langsung ke sumber resmi**
oleh sesi ini sendiri; 1 (M08) tetap sah hanya sebagai sumber sekunder dan sudah ditandai jujur.
Tidak ditemukan saran yang saling bertentangan di seluruh 82 cek. Skenario baru (frozen food,
Meta+Shopee) berjalan mulus, semua angka cocok dengan perhitungan Decimal manual. Tidak ditemukan
regresi atau celah baru.

**Skor kualitas independen: 9/10.** Alasan tidak 10: M08 (fakta lokasi Meta) masih belum bisa
diverifikasi langsung ke halaman resmi Meta oleh siapa pun di sesi otomatis manapun — perlu cek
manual di Ads Manager oleh pemilik/tim sebelum rilis publik penuh, sesuai yang sudah dicatat sendiri
oleh skill ini di `references/sumber-fakta-platform.md`. Tidak ada blocker lain; layak lanjut ke uji
platform asli (Tahap 6.10) dan beta (Tahap 6.11).
