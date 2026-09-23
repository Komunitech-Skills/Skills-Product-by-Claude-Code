---
name: pengingat-follow-up
description: Daftar pantauan follow-up lokal (piutang, prospek, timesheet klien, janji) yang diisi lewat kalimat biasa ("ingatkan saya tagih Bu Rina tgl 3, 4,5 jt"), lalu rekap harian berisi yang jatuh tempo hari ini, terlambat (berapa hari), dan H-1, lengkap dengan DRAF pesan siap kirim yang dikirim sendiri oleh pemilik. Termasuk rekap jam & nilai timesheet per klien, dan jadwal otomatis jam 08.00 WIB ke Telegram lewat OpenClaw. Gunakan saat pengguna bilang ingatkan saya, jangan sampai lupa follow-up/nagih, pengingat jatuh tempo, daftar tagihan yang harus di-follow-up, rekap jam kerja klien, reminder, follow-up tracker, due date reminder, timesheet summary. Bukan untuk menyusun urutan pesan lengkap satu prospek (follow-up-prospek), surat teguran/denda (tagih-piutang), membuat invoice (buat-invoice), atau laporan penjualan terjadwal (laporan-otomatis-terjadwal).
---

# Pengingat Follow-up

## Tujuan
Pemilik usaha tidak lagi lupa menagih, menindaklanjuti calon pembeli, atau mengirim rekap jam
kerja ke klien. Semua janji follow-up dicatat di **satu daftar lokal**, lalu setiap pagi pemilik
menerima rekap berisi apa yang harus dikerjakan hari itu, **plus draf pesan siap kirim**.
**Pemilik sendiri yang mengirim** pesan ke pelanggan. Bot tidak pernah mengirim tagihan langsung ke pelanggan.

## Kapan digunakan
- "Ingatkan saya follow-up Bu Rina tgl 3 kalau belum bayar 4,5 jt."
- "Catat: Pak Budi minta dihubungi lagi Senin soal penawaran katering."
- "Hari ini saya harus nagih siapa saja?" / "Rekap pengingat hari ini."
- "Bu Rina sudah bayar." / "Tunda Pak Budi ke Kamis." / "Hapus yang Toko Sinar."
- "Catat 2 jam untuk PT Kreatif, revisi logo." / "Rekap jam kerja PT Kreatif minggu ini."
- "Aktifkan pengingat follow-up tiap pagi jam 8 ke Telegram."

## Kapan TIDAK digunakan
- Butuh urutan pesan lengkap H+1/3/7/14 untuk satu prospek → `follow-up-prospek`.
- Butuh surat teguran/somasi, hitung denda, atau umur piutang dari CSV akuntansi → `tagih-piutang`.
- Membuat invoice dari rekap timesheet → `buat-invoice` (pakai angka dari subperintah `timesheet`).
- Laporan penjualan/kas/stok terjadwal → `laporan-otomatis-terjadwal`.
- Kirim pesan otomatis/massal ke pelanggan, atau bot yang menagih sendiri lewat WhatsApp → **tolak**.
  Jelaskan: risiko nomor diblokir (WhatsApp Web tidak resmi) dan risiko salah tagih. Skill ini hanya
  menyiapkan draf untuk pemilik. Promo massal → `broadcast-wa` (dikirim manual).
- Jika skill rujukan di atas tidak terpasang: tetap bantu memakai template bawaan skill ini
  (`references/template-pesan.md`) dan sebutkan bahwa versi lengkapnya ada di skill tersebut.

## Data & privasi (wajib)
- File di folder kerja pengguna: `pengingat/DAFTAR.csv` dan `pengingat/timesheet.csv` (contoh:
  `templates/`). Folder kerja = workspace OpenClaw, atau folder proyek di Claude Code/Codex/Cursor.
