# Pilah Inbox, Balas yang Penting Dulu

**Tempel email yang menumpuk, dapatkan urutan kerja, ringkasan, draf balasan siap edit, dan peringatan bila ada yang mirip penipuan.**

Diuji AI penguji independen di OpenClaw: 5,5 → 8,0 dari 10 (email penipuan modus "rekening baru" terdeteksi dengan alasan yang benar, dan draf balasan memakai kolom isian alih-alih mengarang harga atau tanggal).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu email mana yang dibalas dulu.** Tenggat, nominal, klien penting, dan kata "segera" menentukan urutan P1-P3, lengkap dengan alasan pendek.
- ✅ **Ringkasan 1-2 kalimat per email** dan daftar tindakan dengan tenggat, jadi tidak perlu membaca ulang semuanya.
- ✅ **Draf balasan siap edit** yang sopan. Harga, tanggal, dan janji yang belum Anda putuskan ditandai `[isian]`, tidak dikarang.
- ✅ **Peringatan penipuan email (phishing) tanpa membuka tautan:** nama pengirim vs alamat sebenarnya, tautan mencurigakan, permintaan kode rahasia (OTP/PIN), dan modus "ganti rekening baru".
- ✅ **Menjaga privasi:** skill ini sendiri tidak mengirim email ke mana pun (isi email tetap diproses oleh model AI di aplikasi agent Anda, lihat FAQ); rekap untuk tim dirancang tanpa nama lengkap, alamat, rekening, atau angka rahasia.

## Cocok untuk siapa
- Pemilik usaha yang menerima penawaran, tagihan, dan keluhan lewat email.
- Konsultan/freelancer dengan banyak klien.
- Admin kantor yang mengurus tagihan vendor.
- **Bukan untuk:** meringkas grup WhatsApp (skill Ringkas Grup WA, `ringkas-grup-wa`), memilah keluhan marketplace (skill Pilah Keluhan, `triase-keluhan-pelanggan`), atau mengirim/membalas email otomatis dan masuk ke akun email (skill ini tidak melakukannya).

## Contoh sebelum & sesudah
**Sebelum:** 10 email pagi hari. Tagihan Rp7.450.000 jatuh tempo dua hari lagi terbenam di bawah promosi, dan email "rekening kami berganti, mohon transfer ke rekening baru" nyaris dibalas.

**Sesudah (cukup tempel emailnya):** tagihan di urutan teratas, permintaan penawaran Rp18.000.000 berikutnya, dua email dicurigai penipuan dengan alasannya, promosi diarsipkan, draf balasan untuk semua yang perlu dijawab. Cuplikan keluarannya (contoh dengan data fiktif, dari `examples/01-pemilik-usaha-10-email.md`):

```
**Waspada dulu (2 email dicurigai phishing, jangan dibalas atau diklik)**
- **E7 "Mas Agus", rekening baru**: isinya meminta transfer ke rekening baru dan menyebut rekening lama ditutup, dengan tekanan "segera". Ini modus umum penipuan tagihan. Domainnya sama dengan vendor Anda di E3, tetapi akun bisa saja diretas atau dipalsukan. Jangan transfer; telepon Mas Agus ke nomor yang sudah Anda simpan dan tanyakan dulu.
…
**Ringkasan:** 10 email: 2 dicurigai phishing, 3 perlu tindakan hari ini atau besok (P1), 2 perlu balasan (P2-P3), 3 cukup diarsipkan.
| Urut. | Email | Prioritas dan alasan | Ringkasan dan tindakan |
|---|---|---|---|
| 1 | E3 Pak Hendra, tagihan | P1: jatuh tempo 8 Okt (2 hari), Rp7.450.000 | Menagih INV-0417. Cocokkan dengan catatan, konfirmasi atau bayar sebelum 8 Okt (tenggat dari email) |
| 2 | E6 Dina Lestari, komplain | P1: pesanan 6 hari belum sampai, mengancam refund | Cek resi hari ini, kabari Dina siang ini (saran) |
…
E3 (Pak Hendra)
Subjek: Re: Tagihan INV-0417 jatuh tempo
Selamat siang Pak Hendra, terima kasih atas tagihannya. Kami catat invoice INV-0417 sebesar Rp7.450.000, jatuh tempo 8 Oktober 2026. Pembayaran kami jadwalkan [isian: tanggal bayar]; bukti transfer kami kirim setelahnya. Hormat saya, [isian: nama]
```

## Cara pakai
Tempel email (pengirim, subjek, isi), lalu tulis misalnya:
- "Ini 10 email pagi ini. Mana yang duluan? Siapkan balasannya."
- "Email ini asli atau penipuan?"
- "Ringkas 6 email klien ini dan buat daftar tindakan minggu ini."

Tidak perlu lengkap. Yang kurang ditandai `[isian]` dan ditanyakan maksimal tiga hal di akhir. Anda yang membaca dan mengirim balasannya; skill ini tidak masuk ke akun email, tidak membuka tautan, dan tidak mengirim apa pun.

## Instalasi singkat
Salin folder `triase-email-masuk` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` di dalam paket. Python tidak wajib; hanya dipakai bila Anda menyerahkan folder atau CSV (file tabel dari Excel) berisi banyak email.

**Hasil uji (OpenClaw, uji otomatis agent, diuji pada v1.0.0; versi terkini 1.0.1):** rata-rata nilai 5,5 tanpa skill menjadi 8,0 dengan skill (skala 10), dari dua skenario: 10 email campuran (satu penipuan "ganti rekening", satu tagihan bertenggat, dua klien) dan jebakan "balas OK, kirim rekening, klik tautan". Catatan jujur dari uji itu: pada skenario jebakan masih ada janji karangan kecil di draf ("akan proses pembayaran sebelum jatuh tempo"); versi 1.0.1 menambah aturan yang melarang janji seperti itu. Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama). Angka di bagian "Bukti uji di bot Telegram" di bawah berasal dari uji tersendiri (satu skenario dengan topik lain), jadi tidak sama dengan angka ini.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 13, 2026-10-12.
- Tanpa skill: https://t.me/c/4407409583/1101/1186 — skor 7,5
- Dengan skill: https://t.me/c/4407409583/1102/1188 — skor 8
Verdik gelombang: BELUM — Tanpa skill sudah menandai email penipuan dan memberi 5 draf (namun menjanjikan ganti rugi tanpa tanya pemilik); dengan skill memakai isian untuk keputusan pemilik dan 3 pertanyaan di akhir, tetapi selisihnya belum mencapai acuan 1,5.

## FAQ
**Apakah skill ini membaca atau membalas email saya sendiri?**
Tidak. Anda yang menempelkan email, dan Anda yang mengirim balasannya. Tidak ada koneksi ke akun email.

**Seberapa yakin deteksi phishingnya?**
Hanya dugaan dari teks. Email penipuan bisa tampak rapi dan email asli bisa tampak aneh, jadi hasilnya berupa dugaan ("dicurigai") disertai cara verifikasi lewat jalur lain (telepon ke nomor resmi).

**Apakah isi email saya dikirim ke pihak lain?**
Skill ini sendiri tidak mengirim apa pun. Namun email yang Anda tempel diproses oleh model AI di aplikasi agent Anda, jadi ikuti kebijakan privasi aplikasi itu. Samarkan data yang sangat rahasia sebelum menempel.

## Catatan
Bukan nasihat hukum atau keuangan. Karya orisinal Komunitech; merek pihak ketiga hanya disebut sebagai contoh dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan

Versi terkini: **1.0.1**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
