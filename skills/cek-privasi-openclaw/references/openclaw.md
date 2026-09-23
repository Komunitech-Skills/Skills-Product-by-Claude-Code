# Perintah & kunci konfigurasi OpenClaw yang dipakai skill ini

Semua yang tertulis di sini **diverifikasi langsung** di OpenClaw **2026.9.5** (mesin uji
terisolasi, `HOME` terpisah, tanpa login kanal apa pun): perintah lewat `--help`, dan nama
kunci konfigurasi (dot path) lewat `openclaw config schema` (skema JSON resmi paket). Kalau
versi OpenClaw pengguna berbeda dan sebuah perintah/kunci tidak ditemukan, katakan jujur bahwa
itu belum bisa dipastikan untuk versi tersebut — **jangan** menyebutnya sebagai perintah pasti.

## 1. Perintah audit bawaan (jalankan ini dulu)

```bash
openclaw security audit
```
Opsi yang terverifikasi lewat `openclaw security audit --help`:
- `--deep` — coba periksa Gateway yang sedang berjalan juga (lebih lengkap, butuh Gateway aktif).
- `--json` — keluaran JSON (lebih mudah diringkas oleh agent).
- `--fix` — **mengubah** sistem. Terverifikasi bahwa ini **bukan sekadar** merapikan izin file:
  di mesin uji, `--fix` juga mengubah nilai config secara langsung (contoh nyata:
  `channels.whatsapp.groupPolicy` dari `"open"` menjadi `"allowlist"` otomatis). Perlakukan
  `--fix` seperti gabungan beberapa perubahan config sekaligus — **jangan** jalankan tanpa
  menjelaskan dulu apa saja yang akan disentuh (dari hasil `security audit --json` sebelumnya)
  dan tanpa izin eksplisit pengguna.

Contoh bentuk keluaran (`--json`, hasil uji nyata di mesin verifikasi — nilai berbeda di
komputer pengguna): setiap `findings[]` punya `severity` (`critical`/`warn`/`info`), `title`,
`detail`, dan `checkId`; **`remediation` bersifat opsional** (tidak selalu ada, mis. pada
finding `summary.attack_surface`). Petakan `severity` ke lampu lalu lintas:
- `critical` → 🔴 Merah
- `warn` → 🟡 Kuning
- `info` → 🟢 Hijau (atau netral, tergantung isi `detail`)

Kalau `exec` tidak diizinkan / perintah tidak bisa dijalankan: beri perintah ini sebagai
salin-tempel untuk dijalankan pengguna sendiri di terminal, lalu tawarkan membaca hasilnya
bersama-sama (tempel keluarannya ke chat).

## 2. Membaca konfigurasi (HANYA BACA, jangan ubah dulu)

```bash
openclaw config get <path> --json
```
**Penting — kalau path belum diatur pengguna, perintah ini KELUAR DENGAN EXIT CODE 1** dan pesan
`"Config path is valid but unset: <path>. The runtime default applies until you set an authored
value..."` (terverifikasi langsung). Ini **BUKAN error yang menghentikan audit** — artinya nilai
bawaan (runtime default) yang berlaku. Untuk tahu nilai bawaan **efektif** yang sebenarnya
dipakai (bukan cuma dugaan dari skema), pakai `openclaw approvals get --json` (lihat §3) dan
`openclaw sandbox explain` (§4), bukan cuma `config get`.

Path yang relevan untuk audit privasi (terverifikasi ada di skema resmi `openclaw config schema`):

