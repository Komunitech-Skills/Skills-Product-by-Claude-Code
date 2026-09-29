# Laporan KPI terjadwal di OpenClaw (Telegram)

Pola perintah di bawah **disalin dari skill `laporan-otomatis-terjadwal`** (Komunitech), yang
sudah menjalankan `openclaw automations add/run/show/disable/enable/edit/rm/list` terhadap Gateway
OpenClaw 2026.9.5 lokal (lihat `references/openclaw.md` skill itu). Skill kpi-tim **sendiri belum
diuji** di Gateway: jika sebuah flag ditolak di versi OpenClaw pengguna, jalankan
`openclaw automations add --help` dan sesuaikan, lalu beri tahu pengguna.

## Aturan sebelum membuat jadwal

1. **Tunjukkan contoh laporan pertama** (hasil `skor_kpi.py skor`) dan minta persetujuan.
2. **Penerima hanya pemilik/manajer** (satu chat pribadi). Laporan berisi skor per orang
   **tidak boleh** dikirim ke grup karyawan. Untuk grup, pakai `--tanpa-nama` (hanya perusahaan &
   divisi) dan tetap minta persetujuan pemilik.
3. **Telegram = default.** WhatsApp hanya dengan nomor terpisah, ke pemilik sendiri, dan
   persetujuan risiko tertulis (WhatsApp Web tidak resmi, nomor bisa diblokir). Tidak ada
   broadcast.
4. Minta izin eksplisit ("Lanjut? ya/tidak") sebelum menjalankan perintah `openclaw`.
5. Jika perintah komputer tidak diizinkan / bukan OpenClaw: berikan perintah sebagai teks siap
   salin, atau arahkan ke Control UI (Settings → Automations).

## Susunan folder yang disarankan

```
KPI/
├── rencana-kpi.csv          ← atau .xlsx dari Excel/Google Sheets
├── realisasi.csv            ← satu file, semua periode (kolom periode), ditambah tiap minggu/bulan
└── RESEP-laporan-kpi.md     ← catatan: perintah, jadwal, penerima (ditulis agent)
```

## Perintah yang dijalankan jadwal (contoh bulanan)

```bash
python3 <folder-skill>/scripts/skor_kpi.py skor --rencana KPI/rencana-kpi.csv \
  --realisasi KPI/realisasi.csv --periode <periode>
```
(Windows: `python` atau `py`.) Mingguan: periode berbentuk `2026-W40`.

## Membuat jadwal (Bentuk A: jadwal & pesan sebagai argumen posisi, TANPA `--cron`)

Bulanan, tanggal 2 pukul 07.00 WIB (memberi waktu 1 hari untuk data akhir bulan):
```bash
openclaw automations add "0 7 2 * *" \
  "Jalankan resep di KPI/RESEP-laporan-kpi.md untuk bulan lalu (format periode YYYY-MM). Pakai HANYA angka dari output skor_kpi.py, jangan menghitung atau membulatkan sendiri. Kirim apa adanya, maksimal 25 baris. Kalau script error atau belum ada realisasi untuk periode itu, kirim pesan singkat 'Data KPI <periode> belum lengkap: <isi error>' dan JANGAN kirim angka nol." \
  --name "Laporan KPI bulanan" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

Mingguan, Senin 07.30 WIB (untuk KPI mingguan / check-in OKR):
```bash
openclaw automations add "30 7 * * 1" "<pesan seperti di atas, periode minggu lalu YYYY-Www>" \
  --name "Laporan KPI mingguan" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```

Jangan menambah `--cron`/`--at`/`--every` pada Bentuk A (argumen posisi pertama akan dianggap
nama dan bentrok dengan `--name`). Bentuk B (opsi penuh): `openclaw automations add --cron
"0 7 2 * *" --message "<pesan>" --tz "Asia/Jakarta" --name "..." --session isolated --announce
--channel telegram --to "<id>"`.

## Setelah dibuat

- Catat `id` dari output JSON `add`. `run`/`disable`/`enable`/`edit`/`rm` **hanya menerima id**
  (nama → "Automation not found"). Lupa id: `openclaw automations list --all`.
- Uji sekali sebelum dianggap aktif: `openclaw automations run <id> --wait`, tunjukkan hasilnya.
- Kelola: `openclaw automations show <id>`, `disable <id>`, `enable <id>`,
  `edit <id> --cron "..."`, `rm <id>`.
- **Komputer/Gateway harus menyala** saat jam jadwal; kalau mati, laporan tidak terkirim (tanpa
  pesan error). Opsi: laptop/mini PC selalu menyala, VPS milik sendiri, atau jasa setup
  Komunitech (lihat `laporan-otomatis-terjadwal/references/mesin-24-jam.md` bila terpasang).
- Setiap run memakai token model (biaya pengguna). `--session isolated` sudah dipasang.

## Pengingat isi data (opsional)

Pengingat ke **pemilik/manajer sendiri** tanggal 1 pukul 16.00: "Waktunya mengisi realisasi KPI
bulan ini di KPI/realisasi.csv (atau kirim rekap grup WA ke saya)". Bentuknya sama, pesannya
cukup teks pengingat. Jangan mengirim pengingat otomatis ke karyawan lewat OpenClaw.
