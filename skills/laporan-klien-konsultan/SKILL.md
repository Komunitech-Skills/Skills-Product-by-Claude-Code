---
name: laporan-klien-konsultan
description: Mencatat pekerjaan harian untuk klien (proyek, jam, status, kendala) di file CSV lokal, lalu menyusun draf laporan progres mingguan/bulanan per klien (ringkasan, selesai, berjalan, butuh dari klien, rencana berikutnya, total jam dihitung script) dalam versi email, WA/Telegram, dan Markdown -- siap ditinjau dan dikirim MANUAL oleh konsultan/freelancer (pajak, hukum, IT, desain, marketing, dst.), tidak pernah otomatis ke klien. Gunakan saat pengguna minta "catat kerjaan klien", "laporan progres klien", "laporan mingguan/bulanan ke klien", client progress report, weekly client update, timesheet klien. Bukan untuk laporan ke atasan internal (laporan-status-kantor) atau menjadwalkan pengiriman (laporan-otomatis-terjadwal, dipakai SETELAH draf ini terbukti benar).
---

# Laporan Klien (Konsultan/Freelancer)

## Tujuan
Konsultan dan freelancer (pajak, hukum, IT, desain, marketing, dll.) yang harus rutin melapor ke
klien cukup **mencatat pekerjaan sekali jalan** saat selesai dikerjakan, lalu tinggal minta
"buatkan laporan mingguan untuk klien X" untuk dapat draf siap tinjau -- tanpa mengetik ulang dari
nol tiap minggu dan tanpa menghitung jam secara manual. Semua angka (total jam, jumlah pekerjaan)
dihitung `scripts/laporan_klien.py`, bukan diperkirakan.

**Versi 1.0.1** (revisi rendah): konversi "N menit" → desimal jam (mis. 90 menit → `--jam 1.5`)
sekarang dijelaskan eksplisit di bagian 1 karena `--jam` hanya menerima desimal; file log CSV
0-byte (bukan sekadar "belum ada catatan", tapi rusak/tanpa header sama sekali) sekarang ditolak
dengan pesan jelas alih-alih diam-diam dianggap "tidak ada catatan". Uji regresi 28/28.

## Kapan digunakan
- "Catat: hari ini saya kerjakan rekonsiliasi bank untuk PT Maju, 2,5 jam, selesai."
- "Buatkan laporan mingguan untuk klien PT Maju Jaya."
- "Rekap kerjaan bulan ini untuk semua klien saya" (jalankan berulang per klien -- lihat Langkah 3).
- Freelancer/konsultan yang selama ini mengetik ulang laporan progres dari memori atau chat WA
  setiap minggu/bulan.

## Kapan TIDAK digunakan
- **Laporan ke atasan/pemilik/tim internal** (bukan ke klien eksternal), newsletter kantor,
  pengumuman internal, memo, laporan insiden → `laporan-status-kantor`. Skill itu juga punya
  varian "3P ke klien" untuk laporan progres sekali-jadi tanpa histori log; skill **ini** dipakai
  saat pekerjaan untuk klien dicatat **rutin dari hari ke hari** dan laporan dirakit dari histori
  itu (jam dihitung otomatis, kendala/kebutuhan klien terkumpul sendiri) -- bukan ditulis ulang
  manual tiap kali.
- **Menjadwalkan pengiriman rutin** (draf otomatis muncul di Telegram tiap Jumat) → skill ini
  tidak membuat jadwal sendiri; setelah draf manual terbukti benar, ikuti
  `references/openclaw-jadwal.md` (memakai skill umum `laporan-otomatis-terjadwal` sebagai
  polanya). **Skill ini sendiri tidak pernah mengirim apa pun ke klien.**
- **Menghitung invoice/tagihan berdasarkan jam** → catat jam di sini boleh, tapi untuk membuat
  invoicenya sendiri pakai `buat-invoice`. Skill ini hanya melaporkan progres, bukan menagih.
- **CRM prospek/calon pembeli** (belum jadi klien, masih tahap penawaran) → `crm-wa`.
- **Follow-up piutang/tagihan klien yang menunggak** → `tagih-piutang`.
- Klien meminta laporan berisi data pribadi pihak ketiga yang tidak perlu (data karyawan klien,
  nomor rekening, dsb.) → catat seperlunya saja (lihat Batasan, UU PDP).

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama klien | Ya | Tanyakan; nama ini dipakai persis sebagai kunci pencarian laporan |
| Nama proyek/layanan | Ya | Tanyakan (mis. "Pembukuan bulanan", "Redesign website") |
| Pekerjaan yang dilakukan | Ya | Tanyakan, satu kalimat singkat per baris log |
| Tanggal | Tidak | Hari ini |
| Jam kerja | Tidak | Kosong (tidak dihitung sebagai 0 jam -- ditandai "tanpa jam" di laporan) |
| Status (selesai/berjalan/terkendala) | Tidak | `berjalan` |
| Kendala (hambatan di pihak konsultan) | Tidak | Kosong |
| Butuh dari klien (data/keputusan yang ditunggu) | Tidak | Kosong |
| Periode laporan (mingguan/bulanan/rentang kustom) | Ya untuk `laporan` | `mingguan` (minggu berjalan Senin-Minggu) |
| Rencana berikutnya | Tidak | Diturunkan otomatis dari pekerjaan berstatus "berjalan" |

