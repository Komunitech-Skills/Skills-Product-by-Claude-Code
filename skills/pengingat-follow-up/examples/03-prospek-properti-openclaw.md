# 03 — Sales properti: follow-up prospek H+1/3/7, janji sekali jalan, jadwal OpenClaw ke Telegram

**Skenario:** Agen properti (member VIP, sudah memakai OpenClaw) baru selesai survei dengan calon pembeli
kemarin, ingin diingatkan H+1/H+3/H+7, punya janji survei lokasi Sabtu jam 9, dan ingin rekap tiap pagi
masuk Telegram. Hari acuan: Kamis, 1 Oktober 2026. Nama & nomor fiktif.

## Input pengguna (persis)
> Pak Andi 0812-0000-1234 kemarin survei rumah tipe 45 Cluster Melati, istrinya masih ragu soal cicilan.
> ingetin aku follow up H+1, H+3, H+7 ya. Sabtu 3 Okt jam 9 aku ada janji survei kavling blok C sama Bu Sari,
> ingetin pagi itu jam 9 juga. Terus tiap pagi jam 8 kirim rekapnya ke Telegram aku aja.

## Proses & output

### 1. Percobaan pertama agent ikut menyimpan nomor HP → ditolak script (benar)
```bash
$S --teks tambah --jenis prospek --nama "Pak Andi" --tanggal "besok" --perihal "rumah tipe 45 Cluster Melati" --catatan "0812-0000-1234, survei kemarin"
```
```
ERROR: kolom catatan berisi nomor HP. Daftar ini cukup menyimpan nama panggilan/kode; kontak sudah ada di HP Anda. Hapus data itu, atau tambahkan --simpan-kontak bila pemilik memang sengaja menyimpannya
(kode keluar 2)
```

### 2. Simpan ulang tanpa nomor. Tahap H+n ditaruh di `catatan` (pribadi) supaya tidak masuk draf
```bash
S="python3 <folder-skill>/scripts/cek_jatuh_tempo.py --hari-ini 2026-10-01"
$S --teks tambah --jenis prospek --nama "Pak Andi" --tanggal "besok"       --perihal "rumah tipe 45 Cluster Melati" --catatan "H+1 setelah survei 30 Sep; istri ragu soal cicilan"
$S --teks tambah --jenis prospek --nama "Pak Andi" --tanggal "+3"          --perihal "rumah tipe 45 Cluster Melati" --catatan "H+3: kirim simulasi KPR"
$S --teks tambah --jenis prospek --nama "Pak Andi" --tanggal "7 hari lagi" --perihal "rumah tipe 45 Cluster Melati" --catatan "H+7: tawarkan jadwal survei ulang"
$S --teks tambah --jenis janji   --nama "Bu Sari"  --tanggal "3 Okt"       --perihal "survei lokasi kavling blok C jam 09.00"
```
Balasan agent:
```
Nomor HP Pak Andi tidak saya simpan (sudah ada di HP Anda). Cukup nama panggilan.

Tersimpan #1: prospek - Pak Andi, Jumat, 2 Oktober 2026 (rumah tipe 45 Cluster Melati).
Tersimpan #2: prospek - Pak Andi, Minggu, 4 Oktober 2026 (rumah tipe 45 Cluster Melati).
Tersimpan #3: prospek - Pak Andi, Kamis, 8 Oktober 2026 (rumah tipe 45 Cluster Melati).
Tersimpan #4: janji - Bu Sari, Sabtu, 3 Oktober 2026 (survei lokasi kavling blok C jam 09.00).
Catatan: Tahun tidak disebut; dipakai 3 Okt 2026 (tanggal terdekat ke depan). Ubah bila maksudnya lain.
```
(H+1/3/7 dihitung dari hari ini 1 Okt, sesuai permintaan "ingetin H+1". Kalau maksudnya dari hari survei
30 Sep, bilang saja nanti saya geser.)

### 3. Rekap pagi Jumat 2 Okt (`--hari-ini 2026-10-02 --teks rekap`, apa adanya)
```
PENGINGAT FOLLOW-UP - Jumat, 2 Oktober 2026

HARI INI (1)
1. #1 Prospek - Pak Andi | rumah tipe 45 Cluster Melati | hari ini
   Catatan: H+1 setelah survei 30 Sep; istri ragu soal cicilan

BESOK / H-1 (1)
1. #4 Janji - Bu Sari | survei lokasi kavling blok C jam 09.00 | besok, 3 Okt 2026

Total piutang tertunggak (terlambat + hari ini): Rp 0
Menyusul 7 hari ke depan: 2 item

DRAF PESAN (cek dulu, lalu salin & kirim sendiri dari WA/email Anda)

#1 untuk Pak Andi:
Halo Pak Andi, semoga harinya lancar. Saya ingin menindaklanjuti rumah tipe 45 Cluster Melati. Apakah ada yang bisa saya bantu jelaskan lagi? Kalau belum jadi prioritas, cukup balas "nanti" saja, saya tidak akan mengganggu.
(Saran: Butuh urutan lengkap H+1/3/7/14? Pakai skill follow-up-prospek.)

#4 untuk Bu Sari:
Halo Bu Sari, mengingatkan janji kita besok, 3 Okt 2026 untuk survei lokasi kavling blok C jam 09.00. Apakah jadwalnya masih sesuai? Terima kasih.

Balas misalnya: "selesai 3", "tunda 3 ke Senin", "hapus 3".
```

