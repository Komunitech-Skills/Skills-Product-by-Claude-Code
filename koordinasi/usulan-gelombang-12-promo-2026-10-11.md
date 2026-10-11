# Usulan keputusan pemilik — gelombang tampilan 12 (S5, 2026-10-11)

**No. 27** (lanjut no. 26 G11b pilot). Dikirim ke Telegram topik "Ringkasan uji" (242) oleh Akun C otomasi.

## Konteks

- Antrian **C1–C5** Akun C: **5/5 selesai** (100%).
- Branch konsolidasi uji: **`cursor/iterasi-otomatis-akun-c-8b42`** (sinkron default 2026-10-11).
- Gelombang 4–11 sudah menampilkan 44 skill (cek `koordinasi/telegram-gelombang-*.md`).
- No. 26 masih menunggu jawaban pemilik (pilot 4 pesan: tangani-keberatan + kelayakan-investasi).

## Kandidat G12 (belum pernah tampil, `lolos_promosi`, selisih ≥ 1,5, sesudah ≥ 8)

Urut selisih terbesar, **hanya skill yang realistis di bot Telegram** (tanpa server SiYuan/Odoo/InvenTree di VM uji):

| Peringkat promo | Skill | Tanpa → Dengan | Selisih | Catatan pra-cek |
|---|---|---|---|---|
| 4 | `cek-privasi-openclaw` | 3 → 9 | +6 | Teks murni; wajib `uji-tg.sh` |
| 13 | `rangkaian-pesan-pelanggan` | 3 → 8,25 | +5,25 | Teks + jadwal; pra-cek panjang |
| 14 | `laporan-otomatis-terjadwal` | 3,5 → 8,6 | +5,1 | Bisa panjang; pra-cek wajib |
| 20 | `fider-masukan-pelanggan` | 5 → 9 | +4 | Produk OSS — uji tanpa install bila skill mengizinkan |
| 29 | `notebook-riset-lokal` | 4,5 → 8,25 | +3,75 | Teks; hindari klaim file lokal di TG |

**Cadangan** (selisih tinggi tapi butuh sistem luar / risiko demo): `siyuan-sop`, `odoo-usaha`, `inventree-gudang`, `kanboard-papan-kerja` — tunda ke gelombang khusus "software pengganti SaaS" setelah uji manusia platform.

## Usulan no. 27 (minta jawaban pemilik)

**a)** Setuju **gelombang 12 = 10 pesan** (5 skill × TANPA/DENGAN) dari tabel kandidat di atas, **topik baru** `G12 …`, pra-cek `uji-tg.sh` per skill, restart gateway, **setelah** no. 26 dijawab?

**b)** G12 diganti isi: sebutkan skill (maks 5).

**c)** Tunda G12 sampai merge branch `cursor/iterasi-otomatis-akun-c-8b42` ke default selesai.

**Rekomendasi Akun C:** **c)** dulu bila merge belum; lalu **a)** dengan 5 skill teks di atas — selisih besar dan belum pernah tampil.
