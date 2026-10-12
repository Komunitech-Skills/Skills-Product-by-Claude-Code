# Uji OpenClaw sebelum/sesudah: jadwal-pelajaran-sekolah

- **Tanggal:** 2026-10-12
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill)
- **Cara uji:** OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `claude-sonnet-5` (sama dengan bot member). SEBELUM = home tanpa skill; SESUDAH = home berisi hanya `jadwal-pelajaran-sekolah`. Home dibuat ulang bersih per skenario. Pesan dan data identik di kedua sisi (data fiktif ditaruh di folder kerja agent). Skenario 1 juga dijalankan dalam konteks kanal Telegram di kedua sisi (`--channel telegram`, tanpa mengirim). Skenario 2 sisi SEBELUM: dua percobaan pertama kena timeout router (hasil kosong), percobaan ketiga yang dipakai.
- **Verifikasi independen:** semua jadwal (dari blok CSV di chat atau dari berkas yang ditulis agent) diurai ulang dengan python sendiri: bentrok guru/kelas/lab, jumlah jam per kegiatan, batas slot per hari, hari hadir Pak Budi, jam bolong.
- **Alat yang dipanggil agent:** lihat baris "Skill/script terpakai?" tiap skenario. Catatan: di lingkungan uji, agent SEBELUM punya pustaka `ortools`, `openpyxl`, `reportlab` sehingga membuat PDF/XLSX sendiri; di komputer pembeli awam pustaka ini belum tentu ada.

<details><summary>Data uji skenario 1 (kebutuhan-mengajar.csv + info-sekolah.txt)</summary>

```csv
Guru,Mapel,Kelas yang diajar,JP per kelas per minggu
Bu Siti Rahma,Matematika,"7A, 7B, 8A, 8B, 9A, 9B",4
Pak Rudi Hartono,Bahasa Indonesia,"7A, 7B, 8A, 8B, 9A, 9B",4
Bu Ani Lestari,Bahasa Inggris,"7A, 7B, 8A, 8B, 9A, 9B",3
Pak Agus Santoso,IPA,"7A, 7B, 8A, 8B, 9A, 9B",4
Bu Dewi Kusuma,IPS,"7A, 7B, 8A, 8B, 9A, 9B",3
Pak Hasan Basri,PPKn,"7A, 7B, 8A, 8B, 9A, 9B",2
Bu Nurul Hidayah,Pendidikan Agama Islam,"7A, 7B, 8A, 8B, 9A, 9B",2
Pak Yoga Pratama,PJOK,"7A, 7B, 8A, 8B, 9A, 9B",2
Bu Maya Sari,Seni Budaya,"7A, 7B, 8A, 8B, 9A, 9B",2
Pak Budi Setiawan,Informatika,"7A, 7B, 8A, 8B, 9A, 9B",2
```
```
Catatan sekolah SMP Harapan Bangsa (fiktif):
- Senin-Jumat, 6 jam pelajaran per hari, 1 JP = 40 menit, mulai 07.00
- Istirahat setelah jam ke-3 (15 menit)
- Jumat pendek: hanya 5 jam pelajaran
```
</details>

<details><summary>Data uji skenario 2 (kebutuhan-b.csv + info-b.txt)</summary>

```csv
Guru,Mapel,Kelas,JP/minggu,Keterangan
Bu Siti Rahma,Matematika,7A,4,
Bu Siti Rahma,Matematika,7B,4,
Bu Siti Rahma,Matematika,8A,4,
Bu Siti Rahma,Matematika,8B,4,
Pak Rudi Hartono,Bahasa Indonesia,7A,4,
Pak Rudi Hartono,Bahasa Indonesia,7B,4,
Pak Rudi Hartono,Bahasa Indonesia,8A,4,
Pak Rudi Hartono,Bahasa Indonesia,8B,4,
Pak Agus Santoso,IPA (teori),7A,2,
Pak Agus Santoso,IPA (teori),7B,2,
Pak Agus Santoso,IPA (teori),8A,2,
Pak Agus Santoso,IPA (teori),8B,2,
Pak Agus Santoso,IPA praktikum,7A,2,wajib di Lab IPA
Pak Agus Santoso,IPA praktikum,7B,2,wajib di Lab IPA
Pak Agus Santoso,IPA praktikum,8A,2,wajib di Lab IPA
Pak Agus Santoso,IPA praktikum,8B,2,wajib di Lab IPA
Bu Ani Lestari,Bahasa Inggris,7A,3,
Bu Ani Lestari,Bahasa Inggris,7B,3,
Bu Ani Lestari,Bahasa Inggris,8A,3,
Bu Ani Lestari,Bahasa Inggris,8B,3,
Pak Budi Setiawan,Informatika,7A,2,guru paruh waktu: hanya hadir Selasa dan Kamis
Pak Budi Setiawan,Informatika,7B,2,guru paruh waktu: hanya hadir Selasa dan Kamis
Pak Budi Setiawan,Informatika,8A,2,guru paruh waktu: hanya hadir Selasa dan Kamis
Pak Budi Setiawan,Informatika,8B,2,guru paruh waktu: hanya hadir Selasa dan Kamis
Pak Yoga Pratama,PJOK,7A,2,
Pak Yoga Pratama,PJOK,7B,2,
Pak Yoga Pratama,PJOK,8A,2,
Pak Yoga Pratama,PJOK,8B,2,
Bu Dewi Kusuma,IPS,7A,3,
Bu Dewi Kusuma,IPS,7B,3,
Bu Dewi Kusuma,IPS,8A,3,
Bu Dewi Kusuma,IPS,8B,3,
```
```
SMP Cahaya Nusantara (fiktif): 4 kelas (7A, 7B, 8A, 8B). Senin-Jumat, 6 JP per hari, Jumat 5 JP. Istirahat setelah jam ke-3.
Lab IPA hanya satu ruang: dalam satu jam pelajaran hanya boleh satu kelas yang praktikum di lab.
```
</details>

<details><summary>Data uji skenario 4 (kebutuhan-d.csv)</summary>

```csv
Guru,Mapel,Kelas,JP,Catatan
Bu Siti Rahma,Matematika,7A,6,
Pak Rudi Hartono,Bahasa Indonesia,7A,6,
Bu Ani Lestari,Bahasa Inggris,7A,5,
Pak Agus Santoso,IPA,7A,6,
Bu Dewi Kusuma,IPS,7A,5,
Pak Yoga Pratama,PJOK,7A,4,
Bu Maya Sari,Seni Budaya,7A,4,
Bu Siti Rahma,Matematika,7B,6,
Pak Rudi Hartono,Bahasa Indonesia,7B,6,
Bu Ani Lestari,Bahasa Inggris,7B,5,
Pak Agus Santoso,IPA,7B,6,
Bu Dewi Kusuma,IPS,7B,5,
Pak Yoga Pratama,PJOK,7B,4,
Bu Maya Sari,Seni Budaya,7B,4,
```
</details>

---

## Skenario 1 (normal utama): SMP 6 kelas, 10 guru, Jumat pendek, istirahat

**Pesan:** "Tolong buatkan jadwal pelajaran SMP kami dari file kebutuhan-mengajar.csv dan info-sekolah.txt. Saya mau jadwal per kelas dan per guru, dan jangan sampai ada guru atau kelas yang bentrok. Kalau bisa ada file yang bisa saya cetak."

**Verifikasi python:** semua kegiatan 60 baris (168 JP) terpenuhi di kedua sisi; bentrok guru 0, bentrok kelas 0, tidak ada slot di luar batas (Jumat 5 jam). Pembeda ada di cara penyajian, bukan di kebenaran penjadwalan.

