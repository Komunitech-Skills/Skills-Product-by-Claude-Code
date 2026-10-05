# Perintah OpenClaw untuk automation pantau-pasar-kripto (v1.0.2; catatan v1.0.10)

> **v1.0.10:** draf siap tempel dibuat oleh `scripts/draf_jadwal.py` (cukup itu; file ini hanya
> dibaca untuk uji §3 atau bila script tidak bisa dijalankan). Folder kerja default draf =
> `$HOME/.openclaw/workspace` (Windows `%USERPROFILE%\.openclaw\workspace`). **Jangan** mengisi
> `--workspace`/`--command-cwd` dengan path tebakan atau path lingkungan agent; `<folder-workspace-member>`
> di bawah = folder yang disebut pengguna, atau default tadi.

> **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.

**Koreksi v1.0.2 (S2-3, lihat `examples/HASIL-UJI.md` "Uji ulang v1.0.1"):** pola utama
diganti dari `--command` (string) ke `--command-argv` (array argv). Alasan: `--command`
dijalankan Gateway lewat `sh -lc <shell>` (login shell) -- di Gateway uji, profil login
mesin (`nvm`) mencetak teks SEBELUM wrapper sempat jalan, sehingga keluaran menjadi
`"nvm\nNO_REPLY"` alih-alih `"NO_REPLY"` murni, dan penekanan pengiriman gagal (Gateway
tetap mencoba mengirim). `--command-argv` tidak lewat shell sama sekali (argv langsung ke
proses `python3`), jadi kebal dari kontaminasi profil login apa pun -- **terbukti** bersih
di Gateway uji Linux. Paragraf di bawah yang sebelumnya menandai `--command-argv` "belum
dicoba" (khusus Windows) sudah diperbaiki: kombinasi lengkapnya (dengan `--command-cwd`,
`--cron`+`--tz`, `--announce`) **terbukti T di Linux**; Windows tetap **S** (logikanya
seharusnya sama karena tanpa shell, tapi belum diuji di mesin Windows sungguhan).

Semua perintah di bawah **diuji sungguhan** (bukan hanya `--help`) terhadap Gateway lokal
OpenClaw **2026.9.5 (ec9c1a1)** (`gateway run --dev --allow-unconfigured --bind loopback
--token ...`, `automations add`/`automations run --wait`, HOME sementara, tanpa model AI &
tanpa kanal login). Status **T** = terbukti jalan di Gateway uji. Status **S** = ada di
`--help`/dokumentasi tapi kombinasi persisnya belum terbukti.

**Koreksi dari draf v1.0.0 (ditemukan uji independen, lihat `examples/HASIL-UJI.md`):**
opsi awal (`--every` + `--tz` + `--trigger-script <file>.sh`) **GAGAL** dua kali di CLI
asli:
- `--tz` **tidak boleh** dipasangkan dengan `--every` -- pesan CLI: *"--tz is only valid
  with --cron or offset-less --at"*. Untuk jadwal berulang yang perlu zona waktu, pakai
  `--cron`, bukan `--every`.
- `--trigger-script` **bukan** shell script yang dibaca kode keluarnya. Menurut dokumentasi
  bawaan OpenClaw (`docs/automation/cron-jobs/schedules.md` §Event triggers) dan dikonfirmasi
  langsung oleh Gateway uji, trigger script adalah **kode JavaScript** (mode `exec`/`json`)
  yang memanggil `await exec({ command: '...' })` lalu memanggil `json({ fire, message?,
  state? })` -- bukan file `.sh` yang exit code-nya dibaca CLI. File `.sh` ditolak dengan
  pesan *"cron trigger script has a syntax error: Unexpected character '!' ..."* (dibaca
  sebagai JS, gagal parse shebang `#!`).
- `openclaw automations run <id> --wait` **mengabaikan/memaksa lewati** trigger (menjalankan
  job langsung) -- jadi TIDAK bisa dipakai untuk menguji apakah trigger akan menyala di
  jadwal sungguhan. Cara uji yang benar ada di §3 di bawah.

Nama subperintah resminya **`automations`** (alias `cron`, keduanya jalan sama).

## 1. Pola UTAMA (T, TERBUKTI di Gateway uji Linux): `--command-argv` + wrapper Python `NO_REPLY`

Paling sederhana, paling murah (job command tidak memanggil model AI sama sekali kecuali
ada yang perlu dilaporkan), dan **tidak lewat shell sama sekali** (lihat S2-3 di atas):

