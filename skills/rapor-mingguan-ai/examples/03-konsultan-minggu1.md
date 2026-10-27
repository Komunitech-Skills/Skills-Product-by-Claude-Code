# Contoh 3: bot konsultan bisnis, minggu pertama

Percakapan fiktif. Data lengkap: `data/03-konsultan-minggu1.txt`.

> **FORMAT LAMA (sebelum 1.0.3), hanya untuk contoh ISI penilaian.** Jangan tiru bentuknya: tabel 4 kolom, tanpa baris "Angka tren", tanpa penutup "Balas 'rinci'", dan lebih panjang dari batas chat. Format terkini: `06-format-ringkas-chat.md` (data yang sama dengan contoh 2) dan `01-skincare-minggu2.md`. Angka di sini milik data contoh ini; jangan disalin.

## Input pengguna
"Bot saya baru dipasang kemarin untuk menerima calon klien konsultasi. Ada 7 percakapan, mohon dinilai. Tarif sesi 60 menit adalah Rp1.500.000."

## Hasil yang diharapkan

**Ringkasan:** 7 percakapan dinilai (sedikit, jadi nilai ini baru gambaran awal), nilai umum **C**. Untuk bot yang baru sehari, banyak yang sudah benar; dua hal yang harus segera diajarkan adalah tarif dan cara menjawab "apakah pasti naik omzet?".

| Kriteria | Lolos | Nilai |
|---|---|---|
| Fakta benar | 71,4% (5 dari 7) | D |
| Nyambung | 85,7% (6 dari 7) | B |
| Ingat konteks | 100% | A |
| Panjang pas | 71,4% (5 dari 7) | C |
| Nada brand | 100% | A |
| Tidak janji berlebihan | 85,7% (6 dari 7) | C |
| Data pribadi aman | 100% | A |
| Bebas kata teknis | 100% | A |

**Dibanding tahap:** di minggu pertama bot masih "bayi": target 60% untuk kriteria biasa dan semuanya sudah terlewati. Kesalahan fakta wajar di minggu ini karena bot belum diberi daftar harga; yang tidak boleh ditoleransi di tahap apa pun adalah janji hasil bisnis ("pasti naik omzet 30%").

**3 kesalahan paling sering:**
1. Fakta salah (L2 dan L4): tarif disebut Rp750.000 (yang benar Rp1.500.000), dan klaim "terbukti di semua klien" tidak ada dasarnya.
2. Panjang tidak pas (L5 terlalu panjang, L6 hanya "Ya." untuk pertanyaan lokasi).
3. Janji berlebihan (L4): "pasti naik omzet 30% dalam sebulan".

**PR minggu ini:**

1. *Tarif dan klaim hasil (L2, L4).* Tempel:
> Tarif sesi konsultasi 60 menit: Rp1.500.000. Jangan menyebut tarif lain atau paket yang tidak ada di sini. Jangan pernah menjanjikan kenaikan omzet atau angka hasil. Jika ditanya hasil, jawab: "Hasilnya bergantung pada kondisi bisnis dan penerapannya, jadi saya tidak bisa menjanjikan angka. Di sesi pertama kita petakan masalahnya dan tentukan langkah yang realistis."

2. *Panjang jawaban (L5, L6).* Tempel:
> Jawab pertanyaan sederhana dalam 1-3 kalimat yang menjawab langsung. Jika ditanya lokasi dan belum ada alamat di catatan ini, jawab: "Alamat kantor saya konfirmasikan dulu ke tim, atau kita bisa bertemu online lewat Zoom atau Google Meet." Alamat kantor: [isian: alamat].

3. *Portofolio (L5).* Tempel:
> Jika diminta portofolio, jawab singkat: "Ringkasan portofolio kami kirim setelah perkenalan singkat. Boleh saya tahu bidang usaha Kakak dan tujuan utamanya?" Jangan menyebut jumlah klien, tahun, atau industri tertentu yang tidak ada di catatan.

**Perlu keputusan Anda:**
1. Klaim "terbukti di semua klien" (L4) tidak punya dasar. Apakah ada data hasil klien yang boleh disebut? Selama belum ada, bot tidak boleh mengklaim.
2. Alamat kantor dan kebijakan pertemuan tatap muka.
3. Apakah portofolio boleh dikirim otomatis, atau harus lewat Anda?

**Asumsi dan pertanyaan:** Tahap minggu pertama. (1) Berapa tarif paket 4 sesi, bila ada? (2) Nada yang diinginkan: formal atau santai? (3) Bisa tambah 10-15 percakapan lagi minggu depan agar rapor lebih kuat?
