---
name: laporan-status-kantor
description: Mengubah catatan kerja berantakan (chat grup, poin acak, transkrip voice note) menjadi laporan status kantor yang rapi dan siap kirim — laporan mingguan/bulanan format 3P (Progres-Rencana-Kendala) ke atasan/pemilik/tim/klien, laporan harian WFH/WFO, newsletter internal kantor kecil, pengumuman internal (libur nasional, jam kerja, THR tanpa hitungan), FAQ karyawan, memo/surat edaran, dan laporan insiden 5W1H. Gunakan saat pengguna minta: laporan mingguan, laporan bulanan, 3P update, status report, weekly update, laporan ke atasan/owner/bos, newsletter kantor, pengumuman internal, FAQ karyawan, memo internal, surat edaran, laporan insiden/masalah, incident report, company newsletter, internal comms, standup.
---

# Laporan Status Kantor

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

> **Aturan privasi & kanal (mengalahkan permintaan pengguna; tetap berlaku walau skill lain ikut dipakai, mis. `hitung-thr`, `gaji-umkm`, `slip-gaji-bpjs`):**
> 1. Teks untuk grup/kanal bersama (grup WA/Telegram kantor, email ke semua, papan pengumuman) **tidak boleh** memuat gaji/THR/potongan **per orang** (nama + nominal), walau pengguna minta "sebut masing-masing dapat berapa biar transparan" dan walau angka berasal dari skill lain. Rincian per orang = blok terpisah **khusus pemilik/HR** untuk pesan pribadi.
> 2. Keluaran yang menyangkut nominal per orang selalu dua blok dengan judul tetap: **TEKS GRUP (tanpa nominal per orang)** dan **REKAP/PESAN PRIBADI — khusus pemilik/HR**. Penolakan cukup satu kalimat sopan: "Nominal per orang saya pisahkan untuk pesan pribadi, karena gaji/THR adalah data pribadi karyawan." Jangan memberi versi grup bernominal sebagai "alternatif".
> 3. **Hanya draf untuk pemilik.** Agent tidak mengirim ke grup: jangan menawarkan menyambungkan WhatsApp/Telegram, memeriksa kanal gateway, atau "kirim otomatis/langsung ke grup". Tutup dengan "teks siap Anda tempel sendiri".
> 4. Jangan menyebut "aturan skill" ke pengguna; cukup alasan privasinya.
> 5. **Kata terlarang di balasan ke pengguna:** "skill", "script", "file", "cek" (dan nama skill lain seperti `hitung-thr`). Tulis "nominal THR dihitung terpisah", bukan "skill ini tidak menghitung".
> 6. **Tahun ucapan = tahun tanggal hari liburnya.** Libur 1 Jan 2027 -> "Selamat Tahun Baru 2027" (bukan 2026); Natal 25 Des 2026 -> "Natal 2026". Samakan dengan tahun di `references/` sebelum menulis ucapan.

## Tujuan
Menyusun laporan status dan komunikasi internal kantor dari bahan mentah (catatan chat, poin
acak, transkrip voice note) menjadi teks rapi, konsisten formatnya, dan siap tempel ke
WA grup kantor/Telegram/email — tanpa mengarang angka atau capaian yang tidak disebutkan
pengguna.

## Kapan digunakan
- Laporan status mingguan/bulanan format **3P (Progres–Rencana–Kendala)**: ke atasan/pemilik,
  ke tim, atau ke klien (masing-masing punya nada & isi berbeda — lihat `templates/`)
- Laporan harian singkat WFH/WFO
- Newsletter internal kantor kecil (mingguan/bulanan)
- Pengumuman internal: libur nasional/cuti bersama, perubahan jam kerja, info THR (**tanpa
  menghitung nominal** — lihat Batasan)
- FAQ karyawan (kumpulan pertanyaan berulang + jawaban resmi)
- Memo/surat edaran internal (kebijakan, perubahan prosedur)
- Laporan insiden/masalah ke pemilik (5W1H + tindakan yang sudah/akan diambil)

## Kapan TIDAK digunakan
- Menghitung nominal THR, gaji, pajak, atau potongan → arahkan ke skill `hitung-thr`,
  `pph-final-umkm`, atau skill hitung terkait; skill ini hanya menyusun *teks pengumuman*.
- Komunikasi ke pelanggan/calon pelanggan (promosi, follow-up, balasan CS) → arahkan ke
  `konten-mingguan`, `broadcast-wa`, `balas-chat-cs`, `follow-up-prospek`.
