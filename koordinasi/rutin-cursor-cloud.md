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
| Telegram keputusan | Akun A baca `getUpdates`, kirim topik 242 | Akun C: kirim **laporan hasil uji** ke topik 242 bila selesai uji; **gelombang tampilan** hanya setelah persetujuan pemilik |
| Lingkungan uji | Scratchpad Akun A/B | `$HOME/komunitech-uji` via `koordinasi/alat-uji/setup-cursor.sh` (`.cursor/environment.json`) |

**API Cursor:** Cloud Agent MCP hanya **`get-automation`** (lookup by UUID). **Tidak ada** API `create-automation` / `update-automation` yang bisa dipanggil dari run ini — pemilik wajib membuat/mengedit Automation di **dashboard UI**. Daftar **Tools** (mis. **Open Pull Request**) juga **hanya** di UI; API tidak bisa mematikan tool PR otomatis.

---

## Konfigurasi UI (copy-paste)

Gunakan blok ini saat membuat Automation baru di dashboard (sesuai screenshot: tab **Triggers**, **Agent Instructions**, daftar **Tools**).

### Nama

`Akun C — iterasi intensif (1 jam)`

_(Alternatif panjang: `Komunitech Skills — Akun C (iterasi intensif, tiap jam)`.)_

### Repository & environment

| Field | Nilai |
|--------|--------|
| **Repository** | `Komunitech-Skills/Skills-Product-by-Claude-Code` |
| **Base / checkout branch** | `claude/claude-code-cli-differences-btizz5` |
| **Environment** | Environment repo yang menjalankan `koordinasi/alat-uji/setup-cursor.sh` (`.cursor/environment.json`) |
| **Secrets** | `Ninerouter_key` (wajib uji OpenClaw); `bot_token` (opsional, gateway / Telegram) |

Branch awal run: **kosongkan** (biar agent pilih `cursor/*` dari prompt), kecuali satu tugas panjang — isi mis. `cursor/uji-risiko-suksesi-8b42`.

### Triggers (jadwal)

1. Tab **Triggers** → **Add trigger** / **Schedule**.
2. Pilih **Cron** (bukan interval sederhana bila ingin selaras Akun A/B).
3. Ekspresi cron (**default agresif — mode intensif**): **`15 * * * *`**
4. Timezone: **UTC** (bila UI menanyakan).
5. **Enable** trigger setelah automation disimpan.

Arti: menit **15** pasti, **setiap jam** (00:15, 01:15, 02:15, … UTC) — iterasi nonstop selama kuota Cloud Agent masih longgar (mis. push 7 hari sebelum limit habis).