### 4. Jadwal OpenClaw — agent menampilkan ringkasan dulu (SKILL.md Langkah 5)
```
Saya akan membuat 2 jadwal di OpenClaw:
1. Rekap follow-up tiap hari 08.00 WIB → Telegram Anda (chat ID 123456789).
2. Pengingat sekali jalan Sabtu 3 Okt 09.00 WIB → Telegram Anda: janji survei dengan Bu Sari (#4), lalu jadwal ini terhapus sendiri.
Pesan hanya dikirim ke ANDA. Bot tidak mengirim apa pun ke Pak Andi/Bu Sari.
Catatan: jadwal hanya jalan bila komputer/Gateway OpenClaw menyala jam segitu. Setiap run memakai token model (biaya Anda).
Lanjut? (ya/tidak)
```
*(pengguna: "ya")*
```bash
openclaw automations add "0 8 * * *" \
  "Pakai skill pengingat-follow-up. Jalankan: python3 /home/<user>/.openclaw/skills/pengingat-follow-up/scripts/cek_jatuh_tempo.py --file /home/<user>/.openclaw/workspace/pengingat/DAFTAR.csv --timesheet-file /home/<user>/.openclaw/workspace/pengingat/timesheet.csv --teks rekap. Kirim teksnya apa adanya dalam Bahasa Indonesia. JANGAN mengubah angka, JANGAN mengirim apa pun ke pelanggan. Jika file belum ada atau script error, laporkan itu saja." \
  --name "Pengingat follow-up harian" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "123456789"

openclaw automations add --name "Survei Bu Sari (#4)" --at "2026-10-03T09:00" --tz "Asia/Jakarta" \
  --message "Ingatkan pemilik: jam 09.00 survei kavling blok C dengan Bu Sari (#4). Tampilkan draf dengan skill pengingat-follow-up: cek_jatuh_tempo.py --file /home/<user>/.openclaw/workspace/pengingat/DAFTAR.csv --teks draf --id 4. Jangan kirim apa pun ke pelanggan." \
  --session isolated --announce --channel telegram --to "123456789" --delete-after-run
```
Hasil uji penguji di Gateway uji OpenClaw 2026.9.5 (HOME sementara, `gateway run --dev --allow-unconfigured --bind loopback`):
```
job 1: schedule {kind: cron, expr: "0 8 * * *", tz: "Asia/Jakarta"}, sessionTarget isolated,
       delivery announce -> telegram:123456789 (explicit), nextRunAtMs 1790211600000 = 2026-09-24 01:00 UTC = 08:00 WIB
job 2: schedule {kind: at, at: "2026-10-03T02:00:00.000Z"} (= 09:00 WIB), deleteAfterRun: true
```
Balasan agent setelah job dibuat:
```
Jadwal aktif (id disimpan: 0b0d67dc-…, 25ff25cc-…). Untuk mengujinya sekarang: openclaw automations run <id> --wait.
Untuk menjeda: openclaw automations disable <id> (pakai id, bukan nama).
Belum diuji sampai pesan benar-benar tiba di Telegram; kalau besok jam 8 tidak ada pesan, kabari saya.
```

## Catatan penguji
- Bagus: penolakan nomor HP (kode 2) bekerja. Kanal Telegram default, konfirmasi "Lanjut? (ya/tidak)",
  `--to` = pemilik, tidak ada broadcast. Semua sintaks OpenClaw di `references/openclaw-jadwal.md` cocok dengan
  `--help` dan terbentuk sungguhan di Gateway uji (lihat HASIL-UJI). Status verifikasi ditulis jujur.
- **Cacat SEDANG terkait:** `draf --id 4` yang dijalankan **1 Okt** (2 hari sebelum janji) menghasilkan
  "mengingatkan janji kita **besok**, 3 Okt 2026", padahal lusa. Sama untuk piutang: `draf --id` item 9 hari ke depan
  berbunyi "jatuh tempo besok" (lihat 04). Rekap aman karena hanya memuat H-1.
- Ringan: SKILL.md tidak memberi panduan pola H+1/3/7 (tiga item terpisah vs. `tunda` setelah follow-up); agent
  bisa menaruh "(H+1)" di `perihal` sehingga bocor ke draf untuk prospek (terjadi di percobaan penguji pertama).
  Draf prospek H+1, H+3, H+7 kalimatnya identik; prospek menerima pesan yang sama 3 kali. Baris
  "Total piutang tertunggak: Rp 0" tidak relevan untuk pengguna tanpa piutang.
