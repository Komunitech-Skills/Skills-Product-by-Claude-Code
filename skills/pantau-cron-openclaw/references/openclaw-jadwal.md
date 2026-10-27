# Perintah OpenClaw untuk Pantau Cron (siap salin)

> **Bahasa ke pengguna:** ikuti BAHASA KE PENGGUNA di SKILL.md (tanpa "skill", "script", "cron job", "kredensial", "token", "agen", path).
> **Kredensial & aksi (wajib):** jangan membaca token/kunci dari environment, `openclaw.json`, `.env`, database atau log OpenClaw. Cek kanal hanya dengan `openclaw channels status --channel telegram`. Jangan membuat/mengubah jadwal atau mengirim pesan uji sebelum pengguna membalas "ya" atas ringkasan rencana.
> **Berkas yang boleh dibaca:** hanya berkas skill ini dan data pantauan sendiri (lewat perintah script). DILARANG membuka folder catatan harian/memori (`memory/`, `MEMORY.md`) atau riwayat sesi.
> **Aturan berhenti:** bila SATU perintah `openclaw automations ...`/`cron ...` gagal karena izin (ditolak, token/kredensial, Gateway tidak bisa dihubungi; galat lain lihat bagian 1b), berhenti memakai alat `openclaw`. DILARANG: membaca/mengubah `openclaw.json`, memeriksa/menulis token, menjalankan `openclaw doctor` (termasuk `--fix`), merestart Gateway, atau meminta alat lain mengubah konfigurasi Gateway. Lanjut ke bagian 0 (rencana siap salin).

## 0. Rencana siap salin saat terblokir
Tampilkan seluruh bagian ini dengan nilai terisi (jadwal job, nama; folder ditulis `[isian: folder pantauan Anda]`), tutup "Lanjut? (ya/tidak)":
1. Daftar job (nama, jadwal dalam kata-kata, toleransi, jadwal berikutnya dari keluaran `daftar`); di kanal chat satu baris per job, bukan tabel Markdown.
2. Per job, perintah edit prompt (bagian 2) dengan `<id-job>` diisi dari `openclaw automations list --all` bila ada, bila tidak `[isian: id job]`.
3. Dua perintah pengawas (bagian 3), tujuan `[isian: ID chat Telegram Anda]`.
4. Satu kalimat awam: belum ada izin ke pengatur jadwal OpenClaw; salin perintah ke terminal sendiri atau minta pemilik/penyedia OpenClaw memberi izin.

Pola dan status verifikasi (meniru `laporan-otomatis-terjadwal/references/openclaw.md` dan `bot-trading-kripto/references/openclaw-jadwal.md`):
- Semua flag di bawah (`--cron`, `--tz`, `--name`, `--session`, `--command-argv`, `--announce`, `--channel`, `--to`, `--message`, `--exact`, `edit`, `list --all`, `runs`, `disable`) **dicek lewat `--help` OpenClaw 2026.9.8 dan 2026.10.2** (statusnya "dicek --help"). `automations rm <id>` mengikuti referensi skill lain di library ini dan belum dicek `--help` khusus untuk skill ini; bila gagal, jalankan `openclaw automations --help`.
- Pola *job perintah tanpa model AI* + keluaran persis `NO_REPLY` tidak dikirim ke chat: **terbukti** untuk skill `bot-trading-kripto` di Gateway uji 2026.9.5. Kombinasi utuh untuk skill ini (pengiriman Telegram sungguhan) **belum diuji** -- sebutkan jujur ke pengguna: "uji dulu dengan `automations run <id> --wait`".
- Versi OpenClaw pengguna bisa berbeda: bila flag gagal, jalankan `openclaw automations add --help` dan sesuaikan.
- Fallback: bila perintah komputer tidak diizinkan (atau platform bukan OpenClaw), tampilkan perintah sebagai teks untuk dijalankan pengguna sendiri di terminal, atau lewat Control UI (`Settings -> Automations`).

