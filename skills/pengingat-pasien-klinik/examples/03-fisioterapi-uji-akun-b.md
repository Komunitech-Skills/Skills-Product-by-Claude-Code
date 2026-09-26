# Uji independen Akun B — Skenario 3 (normal): fisioterapi, sesi lanjutan

Hari acuan: 26 September 2026. Menguji kategori TERLAMBAT dan HARI INI sekaligus, plus
verifikasi independen batas H-1/H-3/terlambat.

## Perintah & keluaran nyata
```
tambah --nama "Pak Joko" --wa 0814-4444-5555 --jenis fisioterapi --tanggal "hari ini" --persetujuan ya
tambah --nama "Bu Wulan" --wa 0815-6666-7777 --jenis fisioterapi --tanggal 2026-09-20 --persetujuan ya
daftar
```
```
{"kelompok": {"terlambat": 1, "hari_ini": 1, "h1": 0, "h3": 0},
 "teks": "TERLAMBAT (1)\n  #3 Bu Wulan | Fisioterapi | 20 Sep 2026 | 0815-6666-7777\n
          HARI INI (1)\n  #2 Pak Joko | Fisioterapi | 26 Sep 2026 | 0814-4444-5555\n\n
          DRAF PESAN (salin & kirim sendiri, JANGAN dikirim otomatis): ..."}
```

## Verifikasi independen batas kategori (Python `datetime`, dihitung terpisah dari skill)
```python
from datetime import date, timedelta
acuan = date(2026, 9, 26)
kasus = {
  -6: "terlambat",  # 20 Sep -> selisih -6 hari -> harus "terlambat"  (cocok: Bu Wulan)
   0: "hari_ini",   # 26 Sep -> selisih 0       -> harus "hari_ini"   (cocok: Pak Joko)
   1: "h1",          # 27 Sep -> selisih 1       -> harus "h1"
   2: "TIDAK MUNCUL",# 28 Sep -> selisih 2       -> BUKAN kategori aktif (by design, sesuai SKILL.md hanya H-3/H-1/hari-ini/terlambat)
   3: "h3",          # 29 Sep -> selisih 3       -> harus "h3"
   4: "TIDAK MUNCUL",# 30 Sep -> selisih 4       -> di luar 4 kategori (benar, bukan bug)
}
```
Semua cocok dengan logika `kelompokkan()` di skrip (diperiksa langsung di kode: `selisih==0` ->
hari_ini, `==1`->h1, `==3`->h3, `<0`->terlambat; selisih 2 dan >=4 sengaja tidak masuk kategori
manapun — ini SESUAI SKILL.md yang hanya menjanjikan 4 kategori tsb, bukan bug).

## Verifikasi batas bulan & tahun kabisat (independen, untuk kasus "X bulan lagi" yang dipakai di
`ubah-status ... --status datang --berikutnya`)
```python
# Kasus lintas tahun: 31 Des 2026 + 1 bulan -> harus 31 Jan 2027
skrip: "Des31 2026 +1bulan -> 2027-01-31"   # BENAR

# Kasus tahun kabisat: 29 Jan 2028 (2028 kabisat, Feb=29 hari) + 1 bulan
skrip: "Jan29 2028 +1bulan -> 2028-02-28 (dipakai 28 Feb 2028)"
manual (Python `calendar.isleap(2028)` = True, Februari 2028 valid sampai tanggal 29):
  -> SEHARUSNYA 2028-02-29, skrip memberi 2028-02-28 -> SELISIH 1 HARI (BUG, lihat di bawah)
```

## TEMUAN (dikonfirmasi ulang secara independen — sudah pernah dicatat di HASIL-UJI.md versi
sebelumnya, tingkat SEDANG, direproduksi lagi di sesi ini)
`parse_tanggal()` pada cabang "N bulan lagi" memakai `min(acuan.day, 28) if bln == 2 else
acuan.day` — nilai 28 di-hardcode untuk Februari **tanpa mengecek tahun kabisat**
(`calendar.isleap`). Dampak: jadwal vaksin/kontrol bertahap yang dijadwalkan ulang dari
tanggal 29/30/31 Januari (atau bulan lain yang lebih panjang) ke Februari di **tahun kabisat**
akan mendapat 28 Februari, padahal 29 Februari valid dan lebih tepat. Dampak praktis kecil
(pengingat maju 1 hari, bukan terlewat) tapi tetap salah hitung matematis untuk kasus tahun
kabisat yang eksplisit di ruang lingkup pengujian (Tahap 6.3 poin "tahun kabisat").

## Hasil
LULUS untuk fungsi inti pengelompokan H-1/H-3/hari-ini/terlambat (100% cocok verifikasi manual).
Bug tahun kabisat pada "N bulan lagi" terkonfirmasi ulang secara independen — lihat skor &
rekomendasi di `HASIL-UJI.md`.
