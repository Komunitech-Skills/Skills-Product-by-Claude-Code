---
name: presentasi-instan
description: Membuat presentasi/pitch deck Indonesia sebagai satu file HTML mandiri yang bisa dibuka di browser laptop/HP tanpa internet dan tanpa PowerPoint/Canva, lalu dicetak jadi PDF lewat menu Print. Gunakan saat pengguna minta dibuatkan presentasi, slide, pitch deck, materi presentasi, proposal presentasi, company profile, atau presentation/slides untuk investor, bank/KUR, klien B2B, reseller, atasan, atau pelatihan karyawan.
---

# Presentasi Instan

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya (kecuali di kanal chat, lihat langkah 7), dan simpan hasil di folder kerja yang disepakati (bukan /tmp); jangan menyebut nama skill atau alat internal ke pengguna (lihat langkah 7).

Mengubah poin-poin dari pengguna menjadi presentasi HTML siap pakai — satu file,
tanpa instalasi, tanpa internet setelah file jadi, langsung bisa dibuka di browser
laptop atau HP dan dicetak ke PDF.

## Kapan digunakan
- Pengguna minta dibuatkan presentasi/pitch deck/slide untuk investor, bank/KUR, klien
  B2B, reseller, atasan/owner, profil perusahaan, atau pelatihan karyawan.
- Pengguna sudah punya poin-poin/notes dan ingin diubah jadi slide rapi.
- Pengguna hanya punya topik dan minta dibuatkan kerangka + isi presentasinya.

## Kapan TIDAK digunakan
- Pengguna secara eksplisit minta file `.pptx` (PowerPoint) — skill ini menghasilkan
  HTML, jelaskan itu ke pengguna; jika environment punya skill/alat pembuat `.pptx`
  terpisah, arahkan ke sana.
- Menghitung HPP, harga jual, PPN, laporan keuangan, cicilan/rasio KUR, atau rekap CSV
  penjualan dari nol → pakai skill `hitung-hpp`, `harga-jual-marketplace`, `hitung-ppn`,
  `laporan-keuangan-emkm`, `pengajuan-kur`, atau `rekap-penjualan-csv` lebih dulu, lalu
  hasil angkanya **dimasukkan** ke presentasi ini (lihat bagian "Angka pinjaman/cicilan"
  dan "Integrasi dengan skill lain").
- Menulis surat penawaran formal satu halaman (bukan slide) → pakai skill
  `surat-penawaran-harga`.
- Menulis perjanjian/kontrak kerja sama → pakai skill `perjanjian-sederhana`.

## Input

| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Untuk apa presentasi ini (konteks/tujuan) | Ya | — (tanyakan) |
| Isi/poin-poin yang mau dimasukkan | Tidak | Buat kerangka + isi contoh berlabel jelas "contoh — sesuaikan", minta pengguna melengkapi |
| Perkiraan jumlah slide / durasi presentasi | Tidak | Ikuti patokan per konteks di `references/aturan-desain.md` #8 |
| Warna/logo brand | Tidak | Pakai salah satu palet netral di `references/aturan-desain.md` #5 |
| Rencana pemakaian: ditampilkan di layar saja / dicetak ke PDF / dua-duanya | Tidak | Buat untuk dua-duanya (mode cetak selalu disertakan) |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan
singkat bernomor (maksimal 5 pertanyaan total, gabungkan baris di atas menjadi
pertanyaan yang wajar, jangan tanya satu-satu). Contoh gabungan pertanyaan:

1. Presentasi ini untuk apa? (mis. pitch ke investor, proposal ke perusahaan lain,
   pengajuan KUR/bank, laporan bulanan ke atasan, profil perusahaan, penawaran ke
   reseller, atau materi pelatihan karyawan)
2. Boleh kirim poin-poin isinya, atau saya buatkan dulu kerangkanya dari topik saja?
3. Kira-kira berapa slide / berapa lama presentasinya?
4. Ada warna atau logo brand yang mau dipakai?
5. Nanti dipakai untuk ditampilkan di layar, dicetak jadi PDF, atau dua-duanya?

(Kalau mau cepat, cukup jawab nomor 1 saja — sisanya saya pakai default yang wajar.)

Jika pengguna terlihat ingin cepat ("buatkan aja", "yang penting jadi"), langsung
pakai default masuk akal di atas dan sebutkan asumsi yang dipakai di ringkasan akhir.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