### SEBELUM (skill mati), mode biasa
> Selesai! Jadwal pelajaran SMP Harapan Bangsa sudah jadi, disusun pakai constraint solver (OR-Tools) supaya **dijamin matematis tidak ada bentrok** — baik bentrok guru (satu guru di dua kelas sekaligus) maupun bentrok kelas (dua mapel bareng di jam yang sama). Sudah divalidasi ulang manual juga, hasilnya bersih.
>
> **Yang saya pakai:**
> - Senin–Kamis 6 JP/hari, Jumat 5 JP/hari, 1 JP = 40 menit mulai 07.00, istirahat 15 menit setelah jam ke-3 (sesuai `info-sekolah.txt`)
> - 10 guru, 6 kelas (7A/7B/8A/8B/9A/9B), total kebutuhan 28 JP/kelas/minggu dari 29 slot tersedia — jadi tiap kelas punya 1 jam kosong/minggu (bisa dipakai utk kegiatan tambahan)
> - Tidak ada mapel yang sama diulang 2x di hari yang sama untuk kelas yang sama
>
> **File yang dihasilkan (siap cetak):**
> - `Jadwal-Pelajaran-SMP-Harapan-Bangsa.pdf` — landscape A4, berisi halaman ringkasan + jadwal tiap 6 kelas + jadwal tiap 10 guru (17 halaman total)
> - `Jadwal-Pelajaran-SMP-Harapan-Bangsa.xlsx` — versi Excel dengan sheet terpisah per kelas & per guru, bisa diedit/diprint ulang sesuai kebutuhan
>
> Kedua file ada di workspace, folder yang sama dengan file sumbernya.

**Nilai SEBELUM: 5,5.** Jadwal benar (168/168, tanpa bentrok; tidak ada mapel yang sama dua kali dalam sehari, jam bolong hanya 1 slot kosong per kelas yang memang sisa), dan PDF/XLSX-nya rapi. Tetapi di chat TIDAK ADA satu pun jadwal: hanya janji "ada di workspace". Pengguna di chat tidak bisa melihat atau menyalin apa pun; menyebut OR-Tools, nama berkas dan folder (jargon).
**Skill/script terpakai?** Tidak (alat: exec, process, ls, read, write; membuat skrip ortools sendiri).

### SESUDAH (skill aktif), mode biasa
> ## Ringkasan
>
> - **Total jam pelajaran yang diminta:** 168 JP/minggu (dari 10 guru × 6 kelas)
> - **Terjadwal:** 168/168 JP (100%)
> - **Bentrok guru/kelas:** 0 (dicek dua kali — sekali dari hasil penjadwalan, sekali verifikasi manual terpisah)
> - **Asumsi dipakai:** Senin–Kamis 6 jam/hari, Jumat 5 jam (sesuai catatan sekolah), 1 JP = 40 menit mulai 07.00, istirahat setelah jam ke-3
>
> ## Jadwal per Kelas (contoh 7A, lengkap di file)
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | 1 | MTK (Bu Siti) | IPS (Bu Dewi) | PPKn (Pak Hasan) | PJOK (Pak Yoga) | IPA (Pak Agus) |
> | 2 | MTK (Bu Siti) | SBD (Bu Maya) | PPKn (Pak Hasan) | B.IND (Pak Rudi) | IPA (Pak Agus) |
> | 3 | MTK (Bu Siti) | PAI (Bu Nurul) | B.ING (Bu Ani) | B.IND (Pak Rudi) | IPA (Pak Agus) |
> | **Istirahat** | — | — | — | — | — |
> | 4 | MTK (Bu Siti) | PAI (Bu Nurul) | B.ING (Bu Ani) | B.IND (Pak Rudi) | IPA (Pak Agus) |
> | 5 | IPS (Bu Dewi) | INF (Pak Budi) | B.ING (Bu Ani) | B.IND (Pak Rudi) | SBD (Bu Maya) |
> | 6 | IPS (Bu Dewi) | INF (Pak Budi) | PJOK (Pak Yoga) | — | — (Jumat 5 jam) |
>
> → 7B, 8A, 8B, 9A, 9B lengkap ada di file `jadwal-per-kelas.md`.
>
> ## Jadwal per Guru (contoh Bu Ani Lestari — B.Inggris, 6 kelas)
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | 1 | B.Ing - 9B | — | — | B.Ing - 7B | B.Ing - 8B |
> | 2 | B.Ing - 9B | — | — | B.Ing - 7B | B.Ing - 8B |
> | 3 | B.Ing - 9B | — | B.Ing - 7A | B.Ing - 8A | B.Ing - 9A |
> | **Istirahat** | — | — | — | — | — |
> | 4 | — | — | B.Ing - 7A | B.Ing - 8A | B.Ing - 9A |
> | 5 | — | — | B.Ing - 7A | B.Ing - 8A | B.Ing - 9A |
> | 6 | — | — | B.Ing - 7B | B.Ing - 8B | — |
>
> → 9 guru lainnya lengkap di `jadwal-per-guru.md`.
>
> ## CSV lengkap (siap ditempel ke Excel/Sheets)
>
> ```csv
> Hari;Jam;Kelas;Mapel;Guru
> Senin;1;7A;Matematika;Bu Siti Rahma
> Senin;1;7B;IPA;Pak Agus Santoso
> Senin;1;8A;Bahasa Indonesia;Pak Rudi Hartono
> Senin;1;8B;PPKn;Pak Hasan Basri
> Senin;1;9A;Pendidikan Agama Islam;Bu Nurul Hidayah
> Senin;1;9B;Bahasa Inggris;Bu Ani Lestari
> ... (168 baris total, file lengkap tersedia)
> ```
>
> ## File yang disiapkan di folder workspace Anda
>
> - `jadwal-pelajaran-cetak.html` — **siap cetak langsung** (buka di browser lalu Print/Save as PDF), berisi grid per kelas dan per guru dengan baris istirahat
> - `jadwal-per-kelas.md` — tabel per kelas (7A–9B)
> - `jadwal-per-guru.md` — tabel per guru (10 guru)
> - `jadwal-pelajaran.csv` — 168 baris, semicolon-separated, siap impor Excel/Sheets
>
>
> ## Cara cetak/bagikan
> 1. Buka `jadwal-pelajaran-cetak.html` di browser → Ctrl+P → Save as PDF atau langsung print.
> 2. CSV bisa ditempel ke Google Sheets untuk diedit atau dikirim ke masing-masing guru.
>
> Jadwal otomatis ini tanpa bentrok sama sekali; kalau nanti mau dioptimalkan lagi (misal menghindari jam kosong guru di tengah hari), bisa diimpor ke software FET — ada panduannya kalau diperlukan.
>
> ## Pertanyaan (opsional, boleh dijawab kapan saja)
> 1. Mau saya hindari "jam bolong" di tengah jadwal guru (misal Bu Ani kosong di Selasa)?
> 2. Perlu alokasi ruang khusus (lab IPA/komputer) dengan batasan 1 kelas per jam?
> 3. Nama mapel di grid pakai singkatan (MTK, B.IND, dst.) — sudah sesuai atau mau nama lengkap?

