# Uji 01 — HPP & harga jual es kopi susu gula aren

Tanggal uji: 2026-10-01 · OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, sama dengan bot). SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill usaha-offline. Teks balasan disalin utuh, tanpa suntingan.

## Pesan member
> Mau jual es kopi susu gula aren di kedai saya. Per gelas pakai: kopi bubuk 18 gram (beli 1 kg 180.000), susu UHT 120 ml (1 liter 19.500), gula aren cair 25 ml (botol 1 liter 45.000), es batu 500 perak, gelas+tutup+sedotan 1.800. Sewa tempat 1,5jt/bln, gaji 1 barista 2,4jt, listrik 600rb. Sehari laku kira2 40 gelas, buka 26 hari. Modal per gelas berapa? enaknya dijual berapa biar untung tapi ga kemahalan?

## Giliran 1

Alat terpakai — SEBELUM: tidak ada (hitung di kepala model). SESUDAH: baca `hitung-hpp/SKILL.md`, `templates/contoh-hpp.json`, `references/format-input.md`, tulis `es-kopi-gula-aren.json`, jalankan `scripts/hitung_hpp.py`. **Skill benar-benar terpakai.**

### SEBELUM (tanpa skill)
> Oke, saya hitung dari bahan baku + biaya tetap per gelas.
>
> **Biaya bahan (variable cost) per gelas:**
> - Kopi bubuk 18g (180rb/kg → 180/g): Rp 3.240
> - Susu UHT 120ml (19.500/L → 19,5/ml): Rp 2.340
> - Gula aren cair 25ml (45rb/L → 45/ml): Rp 1.125
> - Es batu: Rp 500
> - Gelas+tutup+sedotan: Rp 1.800
> - **Total bahan: Rp 9.005/gelas**
>
> **Biaya tetap bulanan:**
> - Sewa Rp 1.500.000 + gaji barista Rp 2.400.000 + listrik Rp 600.000 = **Rp 4.500.000/bln**
> - Volume jual: 40 gelas × 26 hari = 1.040 gelas/bln
> - Biaya tetap per gelas: 4.500.000 ÷ 1.040 = **Rp 4.327/gelas**
>
> **Modal penuh per gelas = 9.005 + 4.327 ≈ Rp 13.330**
>
> Itu titik impas (balik modal, belum untung). Jadi jual di bawah itu sudah rugi.
>
> **Opsi harga jual + proyeksi untung/bulan (1.040 gelas):**
> - Rp 15.000 → untung ~Rp 1,7 jt/bln (margin tipis, hindari)
> - Rp 17.000 → untung ~Rp 3,8 jt/bln (margin ~21%)
> - **Rp 18.000 → untung ~Rp 4,9 jt/bln (margin ~26%) — saran saya, pas buat kedai kecil/menengah, ga kemahalan**
> - Rp 20.000 → untung ~Rp 6,9 jt/bln (margin ~33%, oke kalau lokasi/branding mendukung)
>
> **Rekomendasi:** jual di **Rp 18.000**. Harga kompetitif untuk es kopi susu gula aren kedai (pasaran umumnya 15rb–22rb), margin sehat ~26%, dan masih ada ruang naik ke 20rb kalau nanti mau tambah promo/varian premium tanpa kelihatan mahal banget. Hindari di bawah Rp 16.000 karena marginnya terlalu tipis buat nutup risiko (bahan naik, gelas sisa, dll).

