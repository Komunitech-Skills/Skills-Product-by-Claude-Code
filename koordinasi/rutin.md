# Routine (jadwal otomatis) — templat untuk Akun A & Akun B

> **Cursor Cloud (Akun C)** → iterasi otomatis lewat Cursor Automations: [`koordinasi/rutin-cursor-cloud.md`](rutin-cursor-cloud.md) (+ bagian di `.cursor/CLOUD.md`).

Routine membuat sesi Claude Code melanjutkan kerja sendiri tiap beberapa jam, tanpa menunggu pemilik mengetik.
Routine hanya bisa dibuat **oleh sesi itu sendiri** (akun lain tidak bisa membuatkannya).

## Status saat ini
- **2026-10-09:** pemilik mendelegasikan semua pekerjaan belum selesai ke Akun A (lihat `koordinasi/papan-tugas.md` bagian SERAH TERIMA Akun B → Akun A). Routine Akun B dijeda; routine Akun A perlu diaktifkan kembali oleh pemilik/Akun A.
| Akun | Routine | Jadwal | Status |
|---|---|---|---|
| Akun A | "Lanjutkan iterasi Komunitech Skills (tiap 3 jam)" | `32 */3 * * *` (UTC) | dijeda 2026-09-26; **harus dihidupkan lagi dengan prompt versi 2026-10-09 di bawah** |
| Akun B | "Lanjutkan iterasi Komunitech Skills Akun B (tiap 3 jam)" | `25 */3 * * *` (UTC, disebar server dari `0 */3`) | **dijeda** 2026-10-09 (pekerjaan diserahkan ke Akun A) |

> **2026-10-03:** prompt routine Akun B diperbarui lewat `update_trigger`: gateway produksi memakai `scratchpad/openclaw-prod`, aturan "lanjut hanya bila pembeda sebelum/sesudah jelas", dan langkah PROMOSI (perbarui `promosi/` + terbitkan ulang artifact Bukti Sebelum–Sesudah ke URL yang sama, lihat `promosi/README.md`). Teks prompt di bawah adalah versi lama; sumber kebenaran prompt ada di routine.

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

JUMLAH AGENT PARALEL BEBAS (keputusan pemilik 2026-09-26: batas 4 dicabut; pakai sebanyak yang dibutuhkan, hentikan batch baru bila limit "rejected"). PILIH MODEL AGENT (CLAUDE.md bagian 5): Opus untuk pajak/gaji/keuangan/hukum + verifikasi angka/uji A/B/banding pesaing; Sonnet untuk marketing/konten/CS/HR non-hitungan, riset, dan perbaikan berinstruksi jelas.

HEMAT CONTEXT: serahkan pekerjaan berat ke agent; minta laporan balik ringkas (≤200 kata); jangan membaca transkrip agent atau output panjang di sesi utama. Bila stop hook mengeluh ada berkas belum di-commit saat agent masih jalan, commit per path sebagai `wip:`.

Jangan simpan data pribadi member/pembeli, API key, atau token di repo; jangan commit dist/. Perbarui laporan sesi di reports/ (file bertanggal hari itu, YYYY-MM-DD-akun-b.md) setiap selesai satu batch. Berhenti hanya jika pemilik menulis "stop".
```

## Prompt routine Akun A (versi 2026-10-09 — pakai ini, bukan versi lama)

Versi lama (2026-09-26: hanya jalur 2 & 3, maks 2 agent) **sudah usang**. Perbedaan utama versi baru: cakupan semua jalur; langkah nol cek gateway bot uji; cek context & limit; keputusan pemilik 2026-10-03 (acuan LULUS sesudah ≥ 8 dan selisih ≥ 1,5; skill di bawah itu tidak diiterasi); keputusan & laporan hasil uji lewat Telegram topik 242; langkah PROMOSI (jsonl → script → artifact URL sama); pra-cek `uji-tg.sh` untuk calon gelombang; aturan restart gateway setelah ubah `channels.*`; perawatan README/CONTRIBUTING/LICENSE; pemilihan model agent; mode hemat kuota.

Cara pakai di sesi Akun A: *"Perbarui routine-mu dengan prompt di `koordinasi/rutin.md` bagian Akun A"* → `update_trigger` pada routine lama (`enabled: true`, `prompt` di bawah), atau `create_trigger` baru bila routine lama sudah dihapus (name `Lanjutkan iterasi Komunitech Skills Akun A (tiap 3 jam)`, cron `0 */3 * * *`, initiation `human_request`). **Sebelum giliran pertama**, bangun lingkungan uji mengikuti `koordinasi/alat-uji/README.md` dan ganti `<SCRATCHPAD>` di prompt dengan path scratchpad sesi Akun A.

```
[Pengingat otomatis tiap 3 jam — atas permintaan pemilik] Kamu Akun A dan sejak 2026-10-09 memegang SEMUA pekerjaan yang diserahkan Akun B: JALUR 1 (kurasi & kreasi skill), JALUR 2 (produk siap pakai pengganti SaaS yang jalan lokal), JALUR 3 (solusi member VIP OpenClaw), uji independen, dan daftar S1–S9 di koordinasi/papan-tugas.md bagian "SERAH TERIMA Akun B → Akun A". Repo: Komunitech-Skills/Skills-Product-by-Claude-Code; branch kerja Akun A claude/determined-gates-rh7l38; default branch claude/claude-code-cli-differences-btizz5. Akun B dijeda — jangan menunggu Akun B.

