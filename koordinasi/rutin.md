# Routine (jadwal otomatis) — templat untuk Akun A & Akun B

Routine membuat sesi Claude Code melanjutkan kerja sendiri tiap beberapa jam, tanpa menunggu pemilik mengetik.
Routine hanya bisa dibuat **oleh sesi itu sendiri** (akun lain tidak bisa membuatkannya).

## Status saat ini
| Akun | Routine | Jadwal | Status |
|---|---|---|---|
| Akun A | "Lanjutkan iterasi Komunitech Skills (tiap 3 jam)" | `32 */3 * * *` (UTC) | **dijeda** 2026-09-26 (limit Akun A hampir habis; semua kerja diserahkan ke Akun B) |
| Akun B | "Lanjutkan iterasi Komunitech Skills Akun B (tiap 3 jam)" | `25 */3 * * *` (UTC, disebar server dari `0 */3`) | **aktif** sejak 2026-09-26 (dibuat sesi Akun B) |

## Cara membuat (Akun B)
Di sesi Akun B, minta Claude: *"Buat routine sesuai `koordinasi/rutin.md` bagian Akun B."* Claude memakai tool
`create_trigger` (server claude-code-remote) dengan:
- **name:** `Lanjutkan iterasi Komunitech Skills Akun B (tiap 3 jam)`
- **cron_expression:** `0 */3 * * *` (menit 0 → server menyebarkannya otomatis; ganti ke `0 */6 * * *` bila limit ketat)
- **target:** sesi ini sendiri (default, tanpa `persistent_session_id` dan tanpa `create_new_session_on_fire`)
- **initiation:** `human_request`
- **prompt:** teks di bawah, persis.

Menjeda/menghidupkan lagi: `update_trigger` dengan `enabled: false` / `true`.

### Prompt routine Akun B
```
[Pengingat otomatis tiap 3 jam — atas permintaan pemilik] Kamu Akun B dan kini memegang SEMUA pekerjaan: JALUR 1 (kurasi & kreasi skill), JALUR 2 (produk siap pakai pengganti SaaS yang jalan lokal), JALUR 3 (solusi member VIP OpenClaw), uji independen, dan serah terima Akun A (H1–H6 di koordinasi/papan-tugas.md).

LANGKAH PERTAMA — CEK CONTEXT & LIMIT: panggil get_session (tanpa session_id) dan baca external_metadata.context_usage (used_tokens / max_tokens) serta rate_limit_info.
- > 300.000 token: di awal balasan tulis satu baris ke pemilik, mis. "Context sesi sudah ±X ribu token — sebaiknya jalankan /compact saat sempat." Lalu lanjut kerja.
- > 600.000 token: jangan mulai batch baru; selesaikan & commit pekerjaan yang sedang berjalan, lalu minta pemilik menjalankan /compact.
- rate_limit_info.status = "rejected": jangan mulai agent baru; laporkan singkat kapan limit reset.

LANGKAH KEDUA — KOORDINASI: `git fetch origin`; baca koordinasi/papan-tugas.md (bagian SERAH TERIMA Akun A → Akun B, antrean U, dan Permintaan antar-akun). Bila branch Akun A (claude/determined-gates-rh7l38) punya commit baru, gabungkan ke branch ini dengan merge commit (bukan rebase), selesaikan konflik catalog.csv/laporan, jalankan validate.py, push.

LANGKAH KERJA: jika agent dari giliran sebelumnya masih berjalan, JANGAN mulai duplikat — proses hasil yang sudah masuk. Lanjutkan agent yang terhenti karena limit (SendMessage). Urutan prioritas: (1) revisi H1–H3 lalu uji ulang, (2) antrean uji U yang "siap diuji", (3) H4 solusi-vip, (4) skill/produk baru dari research/backlog.md dan research/software-pengganti-saas-*.md. Pembuat revisi dan penguji WAJIB sub-agent berbeda; pembuat tidak menulis examples/HASIL-UJI.md. Untuk tiap skill: tes unit, validate.py, scripts/uji_openclaw.sh, commit `skill: <nama> (<status>)` & push. Skill lulus: isi status/skor/platform_teruji dan tier_final/harga_final_idr = usulan di catalog.csv. Buat & merge PR pembaruan default branch (claude/claude-code-cli-differences-btizz5) secara berkala setelah validate.py lulus di worktree bersih.

MAKSIMAL 4 AGENT PARALEL. PILIH MODEL AGENT (CLAUDE.md bagian 5): Opus untuk pajak/gaji/keuangan/hukum + verifikasi angka/uji A/B/banding pesaing; Sonnet untuk marketing/konten/CS/HR non-hitungan, riset, dan perbaikan berinstruksi jelas.

HEMAT CONTEXT: serahkan pekerjaan berat ke agent; minta laporan balik ringkas (≤200 kata); jangan membaca transkrip agent atau output panjang di sesi utama. Bila stop hook mengeluh ada berkas belum di-commit saat agent masih jalan, commit per path sebagai `wip:`.

Jangan simpan data pribadi member/pembeli, API key, atau token di repo; jangan commit dist/. Perbarui laporan sesi di reports/ (file bertanggal hari itu, YYYY-MM-DD-akun-b.md) setiap selesai satu batch. Berhenti hanya jika pemilik menulis "stop".
```

## Prompt routine Akun A (arsip, sedang dijeda)
Sama strukturnya, dengan cakupan JALUR 2 & 3 + perawatan, maksimal 2 agent paralel. Dihidupkan lagi hanya atas permintaan pemilik.