```bash
openclaw automations add --cron "0 * * * *" --tz "Asia/Jakarta" \
  --name "Cek ambang kripto (per jam)" --session isolated \
  --command-argv '["python3", "<folder-skill-ini-absolut>/scripts/cek_dan_lapor.py", "--konfigurasi", "kripto/konfigurasi.json", "--state", "kripto/state.json"]' \
  --command-cwd "<folder-workspace-member>" \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
(Windows: ganti `"python3"` jadi `"python"` di elemen pertama array kalau `python3` tidak
ada di PATH member -- lihat catatan status di bawah.)

**Kenapa `--command-argv`, bukan `--command`:** `--command <shell>` dijalankan Gateway
lewat `sh -lc <shell>` (login shell) -- yang berarti file profil login (`.bashrc`,
`.profile`, skrip `nvm`, dll.) ikut dieksekusi/dicetak SEBELUM `python3` sempat jalan. Di
Gateway uji, ini membuat keluaran job menjadi `"nvm\nNO_REPLY"` alih-alih `"NO_REPLY"`
murni, sehingga deteksi "tidak ada balasan" oleh OpenClaw gagal dan Gateway tetap mencoba
mengirim pesan tiap jam walau kondisinya tenang. `--command-argv` menjalankan `python3`
langsung sebagai proses (array argv, tanpa shell perantara), jadi kebal dari kontaminasi
profil login apa pun -- **terbukti bersih** di Gateway uji Linux (lihat
`examples/HASIL-UJI.md` "Uji ulang v1.0.1", S2-3).

**Windows (S, BELUM diuji di mesin Windows sungguhan):** secara desain `--command-argv`
seharusnya bekerja sama di Windows (tidak bergantung `sh`), tapi kombinasi ini belum
dicoba di Gateway Windows sungguhan pada sesi uji manapun -- hanya **T di Linux**. Kalau
member memakai Windows, jelaskan statusnya jujur, uji dulu dengan `automations run <id>
--wait` (§3) sebelum mengaktifkan jadwal produksi, dan siapkan fallback perintah
salin-tempel manual kalau gagal.

**Alternatif `--command` (string shell) -- HANYA kalau versi OpenClaw member tidak
mendukung `--command-argv`:** bentuk `--command "cd '<folder-workspace-member>' && python3
'<folder-skill-ini-absolut>/scripts/cek_dan_lapor.py' --konfigurasi kripto/konfigurasi.json
--state kripto/state.json"` juga **T** (terbukti jalan), TAPI berisiko kena masalah profil
login di atas -- kalau terpaksa memakainya, jalankan uji manual dulu (§3, langkah 1) dan
periksa SENDIRI bahwa keluaran kondisi tenang persis `NO_REPLY` (tanpa baris lain di
depannya) sebelum mengaktifkan ke jadwal produksi.

**Cara kerja:** `cek_dan_lapor.py` (lihat isinya, sudah diuji offline di
`tests/uji_regresi.py`) menjalankan `cek_ambang.py`. Kalau exit code-nya **2** (ambang
harga baru terlewati) atau **3** (pemantauan bermasalah yang perlu dilaporkan -- gagal
total, cache basi, ambang % tak bisa dicek, atau baru pulih, lihat S2-2), wrapper mencetak
`pesan_singkat` yang sudah jadi (siap diumumkan lewat `--announce`). Kalau tidak, wrapper
mencetak literal `NO_REPLY` -- OpenClaw **tidak memposting apa pun** ke kanal kalau
keluaran job persis `NO_REPLY` (dikonfirmasi lewat `automations run --wait`, lihat §3).
Wrapper **SELALU** keluar dengan kode 0, supaya Gateway tidak salah mencatat giliran normal
(ambang terlewati/pemantauan bermasalah) sebagai job yang *error*.

Opsi yang dipakai (T = dicoba sungguhan di Gateway uji Linux untuk skill ini):
- `--cron "0 * * * *"` (T) -- setiap jam tepat. `--tz "Asia/Jakarta"` (T) boleh dipasangkan
  dengan `--cron` (berbeda dari `--every`, lihat catatan koreksi di atas).
- `--command-argv` (T di Linux, S di Windows) -- payload command sebagai array argv (bukan
  string shell), supaya tidak melewati `sh -lc` sama sekali.
- `--command-cwd` (T) -- direktori kerja saat wrapper dijalankan, supaya path relatif
  `kripto/konfigurasi.json`/`kripto/state.json` merujuk ke workspace member yang benar.
- `--session isolated`, `--announce`, `--channel telegram`, `--to <chat-id>` -- sama seperti
  pola `laporan-otomatis-terjadwal` (T di skill itu, dipakai ulang di sini).