1. **Tentukan jenis presentasi** dari jawaban pengguna, lalu baca template yang sesuai
   di `templates/`: `pitch-investor.md`, `proposal-b2b.md`, `pengajuan-kur.md`,
   `laporan-bulanan.md`, `profil-perusahaan.md`, `produk-ke-reseller.md`, atau
   `pelatihan-karyawan.md`. Jika tidak ada yang cocok persis, gabungkan struktur yang
   paling dekat lalu sesuaikan dengan konteks pengguna.
   - **Jika pengguna mengirim file CSV/Excel data penjualan**, langkah wajib (bukan
     opsional): rekap dulu datanya dengan skill `rekap-penjualan-csv` (bila terpasang)
     atau `scripts/rekap.py`-nya, baru masukkan hasilnya ke slide. Jangan menjumlahkan
     atau merata-rata angka dari CSV secara manual/kira-kira.
   - **Jika presentasinya untuk pengajuan KUR/kredit** (`templates/pengajuan-kur.md`),
     lihat aturan wajib di bagian "Angka pinjaman/cicilan (khusus KUR)" di bawah sebelum
     mengisi slide cicilan/rasio/agunan.
2. **Susun outline slide** mengikuti struktur di template terpilih, isi dengan konten
   dari pengguna. Jika pengguna hanya memberi topik, buat isi contoh yang masuk akal
   untuk konteks itu dan **tandai jelas** bagian yang perlu diisi pengguna (mis.
   `[isi nama perusahaan Anda]`).
   **Klaim di slide hanya dari fakta pengguna.** Kalimat tentang kinerja, kecepatan, tren,
   reputasi, atau pertumbuhan (mis. "pelanggan bertambah tiap tahun", "selesai 1–2 hari",
   "repeat order rutin") yang tidak diberikan pengguna jangan ditulis sebagai fakta; tulis
   `[isi: ...]` (mis. `[isi: lama pengerjaan]`) atau hapus.
3. **Baca `references/aturan-desain.md`** dan terapkan: batas kata per slide, kontras
   warna, tumpukan font aman, palet warna, format Rupiah, jumlah slide wajar.
