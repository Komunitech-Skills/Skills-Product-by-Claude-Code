# Uji Ulang Independen v1.0.1 — Akun B (2026-09-26)

Penguji: sesi terpisah (bukan pembuat, bukan penguji v1.0.0). Fokus: regresi terhadap temuan v1.0.0
(harga "25.000" terbaca 25; template tanpa opsi batal/refund; hash commit 41 karakter).

## (a) `scripts/hitung_validasi.py` — parsing uang, 31 variasi (≥25 diminta)

Semua nilai dihitung ulang manual dengan `Decimal` (independen dari kode), lalu dibandingkan dengan
output `parse_uang()` sesungguhnya.

| Input | Ekspektasi independen | Hasil aktual | Status |
|---|---|---|---|
| `25.000` | 25000 | 25000 | OK |
| `Rp25.000` | 25000 | 25000 | OK |
| `Rp 25.000,-` | ditolak (titik+koma campur) | ditolak | OK |
| `25rb` | 25000 | 25000 | OK |
| `25 ribu` | 25000 | 25000 | OK |
| `1,5jt` | 1500000 | 1500000 | OK |
| `1.500.000` | 1500000 | 1500000 | OK |
| `12,5` | ditolak (koma tanpa rb/jt, ambigu) | ditolak | OK |
| `25,000` (gaya Inggris) | ditolak (koma tanpa rb/jt) | ditolak | OK |
| `0` | 0 | 0 | OK |
| `-5000` | ditolak (bukan angka dikenali — tanda minus tak didukung) | ditolak | OK |
| `abc` | ditolak | ditolak | OK |
| `25000` | 25000 | 25000 | OK |
| `Rp25000` | 25000 | 25000 | OK |
| `rp.25.000` | 25000 | 25000 | OK |
| `IDR 25000` | 25000 | 25000 | OK |
| `1jt` | 1000000 | 1000000 | OK |
| `1 juta` | 1000000 | 1000000 | OK |
| `2,5rb` | 2500 | 2500 | OK |
| `25.5` | ditolak (ambigu ribuan/desimal) | ditolak | OK |
| `1.234,56` | ditolak (titik+koma campur) | ditolak | OK |
| `100.000.000` | 100000000 | 100000000 | OK |
| `1.00` | ditolak (grup bukan 3 digit) | ditolak | OK |
| `1.0` | ditolak (grup bukan 3 digit) | ditolak | OK |
| `""` (kosong) | ditolak | ditolak | OK |
| `"   "` (spasi) | ditolak | ditolak | OK |
| `25.rb` | ditolak (titik sebelum singkatan tak valid) | ditolak | OK |
| `rb25` | ditolak (singkatan bukan di akhir, sisa bukan digit) | ditolak | OK |
| `25000 ` (spasi trailing) | 25000 | 25000 | OK |
| `12.34.56` | ditolak (grup kedua bukan 3 digit) | ditolak | OK |
| `1.500rb` | 1500000 | 1500000 | OK |

**31/31 cocok dengan ekspektasi independen.** Temuan v1.0.0 ("25.000" terbaca 25) **sudah tidak
terjadi lagi** — sekarang benar dibaca 25000, dan nilai ambigu (`12,5`, `25,000` gaya Inggris,
`25.5`, `1.234,56`, `1.00`) semuanya **ditolak eksplisit**, bukan ditebak. Pesan error konsisten
dan menyebut saran format yang benar.

Uji bawaan repo (`tests/uji_regresi.py`) juga lolos:
```
OK: semua kasus regresi parsing uang Indonesia lolos (14 diterima + 9 ditolak = 23 kasus).
```

## (b) Regresi konversi, margin, balik modal, batas 8%/15%

- Batas atas: `ditawari=100, preorder=15` → konversi 15.0% → **LULUS** (≥15% termasuk LULUS, sesuai dokumentasi).
- Batas bawah bersyarat: `ditawari=100, preorder=8` → konversi 8.0% → **LULUS BERSYARAT** (≥8% termasuk).
- Di bawah batas: `ditawari=100, preorder=7` → konversi 7.0% → **GAGAL**.
- Margin & balik modal (lihat skenario E2E di bawah) dicocokkan manual dengan Decimal — hasil sama persis.