| Path config | Artinya (bahasa awam) | Nilai bawaan efektif (terverifikasi) |
|---|---|---|
| `tools.profile` | Profil kemampuan AI: `minimal`, `coding`, `messaging`, atau `full`. **`messaging` TIDAK punya `exec`/`read`/`write`/`edit` sama sekali** (hanya tool pesan & sesi) — lihat dampak di `references/dampak-perubahan.md`. `full` = semua tool termasuk perintah komputer. | Onboarding lokal umumnya memasang `full`. Selalu cek `config get tools.profile` untuk memastikan. |
| `tools.exec.mode` | Apakah perintah komputer (`exec`) boleh jalan: `deny` (tidak boleh), `allowlist` (hanya yang diizinkan), `ask` (**ditinjau manusia** — perlu klien approval terhubung), `auto` (**ditinjau AI reviewer/classifier dulu**, bukan "tanpa tinjauan"), `full` (jalan tanpa tinjauan sama sekali). | **Bawaan runtime = `full`, dengan `ask: "off"`** — terverifikasi lewat `openclaw approvals get --json` (`effectivePolicy` menunjukkan `mode: "full"`, `ask: "off"` bila belum diatur). Artinya perintah komputer **jalan tanpa persetujuan** kecuali diubah. |
| `tools.exec.security` | Sama kategorinya (`deny`/`allowlist`/`full`) tapi untuk tingkat keamanan perintah | Bawaan efektif `full` (sama sumber verifikasi seperti baris di atas). |
| `agents.defaults.sandbox.mode` | Apakah AI berjalan di "kotak pasir" terisolasi (container): `off`, `non-main`, `all`. `all` **butuh Docker/Podman terpasang** — lihat `references/dampak-perubahan.md`. | `off` bila tidak diatur (dikonfirmasi lewat `openclaw sandbox explain`). |
| `session.dmScope` | Bagaimana AI mengingat percakapan pribadi (DM): `main` (semua orang berbagi satu ingatan — **berisiko** bila banyak orang chat pribadi ke bot yang sama), `per-peer`/`per-channel-peer`/`per-account-channel-peer` (tiap pengirim terpisah) | `main` bila tidak diatur |
| `channels.whatsapp.dmPolicy` (ganti `whatsapp` dengan kanal lain, mis. `telegram`) | Siapa yang boleh chat pribadi ke bot: `pairing` (harus disetujui dulu), `allowlist` (hanya nomor tertentu), `open` (siapa saja), `disabled` | `pairing` |
| `channels.whatsapp.allowFrom` | Daftar nomor/akun yang diizinkan (kalau `dmPolicy` bukan `open`) | kosong |
| `channels.whatsapp.groupPolicy` | Siapa yang boleh memicu bot di grup: `open`, `allowlist`, `disabled` | `allowlist` |
| `messages.groupChat.historyLimit` | Berapa banyak pesan grup lama yang dibaca AI sebagai konteks | sesuai skema, bisa diatur |
| `commands.ownerAllowFrom` | Daftar "pemilik" yang boleh memakai perintah sensitif (jadwal, dsb.) | kosong |
| `security.installPolicy` | Aturan pemasangan skill/plugin baru (mis. dari ClawHub) | tergantung setup |
| `gateway.auth.mode` | Cara Control UI/app login ke Gateway: `none`, `token`, `password`, `trusted-proxy`. Mengubah ini **butuh restart Gateway** (OpenClaw menampilkan peringatan ini sendiri) | tergantung setup |

Semua path ini **ada** di skema konfigurasi resmi paket 2026.9.5. Nilai bawaan di tabel diambil
dari verifikasi langsung (bukan cuma dugaan dari skema) kecuali disebutkan lain; nilai
**aktual** di komputer pengguna tetap bisa berbeda — selalu cek dengan `config get`/`approvals
get`, jangan asumsikan.

## 3. Persetujuan perintah komputer (exec approvals) — cara membaca nilai EFEKTIF

```bash
openclaw approvals get --json
```
(`openclaw approvals` adalah alias `openclaw exec-approvals`, terverifikasi lewat
`openclaw approvals --help`.) Ini yang menunjukkan **nilai efektif sebenarnya** (`effectivePolicy`),
termasuk saat `config get` bilang "valid but unset". Contoh nyata dari mesin verifikasi (config
belum diatur sama sekali): `mode: "full"`, `security: "full"`, `ask: "off"` — persis bawaan yang
dijelaskan di tabel §2.

```bash
openclaw approvals pending --json
```
**Butuh Gateway yang sedang berjalan dan berkredensial** — akan gagal di mesin tanpa Gateway
aktif. Kalau gagal, jangan anggap ini error audit; jelaskan ke pengguna bahwa pemeriksaan ini
perlu Gateway hidup, dan lewati kalau tidak relevan untuk audit dasar.

## 4. Sandbox

```bash
openclaw sandbox explain
```
Terverifikasi lewat `openclaw sandbox --help`: menjelaskan kebijakan sandbox/tool efektif untuk
sesi/agent saat ini — tanpa mengubah apa pun.

## 5. Telemetri — dua hal yang berbeda, jangan dicampur

1. **Cek pembaruan harian** (versi, OS, arsitektur Node/CLI) — ini **selalu berjalan**, bukan
   bagian dari "statistik anonim" yang bisa dimatikan. Bukan isi pesan, tapi tetap keluar dari
   komputer pengguna sekali sehari.
2. **Statistik pemakaian anonim** (opt-in) — **mati secara bawaan**. Cek & atur dengan:
   ```bash
   openclaw telemetry show
   openclaw telemetry on   # hanya dengan izin pengguna
   openclaw telemetry off
   ```
Jelaskan kedua hal ini terpisah ke pengguna — jangan bilang "telemetri OpenClaw sepenuhnya mati"
kalau yang dimaksud cuma statistik opt-in; cek versi harian tetap ada.

## 6. Mengubah konfigurasi — SELALU satu per satu, SELALU dengan izin

