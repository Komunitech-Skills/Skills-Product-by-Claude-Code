# Rutin iterasi — Cursor Cloud Agent (Akun C) via **Cursor Automations**

Playbook untuk pemilik membuat **Automation** di dashboard Cursor yang menjalankan Cloud Agent (Akun C) berkala — setara niatnya dengan `koordinasi/rutin.md` (routine Claude Code tiap 3 jam), tetapi **bukan** `create_trigger` Claude.

> **Cursor Cloud → lihat file ini.** Claude Code Akun A/B → `koordinasi/rutin.md`.

---

## Perbedaan utama vs `rutin.md`

| Aspek | Claude Code (`rutin.md`) | Cursor Cloud (file ini) |
|--------|---------------------------|-------------------------|
| Penjadwal | `create_trigger` / `update_trigger` di sesi Claude | **Cursor Automations** (UI dashboard pemilik) |
| Sesi | Satu sesi panjang; routine memicu giliran di sesi yang sama | **Setiap jadwal = run Cloud Agent baru** (VM/snapshot baru; bukan lanjutan chat sebelumnya) |
| Peran | Akun A / Akun B (semua jalur) | **Akun C** — penguji independen, draf skill bila ditugaskan (`AGENTS.md`, `papan-tugas.md`) |
| Branch | `claude/determined-gates-rh7l38`, `claude/dreamy-archimedes-suxhgj`, dll. | `cursor/<nama-tugas>-8b42` (atau lanjut branch `cursor/*` yang sudah ada untuk tugas yang sama) |
| Base | default branch | `claude/claude-code-cli-differences-btizz5` |
| PR | Akun A/B merge PR default branch berkala | **Jangan buat PR otomatis** — hanya bila pemilik minta eksplisit |
| Context limit | `get_session`, token > 300k / 600k | Tidak ada sesi panjang; tiap run mulai dari snapshot + git |
| Telegram keputusan | Akun A baca `getUpdates`, kirim topik 242 | Akun C: **push per commit uji** + laporan/progres ke topik 242 (`tester_bot_token`, `pilot/tg.py`); log git [`automation-progress-akun-c.md`](automation-progress-akun-c.md); gelombang tampilan hanya setelah persetujuan pemilik |
| Push git | Commit + push berkala | **Push segera setelah setiap commit `uji:`**; commit lain push minimal sekali sebelum run berakhir |
| Lingkungan uji | Scratchpad Akun A/B | `$HOME/komunitech-uji` via `koordinasi/alat-uji/setup-cursor.sh` (`.cursor/environment.json`) |

**API Cursor:** Cloud Agent MCP hanya **`get-automation`** (lookup by UUID). **Tidak ada** API `create-automation` / `update-automation` yang bisa dipanggil dari run ini — pemilik wajib membuat/mengedit Automation di **dashboard UI**. Daftar **Tools** (mis. **Open Pull Request**) juga **hanya** di UI; API tidak bisa mematikan tool PR otomatis.

---

## Konfigurasi UI (copy-paste)

Gunakan blok ini saat membuat Automation baru di dashboard (sesuai screenshot: tab **Triggers**, **Agent Instructions**, daftar **Tools**).

### Nama

`Akun C — iterasi (30 menit)`

_(Alternatif panjang: `Komunitech Skills — Akun C (automation, tiap 30 menit)`.)_

### Repository & environment

| Field | Nilai |
|--------|--------|
| **Repository** | `Komunitech-Skills/Skills-Product-by-Claude-Code` |
| **Base / checkout branch** | `claude/claude-code-cli-differences-btizz5` |
| **Environment** | Environment repo yang menjalankan `koordinasi/alat-uji/setup-cursor.sh` (`.cursor/environment.json`) |
| **Secrets** | `Ninerouter_key` (wajib uji OpenClaw); `tester_bot_token` (wajib laporan/progres Telegram 242); `bot_token` (opsional, gateway OpenClaw / uji-tg) |

Branch awal run: **kosongkan** (biar agent pilih `cursor/*` dari prompt), kecuali satu tugas panjang — isi mis. `cursor/uji-risiko-suksesi-8b42`.

### Triggers (jadwal)

