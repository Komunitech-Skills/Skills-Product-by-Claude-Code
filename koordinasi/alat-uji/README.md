# Alat uji Akun B — salinan untuk serah terima (2026-10-09)

Semua berkas di sini disalin dari scratchpad sesi Akun B (`/tmp/claude-0/.../scratchpad/`) agar Akun A bisa membangun ulang lingkungan uji. **Tidak ada token/kunci di dalamnya**; semua rahasia dibaca dari environment variable (`bot_token` = token bot penguji, `Ninerouter_key` = kunci router model). Jangan pernah mencetak atau menyimpan nilainya.

## Isi
| Berkas | Fungsi |
|---|---|
| `tg-setup-notes.md` | Catatan operator: cara bot uji dipasang, risiko, revert, instalasi produksi terpisah, pelajaran gelombang 11 |
| `config-bot-uji/openclaw.json` | Config OpenClaw bot uji (@KTclaude1_bot). `apiKey` memakai placeholder `${NINEROUTER_UJI_KEY}`. Heartbeat sudah dimatikan (`agents.defaults.heartbeat.every: "0m"`) |
| `config-bot-uji/workspace/*.md` | AGENTS/SOUL/IDENTITY bot uji (USER.md sengaja tidak disalin) |
| `oc.sh`, `oc-tg.sh` | Pembungkus `openclaw` dengan env bersih; hanya meneruskan kunci router (dan token bot untuk `oc-tg.sh`) |
| `gw-cek.sh` | Cek/nyalakan ulang gateway bot uji (dipanggil tiap giliran routine). **Perbaiki sebelum dipakai:** ganti `pkill -TERM -f openclaw-gateway` dengan kill PID persis (`pgrep -f "^openclaw-gateway$"`), karena `pkill -f` bisa mengenai proses penguji |
| `mk-home.sh` | Buat HOME OpenClaw terpisah berisi hanya skill yang disebut (tanpa skill = sisi "sebelum"). Tambahkan guard `"${VAR:?}"` pada `rm -rf` |
| `uji.sh` | Jalankan satu pesan di HOME tertentu secara lokal (`openclaw agent --local`), hasil ke berkas |
| `uji-tg.sh` | Sama, tetapi dengan konteks kanal Telegram (`--channel telegram` tanpa `--deliver`) — pra-cek wajib calon gelombang |
| `pilot/tg.py` | `tg.call('sendMessage', chat_id=-1004407409583, message_thread_id=242, text=...)` untuk laporan/keputusan ke topik "Ringkasan uji" |
| `pilot/mktopics-g11.py`, `kirim-urut2.py`, `poll-g2.py`, `kumpul-g11.py`, `cek-status.py` | Gelombang Telegram: buat topik baru, kirim pesan berurutan dengan jeda, ambil balasan, kumpulkan transkrip. Ganti nomor gelombang & daftar pesan |
| `brief/maker-umum.md`, `brief/tester-umum.md` | Brief standar untuk sub-agent pembuat dan penguji (pola wajib, acuan LULUS) |

## Membangun ulang (urutan)
1. Pasang OpenClaw dua kali di scratchpad: `openclaw-prod` (gateway bot uji, `npm i openclaw@2026.9.x` di folder sendiri) dan `/tmp/uji-openclaw` (dipakai `scripts/uji_openclaw.sh`). Jangan pernah menjalankan `uji_openclaw.sh` terhadap instalasi gateway.
2. Buat `openclaw-real/home/.openclaw/` dari `config-bot-uji/`; set env `bot_token`, `Ninerouter_key` (secret environment, bukan ditempel di chat).
3. Path: semua skrip kini memakai `SP=${SCRATCHPAD:?}` (tanpa path sesi tertanam). Jalankan `export SCRATCHPAD=<folder scratchpad sesi>` sebelum memakai skrip, atau (di salinan kerja) ganti baris `SP=...` di atas tiap `.sh`.
4. `bash gw-cek.sh` → harus `GATEWAY: HIDUP`/`DINYALAKAN ULANG`. Gateway sering mati saat idle; routine 3 jam menyalakan ulang.
5. Uji sebelum/sesudah: `mk-home.sh sebelum` (tanpa skill) dan `mk-home.sh nama-skill nama-skill`, lalu `uji.sh`/`uji-tg.sh` per skenario. Acuan LULUS: sesudah ≥ 8 dan selisih ≥ 1,5.
6. Setelah mengubah `channels.*` di config bot uji: **restart gateway** (hot reload membuat semua balasan ditolak).

## Catatan 2026-10-09 (dibangun ulang oleh Akun A)
- Lingkungan dibangun ulang di scratchpad sesi baru: `openclaw-prod` (Node 24.21.0 dari nodejs.org, SHA-256 cocok dengan SHASUMS256.txt, + `npm i openclaw@2026.9.8` dari registry resmi) dan `openclaw-real` (skrip + `home/.openclaw` dari `config-bot-uji/`). `openclaw-prod` sengaja 2026.9.8, bukan 2026.9.6 milik `/tmp/uji-openclaw`: config bot uji ditulis oleh 2026.9.7 dan 2026.9.6 menolak menjalankan gateway ("binary lebih tua dari config").
- Perubahan skrip: (1) path sesi tertanam diganti `SP=${SCRATCHPAD:?}` (skrip Python membaca `os.environ["SCRATCHPAD"]`); (2) `gw-cek.sh` tidak lagi memakai `pkill -f`, melainkan `kill` PID persis dari `pgrep -f "^openclaw-gateway$"` (pengecekan hidup memakai pola yang sama); (3) `mk-home.sh` memakai `rm -rf "${R:?}/homes/${N:?}"`. Selain itu isi skrip tidak diubah.
- Heartbeat tetap mati (`agents.defaults.heartbeat.every: "0m"`), terkonfirmasi di log gateway (`[heartbeat] disabled`).
- Lanjutan: `pilot/tg.py` membaca env `tester_bot_token` (bukan `bot_token`); isi env itu sebelum memakai skrip pilot. Router model (`r9wtenn.abc-tunnel.us`) bisa sewaktu-waktu mengembalikan HTTP 530 (tunnel mati); itu masalah sisi router, bukan skrip.
