# CV & Lamaran yang Cocok dengan Lowongan

**Tempel lowongan + ceritakan pengalaman Anda, dapat CV ramah ATS (sistem penyaring CV otomatis di portal karier) dan surat lamaran siap kirim — tanpa karangan.**

Diuji AI penguji independen di OpenClaw: 6,0 → 8,5 dari 10 (CV disusun tanpa keahlian karangan, celah kerja 21 bulan ditandai, dan kecocokan lowongan dinilai berbobot; tanpa skill, CV tetap memuat keahlian yang tidak pernah disebut pengguna).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Profil pengalaman induk — isi riwayat kerja sekali, dipakai berulang di setiap lamaran (tidak ketik ulang)
- ✅ Evaluasi kecocokan lowongan: skor + alasan + celah, sebelum Anda buang waktu melamar yang tidak cocok
- ✅ CV otomatis disesuaikan kata kunci lowongan; pengalaman dan gelar tidak dikarang
- ✅ Format ramah ATS (satu kolom, tanpa tabel/foto) — membantu CV terbaca oleh penyaringan otomatis di portal karier & website perusahaan (tanpa jaminan lolos)
- ✅ Skor kecocokan kata kunci dihitung dengan skrip (program hitung kecil), bukan dikira-kira, lengkap daftar kata kunci yang hilang
- ✅ Surat lamaran formal, email singkat, dan pesan WA/LinkedIn ke rekruter — sekali jalan
- ✅ Latihan wawancara metode STAR (Situasi, Tugas, Aksi, Hasil) berbasis pengalaman nyata Anda, lengkap sesi tanya-jawab bermain peran
- ✅ Bahasa Indonesia & Inggris, plus checklist typo/format sebelum kirim

## Cocok untuk siapa
- Pencari kerja yang mau melamar posisi tertentu dan ingin CV-nya "nyambung" dengan lowongan
- Profesional yang pindah karier dan bingung menonjolkan pengalaman yang relevan
- Fresh graduate yang belum tahu format CV yang benar

## Contoh sebelum & sesudah
**Sebelum:** CV umum dikirim ke semua lowongan, tidak ada yang dipanggil wawancara.

**Sesudah (cukup ketik):** "Sesuaikan CV saya dengan lowongan ini: [tempel lowongan]. Pengalaman saya: ..."

Cuplikan hasil (contoh dengan data fiktif: lowongan Staff Admin Gudang; dipotong dari `examples/01-admin-gudang.md`; WMS = aplikasi pengelola gudang):
```
## Skor Kecocokan Kata Kunci
…
48% kata kunci lowongan ditemukan di draf CV (12/25)
…
Saya cek dulu ke Ibu Siti: apakah pernah pakai aplikasi WMS (Warehouse Management
System) atau alat scan barcode di CV Berkah Jaya? Kalau belum pernah, saya tidak akan
menuliskannya — biar CV tetap jujur, saya hanya akan menonjolkan pengalaman stock
opname dan pencatatan stok yang memang sudah dimiliki.
…
## CV Versi ATS (Bahasa Indonesia)
…
RINGKASAN PROFIL
Admin Gudang dengan 2 tahun pengalaman mencatat keluar-masuk barang, mengelola kartu
stok, dan melakukan stock opname bulanan. Teliti dan terbiasa bekerja dengan target
laporan inventory yang akurat.
```
Hasil lengkapnya juga memuat surat lamaran, email singkat, dan checklist sebelum kirim.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Sesuaikan CV saya dengan lowongan Admin Gudang ini [tempel]"
- "Saya cocok nggak sama lowongan ini? Kasih skor sama alasannya"
- "Bikinkan surat lamaran untuk posisi Staff Finance di PT Sejahtera"
- "Cek CV saya cocok nggak sama lowongan ini"
- "Bikinkan pesan WA buat kenalan ke HRD-nya"
- "Latih saya wawancara buat posisi ini pakai metode STAR"

Lamaran pertama, Anda akan diajak mengisi **profil pengalaman induk** (riwayat kerja, pendidikan, keahlian, ekspektasi gaji). Simpan hasilnya sebagai file di komputer Anda — lamaran berikutnya tinggal tempel lagi, tidak perlu mengetik ulang.

## Instalasi singkat
Salin folder `cv-lamaran-ats` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.1.3), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **8,5** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Diminta menulis gelar S1/Brevet/SAP yang tidak dimiliki: dengan skill menolak, menyusun CV jujur, menandai celah kerja 21 bulan, plus surat lamaran siap kirim.

**Status uji (jujur):** skor kecocokan kata kunci perkiraan, bukan jaminan lolos ATS. Sudah diuji di OpenClaw (uji otomatis agent). Tidak login ke JobStreet/LinkedIn — Anda tempel lowongan sendiri.

## FAQ
**Apakah CV saya "digemukkan" dengan pengalaman palsu?**
Tidak. Skill ini hanya menyusun ulang dan mencocokkan kata kunci dari pengalaman yang benar-benar Anda berikan. Kalau Anda memang belum punya suatu keahlian, itu tidak akan dikarang masuk CV.

**Skor kecocokan kata kunci artinya apa?**
Perkiraan sederhana seberapa banyak kata kunci penting di lowongan yang juga muncul di CV Anda — mirip cara sistem ATS memindai. Bukan jaminan lolos, tapi membantu tahu bagian mana yang perlu diperjelas.

**Bisa buat versi CV yang lebih "cantik" (ada warna/desain)?**
Bisa, tapi versi ATS (teks polos, satu kolom) tetap yang utama untuk lamaran online. Versi visual hanya disarankan untuk dikirim langsung ke perusahaan kecil yang tidak pakai sistem ATS.

**Apakah skill ini mengambil lowongan otomatis dari LinkedIn/JobStreet/Glints?**
Tidak. Anda yang menempel teks lowongan dari sumber mana pun (JobStreet, Glints, Kalibrr, LinkedIn, Instagram, dll). Skill ini tidak login atau mengambil data otomatis dari situs manapun — risiko melanggar aturan platform tersebut lebih kecil.

## Riwayat perubahan

Versi terkini: **1.1.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
