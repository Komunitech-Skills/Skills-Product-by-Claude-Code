# Progres automation Akun C (Cursor Cloud)

Log ringkas **antar-run** untuk jadwal **Cursor Automations**. Setiap run = VM baru; file ini + git + Telegram topik 242 menjadi sumber kebenaran pemilik (bukan chat automation).

**Pemilik:** baca entri teratas + pesan Telegram thread 242 (`Ringkasan uji`) untuk status tanpa membuka Run History.

**Agent (Akun C):** baca file ini di **LANGKAH NOL**; perbarui setelah **setiap push** (khususnya commit `uji:`).

---

## Cara agent memperbarui

1. Setelah `python3 scripts/validate.py` lolos dan **commit** (terutama `uji: <nama> vX.Y.Z <skor>/10`):
   - **`git push -u origin HEAD` segera** — jangan menunggu akhir run.
2. Tambah baris di tabel **Log run** di bawah (run terbaru di atas).
3. Kirim **satu pesan** ke Telegram topik 242 lewat `koordinasi/alat-uji/pilot/tg.py` (butuh secret `tester_bot_token`), awali `@nikioktarian`:

   ```
   [Akun C auto] <UTC ISO8601 singkat> branch=<cursor/…> commit=<hash pendek> | <1 kalimat: uji selesai skor X/10 verdik … ATAU docs/koordinasi …> | berikutnya: <item papan tugas>
   ```

4. Bila commit uji: sertakan **skor tanpa → dengan**, **verdik** (LULUS/BELUM), **satu kalimat pembeda** (sama format laporan uji `CLAUDE.md` 2026-10-03).
5. Jangan kirim duplikat: bandingkan hash commit terakhir di tabel dengan commit yang baru di-push.

Contoh kirim (dari `$HOME/komunitech-uji/openclaw-real/pilot/` atau path repo `koordinasi/alat-uji/pilot/`):

```bash
cd "$HOME/komunitech-uji/openclaw-real/pilot" 2>/dev/null || cd koordinasi/alat-uji/pilot
python3 tg.py sendMessage chat_id=-1004407409583 message_thread_id=242 text='@nikioktarian [Akun C auto] …'
```

---

## Status automation (isi pemilik setelah buat di UI)

| Field | Nilai |
|--------|--------|
| Nama | `Akun C — iterasi (30 menit)` |
| Cron disarankan | **`*/30 * * * *`** (UTC) — menit :00 dan :30 |
| Overlap run | Bila Run History masih **Running** saat jadwal berikutnya → **`0 * * * *`** (tiap jam) atau **`15 */2 * * *`** |
| Automation UUID | _(isi pemilik dari URL dashboard)_ |
| Playbook | `koordinasi/rutin-cursor-cloud.md` |

---

## Log run

_(Agent: sisipkan baris baru di bawah header tabel; run terbaru paling atas.)_

| UTC (approx) | Branch | Commit | Ringkasan | Telegram 242 |
|--------------|--------|--------|-----------|--------------|
| 2026-10-10 | `cursor/cloud-md-8b42` | `bcd67a55` | Playbook: push per commit uji, Telegram 242, cron 30 menit | manual run docs (no TG) |

---

## Run berikutnya (hint untuk agent)

_(Agent: timpa baris ini setiap akhir run — 1–3 bullet prioritas dari `papan-tugas.md`.)_

- Baca `koordinasi/papan-tugas.md` (Akun C, SERAH TERIMA, Permintaan antar-akun).
- Lanjut branch `cursor/*` aktif atau buat baru dari `claude/claude-code-cli-differences-btizz5`.
