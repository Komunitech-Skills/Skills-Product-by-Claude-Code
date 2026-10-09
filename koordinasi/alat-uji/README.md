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
3. Sesuaikan path absolut di semua `.sh` (variabel `R`, `P`, `S`) ke scratchpad sesi baru.
4. `bash gw-cek.sh` → harus `GATEWAY: HIDUP`/`DINYALAKAN ULANG`. Gateway sering mati saat idle; routine 3 jam menyalakan ulang.
5. Uji sebelum/sesudah: `mk-home.sh sebelum` (tanpa skill) dan `mk-home.sh nama-skill nama-skill`, lalu `uji.sh`/`uji-tg.sh` per skenario. Acuan LULUS: sesudah ≥ 8 dan selisih ≥ 1,5.
6. Setelah mengubah `channels.*` di config bot uji: **restart gateway** (hot reload membuat semua balasan ditolak).
