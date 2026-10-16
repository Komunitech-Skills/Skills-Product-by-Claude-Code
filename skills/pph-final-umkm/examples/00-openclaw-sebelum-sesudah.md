# Uji OpenClaw sebelum/sesudah: pph-final-umkm

## Uji ulang 1.0.5 (2026-10-16, penguji independen)

- **Tanggal:** 2026-10-16, dijalankan ±15.35-15.42 WIB ("hari ini" di semua skenario = Jumat, 16 Oktober 2026; batas setor masa September, Kamis 15 Oktober 2026, sudah lewat 1 hari).
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill; hanya membaca folder skill, pesan uji, jawaban, dan jejak alat).
- **Versi skill:** 1.0.5 (perubahan 1.0.4/1.0.5 di `CHANGELOG.md`: PPh 22 marketplace dikreditkan per bulan, jangka waktu tarif mengikuti PP 20/2026, "hari ini"/subtotal/proyeksi dicetak oleh hitungan, mode tabel kemungkinan).
- **Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per skenario), model router Komunitech (`claude-sonnet-5`), TZ Asia/Jakarta. Home dibuat ulang bersih (`mk-home.sh`) berisi **hanya** `pph-final-umkm`. Pesan identik dengan uji 14 Oktober. Skenario 1 juga dijalankan di konteks kanal Telegram (`uji-tg.sh`, `--channel telegram`, tanpa mengirim). Kelima skenario berhasil pada percobaan pertama.
- **Pembanding TANPA skill:** skor uji 14 Oktober 2026 dipakai ulang (rata-rata **6,8**), tidak diuji ulang. Catatan: "hari ini" baseline = Rabu 14 Oktober (masa September belum lewat), uji ini = Jumat 16 Oktober.
- **Alat yang dipanggil agent:** `skills_read` lalu `pph_final.py` lewat exec di kelima skenario, selalu dengan `--hari-ini 2026-10-16` (1/1T: `--tahun-terdaftar 2020 --marketplace --pph22 ...`; 2: `--jenis badan --jenis-badan pt-perorangan`; 3: `--bulan-awal 7 --omzet-sebelumnya 410jt --proyeksi-mulai 10`; 4: `--kemungkinan`). Balasan menyalin keluaran hitungan hampir apa adanya. **Di kelima run agent lebih dulu menjalankan `find /` untuk mencari skrip** (dihentikan sendiri dalam beberapa detik; lihat catatan jujur).
- **Durasi agent:** 54-68 detik per skenario (total per percobaan 64-114 detik).
- **Data:** fiktif.

### Ringkasan skor

| Skenario | Tanpa skill (14 Okt) | Dengan skill 1.0.5 | Alasan ringkas (sisi DENGAN) |
|---|:-:|:-:|---|
| 1. Olshop Shopee + toko, NPWP 2020, Jan-Sep, PPh 22 Shopee (lokal) | 8 | **9** | Angka benar; PPh 22 dikreditkan (Agustus lebih Rp72.500, September kurang Rp165.000); "hari ini" Jumat 16 Okt benar, masa September ditandai sudah lewat; tanpa batas tahun (PP 20/2026); pengingat surat pernyataan bersyarat (Senin 31 Agustus 2026). Kurang: tabel 9 kolom dengan 7 baris nol |
| 1T. Skenario 1 di konteks Telegram | 6,5 | **8,5** | Utuh 3.801 karakter (satu pesan), kalimat pertama langsung "kurang Rp165.000 ... sudah lewat batas waktu". Kurang: klaim tambahan "DJP hanya memperbolehkan pengembalian, bukan pemindahan saldo"; syarat surat pernyataan dihilangkan; tabel lebar di ponsel |
| 2. PT perorangan katering, "baru 409 juta" | 5,5 | **9** | Koreksi di kalimat pertama; 9 masa (total Rp2.045.000) benar dan semuanya sudah lewat; batas setor digeser libur; PT perorangan tanpa batas tahun (tanpa skill keliru "3 tahun, 2026 terakhir"); tanya omzet gabungan Rp4,8 miliar |
| 3. Bengkel, Jan-Jun gelondongan 410 juta + proyeksi Okt-Des | 7 | **9** | Kalimat pertama: Juli-September Rp975.000 (salah Rp995.000 versi 1.0.3 hilang), Juli-Desember Rp2.475.000; masa lewat ditandai; Oktober -> Senin 16 Nov; proyeksi berlabel. Kurang: 4.217 karakter, 9 butir catatan |
| 4. Input kurang: "omzet oktober kira2 85jt" | 7 | **8,5** | Kerjakan dulu: tabel kemungkinan (s.d. Rp415 juta = Rp0; Rp500 juta+/badan = Rp425.000), batas Senin 16 Nov 2026 (31 hari lagi), 3 pertanyaan. Kurang: baris tengah tanpa contoh angka; "dll" tambahan agent |
| **Rata-rata** | **6,8** | **8,8** | |

- **Selisih:** +2,0 poin (acuan ≥ 1,5).
- **Kesalahan angka pajak di sisi DENGAN skill:** tidak ada (lihat verifikasi di bawah).
- **Verdik: LULUS** (DENGAN 8,8 ≥ 8; selisih 2,0 ≥ 1,5; tanpa salah angka pajak).

**Kalimat pembeda:** Dengan skill, setiap jawaban berisi tabel per bulan yang mengkreditkan PPh 22 marketplace (Agustus lebih Rp72.500 bisa diminta kembali, September kurang Rp165.000), menandai masa yang sudah lewat batas setor per hari ini lengkap dengan pergeseran libur, dan menyatakan tarif 0,5% orang pribadi/PT perorangan tanpa batas tahun sesuai PP 20/2026; tanpa skill batas setor hanya "tanggal 15" dan batas 3/4/7 tahun yang sudah usang masih disebut.

**Konteks Telegram (1T):** isi utuh dan sama dengan versi lokal (tabel, ringkasan, catatan, disclaimer, 3 pertanyaan), 3.801 karakter, muat dalam satu pesan Telegram (batas 4.096), tanpa kata proses. Tampilan tabel 9 kolom di aplikasi Telegram belum dilihat di bot asli.

### Verifikasi angka independen (penguji)

Kalkulator Python milik penguji (tidak mengimpor script skill): orang pribadi = 0,5% × bagian omzet kumulatif di atas Rp500 juta; badan = 0,5% × omzet; dibulatkan ke bawah; kurang setor = maks(0, PPh − PPh 22), lebih = maks(0, PPh 22 − PPh); batas setor tanggal 15 bulan berikutnya digeser ke hari kerja memakai daftar libur & cuti bersama 2026 yang disusun penguji sendiri; nama hari dari kalender Python.

| Kasus | Hitung ulang penguji | Balasan DENGAN 1.0.5 |
|---|---|---|
| Hari ini / batas masa September | Jumat 16 Okt 2026; 15 Okt 2026 = Kamis (bukan libur) -> sudah lewat 1 hari | sama (semua skenario) ✓ |
| 1/1T Agustus | kumulatif Rp521.500.000, kena Rp21.500.000, PPh Rp107.500, PPh 22 Rp180.000 -> lebih Rp72.500 (tidak telat) | sama ✓ |
| 1/1T September | PPh Rp330.000 − Rp165.000 = kurang Rp165.000; batas Kamis 15 Okt 2026, sudah lewat | sama ✓ |
| 1/1T total & lain | PPh Rp437.500; kurang Rp165.000; lebih Rp72.500; sisa ke Rp4,8 miliar Rp4.212.500.000; akhir bulan lewat Rp500 juta = Senin 31 Agustus 2026 | sama ✓ |
| 1/1T jangka waktu | NPWP 2020: batas lama 2020-2026; PP 20/2026 (menurut `references/`) menghapus Pasal 59 -> tanpa batas | "tidak ada lagi batas tahun" ✓ |
| 2 PT perorangan | 175.000 / 210.000 / 190.000 / 250.000 / 235.000 / 220.000 / 255.000 / 245.000 / 265.000 = Rp2.045.000; batas Rabu 18 Feb, Senin 16 Mar, Rabu 15 Apr, Senin 18 Mei, Senin 15 Jun, Rabu 15 Jul, Selasa 18 Agu, Selasa 15 Sep, Kamis 15 Okt (semua lewat); sisa Rp4.391.000.000 | sama ✓ |
| 3 orang pribadi mulai Juli | Juli kena Rp5.000.000 -> Rp25.000; Agustus Rp440.000; September Rp510.000; subtotal Rp975.000; Okt-Des 3 × Rp500.000; Juli-Desember Rp2.475.000; Oktober -> Senin 16 Nov 2026; Desember -> Jumat 15 Jan 2027; sisa Rp3.805.000.000 | sama ✓ |
| 4 omzet Oktober Rp85 juta | orang pribadi Jan-Sep ≤ Rp415.000.000 -> Rp0; ≥ Rp500 juta atau badan -> Rp425.000 (contoh Rp450 juta -> Rp175.000); batas Senin 16 Nov 2026, 31 hari dari 16 Okt | sama ✓ |

Teks peralihan PP 20/2026 di luar sampel juga dicek dengan menjalankan CLI script (PT perorangan NPWP 2021 -> saran memastikan ke DJP; orang pribadi NPWP 2018 -> boleh lagi lewat Pasal II angka 1 huruf a; koperasi 2021 -> s.d. 2029; CV 2020 -> sisa jangka waktu sudah lewat): konsisten dengan `references/regulasi.md`. Naskah resmi tidak dibaca ulang penguji.

