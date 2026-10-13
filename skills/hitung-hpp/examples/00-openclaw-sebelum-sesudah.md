# Uji OpenClaw SEBELUM vs SESUDAH: hitung-hpp

**Sumber (ada di paket VIP):** `solusi-vip/usaha-offline/UJI-OPENCLAW.md` (tabel skor skenario 01, bagian "Cacat per skill", "Uji ulang 2026-10-01 (keuangan)" dan "putaran 2") dengan rincian per skenario di `solusi-vip/usaha-offline/uji-openclaw/01-hpp-harga-jual.md`, `01-hpp-harga-jual-ulang.md`, dan `01-hpp-harga-jual-ulang2.md`.
**Tanggal uji:** 2026-10-01 (Asia/Jakarta).
**Versi skill saat uji:** uji pertama kira-kira 1.0.2 (disimpulkan dari riwayat `catalog.csv` sebelum perbaikan pasca-uji; berkas sumber tidak menyebut versi), uji ulang 1 = 1.0.3, uji ulang 2 = 1.0.4. Versi di katalog saat ini: 1.0.4.
**Penguji (agent):** agent penguji independen (bukan pembuat skill); tiap uji ulang oleh penguji independen lain.

> Berkas ini ringkasan yang disalin dari catatan uji solusi VIP Usaha Offline (uji dilakukan per solusi, bukan per skill). Angka disalin apa adanya dari sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, satu giliran per panggilan, tanpa Telegram/gateway). Model: router Komunitech `ninerouter/komunitech` (dilayani `claude-sonnet-5`), sama dengan bot member.
- **SEBELUM** = home OpenClaw tanpa skill. **SESUDAH** = home berisi paket skill usaha-offline (24 skill, termasuk `hitung-hpp`). Pesan member identik; data fiktif.
- Uji ulang hanya mengulang sisi SESUDAH dengan pesan yang sama; skor SEBELUM dipakai ulang dari uji pertama.
- Semua angka dihitung ulang penguji dengan Python (HPP penuh Rp13.331,92 per gelas; BEP = biaya tetap ÷ (harga − biaya variabel), dibulatkan ke atas).

**Pesan member (skenario 01):** "Mau jual es kopi susu gula aren di kedai saya. Per gelas pakai: kopi bubuk 18 gram (beli 1 kg 180.000), susu UHT 120 ml (1 liter 19.500), gula aren cair 25 ml (botol 1 liter 45.000), es batu 500 perak, gelas+tutup+sedotan 1.800. Sewa tempat 1,5jt/bln, gaji 1 barista 2,4jt, listrik 600rb. Sehari laku kira2 40 gelas, buka 26 hari. Modal per gelas berapa? enaknya dijual berapa biar untung tapi ga kemahalan?"

## Skor

| Skenario | Versi skill | Skor tanpa skill | Skor dengan skill | Pembeda (satu kalimat) |
|---|---|:-:|:-:|---|
| 01 HPP dan harga jual es kopi, uji pertama | ±1.0.2 | 8 | 7 | Dengan skill: tabel HPP per komponen (Rp13.332 per gelas), BEP per pilihan harga, dan file resep tersimpan, tetapi harga yang disarankan (Rp18.000) tidak ada di tabel script sehingga BEP ditaksir ~429-460 (benar 501 gelas) dan ada klaim salah soal komponen biaya terbesar; tanpa skill semua angkanya benar tetapi tanpa BEP. |
| 01, uji ulang 1 (hanya sisi SESUDAH) | 1.0.3 | 8 (dari uji pertama) | 8 | BEP Rp18.000 kini benar (501 gelas) dan bahan baku (Rp7.205, 54%) disebut komponen terbesar, tetapi BEP Rp19.000 dan Rp20.000 ditulis 450 dan 409 (script: 451 dan 410, selisih 1 gelas). |
| 01, uji ulang 2 (hanya sisi SESUDAH) | 1.0.4 | 8 (dari uji pertama) | 8,5 | Semua BEP sama persis dengan script (Rp18.000 = 501, Rp20.000 = 410, Rp21.000 = 376, Rp22.000 = 347). |
| **Rata-rata skenario ini** (skenario tunggal) | | **8** | **7** (uji pertama) → **8,5** (1.0.4) | Selisih -1 pada uji pertama (tanpa skill menang), +0,5 pada uji ulang terakhir. |

Rata-rata seluruh solusi usaha-offline (5 skenario, skill berbeda) di uji pertama: 7,8 → 7,8. Itu skor solusi, bukan skor skill ini.

## Verdik
**LULUS pada uji ulang 2 (skor 8,5, 1.0.4).** Pada uji pertama, skenario ini dimenangkan sisi SEBELUM (8 vs 7).

## Catatan jujur
- Selisih akhir hanya +0,5 poin; sumber menyimpulkan paket skill "tidak membuat jawaban satu-giliran lebih akurat" untuk model ini. Nilai tambah yang tercatat: tabel BEP per harga yang dihitung script, peringatan HPP naik bila penjualan di bawah target, dan file resep tersimpan yang bisa diubah.
- Skor 8,5 adalah skor sisi SESUDAH setelah skill diperbaiki dari temuan uji pertama; sisi SEBELUM tidak dijalankan ulang.
- Sisa kecil di uji ulang 2: klaim "harga pasar umumnya 18-25rb" tanpa sumber. Harga Rp21.000 tidak ada di `banding_harga` file JSON, tetapi angkanya identik dengan keluaran script (argumen tool call tidak dapat diaudit).
- Satu skenario saja, satu penguji per putaran.
