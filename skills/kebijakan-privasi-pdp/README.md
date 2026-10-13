# Kebijakan Privasi Sesuai UU PDP, Siap Tempel

**Ceritakan cara usahamu mengelola data pelanggan. Dalam hitungan menit kamu dapat kebijakan privasi, kalimat persetujuan, dan balasan untuk permintaan pelanggan yang mengacu pada UU 27/2022 tentang Pelindungan Data Pribadi.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Kebijakan privasi lengkap** untuk website, toko online, aplikasi, WhatsApp Business, klinik, atau jasa. Bahasa Indonesia, dengan versi Inggris bila perlu.
- ✅ **Kalimat persetujuan siap pakai** untuk formulir website, pesan salam WA, Google Form, dan formulir pasien. Persetujuan dibuat aktif (bukan "dianggap setuju").
- ✅ **Cek kebijakan yang sudah ada**: AI agent membaca seluruh kebijakanmu kalimat demi kalimat dan memeriksanya terhadap 16 kategori risiko, misalnya data dijual atau dibagikan ke mitra, "dianggap setuju", permintaan hapus data ditolak, atau data anak tanpa izin orang tua. Setiap temuan disertai kutipan kalimat, risikonya, dan kalimat pengganti. Setelah itu script menghitung skor kelengkapan 0–100 sebagai pemeriksa kedua.
- ✅ **Siap saat pelanggan minta datanya dihapus.** Ada template balasan akses, koreksi, hapus, dan berhenti promo, lengkap dengan tenggat 3×24 jam.
- ✅ **Checklist darurat kebocoran data**: langkah per jam dan draf pemberitahuan ke pelanggan dan lembaga dalam 3×24 jam.

## Cocok untuk siapa
- Pemilik toko online, penjual marketplace, dan pebisnis yang jualan lewat WhatsApp
- Pemilik website, landing page, atau aplikasi yang mengumpulkan data pengguna
- Klinik, praktik, salon/kecantikan, kursus, travel, dan jasa lain yang mencatat data pelanggan
- Admin, marketing, atau freelancer yang diminta "bikin privacy policy" oleh klien

## Contoh sebelum & sesudah
**Sebelum:** Kebijakan privasi disalin dari website luar negeri. Isinya menyebut GDPR dan "California", ada kalimat "dengan menggunakan situs ini Anda dianggap setuju", dan tidak ada kontak atau masa simpan. Pelanggan tanya "data saya dipakai buat apa?", kamu bingung jawabnya.

**Sesudah (cukup ketik):** "Bikinin kebijakan privasi toko kue online aku, jualan lewat website & WA, pakai kurir, payment gateway, dan Meta Pixel."
→ Kebijakan privasi 12 bagian dengan tabel *data–tujuan–dasar–masa simpan*, bagian penyimpanan di luar negeri yang jujur (WhatsApp/Meta), hak pelanggan dan cara mengajukannya dalam 3×24 jam, pemberitahuan bila terjadi kebocoran, pesan salam WA dengan pilihan "SETUJU PROMO", dan daftar isian yang masih perlu kamu lengkapi. Skor struktur 100/100 (status "BELUM SIAP" sampai isian dilengkapi).

## Cara pakai
Setelah skill terpasang, ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan kebijakan privasi untuk aplikasi booking salon saya"
- "Bikin kalimat persetujuan data untuk Google Form pendaftaran seminar"
- "Cek kebijakan privasi ini, sudah sesuai UU PDP belum?" (tempel teks atau lampirkan file .md/.txt)
- "Pelanggan minta nomornya dihapus dari daftar promo, balasnya gimana?"
- "Akun email toko saya dibobol, data pelanggan mungkin bocor, harus ngapain?"

Bisa juga dipakai tanpa AI: pemeriksa kebijakan bisa dijalankan langsung dengan
`python3 scripts/cek_kebijakan.py kebijakan.md` (Windows: `python` atau `py`). Tidak perlu instal apa pun selain Python.

### Keterbatasan pemeriksa otomatis (baca dulu)
Script `cek_kebijakan.py` adalah **alat bantu**, bukan pemeriksa hukum. Ia hanya mencari kata dan pola tertentu, sehingga:
- Kalimat berisiko yang ditulis dengan kata lain sering **tidak tertangkap**. Pada uji buta oleh penguji independen, script hanya menandai sekitar 4 dari 10 kalimat berisiko, dan pada satu kebijakan klinik berbahasa Inggris tidak menandai satu pun dari 5 risiko.
- Jika script tidak menemukan apa pun, artinya hanya "tidak ada pola yang cocok", **bukan** "kebijakan aman". Script sendiri menampilkan peringatan ini.
- Skor 0–100 mengukur **kelengkapan bagian** (ada/tidaknya kontak, masa simpan, hak pelanggan, dll.), bukan kebenaran isi. Pada teks bahasa Inggris, beberapa bagian bisa terbaca "tidak ada" padahal ada.

Karena itu, di mode cek, AI agent **wajib membaca kebijakanmu sendiri lebih dulu** per kategori risiko, lalu memakai script hanya untuk cek silang. Setiap perbedaan antara keduanya dijelaskan di laporan. Jika kamu memakai script tanpa AI, bacalah kebijakanmu dengan daftar kategori di `references/kategori-risiko-cek.md`. Untuk data kesehatan, anak, atau keuangan dalam jumlah besar, tetap mintalah konsultan hukum meninjau.

## Instalasi singkat
Salin folder `kebijakan-privasi-pdp` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows) ada di `CARA-INSTAL.md` di dalam paket.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 5, 2026-10-03.
- Tanpa skill: https://t.me/c/4407409583/629/643 — skor 5,5
- Dengan skill: https://t.me/c/4407409583/630/645 — skor 8,5
Verdik gelombang: LULUS — DENGAN memuat dasar pemrosesan per tujuan, masa simpan, transfer luar negeri (Ps. 56), kebocoran 3×24 jam (Ps. 46), hak Ps. 5–13, plus Shopify/WhatsApp sebagai penerima; TANPA langsung jadi tetapi menyebut data Meta Pixel "bukan data pribadi" dan melewatkan transfer luar negeri, kebocoran, dan masa simpan.

## FAQ
**Apakah usaha kecil juga wajib punya kebijakan privasi?**
UU PDP berlaku untuk siapa pun yang memproses data pribadi orang lain untuk usaha, termasuk UMKM yang mencatat nomor WA dan alamat pelanggan. Undang-undang ini mewajibkan kamu memberi tahu pelanggan data apa yang dikumpulkan, untuk apa, berapa lama disimpan, dan apa saja hak mereka (Pasal 21). Kebijakan privasi adalah cara paling praktis untuk memenuhinya.

**Apakah hasilnya dijamin sah dan bebas sanksi?**
Tidak ada dokumen yang bisa menjamin itu. Skill ini menyusun draf yang mengacu pada UU 27/2022 (dicek 25 September 2026) dan menandai hal yang belum pasti. Peraturan pelaksananya, PP 33/2026, baru berlaku 16 Januari 2027, dan lembaga pengawas PDP belum terbentuk saat pengecekan. Jika usahamu memproses data kesehatan, anak, atau keuangan dalam jumlah besar, mintalah konsultan hukum meninjau hasilnya.

**Data pelanggan saya aman kalau saya tempel ke AI?**
Untuk menyusun kebijakan, kamu tidak perlu menempel data pelanggan asli. Cukup ceritakan *jenis* datanya. Skill ini juga diinstruksikan untuk tidak menyimpan atau mengirim data yang kamu tempel ke tempat lain.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
