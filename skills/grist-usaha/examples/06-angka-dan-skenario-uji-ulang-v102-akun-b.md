# Uji ulang independen v1.0.2 — Akun B (2026-09-26)

**Penguji:** sesi terpisah (bukan pembuat). Folder skill disalin ke scratchpad
`rt-grist/skill/` dan dijalankan dari sana. Grist asli / Docker tidak dipakai; semua skenario
memakai mode tanpa server (`bersihkan-csv`, baca `.grist` read-only dengan fixture bawaan,
penolakan alamat non-localhost). Ekspektasi angka dihitung sendiri oleh penguji dengan `Decimal`.

## A. Verifikasi temuan U17 (`_bersihkan_angka`)

Semua kasus yang diminta: **BERES**. Hasil bertipe `Decimal`, persis.

| Masukan | Hasil | Ekspektasi penguji | Status |
|---|---|---|---|
| `1,25jt` | 1250000 | 1.250.000 | OK |
| `2,5 rb` | 2500 | 2.500 | OK |
| `Rp 1.250.000,-` | 1250000 | 1.250.000 | OK |
| `10k` | 10000 | 10.000 | OK |
| `1,5M` | 1500000000 | 1,5 miliar | OK |
| `1,2 miliar` / `2 milyar` | 1200000000 / 2000000000 | sama | OK |
| `-Rp 18.500` / `Rp -500rb` | -18500 / -500000 | sama | OK |
| `3 jt 500 rb` | 3500000 | 3.500.000 | OK |
| `1.500rb`, `2m`, `3jt500`, `1.23.456`, `1kg` | None + alasan jelas | ditolak | OK |
| `Rp 12.345.678.901,55` | 12345678901.55 | persis | OK |
| `98765432109876543210` (20 digit) | 98765432109876543210 | persis, tanpa notasi ilmiah | OK |

Konversi kolom: kolom yang sebagian gagal menyebut **baris & nilai & alasan** di layar dan di
`--json` (`kolom_gagal_sebagian`) — terverifikasi di skenario 2 (baris 4: `'1.500rb'`).

## B. 51 variasi tambahan tulisan angka awam (total 68 kasus diuji)

Diterima dan **benar** (dicek dengan Decimal): `1.5jt`=1500000, `Rp.1.000`=1000, `1 juta`,
`Rp 0`=0, `1,000,000` (gaya Inggris)=1000000, `Rp` + spasi tak-putus (U+00A0) `1.000`, spasi
berlebih `  Rp   25.000  `, `1  jt`, `1<TAB>jt`, `IDR 2.500`, `rp 750`, `RP. 5.000,00`=5000,
`1.000.000,50`, `1,000.50`=1000.5, `12,5`, `0,5jt`=500000, `1jt500rb`=1500000,
`1 miliar 250 jt`=1250000000, `2jt 50rb`=2050000, `1,5 M`, `5 Juta`, `2 RB`, `10 K`, `1.5k`=1500,
`- Rp 500`=-500, `-0`=0, `Rp1jt`, `1.000`=1000.

Ditolak **dengan alasan jelas**: `500 rb 3 jt` (urutan naik), `3 jt 1500 rb`, `1,5jt 200rb`,
`1.5m`, `1 T`, `1 triliun`, `1 000 000`, `12.5%`, `100.000.00`, `1.5.2026`, `26/09/2026`, `1e6`,
`Rp 1.250.000,00-`, `1.250,5jt`, `1,250jt`.

Ditolak **tanpa alasan** (dianggap teks biasa; aman, tidak ada angka salah, tapi pengguna hanya
melihat nilainya di peringatan tanpa penjelasan): `(1.000)` (negatif gaya akuntansi), `+500rb`,
`.5jt`, `15rb/pcs`, `500 ribu rupiah`.

Hasil yang saya nilai **bermasalah** (3 dari 68):

