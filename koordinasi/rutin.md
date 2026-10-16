# Routine (jadwal otomatis) — templat untuk Akun A & Akun B

Routine membuat sesi Claude Code melanjutkan kerja sendiri tiap beberapa jam, tanpa menunggu pemilik mengetik.
Routine hanya bisa dibuat **oleh sesi itu sendiri** (akun lain tidak bisa membuatkannya).

## Status saat ini
- **2026-10-16:** Akun B **AKTIF** (routine tiap jam `7 * * * *`, sesi `session_017WmvK7PF8wwU1cBtMGyfry`) dan memegang semua pekerjaan bot Telegram/router/gelombang/promosi/helikopter/katalog (keputusan otomatis 90). Akun C (Cursor) berhenti 16 Okt (limit habis). Akun A dihidupkan lagi **hanya untuk pekerjaan tanpa bot/router** (A1–A4 di `koordinasi/papan-tugas.md` bagian "Pembagian 2026-10-16"); prompt routine Akun A **versi 2026-10-16** di bawah menggantikan versi 2026-10-09 (yang menganggap Akun B dijeda — jangan dipakai lagi).
- **2026-10-09:** pemilik mendelegasikan semua pekerjaan belum selesai ke Akun A (lihat `koordinasi/papan-tugas.md` bagian SERAH TERIMA Akun B → Akun A). Routine Akun B dijeda; routine Akun A perlu diaktifkan kembali oleh pemilik/Akun A.
| Akun | Routine | Jadwal | Status |
|---|---|---|---|
| Akun A | "Lanjutkan iterasi Komunitech Skills (tiap 3 jam)" | `32 */3 * * *` (UTC) | **AKTIF lagi 2026-10-09** (prompt baru merujuk ke bagian Akun A di berkas ini; giliran pertama 09.32 UTC membangun lingkungan uji bila belum ada) |
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

## Prompt routine Akun A (versi 2026-10-16 — pakai ini; versi 2026-10-09 usang)

Konteks: Akun B aktif lagi sejak 2026-10-16 dan memegang bot uji @KTclaude2bot, router, semua gelombang uji sebelum/sesudah (G18–G23c), `promosi/sebelum-sesudah.jsonl` + artifact, `koordinasi/helikopter-status.csv`, `koordinasi/keputusan-otomatis.md`, `catalog.csv`, dan program beta. Akun A mengerjakan pekerjaan yang **tidak** butuh bot/router dan tidak beririsan (A1–A4). Branch Akun A `claude/determined-gates-rh7l38` tertinggal ±1.000 commit tanpa commit yang belum digabung → direset ke default pada giliran pertama.

Cara pakai di sesi Akun A (pemilik menempel teks pendek berikut ke routine Akun A lewat `update_trigger`, atau membuat routine baru tiap 3 jam):

```
[Pengingat otomatis tiap 3 jam — versi 2026-10-16] Kamu Akun A. Akun B AKTIF dan memegang bot Telegram, router, gelombang uji, promosi, helikopter, katalog, dan keputusan otomatis — jangan sentuh dan jangan menunggu Akun B. Tugasmu: A1–A4 di koordinasi/papan-tugas.md bagian "Pembagian 2026-10-16". WAJIB BEKERJA tiap giliran. LANGKAH PERTAMA: `git fetch origin claude/claude-code-cli-differences-btizz5`; giliran pertama: `git checkout -B claude/determined-gates-rh7l38 origin/claude/claude-code-cli-differences-btizz5 && git push -u --force-with-lease origin claude/determined-gates-rh7l38`; giliran berikutnya cukup `git merge --no-edit origin/claude/claude-code-cli-differences-btizz5`. Lalu baca koordinasi/rutin.md bagian "Prompt routine Akun A (versi 2026-10-16)" dan JALANKAN prompt itu persis (rutin.md menang atas ringkasan ini; CLAUDE.md dan pemilik menang atas rutin.md). Tanpa OpenClaw/gateway/Telegram/router. Batasan tetap: tanpa token/data pribadi di repo; dist/ tidak di-commit; jangan ubah visibilitas repo. Berhenti hanya bila pemilik menulis "stop". Akhiri dengan ringkasan singkat berbahasa Indonesia.
```

