# Laporan Terjadwal Gagal? Langsung Ketahuan

**Pantau Cron OpenClaw** -- tagline: *jadwal otomatis Anda diam-diam mati? Anda dikabari lewat Telegram, tidak perlu menunggu sadar sendiri.*

Diuji AI penguji independen di OpenClaw: 4,63 → 8,19 dari 10 (tanpa skill asisten hanya menjawab "sudah terpasang dan aktif" tanpa bukti; dengan skill jadwal yang terlambat atau hilang ketahuan dari hitungan jam).

Laporan harian 21.00, tagihan piutang 07.45, ringkasan stok... semuanya berjalan otomatis lewat OpenClaw. Sampai suatu hari laptop tertidur atau OpenClaw berhenti, dan **tidak ada yang memberi tahu**. Skill ini membuat setiap jadwal otomatis "melapor selesai" setiap kali sukses. Kalau laporannya tidak datang tepat waktu, Anda dikabari lewat Telegram (pengiriman ke Telegram sungguhan belum diuji langsung; lihat "Hasil uji" di bawah). Kalau semua jadwal lapor tepat waktu, Anda tidak diganggu.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- **Gagal tidak lagi diam-diam**: peringatan lewat Telegram saat laporan terlambat atau hilang, lengkap dengan jadwal yang terlewat (selama komputer dan OpenClaw menyala; pengiriman ke Telegram sungguhan belum diuji langsung).
- **Tidak berisik**: tidak ada pesan "semua aman" tiap jam; cukup satu ringkasan pagi dan peringatan hanya saat perlu (masalah yang sama tidak diulang-ulang, dan ada kabar saat sudah pulih).
- **Angka waktu dihitung, bukan ditebak**: jatuh tempo dihitung otomatis, termasuk lewat tengah malam, akhir bulan, dan WIB/WITA/WIT.
- **Data di komputer Anda sendiri**: tanpa akun, tanpa langganan, tanpa kunci API. Layanan luar hanya opsi lanjutan.
- **Hemat**: pengawas tidak memakai AI, jadi tanpa biaya pemakaian AI.

## Cocok untuk siapa
Member VIP dan pengguna OpenClaw yang sudah punya beberapa laporan/jadwal otomatis dan tidak ingin tahu terlambat bahwa salah satunya mati: pemilik toko, manajer kantor, pemilik klinik, konsultan.

## Sebelum / sesudah
| Sebelum | Sesudah |
|---|---|
| Baru sadar laporan mati saat dibutuhkan, berhari-hari kemudian. Asisten tanpa skill hanya menjawab "sudah terpasang dan aktif" tanpa bukti, dan tidak ada pengawas bagi jadwal yang hilang | Daftar jadwal yang dipantau, satu langkah "lapor selesai" di akhir tiap laporan, pengawas siap salin, dan peringatan Telegram hanya saat ada yang terlambat atau hilang |

Versi 1.0.3. Laporan pantauan memisahkan blok **BERMASALAH** (HILANG/TERLAMBAT) dan blok **OK**.

## Contoh isi peringatan (keluaran nyata dari uji)
Data contoh fiktif (Toko Bangunan Sinar Jaya), uji OpenClaw 12 Okt 2026; teks ini yang diteruskan ke Telegram (`examples/02-job-mana-yang-terlambat-hari-ini.md`):
```
PANTAU CRON - 12 Okt 21.40 WIB
BERMASALAH (2 dari 3):
- HILANG backup-data: belum pernah lapor selesai sejak didaftarkan (2 jadwal terlewat, terakhir 11 Okt 02.00 WIB). Cek apakah langkah "lapor selesai" sudah ditambahkan di akhir jadwal otomatis itu.
- TERLAMBAT laporan-harian: jadwal 12 Okt 21.00 WIB belum ada kabar "selesai", lewat 40 menit dari jadwal (toleransi 30 menit). Terakhir lapor selesai 11 Okt 21.03 WIB.
OK (1):
- tagih-piutang: terakhir lapor selesai 12 Okt 07.46 WIB; berikutnya 13 Okt 07.45 WIB.
```