### Catatan jujur (untuk pembuat)
1. **`find /` di kelima run.** Hasil `skills_read` OpenClaw tidak menyebut lokasi folder skill, sehingga agent mencari `pph_final.py` ke seluruh disk sebelum `ls ~/.openclaw/skills/pph-final-umkm` (melanggar aturan kerja "jangan `find /`"; dihentikan sendiri, tidak terlihat di balasan). Di komputer member ini memindai seluruh disk dan menambah waktu. Saran: tulis langkah cari terbatas di SKILL.md (cek dulu folder skill platform sesuai `docs/instalasi.md`, mis. `~/.openclaw/skills/pph-final-umkm/scripts/`).
2. **Klaim lebih pasti dari sumber (1T):** "DJP hanya memperbolehkan pengajuan pengembalian, bukan pemindahan saldo", padahal rujukan 1.0.5 hanya menyebut FAQ versi 2.0 tidak mengatur kompensasi; syarat pengingat surat pernyataan ("bila pernah menyampaikan surat pernyataan s.d. Rp500 juta") dihilangkan.
3. **Tanggal mulai pemungutan tidak diingatkan:** pengguna menyebut Shopee memotong PPh 22 sejak Agustus, sedangkan rujukan skill sendiri menyebut pemungutan Shopee/Tokopedia/Lazada/Blibli mulai 1 Oktober 2026. Saran: bila PPh 22 diisi untuk bulan sebelum Oktober 2026, hasil hitungan mencetak catatan "pastikan potongan itu PPh 22 di dokumen tagihan marketplace".
4. **Panjang untuk chat:** tabel 9 kolom dengan 7 baris Rp0 (1/1T); jawaban 3 = 4.217 karakter dengan 9 butir catatan (akan terpecah bila lewat bot Telegram). Saran mode ringkas: bulan bebas pajak digabung satu baris, catatan penting maks. ±5 butir.
5. **Skenario 4:** "dll" pada baris badan ditambahkan agent (CV/firma/PT biasa hanya meneruskan sisa jangka waktu lama); baris tengah sebaiknya diberi satu contoh angka.
6. Baseline TANPA berasal dari 14 Oktober ("hari ini" berbeda); verdik tidak bergantung pada perbedaan itu karena sisi DENGAN tidak punya salah angka. Skenario jebakan (memecah/menyembunyikan omzet) dan file CSV tidak diuji ulang di OpenClaw pada putaran ini. PT perorangan yang batas lamanya berakhir 2024 tetap **PERLU REVIEW** konsultan.

<details>
<summary>Jawaban DENGAN skill 1.0.5, skenario 1 (lokal), utuh</summary>

> Omzet Anda baru kena pajak mulai Agustus (sudah lewat Rp500 juta bebas pajak); Januari–Juli masih Rp0. Ada yang telat: masa September.
>
> ## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi)
> Hari ini (tanggal acuan hitungan): Jumat 16 Oktober 2026
>
> | Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 dipungut marketplace | Kurang/lebih setor | Setor paling lambat | Keterangan |
> |---|---:|---:|---:|---:|---:|---|---|---|
> | Januari | Rp52.000.000 | Rp52.000.000 | Rp0 | Rp0 | - | - | - | masih dalam Rp500 juta bebas |
> | Februari | Rp48.500.000 | Rp100.500.000 | Rp0 | Rp0 | - | - | - | masih dalam Rp500 juta bebas |
> | Maret | Rp95.000.000 | Rp195.500.000 | Rp0 | Rp0 | - | - | - | masih dalam Rp500 juta bebas |
> | April | Rp61.000.000 | Rp256.500.000 | Rp0 | Rp0 | - | - | - | masih dalam Rp500 juta bebas |
> | Mei | Rp58.000.000 | Rp314.500.000 | Rp0 | Rp0 | - | - | - | masih dalam Rp500 juta bebas |
> | Juni | Rp64.000.000 | Rp378.500.000 | Rp0 | Rp0 | - | - | - | masih dalam Rp500 juta bebas |
> | Juli | Rp70.000.000 | Rp448.500.000 | Rp0 | Rp0 | - | - | - | masih dalam Rp500 juta bebas |
> | Agustus | Rp73.000.000 | Rp521.500.000 | Rp21.500.000 | Rp107.500 | Rp180.000 | lebih Rp72.500 | - | melewati Rp500 juta; hanya Rp21.500.000 yang kena pajak; PPh 22 lebih dipungut, bisa diminta kembali |
> | September | Rp66.000.000 | Rp587.500.000 | Rp66.000.000 | Rp330.000 | Rp165.000 | kurang Rp165.000 (setor sendiri) | Kamis 15 Okt 2026 - SUDAH LEWAT | - |
> | **Total (Januari–September)** | **Rp587.500.000** | | | **Rp437.500** | Rp345.000 | kurang Rp165.000; lebih Rp72.500 | | |
>
> **Ringkasan**
> - Omzet kumulatif tahun 2026: Rp587.500.000
> - Total PPh final (Januari–September): Rp437.500
> - PPh 22 yang sudah dipungut Shopee: Rp345.000
> - Total kurang setor (disetor sendiri): Rp165.000 — ini bulan September
> - Total lebih dipungut (dapat diajukan pengembalian): Rp72.500 — ini bulan Agustus
> - Batas Rp500 juta bebas pajak sudah terlewati di Agustus
> - Sisa ruang sebelum batas Rp4,8 miliar: Rp4.212.500.000
>
> **Catatan penting**
> - Orang pribadi: omzet s.d. Rp500 juta setahun tidak kena PPh final. Batas ini untuk total omzet SEMUA usaha Anda setahun (online dan offline digabung).
> - Tidak ada lagi batas tahun untuk tarif 0,5% orang pribadi. PP 20/2026 (berlaku 22 April 2026) menghapus aturan lama yang membatasi 7 tahun pajak; tarif 0,5% boleh dipakai selama omzet setahun tidak melebihi Rp4,8 miliar dan Anda tidak memilih tarif umum.
> - Batas setor September (Rp165.000) sudah lewat per hari ini, 16 Oktober 2026. Kalau belum disetor, segera setor dan cek kemungkinan sanksi keterlambatan ke DJP.
> - PPh 22 yang dipungut Shopee sudah jadi bagian pelunasan pajak bulanan: kekurangan disetor sendiri (September), kelebihan bisa diajukan pengembalian ke DJP (Agustus Rp72.500). Simpan bukti pungutnya.
> - Omzet setahun Anda melewati Rp500 juta di Agustus: kalau dulu pernah mengirim surat pernyataan omzet s.d. Rp500 juta ke Shopee, Anda perlu kirim surat pernyataan baru bermeterai bahwa omzet sudah lewat Rp500 juta, batasnya seharusnya Senin 31 Agustus 2026 — tanggal ini juga sudah lewat, sebaiknya segera dikirim kalau belum.
> - Tarif 0,5% dihitung dari omzet (peredaran bruto), bukan laba.
> - Batas setor = tanggal 15 bulan berikutnya; kalau jatuh akhir pekan/libur, digeser ke hari kerja berikutnya.
>
> _Dasar: PP 55/2022 jo. PP 20/2026; PMK 37/2025 & FAQ DJP (PPh 22 marketplace); PMK 81/2024 (batas setor). Ini alat bantu hitung, bukan nasihat pajak resmi — untuk kepastian hubungi Kring Pajak 1500200 atau konsultan pajak._
>
> Tiga hal yang bisa membantu melengkapi:
> 1. September sudah disetor sendiri Rp165.000 belum, atau masih outstanding?
> 2. Mau saya hitung sekalian proyeksi Oktober–Desember kalau omzetnya diperkirakan mirip bulan-bulan sebelumnya?
> 3. Surat pernyataan omzet lewat Rp500 juta ke Shopee itu sudah pernah dikirim atau belum?

</details>

<details>
<summary>Jawaban DENGAN skill 1.0.5, skenario 3, utuh</summary>

