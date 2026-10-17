# Notulen Rapat Rapi dari Catatan Berantakan

**Tempel catatan atau transkrip rapat, dapat notulen lengkap dan pesan ringkas siap kirim ke grup WA.**

*Diuji AI penguji independen di OpenClaw: 6 → 9 dari 10 pada uji ulang v1.0.4 (13 Okt 2026, skenario sama dengan uji pertama; uji pertama 6 → 8,5, lalu 9). Tanggal seperti "Jumat depan" dihitung jadi tanggal nyata atau ditandai ambigu, angka yang tidak jelas ditandai (bukan ditebak), dan tidak ada tugas karangan.*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ Keputusan, poin diskusi, dan daftar tugas dipisah dengan jelas
- ✅ Tabel tugas lanjutan (action item): siapa, mengerjakan apa, dan tenggatnya kapan. "Jumat depan" diubah menjadi tanggal nyata; tafsiran yang bisa ganda diberi tanda "perkiraan" agar Anda cek
- ✅ Dirancang agar tidak mengarang: usulan tidak ditulis sebagai keputusan, dan hal yang belum jelas diberi tanda ⚠️ (tetap baca ulang sebelum dibagikan)
- ✅ Bonus pesan ringkas untuk grup WhatsApp, tinggal salin dan kirim
- ✅ Bisa dari catatan tangan, transkrip Zoom/Google Meet, atau ringkasan voice note

## Cocok untuk siapa
- Pemilik usaha yang rutin rapat mingguan dengan tim
- Sekretaris, admin kantor, dan notulis organisasi
- Pengurus RT/RW, koperasi, yayasan, komite sekolah, dan panitia acara

## Contoh sebelum & sesudah
**Sebelum:** Selesai rapat, catatan berserakan di HP. Seminggu kemudian tim lupa siapa yang harus mengerjakan apa.

**Sesudah (cukup ketik):** "rangkumin dong rapat RT kemarin buat dikirim ke grup warga" lalu tempel catatan rapatnya. Cuplikan hasil (PIC = penanggung jawab; nama fiktif; contoh lengkap di `examples/02-singkat-rapat-rt-pesan-wa.md`):
```
Selamat pagi, Bapak/Ibu warga RT 05.
Berikut ringkasan rapat RT pada Minggu, 20 September 2026:
1. Iuran keamanan naik dari Rp 50.000 menjadi *Rp 60.000* (disetujui mayoritas warga yang hadir). Mulai bulan apa akan diinformasikan kemudian.
2. *Kerja bakti membersihkan got: Sabtu, 26 September 2026, pukul 07.00.* Setiap rumah mengirim 1 orang.
3. Lampu jalan Gang 3 yang mati akan dilaporkan ke kelurahan oleh Pak Joko.
4. Usulan grup WA khusus info keamanan akan dibahas lagi di rapat berikutnya.
Notulen lengkap tersedia di sekretaris RT. Terima kasih atas kehadirannya.
...
| No | Tugas | PIC | Tenggat | Status |
| 1 | Melaporkan lampu jalan Gang 3 yang mati ke kelurahan | Pak Joko | Senin, 21 September 2026 ("minggu depan") ⚠️ | Belum mulai |
...
> 🔒 **Catatan untukmu:** poin **tunggakan iuran Pak Budi** hanya ada di notulen lengkap dan **sengaja tidak dimasukkan ke pesan grup WA**, karena menyangkut data pribadi warga.
```

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Buatkan notulen dari transkrip meeting ini: [tempel]"
- "Rangkum rapat RT tadi malam jadi pesan WA untuk warga"
- "Dari catatan ini, siapa saja yang dapat tugas dan kapan tenggatnya?"

## Syarat
Skill ini tidak mentranskrip rekaman. Tempelkan teks transkrip (fitur transkrip Zoom/Meet/perekam HP) atau ringkasan voice note. Konversi tanggal memakai Python (opsional); tanpa Python, tanggal dihitung manual dan diberi tanda.

