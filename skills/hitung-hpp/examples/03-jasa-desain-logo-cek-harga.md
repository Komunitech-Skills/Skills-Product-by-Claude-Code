# 03 — Jasa desain logo: cek tarif saat ini & BEP

**Skenario:** S3 — permintaan normal untuk usaha jasa (1 unit = 1 proyek), dengan penyusutan laptop bernilai sisa.

**Input pengguna (persis):**
> Saya freelance desain logo. Rata-rata 6 jam per proyek, tarif waktu saya anggap 75rb/jam. Langganan software 450rb/bulan, internet 350rb/bulan, laptop 18 juta dipakai 3 tahun, nanti dijual lagi kira-kira 3 juta. Sebulan dapat 8 proyek. Sekarang saya pasang Rp 750.000 per logo. Masih untung? BEP berapa?

**Yang dilakukan agent:**
```bash
python3 <folder-skill>/scripts/hitung_hpp.py --file hpp-logo.json
python3 <folder-skill>/scripts/hitung_hpp.py --file hpp-logo.json --margin 30 --bulatkan 50000   # pembanding
```
<details><summary>Isi hpp-logo.json</summary>

```json
{
  "nama_produk": "Jasa Desain Logo",
  "jenis": "jasa",
  "satuan_produk": "proyek",
  "hasil_per_batch": 1,
  "produksi_per_bulan": 8,
  "tenaga_kerja": [{"nama": "Waktu desain (tarif sendiri)", "upah_per_jam": "75.000", "jam": 6, "per": "unit"}],
  "overhead": [
    {"nama": "Langganan software desain", "biaya": "450.000", "per": "bulan"},
    {"nama": "Internet", "biaya": "350.000", "per": "bulan"}
  ],
  "alat": [{"nama": "Laptop", "harga": "18.000.000", "umur_bulan": 36, "nilai_sisa": "3.000.000"}],
  "harga_jual": "750.000"
}
```
</details>

## Output

## HPP Jasa Desain Logo (per proyek)

Hasil per batch: 1 proyek | Produksi per bulan: 8 proyek

| Kategori | Komponen | Cara hitung | Biaya | Per proyek |
|---|---|---|---:|---:|
| Tenaga kerja | Waktu desain (tarif sendiri) | Rp 75.000/jam x 6 jam | Rp 450.000 /unit | Rp 450.000 |
| Overhead | Langganan software desain | biaya langsung | Rp 450.000 /bulan | Rp 56.250 |
| Overhead | Internet | biaya langsung | Rp 350.000 /bulan | Rp 43.750 |
| Penyusutan alat | Laptop | (Rp 18.000.000 - sisa Rp 3.000.000) / 36 bulan | Rp 416.666,67 /bulan | Rp 52.083,33 |

**Ringkasan HPP per proyek**

- Tenaga kerja: Rp 450.000
- Overhead: Rp 100.000
- Penyusutan alat: Rp 52.083,33
- **HPP per proyek: Rp 602.083,33**
  - biaya variabel Rp 450.000 + biaya tetap dialokasikan Rp 152.083,33

**Harga jual** (dibulatkan ke atas kelipatan Rp 500)

- Harga saat ini Rp 750.000: laba Rp 147.916,67 per proyek (margin 19,72%, markup 24,57%)

**Titik impas (BEP) per bulan** pada harga Rp 750.000

- Biaya tetap bulanan: Rp 1.216.666,67 (biaya bulanan dalam HPP Rp 800.000 + penyusutan Rp 416.666,67 + biaya tetap lain Rp 0)
- Margin kontribusi per proyek: Rp 300.000 (harga - biaya variabel Rp 450.000)
- **BEP: 5 proyek per bulan** (tepatnya 4,06), atau omzet **Rp 3.041.667** per bulan
- BEP = 50,69% dari rencana produksi 8 proyek

**Catatan**
- HPP ditampilkan sampai 2 angka desimal; harga rekomendasi dibulatkan KE ATAS ke kelipatan Rp 500 agar margin tidak kurang dari target.
- Biaya 'per bulan' dan penyusutan dibagi ke produksi per bulan. Jika penjualan lebih sedikit dari itu, HPP per unit sebenarnya naik.
- Margin = laba / harga jual. Markup = laba / HPP. Margin 30% setara markup 42,86%.

**Jawaban singkat:** Masih untung **Rp147.917 per proyek** di atas tarif waktu Anda sendiri (margin 19,72%). Minimal **5 proyek/bulan** supaya software, internet, dan laptop tertutup.

**Margin vs markup:** margin 19,72% = untung dibagi harga jual; markup 24,57% = untung dibagi HPP.

💡 Saran:
- Kalau ingin margin 30%, tarif minimal Rp860.119 → dibulatkan **Rp900.000** per logo (laba Rp297.917, margin 33,1%).
- Biaya tetap Rp1,22 juta/bulan dibagi 8 proyek = Rp152.083/proyek. Kalau bulan sepi (4 proyek), porsinya dua kali lipat — pertimbangkan paket atau retainer.

## Catatan penguji
- Jasa ditangani dengan baik (upah per jam × jam, per unit). Penyusutan (18 jt − 3 jt) ÷ 36 = 416.666,67/bulan → ÷ 8 = 52.083,33/proyek. BEP 1.216.666,67 ÷ 300.000 = 4,06 → 5. Dicek independen.
- Ringan: judul bagian "Harga jual (dibulatkan ke atas kelipatan Rp 500)" tetap tampil walaupun hanya mode cek harga (tidak ada pembulatan).
