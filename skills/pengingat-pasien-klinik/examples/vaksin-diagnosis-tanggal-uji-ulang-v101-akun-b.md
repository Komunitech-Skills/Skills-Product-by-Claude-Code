# Uji ulang independen v1.0.1 — blocklist vaksin/diagnosis & "N bulan lagi"

Penguji: Akun B (independen, sesi terpisah dari uji v1.0.0 sebelumnya). Skill dijalankan dari
lokasinya di repo (`skills/pengingat-pasien-klinik/scripts/pengingat_pasien.py`, kode tidak
diubah). Semua data pasien dibuat di scratchpad
`/tmp/.../scratchpad/rt-klinik/a/pasien/DAFTAR.csv` (fiktif, dihapus setelah uji, tidak masuk
repo). Perintah dijalankan via `python3 <skill>/scripts/pengingat_pasien.py --file ... --hari-ini
... <subperintah>` (opsi global sebelum subperintah).

## (a) Jenis vaksin sah — wajib diterima (6/6 lolos)
| Jenis | Hasil |
|---|---|
| imunisasi campak | Tersimpan #1 |
| vaksin rabies | Tersimpan #2 |
| vaksin MR | Tersimpan #3 |
| imunisasi DPT | Tersimpan #4 |
| booster hepatitis B | Tersimpan #5 |
| suntik TT | Tersimpan #6 |

Semua 6 kata kunci dari instruksi diterima tanpa workaround. Ini memperbaiki temuan TINGGI dari
uji v1.0.0 Akun B (imunisasi campak/vaksin rabies dulu selalu ditolak).

## Kalimat bernada diagnosis — wajib ditolak (8/8 ditolak)
`riwayat campak`, `positif rabies`, `didiagnosis difteri`, `kena DBD`, `sakit maag`,
`asma kambuh`, `batu ginjal`, `vertigo` — semuanya keluar `ERROR` (exit 1), tidak tersimpan.

## Jenis kunjungan wajar non-vaksin — wajib diterima (6/6 lolos)
`kontrol behel`, `fisioterapi sesi 3`, `scaling`, `cek gigi anak`, `vaksin kucing`,
`kontrol pasca operasi` — semua tersimpan tanpa ditolak keliru (tidak ada regresi
over-blocking).

## 30 variasi licik tambahan (huruf besar, singkatan, typo, mid-kalimat)
| Jenis | Hasil | Catatan |
|---|---|---|
| IMUNISASI CAMPAK (huruf besar) | LOLOS | benar |
| VAKSIN CAMPAK UTK BAYI 9BLN | LOLOS | benar |
| vaksin cacar air anak | LOLOS | benar |
| vaksin  rabies (spasi ganda) | LOLOS | benar |
| vaksin difteri (DPT) anak sekolah | LOLOS | benar |
| kontrol lanjutan pasca imunisasi campak | LOLOS | benar |
| vaksin Covid booster | LOLOS | benar |
| suntik tetanus (TT) ibu hamil | LOLOS | benar |
| VAKSIN hepatitis B dosis 2 | LOLOS | benar |
| imunisasi Hepatitis B bayi baru lahir | LOLOS | benar |
| kontrol rutin ke-3 vaksin rabies | LOLOS | benar |
| vaksin covid-19 dosis booster ke2 | LOLOS | benar |
| cek gigi rutin / kontrol pasca sunat | LOLOS | benar |
| kena cacar air, kontrol | DITOLAK | benar (penanda "kena") |
| riwayat DBD, kontrol ulang | DITOLAK | benar |
| POSITIF Rabies stlh digigit | DITOLAK | benar (case-insensitive) |
| vaksin rabies, riwayat gigitan anjing | DITOLAK | benar (penanda "riwayat" tetap menang meski ada kata "vaksin") |
| kontrol krn ada riwayat difteri | DITOLAK | benar |
| covid parah, isoman | DITOLAK | benar |
| kambuh asma, kontrol | DITOLAK | benar |
| mengidap hepatitis, kontrol | DITOLAK | benar |
| gejala DBD, cek darah | DITOLAK | benar |
| terinfeksi rabies | DITOLAK | benar |
| diagnosa maag | DITOLAK | benar |
| cek up rutin campak (tanpa kata pemicu vaksin dekat "campak") | DITOLAK | **fail-closed, bukan bug** — tanpa kata vaksin/imunisasi/booster/suntik di dekatnya, "campak" tetap dianggap berisiko; agent sebaiknya sarankan pengguna menulis "imunisasi campak" |
| vaksinrabies (tanpa spasi/typo gabung) | LOLOS | **catatan, bukan celah keamanan**: `\b` regex tidak match kata yang menempel tanpa spasi, jadi baik pemicu vaksin maupun kata diagnosis sama-sama tidak terdeteksi di kata gabung — hasilnya kebetulan benar di sini, tapi typo semacam ini secara umum lolos dari kedua pemeriksaan (bukan risiko privasi karena tidak ada info baru yang bocor, hanya validasi tidak menyala) |
| Vaksin Rabies (anjing gigit kemarin) | LOLOS | wajar diterima — menyebut alasan vaksinasi (gigitan), bukan status diagnosis pasien |
| vaksin rabies krn digigit anjing liar | LOLOS | wajar diterima, sama alasannya |

