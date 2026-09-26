# Grist Usaha — asisten AI untuk database "spreadsheet pintar" Anda

**Ganti Airtable & Google Sheets lanjutan dengan Grist di komputer Anda sendiri — AI yang merancang tabel, menulis rumus, dan membaca laporannya.**

Data tetap di komputer Anda. Tidak ada biaya bulanan per baris data seperti Airtable. Tidak ada
batas jumlah baris paket gratis. Cukup ketik permintaan biasa, agent yang merancang tabel,
menulis rumus, membersihkan & memasukkan data CSV, dan membacakan ringkasannya.

> **Skill ini mengoperasikan Grist milik Anda, bukan menggantikannya.** Grist (dibuat Grist Labs
> Inc., lisensi Apache-2.0) diunduh & dipasang sendiri mengikuti `docs/panduan-grist.md` — gratis,
> resmi, tanpa akun berbayar. Komunitech tidak berafiliasi dengan Grist Labs Inc.

## Kenapa ini, bukan sekadar pakai Grist sendiri?
Grist memang bisa dipakai sendiri tanpa AI — tapi merancang struktur tabel yang benar, menulis
rumus Python yang tepat, dan merapikan data CSV berantakan (angka "Rp 1.234.567,89", nama kolom
berspasi) makan waktu dan gampang salah untuk yang belum terbiasa. Skill ini membuat semua itu
tinggal minta lewat kalimat biasa.

## 3–5 manfaat
1. **Tidak perlu belajar Grist dari nol** — sebut kebutuhan Anda ("catat pelanggan", "jadwal
   posting sosmed"), agent yang merancang tabel & kolomnya (4 pola siap pakai untuk UMKM).
2. **Rumus dijamin benar secara nalar** — 5 rumus siap tempel untuk kebutuhan umum (rapikan
   nomor WA, total setelah diskon, status stok, hitung mundur hari), bukan tebakan.
3. **Data berantakan jadi rapi otomatis** — angka Rupiah format apa pun ("Rp 1,25jt" ditulis beda-
   beda orang) dirapikan sebelum masuk ke Grist.
4. **Laporan tanpa buka Grist** — tanya "stok apa yang menipis?" dan langsung dapat jawabannya,
   dibaca langsung dari file `.grist` Anda (bahkan saat Grist tidak menyala).
5. **Aman by design** — kunci API tersimpan lokal & tidak pernah tercetak, semua tindakan
   menulis (buat tabel/impor data) selalu dikonfirmasi dulu, tidak ada perintah hapus.

## Cocok untuk siapa
- Pemilik usaha yang selama ini pakai Google Sheets untuk daftar pelanggan/pesanan/stok dan mulai
  kesulitan (kolom berantakan, rumus manual, lupa update).
- Yang pernah lirik Airtable tapi keberatan biaya bulanan per pengguna/baris.
- Tim kecil (2–5 orang) yang ingin satu "database" bersama di jaringan kantor sendiri (lewat
  Docker), tanpa data dititipkan ke pihak lain.

## Contoh sebelum/sesudah
**Sebelum:** "Tabel pelanggan saya di Google Sheets berantakan, kolom nomor HP formatnya
macam-macam (`0812...`, `+62812...`), saya harus rapikan manual satu-satu tiap mau kirim WA."

**Sesudah** (lihat transkrip nyata di `examples/02-rancang-dan-buat-tabel-pelanggan.md`):
tabel Pelanggan di Grist dengan kolom rumus `TeleponRapi` yang otomatis mengubah semua format
nomor jadi `62812...` — tinggal disalin ke tautan `wa.me/`.

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
2. **Pasang skill ini** di platform Anda — lihat `docs/instalasi.md` untuk lokasi persis per
   platform:
   - **Claude Code / OpenClaw:** salin folder `grist-usaha` ke folder skills platform Anda.
   - **Cursor / Codex:** ikuti petunjuk di `docs/instalasi.md` sesuai versi Anda.
3. Butuh 30 detik: Python 3.8+ sudah cukup, tidak ada paket tambahan yang perlu diinstal
   (`pip install` apa pun).
4. (Opsional, hanya untuk kemampuan buat-tabel/impor-CSV otomatis) simpan kunci API Grist —
   `docs/panduan-grist.md` bagian 6.

## FAQ
**1. Data saya aman, kan?** Ya — semuanya tetap di file `.grist` di komputer Anda (atau server
Docker di jaringan kantor Anda sendiri). Skill ini tidak pernah mengunggah data ke server
Komunitech atau pihak lain. Kunci API (bila dipakai) tersimpan lokal, tidak pernah tercetak.

**2. Perlu bisa coding untuk pakai rumus Python-nya?** Tidak — tinggal minta ke agent, rumus
sudah disediakan siap tempel di `references/rumus-umum.md`. Anda tinggal salin ke kotak formula
Grist.

**3. Bedanya sama skill `crm-wa`/`buku-stok` apa?** Skill ini untuk tabel fleksibel gaya
spreadsheet yang inginnya bisa diatur/dibuka sendiri di Grist. `crm-wa`/`buku-stok` adalah
aplikasi khusus dengan logika bawaan (follow-up berjenjang, potong stok marketplace) — lihat
tabel "Pilih skill yang mana?" di `SKILL.md`.

## Kejujuran soal status skill ini (penting)
Skill ini berstatus **draft**, dibuat & diuji dalam satu sesi kerja Komunitech dengan file
`.grist` **tiruan** (skemanya disusun dari kode sumber resmi Grist, bukan dari Grist sungguhan
yang dijalankan) dan server REST API tiruan — lihat `examples/HASIL-UJI.md` untuk rincian lengkap
apa yang sudah & belum diuji. Sebelum rilis ke pembeli, skill ini akan diuji ulang terhadap Grist
Desktop/Docker sungguhan oleh tim Komunitech.

---
*Komunitech tidak berafiliasi dengan Grist Labs Inc. "Grist" adalah merek milik pemiliknya.*
