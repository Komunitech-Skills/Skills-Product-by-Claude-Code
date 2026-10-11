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

UJI: brief tester-umum.md; uji.sh / run-uji.sh; uji-tg.sh bila perlu. Sebelum commit uji: validate.py + regresi. Commit: uji: <nama> vX.Y.Z <skor>/10. SETELAH COMMIT UJI (wajib): git push -u origin HEAD segera → perbarui koordinasi/automation-progress-akun-c.md (tabel log) → kirim SATU pesan Telegram thread 242 via pilot/tg.py (tester_bot_token). TELEGRAM WAJIB MULTILINE (section + newline): baris1 @nikioktarian, baris2 [Akun C auto], baris kosong, metadata (Waktu UTC / Branch / Commit), blok "Hasil uji" (Skill, Skor tanpa→dengan, Verdik, Pembeda), blok "Berikutnya" (bullet). DILARANG satu baris dengan pemisah | atau ; — salin struktur template persis dari automation-progress-akun-c.md (heredoc/cat, bukan string pipa). Jangan catalog.csv. Bukan gelombang tampilan tanpa persetujuan pemilik.

Run hanya docs/koordinasi: satu commit+push di akhir + SATU pesan Telegram 242 multiline (template "Docs/koordinasi" di automation-progress-akun-c.md) + automation-progress.

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
5. **Setiap commit `uji:`:** `python3 scripts/validate.py` → commit → **`git push -u origin HEAD` segera** → perbarui [`automation-progress-akun-c.md`](automation-progress-akun-c.md) → satu pesan Telegram 242 **multiline** (template Hasil uji — bukan satu baris pipa).
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
3. **Setelah setiap commit `uji:`:** validate → commit → **push segera** → baris log + **Telegram 242 multiline** (template di automation-progress-akun-c.md). Jangan menunggu akhir run untuk push uji.
4. **Run hanya docs:** satu push + satu pesan Telegram **multiline** (template Docs/koordinasi) di akhir run.
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