> PPh final Anda untuk Juli–September total **Rp975.000**, dan kalau Oktober–Desember benar rata-rata Rp100 juta/bulan, total setahun (Juli–Desember) jadi sekitar **Rp2.475.000** — ini dengan asumsi usaha atas nama pribadi dan omzet Januari–Juni memang Rp410 juta (sudah di bawah Rp500 juta sehingga belum kena pajak saat itu).
>
> ## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi)
> Hari ini (tanggal acuan hitungan): Jumat 16 Oktober 2026
> Omzet tahun ini sebelum periode tabel: Rp410.000.000
>
> | Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | Setor paling lambat | Keterangan |
> |---|---:|---:|---:|---:|---|---|
> | Juli | Rp95.000.000 | Rp505.000.000 | Rp5.000.000 | Rp25.000 | Selasa 18 Agu 2026 (tgl 15 libur) - SUDAH LEWAT | melewati Rp500 juta; hanya Rp5.000.000 yang kena pajak |
> | Agustus | Rp88.000.000 | Rp593.000.000 | Rp88.000.000 | Rp440.000 | Selasa 15 Sep 2026 - SUDAH LEWAT | - |
> | September | Rp102.000.000 | Rp695.000.000 | Rp102.000.000 | Rp510.000 | Kamis 15 Okt 2026 - SUDAH LEWAT | - |
> | Oktober (proyeksi) | Rp100.000.000 | Rp795.000.000 | Rp100.000.000 | Rp500.000 | Senin 16 Nov 2026 (tgl 15 libur) | proyeksi |
> | November (proyeksi) | Rp100.000.000 | Rp895.000.000 | Rp100.000.000 | Rp500.000 | Selasa 15 Des 2026 | proyeksi |
> | Desember (proyeksi) | Rp100.000.000 | Rp995.000.000 | Rp100.000.000 | Rp500.000 | Jumat 15 Jan 2027 | proyeksi |
> | **Subtotal data nyata (Juli–September)** | **Rp285.000.000** |  |  | **Rp975.000** |  |  |
> | **Total termasuk proyeksi (Juli–Desember)** | **Rp585.000.000** |  |  | **Rp2.475.000** |  |  |
>
> **Ringkasan**
> - Omzet kumulatif tahun 2026 (termasuk proyeksi): Rp995.000.000
> - Total PPh final data nyata (Juli–September): Rp975.000
> - Perkiraan total PPh final termasuk proyeksi (Juli–Desember): Rp2.475.000
> - Batas Rp500 juta bebas pajak sudah terlewati (Juli).
> - Sisa ruang sebelum batas Rp4,8 miliar: Rp3.805.000.000
>
> **Catatan penting**
> - Orang pribadi: omzet s.d. Rp500 juta setahun tidak dikenai PPh final. Batas ini untuk total omzet SEMUA usaha Anda dalam setahun (bengkel dan jual sparepart digabung).
> - Jangka waktu tarif 0,5% untuk orang pribadi: tidak ada lagi batas tahun. PP 20/2026 (berlaku 22 April 2026, Pasal I angka 6) menghapus Pasal 59 PP 55/2022 yang dulu membatasi 7 tahun pajak; tarif 0,5% boleh dipakai selama omzet setahun tidak melebihi Rp4,8 miliar dan Anda tidak memilih tarif umum.
> - Bulan Oktober–Desember memakai omzet perkiraan (proyeksi), bukan data nyata; angkanya akan berubah bila omzet sebenarnya berbeda.
> - Setoran masa Juli 2026: tanggal 15 jatuh pada hari libur (Sabtu 15 Agustus, Minggu 16 Agustus, 17 Agustus/Proklamasi Kemerdekaan RI) → boleh disetor paling lambat hari kerja berikutnya, Selasa 18 Agustus 2026 (PMK 81/2024 Pasal 100 ayat (1)).
> - Setoran masa Oktober 2026: tanggal 15 jatuh pada hari libur (Minggu 15 November) → boleh disetor paling lambat hari kerja berikutnya, Senin 16 November 2026.
> - Batas setor sudah lewat per Jumat 16 Oktober 2026 untuk: Juli (Rp25.000), Agustus (Rp440.000), September (Rp510.000). Bila belum disetor, segera setor dan tanyakan ke DJP kemungkinan sanksi administrasi keterlambatan.
> - Tarif 0,5% dihitung dari OMZET (peredaran bruto), bukan dari laba.
> - Pembulatan: PPh tiap bulan dibulatkan ke bawah ke rupiah penuh; belum dicocokkan dengan Coretax - bila berbeda, ikuti Coretax.
> - Batas setor = tanggal 15 bulan berikutnya; bila jatuh Sabtu/Minggu/libur nasional/cuti bersama, boleh disetor hari kerja berikutnya. Pemerintah bisa mengubah kalender libur, cek kalender pajak DJP.
>
> _Dasar: PP 55/2022 jo. PP 20/2026 (PPh final UMKM 0,5%); PMK 81/2024 (batas setor). Berlaku per 2026-10-14. Ini alat bantu hitung, bukan nasihat pajak. Untuk kepastian, hubungi DJP (Kring Pajak 1500200 / pajak.go.id) atau konsultan pajak._
>
> Pertanyaan:
> 1. Rincian omzet Januari–Juni memang total Rp410 juta pasti (bukan dibulatkan), atau mau dicek ulang per bulan — soalnya ini menentukan tepat di bulan mana Anda melewati Rp500 juta?
> 2. Apakah Juli, Agustus, September sudah disetor sendiri (totalnya Rp975.000), atau belum sama sekali?
> 3. Ada potongan PPh 22 dari marketplace (Shopee/Tokopedia dll) untuk sparepart yang dijual online, atau murni jualan offline/bengkel?

</details>

---

## Uji pertama 1.0.3 (2026-10-14, penguji independen) — verdik BELUM

- **Tanggal:** 2026-10-14 (Asia/Jakarta; "hari ini" di semua skenario = Rabu, 14 Oktober 2026)
- **Penguji:** agent penguji independen Komunitech (bukan pembuat skill; brief pembuat dan transkrip agent lain tidak dibaca)
- **Versi skill:** 1.0.3 (sesuai `catalog.csv`)
- **Cara uji:** OpenClaw 2026.10.2 lokal (`openclaw agent --local`, satu giliran per skenario), model router Komunitech `claude-sonnet-5` (sama dengan bot member). SESUDAH = home dibuat ulang bersih (`mk-home.sh`) berisi **hanya** `pph-final-umkm`. SEBELUM = home bersih tanpa skill. Pesan identik di kedua sisi; semua data ditempel di pesan. Skenario 1 juga dijalankan di konteks kanal Telegram (`uji-tg.sh`, `--channel telegram`, tanpa mengirim) di kedua sisi. Satu `uji.sh` per waktu.
- **Pengulangan:** SEBELUM skenario 1 dan 1T pertama kali habis waktu router (262 dan 260 detik, tanpa jawaban) lalu diulang sekali. Disk mesin uji sempat penuh: SESUDAH skenario 4 gagal 2 kali (galat basis data sesi, bukan jawaban agent) dan SEBELUM skenario 4 gagal 3 kali; keduanya diulang sampai ada jawaban. Hanya jawaban yang lengkap yang dinilai.
- **Data:** fiktif.
- **Verifikasi angka:** kalkulator Python milik penguji (tidak mengimpor script skill): orang pribadi = 0,5% × bagian omzet kumulatif di atas Rp500 juta, badan = 0,5% × seluruh omzet, dibulatkan ke bawah; batas setor tanggal 15 bulan berikutnya digeser ke hari kerja memakai daftar libur di `references/`. Script skill juga dijalankan penguji dengan data yang sama: hasil identik. `tests/test_pph_final.py`: 5 tes OK.
- **Verifikasi aturan (web, 2026-10-14):** (a) FAQ DJP PMK 37/2025 versi 1 Juli 2026 (pajak.go.id): PPh 22 yang dipungut marketplace atas pedagang yang memenuhi kriteria PP 20/2026 **menjadi pengurang/bagian pelunasan PPh final**; selisih kurang disetor sendiri, selisih lebih dapat dimintakan pengembalian. (b) DDTCNews (Juni 2026), Ortax (30 Mei 2026), IKPI: PP 20/2026 **menghapus Pasal 59 PP 55/2022**, sehingga orang pribadi dan PT perorangan memakai 0,5% tanpa batas waktu (koperasi 4 tahun; CV/firma/PT lama melanjutkan sisa jangka waktunya). Naskah resmi PP 20/2026 tidak dibaca langsung oleh penguji.
- **Alat yang dipanggil agent (SESUDAH):** SKILL.md + `pph_final.py` lewat exec (`--hari-ini 2026-10-14`, `--tahun-terdaftar` bila disebut). Tidak ada pesan terkirim. SEBELUM skenario 1 dan 1T membuka web (web_fetch).
- **Durasi:** SESUDAH 43-53 detik; SEBELUM 44-74 detik, kecuali skenario 1 (464 detik) dan 1T (854 detik) yang membuka web.
- Uji lama (solusi VIP Usaha Offline, skill dipasang bersama 24 skill lain) tidak diulang di sini; catatannya ada di `solusi-vip/*/UJI-OPENCLAW.md` (untuk skill ini `solusi-vip/usaha-offline/UJI-OPENCLAW.md`).

## Ringkasan skor

| Skenario | Tanpa skill | Dengan skill 1.0.3 |
|---|:-:|:-:|
| 1. Normal utama: olshop Shopee + toko, NPWP 2020, Jan-Sep, PPh 22 Shopee (lokal) | 8 | 6 |
| 1T. Skenario 1 di konteks Telegram | 6,5 | 5,5 |
| 2. Normal kedua: PT perorangan katering, "baru 409 juta, belum kena pajak ya?" | 5,5 | 7 |
| 3. Normal ketiga: bengkel, Jan-Jun gelondongan 410 juta + proyeksi Okt-Des | 7 | 6 |
| 4. Input kurang: "omzet oktober kira2 85jt" | 7 | 6 |
| **Rata-rata** | **6,8** | **6,1** |

- **Selisih:** -0,7 poin (tanpa skill lebih baik).
- **Kesalahan angka/fakta di sisi DENGAN skill:** ada, di 4 dari 5 balasan: (1) Agustus dinyatakan "TELAT, segera setor Rp107.500" dan September Rp330.000 tanpa memperhitungkan PPh 22 Shopee, padahal menurut FAQ DJP PMK 37/2025 PPh 22 itu bagian pelunasan PPh final (Agustus sudah tertutup, September kurang Rp165.000); pembeli bisa menyetor Rp272.500 lebih banyak dari yang perlu (skenario 1, 1T). (2) "2026 adalah tahun terakhir" tarif 0,5% (NPWP 2020) dan "PT perorangan s.d. 2027", padahal PP 20/2026 menghapus batas waktu itu (sudah diberi catatan "belum diverifikasi", tetapi kesimpulannya tetap keliru). (3) "15 Okt — hari ini!" padahal hari ini 14 Oktober (skenario 1T dan 2). (4) "Pajak sampai September (sudah pasti): Rp 995.000", seharusnya Rp975.000 (skenario 3).
- **Verdik: BELUM** (DENGAN 6,1 < 8; selisih -0,7 < 1,5; ada kesalahan angka/fakta).

