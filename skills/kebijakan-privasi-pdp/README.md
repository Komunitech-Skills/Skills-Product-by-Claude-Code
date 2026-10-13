# Kebijakan Privasi Sesuai UU PDP, Siap Tempel

**Ceritakan cara usaha Anda mengelola data pelanggan. Dalam hitungan menit Anda dapat kebijakan privasi, kalimat persetujuan, dan balasan untuk permintaan pelanggan yang mengacu pada UU 27/2022 tentang Pelindungan Data Pribadi.**

Diuji AI penguji independen di OpenClaw: 5,0 → 9,0 dari 10 (tanpa skill memakai "dianggap setuju", melewatkan klausul kebocoran data dan penyimpanan di luar negeri, serta salah menghitung tenggat; dengan skill ketiganya ditangani).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Kebijakan privasi lengkap** untuk website, toko online, aplikasi, WhatsApp Business, klinik, atau jasa. Bahasa Indonesia, dengan versi Inggris bila perlu.
- ✅ **Kalimat persetujuan siap pakai** untuk formulir website, pesan salam WA, Google Form, dan formulir pasien. Persetujuan dibuat aktif (bukan "dianggap setuju").
- ✅ **Cek kebijakan yang sudah ada**: AI agent membaca seluruh kebijakan Anda kalimat demi kalimat dan memeriksanya terhadap 16 kategori risiko, misalnya data dijual atau dibagikan ke mitra, "dianggap setuju", permintaan hapus data ditolak, atau data anak tanpa izin orang tua. Setiap temuan disertai kutipan kalimat, risikonya, dan kalimat pengganti. Setelah itu program pemeriksa kecil (script) menghitung skor kelengkapan 0–100 sebagai pemeriksa kedua.
- ✅ **Siap saat pelanggan minta datanya dihapus.** Ada template balasan akses, koreksi, hapus, dan berhenti promo, lengkap dengan tenggat 3×24 jam.
- ✅ **Checklist darurat kebocoran data**: langkah per jam dan draf pemberitahuan ke pelanggan dan lembaga dalam 3×24 jam.

## Cocok untuk siapa
- Pemilik toko online, penjual marketplace, dan pebisnis yang jualan lewat WhatsApp
- Pemilik website, landing page, atau aplikasi yang mengumpulkan data pengguna
- Klinik, praktik, salon/kecantikan, kursus, travel, dan jasa lain yang mencatat data pelanggan
- Admin, marketing, atau freelancer yang diminta "bikin privacy policy" oleh klien

## Contoh sebelum & sesudah
**Sebelum:** Kebijakan privasi disalin dari website luar negeri. Isinya menyebut GDPR (aturan data pribadi Uni Eropa) dan "California", ada kalimat "dengan menggunakan situs ini Anda dianggap setuju", dan tidak ada kontak atau masa simpan. Pelanggan tanya "data saya dipakai buat apa?", Anda bingung jawabnya.

**Sesudah (cukup ketik):** "Bikinin kebijakan privasi toko kue online aku, jualan lewat website & WA, pakai kurir, payment gateway, dan Meta Pixel."
(payment gateway = layanan pembayaran online; Meta Pixel = pelacak iklan dari Meta)

Cuplikan hasil (dipotong; contoh dengan data fiktif dari `examples/uji-pembuat-01-toko-kue-susun-dan-cek.md`):
```
# Kebijakan Privasi Dapur Bu Sari
…
## 3. Tujuan, dasar pemrosesan, dan masa simpan
| Data | Untuk apa | Dasar pemrosesan (UU PDP Pasal 20) | Disimpan berapa lama |
| Nama, no. WA, alamat, catatan pesanan | Memproses & mengirim pesanan | Pelaksanaan perjanjian (pesanan Anda) | 10 tahun untuk catatan transaksi (kewajiban pembukuan pajak) |
| Isi chat WhatsApp | Menjawab pertanyaan & keluhan | Pelaksanaan perjanjian / kepentingan yang sah | 1 tahun sejak chat terakhir |
| No. WA | Mengirim info promo | Persetujuan Anda (bisa ditarik kapan saja) | Sampai Anda menarik persetujuan |
…
## 4. Kepada siapa data dibagikan
Kami **tidak menjual** data pribadi Anda. Data hanya kami bagikan seperlunya kepada:
…
## 5. Penyimpanan data di luar negeri
…
```
Hasil lengkapnya: kebijakan 12 bagian, hak pelanggan dan cara mengajukannya dalam 3×24 jam, pemberitahuan bila terjadi kebocoran, pesan salam WA dengan pilihan "SETUJU PROMO", dan daftar isian yang masih perlu Anda lengkapi. Skor struktur 100/100 (status "BELUM SIAP" sampai isian dilengkapi).

