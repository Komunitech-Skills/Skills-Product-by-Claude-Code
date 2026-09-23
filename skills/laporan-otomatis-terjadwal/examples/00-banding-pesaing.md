# 00 — Uji banding pesaing: laporan-otomatis-terjadwal

Tanggal: 2026-09-23. Sumber hanya dibaca; tidak ada script pihak ketiga dijalankan; tidak ada teks disalin.

## Pencarian
| Sumber | Kata kunci | Hasil |
|---|---|---|
| Web | "openclaw skill scheduled report cron telegram daily business report clawhub" | `openclaw-cron` (Liuzln/openclaw-skills, via skills.lc & LobeHub); artikel panduan cron (RamNode, SFAI Labs, Stack Junkie) — bukan skill |
| github.com/VoltAgent/awesome-openclaw-skills | kategori laporan/otomasi | `biz-reporter` (GA4/Stripe/HubSpot via API, ditandai "Suspicious" oleh VirusTotal/OpenClaw di clawskills.sh), `daily-report`, `ai-daily-briefing` — tidak ada yang berbasis file CSV lokal + UMKM Indonesia |
| manairalabs/bicara-skills, alvinindra/bahasa-skills | daftar skill | Tidak ada skill laporan terjadwal |
| anthropics/skills, skills.sh | laporan terjadwal | Tidak ditemukan yang sebanding |

## Pesaing yang dinilai
**`openclaw-cron`** — https://github.com/Liuzln/openclaw-skills (SKILL.md: `skills/openclaw-cron/SKILL.md`, branch `master`). Lisensi: **MIT** (dinyatakan di README; file LICENSE tidak ditemukan di raw branch). 6 bintang. Isi: pembungkus perintah `openclaw cron add/list/run/disable/runs`, pola jadwal, daftar opsi, bahasa Mandarin + Inggris, contoh zona waktu Asia/Shanghai.

`biz-reporter` tidak dijalankan: butuh API pihak ketiga dan ditandai mencurigakan.

## S1 dengan instruksi pesaing
Input: "Buatkan laporan penjualan otomatis tiap Senin jam 7 pagi, kirim ke Telegram saya. File kasirnya saya taruh di folder laporan/masuk/penjualan, chat id telegram saya 123456789"

**Agent dengan `openclaw-cron`:**
```
openclaw cron add \
  --name "Laporan penjualan mingguan" \
  --cron "0 7 * * 1" \
  --tz "Asia/Jakarta" \
  --agent main \
  --message "Baca CSV terbaru di laporan/masuk/penjualan dan buat laporan penjualan minggu lalu" \
  --announce \
  --channel telegram \
  --to "telegram:123456789"

Uji: openclaw cron run <job-id>
Jeda: openclaw cron disable <job-id>
```
Catatan penguji atas output pesaing:
- Sintaks dasar valid di OpenClaw 2026.9.5 (`--name/--cron/--tz/--agent/--message/--announce/--channel/--to`). Pesaing menyebut `--account-id` untuk akun Telegram khusus — flag itu **tidak ada** (yang benar `--account`, dicek `--help`).
- Tidak ada perhitungan angka (model menghitung sendiri tiap minggu), tidak ada cek data kosong, tidak ada contoh laporan pertama, tidak ada batas privasi/kanal, tidak ada konteks Rupiah/WIB/WhatsApp.

**Agent dengan skill kita:** lihat `01-penjualan-mingguan-telegram.md`.

## Penilaian (1–10)
| Kriteria | openclaw-cron | **laporan-otomatis-terjadwal** |
|---|---|---|
| Kualitas hasil S1 | 5 (jadwal jadi, isi laporan tak terjamin) | **8** |
| Kesesuaian konteks Indonesia | 2 | **9** |
| Akurasi (angka & perintah) | 5 (angka tidak dihitung script; 1 flag salah) | **7** (angka benar; beberapa perintah di references salah — lihat HASIL-UJI) |
| Siap pakai untuk awam | 4 | **8** |

**Kesimpulan:** skill kita **menang** jelas. Pesaing hanya pembungkus CLI umum.

## Yang bisa dipelajari (ide, bukan salinan)
- Pesaing menyajikan "pola umum" jadwal (harian/mingguan/per jam/sekali jalan) dalam satu tabel singkat — skill kita bisa menambah tabel cron siap pakai ber-WIB (mis. "setiap hari kerja 07:30" = `30 7 * * 1-5`).
- Saran memakai akun/bot Telegram khusus laporan agar chat utama tidak penuh — relevan untuk pemilik yang juga memakai bot untuk CS.
- Pesaing menunjukkan `openclaw cron runs <id>` untuk riwayat — sudah ada di references kita, bisa dinaikkan ke SKILL.md Langkah 7.