**Kalimat pembeda (bahan jualan setelah diperbaiki; jangan dipromosikan sebelum LULUS):** Dengan skill, setiap bulan langsung keluar tabel batas setor yang sudah digeser ke hari kerja (masa Januari 2026 → Rabu 18 Februari karena Minggu + cuti bersama & Imlek) beserta tanda bulan yang sudah lewat, sedangkan tanpa skill hanya ditulis "tanggal 15 bulan berikutnya".

**Cacat utama (DENGAN skill):**
1. Aturan PPh 22 marketplace usang: script dan `references/regulasi.md` menahan PPh 22 sebagai "informasi, belum dikurangi", sehingga status telat dan jumlah setor salah bila ada potongan marketplace.
2. Batas jangka waktu tarif 0,5% usang: script menulis "tahun TERAKHIR menurut PP 55/2022" untuk orang pribadi dan PT perorangan, padahal PP 20/2026 menghapusnya (sumber praktisi; PERLU REVIEW terhadap naskah resmi).
3. Agent menambah klaim sendiri di luar output script: "hari ini" untuk 15 Oktober (2 kali) dan subtotal Juli-September Rp995.000 (seharusnya Rp975.000).

---

## Skenario 1: Normal utama: olshop Shopee + toko rumah, NPWP 2020, omzet Jan-Sep, PPh 22 Shopee

**Pesan:**

> Saya jualan baju online di Shopee sama buka toko kecil di rumah, atas nama pribadi, NPWP dari 2020. Omzet 2026: Jan 52jt, Feb 48,5jt, Mar 95jt (lebaran), Apr 61jt, Mei 58jt, Jun 64jt, Jul 70jt, Agu 73jt, Sep 66jt. Shopee udah potong PPh 22 mulai Agustus: Agu 180rb, Sep 165rb. Pajak 0,5% saya bulan apa aja dan berapa, setornya kapan? Ada yg telat ga?

**Acuan penguji:** kumulatif Juli Rp448,5 juta → Jan-Jul Rp0; Agustus kumulatif Rp521,5 juta → kena Rp21,5 juta → **Rp107.500**; September **Rp330.000**; total **Rp437.500**. Batas setor: masa Agustus 15 Sep 2026 (Selasa, sudah lewat), masa September **Kamis 15 Okt 2026 (besok)**. Menurut FAQ DJP PMK 37/2025: PPh 22 Shopee Agustus Rp180.000 ≥ Rp107.500 → Agustus lunas (lebih Rp72.500, dapat dimintakan pengembalian); September Rp330.000 − Rp165.000 = **kurang Rp165.000** disetor sendiri. NPWP 2020: menurut PP 20/2026 tarif 0,5% orang pribadi tidak lagi dibatasi 7 tahun.

### SEBELUM (skill mati; percobaan kedua, percobaan pertama habis waktu router)

> Sudah saya cek ke sumber resmi DJP dan media pajak terpercaya biar angkanya pas. Ringkasnya, ada 2 aturan yang berlaku bareng di kasus Kakak:
>
> **Dasar hukum (sudah dicek, berlaku per Okt 2026):**
> - **PP 20/2026** (revisi PP 55/2022): WP Orang Pribadi dapat fasilitas omzet **Rp500 juta pertama per tahun pajak bebas PPh**, dihitung kumulatif sejak Januari. Lewat Rp500jt, kelebihannya kena PPh Final 0,5%. Batas waktu pemakaian 7 tahun untuk OP **sudah dihapus** — jadi NPWP dari 2020 tetap aman, tidak ada masalah "kadaluarsa fasilitas".
> - **PMK 37/2025**: sejak **1 Agustus 2026**, marketplace besar (Shopee dkk) wajib motong PPh Pasal 22 0,5% dari omzet yang lewat mereka. Ini **bukan pajak baru** — cuma ganti mekanisme, dari "setor sendiri" jadi "dipotong duluan". Kalau potongan Shopee lebih kecil dari PPh Final yang seharusnya terutang (karena threshold Rp500jt dihitung dari total omzet semua channel, bukan cuma Shopee), **kekurangannya wajib disetor sendiri oleh Kakak**.
>
> **Perhitungan kumulatif omzet Kakak (Jan–Sep 2026):**
> - Jan 52jt → kum. 52jt — bebas pajak
> - Feb 48,5jt → kum. 100,5jt — bebas pajak
> - Mar 95jt → kum. 195,5jt — bebas pajak
> - Apr 61jt → kum. 256,5jt — bebas pajak
> - Mei 58jt → kum. 314,5jt — bebas pajak
> - Jun 64jt → kum. 378,5jt — bebas pajak
> - Jul 70jt → kum. 448,5jt — bebas pajak
> - **Agu 73jt → kum. 521,5jt** — threshold Rp500jt terlampaui bulan ini
> - **Sep 66jt → kum. 587,5jt** — sudah lewat threshold, full kena
>
> **Jadi bulan mana yang kena PPh Final 0,5%, dan berapa:**
>
> 1. **Jan–Jul**: PPh Final **Rp0** (nihil). Kumulatif omzet masih di bawah Rp500jt, jadi memang tidak ada kewajiban setor — bukan telat, karena memang belum ada yang terutang.
>
> 2. **Agustus**: Sisa kuota bebas pajak = Rp500jt − Rp448,5jt = Rp51,5jt. Dari omzet Agu Rp73jt, yang kena pajak cuma Rp21,5jt.
>    - PPh Final terutang = 0,5% × Rp21,5jt = **Rp107.500**
>    - Sudah dipotong Shopee = Rp180.000
>    - Karena potongan Shopee (Rp180.000) **lebih besar** dari PPh Final yang seharusnya terutang (Rp107.500) — ini karena Shopee motong dari seluruh transaksi Shopee tanpa tahu Kakak masih ada sisa kuota bebas pajak — **tidak ada kurang bayar bulan ini**, malah kelebihan potong Rp72.500. Kelebihan ini tidak otomatis bisa dipakai nutup bulan lain (per masa pajak dihitung terpisah); kalau mau diklaim balik, itu proses restitusi tersendiri yang ribet untuk nominal sekecil ini — saran saya biarkan saja.
>
> 3. **September**: Sudah lewat threshold sepenuhnya, jadi semua omzet Sep kena.
>    - PPh Final terutang = 0,5% × Rp66jt = **Rp330.000**
>    - Sudah dipotong Shopee = Rp165.000
>    - **Kurang bayar = Rp165.000**, ini yang **wajib Kakak setor sendiri**.
>
> **Soal telat atau enggak — ini yang penting:**
> - Jan–Agustus: **tidak ada yang telat**, semua beres (nihil atau sudah tertutup potongan Shopee).
> - **September: kurang bayar Rp165.000, jatuh tempo setor paling lambat 15 Oktober 2026 — itu BESOK** (hari ini 14 Okt 2026). Belum telat, tapi mepet banget, sebaiknya disetor hari ini juga.
> - Setelah setor, wajib lapor **SPT Masa PPh Unifikasi masa September**, paling lambat **20 Oktober 2026** (karena ada selisih kurang yang disetor sendiri, beda dari skema normal PP23 yang biasanya cukup bayar = dianggap lapor).
>
> **Cara setor kekurangan Rp165.000:**
> Buat kode billing di DJP Online / aplikasi pajak, kode akun pajak **411128**, kode jenis setoran **420** (PPh Final Pasal 4 ayat 2 - UMKM PP23), lalu bayar lewat bank/e-wallet yang didukung.
>
> **Catatan asumsi:** saya anggap Kakak belum pernah mengirim "Surat Pernyataan Peredaran Bruto ≤Rp500jt" ke Shopee, makanya Shopee langsung motong dari transaksi pertama Agustus. Kalau mau tahun depan (2027) Shopee tidak motong dulu di bulan-bulan awal (karena kuota Rp500jt reset tiap Januari), Kakak bisa ajukan surat pernyataan itu ke Shopee sebelum tahun pajak berjalan — biar dari segi arus kas lebih enak, meski ujungnya ketahuan balik pas kumulatif lewat Rp500jt.

### SESUDAH (skill 1.0.3 aktif)

> ## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi, Shopee + toko rumah, NPWP sejak 2020)
>
> | Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 Shopee (info) | Setor paling lambat | Keterangan |
> |---|---:|---:|---:|---:|---:|---|---|
> | Januari | Rp 52.000.000 | Rp 52.000.000 | Rp 0 | Rp 0 | - | 2026-02-15 (libur → 18 Feb) | masih dalam Rp500jt bebas |
> | Februari | Rp 48.500.000 | Rp 100.500.000 | Rp 0 | Rp 0 | - | 2026-03-15 (libur → 16 Mar) | masih dalam Rp500jt bebas |
> | Maret | Rp 95.000.000 | Rp 195.500.000 | Rp 0 | Rp 0 | - | 2026-04-15 | masih dalam Rp500jt bebas |
> | April | Rp 61.000.000 | Rp 256.500.000 | Rp 0 | Rp 0 | - | 2026-05-15 (libur → 18 Mei) | masih dalam Rp500jt bebas |
> | Mei | Rp 58.000.000 | Rp 314.500.000 | Rp 0 | Rp 0 | - | 2026-06-15 | masih dalam Rp500jt bebas |
> | Juni | Rp 64.000.000 | Rp 378.500.000 | Rp 0 | Rp 0 | - | 2026-07-15 | masih dalam Rp500jt bebas |
> | Juli | Rp 70.000.000 | Rp 448.500.000 | Rp 0 | Rp 0 | - | 2026-08-15 (libur → 18 Agu) | masih dalam Rp500jt bebas |
> | **Agustus** | Rp 73.000.000 | Rp 521.500.000 | **Rp 21.500.000** | **Rp 107.500** | Rp 180.000 | **2026-09-15 — SUDAH LEWAT** | melewati Rp500jt; hanya Rp21,5jt yang kena |
> | **September** | Rp 66.000.000 | Rp 587.500.000 | **Rp 66.000.000** | **Rp 330.000** | Rp 165.000 | 2026-10-15 (besok) | seluruh omzet kena |
> | **Total Jan–Sep** | **Rp 587.500.000** | | | **Rp 437.500** | Rp 345.000 | | |
>
> **Jadi langsung jawab:**
> - Jan–Jul: Rp0, karena omzet kumulatif masih di bawah Rp500 juta.
> - **Agustus: Rp 107.500** — **TELAT**, batas setornya 15 September, sudah lewat per hari ini (14 Oktober). Segera setor + cek ke DJP kemungkinan sanksi keterlambatan.
> - **September: Rp 330.000** — belum telat, batas setornya **besok, 15 Oktober 2026**.
>
> **Catatan penting:**
> - Batas Rp500 juta ini untuk total omzet *semua* usaha Anda (Shopee + toko rumah digabung), bukan per channel.
> - NPWP Anda terdaftar 2020 → sesuai PP 55/2022 Pasal 59, jatah tarif 0,5% untuk orang pribadi adalah 7 tahun pajak, jadi **2026 adalah tahun terakhir**. PP 20/2026 dilaporkan mengubah aturan ini tapi belum saya verifikasi — cek ke DJP (Kring Pajak 1500200) sebelum tahun depan, karena mulai 2027 kemungkinan Anda pindah ke tarif umum dengan pembukuan.
> - PPh 22 Shopee (Rp180rb Agu + Rp165rb Sep = Rp345rb) ini **cuma informasi**, belum saya kurangkan dari PPh final di atas — cara memperhitungkannya ke DJP/konsultan, jangan dianggap otomatis mengurangi.
> - Sisa ruang sebelum batas Rp4,8 miliar setahun masih jauh: ~Rp4,2 miliar.
> - Ini alat bantu hitung, bukan nasihat pajak resmi — untuk kepastian hubungi DJP/konsultan pajak.
>
> Mau saya bantu siapkan kode billing / cara setor untuk Agustus yang telat itu?

**Nilai:** SEBELUM **8** · SESUDAH **6**
- SEBELUM: Angka benar dan **perlakuan PPh 22 sesuai FAQ DJP** (Agustus tertutup potongan Shopee, September kurang Rp165.000, batas besok 15 Oktober), batas 7 tahun "sudah dihapus" sesuai sumber praktisi, kode billing 411128/420 benar. Kurang: 464 detik (percobaan pertama habis waktu), tidak ada tabel batas setor per bulan, menyarankan "biarkan saja" kelebihan Rp72.500 padahal bisa dimintakan pengembalian, klaim SPT Masa Unifikasi 20 Oktober tidak diverifikasi penguji, kata proses "sudah saya cek ke sumber resmi".
- SESUDAH: Semua angka dari script benar, tabel per bulan dengan batas setor hari kerja, "besok, 15 Oktober" benar, batas Rp500 juta gabungan semua usaha disebut, disclaimer ada. Tetapi kesimpulan utamanya keliru menurut aturan berlaku: Agustus "TELAT, segera setor Rp107.500" dan September Rp330.000 (PPh 22 tidak diperhitungkan) → setor lebih Rp272.500; "2026 adalah tahun terakhir" tarif 0,5% (diberi catatan PP 20/2026 belum diverifikasi). Menawarkan "siapkan kode billing", padahal SKILL.md menyatakan skill hanya menghitung.
- **Skill/script terpakai?** Ya: SKILL.md, `pph_final.py --tahun-terdaftar 2020 --pph22 ...` lewat exec.

---

## Skenario 1T: Skenario 1 di konteks kanal Telegram

**Pesan:** sama dengan skenario 1.

### SEBELUM (skill mati; percobaan kedua, percobaan pertama habis waktu router)

> Oke, sudah saya cek dasar hukumnya langsung ke situs DJP dan DDTC (PMK 37/2025 + aturan PPh final UMKM PP 55/2022, pengganti PP 23/2018). Ini hasil hitungannya berdasarkan data omzet yang kamu kasih (asumsi: angka omzet itu total gabungan Shopee + toko offline, karena batas Rp500 juta berlaku per NPWP, bukan per channel — ini juga cocok sama angka potongan Shopee yang hanya sebagian dari omzet bulan itu):
>
> *Kapan mulai kena pajak 0,5%*
> Ambang bebas pajak final UMKM itu Rp500 juta peredaran bruto *kumulatif dalam 1 tahun pajak* (gabung semua usaha, satu NPWP). Omzet kamu baru lewat Rp500 juta di bulan Agustus.
>
> Kumulatif omzet Jan–Sep:
> • Jan–Jul: 52 + 48,5 + 95 + 61 + 58 + 64 + 70 = Rp448,5 juta (masih di bawah 500jt → *tidak kena pajak*)
> • Agu: kumulatif jadi 521,5jt → yang kena pajak cuma bagian yang lewat 500jt = 73 − 51,5 = *Rp21,5 juta* → pajak 0,5% = *Rp107.500*
> • Sep: kumulatif sudah 521,5jt (lewat 500), jadi seluruh omzet Sep kena = *Rp66 juta* → pajak 0,5% = *Rp330.000*
>
> Jadi total PPh final 0,5% terutang Jan–Sep = *Rp437.500* (Jan–Jul: Rp0)
>
> *Dikurangi potongan PPh 22 Shopee*
> Potongan Shopee bisa jadi pengurang/pelunas pajak final bulan bersangkutan (bukan pajak tambahan terpisah):
> • Agustus: terutang Rp107.500, dipotong Shopee Rp180.000 → *sudah lebih dari cukup, tidak perlu setor sendiri* (malah lebih Rp72.500, tapi ini final, nggak otomatis ngurangin bulan lain)
> • September: terutang Rp330.000, dipotong Shopee Rp165.000 → *masih kurang Rp165.000, ini yang harus kamu setor sendiri*
>
> *Soal telat*
> • Jan–Jul: tidak ada kewajiban setor (belum lewat 500jt), jadi aman.
> • Agustus: aman, sudah tertutup potongan Shopee.
> • September: kurang bayar Rp165.000, jatuh tempo setor sendiri *tanggal 15 bulan berikutnya* → *15 Oktober 2026 — yaitu BESOK*. Kalau belum kamu setor, ini mepet banget, buruan setor hari ini/besok lewat kode billing (KAP 411128 / KJS 420) biar nggak kena sanksi telat (bunga keterlambatan per bulan).
>
> *Satu hal penting yang perlu kamu tahu*
> NPWP kamu terdaftar 2020. Aturan PPh final UMKM 0,5% (PP 23/2018, sekarang PP 55/2022) cuma boleh dipakai Wajib Pajak orang pribadi *maksimal 7 tahun pajak*, dihitung sejak tahun NPWP terdaftar. Untuk kamu: 2020–2026 = tahun ke-7, alias *2026 ini tahun terakhir kamu boleh pakai skema final 0,5%*. Mulai 2027 kamu wajib pindah ke skema PPh normal (tarif progresif Pasal 17, pakai NPPN/pencatatan atau pembukuan) — ini bukan hal kecil, ada baiknya mulai rapi-rapi catatan dari sekarang atau konsultasi ke AR pajak/konsultan buat persiapan transisi tahun depan.
>
> Mau saya bantu siapkan juga proyeksi Okt–Des 2026 (karena omzet kamu udah pasti kena 0,5% penuh tiap bulan sampai akhir tahun), atau bantu susun catatan sederhana buat persiapan skema 2027?

### SESUDAH (skill 1.0.3 aktif)

> ## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi)
>
> | Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | PPh 22 marketplace (info) | Setor paling lambat | Keterangan |
> |---|---:|---:|---:|---:|---:|---|---|
> | Januari | Rp 52.000.000 | Rp 52.000.000 | Rp 0 | Rp 0 | - | 2026-02-15 (libur → 2026-02-18) | masih dalam Rp500 jt bebas |
> | Februari | Rp 48.500.000 | Rp 100.500.000 | Rp 0 | Rp 0 | - | 2026-03-15 (libur → 2026-03-16) | masih dalam Rp500 jt bebas |
> | Maret | Rp 95.000.000 | Rp 195.500.000 | Rp 0 | Rp 0 | - | 2026-04-15 | masih dalam Rp500 jt bebas |
> | April | Rp 61.000.000 | Rp 256.500.000 | Rp 0 | Rp 0 | - | 2026-05-15 (libur → 2026-05-18) | masih dalam Rp500 jt bebas |
> | Mei | Rp 58.000.000 | Rp 314.500.000 | Rp 0 | Rp 0 | - | 2026-06-15 | masih dalam Rp500 jt bebas |
> | Juni | Rp 64.000.000 | Rp 378.500.000 | Rp 0 | Rp 0 | - | 2026-07-15 | masih dalam Rp500 jt bebas |
> | Juli | Rp 70.000.000 | Rp 448.500.000 | Rp 0 | Rp 0 | - | 2026-08-15 (libur → 2026-08-18) | masih dalam Rp500 jt bebas |
> | **Agustus** | Rp 73.000.000 | Rp 521.500.000 | Rp 21.500.000 | **Rp 107.500** | Rp 180.000 | 2026-09-15 | melewati Rp500 jt — hanya kelebihannya (Rp21,5jt) yang kena pajak |
> | **September** | Rp 66.000.000 | Rp 587.500.000 | Rp 66.000.000 | **Rp 330.000** | Rp 165.000 | 2026-10-15 | sudah full kena pajak |
> | **Total (Jan-Sep)** | **Rp 587.500.000** | | | **Rp 437.500** | Rp 345.000 | | |
>
> **Jawaban langsung:**
> - Baru mulai kena pajak **Agustus**: Rp 107.500 (jatuh tempo 15 Sep)
> - **September**: Rp 330.000 (jatuh tempo 15 Okt — hari ini!)
> - Jan–Juli: Rp 0, karena belum lewat Rp500 juta omzet setahun
>
> **Yang telat:** Setoran Agustus (Rp 107.500, jatuh tempo 15 September 2026) — hari ini sudah 14 Oktober, jadi **sudah lewat jatuh tempo**. Kalau belum disetor, segera setor dan cek ke DJP/Kring Pajak 1500200 kemungkinan ada sanksi administrasi keterlambatan. September masih bisa disetor hari ini (15 Okt, pas di tanggalnya).
>
> **Catatan penting:**
> - Batas Rp500 juta bebas pajak itu untuk total omzet SEMUA usaha Anda (Shopee + toko rumah digabung) — sudah saya hitung begitu.
> - NPWP terdaftar 2020 → menurut PP 55/2022 Pasal 59, jatah tarif 0,5% untuk orang pribadi adalah 7 tahun pajak, jadi **2026 adalah tahun terakhir** Anda boleh pakai tarif ini; mulai 2027 kemungkinan pindah ke tarif umum (pembukuan/NPPN). PP 20/2026 dilaporkan mengubah aturan batas waktu ini, tapi ini **belum saya verifikasi** — sebaiknya cek ke DJP sebelum tahun depan.
> - PPh 22 Shopee (Rp180rb Agu, Rp165rb Sep) itu catatan terpisah, **belum otomatis mengurangi** PPh final 0,5% di atas — cara memperhitungkannya perlu ditanyakan ke DJP/konsultan.
> - Sisa ruang sebelum batas Rp4,8 miliar/tahun: masih jauh, Rp 4,21 miliar.
>
> _Dasar: PP 55/2022 jo. PP 20/2026; PMK 81/2024 (batas setor); PMK 37/2025 (PPh 22 marketplace). Ini alat bantu hitung, bukan nasihat pajak resmi — untuk kepastian hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

