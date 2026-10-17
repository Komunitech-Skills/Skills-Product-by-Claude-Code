# Cara Memasang Skill Komunitech

Skill adalah **folder** berisi file `SKILL.md`. Cara memasangnya: **salin folder skill ke folder "skills" milik AI agent kamu.** Setelah itu, cukup minta tolong seperti biasa. AI agent akan memakai skill secara otomatis bila relevan.

> Pastikan yang disalin adalah folder skill-nya (misalnya `kasir-lokal`, yang di dalamnya langsung ada `SKILL.md`), bukan folder hasil ekstrak ZIP yang membungkusnya.

## Pilih platform yang kamu pakai

| Platform | Folder tujuan global (Mac/Linux) | Folder tujuan proyek (opsional) | Cek skill terpasang |
|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` | `.claude/skills/` di repo | ketik `/skills` |
| **OpenAI Codex** | `~/.agents/skills/` | `.agents/skills/` (dari folder kerja hingga root repo) | ketik `/skills` |
| **Cursor** | `~/.cursor/skills/` atau `~/.agents/skills/` | `.cursor/skills/` atau `.agents/skills/` di repo | ketik `/nama-skill` di Agent chat, atau Settings → Rules |
| **OpenClaw** | `~/.openclaw/skills/` | `skills/` di workspace OpenClaw | `openclaw skills list` |

**Windows (global):** `%USERPROFILE%\.claude\skills\`, `%USERPROFILE%\.agents\skills\`, `%USERPROFILE%\.cursor\skills\` — struktur sama, hanya lokasi home Windows.

Memakai lebih dari satu platform? Salin folder skill ke **masing-masing** folder tujuan. Hindari memasang skill **identik** di banyak folder sekaligus pada **satu** platform (mis. `~/.cursor/skills` dan `~/.claude/skills` di Cursor), agar agent tidak memuat dobel.

## Cara termudah: lewat File Explorer / Finder

**Windows**
1. Ekstrak ZIP (klik kanan → *Extract All*).
2. Tekan **Win + R**, tempel alamat folder tujuan dari tabel (mis. `%USERPROFILE%\.claude\skills`), tekan Enter.
   Jika muncul pesan folder tidak ditemukan: buka `%USERPROFILE%`, buat folder `.claude`, lalu di dalamnya buat folder `skills`.
3. Seret folder skill ke jendela tersebut.

**Mac**
1. Klik dua kali ZIP untuk mengekstrak.
2. Di Finder tekan **Cmd + Shift + G**, tempel alamat folder tujuan (mis. `~/.claude/skills`), tekan Enter.
   Jika folder belum ada: tekan **Cmd + Shift + .** untuk menampilkan folder tersembunyi, lalu buat foldernya.
3. Seret folder skill ke jendela tersebut.

## Cara cepat: satu perintah

Jalankan di folder tempat file ZIP berada. Ganti `NAMA-FILE.zip` dan folder tujuan sesuai platform.

**Windows (PowerShell)**
```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Expand-Archive NAMA-FILE.zip "$env:USERPROFILE\.claude\skills" -Force
```

**Mac / Linux (Terminal)**
```bash
mkdir -p ~/.claude/skills && unzip -o NAMA-FILE.zip -d ~/.claude/skills
```

File `LISENSI.txt` dan `CARA-INSTAL.md` yang ikut terekstrak boleh dipindah/dihapus dari folder skills.

## Catatan per platform

**OpenClaw.** Cara paling andal untuk semua agent di mesin yang sama:
```bash
openclaw skills install ./nama-skill --global
```
Skill masuk ke `~/.openclaw/skills/`. Untuk **satu workspace** saja, hilangkan `--global` (skill masuk folder `skills/` workspace). Alternatif: halaman **Plugins → Skills** di gateway, atau impor ZIP bila tersedia. Skill terbaca pada pesan berikutnya; cek dengan `openclaw skills check`.

**Claude Code.** Skill di `~/.claude/skills/` atau `.claude/skills/` repo terbaca otomatis. Jika folder global baru dibuat saat sesi sudah jalan, jalankan `/reload-skills` atau buka sesi baru.

**Codex.** Skill user di `~/.agents/skills/`; skill tim di `.agents/skills/` di repo. Skill terbaca pada pesan berikutnya. Bisa dipanggil langsung dengan `$nama-skill`.

**Cursor.** Agent memuat skill dari folder proyek (`.cursor/skills/`, `.agents/skills/`) dan folder user di komputer lokal. Untuk **Cursor Cloud Agent**, skill di `~/.cursor/skills/` **tidak otomatis ikut** — pasang skill di **repo** (`.cursor/skills/`) atau aktifkan **Sync Skills** di Settings → Agents bila ingin memakai skill pribadi di cloud. Setelah memasang, buka chat Agent baru. **Catatan uji 2026-10-14:** pada run **Cloud Automation** (jadwal otomatis) Cursor, skill di `.cursor/skills/` repo tidak muncul di daftar skill agent pada empat run berturut; pemasangan dan script tetap berjalan. Untuk memakai skill di Cursor, pakai chat Agent di aplikasi Cursor, bukan jadwal otomatis, sampai Cursor memperbaikinya. Cursor juga bisa membaca skill dari folder Claude/Codex (`~/.claude/skills`, `~/.codex/skills`) untuk kompatibilitas; jangan duplikasi skill yang sama di banyak folder.

## Khusus pembeli paket VIP

Selain folder-folder skill, ZIP VIP berisi dua tambahan:
- **`solusi-vip/`** — panduan per profesi (toko online, klinik, konsultan, usaha offline, kantor & manajemen, kripto & keuangan pribadi). Mulai dari `solusi-vip/README.md`, lalu buka `PANDUAN.md` dan `CEKLIS.md` di folder profesimu. Isinya file panduan (`.md`), bukan skill; tidak perlu disalin ke folder skills.
- **`templates/openclaw-AGENTS-komunitech.md`** — blok aturan kerja untuk OpenClaw. Panduan solusi-vip merujuknya: tempel isinya ke file `AGENTS.md` agent OpenClaw-mu (ikuti langkah di `PANDUAN.md`).

Memasang semua skill VIP satu per satu (salin manual per folder) memakan waktu kira-kira 1–2 menit, jadi lebih cepat bila seluruh folder skill disalin sekaligus ke folder tujuan.

## Skill yang memakai script

Beberapa skill menyertakan script Python (folder `scripts/`). Mac dan Linux umumnya sudah punya Python. Di Windows, pasang gratis dari [python.org](https://www.python.org/downloads/) dan centang **"Add Python to PATH"** saat instalasi. Tanpa Python, skill tetap berjalan tetapi perhitungan tidak diverifikasi script.

## Masalah umum

| Masalah | Solusi |
|---|---|
| Skill tidak muncul | Pastikan `SKILL.md` ada **langsung** di dalam folder skill, bukan di dalam folder bertingkat. Buka sesi/chat baru. |
| Skill tidak dipakai otomatis | Sebut kebutuhannya lebih jelas, atau panggil namanya langsung (mis. "pakai skill kasir-lokal" atau `/kasir-lokal` di Cursor). |
| Error "python not found" | Pasang Python (lihat di atas), lalu buka ulang aplikasi. |
| Skill hilang di Cursor Cloud | Pasang di `.cursor/skills/` dalam repo, atau sync skill user lewat Settings → Agents. |

---
*Verifikasi lokasi folder: Cursor, Claude Code, Codex, OpenClaw — **2026-10-14** (sumber resmi; lihat `research/sources/platform-2026-10-14.md`). Platform sekunder (Antigravity, Hermes, Grok, Muse) belum terverifikasi. Hubungi Komunitech bila ada kendala.*
