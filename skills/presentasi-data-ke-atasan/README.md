# Ubah Angka Jadi Pesan yang Didengar Atasan

**Kirim data/analisis, dapat 4 format siap kirim: WA, email, 1 halaman eksekutif, dan skrip bicara.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Satu kalimat inti ("so what") yang langsung menjawab "jadi bagaimana?" — bukan
  tabel mentah yang harus ditafsirkan atasan sendiri
- ✅ 3 angka pendukung yang **dihitung script** (Decimal), bukan dikira-kira
- ✅ Grafik yang tepat untuk pesannya — bukan grafik asal ada
- ✅ Risiko & rekomendasi dengan aksi, PIC, dan tenggat yang jelas — bukan saran umum
- ✅ 4 format sekaligus: ringkasan WA 5 baris, email formal, 1 halaman eksekutif, skrip
  bicara 2 menit — tinggal pilih sesuai kanalnya

## Cocok untuk siapa
- Karyawan/staf yang harus lapor angka ke atasan/owner tapi bingung mulai dari mana
- Pemilik usaha yang mau mengajukan pinjaman/dana ke bank atau investor
- Admin/finance yang setiap bulan membuat laporan kinerja untuk pemilik
- Siapa pun yang sudah punya angka (dari `analisis-excel`/`rekap-penjualan-csv`/laporan
  kasir) dan perlu mengubahnya jadi pesan yang enak dibaca orang sibuk

## Contoh sebelum & sesudah
**Sebelum:** "Omzet September 24.500.000, Agustus 32.000.000, biaya iklan naik dari
4 juta ke 5,6 juta..." — dikirim apa adanya ke atasan, tidak jelas kesimpulannya apa.

**Sesudah (cukup ketik):** "Tolong buatkan ringkasan untuk owner dari data ini: omzet
Agustus 32 juta, September 24,5 juta; biaya iklan Agustus 4 juta, September 5,6 juta"
→
```
📊 *Kinerja September 2026*
Omzet turun 23% (bulan puasa), tapi biaya iklan naik 40% — rasio
biaya/omzet melonjak dari 12% ke 23%.
• Omzet: Rp32 juta → Rp24,5 juta (-23%)
• Biaya iklan: Rp4 juta → Rp5,6 juta (+40%)
• Rasio biaya iklan/omzet: 12% → 23%
👉 Usul turunkan budget iklan Shopee ~Rp1 juta/bulan mulai minggu
depan sambil evaluasi materi iklan.
```
Plus versi email formal, 1 halaman eksekutif, dan skrip bicara 2 menit — semua dengan
angka yang sama persis.

**Hasil uji (OpenClaw, uji otomatis agent, 2026-10-01):** rata-rata nilai 7,5 tanpa skill menjadi 8,75 dengan skill (skala 10), pada dua skenario.
Pembeda nyata ada di skenario normal: dengan skill Anda langsung mendapat pesan inti "jadi bagaimana?" yang siap kirim, bukan sekadar daftar angka.
Jujur: saat diminta menulis penurunan omzet 19,2% sebagai "sekitar 10%", AI tanpa skill pun menolak dan memakai angka asli, jadi itu bukan pembeda.
Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Tolong buatkan ringkasan untuk owner dari data ini: omzet Agustus 32 juta, September 24,5 juta."
- "Ubah analisis ini jadi pesan WA 5 baris untuk bos."
- "Buatkan email formal dan skrip bicara 2 menit untuk laporan ke direktur."

## Syarat
Tidak perlu instalasi apa pun untuk pemakaian dasar. Untuk perhitungan selisih/persen
yang diverifikasi script, dibutuhkan Python (biasanya sudah ada di Mac/Linux; di Windows
bisa dipasang gratis dari python.org) — hanya Python standar, tanpa paket tambahan.

## Instalasi singkat
Salin folder `presentasi-data-ke-atasan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah angkanya bisa salah/dikarang AI?**
Tidak — selisih dan persen perubahan dihitung lewat script Python (`Decimal`, presisi
uang), bukan ditaksir model. Angka hanya diambil dari data yang kamu berikan.

**Bisa langsung dari file Excel/CSV penjualan?**
Bisa — jalankan dulu `analisis-excel` atau `rekap-penjualan-csv` untuk mengolah filenya,
lalu hasilnya dibawa ke skill ini untuk diubah jadi pesan siap kirim.

**Beda dengan `presentasi-instan`?**
`presentasi-instan` membuat **slide/deck** banyak halaman untuk ditampilkan/dicetak.
Skill ini fokus ke **satu pesan inti** dalam format pendek (WA/email/1 halaman/skrip
bicara) — cocok untuk update cepat, bukan deck presentasi penuh.