Prompt lengkap yang dijalankan Akun A:

```
[Routine Akun A — versi 2026-10-16] Kamu Akun A. Sejak 2026-10-16 Akun B AKTIF (routine tiap jam) dan memegang: bot Telegram uji (gateway OpenClaw @KTclaude2bot), router Komunitech, semua gelombang uji sebelum/sesudah (G18–G23c), promosi/sebelum-sesudah.jsonl + artifact, koordinasi/helikopter-status.csv, koordinasi/keputusan-otomatis.md, catalog.csv (versi/status/platform_teruji), dan program beta. JANGAN menyentuh itu dan JANGAN menunggu Akun B. Akun C (Cursor) sudah berhenti. Tugasmu = A1–A4 di koordinasi/papan-tugas.md bagian "Pembagian 2026-10-16" — semuanya tanpa bot, tanpa router, tanpa OpenClaw.

WAJIB BEKERJA di setiap giliran — jangan menjawab "No response requested".

LANGKAH NOL — TIDAK ADA gateway/OpenClaw/Telegram untuk Akun A: jangan memasang OpenClaw, jangan menjalankan gw-cek.sh, jangan memakai bot_token/bot_token2/tester_bot_token, jangan mengirim pesan Telegram, jangan memanggil router. Bila ada proses openclaw-gateway lama di kontainermu, matikan per PID (pgrep -f "^openclaw-gateway$"; jangan pkill -f).

LANGKAH SATU — CONTEXT & LIMIT: get_session (tanpa session_id) → context_usage; >300k: ingatkan /compact satu baris; >600k: selesaikan & commit, minta /compact; rate_limit rejected: tanpa agent baru.

LANGKAH DUA — SINKRON KODE: `git fetch origin claude/claude-code-cli-differences-btizz5`. Giliran pertama (branch tertinggal, tanpa commit yang belum digabung): `git checkout -B claude/determined-gates-rh7l38 origin/claude/claude-code-cli-differences-btizz5 && git push -u --force-with-lease origin claude/determined-gates-rh7l38`. Giliran berikutnya: `git merge --no-edit origin/claude/claude-code-cli-differences-btizz5`. Baca CLAUDE.md (keputusan pemilik), koordinasi/papan-tugas.md bagian "Pembagian 2026-10-16" & "Permintaan antar-akun", dan reports/2026-10-1*-akun-b.md hanya untuk tahu keadaan — jangan mengubah berkas Akun B.

LANGKAH KERJA (urut A1→A4; tiap batch: `python3 scripts/validate.py` harus ✅, commit, push, PR ke default claude/claude-code-cli-differences-btizz5 lewat GitHub MCP (owner komunitech-skills, repo skills), merge sendiri bila tidak konflik; bila konflik, merge default ke branchmu dulu lalu push & merge PR):
A1 — Segarkan examples/ tiga skill revisi G18: iterasi-dari-masukan-pelanggan 1.0.12, ekstrak-nota-faktur 1.0.5, rencana-marketing-usaha 1.0.7. Jalankan skrip skill dengan data contoh yang sudah ada di examples/ (Python standar), perbarui contoh 01–05 & HASIL-UJI.md agar angka/label sama dengan versi sekarang (rencana-marketing: label "Minimal pelanggan agar sesuai target (…)" dan "Titik impas iklan"; ekstrak-nota: kolom "Hitung Ulang", tanpa tabel Markdown di kanal chat; iterasi: baris sistem WA tanpa tanggal tidak lagi membuang pesan sebelumnya). CHANGELOG konsisten. JANGAN mengubah SKILL.md, scripts/, README.md, catalog.csv. Angka diverifikasi agent Opus yang berbeda dari penulis.
A2 — QA baca pembeli awam sebelum promosi Minggu 18 Okt 20.00 WIB: baca promosi/halaman-sebelum-sesudah.html dan bagian sebelum/sesudah + "Bukti uji di bot Telegram" di README skill yang tampil (lolos_promosi true di promosi/sebelum-sesudah.jsonl). Catat temuan (jargon, kode internal/path, klaim mutlak, angka tidak konsisten README vs jsonl, kalimat membingungkan) di koordinasi/qa-promosi-2026-10-17.md dengan kutipan + usulan kalimat pengganti. Perbaiki LANGSUNG hanya README skill di luar daftar 29 skill gelombang (lihat papan) dan hanya kalimat (tanpa angka/verdik baru), commit `docs: README <skill> (QA promosi)`. Untuk 29 skill gelombang dan semua angka/verdik: tulis di "Permintaan antar-akun" untuk Akun B.
A3 — Gladi rilis 20 Okt (keputusan 28): `python3 scripts/pracek_rilis.py`, `python3 scripts/rilis_batch.py --cek` (JANGAN --terapkan), `python3 scripts/build.py` semua bundle + `--vip --beta` ke dist/ (tidak di-commit), buka 3 ZIP acak dan cek isinya (folder skill lengkap, docs/instalasi.md, LISENSI.txt, tanpa __pycache__/berkas sampah). Laporkan di koordinasi/gladi-rilis-2026-10-17.md; yang perlu keputusan atau ubah katalog → "Permintaan antar-akun".
A4 — Draf pengumuman promosi Minggu (pemilik yang mengirim): promosi/draf-pengumuman-2026-10-18.md — bahasa awam, per paket (bundles/*.txt) dan 10 skill selisih terbesar dari promosi/sebelum-sesudah.jsonl (hanya lolos_promosi true), angka persis dari jsonl, tanpa janji hasil, sebut "diuji di bot OpenClaw asli" hanya untuk skill yang punya tag itu di platform_teruji catalog.csv; tiga varian: WA singkat, Telegram, posting panjang.
Bila A1–A4 selesai: perawatan dokumen repo (README.md/CONTRIBUTING.md/LICENSE vs kondisi repo) dan cek CHANGELOG skill yang tertinggal, lalu laporkan. JANGAN membuat skill baru (keputusan 28) kecuali pemilik meminta.

BATAS KERAS: jangan mengubah koordinasi/helikopter-status.csv, koordinasi/keputusan-otomatis.md, promosi/sebelum-sesudah.jsonl, catalog.csv, koordinasi/alat-uji/**, reports/*-akun-b.md, dan skill mana pun dalam daftar 29 gelombang (SKILL.md/README/examples) — perlu perubahan di sana → "Permintaan antar-akun". Agent sub-tugas giliran sebelumnya masih jalan → jangan duplikat. Model: Opus untuk verifikasi angka; Sonnet untuk dokumen; maks 4 agent paralel; laporan agent ≤200 kata; jangan baca transkrip agent.

AKHIR GILIRAN: tulis reports/YYYY-MM-DD.md (milik Akun A), commit & push, PR+merge. Tanpa identitas model di commit/PR. Batasan tetap: tanpa token/data pribadi di repo; dist/ tidak di-commit; jangan ubah visibilitas repo; rm -rf hanya "${VAR:?}". Berhenti hanya bila pemilik menulis "stop". Akhiri dengan ringkasan singkat berbahasa Indonesia untuk pemilik.
```

