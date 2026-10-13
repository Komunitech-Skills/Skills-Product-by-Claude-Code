# CV & Lamaran yang Cocok dengan Lowongan

**Tempel lowongan + ceritakan pengalamanmu, dapat CV ramah ATS dan surat lamaran siap kirim — tanpa karangan.**

## Manfaat
- ✅ Profil pengalaman induk — isi riwayat kerja sekali, dipakai berulang di setiap lamaran (tidak ketik ulang)
- ✅ Evaluasi kecocokan lowongan: skor + alasan + celah, sebelum kamu buang waktu melamar yang tidak cocok
- ✅ CV otomatis disesuaikan kata kunci lowongan, tanpa mengarang pengalaman/gelar
- ✅ Format ramah ATS (satu kolom, tanpa tabel/foto) — lolos penyaringan otomatis di portal karier & website perusahaan
- ✅ Skor kecocokan kata kunci dihitung script, bukan dikira-kira, lengkap daftar kata kunci yang hilang
- ✅ Surat lamaran formal, email singkat, dan pesan WA/LinkedIn ke rekruter — sekali jalan
- ✅ Latihan wawancara metode STAR berbasis pengalaman nyatamu, lengkap sesi roleplay tanya-jawab
- ✅ Bahasa Indonesia & Inggris, plus checklist typo/format sebelum kirim

## Cocok untuk siapa
- Pencari kerja yang mau melamar posisi tertentu dan ingin CV-nya "nyambung" dengan lowongan
- Profesional yang pindah karier dan bingung menonjolkan pengalaman yang relevan
- Fresh graduate yang belum tahu format CV yang benar

## Contoh sebelum & sesudah
**Sebelum:** CV umum dikirim ke semua lowongan, tidak ada yang dipanggil wawancara.

**Sesudah (cukup ketik):** "Sesuaikan CV saya dengan lowongan ini: [tempel lowongan]. Pengalaman saya: ..."
→ CV versi ATS, skor kecocokan kata kunci, surat lamaran, dan pesan ke rekruter — semua siap tempel.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Sesuaikan CV saya dengan lowongan Admin Gudang ini [tempel]"
- "Saya cocok nggak sama lowongan ini? Kasih skor sama alasannya"
- "Bikinkan surat lamaran untuk posisi Staff Finance di PT Sejahtera"
- "Cek CV saya cocok nggak sama lowongan ini"
- "Bikinkan pesan WA buat kenalan ke HRD-nya"
- "Latih saya wawancara buat posisi ini pakai metode STAR"

Lamaran pertama, kamu akan diajak mengisi **profil pengalaman induk** (riwayat kerja, pendidikan, keahlian, ekspektasi gaji). Simpan hasilnya sebagai file di komputermu — lamaran berikutnya tinggal tempel lagi, tidak perlu mengetik ulang.

## Instalasi singkat
Salin folder `cv-lamaran-ats` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap per platform (termasuk Windows): lihat `docs/instalasi.md` dan `CARA-INSTAL.md` di paket.

**Hasil uji (angka nyata):** uji OpenClaw (home terisolasi), 1 Okt 2026 (v1.1.3), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **8,5** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Diminta menulis gelar S1/Brevet/SAP yang tidak dimiliki: dengan skill menolak, menyusun CV jujur, menandai celah kerja 21 bulan, plus surat lamaran siap kirim.

**Status uji (jujur):** skor kecocokan kata kunci perkiraan, bukan jaminan lolos ATS. Sudah diuji di OpenClaw (uji otomatis agent). Tidak login ke JobStreet/LinkedIn — Anda tempel lowongan sendiri.

## FAQ
**Apakah CV saya "digemukkan" dengan pengalaman palsu?**
Tidak. Skill ini hanya menyusun ulang dan mencocokkan kata kunci dari pengalaman yang benar-benar kamu berikan. Kalau kamu memang belum punya suatu keahlian, itu tidak akan dikarang masuk CV.

**Skor kecocokan kata kunci artinya apa?**
Perkiraan sederhana seberapa banyak kata kunci penting di lowongan yang juga muncul di CV-mu — mirip cara sistem ATS memindai. Bukan jaminan lolos, tapi membantu tahu bagian mana yang perlu diperjelas.

**Bisa buat versi CV yang lebih "cantik" (ada warna/desain)?**
Bisa, tapi versi ATS (teks polos, satu kolom) tetap yang utama untuk lamaran online. Versi visual hanya disarankan untuk dikirim langsung ke perusahaan kecil yang tidak pakai sistem ATS.

**Apakah skill ini mengambil lowongan otomatis dari LinkedIn/JobStreet/Glints?**
Tidak. Kamu yang menempel teks lowongan dari sumber mana pun (JobStreet, Glints, Kalibrr, LinkedIn, Instagram, dll). Skill ini tidak login atau mengambil data otomatis dari situs manapun — lebih aman dan tidak melanggar aturan platform tersebut.

## Riwayat versi singkat
- **1.1.0** — tambah profil pengalaman induk, evaluasi kecocokan lowongan (skor+alasan+celah), dan latihan wawancara STAR.
- **1.0.1** — versi awal: CV ramah ATS, surat lamaran, skor kecocokan kata kunci.
