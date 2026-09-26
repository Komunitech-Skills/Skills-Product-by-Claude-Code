---
name: laporan-harian-usaha
description: Satu laporan harian/mingguan gabungan untuk pemilik usaha dari alat lokal Komunitech yang terpasang (kasir-lokal, buku-stok, absensi-lokal, pengingat-follow-up, crm-wa) - omzet & perbandingan % dengan kemarin/minggu lalu, stok menipis/habis, kehadiran & lembur, tagihan jatuh tempo, prospek/pipeline CRM & konversi, hal yang perlu perhatian - siap kirim ke Telegram pemilik lewat OpenClaw tiap malam/Senin pagi, hanya membaca data. Gunakan saat pengguna minta "laporan harian usaha", "ringkasan toko hari ini", "rekap semua", "dashboard usaha", daily business report, owner dashboard. Rekap satu alat saja pakai skill alat itu.
---

# Laporan Harian Usaha (pengganti dashboard SaaS)

## Tujuan
Pemilik usaha cukup membaca **satu pesan** tiap malam (dan satu tiap Senin pagi) untuk tahu kondisi usahanya: penjualan, stok, karyawan, tagihan, dan apa yang harus dibereskan besok. Semua angka diambil dari alat lokal Komunitech yang sudah ia pakai, dijalankan oleh `scripts/laporan.py`. Tanpa aplikasi dashboard berbayar, tanpa internet, data tetap di komputernya.

## Kapan digunakan
- "Laporan usaha hari ini", "ringkasan toko hari ini", "rekap semua", "gimana usaha kemarin?"
- "Laporan minggu lalu", "bandingkan dengan minggu sebelumnya"
- "Kirim laporan harian ke Telegram saya tiap jam 9 malam" / "tiap Senin pagi kirim laporan mingguan" (OpenClaw)

## Kapan TIDAK digunakan
- Hanya butuh satu hal: struk/tutup kasir/rekap bulanan pajak → `kasir-lokal`; opname/picking → `buku-stok`; rekap gaji & upah lembur → `absensi-lokal`; draf tagihan & nama pelanggan → `pengingat-follow-up` ("rekap pengingat"); nama/nomor prospek, draf follow-up, atau catat lead baru → `crm-wa` ("follow-up hari ini", "rekap CRM", "catat: ...").
- Data dari file CSV/Excel aplikasi lain (Moka, Majoo, marketplace) → `rekap-penjualan-csv`. Laporan terjadwal dari file seperti itu → `laporan-otomatis-terjadwal`.
- Laba rugi/neraca → `laporan-keuangan-emkm`. Arus kas ke depan → `arus-kas-13minggu`.
- **Mengubah data** (catat penjualan, stok, absen, tandai lunas) → skill alatnya masing-masing. Skill ini **hanya membaca**.
- Kirim laporan ke pelanggan/grup/broadcast → **tolak**. Laporan hanya untuk pemilik, atau penerima lain yang **pemilik tunjuk secara eksplisit** (chat pribadi masing-masing) — lihat Langkah C.

## Cara kerja (penting untuk dijelaskan bila ditanya)
1. Script mencari alat yang terpasang dari lokasi data default masing-masing alat (ENV sama: `KOMUNITECH_KASIR_DB`, `KOMUNITECH_STOK_DB`, `KOMUNITECH_ABSENSI_DB`, `KOMUNITECH_CRM_DB`, `KOMUNITECH_DATA`) dan `pengingat/DAFTAR.csv` (folder kerja, workspace OpenClaw `~/.openclaw/workspace`, atau `~/KomunitechData`). Alat yang tidak ada **dilewati dengan catatan**, bukan error.
2. Database dibuka **read-only** (`mode=ro`, batas tunggu 10 detik) lalu disalin ke folder sementara. File asli tidak pernah ditulis (diuji: sidik file sebelum = sesudah) — berlaku juga untuk database crm-wa.
3. Angka dihitung oleh **perintah laporan resmi** tiap alat (`kasir.py rekap`, `stok.py laporan ringkas`, `absensi.py harian/rekap`, `cek_jatuh_tempo.py rekap`, `crm.py rekap --json`) pada salinan itu. Karena memakai "pintu resmi" alat, laporan tetap benar walau struktur database alat berubah di versi baru. Hanya 3 hal dibaca langsung dari salinan (dengan cek kolom dulu; jika berubah, bagian itu dilewati dan catatannya ikut tampil di PERLU PERHATIAN): selisih kas (tabel `sesi` kasir); nota kasir yang **sah** (bukan yang di-void) per tanggal dibandingkan satu per satu dengan nomor nota di tabel `pesanan` buku-stok, jadi impor **sebagian** pun terdeteksi, begitu juga nota yang di-void **setelah** diimpor tetapi stoknya belum dikembalikan (`pesanan.dibatalkan` = 0); dan jam masuk paling awal (tabel `shift`+`karyawan` absensi) untuk menghindari alarm keliru sebelum jam kerja mulai. Bagian PROSPEK memakai `crm.py rekap --json` (kontrak `skema_json` 1) apa adanya, tanpa baca tabel langsung.
4. Script alat dicari di folder skills yang sama dengan skill ini (lalu `~/.openclaw/skills`, `~/.claude/skills`, `~/.agents/skills`, `~/.cursor/skills`). Jadi pasang skill alat di folder yang sama.

