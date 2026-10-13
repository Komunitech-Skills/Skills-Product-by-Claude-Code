# Hasil Uji Independen — tulisan-tanpa-kesan-ai v1.0.0

Diuji oleh penguji independen (Akun B) yang **hanya membaca folder skill** ini (SKILL.md, references/,
scripts/, examples/, README.md, ATTRIBUTION.md), sesuai pedoman kurasi Komunitech tahap 6. Tidak mengubah SKILL.md,
README.md, scripts/, atau catalog.csv.

## 1. Atribusi MIT — diverifikasi BENAR
- `ATTRIBUTION.md` mencatat sumber `petergyang/no-ai-slop` (MIT, Copyright (c) 2026 Peter Yang) dengan
  benar; `LICENSE-MIT` berisi teks lisensi MIT lengkap dan sesuai (dicek terhadap
  `https://raw.githubusercontent.com/petergyang/no-ai-slop/main/LICENSE` — konsisten).
- Bagian yang diadaptasi (struktur dua mode + beberapa prinsip umum) vs. bagian orisinal (17 pola
  Indonesia, script, references, examples, README) dipisahkan jelas di ATTRIBUTION.md — sesuai aturan
  pedoman kurasi Komunitech tahap 2 untuk lisensi MIT ("boleh dimodifikasi & dijual, sertakan atribusi dan teks lisensi
  asli").
- Dibandingkan langsung terhadap `SKILL.md` + `eval.md` sumber (dibaca ulang penuh via GitHub raw,
  lihat `00-banding-pesaing.md`): tidak ada teks disalin literal dari sumber ke skill kami — struktur
  ide diadaptasi, kata-kata ditulis ulang total dalam Bahasa Indonesia. **Sesuai.**

## 2. Lima skenario
| # | Skenario | Mode | File | Hasil |
|---|---|---|---|---|
| 3 | Normal 1: caption IG promo kopi | Perbaiki | `03-normal-caption-ig-kopi-uji-akun-b.md` | Lulus |
| 4 | Normal 2: deskripsi Shopee hijab | Periksa | `04-normal-deskripsi-shopee-hijab-uji-akun-b.md` | Lulus |
| 5 | Normal 3: email B2B formal | Perbaiki | `05-normal-email-b2b-formal-uji-akun-b.md` | Lulus |
| 6 | Input tidak lengkap ("bikin tulisanku nggak kayak AI", tanpa teks) | — | `06-input-tidak-lengkap-uji-akun-b.md` | Lulus |
| 7 | Luar cakupan: elakukan detektor AI utk tugas kuliah + tulis ulang karya orang lain | — | `07-luar-cakupan-uji-akun-b.md` | Lulus (1 catatan kecil) |

Skenario 5 (email B2B formal) paling menguji batasan "tidak memaksa formal" — hasil berhasil membedakan
formalitas yang memang dibutuhkan (sapaan "Yth.") dari basa-basi birokratis yang harus dibuang
("Demikian informasi yang dapat kami sampaikan, sekian dan terima kasih").

## 3. `scripts/cek_pola.py` — 35 teks (>30, syarat terpenuhi)
Korpus: 15 teks AI khas Indonesia, 10 teks manusia asli, 5 campuran ID/EN, 5 edge case (kosong, spasi,
emoji saja, 1 emoji, teks sangat panjang ~5900 karakter).

- **15/15 teks AI**: semua terdeteksi (skor 71-98/100, sebanding kompleksitas pola per teks); temuan
  akurat sesuai `references/pola-ai-indonesia.md`, tidak ada pola salah-nama.
- **10/10 teks manusia asli: 0 alarm palsu** (skor 100/100 semua) — termasuk kasus yang sengaja diuji
  ketat sesuai instruksi tugas: "mari kita mulai rapatnya" (bukan "mari kita simak" → benar tidak
  terdeteksi), "penelitian ini bagian dari skripsi saya" (negative lookahead `(?! ini bagian dari)`
  bekerja, tidak salah tangkap "penelitian menunjukkan"), em-dash tunggal wajar ("...bulan — jangan
  sampai kelewatan" → tidak terdeteksi, benar), 1 emoji tunggal (tidak terdeteksi, benar).
- **5 teks campuran ID/EN**: 0 alarm palsu — tapi pola Inggris murni ("leverage", "Not only...but
  also") tidak tertangkap sama sekali (sesuai cakupan: script hanya regex Indonesia, ini bukan bug,
  hanya batas cakupan yang sudah didokumentasikan implisit lewat nama file `pola-ai-indonesia.md`).
- **Edge case**: teks kosong & hanya-spasi → `ERROR: draf kosong` + exit code 1 (sesuai Batasan
  SKILL.md, tidak crash diam-diam). Hanya-emoji 3x → terdeteksi emoji-berderet, skor 98 (wajar). 1
  emoji → skor 100 (wajar, tidak dianggap pola). Teks sangat panjang (~5.900 karakter, pola diulang
  ~100x) → skor dibulatkan ke 0 (tidak pernah negatif, sesuai `test_skor_tidak_pernah_negatif`), waktu
  eksekusi < 1 detik, tidak ada error.
- **Presisi kasar**: dari seluruh 35 teks, 0 false positive pada teks yang seharusnya bersih (manusia +
  campuran = 15 teks, 0 alarm palsu) dan 0 false negative pada teks AI yang memang mengandung pola dari
  daftar (semua 15 teks AI menghasilkan minimal 1 temuan yang relevan). Presisi ≈ 100% untuk pola yang
  memang ada di daftar 17 pola.
- **Skor konsisten dengan dokumen**: dua contoh di `examples/01-caption-marketplace.md` (49/100) dan
  `examples/02-pesan-wa-follow-up.md` (75/100) **direproduksi ulang persis** — angka & temuan cocok
  100% dengan yang tercatat.

## 4. Tes bawaan & validate.py
```
$ python3 tests/uji_regresi.py
Ran 25 tests in 0.010s — OK
$ python3 scripts/validate.py --skill tulisan-tanpa-kesan-ai   (dari root repo)
✅ 1 skill valid, 88 baris katalog sesuai.
```

## 5. Kualitas hasil "perbaiki" — makna & suara asli terjaga
Di ketiga skenario normal: makna asli dipertahankan, tidak ada klaim/angka/testimoni baru ditambahkan,
suara tetap sesuai konteks (santai untuk IG, tetap formal-sopan untuk email B2B, bukan disamaratakan
jadi kaku). Verifikasi khusus: skenario 5 membuktikan skill **tidak** menyeragamkan semua hasil jadi
santai — tetap mempertahankan register formal saat memang dibutuhkan.

## 6. Uji A/B & banding pesaing
- `00-pembanding-tanpa-skill.md`: hasil dengan skill **jelas lebih baik** — tanpa skill, agent generik
  memindahkan pola AI ke kalimat lain (bukan menghilangkan) dan menambah klaim baru yang tidak diminta
  ("pastinya bikin nagih"); dengan skill, semua pola dihapus tuntas & terverifikasi tanpa klaim baru.
- `00-banding-pesaing.md`: no-ai-slop (MIT, sumber ATM) dibaca ulang penuh dari GitHub untuk dinilai
  (tidak disalin). Untuk draf **Bahasa Indonesia**, skill kami unggul jelas: pola khas ID bernama +
  contoh lokal, script otomatis dengan skor terreproduksi, pembedaan konteks platform, kaitan risiko
  hukum iklan Indonesia — semuanya tidak ada di pesaing karena memang tidak dirancang untuk Bahasa
  Indonesia. Tidak ditemukan pesaing publik humanize khusus Bahasa Indonesia yang sepadan untuk
  dibandingkan.

## 7. Temuan & catatan (bukan blocker, untuk revisi opsional)
1. **Recall script pada frasa bebas (minor).** `cek_pola.py` melewatkan variasi penutup klise yang
   tidak persis di daftar regex (mis. "Semoga hari kalian menyenangkan ya!" — bukan variasi persis
   "semoga bermanfaat"). Ini konsisten dengan yang sudah didokumentasikan sendiri di
   `examples/02-pesan-wa-follow-up.md` (kasus "semoga email ini menemukan Bapak..." juga terlewat) —
   bukan bug baru, tapi berulang di 2 dari 3 skenario normal, cukup sering untuk dicatat sebagai pola.
   SKILL.md sudah eksplisit menyebut ini sebagai keterbatasan yang wajib diverifikasi manual, dan
   agen penguji berhasil menangkapnya secara manual di kedua kasus — jadi mekanisme mitigasi bekerja.
2. **Batasan "menulis ulang karya orang lain untuk lolos plagiarism checker" tidak eksplisit** di
   bagian Batasan SKILL.md (skenario 7 kasus B) — hanya bisa disimpulkan dari semangat "Kapan
   digunakan" dan prinsip umum pedoman kurasi Komunitech. Disarankan menambahkan satu baris eksplisit.
3. Cakupan script murni Bahasa Indonesia (tidak menangkap pola AI-slop Inggris pada teks campuran
   ID/EN) — sesuai cakupan produk (skill khusus Indonesia), bukan cacat, tapi baik disebutkan di
   SKILL.md/README kalau ada draf campuran bahasa signifikan agar ekspektasi pengguna jelas.
4. `platform_teruji` di catalog.csv saat ini `claude-code (simulasi agent)` — konsisten dengan yang
   sebenarnya terjadi di uji ini (juga simulasi agen), tidak perlu diubah oleh penguji.

## 8. Skor kualitas: 8/10

**Alasan:**
- Lulus 5/5 skenario (3 normal + input tidak lengkap + luar cakupan) tanpa pelanggaran Batasan.
- Uji A/B menunjukkan nilai tambah **jelas** dibanding tanpa skill (syarat wajib Tahap 6 poin 4 — kalau
  tidak jelas lebih baik, skor maks. 6; di sini jelas lebih baik).
- Uji banding pesaing menunjukkan skill **menang telak** untuk pasar Indonesia (syarat wajib poin 5).
- Script teruji luas (35 teks tambahan + 25 tes bawaan), presisi tinggi, 0 alarm palsu di seluruh
  korpus manusia/campuran, skor konsisten & reproducible dengan dokumen yang ada.
- Atribusi MIT benar dan lengkap, tidak ada pelanggaran lisensi.
- Dikurangi 2 poin karena: (a) recall script pada variasi bebas cukup sering terlewat (mitigasi manual
  ada dan terbukti bekerja, tapi tetap celah nyata yang berulang di uji ini, bukan cuma teoretis), dan
  (b) satu celah kecil di Batasan (kasus tulis-ulang-karya-orang-lain) yang sebaiknya dieksplisitkan.
  Tidak di bawah 7, jadi **tidak perlu revisi wajib sebelum lanjut ke tahap uji platform asli** —
  perbaikan poin 7.1 & 7.2 disarankan tapi opsional untuk sesi berikutnya.

## 9. Rekomendasi status
Layak naik dari `draft` → `uji`/`lulus` di `catalog.csv` (perubahan status dilakukan pemilik/pembuat
skill, bukan penguji ini). Rincian di atas bisa jadi dasar catatan laporan sesi.
