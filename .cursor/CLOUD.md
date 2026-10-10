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
| Branch kerja | `cursor/<nama-tugas>-8b42` (satu tugas = satu branch) |
| Sebelum commit | `python3 scripts/validate.py` harus lolos |
| Pola commit | `skill: …`, `uji: …`, `riset: …`, `docs: …` |
| Akhir run (uji/testing atau sesi kerja) | **commit + push** wajib — VM ulang dari snapshot; kerja tidak di-commit hilang |
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

- Hanya dari **environment secrets** Cursor (Settings → Cloud Agents → environment). **Jangan** cetak, commit, log, atau tanya ke pemilik.
- Satu token bot = satu gateway polling. Nyalakan gateway hanya lewat **`gw-cek.sh`**. Matikan hanya per PID: `pgrep -f "^openclaw-gateway$"` lalu `kill` — **dilarang** `pkill -f` (bisa membunuh proses penguji).
- Setelah ubah `channels.*` di config bot uji: **restart gateway** (hot reload menolak semua balasan).

---

## Telegram (bot penguji)

- Laporan uji & hal yang butuh keputusan pemilik → grup uji, topik **"Ringkasan uji"**: `chat_id=-1004407409583`, `message_thread_id=242`.
- Kirim lewat `pilot/tg.py`, awali `@nikioktarian`, format keputusan di `CLAUDE.md` (2026-10-03). Nomor keputusan lanjut dari entri terakhir di `koordinasi/` / `reports/`.
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

Pemilik dapat menjadwalkan Akun C seperti routine Claude Code tiap 3 jam — lewat **Cursor Automations** (dashboard), bukan API dari agent.

| Topik | Rincian |
|--------|---------|
| Playbook lengkap | [`koordinasi/rutin-cursor-cloud.md`](../koordinasi/rutin-cursor-cloud.md) — prompt siap salin, cron, checklist |
| vs Claude | [`koordinasi/rutin.md`](../koordinasi/rutin.md) memakai `create_trigger` di sesi yang sama; Cloud = **run baru tiap jadwal**, VM dari snapshot |
| Buat automation | Cursor → **Automations** → repo Skills → environment dengan `setup-cursor.sh` + secrets → cron (disarankan **`15 */3 * * *`** UTC) → tempel prompt dari rutin-cursor-cloud.md → Enable → uji **Run now** |
| API agent | Tidak ada tool buat automation dari run; hanya dokumentasi UI. Lookup id: MCP `cursor-cloud` → `get-automation` |
| Jadwal | Default **tiap 3 jam** (menit 15 UTC); **`0 */6 * * *`** bila kuota ketat — sama niatnya dengan Akun A/B di rutin.md |
| Branch | Lanjut `cursor/<tugas>-8b42` yang aktif, atau branch baru dari `claude/claude-code-cli-differences-btizz5` — detail di playbook |
| Push | **Wajib** setiap run (`git push -u origin HEAD`); tanpa push pekerjaan hilang saat VM recycle |
| PR | **Jangan** otomatis; hanya jika pemilik minta eksplisit (sama tabel Git & PR di atas) |