Semua sesuai rumus & ambang yang didokumentasikan di SKILL.md. Tidak ada regresi.

## (c) Template pre-order — opsi batal/refund

`templates/pesan-uji-murah.md` diperiksa: baris pembuka eksplisit mewajibkan setiap template yang
meminta bayar duluan (#1 Broadcast WA, #4 Listing PO marketplace) mencantumkan kebijakan batal/refund
**sejak awal**, bukan opsional.

- Template #1 (WA pre-order): mencantumkan "uang kamu aku kembalikan 100%" jika tidak jadi diproduksi
  atau batal karena alasan lain, **plus** hak pembeli membatalkan kapan saja sebelum produksi mulai
  tanpa alasan, dengan tenggat waktu pengembalian dana yang konkret (`[jumlah hari]`).
- Template #4 (listing PO marketplace): mencantumkan "Kebijakan batal: ... uang kembali 100% paling
  lambat [jumlah hari] hari kerja. Mau batal sebelum masuk produksi? Chat aja, tanpa syarat."

Bahasanya jujur dan jelas (tidak menjanjikan lebih dari yang bisa dipenuhi UMKM kecil — dana
kembali, bukan kompensasi lain). **Temuan v1.0.0 (template tanpa opsi batal/refund) sudah diperbaiki.**

## (d) Hash commit di ATTRIBUTION.md

```
- **Commit yang dipakai:** `1cef1a9eae10017389863d51e289e0ae41e17fcb` ...
```
Panjang hash dihitung dengan `len()` di Python: **40 karakter** (hash SHA-1 git yang valid).
**Temuan v1.0.0 (hash 41 karakter) sudah diperbaiki.**

## (e) Skenario normal ujung-ke-ujung — es kopi literan, harga "35.000"

Perintah:
```
python3 scripts/hitung_validasi.py --ditawari 25 --preorder 5 --harga "35.000" --hpp "15rb" --biaya-uji "40000"
```
Output:
```
=== HASIL VALIDASI IDE ===
Ditawari       : 25 orang/tampilan
Pre-order/beli : 5
Konversi       : 20.0%
Ambang         : LULUS >= 15% | LULUS BERSYARAT >= 8% | GAGAL < 8%
Klasifikasi    : LULUS
Saran          : Datanya cukup mendukung untuk LANJUT...

=== MARGIN & BIAYA UJI ===
Margin per unit      : Rp20.000  (Rp35.000 - Rp15.000)
Total margin preorder: Rp100.000  (20000 x 5 unit)
Biaya uji            : Rp40.000
Selisih              : Rp60.000  (SUDAH balik modal uji)
```
Verifikasi independen (Decimal): konversi = 5/25×100 = 20.0%; margin/unit = 35000−15000 = 20000;
total margin = 20000×5 = 100000; selisih = 100000−40000 = 60000. **Semua cocok persis.** "35.000"
dibaca benar sebagai 35000 (bukan 35 atau 35.000 desimal) — konfirmasi ulang bahwa bug v1.0.0 tidak
kambuh di jalur harga literal yang paling umum dipakai UMKM.

## Ringkasan uji tambahan dijalankan

- `python3 tests/uji_regresi.py` → lolos (23 kasus).
- `python3 scripts/validate.py --skill validasi-ide-produk-baru` (dari root repo) → `✅ 1 skill valid, 87 baris katalog sesuai.`

## Kesimpulan pengujian ini

Ketiga temuan v1.0.0 (parsing "25.000" salah, template tanpa batal/refund, hash 41 karakter) **semua
sudah diperbaiki dan tervalidasi ulang secara independen** dengan bukti kuantitatif di atas.
Tidak ditemukan regresi baru pada konversi/margin/balik modal/ambang 8%/15%.
