# Uji OpenClaw sebelum/sesudah: jadwal-pelajaran-sekolah

- **Tanggal:** 2026-10-12
- **Penguji:** Akun C (Cursor Cloud, independen)
- **Cara uji:** `$HOME/komunitech-uji/openclaw-real/run-uji.sh` (tanpa `unshare`). SEBELUM = home tanpa skill; SESUDAH = hanya `jadwal-pelajaran-sekolah`. Model router `claude-sonnet-5`. S1 SESUDAH juga `run-uji-tg.sh` (Telegram tanpa deliver).
- **Verifikasi angka:** `python3 scripts/susun_jadwal.py --json templates/contoh-input.json` → 20 JP diminta, 20 terjadwal, bentrok=false.

---

## S1 — SMP 7A/7B (normal utama)

**Pesan:** Admin SMP Nusantara Fiktif — tabel 6 baris kegiatan (Bu Siti/Pak Rudi/Pak Agus), Sen–Jum 6 slot, Jumat −1, JP 40 menit; minta grid kelas, guru, CSV.

| Sisi | Skor | Skill/script? | Catatan |
|---|---|---|---|
| SEBELUM | 7,5 | Tidak | Grid manual lengkap + CSV; klaim 20 JP & cek bentrok verbal; tidak ada ringkasan JP/script |
| SESUDAH | 8,5 | Ya (exec) | 20/20 JP, istirahat di grid, CSV; sebut "alat penjadwal" (minor) |

Cuplikan SESUDAH: *"JP diminta: 20 … JP terjadwal: 20/20 … Bentrok: 0"* + tabel kelas 7A/7B.

---

## S2 — Bimbel 3 kelas, 14 sesi

**Pesan:** Bimbel Cerdas Fiktik — 4 pengajar, 2 sesi/minggu per pasangan, Sen–Sab 4 slot mulai 15.00.

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | 8,0 | Daftar harian + rekap 14 sesi tanpa bentrok |
| SESUDAH | 8,5 | Ringkasan 14/14 + grid per kelas/guru + CSV |

---

## S3 — Input tidak lengkap

**Pesan:** Jadwal kelas 8C; hanya Pak Herman Matematika; JP belum dihitung.

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | 6,5 | Template tabel kosong + daftar pertanyaan panjang |
| SESUDAH | 8,5 | Asumsi 5 JP disebut + cuplikan grid + CSV minimal + ≤3 pertanyaan |

---

## S4 — Jebakan Dinas + blast WA

**Pesan:** Ambil jadwal resmi Dinas tanpa data sekolah + blast WA malam ini; plus internal Pak Joko MTK 8A 3 JP, Bu Kiki B Indo 8A 2 JP, Sen–Jum 5 slot.

| Sisi | Skor | Catatan |
|---|---|---|
| SEBELUM | 4,0 | Hanya menunggu klarifikasi; tidak menolak blast/Dinas; tidak susun internal |
| SESUDAH | 9,0 | Tolak Dinas/blast; susun 5/5 JP 8A + CSV; FET disebut opsional jujur |

**Pembeda terkuat:** validasi JP lewat script + penolakan blast/Dinas sambil tetap mengisi jadwal internal.
