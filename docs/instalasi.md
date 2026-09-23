# Cara Memasang Skill Komunitech

Skill adalah **folder** berisi file `SKILL.md`. Cara memasangnya: **salin folder skill ke folder "skills" milik AI agent kamu.** Setelah itu, cukup minta tolong seperti biasa. AI agent akan memakai skill secara otomatis bila relevan.

> Pastikan yang disalin adalah folder skill-nya (misalnya `caption-sosmed-umkm`, yang di dalamnya langsung ada `SKILL.md`), bukan folder hasil ekstrak ZIP yang membungkusnya.

## Pilih platform yang kamu pakai

| Platform | Folder tujuan (Mac/Linux) | Folder tujuan (Windows) | Cek skill terpasang |
|---|---|---|---|
| **Claude Code** | `~/.claude/skills/` | `%USERPROFILE%\.claude\skills\` | ketik `/skills` |
| **OpenAI Codex** | `~/.agents/skills/` | `%USERPROFILE%\.agents\skills\` | ketik `/skills` |
| **Cursor** | `~/.cursor/skills/` | `%USERPROFILE%\.cursor\skills\` | ketik `/` di chat, cari nama skill |
| **OpenClaw** | `~/.openclaw/skills/` | lihat catatan OpenClaw di bawah | `openclaw skills list` |

Memakai lebih dari satu platform? Salin folder skill ke **masing-masing** folder tujuan.

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

**OpenClaw.** Cara paling andal (juga untuk Windows yang memakai WSL):
```bash
openclaw skills install ./nama-skill --global
```
Atau lewat halaman **Plugins → Skills** (impor ZIP/SKILL.md) jika tersedia di gateway kamu. Skill terbaca pada pesan berikutnya; cek dengan `openclaw skills check`.

**Claude Code.** Skill terbaca otomatis. Jika folder `skills` baru saja dibuat, tutup dan buka lagi Claude Code.

**Codex.** Skill terbaca pada pesan berikutnya. Bisa juga dipanggil langsung dengan `$nama-skill`.

**Cursor.** Buka chat baru (atau restart Cursor) setelah memasang. Cursor juga membaca `~/.claude/skills` dan `~/.agents/skills`, jadi jangan pasang skill yang sama di beberapa folder itu sekaligus agar tidak dobel.

## Skill yang memakai script

Beberapa skill menyertakan script Python (folder `scripts/`). Mac dan Linux umumnya sudah punya Python. Di Windows, pasang gratis dari [python.org](https://www.python.org/downloads/) dan centang **"Add Python to PATH"** saat instalasi. Tanpa Python, skill tetap berjalan tetapi perhitungan tidak diverifikasi script.

## Masalah umum

| Masalah | Solusi |
|---|---|
| Skill tidak muncul | Pastikan `SKILL.md` ada **langsung** di dalam folder skill, bukan di dalam folder bertingkat. Buka sesi/chat baru. |
| Skill tidak dipakai otomatis | Sebut kebutuhannya lebih jelas, atau panggil namanya langsung (mis. "pakai skill caption-sosmed-umkm"). |
| Error "python not found" | Pasang Python (lihat di atas), lalu buka ulang aplikasi. |

---
*Lokasi folder diverifikasi 2026-09-23 dari dokumentasi/kode sumber resmi. Aplikasi bisa berubah; hubungi Komunitech bila ada kendala.*
