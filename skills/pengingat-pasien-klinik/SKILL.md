---
name: pengingat-pasien-klinik
description: Buku jadwal lokal pengingat kontrol/vaksin pasien untuk klinik, praktik dokter/bidan/dokter gigi, dan klinik hewan (CSV lokal, tanpa rekam medis/diagnosis) — catat nama panggilan, nomor WA, jenis kunjungan umum, dan tanggal berikutnya; lihat daftar H-3/H-1/hari-ini/terlambat lengkap DRAF pesan WA sopan siap disalin staf (bukan kirim otomatis); ringkasan harian ke pemilik/PIC tanpa nomor WA (nama boleh inisial); catatan persetujuan pasien (UU PDP) + perintah hapus data. Gunakan saat diminta buat pengingat kontrol/vaksin pasien, jadwal kunjungan ulang, siapa yang harus diingatkan hari ini/besok, patient recall/appointment reminder, vaccine reminder klinik hewan. JANGAN untuk diagnosis, rekam medis, atau kirim pesan otomatis/broadcast ke pasien.
---

# Pengingat Pasien Klinik (Kontrol & Vaksin)

## Tujuan
Klinik, praktik dokter/bidan/dokter gigi, dan klinik hewan sering lupa mengingatkan pasien soal
jadwal kontrol atau vaksin berikutnya. Skill ini menjadi **buku jadwal lokal minimal** — hanya
nama panggilan, nomor WA, jenis kunjungan umum, dan tanggal — lalu setiap hari menyiapkan daftar
siapa yang harus diingatkan (H-3, H-1, hari ini, terlambat) beserta **draf pesan WA sopan siap
disalin**. **Staf yang menyalin dan mengirim sendiri.** Tidak ada pengiriman otomatis, tidak ada
broadcast, dan **tidak ada diagnosis atau rekam medis** yang disimpan.

## Kapan digunakan
- "Catat: Bu Sari, WA 0812-0000-1111, kontrol gigi tanggal 10 Oktober, setuju dihubungi."
- "Ada pasien vaksin hewan (kucing Mimi) minggu depan, nomor pemiliknya 0812..., boleh diingatkan."
- "Siapa yang harus diingatkan hari ini?" / "Daftar H-1 besok." / "Ada yang terlewat gak?"
- "Bu Sari sudah datang, jadwalkan lagi 1 bulan lagi." / "Sudah saya ingatkan Bu Sari."
- "Pak Budi batal, pindah dokter." / "Ubah nomor WA Bu Sari."
- "Bu Sari minta datanya dihapus." / "Hapus semua data nomor 0812..."
- "Impor daftar pasien kontrol dari CSV ini."
- "Kirim ringkasan pengingat pasien tiap pagi ke Telegram saya." (OpenClaw)

## Kapan TIDAK digunakan
- **Diagnosis, rekam medis, hasil lab, atau instruksi medis** apa pun → **tolak**, arahkan ke
  tenaga kesehatan. Skill ini hanya mencatat *jenis kunjungan umum* (kontrol, vaksin, cabut
  jahitan, cek gigi, vaksin hewan, groom, sunat, medical check up, dll), **bukan** nama penyakit.
- Leaflet edukasi pasien, FAQ klinik, balasan chat umum, atau rekap kunjungan agregat →
  `edukasi-pasien-klinik`.
- **Kirim pesan otomatis/broadcast ke pasien** → **tolak**. Keputusan pemilik: OpenClaw memakai
  WhatsApp Web (tidak resmi); pesan otomatis ke pasien berisiko nomor diblokir **dan** melanggar
  prinsip "manusia yang mengirim" untuk data kesehatan. Skill ini hanya menyiapkan draf.
- CRM prospek/penjualan → `crm-wa`. Piutang/follow-up umum non-klinik → `pengingat-follow-up`.
- Jika skill rujukan di atas tidak terpasang, tetap bantu memakai kemampuan bawaan skill ini saja.

## Data & privasi (wajib — UU PDP 27/2022)
- File CSV di folder kerja pengguna: `pasien/DAFTAR.csv` (workspace OpenClaw, atau folder proyek
  di Claude Code/Codex/Cursor). Kolom: `id, nama_panggilan, wa, jenis, tanggal, status,
  persetujuan, dibuat, diingatkan_pada, catatan`.