```bash
openclaw config set <path> <nilai>
```
(terverifikasi lewat `openclaw config --help` / `openclaw config set --help`). Sebelum menjalankan:
1. Sebutkan **path**, nilai **sekarang**, nilai **baru yang diusulkan**, dan **efeknya** dalam
   bahasa awam.
2. Tanya "Lanjut ubah ini? (ya/tidak)". Tunggu jawaban eksplisit.
3. Setelah diubah, jalankan ulang `openclaw config get <path>` untuk konfirmasi perubahan
   tersimpan, dan catat **cara membatalkan** (nilai lama, atau `openclaw config unset <path>`
   bila path tidak wajib diisi — terverifikasi lewat `openclaw config --help`).

**Jangan pernah** mengubah lebih dari satu pengaturan dalam satu persetujuan. Kalau pengguna
bilang "ubah semua yang perlu", tetap sebutkan satu per satu dan minta konfirmasi tiap butir
(boleh dipercepat dengan "ya untuk semua" **hanya** setelah pengguna melihat daftar lengkap
perubahan yang diusulkan).

**Jaring pengaman bawaan** (boleh disebutkan ke pengguna sebagai penenang, bukan pengganti
langkah "cara membatalkan" di atas):
- Terverifikasi: setiap `openclaw config set`/`config unset` menyimpan salinan config sebelumnya
  sebagai `openclaw.json.bak`, `.bak.1`, `.bak.2`, dst. di folder state OpenClaw (bertambah tiap
  perubahan). ini cadangan tambahan di luar cara membatalkan resmi (nilai lama/`config unset`).
- `openclaw config set --dry-run` / `openclaw config unset --dry-run` (terverifikasi lewat
  `--help`): **melihat efek perubahan tanpa benar-benar menyimpannya**. Tawarkan ini dulu untuk
  pengguna yang ragu.
- `openclaw backup create` (terverifikasi lewat `openclaw backup --help`): membuat arsip cadangan
  config + kredensial + sesi + workspace. Untuk perubahan besar (mis. sebelum mengubah banyak
  pengaturan sekaligus), tawarkan menjalankan ini dulu.

## 7. Permintaan hapus data (hak subjek data / UU PDP)

```bash
openclaw memory forget --session <id-or-key> --dry-run
```
(terverifikasi lewat `openclaw memory forget --help`; pilih target dengan `--session`,
`--participant <actor-id>`, `--hook-source <sumber>`, dan/atau `--since <tanggal>` — bisa
digabung.) `--dry-run` **melaporkan semua yang AKAN dihapus tanpa benar-benar menulis
perubahan**. Dipakai kalau pengguna (atau pelanggan yang memintanya) ingin data percakapan
tertentu dihapus dari memori/sesi OpenClaw. Jalankan `--dry-run` dulu, tunjukkan laporannya,
baru minta persetujuan untuk menjalankan ulang tanpa `--dry-run`. Untuk lokasi transkrip mentah,
rujuk ke `~/.openclaw` (lihat §"Penyimpanan memori/log" di `SKILL.md`).

## 8. Aturan pemilik untuk jalur "Solusi Member VIP" (WAJIB diikuti)

Sesuai keputusan pemilik di `CLAUDE.md` §1 ("Keputusan pemilik untuk jalur 3"):
- Kalau audit menemukan `channels.whatsapp.dmPolicy: "open"` pada nomor WA yang sama dengan
  nomor utama usaha, tandai ini 🔴 dan sarankan: (a) pindah ke **nomor WA terpisah** khusus
  bot dengan persetujuan risiko tertulis dari pengguna, atau (b) pakai **Telegram** sebagai
  kanal utama (tanpa risiko blokir).
- Kalau pengguna menyebut agen CS di WA membalas otomatis ke pelanggan (bukan draf/Copilot),
  tandai ini 🔴/🟡 tergantung konteks dan ingatkan aturan pemilik: **agen CS WA harus mode
  Copilot** (AI menyiapkan draf, manusia yang mengirim), bukan auto-reply langsung.
- Jangan menyarankan pengetatan yang secara tidak sengaja mematikan automation laporan
  (`laporan-otomatis-terjadwal`, `buku-stok`) tanpa peringatan — lihat
  `references/dampak-perubahan.md`.

## 9. Yang TIDAK bisa diverifikasi di sesi ini

- Alur lengkap approval lewat reaksi 👍/👎 di WhatsApp — hanya disebut sebagai kemampuan umum
  (`approvals.exec` ada di skema config), bukan langkah pasti per platform.
- Efek `security audit --deep` yang butuh Gateway aktif — tidak dijalankan dalam mode verifikasi
  ini (tanpa Gateway).
- Nilai bawaan **sebenarnya** yang dipakai komputer pengguna — selalu bisa berbeda dari skema;
  jangan disamakan tanpa mengecek `config get`/`approvals get` langsung di mesin pengguna.