4. **Baca `references/kerangka-html.md`** dan gunakan kerangkanya sebagai dasar file
   HTML tunggal. Isi variabel warna/font sesuai palet yang dipilih (langkah 3), isi
   tiap `<section class="slide">` dengan konten dari langkah 2.
   - Semua CSS & JavaScript tetap inline di file yang sama — **jangan** menambahkan
     `<link>`/`<script src>` ke internet.
   - Jika ada logo/gambar dari pengguna, sisipkan sebagai `base64` (lihat
     `kerangka-html.md` aturan #3).
   - Format setiap angka uang sebagai `Rp 1.250.000` (lihat `aturan-desain.md` #6).
5. **Simpan sebagai satu file `.html`** (nama file singkat, tanpa spasi, mis.
   `pitch-usahaku.html`).
6. **Validasi otomatis**, jalankan (Windows: ganti `python3` dengan `python` atau `py`):
   ```
   python3 <folder-skill-ini>/scripts/validasi_html.py <file.html>
   ```
   - Jika ada **ERROR** (mis. masih ada rujukan internet, atau `@media print` hilang),
     perbaiki HTML lalu jalankan ulang sampai lulus.
   - Jika ada **peringatan** (mis. slide terlalu padat teks), pertimbangkan
     memperbaikinya; boleh dikirim ke pengguna apa adanya jika pengguna memang minta
     konten sepadat itu, tapi sebutkan peringatannya dalam bahasa awam.
   - Jika Python tidak bisa dijalankan di lingkungan pengguna, periksa manual: pastikan
     tidak ada teks `http://`/`https://` di dalam file, ada blok `@media print`, dan
     tidak ada slide yang terlihat penuh sesak — lalu beri tahu pengguna bahwa
     pengecekan otomatis dilewati.
7. **Sampaikan hasil ke pengguna** mengikuti format output di bawah.
   - **Berkas hasil di kanal chat (Telegram/WhatsApp):** pengguna di HP tidak bisa membuka folder di komputer agent. Setelah file `.html` jadi dan lolos `validasi_html.py`, **WAJIB lampirkan/kirim file `.html` itu sebagai dokumen** bila kanal bisa mengirim file. Bila tidak bisa, **jangan menyebut jalur/folder kerja atau nama file di komputer**; ringkas isi slide per slide di chat (satu baris per slide) dan cukup tawarkan "balas 'kirim file'". Jangan menawarkan "kirim file" sebagai pengganti mencoba melampirkan.
   - **Tampilan di chat:** jangan pakai tabel Markdown; ringkasan slide ditulis sebagai daftar bernomor.
   - **Bahasa ke pengguna:** tulis hasil cek `validasi_html.py` dengan kalimat awam (mis. "file bisa dibuka tanpa internet dan siap dicetak jadi PDF"); jangan memakai kata "LULUS"/"validasi". **Jangan menyebut nama skill atau alat internal** (mis. `rekap-penjualan-csv`, `pengajuan-kur`, "skill laporan keuangan") — cukup sebut hasilnya ("rekap penjualan", "simulasi cicilan KUR"). Bila perlu saran, sebut kebutuhannya, bukan nama skill-nya.

## Format output

```
Presentasi [judul] sudah jadi: [nama-file.html] ([jumlah] slide)

Cara pakai:
- Buka file-nya dua kali klik, atau tarik ke jendela browser (Chrome/Edge/Safari) — bisa dibuka di laptop maupun HP, tanpa internet.
- Navigasi: tombol panah kiri/kanan atau geser jari (di HP), atau klik tombol ‹ › di bawah layar. Kalau HP dipegang tegak, akan muncul pesan untuk memutar ke posisi mendatar (landscape) supaya teks terbaca.
- Mau edit teks langsung? Klik tombol "✏️ Edit" di pojok kanan bawah, ubah teksnya, klik "✔ Selesai edit", lalu simpan dengan Ctrl+S/Cmd+S ("Webpage, HTML only") — **hanya bisa di laptop/komputer**; di HP, minta saya (AI) yang mengubah teksnya lalu kirim ulang filenya.
- Cetak jadi PDF: buka file → Ctrl+P (Windows) / Cmd+P (Mac) → tujuan "Simpan sebagai PDF"/"Save as PDF" → margin "Tidak ada"/"None" → centang "Grafis latar"/"Background graphics" (ukuran halaman sudah otomatis pas, tidak perlu pilih kertas/orientasi manual).

Asumsi yang dipakai (kalau ada): [...]
Bagian yang masih perlu Anda lengkapi (kalau ada): [...]
Catatan kelayakan pinjaman (khusus KUR, kalau ada, TIDAK ditaruh di slide): [mis. "rasio cicilan/laba 46,6% = kategori BERAT menurut simulasi KUR; plafon yang lebih aman sekitar Rp ..."]
Sudah dicek: [bahasa awam, mis. "file bisa dibuka tanpa internet dan siap dicetak jadi PDF"; bila ada peringatan, sebutkan apa yang perlu diperbaiki, mis. "slide 4 terlalu padat, sebaiknya dipecah jadi dua"]
```

Di kanal chat (Telegram/WhatsApp): kirim file `.html`-nya sebagai dokumen bersama pesan ini (langkah 7); baris "Presentasi ... sudah jadi" cukup memuat judul dan jumlah slide, tanpa jalur/folder komputer.

## Contoh

**Input pengguna:** "Buatkan presentasi untuk pengajuan KUR ke BRI. Usaha saya warung
sembako, sudah jalan 4 tahun, omzet rata-rata Rp 35.000.000/bulan. Mau pinjam Rp
50.000.000 untuk nambah stok dan gerobak keliling."

**Output (ringkas):**
```
Presentasi Pengajuan KUR - Warung Sembako sudah jadi: pengajuan-kur-warung.html (10 slide)

Cara pakai:
- Buka file-nya dua kali klik, bisa dibuka di laptop maupun HP, tanpa internet.
- Cetak jadi PDF: Ctrl+P / Cmd+P → Simpan sebagai PDF → margin Tidak ada → centang Grafis latar.

Asumsi yang dipakai: warna palet "Hijau Amanah" (belum ada warna brand disebutkan), 
jumlah karyawan & alamat usaha ditulis sebagai [isi data Anda] karena belum diberikan.

Perlu Anda lengkapi: jumlah karyawan, alamat usaha, dan legalitas usaha (NIB/NPWP jika ada).

Catatan: presentasi ini pelengkap, bukan pengganti formulir resmi KUR — cek syarat 
terbaru ke bank/penyalur KUR yang dituju.

Sudah dicek: file bisa dibuka tanpa internet dan siap dicetak jadi PDF.
```

## Angka pinjaman/cicilan (khusus KUR/kredit) — WAJIB, jangan hitung kira-kira

Presentasi ini **tidak boleh menghitung sendiri** cicilan, rasio cicilan-terhadap-laba,
atau kelayakan plafon/agunan — itu adalah pekerjaan skill `pengajuan-kur`:
- Jika skill `pengajuan-kur` **terpasang** di environment ini: panggil skill tersebut
  (atau jalankan `scripts/simulasi_kur.py` miliknya) dengan plafon, tenor, dan data
  laba/cicilan lain dari pengguna. Masukkan **nominal cicilan dan rasio cicilan/laba
  (angka)** ke slide "Jumlah pinjaman & rencana pengembalian" di
  `templates/pengajuan-kur.md`. **Jangan** menaruh label penilaian kelayakan seperti
  "BERAT"/"AMAN" dari `pengajuan-kur` di slide yang akan dilihat pihak bank — itu
  penilaian internal untuk pengguna, bukan untuk presentasi ke bank. Sampaikan label
  kelayakan itu (mis. "rasio 46,6% = kategori BERAT menurut simulasi KUR") beserta perkiraan plafon yang lebih
  aman ke **pengguna** di ringkasan akhir, supaya dipertimbangkan sebelum diajukan.
- Jika skill `pengajuan-kur` **tidak terpasang**: jangan mengarang atau menghitung
  kira-kira di kepala. Tulis `[isi]` pada angka cicilan/rasio, dan tambahkan catatan di
  slide (font kecil) atau di ringkasan akhir: "Cicilan & rasio kemampuan bayar perlu
  dihitung dengan simulasi KUR resmi (mis. dari bank penyalur) sebelum dipakai ke bank."
- Angka omzet/laba yang jadi dasar rasio (lihat bagian CSV di bawah) juga wajib berasal
  dari data pengguna atau hasil rekap, bukan perkiraan.

## Integrasi dengan skill lain

Jika pengguna sudah punya hasil dari skill lain di library ini, atau data mentah yang
perlu dihitung, **masukkan hasilnya ke slide, jangan menghitung ulang manual/kira-kira**:
- **`rekap-penjualan-csv`** → **wajib** dipakai (langkah 1) bila pengguna mengirim file
  CSV/Excel data penjualan, untuk angka omzet, produk terlaris, tren penjualan pada
  slide "Traksi" (pitch investor), "Omzet & histori penjualan" (KUR), atau "Rincian
  kinerja" (laporan bulanan). Jika skill itu tidak terpasang, hitung dengan
  `scripts/rekap.py` miliknya lewat Python secara eksplisit (bukan dijumlah di kepala).
- **`pengajuan-kur`** → **wajib** dipakai untuk cicilan/rasio/cek plafon-agunan pada
  template `pengajuan-kur.md` (lihat bagian di atas).
- **`laporan-keuangan-emkm`** → ringkasan laba-rugi untuk slide "Proyeksi keuangan"
  atau "Capaian vs target".
- **`hitung-hpp`** → dasar perhitungan margin untuk slide "Perkiraan margin keuntungan"
  di template `produk-ke-reseller.md`.

## Checklist sebelum mengirim hasil
- [ ] Semua angka Rupiah format `Rp 1.250.000`, tidak ada angka yang dikarang.
- [ ] Angka cicilan/rasio KUR berasal dari skill `pengajuan-kur` (atau ditandai `[isi]` + catatan bila skill itu tidak terpasang), bukan hitungan kira-kira.
- [ ] Angka dari CSV penjualan berasal dari `rekap-penjualan-csv`/`scripts/rekap.py`, bukan dijumlah manual.
- [ ] Tidak ada `<link>`/`<script src>` ke internet, tidak ada gambar dengan path lokal — sudah dicek `validasi_html.py`.
- [ ] Ada `@page { size: 1920px 1080px; margin: 0; }` dan blok `@media print`, sudah dicoba cetak PDF-nya tidak terpotong.
- [ ] Tidak ada klaim tanpa dasar (halal, BPOM, "terlaris", "pelanggan bertambah", "selesai 1–2 hari") kecuali diberikan pengguna; selain itu `[isi: ...]`.
- [ ] Bagian yang belum terisi ditandai jelas, bukan dikarang seolah-olah data asli.
- [ ] Kanal chat: file `.html` dilampirkan sebagai dokumen; bila tidak bisa, tidak ada jalur/folder disebut, isi slide diringkas per slide, dan hanya ditawarkan "balas 'kirim file'"; tidak ada tabel Markdown.
- [ ] Balasan memakai bahasa awam: tanpa kata "LULUS"/"validasi" dan tanpa nama skill/alat internal.

## Batasan & penanganan error
- **Bukan pengganti PowerPoint/Canva penuh** — tidak ada transisi 3D, tidak ada
  animasi kompleks; fokus pada kerapian, keterbacaan, dan kemudahan pakai tanpa
  instalasi. Jika pengguna butuh fitur PowerPoint spesifik (mis. edit di Microsoft
  Office, mode presenter dua layar bawaan PowerPoint), jelaskan keterbatasan ini.
- **File gambar/logo besar** membuat ukuran HTML membesar (karena disisipkan base64).
  Jika pengguna memberi banyak foto beresolusi tinggi, sarankan mengecilkan ukurannya
  dulu atau batasi ke logo + 1-2 foto produk penting saja.
- **Jika Python tidak tersedia** untuk menjalankan `validasi_html.py`, tetap lanjutkan
  memberi file presentasi ke pengguna, tapi sebutkan bahwa pengecekan otomatis
  dilewati dan lakukan pengecekan manual sesuai langkah 6.
- **Di luar cakupan:** presentasi bahasa asing selain Indonesia (bisa dibuat jika
  pengguna minta eksplisit, tapi bukan default), pembuatan video, atau publikasi ke
  hosting/link publik — skill ini murni menghasilkan file lokal.