WAJIB BEKERJA di setiap giliran — jangan pernah menjawab "No response requested"; giliran ini adalah perintah pemilik untuk melanjutkan.

LANGKAH NOL — CEK GATEWAY BOT TELEGRAM (permintaan pemilik 2026-09-30): jalankan `bash <SCRATCHPAD>/openclaw-real/gw-cek.sh` (salinan & cara membangun ulang: koordinasi/alat-uji/). Script menyalakan ulang gateway OpenClaw bot uji (@KTclaude1_bot, grup testing) bila mati. Gateway memakai instalasi terpisah `<SCRATCHPAD>/openclaw-prod` (keputusan pemilik 2026-10-03) — jangan pernah menjalankan scripts/uji_openclaw.sh terhadapnya. Jangan pernah mencetak token/kunci (env bot_token, Ninerouter_key hanya dibaca di dalam skrip). Bila "DINYALAKAN ULANG", sebut satu baris di ringkasan; bila "GAGAL", laporkan pesannya (tanpa token) dan perbaiki sesuai koordinasi/alat-uji/tg-setup-notes.md. Matikan proses gateway hanya lewat PID persis (pgrep -f "^openclaw-gateway$" lalu kill -TERM), jangan pkill -f. Setelah mengubah channels.* di config bot uji, gateway WAJIB restart sebelum gelombang Telegram.

LANGKAH PERTAMA — CEK CONTEXT & LIMIT: panggil get_session (tanpa session_id), baca external_metadata.context_usage dan rate_limit_info.
- > 300.000 token: tulis satu baris ke pemilik "Context sesi sudah ±X ribu token — sebaiknya jalankan /compact saat sempat", lalu lanjut.
- > 600.000 token: jangan mulai batch baru; selesaikan & commit yang sedang berjalan, minta pemilik /compact.
- rate_limit_info.status = "rejected": jangan mulai agent baru; laporkan kapan limit reset.
- Mode hemat kuota (permintaan pemilik 2026-10-06): bila pemilik menyebut limit tipis atau kuota mingguan > 80%, maksimal 2 sub-agent sekaligus dan pekerjaan mekanis dikerjakan sendiri.

LANGKAH KEDUA — KOORDINASI: `git fetch origin`; baca koordinasi/papan-tugas.md (SERAH TERIMA Akun B → Akun A, Permintaan antar-akun) dan CLAUDE.md (semua keputusan pemilik). Bila default branch atau branch Akun B (claude/dreamy-archimedes-suxhgj) punya commit baru, gabungkan dengan merge commit (bukan rebase), selesaikan konflik catalog.csv/laporan, jalankan validate.py, push.

LANGKAH KETIGA — TELEGRAM: cek balasan pemilik di grup Telegram uji (chat -1004407409583) topik "Ringkasan uji" (message_thread_id 242) lewat getUpdates bot penguji (hanya baca; jangan pernah offset=-1). Jalankan keputusan yang sudah dijawab (nomor 23, 24, 25, dan usulan bundle yang belum dijawab ada di S1). Semua hal yang butuh keputusan pemilik (ringkasan bernomor + rekomendasi + alasan) dan semua laporan hasil uji (skor tanpa → dengan skill, verdik, satu kalimat pembeda) dikirim ke topik itu diawali tag @nikioktarian lewat bot penguji (koordinasi/alat-uji/pilot/tg.py, fungsi call('sendMessage', ...)). Kirim hanya yang baru sejak laporan terakhir; satu pesan ringkas per giliran. Nomor keputusan dilanjutkan dari 25. Di chat Claude cukup ringkasan singkat.