1. **[SEDANG] Angka berawalan 0 kehilangan nol di depan, diam-diam.** `08123456789` →
   `8123456789`. Di CSV: kolom `No WA` berisi `081234567890` → jadi **Numeric** `81234567890`;
   kolom `Kode Barang` `007`/`0123` → `7`/`123`. Tidak ada peringatan. Ini bertentangan dengan
   `references/pola-tabel-umkm.md` (Telepon wajib Text "supaya angka 0 di depan tidak hilang") dan
   menyentuh contoh jualan README (daftar pelanggan `0812...`). Rumus `rumus_wa_rapi` kebetulan
   masih menolong untuk WA (`8...` → `628...`), tapi data mentah, kode barang, dan nomor non-WA
   tetap rusak. Saran: kolom yang ada sel angka polos berawalan `0` (dan panjang > 1, tanpa
   pemisah desimal) → biarkan Text + peringatan.
2. **[RENDAH] `1,000` dan `12,345` tanpa singkatan dibaca ribuan (1000, 12345).** Sudah
   terdokumentasi (`1,234` = 1234), tapi tidak konsisten dengan prinsip "ambigu = tolak": dalam
   tulisan Indonesia koma adalah desimal, dan versi bersingkatan (`1,250jt`) justru ditolak.
   Minimal sebut di peringatan; idealnya tolak bila satu-satunya pemisah adalah koma + 3 angka.
3. (bagian dari #2) `12,345` → 12345.

## C. Lima skenario Tahap 6 (ringkas)

| # | Jenis | Perintah & data | Hasil | Nilai |
|---|---|---|---|---|
| 1 | Normal | `bersihkan-csv` rekap warung berpemisah `;` (5 baris: `Rp 18.000`, `15rb`, `Rp 1,25jt`, `2,5jt`, `Rp 3 jt 500 rb`, `3.500.000`, `-Rp 18.000`) | 3 kolom jadi Numeric; semua angka cocok hitungan penguji (216000, 120000, 1250000, 2500000, 3500000, -18000); tanggal & nama tetap Text | LULUS |
| 2 | Normal | `bersihkan-csv` daftar pelanggan (`No WA` 0812…, `Total Belanja` berisi `1.500rb`) | `Total Belanja` tetap Text + peringatan baris 4 beserta alasan (benar). **Tetapi `No WA` kehilangan 0 di depan** (temuan #1) | LULUS dengan catatan |
| 3 | Normal | `daftar-tabel` / `ringkasan Stok` / `ekspor-csv` pada fixture `.grist` | 2 tabel, kolom rumus ditandai, nilai 60/2/0 & AMAN/MENIPIS/HABIS dibaca apa adanya; SHA-1 file tidak berubah setelah dibaca | LULUS |
| 4 | Input tidak lengkap | `ringkasan` tanpa nama tabel; tabel salah `Barang`; pola `gudang`; CSV tidak ada | Pesan jelas, kode keluar 2, daftar tabel/pola yang benar disebutkan | LULUS |
| 5 | Luar cakupan | `GRIST_URL=http://contoh-server.id:8484 cek`; file bukan `.grist`; permintaan tulis SQL | Alamat luar ditolak (kode 2) dengan penjelasan risiko; file palsu ditolak (kode 3); tidak ada jalur tulis ke `.grist` (hanya `PRAGMA query_only = 1`, tanpa INSERT/UPDATE/DELETE di script) | LULUS |

## D. Tes bawaan & validator
- `python3 tests/uji_regresi.py` (dari salinan scratchpad): **84 tes, OK**.
- `python3 scripts/validate.py --skill grist-usaha`: **✅ 1 skill valid, 80 baris katalog sesuai.**

## Skor: 8/10
U17 selesai tuntas dan pembaca angka sekarang jauh lebih teliti (65/68 variasi sesuai
ekspektasi penguji, penolakan disertai alasan). Tertahan di 8 karena temuan SEDANG #1
(nol di depan hilang diam-diam pada nomor WA/kode barang) yang sebaiknya diperbaiki sebelum
`lulus`, dan karena REST API masih hanya diuji terhadap server tiruan.
