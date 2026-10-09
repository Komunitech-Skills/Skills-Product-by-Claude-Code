# Uji 02 — Normal: stock opname Rak A (draf → isi → pratinjau → konfirmasi), 3 selisih

**Server/data:** sama dengan Uji 01 (InvenTree 1.5.6 Docker, data penguji).
**Permintaan:** "Mau stock opname Rak A."

## Langkah 1 — `opname-draf --lokasi "Rak A"`
```
LEMBAR OPNAME Gudang Utama/Rak A: 12 item -> opname-gudang-utama-rak-a-2026-09-29.csv
```
CSV: BOM UTF-8, CRLF, pemisah `;`, desimal koma (`18,5`, `42,5`), 12 baris = 12 item stok Rak A (cocok dengan data penguji).

## Langkah 2 — petugas mengisi (simulasi)
3 selisih: SM-01 batch SMN-2608 60 → **58** (catatan "2 sak sobek dibuang"); KW-01 18,5 → **17,25** kg; CT-05 batch CTW-2609 10 → **11**. 3 sama: SM-02 22, TH-01 17,5, PK-05 42,5. 6 baris dikosongkan.

## Langkah 3 — pratinjau `opname --file opname-rak-a-terisi.csv`
```
PRATINJAU OPNAME dari opname-rak-a-terisi.csv: 6 item dihitung, 6 dilewati (stok_fisik kosong)
- Cat Tembok Putih 5 kg [CT-05] Gudang Utama/Rak A batch CTW-2609: sistem 10, fisik 11 -> LEBIH 1
- Kawat Bendrat [KW-01] Gudang Utama/Rak A: sistem 18,5 kg, fisik 17,25 kg -> KURANG 1,25 kg
- Paku 5 cm [PK-05] ...: sistem 42,5 kg, fisik 42,5 kg -> sama
- Semen Portland 50 kg [SM-01] ... batch SMN-2608: sistem 60 sak, fisik 58 sak -> KURANG 2 sak
- Semen Putih 40 kg [SM-02] ...: sistem 22 sak, fisik 22 sak -> sama
- Thinner 1 L [TH-01] ...: sistem 17,5 L, fisik 17,5 L -> sama
Ringkasan: 3 item selisih, 3 item sama.
Belum disimpan. ...
```
**Tidak ada penulisan:** jumlah semua item Rak A tetap; jumlah entri Stock Tracking tetap 28. ✔

## Langkah 4 — "ya"
- Dengan token `agen-baca` (default): `GALAT: 403 dari InvenTree: akun pemilik token TIDAK PUNYA HAK ... (POST /stock/count/ ...)` exit 5 — pesan Indonesia, tidak mencoba jalan lain. ✔
- Dengan `--kunci-file ...inventree-kunci-gudang.txt --catatan "opname akhir September"`:
```
TERSIMPAN: hasil opname 6 item dicatat di InvenTree (3 item disesuaikan).
Catatan transaksi: Opname 2026-09-29 via Komunitech inventree-gudang: opname akhir September
```

## Verifikasi independen (API admin)
| Item | Sebelum | Sesudah (API) | Tracking |
|---|---|---|---|
| id 1 SM-01 SMN-2608 | 60 | **58** | "Stock counted" {quantity 58} |
| id 12 KW-01 | 18,5 | **17,25** | ✔ |
| id 14 CT-05 CTW-2609 | 10 | **11** | ✔ |
| id 4, 18, 21 (sama) | 22 / 17,5 / 42,5 | tetap | entri "Stock counted" ✔ |
Total tracking 28 → 34 (tepat 6 entri). Tidak ada item lain berubah. ✔

## Uji pengaman tambahan
1. **Lembar lama dikirim ulang** (`--ya` kedua kali dengan lembar yang sama) → `BERHENTI: stok berikut BERUBAH ... (id 14: di lembar 10, sekarang 11; id 12; id 1)`, exit 2, tidak menyimpan. Mencegah double-posting. ✔
2. **Transaksi di sela** (draf baru, lalu 1 kaleng CT-05 id 13 terjual lewat API, lalu `--ya`) → `BERHENTI ... id 13: di lembar 14, sekarang 13`; tracking tetap 35. ✔
3. **Lembar rusak** (fisik −3, "dua puluh", id ganda) → ketiga masalah didaftar sekaligus, "TIDAK ADA yang disimpan", exit 2. ✔

**Temuan (RENDAH):** kolom `catatan` per baris (mis. "2 sak sobek dibuang") tidak ditampilkan di pratinjau dan tidak dikirim ke InvenTree — informasi petugas hilang diam-diam. `stocktake_date` InvenTree hanya diperbarui untuk item yang jumlahnya berubah (id 4/18/21 tetap kosong) walau SKILL.md menulis "semua item dicatat sebagai hasil hitung" — benar untuk riwayat, tidak untuk kolom tanggal opname.

**Hasil: LULUS.**
