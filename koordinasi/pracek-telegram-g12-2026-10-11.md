# Pra-cek Telegram — calon gelombang 12 (2026-10-11, Akun C)

Alat: `run-uji-tg.sh` (`--channel telegram`, tanpa `--deliver`). OpenClaw 2026.9.8 via `openclaw-prod`, model router `claude-sonnet-5`. Gateway bot uji: dinyalakan ulang sebelum uji (`gw-cek.sh`).

| Skill | Versi (repo) | Pesan | Karakter | Skill/script terpakai? | LOLOS pra-cek? | Catatan |
|---|---|---|---|---|---|---|
| `tagih-piutang` | 1.0.7 | S1 OpenClaw (CSV `piutang-toko-bangunan.csv`, hari ini 10 Okt 2026) | 4290 | ya (`read`, `exec`) | **ya** | Total telat Rp142.540.000 & 3 draf WA terbesar utuh di chat; angka cocok perhitungan independen. |
| `siyuan-sop` | 1.0.10 | S1 giliran 1 (cari retur/jam buka + SOP >90 hari) | 1223 | ya (`read`, `exec`) | **ya** | Retur & jam buka lengkap; daftar SOP lama; server tiruan 127.0.0.1:6806 + kunci di `~/.komunitech/siyuan-kunci.txt` home uji. |

**Belum pra-cek run ini (tetap wajib sebelum kirim G12):** `cek-privasi-openclaw`, `odoo-usaha`, `persiapan-jual-atau-wariskan-usaha` (C3 sudah OK 2026-10-10, ulang setelah sync bot uji).

**Rekomendasi:** `tagih-piutang` & `siyuan-sop` layak masuk daftar kirim bila pemilik setuju no. 26; jangan kirim gelombang tanpa persetujuan.

Artefak mentah: `$HOME/komunitech-uji/openclaw-real/hasil/tp-g12-tagih-tg-s1.txt`, `sy-g12-siyuan-tg-s1.txt`.
