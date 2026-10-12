# Skenario 1 (normal utama): pantau laporan harian dan piutang

**Input (pesan pengguna, versi 1.0.2):** "Tolong pantau laporan harian jam 21.00 dan tagih piutang 07.45 Senin-Jumat di OpenClaw saya, kabari lewat Telegram kalau ada yang gagal jalan."

**Output SESUDAH (skill aktif, run biasa):**

> Sudah saya daftarkan dua jadwal ke pantauan (bisa langsung dikerjakan): **laporan-harian** (tiap hari 21.00 WIB) dan **piutang-pagi** (Senin-Jumat 07.45 WIB), toleransi keterlambatan 30 menit untuk keduanya.
>
> Pemasangan penuh (sampai kabar benar-benar masuk ke Telegram) belum bisa saya lakukan dari sini karena belum ada izin ke pengatur jadwal OpenClaw Anda. Berikut rencana lengkap, siap salin ke terminal Anda sendiri, atau minta pemilik/penyedia OpenClaw Anda yang menjalankannya:
>
> **1. Ringkasan jadwal yang dipantau**
>
> | Nama | Jadwal | Toleransi | Jadwal berikutnya |
> |---|---|---|---|
> | laporan-harian | tiap hari 21.00 WIB | 30 menit | 12 Okt 21.00 WIB |
> | piutang-pagi | Senin-Jumat 07.45 WIB | 30 menit | 13 Okt 07.45 WIB |
>
> **2. Tambahan di akhir tiap jadwal, supaya pantauan tahu sudah selesai**
>
> Untuk **laporan-harian**, tambahkan kalimat ini di akhir isi pesannya:
> > "Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah python3 [isian: folder pantauan Anda]/scripts/pantau_cron.py ping laporan-harian . Jangan dijalankan bila ada langkah yang gagal."
>
> ```bash
> openclaw automations list --all          # catat id jadwal "laporan-harian"
> openclaw automations edit [isian: id jadwal laporan-harian] --message "<isi pesan lama laporan-harian, lengkap> Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah python3 [isian: folder pantauan Anda]/scripts/pantau_cron.py ping laporan-harian . Jangan dijalankan bila ada langkah yang gagal."
> ```
>
> Untuk **piutang-pagi**, sama polanya:
> ```bash
> openclaw automations edit [isian: id jadwal piutang-pagi] --message "<isi pesan lama piutang-pagi, lengkap> Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah python3 [isian: folder pantauan Anda]/scripts/pantau_cron.py ping piutang-pagi . Jangan dijalankan bila ada langkah yang gagal."
> ```
> (Catatan: jadwal ini perlu izin menjalankan perintah agar langkah "lapor selesai" di atas bisa jalan.)
>
> **3. Dua pengawas (tanpa biaya token tambahan)**
>
> Pengawas tiap jam (hanya bicara kalau ada masalah):
> ```bash
> openclaw automations add --cron "5 * * * *" --tz "Asia/Jakarta" \
>   --name "Pengawas jadwal (tiap jam)" --session isolated \
>   --command-argv '["python3", "[isian: folder pantauan Anda]/scripts/pantau_cron.py", "cek", "--openclaw"]' \
>   --announce --channel telegram --to "[isian: ID chat Telegram Anda]"
> ```
>
> Ringkasan harian sekali, jam 08.00 WIB:
> ```bash
> openclaw automations add --cron "0 8 * * *" --tz "Asia/Jakarta" \
>   --name "Ringkasan pantauan jadwal (harian)" --session isolated \
>   --command-argv '["python3", "[isian: folder pantauan Anda]/scripts/pantau_cron.py", "cek", "--tanpa-catat"]' \
>   --announce --channel telegram --to "[isian: ID chat Telegram Anda]"
> ```
>
> **4.** Pemasangan otomatis belum bisa dilakukan dari sini karena belum ada izin ke pengatur jadwal OpenClaw Anda. Cukup salin perintah di atas ke terminal Anda sendiri, atau minta pemilik/penyedia OpenClaw Anda memberi izin.
>
> ---
> Catatan jujur: pemasangan penuh di pengatur jadwal OpenClaw (sampai kabar benar-benar masuk ke Telegram) belum teruji otomatis; setelah terpasang, kita jalankan satu uji peringatan dulu.
>
> Lanjut? (ya/tidak)
>
> Dua hal yang masih perlu saya ketahui:
> (a) Kabar dikirim ke Telegram pribadi Anda, bukan grup?
> (b) Toleransi terlambat 30 menit untuk kedua jadwal itu sudah cukup, atau mau diubah?

**Catatan:** konteks Telegram (`uji-tg.sh`) hasilnya serupa (rencana lengkap, 3 pertanyaan; ada kata "token"/"kata sandi" bocor dan pertanyaan 1 yang mengulang info); lihat `00-openclaw-sebelum-sesudah.md`. Jadwal berikutnya (12 Okt 21.00 WIB; 13 Okt 07.45 WIB) benar. Satu panggilan `automations` yang gagal lalu berhenti (run Telegram); config/token tidak disentuh. Tanpa skill: 2 dari 3 percobaan timeout tanpa jawaban. Nilai: sebelum 3 / sesudah 7,75.
