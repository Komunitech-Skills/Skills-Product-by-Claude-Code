# Ringkasan harian otomatis ke Telegram (OpenClaw)

**Status verifikasi (jujur).** Flag `openclaw automations add --command-argv ... --announce
--channel telegram --to ...` di bawah disalin dari pola yang sama yang sudah dijalankan sungguhan
di Gateway OpenClaw untuk `crm-wa` dan `pengingat-follow-up`
(`skills/crm-wa/references/openclaw-jadwal.md`, `skills/pengingat-follow-up/references/openclaw-jadwal.md`)
dan untuk paket klinik (`solusi-vip/klinik/jadwal-openclaw.md`). **Tidak ada flag baru yang
ditebak di sini.** Kombinasi utuh khusus skill `pengingat-pasien-klinik` **belum diuji** di
Gateway sungguhan — tandai 📖 (flag terverifikasi di skill lain, kombinasi ini belum dicoba)
sampai diuji ulang saat Tahap 6.

## Aturan (mengikuti keputusan pemilik Komunitech, 2026-09-23 & 2026-09-26)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik/PIC klinik**, bukan pasien
  atau grup.
- Jadwal ini hanya menjalankan perintah **baca** (`ringkasan`), **tidak pernah** `tambah`,
  `ubah`, `ubah-status`, `hapus`, `impor`, atau `--ya`.
- **Selalu pakai `--samarkan`** pada job terjadwal: teksnya tersimpan di riwayat chat Telegram
  pemilik, jadi nama pasien ditampilkan inisial. Ringkasan **tidak pernah** memuat nomor WA
  (dengan atau tanpa `--samarkan`), jadi tidak ada risiko nomor pasien bocor ke Telegram.
- Tidak ada WhatsApp untuk pengingat pasien: kanal ke pemilik memakai Telegram saja. WhatsApp
  hanya diizinkan untuk **draf yang dikirim manusia**, bukan untuk automations OpenClaw.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" ke pemilik/PIC sebelum membuat jadwal.

## Syarat
- Gateway OpenClaw berjalan di komputer yang **sama dengan file `pasien/DAFTAR.csv`** dan
  **menyala saat jadwal** (laptop/mini PC yang selalu menyala atau VPS milik klinik; Komunitech
  menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik/PIC diketahui.
- Zona waktu jadwal (`--tz`) sama dengan zona pemakaian sehari-hari (default Asia/Jakarta/WIB).

## Perintah langsung (disarankan, tanpa kuota model)
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/pengingat-pasien-klinik/scripts/pengingat_pasien.py'))"
   ```
2. Ringkasan harian jam 07.30 WIB:
   ```bash
   openclaw automations add --name "Ringkasan pengingat pasien harian" --cron "30 7 * * *" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/pengingat-pasien-klinik/scripts/pengingat_pasien.py","--file","/path/ke/pasien/DAFTAR.csv","ringkasan","--samarkan"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
   - Ganti `/path/ke/pasien/DAFTAR.csv` dengan lokasi file sungguhan di komputer klinik.
   - Ingin ringkasan tanpa daftar nama sama sekali (hanya angka): tambahkan `"--tanpa-nama"`.
   - Windows: ganti `"python3"` dengan `"py"` (belum diuji).
3. WITA: `--tz Asia/Makassar`; WIT: `--tz Asia/Jayapura`.

## Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id>` |
| Lihat hasil | `openclaw automations runs <id>` |
| Hentikan / aktifkan | `openclaw automations disable <id>` / `enable <id>` |
| Hapus | `openclaw automations rm <id>` |

## Yang BELUM diverifikasi ⚠️
- Kombinasi utuh job terjadwal + script `pengingat_pasien.py` di Gateway OpenClaw sungguhan
  (pola cron & `--command-argv`-nya sendiri sudah ✅ untuk skill lain).
- Draf pesan **per pasien** tidak dijadwalkan otomatis dan memang **tidak boleh** — draf hanya
  dibuat lewat `daftar`/`draf` yang dijalankan staf secara sadar, bukan lewat automations, agar
  tidak ada risiko draf berisi data pasien tersimpan di riwayat chat Telegram/WhatsApp pemilik
  tanpa disadari.
- Tanpa OpenClaw (Claude Code/Codex/Cursor): staf cukup mengetik "daftar pengingat hari ini" tiap
  pagi, atau memasang pengingat kalender sendiri.