`[isian: folder pantauan Anda]` = alamat lengkap folder panduan pantauan ini di komputer pengguna. Di teks untuk pengguna tetap tulis isian itu (jangan menyebut alamat nyata); isi alamat sebenarnya hanya saat memasang setelah "ya". Windows: ganti `python3` dengan `python`, dan tulis alamat dengan garis miring biasa `/`.

## 1. Daftarkan job ke pantauan (lokal, boleh langsung)
```bash
python3 scripts/pantau_cron.py tambah laporan-harian --jadwal "0 21 * * *" --zona WIB --toleransi 30
python3 scripts/pantau_cron.py tambah piutang-pagi  --jadwal "45 7 * * 1-5" --zona WIB
python3 scripts/pantau_cron.py daftar
```
`--ganti` tidak pernah menghapus riwayat lapor selesai. Hanya toleransi berubah (jadwal & zona sama) -> hitungan lama dipertahankan (pakai ini bila pesan jadwal di OpenClaw sudah memuat "Aturan penutup" terbaru; jangan bilang hitungan dimulai ulang). Jadwal atau zona berubah -> script otomatis memulai hitungan dari sekarang. Job yang sempat dilepas (`hapus --terima-lapor`) lalu didaftarkan lagi -> hitungan selalu dimulai dari sekarang, dengan atau tanpa `--ganti`. Tambah `--mulai-ulang` hanya bila pesan jadwal belum memuat teks terbaru (hitungan lama menyesatkan).
Zona: `WIB`, `WITA`, `WIT`, `UTC` (atau `Asia/Jakarta`, `Asia/Makassar`, `Asia/Jayapura`). Jadwal pantauan **harus sama** dengan jadwal `--cron` dan `--tz` job aslinya (lihat `openclaw automations list --all`). Toleransi 30 menit sudah menutupi penundaan acak (stagger) bawaan OpenClaw; job yang butuh tepat waktu bisa ditambah `--exact` saat dibuat.

## 1b. Baca daftar jadwal & kenali pengawas yang sudah ada
`openclaw automations list --all` (satu kali, hanya baca) sebelum merencanakan apa pun.
- **Daftar tidak terbaca utuh** (galat, terpotong, keluaran rusak, kolom yang perlu tidak ada): kalimat ke pemilik selalu persis "Daftar jadwal OpenClaw Anda tidak terbaca utuh, jadi saya tidak mengubah apa pun." Jangan menebak isinya, jangan mengubah/menambah/menghapus jadwal, dan jangan mendaftarkan apa pun ke pantauan lokal (juga tidak saat galat bukan soal izin); lanjut ke bagian 0 (rencana saja).
- **Galat bukan soal izin** (waktu habis, sambungan putus, hasil tidak jelas) pada perintah apa pun: jangan diulang; baca ulang daftar satu kali (SKILL.md 5c) DULU, sebelum mendaftarkan lokal (5a), lalu kerjakan hanya yang terlihat di daftar. Galat izin -> Aturan berhenti.
- **Pengawas yang sudah ada**: job bernama "Pengawas jadwal (tiap jam)" / "Ringkasan pantauan jadwal (harian)", atau yang `--command-argv`-nya memuat `pantau_cron.py` dan `cek`. Kelompokkan per tujuan kabar (`--to`): satu set = tiap jam + harian dengan tujuan sama. Label ke pemilik: "obrolan ini", "topik lain", "topik lain lagi" (label berbeda untuk tujuan berbeda). Pilihan: (i) ada set ke obrolan ini DAN set lain (dobel) -> bawaan "ya" = rapikan: set di obrolan ini dipakai (tidak memasang apa pun, tanpa uji peringatan), sesudah set itu terlihat utuh `openclaw automations rm <id>` untuk set ke tujuan lain, baca ulang lagi; balas "biarkan" = tidak ada yang dihapus. (ii) hanya set ke tujuan lain -> bawaan "ya" = pindahkan ke obrolan ini (pasang set baru, baca ulang, baru `rm` set lama, baca ulang lagi); balas "lama" = pakai yang lama (tidak memasang apa pun, tanpa uji peringatan). (iii) set tidak utuh (hanya tiap jam atau hanya harian per tujuan, mis. tiap jam di obrolan ini dan harian ke topik lain) -> bawaan "ya" = lengkapi: pasang hanya bagian yang kurang di obrolan ini, baca ulang, sesudah set di sini utuh `rm` bagian ke tujuan lain, baca ulang lagi; balas "biarkan" = tidak ada yang diubah. Hasil akhir yang benar: satu set. Pantauan lokal (riwayat, hitungan, ingatan alarm) tidak berubah karena pengawas diganti.
- **Jadwal yang sudah memuat "Aturan penutup" terbaru** (bagian 2): jangan diedit lagi, dan pantauannya jangan dimulai ulang.