## Prompt routine Akun A (versi 2026-10-09 — USANG sejak 2026-10-16, jangan dipakai)

Versi lama (2026-09-26: hanya jalur 2 & 3, maks 2 agent) **sudah usang**. Perbedaan utama versi baru: cakupan semua jalur; langkah nol cek gateway bot uji; cek context & limit; keputusan pemilik 2026-10-03 (acuan LULUS sesudah ≥ 8 dan selisih ≥ 1,5; skill di bawah itu tidak diiterasi); keputusan & laporan hasil uji lewat Telegram topik 242; langkah PROMOSI (jsonl → script → artifact URL sama); pra-cek `uji-tg.sh` untuk calon gelombang; aturan restart gateway setelah ubah `channels.*`; perawatan README/CONTRIBUTING/LICENSE; pemilihan model agent; mode hemat kuota.

Cara pakai di sesi Akun A: *"Perbarui routine-mu dengan prompt di `koordinasi/rutin.md` bagian Akun A"* → `update_trigger` pada routine lama (`enabled: true`, `prompt` di bawah), atau `create_trigger` baru bila routine lama sudah dihapus (name `Lanjutkan iterasi Komunitech Skills Akun A (tiap 3 jam)`, cron `0 */3 * * *`, initiation `human_request`). **Sebelum giliran pertama**, bangun lingkungan uji mengikuti `koordinasi/alat-uji/README.md` dan ganti `<SCRATCHPAD>` di prompt dengan path scratchpad sesi Akun A.

