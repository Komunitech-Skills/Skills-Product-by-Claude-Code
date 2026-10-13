# Rangkaian Pesan ke Pelanggan, Tinggal Salin

**Dari satu kalimat, AI menyiapkan seluruh urutan pesan WhatsApp/Telegram/email lengkap dengan jadwal dan kapan harus berhenti.**

## Manfaat
- ✅ **8 situasi siap pakai:** sambutan pelanggan baru, edukasi sebelum beli, keranjang tertunda, setelah beli, minta ulasan, perpanjangan/langganan, ajak balik pelanggan lama, peluncuran produk baru.
- ✅ **Semua pesan ditulis utuh**, bahasa WA sehari-hari yang sopan, tinggal isi `[nama]` dan salin. Tidak ada saran umum "buatlah pesan yang menarik".
- ✅ **Tanggal kirim dihitung**, bukan dikira: hari Minggu dan hari libur dilewati, dan bila banyak pelanggan, jadwal dibagi per hari supaya nomor WA Anda aman (maks. 10 pesan per hari).
- ✅ **Aman dan sopan:** opt-out "balas stop" di tiap pesan, berhenti begitu pelanggan membalas atau komplain, tanpa urgensi palsu, diskon karangan, atau ulasan palsu.
- ✅ **Cocok dengan cara kerja sehari-hari:** pemilik yang menekan kirim (mode Copilot). OpenClaw hanya bisa mengingatkan Anda di Telegram, tidak mengirim ke pelanggan.

## Cocok untuk siapa
- Pemilik toko online, toko kue, kafe, salon, bengkel, jasa servis, kursus, katering, dan usaha langganan
- Admin/CS yang diminta "bikin follow-up ke pelanggan" dan bingung mulai dari mana
- Pengguna listmonk atau Telegram yang butuh isi urutan pesan
- **Bukan untuk:** kirim massal otomatis ke ratusan nomor, pesan pertama ke calon pelanggan (pakai `pesan-prospek-wa`), prospek yang diam sesudah penawaran (`follow-up-prospek`), atau balas keluhan (`balas-chat-cs`)

## Contoh sebelum & sesudah
**Sebelum:** Pelanggan baru dibiarkan sampai tiba-tiba ditawari promo; keranjang tertunda tidak pernah ditanya; ulasan hanya diminta kalau ingat; pesan promo dikirim sama ke semua orang dan sering diabaikan atau dilaporkan spam.

**Sesudah (cukup ketik):** "Toko kue saya mau bikin pesan sambutan buat pelanggan baru, pelanggan pertama beli Rabu 7 Oktober."
→ Tabel 4 pesan dengan tanggal (7, 10, 17, 28 Oktober), keempat pesan ditulis lengkap dengan "balas stop", aturan kapan berhenti, dan cara kirim dari WA Anda sendiri. Contoh lengkap ada di `examples/`.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.1):** rata-rata nilai 3,0 tanpa skill menjadi 8,25 dengan skill (skala 10). Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa, misalnya:
- "Bikin rangkaian pesan sambutan untuk pelanggan baru toko saya."
- "Pembeli sering tanya-tanya lalu hilang, bikin follow-up-nya."
- "Aku mau minta ulasan Google setelah servis selesai."
- "Buat pengingat perpanjangan langganan, jatuh tempo 20 Desember."

Tidak perlu akun atau API key. Skill hanya menyiapkan pesan dan jadwal; **Anda yang mengirim**, satu per satu. Script jadwal (Python standar) membantu menghitung tanggal, dan skill tetap berguna walau script tidak bisa dijalankan.

## Instalasi singkat
Salin folder `rangkaian-pesan-pelanggan` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 12, 2026-10-12 (tautan pesan tidak tercatat di log ini).
- Skor: 7,5 tanpa skill menjadi 8,75 dengan skill.
Verdik gelombang: BELUM — Dengan skill jadwal bertanggal, opt-out `stop`, dan tabel lebih terstruktur; tanpa skill sudah menolak blast dan diskon untuk bintang 5, sehingga selisihnya (+1,25) belum mencapai acuan 1,5.

## FAQ
**Bisa dipakai untuk kirim otomatis ke semua pelanggan?**
Tidak, dan itu disengaja. WhatsApp bisa membatasi nomor yang mengirim pesan massal, dan pelanggan lebih membalas pesan personal. Skill menyiapkan pesan dan daftar kirim harian; Anda yang menekan kirim. Untuk email ke daftar yang sudah setuju, Anda bisa menjadwalkannya sendiri di alat seperti listmonk.

**Boleh minta ulasan bintang 5 atau memberi hadiah untuk ulasan?**
Skill tidak menyusun pesan seperti itu. Banyak platform ulasan melarang imbalan dan penyaringan pelanggan yang puas saja, dan ulasan yang tampak dipesan menurunkan kepercayaan. Pesan ulasan di skill ini meminta pengalaman apa adanya, sekali dengan satu pengingat.

**Bagaimana dengan data pelanggan dan aturan perlindungan data?**
Skill hanya menyarankan data minimal (nama panggilan, kanal, tahap, status), mewajibkan opt-out di tiap pesan, dan menolak daftar nomor beli/bocoran. Ringkasan etika dan dasar hukum ada di `references/etika-dan-hukum.md` (bukan nasihat hukum).

## Catatan versi
- **1.0.0 (2026-10-06):** rilis awal.