- Kolom `DAFTAR.csv`: `id,jenis,nama,tanggal,nominal,perihal,status,catatan,dibuat`.
  - `jenis`: `piutang` | `prospek` | `timesheet` | `janji` | `lainnya`
  - `nama`: **nama panggilan atau kode saja** ("Bu Rina", "PLG-07"). Jangan menyimpan nomor HP, email, alamat, atau NIK.
    Script menolak kolom yang berisi pola nomor HP, email, atau 16 digit (kode keluar 2).
  - `perihal`: masuk ke draf untuk pelanggan (mis. "INV-012", "penawaran katering").
  - `catatan`: **pribadi pemilik**. Tampil di rekap untuk pemilik, **tidak pernah** masuk ke draf.
  - `status`: `aktif` | `selesai`. "Hapus" = baris dibuang permanen.
- Sarankan `bersihkan --lebih-dari 30` sebulan sekali agar data pihak ketiga tidak menumpuk (UU PDP: data minimal).

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Siapa (nama panggilan/kode) | Ya | — (tanyakan) |
| Kapan (tanggal jatuh tempo / tanggal follow-up) | Ya | Hari ini, dan sebutkan asumsinya |
| Jenis | Tidak | Ditebak dari kalimat: "bayar/tagih/invoice/nota" → piutang; "penawaran/tawarin/calon/prospek" → prospek; "jam kerja/timesheet" → timesheet; "ketemu/meeting/janji" → janji; selain itu → lainnya |
| Nominal | Tidak (disarankan untuk piutang) | Kosong; draf tanpa angka |
| Perihal (no. invoice/produk) | Tidak | Kosong ("pembayaran tagihan") |
| Kanal & jam rekap otomatis | Tidak | Telegram, 08.00 WIB (Asia/Jakarta) |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Kalimat seperti contoh
pertama di atas sudah cukup, jadi langsung simpan.

## Langkah kerja
Semua perintah dijalankan dari folder kerja pengguna. Windows: ganti `python3` dengan `python` atau `py`.
`S` di bawah = `python3 <folder-skill-ini>/scripts/cek_jatuh_tempo.py`.

### 1. Tambah item dari kalimat biasa
```bash
S --teks tambah --jenis piutang --nama "Bu Rina" --tanggal "tgl 3" --nominal "4,5 jt" --perihal "INV-012"
```
- Tanggal diterima apa adanya: `3/10`, `03-10-2026`, `3 Okt`, `3 Oktober 2026`, `besok`, `lusa`,
  `Jumat`, `3 hari lagi`, `2026-10-03`. Urutan selalu hari/bulan. **Jangan mengonversi sendiri.**
  Serahkan teks asli ke script.
- Tahun tidak disebut → script memilih tanggal terdekat ke depan. Jika tanggal itu baru lewat ≤ 60 hari
  (mis. "20 Sep" diucapkan 1 Okt), script memakai tahun ini dan item masuk TERLAMBAT.
  **Sampaikan `Catatan:` dari script ke pengguna apa adanya.**
- Nominal: `4,5 jt`, `4.500.000`, `Rp4.500.000`, `750rb`, `1,2 M`, `4 jt 500 rb`.
- Balas singkat dengan teks hasil script, mis. "Tersimpan #3: piutang - Bu Rina, Sabtu, 3 Oktober 2026, Rp 4.500.000."
- "Kalau belum bayar" tidak perlu kolom khusus. Item tetap aktif sampai pemilik bilang sudah bayar.
- Daftar banyak sekaligus (tabel, CSV, foto daftar piutang): baca, tunjukkan ringkasannya, minta "ya",
  lalu jalankan `tambah` per baris. Jangan menulis CSV langsung, karena validasi ada di script.

### 2. Tandai selesai / tunda / ubah / hapus lewat chat
```bash
S --teks selesai --id 3            # "Bu Rina sudah bayar"
S --teks tunda --id 5 --ke "Senin" # "tunda Pak Budi ke Senin"
S --teks ubah --id 3 --nominal "3 jt" --perihal "sisa INV-012"
S --teks hapus --id 7              # permanen: konfirmasi "ya" dulu
S --teks daftar [--semua]          # cari nomor item dari nama
```
Pengguna menyebut nama, bukan nomor → jalankan `daftar` dulu. Jika ada lebih dari satu yang cocok, tanyakan yang mana.
Pembayaran sebagian → `ubah --nominal <sisa>` dan tambahkan catatan.

