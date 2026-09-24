# Perintah OpenClaw untuk automation pantau-pasar-kripto

Semua opsi di bawah **diverifikasi lewat `openclaw automations add --help`** di OpenClaw
**2026.9.5 (ec9c1a1)** (`source /tmp/oc/env.sh` lalu `node .../openclaw.mjs automations add
--help` dengan `HOME` sementara -- sama seperti metode `laporan-otomatis-terjadwal`).
**Berbeda dari `laporan-otomatis-terjadwal`:** kombinasi `--command` + `--trigger-script`
di bawah **belum berhasil dijalankan sungguhan terhadap Gateway uji** saat skill ini
ditulis (percobaan `gateway run --dev` di sandbox penulisan skill ini gagal start dalam
waktu terbatas) -- jadi tandanya **S** (didukung menurut `--help`, kombinasi persis belum
dibuktikan), bukan **T**. **Uji dulu dengan `openclaw automations run <id> --wait` sebelum
mengaktifkan jadwal**, dan kalau perilakunya beda dari dugaan di bawah, pakai Opsi B
(job agent biasa) yang polanya sama persis dengan `laporan-otomatis-terjadwal`
(skill itu **sudah** membuktikan pola ini jalan sungguhan di Gateway uji).

Nama subperintah resminya **`automations`** (alias `cron`, keduanya jalan sama).

## Opsi A -- hemat token: skrip yang memutuskan, agent hanya dipanggil saat perlu (status S)
Ide: `--command` menjalankan `cek_ambang.py` di Gateway secara berkala TANPA melibatkan
model AI sama sekali (murah, cepat). `--trigger-script` (skrip kondisi terpisah, field
`--help`: *"Condition script file, or - for stdin"*) diharapkan menentukan apakah job ini
"menyala" (dan karenanya mengumumkan/memanggil agent) pada giliran itu -- **konvensi
persis kode keluar yang dianggap "trigger" belum kami buktikan**, jadi tulis skrip
kondisi ini supaya **exit 0 = ambang terlewati** (mengikuti konvensi Unix umum untuk
"kondisi terpenuhi"), lalu **wajib diuji** dengan `automations run <id> --wait` -- kalau
ternyata job tetap jalan setiap kali (bukan hanya saat ambang terlewati), berarti
konvensinya terbalik atau berbeda; sesuaikan skrip kondisi atau pindah ke Opsi B.

Skrip kondisi contoh (simpan sebagai `kripto/trigger_ambang.sh` di workspace member,
**bukan** bagian dari paket skill karena path-nya spesifik per member):
```bash
#!/bin/sh
python3 "<folder-skill-ini-absolut>/scripts/cek_ambang.py" \
  --konfigurasi kripto/konfigurasi.json --state kripto/state.json --keluaran json > /tmp/hasil-cek-kripto.json
KODE=$?
# cek_ambang.py: exit 2 = ADA ambang terlewati -> exit 0 di sini supaya trigger "menyala"
[ "$KODE" -eq 2 ]
```
(Windows: sarankan menjalankan lewat WSL/Git Bash, atau pindah ke Opsi B yang tidak
butuh shell script terpisah.)

```bash
openclaw automations add --every 1h --trigger-script "<path-absolut>/kripto/trigger_ambang.sh" \
  --command "cat /tmp/hasil-cek-kripto.json" \
  --name "Cek ambang kripto" --tz "Asia/Jakarta" \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Opsi yang dipakai (semua ada di `--help`, tanda ✅ = sudah dicoba di skill sejenis
`laporan-otomatis-terjadwal` walau bukan kombinasi persis ini):
- `--every 1h` ✅ -- interval (alternatif: `--cron "0 * * * *"` untuk tiap jam tepat).
- `--trigger-script <path>` -- **status S**, lihat catatan di atas.
- `--command <shell>` -- job command (bukan job agent) yang isi keluarannya bisa
  `--announce` ke kanal. Kalau member ingin pesan yang lebih rapi (bukan JSON mentah),
  ganti `--command` dengan skrip lain yang memformat `pesan_singkat` dari hasil JSON
  (`cek_ambang.py` sudah menyediakan field itu -- tinggal `python3 -c "import json;
  print(json.load(open('/tmp/hasil-cek-kripto.json'))['pesan_singkat'])"`).
