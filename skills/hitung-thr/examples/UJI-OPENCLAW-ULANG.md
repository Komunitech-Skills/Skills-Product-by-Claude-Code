# Uji ulang OpenClaw — hitung-thr 1.0.4

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech` (jawaban dilayani `claude-sonnet-5`). Home baru `sol2-thr` (dibuat ulang lewat script reset sebelum skenario). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama (uji OpenClaw sebelumnya, keluaran `hasil/t-tes1.txt`). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran).
Home `sol2-thr` hanya berisi skill `hitung-thr`.

## Cacat lama (uji sebelumnya, versi < 1.0.4)
Keluaran lama dibuka dengan *"Masa kerja Budi — maaf, karyawan Anda — …"* (nama contoh dari skill bocor) dan menulis *"Rincian THR Idul Fitri 1449 H"* (salah; Idul Fitri 2027 = 1448 H). Skor lama tidak tercatat di repo; penguji menilainya ±6/10 dari keluaran itu.

## Pesan member (giliran 1)
> Halo, hitungin THR karyawan saya dong. Gajinya 4,5 juta sebulan, mulai kerja 1 Maret 2026, lebarannya 20 Maret 2027.

## Giliran 1 — alat `read, memory_search, tool_call` (30 dtk)
> Sebelum saya hitung, saya perlu 2 info tambahan ya:
>
> 1. **Nama karyawan** — untuk ditulis di rincian (saya tidak boleh pakai nama contoh dari skill).
> 2. **Status PTKP** (TK/0, K/1, dst.) — opsional. Kalau tidak disebutkan, saya hanya hitung THR-nya saja tanpa potongan PPh 21 tambahan.
>
> Catatan sementara dari data yang sudah ada:
> - Mulai kerja 1 Maret 2026 s.d. Idul Fitri 20 Maret 2027 → masa kerja 12 bulan 20 hari → **≥12 bulan, jadi THR penuh 1 bulan gaji**.
> - Karena tahun Hijriah-nya tidak Anda sebutkan, saya akan tulis "Idul Fitri 2027" saja (tanpa embel-embel tahun Hijriah) kecuali Anda ingin saya cek dengan tool konversi kalender.
> - Nama usaha untuk judul rincian — boleh sebutkan, atau saya pakai "Usaha Anda" saja.
>
> Boleh balas nama karyawannya (dan PTKP/nama usaha kalau mau) biar langsung saya hitungkan lengkap?

## Giliran 2
Uji sebelumnya tidak punya giliran 2. Penguji menjawab sekali sebagai member awam: *"ga usah pake nama, langsung aja"*. Alat `exec` (35 dtk).

> **Rincian THR Idul Fitri 2027 — Usaha Anda**
> Hari raya: Sabtu, 20 Maret 2027 · **Batas bayar (H-7): Sabtu, 13 Maret 2027** · Rencana bayar: Sabtu, 13 Maret 2027
>
> | Nama | Status | Masa kerja | Upah 1 bulan | Rumus | THR | PPh 21 karena THR | THR diterima |
> |---|---|---:|---:|---|---:|---:|---:|
> | Karyawan 1 | Tetap (PKWTT) | 12 bln | Rp 4.500.000 | masa kerja ≥ 12 bulan → 1 × upah | **Rp 4.500.000** | – | Rp 4.500.000 |
> | **Total** | | | | | **Rp 4.500.000** | **Rp 0** | **Rp 4.500.000** |
>
> Catatan:
> - Status PTKP tidak diisi, jadi potongan PPh 21 atas THR belum dihitung. Kalau mau sekalian, kasih tahu status PTKP-nya (mis. TK/0, K/1).
> - THR wajib dibayar penuh (tidak dicicil) paling lambat 7 hari sebelum hari raya. Terlambat bayar: denda 5% dari total THR, dan THR tetap wajib dibayar (Permenaker 6/2016 Pasal 10).
> - THR bukan dasar iuran BPJS.
> - Masa kerja dihitung bulan penuh inklusif sampai tanggal hari raya (1 Mar 2026 s.d. 20 Mar 2027 = 12 bulan lebih 19 hari → tetap dihitung 12 bulan, jadi THR penuh).
>
> **Draf pengumuman untuk karyawan** (tanpa nominal pribadi, siap kirim):
>
> ```
> Yth. Rekan-rekan karyawan Usaha Anda,
>
> Menyambut Idul Fitri 2027, perusahaan akan membayarkan Tunjangan Hari Raya (THR) Keagamaan pada Sabtu, 13 Maret 2027 (paling lambat 7 hari sebelum hari raya).
>
> Ketentuan besaran THR (Permenaker 6/2016 & SE Menaker M/3/HK.04.00/III/2026):
> • Masa kerja 12 bulan atau lebih: 1 bulan upah (gaji pokok + tunjangan tetap).
> • Masa kerja 1 s.d. kurang dari 12 bulan: masa kerja ÷ 12 × 1 bulan upah.
> • THR dibayar penuh, tidak dicicil, dan dikenai PPh 21 sesuai ketentuan pajak.
>
> Rincian THR masing-masing akan disampaikan secara pribadi. Ada pertanyaan, silakan hubungi HR/keuangan.
>
> Selamat menyambut hari raya. Terima kasih atas kerja keras Bapak/Ibu.
>
> Salam,
> Manajemen Usaha Anda
> ```
>
> _Alat bantu hitung, bukan nasihat hukum/pajak. Dasar: Permenaker 6/2016, SE Menaker M/3/HK.04.00/III/2026, PP 58/2023 & PMK 168/2023 (PPh 21 TER). Untuk sengketa hubungi Disnaker/Posko THR (poskothr.kemnaker.go.id)._
>
> Tidak ada file CSV yang dibuat untuk perhitungan ini (dihitung langsung via command, bukan dari file), jadi tidak ada data sensitif yang tersimpan di disk. Kalau mau sekalian hitung PPh 21-nya, tinggal kasih status PTKP.

## Verifikasi independen
- Masa kerja 1 Mar 2026 s.d. 20 Mar 2027 = 12 bulan 19 hari (inklusif 20 hari) → ≥ 12 bulan → THR = 1 × 4.500.000 = **Rp4.500.000** ✔ (Permenaker 6/2016 Ps. 3).
- 20 Mar 2027 = Sabtu, H-7 = Sabtu 13 Mar 2027 ✔ (secara aritmetika).
- **Tanggal dari pengguna keliru:** Idul Fitri 1448 H diperkirakan ±10 Maret 2027. Script skill sendiri (`tahun_hijriah.py 2027-03-20`) mengeluarkan *"2027-03-20 = 11 Syawal 1448 H"*, bukan 1 Syawal — tanda jelas tanggalnya salah. Bila Lebaran 10 Maret, batas bayar sebenarnya **Rabu, 3 Maret 2027**. Balasan menetapkan rencana bayar 13 Maret, **setelah** Lebaran yang sebenarnya, jadi member berisiko telat dan terkena denda 5%. Nilai THR tidak berubah (masa kerja tetap ≥ 12 bulan s.d. 10 Mar 2027).
- Dasar yang dikutip untuk Lebaran 2027 adalah *"SE Menaker M/3/HK.04.00/III/2026"*, SE untuk Lebaran 2026, bukan 2027 (sama seperti keluaran lama).
- Kolom *"PPh 21 karena THR: –"* tetapi baris total *"Rp 0"*: tidak konsisten. PPh belum dihitung, bukan nol.

## Penilaian
- **Cacat lama hilang: YA.** Tidak ada "Budi"; dipakai *"Karyawan 1"* dan *"Usaha Anda"*. Tidak ada "1449 H"; ditulis *"Idul Fitri 2027"* tanpa tahun Hijriah.
- **Regresi baru:** giliran 1 **bertanya nama karyawan dulu** (*"saya tidak boleh pakai nama contoh dari skill"*), padahal SKILL.md 1.0.4 sendiri menyuruh memakai "Karyawan 1" bila nama tidak ada. Akibatnya hitungan lengkap baru keluar di giliran 2. Kalimat itu juga membocorkan urusan internal skill ke member.
- **Tanggal Lebaran keliru tidak ditanggapi** (lihat verifikasi). Agent tidak menjalankan `tahun_hijriah.py`, padahal script itu bisa mendeteksi 20 Maret = 11 Syawal.
- **Skor: 7/10** (lama ±6). Angka benar dan cacat lama hilang, tetapi ada satu giliran tambahan yang tidak perlu dan risiko salah tanggal bayar yang lolos.
- Saran: (1) SKILL.md: "jangan menanyakan nama — langsung pakai Karyawan 1"; (2) `tahun_hijriah.py`/`thr.py` memberi peringatan bila tanggal hari raya bukan ±2 hari dari 1 Syawal/10 Dzulhijjah tabular ("tanggal yang Anda sebut = 11 Syawal; Idul Fitri 1448 H diperkirakan ±10 Maret 2027 — mohon cek pengumuman Kemenag"), dan agent wajib menjalankan cek ini untuk Idul Fitri/Idul Adha; (3) kutip SE THR "tahun berjalan (terbit menjelang hari raya)" bila SE tahun itu belum ada; (4) kolom PPh yang belum dihitung ditulis "belum dihitung" di baris total juga.
