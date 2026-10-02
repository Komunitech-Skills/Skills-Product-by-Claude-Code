---
name: laporan-status-kantor
description: Mengubah catatan kerja berantakan (chat grup, poin acak, transkrip voice note) menjadi laporan status kantor yang rapi dan siap kirim — laporan mingguan/bulanan format 3P (Progres-Rencana-Kendala) ke atasan/pemilik/tim/klien, laporan harian WFH/WFO, newsletter internal kantor kecil, pengumuman internal (libur nasional, jam kerja, THR tanpa hitungan), FAQ karyawan, memo/surat edaran, dan laporan insiden 5W1H. Gunakan saat pengguna minta: laporan mingguan, laporan bulanan, 3P update, status report, weekly update, laporan ke atasan/owner/bos, newsletter kantor, pengumuman internal, FAQ karyawan, memo internal, surat edaran, laporan insiden/masalah, incident report, company newsletter, internal comms, standup.
---

# Laporan Status Kantor

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

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
  `caption-sosmed-umkm`, `broadcast-wa`, `balas-chat-cs`, `follow-up-prospek`.
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

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan
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
   `templates/pengumuman-internal.md` bagian terkait. Tanggal libur nasional/cuti bersama
   dan nominal THR **wajib diisi pengguna** (skill ini tidak menghitung atau mengarang
   tanggal resmi pemerintah yang berubah tiap tahun).
   - **Pengumuman untuk grup/seluruh karyawan TIDAK BOLEH memuat nominal gaji/THR per orang
     atau nama+nominal** — meski pengguna memintanya. Isi hanya info umum: tanggal bayar,
     dasar aturan, rumus umum. Tolak sopan permintaan itu, jelaskan alasannya (data pribadi),
     dan tawarkan pesan pribadi/HR per karyawan sebagai gantinya.
   - **Jangan menghitung THR sendiri.** Bila pengguna minta nominal: pakai skill `hitung-thr`
     bila terpasang, lalu rincian per orang hanya untuk pesan pribadi/HR. Bila tidak terpasang,
     katakan nominal perlu dihitung terpisah (mis. oleh HR/akuntan) dan jangan menyertakan
     angka hitungan sendiri.
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
🧩 *Tim Produk* — 15–19 Sep 2026
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
- [ ] Pengumuman grup tidak memuat nominal gaji/THR per orang; THR tidak dihitung sendiri
- [ ] Data sensitif karyawan (gaji individu, alasan cuti pribadi, penilaian kinerja personal)
      tidak dicantumkan tanpa izin eksplisit dari pengguna
- [ ] Asumsi yang dipakai (periode, penerima, nada) disebutkan di akhir jika ditebak

## Batasan & penanganan error
- **Privasi karyawan (default):** di laporan ke atasan/pemilik/klien, jangan sebut nama karyawan untuk hal negatif atau pribadi (sakit, izin, kinerja, kesalahan) — tulis "staf/tim [bagian]", kecuali pengguna meminta nama disebut secara eksplisit. Info kesehatan tidak dirinci.
- **Tuduhan tanpa bukti / sanksi / PHK:** jangan menulis memo atau pengumuman yang menyalahkan orang tertentu tanpa fakta tertulis, atau mengumumkan PHK/sanksi sepihak. Sampaikan fakta kejadian secara netral (format laporan insiden 5W1H), lalu arahkan ke skill `surat-peringatan-karyawan` untuk teguran resmi dan ke konsultan hukum/Disnaker untuk PHK.
- **Bukan penghitung uang.** THR, gaji, lembur, pajak → arahkan ke skill hitung yang sesuai
  (`hitung-thr`, `pph-final-umkm`, dst.); skill ini hanya merapikan *teks pengumumannya*.
- **Tidak mengarang tanggal resmi** (libur nasional, cuti bersama) — tanggal berubah tiap
  tahun (SKB 3 Menteri); minta pengguna mengisi atau tandai `[isi: tanggal sesuai SKB tahun
  berjalan]`.
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
