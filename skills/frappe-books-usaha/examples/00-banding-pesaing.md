# Uji banding pesaing — Akun B, 26 Sep 2026

Kata kunci yang dicari: "Frappe Books MCP server", "Frappe Books agent skill SKILL.md books.db",
"clawhub/skills.sh accounting skill sqlite invoices receivables aging". Sumber: web search, GitHub, clawskills.sh (indeks ClawHub).
Pesaing hanya **dibaca untuk dinilai**, tidak diinstal/dijalankan, tidak disalin.

| Kandidat | Cocok untuk Frappe Books desktop? | Catatan |
|---|---|---|
| esafwan/frappe_data_skill (GitHub, ISC, 1 bintang, 3 commit) | **Tidak** — untuk situs Frappe Framework/ERPNext via MCP/REST/bench | Butuh API key; bisa create/update/delete dokumen (tidak read-only) |
| appliedrelevance/frappe_mcp_server (LobeHub) | **Tidak** — REST API Frappe Framework | Butuh FRAPPE_URL + API key/secret; Frappe Books tidak punya REST API |
| "database-query" (ClawHub, klaim 95rb+ instal) | Generik SQLite → bisa membuka `.books.db` | Tidak tahu skema Frappe Books: UTC vs WIB, submitted/cancelled, retur, Currency teks; tanpa jaminan read-only |
| invoice-chaser / invoice-tracker-pro (clawskills.sh) | Tidak membaca Frappe Books | Pelacak invoice sendiri; aging 30 hari generik, bukan Indonesia |

## Penilaian skenario normal pertama (toko kopi, "penjualan September + belum dibayar")
- Pesaing khusus Frappe (frappe_data_skill, frappe_mcp_server): **tidak bisa menjalankan skenario** (tidak ada server/API di Frappe Books desktop).
- Skill SQL generik: perilakunya setara kolom "tanpa skill" di `00-pembanding-tanpa-skill.md` — hasil terbaik yang
  masuk akal Rp 518.000 (salah Rp 46.000 karena tanggal UTC), tanpa pemisahan draf/batal/retur.
- **frappe-books-usaha:** Rp 564.000 / belum dibayar Rp 410.000, benar, read-only.

Skor berdampingan (skenario ini): frappe-books-usaha 9/10 · SQL generik 4/10 · pesaing khusus Frappe tidak berlaku.
**Skill kita tidak kalah** untuk laporan. Tidak ditemukan pesaing publik yang menyiapkan CSV Import Wizard Frappe Books.

Sumber: https://github.com/esafwan/frappe_data_skill · https://lobehub.com/mcp/appliedrelevance-frappe_mcp_server ·
https://clawskills.sh/ · https://clawskills.sh/skills/audsmith28-invoice-chaser · https://github.com/VoltAgent/awesome-openclaw-skills
