# 03 — Toko bangunan ditawari "bunga 0,5% per bulan", KUR Kecil Rp 150 juta akad ke-2

**Skenario:** S3 — pengguna membawa penawaran bank (bunga per bulan, kemungkinan flat), KUR Kecil sektor perdagangan akad kedua. Fiktif.

**Input pengguna (persis):**
> Pak/Bu, toko bangunan saya ditawarin KUR 150 juta 4 tahun, katanya bunganya 0,5% per bulan. Ini KUR kedua saya, yang pertama dulu 50 juta udah lunas. Laba bersih toko rata2 9 juta sebulan. Itu wajar nggak? Buat tambah stok semen & besi.

Perintah:
```bash
python3 scripts/simulasi_kur.py --plafon "Rp 150.000.000" --tenor 48 --kur --sektor perdagangan --akad-ke 2 \
  --penggunaan modal-kerja --bunga "0,5%/bulan" --laba-bersih "Rp 9.000.000"
```

## Output (mengikuti SKILL.md)

## Cek Penawaran KUR — Toko Bangunan
⚠️ Bunga yang dipakai: **0,5% per bulan dari bank = 6% per tahun** (dikonversi ×12). Belum jelas **flat atau efektif** — ini kunci jawabannya.

### 1. Simulasi (Rp 150.000.000, 48 bulan)
| | Jika 6% **efektif** (anuitas) | Jika 6% **flat** |
|---|---:|---:|
| Cicilan/bulan | Rp 3.522.754 | **Rp 3.875.000** |
| Total bunga | Rp 19.092.208 | Rp 36.000.000 |
| Total dibayar | Rp 169.092.208 | Rp 186.000.000 |
| Setara bunga efektif | 6% | **±10,97%/tahun** |

### Apakah wajar?
Pinjaman Rp150 juta = **KUR Kecil** (Pasal 43). Untuk sektor perdagangan non-ekspor, **akad kedua** bunganya **7% efektif/tahun** (Pasal 44) — *catatan: karena KUR pertama Anda Rp 50 juta (KUR Mikro), menurut Pasal 44 ayat (3) huruf b bunga KUR Kecil pertama Anda = bunga KUR Mikro terakhir + 1% = 7%; hasilnya sama.* Pada 7% efektif, cicilan acuan ± **Rp 3.591.937/bulan**, dan bunga flat yang setara hanya **±3,74%/tahun**.
- Kalau 0,5%/bulan itu **efektif** (6%/tahun) → malah di bawah acuan; minta tabel angsuran untuk memastikan.
- Kalau 0,5%/bulan itu **flat** → setara ±10,97% efektif, **jauh di atas** acuan KUR 7%. Tanyakan dasar perhitungannya, minta **tabel angsuran resmi**, dan pastikan ini produk KUR (bukan kredit komersial).

### 2. Kemampuan bayar (laba Rp 9.000.000)
- Skenario efektif: cicilan 39,1% → 🟡 **BERAT**; skenario flat: 43,1% → 🟡 **BERAT**; pada acuan 7%: ±39,9%.
- ⚠️ Agar ≤ 30%: plafon maks ± **Rp 114.966.000** (efektif 6%) atau ± Rp 104.516.000 (bila flat). Pertimbangkan plafon lebih kecil atau stok bertahap.

### Ketentuan lain (Permenko 1/2026)
- ✔ Tenor 48 bulan = batas awal modal kerja KUR Kecil (Pasal 45).
- ✔ **NPWP wajib** untuk KUR Kecil (Pasal 41).
- ℹ️ Plafon > Rp100 juta → bank **boleh** meminta agunan tambahan (Pasal 20 ayat 2); siapkan dokumen agunan bila diminta.
- ℹ️ Sektor perdagangan non-ekspor: akumulasi pinjaman KUR maks Rp500 juta termasuk KUR Mikro (Pasal 43 ayat 3).

### Langkah berikutnya
1. Tanyakan ke bank: "0,5% itu flat atau efektif? Berapa bunga efektif per tahunnya?" dan minta tabel angsuran.
2. Tanyakan rincian biaya (asuransi, materai, notaris); nilai cair harus sama dengan nilai akad (Pasal 13 ayat 2).
3. Cek SLIK OJK sendiri.

Catatan: Simulasi ini bukan penawaran atau jaminan persetujuan kredit. Keputusan & angka final ada di bank. Dasar: Permenko Perekonomian 1/2026 (dicek per 2026-09-23) — konfirmasi ke bank penyalur.

## Catatan penguji
- ✅ Konversi per bulan ×12 + peringatan flat/efektif bekerja; perbandingan dengan acuan 7% muncul otomatis di `cek_ketentuan_kur`.
- ✅ Verifikasi independen: anuitas 6% 3.522.754,36; efektif setara flat 10,975%; anuitas 7% 3.591.936,70; flat setara acuan 3,74%; plafon maks 114.966.858 → 114.966.000 dan 104.516.129 → 104.516.000 — cocok.
- ⚠ `regulasi.md` tidak memuat **Pasal 44 ayat (3)–(4)** (graduasi dari KUR Mikro sektor perdagangan: bunga KUR Kecil = bunga Mikro terakhir + 1%, naik 1% per akad, maks 9%). Catatan graduasi di atas ditambahkan penguji dari teks Permenko; agent lain akan memakai `--akad-ke` apa adanya. Contoh salah: pernah 2× KUR Mikro dagang (6%, 7%) lalu KUR Kecil pertama → script `--akad-ke 1` memberi 6%, seharusnya 8%.
- ⚠ Kategori rasio utama di script dihitung dari kolom anuitas; bila penawaran bank ternyata flat, agent harus memakai baris flat (dilakukan manual di atas).