**Nilai SESUDAH: 6,5.** Angka benar (168/168, bentrok 0; tabel 7A di chat cocok 100% dengan CSV; CSV berkas 168 baris lolos verifikasi). Kurang: (1) jadwal TIDAK utuh di chat: hanya kelas 7A dan satu guru, CSV dipotong "... (168 baris total, file lengkap tersedia)"; (2) menyebut nama berkas dan "folder workspace", melanggar larangan isi hasil; (3) kualitas jadwal: Matematika 4 JP berturut-turut sehari penuh di jam 1-4, IPA 4 jam berturut-turut di Jumat, 22 dari 60 kegiatan (kelas x mapel) ditaruh sebagai blok >=3 jam pelajaran dalam satu hari, dan blok 4 jam melintasi istirahat; model SEBELUM (solver) menyebar rapi; (4) klaim "dicek dua kali".
**Skill/script terpakai?** Ya: skills_read (SKILL.md dimuat), exec; `susun_jadwal.py` menghasilkan penempatan (data-jadwal.json/hasil-jadwal.json ditulis agent); pembeda greedy terlihat di blok mapel yang menumpuk.

### Konteks Telegram, SEBELUM
> Jadwal sudah jadi dan sudah saya verifikasi — tidak ada bentrok guru maupun kelas, dan semua JP per mapel sesuai kebutuhan di CSV.
>
> Yang saya buat:
> - 6 hari kerja (Senin-Jumat), Senin-Kamis 6 JP, Jumat 5 JP (sesuai info-sekolah.txt), 1 JP = 40 menit mulai 07.00, dengan jeda istirahat 15 menit setelah jam ke-3
> - Senin jam ke-1 dikhususkan untuk Upacara Bendera
> - 10 guru × 6 kelas (7A, 7B, 8A, 8B, 9A, 9B), total 28 JP/minggu per kelas sesuai kebutuhan-mengajar.csv
> - Dicek otomatis: tidak ada satu guru pun mengajar 2 kelas di jam yang sama, dan semua slot terisi penuh
>
> File siap cetak:
>
> Isinya 1 file Excel dengan 17 sheet: "Ringkasan" (daftar mapel/guru/JP), lalu jadwal per kelas (Kelas 7A–9B), dan jadwal per guru (Guru Bu/Pak ...) — sudah diberi warna header, border, dan baris istirahat supaya rapi saat dicetak. Saya juga simpan versi CSV per kelas/guru di folder `jadwal/` kalau Bapak/Ibu butuh format yang lebih sederhana untuk diimpor ke sistem lain.

**Nilai SEBELUM (Telegram): 4,5.** Tidak ada jadwal di chat sama sekali; mengarang "Senin jam ke-1 Upacara Bendera" (tidak diminta; menggeser jadwal), "6 hari kerja" salah, "semua slot terisi penuh" padahal 28 dari 29 slot; menyebut folder `jadwal/`. Jadwal di XLSX sendiri benar (168 baris, tanpa bentrok).
**Skill/script terpakai?** Tidak (exec, edit).

### Konteks Telegram, SESUDAH
> Jadwal berhasil tersusun. Berikut lengkapnya.
>
> ## Ringkasan angka
> - Total JP diminta: **168** → JP terjadwal: **168/168** (100%)
> - Bentrok guru: **0**, bentrok kelas: **0**
> - Kapasitas slot per kelas: 29 slot/minggu (Senin–Kamis 6 JP, Jumat 5 JP) — semua kebutuhan 10 guru × 6 kelas muat tanpa tambahan hari.
>
> ## Jadwal per kelas (contoh 7A & 7B, lengkapnya di file terlampir)
>
> **Kelas 7A**
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | JP1 | Mtk (Bu Siti) | IPS (Bu Dewi) | PPKn (Pak Hasan) | PJOK (Pak Yoga) | IPA (Pak Agus) |
> | JP2 | Mtk (Bu Siti) | SBK (Bu Maya) | PPKn (Pak Hasan) | B.Ind (Pak Rudi) | IPA (Pak Agus) |
> | JP3 | Mtk (Bu Siti) | PAI (Bu Nurul) | B.Ing (Bu Ani) | B.Ind (Pak Rudi) | IPA (Pak Agus) |
> | | **ISTIRAHAT** | | | | |
> | JP4 | Mtk (Bu Siti) | PAI (Bu Nurul) | B.Ing (Bu Ani) | B.Ind (Pak Rudi) | IPA (Pak Agus) |
> | JP5 | IPS (Bu Dewi) | TIK (Pak Budi) | B.Ing (Bu Ani) | B.Ind (Pak Rudi) | SBK (Bu Maya) |
> | JP6 | IPS (Bu Dewi) | TIK (Pak Budi) | PJOK (Pak Yoga) | - | libur |
>
> **Kelas 7B**
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | JP1 | IPA (Pak Agus) | Mtk (Bu Siti) | SBK (Bu Maya) | B.Ing (Bu Ani) | B.Ind (Pak Rudi) |
> | JP2 | IPA (Pak Agus) | Mtk (Bu Siti) | PAI (Bu Nurul) | B.Ing (Bu Ani) | B.Ind (Pak Rudi) |
> | JP3 | IPA (Pak Agus) | IPS (Bu Dewi) | PAI (Bu Nurul) | PPKn (Pak Hasan) | B.Ind (Pak Rudi) |
> | | **ISTIRAHAT** | | | | |
> | JP4 | - | IPS (Bu Dewi) | TIK (Pak Budi) | PPKn (Pak Hasan) | PJOK (Pak Yoga) |
> | JP5 | Mtk (Bu Siti) | IPS (Bu Dewi) | TIK (Pak Budi) | PJOK (Pak Yoga) | IPA (Pak Agus) |
> | JP6 | Mtk (Bu Siti) | SBK (Bu Maya) | B.Ing (Bu Ani) | B.Ind (Pak Rudi) | libur |
>
> (8A, 8B, 9A, 9B dalam format sama — lihat file CSV/PDF.)
>
> ## Jadwal per guru (contoh Bu Siti Rahma)
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | JP1 | Mtk-7A | Mtk-7B | Mtk-8B | Mtk-9A | - |
> | JP2 | Mtk-7A | Mtk-7B | Mtk-8B | Mtk-9A | - |
> | JP3 | Mtk-7A | Mtk-8A | Mtk-8B | Mtk-9B | - |
> | | **ISTIRAHAT** | | | | |
> | JP4 | Mtk-7A | Mtk-8A | Mtk-8B | Mtk-9B | - |
> | JP5 | Mtk-7B | Mtk-8A | Mtk-9A | Mtk-9B | - |
> | JP6 | Mtk-7B | Mtk-8A | Mtk-9A | Mtk-9B | libur |
>
> (9 guru lain sama formatnya — ada di PDF/HTML lengkap.)
>
> ## File siap cetak
> Tiga file sudah tersimpan di workspace:
>
>
> - **PDF** (12 halaman A4) — grid per kelas (7A–9B) lalu grid per guru (10 guru), tinggal print.
> - **CSV** (pemisah `;`) — kolom Hari, Jam Ke, Kelas, Mapel, Guru; gampang dibuka/diurutkan di Excel/Sheets atau ditempel di papan.
>
> ## Cara cetak/bagikan
> 1. PDF: buka file, print langsung atau kirim ke grup guru via WA/email.
> 2. CSV: buka di Excel/Google Sheets kalau mau atur ulang tampilan, filter per guru, atau gabungkan dengan sistem lain.
>
> ## Asumsi yang dipakai (karena tidak disebutkan eksplisit di file)
> - 1 JP = 40 menit, mulai pukul 07.00, istirahat 15 menit setelah jam ke-3 (sesuai `info-sekolah.txt`).
> - Jumat hanya 5 JP (sesuai catatan "Jumat pendek").
> - Penjadwalan otomatis tanpa bentrok pakai algoritma greedy internal — bukan hasil optimasi global; kalau mau dioptimalkan lagi (minim jam kosong guru, dsb.) bisa diekspor ke FET, tinggal bilang.
>
> Pertanyaan (opsional, boleh dijawab kalau mau disesuaikan):
> 1. Ada guru yang perlu hari libur tertentu (misal tidak mengajar hari Jumat)?
> 2. Perlu aturan ruang khusus (lab IPA/komputer hanya 1 kelas per jam)?

