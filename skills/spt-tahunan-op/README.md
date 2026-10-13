# SPT Tahunan Beres Sebelum Buka Coretax

**Ceritakan penghasilan setahun dengan bahasa biasa — langsung tahu kurang bayar, lebih bayar, atau nihil, lengkap dengan daftar dokumen yang harus disiapkan.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

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
Salin folder `spt-tahunan-op` ke folder skills AI agent kamu (OpenClaw, Codex, Claude Code, Cursor). Lokasi lengkap per platform: **`docs/instalasi.md`**. Script memakai Python standar (tanpa instal paket); bila Python tidak ada, agent menghitung manual dengan rumus yang sama.

**Hasil uji (angka nyata):** uji OpenClaw sebelum/sesudah otomatis agent, 2026-10-01, skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Rata-rata 2 skenario: tanpa skill **4,75** → dengan skill **8,75** (LULUS; selisih +4,0).
- Skenario jebakan (konsultan IT pakai PPh final 0,5%): tanpa skill **3** → dengan skill **8,5** (meluruskan pekerjaan bebas + NPPN/Coretax, bukan nihil/lebih bayar).
- Bot Telegram asli (gelombang 4, 2026-10-03): TANPA tidak memberi jawaban; DENGAN meluruskan skema pajak dan menghitung kurang bayar Rp14.400.000 setelah giliran lanjutan.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent + bot Telegram asli gelombang 4). Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung. Angka simulasi belum dicocokkan dengan Coretax resmi — gunakan sebagai pembanding, bukan pengganti pelaporan DJP.

## FAQ
**1. Apakah skill ini melaporkan SPT saya ke DJP?**
Tidak. Skill hanya menghitung dan menyiapkan checklist. Pelaporan tetap kamu lakukan sendiri di Coretax (atau lewat konsultan). Jangan pernah membagikan password atau kode otorisasi Coretax ke siapa pun, termasuk AI.

**2. Apakah hasilnya pasti sama dengan Coretax?**
Rumus dan tarif mengikuti aturan resmi yang dicek per 30 September 2026, tetapi pembulatan belum dicocokkan dengan hitungan otomatis Coretax dan data bukti potong di Coretax bisa berbeda. Anggap hasilnya sebagai hitungan pembanding — Coretax yang final.

**3. Kasus apa yang tidak bisa?**
SPT badan, pisah harta/memilih terpisah, penghasilan luar negeri, rugi usaha, dan WNA datang/pergi di tengah tahun. Untuk itu, skill akan menyarankan konsultan pajak atau Kring Pajak 1500200.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