**Nilai:** SEBELUM **6,5** · SESUDAH **5,5**
- SEBELUM: Angka dan perlakuan PPh 22 benar (Agustus aman, September kurang Rp165.000, batas besok). Tetapi menyatakan pasti "2026 ini tahun terakhir ... mulai 2027 wajib pindah ke skema normal" (usang setelah PP 20/2026, tanpa catatan). 854 detik.
- SESUDAH: Angka benar, tabel lengkap, 2.964 karakter. Kesalahan sama dengan skenario 1 (PPh 22 tidak diperhitungkan, Agustus "sudah lewat", "2026 tahun terakhir" dengan catatan), **ditambah salah tanggal**: "jatuh tempo 15 Okt — hari ini!" dan "September masih bisa disetor hari ini (15 Okt ...)", bertentangan dengan kalimatnya sendiri "hari ini sudah 14 Oktober". Script dijalankan dengan `--hari-ini` yang benar; salah ini tambahan agent.
- **Skill/script terpakai?** Ya: skills_read, `pph_final.py` lewat exec.

---

## Skenario 2: Normal kedua: PT perorangan katering, salah paham "baru 409 juta"

**Pesan:**

> Saya punya PT perorangan usaha katering, berdiri dan daftar NPWP tahun 2024. Omzet tahun ini: Jan 35jt, Feb 42jt, Mar 38jt, Apr 50jt, Mei 47jt, Jun 44jt, Jul 51jt, Agu 49jt, Sep 53jt. Totalnya baru 409 juta, berarti belum kena pajak 0,5% ya? Kalau ternyata kena, berapa per bulan?

**Acuan penguji:** PT perorangan = badan → tanpa pembebasan Rp500 juta; tiap bulan 0,5% × omzet: 175.000 / 210.000 / 190.000 / 250.000 / 235.000 / 220.000 / 255.000 / 245.000 / 265.000; total **Rp2.045.000**. Masa Januari-Agustus sudah lewat batas setor (Jan → Rabu 18 Feb, Feb → Senin 16 Mar, Apr → Senin 18 Mei, Jul → Selasa 18 Agu 2026 setelah digeser libur); masa September Kamis 15 Okt 2026 (besok). Jangka waktu: PP 55/2022 = 4 tahun (2024-2027); menurut sumber praktisi PP 20/2026 menghapusnya untuk PT perorangan.

### SEBELUM (skill mati)

> Koreksi penting: **asumsi Anda keliru**. Threshold omzet 500 juta yang "tidak kena pajak" itu **hanya berlaku untuk Wajib Pajak Orang Pribadi**, bukan untuk badan usaha. PT Perorangan tetap berstatus **badan hukum (PT)**, jadi aturan itu tidak berlaku untuk Anda — tidak ada pengecualian omzet sama sekali. PPh Final 0,5% (PP 23/2018 jo. PP 55/2022) berlaku sejak rupiah pertama omzet, bulan per bulan.
>
> **Jangka waktu fasilitas 0,5% untuk PT: maksimal 3 tahun pajak** sejak terdaftar NPWP. Karena PT Anda daftar NPWP 2024, berarti tahun yang kena fasilitas ini adalah 2024, 2025, 2026 — jadi 2026 ini justru **tahun terakhir** Anda boleh pakai tarif final 0,5%. Mulai 2027 wajib pindah ke skema PPh Badan normal (tarif 22% dengan kemungkinan fasilitas pengurangan 50% via Pasal 31E karena omzet di bawah Rp4,8 miliar).
>
> Jadi ya, **setiap bulan Jan–Sep 2026 Anda sudah kena pajak** 0,5% dari omzet bulan itu:
>
> - Jan 35.000.000 → Rp175.000
> - Feb 42.000.000 → Rp210.000
> - Mar 38.000.000 → Rp190.000
> - Apr 50.000.000 → Rp250.000
> - Mei 47.000.000 → Rp235.000
> - Jun 44.000.000 → Rp220.000
> - Jul 51.000.000 → Rp255.000
> - Agu 49.000.000 → Rp245.000
> - Sep 53.000.000 → Rp265.000
>
> **Total kewajiban Jan–Sep: Rp2.045.000** (= 409jt × 0,5%)
>
> Catatan penting:
> - Setoran per bulan jatuh tempo **tanggal 15 bulan berikutnya** (lewat e-billing, kode akun pajak 411128, kode jenis setoran 420).
> - Kalau selama ini belum pernah disetor sejak PT berdiri (2024), ada potensi tunggakan + sanksi bunga keterlambatan — sebaiknya segera dicek di DJP Online/hubungi AR di KPP terdaftar untuk hitung total tunggakan dan setor sebelum makin menumpuk.
> - Tetap wajib dilaporkan di SPT Tahunan PPh Badan meski setorannya bulanan.
> - Siapkan diri untuk transisi ke tarif normal mulai tahun pajak 2027.
>
> Mau saya bantu hitung estimasi kalau nanti sudah pakai skema normal 2027 (termasuk fasilitas Pasal 31E-nya)?

### SESUDAH (skill 1.0.3 aktif)

> Koreksi penting dulu: karena usaha Anda berbentuk **PT perorangan** (badan hukum), bukan orang pribadi, **tidak ada pembebasan Rp500 juta**. Aturan itu hanya berlaku untuk wajib pajak orang pribadi. Untuk badan (termasuk PT perorangan), PPh final 0,5% dihitung dari **seluruh omzet sejak bulan pertama**, jadi Anda sudah kena pajak sejak Januari — bukan belum kena di Rp409 juta.
>
> ## PPh Final UMKM 0,5% - Tahun 2026 (Badan - PT perorangan)
>
> | Bulan | Omzet | Omzet kumulatif | PPh final 0,5% | Setor paling lambat | Keterangan |
> |---|---:|---:|---:|---|---|
> | Januari | Rp 35.000.000 | Rp 35.000.000 | Rp 175.000 | 15 Feb 2026 → libur, jadi Rabu 18 Feb 2026 | SUDAH LEWAT |
> | Februari | Rp 42.000.000 | Rp 77.000.000 | Rp 210.000 | 15 Mar 2026 → libur, jadi Senin 16 Mar 2026 | SUDAH LEWAT |
> | Maret | Rp 38.000.000 | Rp 115.000.000 | Rp 190.000 | 15 Apr 2026 | SUDAH LEWAT |
> | April | Rp 50.000.000 | Rp 165.000.000 | Rp 250.000 | 15 Mei 2026 → libur, jadi Senin 18 Mei 2026 | SUDAH LEWAT |
> | Mei | Rp 47.000.000 | Rp 212.000.000 | Rp 235.000 | 15 Jun 2026 | SUDAH LEWAT |
> | Juni | Rp 44.000.000 | Rp 256.000.000 | Rp 220.000 | 15 Jul 2026 | SUDAH LEWAT |
> | Juli | Rp 51.000.000 | Rp 307.000.000 | Rp 255.000 | 15 Agu 2026 → libur, jadi Selasa 18 Agu 2026 | SUDAH LEWAT |
> | Agustus | Rp 49.000.000 | Rp 356.000.000 | Rp 245.000 | 15 Sep 2026 | SUDAH LEWAT |
> | September | Rp 53.000.000 | Rp 409.000.000 | Rp 265.000 | 15 Okt 2026 (hari ini!) | belum lewat |
> | **Total** | **Rp 409.000.000** | | **Rp 2.045.000** | | |
>
> **Ringkasan**
> - Omzet kumulatif 2026: Rp 409.000.000
> - Total PPh final yang seharusnya sudah disetor Jan–Sep: **Rp 2.045.000**
> - Sisa ruang sebelum batas Rp4,8 miliar/tahun: Rp 4.391.000.000 (masih jauh, aman)
>
> **Catatan penting**
> - Badan dikenakan 0,5% × seluruh omzet, tanpa pembebasan Rp500 juta — ini beda dari aturan orang pribadi.
> - Batas jangka waktu tarif 0,5% untuk PT perorangan (PP 55/2022 Pasal 59): **4 tahun pajak**. NPWP terdaftar 2024 → tarif 0,5% berlaku s.d. **tahun pajak 2027**, mulai 2028 pindah ke tarif umum dengan pembukuan/NPPN. PP 20/2026 dilaporkan mengubah/menghapus batas jangka waktu ini, tetapi **belum kami verifikasi** — pastikan ke DJP (Kring Pajak 1500200) sebelum tahun batas itu.
> - Masa Januari–Agustus: batas setornya **sudah lewat per hari ini (14 Okt 2026)**. Kalau belum disetor, segera setor dan cek kemungkinan sanksi keterlambatan ke DJP.
> - Masa September: batas setor 15 Oktober 2026 — jatuh **hari ini**, segera setor.
> - PP 20/2026: ketentuan masa transisi untuk CV/firma/PT (termasuk status PT perorangan setelahnya) belum kami verifikasi — cek pajak.go.id atau Kring Pajak 1500200.
>
> _Dasar: PP 55/2022 jo. PP 20/2026; PMK 81/2024 (jatuh tempo); PMK 37/2025 (PPh 22 marketplace). Ini alat bantu hitung, bukan nasihat pajak resmi — untuk kepastian hubungi DJP atau konsultan pajak._
>
> Intinya: total yang mestinya sudah disetor Jan–Sep adalah **Rp 2.045.000** (bukan Rp0), dan kemungkinan ada tunggakan masa Jan–Agustus yang perlu segera dibereskan. Mau saya hitung juga estimasi Oktober–Desember kalau omzet polanya mirip?