## Input
| Info | Wajib? | Default |
|---|---|---|
| Periode | Tidak | Harian = hari ini (WIB). Mingguan = minggu lalu Senin–Minggu |
| Tanggal | Tidak | `hari-ini`; bisa `kemarin`, `2026-09-24`, `24/09/2026` |
| Zona waktu | Tidak | `Asia/Jakarta` (WIB). WITA `Asia/Makassar`, WIT `Asia/Jayapura` |
| Lokasi data lain | Tidak | Lokasi default alat. Pakai `--kasir-db`, `--stok-db`, `--absensi-db`, `--pengingat`, `--crm-db` bila beda |
| Samarkan nama karyawan | Tidak | Tidak. `--samarkan` = inisial (disarankan bila laporan dibaca orang lain) |

Tidak perlu bertanya apa pun untuk laporan pertama: langsung jalankan. Bertanya hanya saat membuat jadwal (lihat Langkah C).

## Langkah kerja

### A. Laporan sekarang
Jalankan (Windows: `python` atau `py` sebagai ganti `python3`):
```bash
python3 <folder-skill-ini>/scripts/laporan.py                       # harian, hari ini
python3 <folder-skill-ini>/scripts/laporan.py --tanggal kemarin
python3 <folder-skill-ini>/scripts/laporan.py --periode mingguan    # minggu lalu vs minggu sebelumnya
python3 <folder-skill-ini>/scripts/laporan.py --json                # untuk dibaca agent (berisi juga "teks")
```
1. Kirim `teks` **apa adanya**. Boleh menambah 1–3 kalimat saran di bawahnya ("Besok: restock RB, tanya Joko kenapa tidak absen"), tetapi **jangan mengubah angka, persen, tanggal**, dan jangan menambah angka yang tidak ada di laporan.
2. Bagian bertuliskan "Belum ada data" → jelaskan singkat: alat itu belum dipakai, atau lokasinya beda (tanya lokasinya, lalu pakai opsi `--...-db`). Jangan mengisi dengan perkiraan.
3. Pengguna bertanya "siapa yang harus ditagih?" → laporan sengaja tanpa nama pelanggan; jalankan skill `pengingat-follow-up` ("rekap pengingat").
4. Kode keluar 2 = argumen salah (mis. tanggal belum terjadi): sampaikan pesan error-nya dengan bahasa sederhana.

### B. Pertanyaan lanjutan
- "Kenapa omzet turun?" → lihat per metode bayar, terlaris, dan void/retur di laporan; detail per jam ada di `kasir-lokal` (`rekap --tanggal ...`).
- "Detail stok menipis?" → `buku-stok` `laporan menipis`. "Rekap lembur bulan ini?" → `absensi-lokal` `rekap`.

### C. Jadwal otomatis ke Telegram (OpenClaw)
Ikuti `references/openclaw-jadwal.md` (perintah sudah diuji dengan CLI OpenClaw asli). Sebelum membuat jadwal, tanyakan **sekali**:
1. Jam laporan harian (default 21.00 WIB, setelah tutup toko; toko tutup lewat tengah malam → jam 07.00 dengan `--tanggal kemarin`).
2. Laporan mingguan Senin pagi juga? (default ya, 07.00 WIB)
3. ID chat Telegram pemilik (cara mencarinya ada di referensi).
4. Nama karyawan disamarkan? (default tidak)

Lalu tunjukkan perintahnya + "Lanjut? (ya/tidak)". Kanal default **Telegram (bot resmi)**. WhatsApp hanya dengan **nomor terpisah** milik pemilik + persetujuan risiko tertulis. **Tanpa broadcast**, tanpa grup, tanpa pelanggan.

Penerima boleh lebih dari satu: **pemilik bersama atau pengelola yang pemilik tunjuk secara eksplisit** (mis. "kirim juga ke chat Bu Rina, dia rekan usaha saya") boleh menerima, masing-masing di **chat pribadinya sendiri** (bukan grup). Tanpa penunjukan eksplisit dari pemilik, jangan menambah penerima sendiri.

