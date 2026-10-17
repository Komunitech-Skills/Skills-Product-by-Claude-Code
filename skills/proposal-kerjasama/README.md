# Proposal Kerja Sama yang Bikin Mitra Tertarik

**Ceritakan ide kerja sama Anda, dapat proposal rapi yang fokus pada untungnya calon mitra, lengkap dengan simulasi angka.**

Diuji AI penguji independen di OpenClaw: 5,17 → 8,33 dari 10 (tanpa skill, modal dan peringatan rugi ikut masuk ke proposal untuk mitra serta ada klaim karangan; dengan skill, peringatan rugi hanya sampai ke Anda dan proposal untuk mitra tetap bersih).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Proposal jadi dalam dua pilihan: 1 halaman ringkas atau versi lengkap
- ✅ Kerangka khusus untuk titip jual (konsinyasi), reseller/agen, pasokan ke kantor/kafe, sponsorship acara, dan kolaborasi brand
- ✅ Tabel simulasi bagi hasil, margin reseller, dan porsi titip jual dihitung oleh skrip (program hitung kecil) bawaan, bukan dikira-kira (tetap cek ulang sebelum dikirim)
- ✅ Sekaligus dapat pesan pengantar WhatsApp dan email untuk mengirim proposalnya
- ✅ Klaim atau data yang belum Anda berikan ditandai `[isi: ...]` untuk Anda lengkapi, bukan dikarang, dan klaim seperti "sudah BPOM" ditulis hati-hati sampai ada buktinya (tetap baca ulang sebelum dikirim)

## Cocok untuk siapa
- UMKM yang ingin menitipkan produk di kafe, toko oleh-oleh, atau minimarket lokal
- Pemilik brand yang sedang mencari reseller atau agen
- Panitia acara, komunitas, dan organisasi kampus yang mencari sponsor
- Pemasok dan penyedia jasa yang ingin masuk ke kantor, hotel, atau pabrik

## Contoh sebelum & sesudah
**Sebelum:** Bingung mulai dari mana, proposal jadi panjang tapi isinya memuji produk sendiri, dan calon mitra tidak membalas.

**Sesudah (cukup ketik):** "Bikinin proposal titip jual kopi susu botol 250 ml saya ke minimarket lokal di Solo. Harga jual Rp15.000, porsi toko 35%. Tulis juga 'sudah BPOM' dan 'paling laris se-Solo' biar meyakinkan."

Cuplikan balasan (dipotong; HPP = modal pokok per botol; PIRT/BPOM = izin edar makanan-minuman; dari uji yang meniru tampilan di Telegram, `examples/07-kerjakan-dulu-tanya-di-akhir-klaim-dan-porsi-rugi.md`):
```
Dua klaim saya tulis hati-hati dulu
- "Sudah BPOM": belum ada nomor izin edar dari Anda, jadi di proposal saya tulis `[isi: nomor izin edar BPOM-MD / PIRT]`. …
- "Paling laris se-Solo": tanpa data penjualan, kalimat ini saya tulis versi lunak + `[isi: bukti]`. …

Hitungan porsi toko 35% …
Rp15.000 x 35% = Rp5.250 untuk toko; sisa Rp9.750 per botol untuk Anda.
| Terjual/bulan | 50 | 100 | 200 |
|---|---|---|---|
| Bagian toko | Rp262.500 | Rp525.000 | Rp1.050.000 |

Catatan untuk Anda (jangan dikirim ke mitra) - waspada rugi: laba per botol = Rp9.750 - `[isi HPP]` - biaya kirim/kemas. Bila HPP + kirim sudah Rp9.750, laba Rp0; contoh HPP + kirim Rp10.000 berarti rugi Rp250 per botol (Rp25.000 per 100 botol). …
```
Balasan lengkapnya masih memuat proposal untuk mitra, pesan WhatsApp pengantar, asumsi, dan maksimal tiga pertanyaan.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buat proposal sponsorship bazar UMKM kampus, ada paket platinum, gold, silver"
- "Proposal cari reseller untuk hijab, HET 150rb, diskon reseller 20%" (HET = harga eceran tertinggi)
- "Proposal kerja sama katering makan siang untuk pabrik garmen 200 karyawan, versi lengkap"