## Cara pakai (cukup bicara ke asisten OpenClaw Anda)
- "Pantau laporan harian 21.00 dan piutang 07.45 Senin-Jumat saya. Kabari ke Telegram kalau gagal."
- "Job mana yang terlambat hari ini?"
- "Daftarkan laporan mingguan Senin 07.00 ke pantauan."
- "Kabari kalau laporan otomatis saya mati." (tidak perlu menyebut jadwalnya dulu; asisten mengerjakan dulu dengan contoh atau jadwal yang terdeteksi, lalu bertanya di akhir)
Asisten akan mendaftarkan jadwal, menambahkan satu langkah "lapor selesai" di akhir tiap laporan, memasang pengawas, lalu meminta persetujuan Anda sebelum mengubah apa pun. Bila belum ada izin ke pengatur jadwal OpenClaw Anda, asisten berhenti setelah satu kali gagal (tidak mengutak-atik pengaturan Anda) dan memberi rencana lengkap yang bisa Anda salin sendiri. Pemasangan penuh di pengatur jadwal (sampai kabar masuk ke Telegram) belum teruji otomatis; setelah terpasang, asisten mengajak satu uji peringatan.

## Instalasi singkat
Folder `pantau-cron-openclaw` disalin ke lokasi skill platform Anda -- lokasi lengkap per platform (OpenClaw, Codex, Claude Code, Cursor) ada di `docs/instalasi.md` dalam paket. Dipakai dengan OpenClaw; butuh Python 3 (Windows: `python` atau `py`). Tidak perlu memasang paket tambahan.

## Yang perlu Anda siapkan
- OpenClaw berjalan dan Telegram sudah terhubung (bot resmi). Belum? Skill Laporan Otomatis Terjadwal (menyiapkan laporan otomatis ke Telegram) memandu.
- Komputer dan OpenClaw menyala saat jam jadwal. Pengawas di komputer ikut diam bila komputer mati total -- untuk itu ada opsi layanan pemantau luar milik Anda sendiri (Healthchecks, dipasang sendiri atau berlangganan; tidak berafiliasi dengan Komunitech), atau komputer yang menyala 24 jam. Komunitech menyediakan **jasa setup berbayar**.

## Batas yang jujur
- Skill tahu **apakah jadwal otomatis sudah lapor selesai**, bukan apakah isinya benar.
- Ini untuk memantau jadwal otomatis dan sistem **milik sendiri** (atau tim dengan pemberitahuan tertulis). Skill menolak memantau komputer/aktivitas orang lain diam-diam.

**Hasil uji (angka nyata):** uji OpenClaw 12 Okt 2026 (diuji pada v1.0.2; v1.0.3 merapikan bahasa balasan), skor 1–10 penguji independen dari 4 skenario: tanpa skill **4,63** → dengan skill **8,19** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Hasil di bot Telegram asli ada di bagian berikutnya. Tanpa skill asisten menjawab "sudah terpasang dan aktif" tanpa bukti dan tidak ada pengawas bagi jadwal yang hilang; dengan skill ada daftar jadwal, langkah "lapor selesai", dan pengawas siap salin.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan bot Telegram uji. Perhitungan jadwal dicocokkan dengan hitungan independen pada 200 kasus acak (tanpa selisih). Pemasangan penuh sampai kabar HILANG/TERLAMBAT benar-benar masuk ke Telegram belum diuji langsung (di mesin uji belum ada OpenClaw penuh yang bisa dipakai agent). Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 15, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1250/1265 — skor 4
- Dengan skill: https://t.me/c/4407409583/1251/1268 — skor 8
Verdik gelombang: LULUS — Tanpa skill bot menjawab setelah 14 menit dengan klaim "sudah terpasang dan aktif" yang tidak diverifikasi dan tanpa pengawas bagi jadwal yang hilang; dengan skill ada daftar 3 jadwal, langkah lapor selesai, dua pengawas siap salin, dan konfirmasi "Lanjut? (ya/tidak)" sebelum apa pun dipasang.

## FAQ
**1. Apakah ini memata-matai komputer saya atau karyawan?**
Tidak. Skill hanya mencatat "jadwal X melapor selesai pukul sekian" di komputer Anda. Ia tidak membaca layar, pesan, atau file, dan menolak dipakai untuk mengawasi orang lain diam-diam.

**2. Bagaimana kalau komputer saya mati total?**
Pengawas di komputer ikut mati, jadi tidak ada peringatan sampai komputer menyala. Untuk jaminan lebih kuat, pakai opsi layanan luar (panduan di skill) atau mesin 24 jam. Kami tidak menjanjikan "pasti ketahuan" tanpa itu.

**3. Apakah bisa dipakai di WITA/WIT dan untuk jadwal bulanan?**
Bisa. Zona WIB, WITA, WIT didukung, dan jadwal otomatis seperti "tanggal 1 tiap bulan" atau "Senin-Jumat" dihitung lewat rumus tetap (dicocokkan dengan hitungan independen pada 200 kasus acak, tanpa selisih).

## Untuk pengembang / penguji
`python3 tests/uji_regresi.py` menjalankan uji regresi (parsing jadwal, jatuh tempo lintas hari/bulan, toleransi, status, zona waktu, input rusak).
