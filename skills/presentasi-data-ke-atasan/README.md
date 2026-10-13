# Ubah Angka Jadi Pesan yang Didengar Atasan

**Kirim data/analisis, dapat 4 format siap kirim: WA, email, 1 halaman eksekutif, dan skrip bicara.**

*Diuji AI penguji independen di OpenClaw: 7,5 → 8,75 dari 10 (pembedanya: tanpa skill AI memberi daftar angka tanpa kalimat inti dan tanpa rekomendasi, dengan skill ada pesan inti "jadi bagaimana?" yang siap kirim; untuk menolak memoles angka, AI biasa sudah sama baiknya).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Satu kalimat inti yang langsung menjawab "jadi bagaimana?" — bukan
  tabel mentah yang harus ditafsirkan atasan sendiri
- ✅ 3 angka pendukung yang **dihitung oleh skrip** (selisih dan persen, presisi rupiah), bukan dikira-kira
- ✅ Saran grafik yang tepat untuk pesannya — bukan grafik asal ada
- ✅ Risiko & rekomendasi dengan aksi, penanggung jawab (PIC), dan tenggat — bukan saran umum
  (bila penyebab turunnya angka tidak Anda sebutkan, rekomendasinya masih umum dan AI akan menyebutnya terus terang)
- ✅ 4 format sekaligus: ringkasan WA 5 baris, email formal, 1 halaman eksekutif, skrip
  bicara ±2 menit — tinggal pilih sesuai kanalnya

## Cocok untuk siapa
- Karyawan/staf yang harus lapor angka ke atasan/owner tapi bingung mulai dari mana
- Pemilik usaha yang mau mengajukan pinjaman/dana ke bank atau investor
- Admin/finance yang setiap bulan membuat laporan kinerja untuk pemilik
- Siapa pun yang sudah punya angka (dari skill **Analisis Excel**, skill **Rekap Penjualan CSV** (CSV = file tabel sederhana yang bisa dibuka di Excel), atau
  laporan kasir) dan perlu mengubahnya jadi pesan yang enak dibaca orang sibuk

## Contoh sebelum & sesudah
**Sebelum:** "Omzet September 24.500.000, Agustus 32.000.000, biaya iklan naik dari
4 juta ke 5,6 juta..." — dikirim apa adanya ke atasan, tidak jelas kesimpulannya apa.

**Sesudah (cukup ketik):** "Tolong buatkan ringkasan buat owner. Omzet Agustus Rp32.000.000, September (bulan puasa) Rp24.500.000. Biaya iklan Agustus Rp4.000.000, September Rp5.600.000. Ini untuk owner, tujuannya lapor kondisi terkini dan minta persetujuan turunkan budget iklan."
→ Cuplikan ringkasan WA (contoh uji simulasi, data fiktif; dari `examples/01-omzet-turun-bulan-puasa.md`):
```
📊 *Kinerja September 2026*
Omzet turun 23% (bulan puasa), tapi biaya iklan justru naik 40% —
efisiensi iklan menurun tajam.
• Omzet: Rp32.000.000 → Rp24.500.000 (-23%)
• Biaya iklan: Rp4.000.000 → Rp5.600.000 (+40%)
• Rasio biaya iklan/omzet: 12,5% → 22,9%
👉 Usul turunkan budget iklan [isian: kanal iklan] sebesar [isian: nominal]/bulan
mulai minggu depan sambil evaluasi materi iklan. Mohon persetujuan Bapak/Ibu.
```
Bagian `[isian: ...]` sengaja dikosongkan karena kanal iklan dan nominalnya tidak Anda sebutkan; tinggal Anda isi. Hasil aslinya juga memuat versi email formal, 1 halaman eksekutif, dan skrip bicara, semuanya memakai angka yang sama.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Tolong buatkan ringkasan untuk owner dari data ini: omzet Agustus 32 juta, September 24,5 juta."
- "Ubah analisis ini jadi pesan WA 5 baris untuk bos."
- "Buatkan email formal dan skrip bicara 2 menit untuk laporan ke direktur."

## Syarat
Tidak perlu instalasi apa pun untuk pemakaian dasar. Untuk perhitungan selisih/persen
yang diverifikasi skrip, dibutuhkan Python (biasanya sudah ada di Mac/Linux; di Windows
bisa dipasang gratis dari python.org) — hanya Python standar, tanpa paket tambahan.

## Instalasi singkat
Salin folder `presentasi-data-ke-atasan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`, dua skenario): rata-rata nilai 7,5 tanpa skill menjadi 8,75 dengan skill (skala 10): skenario laporan omzet/iklan/pesanan 3 bulan 6,5 → 8,5, skenario diminta memoles penurunan omzet 8,5 → 9. Pembeda nyata ada di skenario normal: dengan skill Anda langsung mendapat pesan inti "jadi bagaimana?" yang siap kirim, bukan sekadar daftar angka.
- Jujur: saat diminta menulis penurunan omzet 19,2% sebagai "sekitar 10%", AI tanpa skill pun menolak dan memakai angka asli, jadi itu bukan pembeda. Pada uji yang sama, skrip bicara "2 menit" baru ±179 kata (sasaran ±280–320 kata), dan rekomendasi masih umum bila penyebab turunnya omzet tidak Anda sebutkan.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah angkanya bisa salah/dikarang AI?**
Skill dirancang agar tidak: selisih dan persen perubahan dihitung lewat skrip Python
(hitungan desimal berpresisi uang), bukan ditaksir model, dan angka hanya diambil dari data
yang Anda berikan. Tetap cek ulang angka penting sebelum dikirim ke atasan.

**Bisa langsung dari file Excel/CSV penjualan?**
Bisa — jalankan dulu skill **Analisis Excel** (`analisis-excel`) atau **Rekap Penjualan CSV**
(`rekap-penjualan-csv`) untuk mengolah filenya, lalu hasilnya dibawa ke skill ini untuk diubah
jadi pesan siap kirim.

**Beda dengan skill Presentasi Instan (`presentasi-instan`)?**
Presentasi Instan membuat **slide/deck** banyak halaman untuk ditampilkan/dicetak.
Skill ini fokus ke **satu pesan inti** dalam format pendek (WA/email/1 halaman/skrip
bicara) — cocok untuk update cepat, bukan deck presentasi penuh.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
