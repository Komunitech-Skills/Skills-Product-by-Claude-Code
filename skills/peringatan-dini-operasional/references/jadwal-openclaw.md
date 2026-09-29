# Menjadwalkan peringatan dini harian di OpenClaw

Pola perintah di bawah **disalin dari skill `laporan-otomatis-terjadwal`** (lihat
`references/openclaw.md` di skill itu), yang sudah diverifikasi lewat `--help` dan dijalankan
sungguhan terhadap Gateway uji OpenClaw **2026.9.5**. Skill ini tidak menambah perintah/flag baru.
Kalau versi OpenClaw pengguna berbeda dan sebuah flag gagal, jalankan
`openclaw automations add --help` dulu dan beri tahu pengguna.

Kalau pengguna juga memasang `laporan-otomatis-terjadwal`, pakai alur lengkap skill itu
(kanal, izin WhatsApp, mesin 24 jam). Ringkasan di bawah cukup untuk kasus peringatan dini.

## 0. Syarat
- Log harian disimpan di **satu file tetap** di komputer yang menjalankan OpenClaw, mis.
  `Dokumen/Laporan-AI/log-harian.csv` (atau `.xlsx`), dan diisi tiap hari sebelum jam kirim.
- Kanal **Telegram** (default, bot resmi) sudah ditambahkan:
  `openclaw channels add --channel telegram --token <token-dari-BotFather>`.
- WhatsApp hanya dengan **nomor terpisah**, laporan hanya ke pemilik sendiri, dan persetujuan
  risiko tertulis (lihat `laporan-otomatis-terjadwal` Langkah 4). Tidak pernah ke grup/pelanggan.
- Komputer/Gateway harus menyala pada jam kirim; kalau mati, laporan tidak terkirim.

## 1. Uji manual dulu (sebelum membuat jadwal)
```bash
python3 <folder-skill-ini>/scripts/peringatan_dini.py "<path-log>" --nama-usaha "<nama>" [opsi target/stok]
```
(Windows: `python` atau `py`.) Tunjukkan hasilnya ke pengguna sebagai contoh pesan pertama.

## 2. Buat jadwal (Bentuk A — minta izin "ya" dulu)
```bash
openclaw automations add "0 20 * * *" \
  "Pakai skill peringatan-dini-operasional. Jalankan scripts/peringatan_dini.py pada file <path-log> dengan --tanggal <tanggal hari ini WIB, YYYY-MM-DD> --nama-usaha \"<nama>\" <opsi target/stok yang sama dengan uji manual>. Kirim isi laporan teks apa adanya (jangan mengubah angka, jangan menambah angka). Kalau hasilnya LOG HARIAN BELUM DIISI atau GALAT, kirim itu saja dengan singkat -- JANGAN menulis 'aman' atau angka nol." \
  --name "Peringatan dini harian" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
- Jangan menambahkan `--cron`/`--at`/`--every` pada Bentuk A (argumen posisi pertama akan
  berubah arti menjadi nama job dan bentrok dengan `--name`).
- Jam lain: `"0 7 * * *"` (pagi, untuk log kemarin → pakai `--tanggal` = tanggal kemarin),
  `"0 20 * * 1-6"` (Senin–Sabtu saja).
- **Catat `id`** dari hasil `add` (field `"id"`). `run`/`disable`/`enable`/`edit`/`rm` hanya
  menerima id, bukan nama.

## 3. Uji sekali, lalu kelola
```bash
openclaw automations run <id> --wait     # uji sekarang, tunjukkan hasilnya ke pengguna
openclaw automations list --all          # lihat semua jadwal (cari id lewat nama)
openclaw automations disable <id>        # jeda
openclaw automations enable <id>         # aktifkan lagi
openclaw automations edit <id> --cron "0 19 * * *" --tz "Asia/Jakarta"   # ubah jam
openclaw automations rm <id>             # hapus permanen
```

## 4. Kalau tidak memakai OpenClaw / perintah komputer tidak diizinkan
Berikan perintah di atas sebagai teks siap salin-tempel, atau arahkan ke Control UI
(`Settings → Automations`). Claude Code / Codex / Cursor tidak punya penjadwal OpenClaw; di sana
skill dipakai manual (kirim file → dapat laporan).

Setiap run memakai token model (biaya ditanggung pengguna); `--session isolated` menjaga jadwal
tidak mencampuri chat utama.
