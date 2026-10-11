# Progres automation Akun C (Cursor Cloud)

Log ringkas **antar-run** untuk jadwal **Cursor Automations**. Setiap run = VM baru; file ini + git + Telegram topik 242 menjadi sumber kebenaran pemilik (bukan chat automation).

**Pemilik:** baca entri teratas + pesan Telegram thread 242 (`Ringkasan uji`) untuk status tanpa membuka Run History.

**Agent (Akun C):** baca file ini di **LANGKAH NOL**; perbarui setelah **setiap push** (khususnya commit `uji:`).

**Branch kanonik (run automation/jadwal):** `cursor/iterasi-otomatis-akun-c-8b42` — tulis branch ini di metadata Telegram dan kolom Branch tabel log kecuali papan-tugas/chat pemilik menetapkan branch one-off. Jangan buat branch `cursor/iterasi-otomatis-akun-c-HHMM` per run.

---

## Dashboard antrean Akun C

Jalankan sebelum kirim Telegram (rollup run atau setelah commit `uji:`):

```bash
bash koordinasi/alat-uji/progress-akun-c.sh
```

| Metrik | Nilai (contoh — jalankan script untuk angka live) |
|--------|-----------------------------------------------------|
| **Antrean** | **12/17 (71%)** ← `selesai/total` dari papan |
| Selesai | 12 |
| Sedang | 0 |
| Tersisa | 5 |
| **Skala TG** | **71/100** ← `persen` selesai (bukan 100 item) |

### Apa yang dihitung (sumber: `koordinasi/papan-tugas.md`)

1. **Tabel `## Tugas Akun C`** — baris `C1`…`Cn`; status kolom terakhir (`selesai` / `sedang` / `belum`…).
2. **`## Antrean uji Akun C`** — baris `- [x]` selesai, `- [~]` sedang, `- [ ]` tersisa.
3. **`## Permintaan antar-akun — progress Akun C`** — checkbox yang sama.

**Bukan** seluruh papan (Akun A/B, U1–U22, S1–S9) — hanya antrean yang ditugaskan ke Akun C.

### Cara memperbarui hitungan

| Aksi | Di mana |
|------|---------|
| Uji skill selesai | Centang `- [x]` di **Antrean uji** atau tulis `selesai` di baris `Cn` |
| Sedang dikerjakan run ini | `- [~]` atau status `dikerjakan (Akun C, …)` |
| Item manual / luar papan | Tambah baris di tabel **Override manual** di bawah (opsional) |

### Override manual (opsional)

| id | status |
|----|--------|
| _(contoh: gelombang-tg-12)_ | tersisa |

---

## Cara agent memperbarui

1. Setelah `python3 scripts/validate.py` lolos dan **commit** (terutama `uji: <nama> vX.Y.Z <skor>/10`):
   - **`git push -u origin HEAD` segera** — jangan menunggu akhir run.
2. Tambah baris di tabel **Log run** di bawah (run terbaru di atas).
3. Kirim **satu pesan multiline** ke Telegram topik 242 lewat `koordinasi/alat-uji/pilot/tg.py` (butuh secret `tester_bot_token`).

   **Aturan format (wajib — supaya tidak berantakan di Telegram):**

   - **Dilarang** format satu baris dengan pemisah `|` (pipe), `;`, atau koma runtut untuk menggantikan baris baru.
   - **Wajib** baris pertama: `@nikioktarian` (tanpa teks lain di baris itu).
   - **Wajib** baris kedua: `[Akun C auto]` saja.
   - **Wajib** baris kosong setelah tag, lalu **blok metadata** (satu field per baris), lalu **blok isi** dengan judul section di baris sendiri, lalu **blok Berikutnya**.
   - Gunakan **newline sungguhan** (`\n` / heredoc), bukan literal `\n` di dalam satu baris panjang.
   - Skor pakai koma desimal Indonesia (`8,5`), panah `→` untuk tanpa → dengan.

4. **Sebelum** kirim Telegram: `bash koordinasi/alat-uji/progress-akun-c.sh` — salin baris **Antrian** ke blok **Progress** (template di bawah).
5. Bila commit **`uji:`**: pakai template **Hasil uji** di bawah (skor tanpa → dengan, verdik LULUS/BELUM/GAGAL, satu kalimat pembeda — sama `CLAUDE.md` 2026-10-03).
6. Bila run **hanya docs/koordinasi** (tanpa commit `uji:`): pakai template **Docs/koordinasi** atau **Ringkasan run**; kirim **sekali** di akhir run setelah push.
7. Jangan kirim duplikat: bandingkan hash commit terakhir di tabel dengan commit yang baru di-push.

### Template Telegram — commit `uji:` (salin struktur, ganti placeholder)

```
@nikioktarian
[Akun C auto]

Waktu (UTC): YYYY-MM-DDTHH:MMZ
Branch: cursor/iterasi-otomatis-akun-c-8b42
Commit: <hash 7 char>

Progress
Antrian: <selesai>/<total> (<persen>%)
Selesai: <n> | Sedang: <n> | Tersisa: <n>
Skala: <persen>/100

Hasil uji
Skill: <nama-skill> vX.Y.Z
Skor: tanpa <n,n>/10 → dengan <n,n>/10
Verdik: LULUS | BELUM | GAGAL
Pembeda: <satu kalimat konkret beda tanpa vs dengan skill>

Berikutnya
- <1–3 bullet dari papan-tugas.md>
```

