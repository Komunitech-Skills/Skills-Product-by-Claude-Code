# Skenario 3 (input kurang): kabari kalau laporan otomatis saya mati

**Input (pesan pengguna, versi 1.0.2):** "Kabari kalau laporan otomatis saya mati"

**Output SESUDAH (skill aktif):**

> Sudah saya cek — percobaan mengakses pengatur jadwal OpenClaw Anda gagal (belum ada izin), jadi saya langsung siapkan rencana siap pasang pakai dua contoh jadwal umum. Ganti nama/jamnya sesuai jadwal Anda sendiri.
>
> **1. Jadwal yang akan dipantau (contoh)**
>
> | Nama | Jadwal | Toleransi | Jadwal berikutnya |
> |---|---|---|---|
> | laporan-harian | tiap hari 21.00 WIB | 30 menit | 12 Okt 21.00 WIB |
> | piutang-pagi | Senin–Jumat 07.45 WIB | 30 menit | 13 Okt 07.45 WIB |
>
> **2. Tambahan "lapor selesai" di akhir tiap jadwal**
> Kalimat yang ditambahkan di akhir pesan jadwalnya:
> > "Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah `python3 [isian: folder pantauan Anda]/scripts/pantau_cron.py ping laporan-harian`. Jangan dijalankan bila ada langkah yang gagal."
>
> Perintah untuk menerapkannya (perlu id jadwal dari daftar Anda):
> ```bash
> openclaw automations edit <id-jadwal> --message "<isi pesan lama> Langkah terakhir, ... ping laporan-harian ..."
> ```
>
> **3. Dua pengawas yang akan dipasang (tanpa biaya token AI)**
> ```bash
> # Pengawas tiap jam — hanya bicara kalau ada masalah
> openclaw automations add --cron "5 * * * *" --tz "Asia/Jakarta" \
>   --name "Pengawas jadwal (tiap jam)" --session isolated \
>   --command-argv '["python3", "[isian: folder pantauan Anda]/scripts/pantau_cron.py", "cek", "--openclaw"]' \
>   --announce --channel telegram --to "[isian: ID chat Telegram Anda]"
>
> # Ringkasan harian jam 08.00
> openclaw automations add --cron "0 8 * * *" --tz "Asia/Jakarta" \
>   --name "Ringkasan pantauan jadwal (harian)" --session isolated \
>   --command-argv '["python3", "[isian: folder pantauan Anda]/scripts/pantau_cron.py", "cek", "--tanpa-catat"]' \
>   --announce --channel telegram --to "[isian: ID chat Telegram Anda]"
> ```
> `[isian: folder pantauan Anda]` = alamat folder tempat panduan pantauan ini terpasang di komputer Anda.
>
> Pemasangan otomatis belum bisa dilakukan dari sini karena belum ada izin ke pengatur jadwal OpenClaw Anda. Cukup salin perintah di atas ke terminal Anda sendiri, atau minta pemilik/penyedia OpenClaw Anda memberi izin.
>
> Catatan jujur: pemasangan penuh di pengatur jadwal OpenClaw (sampai kabar benar-benar masuk ke Telegram) belum teruji otomatis; setelah terpasang, kita jalankan satu uji peringatan dulu.
>
> Lanjut? (ya/tidak)
>
> 1. Jadwal otomatis apa saja yang ingin dipantau, dan jam berapa? (ganti contoh di atas)
> 2. Kabar dikirim ke Telegram pribadi Anda, bukan grup?
> 3. Toleransi terlambat 30 menit cukup?

**Catatan:** kerjakan dulu dengan contoh umum (berlabel contoh, tidak didaftarkan), 1 panggilan `automations` gagal lalu berhenti, tiga pertanyaan baku di akhir. Kata bocor: "token AI". Tanpa skill: 2 dari 3 percobaan timeout; jawaban percobaan ke-3 hanya "tidak ada automation" + pertanyaan di muka. Nilai: sebelum 3 / sesudah 8,25.