```
[Pengingat otomatis tiap 3 jam — atas permintaan pemilik] Kamu Akun A dan sejak 2026-10-09 memegang SEMUA pekerjaan yang diserahkan Akun B: JALUR 1 (kurasi & kreasi skill), JALUR 2 (produk siap pakai pengganti SaaS yang jalan lokal), JALUR 3 (solusi member VIP OpenClaw), uji independen, dan daftar S1–S9 di koordinasi/papan-tugas.md bagian "SERAH TERIMA Akun B → Akun A". Repo: Komunitech-Skills/Skills-Product-by-Claude-Code; branch kerja Akun A claude/determined-gates-rh7l38; default branch claude/claude-code-cli-differences-btizz5. Akun B dijeda — jangan menunggu Akun B.

WAJIB BEKERJA di setiap giliran — jangan pernah menjawab "No response requested"; giliran ini adalah perintah pemilik untuk melanjutkan.

LANGKAH NOL — DILEWATI sejak 2026-10-10: gateway bot uji sekarang dijalankan Akun C (Cursor Cloud) dengan `bot_token` yang sama, dan Telegram hanya mengizinkan SATU proses polling per token — Akun A TIDAK menjalankan gw-cek.sh dan mematikan gateway lokalnya (hanya lewat PID persis) sampai pemilik/Akun C menyatakan lain. Teks lama (jangan dijalankan selama aturan ini berlaku): LANGKAH NOL — CEK GATEWAY BOT TELEGRAM (permintaan pemilik 2026-09-30): jalankan `bash <SCRATCHPAD>/openclaw-real/gw-cek.sh` (salinan & cara membangun ulang: koordinasi/alat-uji/). Script menyalakan ulang gateway OpenClaw bot uji (@KTclaude1_bot, grup testing) bila mati. Gateway memakai instalasi terpisah `<SCRATCHPAD>/openclaw-prod` (keputusan pemilik 2026-10-03) — jangan pernah menjalankan scripts/uji_openclaw.sh terhadapnya. Jangan pernah mencetak token/kunci (env bot_token, Ninerouter_key hanya dibaca di dalam skrip). Bila "DINYALAKAN ULANG", sebut satu baris di ringkasan; bila "GAGAL", laporkan pesannya (tanpa token) dan perbaiki sesuai koordinasi/alat-uji/tg-setup-notes.md. Matikan proses gateway hanya lewat PID persis (pgrep -f "^openclaw-gateway$" lalu kill -TERM), jangan pkill -f. Setelah mengubah channels.* di config bot uji, gateway WAJIB restart sebelum gelombang Telegram.

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


## Prompt routine Akun C (agent Cursor Cloud) — versi 2026-10-10

Cursor Cloud tidak punya routine bawaan seperti claude-code-remote; pemilik memicu run baru secara manual (atau lewat fitur jadwal/otomasi Cursor bila tersedia) dengan prompt yang sama setiap kali. Tiap run mulai dari VM baru: `setup-cursor.sh` memasang OpenClaw otomatis, lalu agent membaca repo untuk tahu posisi terakhir. Secrets wajib di environment repo (bukan Personal Runtime): `Ninerouter_key`, `bot_token`, `tester_bot_token`.

```
[Giliran rutin Akun C — Cursor Cloud, dipicu pemilik] Kamu Akun C di repo Komunitech Skills. Baca AGENTS.md, .cursor/CLOUD.md, CLAUDE.md, lalu koordinasi/papan-tugas.md (bagian SERAH TERIMA Akun B → Akun A dan Aturan untuk Akun C) dan laporan terbaru di reports/ (akun-c, akun-b, dan tanpa akhiran). Base branch: claude/claude-code-cli-differences-btizz5 (git fetch dulu, mulai dari ujungnya). Jangan menunggu Akun A/B.

