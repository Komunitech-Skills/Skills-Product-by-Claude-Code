# Pra-cek Telegram — kandidat gelombang 12 (2026-10-11, Akun C)

Metode: `run-uji-tg.sh` (`--channel telegram`, tanpa kirim), HOME hanya skill yang diuji, 1 pesan per skill. Penilaian dari isi chat saja.

## `cek-privasi-openclaw` — LOLOS pra-cek

| Item | Nilai |
|---|---|
| Pesan uji | OpenClaw dipakai balas chat pelanggan WA Business toko kue — cek privasi/keamanan data pelanggan |
| Karakter balasan | 6637 |
| Alat agent | read, exec, process |
| Durasi | ~6 menit |
| Keluaran | `$HOME/komunitech-uji/openclaw-real/hasil/g12-cpo-out.txt` (tidak di-commit) |

**Isi:** Audit baca-saja (`security audit`, approvals, config), format lampu 🔴/🟡/🟢, UU PDP singkat, mode Copilot WA, **tanpa** mengubah config; tidak mengarah ke file eksternal saja.

**Catatan gelombang:** Balasan >4096 karakter — bot produksi biasanya memecah jadi beberapa pesan; pantau saat pilot G12. Endpoint router di balasan berasal dari HOME uji (bukan data pembeli).

## Belum di-run run ini

| Skill | Alasan tunda |
|---|---|
| `rangkaian-pesan-pelanggan` | Run berikutnya (1 pra-cek per run) |
| `laporan-otomatis-terjadwal` | idem |
| `fider-masukan-pelanggan` | idem |
| `notebook-riset-lokal` | idem |