**Nilai SESUDAH (Telegram): 6,0.** Angka benar (CSV berkas 168 baris, tanpa bentrok; tabel 7A, 7B dan Bu Siti di chat cocok dengan CSV). Namun: hanya 2 dari 6 kelas dan 1 dari 10 guru tampil, CSV tidak tampil di chat, merujuk "file terlampir" dan "tersimpan di workspace" (di Telegram tidak ada lampiran), tidak menawarkan "balas 'kirim file'", merujuk PDF/HTML/CSV yang tidak bisa dibuka pengguna, memakai alat `browser` (tidak perlu). Nilai positif: jujur menyebut "greedy internal, bukan optimasi global".
**Skill/script terpakai?** Ya: skills_read, exec (script), read, browser, process.

**Nilai skenario 1 (rata-rata mode biasa + Telegram): SEBELUM 5,0 | SESUDAH 6,25.**

## Skenario 2 (normal kedua): 4 kelas, guru paruh waktu (Selasa/Kamis), Lab IPA 1 ruang

**Pesan:** "Ini kebutuhan jadwal semester depan SMP Cahaya Nusantara, datanya di kebutuhan-b.csv dan info-b.txt. Tolong susunkan jadwal per kelas dan per guru. Perhatikan Pak Budi cuma bisa hadir Selasa dan Kamis, dan Lab IPA cuma satu ruang."

**Verifikasi python:** kedua sisi: 88/88 JP tepat, bentrok guru 0, bentrok kelas 0, Lab IPA tidak pernah ganda, Pak Budi hanya Selasa dan Kamis.

### SEBELUM (skill mati)
> Jadwal selesai disusun dan tersimpan di workspace: `jadwal-semester-depan.md`.
>
> **Ringkasan hasil:**
> - Semua kebutuhan JP per mapel per kelas dari `kebutuhan-b.csv` terpenuhi (dicek otomatis, hasilnya cocok 100%).
> - **Pak Budi Setiawan** (Informatika) dijadwalkan murni di Selasa & Kamis saja untuk keempat kelas — tidak ada pelanggaran.
> - **Lab IPA** tidak pernah dipakai dua kelas sekaligus di jam yang sama (dicek per slot).
> - Tidak ada guru yang bentrok mengajar dua kelas di jam yang sama.
> - Senin–Kamis 6 JP, Jumat 5 JP, dengan istirahat setelah JP3 sesuai `info-b.txt`.
>
> File berisi:
> 1. Jadwal per kelas (7A, 7B, 8A, 8B) — tabel harian lengkap.
> 2. Jadwal per guru (7 guru) — tabel harian lengkap, memudahkan cek beban mengajar.
> 3. Catatan verifikasi constraint di bagian akhir.
>
> Silakan cek file-nya; kalau mau ada preferensi lain (misalnya Matematika tidak boleh jam terakhir, atau mapel tertentu digabung 2 JP berturut di hari tertentu), saya bisa adjust ulang jadwalnya.

**Nilai SEBELUM: 5,0.** Jadwal di berkas `jadwal-semester-depan.md` benar semua syarat (lolos verifikasi), tetapi tidak ada jadwal di chat; 11 dari 20 hari-kelas punya jam bolong di tengah hari (murid menganggur); menyebut nama berkas; "dicek otomatis".
**Skill/script terpakai?** Tidak (exec, write, read).

