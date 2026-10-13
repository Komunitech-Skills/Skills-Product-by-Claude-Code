# Jalur 2 — Bot di dalam grup WA (live) via OpenClaw

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Baca ini hanya bila pengguna secara eksplisit ingin bot ikut ke dalam grup dan merespons
langsung di sana**, bukan sekadar meringkas file ekspor (itu Jalur 1 — jalur utama skill ini,
tanpa risiko, lihat `SKILL.md`). Jalur 2 **tidak** dijalankan otomatis oleh skill ini — skill
hanya menjelaskan langkah & konfigurasinya, dan pengguna/pemilik yang menjalankannya sendiri
di komputer mereka (atau lewat jasa pendampingan).

Semua perintah & kunci config di bawah **diverifikasi langsung** pada OpenClaw **2026.9.5
(ec9c1a1)** di mesin uji terisolasi (`config set ... --dry-run --strict-json` lalu
`config validate`, dan `--help` tiap perintah) atau dari dokumentasi resmi `docs.openclaw.ai`. Tidak ada kode yang benar-benar
dijalankan terhadap WhatsApp asli (tidak ada login/QR/gateway berjalan) — jadi tandai **B**
= belum diverifikasi ujung-ke-ujung dengan WhatsApp nyata.

## Prasyarat wajib (kebijakan Komunitech)
1. **Nomor WhatsApp TERPISAH** untuk bot, bukan nomor utama usaha/pribadi. Login hanya lewat
   scan QR: `openclaw channels login --channel whatsapp` (T, dari dokumentasi — belum diuji
   di sesi ini karena butuh WhatsApp asli).
2. **Tidak ada broadcast/blast.** Bot hanya boleh menjawab saat diminta di grup, dan hasilnya
   sebaiknya dikirim ke **DM pemilik**, bukan ke grup.
3. **Anggota grup wajib diberi tahu** bahwa ada bot AI yang bisa dipanggil di grup itu (etika
   & UU PDP No. 27/2022 — status regulasi **L**, cek dasar hukum sebelum dikutip pasti).
4. Grup sensitif (keluarga, pasien, HR) → **jangan** sarankan Jalur 2. Arahkan ke Jalur 1.

## Langkah konfigurasi (kunci config terverifikasi)

Semua perintah berikut dijalankan **oleh pemilik** di komputernya sendiri, satu per satu,
dengan `openclaw config validate` setelahnya. **Jangan** jalankan ini untuk pengguna tanpa
menjelaskan efeknya dulu — baca peta dampak di `skills/cek-privasi-openclaw/references/dampak-perubahan.md`
sebelum menawarkan, terutama baris "Dua kunci grup WA yang sering tertukar".

1. **Tambah akun WhatsApp kedua & login** (di luar cakupan verifikasi CLI murni; ikuti
   `docs.openclaw.ai/channels/whatsapp`):
   ```bash
   openclaw channels add --channel whatsapp
   openclaw channels login --channel whatsapp
   ```

2. **Batasi grup mana saja yang diproses** (opsional; kosongkan/`"*"` = semua grup yang sudah
   ada tetap diproses — **T**, terverifikasi lewat `config set ... --dry-run`):
   ```bash
   openclaw config set 'channels.whatsapp.groups' '{"<ID_GRUP>@g.us": {}}' --strict-json --dry-run
   openclaw config set 'channels.whatsapp.groups' '{"<ID_GRUP>@g.us": {}}' --strict-json
   ```
   Cari ID grup: `openclaw directory groups list --channel whatsapp --json` (**T**, perintah ada;
   perlu akun WA yang sudah login untuk hasil nyata — **B**).

3. **Batasi siapa yang boleh memicu bot di grup** — kunci **`groupAllowFrom`**, **wajib diisi
   eksplisit** dengan nomor E.164 pemilik (mis. `+6281200000001`, nomor fiktif contoh). Kalau
   dibiarkan kosong, pengecekan pengirim jatuh ke `allowFrom` (daftar DM) yang biasanya berisi
   `"*"` — itu membuat grup terbuka untuk siapa pun meski `groupPolicy` sudah `allowlist`
   (lihat peta dampak `cek-privasi-openclaw`). **T**, terverifikasi:
   ```bash
   openclaw config set channels.whatsapp.groupPolicy allowlist --dry-run
   openclaw config set channels.whatsapp.groupPolicy allowlist
   openclaw config set 'channels.whatsapp.groupAllowFrom' '["+6281200000001"]' --strict-json --dry-run
   openclaw config set 'channels.whatsapp.groupAllowFrom' '["+6281200000001"]' --strict-json
   ```
   (Isi nomor pemilik yang sebenarnya, ganti nomor contoh di atas.)

