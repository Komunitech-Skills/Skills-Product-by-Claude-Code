# HASIL UJI ULANG - kanboard-papan-kerja

## Uji ulang 1.0.1 (2026-09-30)

- **Penguji:** agent independen (simulasi agent). **Kanboard asli:** tag v1.2.54, `php -S` (PHP 8.4.19 + SQLite), database baru, 2 papan dari template, ±20 kartu; server tiruan pembuat tidak dipakai. Server milik penguji sudah dimatikan.
- `tests/uji_regresi.py` 142/142 lulus; `validate.py --skill kanboard-papan-kerja` valid.

### Bukti (input baru, jam sekarang 20:09 WIB)
- Jam: "jam 3 sore"=15:00, "10.00"=10:00, "Jumat 10.00"=10:00, pagi jam 8=08:00, 12 siang=12:00, 7 malam=19:00, 11 malam=23:00, "pukul 9"=09:00; "jam 3" dan "jam 3" tanpa hari ditolak dengan SARAN; jam 25 ditolak. Cek epoch di DB benar.
- Tanggal tanpa tahun: 29/09, 27/09, 01/08 (>1 hari, <=60 hari lalu) tetap 2026 + PERINGATAN "SUDAH LEWAT... maksudnya 2027?"; 31/07 dan 15/01 (>60 hari) ke 2027 + PERINGATAN. "kemarin" dikenali.
- Zona: `--tz WITA/WIT` "besok jam 9 pagi" tersimpan 01:00Z / 00:00Z (tanpa konversi ganda). Laporan WIB/WITA/WIT (hari ini, terlambat) dihitung ulang independen dari API mentah: COCOK; batas tengah malam benar (kartu 23:00 WIB tidak "hari ini" di WITA).
- Kolom Selesai (jatuh tempo hari ini & lewat) tidak masuk hari-ini/terlambat/macet.
- Data aneh (null, string, tipe salah, hasil `[1,2,3]`) dari 4 server tiruan: 0 traceback, pesan GAGAL kode 4. Balasan 501 -> pesan "bukan JSON-RPC Kanboard".
- Regresi 06-10: tidak ada (pratinjau vs `--ya`, kartu ganda ditolak, PIC 1 huruf ditolak, singkatan opsi ditolak, 401, host tak diizinkan, skema salah, kartu sudah di kolom itu); token 0 kemunculan di log PHP.

### Temuan
- **Sedang (bukan regresi, ada sejak 1.0.0):** bila zona waktu PROFIL pengguna (mis. Asia/Jakarta) berbeda dari zona APLIKASI Kanboard (default UTC), `getTimezone` mengembalikan zona pengguna tetapi API mengurai tenggat memakai zona aplikasi -> tenggat tersimpan bergeser 7 jam (jam 09:00 tersimpan 16:00 WIB di tampilan Kanboard). Reproduksi nyata. Saran: `cek` memperingatkan/dokumentasikan agar zona aplikasi = zona profil, atau uji satu kartu.
- Rendah: "jam 12 malam" = 00:00 hari yang disebut (ambigu); "jam 13 pagi"/"jam 3 sore pagi" (kontradiktif) diterima diam-diam; galat data aneh menyebut nama Exception (ValueError) tanpa SARAN.

### Skor: **8,5/10**
Semua temuan sedang/rendah 1.0.0 (#1-#9) terbukti diperbaiki dan tanpa regresi; sisa risiko: pergeseran zona profil vs aplikasi. Layak lanjut ke `beta`.
