# Pilih Pemasok Paling Untung, Bukan Paling Murah

**Tempel penawaran dari beberapa pemasok, dapatkan total biaya sampai di tempat, pilihan terbaik beserta alasannya, dan pesan WA siap kirim untuk menawar atau menanyakan yang belum jelas.**

Diuji AI penguji independen di OpenClaw: 6,5 → 8,2 dari 10. Pembedanya: tanpa skill, AI sempat menyebut pemasok yang total biayanya lebih mahal sebagai "paling hemat"; dengan skill, setiap selisih ditulis "A lebih murah/mahal Rp… daripada B", ditambah batas ongkir bila ongkir pemasok belum diketahui.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor; langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk hitungan yang tepat; tanpa Python skill tetap berjalan, AI menghitung langsung tetapi angkanya sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tahu uang yang benar-benar keluar**, bukan cuma harga satuan: harga grosir bertingkat, minimal order, isi per dus, ongkir, PPN, dan biaya lain dihitung untuk jumlah yang Anda butuhkan.
- ✅ **Lebih sulit terjebak harga "belum PPN"**: pemasok yang sudah PKP (memungut PPN) dan yang belum dibandingkan setara; bila usaha Anda sendiri PKP, PPN yang bisa dikreditkan ikut diperhitungkan.
- ✅ **Pilihan terbaik dengan alasan jelas**: nilai gabungan biaya, kecepatan kirim, termin bayar (DP/tempo/COD), kualitas, dan fleksibilitas minimal order; bobotnya bisa Anda ubah sesuai prioritas.
- ✅ **Tahu kapan pilihan berubah**: bila jumlah beli jadi 2 kali, bila pemasok termurah telat, bila pesanan dibagi ke dua pemasok, atau bila status PPN pemasok ternyata berbeda.
- ✅ **Data belum lengkap tetap berguna**: bila ongkir belum diketahui, Anda diberi batas ongkir maksimal agar pemasok itu masih tidak lebih mahal (mis. "maksimal Rp700 per kg"), lalu pesan WA untuk menanyakannya.

## Cocok untuk siapa
- Pemilik kafe, resto, toko bahan kue, toko online, konveksi, percetakan, dan usaha yang rutin membeli bahan baku, kemasan, atau barang dagangan.
- Admin pembelian dan staf kantor yang harus menyiapkan perbandingan penawaran untuk atasan.
- Reseller/dropshipper yang memilih pemasok grosir.
- **Bukan untuk:** mencatat stok (`buku-stok`), menentukan kapan pesan ulang (`rencana-restok-barang`), atau membuat penawaran harga ke pelanggan Anda (`surat-penawaran-harga`).

## Contoh sebelum & sesudah
**Sebelum:** tiga balasan WA pemasok terigu untuk 600 kg yang harus tiba dalam 5 hari. Harga PT Mitra Pangan Jaya Rp11.200/kg tampak paling murah per kg, tetapi belum termasuk PPN dan ongkir.

**Sesudah (cukup tempel balasan WA-nya).** Cuplikan dari uji OpenClaw versi 1.0.1, data fiktif (di versi 1.0.2 tabel juga memuat kolom lama kirim dan cara bayar):

```
| Pemasok | Total bayar (per kg) | Selisih vs termurah | Skor (peringkat) |
|---|---|---|---|
| Toko Tepung Sentosa | Rp6.826.000 (Rp11.377) | termurah sementara | 86,5 (1) |
| PT Mitra Pangan Jaya | Rp7.625.700 (Rp12.710) | lebih mahal Rp799.700 (11,7%) | 85,8 (2) |
| CV Berkah Gandum | Rp7.140.000 (Rp11.900) | lebih mahal Rp314.000 (4,6%) | 63,0 (3, telat) |

**Rekomendasi: Toko Tepung Sentosa**
- Toko Tepung Sentosa adalah yang termurah (sementara: status PPN belum jelas): lebih murah Rp314.000 daripada CV Berkah Gandum untuk 600 kg, termurah berikutnya.
- Bila Toko Tepung Sentosa (termurah) telat 7 hari (tiba hari ke-10, melewati tenggat 5 hari): rekomendasi pindah ke PT Mitra Pangan Jaya, yang lebih mahal Rp799.700 (11,7%) daripada Toko Tepung Sentosa.
- Bila Toko Tepung Sentosa ternyata PKP dan harganya belum termasuk PPN: total naik jadi Rp7.576.860; Toko Tepung Sentosa tetap lebih murah Rp48.840 daripada PT Mitra Pangan Jaya, tapi rekomendasi berubah ke PT Mitra Pangan Jaya karena skor gabungannya lebih tinggi (unggul di termin).
```

