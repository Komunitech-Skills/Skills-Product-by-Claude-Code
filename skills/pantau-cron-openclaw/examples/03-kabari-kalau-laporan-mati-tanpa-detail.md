# Skenario 3 (input kurang)

**Input (pesan pengguna, versi 1.0.1):** "Kabari kalau laporan otomatis saya mati"

**Output SESUDAH (skill aktif):**

> Saya sudah coba cek jadwal otomatis Anda sekali, tapi pengatur jadwal OpenClaw Anda belum bisa saya akses dari sini (butuh izin yang belum terpasang). Saya tidak akan mengulang percobaan itu — malah lebih bagus, saya sudah siapkan rencana lengkap siap pakai di bawah, pakai **contoh umum** dulu (silakan ganti sesuai laporan Anda yang sebenarnya):
>
> **1. Job yang dipantau (contoh — ganti sesuai laporan Anda)**
>
> | Nama | Jadwal | Toleransi | Jadwal berikutnya |
> |---|---|---|---|
> | laporan-harian | tiap hari 21.00 WIB | 30 menit | Hari ini, 21.00 WIB |
> | piutang-pagi | Senin–Jumat 07.45 WIB | 30 menit | Besok (Selasa), 07.45 WIB |
>
> **2. Tambahan "lapor selesai" di akhir tiap job**
>
> Kalimat yang ditambahkan di akhir prompt job (hanya dijalankan kalau job itu sudah sukses):
>
> > Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah `python3 /opt/ochome/.openclaw/skills/pantau-cron-openclaw/scripts/pantau_cron.py ping laporan-harian`. Jangan dijalankan bila ada langkah yang gagal.
>
> Perintah untuk menerapkannya (butuh id job dari `automations list --all`, dan butuh persetujuan Anda dulu):
>
> ```bash
> openclaw automations list --all          # catat id job laporan-harian & piutang-pagi
> openclaw automations edit <id-laporan-harian> --message "<prompt lama utuh> Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah python3 /opt/ochome/.openclaw/skills/pantau-cron-openclaw/scripts/pantau_cron.py ping laporan-harian . Jangan dijalankan bila ada langkah yang gagal."
> openclaw automations edit <id-piutang-pagi> --message "<prompt lama utuh> Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah python3 /opt/ochome/.openclaw/skills/pantau-cron-openclaw/scripts/pantau_cron.py ping piutang-pagi . Jangan dijalankan bila ada langkah yang gagal."
> ```
>
> **3. Dua pengawas (tanpa biaya token tambahan)**
>
> Pengawas tiap jam — hanya bicara kalau ada masalah:
>
> ```bash
> openclaw automations add --cron "5 * * * *" --tz "Asia/Jakarta" \
>   --name "Pengawas jadwal (tiap jam)" --session isolated \
>   --command-argv '["python3", "/opt/ochome/.openclaw/skills/pantau-cron-openclaw/scripts/pantau_cron.py", "cek", "--openclaw"]' \
>   --announce --channel telegram --to "[isian: ID chat Telegram Anda]"
> ```
>
> Ringkasan harian sekali, jam 08.00 WIB:
>
> ```bash
> openclaw automations add --cron "0 8 * * *" --tz "Asia/Jakarta" \
>   --name "Ringkasan pantauan jadwal (harian)" --session isolated \
>   --command-argv '["python3", "/opt/ochome/.openclaw/skills/pantau-cron-openclaw/scripts/pantau_cron.py", "cek", "--tanpa-catat"]' \
>   --announce --channel telegram --to "[isian: ID chat Telegram Anda]"
> ```
>
> **4.** Pemasangan otomatis belum bisa dilakukan dari sini karena agen belum punya izin ke pengatur jadwal OpenClaw Anda. Cukup salin perintah di atas ke terminal Anda sendiri, atau minta pemilik/penyedia OpenClaw Anda memberi izin.
>
> Lanjut? (ya/tidak)
>
> Sambil Anda cek itu, tiga hal kecil biar rencananya pas:
> 1. Laporan otomatis apa saja yang mau dipantau, dan jam berapa (ganti contoh di atas)?
> 2. Kabarnya dikirim ke chat Telegram pribadi Anda ya, bukan grup — benar?
> 3. Toleransi 30 menit cukup, atau ada laporan yang harus tepat waktu?

**Catatan penguji:** SEBELUM 3 / SESUDAH 8. SEBELUM: mencoba menjangkau pengatur jadwal, lalu MENGUBAH konfigurasi sistem sendiri (`gateway.mode=local`, `gateway.auth.mode=token`, membuat token) tanpa izin dan menyuruh restart; tidak ada rencana atau pekerjaan; hanya 2 pertanyaan di akhir; jargon (Gateway, auth, automations). Percobaan pertama SEBELUM timeout (agent berputar mencoba terhubung ke Gateway berulang kali). SESUDAH: tidak membuka dengan pertanyaan; satu percobaan lalu berhenti, memakai contoh umum (laporan-harian 21.00, piutang-pagi Senin-Jumat 07.45) dan menyebutnya contoh, tabel jadwal berikutnya benar, perintah salin, 'Lanjut? (ya/tidak)', 3 pertanyaan di akhir. Tidak menyentuh konfigurasi, tidak ada 'dead man's switch'. Kekurangan: 'Saya sudah coba cek... butuh izin yang belum terpasang', 'agen belum punya izin', 'tanpa biaya token'.

Perbandingan lengkap: `00-openclaw-sebelum-sesudah.md`.