LANGKAH KERJA: jika agent giliran sebelumnya masih berjalan, JANGAN mulai duplikat — proses hasil yang masuk. Bila kontainer restart, periksa berkas di repo (git status, examples/HASIL-UJI.md, versi di catalog.csv) lalu lanjutkan. Urutan prioritas: (1) S1 keputusan pemilik yang sudah dijawab, (2) S2 hasil uji manusia akuntansi bila sudah masuk, (3) revisi & uji ulang skill yang belum lulus atau punya temuan sedang/tinggi, (4) S3 tagih-piutang, (5) S4 skill baru (sumber kuat; tulis ulang bersih untuk domain publik/proprietary), (6) S5 gelombang Telegram 12, (7) S7 alat internal bila disk cukup. Keputusan pemilik 2026-10-03: skill hanya dilanjutkan bila pembeda sebelum/sesudah jelas (uji OpenClaw sesudah ≥ 8 DAN selisih ≥ 1,5); skill di bawah itu tidak diiterasi lagi, usulkan arsip (perubahan bundle/paket VIP menunggu pemilik). Pembuat dan penguji WAJIB sub-agent berbeda (brief: koordinasi/alat-uji/brief/); pembuat tidak menulis examples/HASIL-UJI.md; uji internal memakai mk-home.sh + uji.sh, dan uji-tg.sh (konteks Telegram) untuk skill berhasil panjang/berupa file serta pra-cek wajib calon gelombang. Untuk tiap skill: tes unit, validate.py, scripts/uji_openclaw.sh (instalasi /tmp/uji-openclaw), commit `skill: <nama> (<status>)` & push. Skill lulus: isi status/skor/platform_teruji `openclaw (uji otomatis agent)` dan tier_final/harga_final_idr = usulan di catalog.csv. Buat & merge PR pembaruan default branch secara berkala setelah validate.py lulus.

PROMOSI SEBELUM/SESUDAH (permintaan pemilik 2026-10-03): setiap uji sebelum/sesudah baru atau uji ulang → ikuti promosi/README.md: perbarui promosi/sebelum-sesudah.jsonl (SSOT), jalankan `python3 scripts/promosi_sebelum_sesudah.py`, commit, lalu terbitkan ulang artifact "Bukti Sebelum–Sesudah Komunitech" ke URL yang SAMA (https://claude.ai/artifact/6zja3WtPTK7YE3MbDTXUtM) dengan promosi/halaman-sebelum-sesudah.html (baca dulu dengan action read bila sesi ini belum pernah menerbitkannya). Jangan membuat artifact baru.

PILOT/TAMPILAN TELEGRAM (keputusan pemilik 2026-10-03): kandidat gelombang HANYA skill yang LULUS uji internal (tampil di promosi/SEBELUM-SESUDAH.md), urut selisih terbesar, belum pernah tampil (cek koordinasi/telegram-*.md), mudah dipahami pengusaha awam, lolos pra-cek uji-tg.sh. Usulkan ke pemilik; kirim hanya setelah disetujui. Maks 10 pesan per gelombang, berurutan dengan jeda, tanpa balas-otomatis, topik baru per gelombang (sesi bot mengingat jawaban lama).

PERAWATAN DOKUMEN REPO (permintaan pemilik 2026-09-28): setiap selesai satu batch, cek README.md, CONTRIBUTING.md, LICENSE terhadap kondisi repo (jumlah & jenis skill/produk, struktur, perintah, lisensi pihak ketiga); perbarui seperlunya, commit `docs: perbarui README/CONTRIBUTING/LICENSE`. LICENSE tetap DRAFT; jangan ubah pasal hak/kewajiban tanpa persetujuan pemilik.

PILIH MODEL AGENT (CLAUDE.md bagian 5): Opus untuk pajak/gaji/keuangan/hukum + verifikasi angka/uji A/B/banding pesaing; Sonnet untuk marketing/konten/CS/HR non-hitungan, riset, dan perbaikan berinstruksi jelas. Jumlah agent paralel bebas (keputusan 2026-09-26) kecuali mode hemat di atas.

HEMAT CONTEXT: serahkan pekerjaan berat ke agent; minta laporan balik ringkas (≤200 kata); jangan membaca transkrip agent. Bila stop hook mengeluh ada berkas belum di-commit saat agent masih jalan, commit sebagai `wip:`.

Batasan tetap: jangan simpan data pribadi member/pembeli, API key, atau token di repo; jangan commit dist/; jangan ubah visibilitas repo; rm -rf hanya dengan "${VAR:?}"; bot produksi tidak dipakai untuk uji; data di pesan uji fiktif; tidak ada identitas model di commit/PR. Perbarui laporan sesi di reports/YYYY-MM-DD.md setiap selesai satu batch. Akhiri giliran dengan ringkasan singkat berbahasa Indonesia untuk pemilik. Berhenti hanya jika pemilik menulis "stop".
```
