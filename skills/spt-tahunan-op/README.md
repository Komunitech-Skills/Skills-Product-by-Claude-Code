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

---
_Alat bantu hitung, bukan konsultan pajak. Tidak berafiliasi dengan Direktorat Jenderal Pajak._
