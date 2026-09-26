# Gaji Nggak Numpang Lewat Lagi

**Atur anggaran keluarga, dana darurat, pelunasan utang, dan tabungan untuk DP rumah, sekolah anak, haji, sampai pensiun — dalam Rupiah, dihitung pasti, dengan bahasa sehari-hari.**

## Manfaat
- ✅ **Anggaran bulanan yang pas untuk keluarga Indonesia** — kiriman orang tua, arisan, zakat/perpuluhan/sedekah (opsional), cicilan motor/KPR, THR dibagi 12, dan jebakan top-up e-wallet sudah dipikirkan. Setiap rupiah punya tugas sampai sisa Rp0.
- ✅ **Tahu persis kapan utang lunas** — metode Avalanche (paling hemat) vs Snowball (paling cepat terasa menang), lengkap dengan jadwal per bulan, total bunga, dan selisih biayanya.
- ✅ **Bongkar bunga flat** — leasing "cuma 12% flat" ternyata ±21,6% efektif. Bandingkan pinjaman dengan angka yang jujur.
- ✅ **Alarm bahaya** — cicilan minimum yang tidak menutup bunga, bunga di atas batas OJK/BI (tanda pinjol ilegal), dan larangan tegas gali lubang tutup lubang, plus kontak resmi OJK.
- ✅ **Target jelas per bulan** — "DP rumah 60 juta 5 tahun lagi" → berapa yang harus ditabung tiap bulan, dengan asumsi inflasi tertulis.

## Cocok untuk siapa
- Karyawan & PNS yang gajinya "habis sebelum tanggal tua"
- Pasangan muda yang baru menggabungkan keuangan dan punya anak
- Pekerja lepas, driver ojol, pedagang dengan penghasilan tidak tetap
- Siapa pun yang punya beberapa cicilan (kartu kredit, paylater, KTA, pinjol legal) dan ingin keluar dari utang
- **Bukan untuk:** keuangan usaha (pakai `arus-kas-13minggu` / `laporan-keuangan-emkm`), THR karyawan (`hitung-thr`), atau mencari saran saham/kripto/reksa dana tertentu.

## Contoh sebelum & sesudah
**Sebelum (tanpa skill):** "Coba terapkan 50/30/20 dan lunasi utang berbunga tertinggi dulu." — saran umum, tanpa angka, tanpa memperhitungkan kiriman ortu dan THR, tidak tahu kapan lunas.

**Sesudah:** Keluarga Dimas & Rina (pemasukan Rp10,29 juta termasuk THR ÷ 12, empat utang) mendapat:
- Anggaran lengkap per pos dengan sisa **Rp0**, dibandingkan pola 60/20/20.
- Avalanche: **semua utang lunas bulan ke-15, total bunga Rp3.345.301** — hemat Rp156.108 dibanding Snowball.
- Dana darurat 9 bulan (Rp72,45 juta) tercapai 19 bulan setelah utang lunas.
- 5 langkah konkret minggu ini.
Contoh lengkap: `examples/uji-pembuat-01-keluarga-muda-cicilan.md`.

## Cara pakai
Setelah terpasang, cukup cerita dengan kalimat biasa:
- "Gaji saya 7 juta, istri 3 juta, bantu atur anggaran bulanan."
- "Utang kartu kredit 12 juta dan paylater 3 juta, mana dulu yang dilunasi?"
- "Freelancer, pengeluaran pokok 5 juta, dana darurat berapa?"
- "Mau umrah berdua 4 tahun lagi, nabung berapa sebulan?"

Kalau data kurang, AI bertanya sekali saja. Angka dihitung oleh script Python bawaan (tanpa instalasi tambahan, tanpa internet); kalau script tidak bisa dijalankan, AI memakai rumus tertulis yang sama.

## Instalasi singkat
Salin folder `atur-keuangan-pribadi` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

## FAQ
**Apakah skill ini menyarankan investasi tertentu?**
Tidak. Skill ini tidak pernah merekomendasikan beli/jual saham, kripto, reksa dana, emas, atau produk bank/fintech tertentu. Imbal hasil hanya dipakai sebagai asumsi yang kamu tentukan sendiri.

**Data keuangan saya dikirim ke mana?**
Tidak ke mana-mana oleh skill ini. Script berjalan di komputer kamu, tanpa internet, dan tidak menyimpan file.

**Apakah hasilnya pasti tepat?**
Hitungannya pasti (diuji dengan verifikasi independen), tetapi hasilnya simulasi: bunga bisa berubah, ada denda/biaya admin, dan hidup tidak selalu sesuai rencana. Ini **bukan nasihat keuangan**; untuk kasus rumit, konsultasikan ke perencana keuangan bersertifikat. Aturan OJK/BI dicek 26 September 2026.

**Bunga KTA saya "0,9% per bulan", apakah dihitung benar?**
Ya. Sebutkan satuannya (per bulan/per tahun). Kalau satuannya tidak jelas, AI akan menanyakan dulu — karena 0,9% per bulan flat ternyata setara ±19,5% per tahun efektif, sedangkan 0,9% per tahun hanya ±1,7%.

## Riwayat versi
- **v1.0.2 (2026-09-26)** — perbaikan kecil (angka hitungan tidak berubah): satuan bunga bahasa sehari-hari diterima ("18% setahun", "1,5% sebulan", "1,5 persen per bulan"; kata "flat"/"efektif" dikenali); pos anggaran yang janggal kecil (< Rp10.000, mis. "Makan=1.500") kini diperingatkan; target: bila dana terkumpul sudah cukup untuk harga sekarang, pesan menyebutnya lebih dulu lalu menampilkan kebutuhan setelah inflasi (tidak lagi bertentangan); catatan "bila bunganya FLAT" tidak muncul untuk bunga bertanda efektif; label pos salah dan angka negatif (mis. `--saldo -500rb`) diberi pesan yang jelas dalam bahasa Indonesia.
- **v1.0.1 (2026-09-26)** — satuan bunga wajib jelas (per bulan/per tahun) agar bunga flat KTA tidak salah baca; peringatan angka yang terlalu kecil (mis. "1.500"); target menampilkan "tercapai bulan ke berapa"; catatan menilai tawaran take over/refinancing.
- **v1.0.0 (2026-09-26)** — rilis awal.