## Cara pakai
Setelah skill terpasang, ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan kebijakan privasi untuk aplikasi booking salon saya"
- "Bikin kalimat persetujuan data untuk Google Form pendaftaran seminar"
- "Cek kebijakan privasi ini, sudah sesuai UU PDP belum?" (tempel teks atau lampirkan file teks biasa, berekstensi .md atau .txt)
- "Pelanggan minta nomornya dihapus dari daftar promo, balasnya gimana?"
- "Akun email toko saya dibobol, data pelanggan mungkin bocor, harus ngapain?"

Pemeriksa kebijakan juga bisa dijalankan tanpa AI (caranya ada di bagian Instalasi singkat di bawah).

### Keterbatasan pemeriksa otomatis (baca dulu)
Script `cek_kebijakan.py` adalah **alat bantu**, bukan pemeriksa hukum. Ia hanya mencari kata dan pola tertentu, sehingga:
- Kalimat berisiko yang ditulis dengan kata lain sering **tidak tertangkap**. Pada uji buta oleh penguji independen, script hanya menandai sekitar 4 dari 10 kalimat berisiko, dan pada satu kebijakan klinik berbahasa Inggris tidak menandai satu pun dari 5 risiko.
- Jika script tidak menemukan apa pun, artinya hanya "tidak ada pola yang cocok", **bukan** "kebijakan aman". Script sendiri menampilkan peringatan ini.
- Skor 0–100 mengukur **kelengkapan bagian** (ada/tidaknya kontak, masa simpan, hak pelanggan, dll.), bukan kebenaran isi. Pada teks bahasa Inggris, beberapa bagian bisa terbaca "tidak ada" padahal ada.

Karena itu, di mode cek, AI agent **wajib membaca kebijakan Anda sendiri lebih dulu** per kategori risiko, lalu memakai script hanya untuk cek silang. Setiap perbedaan antara keduanya dijelaskan di laporan. Jika Anda memakai script tanpa AI, bacalah kebijakan Anda dengan daftar kategori di `references/kategori-risiko-cek.md`. Untuk data kesehatan, anak, atau keuangan dalam jumlah besar, tetap mintalah konsultan hukum meninjau.

## Instalasi singkat
Salin folder `kebijakan-privasi-pdp` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

Memakai pemeriksa kebijakan tanpa AI: jalankan `python3 scripts/cek_kebijakan.py kebijakan.md` dari folder skill (Windows: `python` atau `py`). Tidak perlu instal apa pun selain Python.

**Hasil uji (angka nyata):** dua sumber, skor 1–10.
- **Uji OpenClaw otomatis agent, Sep–Okt 2026** (v1.0.7; angka dari `examples/00-openclaw-sebelum-sesudah.md`): tanpa skill **5,0** → dengan skill **9,0** (LULUS). Tanpa skill ada kalimat "dianggap setuju", promo tanpa persetujuan terpisah, tanpa klausul kebocoran dan transfer ke luar negeri, serta salah hitung tenggat (sekitar 34 jam, seharusnya sekitar 10 jam).
- **Uji bot Telegram asli, gelombang 5 (2026-10-03):** **5,5** → **8,5**. Dengan skill memuat dasar UU PDP lengkap (transfer ke luar negeri, kebocoran 3×24 jam, hak pemilik data); tanpa skill promo cukup diberi opsi berhenti (opt-out) dan transfer luar negeri serta kebocoran terlewat.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan bot Telegram asli (gelombang 5). Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Catatan: detail PP 33/2026 berasal dari sumber sekunder dan belum dicek ke naskah resminya.

## FAQ
**Apakah usaha kecil juga wajib punya kebijakan privasi?**
UU PDP berlaku untuk siapa pun yang memproses data pribadi orang lain untuk usaha, termasuk UMKM yang mencatat nomor WA dan alamat pelanggan. Undang-undang ini mewajibkan Anda memberi tahu pelanggan data apa yang dikumpulkan, untuk apa, berapa lama disimpan, dan apa saja hak mereka (Pasal 21). Kebijakan privasi adalah cara paling praktis untuk memenuhinya.

**Apakah hasilnya dijamin sah dan bebas sanksi?**
Tidak ada dokumen yang bisa menjamin itu. Skill ini menyusun draf yang mengacu pada UU 27/2022 (dicek 25 September 2026) dan menandai hal yang belum pasti. Peraturan pelaksananya, PP 33/2026, baru berlaku 16 Januari 2027, dan lembaga pengawas PDP belum terbentuk saat pengecekan. Jika usaha Anda memproses data kesehatan, anak, atau keuangan dalam jumlah besar, mintalah konsultan hukum meninjau hasilnya.

**Data pelanggan saya aman kalau saya tempel ke AI?**
Untuk menyusun kebijakan, Anda tidak perlu menempel data pelanggan asli. Cukup ceritakan *jenis* datanya. Skill ini juga diinstruksikan untuk tidak menyimpan atau mengirim data yang Anda tempel ke tempat lain.

## Riwayat perubahan

Versi terkini: **1.0.8**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
