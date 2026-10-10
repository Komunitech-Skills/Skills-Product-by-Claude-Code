# Usulan gelombang Telegram 12 — 2026-10-10 (Akun C)

**Status:** menunggu persetujuan pemilik (bukan kirim otomatis). Acuan tampilan: LULUS internal, selisih ≥ 1,5, belum pernah tampil di `koordinasi/telegram-gelombang-*.md` (kecuali G11/G11b untuk skill yang sama).

## Pra-cek `uji-tg.sh` / `run-uji-tg.sh` (skenario 1, `--channel telegram`, tanpa deliver)

| Skill | Versi (catalog) | Karakter jawaban TG | Skill terbaca? | Catatan |
|---|---|---|---|---|
| persiapan-jual-atau-wariskan-usaha | 1.0.1 | 8034 | ya (`read`, `exec`) | Utuh di chat; cocok S1 Bu Sri (OpenClaw 2026-10-10). C3 sudah LOLOS di run sebelumnya. |
| checklist-keamanan-pangan-usaha | 1.0.x | 8246 | ya (`read`, `ls`) | Utuh di chat; checklist + log suhu siap tempel. |
| iterasi-dari-masukan-pelanggan | 1.0.10 | 7417 | ya (`read`, `exec`, `write`) | Utuh di chat TG; data uji `chat-wa-september.txt` + `ulasan-shopee-september.csv` di workspace (salin dari `examples/data/`). Pra-cek Akun C 2026-10-10 ~19:30 UTC. |
| cek-risiko-dan-asuransi-usaha | 1.0.2 | 4048 | ya (`read`, `exec`, `write`) | Utuh di chat (tabel risiko + dana darurat Rp47,4 jt, kekurangan Rp39,4 jt). Pra-cek Akun C 2026-10-10 ~19:32 UTC. |
| cari-prospek-web | 1.0.2 | *(butuh web_search)* | — | LULUS 6,7→8,2 setelah C2 DuckDuckGo; pra-cek + pastikan `web_search` hidup di bot uji. |

## Rekomendasi daftar kirim (maks 10 pesan = 5 skill × TANPA/DENGAN)

Urut **selisih promosi** + pra-cek OK + belum pernah tampil:

1. **checklist-keamanan-pangan-usaha** (+2,4) — 2 pesan  
2. **persiapan-jual-atau-wariskan-usaha** (+2,6) — 2 pesan; jawaban panjang sudah aman di TG  
3. **iterasi-dari-masukan-pelanggan** (+1,7) — 2 pesan **setelah** pra-cek dengan data uji di workspace  
4. **cek-risiko-dan-asuransi-usaha** (+2,1) — 2 pesan **cadangan** bila pra-cek lolos  

**Tidak usul ulang di G12:** `tangani-keberatan-pelanggan`, `kelayakan-investasi-usaha`, `aktifkan-kembali-pelanggan`, `triase-keluhan-pelanggan` (sudah G11/G11b; selisih +1,0 untuk dua pertama).

## Keputusan pemilik (usulan nomor lanjutan thread 242)

**No. 26 — Gelombang 12:** Setuju kirim **4 skill / 8 pesan** (checklist-keamanan-pangan-usaha, persiapan-jual-atau-wariskan-usaha, iterasi-dari-masukan-pelanggan, cek-risiko-dan-asuransi-usaha) di **topik baru**, pola G11b (`skills: []` TANPA, satu skill DENGAN), restart gateway setelah ubah `channels.*`, pra-cek `uji-tg.sh` wajib untuk iterasi & cek-risiko sebelum kirim.

**No. 27 — Bundle (belum dijawab):** tetap usulkan `checklist-keamanan-pangan-usaha` → `paket-kafe-warung`, `proses-pesanan-wa` → `paket-toko-online` (sama seperti S1).