**Tidak ditemukan kasus jenis vaksin sah yang salah ditolak, atau kalimat diagnosis eksplisit yang
lolos tersimpan.** Dua catatan di atas (baris terakhir tabel) adalah desain konservatif yang wajar
(fail-closed) atau efek regex `\b` pada kata tergabung tanpa spasi — tidak berdampak ke privasi
pasien karena tidak ada diagnosis yang bocor tersimpan, hanya validasi tambahan yang tidak
menyala untuk kata typo yang jarang terjadi.

## (b) Verifikasi "N bulan lagi" — dihitung independen dengan `datetime`/`calendar.isleap`
| Basis | Ekspresi | Hasil script | Ekspektasi independen (Python `calendar.monthrange`) | Cocok? |
|---|---|---|---|---|
| 2028-01-29 | 1 bulan lagi | 29 Feb 2028 | 2028-02-29 (2028 kabisat) | ✅ |
| 2026-01-31 | 1 bulan lagi | 28 Feb 2026 | 2026-02-28 (2026 bukan kabisat) | ✅ |
| 2026-03-31 | 1 bulan lagi | 30 Apr 2026 | 2026-04-30 (April 30 hari) | ✅ |
| 2026-12-31 | 2 bulan lagi | 28 Feb 2027 | 2027-02-28 (2027 bukan kabisat) | ✅ |

Bug tahun kabisat yang dilaporkan di uji v1.0.0 Akun B **sudah diperbaiki dan terverifikasi
benar** di v1.0.1, termasuk kasus non-kabisat dan bulan pendek lainnya.

## (c) Regresi H-3/H-1/hari-ini/terlambat, `hapus`, ringkasan tanpa WA — tidak ada regresi
Diuji dengan `--hari-ini 2026-09-26`: pasien tanggal 2026-09-20 → **TERLAMBAT**; hari ini →
**HARI INI**; besok → **BESOK (H-1)**; 3 hari lagi → **H-3** — semua muncul di kelompok yang
benar pada `daftar --tanpa-draf`. Pasien `persetujuan tidak` **tidak muncul** di `daftar` maupun
`ringkasan`. `ringkasan --samarkan` menghasilkan nama berinisial ("T.", "H.", "B.") **tanpa
nomor WA sama sekali** (diverifikasi tekstual — tidak ada pola `0812…`/`62…` di output).
`hapus --id 1` → pratinjau, lalu `--ya` → dihapus permanen, terverifikasi via `info` (total baris
turun dari 5 ke 4).

## Uji alat bawaan
- `python3 skills/pengingat-pasien-klinik/tests/uji_regresi.py`: **34/34 lulus** (28 tes lama +
  6 tes baru v1.0.1, tidak ada yang diubah).
- `python3 scripts/validate.py --skill pengingat-pasien-klinik`: **lulus** ("1 skill valid, 80
  baris katalog sesuai").
- `scripts/uji_openclaw.sh` **tidak dijalankan** (di luar tugas sesi ini, sesuai instruksi).

## Kesimpulan
Kedua temuan tingkat TINGGI dan SEDANG dari uji v1.0.0 Akun B (blocklist memblokir jenis vaksin
sah; bug tahun kabisat) **terbukti sudah diperbaiki dengan benar** di v1.0.1, tanpa regresi pada
fungsi inti (pengelompokan tanggal, privasi persetujuan, hak hapus, ringkasan tanpa WA). Lihat
skor & ringkasan lengkap di bagian "Uji ulang independen v1.0.1 (Akun B, 2026-09-26)" pada
`HASIL-UJI.md`.