## 2. Varian trigger JavaScript (T -- diverifikasi ULANG sendiri, bukan cuma mengutip penguji)

Kalau ingin job **tidak berjalan sama sekali** saat tenang (bukan berjalan lalu mencetak
`NO_REPLY`), OpenClaw mendukung trigger dalam kode JavaScript. Bentuk berikut **terbukti
menyala (`fire: true`) hanya saat ambang terlewati, dan tidak menyala saat data tenang** --
awalnya ditemukan penguji independen (`/tmp/uji-kripto-oc/trig2.js` & `trig3.js`), dan
**diverifikasi ULANG secara independen** di sesi revisi ini (Gateway `--dev` sendiri, port
terpisah, `--every 30s` selama >60 detik): job dengan data tenang tercatat **0 run**
(`automations runs <id>` -> `"total": 0`), job dengan data ambang terlewati tercatat
**1 run** dengan `"triggerFired": true`. Catatan dari verifikasi ulang: `completionStatus`
run itu tercatat `"failed"` BUKAN karena trigger/command-nya gagal (command tetap
`"exitCode": 0` & `triggerFired: true`), melainkan karena kanal pengiriman belum
dikonfigurasi di lingkungan uji (`deliveryError: "Channel is required..."`) -- di lingkungan
member yang kanalnya sudah aktif, ini semestinya tidak muncul; tetap perhatikan
`deliveryStatus`/`deliveryError` di `automations runs` saat menguji bersama member, jangan
cuma `triggerFired`.

```js
const res = await exec({
  command: 'cd "<folder-workspace-member>" && python3 "<folder-skill-ini-absolut>/scripts/cek_ambang.py" --konfigurasi kripto/konfigurasi.json --state kripto/state.json --keluaran teks; echo KODE=$?'
});
const out = String(res?.aggregated ?? res?.stdout ?? JSON.stringify(res));
json({ fire: out.includes('KODE=2') || out.includes('KODE=3'), message: out.slice(0, 1500), state: { n: (trigger.state?.n ?? 0) + 1 } });
```
Simpan sebagai file `.js` lokal lalu:
```bash
openclaw automations add --every 30s --trigger-script "<path-ke-file>.js" \
  --command "echo dipicu" --name "Cek ambang kripto (trigger JS)" \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Catatan status: pola trigger JS ITU SENDIRI (`exec` + `json({fire,...})`) **T** -- terbukti
`fire: true` pada data ambang terlewati dan `fire: false` pada data tenang di Gateway uji.
Tapi kombinasi lengkap dengan `--cron`/`--tz` (bukan `--every` detik seperti contoh uji) dan
dengan pengiriman `--announce` yang sesungguhnya **belum diuji ujung-ke-ujung** untuk skill
ini -- tandai **S** untuk kombinasi itu, uji dulu dengan cara di §3 sebelum diandalkan penuh.
Kalau ragu, pakai Pola 1 (`--command-argv` + wrapper) yang sudah terbukti penuh.

## 3. Cara UJI YANG BENAR (koreksi dari v1.0.0)

`automations run <id> --wait` **memaksa job jalan, mengabaikan trigger** -- jangan
memakainya untuk menyimpulkan "trigger bekerja". Untuk memverifikasi perilaku trigger/
wrapper sebelum mengaktifkan jadwal ke member:
1. **Uji wrapper/`cek_dan_lapor.py` di luar OpenClaw dulu**, langsung dari terminal, dengan
   data tenang lalu data ambang terlewati (`--harga-file` untuk simulasi, lihat
   `SKILL.md`/`tests/uji_regresi.py`) -- pastikan keluarannya `NO_REPLY` vs pesan yang
   benar, sebelum menyambungkannya ke automation.
2. Untuk Pola 1 (`--command-argv`): `automations run <id> --wait` **valid** dipakai di
   sini, karena job-nya sendiri (bukan trigger) yang ingin diuji -- job SELALU jalan (tidak
   ada trigger terpisah), yang membedakan tenang/terpicu adalah isi keluaran wrapper
   (`NO_REPLY` vs pesan). Jalankan sekali dengan kondisi data tenang (harus keluaran job
   PERSIS `NO_REPLY` -- periksa `completionStatus: succeeded` DAN tidak ada upaya
   pengiriman/`deliveryError` di `automations runs <id>`, bukan cuma isi `summary`, lihat
   S2-3) dan sekali dengan kondisi ambang terlewati (harus ada pesan terkirim), baru anggap
   terbukti.
3. Untuk Pola 2 (trigger JS): **JANGAN** pakai `run --wait` untuk menguji apakah trigger
   menyala. Biarkan jadwalnya berjalan dengan interval pendek sementara (mis. `--every
   30s`) di lingkungan uji, amati `automations runs <id>` -- hitung berapa kali job benar-
   benar dieksekusi ("run") dibanding berapa kali trigger dievaluasi. Baru setelah terbukti
   perilakunya sesuai, ganti ke jadwal produksi (`--cron` + `--tz Asia/Jakarta`) dan hapus
   job uji sementara.

## 4. Ringkasan pagi (harga + berita) -- job agent, SELALU mengumumkan

Beda dari cek ambang: ringkasan pagi memang harus mengumumkan SETIAP kali (bukan hanya saat
ada kejadian), jadi cukup job agent biasa (S -- sintaksnya konsisten dengan pola
`laporan-otomatis-terjadwal` yang **T**, tapi kombinasi persis untuk isi prompt ini belum
diuji ulang di sesi uji independen skill ini, karena butuh model AI sungguhan):
```bash
openclaw automations add "0 7 * * *" \
  "Jalankan 'python3 <folder-skill-ini-absolut>/scripts/cek_ambang.py --konfigurasi kripto/konfigurasi.json --state kripto/state.json' untuk data harga. Cari berita terbaru untuk kata kunci di kripto/PANTAU.md kalau ada akses pencarian web (sertakan tautan sumber tiap judul); kalau tidak ada akses, katakan jujur tidak bisa mencari berita. Susun ringkasan sesuai format Langkah B di SKILL.md skill pantau-pasar-kripto, sertakan disclaimer." \
  --tz "Asia/Jakarta" --name "Ringkasan pagi kripto" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Ini "Bentuk A" (jadwal & pesan sebagai posisi, TANPA `--cron`) -- lihat aturan posisi-vs-
