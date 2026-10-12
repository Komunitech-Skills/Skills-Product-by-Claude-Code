# Gelombang Telegram 12 — persiapan (BELUM dikirim)

**Status:** menunggu jawaban pemilik **no. 26** (pilot G11b, 4 pesan) dan **no. 27** (`usulan-gelombang-12-promo-2026-10-11.md`).

Pra-cek `uji-tg.sh`: **5/5 LOLOS** — rincian `pracek-telegram-g12-2026-10-11.md`.

## Skill & urutan (10 pesan)

| # | Skill | TANPA/DENGAN | Selisih promo | Pra-cek |
|---|---|---|---|---|
| 1–2 | `cek-privasi-openclaw` | topik TBD | +6 | LOLOS |
| 3–4 | `rangkaian-pesan-pelanggan` | topik TBD | +5,25 | LOLOS |
| 5–6 | `laporan-otomatis-terjadwal` | topik TBD | +5,1 | LOLOS |
| 7–8 | `fider-masukan-pelanggan` | topik TBD | +4 | LOLOS (mock Fider) |
| 9–10 | `notebook-riset-lokal` | topik TBD | +3,75 | LOLOS (mock ON) |

Teks pesan: `koordinasi/alat-uji/pilot/msgs-g12.json` (field `topic` diisi setelah `mktopics-g12.py`).

## Checklist sebelum kirim (setelah persetujuan pemilik)

1. Backup skill bot + `openclaw.json` (pola G11b).
2. Buat **topik baru** grup uji (nama mis. `G12 …`): `cd koordinasi/alat-uji/pilot && python3 mktopics-g12.py` → `topik-g12.json`; patch `topic` di `msgs-g12.json`.
3. Patch config: topik TANPA → `skills: []`, topik DENGAN → hanya skill itu (satu skill per pasangan topik).
4. **Restart gateway** (`gw-cek.sh`) setelah ubah `channels.*`.
5. Mock/lokal bila perlu: Fider `127.0.0.1:3000`, Open Notebook `127.0.0.1:5055`, CSV fiktif `laporan/masuk/` untuk laporan-otomatis.
6. Kirim berurutan (`kirim-urut2.py`), kumpulkan jawaban, nilai tanpa→dengan, tulis `telegram-gelombang-12-<tanggal>.md`, lapor topik 242.

## Catatan tampilan

- `cek-privasi-openclaw`: balasan pra-cek >4096 karakter — pantau pemecahan pesan di bot.
- `fider-masukan-pelanggan` / `notebook-riset-lokal`: tanpa mock di bot uji, balasan bisa hanya instruksi setup (~992 char) — **bukan** acuan promosi.
