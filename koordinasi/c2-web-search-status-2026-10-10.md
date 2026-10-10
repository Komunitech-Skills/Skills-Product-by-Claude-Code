# Status C2 — web_search bot uji (2026-10-10)

Ringkasan untuk pemilik/Akun A; detail uji di branch `cursor/web-search-cari-prospek-8b42`.

## Config tersimpan (tanpa kunci)

- `koordinasi/alat-uji/config-bot-uji/openclaw.json`: `tools.web.search.enabled`, `provider: duckduckgo`, plugin `duckduckgo` enabled.
- VM Cursor: plugin disalin/symlink lewat `setup-cursor.sh` + `mk-home.sh` (lihat commit di branch web-search).

## Hasil

- Pencarian hidup (uji parsial + uji OpenClaw `cari-prospek-web` v1.0.2): **LULUS** 6,7 → 8,2 (+1,5).
- Keputusan 24 tahap 2: **bukan arsip** — skill tetap dijual; promosi setelah merge examples ke default.

## Run berikutnya

- Merge branch web-search + examples skill ke default (Akun A/B).
- Bila DuckDuckGo diblokir di IP lain: fallback `TAVILY_API_KEY` / `BRAVE_API_KEY` di environment repo (nama env persis, tanpa commit nilai).