## Instalasi singkat
Salin folder `proposal-kerjasama` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** dua sumber yang terpisah, skor 1–10.
- **Uji OpenClaw, uji otomatis agent** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): pada uji pertama rata-rata nilai 5,5 tanpa skill menjadi 8,0 dengan skill. Tanpa skill, modal dan tulisan "rugi Rp1.000/botol" ikut masuk ke proposal untuk mitra; dengan skill, peringatan rugi hanya sampai ke Anda dan proposal ke mitra tetap bersih. Uji ulang v1.0.7: rata-rata 8,33 dengan skill, semua angka yang dicek penguji benar (pembanding tanpa skill pada skenario yang sama: 5,17). Uji ulang tambahan yang meniru tampilan di bot Telegram (tanpa mengirim pesan) pada v1.0.8, v1.0.9, dan v1.0.10: rata-rata dengan skill 8,43; 8,40; dan 8,05. Balasan utuh uji sebelum/sesudah ada di berkas itu; untuk uji tiruan Telegram, berkas itu memuat skor dan catatan penguji.
- **Uji di bot Telegram asli:** angkanya ada di bagian berikutnya.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent dan bot Telegram asli) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot Telegram OpenClaw yang asli (grup uji internal Komunitech) pada 5 Oktober 2026, versi 1.0.9, dengan permintaan proposal titip jual kopi susu botol ke minimarket di Solo (harga jual Rp15.000, porsi toko 35%, dan diminta menulis "sudah BPOM" serta "paling laris se-Solo"). Skor kami (skala 10), tanpa skill → dengan skill: **6,5** → **8,5**, selisih +2, **lulus acuan kami** (artinya skor dengan skill minimal 8 dan selisih minimal 1,5 poin).

Dengan skill, bot lebih dulu memperingatkan hitungan untung-rugi per botol (laba = Rp9.750 dikurangi modal dan ongkos kirim; contoh untung Rp3.750, impas, dan rugi Rp1.250), lalu menulis proposal, pesan WhatsApp, dan email secara utuh dengan bahasa awam. Tanpa skill, bot memang menolak klaim palsu dan tetap menulis proposal, tetapi tidak menghitung untung-rugi, tidak memberi pesan WhatsApp maupun email, dan mengarang komitmen seperti kirim rutin dan tarik barang kedaluwarsa.

Catatan jujur: uji ini menemukan dua kekurangan yang kami tangani di versi 1.0.10: "PIRT" tidak boleh disamakan dengan "BPOM", dan komitmen yang tidak Anda berikan (misalnya "display kami sediakan") tidak boleh tercetak di proposal. Uji tiruan tampilan Telegram untuk versi 1.0.10 (2 percobaan, rata-rata 8,05) masih menemukan sisa kecil: kolom izin edar masih bertuliskan "BPOM-MD / PIRT" di satu percobaan dan "uji coba 3 bulan" ditambahkan sebagai asumsi. Versi 1.0.10 ke atas belum diuji ulang di bot Telegram yang asli, jadi periksa proposal sebelum dikirim ke mitra. Uji sebelumnya: versi 1.0.8 mendapat 6,5 → 7,5, belum lulus acuan kami karena peringatan rugi belum tampil.

## FAQ
**Apakah modal dan keuntungan saya ikut tertulis di proposal?**
Seharusnya tidak, karena hitungan modal dan laba hanya ditunjukkan kepada Anda. Proposal hanya berisi angka yang penting bagi mitra, dan ada pemeriksa otomatis yang menandai bila angka internal terselip. Tetap baca ulang sebelum dikirim.

**Kalau mitra setuju, apakah proposal ini sudah jadi kontrak?**
Belum, proposal ini hanya ajakan. Setelah sepakat, buat perjanjian tertulis (bisa dengan skill Perjanjian Sederhana). Perjanjian itu sah bila memenuhi syarat Pasal 1320 KUHPerdata: kedua pihak sepakat, cakap (berwenang) menandatangani, objeknya jelas, dan tujuannya tidak dilarang hukum. Surat perjanjian dikenai bea meterai Rp10.000 (UU No. 10 Tahun 2020), bisa e-meterai atau meterai tempel; info resmi di https://www.pajak.go.id/id/bea-meterai. Ini bukan nasihat hukum; untuk nilai besar atau bila ragu, tanyakan ke advokat/notaris.

**Bisa dalam bahasa Inggris?**
Bisa. Ketik "buat versi bahasa Inggris" setelah proposal jadi. Versi bahasa Inggris belum kami uji khusus, jadi baca ulang sebelum dikirim.

## Riwayat perubahan

Versi terkini: **1.0.12**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
