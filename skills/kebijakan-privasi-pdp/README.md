# Kebijakan Privasi Sesuai UU PDP, Siap Tempel

**Ceritakan cara usahamu mengelola data pelanggan. Dalam hitungan menit kamu dapat kebijakan privasi, kalimat persetujuan, dan balasan untuk permintaan pelanggan yang mengacu pada UU 27/2022 tentang Pelindungan Data Pribadi.**

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

## FAQ
**Apakah usaha kecil juga wajib punya kebijakan privasi?**
UU PDP berlaku untuk siapa pun yang memproses data pribadi orang lain untuk usaha, termasuk UMKM yang mencatat nomor WA dan alamat pelanggan. Undang-undang ini mewajibkan kamu memberi tahu pelanggan data apa yang dikumpulkan, untuk apa, berapa lama disimpan, dan apa saja hak mereka (Pasal 21). Kebijakan privasi adalah cara paling praktis untuk memenuhinya.

**Apakah hasilnya dijamin sah dan bebas sanksi?**
Tidak ada dokumen yang bisa menjamin itu. Skill ini menyusun draf yang mengacu pada UU 27/2022 (dicek 25 September 2026) dan menandai hal yang belum pasti. Peraturan pelaksananya, PP 33/2026, baru berlaku 16 Januari 2027, dan lembaga pengawas PDP belum terbentuk saat pengecekan. Jika usahamu memproses data kesehatan, anak, atau keuangan dalam jumlah besar, mintalah konsultan hukum meninjau hasilnya.

**Data pelanggan saya aman kalau saya tempel ke AI?**
Untuk menyusun kebijakan, kamu tidak perlu menempel data pelanggan asli. Cukup ceritakan *jenis* datanya. Skill ini juga diinstruksikan untuk tidak menyimpan atau mengirim data yang kamu tempel ke tempat lain.

## Riwayat versi
- **1.0.4 (25 Sep 2026)** — perbaikan kecil dari uji ulang buta v1.0.3 (skor 8/10; alur skill menangkap 21/21 risiko di 3 dokumen buta, script saja 7/21): teks perbaikan K5 (merger/pengambilalihan) kini menyebut pemberitahuan **sebelum dan sesudah** pengalihan (UU PDP Ps. 48); nama layanan asing dicocokkan per kata utuh sehingga "laws", "metadata", "driver" tidak lagi memicu catatan transfer LN palsu; Ps. 2, 47, 48 di `references/dasar-hukum.md` dinaikkan ke ✅ (≥2 sumber sekunder). Tes regresi: 264 uji.
- **1.0.3 (25 Sep 2026)** — revisi dari uji ulang independen ke-3 (`examples/07-uji-ulang-v1.0.2.md`, temuan U3-1): mode cek kini **dibaca agent lebih dulu** terhadap 16 kategori risiko berbasis makna (`references/kategori-risiko-cek.md`, contoh parafrasa ID & EN + dasar pasal), script menjadi pemeriksa kedua, dan setiap selisih dijelaskan. Format laporan: temuan agent per kategori dulu, ringkasan script sesudahnya; dilarang menyimpulkan "tidak ada frasa berisiko" dari script saja. Script tidak lagi mencetak "FRASA BERISIKO: tidak ditemukan", melainkan peringatan bahwa hasil kosong bukan jaminan aman (teks & JSON `pesan_risiko`). Salah-positif "tidak menjual … kepada pihak mana pun" diperbaiki. Pola kata kunci sengaja tidak ditambah. Tes regresi: 255 uji (angka akurasi di tes bawaan berasal dari set yang dipakai menyetel, bukan akurasi nyata).
- **1.0.2 (25 Sep 2026)** — revisi dari uji ulang independen (`examples/06-uji-ulang-v1.0.1.md`, B-1..B-8): pemeriksa kini menandai berbagi data ke mitra iklan/pemasaran/pengiklan dalam Bahasa Indonesia, termasuk di klausa kedua ("tidak menjual data, **tetapi** dapat membagikannya ke mitra iklan", "kecuali kepada mitra pemasaran"); frasa Inggris dengan kata sisipan ("sell or rent aggregated and personal information", "share … with advertisers", "disclose … for advertising"); "bukan tidak mungkin kami menjual", "diam kami anggap setuju", "untuk tujuan apa pun"; batas usia 13 tahun (COPPA) ditandai (anak di Indonesia = di bawah 18 tahun). Salah-positif dikurangi (jam operasional berubah, kata "WhatsApp" tanpa nomor, "keamanan data penting bagi kami", "berlaku untuk layanan kami"). Satu temuan per kalimat, urutan status dijelaskan, kunci JSON seragam. Tes regresi: 239 uji (set penguji 48 frasa + 22 unsur + 3 dokumen, set kontrol baru 48 frasa + 10 unsur).
- **1.0.1 (25 Sep 2026)** — revisi dari temuan penguji independen: pemeriksa `cek_kebijakan.py` kini membaca polaritas kalimat (kalimat patuh "tidak akan dijual" tidak lagi ditandai; "tidak akan memberi tahu bila bocor" ditandai TINGGI dan tidak dihitung sebagai unsur), deteksi frasa jual/sewa/monetisasi data ID & EN diperluas, pola unsur diperluas (server Singapura, "simpan 2 tahun", "mencabut persetujuan", "di bawah 18 tahun"), isian kosong menurunkan skor (status BELUM SIAP), HTML mentah & UTF-16 tanpa BOM terbaca, kinerja linier. Template persetujuan klinik diperbaiki (persetujuan bukan syarat pelayanan) + varian Google Form. Rujukan pasal diperbaiki (Ps. 5 identitas; Ps. 68 denda Rp6 miliar). Tes regresi: 133 uji.
- **1.0.0 (25 Sep 2026)** — rilis draf pertama.