1. Tab **Triggers** → **Add trigger** / **Schedule**.
2. Pilih **Cron** (bukan interval sederhana bila ingin selaras Akun A/B).
3. Ekspresi cron (**default disarankan**): **`*/30 * * * *`**
4. Timezone: **UTC** (bila UI menanyakan).
5. **Enable** trigger setelah automation disimpan.

Arti: **setiap 30 menit** (…:00 dan …:30 UTC) — pemilik memantau lewat push git + Telegram 242 + [`automation-progress-akun-c.md`](automation-progress-akun-c.md), tanpa harus membuka Run History.

**Overlap run:** bila **Run History** menunjukkan run sebelumnya masih **Running** saat jadwal berikutnya (uji OpenClaw panjang), naikkan interval: **`0 * * * *`** (tiap jam) atau **`15 */2 * * *`**. Kuota ketat → `0 */6 * * *`.

Offset dari Akun A (`32 */3`) dan B (`25 */3`) tetap disebar; Akun C bisa lebih sering karena tiap run = VM baru, bukan sesi panjang Claude Code.

### Tools (penting — no auto PR)

Di panel **Tools** / **Agent tools**, sesuaikan dengan playbook:

| Tool | Setting |
|------|---------|
| **Open Pull Request** | **OFF / disabled** — Akun C hanya commit + push; PR hanya bila pemilik minta eksplisit di chat run |
| Shell, Git, Read file, dll. | **ON** — diperlukan untuk uji, validate, push |
| Tool lain | Default OK; jangan aktifkan apa pun yang membuat PR atau merge otomatis |

Cursor **tidak** mengekspos API untuk daftar tool ini; checklist di atas harus dicek manual setiap kali edit automation.

### Model

| Rekomendasi | Kapan |
|-------------|--------|
| **Auto** atau **Claude Sonnet** (tier terbaru yang tersedia di Cloud) | Default automation — uji skill umum, docs, koordinasi, OpenClaw (kecuali hitungan berat) |
| **Opus** (atau model reasoning terkuat) | Run manual sekali-kali bila giliran itu hanya uji skill **pajak/gaji/keuangan/hukum** + verifikasi angka (`CLAUDE.md` §5) |

Jangan andalkan model lemah untuk uji regresi script pajak; jadwalkan Opus lewat **Run now** di minggu itu, bukan mengganti cron.

### Memories

| Setting | Alasan |
|---------|--------|
| **Memories: OFF** | Setiap jadwal = run Cloud Agent **baru** (VM/snapshot baru). Konteks benar ada di **git** (`papan-tugas.md`, `reports/`, branch `cursor/*`). Memories dari chat pemilik bisa salah arahkan prioritas antar-run. |
| Jika UI memaksa Memories ON | Kosongkan / jangan simpan memory khusus automation; andalkan prompt + repo saja |

### Agent Instructions (salin seluruh blok)