- **Hanya data minimal**: nama panggilan (bukan nama lengkap/KTP), nomor WA, jenis kunjungan
  umum, tanggal. **Tidak pernah** diagnosis, riwayat penyakit, hasil pemeriksaan, NIK, atau
  rekam medis. Script menolak isian yang menyerupai nama penyakit (kode keluar 1) atau berisi
  nomor HP/email/NIK pihak lain di kolom nama/catatan (kode keluar 2).
- **Persetujuan wajib** (`--persetujuan ya|tidak`) saat pasien pertama kali dicatat: apakah
  pasien setuju dihubungi lewat WA untuk pengingat. Persetujuan `tidak` **tidak pernah** muncul
  di `daftar`, `draf`, atau `ringkasan` — datanya tersimpan hanya sebagai catatan agar staf tidak
  bertanya ulang, sampai pasien mengubah pikiran (`ubah --persetujuan ya`).
- **Hak hapus**: `hapus --id <id>` atau `hapus --wa <nomor>` (pratinjau → `--ya`) menghapus
  permanen. Jalankan segera bila pasien meminta datanya dihapus.
- Ringkasan untuk pemilik (`ringkasan`) **tidak pernah** memuat nomor WA; pakai `--samarkan`
  agar nama tampil inisial (mis. "Bu S.") untuk laporan yang dikirim lewat jadwal OpenClaw.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama panggilan pasien (atau nama hewan + pemilik) | Ya | — (tanyakan) |
| Nomor WA (pasien atau pemilik hewan) | Ya | — (tanyakan) |
| Jenis kunjungan berikutnya | Ya | — (tanyakan; **harus umum**, bukan diagnosis) |
| Tanggal kunjungan berikutnya | Ya | — (tanyakan) |
| Persetujuan dihubungi (ya/tidak) | Ya | — (tanyakan secara eksplisit, jangan diasumsikan "ya") |
| Nama klinik (untuk draf pesan) | Tidak | Draf memakai "kami" |
| Catatan tambahan non-medis | Tidak | Kosong |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan bernomor (maks. 5 pertanyaan),
termasuk pertanyaan persetujuan. Jangan pernah mengasumsikan persetujuan "ya" tanpa pasien
menyatakannya.

## Cara menjalankan script
Path relatif terhadap folder berisi SKILL.md ini (Windows: ganti `python3` dengan `python`/`py`):
```bash
python3 <folder-skill-ini>/scripts/pengingat_pasien.py <perintah> [opsi] --json
```
Database default `pasien/DAFTAR.csv` di folder kerja; ganti dengan `--file PATH` bila perlu
(pakai lokasi yang sama di semua perintah). Semua perintah, contoh, dan opsi lengkap ada di
`references/perintah.md`.

## Langkah kerja

