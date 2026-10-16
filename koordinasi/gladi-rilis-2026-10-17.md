# Gladi rilis 20 Okt 2026 (A3) dan uji pasang (A6) - Akun A

Dikerjakan 2026-10-16. Pembeli fiktif: "Gladi Rilis". dist/ tidak di-commit. `catalog.csv` tidak diubah.

## A3 - Gladi rilis

| Langkah | Hasil |
|---|---|
| `python3 scripts/pracek_rilis.py` | OK: 123 calon beta, 0 ditunda, 0 skill dengan celah |
| `python3 scripts/rilis_batch.py --cek` (tanpa `--terapkan`) | OK, siap `--terapkan`; validate.py lolos. Catatan skrip: jadwal keputusan 62 = 2026-10-20 (tanggal efektif 2026-10-16 lebih awal); pastikan tidak ada "batal 62" di `koordinasi/keputusan-otomatis.md` |
| `build.py` tanpa `--izinkan-draft` | GAGAL untuk semua bundle ("Belum rilis: ..."). Wajar: status belum `rilis` sebelum `--terapkan`. Setelah `rilis_batch.py --terapkan` build harus diulang tanpa flag itu |
| `build.py --izinkan-draft` 11 bundle + `--vip --beta` + 1 skill ecer (hitung-ppn) | Semua 13 ZIP berhasil dibuat di dist/ |

Pemeriksaan semua 13 ZIP: tanpa `__pycache__`, `.pyc`, `tests/`, `.DS_Store`, `.git`, `node_modules`, `.env` (0 temuan). Setiap folder skill punya `SKILL.md` (VIP: 139 skill; folder `templates/` di akar VIP memang `templates/openclaw-AGENTS-komunitech.md`, bukan skill). `LISENSI.txt` ada di semua ZIP (berisi nama pembeli, kode, jenis, versi skill). Panduan instalasi masuk sebagai `CARA-INSTAL.md` di akar ZIP (isi identik dengan `docs/instalasi.md`; dinamai ulang oleh `build.py`, bukan `docs/instalasi.md`). Bundle tertentu membawa `docs/panduan-*.md`; VIP membawa `solusi-vip/` (101 berkas).

3 ZIP dibuka manual: ecer hitung-ppn (16 berkas), paket-karyawan-ai-openclaw (96), VIP (3289). Lengkap dan bersih.

Temuan kecil: berkas `*.log` di `pantau-cron-openclaw/examples/data/...` ikut ZIP; itu data contoh, bukan sampah.

## Uji pasang

HOME uji kosong terpisah (bukan HOME gateway): `scratchpad/gladi-home-ecer`, `-bundle`, `-vip`. OpenClaw 2026.9.8 (paket openclaw-prod). Gateway tidak dinyalakan, tanpa token, tanpa instal paket baru.

Cara: ekstrak ZIP, lalu `openclaw skills install ./nama-skill --global` per folder (persis `docs/instalasi.md`), lalu `openclaw skills list --json`.

| ZIP | Terpasang | Terdaftar di `skills list` | Tidak eligible |
|---|---|---|---|
| ecer hitung-ppn | 1 | 1 | 0 |
| paket-karyawan-ai-openclaw | 5 | 5 | 0 |
| VIP (--vip --beta) | 139 | 139 | 0 |

Semua perintah install sukses tanpa galat. Catatan praktis: memasang 139 skill VIP satu per satu memakan sekitar 80 detik+; pembeli VIP sebaiknya memakai salin folder (File Explorer) yang sudah ada di panduan.

Claude Code / Codex / Cursor: jalur di panduan (`~/.claude/skills/`, `~/.agents/skills/`, `~/.cursor/skills/`) cocok dengan isi ZIP, karena setiap folder skill berisi `SKILL.md` langsung di dalamnya dan tidak ada folder pembungkus. Hanya diperiksa jalurnya, tidak dijalankan.

`docs/instalasi.md` tidak diubah: tidak ada langkah yang terbukti keliru.

## Untuk keputusan / perubahan lain (tidak dikerjakan)
1. Pastikan urutan hari rilis: `rilis_batch.py --terapkan` dulu, baru `build.py` tanpa `--izinkan-draft`.
2. Opsional: `CARA-INSTAL.md` tidak menyebut `solusi-vip/` dan `templates/openclaw-AGENTS-komunitech.md` di ZIP VIP.
3. Opsional: tambah catatan waktu pemasangan massal VIP.
