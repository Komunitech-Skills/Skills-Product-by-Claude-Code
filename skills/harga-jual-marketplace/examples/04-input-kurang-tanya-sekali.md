# 04 — Input kurang: biaya platform tidak disebut

**Skenario:** S4 — input tidak lengkap. Biaya admin (wajib) tidak ada; skill dilarang mengarang persentase.

**Input pengguna (persis):**
> Harga jual di Tokopedia buat produk modal 30rb berapa ya biar untung?

## Output (balasan pertama — bertanya sekali)

Bisa! Supaya hitungannya akurat, saya perlu angka dari **Seller Center** kamu (biaya tiap toko bisa beda per kategori dan program):

1. **Biaya admin/komisi** berapa persen untuk kategori produkmu?
2. Ikut program **gratis ongkir/cashback**? Kalau ya, berapa persen dan ada batas maksimumnya?
3. Ada **biaya per pesanan** (biaya proses/layanan tetap)? Berapa rupiah?
4. Mau untung berapa: **persen dari harga jual** (margin) atau **rupiah per barang**? Kalau belum tahu, saya pakai margin 20%.
5. Sudah menyerahkan **surat pernyataan omzet ≤ Rp500 juta** ke Tokopedia? Kalau belum, PPh 22 0,5% ikut saya hitung.

Kalau cuma mau gambaran dulu, saya bisa pakai angka **contoh** (bukan tarif resmi) — hasilnya akan saya beri label jelas.

**Balasan pengguna:**
> admin 6,5%, gratis ongkir 4%, biaya proses 1.000. mau untung 10rb per barang. belum kirim surat pernyataan

**Perintah:**
```bash
python3 <folder-skill>/scripts/harga_marketplace.py --platform "Tokopedia" --modal 30.000 --admin "6,5" --layanan 4 --per-pesanan 1.000 --target-laba 10.000
```

## Output (balasan kedua)

### Tokopedia - target laba Rp 10.000 per barang
- Harga minimal agar tidak rugi: **Rp 34.832**
- Harga tepat sesuai target: Rp 46.068
- **Harga rekomendasi (dibulatkan ke atas kelipatan Rp 500): Rp 46.500**

Rincian pada harga rekomendasi:

| Komponen | Nilai |
|---|---:|
| Harga tayang | Rp 46.500 |
| Biaya admin/komisi (6,5%) | -Rp 3.023 |
| Biaya layanan/program ongkir (4%) | -Rp 1.860 |
| Biaya per pesanan (dibagi 1 barang) | -Rp 1.000 |
| PPh 22 marketplace (0,5%) | -Rp 233 |
| **Uang diterima dari marketplace** | **Rp 40.385** |
| Modal/HPP | -Rp 30.000 |
| **Laba bersih per barang** | **Rp 10.385** |
| Margin (laba / harga setelah voucher) | 22,33% |
| Markup (laba / modal) | 34,62% |

**Catatan & asumsi**
- Persentase biaya platform berasal dari input Anda. Cek angka terbaru di Seller Center masing-masing (berbeda per kategori & program, dan bisa berubah).
- Biaya persen dan PPh 22 dihitung dari harga setelah voucher toko. Jika platform Anda memakai dasar lain, hasil bisa sedikit berbeda.
- Biaya dihitung tanpa pembulatan; angka di tabel dibulatkan ke rupiah terdekat.
- PPh 22 marketplace 0,5% (PMK 37/2025, berlaku 1 Agustus 2026). Penjual orang pribadi dengan omzet setahun s.d. Rp500 juta bisa dikecualikan jika sudah menyampaikan surat pernyataan ke marketplace; hitung ulang dengan --pph22 tidak. PPh 22 ini bukan pajak baru; cara memperhitungkannya dengan PPh final Anda, tanyakan ke DJP/konsultan.
- Berlaku per 2026-09-23. Alat bantu hitung, bukan nasihat pajak.

💡 Saran: pasang **Rp46.500** → untung bersih Rp10.385 per barang. Jangan pasang di bawah **Rp34.832** (rugi). Kalau omzet setahunmu ≤ Rp500 juta, serahkan surat pernyataan ke Tokopedia supaya PPh 22 (Rp233/barang di harga ini) tidak dipotong.

## Catatan penguji
- Bertanya sekali, tepat 5 pertanyaan bernomor, tidak mengarang persentase, menawarkan opsi angka contoh berlabel. Sesuai SKILL.md.
- Angka dicek independen: impas 31.000 ÷ 0,89 = 34.831,5 → Rp34.832; target (31.000 + 10.000) ÷ 0,89 = 46.067,4 → Rp46.068 → Rp46.500. Benar.
- Ringan: baris tabel dibulatkan sendiri-sendiri (3.023 + 233 dari 3.022,50 + 232,50), sehingga jumlah yang terlihat Rp1 berbeda dari "uang diterima". Wajar, tetapi bisa membingungkan pengguna teliti.
