# Laporan Terjadwal Gagal? Langsung Ketahuan

**Pantau Cron OpenClaw** -- tagline: *jadwal otomatis Anda diam-diam mati? Kami kabari lewat Telegram sebelum Anda sadar sendiri.*

Laporan harian 21.00, tagihan piutang 07.45, ringkasan stok... semuanya berjalan otomatis lewat OpenClaw. Sampai suatu hari laptop tertidur atau gateway mati, dan **tidak ada yang memberi tahu**. Skill ini membuat setiap jadwal otomatis "melapor selesai" setiap kali sukses. Kalau laporannya tidak datang tepat waktu, Anda dikabari. Kalau semua aman, Anda tidak diganggu.

## Manfaat
- **Tidak ada lagi gagal diam-diam**: peringatan Telegram saat laporan terlambat atau hilang, lengkap dengan jadwal yang terlewat.
- **Tidak berisik**: tidak ada pesan "semua aman" tiap jam; cukup satu ringkasan pagi dan peringatan hanya saat perlu (masalah yang sama tidak diulang-ulang, dan ada kabar saat sudah pulih).
- **Angka waktu dihitung, bukan ditebak**: jatuh tempo dihitung otomatis, termasuk lewat tengah malam, akhir bulan, dan WIB/WITA/WIT.
- **Data di komputer Anda sendiri**: tanpa akun, tanpa langganan, tanpa kunci API. Layanan luar hanya opsi lanjutan.
- **Hemat**: pengawas tidak memakai AI, jadi tanpa biaya token.

## Cocok untuk siapa
Member VIP dan pengguna OpenClaw yang sudah punya beberapa laporan/jadwal otomatis dan tidak ingin tahu terlambat bahwa salah satunya mati: pemilik toko, manajer kantor, pemilik klinik, konsultan.

## Sebelum / sesudah
> Bagian ini **diisi setelah uji** (hasil uji sebelum/sesudah OpenClaw akan ditempel di `examples/`).

| Sebelum | Sesudah |
|---|---|
| Baru sadar laporan mati saat dibutuhkan, berhari-hari kemudian | _akan diisi dari hasil uji_ |

Versi 1.0.1. Laporan pantauan memisahkan blok **BERMASALAH** (HILANG/TERLAMBAT) dan blok **OK**.

## Contoh peringatan Telegram
```
PANTAU CRON - 12 Okt 21.40 WIB
BERMASALAH (1 dari 2):
- TERLAMBAT laporan-harian: jadwal 12 Okt 21.00 WIB belum ada ping, lewat 40 menit dari jadwal (toleransi 30 menit). Ping terakhir 11 Okt 21.02 WIB.
OK (1): piutang-pagi
```

## Cara pakai (cukup bicara ke agen Anda)
- "Pantau laporan harian 21.00 dan piutang 07.45 Senin-Jumat saya. Kabari ke Telegram kalau gagal."
- "Job mana yang terlambat hari ini?"
- "Daftarkan laporan mingguan Senin 07.00 ke pantauan."
- "Kabari kalau laporan otomatis saya mati." (tidak perlu menyebut jadwalnya dulu; agen mengerjakan dulu dengan contoh atau jadwal yang terdeteksi, lalu bertanya di akhir)
Agen akan mendaftarkan jadwal, menambahkan satu langkah "lapor selesai" di akhir tiap laporan, memasang pengawas, lalu meminta persetujuan Anda sebelum mengubah apa pun. Bila agen belum punya izin ke pengatur jadwal OpenClaw Anda, ia berhenti setelah satu kali gagal (tidak mengutak-atik konfigurasi atau kunci Anda) dan memberi rencana lengkap yang bisa Anda salin sendiri.

## Instalasi singkat
Folder `pantau-cron-openclaw` disalin ke lokasi skill platform Anda -- lokasi lengkap per platform (OpenClaw, Codex, Claude Code, Cursor) ada di `docs/instalasi.md` dalam paket. Dipakai dengan OpenClaw; butuh Python 3 (Windows: `python` atau `py`). Tidak perlu memasang paket tambahan.

## Yang perlu Anda siapkan
- OpenClaw berjalan dan Telegram sudah terhubung (bot resmi). Belum? Skill `laporan-otomatis-terjadwal` memandu.
- Komputer/gateway menyala saat jam jadwal. Pengawas lokal ikut diam bila komputer mati total -- untuk itu ada opsi layanan luar milik Anda sendiri (Healthchecks self-host/hosted; tidak berafiliasi dengan Komunitech), atau mesin 24 jam. Komunitech menyediakan **jasa setup berbayar**.

## Batas yang jujur
- Skill tahu **apakah job melapor**, bukan apakah isinya benar.
- Ini untuk memantau job dan sistem **milik sendiri** (atau tim dengan pemberitahuan tertulis). Skill menolak memantau komputer/aktivitas orang lain diam-diam.

## FAQ
**1. Apakah ini memata-matai komputer saya atau karyawan?**
Tidak. Skill hanya mencatat "job X melapor selesai pukul sekian" di komputer Anda. Ia tidak membaca layar, pesan, atau file, dan menolak dipakai untuk mengawasi orang lain diam-diam.

**2. Bagaimana kalau komputer saya mati total?**
Pengawas lokal ikut mati, jadi tidak ada peringatan sampai komputer menyala. Untuk jaminan lebih kuat, pakai opsi layanan luar (panduan di skill) atau mesin 24 jam. Kami tidak menjanjikan "pasti ketahuan" tanpa itu.

**3. Apakah bisa dipakai di WITA/WIT dan untuk jadwal bulanan?**
Bisa. Zona WIB, WITA, WIT didukung, dan jadwal cron seperti "tanggal 1 tiap bulan" atau "Senin-Jumat" dihitung dengan benar.

## Untuk pengembang / penguji
`python3 tests/uji_regresi.py` menjalankan uji regresi (parsing jadwal, jatuh tempo lintas hari/bulan, toleransi, status, zona waktu, input rusak).