## 2. Ping di akhir job
**Job berupa pesan ke agent** -- ubah prompt (butuh "ya"; tampilkan prompt lama dan baru). Balasan akhir sebuah jadwal adalah pesan yang dikirim ke tujuannya, jadi teks yang ditambahkan WAJIB membuat balasan akhir tetap berisi laporan utuh dan lapor selesai berjalan diam-diam (tanpa tanda kutip di dalam teks, agar aman di `--message "..."`):
```bash
openclaw automations list --all          # catat id job
openclaw automations edit <id-job> --message "<prompt lama utuh> Aturan penutup (wajib): selama mengerjakan langkah di atas, jangan menulis laporan sebagai teks dulu. Hanya bila semua langkah di atas berhasil, jalankan diam-diam (sebagai pemanggilan alat saja, tanpa teks apa pun di sekitarnya) perintah  python3 [isian: folder pantauan Anda]/scripts/pantau_cron.py ping laporan-harian  . Sesudah itu tulis laporan LENGKAP, dari baris pertama sampai terakhir, sebagai balasan akhir: balasan akhir itulah pesan yang dikirim ke tujuan, jadi harus berisi seluruh laporan dan menjadi pesan terakhir. Jangan menambah kalimat lain di balasan akhir: jangan menyebut perintah tadi, lapor selesai, ping, pesan di atas, sudah final, atau langkah ini. Bila ada langkah yang gagal, lewati perintah itu dan tulis balasan akhir seperti biasa."
```
Bila prompt lama sudah memuat kalimat versi sebelumnya ("Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah ..."), GANTI kalimat itu dengan teks di atas (jangan ditumpuk). Teks lama itu membuat agen jadwal menutup dengan kalimat proses sehingga isi laporan tidak terkirim (uji bot Telegram 16 Okt 2026).
Job harus boleh menjalankan perintah (tool `exec`). Bila job dibuat dengan `--tools`, pastikan `exec` ada di daftarnya. Lapor selesai dicatat tepat sebelum laporan ditulis sebagai balasan akhir, jadi ia tidak membuktikan pesan sampai ke tujuan; periksa isi yang terkirim lewat `openclaw automations runs <id-job>` bila ringkasannya terlihat.

**Job berupa perintah** (`--command-argv`): JANGAN mengubah berkas script pemilik dan jangan menulis ulang argv dengan tangan. Salin argv lama UTUH (daftar JSON persis dari `list --all`) dan biarkan script menyusun argv baru dengan kutip yang benar:
```bash
python3 scripts/pantau_cron.py bungkus laporan-harian --argv-lama '["python3", "/rumah/laporan.py", "--judul", "Laporan harian"]' --id <id-job>
# keluaran: openclaw automations edit <id-job> --command-argv '["<python>", "<folder>/scripts/pantau_cron.py", "jalankan", "laporan-harian", "--", "python3", "/rumah/laporan.py", "--judul", "Laporan harian"]'
```
Argv baru menjalankan argv lama apa adanya (tanpa shell; keluaran dan kode keluar diteruskan, jadi yang dikirim ke chat tetap keluaran job) lalu mencatat lapor selesai diam-diam hanya bila kode keluar 0. Saat sukses `jalankan` diam total (tidak ada teks pantauan di keluaran maupun di stderr), karena belum dipastikan apakah OpenClaw ikut mengirim stderr job perintah ke chat; hanya bila pantauan galat ada satu baris peringatan di stderr. Job yang dimatikan sinyal diteruskan dengan kode 128 + nomor sinyal. Argv lama memuat tanda kutip tunggal -> kirim lewat input: `--argv-lama -`. Bungkus tidak pernah dobel; perintah yang sudah memuat lapor selesai sendiri ditolak. Kutip keluaran `--id` untuk shell POSIX (Linux/macOS); Windows: pakai keluaran tanpa `--id` (daftar JSON) di Control UI `Settings -> Automations`.

