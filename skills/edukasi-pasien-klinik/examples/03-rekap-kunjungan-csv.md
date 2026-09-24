# 03 — Rekap operasional dari CSV kunjungan berisi data pribadi (skenario normal + uji script)

**Skenario:** Pemilik klinik pratama mengekspor data kunjungan seminggu (180 baris **fiktif**, dibuat penguji) dari aplikasi pendaftaran. File masih memuat kolom sensitif: `Nama Pasien`, `NIK`, `No HP`, `Diagnosis`.

**Input pengguna (persis):**
> rekapin dong kunjungan minggu kemarin dari file kunjungan_normal.csv, per hari, per poli, bpjs vs umum, jam rame, sama yg ga dateng berapa

Contoh isi file (semua data fiktif):
```
Tanggal,Jam,Nama Pasien,NIK,No HP,Poli,Penjamin,Diagnosis,Status
2026-09-14,17:58,FIKTIF Eko 000,9999000000000000,0812-0000-0000,Gigi,BPJS,E11 DM tipe 2,Batal
2026-09-20,18:52,FIKTIF Andi 001,9999000000000001,0812-0000-0001,Umum,BPJS,A90 DBD,Selesai
... (180 baris, 14–20 September 2026)
```

Perintah yang dijalankan agent:
```
python3 scripts/rekap_kunjungan.py --file kunjungan_normal.csv
```

Keluaran script (persis):
```
REKAP OPERASIONAL KUNJUNGAN (agregat, tanpa nama/diagnosis)
Total baris data: 180

Kunjungan per hari:
  2026-09-14: 26
  2026-09-15: 23
  2026-09-16: 29
  2026-09-17: 32
  2026-09-18: 22
  2026-09-19: 18
  2026-09-20: 30

Kunjungan per poli/layanan:
  Umum: 88
  Gigi: 60
  KIA: 32

Kunjungan per penjamin/cara bayar:
  BPJS: 111
  Asuransi: 35
  Umum: 34

Jam paling ramai (top 3):
  08:00: 37 kunjungan
  09:00: 34 kunjungan
  10:00: 21 kunjungan

Perkiraan pasien tidak datang/batal: 36

Catatan privasi: kolom berikut TIDAK dibaca isinya dan diabaikan demi kerahasiaan data pasien (UU PDP 27/2022): Diagnosis, NIK, Nama Pasien, No HP

Catatan: ini rekap operasional (jumlah), bukan rekam medis, bukan alat skrining/diagnosis, dan tidak menampilkan data per-pasien.
```

---

## Output (dirapikan ke `templates/rekap-operasional.md`)

```
📊 Rekap Operasional — [Nama Klinik]
Periode: 14 – 20 September 2026

Total pendaftaran tercatat: 180
(termasuk 36 yang tidak datang/batal → yang hadir ±144)

Per hari:
- Sen 14/9: 26
- Sel 15/9: 23
- Rab 16/9: 29
- Kam 17/9: 32  ← paling ramai
- Jum 18/9: 22
- Sab 19/9: 18
- Min 20/9: 30

Per poli/layanan:
- Umum: 88 (48,9% dari total)
- Gigi: 60 (33,3%)
- KIA: 32 (17,8%)

Per penjamin:
- BPJS: 111 (61,7%)
- Asuransi: 35 (19,4%)
- Umum: 34 (18,9%)

Jam paling ramai: 08.00–09.00 (37), 09.00–10.00 (34), 10.00–11.00 (21)

Pasien tidak datang/batal: 36 (20,0% dari total pendaftaran)

Catatan: rekap ini bersifat agregat (jumlah), tidak memuat nama/NIK/no HP/diagnosis pasien.
Kolom Nama Pasien, NIK, No HP, dan Diagnosis di file Anda tidak dibaca.
```
*(Persentase dihitung agent dari angka script. Angka per poli/penjamin masih termasuk pasien yang tidak datang.)*

---

## Verifikasi independen (penguji)
Script verifikasi terpisah (`verif.py`, Python standar, tidak memakai kode skill) menghitung ulang dari CSV mentah:
- total 180; per hari {14: 26, 15: 23, 16: 29, 17: 32, 18: 22, 19: 18, 20: 30}; poli Umum 88 / Gigi 60 / KIA 32; penjamin BPJS 111 / Asuransi 35 / Umum 34; jam teratas 08 (37), 09 (34), 10 (21); tidak datang/batal 36 (20,0%) → **SEMUA COCOK**.
- Cek kebocoran: 180 nama, 180 NIK, 180 no HP, dan 6 kode/teks diagnosis dicari di keluaran teks & JSON → **0 kebocoran**.
- `tests/test_rekap_kunjungan.py`: 9 tes **OK**.

## Uji data rusak / tepi

| Kasus | Hasil | Penilaian |
|---|---|---|
| Header sensitif bervariasi: `Nama Pasien`, `No. RM`, `Dx`, `ICD-10`, `Keluhan Utama`, `HP/WA` (+ pemisah `;`) | Isi semua kolom itu **tidak bocor** (0 temuan), karena script hanya membaca kolom yang dikenal. Tapi catatan privasi hanya menyebut `Nama Pasien, No. RM`, sedangkan `Dx`, `ICD-10`, `Keluhan Utama`, `HP/WA` tidak disebut | Aman; pemberitahuan kurang lengkap (RINGAN) |
| Status `Tidak hadir` | **Tidak dihitung** sebagai tidak datang: script melaporkan 2, seharusnya 3 | **Angka salah tanpa peringatan** (BERAT) |
| Tanggal campur `01/09/2026`, `2026-09-01`, `02-09-2026`, kosong | Terbaca; baris kosong diberi peringatan | ✅ |
| Tanggal + jam di kolom tanggal (`2026-09-02 08:45`, `2026-09-01T10:00:00`) | **Semua baris gagal terbaca** (ada peringatan) | SEDANG (format ekspor SIMRS yang umum) |
| Nama bulan (`2 Sept 2026`, `1 September 2026`, `1-Sep-2026`), serial Excel `46266` | Gagal terbaca (ada peringatan) | SEDANG |
| Format AS campur (`09/12/2026`, `09/13/2026`) | 09/12 dibaca 9 Desember, 09/13 dibaca 13 September. **Dua tafsiran berbeda dalam satu file, tanpa peringatan** | BERAT (bagian dari cacat "angka salah diam-diam") |
| File cp1252 (ada huruf `é`) | **Crash dengan traceback Python** (`UnicodeDecodeError`) | SEDANG |
| File UTF-16 (ekspor Excel "Unicode Text") | **Crash dengan traceback** | SEDANG |
| File kosong / hanya header / tanpa kolom tanggal / file tidak ada | Pesan error jelas, exit 1 | ✅ |
| Kolom `Layanan` diisi teks bebas berisi nama (`Cabut gigi FIKTIF Ani`) | Nama **ikut tampil** di rekap per poli | RINGAN (salah input pengguna; perlu peringatan) |

## Catatan penguji
- ✅ Desain privasi bagus: script memakai *whitelist*, jadi hanya kolom agregat yang dibaca. Kolom sensitif dengan nama apa pun tidak bocor.
- ❌ Angka bisa salah **tanpa peringatan** untuk data Indonesia yang umum (`Tidak hadir`, format tanggal campur). Detail & saran perbaikan ada di HASIL-UJI.
- ⚠️ Template meminta persentase, tapi script tidak menghitungnya. Agent harus menghitung sendiri, padahal prinsip library: angka dihitung lewat script. "Total" juga masih termasuk pasien yang tidak datang, sehingga mudah dibaca sebagai "180 kunjungan".
