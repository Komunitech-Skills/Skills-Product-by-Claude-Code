# SPT Tahunan Beres Sebelum Buka Coretax

**Ceritakan penghasilan setahun dengan bahasa biasa — dapat hitungan kurang bayar, lebih bayar, atau nihil untuk SPT Tahunan (laporan pajak tahunan) orang pribadi, lengkap dengan daftar dokumen yang harus disiapkan.**

Diuji AI penguji independen di OpenClaw: rata-rata 3,75 → 8,5 dari 10 pada uji lengkap terakhir (2 skenario, versi 1.0.3, 1 Okt 2026). Skenario dengan beda terbesar, konsultan IT yang memakai PPh final 0,5%, diuji ulang di versi 1.0.5 (3 Okt 2026): 2 → 9 (tanpa skill AI menganggap konsultan IT boleh memakai 0,5% dan menulis batas lapor 31 Maret 2026 tanpa menyebut sudah lewat; dengan skill pekerjaan bebas dan NPPN diluruskan, keterlambatan disebut, dan kurang bayar dihitung).

> ⚠️ **Alat bantu hitung, bukan nasihat pajak dan bukan konsultan pajak.** Pembulatan belum dicocokkan dengan Coretax (sistem pajak online Direktorat Jenderal Pajak/DJP); Coretax yang final. Tidak berafiliasi dengan Direktorat Jenderal Pajak.

> **Formulir lama vs Coretax:** untuk tahun pajak 2025 dan seterusnya, SPT Tahunan orang pribadi dilaporkan lewat **SPT Tahunan OP di Coretax** — satu formulir dinamis yang **menggantikan formulir 1770 seri lama (1770, 1770 S, 1770 SS) sejak tahun pajak 2025** (PER-11/PJ/2025). Bila di FAQ atau artikel DJP Anda masih menemukan penjelasan formulir 1770, itu formulir lama untuk tahun pajak sebelum 2025; skill ini memetakan angka ke SPT OP Coretax.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Tidak kaget di Coretax: dapat perkiraan sejak awal berapa pajak yang harus disetor (atau dikembalikan) dan alasannya
- ✅ Angka dihitung skrip dengan tarif Pasal 17 UU HPP (Harmonisasi Peraturan Perpajakan) & PTKP (penghasilan tidak kena pajak) resmi — PKP (penghasilan kena pajak) dibulatkan sesuai aturan, bukan dikira-kira
- ✅ Menangani kasus yang sering bikin bingung: pindah kerja (2 bukti potong A1, yaitu bukti potong PPh 21 dari kantor), karyawan + usaha sampingan, freelancer NPPN (cara menghitung pajak dari persentase penghasilan, tanpa pembukuan), zakat, suami-istri digabung
- ✅ Peta "angka ini masuk bagian mana" di SPT Tahunan OP Coretax (laporan pajak tahunan), yang menggantikan formulir 1770 seri lama sejak tahun pajak 2025 (PER-11/PJ/2025)
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
- Uji lengkap terakhir (versi 1.0.3, 1 Okt 2026), rata-rata 2 skenario: tanpa skill **3,75** → dengan skill **8,5** (selisih +4,75). Karyawan pindah kerja dengan 2 bukti potong A1: **6** → **9**; kedua sisi menghitung kurang bayar Rp4.125.000 dengan benar, pembedanya prosedur Coretax (tanpa skill masih menyuruh memakai formulir 1770 S lama, padahal sejak tahun pajak 2025 sudah diganti SPT OP Coretax) dan status tenggat. Konsultan IT yang memakai PPh final 0,5%: **1,5** → **8**; tanpa skill menyimpulkan lebih bayar Rp1.900.000 (keliru), dengan skill pekerjaan bebas dan NPPN diluruskan dan kurang bayar Rp14.400.000 dihitung. Putaran ini belum lulus karena satu saran tanggal yang sudah lewat (pemberitahuan NPPN tahun 2026); diperbaiki di versi 1.0.4, dan pada uji ulang kesalahan itu tidak muncul lagi (2 dari 2 sesi, skor dengan skill 9). Uji pertama (1 Okt 2026, versi sebelumnya): rata-rata 4,75 → 8,75.
- Uji ulang versi terbaru 1.0.5 (3 Okt 2026), hanya kasus konsultan IT: tanpa skill **2** → dengan skill **9** (LULUS). Tanpa skill AI menulis "Deadline lapor: 31 Maret 2026" tanpa menyebut sudah lewat dan memakai formulir lama; dengan skill baris pertama menyebut sudah terlambat 186 hari (pada tanggal uji), denda Rp100.000, dan kurang bayar Rp14.400.000 dihitung. Penguji menyarankan hasilnya tetap dicek konsultan pajak.
- Bot Telegram uji (bot OpenClaw asli di grup uji Komunitech), 3 Okt 2026: tanpa skill tidak memberi jawaban; dengan skill skema pajaknya diluruskan dan kurang bayar Rp14.400.000 dihitung setelah giliran lanjutan.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent) dan di bot Telegram uji. Claude Code (simulasi agent). Codex dan Cursor belum kami uji langsung. Hasil hitungan adalah pembanding, bukan pengganti pelaporan ke DJP (lihat peringatan di atas).

## FAQ
**1. Apakah skill ini melaporkan SPT saya ke DJP?**
Tidak. Skill hanya menghitung dan menyiapkan checklist. Pelaporan tetap Anda lakukan sendiri di Coretax (atau lewat konsultan). Jangan pernah membagikan password atau kode otorisasi Coretax ke siapa pun, termasuk AI.

**2. Apakah hasilnya sama persis dengan Coretax?**
Rumus dan tarif mengikuti aturan resmi yang dicek per 30 September 2026 (rujukan batas lapor, PTKP, tarif, PPh final 0,5%, dan bentuk SPT dicek ulang 14 Oktober 2026), tetapi pembulatan belum dicocokkan dengan hitungan otomatis Coretax dan data bukti potong di Coretax bisa berbeda. Anggap hasilnya sebagai hitungan pembanding — Coretax yang final.

**3. Kasus apa yang tidak bisa?**
SPT badan, pisah harta/memilih terpisah, penghasilan luar negeri, rugi usaha, dan WNA datang/pergi di tengah tahun. Untuk itu, skill akan menyarankan konsultan pajak atau Kring Pajak 1500200.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