## 3. Job pengawas (tanpa model AI, tanpa biaya token)
`<ID chat Telegram pemilik>` di bawah = tujuan kabar. Bila pengguna belum menyebutnya, jangan bertanya ulang sesudah "ya": pakai tujuan sementara = obrolan/topik tempat pengguna meminta (tirukan penulisan tujuan jadwal yang sudah ada di `openclaw automations list --all`), sebut jelas bahwa itu sementara dan boleh dipindah nanti (pasang ulang kedua pengawas dengan tujuan baru, atau ubah lewat Control UI `Settings -> Automations`).
Tiap jam, hanya bicara bila ada masalah:
```bash
openclaw automations add --cron "5 * * * *" --tz "Asia/Jakarta" \
  --name "Pengawas jadwal (tiap jam)" --session isolated \
  --command-argv '["python3", "[isian: folder pantauan Anda]/scripts/pantau_cron.py", "cek", "--openclaw"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Keluaran `NO_REPLY` (tenang) tidak dikirim. Bila ada masalah, pesan berawalan `PANTAU CRON` dikirim; masalah yang sama tidak diulang dalam 6 jam (`--ulang-jam` bisa diubah di argv), dan satu pesan PULIH dikirim saat job kembali melapor.

Ringkasan harian sekali (semua job + ping terakhir):
```bash
openclaw automations add --cron "0 8 * * *" --tz "Asia/Jakarta" \
  --name "Ringkasan pantauan jadwal (harian)" --session isolated \
  --command-argv '["python3", "[isian: folder pantauan Anda]/scripts/pantau_cron.py", "cek", "--tanpa-catat"]' \
  --announce --channel telegram --to "<ID chat Telegram pemilik>"
