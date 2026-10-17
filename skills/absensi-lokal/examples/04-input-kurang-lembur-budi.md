# 04 — Input tidak lengkap: "hitung lembur Budi bulan ini"

> **Catatan revisi 1.0.8:** teks rekap di bawah disesuaikan dengan keluaran skrip terbaru (kode karyawan disembunyikan, "kelonggaran telat" menggantikan "toleransi terlambat"). Angkanya tidak berubah dari hasil uji aslinya.

**Skenario:** input tidak lengkap. Database toko dari contoh 01 sudah ada (data Agustus). Hari ini 24/09/2026; file mesin September **belum** diimpor dan belum ada lembur disetujui untuk Budi di September.

## Input pengguna (persis)

> hitung lembur Budi bulan ini

## Output (mengikuti SKILL.md)

Agent menjalankan `rekap --karyawan Budi --json` (baca saja). Hasil script:
```
REKAP ABSENSI SEPTEMBER 2026 (S.D. 24/09/2026) - Toko Maju Jaya (fiktif)
1. Budi - Gudang
   Hadir 0 dari 21 hari kerja | Tanpa keterangan 20
   Terlambat 0x (0 menit) | Pulang cepat 0x (0 menit)
   Jam kerja 0 menit
Hari kerja tanpa absen & tanpa keterangan (mohon dikonfirmasi: izin/sakit/cuti/alpa?):
- Budi: 01/09, 02/09, ... 23/09
```
`lembur_rincian` kosong. Agent **tidak** mengira-ngira lembur dari jam pulang (SKILL.md aturan 5) dan tidak meminta konfirmasi alpa untuk 20 hari (datanya memang belum dimasukkan). Satu pesan:

```
Untuk menghitung lembur Budi bulan September, saya perlu 2 hal:
1. Data absen September belum ada. Kirim file ekspor mesin absen September (CSV/Excel),
   atau sebutkan jam masuk–pulang Budi di hari-hari ia lembur.
2. Lembur mana saja yang Bapak perintahkan/setujui untuk Budi? Tulis tanggal + berapa jam
   + siapa yang menyuruh, mis. "8/9 2 jam, Minggu 13/9 5 jam, disuruh Pak Hendra".
   (Menurut PP 35/2021 Pasal 28, lembur harus ada perintah pengusaha dan persetujuan pekerja,
   jadi saya tidak menghitung lembur otomatis dari jam pulang.)
Gaji Budi sudah tercatat Rp 3.300.000 (tanpa tunjangan tetap), upah sejam = 1/173 x Rp 3.300.000
= Rp 19.075. Kalau gajinya berubah, kabari ya.
```

**Balasan pengguna:** "8/9 2 jam, minggu 13/9 5 jam, disuruh saya sendiri"

→ `lembur --karyawan Budi --tanggal 2026-09-08 --jam 2 --catatan "perintah pemilik"` dan `--tanggal 2026-09-13 --jam 5` (pratinjau):
```
Saya akan mencatat lembur yang DISETUJUI (belum disimpan):
- Budi, Selasa 08/09: 2 jam, hari kerja (Pasal 31 ayat (1)) = 3,5 jam setara ≈ Rp 66.763
- Budi, Minggu 13/09: 5 jam, hari istirahat pola 6 hari (Pasal 31 ayat (2) huruf a) = 10 jam setara ≈ Rp 190.751
Catatan: tanggal-tanggal ini belum ada data absen; setelah disimpan akan muncul peringatan
"lembur tanpa absen" sampai file mesin September dimasukkan.
Simpan? Balas "ya".
```
Setelah "ya" dan rekap: total Budi (3,5 + 10) × 3.300.000 ÷ 173 = 257.514 (13,5 × 19.075,14 = 257.514,45 → Rp 257.514).

## Catatan penguji
- Perilaku sesuai SKILL.md: bertanya **sekali**, daftar singkat bernomor, menyebut dasar Pasal 28, tidak menebak.
- Angka pratinjau dicek dengan rumus manual penguji: 3,5 × 3.300.000 ÷ 173 = 66.763,01; 10 × 3.300.000 ÷ 173 = 190.751,45; total 13,5 × 3.300.000 ÷ 173 = 257.514,45 → Rp 257.514 (dibulatkan sekali, bukan 66.763 + 190.751 = 257.514 — kebetulan sama).
- Kurang: script menampilkan 20 tanggal "mohon dikonfirmasi: izin/sakit/cuti/alpa?" padahal **tidak ada satu pun tap** di periode itu. Agent yang mengikuti SKILL.md langkah D.2 secara harfiah bisa menanyakan 20 tanggal alpa. Script sebaiknya mendeteksi "belum ada data absen sama sekali pada periode ini — sudah impor file mesin?" dan tidak menyarankan konfirmasi alpa.
- Nama tak dikenal (`--karyawan Bambang`) → `GAGAL: Karyawan 'Bambang' tidak dikenal` + daftar karyawan terdaftar: jelas.
