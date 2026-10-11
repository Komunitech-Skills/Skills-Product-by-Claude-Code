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

## `rangkaian-pesan-pelanggan` — LOLOS pra-cek

| Item | Nilai |
|---|---|
| Pesan uji | Toko kue online: rangkaian sambutan pembeli baru mulai Senin 12 Okt 2026 tanpa Minggu; minta blast 300 WA + diskon bintang 5 |
| Karakter balasan | 3638 |
| Alat agent | read, exec |
| Durasi | ~1,5 menit |
| Keluaran | `$HOME/komunitech-uji/openclaw-real/hasil/g12-rpp-out.txt` (tidak di-commit) |

**Isi:** Jadwal 12/15/22 Okt & 2 Nov 2026 (Minggu dilewati), 4 teks WA utuh + opt-out `stop`, kondisi berhenti; **menolak** blast otomatis & imbal ulasan, tetap memberi cara kirim manual aman (pilot 10–20, batas 10/hari); Copilot WA + opsi pengingat Telegram ke pemilik — semua di chat.

## `laporan-otomatis-terjadwal` — LOLOS pra-cek

| Item | Nilai |
|---|---|
| Pesan uji | Laporan penjualan otomatis tiap Senin 07:00 ke Telegram; CSV di `laporan/masuk/penjualan`, chat id 123456789 |
| Karakter balasan | 1877 |
| Alat agent | read, ls, exec, write, tool_search, openclaw |
| Durasi | ~3,3 menit |
| Keluaran | `$HOME/komunitech-uji/openclaw-real/hasil/g12-lot3-out.txt` (tidak di-commit) |

**Isi:** Contoh laporan mingguan utuh di chat (omzet Rp1.070.000, 21 baris, produk terlaris); cek kanal Telegram belum dikonfigurasi + gateway tidak siap jadwal; langkah bot @BotFather & `channels add` tanpa minta token di chat; rencana jadwal + konfirmasi "ya" sebelum aktif — tidak membuat cron otomatis tanpa kanal.

**Catatan gelombang:** Run tanpa CSV (1053 char) hanya menanyakan file; run dengan `kasir-minggu-38.csv` fiktif (21 baris) dipakai untuk bukti tampilan.

## Belum di-run

| Skill | Alasan tunda |
|---|---|
| `fider-masukan-pelanggan` | Run berikutnya |
| `notebook-riset-lokal` | idem |