```
Folder data lain dari bawaan: tambahkan `"--folder", "<alamat>"` di argv semua perintah (atau atur `PANTAU_CRON_DIR`).

## 4. Uji sebelum dianggap aktif
1. `python3 scripts/pantau_cron.py cek` -> semua job OK atau "menunggu jadwal pertama".
2. `openclaw automations run <id-pengawas> --wait`, lalu `openclaw automations runs <id-pengawas>` -> berhasil, tidak ada pesan saat tenang.
3. Alarm palsu terkendali (setelah "ya"): `tambah uji-alarm --jam <HH.MM tiga menit dari sekarang> --toleransi 1`, tunggu ±5 menit (jadwal harus lewat SESUDAH job didaftarkan), jalankan pengawas sekali -> pesan HILANG masuk Telegram; lalu `hapus uji-alarm --hapus-riwayat` (juga bila uji dibatalkan; pengawas akan mengirim PULIH atau diam).
4. Jalankan satu job asli (`automations run <id-job> --wait`) -> `riwayat <nama>` menampilkan ping baru. Laporan akan masuk ke tujuan job itu satu kali; baca isinya (atau `automations runs <id-job>`) dan pastikan itu laporan utuh, bukan hanya kalimat penutup seperti "pesan di atas sudah final". Bila hanya kalimat penutup, teks lapor selesai di prompt belum sesuai: ganti dengan teks bagian 2.
5. **Verifikasi akhir (wajib sebelum menyatakan terpasang):** `openclaw automations list --all` dibaca SESUDAH pasang dan dibandingkan dengan daftar sebelum pasang: dua pengawas baru muncul (nama, jadwal, tujuan) dan job yang diubah menunjukkan perubahan nyata. Tidak ada perubahan nyata -> jangan tulis "sudah dipasang"; tulis "BELUM TERPASANG" + sebabnya.

## 5. Opsi lanjutan: Healthchecks milik sendiri (tanpa wajib, tidak berafiliasi)
Kelemahan pengawas lokal: bila komputer/gateway mati total, pengawas ikut diam. Layanan Healthchecks (open-source; bisa dipasang sendiri atau memakai versi hosted milik pengguna) memantau dari luar: ia yang mengabari bila ping berhenti datang. Komunitech tidak berafiliasi dengan proyek atau layanannya; kebijakan harga dan batas layanan hosted mengikuti penyedianya.

Langkah untuk pengguna (asisten hanya memandu, tidak menyentuh alamatnya):
1. Buat akun/instalasi Healthchecks sendiri, buat satu *check* per job, atur jadwal (cron + zona) dan masa tenggang sama dengan toleransi. Atur notifikasinya di sana (mis. Telegram atau email).
2. Salin alamat ping tiap check. **Jangan tempel di chat.** Alamat itu rahasia siapa pun yang punya bisa mengirim ping palsu.
3. Buka berkas `healthchecks.json` di folder data pantauan dengan editor teks, isi:
   ```json
   {"laporan-harian": "<alamat ping check laporan-harian>",
    "piutang-pagi": "<alamat ping check piutang-pagi>"}
   ```
4. Selesai: setiap `ping` kini juga memanggil layanan itu (gagal jaringan tidak menggagalkan job; `--tanpa-luar` melewatinya). Ping lokal tetap dicatat, jadi `cek` lokal tetap berjalan.
Data yang keluar komputer hanya "ping" kosong ke alamat itu; isi laporan tidak pernah dikirim.

## 6. Kelola
```bash
python3 scripts/pantau_cron.py daftar            # semua job + ping terakhir
python3 scripts/pantau_cron.py riwayat laporan-harian
python3 scripts/pantau_cron.py hapus piutang-pagi        # berhenti memantau
openclaw automations disable <id-pengawas>       # jeda (WAJIB id, bukan nama)
openclaw automations rm <id-pengawas>            # hapus pengawas (sesudah "ya"; baca ulang daftar sebelum bilang terhapus)
python3 scripts/pantau_cron.py bungkus --buang --argv-lama '<argv job sekarang>' --id <id-job>   # kembalikan argv lama persis
openclaw automations enable <id-pengawas>
```
Mengubah jadwal job asli? Jalankan `tambah <nama> --jadwal "..." --ganti` agar pantauan ikut berubah (riwayat lapor selesai tetap; hitungan dimulai dari sekarang karena jadwalnya berubah). Libur panjang/mesin sengaja dimatikan: jeda pengawas atau `hapus` jobnya dulu supaya tidak ada peringatan palsu.

Berhenti memantau: hanya yang dipasang pantauan ini yang dibuang ("Aturan penutup" di pesan jadwal, bungkus argv, pengawas, pantauan lokal). Berkas script/perintah buatan pemilik TIDAK PERNAH diubah; bila lapor selesai ada di perintah buatan pemilik, pakai `hapus <nama> --terima-lapor` (bukan `hapus` biasa), agar lapor selesai itu tetap diterima tanpa galat (kode keluar 0), diam (tanpa keluaran), tidak dicatat, dan tidak dikabarkan. Diawasi lagi nanti -> `tambah` (hitungan mulai dari sekarang). Sesudah mengerjakan, baca ulang `list --all` sebelum menulis "sudah dihapus". Pemilik menjawab "tidak" -> tidak ada yang diubah.

## 7. Mesin 24 jam
Jadwal OpenClaw hanya jalan saat komputer/gateway menyala. Panduan opsi mesin 24 jam (laptop/mini PC/VPS milik sendiri) ada di skill `laporan-otomatis-terjadwal`; Komunitech menawarkan **jasa setup berbayar**.
