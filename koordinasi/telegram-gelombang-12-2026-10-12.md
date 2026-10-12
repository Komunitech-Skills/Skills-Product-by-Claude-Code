# Gelombang Telegram 12 — 2026-10-12

Keputusan pemilik **no. 27** (disetujui 2026-10-12). Penilai: Akun C (Cursor Cloud). Lima skill × TANPA/DENGAN, **10 pesan**, topik **1118–1127** (`topik-g12.json`). Pesan: `msgs-g12.json`. Mock lokal: Fider `127.0.0.1:3000`, Open Notebook `127.0.0.1:5055`, CSV fiktif `~/laporan/masuk/penjualan/kasir-minggu-38.csv`. Gateway di-restart setelah `patch-topik.py`. Transkrip: `jawaban-g12-tg.txt` (HOME uji; gabungan `updates-g2.jsonl` + fallback `session_transcript_fts` bila poller melewatkan balasan panjang).

**Catatan teknis:** poller `poll-g2.py` sering hanya menangkap pesan "Working" untuk balasan >7 menit (`cek-privasi-openclaw`); skor memakai transkrip sesi sqlite. `laporan-otomatis-terjadwal` DENGAN tidak menemukan CSV (agent mencari `workspace`, file ada di HOME). `fider-masukan-pelanggan` DENGAN meminta `simpan-kunci` padahal kunci sudah di `~/.komunitech/` — TANPA tanpa skill justru memanggil API mock dengan sukses.

## Skor & verdik

| Skill | TANPA | DENGAN | Selisih | Verdik | Pembeda (satu kalimat) |
|---|---|---|---|---|---|
| cek-privasi-openclaw | 7,5 | 9 | +1,5 | **LULUS** | DENGAN format lampu 🔴/🟡/🟢, UU PDP, exec/sandbox; TANPA audit teknis bagus tapi tanpa kerangka skill. |
| rangkaian-pesan-pelanggan | 7,5 | 8,75 | +1,25 | **BELUM** | DENGAN jadwal tanggal + opt-out `stop` + tabel; TANPA sudah menolak blast/diskon bintang 5 tapi jadwal kurang terstruktur. |
| laporan-otomatis-terjadwal | 8 | 6 | −2,0 | **BELUM** | TANPA contoh laporan angka utuh dari CSV; DENGAN menolak karena folder tidak di workspace (masalah path lingkungan, bukan promosi). |
| fider-masukan-pelanggan | 8 | 5 | −3,0 | **BELUM** | TANPA (tanpa skill) pratinjau impor + ringkasan QRIS 14 suara; DENGAN hanya instruksi kunci (~449 char di chat). |
| notebook-riset-lokal | 6,5 | 7 | +0,5 | **BELUM** | Keduanya jawab 0,5% dari pengetahuan umum; DENGAN cek daftar notebook skill, mock API terbatas (endpoint ask/search). |

**10/10 pesan terkirim**; tidak ada `PlatformMessageNotDispatchedError`. Balasan utuh di chat untuk 7/10 pasangan (3 pasangan butuh transkrip sqlite / balasan pendek).

## Rekomendasi

- **Promosi pilot:** `cek-privasi-openclaw` (selisih ≥1,5, format tampilan kuat).
- **Tetap bundle, jangan promosi Telegram dulu:** `rangkaian-pesan-pelanggan` (selisih <1,5), `notebook-riset-lokal`.
- **Perbaiki lingkungan / skill sebelum tampilan:** `laporan-otomatis-terjadwal` (samakan path CSV workspace↔HOME bot uji); `fider-masukan-pelanggan` (kunci & mock harus terbaca saat skill aktif).
- **Berikutnya:** C10 gelombang 13 (bot pertama, topik sudah 1093–1102) atau C9 pra-cek beta lokal.
