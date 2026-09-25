# Pesan pembuka untuk sesi Claude Code di Akun B

Buat sesi baru di akun kedua dengan repo **Komunitech-Skills/Skills**, lalu tempel pesan di bawah ini apa adanya.

---

Kamu adalah Akun B dalam kolaborasi 2 akun Claude Code untuk repo ini. Akun A (sesi lain) sudah bekerja di branch `claude/determined-gates-rh7l38`, dan semua pekerjaan terbaru ada di sana (default branch repo masih versi lama).

Langkah pertama:
1. `git fetch origin claude/determined-gates-rh7l38` lalu `git merge --ff-only origin/claude/determined-gates-rh7l38` ke branch kerjamu (branch-mu masih kosong, jadi ini aman). Jangan rebase atau force-push branch lain.
2. Baca `CLAUDE.md`, lalu `koordinasi/papan-tugas.md`. Tugasmu hanya **Jalur 1 (kurasi & kreasi skill)**, kolom "Jalur 1 — Akun B". Jangan menyentuh skill milik jalur lain.
3. Tulis nama branch kerjamu di baris "Branch Akun B" pada papan tugas, commit & push.
4. Ambil tugas berikutnya yang berstatus `belum` (mulai dari B1), ubah statusnya jadi `dikerjakan (Akun B, tanggal)`, commit & push, lalu kerjakan sesuai Tahap 1–8 CLAUDE.md: buat skill → uji independen oleh agent terpisah (5 skenario + A/B + banding pesaing + verifikasi angka) → revisi bila skor < 7 → `python3 scripts/validate.py` → commit `skill: <nama> (<status>)` → push.
5. Maksimal 2 agent paralel; serahkan pekerjaan berat ke agent dan minta laporan balik ringkas (≤200 kata) supaya context sesi tidak membengkak. Jangan menulis pola teks "curl | sh" secara harfiah (validator menandainya).
6. Laporan sesi tulis di `reports/YYYY-MM-DD-akun-b.md`. Di awal setiap giliran, merge ulang `origin/claude/determined-gates-rh7l38` agar tetap sinkron.
7. Hal yang butuh keputusan pemilik (harga final, lisensi abu-abu, regulasi ragu) → catat sebagai PERLU REVIEW, jangan diputuskan sendiri.

Lanjutkan tugas-tugas Jalur 1 secara berurutan sampai pemilik menulis "stop".
