# Usulan gelombang Telegram 12 — 2026-10-11 (Akun C, S5)

**Tujuan:** 5 skill LULUS (sesudah ≥ 8, selisih ≥ 1,5) dari `promosi/sebelum-sesudah.jsonl` yang **belum** tampil di `koordinasi/telegram-gelombang-*.md` (gelombang 4–11b), urut selisih terbesar. Format: 10 pesan (TANPA/DENGAN per skill), topik forum baru `G12 …`, `skills: []` vs satu skill, **restart gateway** setelah ubah `channels.*`, pra-cek `run-uji-tg.sh` wajib per skill sebelum kirim.

**Menunggu persetujuan pemilik** (bukan gelombang tampilan otomatis).

## Kandidat (5 skill × 2 = 10 pesan)

| # | Skill | Selisih (promosi) | Sesudah | Alasan pilih |
|---|---|---|---|---|
| 1 | `cek-privasi-openclaw` | +6,0 | 8,9 | Janji situs (privasi OpenClaw) belum pernah pilot TG; pembeda jelas vs jawaban generik. |
| 2 | `odoo-usaha` | +5,9 | 8,9 | Produk pengganti SaaS; skenario “jangan hapus data pakai kunci” kuat untuk demo. |
| 3 | `pantau-website-toko` | +5,7 | 8,7 | E-commerce UMKM; tolak pantau sainger + Uptime Kuma sendiri. |
| 4 | `laporan-otomatis-terjadwal` | +5,1 | 8,6 | VIP OpenClaw; hasil panjang — **wajib pra-cek Telegram** sebelum setuju kirim. |
| 5 | `kanboard-papan-kerja` | +5,0 | 9,0 | Produktivitas tim; selisih besar, belum pernah tampil. |

**Cadangan** (bila pra-cek gagal/timeout): `rangkaian-pesan-pelanggan` (+5,25), `inventree-gudang` (+4,5), atau `simulasi-cicilan-pinjaman` (+2,25, baru masuk bundle admin-keuangan).

## Checklist sebelum kirim (Akun C / Akun A)

1. Sinkron skill bot uji ke versi repo + backup config/skill.
2. Buat 10 topik (`mktopics-g11.py` pola G11b, prefix `G12`).
3. Patch config per topik; **restart gateway** (`gw-cek.sh`).
4. Pra-cek: `export SCRATCHPAD=$HOME/komunitech-uji` lalu `run-uji-tg.sh` skenario 1 setiap skill (timeout 1200s bila perlu).
5. Kirim berurutan (`kirim-urut2.py`), kumpulkan jawaban, nilai independen, lapor ke thread 242.

## Keputusan pemilik (isi setelah jawab)

- [ ] Setuju gelombang 12 dengan 5 skill di atas
- [ ] Ganti skill: ___
- [ ] Tunda (alasan): ___