### A. Catat pasien baru
`tambah --nama "Bu Sari" --wa "0812-0000-1111" --jenis kontrol --tanggal "10 Okt" --persetujuan ya [--catatan "..."]`
- **Tanyakan persetujuan secara eksplisit** ("Bu Sari setuju diingatkan lewat WA untuk jadwal
  kontrolnya?") sebelum mengisi `--persetujuan`. Jangan menebak "ya".
- `jenis` hanya kategori umum (kontrol, vaksin, cabut jahitan, cek gigi, vaksin hewan, groom,
  sunat, medical check up, dll). Kalau pengguna menyebut nama penyakit/diagnosis, script menolak
  (kode keluar 1) — minta pengguna menyebut jenis kunjungan saja, bukan diagnosisnya.
- Nomor WA diterima format apa pun (0812…, +62812…, 62812…) dan disimpan sebagai `62…`.
- Klinik hewan: nama pasien = nama hewan (mis. "Kucing Mimi"), nomor WA = nomor pemilik.

### B. Daftar harian & draf pesan (inti)
`daftar [--kapan terlambat|hari-ini|besok|h-3|minggu-ini|semua] [--tanpa-draf] [--klinik "Nama Klinik"]`
- Tanpa `--kapan`: tampilkan **TERLAMBAT, HARI INI, BESOK (H-1), H-3** apa adanya, lalu **DRAF
  PESAN** per pasien (maks. 15) dengan format "Halo [nama], ini pengingat dari [klinik] untuk
  jadwal [jenis] Anda pada [tanggal]. Mohon konfirmasi kehadiran Anda...".
- Tampilkan teks **apa adanya**. Boleh memperhalus bahasa draf atas permintaan staf, tapi
  **tanggal, nama, dan jenis kunjungan tidak boleh diubah**, dan **jangan pernah menambahkan
  saran medis atau menyebut nama penyakit** ke dalam draf.
- Sampaikan ke pengguna: **"Ini draf untuk disalin dan dikirim sendiri, bukan kiriman otomatis."**
- Draf 1 pasien saja: `draf --id 3 [--klinik "Nama Klinik"]` (ditolak bila persetujuan pasien itu
  "tidak" — sampaikan alasannya).

### C. Setelah diingatkan / pasien datang / batal
```bash
ubah-status --id 3 --status sudah-diingatkan          # staf sudah kirim draf
ubah-status --id 3 --status datang --berikutnya "3 bulan lagi"   # datang + jadwalkan lagi
ubah-status --id 3 --status batal --alasan "pindah kota"
```
- `datang` + `--berikutnya` otomatis membuat jadwal berikutnya (status kembali `dijadwalkan`) —
  dipakai untuk vaksin bertahap/kontrol rutin. Tanpa `--berikutnya`, pasien berhenti muncul di
  daftar (kunjungan itu selesai).
- `batal` menghentikan pengingat untuk jadwal itu; `--alasan` boleh diisi (jangan berisi nama
  penyakit atau data pribadi pihak lain — script menolak bila ada).
- Ubah data yang salah ketik: `ubah --id 3 --wa "..." / --tanggal "..." / --jenis "..." / --catatan "..."`.

### D. Impor dari daftar lama
`impor daftar.csv [--jenis-default kontrol] [--tanggal-default "..."] [--persetujuan-default ya|tidak]`
→ pratinjau (jumlah diterima/ditolak per baris) → setuju → ulangi + `--ya`.
- Kolom dikenali otomatis: nama/nama_panggilan/pasien, wa/no wa/nomor/hp, jenis, tanggal, dan
  persetujuan/setuju/consent. **Jika file tidak punya kolom persetujuan, `--persetujuan-default`
  wajib diisi** — tanyakan ke pengguna dulu apakah semua pasien di file itu memang sudah pernah
  menyetujui dihubungi; jangan asumsikan "ya" begitu saja.
- Baris yang gagal (nomor rusak, jenis menyerupai diagnosis, dll.) dilaporkan di `ditolak`, tidak
  menghentikan impor baris lain.

### E. Hapus data (hak pasien / UU PDP)
`hapus --id 3` atau `hapus --wa 0812-0000-1111` → pratinjau (nama & jadwal yang akan hilang) →
setuju → ulangi + `--ya`. Jalankan **segera** saat pasien memintanya, jangan ditunda.

### F. Ringkasan harian untuk pemilik/PIC (OpenClaw → Telegram)
`ringkasan [--samarkan] [--tanpa-nama]` → jumlah TERLAMBAT/HARI INI/BESOK/H-3 + daftar nama
(inisial bila `--samarkan`) dan jenis kunjungan, **tanpa nomor WA sama sekali**. Untuk jadwal
otomatis ke Telegram, ikuti `references/openclaw-jadwal.md` — **selalu pakai `--samarkan`** pada
job terjadwal karena hasilnya tersimpan di riwayat chat Telegram pemilik. Tunjukkan ringkasan
perintah dan tanya "Lanjut? (ya/tidak)" sebelum membuat jadwal.

## Format output
- Simpan/ubah: satu baris konfirmasi dari script, mis. `Tersimpan #1: Bu Sari | Kontrol | Sabtu,
  10 Oktober 2026 | persetujuan: ya`, + `peringatan` bila ada (nomor tidak wajar, tahun ditebak, dll).
- `daftar`: teks berkelompok TERLAMBAT/HARI INI/BESOK/H-3 + DRAF PESAN, apa adanya dari script.
- `ringkasan`: ringkasan angka + daftar nama (inisial opsional), tanpa nomor WA.
- Tanggal ditulis `Sabtu, 10 Oktober 2026` atau `10 Okt 2026` (dari script, jangan dihitung sendiri).

## Contoh
**Input pengguna:** "Catat Bu Sari, kontrol gigi lagi 10 hari lagi, WA 0812-0000-1111. Dia bilang boleh diingatkan." (hari ini 26 Sep 2026)
**Proses:** `tambah --nama "Bu Sari" --wa "0812-0000-1111" --jenis "kontrol gigi" --tanggal "10 hari lagi" --persetujuan ya`
**Output:**
```
Tersimpan #1: Bu Sari | Kontrol gigi | Selasa, 6 Oktober 2026 | persetujuan: ya
```
H-3 (3 Okt), daftar menampilkan:
```
H-3 (1)
  #1 Bu Sari | Kontrol gigi | 6 Okt 2026 | 0812-0000-1111

DRAF PESAN (salin & kirim sendiri, JANGAN dikirim otomatis):

#1 Bu Sari (0812-0000-1111):
Halo Bu Sari, ini pengingat dari kami untuk jadwal kontrol gigi Anda pada 6 Okt 2026. Mohon
konfirmasi kehadiran Anda. Kalau perlu mengubah jadwal, silakan balas pesan ini. Terima kasih.
```
Contoh sesi lengkap: `examples/`.

## Checklist sebelum menjawab
- [ ] Tidak ada pesan yang dikirim ke pasien oleh agent; draf ditandai "salin & kirim sendiri".
- [ ] Persetujuan pasien ditanyakan secara eksplisit, bukan diasumsikan.
- [ ] `jenis` dan `catatan` tidak memuat diagnosis, nama penyakit, atau saran medis.
- [ ] Tidak ada nomor HP/email/NIK pihak lain yang masuk ke kolom nama/catatan.
- [ ] Ringkasan untuk pemilik tidak memuat nomor WA.
- [ ] Permintaan hapus data dijalankan segera setelah dikonfirmasi.
- [ ] Tanggal & pengelompokan (terlambat/H-1/H-3) berasal dari script, bukan dihitung manual.

## Batasan & penanganan error
- Bukan rekam medis elektronik dan bukan pengganti sistem antrean klinik. Tidak membaca chat WA
  atau riwayat pasien di sistem lain; semua data dimasukkan lewat perintah `tambah`/`impor`.
- Script keluar `ERROR: ...` (kode 1) untuk input salah/ambigu (tanggal, jenis menyerupai
  diagnosis) — sampaikan pesannya, minta perbaikan, jangan menebak.
- Kode keluar 2 = ditolak karena berisi data pribadi pihak lain (nomor HP/email/NIK) di kolom
  yang bukan untuk itu — arahkan ke kolom yang benar (`--wa` untuk nomor).
- Baris CSV rusak (kolom kelebihan, dll.) tidak menghentikan program; dilaporkan di
  `baris_ditolak` dan tetap tersimpan apa adanya di posisinya sampai diperbaiki manual.
- File Excel ANSI/Windows-1252 bisa dibaca; disimpan ulang sebagai UTF-8 saat ada perubahan.
  Teks berawalan `=`, `+`, `@`, `-` diamankan agar tidak dibaca sebagai rumus.
- Satu file dipakai satu komputer. Jangan buka file yang sama dari dua komputer sekaligus lewat
  Google Drive/Dropbox (bisa saling menimpa).
- Zona waktu default Asia/Jakarta (`--tz Asia/Makassar` untuk WITA, `Asia/Jayapura` untuk WIT).
- **Python tidak bisa dijalankan:** skill tetap bisa dipakai manual — simpan daftar di
  spreadsheet dengan kolom yang sama, urutkan berdasarkan tanggal, dan susun draf pesan sesuai
  format di atas manual. Beri tahu pengguna "dihitung/disusun manual, mohon dicek".
