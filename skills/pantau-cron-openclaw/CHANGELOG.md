# Riwayat perubahan — pantau-cron-openclaw

Catatan teknis per versi.

## Catatan revisi 1.0.5 (2026-10-17)
- Revisi dari uji ulang di bot Telegram asli (16 Okt 2026, v1.0.4, skor 8 LOLOS, dengan empat cacat):
  1. **Isi laporan hilang saat jalan-sekali.** Kalimat lama "Langkah terakhir, hanya bila semua langkah di atas berhasil dan pesan sudah terkirim: jalankan perintah ..." membuat agen jadwal menulis laporan, menjalankan lapor selesai, lalu menutup dengan kalimat proses ("Pesan di atas sudah final dan ping monitor cron berhasil dicatat."); balasan akhir agen jadwal adalah pesan yang dikirim ke grup, sehingga hanya kalimat itu yang terkirim (Tagih Piutang), dan Laporan Harian diawali kalimat proses. Diganti "Aturan penutup (wajib)" (SKILL.md Langkah 2 dan references/openclaw-jadwal.md bagian 2): laporan tidak ditulis sebagai teks dulu; bila semua langkah berhasil, lapor selesai dijalankan diam-diam sebagai pemanggilan alat; lalu laporan LENGKAP ditulis sebagai balasan akhir dan menjadi pesan terakhir; balasan akhir tidak boleh menyebut perintah, lapor selesai, ping, "pesan di atas", "sudah final". Teks tanpa tanda kutip agar aman di `--message "..."`. Prompt yang sudah memuat teks lama wajib DIGANTI, tidak ditumpuk.
  2. **Rencana tidak menyebut uji jalan-sekali.** Langkah 4 kini punya format rencana wajib dengan baris "Setelah Anda balas ya, tiap jadwal saya jalankan sekali untuk uji (laporan akan masuk ke grup)".
  3. **Pantauan lama tidak ditawarkan untuk dihapus.** Tawaran satu baris (bukan hapus otomatis; "ya" atas rencana bukan jawabannya) wajib ada di rencana dan di hasil pemasangan (5g).
  4. **Bot membuka folder catatan harian (memory).** Larangan eksplisit di Aturan kerja, UNTUK AGENT SAJA, dan references: hanya baca berkas skill dan data pantauan sendiri.
- Tambahan: Langkah 5e kini meminta memeriksa (bila terlihat) bahwa isi yang terkirim saat jalan-sekali adalah laporan utuh, bukan hanya status "ok"; Batasan menyebut jujur bahwa lapor selesai dicatat sebelum balasan akhir ditulis, jadi tidak membuktikan pesan sampai. Contoh ringkas tidak lagi menyebut tabel di kanal chat.
- Script tidak berubah (logika dan teks keluaran sama); belum ada konstanta versi di script. Ditambah uji konsistensi teks (tests/uji_regresi.py: teks "Aturan penutup" sama di SKILL.md dan references, tanpa tanda kutip, tanpa teks lama; baris rencana wajib ada).
- Belum diuji ulang di bot Telegram.