### 3. Rekap harian (manual atau terjadwal)
```bash
S --teks rekap            # teks siap kirim ke pemilik
S rekap                   # JSON (terlambat, jatuh_tempo_hari_ini, besok_h_1, ringkasan, baris_ditolak)
S --teks draf --id 3      # draf untuk satu item
```
Rekap berisi: **TERLAMBAT** (lewat N hari, paling lama di atas), **HARI INI**, **BESOK / H-1**,
total piutang tertunggak (bilangan bulat), jumlah item 7 hari ke depan, lalu **DRAF PESAN** per item
(maks. 10, sisanya lewat `draf --id`).
- Tampilkan teks rekap **apa adanya**. Boleh memperhalus draf jika pemilik minta, tapi nominal,
  tanggal, dan jumlah hari **tidak boleh diubah**.
- Nada draf piutang mengikuti tahap `tagih-piutang`: H-1 dan hari H ramah; lewat 1–6 hari "mungkin
  terlewat"; 7–29 hari minta tanggal pasti; ≥ 30 hari pemberitahuan tertulis. Jika pemilik sudah
  ≥ 2 kali mengingatkan tanpa hasil, atau minta denda/somasi → pakai `tagih-piutang`.
- Prospek: draf singkat yang tidak memaksa. Untuk urutan lengkap → `follow-up-prospek`.
- Timesheet: draf memakai placeholder `[TOTAL JAM]`/`[NILAI]`. Isi dengan Langkah 4 sebelum ditampilkan.
- Janji: draf konfirmasi jadwal. Lainnya: pengingat untuk pemilik saja (tanpa draf).
- `baris_ditolak` tidak kosong → **wajib** sebutkan nomor baris & alasannya. Jangan diam-diam dilewati.

### 4. Timesheet klien
```bash
S --teks catat-jam --klien "PT Kreatif" --jam "1:30" --tanggal "hari ini" --tarif "150rb" --keterangan "revisi logo"
S --teks timesheet --periode minggu-ini [--klien "PT Kreatif"] [--tarif "150rb"]
S --teks timesheet --dari "1/9/2026" --sampai "30/9/2026"
```
- Jam: `1:30`, `1,5`, `90m`, `2 jam`, `1j30m`. Periode: `minggu-ini` (Senin–Minggu), `minggu-lalu`,
  `bulan-ini` (default), `bulan-lalu`, atau `--dari/--sampai`.
- Rumus: nilai per klien = Σ(menit × tarif ÷ 60), dihitung persis lalu **dibulatkan sekali** ke rupiah
  terdekat (0,5 ke atas) per klien. Total = jumlah nilai per klien.
- Dengan `--klien`, script juga mengeluarkan **draf pesan ke klien** + rincian per tanggal.
  Pemilik yang menyetujui dan mengirim. Ingin invoice? Lanjutkan ke `buat-invoice`.

### 5. Jadwal otomatis (OpenClaw)
Ikuti `references/openclaw-jadwal.md`: rekap tiap hari 08.00 WIB (`--tz Asia/Jakarta`,
`--session isolated`) ke **Telegram pemilik** (default), pengingat sekali jalan (`--at`), dan rekap timesheet
Jumat sore. Selalu tunjukkan ringkasan dan minta "Lanjut? (ya/tidak)" sebelum membuat jadwal.
Untuk WhatsApp berlaku syarat berikut: **nomor terpisah** milik pemilik, laporan hanya ke pemilik sendiri,
dan ada persetujuan risiko tertulis. **Tidak ada broadcast** dan tidak ada pengiriman ke grup atau pelanggan.
Di Claude Code/Codex/Cursor (tanpa Gateway): skill tetap jalan sebagai daftar pantauan manual.
Pengguna cukup mengetik "rekap pengingat" setiap pagi, atau memasang pengingat kalender HP sendiri.

## Format output
- Tambah/ubah/selesai/tunda/hapus: satu-dua baris konfirmasi dari script (+ `Catatan:` bila ada).
- Rekap harian: teks `rekap --teks` (contoh di `references/template-pesan.md`), diakhiri
  "Balas misalnya: selesai 3, tunda 3 ke Senin, hapus 3".
