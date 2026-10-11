# CLOUD.md — instruksi khusus Cursor Cloud Agent (Akun C)

**Hanya untuk agent yang jalan di Cursor Cloud.** IDE lokal tidak perlu membaca file ini.

## Urutan baca (wajib)

1. **`AGENTS.md`** — peran Akun C, aturan repo untuk agent non-Claude, pointer ke sumber kebenaran.
2. **`.cursor/CLOUD.md`** (file ini) — bootstrap VM, OpenClaw uji, git/PR Cloud, rahasia, Telegram.
3. **`CLAUDE.md`** — baca penuh saat mengerjakan **skill** (Tahap 1–8, lisensi, format SKILL.md, keputusan pemilik). Jangan salin isi CLAUDE.md ke sini; CLAUDE tetap sumber kebenaran pabrik skill.

**Alasan urutan:** AGENTS mengarahkan Cloud; CLOUD berisi ops lingkungan yang tidak ada di IDE lokal; CLAUDE berisi aturan lengkap produksi skill.

---

## Peran & koordinasi

- **Akun C** — agent Cursor Cloud (docs, uji skill, riset ringan). Ambil tugas dari `koordinasi/papan-tugas.md` (bagian *Pembagian jalur*, *SERAH TERIMA Akun B → Akun A*, *Aturan untuk Akun C*). Jangan edit `skills/<nama>` di luar tugasmu.
- **Pembuat ≠ penguji** — satu sesi tidak boleh membuat/merevisi skill **dan** menulis `examples/HASIL-UJI.md`, `00-openclaw-sebelum-sesudah.md`, skor, verdik. Pembuat → `uji`; penguji → `examples/` + skor. Tulis ulang bersih: sesi A hanya daftar ide di `research/sources/`; sesi B tulis skill tanpa membaca sumber. Brief: `koordinasi/alat-uji/brief/`.

---

## Git & PR (Cloud)

| Aturan | Nilai |
|--------|--------|
| Base branch | `claude/claude-code-cli-differences-btizz5` |
| Branch automation (cron) | **`cursor/iterasi-otomatis-akun-c-8b42`** — kanonik; LANGKAH NOL: `git checkout -B …` + merge default bila perlu (`koordinasi/rutin-cursor-cloud.md`) |
| Branch kerja manual / one-off | `cursor/<nama-tugas>-8b42` hanya bila pemilik atau `papan-tugas.md` menulis eksplisit; **jangan** buat `cursor/iterasi-otomatis-akun-c-HHMM` per run |
| Sebelum commit | `python3 scripts/validate.py` harus lolos |
| Pola commit | `skill: …`, `uji: …`, `riset: …`, `docs: …` |
| Push | **Setelah setiap commit `uji:`** → `git push -u origin HEAD` segera (jangan menumpuk uji tanpa push). Commit lain: push minimal **sekali** sebelum run berakhir |
| Akhir run | VM ulang dari snapshot; tanpa push pekerjaan hilang — lihat juga push per-commit uji di atas |
| Pull request | **Jangan buat PR** otomatis setelah uji/testing atau akhir run. Buat PR **hanya** bila pemilik **secara eksplisit** meminta. |
| Merge | Jangan merge PR sendiri |

---

## Bootstrap lingkungan (`.cursor/environment.json`)

Saat run Cloud dimulai, Cursor menjalankan:

```json
"install": "bash koordinasi/alat-uji/setup-cursor.sh"
```

Skrip idempoten membangun di **`$HOME/komunitech-uji`** (default `BASE`):

| Path / alat | Fungsi |
|-------------|--------|
| `$BASE/openclaw-prod` | OpenClaw `@2026.9.8` untuk gateway bot uji |
| `$BASE/openclaw-real/` | HOME bot uji + alat uji |
| `oc.sh` | Pembungkus `openclaw` + `Ninerouter_key` → env bersih |
| `oc-tg.sh` | Sama + `bot_token` (gateway / konteks Telegram) |
| `mk-home.sh` | HOME terpisah per skenario (sebelum / sesudah skill) |
| `uji.sh` | Satu giliran agent lokal → file hasil |
| `uji-tg.sh` | Sama + `--channel telegram` tanpa `--deliver` (pra-cek gelombang) |
| `gw-cek.sh` | Cek/nyalakan gateway bot uji |
| `pilot/tg.py` | Kirim laporan/keputusan ke Telegram |

**Acuan LULUS uji OpenClaw:** skor sesudah ≥ **8** dan selisih rata-rata ≥ **1,5** — detail di `koordinasi/alat-uji/README.md` dan `brief/tester-umum.md`.

**Pisahkan instalasi:** `scripts/uji_openclaw.sh` memakai `/tmp/uji-openclaw` (uji muat skill). **Jangan** arahkan skrip itu ke `openclaw-prod`. Bot produksi (VPS pemilik) **tidak** dipakai untuk uji.

### Fallback `run-uji.sh` (VM Cursor)

`uji.sh` bawaan memakai `unshare` (isolasi mount). Di banyak VM Cursor, `unshare` **gagal** (hak container).

1. Coba dulu: `cd "$HOME/komunitech-uji/openclaw-real" && ./uji.sh …`
2. Jika error terkait `unshare` / user namespace: jalankan uji **setara tanpa isolasi** — HOME uji langsung, perintah inti sama seperti di dalam `uji.sh` (`openclaw agent --local`, `--session-id`, `-m`, `--json`), output ke `$R/hasil/`. Simpan wrapper sebagai `./run-uji.sh` di folder yang sama (tidak di-commit ke repo kecuali tim menstandarkan). Contoh sesi: `reports/2026-10-10-akun-c.md`.