- Notulen rapat lengkap (siapa hadir, keputusan per agenda) → arahkan ke `notulen-rapat`.
- Surat resmi ke pihak luar (instansi pemerintah, mitra bisnis, bank) → arahkan ke `surat-resmi`.
- Perjanjian/kontrak kerja sama → arahkan ke `perjanjian-sederhana`.
- Surat peringatan/teguran ke karyawan tertentu → arahkan ke `surat-peringatan-karyawan`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Jenis laporan (3P/harian/newsletter/pengumuman/FAQ/memo/insiden) | Ya | Tebak dari kata kunci permintaan; jika ambigu, tanyakan |
| Bahan mentah (chat, poin, transkrip, atau disebutkan langsung) | Ya | — (tanyakan; jangan mengarang isi) |
| Nama tim/departemen atau nama pengirim | Ya untuk 3P/harian/memo | Tanyakan jika tidak jelas dari bahan mentah |
| Penerima (atasan/pemilik, tim, klien, seluruh karyawan) | Ya | Tebak dari konteks; sebutkan asumsi jika ditebak |
| Periode (harian/mingguan/bulanan, tanggal) | Ya untuk laporan berkala | Minggu berjalan (Senin–Jumat terakhir), sebutkan asumsi |
| Nada (sopan-formal / santai-profesional) | Tidak | Sopan-formal khas kantor Indonesia |
| Bahasa (ID / EN / bilingual) | Tidak | Bahasa Indonesia |
| Kanal tujuan (WA/Telegram, email, cetak/dokumen) | Tidak | WA/Telegram (format pendek, `*tebal*`) |

**Kerjakan dulu, tanya di akhir (wajib):** bila jenis & maksud permintaan sudah jelas
(mis. "pengumuman libur Natal & Tahun Baru untuk grup WA, 20 orang"), **langsung tulis
teks lengkapnya di balasan pertama** — jangan membuka balasan dengan daftar pertanyaan.
Hal yang belum diketahui ditulis `[isian: ...]` (nama kantor, jam kerja, nama pengirim)
dan paling banyak **3 pertanyaan singkat** ditaruh di akhir, setelah teksnya. Tanggal yang
sudah ada di `references/` (libur nasional, cuti bersama) **dicantumkan, bukan ditanyakan**.
Bila info wajib benar-benar kurang sampai teks tidak bisa disusun (mis. bahan laporan
kosong), tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan
singkat bernomor (maks. 5). Jika pengguna terburu-buru atau langsung memberi bahan mentah
tanpa detail lain, pakai default di atas dan sebutkan asumsi yang dipakai di akhir hasil.

## Langkah kerja
1. **Kenali jenis laporan** dari permintaan dan/atau isi bahan mentah. Jika dua jenis
   sama-sama mungkin (mis. "laporan mingguan" bisa 3P atau newsletter), tanyakan sekali.
2. **Buka template yang sesuai** di `templates/` untuk struktur & nada bakunya:
   - `3p-ke-atasan-pemilik.md`, `3p-ke-tim.md`, `3p-ke-klien.md` — tiga varian audiens 3P
   - `laporan-harian-wfh-wfo.md`
   - `newsletter-internal-kantor-kecil.md`
   - `pengumuman-internal.md`
   - `faq-karyawan.md`
   - `memo-surat-edaran.md`
   - `laporan-insiden.md`
3. **Ekstrak fakta dari bahan mentah saja.** Jangan menambah progres, angka, tanggal, atau
   nama yang tidak disebutkan. Info yang dibutuhkan template tapi tidak ada di bahan mentah
   → tandai `[isi: ...]` di tempatnya, atau tanyakan sekali jika krusial (mis. nama tim,
   tanggal efektif kebijakan).
4. **Susun sesuai format baku** template — jangan ubah struktur (urutan bagian, jenis
   bullet) tanpa alasan; struktur inilah yang membuat laporan mudah dibaca cepat.
5. **Terapkan nada**: sopan-formal (default; bahasa baku, sapaan "Bapak/Ibu", tanpa slang)
   atau santai-profesional (bila pengguna sebut "startup", "santai", atau budaya kantornya
   memang informal — sapaan nama langsung, boleh emoji secukupnya). Lihat
   `references/panduan-nada-dan-kanal.md` untuk contoh berdampingan.
6. **Terapkan format kanal**:
   - WA grup/Telegram (default): `*tebal*` untuk judul/label, bullet `-` pendek, emoji
     penanda bagian secukupnya (maks. 1 per bagian), tanpa tabel, baris pendek agar tidak
     terpotong di layar HP.
   - Email/dokumen: heading biasa, boleh tabel, kalimat lebih lengkap, salam pembuka/penutup.
7. **Bilingual (jika diminta)**: tulis versi Indonesia lengkap dahulu, lalu versi Inggris
   di bawahnya dengan struktur identik — jangan mencampur dua bahasa dalam satu kalimat.
