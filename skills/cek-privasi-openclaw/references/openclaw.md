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
- `--fix` — **mengubah** sistem (menerapkan perbaikan aman + memperbaiki izin file). **Jangan**
  jalankan `--fix` tanpa izin eksplisit pengguna untuk setiap perbaikan, sesuai alur skill ini.

Contoh bentuk keluaran (`--json`, hasil uji nyata di mesin verifikasi — nilai berbeda di
komputer pengguna): setiap `findings[]` punya `severity` (`critical`/`warn`/`info`), `title`,
`detail`, dan `remediation`. Petakan `severity` ke lampu lalu lintas:
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
Path yang relevan untuk audit privasi (terverifikasi ada di skema resmi `openclaw config schema`):

| Path config | Artinya (bahasa awam) | Nilai bawaan (default skema) |
|---|---|---|
| `tools.profile` | Profil kemampuan AI: `minimal`, `coding`, `messaging`, atau `full`. `full` berarti AI bisa menjalankan perintah komputer & membaca/menulis file secara luas. | tergantung setup; onboarding lokal umumnya memasang `full` |
| `tools.exec.mode` | Apakah perintah komputer (`exec`) boleh jalan: `deny` (tidak boleh), `allowlist` (hanya yang diizinkan), `ask` (tanya dulu), `auto`/`full` (jalan tanpa tanya) | tergantung setup |
| `tools.exec.security` | Sama kategorinya (`deny`/`allowlist`/`full`) tapi untuk tingkat keamanan perintah | tergantung setup |
| `agents.defaults.sandbox.mode` | Apakah AI berjalan di "kotak pasir" terisolasi: `off`, `non-main`, `all` | `off` bila tidak diatur |
| `session.dmScope` | Bagaimana AI mengingat percakapan pribadi (DM): `main` (semua orang berbagi satu ingatan — **berisiko** bila banyak orang chat pribadi ke bot yang sama), `per-peer`/`per-channel-peer`/`per-account-channel-peer` (tiap pengirim terpisah) | `main` bila tidak diatur |
| `channels.whatsapp.dmPolicy` (ganti `whatsapp` dengan kanal lain, mis. `telegram`) | Siapa yang boleh chat pribadi ke bot: `pairing` (harus disetujui dulu), `allowlist` (hanya nomor tertentu), `open` (siapa saja), `disabled` | `pairing` |
| `channels.whatsapp.allowFrom` | Daftar nomor/akun yang diizinkan (kalau `dmPolicy` bukan `open`) | kosong |
| `channels.whatsapp.groupPolicy` | Siapa yang boleh memicu bot di grup: `open`, `allowlist`, `disabled` | `allowlist` |
| `messages.groupChat.historyLimit` | Berapa banyak pesan grup lama yang dibaca AI sebagai konteks | sesuai skema, bisa diatur |
| `commands.ownerAllowFrom` | Daftar "pemilik" yang boleh memakai perintah sensitif (jadwal, dsb.) | kosong |
| `security.installPolicy` | Aturan pemasangan skill/plugin baru (mis. dari ClawHub) | tergantung setup |

Semua path ini **ada** di skema konfigurasi resmi paket 2026.9.5. Nilai bawaan di tabel diambil
dari deskripsi skema; nilai **aktual** di komputer pengguna bisa berbeda — selalu cek dengan
`config get`, jangan asumsikan.

## 3. Persetujuan perintah komputer (exec approvals)

```bash
openclaw approvals get --json
openclaw approvals pending --json
```
(`openclaw approvals` adalah alias `openclaw exec-approvals`, terverifikasi lewat
`openclaw approvals --help`.) Dipakai untuk memeriksa apakah ada permintaan persetujuan yang
menumpuk, dan bagaimana kebijakan approval saat ini diatur.

## 4. Sandbox

```bash
openclaw sandbox explain
```
Terverifikasi lewat `openclaw sandbox --help`: menjelaskan kebijakan sandbox/tool efektif untuk
sesi/agent saat ini — tanpa mengubah apa pun.

## 5. Telemetri

```bash
openclaw telemetry show
```
Menampilkan pratinjau data pembaruan harian yang dikirim (versi, OS, arsitektur — bukan isi
pesan). Statistik anonim **mati secara bawaan**; nyalakan/matikan dengan `openclaw telemetry on`
atau `openclaw telemetry off` — **hanya dengan izin pengguna**.

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

## 7. Yang TIDAK bisa diverifikasi di sesi ini

- Alur lengkap approval lewat reaksi 👍/👎 di WhatsApp — hanya disebut sebagai kemampuan umum
  (`approvals.exec` ada di skema config), bukan langkah pasti per platform.
- Efek `security audit --deep` yang butuh Gateway aktif — tidak dijalankan dalam mode verifikasi
  ini (tanpa Gateway).
- Nilai bawaan **sebenarnya** yang dipakai komputer pengguna — selalu bisa berbeda dari skema;
  jangan disamakan tanpa mengecek `config get` langsung di mesin pengguna.