4. **Cabut kemampuan berbahaya dari grup** (grup dipakai banyak orang, bukan hanya pemilik) —
   deny `group:runtime` (exec) dan `group:fs` (baca/tulis file) khusus grup itu. **T**,
   terverifikasi lewat notasi bracket (ID grup berisi `.` sehingga notasi titik biasa gagal):
   ```bash
   openclaw config set 'channels.whatsapp.groups["<ID_GRUP>@g.us"].tools.deny' '["group:runtime","group:fs"]' --strict-json --dry-run
   openclaw config set 'channels.whatsapp.groups["<ID_GRUP>@g.us"].tools.deny' '["group:runtime","group:fs"]' --strict-json
   ```

5. **Validasi akhir:**
   ```bash
   openclaw config validate
   openclaw security audit --deep
   ```

## Cara memicu ringkasan di grup

- Pola pemicu: mention bot atau kata kunci, mis. `@bot ringkas` atau `#ringkas` (pola mention
  persis bergantung pengaturan `mentionPatterns` kanal — **S**, kunci ada di schema config,
  contoh isi belum diuji dengan WhatsApp nyata).
- OpenClaw menyuntikkan pesan grup yang **belum diproses sejak jawaban terakhir bot** sebagai
  konteks. **Default 50 pesan.** Bisa dinaikkan lewat `historyLimit` pada kanal/akun/grup.
  **Terverifikasi dari schema config (`config schema --json`, 2026.9.5): field `historyLimit`
  muncul di banyak level (kanal, akun, grup) dengan batas atas berbeda-beda** — sebagian
  bertipe integer tanpa batas atas praktis (`maximum: 9007199254740991`), sebagian lain
  (ditemukan di beberapa objek grup per-kanal, bukan objek `channels.whatsapp.groups.<id>`
  yang dipakai contoh di atas) dibatasi `maximum: 20`. **Batas efektif yang benar-benar
  dipakai untuk grup WhatsApp saat runtime BELUM DIPASTIKAN (B)** — schema hanya membatasi
  *nilai yang boleh ditulis*, bukan berapa yang benar-benar dipakai OpenClaw saat memproses
  grup WA. **Uji dengan grup WhatsApp asli sebelum menjanjikan angka tertentu ke pembeli.**
  Contoh menaikkan (di level akun kanal WhatsApp, tervalidasi skema):
  ```bash
  openclaw config set 'channels.whatsapp.historyLimit' 200 --strict-json --dry-run
  ```
- Ringkasan sebaiknya dikirim **ke DM pemilik** (`--announce --channel whatsapp --to <nomor
  pemilik>` bila lewat automation, atau cukup balasan biasa di sesi DM pemilik), bukan
  diposting balik ke grup, agar anggota grup lain tidak terganggu.
- **Ringkasan terjadwal otomatis tiap sore untuk grup WhatsApp: BELUM TERVERIFIKASI (B).**
  Heartbeat OpenClaw tidak berjalan di sesi grup, dan *ambient room events* (bot "mendengar"
  tanpa dipanggil) belum tersedia untuk WhatsApp per dokumentasi resmi — baru ada untuk
  Discord, Slack, dan grup Telegram. Untuk grup **Telegram**, jadwal otomatis lebih masuk akal
  (fitur ambient room events didukung) — tapi ini di luar cakupan skill ini yang berfokus pada
  ekspor WhatsApp; jangan janjikan jadwal otomatis untuk grup WA sebelum diuji langsung.
- Memicu bot yang memakai **nomor pribadi pemilik sendiri** (bukan nomor terpisah) di dalam
  grup: **belum terverifikasi (B)**. Tetap sarankan nomor terpisah sesuai keputusan pemilik.

## Ringkasan status verifikasi

| Klaim | Status |
|---|---|
| Kunci `channels.whatsapp.groupPolicy` + `groupAllowFrom` memvalidasi lewat CLI 2026.9.5 | **T** |
| Notasi bracket `groups["<id>@g.us"].tools.deny` diperlukan (notasi titik gagal karena ID berisi titik) | **T** |
| `groupAllowFrom` wajib diisi eksplisit agar tidak jatuh ke `allowFrom` (`"*"`) | **T** (dari peta dampak `cek-privasi-openclaw`, dikutip ulang) |
| `historyLimit` default grup = 50, bisa dinaikkan | **T** (dokumentasi) untuk defaultnya; batas efektif runtime WA = **B** |
| Ringkasan terjadwal otomatis untuk grup WhatsApp | **B** — tidak didukung heartbeat/ambient room events per dokumentasi; jangan dijanjikan |
| Mention pattern (`@bot ringkas`) memicu bot di grup nyata | **S** — mekanismenya ada, pola persis belum diuji dengan WhatsApp asli |
| Bot dengan nomor pribadi pemilik bisa dipicu di grup miliknya sendiri | **B** |

## Setelah konfigurasi

Sarankan pengguna menjalankan `cek-privasi-openclaw` untuk audit menyeluruh setelah mengubah
config di atas, dan **selalu** minta konfirmasi eksplisit sebelum menjalankan `config set`
apa pun (bukan `--dry-run`) di komputer pengguna sungguhan — ini mengubah cara bot merespons
untuk semua anggota grup, bukan cuma pemilik.
