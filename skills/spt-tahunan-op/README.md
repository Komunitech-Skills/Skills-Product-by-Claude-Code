# SPT Tahunan Beres Sebelum Buka Coretax

**Ceritakan penghasilan setahun dengan bahasa biasa — dapat hitungan kurang bayar, lebih bayar, atau nihil untuk SPT Tahunan (laporan pajak tahunan) orang pribadi, lengkap dengan daftar dokumen yang harus disiapkan.**

Diuji AI penguji independen di OpenClaw: 4,75 → 8,75 dari 10 pada uji pertama (pada kasus konsultan IT yang memakai PPh final 0,5%, AI tanpa skill salah menyimpulkan nihil/lebih bayar; dengan skill pekerjaan bebas dan NPPN diluruskan dan kurang bayar dihitung); uji ulang terakhir pada kasus konsultan itu: 2 → 9.

> ⚠️ **Alat bantu hitung, bukan nasihat pajak dan bukan konsultan pajak.** Pembulatan belum dicocokkan dengan Coretax (sistem pajak online Direktorat Jenderal Pajak/DJP); Coretax yang final. Tidak berafiliasi dengan Direktorat Jenderal Pajak.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak kaget di Coretax: dapat perkiraan sejak awal berapa pajak yang harus disetor (atau dikembalikan) dan alasannya
- ✅ Angka dihitung skrip dengan tarif Pasal 17 UU HPP (Harmonisasi Peraturan Perpajakan) & PTKP (penghasilan tidak kena pajak) resmi — PKP (penghasilan kena pajak) dibulatkan sesuai aturan, bukan dikira-kira
- ✅ Menangani kasus yang sering bikin bingung: pindah kerja (2 bukti potong A1, yaitu bukti potong PPh 21 dari kantor), karyawan + usaha sampingan, freelancer NPPN (cara menghitung pajak dari persentase penghasilan, tanpa pembukuan), zakat, suami-istri digabung
- ✅ Peta "angka ini masuk bagian mana" di formulir SPT (laporan pajak tahunan) Coretax yang baru (1770/1770S sudah dihapus)
- ✅ Checklist dokumen pribadi: bukti potong, harta, utang, bukti zakat, bukti setor — tinggal centang

## Cocok untuk siapa
- Karyawan yang tahun lalu pindah kerja atau punya dua kantor
- Freelancer, desainer, penulis, konsultan, dokter/pengacara praktik mandiri yang memakai norma (NPPN)
- Karyawan yang punya usaha sampingan / toko online (PPh final 0,5%, yaitu pajak final atas omzet usaha kecil)
- Siapa pun yang ingin mengecek hitungan sebelum melapor sendiri atau menyerahkan ke konsultan

## Contoh sebelum & sesudah
**Sebelum:** Buka Coretax, tiba-tiba muncul "kurang bayar Rp5,7 juta" setelah memasukkan dua bukti potong — tidak tahu itu benar atau salah, lalu panik.

**Sesudah (cukup ketik):** "Tahun 2025 saya pindah kerja bulan Juli. Di A1 kantor lama penghasilan neto 90 juta, PPh 21 dipotong 1.350.000. Kantor baru neto 60 juta, PPh 21-nya nol. Saya menikah, anak satu. SPT saya nanti gimana?"