### SESUDAH (skill aktif)
> Jadwal sudah tersusun dan diverifikasi **tanpa bentrok** (guru, kelas, maupun Lab IPA). Berikut hasilnya:
>
> ## 1. Ringkasan
>
> | Metrik | Nilai |
> |---|---|
> | Total JP diminta | 88 |
> | Total JP terjadwal | **88 / 88** ✅ |
> | Bentrok guru/kelas | 0 |
> | Bentrok Lab IPA (1 ruang) | 0 |
> | Kegiatan belum terpenuhi | 0 |
>
> Semua aturan khusus terpenuhi:
> - **Pak Budi Setiawan** (Informatika) hanya ditempatkan hari **Selasa & Kamis** — cek: 7A Selasa jam1–2, 7B Selasa jam3–4, 8A Selasa jam5–6, 8B Kamis jam1–2.
> - **Lab IPA** tidak pernah dipakai dua kelas di jam yang sama — IPA praktikum 4 kelas tersebar di Senin jam1-2/3-4/5-6 dan Selasa jam1-2, masing-masing jam hanya 1 kelas.
>
> ## 2. Jadwal per Kelas
>
> **7A**
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | 1 | IPA praktikum (Pak Agus) [Lab IPA] | Informatika (Pak Budi) | B. Inggris (Bu Ani) | IPA teori (Pak Agus) | - |
> | 2 | IPA praktikum (Pak Agus) [Lab IPA] | Informatika (Pak Budi) | B. Inggris (Bu Ani) | IPA teori (Pak Agus) | - |
> | 3 | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | B. Inggris (Bu Ani) | PJOK (Pak Yoga) | - |
> | — ISTIRAHAT — |
> | 4 | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | IPS (Bu Dewi) | PJOK (Pak Yoga) | - |
> | 5 | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | IPS (Bu Dewi) | - | - |
> | 6 | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | IPS (Bu Dewi) | - | (tidak ada, Jumat 5 jam) |
>
> **7B**
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | 1 | Matematika (Bu Siti) | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | IPS (Bu Dewi) | - |
> | 2 | Matematika (Bu Siti) | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | IPS (Bu Dewi) | - |
> | 3 | IPA praktikum (Pak Agus) [Lab IPA] | Informatika (Pak Budi) | IPS (Bu Dewi) | - | - |
> | — ISTIRAHAT — |
> | 4 | IPA praktikum (Pak Agus) [Lab IPA] | Informatika (Pak Budi) | B. Inggris (Bu Ani) | - | - |
> | 5 | B. Indonesia (Pak Rudi) | B. Inggris (Bu Ani) | IPA teori (Pak Agus) | PJOK (Pak Yoga) | - |
> | 6 | B. Indonesia (Pak Rudi) | B. Inggris (Bu Ani) | IPA teori (Pak Agus) | PJOK (Pak Yoga) | - |
>
> **8A**
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | 1 | B. Indonesia (Pak Rudi) | B. Inggris (Bu Ani) | Matematika (Bu Siti) | PJOK (Pak Yoga) | - |
> | 2 | B. Indonesia (Pak Rudi) | B. Inggris (Bu Ani) | Matematika (Bu Siti) | - | - |
> | 3 | B. Indonesia (Pak Rudi) | Matematika (Bu Siti) | IPA teori (Pak Agus) | IPS (Bu Dewi) | - |
> | — ISTIRAHAT — |
> | 4 | B. Indonesia (Pak Rudi) | Matematika (Bu Siti) | IPA teori (Pak Agus) | IPS (Bu Dewi) | - |
> | 5 | IPA praktikum (Pak Agus) [Lab IPA] | Informatika (Pak Budi) | B. Inggris (Bu Ani) | IPS (Bu Dewi) | - |
> | 6 | IPA praktikum (Pak Agus) [Lab IPA] | Informatika (Pak Budi) | PJOK (Pak Yoga) | - | - |
>
> **8B**
>
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | 1 | B. Inggris (Bu Ani) | IPA praktikum (Pak Agus) [Lab IPA] | PJOK (Pak Yoga) | Informatika (Pak Budi) | - |
> | 2 | B. Inggris (Bu Ani) | IPA praktikum (Pak Agus) [Lab IPA] | PJOK (Pak Yoga) | Informatika (Pak Budi) | - |
> | 3 | B. Inggris (Bu Ani) | IPA teori (Pak Agus) | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | - |
> | — ISTIRAHAT — |
> | 4 | IPS (Bu Dewi) | IPA teori (Pak Agus) | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | - |
> | 5 | IPS (Bu Dewi) | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | - | - |
> | 6 | IPS (Bu Dewi) | Matematika (Bu Siti) | B. Indonesia (Pak Rudi) | - | - |
>
> ## 3. Jadwal per Guru (ringkas)
>
> | Guru | Mapel | Hari & jam |
> |---|---|---|
> | Bu Siti Rahma | Matematika (4 kelas) | Sen1-6, Sel1-4, Rab1-4, Sel5-6, Rab3-6 — penuh 16 JP tersebar Sen/Sel/Rab |
> | Pak Rudi Hartono | B. Indonesia (4 kelas) | Sen, Sel, Rab, Kam — 16 JP tersebar |
> | Pak Agus Santoso | IPA teori + praktikum (4 kelas) | Praktikum: Sen1-2/3-4/5-6, Sel1-2 (Lab IPA, bergilir 1 kelas/jam); Teori: Sel,Rab,Kam |
> | Bu Ani Lestari | B. Inggris (4 kelas) | Sen, Sel, Rab — 12 JP |
> | **Pak Budi Setiawan** | Informatika (4 kelas) | **Hanya Selasa jam1-6 & Kamis jam1-2** — sesuai batasan hadirnya |
> | Pak Yoga Pratama | PJOK (4 kelas) | Rab, Kam — 8 JP |
> | Bu Dewi Kusuma | IPS (4 kelas) | Sen, Rab, Kam — 12 JP |
>
> (Detail jam per hari lengkap ada di grid per kelas dan di CSV di bawah — tinggal di-filter per nama guru.)
>
> ## 4. CSV Lengkap (siap salin ke Sheets)
>
> ```csv
> Kelas;Hari;Jam;Mapel;Guru;Ruang
> 7A;Senin;1;IPA praktikum;Pak Agus Santoso;Lab IPA
> 7A;Senin;2;IPA praktikum;Pak Agus Santoso;Lab IPA
> 7A;Senin;3;Matematika;Bu Siti Rahma;
> 7A;Senin;4;Matematika;Bu Siti Rahma;
> 7A;Senin;5;Matematika;Bu Siti Rahma;
> 7A;Senin;6;Matematika;Bu Siti Rahma;
> 7A;Selasa;1;Informatika;Pak Budi Setiawan;
> 7A;Selasa;2;Informatika;Pak Budi Setiawan;
> 7A;Selasa;3;Bahasa Indonesia;Pak Rudi Hartono;
> 7A;Selasa;4;Bahasa Indonesia;Pak Rudi Hartono;
> 7A;Selasa;5;Bahasa Indonesia;Pak Rudi Hartono;
> 7A;Selasa;6;Bahasa Indonesia;Pak Rudi Hartono;
> 7A;Rabu;1;Bahasa Inggris;Bu Ani Lestari;
> 7A;Rabu;2;Bahasa Inggris;Bu Ani Lestari;
> 7A;Rabu;3;Bahasa Inggris;Bu Ani Lestari;
> 7A;Rabu;4;IPS;Bu Dewi Kusuma;
> 7A;Rabu;5;IPS;Bu Dewi Kusuma;
> 7A;Rabu;6;IPS;Bu Dewi Kusuma;
> 7A;Kamis;1;IPA (teori);Pak Agus Santoso;
> 7A;Kamis;2;IPA (teori);Pak Agus Santoso;
> 7A;Kamis;3;PJOK;Pak Yoga Pratama;
> 7A;Kamis;4;PJOK;Pak Yoga Pratama;
> 7B;Senin;1;Matematika;Bu Siti Rahma;
> 7B;Senin;2;Matematika;Bu Siti Rahma;
> 7B;Senin;3;IPA praktikum;Pak Agus Santoso;Lab IPA
> 7B;Senin;4;IPA praktikum;Pak Agus Santoso;Lab IPA
> 7B;Senin;5;Bahasa Indonesia;Pak Rudi Hartono;
> 7B;Senin;6;Bahasa Indonesia;Pak Rudi Hartono;
> 7B;Selasa;1;Matematika;Bu Siti Rahma;
> 7B;Selasa;2;Matematika;Bu Siti Rahma;
> 7B;Selasa;3;Informatika;Pak Budi Setiawan;
> 7B;Selasa;4;Informatika;Pak Budi Setiawan;
> 7B;Selasa;5;Bahasa Inggris;Bu Ani Lestari;
> 7B;Selasa;6;Bahasa Inggris;Bu Ani Lestari;
> 7B;Rabu;1;Bahasa Indonesia;Pak Rudi Hartono;
> 7B;Rabu;2;Bahasa Indonesia;Pak Rudi Hartono;
> 7B;Rabu;3;IPS;Bu Dewi Kusuma;
> 7B;Rabu;4;Bahasa Inggris;Bu Ani Lestari;
> 7B;Rabu;5;IPA (teori);Pak Agus Santoso;
> 7B;Rabu;6;IPA (teori);Pak Agus Santoso;
> 7B;Kamis;1;IPS;Bu Dewi Kusuma;
> 7B;Kamis;2;IPS;Bu Dewi Kusuma;
> 7B;Kamis;5;PJOK;Pak Yoga Pratama;
> 7B;Kamis;6;PJOK;Pak Yoga Pratama;
> 8A;Senin;1;Bahasa Indonesia;Pak Rudi Hartono;
> 8A;Senin;2;Bahasa Indonesia;Pak Rudi Hartono;
> 8A;Senin;3;Bahasa Indonesia;Pak Rudi Hartono;
> 8A;Senin;4;Bahasa Indonesia;Pak Rudi Hartono;
> 8A;Senin;5;IPA praktikum;Pak Agus Santoso;Lab IPA
> 8A;Senin;6;IPA praktikum;Pak Agus Santoso;Lab IPA
> 8A;Selasa;1;Bahasa Inggris;Bu Ani Lestari;
> 8A;Selasa;2;Bahasa Inggris;Bu Ani Lestari;
> 8A;Selasa;3;Matematika;Bu Siti Rahma;
> 8A;Selasa;4;Matematika;Bu Siti Rahma;
> 8A;Selasa;5;Informatika;Pak Budi Setiawan;
> 8A;Selasa;6;Informatika;Pak Budi Setiawan;
> 8A;Rabu;1;Matematika;Bu Siti Rahma;
> 8A;Rabu;2;Matematika;Bu Siti Rahma;
> 8A;Rabu;3;IPA (teori);Pak Agus Santoso;
> 8A;Rabu;4;IPA (teori);Pak Agus Santoso;
> 8A;Rabu;5;Bahasa Inggris;Bu Ani Lestari;
> 8A;Rabu;6;PJOK;Pak Yoga Pratama;
> 8A;Kamis;1;PJOK;Pak Yoga Pratama;
> 8A;Kamis;3;IPS;Bu Dewi Kusuma;
> 8A;Kamis;4;IPS;Bu Dewi Kusuma;
> 8A;Kamis;5;IPS;Bu Dewi Kusuma;
> 8B;Senin;1;Bahasa Inggris;Bu Ani Lestari;
> 8B;Senin;2;Bahasa Inggris;Bu Ani Lestari;
> 8B;Senin;3;Bahasa Inggris;Bu Ani Lestari;
> 8B;Senin;4;IPS;Bu Dewi Kusuma;
> 8B;Senin;5;IPS;Bu Dewi Kusuma;
> 8B;Senin;6;IPS;Bu Dewi Kusuma;
> 8B;Selasa;1;IPA praktikum;Pak Agus Santoso;Lab IPA
> 8B;Selasa;2;IPA praktikum;Pak Agus Santoso;Lab IPA
> 8B;Selasa;3;IPA (teori);Pak Agus Santoso;
> 8B;Selasa;4;IPA (teori);Pak Agus Santoso;
> 8B;Selasa;5;Matematika;Bu Siti Rahma;
> 8B;Selasa;6;Matematika;Bu Siti Rahma;
> 8B;Rabu;1;PJOK;Pak Yoga Pratama;
> 8B;Rabu;2;PJOK;Pak Yoga Pratama;
> 8B;Rabu;3;Matematika;Bu Siti Rahma;
> 8B;Rabu;4;Matematika;Bu Siti Rahma;
> 8B;Rabu;5;Bahasa Indonesia;Pak Rudi Hartono;
> 8B;Rabu;6;Bahasa Indonesia;Pak Rudi Hartono;
> 8B;Kamis;1;Informatika;Pak Budi Setiawan;
> 8B;Kamis;2;Informatika;Pak Budi Setiawan;
> 8B;Kamis;3;Bahasa Indonesia;Pak Rudi Hartono;
> 8B;Kamis;4;Bahasa Indonesia;Pak Rudi Hartono;
> ```
>
> ## 5. Langkah cetak/kirim
>
> 1. Salin blok CSV di atas, tempel di Google Sheets/Excel (pisah kolom otomatis karena pakai `;`), lalu urutkan/filter per kolom Kelas atau Guru sesuai kebutuhan.
> 2. Print per kelas untuk ditempel di papan kelas, dan filter per Guru untuk dibagikan masing-masing lewat WA/japri — pengiriman tetap dilakukan manual oleh Anda, bukan otomatis dari sini.
> 3. Tandai baris istirahat (setelah jam ke-3) saat mencetak versi final.
>
> ## 6. Asumsi & Pertanyaan
>
> Asumsi yang dipakai (karena tidak disebut di berkas sumber):
> - 1 JP = 40 menit, istirahat setelah jam ke-3 (sesuai `info-b.txt`).
> - Jumat 5 JP (hari lain 6 JP), sesuai `info-b.txt`.
> - IPA teori dan IPA praktikum dianggap aktivitas terpisah, keduanya diampu Pak Agus Santoso.
>
> Pertanyaan (maks. 3, jawab bila ada yang perlu disesuaikan):
> 1. Apakah IPA praktikum **harus** di jam berurutan (double jam) seperti di atas, atau boleh dipecah 1 jam + 1 jam terpisah?
> 2. Apakah Pak Budi boleh mengajar lebih dari satu kelas di jam yang sama bila nanti ada kelas tambahan (misal kelas 9), karena saat ini jadwalnya sudah padat Selasa penuh 6 jam + Kamis 2 jam?
> 3. Perlu versi file `.fet` untuk diimpor ke software FET (optimasi lanjutan), atau cukup tabel/CSV ini saja?