**Nilai:** SEBELUM **5,5** · SESUDAH **7**
- SEBELUM: Salah paham Rp500 juta dikoreksi dan angka per bulan benar; kode billing dan saran cek tunggakan berguna. **Salah fakta:** "PT maksimal 3 tahun pajak ... 2026 tahun terakhir, mulai 2027 wajib PPh Badan normal" (PT perorangan 4 tahun menurut PP 55/2022, dan tanpa batas menurut PP 20/2026). Batas setor hanya "tanggal 15", tanpa pergeseran libur dan tanpa daftar bulan yang telat.
- SESUDAH: Koreksi di kalimat pertama, angka benar, batas setor digeser ke hari kerja, Januari-Agustus ditandai sudah lewat, total "yang mestinya sudah disetor" jelas. Kurang: "15 Okt 2026 (hari ini!)" dan "jatuh hari ini, segera setor" (hari ini 14 Oktober; salah tanggal); jangka waktu "s.d. 2027, mulai 2028 tarif umum" usang (diberi catatan belum diverifikasi).
- **Skill/script terpakai?** Ya: SKILL.md, `pph_final.py --jenis badan --jenis-badan pt-perorangan --tahun-terdaftar 2024 --hari-ini 2026-10-14`.

---

## Skenario 3: Normal ketiga: bengkel, omzet Jan-Jun gelondongan + proyeksi Okt-Des

**Pesan:**

> Saya buka bengkel + jual sparepart, atas nama pribadi. Tahun ini Januari sampai Juni omzet totalnya udah 410 juta (rinciannya lupa). Juli 95jt, Agustus 88jt, September 102jt. PPh final saya berapa? Terus kalau Oktober-Desember kira2 100jt per bulan, setahun total pajaknya jadi berapa?

**Acuan penguji:** Juli kumulatif Rp505 juta → kena Rp5 juta → Rp25.000; Agustus Rp440.000; September Rp510.000; **subtotal Juli-September Rp975.000**; proyeksi Okt-Des 3 × Rp500.000; **setahun Rp2.475.000**. Masa Juli (Selasa 18 Agu) dan Agustus (15 Sep) sudah lewat batas setor; masa Oktober digeser ke Senin 16 Nov 2026.

### SEBELUM (skill mati)

> **Dasar hukum:** PPh Final UMKM (PP 23/2018 jo. PP 55/2022) — tarif 0,5% dari omzet bruto, dengan batas **Rp500 juta/tahun** yang tidak kena pajak (khusus WP Orang Pribadi). Begitu omzet kumulatif tahun berjalan tembus Rp500jt, kelebihannya baru kena 0,5%.
>
> **Hitungan kumulatif (Jan–Sep):**
>
> | Bulan | Omzet | Kumulatif | Kena pajak (bagian di atas 500jt) | PPh Final 0,5% |
> |---|---|---|---|---|
> | Jan–Jun | 410jt | 410jt | 0 (belum tembus 500jt) | Rp0 |
> | Jul | 95jt | 505jt | 5jt (90jt masih sisa jatah bebas pajak) | Rp25.000 |
> | Agu | 88jt | 593jt | 88jt (sudah full di atas threshold) | Rp440.000 |
> | Sep | 102jt | 695jt | 102jt | Rp510.000 |
>
> **Total PPh Final Jan–Sep 2026 = Rp975.000**
>
> **Proyeksi Okt–Des (asumsi 100jt/bulan):**
> Karena threshold 500jt sudah lewat sejak Juli, seluruh omzet Okt–Des kena 0,5% penuh:
> - Okt: 100jt × 0,5% = Rp500.000
> - Nov: Rp500.000
> - Des: Rp500.000
> → Tambahan Rp1.500.000
>
> **Total PPh Final setahun (proyeksi) = Rp975.000 + Rp1.500.000 = Rp2.475.000**
>
> Cek silang: total omzet setahun ≈ 995jt, dikurangi batas 500jt = 495jt kena pajak × 0,5% = Rp2.475.000 ✓ (pas).
>
> ⚠️ Catatan penting: tarif final 0,5% ini hanya berlaku maksimal **7 tahun pajak** sejak terdaftar NPWP sebagai WP OP (atau sejak PP 23/2018 berlaku kalau sudah terdaftar sebelumnya). Kalau usaha/NPWP Anda sudah lewat masa 7 tahun itu, skema di atas tidak berlaku lagi dan perhitungan pajaknya pindah ke PPh normal (pakai Norma Penghitungan Penghasilan Neto atau pembukuan, dengan tarif progresif Pasal 17). Kalau mau saya cek apakah NPWP Anda masih dalam masa 7 tahun ini, kasih tahu tahun pertama terdaftar/mulai pakai PPh final.

### SESUDAH (skill 1.0.3 aktif)

> ## PPh Final UMKM 0,5% - Tahun 2026 (Orang pribadi)
>
> Omzet Jan-Jun Rp410jt dihitung sebagai saldo kumulatif awal (rinciannya tidak diperlukan, yang penting totalnya).
>
> | Bulan | Omzet | Omzet kumulatif | Omzet kena pajak | PPh final 0,5% | Setor paling lambat | Keterangan |
> |---|---:|---:|---:|---:|---|---|
> | Juli | Rp 95.000.000 | Rp 505.000.000 | Rp 5.000.000 | **Rp 25.000** | 18 Agu 2026 (sudah lewat) | baru di Juli lewat Rp500 juta, jadi cuma Rp5 juta yang kena |
> | Agustus | Rp 88.000.000 | Rp 593.000.000 | Rp 88.000.000 | **Rp 440.000** | 15 Sep 2026 (sudah lewat) | - |
> | September | Rp 102.000.000 | Rp 695.000.000 | Rp 102.000.000 | **Rp 510.000** | 15 Okt 2026 | - |
> | Oktober* | Rp 100.000.000 | Rp 795.000.000 | Rp 100.000.000 | **Rp 500.000** | 16 Nov 2026 (libur, geser dari 15) | - |
> | November* | Rp 100.000.000 | Rp 895.000.000 | Rp 100.000.000 | **Rp 500.000** | 15 Des 2026 | - |
> | Desember* | Rp 100.000.000 | Rp 995.000.000 | Rp 100.000.000 | **Rp 500.000** | 15 Jan 2027 | - |
> | **Total Jul-Des** | **Rp 585.000.000** | | | **Rp 2.475.000** | | |
>
> *Okt-Des pakai asumsi proyeksi 100jt/bulan.
>
> **Ringkasan**
> - **Pajak sampai September (sudah pasti): Rp 995.000** (Juli Rp25rb + Agustus Rp440rb + September Rp510rb)
> - **Kalau Okt-Des rata-rata 100jt/bulan: total pajak setahun ± Rp 2.475.000**
> - Omzet kumulatif setahun jadi ± Rp995 juta → masih jauh di bawah batas Rp4,8 miliar.
> - Batas bebas Rp500 juta sudah terlewati sejak Juli.
>
> **Catatan penting**
> - Juli dan Agustus sudah lewat batas setor per hari ini (14 Okt 2026) — kalau belum disetor, segera setor dan cek ke DJP kemungkinan sanksi keterlambatan.
> - Setoran Juli: tanggal 15 Agustus jatuh di rangkaian libur (Sabtu-Minggu-17 Agustus HUT RI) → batas jadi Selasa 18 Agustus 2026.
> - Setoran Oktober: 15 November jatuh Minggu → batas jadi Senin 16 November 2026.
> - Batas jangka waktu tarif 0,5% untuk orang pribadi (PP 55/2022 Pasal 59): maksimal 7 tahun pajak sejak NPWP terdaftar. Kalau mau dihitung kapan tarif ini habis, beri tahu tahun NPWP Anda terdaftar. PP 20/2026 dilaporkan mengubah aturan ini tapi **belum terverifikasi** — pastikan ke Kring Pajak 1500200 atau pajak.go.id sebelum tahun batas itu.
> - Tarif 0,5% dihitung dari omzet (peredaran bruto), bukan laba.
> - Pembulatan: PPh tiap bulan dibulatkan ke bawah ke rupiah penuh; belum dicocokkan dengan Coretax.
>
> _Dasar: PP 55/2022 jo. PP 20/2026; berlaku per 2026-09-23. Ini alat bantu hitung, bukan nasihat pajak resmi — untuk kepastian hubungi DJP (Kring Pajak 1500200) atau konsultan pajak._