Cuplikan hasil (dipotong; contoh uji simulasi dengan data fiktif, tanggal acuan 30 Sep 2026, dari `examples/01-dua-pemberi-kerja.md`):
```
2. PTKP & Penghasilan Kena Pajak (PKP)
- PTKP K/1: Rp 63.000.000
- PKP = Rp 150.000.000 − Rp 63.000.000 = Rp 87.000.000 → dibulatkan ke bawah ribuan: Rp 87.000.000

3. PPh terutang (tarif Pasal 17 UU HPP)
- 5% × Rp 60.000.000 = Rp 3.000.000
- 15% × Rp 27.000.000 = Rp 4.050.000
- PPh terutang: Rp 7.050.000

4. Kredit pajak (sudah dipotong/dibayar)
- Total kredit: Rp 1.350.000

5. Hasil: KURANG BAYAR
PPh terutang Rp 7.050.000 − kredit Rp 1.350.000 = Rp 5.700.000 harus disetor (PPh Pasal 29) sebelum lapor.
…
```
(K/1 = menikah dengan satu tanggungan anak; PPh Pasal 29 = kekurangan pajak yang disetor sebelum melapor.) Hasil lengkapnya juga memuat penjelasan sederhana kenapa kurang bayar (dua kantor sama-sama memakai PTKP penuh), langkah bayar lewat kode billing (kode pembayaran dari Coretax), dan checklist dokumen.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Hitung SPT tahunan saya: karyawan TK/0, di A1 neto 114 juta, PPh 21 dipotong 3 juta."
- "Saya freelancer desain di Bandung, penghasilan 2025 240 juta, sudah lapor NPPN. Kurang bayar berapa?"
- "Karyawan K/2 plus usaha jasa, zakat ke BAZNAS 5 juta — pajak tahunan saya berapa?"

## Instalasi singkat
Salin folder `spt-tahunan-op` ke folder skills AI agent Anda (OpenClaw, Codex, Claude Code, Cursor). Lokasi lengkap per platform: **`docs/instalasi.md`** (di dalam paket bernama `CARA-INSTAL.md`). Skrip memakai Python standar (tanpa instal paket); bila Python tidak ada, agent menghitung manual dengan rumus yang sama.

**Hasil uji (angka nyata):** uji OpenClaw sebelum/sesudah otomatis agent, skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Uji pertama (1 Okt 2026), rata-rata 2 skenario: tanpa skill **4,75** → dengan skill **8,75** (LULUS; selisih +4,0). Kasus karyawan pindah kerja dengan 2 bukti potong A1: kedua sisi menghitung angkanya dengan benar (6,5 → 9); pembedanya prosedur Coretax dan status tenggat. Kasus jebakan (konsultan IT pakai PPh final 0,5%): tanpa skill **3** → dengan skill **8,5** (meluruskan pekerjaan bebas + NPPN/Coretax, bukan nihil/lebih bayar).
- Uji ulang v1.0.5 (3 Okt 2026), hanya kasus konsultan IT: tanpa skill **2** → dengan skill **9**. Tanpa skill AI menulis "Deadline lapor: 31 Maret 2026" tanpa menyebut sudah lewat dan memakai formulir lama; dengan skill baris pertama menyebut sudah terlambat 186 hari (pada tanggal uji), denda Rp100.000, dan kurang bayar Rp14.400.000 dihitung. Penguji menyarankan hasilnya tetap dicek konsultan pajak.
- Bot Telegram uji (bot OpenClaw asli di grup uji Komunitech), 3 Okt 2026: tanpa skill tidak memberi jawaban; dengan skill skema pajaknya diluruskan dan kurang bayar Rp14.400.000 dihitung setelah giliran lanjutan.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan di bot Telegram uji. Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung. Hasil hitungan adalah pembanding, bukan pengganti pelaporan ke DJP (lihat peringatan di atas).

## FAQ
**1. Apakah skill ini melaporkan SPT saya ke DJP?**
Tidak. Skill hanya menghitung dan menyiapkan checklist. Pelaporan tetap Anda lakukan sendiri di Coretax (atau lewat konsultan). Jangan pernah membagikan password atau kode otorisasi Coretax ke siapa pun, termasuk AI.

**2. Apakah hasilnya sama persis dengan Coretax?**
Rumus dan tarif mengikuti aturan resmi yang dicek per 30 September 2026, tetapi pembulatan belum dicocokkan dengan hitungan otomatis Coretax dan data bukti potong di Coretax bisa berbeda. Anggap hasilnya sebagai hitungan pembanding — Coretax yang final.

**3. Kasus apa yang tidak bisa?**
SPT badan, pisah harta/memilih terpisah, penghasilan luar negeri, rugi usaha, dan WNA datang/pergi di tengah tahun. Untuk itu, skill akan menyarankan konsultan pajak atau Kring Pajak 1500200.

## Riwayat perubahan

Versi terkini: **1.0.5**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
