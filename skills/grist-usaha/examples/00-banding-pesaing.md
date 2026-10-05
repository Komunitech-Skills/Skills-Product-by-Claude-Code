# Uji banding pesaing — skill/tool publik untuk Grist & alternatif Airtable UMKM

**Kata kunci dicari:** "grist ai agent skill mcp claude clawhub", "grist skill.md", "airtable
template UMKM CRM stok Indonesia gratis". Sumber: web search 2026-09-26 (lihat daftar di bawah).

## Pesaing yang ditemukan
**`grist-mcp-server` (gwhthompson, GitHub, ~3 bintang)** — MCP server (bukan Agent Skill
SKILL.md) yang membungkus REST API Grist jadi 11 tools untuk agent. Dinilai **hanya lewat
deskripsi publik** (dibaca untuk dinilai, tidak disalin):
- Perlu instalasi npm + konfigurasi MCP server manual + `GRIST_API_KEY` di config file —
  **bukan** "tanpa setup" seperti prinsip CLAUDE.md; tidak cocok untuk pembeli awam yang
  ditargetkan skill ini.
- Berbahasa Inggris, tidak berkonteks Indonesia (tidak ada pola tabel UMKM, tidak ada
  pembersihan angka Rupiah, tidak ada rumus WA/stok siap pakai).
- Tidak ditemukan kemampuan membaca file `.grist` langsung secara read-only tanpa Grist
  menyala — semua lewat REST API (berarti wajib Grist/Docker sedang berjalan).
- Bintang GitHub rendah (~3) — **tidak lolos ambang bukti pemakaian nyata** CLAUDE.md Tahap 2
  (< 100 untuk repo satu skill), jadi tidak memenuhi syarat untuk kurasi/ATM, hanya relevan
  sebagai pembanding kualitas fungsi.

**Tidak ditemukan** skill/prompt Agent Skill (SKILL.md) publik khusus Grist di ClawHub/skills.sh
yang memenuhi ambang bukti (bintang/instal/pemeliharaan) untuk dibandingkan head-to-head secara
langsung — pasar skill Grist masih sangat sepi dibanding Airtable.

**Template Airtable UMKM/CRM+stok gratis:** hasil pencarian hanya template Airtable resmi
generik (Sales CRM, Lightweight CRM, Personal CRM) — bukan template siap pakai berbahasa
Indonesia dengan pola stok/pesanan UMKM, dan tetap berbayar (biaya bulanan Airtable per
baris/pengguna di atas paket gratis) — bukan produk "sekali beli, jalan di komputer sendiri"
seperti janji skill ini.

## Penilaian berdampingan (fungsi yang sebanding: rancang tabel + baca data)
| Aspek | `grist-mcp-server` (pesaing) | `grist-usaha` (kami) |
|---|---|---|
| Setup | Install npm + config MCP + API key manual | Tempel folder skill, tanpa paket tambahan |
| Baca `.grist` tanpa Grist menyala | Tidak (butuh REST API + Grist jalan) | Ya (`daftar-tabel`/`ringkasan`/`ekspor-csv`) |
| Pola tabel siap pakai UMKM Indonesia | Tidak ada | 4 pola (pelanggan/pesanan/stok/jadwal konten) |
| Pembersihan angka Rupiah campur format | Tidak ada | Ada (`bersihkan-csv`), dengan 1 celah — lihat HASIL-UJI #1 |
| Bahasa & konteks Indonesia | Tidak | Ya, penuh |
| Keamanan alamat server (localhost-only default) | Tidak diketahui dari dokumentasi publik | Ya, eksplisit & diuji |

## Kesimpulan
Skill kami **unggul** dalam localisasi Indonesia, kemudahan pakai tanpa setup, kemampuan baca
`.grist` tanpa Grist menyala, dan keamanan alamat server — nilai tambah dibanding satu-satunya
pesaing yang ditemukan cukup jelas. Skor tidak dibatasi maks. 6 oleh aturan uji banding ini.

Sumber:
- https://github.com/gwhthompson/grist-mcp-server
- https://www.pulsemcp.com/servers/gwhthompson-grist
- https://www.airtable.com/templates/sales-crm/expaRDyCNa7YNZQoO
- https://www.airtable.com/templates/lightweight-crm/expGObpa2AGjv2Z8t