- `--tz "Asia/Jakarta"` ✅ -- wajib eksplisit.
- `--announce` ✅, `--channel telegram` ✅, `--to <chat-id>` ✅ -- sama seperti
  `laporan-otomatis-terjadwal` §4, lihat kanal di bawah.

## Opsi B -- job agent biasa, pola TERBUKTI (dipakai `laporan-otomatis-terjadwal`)
Kalau Opsi A tidak berperilaku seperti diharapkan setelah diuji, pakai pola ini (agent
dipanggil tiap giliran, sedikit lebih boros token, tapi **terbukti jalan** karena identik
dengan yang sudah dijalankan sungguhan di Gateway uji untuk skill lain):
```bash
openclaw automations add "0 * * * *" \
  "Jalankan 'python3 <folder-skill-ini-absolut>/scripts/cek_ambang.py --konfigurasi kripto/konfigurasi.json --state kripto/state.json'. Kalau field ambang_terlewati bernilai true, kirim isi field pesan_singkat apa adanya. Kalau false, JANGAN kirim apa pun (diam saja, jangan announce)." \
  --tz "Asia/Jakarta" --name "Cek ambang kripto (per jam)" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Ini "Bentuk A" (jadwal & pesan sebagai posisi, TANPA `--cron` -- lihat aturan
posisi-vs-`--name`/`--cron` di `laporan-otomatis-terjadwal/references/openclaw.md` §1,
berlaku sama di sini). Catatan: `--announce` tetap mengirim SESUATU tiap giliran kalau
agent menghasilkan teks akhir apa pun -- instruksi "jangan kirim apa pun kalau false" ada
di prompt, tapi **belum diuji** apakah agent benar-benar bisa membuat `--announce` tidak
mengirim apa-apa pada giliran itu (kemungkinan tetap mengirim teks kosong/konfirmasi
"tidak ada ambang terlewati"). Uji sekali dengan `automations run <id> --wait` dan
sampaikan hasil nyatanya ke member -- kalau ternyata tetap selalu mengirim pesan
(walau isinya "tidak ada perubahan"), itu bukan bug skill, cukup beri tahu member.

## Ringkasan pagi (harga + berita) -- job agent, SELALU mengumumkan
```bash
openclaw automations add "0 7 * * *" \
  "Jalankan 'python3 <folder-skill-ini-absolut>/scripts/cek_ambang.py --konfigurasi kripto/konfigurasi.json --state kripto/state.json' untuk data harga. Cari berita terbaru untuk kata kunci di kripto/PANTAU.md kalau ada akses pencarian web (sertakan tautan sumber tiap judul); kalau tidak ada akses, katakan jujur tidak bisa mencari berita. Susun ringkasan sesuai format Langkah B di SKILL.md skill pantau-pasar-kripto, sertakan disclaimer." \
  --tz "Asia/Jakarta" --name "Ringkasan pagi kripto" --session isolated \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Job ini **selalu** mengumumkan (bukan hanya saat ambang terlewati), jadi tidak butuh
`--trigger-script`.

## Menguji, melihat, menjeda, menghapus (sama seperti `laporan-otomatis-terjadwal`)
```bash
openclaw automations run <id> --wait      # uji sekali, tunjukkan hasilnya ke member
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

## Kanal pengiriman
Sama persis aturan `laporan-otomatis-terjadwal` §4: **Telegram = default** (API resmi,
tanpa risiko blokir). **WhatsApp hanya** dengan nomor terpisah dari nomor
pribadi/usaha utama + persetujuan risiko tertulis member (WhatsApp Web tidak resmi,
lihat `references/mesin-24-jam.md`-nya `laporan-otomatis-terjadwal` untuk teks lengkap
risiko). Tidak pernah ke grup atau ke pelanggan -- notifikasi ini murni untuk pemilik
sendiri.

## Syarat "komputer harus menyala"
Sama seperti semua automation OpenClaw: jadwal berjalan di dalam proses Gateway, kalau
komputer mati/tidur saat jam jadwal, cek/ringkasan itu **tidak terjadi** (bukan gagal
dengan pesan error). Jelaskan ini ke member sebelum jadwal dianggap aktif, tawarkan opsi
mesin selalu menyala (laptop/mini PC/VPS) atau jasa setup Komunitech -- sama seperti
`laporan-otomatis-terjadwal` Langkah 8.
