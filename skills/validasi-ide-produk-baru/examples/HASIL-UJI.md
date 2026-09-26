# Hasil Uji Independen — validasi-ide-produk-baru v1.0.0

**Penguji:** Akun B (agen terpisah, hanya membaca folder `skills/validasi-ide-produk-baru/`, tidak membuat skill ini).
**Tanggal:** 2026-09-26.

## 1. Ringkasan aktivitas uji
- Dibaca penuh: `SKILL.md`, `README.md`, `ATTRIBUTION.md`, `LICENSE-APACHE`, `templates/`, `references/`, `scripts/hitung_validasi.py`, `examples/01`–`02` (contoh dari pembuat).
- 5 skenario baru dijalankan (bukan menimpa 01/02): 3 normal (`03` sambal botolan, `04` cuci AC panggilan Bekasi, `05` kursus Inggris anak online), 1 input tidak lengkap (`06`, "mau jual kue"), 1 luar cakupan (`07`, skema member-get-member berjanji untung 20%/bulan + riset pasar nasional).
- `scripts/hitung_validasi.py` diuji dengan 17 kombinasi data: normal, tepat di ambang 15% dan 8%, nol, negatif, ditawari 0, preorder>ditawari, harga 0, format Rupiah bertitik ribuan, non-numerik, JSON rusak/tidak ada, ambang kustom terbalik, hpp≥harga, preorder desimal. Semua hasil diverifikasi independen dengan `Decimal` manual — cocok, **kecuali satu bug (lihat §3)**.
- Uji A/B tanpa-skill vs dengan-skill: `examples/00-pembanding-tanpa-skill.md`.
- Uji banding pesaing (`define-hypothesis` dari `product-on-purpose/pm-skills`, dibaca-nilai saja, tidak disalin): `examples/00-banding-pesaing.md`.
- `python3 scripts/validate.py --skill validasi-ide-produk-baru` → **lolos** ("1 skill valid, 86 baris katalog sesuai"). (Catatan: `python3 scripts/validate.py` tanpa filter menampilkan 1 masalah tak terkait — `analisis-rasio-keuangan-usaha` belum ada di catalog.csv — di luar cakupan skill yang diuji di sini, tidak diubah.)
- `bash scripts/uji_openclaw.sh` **sengaja tidak dijalankan** sesuai instruksi tugas.

## 2. Atribusi Apache-2.0 (audit)
- `LICENSE-APACHE` berisi teks Apache License 2.0 lengkap (189 baris, awal & format sesuai teks resmi) — diverifikasi cocok dengan `LICENSE` di repo sumber `product-on-purpose/pm-skills` (dicek langsung via clone).
- Repo sumber dikonfirmasi **tidak** punya file `NOTICE`/`NOTICE.txt` — klaim di `ATTRIBUTION.md` benar.
- Klaim "file telah diubah, tidak ada teks sumber disalin verbatim" — diverifikasi masuk akal: dibandingkan struktur `define-hypothesis/SKILL.md` (format "We believe that... for... will...", bahasa Inggris, istilah A/B test/statistical requirements/sample size, tim produk software) dengan `SKILL.md` skill ini (bahasa Indonesia penuh, metode uji WA/IG/marketplace/warung, ambang 15%/8%, tidak ada satu kalimat yang sama). **Tidak ditemukan teks yang disalin.**
- Commit hash yang dicatat di `ATTRIBUTION.md` (`1cef1a9eae10017389863d51e289e0ae41e17fcb`) — panjang hash 41 karakter, satu karakter lebih dari hash git SHA-1 standar (40 karakter); kemungkinan salah ketik satu digit saat mencatat. Tidak memengaruhi keabsahan audit lisensi (repo & isi sudah diverifikasi langsung), tapi sebaiknya diperbaiki demi presisi catatan.
- **Kesimpulan atribusi: lolos**, satu catatan kecil (panjang hash) untuk diperbaiki pembuat.

## 3. Temuan skrip (`hitung_validasi.py`) — 1 bug, tingkat sedang
**Bug: parsing harga/hpp/biaya-uji format Rupiah Indonesia (titik sebagai pemisah ribuan) salah tanpa peringatan.**

