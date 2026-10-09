# HASIL UJI INDEPENDEN — kanboard-papan-kerja v1.0.0

- **Tanggal:** 2026-09-30 (±19:50–21:10 WIB)
- **Penguji:** agent penguji independen (Claude Code, simulasi agent) — bukan pembuat; membaca folder skill, `docs/panduan-kanboard.md`, `research/sources/kanboard-2026-09-30.md`. Skill disalin ke folder uji di scratchpad (tanpa `tests/`), tidak dipasang di `.claude/skills/`.
- **Kanboard asli milik penguji:** `git clone --depth 1 --branch v1.2.54` dari github.com/kanboard/kanboard (tag terbaru, commit `9ce6a5e`, 28 Agu 2026), `APP_VERSION=v1.2.54 php -S 127.0.0.1:8090`, PHP 8.4.19 + SQLite, database baru. Tidak ada paket sistem yang dipasang. Server tiruan pembuat **tidak** dipakai. Docker tidak dipakai (daemon mati).
- **Data uji baru:** 3 akun (Manajer/Pengguna), 3 papan dari template skill, 27 kartu; zona server diuji **UTC dan Asia/Jakarta**, pengguna WIB/WITA/WIT. Token pribadi dibuat acak oleh penguji dan ditulis ke `users.api_access_token` (setara tombol "Generate token baru"); `date_moved` beberapa kartu dimundurkan langsung di DB uji agar ada kartu macet.
- **OpenClaw:** `bash scripts/uji_openclaw.sh` → OpenClaw 2026.9.7: eligible/modelVisible/commandVisible 117/117 ✔.
- **Validator:** `python3 scripts/validate.py --skill kanboard-papan-kerja` → ✅ valid.

## Ringkasan skenario
| # | Skenario | Hasil | Angka diverifikasi independen |
|---|---|---|---|
| 06 | Papan produksi konveksi (Manajer, server UTC): buat papan, 13 kartu, laporan, batas tengah malam WIB | Lulus (2 temuan sedang di pembacaan tenggat) | Ya — dump DB epoch→UTC/WIB + jam palsu 01:00 WIB |
| 07 | Papan order-pengiriman toko online (peran Pengguna → `--pribadi`, server Asia/Jakarta), pindah kartu, 403 | Lulus | Ya — DB + `getTask` setelah pindah |
| 08 | Papan proyek jasa desain, `--tz WITA`, batas WIP, kartu tertutup & papan nonaktif | Lulus (1 temuan rendah) | Ya — DB dalam WIB/WITA |
| 09 | Input tidak lengkap: tanpa kunci/URL, Kanboard mati, 401, kunci rusak, URL tanpa skema | Lulus | — |
| 10 | Di luar cakupan (hapus papan, tutup kartu, kirim WA) + keamanan | Lulus (1 temuan rendah) | — |
| A/B | Skenario 06 tanpa skill | Skill jelas lebih baik | Ya |
| Pesaing | bivex/kanboard-mcp, ChristianJStarr/kanboard-mcp (dibaca saja) | Skill menang telak untuk audiens ini | — |

## Verifikasi hitungan independen (script penguji `verif.py`, tidak mengimpor kode skill)
Menghitung ulang dari `getMyProjects`/`getColumns`/`getAllTasks` mentah dengan `zoneinfo` (Asia/Jakarta/Makassar/Jayapura) lalu dibandingkan dengan `laporan --json`:
```
== akun sari (server Asia/Jakarta)
WIB independen (terbuka,telat,hari-ini,macet)= (20, 5, 7, 5) skill= (20, 5, 7, 5) COCOK
WITA independen (terbuka,telat,hari-ini,macet)= (20, 5, 6, 5) skill= (20, 5, 6, 5) COCOK
WIT independen (terbuka,telat,hari-ini,macet)= (20, 5, 5, 5) skill= (20, 5, 5, 5) COCOK
== akun dimas (server Asia/Jakarta)
WIB independen (terbuka,telat,hari-ini,macet)= (19, 7, 6, 5) skill= (19, 7, 6, 5) COCOK
WITA independen (terbuka,telat,hari-ini,macet)= (19, 7, 5, 5) skill= (19, 7, 5, 5) COCOK
WIT independen (terbuka,telat,hari-ini,macet)= (19, 7, 5, 5) skill= (19, 7, 5, 5) COCOK
== akun sari (server UTC)
WIB independen (terbuka,telat,hari-ini,macet)= (20, 5, 7, 5) skill= (20, 5, 7, 5) COCOK
WITA independen (terbuka,telat,hari-ini,macet)= (20, 5, 6, 5) skill= (20, 5, 6, 5) COCOK
WIT independen (terbuka,telat,hari-ini,macet)= (20, 5, 5, 5) skill= (20, 5, 5, 5) COCOK
== akun dimas (server UTC)
WIB independen (terbuka,telat,hari-ini,macet)= (19, 7, 6, 5) skill= (19, 7, 6, 5) COCOK
WITA independen (terbuka,telat,hari-ini,macet)= (19, 7, 5, 5) skill= (19, 7, 5, 5) COCOK
WIT independen (terbuka,telat,hari-ini,macet)= (19, 7, 5, 5) skill= (19, 7, 5, 5) COCOK
```
12/12 kombinasi (2 akun × 2 zona server × 3 zona pengguna) **COCOK**. Tenggat yang ditulis skill dicek di DB: benar untuk server UTC (mis. "Jumat jam 10:00" WIB → 03:00 UTC) dan Asia/Jakarta, serta WITA (+1 jam). Batas tengah malam: kartu yang tanggal UTC-nya "hari ini" tetapi WIB-nya besok (dan sebaliknya) dipilah benar.

