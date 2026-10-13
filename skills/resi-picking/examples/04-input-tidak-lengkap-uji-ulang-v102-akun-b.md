# Uji ulang v1.0.2 — Skenario 4: input tidak lengkap (hanya file pesanan minimal)

File fiktif `pesanan-minimal.csv` hanya berisi 4 kolom wajib minimum (`No. Pesanan, Nama Produk,
Nomor Referensi SKU, Jumlah`) — tanpa lokasi rak, tanpa stok, tanpa kurir/resi/status/catatan.

```
python3 scripts/resi.py pesanan-minimal.csv --json
```

## Hasil
- `ok: true`, jalan tanpa error meski banyak kolom opsional tidak ada.
- `pemetaan_lokasi: null`, `pemetaan_stok: null` — sesuai dokumentasi (default: daftar ambil
  diurutkan per SKU saja tanpa rak, tanpa peringatan stok).
- `kurir: {"(tanpa kurir)": 2}` — dikelompokkan wajar sebagai satu grup "(tanpa kurir)", tidak
  crash karena kolom kurir tak ada.
- Peringatan otomatis: "2 pesanan tanpa nomor resi..." dan "Kolom status tidak terdeteksi di file
  ini - SEMUA baris dianggap perlu dikemas..." — keduanya akurat dan actionable, bukan generik.
- Verifikasi independen: MIN001 (GK-AK-01 x5) + MIN002 (GK-AK-02 x3) = **8 pcs**, 2 pesanan aktif,
  2 jenis barang — cocok dengan `total_barang: 8.0` di JSON.

**Hasil: BENAR.** Skill tetap berguna dan jujur soal keterbatasannya saat input minimal, sesuai
prinsip pedoman kurasi Komunitech "instan tapi reliable" (pakai default masuk akal + sebutkan asumsi/keterbatasan).