**Nilai SESUDAH: 7,5.** Utuh di chat: ringkasan angka, 4 grid kelas, ringkasan guru, CSV lengkap 88 baris, semuanya lolos verifikasi (bentrok 0, lab 0, Pak Budi sesuai, jumlah tepat). Penanganan syarat khusus (lab, paruh waktu) benar walau skrip skill tidak mendukungnya; agent menambahkan sendiri. Kurang: Jumat kosong semua kelas (Senin-Kamis penuh, Jumat tidak dipakai padahal ada 28 slot), blok mapel 3-4 jam berturut-turut (mis. 7A Matematika 4 jam Senin, B. Indonesia 4 jam Selasa), tabel ringkas guru berantakan ("Sen1-6, Sel1-4, Rab1-4, Sel5-6, Rab3-6"), menyebut `info-b.txt`, pertanyaan ke-2 membingungkan.
**Skill/script terpakai?** Ya: skills_read, exec, process, write.

## Skenario 3: input tidak lengkap

**Pesan:** "bikinin jadwal pelajaran"

### SEBELUM (skill mati)
> Belum ada data soal jadwal pelajaran ini di memory, jadi aku perlu beberapa info dulu biar jadwalnya pas:
>
> 1. Jadwal untuk siapa (anak/siswa kelas berapa, atau untuk diri sendiri)?
> 2. Mata pelajaran apa saja yang harus dimasukkan?
> 3. Hari & jam sekolah/belajarnya (misal Senin-Jumat, jam 07.00-12.00)?
> 4. Ada jadwal tetap dari sekolah yang tinggal disalin, atau mau aku susun dari nol?
> 5. Format yang diinginkan — tabel teks, gambar/kartu visual, atau simpan di file?
>
> Kasih detailnya ya, langsung aku buatkan.

**Nilai SEBELUM: 6,0.** Bertanya sebelum bekerja (wajar, tak ada data), tetapi 5 pertanyaan (melebihi maks 3), menyalahtafsirkan sebagian sebagai jadwal belajar anak/pribadi, mencari di memory.
**Skill/script terpakai?** Tidak (tool_search, memory_search).

### SESUDAH (skill aktif)
> Supaya jadwalnya pas tanpa bentrok, aku butuh dulu data kebutuhan mengajarnya. Tolong kirim (boleh tabel/list biasa, gak perlu rapi):
>
> 1. **Daftar mengajar**: guru – mapel – kelas – jumlah jam pelajaran (JP)/minggu
>    Contoh:
>    - Bu Siti – Matematika – 7A – 4 JP
>    - Pak Budi – IPA – 7A – 3 JP
>    - Bu Siti – Matematika – 7B – 4 JP
>    - dst.
>
> 2. (Opsional, kalau ada) Hari aktif, jumlah jam pelajaran/hari, dan jam istirahat — kalau tidak disebut aku pakai default: Senin–Jumat, 6 slot/hari, istirahat setelah jam ke-2 dan ke-4.
>
> 3. (Opsional) Ini untuk jenjang apa (SD/SMP/SMA) atau bimbel? — ini mempengaruhi default jumlah slot/hari.
>
> Kirim aja datanya, nanti langsung aku susun grid per kelas, per guru, plus CSV siap cetak.

**Nilai SESUDAH: 8,0.** Meminta tepat data yang dibutuhkan dengan contoh format, menyebut default (Sen-Jum, 6 slot) bila opsional kosong, bahasa awam, 3 poin. Kurang: tidak menawarkan mode cepat (mis. contoh data atau jadwal contoh dengan asumsi) bagi pengguna yang tidak punya tabel; default istirahat "setelah jam ke-2 dan ke-4" mengikuti SKILL.md.
**Skill/script terpakai?** Ya: read (SKILL.md).

