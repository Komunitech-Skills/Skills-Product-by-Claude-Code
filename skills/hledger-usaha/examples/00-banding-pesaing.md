# 00 — Uji banding pesaing (skenario 01, toko kue)

> Penguji independen (Akun B), 2026-09-26. Skill/aplikasi pesaing hanya **dibaca untuk dinilai**; tidak ada kode pesaing yang dijalankan atau disalin.

## Pencarian
Kata kunci: "hledger agent skill SKILL.md plain text accounting Claude", "clawhub hledger OR ledger-cli OR beancount skill bookkeeping", "Frappe Books free desktop accounting". Sumber: WebSearch, ClawHub (halaman + API publik), GitHub.

| Kandidat | Sumber | Bukti pemakaian | Catatan |
|---|---|---|---|
| **Hledger** (@bisbeebucky) | https://clawhub.ai/bisbeebucky/hledger | 1.223 unduhan, 31 instal, 0 bintang, 1 versi (1.0.0, terbit 28 Feb 2026, metadata diperbarui 18 Mei 2026) | Pesaing skill paling langsung. MIT/MIT-0 |
| openaccountant/skills (`profit-loss`, `import-transactions`, `month-end-close`) | https://github.com/openaccountant/skills | 78 bintang, 16 fork, 5 commit | Generik (AS), tidak memakai hledger/ledger/beancount, bukan double-entry berbasis file |
| Setup hledger + Obsidian + Claude Code (Mandalivia) | https://www.mandalivia.com/obsidian/hledger-obsidian-personal-finance-with-claude-code/ | Artikel/forum PTA | Keuangan pribadi, bukan skill terpaket |
| HLedger MCP | https://agentpedia.codes/mcp/hledger-mcp | — | Server MCP (butuh instalasi Node/konfigurasi), bukan SKILL.md |
| **Frappe Books** (aplikasi desktop) | https://github.com/frappe/books, https://frappe.io/books | Proyek populer (AGPL-3.0), dirilis 2020 | Pengganti SaaS, bukan skill AI; dilaporkan pembaruan terhambat sertifikat code-signing |

## Isi skill pesaing ClawHub "Hledger" (dibaca, tidak dijalankan)
- `SKILL.md`: pembungkus tipis — "Executes arbitrary `hledger` subcommands", contoh `balance`, `register Assets`. Tidak ada cara mencatat transaksi, bagan akun, impor bank, validasi, atau format laporan.
- `index.js`: `exec(\`hledger ${input}\`)` — string masuk ke **shell** tanpa validasi. Klaim "does not allow arbitrary shell execution" tidak benar: input seperti `bal; <perintah lain>` akan dijalankan shell. `skill-card.md` pesaing sendiri mengakui risiko ini. (Tahap 3: gagal audit keamanan bila akan dikurasi.)

## Skenario 01 dengan pesaing (dinilai berdasarkan kemampuan yang dideskripsikan)
Pesaing tidak bisa mencatat 15 transaksi dari kalimat; agent harus menulis jurnal sendiri (hasilnya sama dengan "tanpa skill" di `00-pembanding-tanpa-skill.md`: laba Rp 414.749,50 — salah), lalu pesaing hanya menjalankan `hledger is`/`bs` dan mengembalikan tabel Inggris mentah.

| Kriteria (bobot) | Pesaing ClawHub "Hledger" | Frappe Books | **hledger-usaha** |
|---|---|---|---|
| Catat dari kalimat biasa (20) | 0 — tidak ada | 5 — formulir manual, bukan AI | **19** — 15 transaksi batch, "Artinya:" |
| Ketepatan angka (20) | Bergantung jurnal agent; di simulasi salah | Tepat (double-entry) jika diisi benar | **20** — sama dengan hledger & Decimal sampai sen |
| Impor mutasi bank Indonesia (15) | 0 | 7 — impor CSV umum, perlu pemetaan manual | **14** — BCA/Mandiri otomatis, aturan, uji silang hledger |
| Laporan bahasa Indonesia siap kirim (15) | 2 — tabel Inggris mentah | 8 — GUI, bisa bahasa lain terbatas | **14** — laba rugi/neraca/arus kas Rupiah |
| Keamanan & keandalan tulis (15) | 2 — injeksi shell | 12 — aplikasi desktop | **14** — pratinjau, persetujuan, cadangan, rollback, cek dobel |
| Tanpa setup bagi awam (15) | 5 — butuh hledger + Node | 9 — instal aplikasi | **12** — Python; hledger opsional |
| **Total (100)** | **9** | **41** | **93** |

## Kesimpulan
**hledger-usaha menang telak** atas satu-satunya skill hledger yang ditemukan (pembungkus tipis dengan celah injeksi shell) dan atas skill akuntansi generik. Frappe Books adalah alternatif aplikasi (GUI, AGPL) yang kuat untuk pengguna yang ingin formulir, tetapi tidak dioperasikan AI dan tidak berfokus pada mutasi bank Indonesia. Tidak ada kelebihan pesaing yang perlu diadopsi, kecuali ide Frappe Books untuk invoice — sudah ditangani skill lain (`dolibarr-usaha`).
