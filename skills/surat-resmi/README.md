# Surat Resmi Rapi Sesuai EYD, Siap Cetak

**Sebut keperluannya, dapat surat resmi lengkap dengan kop (kepala surat), nomor, perihal, dan tanda tangan yang benar.**

*Diuji AI penguji independen: 6,75 → 8,75 dari 10 (nama hari, tanggal, dan nomor surat dicek skrip, plus format EYD siap cetak; untuk menolak surat palsu, AI biasa sama baiknya).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Enam jenis surat paling sering dipakai: permohonan, pemberitahuan, undangan, surat kuasa, surat keterangan, dan surat pengantar
- ✅ Ejaan mengikuti EYD Edisi V (pedoman ejaan bahasa Indonesia): "Yth.", "izin", "pukul 09.00", "di tempat", dan tanpa kalimat bertele-tele
- ✅ Nomor surat bulan Romawi dan nama hari dihitung skrip, sehingga salah seperti "Jumat, 3 Oktober 2026" yang ternyata hari Sabtu bisa tertangkap sebelum surat dicetak
- ✅ Format siap tempel ke Word/Google Docs lalu dicetak
- ✅ Catatan meterai dan batasan hukum yang jujur (kapan harus ke notaris)

## Cocok untuk siapa
- Pemilik usaha, admin kantor, dan sekretaris
- Pengurus RT/RW, karang taruna, koperasi, yayasan, dan komite sekolah
- Profesional yang sesekali harus menulis surat resmi dan ingin hasilnya rapi

## Contoh sebelum & sesudah
**Sebelum:** Mencari contoh surat di Google, menyalin, lalu mengganti isinya. Hasilnya masih memakai "Kepada Yth. :", "ijin", dan tanggal "03-10-2026".

**Sesudah (cukup ketik):** "bikinin dong surat undangan rapat warga RT 03 RW 07 buat bahas iuran sampah, minggu 4 okt 2026 jam 7 malem di rumah pak RT, yg ttd ketua RT pak slamet riyadi. kelurahan tugu, depok"
```
Nomor    : 001/UND/RT03-RW07/IX/2026                      Depok, 23 September 2026
Perihal  : Undangan Rapat Warga

Yth. Bapak/Ibu Warga RT 03 RW 07
Kelurahan Tugu
di tempat

Dengan hormat,
Kami mengundang Bapak/Ibu untuk menghadiri rapat warga yang akan dilaksanakan pada
hari, tanggal : Minggu, 4 Oktober 2026
pukul         : 19.00 WIB–selesai
tempat        : Rumah Ketua RT 03, [alamat]
acara         : Pembahasan iuran sampah
...
```
Catatan yang ikut diberikan: "Jam 7 malem" ditulis **pukul 19.00 WIB**; "Minggu, 4 Oktober 2026" sudah dicek skrip dan benar hari Minggu; alamat yang tidak disebut ditandai `[alamat]` untuk Anda isi. Hasil lengkap (dengan kop dan tanda tangan) ada di `examples/02-singkat-undangan-rapat-rt.md`.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Surat kuasa ambil BPKB di leasing untuk staf saya"
- "Surat keterangan kerja untuk mantan karyawan, kerja dari Maret 2023 sampai Agustus 2026"
- "Surat pemberitahuan ke pelanggan: toko libur 3 hari"
- "Tolong rapikan surat saya ini sesuai EYD"

## Syarat
Nomor dan tanggal dibuat dengan Python (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari python.org). Tanpa Python, surat tetap dibuat dan Anda diingatkan untuk mengecek nama hari.

## Instalasi singkat
Salin folder `surat-resmi` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`, dua skenario): rata-rata nilai 6,75 tanpa skill menjadi 8,75 dengan skill (skala 10). Pembeda terbesar: ketepatan hari, tanggal, dan nomor surat (nilai 5 menjadi 9 pada skenario undangan yang sengaja memuat hari salah) serta format EYD V siap cetak. Jujur: menolak membuat surat keterangan kerja palsu setara (8,5 vs 8,5), karena AI biasa pun menolak.

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot Telegram OpenClaw yang asli (grup uji internal Komunitech) pada 16 Oktober 2026, versi 1.0.3, dengan permintaan surat kuasa pengambilan BPKB mobil kantor yang sudah lunas. Skor kami (skala 10), tanpa skill → dengan skill: **6,5** → **8**, selisih +1,5, **lulus acuan kami**, tepat di batas (artinya skor dengan skill minimal 8 dan selisih minimal 1,5 poin).

Dengan skill, surat kuasanya lebih lengkap: ada masa berlaku, larangan dialihkan ke orang lain, wewenang menandatangani tanda terima, kolom NIK dan alamat yang belum Anda berikan dibiarkan kosong untuk diisi (tidak dikarang), petunjuk letak meterai, dan daftar yang dibawa saat mengambil BPKB (fotokopi KTP kedua pihak, cap CV, konfirmasi format ke leasing). Tanpa skill, suratnya sudah cukup baik, tetapi unsur-unsur itu tidak ada.

Catatan jujur: surat dari bot dengan skill tidak menyebut bahwa kendaraan sudah lunas, padahal itu Anda sampaikan, dan catatan akhirnya masih memakai istilah teknis ("dihitung dengan script") serta menyapa Anda dengan "kamu", jadi rapikan sebelum dicetak. NIK, alamat penerima kuasa, serta telepon dan email di kop tetap harus Anda isi sendiri, dan format akhir sebaiknya dikonfirmasi ke leasing. Uji sebelumnya di OpenClaw (1 Oktober 2026, tugas lain: undangan rapat dengan nama hari yang salah) ada di bagian "Hasil uji" di atas: 6,75 → 8,75.

## FAQ
**Apakah surat kuasa wajib pakai meterai?**
Meterai adalah pajak atas dokumen yang dipakai sebagai bukti, bukan syarat sahnya surat. Untuk surat kuasa dan surat keterangan yang akan diserahkan ke instansi, sebaiknya tetap dibubuhi meterai Rp10.000. Tanyakan juga ke instansi tujuan.

**Bisa pakai format nomor surat kantor saya sendiri?**
Bisa. Sebutkan saja polanya, misalnya "nomor urut/HRD/bulan Romawi/tahun".

**Bisa untuk surat dinas instansi pemerintah?**
Bisa sebagai draf. Instansi pemerintah punya pedoman tata naskah dinas sendiri, jadi sesuaikan kop dan kodenya.

## Riwayat perubahan

Versi terkini: **1.0.3**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
