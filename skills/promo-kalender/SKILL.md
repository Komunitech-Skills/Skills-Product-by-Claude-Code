---
name: promo-kalender
description: Menyusun rencana kampanye promo momen belanja Indonesia (gajian, 9.9, 10.10, 11.11, 12.12 Harbolnas, tahun baru, Ramadan-Lebaran, back to school) — mekanisme diskon/flash sale/bundling/voucher/gratis ongkir, target, anggaran, linimasa bertanggal, S&K promo, dengan WAJIB cek margin setelah promo via script (peringatan rugi/tipis). Gunakan saat diminta rencana promo, diskon aman, campaign plan, sale planning. Jadwal konten harian pakai kalender-konten-30hari; biaya marketplace pakai harga-jual-marketplace.
---

# Rencana Promo Momen Belanja

## Tujuan
Membuat rencana promo yang **tetap untung**: mekanisme dipilih berdasarkan hitungan margin (bukan feeling), target dan anggaran jelas, linimasa bertanggal, dan syarat promo jujur sesuai UU Perlindungan Konsumen.

## Kapan digunakan
- "Bikin rencana promo 11.11 buat toko saya", "diskon berapa persen yang aman buat Harbolnas?"
- Merencanakan promo Ramadan/Lebaran, gajian, tahun baru, back to school.
- Mengecek apakah promo yang sudah direncanakan (diskon, bundling, gratis ongkir) masih untung.

## Kapan TIDAK digunakan
- Jadwal posting konten harian/bulanan → `kalender-konten-30hari`.
- Menentukan harga jual normal & menghitung potongan marketplace detail → `harga-jual-marketplace`.
- Menghitung HPP dari bahan → `hitung-hpp` (hasilnya dipakai di sini).
- Menulis naskah live jualan → `naskah-live-jualan`; menulis pesan broadcast → `broadcast-wa`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Momen promo (atau tanggal) | Ya | — (tanyakan; tawarkan momen terdekat dari hari ini) |
| Produk yang dipromokan + harga normal + HPP/modal per unit | Ya | — (tanyakan; HPP belum tahu → tawarkan `hitung-hpp`) |
| Jualan di mana & total % potongan platform | Ya jika marketplace | 0% bila jualan langsung/WA; **jangan mengarang** — minta dari Seller Center |
| Mekanisme yang diinginkan | Tidak | Agent menyimulasikan 2–3 opsi dan merekomendasikan yang labanya terbaik |
| Penjualan normal per periode (unit) | Tidak | Tidak ada pembanding laba "tanpa promo" (sebut) |
| Target unit & anggaran (iklan, materi) | Tidak | Target = kelipatan yang dibutuhkan agar laba sama; anggaran Rp 0 |
| Biaya per pesanan, subsidi ongkir, batas margin aman | Tidak | Rp 0; Rp 0; 10% |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat, pakai default dan tulis asumsinya di bagian akhir.