## Catatan revisi 1.0.4 (2026-10-16)
- Revisi dari uji alur pasang di bot OpenClaw asli (16 Okt 2026, skor 5): setelah pengguna menjawab "ya", bot hanya mengubah pesan dua jadwal lalu berhenti dan bertanya ulang tujuan kabar, sehingga pengawas tidak terpasang. Kini satu "ya" berlaku untuk seluruh rencana: tujuan kabar yang belum disebut memakai obrolan/topik tempat pengguna meminta (sementara, boleh dipindah), dua pengawas dipasang, uji peringatan dan jalan-sekali dijalankan, lalu hasilnya DIVERIFIKASI dengan membaca ulang daftar jadwal OpenClaw. Dilarang menulis "sudah dipasang/selesai" bila daftar sesudah pasang tidak menunjukkan pengawas baru atau perubahan nyata (tulis "BELUM TERPASANG" + sebabnya).
- Daftar pantauan: hanya job yang diminta pengguna. Job yang sudah terdaftar sejak lama disebut "sudah ada di pantauan sejak <tanggal>" (bukan "baru didaftarkan") dan dihitung ulang dengan `--ganti`; job lama yang tidak diminta ditawarkan untuk dihapus. Angka "terlewat" selalu disebut bersama rentangnya dan dibedakan dari "gagal berturut-turut" di daftar jadwal OpenClaw.
- Jawaban "job mana yang terlambat hari ini" dibuka dengan keluaran `cek` apa adanya (susunan PANTAU CRON), maksimal tiga kalimat tambahan, dan jujur bila jadwal belum pernah dijalankan sekali. Bahasa: kata "proses" dilarang; di kanal chat tanpa tabel Markdown.
- Script (hanya teks keluaran, logika deteksi tidak berubah): `daftar` menampilkan "terdaftar sejak <tanggal>"; baris job yang belum punya jadwal jatuh tempo kini berbunyi "terdaftar sejak <tanggal>, jadwal pertama <waktu> belum tiba" (sebelumnya "baru didaftarkan", keliru untuk job lama). Ditambah 2 uji regresi (32 uji lulus).

## Catatan revisi 1.0.3 (2026-10-13)
- Pembersihan kata teknis di jawaban untuk pengguna awam: nama perintah/CLI ikut dilarang muncul, kata "Gateway" diganti "OpenClaw", dan setelah memasang, jadwal dan cara menjeda ditampilkan dalam kalimat biasa ("minta saya menjeda jadwal ini"); perintah teknis hanya bila pengguna memintanya. Logika dan script tidak berubah.

## Catatan revisi 1.0.2 (2026-10-12)
- Revisi dari uji OpenClaw asli (skor 4,63 naik ke 8,19): deskripsi diganti dengan kata pemicu yang lebih mudah dikenali ("jadwal otomatis gagal", "laporan otomatis mati", "kabari kalau laporan saya gagal").
- Ditambah bagian "PENOLAKAN": permintaan memantau komputer, akun, atau aktivitas karyawan/pasangan/orang lain diam-diam ditolak dengan kalimat pertama baku, lalu langsung dilanjutkan dengan rencana contoh untuk jadwal milik sendiri.
- Ditambah "BAHASA KE PENGGUNA" (daftar kata yang dilarang muncul, mis. cron, ping, token, Gateway; diganti "jadwal otomatis" dan "lapor selesai") dan "PENUTUP BAKU" (satu kalimat jujur bahwa pemasangan penuh belum teruji otomatis, "Lanjut? (ya/tidak)", dan tepat tiga pertanyaan). Alamat folder ditulis sebagai `[isian: ...]`.

## Catatan revisi 1.0.1 (2026-10-12)
- Revisi setelah uji pertama (skor 5,25 naik ke 6,75; script terbukti benar pada 800 kasus acak, tetapi perilaku agent saat OpenClaw tidak bisa dihubungi perlu dibenahi): ditambah "ATURAN BERHENTI" (bila perintah `openclaw automations/cron` gagal sekali, agent berhenti memakainya, tidak membaca atau mengubah konfigurasi, tidak memeriksa atau membuat token, tidak menjalankan `openclaw doctor` atau me-restart).
- "Mode terblokir": pekerjaan lokal tetap jalan, lalu agent menampilkan rencana lengkap siap salin dalam satu pesan (tabel job, kalimat "lapor selesai", perintah pengawas) dan satu kalimat awam apa yang perlu dibereskan pengguna. Prinsip "kerjakan dulu, tanya di akhir" (maksimal 3 pertanyaan), blok hasil BERMASALAH/OK, dan penolakan baku ditambahkan; deskripsi disesuaikan.

## Catatan revisi 1.0.0 (2026-10-12)
- Rilis awal (uji internal): memantau jadwal/laporan otomatis OpenClaw milik sendiri agar kegagalan tidak diam-diam: mendaftarkan tiap job (jadwal, toleransi, WIB/WITA/WIT), menambah baris "lapor selesai" di akhir job, dan satu pengawas yang mengabari Telegram hanya bila ada yang terlambat atau hilang. Perhitungan status oleh script `pantau_cron.py`.
