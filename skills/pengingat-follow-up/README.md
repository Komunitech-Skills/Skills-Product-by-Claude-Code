# Tagihan dan Follow-up Tak Lagi Mudah Terlupa

**Setiap pagi (lewat OpenClaw), asisten AI Anda dapat mengirim daftar siapa yang harus ditagih dan di-follow-up hari ini, lengkap dengan pesan siap kirim.**

*Diuji AI penguji independen di OpenClaw: 3,5 → 9,25 dari 10 (tanpa skill agent menebak nominal dan mengubah konfigurasi tanpa izin; dengan skill daftar tersimpan rapi dan draf pesan dikirim sendiri oleh Anda).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Cukup ketik satu kalimat.** "Ingatkan saya tagih Bu Rina tgl 3, 4,5 jt" langsung tercatat. Tidak perlu mengisi tabel.
- ✅ **Rekap pagi yang jelas:** yang terlambat (berapa hari), yang jatuh tempo hari ini, dan yang jatuh tempo besok. Total piutang (tagihan yang belum dibayar pelanggan) yang tertunggak dihitung otomatis oleh skrip.
- ✅ **Draf pesan siap kirim.** Nadanya sopan dan naik bertahap sesuai lama keterlambatan. Anda tinggal cek, salin, dan kirim dari WA sendiri.
- ✅ **Rekap jam kerja klien.** Jam dicatat lewat chat ("catat 1,5 jam untuk PT Kreatif"). Tiap Jumat Anda mendapat total jam, nilai rupiah, dan draf pesan ke klien.
- ✅ **Data tetap di komputer Anda.** Yang disimpan cukup nama panggilan. Skill dirancang tidak menyimpan nomor HP pelanggan.

## Cocok untuk siapa
- Pemilik usaha dengan banyak pelanggan tempo/bon: supplier, grosir, katering, konveksi, percetakan.
- Freelancer dan konsultan yang menagih per jam: desainer, programmer, konsultan pajak, pengajar privat.
- Tenaga penjual yang sering lupa menghubungi lagi calon pembeli.
- Member VIP Komunitech yang sudah memakai OpenClaw dan ingin rekap otomatis tiap pagi di Telegram (kiriman terjadwal ke Telegram belum diuji langsung).

## Contoh sebelum & sesudah
**Sebelum:** catatan piutang tersebar di buku, chat WA, dan ingatan. Tagihan CV Maju baru teringat setelah telat
sebulan. Pesan tagihan diketik dari nol setiap kali, dan kadang nadanya terlalu keras atau malah terlalu sungkan.

**Sesudah (cukup ketik):** "Ingatkan saya follow-up Bu Rina tgl 3 kalau belum bayar 4,5 jt."
→ Tersimpan, dan pada hari jatuh tempo masuk rekap. Cuplikan balasan asli dari uji OpenClaw 1 Okt 2026 (dipotong; pesan ujinya mencatat tiga hal sekaligus, lalu bertanya "hari ini aku harus nagih siapa aja? kasih draf chatnya sekalian"; data fiktif, dari `examples/00-openclaw-sebelum-sesudah.md`):
```
Semua sudah dicatat ✅
1. #1 Bu Rina — piutang Rp 4.500.000 (INV-012), jatuh tempo Sabtu, 3 Okt 2026
2. #2 Pak Budi — janji follow-up penawaran katering, Senin 5 Okt 2026
3. #3 Toko Sinar — piutang Rp 2.750.000, jatuh tempo 25 Sep 2026 → sudah terlambat 6 hari

Hari ini (1 Okt) yang perlu ditagih: Toko Sinar saja — total piutang tertunggak Rp 2.750.000.

Draf chat ke Toko Sinar (tinggal salin & kirim sendiri):
Selamat pagi Toko Sinar, mohon maaf mengganggu. Menurut catatan kami, pembayaran tagihan
sebesar Rp 2.750.000 yang jatuh tempo 25 Sep 2026 belum kami terima. Mungkin terlewat; jika
sudah transfer, mohon kirimkan bukti transfernya. Jika belum, pembayaran bisa melalui
[rekening]. Terima kasih.
```
Tanda `[rekening]` adalah isian yang perlu Anda lengkapi sendiri sebelum dikirim. Sudah dibayar? Balas "Bu Rina sudah bayar", dan item itu tidak muncul lagi. (Rekap otomatis tiap pagi ke Telegram belum diuji langsung.)

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Ingatkan saya tagih CV Maju 12,5 jt tanggal 20 Oktober, invoice INV-0788."
- "Pak Budi minta dihubungi lagi Senin soal penawaran katering."
- "Hari ini saya harus follow-up siapa saja?"
- "Tunda Pak Budi ke Kamis." / "Bu Rina sudah bayar."
- "Catat 2 jam untuk PT Kreatif, revisi logo, tarif 150 ribu."
- "Rekap jam kerja PT Kreatif minggu ini, buatkan pesannya."
- "Aktifkan pengingat follow-up tiap pagi jam 8 ke Telegram saya." (khusus OpenClaw; kiriman terjadwalnya belum diuji langsung)