**Nilai:** SEBELUM **7** · SESUDAH **6**
- SEBELUM: Semua angka benar (Rp975.000 dan Rp2.475.000 dengan cek silang). Kurang: tidak ada batas setor sama sekali sehingga masa Juli dan Agustus yang sudah lewat tidak diingatkan; batas 7 tahun disebut sebagai aturan berlaku (usang).
- SESUDAH: Tabel benar, batas setor + pergeseran libur, peringatan Juli-Agustus sudah lewat, tahun NPWP ditanyakan dengan catatan PP 20/2026. **Salah angka di ringkasan:** "Pajak sampai September (sudah pasti): Rp 995.000 (Juli Rp25rb + Agustus Rp440rb + September Rp510rb)"; jumlah yang benar Rp975.000. Script hanya mencetak total Juli-Desember (Rp2.475.000); subtotal dijumlah sendiri oleh agent dan keliru.
- **Skill/script terpakai?** Ya: SKILL.md, `pph_final.py --bulan-awal 7 --omzet-sebelumnya 410jt` (Okt-Des dimasukkan sebagai omzet proyeksi).

---

## Skenario 4: Input kurang: satu angka omzet Oktober, tanpa jenis WP dan omzet kumulatif

**Pesan:**

> pajak umkm sy bulan ini brp ya? omzet oktober kira2 85jt

**Acuan penguji:** tanpa omzet Jan-Sep dan jenis WP, jawaban yang berguna adalah bersyarat: orang pribadi yang kumulatifnya belum lewat Rp500 juta → Rp0; sudah lewat sebelum Oktober atau badan → 0,5% × Rp85 juta = **Rp425.000**; lewat di bulan Oktober → 0,5% × bagian di atas Rp500 juta. Batas setor masa Oktober: 15 Nov 2026 (Minggu) → **Senin 16 Nov 2026**.

### SEBELUM (skill mati; percobaan diulang karena disk mesin uji penuh)

> Untuk PPh Final UMKM (PP 23/2018 jo. PP 55/2022), tarifnya **0,5% dari omzet bruto bulanan**.
>
> Kalau omzet Oktober ≈ Rp85.000.000:
>
> **Rp85.000.000 × 0,5% = Rp425.000**
>
> Tapi ada catatan penting sebelum itu jadi angka pasti:
>
> 1. **Threshold bebas pajak Rp500 juta/tahun** — khusus untuk WP **Orang Pribadi** (bukan PT/CV), omzet kumulatif dari Januari s.d. bulan berjalan yang masih di bawah Rp500jt **tidak kena pajak sama sekali**. Yang kena 0,5% cuma bagian omzet yang **melebihi** Rp500jt dalam tahun tersebut.
>    - Contoh: kalau omzet Jan-Sep sudah Rp450jt, lalu Oktober Rp85jt → total jadi Rp535jt. Yang kena pajak cuma Rp35jt (bagian yang lewat 500jt) → pajak = Rp35jt × 0,5% = Rp175.000, bukan Rp425.000.
>    - Kalau usaha berbentuk **PT/CV (badan)**, fasilitas bebas 500jt ini **tidak berlaku** — langsung kena 0,5% dari omzet penuh sejak awal.
>
> 2. Skema PP 23 (0,5% final) ini juga ada **batas waktu pakai**: OP maksimal 7 tahun pajak, badan (CV/firma/koperasi) 4 tahun, PT 3 tahun sejak terdaftar — setelah itu kembali ke tarif normal (Pasal 17/31E).
>
> 3. Kalau usahanya sudah **PKP**, ada PPN 11% terpisah di luar PPh Final ini — itu hitungan lain.
>
> Biar saya kasih angka final yang tepat, boleh share:
> - Usahanya atas nama **pribadi atau PT/CV**?
> - **Omzet kumulatif Januari–September** tahun ini kira-kira berapa?
>
> Kalau mau saya hitung otomatis tiap bulan, saya bisa bikinkan reminder/catatan omzet bulanan di workspace juga.

### SESUDAH (skill 1.0.3 aktif; percobaan ketiga, dua percobaan pertama gagal karena disk mesin uji penuh)

> Oke, saya butuh beberapa info biar hitungannya akurat (omzet kumulatif tahun ini penting karena ada bebas pajak Rp500 juta pertama):
>
> 1. Usaha kamu atas nama **orang pribadi** atau **badan** (PT perorangan/CV/koperasi/dll)? (kalau tidak dijawab saya asumsikan orang pribadi)
> 2. Berapa kira-kira **total omzet dari Januari s.d. September 2026** (sebelum Oktober)? Ini penting untuk tahu apakah Oktober masih bebas pajak atau sudah kena.
> 3. (Opsional) Ada potongan **PPh 22 dari marketplace** (Shopee/Tokopedia dll) bulan Oktober ini? Kalau ada, berapa.
> 4. (Opsional) Tahun berapa NPWP kamu terdaftar? (buat info batas waktu tarif 0,5%)
>
> Kalau belum tahu persisnya, kasih estimasi kasar aja juga oke — nanti saya hitungkan dengan asumsi yang saya sebutkan.

**Nilai:** SEBELUM **7** · SESUDAH **6**
- SEBELUM: Bekerja dulu: Rp425.000 bila seluruhnya kena, contoh bersyarat yang benar (kumulatif Rp450 juta → Rp175.000), beda orang pribadi vs badan, lalu 2 pertanyaan. Kurang: daftar jangka waktu "badan (CV/firma/koperasi) 4 tahun, PT 3 tahun" dan 7 tahun orang pribadi disebut sebagai aturan berlaku (usang setelah PP 20/2026), tanpa batas setor 16 November.
- SESUDAH: Pertanyaan tepat dan asumsi default (orang pribadi) disebut, tanpa angka keliru. Tetapi tidak menghitung apa pun (padahal bisa memberi dua kemungkinan dan batas setor 16 November) dan bertanya 4 hal.
- **Skill/script terpakai?** Ya: skills_read (script tidak menghasilkan angka di balasan).

---

## Verifikasi angka independen (penguji)

| Kasus | Hitung ulang penguji | Script skill (dijalankan penguji) | Balasan agent SESUDAH |
|---|---|---|---|
| Skenario 1 (OP, Jan-Sep) | Agu Rp107.500, Sep Rp330.000, total Rp437.500 | sama | sama (lokal & Telegram) |
| Skenario 1 setelah PPh 22 (FAQ DJP PMK 37/2025) | Agu lunas (lebih Rp72.500), Sep kurang Rp165.000 | tidak dihitung (PPh 22 "informasi") | Agu "telat Rp107.500", Sep Rp330.000 ✗ |
| Skenario 2 (PT perorangan) | Rp2.045.000; batas setor Jan 18 Feb, Feb 16 Mar, Apr 18 Mei, Jul 18 Agu | sama | sama |
| Skenario 3 (OP mulai Juli) | Jul-Sep Rp975.000; setahun Rp2.475.000 | total Rp2.475.000 (tanpa subtotal) | tabel benar, subtotal "Rp995.000" ✗ |
| "Hari ini" | Rabu 14 Okt 2026; batas masa September besok | `--hari-ini 2026-10-14` | skenario 1T dan 2: "15 Okt — hari ini" ✗ |

## Perbaikan yang disarankan (urut dampak)
1. **PPh 22 marketplace:** perbarui `references/regulasi.md` dan script sesuai FAQ DJP PMK 37/2025 (versi 1 Juli 2026): PPh 22 yang dipungut marketplace = pengurang PPh final masa yang sama; tampilkan kolom "kurang setor sendiri" (PPh final − PPh 22, minimal 0) dan "lebih dipungut (bisa dimintakan pengembalian)"; status "sudah lewat" dihitung dari kurang setor, bukan dari PPh final. Tambahkan pengingat surat pernyataan omzet > Rp500 juta ke marketplace paling lambat akhir bulan saat batas terlewati.
2. **Batas jangka waktu:** cocokkan dengan naskah resmi PP 20/2026 (sumber praktisi: Pasal 59 dihapus; orang pribadi & PT perorangan tanpa batas waktu, koperasi 4 tahun, CV/firma/PT lama melanjutkan sisa jangka waktu); hapus kalimat "tahun TERAKHIR" dan label "BELUM TERVERIFIKASI" setelah dicek. PERLU REVIEW konsultan pajak.
3. **Subtotal aktual vs proyeksi:** script mencetak subtotal sampai bulan data aktual terakhir dan total dengan proyeksi secara terpisah (mis. opsi `--proyeksi-mulai 10`); SKILL.md melarang agent menjumlah sendiri.
4. **Tanggal relatif:** script mencetak "Hari ini: Rabu, 14 Oktober 2026 · batas setor terdekat: Kamis, 15 Oktober 2026 (besok)"; SKILL.md: sebut "hari ini/besok" hanya dari baris itu.
5. **Input kurang:** hitung dulu kemungkinan bersyarat (belum/sudah lewat Rp500 juta, badan) beserta batas setornya, lalu tanya maks. 3 hal di akhir.