State di `$BASE` **tidak** persist antar run — hasil uji wajib masuk repo (`examples/`, `koordinasi/`) sebelum run berakhir.

---

## Rahasia (environment only)

| Variable | Pemakaian |
|----------|-----------|
| `Ninerouter_key` | Wajib untuk uji sebelum/sesudah (router model) |
| `bot_token` | Opsional; gateway bot penguji & gelombang Telegram |
| `tester_bot_token` | Wajib untuk laporan/progres ke Telegram topik 242 via `pilot/tg.py` (bot penguji, bukan bot OpenClaw) |

- Hanya dari **environment secrets** Cursor (Settings → Cloud Agents → environment). **Jangan** cetak, commit, log, atau tanya ke pemilik.
- Satu token bot = satu gateway polling. Nyalakan gateway hanya lewat **`gw-cek.sh`**. Matikan hanya per PID: `pgrep -f "^openclaw-gateway$"` lalu `kill` — **dilarang** `pkill -f` (bisa membunuh proses penguji).
- Setelah ubah `channels.*` di config bot uji: **restart gateway** (hot reload menolak semua balasan).

---

## Telegram (bot penguji)

- Laporan uji, **progres automation**, & hal yang butuh keputusan pemilik → grup uji, topik **"Ringkasan uji"**: `chat_id=-1004407409583`, `message_thread_id=242`.
- Kirim lewat `pilot/tg.py` (`tester_bot_token`), awali `@nikioktarian`, format keputusan di `CLAUDE.md` (2026-10-03). Nomor keputusan lanjut dari entri terakhir di `koordinasi/` / `reports/`.
- **Automation (jadwal Cloud):** setelah **setiap push** commit uji (dan bila run hanya docs — sekali di akhir), kirim satu pesan ringkas + perbarui [`koordinasi/automation-progress-akun-c.md`](../koordinasi/automation-progress-akun-c.md). Run manual/desktop: laporan tetap ke `reports/YYYY-MM-DD-akun-c.md`.
- **Gelombang tampilan:** hanya setelah persetujuan pemilik; maks. 10 pesan; jeda; tanpa balas-otomatis; topik baru; pra-cek **`uji-tg.sh`** wajib.

---

## Sebelum commit (checklist)

- [ ] `python3 scripts/validate.py` lolos
- [ ] Tes regresi skill terkait lolos
- [ ] Tidak ada `dist/`, data pribadi member/pembeli, atau identitas model di diff
- [ ] `rm -rf` hanya dengan `"${VAR:?}"`

---

## Laporan sesi

Tulis atau tambah bagian di **`reports/YYYY-MM-DD-akun-c.md`** (format ringkas §6 `CLAUDE.md`): progres, tabel skill berubah, PERLU REVIEW, temuan platform, rekomendasi berikutnya.

---

## Iterasi otomatis (Automations)

Pemilik menjadwalkan Akun C lewat **Cursor Automations** (dashboard), bukan API dari agent. **Jadwal disarankan (2026-10-10):** cron **`*/30 * * * *`** UTC (setiap 30 menit, :00 dan :30) — nama *Akun C — iterasi (30 menit)*. Bila **Run History** overlap (uji OpenClaw >30 menit), naikkan ke **`0 * * * *`** atau **`15 */2 * * *`**. Bukan terikat limit 3 jam Claude Code Akun A/B.

Setiap **pemicu automation** = run Cloud Agent baru (`source: automations`); hasil tidak muncul di chat manual — buka Run History atau pantau **git push** + **Telegram 242** + [`automation-progress-akun-c.md`](../koordinasi/automation-progress-akun-c.md).

| Topik | Rincian |
|--------|---------|
| Playbook lengkap | [`koordinasi/rutin-cursor-cloud.md`](../koordinasi/rutin-cursor-cloud.md) — prompt, cron 30 menit, push per commit uji |
| Progres antar-run | [`koordinasi/automation-progress-akun-c.md`](../koordinasi/automation-progress-akun-c.md) — agent wajib perbarui + Telegram setelah push |
| vs Claude | [`koordinasi/rutin.md`](../koordinasi/rutin.md) memakai `create_trigger` di sesi yang sama; Cloud = **run baru tiap jadwal**, VM dari snapshot |
| Buat automation | Cursor → **Automations** → repo Skills → environment + secrets → cron **`*/30 * * * *`** → branch opsional UI = **`cursor/iterasi-otomatis-akun-c-8b42`** → prompt dari rutin-cursor-cloud.md → **Open Pull Request OFF** → Enable → **Run now** |
| Branch legacy | `cursor/iterasi-otomatis-akun-c-*` lama di origin — [`koordinasi/catatan-branch-legacy-automation-akun-c.md`](../koordinasi/catatan-branch-legacy-automation-akun-c.md) |
| API agent | Tidak ada tool buat automation dari run; lookup id: MCP `cursor-cloud` → `get-automation` |
| Push | **Segera setiap commit `uji:`** + push akhir run untuk commit lain; tanpa push pekerjaan hilang saat VM recycle |
| Telegram 242 | Satu pesan ringkas setelah push uji (skor, verdik, branch, commit); format di automation-progress-akun-c.md |
| PR | **Jangan** otomatis; hanya jika pemilik minta eksplisit (sama tabel Git & PR di atas) |