Jika info wajib untuk mencatat kurang, tanyakan **sekali** dalam satu pesan singkat. Jika
pengguna langsung cerita ("kelarin desain logo buat Kopi Senja tadi, 3 jam"), ekstrak
klien/proyek/pekerjaan/jam dari kalimat itu -- proyek boleh ditebak dari konteks ("Desain
logo") bila tidak disebut eksplisit, sebutkan tebakan itu di akhir.

## Langkah kerja
Path script relatif terhadap folder SKILL.md ini. Windows: ganti `python3` dengan `python`/`py`.
File log CSV default: `log-kerja-klien.csv` di folder kerja pengguna (bisa diarahkan ke lokasi
lain dengan `--file`, mis. `laporan/log-kerja-klien.csv`) -- **satu file untuk semua klien**,
dipilah lewat kolom `klien`.

### 1. Catat pekerjaan (dilakukan tiap kali ada progres)
```bash
python3 <folder-skill-ini>/scripts/laporan_klien.py catat \
  --klien "PT Maju Jaya" --proyek "Pembukuan bulanan" \
  --pekerjaan "Rekonsiliasi bank September" --jam 2.5 --status selesai
```
- `--status` : `selesai` | `berjalan` (default) | `terkendala`. Alias umum dikenali (`done`,
  `progress`, `stuck`, dst.) -- lihat pesan error untuk daftar lengkap bila salah ketik.
- `--jam` boleh pakai koma (`2,5`) atau titik (`2.5`); kosongkan bila tidak dihitung per jam
  (mis. retainer bulanan tetap) -- **jangan menebak jam**, biarkan kosong.
- Script hanya menerima **angka desimal jam** (mis. `2.5`), bukan format "N menit" -- kalau
  pengguna menyebut waktu dalam menit (mis. "90 menit", "45 menit tadi"), **agent yang mengonversi**
  ke desimal jam sebelum memanggil `--jam`: menit ÷ 60, dibulatkan 2 desimal bila perlu (contoh:
  90 menit → `--jam 1.5`; 45 menit → `--jam 0.75`; 100 menit → `--jam 1.67`). Sebutkan hasil
  konversi ke pengguna sebelum menyimpan, supaya bisa dikoreksi bila salah dengar.
- `--kendala "..."` untuk hambatan di pihak konsultan (mis. menunggu tools/izin internal).
- `--butuh-klien "..."` untuk hal yang perlu klien berikan/putuskan (mis. dokumen, approval).
- **Sebelum mengetik pekerjaan/kendala/kebutuhan**, lihat Batasan di bawah soal data pribadi/
  rahasia klien yang tidak perlu dicatat.
- Script keluar kode **3** (bukan error, tetap tercatat) bila teks yang dimasukkan mengandung pola
  mirip data pribadi (NIK/KTP/nomor HP/email) atau kata "password"/"rahasia"/"kredensial" --
  tunjukkan peringatan itu ke pengguna dan tawarkan menuliskannya lebih ringkas.

### 2. Susun draf laporan progres satu klien
```bash
python3 <folder-skill-ini>/scripts/laporan_klien.py laporan \
  --klien "PT Maju Jaya" --periode mingguan --json
```
- `--periode`: `mingguan` (alias `minggu-ini`), `minggu-lalu`, `bulanan` (alias `bulan-ini`),
  `bulan-lalu`, atau rentang kustom `--dari YYYY-MM-DD --sampai YYYY-MM-DD`.
- `--rencana "..."` (bisa diulang) untuk menentukan rencana berikutnya secara eksplisit. Tanpa
  ini, rencana diturunkan otomatis dari pekerjaan berstatus `berjalan` ("Lanjutkan: ...") --
  tinjau dan sesuaikan kalimatnya sebelum dikirim, jangan asal salin apa adanya bila kurang pas.
- Tanpa `--json`, keluaran langsung berisi tiga versi berlabel (`=== VERSI EMAIL ===`,
  `=== VERSI WA/TELEGRAM ===`, `=== VERSI MARKDOWN ===`) -- pakai ini untuk langsung menyalin.
  Dengan `--json`, semua field terstruktur tersedia (`teks_email`, `teks_wa`, `markdown`, angka,
  `peringatan`, `catatan`) untuk diolah lebih lanjut.
- **Klien tidak ditemukan** di log → script menyebutkan daftar klien yang memang tercatat; jangan
  membuat laporan kosong yang seolah valid.
- **Tidak ada pekerjaan pada periode itu** → laporan tetap dibuat tapi kosong dengan `catatan`
  yang menjelaskan itu; **jangan mengarang isi** ("berjalan lancar seperti biasa").
- Script keluar kode **3** (draf tetap dibuat) bila salah satu baris log yang masuk periode
  mengandung pola mirip data pribadi/rahasia -- **tinjau bersama pengguna** sebelum draf ini
  dikirim ke klien (lihat Batasan).

### 3. Beberapa klien sekaligus
Ulangi Langkah 2 untuk tiap klien (`--klien` berbeda). Tidak ada mode "semua klien sekaligus" agar
setiap klien tetap mendapat draf yang ditinjau terpisah -- mencampur banyak klien dalam satu pesan
berisiko salah kirim data klien A ke klien B.

### 4. Sebelum mengirim ke klien
Tampilkan draf ke pengguna (konsultan) apa adanya, sebutkan `peringatan`/`catatan` bila ada,
lalu ingatkan: **skill ini tidak pernah mengirim apa pun ke klien** -- konsultan yang meninjau,
mengedit bila perlu (mis. mengisi `[Nama Anda]`), lalu menyalin & mengirim sendiri lewat
email/WA/Telegram.

### 5. (Lanjutan, opsional) Jadwalkan draf otomatis ke Telegram konsultan tiap Jumat sore
Setelah draf manual di atas terbukti benar untuk klien tersebut, tawarkan menjadwalkan
**pembuatan draf** (bukan pengirimannya ke klien) lewat OpenClaw mengikuti
`references/openclaw-jadwal.md` -- draf tetap hanya sampai ke Telegram/WhatsApp konsultan sendiri,
lalu konsultan yang menyalin ke klien manual.

## Format output
Tiga versi, semuanya dari data yang sama (lihat contoh lengkap di `examples/`):
- **Email**: subjek + salam formal + ringkasan + daftar per bagian + penutup.
- **WA/Telegram**: judul `*tebal*`, ringkasan pendek, bullet ringkas per bagian.
- **Markdown**: heading per bagian (Ringkasan, Yang Selesai, Yang Berjalan, Butuh dari Klien,
  Kendala Saat Ini, Rencana Berikutnya, Total Jam) -- cocok disimpan sebagai dokumen/lampiran.

Bagian **Total Jam** selalu berasal dari penjumlahan script (bukan perkiraan), disertai rincian
per proyek dan jumlah entri yang tidak mencatat jam (agar tidak disalahartikan sebagai 0 jam).

## Contoh
**Input pengguna:** "Catat: hari ini aku kelarin rekonsiliasi bank buat PT Maju Jaya, 2,5 jam.
Terus lagi ngerjain draf SPT Masa PPN, masih nunggu faktur pajak masukan Oktober dari mereka."

**Alur:** dua entri `catat` (satu `selesai` 2,5 jam, satu `berjalan` dengan `--butuh-klien`) →
saat diminta "buatkan laporan mingguan untuk PT Maju Jaya", jalankan `laporan --klien "PT Maju
Jaya" --periode mingguan` → tampilkan ketiga versi + catatan bila ada.

Contoh lengkap input/output nyata: `examples/uji-pembuat-01-konsultan-pajak.md`.

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- **UU PDP (UU 27/2022) -- catat seperlunya saja.** Kolom `pekerjaan`/`kendala`/
  `butuh_dari_klien` **tidak untuk** menyimpan data rahasia klien yang tidak perlu: nomor
  rekening, kredensial/password, dokumen internal rahasia klien, atau data pribadi karyawan
  klien. Cukup tulis "menunggu approval dari klien" atau "menunggu dokumen keuangan Q3", bukan
  isi dokumennya. Script mendeteksi (bukan memblokir) pola NIK/KTP/nomor HP/email/kata sandi dan
  keluar dengan **kode 3** -- tinjau ulang baris yang dituding sebelum draf dikirim atau disimpan
  lebih lama dari perlu.
- **Bukan pengganti timesheet resmi/invoice.** Total jam di sini untuk laporan progres, bukan
  dokumen tagihan berkekuatan hukum; untuk menagih klien pakai `buat-invoice`.
- **Tidak pernah mengirim apa pun ke klien secara otomatis.** Draf email/WA/Telegram selalu untuk
  disalin manual oleh konsultan. Penjadwalan OpenClaw (Langkah 5) hanya mengirim draf ke
  Telegram/WhatsApp **konsultan sendiri**, tidak pernah langsung ke klien -- lihat aturan kanal di
  `references/openclaw-jadwal.md` §0.
- **Jam tidak boleh > 24 per baris** dan tidak boleh negatif -- script menolak dengan pesan jelas;
  pekerjaan lintas hari dipecah jadi beberapa baris `catat`.
- **File log rusak/kolom tidak sesuai** → script menyebutkan baris & kolom yang bermasalah;
  jangan mengarang isi baris yang tidak terbaca, minta pengguna memperbaiki filenya.
- **Klien/periode tanpa catatan** → laporan kosong yang jujur (lihat Langkah 2), tidak pernah
  mengisi dengan kalimat generik.
- **Python tidak bisa dijalankan**: rakit laporan manual mengikuti struktur Format Output di
  atas dari catatan yang diberikan pengguna langsung di chat, dan sebutkan bahwa total jam belum
  diverifikasi oleh script.
- **Data tidak pernah dikirim ke luar komputer** oleh script ini -- hanya teks yang mengalir ke
  penyedia model AI (seperti percakapan biasa) dan pesan yang dikirim manual oleh konsultan sendiri.