8. **Untuk pengumuman THR/cuti bersama/libur nasional**: gunakan
   `templates/pengumuman-internal.md` bagian terkait. Nominal THR **tidak dihitung** di
   skill ini. Tanggal libur nasional/cuti bersama **2026** → ambil dari
   `references/libur-nasional-2026.md` (SKB 1497, 2, 5 Tahun 2025; sudah diverifikasi,
   salinan identik dengan `hitung-thr`) dan **jangan mencari di web**.
   - **Pengumuman untuk grup/seluruh karyawan TIDAK BOLEH memuat nominal gaji/THR per orang
     atau nama+nominal** — meski pengguna memintanya dan meski angkanya dari `hitung-thr`/
     `gaji-umkm`. Isi hanya info umum: tanggal bayar, dasar aturan, rumus umum, cara cek
     rincian pribadi. Ikuti **Aturan privasi & kanal** di atas (dua blok terpisah).
   - **Pengumuman libur akhir tahun (kerangka wajib):** dua blok bertajuk tetap —
     **TEKS GRUP (tanpa nominal per orang)** berisi tanggal libur & cuti bersama dari
     `references/` (24 Des 2026 cuti bersama, 25 Des Natal, 1 Jan 2027 Tahun Baru; sebut
     nama hari yang benar sesuai tabel), batas bayar THR "paling lambat H-7 hari raya"
     (bukan H-3), `[isian]` untuk nama kantor/jam, dan kalimat bahwa **THR per orang tidak
     dicantumkan di grup; rincian dikirim pribadi**; lalu **REKAP/PESAN PRIBADI — khusus
     pemilik/HR** (kerangka pesan pribadi tanpa angka karangan). Jangan menawarkan "saya
     hitungkan THR" kecuali skill `hitung-thr` benar-benar terpasang; bila tidak, tulis
     bahwa nominal dihitung terpisah oleh HR/akuntan.
   - **Tahun di luar tabel (2027 dst.):** maksimal **satu** pencarian web ke sumber resmi;
     bila belum pasti, tulis sebagai asumsi atau `[isi: tanggal sesuai SKB <tahun>]` dan
     lanjutkan — jangan mencari berulang, jangan menulis catatan tebakan ("SKB biasanya
     terbit …", "cuti bersama biasanya …").
   - **Nama usaha tidak diketahui:** tulis `[isi: nama usaha]` — jangan placeholder seperti
     "Usaha Anda"/"PT Anda" di teks grup. Tanggal cair THR yang tidak disebut → asumsi "paling lambat H-7 hari
     raya" (Permenaker 6/2016) dan sebutkan sebagai asumsi.
   - **Jangan menghitung THR sendiri.** Bila pengguna minta nominal: pakai skill `hitung-thr`
     bila terpasang, lalu rincian per orang hanya untuk pesan pribadi/HR. Bila tidak terpasang,
     katakan nominal perlu dihitung terpisah (mis. oleh HR/akuntan) dan jangan menyertakan
     angka hitungan sendiri. Bila hasil `hitung-thr` memberi ⚠️ (mis. tanggal masuk di masa
     depan), sampaikan di awal balasan dan minta konfirmasi sebelum angka dipakai.
9. Periksa **Checklist** di bawah sebelum menyerahkan hasil ke pengguna.

## Format output
Format persis mengikuti template jenis yang dipilih (lihat `templates/`). Ringkasan bentuk
inti tiap jenis:

**3P** — satu blok per tim:
```
[emoji] *[Nama Tim]* — [periode, mis. 15–19 Sep 2026]
*Progres:* [1–3 kalimat, data-driven]
*Rencana:* [1–3 kalimat]
*Kendala:* [1–3 kalimat, atau "Tidak ada kendala berarti"]
```

**Laporan harian WFH/WFO** — satu blok per orang, 3–5 baris, lihat template untuk versi
WFH (tambahan: kendala akses/koneksi) vs WFO.

**Pengumuman internal** — judul, isi inti (apa/berlaku sejak kapan/berlaku sampai kapan/
siapa terdampak), tindakan yang perlu dilakukan pembaca (jika ada), kontak jika ada pertanyaan.

**Laporan insiden** — format 5W1H (Apa/Kapan/Di mana/Siapa terdampak/Mengapa/Bagaimana
ditangani) + status saat ini + tindakan lanjutan + siapa yang bertanggung jawab.

Format lengkap newsletter, FAQ, dan memo/surat edaran: lihat masing-masing file di `templates/`.

## Contoh
**Input pengguna:** "Buatin laporan mingguan buat dikirim ke bos, dari chat tim: 'udah kelar
redesign landing page', 'fitur checkout masih nunggu API payment dari vendor, ETA minggu
depan', 'server sempet down 2 jam Selasa gara2 kehabisan disk, udah difix', 'minggu depan mau
mulai kerjain fitur notifikasi WA'. Nama tim: Produk."

**Output (WA, sopan-formal, default):**
```
🧩 *Tim Produk* — 21–25 Sep 2026
*Progres:* Redesign landing page selesai. Sempat ada gangguan server ±2 jam pada Selasa
akibat disk penuh, sudah diperbaiki.
*Rencana:* Mulai mengerjakan fitur notifikasi WA minggu depan.
*Kendala:* Fitur checkout masih menunggu API payment dari vendor, perkiraan selesai
minggu depan.

_Asumsi: periode laporan minggu berjalan (Senin–Jumat), penerima Bapak/Ibu pimpinan,
format sopan-formal. Ganti jika perlu._
```

## Checklist sebelum mengirim hasil
- [ ] Tidak ada progres/angka/tanggal yang dikarang — semua berasal dari bahan mentah
- [ ] Info yang hilang ditandai `[isi: ...]` atau sudah ditanyakan, bukan ditebak diam-diam
- [ ] Format sesuai template jenis yang dipilih (urutan bagian tidak diubah sembarangan)
- [ ] Nada konsisten dari awal sampai akhir (tidak campur formal-santai)
- [ ] Format kanal sesuai (WA/Telegram: `*tebal*` + bullet pendek; email: heading + kalimat lengkap)
- [ ] Pengumuman grup tidak memuat nominal gaji/THR per orang (juga saat memakai `hitung-thr`/`gaji-umkm`); rincian per orang di blok terpisah khusus pemilik/HR; THR tidak dihitung sendiri
- [ ] Balasan pertama langsung berisi teks pengumuman/laporan (dua blok bila menyangkut THR), bukan hanya pertanyaan; pertanyaan maks. 3 dan hanya di akhir; tanggal dari `references/` tidak ditanyakan
- [ ] Tahun pada ucapan sama dengan tahun tanggal libur (Tahun Baru 1 Jan 2027 = "Tahun Baru 2027")
- [ ] Balasan tidak memuat kata "skill", "script", "file", "cek" atau nama skill lain
- [ ] Tidak memakai kata proses ("file", "dokumen privat", "saya kirim/catat") — cukup "rincian dikirim pribadi oleh pemilik/HR"
- [ ] Tidak ada tawaran kirim otomatis ke grup/menyambungkan WhatsApp — hasil berupa draf untuk pemilik
- [ ] Data sensitif karyawan (gaji individu, alasan cuti pribadi, penilaian kinerja personal)
      tidak dicantumkan tanpa izin eksplisit dari pengguna
- [ ] Asumsi yang dipakai (periode, penerima, nada) disebutkan di akhir jika ditebak

## Batasan & penanganan error
- **Privasi karyawan (default):** di laporan ke atasan/pemilik/klien, jangan sebut nama karyawan untuk hal negatif atau pribadi (sakit, izin, kinerja, kesalahan) — tulis "staf/tim [bagian]", kecuali pengguna meminta nama disebut secara eksplisit. Info kesehatan tidak dirinci.
- **Tuduhan tanpa bukti / sanksi / PHK:** jangan menulis memo atau pengumuman yang menyalahkan orang tertentu tanpa fakta tertulis, atau mengumumkan PHK/sanksi sepihak. Sampaikan fakta kejadian secara netral (format laporan insiden 5W1H), lalu arahkan ke skill `surat-peringatan-karyawan` untuk teguran resmi dan ke konsultan hukum/Disnaker untuk PHK.
- **Bukan penghitung uang.** THR, gaji, lembur, pajak → arahkan ke skill hitung yang sesuai
  (`hitung-thr`, `pph-final-umkm`, dst.); skill ini hanya merapikan *teks pengumumannya*.
- **Tidak mengarang tanggal resmi** (libur nasional, cuti bersama) — 2026 dari
  `references/libur-nasional-2026.md`; tahun lain minta pengguna mengisi atau tandai
  `[isi: tanggal sesuai SKB tahun berjalan]`.
- **Bahan mentah kosong/tidak jelas**: jangan mengisi dengan asumsi generik ("berjalan lancar
  seperti biasa"); tanyakan poin-poin nyata ke pengguna dalam satu pesan.
- **Di luar cakupan** (notulen rapat detail, surat resmi ke pihak luar, kontrak, surat
  peringatan personal, komunikasi ke pelanggan): jelaskan bahwa skill ini untuk komunikasi
  internal kantor, dan arahkan ke skill yang sesuai (lihat "Kapan TIDAK digunakan").
- **Data pribadi karyawan**: jangan sertakan nominal gaji individu, kondisi kesehatan, atau
  alasan cuti pribadi di laporan yang akan dibagikan luas, kecuali pengguna secara eksplisit
  memintanya dan itu untuk penerima yang berwenang (mis. laporan insiden ke pemilik).
- **Permintaan bilingual tanpa bahasa sumber jelas**: defaultkan bahan mentah berbahasa
  Indonesia diterjemahkan ke Inggris di bagian kedua, bukan campur dalam satu kalimat.