## Temuan
### Tinggi
- Tidak ada.

### Sedang
1. **"jam 3 sore" → 03:00.** `--tenggat "besok jam 3 sore"` tersimpan Kamis 1 Okt **03:00** WIB (kata sore/malam diabaikan; `_JAM_RE` hanya membaca angka). Bukti: `06` kartu #3. Pratinjau menampilkan 03:00, tetapi pada alur "banyak kartu, satu konfirmasi" mudah terlewat. Saran: kenali pagi/siang/sore/malam (+12 untuk jam 1–11 sore/malam) atau tolak jam 1–6 tanpa keterangan; tambahkan instruksi di SKILL.md agar agent mengonversi ke format 24 jam.
2. **Tanggal tanpa tahun yang baru lewat → tahun depan, tanpa peringatan.** `--tenggat "28/09"` dan `"27/09"` (2–3 hari lalu) tersimpan **2027** (`_tanggal_aman` menggeser ke tahun depan bila > 1 hari lalu), dan PERINGATAN "sudah lewat" tidak muncul — bertentangan dengan SKILL.md ("Tenggat yang sudah lewat diberi PERINGATAN"). Bukti: `06` kartu #4, #6. Saran: geser ke tahun depan hanya bila lewat > ±60 hari, atau selalu minta penegasan saat tahun digeser (tampilkan "PERINGATAN: dibaca sebagai 2027").

### Rendah
3. `"Jumat 10.00"` (jam bertitik tanpa "jam/pukul") → diam-diam 17:00 (`06`).
4. `hari-ini` dan bagian "HARI INI" di `laporan` ikut memuat kartu di **kolom terakhir** (Selesai), tidak konsisten dengan aturan "kolom terakhir = beres" (`08` kartu #26).
5. Data aneh dari server (bukan Kanboard/berbahaya) → **traceback Python** (AttributeError), bukan pesan GAGAL; token tidak tercetak (`10` F).
6. Alamat yang menunjuk aplikasi lain dan membalas 501 → "galat server" (kode 4), bukan "bukan Kanboard" (`09`).
7. `KANBOARD_USER` tanpa `KANBOARD_TOKEN` diam-diam jatuh ke file default (`09`).
8. `--ke` mencocokkan sebagian mulai 1 huruf (`--ke "a"` → Sari Wulandari) tanpa penegasan (`08`; pratinjau tetap menampilkan PIC).
9. `"kemarin"` tidak dikenali; `"Minggu depan"` selalu = +7 hari (bukan hari Minggu) — ambigu, pesan/pratinjau jelas.

## Yang terbukti baik
- Semua perintah bekerja pada Kanboard v1.2.54 asli (cek, daftar-papan, kolom, hari-ini, terlambat, macet, laporan, template, buat-papan, tambah-kartu, pindah-kartu, simpan-kunci, atur).
- Keamanan: 9 metode terlarang ditolak sebelum dikirim (0 permintaan di log server); tulis hanya dengan `--ya`, singkatan ditolak (`allow_abbrev=False` di parser utama & subparser); allowlist host (LAN/internet/nip.io/`user:pw@`/`file://`) dan https wajib untuk internet; redirect ditolak dan penangkap tidak menerima permintaan; timeout saat menulis → kode 8; token 0 kemunculan di semua log/keluaran/log PHP; file kunci 600; peringatan izin file longgar.
- Pesan galat berbahasa awam dengan SARAN; kode keluar konsisten dengan tabel SKILL.md; peran Pengguna diarahkan ke `--pribadi`; ganda/ambigu → kode 7.
- Laporan < 3.500 karakter, kartu tertutup & papan nonaktif tidak dihitung, WIP "MELEBIHI BATAS" tampil.

## Skor: **8/10**
Alasan: inti nilai jual (hitungan terlambat/hari ini/macet lintas zona, template papan, keamanan tulis/token/host) benar dan terverifikasi independen di Kanboard asli; A/B dan banding pesaing menang jelas. Nilai dikurangi karena dua cacat pembacaan tenggat (sedang) yang bisa menyimpan jam/tahun salah secara diam-diam walau terlihat di pratinjau, plus beberapa ketidakkonsistenan kecil. Layak lulus (≥ 7); temuan sedang #1–#2 disarankan diperbaiki sebelum `beta`, lalu diuji ulang singkat.

## Belum diuji oleh penguji
Image Docker resmi, Windows/macOS, jadwal OpenClaw sungguhan ke Telegram, Kanboard di balik HTTPS/reverse proxy, MySQL/PostgreSQL.


## Uji ulang OpenClaw v1.0.5 (2026-10-02)
Skenario U1 (token ditempel + pindah kartu, server tiruan): SEBELUM 4 -> SESUDAH 9, VERDIK LULUS. Tidak ada gema token, pratinjau ditampilkan dulu, saran ganti token di akhir, kartu tidak dipindah sebelum "ya". Rinci: `00-openclaw-sebelum-sesudah.md`.