Seluruh `SKILL.md`, `README.md`, dan `examples/01`–`05` menampilkan harga dengan format Indonesia bertitik ribuan (`Rp45.000`, `Rp28.000`, dst.) dan `templates/pesan-uji-murah.md` mengajarkan pengguna menulis harga dengan format sama. Namun skrip memakai `Decimal(str(nilai))` langsung, yang membaca titik sebagai **titik desimal**, bukan pemisah ribuan:

```
$ python3 scripts/hitung_validasi.py --ditawari 20 --preorder 4 --harga "25.000" --hpp "12.000"
...
Margin per unit      : Rp13  (Rp25 - Rp12)   # seharusnya Rp13.000
```
Untuk angka 3-digit-desimal-persis ("25.000", "150.000", dst — pola paling umum untuk harga UMKM di bawah Rp1 juta), hasilnya **diam-diam salah 1000x lipat**, bukan error. Untuk angka dengan >1 titik ("1.234.567") skrip memang menolak dengan pesan error yang jelas — jadi perilakunya **tidak konsisten**: kadang gagal jelas, kadang salah senyap. Ini berisiko tinggi karena target skill adalah "orang awam teknologi" yang wajar mengetik harga dengan format lokal ini, dan SKILL.md sendiri menampilkannya begitu di semua contoh perintah CLI.

**Dampak:** kalau agent (atau pengguna yang menjalankan skrip manual) memasukkan harga dengan titik ribuan, perhitungan margin/balik modal jadi salah tanpa peringatan apa pun — bertentangan dengan prinsip CLAUDE.md "Reliable: angka dihitung (bukan dikira)".

**Saran perbaikan (untuk pembuat, bukan dikerjakan penguji):** normalisasi input harga/hpp/biaya-uji dengan menghapus titik ribuan sebelum `Decimal()` (mis. deteksi pola `\d{1,3}(\.\d{3})+$` → hapus titik; atau lebih aman, minta strip eksplisit lalu re-parse; jangan izinkan koma desimal & titik ribuan bercampur tanpa aturan jelas), lalu tambahkan kasus uji baru untuk ini.

**Temuan minor kedua (bukan bug, catatan kualitas):** `--preorder 3.5` diterima tanpa validasi meski jumlah orang seharusnya bilangan bulat non-negatif; script tetap menghasilkan "Pre-order/beli: 3.5" yang tidak masuk akal secara semantik (tidak ada "setengah orang pre-order"). Dampak rendah (pengguna awam kecil kemungkinan mengetik desimal untuk jumlah orang), tapi validasi bilangan bulat untuk `--ditawari`/`--preorder` akan menutup celah ini.

Semua kasus lain (batas 15%/8% tepat, nol, negatif, ditawari 0, preorder>ditawari, harga 0, JSON rusak/hilang, ambang terbalik, hpp≥harga, sampel <20) menghasilkan pesan error/peringatan yang jelas dan benar, sesuai `Batasan & Penanganan Error` di `SKILL.md`.

