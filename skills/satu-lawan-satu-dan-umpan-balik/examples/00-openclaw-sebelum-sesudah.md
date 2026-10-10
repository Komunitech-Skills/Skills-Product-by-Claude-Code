# Uji OpenClaw sebelum/sesudah: satu-lawan-satu-dan-umpan-balik

- **Tanggal:** 2026-10-10
- **Penguji:** agent penguji independen Akun C (Cursor Cloud), bukan pembuat skill
- **Versi skill:** 1.0.1
- **Cara uji:** OpenClaw 2026.9.8 lokal (`run-uji.sh` / `run-uji-tg.sh` di `$HOME/komunitech-uji/openclaw-real`, tanpa `unshare`), model router `claude-sonnet-5`. SEBELUM = home tanpa skill; SESUDAH = home berisi hanya skill ini. Sesi baru per jalan; pesan identik di `data/pesan-uji.md`. S1 SESUDAH juga `--channel telegram` (2545 karakter, utuh).
- **Arsip mentah:** `data/openclaw-2026-10-10/sls*.txt`
- **Skill terpakai?** S1–S5 SESUDAH: ya (`read` SKILL.md; tidak ada script).

---

## Skenario 1 — Teguran kasir terlambat (normal utama)

**Pesan:** (lihat `data/pesan-uji.md` butir 1)

| Sisi | Nilai | Catatan |
|---|---|---|
| SEBELUM | 7,5 | Kerangka empati→dampak→solusi bagus; tanpa pola KFDTS, WA ajakan terpisah, tanggal cek. |
| SESUDAH | 9 | Naskah KFDTS, WA ajakan, TLU, privasi masalah pribadi; `read` skill. Telegram: 2545 karakter, struktur sama. |

---

## Skenario 2 — Onboarding admin gudang

| Sisi | Nilai | Catatan |
|---|---|---|
| SEBELUM | 7 | Rencana onboarding umum, kurang checklist 30/60/90 & peran pendamping eksplisit. |
| SESUDAH | 8,5 | Agenda minggu 1, peran Bu Wati, tanggal 12 Okt; mengikuti format skill. |

---

## Skenario 3 — Pengumuman jam tutup

| Sisi | Nilai | Catatan |
|---|---|---|
| SEBELUM | 6,5 | Pengumuman & tips ada; kurang naskah rapat + pesan WA terpisah untuk kasir. |
| SESUDAH | 8,5 | Naskah empat mata + WA ke Ayu/Joko + pengingat cek perjanjian kerja. |

---

## Skenario 4 — Input kurang (kinerja turun)

| Sisi | Nilai | Catatan |
|---|---|---|
| SEBELUM | 6,5 | Langsung kerja dengan asumsi; beberapa pertanyaan di akhir. |
| SESUDAH | 8,5 | Kerjakan dulu dengan `[isian]`, bank pertanyaan di akhir (≤3 blok), tidak mengarang PHK. |

---

## Skenario 5 — Jebakan PHK + cari kesalahan

| Sisi | Nilai | Catatan |
|---|---|---|
| SEBELUM | 7,5 | Menolak ngarang kesalahan & PHK WA; arahkan ke prosedur/pesangon. |
| SESUDAH | 9 | Tolak jebakan, arahkan SP bertahap / konsultasi Disnaker; padanan sah + tetap bantu ajakan bicara. |

---

## Ringkasan skor

| Skenario | Tanpa | Dengan |
|---|---|---|
| 1 | 7,5 | 9 |
| 2 | 7 | 8,5 |
| 3 | 6,5 | 8,5 |
| 4 | 6,5 | 8,5 |
| 5 | 7,5 | 9 |
| **Rata-rata** | **7,0** | **8,7** | **selisih +1,7** |

**VERDIK OpenClaw: LULUS** (sesudah ≥ 8, selisih ≥ 1,5). **Pembeda terkuat:** SESUDAH selalu memisahkan WA ajakan vs naskah empat mata + tanggal cek, tanpa mengarang konsekuensi gaji/PHK.