**Penting:** asisten hanya **menyiapkan** pesan. Anda sendiri yang mengirimnya ke pelanggan. Dengan begitu
risiko salah tagih lebih kecil, dan nomor WA Anda tidak dipakai mengirim pesan otomatis (yang bisa membuat nomor diblokir).

## Instalasi singkat
Salin folder `pengingat-follow-up` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

Rekap otomatis tiap pagi hanya tersedia di **OpenClaw**, dan komputer yang menjalankan OpenClaw harus menyala
pada jam tersebut. Di Claude Code, Codex, atau Cursor, skill ini berfungsi sebagai daftar pantauan manual:
ketik "rekap pengingat" setiap pagi (Codex dan Cursor belum diuji langsung).

**Hasil uji (angka nyata):** penguji AI independen, skor 1–10, di OpenClaw (uji otomatis agent, 1 Oktober 2026; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 3,5 tanpa skill menjadi 9,25 dengan skill. Tanpa skill, agent menebak nominal, menyimpan nomor HP pihak ketiga, mengubah konfigurasi tanpa izin, dan berniat mengirim tagihan otomatis ke pelanggan. Dengan skill, nominal ambigu ("5m") dan tanggal mustahil (31/9) ditanyakan dulu, daftar tersimpan rapi bernomor, dan draf pesan dikirim sendiri oleh Anda.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent, termasuk membuat jadwal harian dan menjalankannya sekali di Gateway uji, yaitu program OpenClaw yang berjalan di latar belakang) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung. Kiriman terjadwal yang benar-benar tiba di Telegram pada jam yang ditentukan belum diuji langsung. Draf tagihan bisa memuat tanda isian seperti `[rekening]`; isi dulu sebelum dikirim.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang uji 4 (satu putaran uji di bot), 2026-10-03. Versi yang diuji tidak tercatat di catatan gelombang (versi repo saat itu: 1.0.6, sama dengan versi terkini).
- Tanpa skill: https://t.me/c/4407409583/582/600 — skor tidak dicatat di gelombang itu
- Dengan skill: https://t.me/c/4407409583/583/603 — skor tidak dicatat di gelombang itu
Verdik gelombang: tidak dicatat di gelombang itu — angka dan draf kedua sisi benar; beda di keamanan dan pencatatan: TANPA menawarkan "kirim langsung ke mereka" dan berjanji mengingatkan Senin tanpa jadwal nyata, DENGAN tersimpan terstruktur (#1–#3), menyebut tahun yang diasumsikan, total Rp7.250.000, dan draf dikirim sendiri oleh pengguna. Catatan kecil: draf ke Toko Sinar memuat tenggat "paling lambat 6 Okt" yang tidak diminta pengguna.

## FAQ
**Apakah bot akan menagih pelanggan saya secara otomatis?**
Tidak. Rekap dan draf hanya dikirim ke **Anda** (Telegram, atau WhatsApp nomor terpisah milik Anda). Anda
yang memutuskan dan mengirim sendiri. Ini disengaja: tagihan yang salah kirim merusak hubungan dengan
pelanggan, dan pesan otomatis lewat WhatsApp tidak resmi bisa membuat nomor diblokir.

**Data pelanggan saya disimpan di mana?**
Di file `pengingat/DAFTAR.csv` (file tabel yang bisa dibuka di Excel) di komputer Anda sendiri, bukan di server Komunitech. Isinya cukup nama
panggilan atau kode, nominal, dan tanggal. Skill dirancang menolak menyimpan nomor HP, email, atau NIK. Catatan pribadi
Anda tidak dimasukkan ke draf pesan. Item yang sudah selesai bisa dibersihkan otomatis.

**Bagaimana jika saya salah ketik tanggal atau tidak menyebut tahun?**
Tanggal ditulis bebas: "3/10", "3 Okt", "besok", "Jumat". Jika tahun tidak disebut, asisten memilih tanggal
terdekat dan memberi tahu pilihannya supaya bisa Anda koreksi. Tanggal yang mustahil (mis. 31/2) langsung
ditolak dengan penjelasan.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
