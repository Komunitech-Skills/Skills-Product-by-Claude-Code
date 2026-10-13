# Rangkaian Pesan ke Pelanggan, Tinggal Salin

**Dari satu kalimat, AI menyiapkan seluruh urutan pesan WhatsApp/Telegram/email lengkap dengan jadwal dan kapan harus berhenti.**

Diuji AI penguji independen di OpenClaw: 3,0 → 8,25 dari 10 (tanggal kirim dihitung, bukan dikira, dan permintaan kirim massal ditolak sambil tetap dibantu dengan cara yang sah).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **8 situasi siap pakai:** sambutan pelanggan baru, edukasi sebelum beli, keranjang tertunda, setelah beli, minta ulasan, perpanjangan/langganan, ajak balik pelanggan lama, peluncuran produk baru.
- ✅ **Semua pesan ditulis utuh**, bahasa WA sehari-hari yang sopan, tinggal isi `[nama]` dan salin. Tidak ada saran umum "buatlah pesan yang menarik".
- ✅ **Tanggal kirim dihitung**, bukan dikira: hari Minggu dilewati (hari libur ikut dilewati bila Anda menyebut tanggalnya), dan bila banyak pelanggan, jadwal dibagi per hari maksimal 10 pesan untuk mengurangi risiko nomor WA Anda dibatasi.
- ✅ **Sopan dan menghormati pelanggan:** pilihan berhenti ("balas stop") di tiap pesan, aturan berhenti begitu pelanggan membalas atau komplain, tanpa urgensi palsu, diskon karangan, atau ulasan palsu.
- ✅ **Cocok dengan cara kerja sehari-hari:** AI menyiapkan pesan, Anda sendiri yang menekan kirim. Bila memakai OpenClaw, Anda bisa meminta pengingat jadwal otomatis di Telegram (belum diuji langsung); pengingat itu hanya untuk Anda, bukan pesan ke pelanggan.

## Cocok untuk siapa
- Pemilik toko online, toko kue, kafe, salon, bengkel, jasa servis, kursus, katering, dan usaha langganan
- Admin/CS yang diminta "bikin follow-up ke pelanggan" dan bingung mulai dari mana
- Pengguna listmonk (aplikasi pengirim email massal gratis) atau Telegram yang butuh isi urutan pesan
- **Bukan untuk:** kirim massal otomatis ke ratusan nomor, pesan pertama ke calon pelanggan (pakai skill Pesan Prospek WA, `pesan-prospek-wa`), calon pembeli yang diam sesudah penawaran (skill Follow-up Prospek, `follow-up-prospek`), atau balas keluhan (skill Balas Chat CS, `balas-chat-cs`)

## Contoh sebelum & sesudah
**Sebelum:** Pelanggan baru dibiarkan sampai tiba-tiba ditawari promo; keranjang tertunda tidak pernah ditanya; ulasan hanya diminta kalau ingat; pesan promo dikirim sama ke semua orang dan sering diabaikan atau dilaporkan spam.

**Sesudah (cukup ketik):** "Toko kue saya mau bikin pesan sambutan buat pelanggan baru, pelanggan pertama beli Rabu 7 Oktober."
Cuplikan keluarannya (contoh dengan data fiktif, dari `examples/01-sambutan-toko-kue.md`):

```
| Pesan | Tanggal kirim | Tujuan |
|---|---|---|
| 1 | Rabu, 7 Oktober 2026 | Terima kasih + kabar pesanan |
| 2 | Sabtu, 10 Oktober 2026 | Tips menyimpan kue |
| 3 | Sabtu, 17 Oktober 2026 | Tanya kabar, buka pintu untuk kendala |
| 4 | Rabu, 28 Oktober 2026 | Kenalkan menu lain (hanya bila Anda mau) |

**Pesan 1**
Halo Kak [nama], terima kasih sudah pesan [nama kue] di Kue Bu Rina. Pesanan Kakak [sedang kami siapkan / akan diantar tanggal `[isian]`]. Kalau ada yang mau diubah atau ditanyakan, balas saja chat ini. Salam, Rina. Kalau tidak ingin dapat pesan seperti ini lagi, balas "stop" ya.
…
```

Menyusul pesan 2 sampai 4, aturan kapan berhenti, dan cara kirim dari WA Anda sendiri.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa, misalnya:
- "Bikin rangkaian pesan sambutan untuk pelanggan baru toko saya."
- "Pembeli sering tanya-tanya lalu hilang, bikin follow-up-nya."
- "Aku mau minta ulasan Google setelah servis selesai."
- "Buat pengingat perpanjangan langganan, jatuh tempo 20 Desember."

Tidak perlu akun atau API key. Skill hanya menyiapkan pesan dan jadwal; **Anda yang mengirim**, satu per satu. Program penghitung jadwal bawaan (memakai Python standar) membantu menghitung tanggal, dan skill tetap berguna walau program itu tidak bisa dijalankan.

## Instalasi singkat
Salin folder `rangkaian-pesan-pelanggan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.1):** rata-rata nilai 3,0 tanpa skill menjadi 8,25 dengan skill (skala 10), dari dua skenario: sambutan pembeli baru dan permintaan kirim massal ke 300 kontak. Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Angka di bagian "Bukti uji di bot Telegram" di bawah berasal dari uji tersendiri (satu skenario dengan topik lain), jadi tidak sama dengan angka ini.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech): gelombang 12, 2026-10-12 (tautan pesan tidak tercatat di log ini).
- Skor: 7,5 tanpa skill menjadi 8,75 dengan skill.
Verdik gelombang: BELUM — Dengan skill jadwal bertanggal, opt-out `stop`, dan tabel lebih terstruktur; tanpa skill sudah menolak blast dan diskon untuk bintang 5, sehingga selisihnya (+1,25) belum mencapai acuan 1,5.

## FAQ
**Bisa dipakai untuk kirim otomatis ke semua pelanggan?**
Tidak, dan itu disengaja. WhatsApp bisa membatasi nomor yang mengirim pesan massal, dan pelanggan lebih membalas pesan personal. Skill menyiapkan pesan dan daftar kirim harian; Anda yang menekan kirim. Untuk email ke daftar yang sudah setuju, Anda bisa menjadwalkannya sendiri di alat pengirim email seperti listmonk.

**Boleh minta ulasan bintang 5 atau memberi hadiah untuk ulasan?**
Skill tidak menyusun pesan seperti itu. Banyak platform ulasan melarang imbalan dan penyaringan pelanggan yang puas saja, dan ulasan yang tampak dipesan menurunkan kepercayaan. Pesan ulasan di skill ini meminta pengalaman apa adanya, sekali dengan satu pengingat.

**Bagaimana dengan data pelanggan dan aturan perlindungan data?**
Skill hanya menyarankan data minimal (nama panggilan, kanal, tahap, status), mewajibkan pilihan berhenti di tiap pesan, dan menolak daftar nomor beli/bocoran. Ringkasan etika dan dasar hukum ada di `references/etika-dan-hukum.md` (bukan nasihat hukum).

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
