# Uji banding pesaing — kanboard-papan-kerja vs server MCP Kanboard publik

**Penguji:** agent penguji independen (Claude Code), 2026-09-30. Pesaing **hanya dibaca** (clone `--depth 1` ke folder uji, kode tidak dijalankan/di-build, tidak disalin).
Kata kunci & sumber: "kanboard MCP", "kanboard skill SKILL.md", "kanboard JSON-RPC agent" (GitHub; catatan riset pembuat juga mencari skills.sh/ClawHub/anthropics/skills — tidak ada SKILL.md khusus Kanboard). Dua pesaing terbaik:

| | **bivex/kanboard-mcp** (Go, MIT, commit terakhir 12 Jun 2026, `main.go` ±8.000 baris) | **ChristianJStarr/kanboard-mcp** (plugin PHP Kanboard, MIT, commit terakhir 23 Mar 2026) | **kanboard-papan-kerja** (kita) |
|---|---|---|---|
| Pemasangan | Butuh Go 1.21 + build, klien MCP, ENV `KANBOARD_API_ENDPOINT`/`API_KEY`/`USERNAME`/`PASSWORD` | Dipasang di folder `plugins` Kanboard + token MCP | Salin folder skill, Python standar, `simpan-kunci` sekali |
| Cakupan | ±190 alat (semua API) termasuk `remove_project`, `delete_task`, `remove_user`, `delete_column`, `remove_all_project_files` | 26 alat, termasuk `delete_task`, `delete_column`, `delete_swimlane`, `delete_category` | 13 perintah; **tanpa** hapus/tutup, metode dikunci allowlist |
| Konfirmasi tulis | Tidak ada (bergantung klien MCP) | Tidak ada | Pratinjau + `--ya` wajib; singkatan opsi ditolak |
| Terlambat | `get_overdue_tasks` = metode bawaan Kanboard (di peta RBAC-nya ditandai app-admin), termasuk kartu di kolom Selesai | Tidak ada | Dihitung, kolom terakhir dikecualikan, per papan/semua papan |
| Hari ini / macet | Tidak ada | Tidak ada | Ada, zona WIB/WITA/WIT, ambang macet `--hari` |
| Tanggal | `date_due` teks "YYYY-MM-DD HH:MM" diteruskan apa adanya (zona server, tanpa konversi) | `due_date` diteruskan apa adanya | Bahasa Indonesia ("Jumat jam 10:00", "25/10", "akhir bulan") → dikonversi ke zona server |
| Template usaha | Tidak ada (kolom bawaan Inggris) | Tidak ada | 4 template Indonesia dengan batas WIP |
| Laporan siap Telegram | Tidak ada | Tidak ada | Satu pesan ≤ 3.500 karakter + panduan jadwal OpenClaw |
| Keamanan jaringan | `http.Client` timeout 30 dtk; tidak terlihat penolakan redirect/allowlist host | Berjalan di dalam Kanboard | Allowlist host, internet wajib https, redirect ditolak, token disamarkan |
| Bahasa & dokumentasi | Inggris, untuk developer | Inggris, untuk admin Kanboard | Indonesia awam, panduan pasang + pengamanan |

## Skenario normal pertama (papan produksi konveksi) — penilaian berdampingan
Karena pesaing tidak dijalankan, penilaian berdasarkan kemampuan yang tersedia di kodenya: untuk membuat papan konveksi, pesaing memerlukan agent memanggil `create_project` lalu `update_column`/`create_column` satu per satu dengan nama kolom karangan agent; untuk "yang telat/hari ini/macet" hanya tersedia `get_overdue_tasks` (bivex) atau tidak ada sama sekali (Christian) — hasilnya sama dengan sisi "tanpa skill" di `00-pembanding-tanpa-skill.md` (kartu Selesai ikut terhitung, tanpa "hari ini"/"macet", tanggal Indonesia tidak dipahami).

| Kriteria (1–5) | bivex | Christian | Kita |
|---|---|---|---|
| Hasil siap pakai untuk pemilik UMKM | 2 | 1 | 5 |
| Ketepatan angka terlambat/hari ini/macet | 2 | 1 | 5 |
| Keamanan (tanpa hapus, konfirmasi, token) | 2 | 2 | 5 |
| Kemudahan pasang orang awam | 1 | 2 | 4 |
| Keluasan fitur Kanboard | 5 | 3 | 2 |

**Kesimpulan:** skill kita menang telak untuk tugas dan audiens ini. Keunggulan pesaing hanya keluasan (komentar, sub-tugas, tag, swimlane, lampiran). Yang layak dipelajari (tulis ulang dengan cara sendiri, bukan disalin): perintah **komentar kartu** (mis. mencatat nomor resi) dan **tag** — kebutuhan wajar toko online, bisa dipertimbangkan di versi berikutnya dengan pola pratinjau + `--ya` yang sama.