### Template Telegram — docs/koordinasi (satu pesan di akhir run)

```
@nikioktarian
[Akun C auto]

Waktu (UTC): YYYY-MM-DDTHH:MMZ
Branch: cursor/iterasi-otomatis-akun-c-8b42
Commit: <hash 7 char>

Progress
Antrian: <selesai>/<total> (<persen>%)
Selesai: <n> | Sedang: <n> | Tersisa: <n>
Skala: <persen>/100

Docs/koordinasi
Ringkasan: <1–2 kalimat apa yang diubah>
File utama: <path relatif, mis. koordinasi/…>

Berikutnya
- <1–3 bullet prioritas run berikutnya>
```

### Template Telegram — ringkasan akhir run (rollup, tanpa commit uji)

```
@nikioktarian
[Akun C auto]

Waktu (UTC): YYYY-MM-DDTHH:MMZ
Branch: cursor/iterasi-otomatis-akun-c-8b42
Commit: <hash 7 char>

Progress
Antrian: <selesai>/<total> (<persen>%)
Selesai: <n> | Sedang: <n> | Tersisa: <n>
Skala: <persen>/100

Ringkasan run
<1–3 kalimat: branch, commit, uji/docs, push>

Berikutnya
- <1–3 bullet dari papan-tugas.md>
```

### Contoh kirim (multiline — disarankan)

Dari `$HOME/komunitech-uji/openclaw-real/pilot/` atau `koordinasi/alat-uji/pilot/`:

```bash
cd "$HOME/komunitech-uji/openclaw-real/pilot" 2>/dev/null || cd koordinasi/alat-uji/pilot

MSG="$(cat <<'EOF'
@nikioktarian
[Akun C auto]

Waktu (UTC): 2026-10-11T06:30Z
Branch: cursor/iterasi-otomatis-akun-c-8b42
Commit: abc1234

Progress
Antrian: 12/17 (71%)
Selesai: 12 | Sedang: 0 | Tersisa: 5
Skala: 71/100

Hasil uji
Skill: contoh-skill v1.0.0
Skor: tanpa 6,2/10 → dengan 8,5/10
Verdik: LULUS
Pembeda: Dengan skill, output punya tabel Rupiah dan langkah terurut; tanpa skill hanya paragraf umum.

Berikutnya
- Uji skill berikutnya di papan (status siap diuji)
EOF
)"

python3 tg.py sendMessage chat_id=-1004407409583 message_thread_id=242 "text=${MSG}"
```

**Jangan** memakai `text='@nikioktarian [Akun C auto] branch=… | …'` — itu format lama yang membuat pesan sulit dibaca di HP.

---

## Status automation (isi pemilik setelah buat di UI)

| Field | Nilai |
|--------|--------|
| Nama | `Akun C — iterasi (30 menit)` |
| Cron disarankan | **`*/30 * * * *`** (UTC) — menit :00 dan :30 |
| Overlap run | Bila Run History masih **Running** saat jadwal berikutnya → **`0 * * * *`** (tiap jam) atau **`15 */2 * * *`** |
| Automation UUID | _(isi pemilik dari URL dashboard)_ |
| Playbook | `koordinasi/rutin-cursor-cloud.md` |
| Branch kanonik | **`cursor/iterasi-otomatis-akun-c-8b42`** (field branch opsional di UI Automation) |

---

## Log run

_(Agent: sisipkan baris baru di bawah header tabel; run terbaru paling atas.)_

| UTC (approx) | Branch | Commit | Ringkasan | Telegram 242 |
|--------------|--------|--------|-----------|--------------|
| 2026-10-11 | `cursor/cloud-md-8b42` | `d7ed8425` | Progress dashboard: `progress-akun-c.sh`, blok Progress di template TG | ya (setelah push) |
| 2026-10-11 | `cursor/cloud-md-8b42` | `c6859ed4` | Template Telegram multiline (section, bukan pipe satu baris) + Agent Instructions | ya (setelah push) |
| 2026-10-10 | `cursor/cloud-md-8b42` | `bcd67a55` | Playbook: push per commit uji, Telegram 242, cron 30 menit | manual run docs (no TG) |

---

## Run berikutnya (hint untuk agent)

_(Agent: timpa baris ini setiap akhir run — 1–3 bullet prioritas dari `papan-tugas.md`.)_

- Uji ulang `cari-prospek-web` v1.0.2 (antrean `- [ ]`, keputusan 24 tahap 2).
- Pemilik: tempel ulang **Agent Instructions** (branch kanonik + LANGKAH NOL checkout `-B`); set field branch UI = `cursor/iterasi-otomatis-akun-c-8b42`.
- Backlog `siap diuji` berikutnya yang ditugaskan ke Akun C di papan/catalog.