Tempel isi **hanya** teks di dalam code fence di bawah ke field **Agent Instructions** (tanpa baris ``` pembuka/penutup).

```
[Pengingat otomatis — iterasi Komunitech Skills Akun C (Cursor Cloud, cron 30 menit)] Kamu Akun C. Repo: Komunitech-Skills/Skills-Product-by-Claude-Code. Default branch: claude/claude-code-cli-differences-btizz5. Baca AGENTS.md, .cursor/CLOUD.md, koordinasi/rutin-cursor-cloud.md, koordinasi/automation-progress-akun-c.md; CLAUDE.md saat mengerjakan skill.

WAJIB BEKERJA setiap run — jangan "No response requested" atau berhenti tanpa commit+push bila ada pekerjaan di papan. Setiap run = VM baru — andalkan git, automation-progress-akun-c.md, papan-tugas.md, reports/YYYY-MM-DD-akun-c.md.

LANGKAH NOL: git fetch origin. Baca papan-tugas (Akun C, SERAH TERIMA, Permintaan antar-akun) + automation-progress-akun-c.md. Branch: lanjut cursor/* aktif atau cursor/<tugas>-8b42 dari default; merge origin/claude/claude-code-cli-differences-btizz5 bila perlu.

GATEWAY (hanya uji OpenClaw/Telegram): gw-cek.sh; jangan cetak secret; restart gateway setelah ubah channels.*; uji_openclaw.sh hanya /tmp/uji-openclaw; bot produksi tidak dipakai.

PEMBUAT ≠ PENGUJI per skill: (A) SKILL/script/README/catalog ATAU (B) examples/ + HASIL-UJI + skor — tidak keduanya skill sama dalam satu run.

UJI: brief tester-umum.md; uji.sh / run-uji.sh; uji-tg.sh bila perlu. Sebelum commit uji: validate.py + regresi. Commit: uji: <nama> vX.Y.Z <skor>/10. SETELAH COMMIT UJI (wajib): git push -u origin HEAD segera → perbarui koordinasi/automation-progress-akun-c.md (tabel log) → kirim Telegram thread 242 via pilot/tg.py (tester_bot_token), awali @nikioktarian, format [Akun C auto] + skor tanpa→dengan + verdik + branch + hash pendek + berikutnya (lihat automation-progress-akun-c.md). Jangan catalog.csv. Bukan gelombang tampilan tanpa persetujuan pemilik.

Run hanya docs/koordinasi: satu commit+push di akhir + satu pesan Telegram 242 + automation-progress.

Jangan commit dist/, secret, data pribadi, identitas model. rm -rf hanya "${VAR:?}". Jangan PR/merge kecuali pemilik minta eksplisit.

Laporan: reports/YYYY-MM-DD-akun-c.md (§6 CLAUDE.md). Prioritas: uji papan → draf bila ditugaskan → status papan. Stop hanya jika pemilik tulis "stop" atau automation disabled.

Akhiri run: ringkasan ID — branch, commit terakhir, push/Telegram sudah atau tidak, item untuk run berikutnya (tulis juga di automation-progress "Run berikutnya").
```

### Setelah simpan

1. **Enable** automation.
2. **Run now** sekali — cek log setup, push ke `origin/cursor/...`, laporan `reports/YYYY-MM-DD-akun-c.md`.
3. Catat **automation id** (UUID dari URL dashboard) di tabel Status di bawah.

---

## Status saat ini

| Item | Rekomendasi | Catatan |
|------|-------------|---------|
| Nama automation | **`Akun C — iterasi (30 menit)`** (lihat [Konfigurasi UI](#konfigurasi-ui-copy-paste)) | Bebas diubah pemilik |
| Jadwal | Cron **`*/30 * * * *`** (UTC) | Overlap → **`0 * * * *`** atau **`15 */2 * * *`**; kuota ketat → `0 */6 * * *` |
| Progres | [`automation-progress-akun-c.md`](automation-progress-akun-c.md) + Telegram **242** | Agent perbarui setelah setiap push commit uji |
| Repo | `Komunitech-Skills/Skills-Product-by-Claude-Code` (atau URL canonical repo) | Environment Cloud harus punya akses git push |
| Environment | `setup-cursor.sh` + `Ninerouter_key`, `tester_bot_token`, `bot_token` (opsional) | Lihat `.cursor/CLOUD.md` |
| Status | **Belum diaktifkan** — pemilik buat di dashboard | Setelah dibuat, catat automation id di `automation-progress-akun-c.md` dan baris bawah tabel ini |

_(Isi baris automation id setelah pemilik membuat di UI: `…`)_

---

## Cara membuat Automation (dashboard Cursor — pemilik)

Langkah umum (label menu bisa sedikit berbeda per versi Cursor):

1. Buka **Cursor** → **Automations** (atau **Cloud Agents** → **Automations**).
2. **Create automation** / **New**.
3. **Repository:** pilih repo Skills (branch default checkout = `claude/claude-code-cli-differences-btizz5`, kecuali automation mengizinkan branch awal lain).
4. **Environment:** pilih environment yang memuat `.cursor/environment.json` (install `koordinasi/alat-uji/setup-cursor.sh`) dan secrets (`Ninerouter_key`, `bot_token` bila perlu).
5. **Schedule:** Custom cron → default **`*/30 * * * *`** (UTC); bila overlap run → **`0 * * * *`** atau **`15 */2 * * *`**. Aktifkan timezone UTC di UI bila ada opsi.
6. **Prompt / Instructions:** salin **seluruh** blok di bagian [Prompt Automation Akun C](#prompt-automation-akun-c) di bawah (tanpa pembungkus markdown code fence di UI — hanya teks prompt).
7. **Branch (opsional):** kosongkan agar agent memilih branch dari prompt; atau isi branch kerja tetap hanya bila satu skill panjang (mis. `cursor/uji-risiko-suksesi-8b42`).
8. Simpan, **Enable** automation. Uji sekali dengan **Run now** / manual trigger.
9. Verifikasi: run muncul di daftar Cloud Agents; ada commit push di branch `cursor/*`; laporan `reports/YYYY-MM-DD-akun-c.md` terbarui.

**Menjeda:** disable automation di dashboard (setara `enabled: false` di Claude).

**Memperbarui prompt:** edit prompt automation → salin versi terbaru dari repo (`git pull` dulu di mesin pemilik) dari file ini.

---

## Strategi branch (setiap run)

1. **`git fetch origin`** — selalu di awal giliran.
2. **Tugas baru** (skill/docs terpisah): `git checkout -b cursor/<nama-singkat>-8b42` dari `origin/claude/claude-code-cli-differences-btizz5`.
3. **Lanjut tugas yang sama** (uji belum selesai, PR belum di-merge): checkout branch `cursor/*` yang sudah dipakai run sebelumnya (cek `papan-tugas.md`, laporan terakhir, atau `git branch -r 'origin/cursor/*'`).
4. **Sync base:** bila default branch maju, `git merge origin/claude/claude-code-cli-differences-btizz5` (merge commit, bukan rebase) sebelum kerja besar; selesaikan konflik di luar `skills/` milik akun lain bila memungkinkan.
5. **Setiap commit `uji:`:** `python3 scripts/validate.py` → commit → **`git push -u origin HEAD` segera** → perbarui [`automation-progress-akun-c.md`](automation-progress-akun-c.md) → satu pesan Telegram 242 (format di file itu).
6. **Akhir run:** push commit lain yang belum ter-push; VM hilang setelah run; tanpa push pekerjaan hilang.
7. **PR:** jangan dibuat agent kecuali pemilik minta di chat/run prompt.

---

## Prioritas kerja Akun C (ringkas)

Ambil hanya dari **`koordinasi/papan-tugas.md`**: bagian *Pembagian jalur* (Akun C), *SERAH TERIMA Akun B → Akun A* (item yang ditugaskan ke Akun C, mis. S4 uji), *Aturan untuk Akun C*, *Permintaan antar-akun*.

Urutan disarankan per giliran (satu run = satu batch fokus):

1. Selesaikan **uji independen** yang statusnya `siap diuji` / ditugaskan ke Akun C (hanya folder `skills/<nama>/examples/`, brief `koordinasi/alat-uji/brief/`).
2. **Draf skill** bila ada baris eksplisit untuk Akun C (pembuat ≠ penguji — run berikutnya atau sesi lain yang uji).
3. **Docs/koordinasi** kecil (mis. perbarui papan-tugas status) bila tidak ada uji antre.
4. Jangan ambil jalur Akun A/B (kurasi massal, solusi-vip, gelombang Telegram tanpa persetujuan, merge default branch).

Acuan lulus uji OpenClaw: sesudah ≥ **8** dan selisih ≥ **1,5** (`koordinasi/alat-uji/README.md`).

---

## Mode iterasi (30 menit)

**Kapan:** automation aktif — pemantauan pemilik lewat **push git**, **Telegram 242**, dan [`automation-progress-akun-c.md`](automation-progress-akun-c.md) (bukan reply chat automation).

**Jadwal UI:** cron **`*/30 * * * *`** (UTC). Lihat [Triggers](#triggers-jadwal) untuk overlap → **`0 * * * *`**.

**Perilaku setiap run (wajib):**

1. **LANGKAH NOL:** baca `automation-progress-akun-c.md` + `papan-tugas.md` + `git fetch`.
2. **Selalu ambil pekerjaan berikutnya** — uji backlog `siap diuji`, draf skill bila ditugaskan, docs/koordinasi kecil.
3. **Setelah setiap commit `uji:`:** validate → commit → **push segera** → baris log + **Telegram 242** (lihat automation-progress-akun-c.md). Jangan menunggu akhir run untuk push uji.
4. **Run hanya docs:** satu push + satu pesan Telegram di akhir run.
5. **Satu run = satu fokus batch** — pembuat≠penguji per skill.
6. **PR / gelombang:** tidak otomatis; gelombang hanya setelah persetujuan pemilik.

**Menjeda:** disable automation atau perlambat cron (`0 * * * *`, `0 */6 * * *`) bila overlap atau kuota menipis.

---

## Prompt Automation Akun C

Salin teks di bawah ke field prompt Automation (versi **2026-10-10**, cron **30 menit**). Isi identik dengan [Agent Instructions](#agent-instructions-salin-seluruh-blok) di atas.

---

## Checklist pemilik setelah run pertama

- [ ] Run selesai tanpa error setup (`setup-cursor.sh` di log environment).
- [ ] Ada push ke `origin/cursor/...`.
- [ ] `python3 scripts/validate.py` lulus di commit terakhir run.
- [ ] Laporan `reports/YYYY-MM-DD-akun-c.md` terupdate.
- [ ] Bila uji OpenClaw: file di `skills/<nama>/examples/` + **push segera** + pesan topik 242 + baris di `automation-progress-akun-c.md`.
- [ ] **Tidak** ada PR otomatis kecuali diminta.

---

## Pembaruan playbook

Saat mengubah prompt atau jadwal: edit file ini di repo → commit `docs: …` → pull di mesin pemilik → tempel prompt baru di Automation UI. Versi prompt sebut tanggal di commit message atau baris Status di atas.


---

## Prompt pendek alternatif untuk dashboard (disarankan sejak 2026-10-13)

Agar pemilik tidak perlu menyalin ulang blok panjang setiap ada perubahan, field **Agent Instructions** di dashboard cukup diisi teks pendek ini; isi lengkapnya dibaca agent dari repo di awal tiap run:

```
Kamu Akun C (Cursor Cloud, penguji independen) untuk repo Komunitech-Skills/Skills-Product-by-Claude-Code. Di awal run: git fetch origin; checkout branch cursor/iterasi-otomatis-akun-c-8b42 (buat dari default claude/claude-code-cli-differences-btizz5 bila belum ada) lalu merge origin/claude/claude-code-cli-differences-btizz5. Buka koordinasi/rutin-cursor-cloud.md dan jalankan PERSIS blok kode di bawah judul "Agent Instructions — versi koreksi Akun B" versi terbaru (termasuk LANGKAH NOL pengaman tumpang tindih, urutan tugas, aturan keamanan). Papan tugas: koordinasi/papan-tugas.md. Jangan cetak secret. Akhiri dengan ringkasan singkat berbahasa Indonesia.
```

## Agent Instructions — versi koreksi Akun B (2026-10-13), pakai ini di dashboard (atau prompt pendek di atas)

Perubahan 2026-10-13 (keputusan otomatis no. 55): C6, C7, C9, C11 selesai; tugas aktif Akun C sekarang **C12** (audit & lengkapi materi jualan README untuk daftar skill di papan C12 — checklist Tahap 8 CLAUDE.md; jangan ubah SKILL.md/catalog/versi/angka uji; validate.py lolos; commit `docs: README jualan <n> skill (C12)`), sebelum C8.
Perubahan 2026-10-12 (keputusan pemilik no. 28 + aturan paralel usulan Cursor, disetujui pemilik): urutan kerja C6 → C7 → C9 batch hingga 3 skill/run (uji ulang skill `beta` di konteks Telegram, lokal) → C8; gelombang Telegram 13 dst. dikirim Akun B dengan bot kedua (@KTclaude2bot), Akun C tidak membuat topik G13+ dan tetap memakai bot pertama (@KTclaude1_bot). Perubahan sebelumnya dari versi 30 menit: interval 1 jam (keputusan pemilik 2026-10-12); cek secret di awal; baca & jalankan jawaban pemilik di topik 242; larangan mengulang uji skill yang sudah `lulus`; satu pesan Telegram per run (tanpa blok persen); tidak ada commit/pesan bila tidak ada perubahan nyata; maksimal satu skill diuji per run.

```
[Iterasi otomatis Akun C — Cursor Cloud, tiap 30 menit, v2026-10-13] Kamu Akun C (penguji independen). Repo Komunitech-Skills/Skills-Product-by-Claude-Code; default branch claude/claude-code-cli-differences-btizz5. Baca AGENTS.md, .cursor/CLOUD.md, koordinasi/rutin-cursor-cloud.md, koordinasi/automation-progress-akun-c.md, koordinasi/papan-tugas.md (bagian Akun C, SERAH TERIMA, Permintaan antar-akun); CLAUDE.md saat menyentuh skill. Setiap run = VM baru; andalkan git + berkas koordinasi.

LANGKAH NOL — pengaman tumpang tindih: baca baris terakhir koordinasi/automation-progress-akun-c.md; bila berumur < 30 menit dan belum ada baris "selesai" untuk run itu, BERHENTI sekarang tanpa commit/pesan (run sebelumnya masih berjalan). Setiap run menulis baris "mulai <UTC>" di awal dan "selesai <UTC>" di akhir. Lalu secret & branch: `test -n "${Ninerouter_key:-}" && echo KEY_SET; test -n "${bot_token:-}" && echo BOT_SET; test -n "${tester_bot_token:-}" && echo TESTER_SET` (jangan cetak nilai). Tanpa KEY_SET: jangan menguji; catat satu baris di automation-progress dan berhenti. git fetch origin; checkout SELALU branch kanonik cursor/iterasi-otomatis-akun-c-8b42 (buat dari default bila belum ada), lalu merge origin/claude/claude-code-cli-differences-btizz5 (merge commit, bukan rebase). DILARANG branch baru per run.

LANGKAH SATU — jawaban pemilik: bila TESTER_SET, baca balasan pemilik di Telegram topik 242 lewat getUpdates (hanya baca; jangan offset=-1). Keputusan yang sudah dijawab dijalankan lebih dulu dari tugas lain dan dicatat di papan tugas. Keputusan baru diusulkan dengan nomor lanjutan (ringkasan bernomor + rekomendasi + alasan).

LANGKAH DUA — kerja, urut prioritas (keputusan pemilik no. 26–28, 2026-10-12, aturan paralel disetujui pemilik 2026-10-12):
Urutan: (1) C6 pilot G11b 4 pesan (tangani-keberatan-pelanggan + kelayakan-investasi-usaha, topik baru, sudah disetujui) → (2) C7 gelombang 12 = 10 pesan (msgs-g12.json, topik baru lewat mktopics-g12.py, sudah disetujui) bila C6 selesai → (2c) C11 uji `cari-prospek-web` 2 pesan di bot pertama dengan web_search hidup (lihat papan C11) → (3) C9 batch uji ulang skill `beta` di konteks Telegram bila tidak ada gelombang aktif → (4) **C12 audit materi jualan README (Tahap 8) — daftar skill di papan C12, maks 8 skill per run, boleh 3 subagent paralel; JANGAN menyentuh skill di luar daftar C12 (Akun B mengerjakan skill bundle lain secara paralel)** → (5) C8 draf skill baru bila syarat terpenuhi → (6) tugas lain di papan untuk Akun C.
Aturan paralel:
- C6 dan C7: SERIAL saja — satu run boleh lanjut C6 lalu C7 bila waktu/kuota cukup; restart gateway sebelum kirim; jeda antar pesan; tanpa balas-otomatis.
- C9 (run-uji-tg.sh LOKAL, tanpa mengirim): dalam SATU run boleh uji hingga 3 skill BERBEDA, urut prioritas catalog (skill yang hasilnya berupa file/jawaban panjang dulu, lalu skor tertinggi); boleh paralel via subagent (maks 3 subagent, tetapi maks 2 proses run-uji-tg.sh berjalan bersamaan agar router tidak timeout) asal tiap subagent hanya membaca satu folder skills/<nama>/ dan hanya menulis koordinasi/pracek-telegram-beta-<tanggal>.md + catatan papan — tanpa ubah SKILL.md/catalog. Setelah semua selesai: SATU commit+push (`uji: batch C9 <tanggal> <n> skill`) + SATU pesan Telegram multiline (ringkas per skill: LOLOS/GAGAL + alasan satu kalimat). Skill GAGAL dicatat di papan tugas (Permintaan antar-akun) untuk diperbaiki akun lain.
- C8 SELESAI (ubah-draf-ke-dokumen & kartu-belajar-anki lulus, jadwal-pelajaran-sekolah arsip): JANGAN membuat draf skill baru (keputusan pemilik no. 28: rilis yang ada, bukan skill baru) kecuali papan tugas menambah baris C8 baru.
- C12 (audit README jualan): maks 8 skill per run dari daftar C12 di papan, boleh 3 subagent paralel (tiap subagent hanya menulis README skill yang ditugaskan). Audit harus MENDALAM, bukan hanya rujukan instalasi: setiap README wajib berakhir dengan blok `**Hasil uji (angka nyata):**` (skor tanpa → dengan skill + sumber berkas uji; jangan mengarang) dan baris `**Status uji (jujur):**` sesuai `platform_teruji`; lengkapi juga judul ≤ 8 kata, 3–5 manfaat, Cocok untuk siapa, Cara pakai, tabel 4 platform, FAQ 3, disclaimer domain sensitif, atribusi skill kurasi. Batch 1 (8 skill, 03:34 UTC) diulang untuk butir Hasil uji. Cek sendiri sebelum commit: `grep -L 'Hasil uji (angka nyata)' skills/<nama>/README.md` kosong. Tulis skill selesai di `koordinasi/c12-readme-progress.md`; SATU commit `docs: README jualan <n> skill (C12)` + push; pesan Telegram 242 satu baris ringkas (jumlah skill, sisa).
- Selain C9: tetap MAKSIMAL SATU skill uji ATAU SATU draf per run.
Gelombang Telegram 13 dan seterusnya dikirim Akun B dengan bot kedua (@KTclaude2bot; C10 dicabut): JANGAN membuat topik G13+, jangan menguji ulang skill `lulus` kecuali versinya naik di catalog atau papan tugas memintanya. Pembuat ≠ penguji per skill. Acuan LULUS: sesudah ≥ 8 DAN selisih ≥ 1,5; di bawah itu tidak diiterasi, usulkan arsip.

GATEWAY (hanya bila perlu Telegram/uji-tg): gw-cek.sh; restart gateway setelah ubah channels.*; uji_openclaw.sh hanya /tmp/uji-openclaw; bot produksi tidak dipakai; jangan pernah cetak secret.

SETELAH UJI: validate.py + regresi lolos → commit `uji: <nama> vX.Y.Z <skor>/10` → push → tambah baris di automation-progress-akun-c.md dan reports/YYYY-MM-DD-akun-c.md → SATU pesan Telegram topik 242 (multiline: @nikioktarian, [Akun C auto], waktu UTC, branch, commit, lalu Hasil uji: skill, skor tanpa→dengan, verdik, satu kalimat pembeda, lalu Berikutnya). Tanpa blok persen/skala.

BILA TIDAK ADA PERUBAHAN NYATA (tidak ada uji, tidak ada keputusan, tidak ada tugas): berhenti tanpa commit, tanpa pesan Telegram; cukup satu baris di automation-progress bila berguna. Jangan commit "hash log" atau dokumen yang hanya mengulang isi lama.

Jangan commit dist/, secret, data pribadi, identitas model. rm -rf hanya "${VAR:?}". Jangan PR/merge kecuali pemilik minta eksplisit. Berhenti hanya bila pemilik menulis "stop" atau automation dimatikan. Akhiri run dengan ringkasan singkat berbahasa Indonesia: branch, commit terakhir, push/Telegram terkirim atau tidak, item run berikutnya.
```

Cron di dashboard (keputusan otomatis no. 31, 2026-10-12, atas pertanyaan pemilik): **`*/30 * * * *`** (tiap 30 menit, UTC). Nama automation: `Akun C — iterasi (30 menit)`. **Pengaman wajib:** di LANGKAH NOL, bila baris terakhir `automation-progress-akun-c.md` berumur < 30 menit dan belum ada baris "selesai" untuk run itu, run baru BERHENTI tanpa commit dan tanpa pesan. Gelombang (C7) boleh melewati batas 30 menit; run berikutnya akan berhenti sendiri karena pengaman.