`--name`/`--cron` di `laporan-otomatis-terjadwal/references/openclaw.md` §1, berlaku sama
di sini: jangan campur argumen posisi dengan `--cron`/`--at`/`--every` sekaligus.

## 5. Menguji, melihat, menjeda, menghapus (T -- sama seperti `laporan-otomatis-terjadwal`)
```bash
openclaw automations run <id> --wait      # jalankan job sekali (utk Pola 1 di atas, ini uji sah)
openclaw automations runs <id>            # riwayat run -- utk mengecek Pola 2 (trigger JS)
openclaw automations list --all           # lihat semua jadwal
openclaw automations show <id>            # detail satu jadwal (boleh nama persis)
openclaw automations disable <id>         # jeda -- WAJIB id (bukan nama)
openclaw automations enable <id>          # aktifkan lagi -- WAJIB id
openclaw automations edit <id> --to "..." # ubah -- WAJIB id
openclaw automations rm <id>              # hapus permanen -- WAJIB id
```
`run`/`disable`/`enable`/`edit`/`rm` menerima **hanya id (UUID)**, terbukti di skill
`laporan-otomatis-terjadwal` (memakai nama menjawab "Automation not found"). Ambil `id`
dari field `"id"` hasil `automations add`.

## 6. Kanal pengiriman
Sama persis aturan `laporan-otomatis-terjadwal` §4: **Telegram = default** (API resmi,
tanpa risiko blokir). **WhatsApp hanya** dengan nomor terpisah dari nomor
pribadi/usaha utama + persetujuan risiko tertulis member (WhatsApp Web tidak resmi,
lihat `references/mesin-24-jam.md`-nya `laporan-otomatis-terjadwal` untuk teks lengkap
risiko). Tidak pernah ke grup atau ke pelanggan -- notifikasi ini murni untuk pemilik
sendiri. Catatan dari uji: kalau kanal belum dikonfigurasi (`--channel`/`--to` kosong atau
kanal belum ditambahkan lewat `openclaw channels add`), Gateway menampilkan
`deliveryPreview` yang memperingatkan pengiriman akan gagal-tertutup ("fail-closed") --
selalu isi `--channel`/`--to` eksplisit dan pastikan kanalnya sudah aktif SEBELUM
mengaktifkan jadwal ke member.

## 7. Syarat "komputer harus menyala"
Sama seperti semua automation OpenClaw: jadwal berjalan di dalam proses Gateway, kalau
komputer mati/tidur saat jam jadwal, cek/ringkasan itu **tidak terjadi** (bukan gagal
dengan pesan error). Jelaskan ini ke member sebelum jadwal dianggap aktif, tawarkan opsi
mesin selalu menyala (laptop/mini PC/VPS) atau jasa setup Komunitech -- sama seperti
`laporan-otomatis-terjadwal` Langkah 8.