## Format output
Teks script (contoh nyata dari data uji, dipotong):
```
LAPORAN HARIAN USAHA
Kamis, 24 September 2026
Dibuat 2026-09-24 21:00 WIB

PENJUALAN
Omzet bersih: Rp 69.000
Nota: 2 (+1 dibatalkan) | rata-rata Rp 34.500
vs kemarin (Rab 23/9): Rp 36.000 -> naik 91,7%
vs Kamis lalu (17/9): Rp 12.000 -> naik 475,0%
Per metode bayar:
- Tunai Rp 51.000
- QRIS Rp 18.000
Terlaris:
1. Kopi Susu Gula Aren: 2 terjual, Rp 36.000

STOK
Minus 1 | habis 1 | menipis 1
- RB Roti Bakar - Coklat: stok -5 (min 5) MINUS
Perlu restock (sampai batas minimum): RB 10, ETM 5, KH 6

KEHADIRAN
Hadir 2 dari 5 terjadwal
Terlambat (1): Andi 08.12 (12 mnt)
Alpa: 1 (Rina)
Lembur perlu keputusan (belum disetujui):
- Sari 24/09: pulang 19.30, 2 jam 30 menit setelah jadwal, tanpa lembur disetujui

TAGIHAN & FOLLOW-UP
Terlambat 1 | hari ini 0 | besok 0
- #2 piutang Rp 12.500.000, lewat 3 hari

PROSPEK
Prospek baru: 1
Follow-up terlambat 1 | hari ini 2 | besok 0 | order perlu konfirmasi 0
Nilai potensi (terlambat + hari ini): Rp 4.500.000
Deal periode ini: 1 senilai Rp 6.000.000 (termasuk dari prospek lama)
Konversi prospek baru periode ini: 0,0% (0 dari 1 prospek baru sudah deal)
Sumber lead terbaik: belum ada deal dari lead periode ini.
Nama & nomor prospek: ketik "follow-up hari ini" atau "rekap CRM".

PERLU PERHATIAN
1. Selisih kas saat tutup kasir 2026-09-24 20:00: KURANG Rp 11.000 (...)
2. 3 dari 5 nota kasir tanggal 2026-09-24 belum diimpor ke buku-stok (stok belum terpotong).
3. 1 follow-up prospek CRM terlambat. Ketik 'follow-up hari ini' untuk daftar & draf pesannya.
```
JSON (`--json`): `periode`, `alat` (status `ada`/`tidak_ada`/`gagal`/`dilewati` + pesan), `penjualan`, `stok`, `kehadiran`, `tagihan`, `prospek`, `perhatian`, `rumus`, `teks`.

## Aturan hitung (eksplisit)
- **Omzet bersih** = `penjualan_bersih` dari kasir-lokal (setelah diskon, retur & void). Uang diterima ditampilkan terpisah bila berbeda (pajak/service).
- **Prospek (crm-wa)**: "Deal periode ini" menghitung semua deal yang *terjadi* di periode (bisa dari prospek lama); "Konversi prospek baru" = prospek yang *masuk* di periode dan sudah deal ÷ prospek masuk periode itu. Keduanya bisa terlihat berbeda (mis. deal 1 tapi konversi 0%) — itu wajar; jelaskan bila pemilik bertanya.
- **Rata-rata per nota** = omzet bersih ÷ (nota jual − nota void), dibulatkan ke rupiah terdekat (0,5 ke atas). Tanpa nota sah → "-".
- **Perubahan %** = (nilai sekarang − pembanding) ÷ pembanding × 100, dibulatkan **1 desimal**, 0,05 ke atas (menjauhi nol). Pembanding Rp 0 → "naik dari Rp 0 (persen tidak dihitung)"; keduanya 0 → "sama-sama Rp 0"; pembanding minus → tidak dihitung. Contoh: 69.000 vs 36.000 → 33.000 ÷ 36.000 × 100 = 91,666… → **91,7%**.
- **Pembanding harian**: kemarin & hari yang sama minggu lalu. **Mingguan**: Senin–Minggu sebelumnya; minggu berjalan dipotong s.d. hari ini dan dibanding hari yang sama minggu sebelumnya.
- **Perlu restock** = stok minimum − stok (dari buku-stok). Status minus/habis/menipis dari buku-stok, posisi saat laporan dibuat.
- Tanpa kasir-lokal tetapi ada buku-stok → penjualan = `omzet_tercatat` buku-stok (dijumlah per hari).
- **PROSPEK**: semua angka (prospek baru, follow-up terlambat/hari ini/besok, deal & nilainya, konversi, sumber terbaik) diambil **apa adanya** dari `crm.py rekap --json` (kontrak `skema_json` 1) — laporan-harian-usaha tidak menghitung ulang dengan rumus lain. `--dari`/`--sampai` mengikuti periode laporan (jadi "prospek baru" & "deal" adalah untuk hari/minggu itu); status follow-up (terlambat/hari ini/besok) selalu dihitung terhadap **hari ini** (bukan periode yang dilaporkan), sama seperti TAGIHAN & FOLLOW-UP. Perbandingan mingguan hanya untuk jumlah lead masuk (vs minggu sebelumnya, memakai jendela yang sama seperti pembanding PENJUALAN mingguan).
- Tanggal "hari ini" dihitung di zona `--tz` (default WIB), bukan jam server. Jam 00.30 WIB = sudah tanggal baru.