### SESUDAH (paket skill)
> Modal (HPP) es kopi susu gula aren kamu = **Rp 13.332/gelas**, dari:
>
> | Komponen | Per gelas |
> |---|---:|
> | Kopi bubuk (18 g) | Rp 3.240 |
> | Susu UHT (120 ml) | Rp 2.340 |
> | Gula aren cair (25 ml) | Rp 1.125 |
> | Es batu | Rp 500 |
> | Gelas+tutup+sedotan | Rp 1.800 |
> | Gaji barista (2,4jt/bln ÷ 1.040 gelas) | Rp 2.308 |
> | Sewa (1,5jt/bln ÷ 1.040) | Rp 1.442 |
> | Listrik (600rb/bln ÷ 1.040) | Rp 577 |
> | **Total HPP** | **Rp 13.332** |
>
> *(asumsi laku 40 gelas x 26 hari = 1.040 gelas/bulan — ini penting, lihat catatan di bawah)*
>
> **Pilihan harga jual:**
>
> | Margin | Harga jual | Untung/gelas | BEP/bulan |
> |---|---:|---:|---:|
> | 20% | Rp 17.000 | Rp 3.668 | 563 gelas |
> | 30% | Rp 19.500 | Rp 6.168 | 429 gelas |
> | 40% | Rp 22.500 | Rp 9.168 | 334 gelas |
>
> 💡 **Saran saya: jual di Rp 18.000–19.500.**
> - Di rentang itu margin ~25-30%, masih wajar untuk segmen kedai/warkop (bukan cafe premium), tapi untungnya tetap sehat.
> - BEP cuma ~429-460 gelas/bulan (±16-17 gelas/hari) — jauh di bawah target 40 gelas/hari kamu, jadi ada margin aman kalau sepi.
> - Rp 22.500 (margin 40%) agak riskan buat kedai biasa, kecuali lokasi/brand kamu memang premium.
> - Komponen biaya terbesar bukan bahan (Rp 7.205), tapi gaji+sewa+listrik yang dialokasikan ke tiap gelas (Rp 4.327) — kalau penjualan harian **di bawah** 40 gelas, HPP per gelas naik cukup signifikan karena biaya tetap ini terbagi ke lebih sedikit gelas. Jadi harga 19.000-19.500 kasih buffer kalau omset realisasinya kadang di bawah target.
>
> Catatan: belum termasuk gaji/ambil untung buat kamu sendiri sebagai pemilik, dan belum dikurangi pajak. File perhitungan saya simpan di `es-kopi-gula-aren.json` di workspace kalau mau diubah-ubah lagi (misal ganti target gelas/hari atau margin).

## Verifikasi independen
Dihitung ulang dengan Python (terpisah dari kedua agent):

| Pos | Angka benar |
|---|---:|
| Kopi 18/1000 × 180.000 | 3.240 |
| Susu 120/1000 × 19.500 | 2.340 |
| Gula aren 25/1000 × 45.000 | 1.125 |
| Es + gelas/tutup/sedotan | 500 + 1.800 |
| **Biaya variabel/gelas** | **9.005** (bahan baku saja tanpa kemasan 7.205) |
| Biaya tetap 4.500.000 ÷ 1.040 gelas | 4.326,92 |
| **HPP penuh/gelas** | **13.331,92** |
| BEP pada Rp17.000 / 19.500 / 22.500 | 563 / 429 / 334 gelas/bln (cocok dengan script) |
| BEP pada **Rp18.000** | 4.500.000 ÷ 8.995 = **501 gelas/bln (±19,3/hari)** |

- **SEBELUM:** semua angka benar (HPP ≈13.330, untung/bulan pada 15/17/18/20 ribu = 1,74/3,82/4,86/6,94 jt — cocok). Tidak menghitung BEP.
- **SESUDAH:** tabel dari script benar semua. **Dua kesalahan di narasi model (bukan dari script):**
  1. "BEP cuma ~429-460 gelas/bulan (±16-17 gelas/hari)" untuk rentang Rp18.000–19.500 — untuk Rp18.000 BEP sebenarnya **501 gelas (±19/hari)**. Harga 18.000 tidak ada di tabel script; model mengira-ngira.
  2. "Komponen biaya terbesar bukan bahan (Rp 7.205), tapi gaji+sewa+listrik … (Rp 4.327)" — salah: 7.205 > 4.327 (apalagi bila kemasan dihitung, 9.005).
- Label "margin 30% → Rp19.500" sebenarnya margin efektif 31,6% (dibulatkan ke atas kelipatan Rp500, dijelaskan script; tidak menyesatkan).

## Nilai
| | Ketepatan | Siap pakai | Aturan ID | Keamanan | Kejelasan | **Skor** |
|---|---|---|---|---|---|---|
| SEBELUM | 9 | 8 | n/a | 9 | 8 | **8** |
| SESUDAH | 6 | 9 | n/a | 9 | 8 | **7** |

Alasan: SESUDAH lebih kaya (tabel per komponen, BEP per harga, file resep tersimpan untuk diubah lagi, peringatan bahwa HPP naik bila penjualan < 40 gelas/hari). Tetapi harga yang **disarankan** (18.000) justru dihitung kira-kira dan BEP-nya meleset ±9%, plus satu klaim salah. SEBELUM lebih sederhana tapi semua angkanya benar. Jujur: untuk skenario ini skill **tidak** menang.
