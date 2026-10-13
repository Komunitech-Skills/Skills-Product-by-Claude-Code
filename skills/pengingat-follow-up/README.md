# Tak Ada Lagi Tagihan dan Follow-up Terlupa

**Setiap pagi, asisten AI Anda mengirim daftar siapa yang harus ditagih dan di-follow-up hari ini, lengkap dengan pesan siap kirim.**

## Manfaat
- ✅ **Cukup ketik satu kalimat.** "Ingatkan saya tagih Bu Rina tgl 3, 4,5 jt" langsung tercatat. Tidak perlu mengisi tabel.
- ✅ **Rekap pagi yang jelas:** yang terlambat (berapa hari), yang jatuh tempo hari ini, dan yang jatuh tempo besok. Total piutang tertunggak dihitung otomatis dan tepat.
- ✅ **Draf pesan siap kirim.** Nadanya sopan dan naik bertahap sesuai lama keterlambatan. Anda tinggal cek, salin, dan kirim dari WA sendiri.
- ✅ **Rekap jam kerja klien.** Jam dicatat lewat chat ("catat 1,5 jam untuk PT Kreatif"). Tiap Jumat Anda mendapat total jam, nilai rupiah, dan draf pesan ke klien.
- ✅ **Data tetap di komputer Anda.** Yang disimpan cukup nama panggilan. Nomor HP pelanggan tidak ikut disimpan.

## Cocok untuk siapa
- Pemilik usaha dengan banyak pelanggan tempo/bon: supplier, grosir, katering, konveksi, percetakan.
- Freelancer dan konsultan yang menagih per jam: desainer, programmer, konsultan pajak, pengajar privat.
- Tenaga penjual yang sering lupa menghubungi lagi calon pembeli.
- Member VIP Komunitech yang sudah memakai OpenClaw dan ingin rekap otomatis tiap pagi di Telegram.

## Contoh sebelum & sesudah
**Sebelum:** catatan piutang tersebar di buku, chat WA, dan ingatan. Tagihan CV Maju baru teringat setelah telat
sebulan. Pesan tagihan diketik dari nol setiap kali, dan kadang nadanya terlalu keras atau malah terlalu sungkan.

**Sesudah (cukup ketik):** "Ingatkan saya follow-up Bu Rina tgl 3 kalau belum bayar 4,5 jt."
→ Tersimpan. Pagi 2 Okt (H-1) dan 3 Okt, rekap di Telegram Anda menampilkan:
```
HARI INI (1)
1. #1 Piutang - Bu Rina | Rp 4.500.000 | INV-012 | jatuh tempo hari ini
Total piutang tertunggak (terlambat + hari ini): Rp 4.500.000

#1 untuk Bu Rina:
Selamat pagi Bu Rina, kami mengingatkan pembayaran INV-012 sebesar Rp 4.500.000 jatuh tempo hari ini, ...
```
Sudah dibayar? Balas "Bu Rina sudah bayar", dan item itu tidak muncul lagi.

**Hasil uji (OpenClaw, uji otomatis agent, 1 Oktober 2026):** rata-rata nilai 3,5 tanpa skill menjadi 9,25 dengan skill (skala 10). Tanpa skill, agent menebak nominal, menyimpan nomor HP pihak ketiga, mengubah konfigurasi tanpa izin, dan berniat mengirim tagihan otomatis ke pelanggan. Dengan skill, nominal ambigu ("5m") dan tanggal mustahil (31/9) ditanyakan dulu, daftar tersimpan rapi bernomor, dan draf pesan dikirim sendiri oleh Anda. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Ingatkan saya tagih CV Maju 12,5 jt tanggal 20 Oktober, invoice INV-0788."
- "Pak Budi minta dihubungi lagi Senin soal penawaran katering."
- "Hari ini saya harus follow-up siapa saja?"
- "Tunda Pak Budi ke Kamis." / "Bu Rina sudah bayar."
- "Catat 2 jam untuk PT Kreatif, revisi logo, tarif 150 ribu."
- "Rekap jam kerja PT Kreatif minggu ini, buatkan pesannya."
- "Aktifkan pengingat follow-up tiap pagi jam 8 ke Telegram saya." (khusus OpenClaw)

**Penting:** asisten hanya **menyiapkan** pesan. Anda sendiri yang mengirimnya ke pelanggan. Dengan begitu
Anda tidak salah tagih, dan nomor WA Anda tidak berisiko diblokir karena pesan otomatis.

## Instalasi singkat
Salin folder `pengingat-follow-up` ke folder skills AI agent kamu:

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

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 4, 2026-10-03.
- Tanpa skill: https://t.me/c/4407409583/582/600 — skor: lihat catatan gelombang
- Dengan skill: https://t.me/c/4407409583/583/603 — skor: lihat catatan gelombang
Verdik gelombang: — — Angka dan draf kedua sisi benar; beda di keamanan dan pencatatan: TANPA menawarkan kirim langsung dan berjanji mengingatkan tanpa jadwal nyata, DENGAN mencatat terstruktur dan draf dikirim sendiri oleh pengguna.

## FAQ
**Apakah bot akan menagih pelanggan saya secara otomatis?**
Tidak. Rekap dan draf hanya dikirim ke **Anda** (Telegram, atau WhatsApp nomor terpisah milik Anda). Anda
yang memutuskan dan mengirim sendiri. Ini disengaja: tagihan yang salah kirim merusak hubungan dengan
pelanggan, dan pesan otomatis lewat WhatsApp tidak resmi bisa membuat nomor diblokir.

**Data pelanggan saya disimpan di mana? Aman?**
Di file `pengingat/DAFTAR.csv` di komputer Anda sendiri, bukan di server Komunitech. Isinya cukup nama
panggilan atau kode, nominal, dan tanggal. Skill menolak menyimpan nomor HP, email, atau NIK. Catatan pribadi
Anda tidak pernah dimasukkan ke draf pesan. Item yang sudah selesai bisa dibersihkan otomatis.

**Bagaimana jika saya salah ketik tanggal atau tidak menyebut tahun?**
Tanggal ditulis bebas: "3/10", "3 Okt", "besok", "Jumat". Jika tahun tidak disebut, asisten memilih tanggal
terdekat dan memberi tahu pilihannya supaya bisa Anda koreksi. Tanggal yang mustahil (mis. 31/2) langsung
ditolak dengan penjelasan.

## Catatan revisi 1.0.6 (2026-10-01)
- Dari uji OpenClaw sebelum/sesudah: draf tagihan sempat memuat `[rekening]` tanpa disebut sebagai bagian yang perlu dilengkapi. Kini setiap placeholder seperti `[rekening]` wajib disebut ke pemilik sebagai yang harus diisi sebelum draf dikirim.
