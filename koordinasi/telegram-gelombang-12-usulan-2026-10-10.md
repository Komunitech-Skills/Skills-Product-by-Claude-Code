# Usulan gelombang Telegram 12 — 2026-10-10 (Akun C)

**Status:** menunggu persetujuan pemilik (bukan kirim otomatis). Acuan: skill **LULUS** di `promosi/sebelum-sesudah.jsonl`, belum tampil di gelombang 4–11b, urut **selisih** terbesar. Pra-cek `uji-tg.sh` wajib per calon sebelum kirim.

**Pra-cek 2026-10-11:** `siyuan-sop` & `tagih-piutang` **LOLOS** (lihat `koordinasi/pra-cek-g12-2026-10-11.md`). Tiga calon lain belum.

## Rekomendasi no. 26 (5 skill × 2 topik = 10 pesan)

| Urut | Skill | Versi (promosi) | Selisih | Catatan |
|---|---|---|---|---|
| 1 | `siyuan-sop` | 1.0.10 | +7,5 | Pembeda kuat (cadangan + TIMPA); uji tiruan SiYuan — sebut di cuplikan. |
| 2 | `cek-privasi-openclaw` | 1.1.4 | +6,0 | Relevan member VIP OpenClaw; skenario jebakan sadap WA. |
| 3 | `odoo-usaha` | 1.0.5 | +5,9 | Server tiruan; pesan uji = tolak kunci admin + hapus massal (sudah di promosi). |
| 4 | `tagih-piutang` | 1.0.7 | +1,8 | Uji OpenClaw Akun C 2026-10-10 LULUS; belum pernah gelombang — **pra-cek TG wajib** (CSV panjang). |
| 5 | `persiapan-jual-atau-wariskan-usaha` | 1.0.1 | +2,6 | C3 TG OK (~8 rb karakter); pra-cek ulang setelah merge skill ke bot uji. |

**Cadangan** bila pra-cek timeout: `pengingat-follow-up` (+5,75), `kanboard-papan-kerja` (+5,0), `inventree-gudang` (+4,5).

## Gelombang promosi G11b (no. 27, terpisah)

Sesuai `koordinasi/telegram-gelombang-11b-2026-10-10.md`: **`tangani-keberatan-pelanggan`** & **`kelayakan-investasi-usaha`** layak cuplikan (LULUS, tampilan bersih). **`aktifkan-kembali-pelanggan`** & **`triase-keluhan-pelanggan`** selisih +1,0 — tetap bundle, **jangan promosi** kecuali pemilik mau pamer perbandingan tipis.

## Checklist operasional (sama gelombang 10–11b)

1. Sinkron skill bot uji ke versi repo (backup `skills-backup-*` + config).
2. Topik baru `G12 … — TANPA/DENGAN`; TANPA `skills: []`, DENGAN hanya skill itu.
3. **Restart gateway** setelah ubah `channels.*`.
4. `kirim-urut2.py` dengan DB di `$HOME/komunitech-uji/...`, jeda antar pesan.
5. Lapor hasil ke thread 242 (@nikioktarian).