## Privasi
- **Tidak ada nama/nomor pelanggan**: tagihan ditampilkan sebagai nomor item (`#2 piutang Rp ...`). Perihal, catatan pribadi, dan nama penyetuju lembur tidak ditampilkan.
- **Tidak ada nama/nomor prospek**: bagian PROSPEK hanya jumlah, nilai rupiah, dan nama sumber lead (Instagram, TikTok, dll.) — kontrak `rekap --json` crm-wa (`skema_json` 1) memang tidak memuat nama kontak atau nomor WA. Nama & draf pesan follow-up tetap lewat `crm-wa` sendiri ("follow-up hari ini", "rekap CRM").
- Nama karyawan = nama panggilan yang sudah ada di absensi; `--samarkan` mengubahnya jadi inisial.
- Laporan hanya dikirim ke pemilik, atau pemilik bersama/pengelola yang **pemilik tunjuk secara eksplisit** (chat pribadi masing-masing). Tanpa grup, tanpa pelanggan, tanpa broadcast. Tidak ada data yang dikirim ke internet oleh script (pengiriman Telegram dilakukan OpenClaw milik pengguna).

## Checklist sebelum mengirim
- [ ] Teks laporan dari script, angka/persen/tanggal tidak diubah
- [ ] Bagian "Belum ada data" tidak diisi perkiraan
- [ ] Tidak ada nama pelanggan/nomor HP/nama & nomor prospek ditambahkan
- [ ] Butir "PERLU PERHATIAN" disampaikan semua
- [ ] Jadwal hanya dibuat setelah pemilik menjawab "ya", tujuan = chat pemilik sendiri (atau chat pribadi penerima yang pemilik tunjuk eksplisit)

## Batasan & penanganan error
- Hanya membaca alat Komunitech di komputer yang sama. Bukan dashboard web, bukan multi-cabang, tidak menarik data marketplace/bank.
- "sedang dipakai program lain" → saat itu ada transaksi yang sedang disimpan; data aman, jalankan lagi sebentar kemudian. Alat lain tetap dilaporkan.
- "script ... tidak ditemukan" → skill alatnya belum terpasang di folder skills yang sama; pasang, atau beri `--kasir-script PATH`/`--crm-script PATH` dst.
- "Jam komputer ini bukan Asia/Jakarta" → hanya **absensi-lokal** yang mencatat jam tap menurut jam komputer; sarankan menyamakan zona waktu komputer. kasir-lokal TIDAK terpengaruh jam komputer: ia mencatat nota menurut zona toko yang diatur di pengaturannya sendiri (`kasir.py info`). Bila zona toko itu beda dengan `--tz` laporan, muncul pesan terpisah "Toko diatur zona X tapi laporan memakai --tz Y"; samakan `--tz` dengan zona toko, bukan zona komputer.
- `--tz` hanya menerima zona Indonesia: Asia/Jakarta (WIB), Asia/Makassar (WITA), Asia/Jayapura (WIT) (dan alias WIB/WITA/WIT/Asia/Pontianak). Zona lain ditolak (kode keluar 2).
- File rusak/bukan database → bagian itu "Belum ada data" + pesan di PERLU PERHATIAN; sarankan pulihkan dari folder backup alatnya (jangan dihapus). Pesan error selalu menyebut path **file asli**, bukan salinan sementara yang dipakai script.
- **Python tidak bisa dijalankan:** jalankan perintah laporan tiap alat satu per satu lewat skill masing-masing, gabungkan hasilnya secara manual dengan rumus di atas, dan beri label "disusun manual, mohon dicek".
- Uji regresi: `python3 <folder-skill-ini>/tests/uji_regresi.py` (membutuhkan skill alat di folder yang sama).