Disusul risiko, pesan WA ke pemasok (mis. menanyakan status PPN), data yang belum ada, asumsi, dan paling banyak tiga pertanyaan.

## Cara pakai
Tempel penawaran (boleh langsung dari chat WA pemasok) lalu tulis misalnya:
- "Saya butuh 300 pcs dalam 2 minggu. Ini 3 penawaran, mana yang paling untung?"
- "Supplier A PKP harga belum PPN, B non-PKP. Bandingkan untuk 50 kg per minggu."
- "Bandingkan lagi, tapi utamakan pengiriman cepat dan tempo bayar."

Tidak perlu lengkap. Data yang belum ada (misalnya ongkir) ditandai `[isian]`, dan AI bertanya paling banyak tiga hal di akhir. Jawaban pertama dibuat ringkas agar muat satu pesan; balas "rincian" bila ingin melihat hitungan per pemasok. Format rapi (opsional) ada di `templates/format-penawaran.md`.

## Instalasi singkat
Salin folder `bandingkan-pemasok-vendor` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` di dalam paket. Tidak perlu akun, API key, atau instalasi tambahan; hitungan memakai Python standar dan berjalan di komputer Anda.

**Hasil uji (angka nyata):** uji OpenClaw otomatis oleh agent penguji independen, 14 Oktober 2026, versi teruji 1.0.1. Skor 1-10, tanpa skill → dengan skill:
- 3 balasan WA pemasok terigu, 600 kg dalam 5 hari: 6 → 8,5 (di konteks kanal Telegram: 6,5 → 8,5).
- Tabel 4 pemasok kotak kue, 1.000 pcs dalam 7 hari, "yang penting cepat": 6,5 → 8.
- Data tidak lengkap (2 harga gula pasir tanpa jumlah dan lama kirim): 7 → 8.
- Permintaan membuat 2 penawaran pembanding fiktif untuk laporan ke atasan: 6,5 → 8.
- Rata-rata 6,5 → 8,2: lulus acuan internal kami. Skenario tambahan dengan data baru (3 penawaran margarin): 6 → 8, dan 6 → 7,5 di konteks Telegram.

Angka kunci dari uji: terigu Rp11.200/kg yang tampak termurah per kg ternyata termahal setelah PPN dan ongkir, lebih mahal Rp799.700 (11,7%) untuk 600 kg dibanding pilihan termurah. Semua angka hitungan dicocokkan dengan hitung ulang independen. Dibandingkan skill publik sejenis pada skenario yang sama: 6,5 vs 8,5. Riwayat jujur: versi 1.0.0 belum lulus (6,5 → 7,0) karena kalimat selisih tanpa subjek membuat AI menyematkan penghematan ke pemasok yang salah; hal itu diperbaiki di 1.0.1. Rincian dan balasan utuh: `examples/00-openclaw-sebelum-sesudah.md`.

**Status uji (jujur):**
- Diuji otomatis oleh agent di OpenClaw. Versi 1.0.0 belum lulus; versi 1.0.1 lulus.
- Pada skenario tambahan ada dua slip kecil tanpa dampak ke rupiah, peringkat, maupun rekomendasi: salah kutip lama kirim, dan satu skor pemasok yang telat (58,9; seharusnya 64,2) karena termin "DP 30% sisa 30 hari" terbaca tanpa tempo. Pembacaan termin itu diperbaiki di versi 1.0.2, yang belum diuji ulang.
- Versi 1.0.2 sudah dicoba sekali di bot Telegram asli untuk kasus terigu (lihat bagian di bawah); kasus termin DP di atas belum diuji ulang. Belum diuji manusia dan belum melalui program beta. Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).
- Versi 1.0.3 hanya mencocokkan rujukan aturan pajak ke sumber resmi (14 Oktober 2026); hitungannya sama dengan 1.0.2. Yang masih perlu dicek konsultan pajak: ongkir yang hanya dititipkan pemasok ke ekspedisi tanpa tambahan biaya.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 14 Okt 2026) dengan pesan yang sama: tiga balasan WA pemasok terigu, 600 kg, harus tiba dalam 5 hari. Tanpa skill skor **6,5** → dengan skill skor **8** (selisih 1,5, tepat di batas lulus acuan kami). Keduanya memilih Toko Tepung Sentosa (Rp6.826.000) dengan total yang benar. Dengan skill, jawaban muat dalam satu pesan dan menambahkan hal yang terlewat tanpa skill: status PPN Toko Tepung Sentosa belum jelas (bila ternyata kena PPN, totalnya Rp7.576.860, hanya Rp48.840 lebih murah daripada PT Mitra Pangan Jaya), total PT Mitra Pangan Jaya Rp7.625.700 yang sudah memasukkan PPN atas ongkir, akibatnya bila pemasok terlambat, dan pesan WA klarifikasi siap kirim. Semua angka cocok dengan hitung ulang terpisah. Catatan jujur: tanpa skill pun AI sudah menghitung total dengan benar dan memilih pemasok yang sama. Dengan skill, skor gabungan (86,5 vs 85,8, "hampir seri") tampil tanpa penjelasan bobotnya, dan keterangan PPN atas ongkir tidak ikut tertulis; balas "rincian" bila ingin melihat hitungan per pemasok.

## FAQ
**Apakah AI selalu memilihkan pemasok yang paling murah?**
Tidak selalu. Pemasok dengan harga satuan termurah bisa menjadi paling mahal setelah ongkir, PPN, atau minimal order dihitung, atau bisa terlambat dari tanggal yang Anda butuhkan. AI memberi pilihan terbaik menurut prioritas Anda beserta alasannya, dan keputusan tetap di tangan Anda.

**Bisakah AI membuatkan penawaran pembanding supaya pengajuan ke atasan atau tender terlihat lengkap?**
Tidak bisa. Penawaran pembanding harus asli dari pemasok sungguhan, jadi AI menyiapkan pesan permintaan penawaran tertulis ke 2-3 pemasok lalu membandingkan semuanya dengan jujur. Permintaan fee pribadi dari pemasok atau mengambil harga lewat login akun marketplace juga ditolak, tetapi perbandingan dari data asli tetap dikerjakan.

**Apakah perhitungan PPN-nya sama dengan faktur?**
PPN dihitung dengan aturan untuk barang biasa (efektif 11% dari harga sebelum PPN) dan dibulatkan ke bawah, sehingga bisa berbeda beberapa rupiah dengan faktur resmi; bila berbeda, ikuti faktur. Asumsi pajak ditulis terbuka di hasil: ongkir yang ditagih pemasok PKP dianggap ikut kena PPN, PPN hanya bisa dikreditkan bila usaha Anda PKP dan punya faktur pajak sah, dan beberapa bahan pokok (mis. beras, gula pasir, telur) dibebaskan PPN. Untuk kasus Anda, ketiga hal ini sebaiknya dicek ke konsultan pajak.

*Dasar aturan (dicocokkan 14 Okt 2026): ongkir di faktur pemasok PKP termasuk Harga Jual (UU PPN Pasal 1 angka 18); pengkreditan PPN masukan UU PPN Pasal 9 ayat (2b) dan (8) huruf b, faktur pajak sah menurut Pasal 13; pembebasan gula PP 49/2022 Pasal 6 hanya untuk gula kristal putih dari tebu tanpa perasa/pewarna, bukan semua jenis gula.*

> **Catatan penting:** alat bantu keputusan pembelian, bukan nasihat pajak atau hukum. Angka hanya dihitung dari penawaran yang Anda berikan; pastikan harga, PPN, ongkir, dan syarat tertulis di penawaran resmi atau faktur pemasok. Nama usaha di contoh fiktif.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
