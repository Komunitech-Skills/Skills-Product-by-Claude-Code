# Uji ulang 01 — HPP & harga jual es kopi (hitung-hpp 1.0.3)

Tanggal uji ulang: 2026-10-01 (Asia/Jakarta) · Penguji independen (bukan pembuat skill) · OpenClaw lokal (`openclaw agent --local`), model router Komunitech `ninerouter/komunitech` (jawaban dilayani `claude-sonnet-5`). Home baru `sol2-usaha-offline` (paket skill solusi, dibuat ulang lewat script reset sebelum skenario). Hanya sisi SESUDAH. Pesan member **identik** dengan uji pertama ([01-hpp-harga-jual.md](01-hpp-harga-jual.md)). Balasan disalin utuh tanpa suntingan. Semua angka dihitung ulang penguji dengan Python. Argumen tool call tidak dapat diaudit (hanya nama tool dari JSON keluaran).

## Pesan member
> Mau jual es kopi susu gula aren di kedai saya. Per gelas pakai: kopi bubuk 18 gram (beli 1 kg 180.000), susu UHT 120 ml (1 liter 19.500), gula aren cair 25 ml (botol 1 liter 45.000), es batu 500 perak, gelas+tutup+sedotan 1.800. Sewa tempat 1,5jt/bln, gaji 1 barista 2,4jt, listrik 600rb. Sehari laku kira2 40 gelas, buka 26 hari. Modal per gelas berapa? enaknya dijual berapa biar untung tapi ga kemahalan?

Alat: `read, write, exec` (47 dtk). Agent menulis `es-kopi-susu-gula-aren.json` di workspace dan menjalankan script. Skill terpakai.

## Balasan (utuh)
> **Modal per gelas (HPP): Rp 13.332** (dibulatkan dari Rp 13.331,92)
>
> Rincian:
> - Bahan baku (kopi, susu, gula aren, es batu): Rp 7.205 (54% dari HPP) — komponen terbesar
> - Gelas+tutup+sedotan: Rp 1.800
> - Gaji barista: Rp 2.307,69/gelas (dari Rp 2,4jt ÷ 1.040 gelas/bln)
> - Sewa + listrik: Rp 2.019,23/gelas (dari Rp 2,1jt ÷ 1.040 gelas/bln)
>
> Catatan: ini dihitung dengan asumsi laku 1.040 gelas/bln (40 gelas × 26 hari) persis sesuai target kamu. Kalau realisasi di bawah itu, modal per gelas naik.
>
> **Pilihan harga jual** (laba kotor & titik impas bulanan dari target 1.040 gelas):
>
> - Rp 15.000 → untung Rp 1.668/gelas (margin 11%) — BEP 751 gelas (72% dari target), *terlalu mepet*
> - Rp 17.000 → untung Rp 3.668/gelas (margin 22%) — BEP 563 gelas (54%)
> - Rp 18.000 → untung Rp 4.668/gelas (margin 26%) — BEP 501 gelas (48%)
> - **Rp 19.000 → untung Rp 5.668/gelas (margin 30%) — BEP 450 gelas (43%)** ← cocok untuk pasar kedai/warkop
> - **Rp 20.000 → untung Rp 6.668/gelas (margin 33%) — BEP 409 gelas (39%)** ← harga umum es kopi susu gula aren
> - Rp 22.500 (margin 40%) → untung Rp 9.168/gelas — BEP 334 gelas (32%)
>
> 💡 **Saran:**
> 1. Harga **Rp 18.000–20.000** paling pas: sudah sejalan dengan harga pasaran es kopi susu gula aren kekinian, margin sehat 26–33%, dan BEP cuma 39–48% dari target penjualanmu — ada ruang aman kalau laris kurang dari 40 gelas/hari.
> 2. Kopi bubuk adalah bahan termahal (Rp 3.240/gelas, 24% dari HPP) — kalau mau tekan modal, cek apakah beli kopi 1 kg bisa dapat harga grosir lebih murah.
> 3. Di atas Rp 22.500 sudah masuk margin 40%, tapi mulai mepet dengan harga jajanan kopi sejenis di sekitar — Rp 20.000 biasanya titik tengah paling nyaman buat pelanggan dan kamu.
>
> Kalau mau, bisa langsung aku bantu susun daftar menu dengan harga final & variasi topping/size.

## Verifikasi independen
Penguji menjalankan ulang script skill pada file JSON yang ditulis agent dengan `--banding-harga "15000;17000;18000;19000;20000;22500"` dan menghitung terpisah dengan Python:

| Pos | Benar | Balasan |
|---|---:|---|
| HPP per gelas | 13.331,92 | 13.332 ✔ |
| Bahan baku (tanpa kemasan) / porsi | 7.205 / 54,0% | ✔ "komponen terbesar" ✔ |
| Kopi bubuk / porsi | 3.240 / 24,3% | ✔ |
| Rp15.000: laba / margin / BEP | 1.668 / 11,1% / 751 gelas (72%) | ✔ |
| Rp17.000 | 3.668 / 21,6% / 563 (54%) | ✔ |
| **Rp18.000** | 4.668 / 25,9% / **501** (48%) | ✔ (dulu ditaksir ~429–460) |
| Rp19.000 | 5.668 / 29,8% / **451** (tepatnya 450,23) | ✘ ditulis **450** |
| Rp20.000 | 6.668 / 33,3% / **410** (tepatnya 409,28) | ✘ ditulis **409** |
| Rp22.500 | 9.168 / 40,7% / 334 (32%) | ✔ |

## Penilaian
- **Cacat lama hilang: YA.** (1) BEP harga yang disarankan kini benar: *"Rp 18.000 → … BEP 501 gelas (48%)"*. (2) Klaim biaya terbesar kini benar: *"Bahan baku … Rp 7.205 (54% dari HPP) — komponen terbesar"*.
- **Regresi/temuan baru (kecil):** BEP Rp19.000 dan Rp20.000 ditulis 450 dan 409 (dibulatkan ke bawah). Script mencetak 451 dan 410 (dibulatkan ke atas, karena BEP harus dibulatkan ke atas). Selisih 1 gelas per bulan, tidak mengubah saran. Ini tanda angka dua harga itu tidak disalin dari tabel script. Klaim pasar ("harga umum es kopi susu gula aren", "harga jajanan kopi sejenis di sekitar") tidak bersumber, sama seperti uji pertama.
- **Skor: 8/10** (uji pertama SESUDAH: 7). Saran: di SKILL.md tegaskan BEP dibulatkan ke atas dan setiap harga di daftar wajib diambil dari tabel "Banding harga".