**Overlap run:** bila **Run History** menunjukkan run sebelumnya masih **Running** saat jadwal berikutnya (uji OpenClaw panjang), ganti cron ke **`15 */2 * * *`** (tiap 2 jam, menit 15). Jangan turunkan ke 3 jam kecuali kuota benar-benar ketat — lihat alternatif di [Status saat ini](#status-saat-ini).

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
[MODE INTENSIF — iterasi nonstop selama kuota Cloud tersedia] [Pengingat otomatis — iterasi Komunitech Skills Akun C (Cursor Cloud)] Kamu Akun C (agent Cursor Cloud). Repo: Komunitech-Skills/Skills-Product-by-Claude-Code. Default branch: claude/claude-code-cli-differences-btizz5. Aturan lengkap: baca AGENTS.md, .cursor/CLOUD.md, lalu CLAUDE.md saat mengerjakan skill. Prioritas: iterasi berkelanjutan — ambil item berikutnya dari papan, uji backlog, docs/koordinasi; jangan akhiri run tanpa commit+push bila masih ada pekerjaan yang bisa diselesaikan.

WAJIB BEKERJA setiap run — jangan menjawab "No response requested" atau berhenti tanpa commit bila ada pekerjaan di papan tugas. Setiap run = VM baru; tidak ada memori chat run sebelumnya — andalkan git + koordinasi/papan-tugas.md + reports/YYYY-MM-DD-akun-c.md.

LANGKAH NOL — BACA & GIT: Baca AGENTS.md dan .cursor/CLOUD.md. Jalankan git fetch origin. Baca koordinasi/papan-tugas.md (Akun C, SERAH TERIMA, Permintaan antar-akun). Pilih branch: lanjutkan cursor/* yang sudah dipakai untuk tugas aktif, atau buat cursor/<nama-tugas>-8b42 dari default branch. Merge origin/claude/claude-code-cli-differences-btizz5 bila perlu (merge commit, bukan rebase).

LANGKAH SATU — GATEWAY (hanya jika run ini menguji OpenClaw/Telegram): bash $HOME/komunitech-uji/openclaw-real/gw-cek.sh. Jangan cetak token/kunci. Matikan gateway hanya lewat PID pgrep -f "^openclaw-gateway$". Setelah ubah channels.* di config bot uji, restart gateway sebelum uji Telegram. scripts/uji_openclaw.sh memakai /tmp/uji-openclaw — jangan arahkan ke openclaw-prod. Bot produksi tidak dipakai.

LANGKAH KERJA — PEMBUAT ≠ PENGUJI: Run ini hanya BOLEH salah satu per skill: (A) membuat/merevisi SKILL.md/script/README/catalog, ATAU (B) menulis examples/00-openclaw-sebelum-sesudah.md, 01–04, HASIL-UJI.md, skor. Jangan keduanya untuk skill yang sama dalam satu run kecuali run hanya docs koordinasi tanpa uji skill itu.

Uji (bila ditugaskan): ikuti koordinasi/alat-uji/brief/tester-umum.md — mk-home.sh + uji.sh (fallback run-uji.sh jika unshare gagal, lihat CLOUD.md). uji-tg.sh untuk pra-cek skill panjang/file. Commit uji: uji: <nama> vX.Y.Z <skor>/10. Jangan ubah catalog.csv (Akun A/B yang merge). Laporkan hasil uji ke Telegram topik "Ringkasan uji" (chat_id -1004407409583, thread 242) lewat pilot/tg.py, awali @nikioktarian — hanya laporan uji baru, bukan gelombang tampilan tanpa persetujuan pemilik.

Sebelum commit: python3 scripts/validate.py dan tes regresi skill terkait. Jangan commit dist/, API key, token, data pribadi, identitas model. rm -rf hanya dengan "${VAR:?}".

GIT AKHIR RUN: commit + push wajib (git push -u origin HEAD). Jangan buat PR kecuali pemilik minta eksplisit di instruksi run. Jangan merge PR sendiri.

Laporan: perbarui atau buat reports/YYYY-MM-DD-akun-c.md (format §6 CLAUDE.md): progres, skill berubah, PERLU REVIEW, temuan platform, rekomendasi berikutnya.

Prioritas: (1) uji independen Akun C di papan tugas (mis. S4), (2) draf skill jika ditugaskan, (3) perbarui status di papan-tugas bila selesai item. Berhenti otomatis hanya jika pemilik menulis "stop" di automation prompt atau dashboard disable.

Akhiri run dengan ringkasan singkat Bahasa Indonesia: branch, commit, apa yang selesai / apa yang menunggu run berikutnya.
```

### Setelah simpan

1. **Enable** automation.
2. **Run now** sekali — cek log setup, push ke `origin/cursor/...`, laporan `reports/YYYY-MM-DD-akun-c.md`.
3. Catat **automation id** (UUID dari URL dashboard) di tabel Status di bawah.

---

## Status saat ini

| Item | Rekomendasi | Catatan |
|------|-------------|---------|
| Nama automation | **`Akun C — iterasi intensif (1 jam)`** (lihat [Konfigurasi UI](#konfigurasi-ui-copy-paste)) | Bebas diubah pemilik |
| Jadwal | Cron **`15 * * * *`** (UTC) — menit 15 **setiap jam** (mode intensif) | Overlap di Run History → **`15 */2 * * *`**; kuota ketat → `0 */6 * * *` atau kembali `15 */3 * * *` |
| Repo | `Komunitech-Skills/Skills-Product-by-Claude-Code` (atau URL canonical repo) | Environment Cloud harus punya akses git push |
| Environment | Environment yang sudah menjalankan `setup-cursor.sh` + secrets `Ninerouter_key` (wajib uji), `bot_token` (opsional gateway) | Lihat `.cursor/CLOUD.md` |
| Status | **Aktif** (cron `15 * * * *` UTC) | Automation id: `dec048a2-c487-11f1-ac31-5e2d0494121f` — [dashboard](https://cursor.com/automations/dec048a2-c487-11f1-ac31-5e2d0494121f). Nama UI saat ini: *Untitled* (disarankan ganti ke *Akun C — iterasi intensif (1 jam)*). **Agent Instructions:** salin ulang dari § Agent Instructions di file ini atau `agent-instructions-mode-intensif.txt` di artifact run — Cursor tidak punya API update prompt dari agent. |

---

## Cara membuat Automation (dashboard Cursor — pemilik)

Langkah umum (label menu bisa sedikit berbeda per versi Cursor):

1. Buka **Cursor** → **Automations** (atau **Cloud Agents** → **Automations**).
2. **Create automation** / **New**.
3. **Repository:** pilih repo Skills (branch default checkout = `claude/claude-code-cli-differences-btizz5`, kecuali automation mengizinkan branch awal lain).
4. **Environment:** pilih environment yang memuat `.cursor/environment.json` (install `koordinasi/alat-uji/setup-cursor.sh`) dan secrets (`Ninerouter_key`, `bot_token` bila perlu).
5. **Schedule:** Custom cron → default intensif **`15 * * * *`** (UTC); bila overlap run → **`15 */2 * * *`**. Aktifkan timezone UTC di UI bila ada opsi.
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
5. **Akhir run:** `python3 scripts/validate.py` → **commit + push** wajib (`git push -u origin HEAD`). VM hilang setelah run; tanpa push pekerjaan hilang.
6. **PR:** jangan dibuat agent kecuali pemilik minta di chat/run prompt.

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

## Mode intensif (limit sisa)

**Kapan:** pemilik mengaktifkan push singkat (mis. ~7 hari sebelum kuota/limit Cloud Agent habis) — **bukan** alasan yang sama dengan limit 3 jam Claude Code Akun A/B; ini khusus **Cursor Cloud Agent**.

**Jadwal UI:** cron **`15 * * * *`** (UTC). Lihat [Triggers](#triggers-jadwal) untuk aturan overlap → **`15 */2 * * *`**.

**Perilaku setiap run (wajib):**

1. **Selalu ambil pekerjaan berikutnya** dari `koordinasi/papan-tugas.md` (Akun C, SERAH TERIMA, Permintaan antar-akun) — uji backlog yang `siap diuji`, draf skill bila ditugaskan, perbaikan docs/koordinasi kecil.
2. **Jangan mengakhiri run** tanpa **commit + push** (`git push -u origin HEAD`) bila ada pekerjaan yang bisa diselesaikan atau dilanjutkan (meski sebagian).
3. **Papan kosong / tidak ada baris Akun C:** `git fetch origin` → baca `reports/` terbaru → cek item internal di papan bagian **Permintaan** (promosi, docs, koordinasi) yang boleh Akun C kerjakan tanpa melanggar pembuat≠penguji.
4. **Satu run = satu fokus batch** (satu uji independen, atau satu draf, atau satu paket docs) — jangan campur pembuat+uji skill yang sama kecuali hanya docs tanpa uji skill itu.
5. **PR / gelombang Telegram:** tetap aturan normal — tidak otomatis; gelombang hanya setelah persetujuan pemilik.

**Menjeda intensif:** disable automation atau ganti cron ke `15 */3 * * *` / `0 */6 * * *` setelah push selesai atau kuota menipis.

---

## Prompt Automation Akun C

Salin teks di bawah ke field prompt Automation (versi **2026-10-10**, mode intensif).

```
[MODE INTENSIF — iterasi nonstop selama kuota Cloud tersedia] [Pengingat otomatis — iterasi Komunitech Skills Akun C (Cursor Cloud)] Kamu Akun C (agent Cursor Cloud). Repo: Komunitech-Skills/Skills-Product-by-Claude-Code. Default branch: claude/claude-code-cli-differences-btizz5. Aturan lengkap: baca AGENTS.md, .cursor/CLOUD.md, lalu CLAUDE.md saat mengerjakan skill. Prioritas: iterasi berkelanjutan — ambil item berikutnya dari papan, uji backlog, docs/koordinasi; jangan akhiri run tanpa commit+push bila masih ada pekerjaan yang bisa diselesaikan.

WAJIB BEKERJA setiap run — jangan menjawab "No response requested" atau berhenti tanpa commit bila ada pekerjaan di papan tugas. Setiap run = VM baru; tidak ada memori chat run sebelumnya — andalkan git + koordinasi/papan-tugas.md + reports/YYYY-MM-DD-akun-c.md.

LANGKAH NOL — BACA & GIT: Baca AGENTS.md dan .cursor/CLOUD.md. Jalankan git fetch origin. Baca koordinasi/papan-tugas.md (Akun C, SERAH TERIMA, Permintaan antar-akun). Pilih branch: lanjutkan cursor/* yang sudah dipakai untuk tugas aktif, atau buat cursor/<nama-tugas>-8b42 dari default branch. Merge origin/claude/claude-code-cli-differences-btizz5 bila perlu (merge commit, bukan rebase).

LANGKAH SATU — GATEWAY (hanya jika run ini menguji OpenClaw/Telegram): bash $HOME/komunitech-uji/openclaw-real/gw-cek.sh. Jangan cetak token/kunci. Matikan gateway hanya lewat PID pgrep -f "^openclaw-gateway$". Setelah ubah channels.* di config bot uji, restart gateway sebelum uji Telegram. scripts/uji_openclaw.sh memakai /tmp/uji-openclaw — jangan arahkan ke openclaw-prod. Bot produksi tidak dipakai.

LANGKAH KERJA — PEMBUAT ≠ PENGUJI: Run ini hanya BOLEH salah satu per skill: (A) membuat/merevisi SKILL.md/script/README/catalog, ATAU (B) menulis examples/00-openclaw-sebelum-sesudah.md, 01–04, HASIL-UJI.md, skor. Jangan keduanya untuk skill yang sama dalam satu run kecuali run hanya docs koordinasi tanpa uji skill itu.

Uji (bila ditugaskan): ikuti koordinasi/alat-uji/brief/tester-umum.md — mk-home.sh + uji.sh (fallback run-uji.sh jika unshare gagal, lihat CLOUD.md). uji-tg.sh untuk pra-cek skill panjang/file. Commit uji: uji: <nama> vX.Y.Z <skor>/10. Jangan ubah catalog.csv (Akun A/B yang merge). Laporkan hasil uji ke Telegram topik "Ringkasan uji" (chat_id -1004407409583, thread 242) lewat pilot/tg.py, awali @nikioktarian — hanya laporan uji baru, bukan gelombang tampilan tanpa persetujuan pemilik.

Sebelum commit: python3 scripts/validate.py dan tes regresi skill terkait. Jangan commit dist/, API key, token, data pribadi, identitas model. rm -rf hanya dengan "${VAR:?}".

GIT AKHIR RUN: commit + push wajib (git push -u origin HEAD). Jangan buat PR kecuali pemilik minta eksplisit di instruksi run. Jangan merge PR sendiri.

Laporan: perbarui atau buat reports/YYYY-MM-DD-akun-c.md (format §6 CLAUDE.md): progres, skill berubah, PERLU REVIEW, temuan platform, rekomendasi berikutnya.

Prioritas: (1) uji independen Akun C di papan tugas (mis. S4), (2) draf skill jika ditugaskan, (3) perbarui status di papan-tugas bila selesai item. Berhenti otomatis hanya jika pemilik menulis "stop" di automation prompt atau dashboard disable.

Akhiri run dengan ringkasan singkat Bahasa Indonesia: branch, commit, apa yang selesai / apa yang menunggu run berikutnya.
```

---

## Checklist pemilik setelah run pertama

- [ ] Run selesai tanpa error setup (`setup-cursor.sh` di log environment).
- [ ] Ada push ke `origin/cursor/...`.
- [ ] `python3 scripts/validate.py` lulus di commit terakhir run.
- [ ] Laporan `reports/YYYY-MM-DD-akun-c.md` terupdate.
- [ ] Bila uji OpenClaw: file di `skills/<nama>/examples/` + (opsional) pesan topik 242.
- [ ] **Tidak** ada PR otomatis kecuali diminta.

---

## Pembaruan playbook

Saat mengubah prompt atau jadwal: edit file ini di repo → commit `docs: …` → pull di mesin pemilik → tempel prompt baru di Automation UI. Versi prompt sebut tanggal di commit message atau baris Status di atas.