- Semua rupiah berformat `Rp 4.500.000`. Tanggal ditulis `Sabtu, 3 Oktober 2026` atau `3 Okt 2026`.

## Contoh
**Input:** "Ingatkan saya follow-up Bu Rina tgl 3 kalau belum bayar 4,5 jt, invoice INV-012." (hari ini 1 Okt 2026)
**Proses:** `tambah --jenis piutang --nama "Bu Rina" --tanggal "tgl 3" --nominal "4,5 jt" --perihal "INV-012"`
**Output:**
```
Tersimpan #1: piutang - Bu Rina, Sabtu, 3 Oktober 2026, Rp 4.500.000 (INV-012).
Catatan: Bulan tidak disebut; dipakai 3 Okt 2026 (tanggal 3 terdekat ke depan). Ubah bila maksudnya lain.
Saya akan menampilkannya di rekap tanggal 2 Okt (H-1) dan 3 Okt. Draf pesan siap kirim akan disertakan.
```
Rekap pagi 3 Okt (potongan):
```
HARI INI (1)
1. #1 Piutang - Bu Rina | Rp 4.500.000 | INV-012 | jatuh tempo hari ini
Total piutang tertunggak (terlambat + hari ini): Rp 4.500.000

#1 untuk Bu Rina:
Selamat pagi Bu Rina, kami mengingatkan pembayaran INV-012 sebesar Rp 4.500.000 jatuh tempo hari ini, 3 Okt 2026. ...
```

## Checklist sebelum membalas
- [ ] Tanggal, nominal, hari terlambat, total, dan nilai timesheet **berasal dari script**, bukan dikira.
- [ ] `Catatan:` script (tahun/bulan ditebak, pembulatan) disampaikan ke pengguna.
- [ ] Tidak ada nomor HP/email/alamat/NIK yang disimpan di daftar.
- [ ] Draf tidak memuat kolom `catatan` pribadi, ancaman, kata "polisi/pidana/viral", atau urgensi palsu.
- [ ] Draf ditandai untuk **dikirim sendiri oleh pemilik**. Bot tidak mengirim ke pelanggan.
- [ ] Baris CSV yang ditolak disebutkan ke pengguna.
- [ ] Jadwal otomatis hanya dibuat setelah pemilik menjawab "ya", dan tujuannya pemilik sendiri.

## Batasan & penanganan error
- Script keluar dengan `ERROR: ...` (kode 1): sampaikan pesannya dengan bahasa sederhana dan minta data yang benar.
  Jangan menebak. Kode 2 = kolom berisi data kontak. Minta nama panggilan saja.
- Baris CSV rusak (tanggal 31/2, nominal "abc", kolom berlebih) **tidak** menghentikan rekap.
  Baris itu dilaporkan di `baris_ditolak` dan tidak dihapus dari file.
- File Excel (`;` sebagai pemisah, BOM) bisa dibaca. Saat disimpan ulang, pemisahnya menjadi koma.
- Script tidak mengetahui apakah pelanggan sudah membayar. Status diubah hanya jika pemilik mengatakannya.
- Script tidak tahu berapa kali pemilik sudah menagih, jadi nada draf dibatasi sampai "pemberitahuan tertulis".
  Somasi dan denda → `tagih-piutang` (bukan nasihat hukum).
- Zona waktu default Asia/Jakarta. Untuk WITA/WIT pakai `--tz Asia/Makassar` / `Asia/Jayapura`.
  Uji dengan `--hari-ini 2026-10-01`.
- **Python tidak bisa dijalankan:** kerjakan manual lalu beri tahu pengguna "dihitung manual, mohon dicek":
  - Hari terlambat = hari ini − tanggal (hari kalender).
  - Total tertunggak = jumlah nominal piutang aktif yang tanggalnya ≤ hari ini.
  - Nilai timesheet = total menit × tarif ÷ 60, dibulatkan ke rupiah terdekat.
  - Ubah CSV dengan hati-hati: satu baris per item, tanggal ISO `YYYY-MM-DD`, nominal angka bulat tanpa titik.
- Jadwal hanya berjalan saat komputer/Gateway OpenClaw menyala (lihat `references/openclaw-jadwal.md`).
