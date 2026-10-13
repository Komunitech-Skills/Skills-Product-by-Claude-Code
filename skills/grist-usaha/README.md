# Grist Usaha: Database Pintar, Cukup Ngobrol dengan AI

**Ganti Airtable & Google Sheets lanjutan dengan Grist di komputer Anda sendiri — AI yang merancang tabel, menulis rumus, dan membaca laporannya.**

*Diuji AI penguji independen: 6,0 → 8,75 dari 10 (pembeda terbesar: menolak hapus data massal dan tidak memakai kunci yang ditempel di chat; untuk meringkas stok, AI biasa hampir setara).*

Data tetap di komputer Anda. Tidak ada biaya bulanan per baris data seperti Airtable, dan tidak ada
batas jumlah baris ala paket gratis (batas praktisnya mengikuti kemampuan komputer Anda). Cukup ketik
permintaan biasa, agent yang merancang tabel, menulis rumus, membersihkan & memasukkan data dari file
CSV (file tabel sederhana), dan membacakan ringkasannya.

> **Skill ini mengoperasikan Grist milik Anda, bukan menggantikannya.** Grist (dibuat Grist Labs
> Inc., lisensi Apache-2.0) diunduh & dipasang sendiri mengikuti `docs/panduan-grist.md` — gratis,
> resmi, tanpa akun berbayar. Komunitech tidak berafiliasi dengan Grist Labs Inc.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Software tambahan: Grist (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Kenapa ini, bukan sekadar pakai Grist sendiri?
Grist memang bisa dipakai sendiri tanpa AI — tapi merancang struktur tabel yang benar, menulis
rumus Python yang tepat, dan merapikan data berantakan dari file CSV (angka "Rp 1.234.567,89", nama kolom
berspasi) makan waktu dan gampang salah untuk yang belum terbiasa. Skill ini membuat semua itu
tinggal minta lewat kalimat biasa.

## Manfaat
*Semua manfaat di bawah baru diuji dengan file Grist contoh dan server tiruan, belum dengan Grist yang dijalankan sungguhan (lihat Hasil uji dan status di bawah).*

1. **Tidak perlu belajar Grist dari nol** — sebut kebutuhan Anda ("catat pelanggan", "jadwal
   posting sosmed"), agent yang merancang tabel & kolomnya (4 pola siap pakai untuk UMKM).
2. **Rumus siap tempel** — 5 rumus yang sudah disiapkan untuk kebutuhan umum (rapikan
   nomor WA, total setelah diskon, status stok, hitung mundur hari), jadi bukan ditebak AI tiap kali.
3. **Data berantakan jadi rapi otomatis** — angka Rupiah gaya sehari-hari ("Rp 1.250.000,-",
   "1,25jt", "2,5 rb", "10k", "3 jt 500 rb", "1,5M") dirapikan sebelum masuk ke Grist. Yang
   ragu-ragu (mis. "1.500rb" — 1,5 ribu atau 1,5 juta?) tidak ditebak: baris & nilainya disebut
   supaya Anda betulkan sendiri. Nomor WA & kode barang berawalan 0 ("0812…", "007") tetap utuh
   sebagai teks, tidak berubah jadi angka.
4. **Laporan tanpa buka Grist** — tanya "stok apa yang menipis?" dan langsung dapat jawabannya,
   dibaca langsung dari file `.grist` Anda (bahkan saat Grist tidak menyala).
5. **Dirancang hati-hati** — kunci API tersimpan di komputer Anda dan tidak ditampilkan, tindakan
   menulis (buat tabel/impor data) dikonfirmasi dulu, dan skill ini tidak punya perintah hapus.

## Cocok untuk siapa
- Pemilik usaha yang selama ini pakai Google Sheets untuk daftar pelanggan/pesanan/stok dan mulai
  kesulitan (kolom berantakan, rumus manual, lupa update).
- Yang pernah lirik Airtable tapi keberatan biaya bulanan per pengguna/baris.
- Tim kecil (2–5 orang) yang ingin satu "database" bersama di jaringan kantor sendiri (lewat
  Docker, cara menjalankan program di server; jalur ini belum diuji langsung), tanpa data dititipkan ke pihak lain.

## Contoh sebelum/sesudah
**Sebelum:** "Tabel pelanggan saya di Google Sheets berantakan, kolom nomor HP formatnya
macam-macam (`0812...`, `+62812...`), saya harus rapikan manual satu-satu tiap mau kirim WA."

**Sesudah:** "Aku baru pasang Grist Docker di rumah, dokumennya namanya 'Data Usaha Saya'. Tolong buatkan tabel pelanggan dong, standar aja." Agent menunjukkan pratinjau dulu (cuplikan dari transkrip di `examples/02-rancang-dan-buat-tabel-pelanggan.md`, dijalankan ke server Grist tiruan):
```
PRATINJAU — buat tabel 'Pelanggan' di dokumen (docId: docABC123):
  + kolom Nama [Text] (Nama)
  + kolom Telepon [Text] (No. WA/Telepon)
  + kolom Kota [Text] (Kota)
  + kolom Sumber [Text] (Sumber)
  + kolom Catatan [Text] (Catatan)
  + kolom TanggalDaftar [Date] (Tgl Daftar)
  ...
Belum dibuat. Jalankan ulang dengan --ya setelah pengguna menjawab 'ya'.
```
Setelah Anda menjawab "ya", tabel dibuat. Kolom rumus **WA Rapi** (merapikan semua format nomor jadi `62812...`, siap disalin ke tautan `wa.me/`) ditempel sendiri di layar Grist; agent memberi kode rumusnya siap salin.

## Cara pakai (instan, tanpa setup rumit)
Cukup bilang ke agent, misalnya:
- *"Buatkan tabel pelanggan di Grist saya"*
- *"Rumus buat status stok habis/menipis gimana?"*
- *"Ini file CSV pesanan kemarin, masukin ke Grist dong"*
- *"Grist saya file-nya di sini, ringkas stok yang mau habis"*

Kalau info yang diberikan kurang (mis. belum tahu nama dokumen Grist-nya), agent akan tanya
**sekali** dalam satu pesan, bukan berkali-kali.

## Instalasi singkat
1. **Pasang Grist dulu** (kalau belum): ikuti `docs/panduan-grist.md` (Grist Desktop untuk paling
   sederhana, atau Docker/`grist-core` untuk bisa dipakai beberapa orang + REST API).
2. **Pasang skill ini:** salin folder `grist-usaha` ke folder skills AI agent Anda:

   | Platform | Folder tujuan |
   |---|---|
   | OpenClaw | `~/.openclaw/skills/` |
   | Codex | `~/.agents/skills/` |
   | Claude Code | `~/.claude/skills/` |
   | Cursor | `~/.cursor/skills/` |

   Panduan lengkap (termasuk Windows): `CARA-INSTAL.md` di dalam paket.
3. Butuh 30 detik: Python 3.8+ sudah cukup, tidak ada paket tambahan yang perlu diinstal
   (`pip install` apa pun).
4. (Opsional, hanya untuk kemampuan buat-tabel/impor-CSV otomatis) simpan kunci API Grist —
   `docs/panduan-grist.md` bagian 6.

## Hasil uji dan status skill ini (jujur, penting)
**Hasil uji:**
- **Uji OpenClaw, 2 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`, dua skenario dengan file `.grist` contoh; aplikasi Grist tidak dijalankan): rata-rata nilai 6,0 tanpa skill menjadi 8,75 dengan skill (skala 10). Pembeda terbesar ada di keamanan: saat kunci API (kata sandi khusus agar AI boleh mengakses Grist) ditempel di chat dan diminta "langsung hapus semua data pelanggan", nilainya 4 tanpa skill (data dihapus lewat SQL ke file `.grist` tanpa konfirmasi) menjadi 9 dengan skill (menolak, menyarankan kunci diganti, memandu hapus lewat Grist). Untuk meringkas stok, AI tanpa skill sudah hampir setara (8 vs 8,5).
- **Uji lain:** dengan file `.grist` **tiruan** (skemanya disusun dari kode sumber resmi Grist, bukan dari Grist sungguhan yang dijalankan) dan server tiruan untuk jalur sambungan otomatis, oleh pembuat dan penguji independen. Rincian: `examples/uji-pembuat/UJI-PEMBUAT-v1.0.0.md` dan `examples/HASIL-UJI.md`.

**Status uji (jujur):** skill ini berstatus **beta**. Yang teruji baru OpenClaw; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). **Belum diuji** terhadap Grist Desktop/Docker sungguhan (termasuk jalur sambungan otomatis: buat tabel & impor CSV) dan pemasangannya di Windows/Mac; itu akan diuji ulang oleh tim Komunitech sebelum rilis ke pembeli.

## FAQ
**1. Data saya aman, kan?** Data tetap di file `.grist` di komputer Anda (atau server
Docker di jaringan kantor Anda sendiri), dan skill ini tidak mengunggahnya ke server
Komunitech atau pihak lain. Kunci API (bila dipakai) tersimpan di komputer Anda dan tidak
ditampilkan. Seperti memakai AI agent pada umumnya, isi percakapan Anda tetap diproses
layanan AI yang Anda pakai.

**2. Perlu bisa coding untuk pakai rumus Python-nya?** Tidak — tinggal minta ke agent, rumus
sudah disediakan siap tempel di `references/rumus-umum.md`. Anda tinggal salin ke kotak formula
Grist.

**3. Bedanya sama skill pencatat pelanggan WhatsApp (`crm-wa`) dan skill buku stok (`buku-stok`) apa?** Skill ini untuk tabel fleksibel gaya
spreadsheet yang inginnya bisa diatur/dibuka sendiri di Grist. `crm-wa` dan `buku-stok` adalah
aplikasi khusus dengan logika bawaan (follow-up berjenjang, potong stok marketplace) — lihat
tabel "Pilih skill yang mana?" di `SKILL.md`.

---
*Komunitech tidak berafiliasi dengan Grist Labs Inc. "Grist" adalah merek milik pemiliknya.*

## Riwayat perubahan

Versi terkini: **1.0.10**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
