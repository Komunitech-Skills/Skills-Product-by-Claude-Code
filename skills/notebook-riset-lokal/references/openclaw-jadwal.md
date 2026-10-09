# Ringkasan notebook terjadwal ke Telegram (OpenClaw)

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Status verifikasi (jujur).** Bentuk perintah di bawah mengikuti pola yang sudah dijalankan sungguhan
di Gateway lokal OpenClaw **2026.9.5/2026.9.6** untuk skill lain di repo ini (`vikunja-tugas`,
`dolibarr-usaha`, `kasir-lokal`: job diterima, jadwal & zona waktu tersimpan, `automations run`
menjalankan script). Untuk `notebook-riset-lokal` sendiri, jadwal **belum** diuji di Gateway
sungguhan maupun terhadap Open Notebook sungguhan (lihat `ATTRIBUTION.md`) — pengiriman ke Telegram
belum diuji (butuh token bot asli & Open Notebook asli). Jika sebuah opsi ditolak, jalankan
`openclaw automations add --help`.

## Aturan (keputusan pemilik Komunitech, 2026-09-23)
- **Telegram (bot resmi) = default.** `--to` selalu ID chat **pemilik/admin**, bukan pelanggan atau grup.
- **Tidak ada broadcast** dan tidak ada pesan otomatis ke pelanggan — ringkasan notebook adalah riset internal, tapi aturan ini tetap berlaku untuk semua jadwal.
- Jadwal hanya menjalankan perintah **baca** (`ringkasan`, `daftar-sumber`, `cari`); tidak pernah `--ya`, `tambah-sumber`, `buat-notebook`, `podcast-mulai`.
- Tunjukkan perintahnya + "Lanjut? (ya/tidak)" sebelum membuat jadwal.
- **Privasi:** ringkasan berisi isi dokumen yang Anda kumpulkan sendiri (regulasi, katalog supplier, notulen internal) dan akan tersimpan di riwayat chat Telegram pemilik. Beri tahu pemilik sebelum membuat jadwal, terutama bila notebook berisi dokumen sensitif (kontrak, data internal).
- Ringkasan berjadwal memakai kuota model AI Open Notebook (lokal/API) setiap kali jalan — beri tahu pemilik bila memakai API berbayar, biaya berulang setiap jadwal.

## Syarat
- Gateway OpenClaw berjalan di komputer/jaringan yang bisa menjangkau Open Notebook (idealnya **komputer yang sama**, karena Open Notebook dibatasi ke `127.0.0.1` — lihat `docs/panduan-open-notebook.md` §4) dan **menyala saat jadwal** (Docker Desktop harus tetap terbuka; laptop/mini PC yang selalu menyala atau VPS milik pemilik — Komunitech menyediakan jasa setup berbayar).
- Kanal Telegram sudah tersambung dan ID chat pemilik diketahui.
- Model AI default sudah diatur di Open Notebook (`docs/panduan-open-notebook.md` §5) — tanpa ini, `ringkasan` gagal setiap kali jadwal jalan.
- Kata sandi API (bila diaktifkan) sudah disimpan (`simpan-kunci`, lihat SKILL.md bagian Persiapan).

## Pilihan 1 (disarankan): perintah langsung, tanpa model AI orkestrasi
Teks script dikirim apa adanya. Model AI Open Notebook sendiri tetap dipakai untuk menyusun ringkasan (bagian dari perintah `ringkasan`), tapi tidak memakai kuota model agent OpenClaw untuk memformat ulang.
1. Cari path lengkap script (`--command-argv` tidak mengenal `~`):
   ```bash
   python3 -c "import os; print(os.path.expanduser('~/.openclaw/skills/notebook-riset-lokal/scripts/notebook.py'))"
   ```
2. Ringkasan mingguan notebook "Regulasi Pajak UMKM", Senin 07.00 WIB:
   ```bash
   openclaw automations add --name "Notebook - ringkasan regulasi pajak" --cron "0 7 * * 1" --tz Asia/Jakarta \
     --command-argv '["python3","/home/NAMA/.openclaw/skills/notebook-riset-lokal/scripts/notebook.py","ringkasan","--notebook","Regulasi Pajak UMKM"]' \
     --announce --channel telegram --to <chat-id-telegram-pemilik>
   ```
- Kata sandi API **tidak** ditulis ke dalam `--command-argv` (jangan pernah menambahkan `--kunci-file`/kata sandi ke argv jadwal). Script membaca kata sandi dari file default (`~/.komunitech/open-notebook-kunci.txt`) atau ENV — untuk ENV, pakai `--command-env` **hanya** untuk `OPEN_NOTEBOOK_URL` (bukan `OPEN_NOTEBOOK_TOKEN`), mis. `--command-env '{"OPEN_NOTEBOOK_URL":"http://127.0.0.1:5055"}'`, agar kata sandi tidak pernah tersimpan di konfigurasi jadwal.
- Windows: pakai `"py"` sebagai ganti `"python3"` (belum diuji) atau Pilihan 2.

## Pilihan 2: pesan ke agent (model AI membaca skill)
Memakai kuota model tambahan (agent OpenClaw). `--tools exec,read` membatasi alat; `--session isolated` memisahkan dari percakapan utama.
```bash
openclaw automations add --name "Notebook - ringkasan mingguan (agent)" --cron "0 7 * * 1" --tz Asia/Jakarta \
  --session isolated --tools exec,read \
  --message "Pakai skill notebook-riset-lokal: jalankan ringkasan untuk notebook 'Regulasi Pajak UMKM' (hanya baca; JANGAN menjalankan tambah-sumber/buat-notebook/podcast-mulai). Kirim jawabannya apa adanya ke saya, sertakan catatan periksa-ulang sumber." \
  --announce --channel telegram --to <chat-id-telegram-pemilik>
```

## Mengelola jadwal
| Tujuan | Perintah |
|---|---|
| Lihat daftar & id | `openclaw automations list` |
| Uji sekarang | `openclaw automations run <id>` |
| Lihat hasil | `openclaw automations runs <id>` (cek `status`, `summary`, `deliveryStatus`) |
| Hentikan / aktifkan | `openclaw automations disable <id>` / `enable <id>` |
| Hapus | `openclaw automations rm <id>` |

## Jika bermasalah
- `summary` berisi "tidak bisa dihubungi" → Docker/Open Notebook mati saat jadwal berjalan, atau `OPEN_NOTEBOOK_URL` di jadwal beda dengan yang dipakai saat chat biasa — samakan lewat `--command-env`.
- `summary` berisi "401" → kata sandi API salah/belum tersimpan di komputer Gateway; buat ulang atau `simpan-kunci` ulang.
- `summary` berisi "Belum ada model AI default" → atur model di Open Notebook (`docs/panduan-open-notebook.md` §5) sebelum jadwal berikutnya jalan.
- `deliveryStatus: not-delivered` → kanal Telegram belum siap (token bot/ID chat).
- Tanpa OpenClaw (Claude Code/Codex/Cursor): ketik "ringkas notebook X" saat dibutuhkan, atau pasang alarm HP sendiri.
