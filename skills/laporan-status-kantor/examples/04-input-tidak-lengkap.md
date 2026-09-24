# Skenario 4 (S4, input tidak lengkap) — permintaan malas/singkat

## Skenario
Pengguna minta laporan mingguan tanpa detail apa pun ("bikinin laporan mingguan dong").

## Input pengguna (persis)
> "bikinin laporan mingguan dong"

## Output (mengikuti SKILL.md — Langkah 1 & bagian Input: "jika info wajib kurang,
tanyakan sekali dalam satu pesan berisi daftar pertanyaan singkat bernomor, maks. 5")

```
Boleh, siap dibantu. Sebelum saya susun, saya perlu beberapa info singkat (jawab dalam
satu pesan aja, boleh dari yang penting-penting saja):
1. Laporan mingguan ini untuk siapa? (atasan/pemilik, tim, atau klien — formatnya beda)
2. Nama tim/departemen/proyek apa?
3. Apa saja yang perlu dilaporkan minggu ini? (progres, rencana, kendala — bisa tempel
   chat atau poin-poin acak, saya yang rapikan)
4. Periode laporannya minggu tanggal berapa? (kalau tidak disebut, saya pakai minggu
   berjalan)
5. Mau dikirim lewat WA/Telegram atau email? (kalau tidak disebut, saya pakai format WA)

Kalau mau cepat, cukup jawab poin 1 dan 3 saja — sisanya saya pakai default yang wajar dan
saya sebutkan asumsinya di laporan.
```

## Catatan penguji

**Bagus:**
- Tepat mengikuti instruksi: bertanya **sekali**, dalam **satu pesan**, **bernomor**,
  maks. 5 pertanyaan — persis sesuai spesifikasi SKILL.md bagian Input dan Langkah kerja
  1.
- Tidak langsung mengarang laporan kosong ("berjalan lancar seperti biasa") — sesuai
  larangan eksplisit di Batasan & Penanganan Error: "jangan mengisi dengan asumsi generik".
- Memberi jalan pintas untuk pengguna terburu-buru ("cukup jawab poin 1 dan 3 saja... saya
  pakai default") — konsisten dengan prinsip CLAUDE.md "instan tapi powerful": pengguna
  awam yang malas mengetik tetap dilayani cepat tanpa dipaksa isi form panjang.
- Pertanyaan wajib yang paling krusial (penerima, jenis, bahan mentah) diprioritaskan di
  urutan atas.

**Temuan:**
- Tidak ada cacat. Ini salah satu bagian skill yang paling matang — jelas menang
  dibanding jawaban AI generik tanpa skill yang biasanya main terka isi laporan kosong
  (lihat perbandingan di `00-pembanding-tanpa-skill.md`).