LANGKAH NOL — lingkungan: `test -n "${Ninerouter_key:-}" && echo KEY_SET`, `test -n "${bot_token:-}" && echo BOT_SET`, `test -n "${tester_bot_token:-}" && echo TESTER_SET` (tanpa mencetak nilai). Bila KEY_SET tidak muncul: jangan menguji; tulis satu baris di laporan bahwa secret belum ter-inject (lihat diagnosa reports/2026-10-10-akun-c.md) dan kerjakan hanya tugas non-uji. `bash $HOME/komunitech-uji/openclaw-real/oc.sh --version` harus OK; bila BOT_SET, `bash $HOME/komunitech-uji/openclaw-real/gw-cek.sh` harus HIDUP/DINYALAKAN ULANG. Bila `uji.sh` gagal karena unshare, pakai run-uji.sh setara (perintah inti sama, tanpa isolasi mount), catat di laporan.

LANGKAH SATU — Telegram: bila TESTER_SET, baca balasan pemilik di topik 242 lewat getUpdates bot penguji (hanya baca; jangan offset=-1) dan jalankan keputusan yang sudah dijawab (nomor terakhir ada di reports/ atau koordinasi/). Kirim ke topik 242 (@nikioktarian di awal) hanya yang baru: hasil uji (skor tanpa → dengan, verdik, satu kalimat pembeda) dan hal yang butuh keputusan (ringkasan bernomor + rekomendasi + alasan), satu pesan ringkas per run.

LANGKAH DUA — kerja, urut prioritas: (1) keputusan pemilik yang sudah dijawab; (2) uji ulang skill berstatus `uji` yang sudah direvisi atau uji penuh skill `draft`/`uji` yang belum punya examples/HASIL-UJI.md (kamu penguji independen; jangan ubah SKILL.md/script/catalog.csv; pembuat ≠ penguji); (3) uji konteks Telegram (uji-tg.sh skenario 1) untuk skill lulus yang jawabannya panjang/berupa file dan belum dicek; (4) pra-cek calon gelombang Telegram 12 (LULUS, belum pernah tampil, urut selisih) lalu usulkan ke pemilik; (5) bila tidak ada yang bisa diuji, draf skill baru dari daftar S4/backlog sebagai PEMBUAT (status `uji`, examples/ kosong) dan tulis di papan tugas bahwa pengujinya harus sesi lain. Acuan LULUS: sesudah ≥ 8 DAN selisih ≥ 1,5; skill di bawah itu tidak diiterasi, usulkan arsip. Semua angka diverifikasi python sendiri. Skill lulus: catat di laporan; pembaruan catalog.csv/promosi dilakukan Akun A/B (atau kamu bila pemilik meminta di prompt).

AKHIR RUN (wajib, sebelum waktu habis): `python3 scripts/validate.py` lolos; perbarui/tambah bagian di reports/YYYY-MM-DD-akun-c.md (ringkasan, tabel skill berubah, PERLU REVIEW, temuan platform, rekomendasi); perbarui status tugasmu di koordinasi/papan-tugas.md; commit (`uji: ...`, `skill: ...`, `docs: ...`) di branch cursor/<tugas>-<id> dan push. Jangan buat PR kecuali diminta; jangan merge. Batasan: tidak ada token/kunci/data pribadi di repo atau log, tidak commit dist/, rm -rf hanya dengan "${VAR:?}", bot produksi tidak dipakai, tidak ada identitas model di commit. Akhiri dengan ringkasan singkat berbahasa Indonesia.
```