## Langkah kerja
1. **Tentukan momen & tanggal.** Tanggal kembar/gajian/tahun baru dihitung script. Ramadan, Lebaran, Imlek, awal tahun ajaran berubah tiap tahun → minta tanggal ke pengguna atau pakai perkiraan di `references/momen-promo.md` dengan label **"(perkiraan — cek SKB 3 Menteri/kalender pendidikan)"**.
2. **Pilih 2–3 opsi mekanisme** yang cocok dengan momen & produk (`references/mekanisme-promo.md`). Produk margin tipis → utamakan bundling/hadiah, bukan diskon besar.
3. **WAJIB cek margin tiap opsi** (path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`):
   ```bash
   python3 <folder-skill-ini>/scripts/cek_promo.py margin --produk "Kaos Polos" --harga-normal "Rp 89.000" \
     --hpp 52.000 --diskon-persen 20 --biaya-platform 10 --biaya-per-pesanan 1.250 \
     --target-unit 120 --unit-normal 50 --anggaran 500rb
   # opsi lain: --harga-promo 59.000 | --potongan-rp 5.000 | --bundling "3=Rp 229.000" | --beli-gratis 2+1
   #            --voucher 10.000 --min-belanja 100.000 | --voucher 10% --maks-voucher 15.000
   #            --subsidi-ongkir 10.000 | --cashback 5 | --biaya-lain 2.000 (hadiah) | --bulatkan 1000
   # banyak produk sekaligus (contoh: templates/promo-contoh.json atau .csv):
   python3 <folder-skill-ini>/scripts/cek_promo.py margin --config promo.json
   ```
   - Status **RUGI** → jangan direkomendasikan. Sajikan alternatif yang sudah dihitung ulang (diskon ≤ `diskon maksimal agar tidak rugi`, bundling, hadiah).
   - Status **TIPIS** → hanya untuk produk pemancing berkuota; tulis risikonya.
   - Pakai angka "klaim aman" dari script untuk materi promo (dibulatkan ke bawah).
4. **Buat linimasa bertanggal:**
   ```bash
   python3 <folder-skill-ini>/scripts/cek_promo.py jadwal --momen 11.11
   python3 <folder-skill-ini>/scripts/cek_promo.py jadwal --momen "Lebaran 2027 (perkiraan)" --tanggal 2027-03-10
   ```
   (`--momen gajian --tanggal-gajian 25`, `--dari YYYY-MM-DD` untuk tanggal acuan, `--pola lebaran|panjang|standar`).
5. **Tulis rencana** dengan format di bawah: angka & tabel margin disalin **apa adanya** dari script.
6. **Syarat & ketentuan promo** ditulis jujur: periode & jam, kuota, minimum belanja, produk yang ikut, tidak dapat digabung (jika benar), cara klaim hadiah. Jangan pakai "terlaris", "harga termurah", atau hitung mundur palsu.
7. **Fallback tanpa Python:** hitung manual dengan rumus di bawah, tunjukkan langkahnya, dan tulis "dihitung manual, belum diverifikasi script".

## Rumus (untuk hitung manual)
Per pesanan berisi q unit: K = harga sebelum voucher (harga promo × q, atau harga paket), V = voucher, B = K − V (dibayar pembeli), a = % biaya platform, c = % cashback penjual, O = subsidi ongkir, F = biaya per pesanan, H = HPP per unit, L = biaya promo lain per unit.
```
Laba per pesanan = B − B×a − B×c − O − F − (H + L)×q      Laba per unit = laba ÷ q
Margin           = laba ÷ B
Harga impas/unit = (H + L + (O + F) ÷ q) ÷ (1 − a − c)     Diskon maks. = 1 − harga impas ÷ harga normal
Kelipatan penjualan agar laba sama = laba per unit normal ÷ laba per unit promo
Unit untuk menutup anggaran        = anggaran ÷ laba per unit promo (bulatkan ke atas)
```
Pembulatan: harga promo dari diskon % dibulatkan **ke atas** ke kelipatan Rp 100 (bisa diubah); persen yang diklaim dibulatkan **ke bawah**; tampilan Rupiah ke rupiah terdekat. Contoh: normal Rp 89.000, diskon 25% → Rp 66.750 → Rp 66.800; biaya platform 10% (Rp 6.680), per pesanan Rp 1.250, HPP Rp 52.000 → laba Rp 6.870/unit (margin 10,3%); impas Rp 59.167 → diskon maks. 33,5%.

## Format output
```
# Rencana Promo <momen> — <nama toko>
**Periode:** <tanggal & jam>  |  **Tujuan:** <mis. habiskan stok / tambah pelanggan baru>  |  **Target:** <unit & laba>  |  **Anggaran:** Rp ...

## 1. Produk & mekanisme (hasil cek margin)
| Produk | Mekanisme | Harga efektif/unit | Laba/unit (normal → promo) | Margin promo | Status |
+ rekomendasi & alasan berbasis angka; opsi yang RUGI ditandai ⛔ dan tidak dipakai

## 2. Hitungan kampanye
Target unit, dibayar pembeli, laba sebelum/sesudah anggaran, unit untuk menutup anggaran, kelipatan penjualan agar laba sama.

## 3. Linimasa (dari script)
| Hari | Tanggal | Fase | Kegiatan |

## 4. Materi & kanal
Konten teaser, hari H, pengingat (rujuk skill konten yang relevan), broadcast hanya ke pelanggan yang setuju.

## 5. Kesiapan operasional
Stok per produk, bahan kemasan, jam potong kirim, jadwal admin/CS.

## 6. Syarat & ketentuan promo (siap tempel)

## 7. Ukuran evaluasi (H+7)
Unit, laba bersih, biaya iklan per pesanan, stok sisa, keluhan.

**Asumsi & catatan:** sumber % biaya platform, momen berlabel perkiraan, aturan promo (UU 8/1999), disclaimer.
```

## Contoh
**Input pengguna:** "Mau ikut 11.11. Kaos harga 89 ribu, modal 52 ribu, jual di Shopee potongan totalnya 10% + 1.250 per pesanan. Biasanya laku 50 kaos per minggu. Enaknya diskon berapa?"

**Output (dipersingkat):**
```
| Opsi | Harga efektif/unit | Laba/unit (normal Rp 26.850 →) | Margin | Status |
| Diskon 30% | Rp 62.300 | Rp 2.820 | 4,5% | ⚠️ TIPIS |
| Diskon 20% | Rp 71.200 | Rp 10.830 | 15,2% | ✅ AMAN |
| Bundling 3 = Rp 229.000 | Rp 76.333 | Rp 16.283 | 21,3% | ✅ AMAN |
Rekomendasi: bundling 3 kaos sebagai promo utama + diskon 20% untuk pembelian satuan.
Diskon 20% baru menyamai laba minggu biasa jika terjual ≥ 124 kaos (2,48x lipat).
Diskon maksimal agar tidak rugi: 33,5%.
```

## Checklist sebelum mengirim hasil
- [ ] Setiap mekanisme sudah dicek script; tidak ada rekomendasi berstatus RUGI.
- [ ] % biaya platform berasal dari pengguna, atau dilabel "contoh — cek angka terbaru di Seller Center"; bila 0%, disebut.
- [ ] Tanggal momen yang berubah tiap tahun diberi label perkiraan; linimasa memakai tanggal dari script (nama hari benar).
- [ ] Klaim diskon memakai angka "klaim aman"; harga normal = harga yang benar-benar berlaku sebelumnya.
- [ ] S&K promo lengkap & jujur (periode, kuota, min. belanja); tidak ada undian tanpa catatan izin.
- [ ] Format Rupiah `Rp 1.250.000`; asumsi & disclaimer ada.

## Batasan & penanganan error
- Script keluar kode 2 + `ERROR: ...` untuk angka tidak valid, persen di luar 0–100, dua mekanisme harga sekaligus, format bundling/beli-gratis salah, harga promo di atas harga normal, atau momen yang tanggalnya berubah tanpa `--tanggal`. Jelaskan dan minta angka yang benar.
- Hitungan per unit/pesanan; retur, biaya iklan per klik, dan subsidi dari platform tidak dimodelkan kecuali dimasukkan sebagai biaya.
- Aturan promo & undian: lihat `references/regulasi.md` (berlaku per 23 September 2026). Ini bukan nasihat hukum; untuk undian berhadiah arahkan ke Dinas Sosial/Kemensos.
- Jangan menjanjikan hasil penjualan; target adalah hitungan kebutuhan, bukan ramalan.