## Instalasi singkat
Salin folder `notulen-rapat` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):**
- **Uji OpenClaw, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario notulen dari catatan rapat berantakan): nilai 6 tanpa skill menjadi 8,5 dengan skill (skala 10); uji ulang setelah perbaikan v1.0.3 bernilai 9. Tanpa skill, "sales sept 2,1M" langsung ditulis Rp2,1 juta tanpa konfirmasi padahal satuan "M" belum jelas, tanggal relatif tidak diubah menjadi tanggal nyata, dan ada satu tugas yang dikarang. Dengan skill, tanggal dihitung program kecil (skrip) (mis. "Sebelum Rabu, 7 Oktober 2026") dan satuan "M" yang belum jelas ditandai untuk dikonfirmasi.
- Uji ulang v1.0.4 (13 Okt 2026, OpenClaw 2026.10.2, penguji independen, pesan identik dengan uji pertama, kalender dicek ulang dengan Python): tanpa skill **6** → dengan skill **9** (lulus acuan kami). Tugas tambahan karangan yang muncul di v1.0.3 tidak muncul lagi; tanggal relatif dihitung script, "Jumat depan" ditandai ambigu (2 atau 9 Okt), satuan "2,1M" diberi tanda cek; tanpa skill "2,1M" berubah jadi Rp2,1 juta dan "forklift 2" dibaca 2 unit.

**Status uji (jujur):** diuji di OpenClaw (satu skenario, terakhir 13 Okt 2026 pada v1.0.4) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot Telegram OpenClaw yang asli (grup uji internal Komunitech) pada 16 Oktober 2026, versi 1.0.4, dengan catatan rapat mingguan yang berantakan (angka "2,1M", tanggal seperti "besok" dan "Jumat depan", dan "forklift 2 rusak"). Skor kami (skala 10), tanpa skill → dengan skill: **5** → **8,5**, selisih +3,5, **lulus acuan kami** (artinya skor dengan skill minimal 8 dan selisih minimal 1,5 poin).

Hanya dengan skill, bot membaca "2,1M" sebagai Rp2.100.000.000 (tanpa skill ditulis Rp2,1 juta), mengubah semua tanggal relatif menjadi tanggal pasti (besok = Jumat, 2 Oktober; sebelum Rabu = sebelum 7 Oktober; rapat berikutnya = Kamis, 8 Oktober), menandai "Jumat depan" yang bisa berarti 2 atau 9 Oktober, dan menambah pesan siap kirim ke grup WhatsApp.

Catatan jujur: tanpa skill pun susunan notulennya rapi; nilainya jatuh karena satu salah tafsir angka ("2,1M" ditulis Rp2,1 juta, padahal konteks sewa forklift dan 60 palet membuatnya jelas miliar). Dengan skill, "M" dibaca miliar dari konteks tanpa tanda [cek]; bila singkatan di catatan Anda memang berarti juta, tulis lengkap. Bot dengan skill juga menambahkan keterangan "pengganti 2 customer yang mundur" pada tugas Tono yang tidak ada di catatan, dan menanyakan ulang waktu rapat yang sudah tersirat ("tadi pagi"), jadi baca ulang sebelum dibagikan. Uji sebelumnya dengan pesan yang sama di OpenClaw lokal (13 Oktober 2026, versi 1.0.4): 6 → 9.

## FAQ
**Bagaimana kalau catatan saya campur bahasa Jawa atau Inggris?**
Umumnya tidak masalah. Notulen ditulis dalam bahasa Indonesia yang rapi, dan maksud aslinya tetap dijaga.

**Apakah AI bisa salah menulis keputusan?**
Bisa, karena AI tidak sempurna. Skill ini dirancang hati-hati: hanya hal yang jelas disepakati yang ditulis sebagai keputusan, dan yang ragu masuk ke daftar "Perlu dikonfirmasi". Tetap baca ulang notulen sebelum dibagikan.

**Hal rahasia seperti gaji ikut masuk ke pesan WA?**
Skill dirancang agar info sensitif hanya ada di notulen lengkap, tidak di pesan grup, dan memberi tahu Anda bila ada yang sengaja dikeluarkan. Tetap periksa pesan grup sebelum dikirim.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