## 4. Kriteria lulus/gagal & template pesan
- Kriteria (Langkah 3 SKILL.md) ditetapkan **sebelum** uji dijalankan di setiap skenario yang disimulasikan, sesuai instruksi — tidak ada penggeseran target setelah lihat hasil.
- Keputusan LANJUT/UBAH/HENTIKAN pada 5 skenario **konsisten dengan angka**: `03` LULUS→LANJUT (16,0%≥15%), `04` LULUS BERSYARAT→UBAH dengan catatan sampel kecil (11,1%, ditawari<20), `05` GAGAL→HENTIKAN default (6,0%<8%) — dengan temuan proses penting: SKILL.md membolehkan ambang diturunkan ke 10%/5% untuk produk harga tinggi (Rp300rb kursus termasuk kategori ini), yang bila dipakai mengubah hasil jadi LULUS BERSYARAT (6,0%>5%). Ini **bukan bug**, tapi celah kejelasan proses: agen wajib menyampaikan kedua kemungkinan ambang ke pengguna sebelum vonis, dan teks SKILL.md sudah melarang penyesuaian diam-diam — jadi ini catatan kewaspadaan implementasi, bukan pelanggaran instruksi tertulis.
- Template pesan (`templates/pesan-uji-murah.md`) diperiksa satu per satu: **tidak ada** klaim menyesatkan (tidak ada "gratis ongkir seumur hidup", tidak ada urgensi palsu), semua penawaran pre-order jujur menyatakan "PO/estimasi kirim X hari" dan "kuota terbatas untuk batch percobaan" (bukan klaim stok habis palsu). Namun **tidak ada template atau kalimat eksplisit soal opsi batal/refund** pre-order di keenam template — ini bertentangan dengan syarat tugas ("ada opsi batal/refund"), dan patut jadi masukan revisi: pengguna yang mem-broadcast pre-order idealnya menyebut sejak awal apa yang terjadi kalau ingin batal (mis. "boleh batal sebelum diproduksi, uang kembali penuh"), bukan cuma tenggat konfirmasi.
- Template "tanya alasan tidak beli" (#6) sopan dan tidak memaksa — baik untuk kualitas data alasan penolakan.

## 5. Kualitas isi lain
- SKILL.md terstruktur jelas, < 300 baris (128 baris), sesuai Tahap 5.
- Batasan domain sensitif (skema piramida/investasi tanpa izin/klaim medis) ditangani tegas dan benar pada skenario `07`.
- Format Output (7 poin) diikuti konsisten pada `examples/01`, `02`, dan simulasi `03`–`05`.
- README.md memenuhi materi jualan Tahap 8 (judul, manfaat, cocok untuk siapa, sebelum/sesudah, instalasi, FAQ 3 pertanyaan) — dicek, lengkap.

## 6. Skor kualitas
**Skor: 7,5/10**

**Alasan:**
- Konten prosedural, template, dan proses hipotesis→kriteria→uji→keputusan kuat, konsisten, dan berbeda telak dari sumber (lolos uji A/B jelas lebih baik dari tanpa-skill, dan tidak kalah dari pesaing — jadi tidak terkena batas skor maks. 6 di kedua uji wajib).
- **Ditahan dari skor lebih tinggi** oleh: (a) bug parsing format Rupiah bertitik ribuan yang **diam-diam salah** — bertentangan langsung dengan prinsip "Reliable" CLAUDE.md dan berisiko tinggi karena polanya sangat umum dipakai target pengguna; (b) template pre-order tidak menyebut opsi batal/refund secara eksplisit di mana pun.
- Kedua temuan **dapat diperbaiki cepat** (perbaikan skrip + tambah satu baris di template) tanpa merombak skill — sesuai CLAUDE.md Tahap 6 poin 7 ("Di bawah 7 → revisi, jangan rilis"), skor 7,5 berada **di atas** ambang revisi wajib, namun kedua temuan tetap direkomendasikan diperbaiki sebelum naik ke status `uji`/`lulus` karena menyentuh keandalan angka dan kejujuran penawaran — dua hal inti yang dituntut CLAUDE.md.

## 7. Rekomendasi ke pembuat/pemilik
1. **Wajib sebelum lulus:** perbaiki parsing harga/hpp/biaya-uji di `hitung_validasi.py` agar format Rupiah bertitik ribuan (`25.000`, `150.000`, dst.) ditangani benar, konsisten (bukan kadang error kadang salah senyap); tambah kasus uji untuk format ini.
2. **Wajib sebelum lulus:** tambahkan satu kalimat opsi batal/refund pre-order di minimal template #1 dan #4 (`templates/pesan-uji-murah.md`).
3. **Disarankan:** validasi `--ditawari`/`--preorder` sebagai bilangan bulat non-negatif (tolak desimal dengan pesan jelas).
4. **Disarankan (kecil):** perbaiki panjang commit hash di `ATTRIBUTION.md` (41→40 karakter, sesuai format SHA-1 git).
5. **Disarankan (kejelasan proses, bukan bug):** tambah satu kalimat di SKILL.md Langkah 3 yang menegaskan agen harus menyampaikan **kedua** hasil (ambang default vs ambang harga-tinggi/impulsif) ke pengguna saat hasil berada di zona yang bisa berubah klasifikasi, bukan hanya melaporkan satu ambang.

Setelah item 1–2 diperbaiki dan diuji ulang oleh penguji independen (sesuai CLAUDE.md Tahap 6 poin 7), skill ini layak lanjut ke uji platform asli.
