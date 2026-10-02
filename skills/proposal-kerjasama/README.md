# Proposal Kerja Sama yang Bikin Mitra Tertarik

**Ceritakan ide kerja samamu, dapat proposal rapi yang fokus pada untungnya calon mitra, lengkap dengan simulasi angka.**

## Manfaat
- ✅ Proposal jadi dalam dua pilihan: 1 halaman ringkas atau versi lengkap
- ✅ Kerangka khusus untuk titip jual (konsinyasi), reseller/agen, pasokan ke kantor/kafe, sponsorship acara, dan kolaborasi brand
- ✅ Tabel simulasi bagi hasil, margin reseller, dan porsi titip jual dihitung otomatis, jadi angkanya pasti benar
- ✅ Sekaligus dapat pesan pengantar WhatsApp dan email untuk mengirim proposalnya
- ✅ Tidak mengarang klaim atau data yang tidak kamu berikan

## Cocok untuk siapa
- UMKM yang ingin menitipkan produk di kafe, toko oleh-oleh, atau minimarket lokal
- Pemilik brand yang sedang mencari reseller atau agen
- Panitia acara, komunitas, dan organisasi kampus yang mencari sponsor
- Pemasok dan penyedia jasa yang ingin masuk ke kantor, hotel, atau pabrik

## Contoh sebelum & sesudah
**Sebelum:** Bingung mulai dari mana, proposal jadi panjang tapi isinya memuji produk sendiri, dan calon mitra tidak membalas.

**Sesudah (cukup ketik):** "Bikin proposal titip jual keripik singkong ke 5 cabang Kopi Senja Jogja, harga 25rb, toko dapat 20%"
→ Proposal 1 halaman berisi skema titip jual, tabel pendapatan kafe per bulan (Rp 250.000–Rp 1.000.000 per cabang), tawaran uji coba 3 bulan, plus pesan WA pengantarnya.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buat proposal sponsorship bazar UMKM kampus, ada paket platinum, gold, silver"
- "Proposal cari reseller untuk hijab, HET 150rb, diskon reseller 20%"
- "Proposal kerja sama katering makan siang untuk pabrik garmen 200 karyawan, versi lengkap"

## Instalasi singkat
Salin folder `proposal-kerjasama` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah modal dan keuntungan saya ikut tertulis di proposal?**
Tidak. Hitungan modal dan laba hanya ditunjukkan ke kamu. Proposal hanya berisi angka yang penting bagi mitra.

**Kalau mitra setuju, apakah proposal ini sudah jadi kontrak?**
Belum. Proposal adalah ajakan. Setelah sepakat, buat perjanjian tertulis (bisa dengan skill Perjanjian Sederhana).

**Bisa dalam bahasa Inggris?**
Bisa. Minta saja "buat versi bahasa Inggris" setelah proposal jadi.

## Catatan revisi 1.0.7 (2026-10-01)
- Kota usaha tidak lagi dikarang dari kota mitra: "titip jual ke minimarket di Solo" tidak akan ditulis "kopi susu literan di Solo". Bila kota usaha tidak Anda sebut, ditulis [isi: kota usaha].
- Modal, HPP, laba/rugi, dan titik impas Anda hanya muncul di "Catatan untuk Anda", tidak di proposal, pesan WA, atau email untuk mitra — termasuk saat AI menjelaskan kenapa porsi toko diturunkan.
- `cek_fakta.py --dokumen-mitra` menandai GAGAL bila angka internal bocor ke dokumen untuk mitra; kategori baru `lokasi` menandai kota mitra yang dipakai sebagai kota usaha. Ditambah pola klaim rasa/tekstur dan janji kirim ("besok dikirim").

## Catatan revisi 1.0.6 (2026-10-01)
- Langkah wajib baru: AI menulis dulu "Fakta dari pengguna", lalu setiap klaim di proposal, pesan WA, dan email harus bisa ditelusuri ke daftar itu.
- Script baru `scripts/cek_fakta.py`: klaim turunan ("sudah dikenal di Solo", "tren terus diminati", "favorit pelanggan"), ukuran kemasan karangan ("250ml" untuk produk literan), sifat produk ("rumahan", "tanpa pengawet"), dan angka kredibilitas yang tidak Anda sebut ditandai GAGAL dan wajib diperbaiki. Klaim yang Anda minta tetapi belum ada buktinya wajib diberi [isi: bukti].

## Catatan revisi 1.0.5 (2026-10-01)
- Tidak menambah klaim pemasaran yang tidak Anda berikan (termasuk klaim turunan seperti "dikenal luas").
- Saran porsi bagi hasil/komisi kini dicek dengan hitungan untung-rugi dan titik impas ditampilkan (porsi di titik impas = laba Rp0, tidak disarankan).
- Komitmen default (display, stok awal, isi ulang) dicatat di Asumsi.
