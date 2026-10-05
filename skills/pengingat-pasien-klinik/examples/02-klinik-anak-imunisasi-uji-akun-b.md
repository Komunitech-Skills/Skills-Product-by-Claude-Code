# Uji independen Akun B — Skenario 2 (normal): klinik anak, imunisasi

Hari acuan: 26 September 2026.

## Perintah pertama (bahasa alami pengguna) & hasil
```
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 --json tambah \
  --nama "Baby Dinda" --wa "0813-2222-3333" --jenis "imunisasi campak" --tanggal "besok" --persetujuan ya
```
```
{"ok": false, "error": "'jenis kunjungan' berisi kata yang menyerupai diagnosis/nama penyakit ('campak'). ..."}
```

## TEMUAN BARU (belum tercatat di HASIL-UJI.md sebelumnya) — tingkat TINGGI
`campak` masuk daftar `KATA_DIAGNOSIS` di `scripts/pengingat_pasien.py` sehingga **"imunisasi
campak" dan "vaksin campak" ditolak total**, padahal ini adalah **nama vaksin/imunisasi rutin
anak yang sangat umum** (bukan penyakit yang sedang diderita pasien), dan skill ini secara
eksplisit menyasar "klinik anak imunisasi" (disebut di kategori `kapan digunakan` SKILL.md).
Diuji ulang untuk kata sejenis:
```
"vaksin campak"  -> DITOLAK ('campak')
"vaksin rabies"  -> DITOLAK ('rabies')   # padahal contoh resmi di SKILL.md: "vaksin hewan"/rabies untuk klinik hewan
"vaksin DBD"     -> DITOLAK ('dbd')
```
`rabies` khususnya bermasalah: SKILL.md sendiri memberi contoh "vaksin hewan" untuk klinik hewan,
dan vaksin rabies adalah jenis vaksin hewan paling umum di Indonesia (wajib di banyak daerah) —
tapi kata itu ada di `KATA_DIAGNOSIS` sehingga tertolak. Ini bukan sekadar kasus tepi; ini
memblokir salah satu skenario inti yang dijanjikan skill sendiri.

**Solusi sementara (workaround) yang berhasil:** tulis jenis kunjungan tanpa menyebut nama
penyakit/vaksin spesifik, mis. `"imunisasi rutin"` atau `"vaksin (imunisasi anak)"` — keduanya
lolos karena tidak memuat kata di `KATA_DIAGNOSIS`:
```
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 --json tambah \
  --nama "Baby Dinda" --wa "0813-2222-3333" --jenis "imunisasi rutin" --tanggal "besok" --persetujuan ya
{"ok": true, "mode": "tersimpan", "id": "1", "teks": "Tersimpan #1: Baby Dinda | Imunisasi rutin | 27 Sep 2026 | persetujuan: ya", "peringatan": []}
```
```
python3 scripts/pengingat_pasien.py --hari-ini 2026-09-26 --json daftar --kapan besok
{"ok": true, "mode": "baca", "kelompok": {..., "h1": 1}, "teks": "BESOK (H-1) (1)\n  #1 Baby Dinda | Imunisasi rutin | 27 Sep 2026 | 0813-2222-3333\n\nDRAF PESAN...\n#1 Baby Dinda (0813-2222-3333):\nHalo Baby Dinda, ini pengingat dari kami untuk jadwal imunisasi rutin Anda pada 27 Sep 2026. ..."}
```
WA dan tanggal H-1 (26+1=27 Sep) benar. Draf pesan sopan dan tidak menyebut nama penyakit.

## Rekomendasi
Keluarkan nama-nama vaksin rutin yang umum diucapkan sebagai jenis kunjungan (campak, rabies,
DBD, difteri, TBC/BCG, dll.) dari `KATA_DIAGNOSIS`, ATAU tambahkan pengecualian khusus saat kata
itu didahului "vaksin"/"imunisasi" (mis. regex `\b(vaksin|imunisasi)\s+campak\b` dikecualikan,
tapi "riwayat campak"/"kena campak" tetap ditolak). Sampai diperbaiki, SKILL.md sebaiknya
menyebutkan contoh kalimat aman ("imunisasi rutin", "vaksin (sebutkan jenisnya di catatan internal
klinik, bukan di skill ini)") agar staf tidak bingung saat ditolak.

## Hasil
LULUS dengan CATATAN — fungsi inti benar setelah workaround, tapi skenario yang dijanjikan SKILL.md
sendiri ("imunisasi"/"vaksin hewan rabies") gagal tanpa workaround. Lihat skor & temuan di
`HASIL-UJI.md`.
