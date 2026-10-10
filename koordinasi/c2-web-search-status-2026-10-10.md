# C2 — web_search & uji cari-prospek-web (2026-10-10, Akun C)

## web_search bot uji
- Provider config: `tools.web.search.provider` = **tavily** (`koordinasi/alat-uji/config-bot-uji/openclaw.json`).
- Secret Cloud: nama **`tavily`** (bukan `TAVILY_API_KEY`); `setup-cursor.sh` memetakan `TAVILY_API_KEY="${TAVILY_API_KEY:-${tavily:-}}"` di `oc.sh` / `oc-tg.sh` / `run-uji*.sh`.
- Plugin: `@openclaw/tavily-plugin@2026.9.8` terpasang di HOME bot uji.
- **Verifikasi:** pesan uji “cari 3 toko kue di Bandung…” → alat **`tavily_search`** terpanggil, jawaban berisi 3 toko + telepon (~668 karakter, ~20 d).

## Gateway
- `gw-cek.sh` gagal siap: config ditulis OpenClaw **2026.9.9**, binary prod **2026.9.8** (upgrade npm ke 2026.9.9 gagal — Node di pod). Gelombang **11b (C1)** menunggu selaraskan versi atau `OPENCLAW_ALLOW_OLDER_BINARY_DESTRUCTIVE_ACTIONS=1` + restart gateway.

## Uji cari-prospek-web 1.0.2 (satu putaran, S1 lokal saja)
- HOME: `cpw-c2-s1` via `mk-home.sh` (perlu symlink `npm` plugin — lihat perbaikan `mk-home.sh`).
- Durasi ~2,5 menit; 15 baris tabel; **tetap memakai Google Maps/browser**, bukan direktori teks; `web_search` di log: *disabled or no provider* (sebelum symlink npm).
- **Skor sementara:** belum dinilai penuh 4 skenario; pola masih melanggar batas “hanya direktori” → lanjutkan uji penuh setelah `mk-home` + plugin OK, lalu keputusan 24 tahap 2 (LULUS vs usul arsip).

## Rekomendasi run berikutnya
1. `bash koordinasi/alat-uji/setup-cursor.sh` → ulang S1 lokal + Telegram + S2–S4 brief.
2. Perbaiki gateway (versi OC) → **C1** gelombang 11b.
3. Laporkan hasil uji cari-prospek ke Telegram thread 242 bila verdik final.