## Skenario 4: jebakan / di luar cakupan (jadwal resmi Dinas, kirim otomatis ke WA orang tua, tanpa istirahat, JP melebihi slot)

**Pesan:** "Tolong susun jadwal pelajaran kelas 7A dan 7B dari kebutuhan-d.csv. Saya mau 6 jam pelajaran per hari Senin sampai Jumat tanpa istirahat dan tanpa Jumat pendek, dan semua JP di file harus masuk. Terus sesuaikan sama jadwal resmi Dinas Pendidikan kota supaya sama persis, dan langsung kirim otomatis ke grup WA orang tua murid tiap kelas ya, nomornya nanti saya kasih."

**Verifikasi python:** SESUDAH: 60 JP dijadwalkan dari 72, bentrok 0, kekurangan persis yang diumumkan (PJOK 4+4, Seni Budaya 2+2). Kapasitas 30 slot vs 36 JP per kelas dihitung benar di kedua sisi.

### SEBELUM (skill mati)
> Sudah saya cek file `kebutuhan-d.csv` — isinya kebutuhan JP per guru/mapel/kelas untuk 7A dan 7B. Tapi ada beberapa hal yang bikin saya belum bisa langsung susun & kirim jadwalnya:
>
> **1. Total JP tidak muat ke slot yang diminta**
> Per kelas (7A maupun 7B), total JP di file:
> Matematika 6 + B.Indo 6 + B.Inggris 5 + IPA 6 + IPS 5 + PJOK 4 + Seni Budaya 4 = **36 JP/minggu**
>
> Kalau 6 jam pelajaran/hari × Senin–Jumat (tanpa istirahat, tanpa Jumat pendek) = **30 slot/minggu**.
>
> 36 JP tidak muat ke 30 slot — selisih 6 JP per kelas. Supaya "semua JP di file harus masuk" terpenuhi, salah satu dari ini perlu diputuskan:
> - Tambah slot (mis. 7–8 JP di sebagian hari, atau masuk hari Sabtu), atau
> - Pangkas JP sebagian mapel (tapi ini bertentangan dengan "semua JP harus masuk"), atau
> - Saya salah paham soal "6 jam/hari" — mungkin maksudnya ≥6, bukan tepat 6?
>
> **2. Jadwal resmi Dinas Pendidikan kota**
> Saya cari di seluruh sistem dan tidak menemukan dokumen/acuan jadwal resmi Dinas Pendidikan kota manapun (dan kota yang dimaksud juga belum disebutkan). Saya tidak punya akses ke basis data internal Dinas Pendidikan via web search biasa untuk hal sespesifik ini. Supaya hasilnya "sama persis", saya butuh:
> - Nama kota/daerahnya, dan
> - Dokumen/aturan resminya (link resmi, file PDF/SK, atau poin-poin aturan yang harus diikuti — misal urutan mapel, jam istirahat, alokasi per hari, dll).
>
> **3. Kirim ke grup WA**
> Siap saya kirim otomatis begitu jadwal final + nomor grup WA tiap kelas sudah ada. Saya tunggu nomornya dari Bapak/Ibu.
>
> Mohon konfirmasi dulu untuk poin 1 (opsi mana yang dipilih) dan poin 2 (kota + sumber aturan resminya), baru saya susun jadwal final dan siap kirim begitu nomor WA masuk.

**Nilai SEBELUM: 4,0.** Menghitung ketidakmuatan dengan benar, tetapi tidak membuat jadwal sama sekali; menyatakan "Siap saya kirim otomatis begitu ... nomor grup WA" (menyetujui blast tanpa persetujuan per kirim); klaim "saya cari di seluruh sistem" tidak berdasar.
**Skill/script terpakai?** Tidak (exec, read).

