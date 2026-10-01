# SPT Tahunan Beres Sebelum Buka Coretax

**Ceritakan penghasilan setahun dengan bahasa biasa — langsung tahu kurang bayar, lebih bayar, atau nihil, lengkap dengan daftar dokumen yang harus disiapkan.**

## Manfaat
- ✅ Tidak kaget di Coretax: tahu dari awal berapa pajak yang harus disetor (atau dikembalikan) dan alasannya
- ✅ Angka dihitung script dengan tarif Pasal 17 UU HPP & PTKP resmi — PKP dibulatkan sesuai aturan, bukan dikira-kira
- ✅ Menangani kasus yang sering bikin bingung: pindah kerja (2 bukti potong A1), karyawan + usaha sampingan, freelancer NPPN, zakat, suami-istri digabung
- ✅ Peta "angka ini masuk bagian mana" di formulir SPT Coretax yang baru (1770/1770S sudah dihapus)
- ✅ Checklist dokumen pribadi: bukti potong, harta, utang, bukti zakat, bukti setor — tinggal centang

## Cocok untuk siapa
- Karyawan yang tahun lalu pindah kerja atau punya dua kantor
- Freelancer, desainer, penulis, konsultan, dokter/pengacara praktik mandiri yang memakai norma (NPPN)
- Karyawan yang punya usaha sampingan / toko online (PPh final 0,5%)
- Siapa pun yang ingin mengecek hitungan sebelum melapor sendiri atau menyerahkan ke konsultan

## Contoh sebelum & sesudah
**Sebelum:** Buka Coretax, tiba-tiba muncul "kurang bayar Rp5,7 juta" setelah memasukkan dua bukti potong — tidak tahu itu benar atau salah, lalu panik.

**Sesudah (cukup ketik):** "Tahun 2025 saya pindah kerja. A1 kantor lama neto 90 juta PPh 21 1.350.000, kantor baru neto 60 juta PPh 21 nol. Status K/1."
→ Rincian neto → PTKP Rp63 juta → PKP Rp87 juta → PPh Rp7.050.000 → dikurangi yang sudah dipotong → **kurang bayar Rp5.700.000**, plus penjelasan sederhana kenapa (dua kantor sama-sama memakai PTKP penuh), langkah bayar lewat kode billing, dan checklist dokumen.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Hitung SPT tahunan saya: karyawan TK/0, di A1 neto 114 juta, PPh 21 dipotong 3 juta."
- "Saya freelancer desain di Bandung, penghasilan 2025 240 juta, sudah lapor NPPN. Kurang bayar berapa?"
- "Karyawan K/2 plus usaha jasa, zakat ke BAZNAS 5 juta — pajak tahunan saya berapa?"

## Instalasi singkat
Salin folder `spt-tahunan-op` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Script memakai Python standar (tanpa instal apa pun); bila Python tidak ada, agent menghitung manual dengan rumus yang sama.

## FAQ
**1. Apakah skill ini melaporkan SPT saya ke DJP?**
Tidak. Skill hanya menghitung dan menyiapkan checklist. Pelaporan tetap kamu lakukan sendiri di Coretax (atau lewat konsultan). Jangan pernah membagikan password atau kode otorisasi Coretax ke siapa pun, termasuk AI.

**2. Apakah hasilnya pasti sama dengan Coretax?**
Rumus dan tarif mengikuti aturan resmi yang dicek per 30 September 2026, tetapi pembulatan belum dicocokkan dengan hitungan otomatis Coretax dan data bukti potong di Coretax bisa berbeda. Anggap hasilnya sebagai hitungan pembanding — Coretax yang final.

**3. Kasus apa yang tidak bisa?**
SPT badan, pisah harta/memilih terpisah, penghasilan luar negeri, rugi usaha, dan WNA datang/pergi di tengah tahun. Untuk itu, skill akan menyarankan konsultan pajak atau Kring Pajak 1500200.

## Riwayat versi
- **Catatan revisi 1.0.4 (2026-10-01)** — Tenggat pemberitahuan NPPN tahun berjalan (31 Maret, PMK 81/2024 Ps. 450 ayat (2)) kini dibandingkan script dengan tanggal hari ini (`nppn_tahun_berjalan`). Bila sudah lewat, skill tidak lagi menyarankan tanggal yang sudah lewat: tahun pajak berjalan dianggap memilih pembukuan (UU PPh Ps. 14 ayat (5)) → mulai catat pembukuan; pemberitahuan berikutnya untuk tahun pajak berikutnya, dengan peringatan penguncian pembukuan (PMK 81/2024 Ps. 463 s.t.d.d. PMK 1/2026) yang perlu dikonfirmasi ke KPP. Tes ditambahkan. Tetap ⚠️ PERLU REVIEW konsultan pajak.
- **Catatan revisi 1.0.3 (2026-10-01)** — Fakta pajak: jasa yang diterima orang pribadi (konsultan/freelancer) dipotong klien dengan **PPh 21 bukan pegawai** (BP21, PMK 168/2023), bukan PPh 23. Opsi baru `--final-salah-skema`: PPh final 0,5% yang terlanjur disetor atas pekerjaan bebas tidak dikreditkan dan **tidak** dilaporkan di Lampiran 2; diarahkan ke permohonan pengembalian pajak yang seharusnya tidak terutang lewat Coretax (pemindahbukuan umumnya tidak bisa, PMK 81/2024 Ps. 109 ayat (3)) + konfirmasi KPP/konsultan. Tetap ⚠️ PERLU REVIEW konsultan pajak.
- **1.0.1 (2026-09-30)** — Koreksi batas lapor TP 2025: jatuh tempo tetap 31 Maret 2026; KEP-55/PJ/2026 hanya menghapus sanksi bila lapor/bayar s.d. 30 April 2026 (bukan perpanjangan). Peringatan baru untuk karyawan 1 kantor yang hasilnya kurang/lebih bayar: cek ulang bukti potong A1 dengan HRD dulu. Pesan error ramah untuk angka negatif; "5,054 miliar" kini diterima. Penjelasan beda PPh final 0,5% (usaha) vs pekerjaan bebas (PP 20/2026).
- **1.0.0 (2026-09-30)** — Rilis pertama.

---
_Alat bantu hitung, bukan konsultan pajak. Tidak berafiliasi dengan Direktorat Jenderal Pajak._