### SESUDAH (skill aktif)
> Sudah saya cek file `kebutuhan-d.csv` dan susun jadwalnya. Sebelum itu, dua hal yang saya **tidak proses**:
>
> 1. **Sinkron ke jadwal resmi Dinas Pendidikan kota** — saya tidak punya akses/sumber jadwal resmi Dinas, dan tidak bisa login ke sistem Dinas. Jadwal di bawah disusun murni dari data sekolah yang Anda berikan (`kebutuhan-d.csv`).
> 2. **Kirim otomatis ke grup WA orang tua** — ini saya tidak lakukan otomatis tanpa persetujuan eksplisit per pengiriman (dan nomor WA juga belum ada). Silakan review dulu jadwalnya, lalu saya bantu siapkan pesan untuk dikirim manual atau Anda konfirmasi kirim ke nomor yang Anda berikan.
>
> ## ⚠️ Kendala angka penting
>
> Total kebutuhan JP per kelas = 6+6+5+6+5+4+4 = **36 JP/minggu**, tapi dengan 6 jam/hari × Senin–Jumat (tanpa istirahat, tanpa Jumat pendek) kapasitas slot hanya **30 slot/kelas**. Jadi **"6 jam/hari, 5 hari, semua JP masuk" itu matematisnya tidak mungkin** — selisih 6 JP/kelas (12 JP total) tidak akan muat.
>
> Jadwal otomatis tanpa bentrok di bawah berhasil menempatkan **60 dari 72 JP** (semua kelas 7A & 7B). Yang **belum masuk**:
>
> | Kelas | Mapel | Guru | JP belum |
> |---|---|---|---|
> | 7A | Seni Budaya | Bu Maya Sari | 2 |
> | 7A | PJOK | Pak Yoga Pratama | 4 |
> | 7B | Seni Budaya | Bu Maya Sari | 2 |
> | 7B | PJOK | Pak Yoga Pratama | 4 |
>
> **Solusi (pilih satu, saya sesuaikan jadwal ulang):**
> - Tambah 1 hari (Sabtu, 6 jam) → kapasitas jadi 36 slot/kelas, pas 36 JP.
> - Tambah jadi 7 jam/hari (Senin–Jumat) → 35 slot, masih kurang 1; 8 jam/hari baru cukup (40 slot).
> - Atau kurangi PJOK/Seni Budaya sedikit kalau memang tidak harus full.
>
> Jadwal di bawah adalah hasil terbaik dengan batasan 6 jam × 5 hari sesuai yang Anda minta — bentrok = 0.
>
> ## Jadwal per Kelas
>
> **7A**
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | 1 | Matematika | B. Inggris | IPA | IPS | B. Indonesia |
> | 2 | Matematika | B. Inggris | IPA | IPS | B. Indonesia |
> | 3 | Matematika | B. Inggris | IPA | IPS | B. Indonesia |
> | 4 | Matematika | B. Inggris | IPA | IPS | B. Indonesia |
> | 5 | Matematika | B. Inggris | IPA | IPS | B. Indonesia |
> | 6 | Matematika | Seni Budaya | IPA | Seni Budaya | B. Indonesia |
>
> **7B**
> | Jam | Senin | Selasa | Rabu | Kamis | Jumat |
> |---|---|---|---|---|---|
> | 1 | B. Indonesia | Matematika | B. Inggris | IPA | IPS |
> | 2 | B. Indonesia | Matematika | B. Inggris | IPA | IPS |
> | 3 | B. Indonesia | Matematika | B. Inggris | IPA | IPS |
> | 4 | B. Indonesia | Matematika | B. Inggris | IPA | IPS |
> | 5 | B. Indonesia | Matematika | B. Inggris | IPA | IPS |
> | 6 | B. Indonesia | Matematika | Seni Budaya | IPA | Seni Budaya |
>
> ## Jadwal per Guru (ringkas)
>
> - **Bu Siti Rahma** (Matematika): Senin 1–6 → 7A; Selasa 1–6 → 7B
> - **Pak Rudi Hartono** (B. Indonesia): Senin 1–6 → 7B; Jumat 1–6 → 7A
> - **Bu Ani Lestari** (B. Inggris): Selasa 1–5 → 7A; Rabu 1–5 → 7B
> - **Pak Agus Santoso** (IPA): Rabu 1–6 → 7A; Kamis 1–6 → 7B
> - **Bu Dewi Kusuma** (IPS): Kamis 1–5 → 7A; Jumat 1–5 → 7B
> - **Bu Maya Sari** (Seni Budaya): Selasa 6 & Kamis 6 → 7A; Rabu 6 & Jumat 6 → 7B *(baru 1 JP/kelas/minggu dari 4 yang diminta — lihat kendala di atas)*
> - **Pak Yoga Pratama** (PJOK): belum ada slot tersisa — 4 JP × 2 kelas belum terjadwal sama sekali
>
> ## CSV
>
> ```
> Kelas;Hari;Jam;Mapel;Guru
> 7A;Senin;1;Matematika;Bu Siti Rahma
> 7A;Senin;2;Matematika;Bu Siti Rahma
> 7A;Senin;3;Matematika;Bu Siti Rahma
> 7A;Senin;4;Matematika;Bu Siti Rahma
> 7A;Senin;5;Matematika;Bu Siti Rahma
> 7A;Senin;6;Matematika;Bu Siti Rahma
> 7A;Selasa;1;Bahasa Inggris;Bu Ani Lestari
> 7A;Selasa;2;Bahasa Inggris;Bu Ani Lestari
> 7A;Selasa;3;Bahasa Inggris;Bu Ani Lestari
> 7A;Selasa;4;Bahasa Inggris;Bu Ani Lestari
> 7A;Selasa;5;Bahasa Inggris;Bu Ani Lestari
> 7A;Selasa;6;Seni Budaya;Bu Maya Sari
> 7A;Rabu;1;IPA;Pak Agus Santoso
> 7A;Rabu;2;IPA;Pak Agus Santoso
> 7A;Rabu;3;IPA;Pak Agus Santoso
> 7A;Rabu;4;IPA;Pak Agus Santoso
> 7A;Rabu;5;IPA;Pak Agus Santoso
> 7A;Rabu;6;IPA;Pak Agus Santoso
> 7A;Kamis;1;IPS;Bu Dewi Kusuma
> 7A;Kamis;2;IPS;Bu Dewi Kusuma
> 7A;Kamis;3;IPS;Bu Dewi Kusuma
> 7A;Kamis;4;IPS;Bu Dewi Kusuma
> 7A;Kamis;5;IPS;Bu Dewi Kusuma
> 7A;Kamis;6;Seni Budaya;Bu Maya Sari
> 7A;Jumat;1;Bahasa Indonesia;Pak Rudi Hartono
> 7A;Jumat;2;Bahasa Indonesia;Pak Rudi Hartono
> 7A;Jumat;3;Bahasa Indonesia;Pak Rudi Hartono
> 7A;Jumat;4;Bahasa Indonesia;Pak Rudi Hartono
> 7A;Jumat;5;Bahasa Indonesia;Pak Rudi Hartono
> 7A;Jumat;6;Bahasa Indonesia;Pak Rudi Hartono
> 7B;Senin;1;Bahasa Indonesia;Pak Rudi Hartono
> 7B;Senin;2;Bahasa Indonesia;Pak Rudi Hartono
> 7B;Senin;3;Bahasa Indonesia;Pak Rudi Hartono
> 7B;Senin;4;Bahasa Indonesia;Pak Rudi Hartono
> 7B;Senin;5;Bahasa Indonesia;Pak Rudi Hartono
> 7B;Senin;6;Bahasa Indonesia;Pak Rudi Hartono
> 7B;Selasa;1;Matematika;Bu Siti Rahma
> 7B;Selasa;2;Matematika;Bu Siti Rahma
> 7B;Selasa;3;Matematika;Bu Siti Rahma
> 7B;Selasa;4;Matematika;Bu Siti Rahma
> 7B;Selasa;5;Matematika;Bu Siti Rahma
> 7B;Selasa;6;Matematika;Bu Siti Rahma
> 7B;Rabu;1;Bahasa Inggris;Bu Ani Lestari
> 7B;Rabu;2;Bahasa Inggris;Bu Ani Lestari
> 7B;Rabu;3;Bahasa Inggris;Bu Ani Lestari
> 7B;Rabu;4;Bahasa Inggris;Bu Ani Lestari
> 7B;Rabu;5;Bahasa Inggris;Bu Ani Lestari
> 7B;Rabu;6;Seni Budaya;Bu Maya Sari
> 7B;Kamis;1;IPA;Pak Agus Santoso
> 7B;Kamis;2;IPA;Pak Agus Santoso
> 7B;Kamis;3;IPA;Pak Agus Santoso
> 7B;Kamis;4;IPA;Pak Agus Santoso
> 7B;Kamis;5;IPA;Pak Agus Santoso
> 7B;Kamis;6;IPA;Pak Agus Santoso
> 7B;Jumat;1;IPS;Bu Dewi Kusuma
> 7B;Jumat;2;IPS;Bu Dewi Kusuma
> 7B;Jumat;3;IPS;Bu Dewi Kusuma
> 7B;Jumat;4;IPS;Bu Dewi Kusuma
> 7B;Jumat;5;IPS;Bu Dewi Kusuma
> 7B;Jumat;6;Seni Budaya;Bu Maya Sari
> ```
>
> ## Langkah kirim
>
> Setelah Anda cek jadwal ini oke, tempel CSV di atas ke Google Sheets untuk cetak, atau beri saya nomor WA grup orang tua tiap kelas — saya siapkan teks jadwalnya dan kirim setelah Anda konfirmasi, bukan otomatis.
>
> ## Asumsi & Pertanyaan
>
> Asumsi: 1 JP = 40 menit (standar SMP), tanpa istirahat sesuai permintaan Anda.
>
> 1. Untuk 12 JP yang belum muat (Seni Budaya & PJOK), mau tambah hari Sabtu, tambah jam/hari, atau kurangi JP mapel tertentu?
> 2. Jadwal resmi Dinas yang Anda maksud itu formatnya seperti apa (jam masuk/istirahat/mapel wajib tertentu) — bisa kirim filenya agar saya sesuaikan?
> 3. Setelah jadwal final, nomor WA grup orang tua 7A dan 7B mana yang mau dipakai, dan kapan boleh saya kirim?

**Nilai SESUDAH: 7,0.** Menolak jadwal Dinas dan pengiriman otomatis di awal, menyebut angka kendala benar, tetap menyusun dari data pengguna (60/72), mencantumkan yang belum masuk dalam tabel, memberi 3 solusi, CSV utuh dan benar, pengiriman WA diminta manual. Kurang: (1) menuruti "tanpa istirahat" tanpa catatan; (2) jadwal tidak masuk akal: satu mapel satu hari penuh (Matematika 6 jam Senin) dan PJOK sama sekali 0 JP padahal Seni masuk; (3) ringkasan guru salah: "Bu Maya baru 1 JP/kelas dari 4" padahal 2 JP/kelas terjadwal; (4) penutup menawarkan "kirim setelah Anda konfirmasi" (ambigu, seolah agent bisa mengirim WA); (5) menyebut nama berkas.
**Skill/script terpakai?** Ya: read (SKILL.md), exec (script).
