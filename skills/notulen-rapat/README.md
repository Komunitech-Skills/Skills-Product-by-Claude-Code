# Notulen Rapat Rapi dari Catatan Berantakan

**Tempel catatan atau transkrip rapat, dapat notulen lengkap dan pesan ringkas siap kirim ke grup WA.**

*Diuji AI penguji independen: 6 → 9 dari 10 (tanggal seperti "Jumat depan" dihitung jadi tanggal nyata, dan angka yang tidak jelas ditandai, bukan ditebak).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

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

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

**Hasil uji (jujur):**
- **Uji OpenClaw, 1 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`, satu skenario notulen dari catatan rapat berantakan): nilai 6 tanpa skill menjadi 8,5 dengan skill (skala 10); uji ulang setelah perbaikan v1.0.3 bernilai 9. Tanpa skill, "sales sept 2,1M" salah ditulis Rp2,1 juta, tanggal relatif tidak diubah menjadi tanggal nyata, dan ada satu tugas yang dikarang. Dengan skill, tanggal dihitung skrip (mis. "Sebelum Rabu, 7 Oktober 2026") dan satuan "M" yang belum jelas ditandai untuk dikonfirmasi.
- Pada uji ulang v1.0.3 masih muncul satu tugas tambahan yang melampaui catatan (diberi peringatan, tetapi tetap tampil). Perbaikannya ada di v1.0.4 dan belum diuji ulang di OpenClaw.

**Status uji (jujur):** diuji di OpenClaw (satu skenario) dan Claude Code (simulasi agent); Codex dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Bagaimana kalau catatan saya campur bahasa Jawa atau Inggris?**
Umumnya tidak masalah. Notulen ditulis dalam bahasa Indonesia yang rapi, dan maksud aslinya tetap dijaga.

**Apakah AI bisa salah menulis keputusan?**
Bisa, karena AI tidak sempurna. Skill ini dirancang hati-hati: hanya hal yang jelas disepakati yang ditulis sebagai keputusan, dan yang ragu masuk ke daftar "Perlu dikonfirmasi". Tetap baca ulang notulen sebelum dibagikan.

**Hal rahasia seperti gaji ikut masuk ke pesan WA?**
Skill dirancang agar info sensitif hanya ada di notulen lengkap, tidak di pesan grup, dan memberi tahu Anda bila ada yang sengaja dikeluarkan. Tetap periksa pesan grup sebelum dikirim.

## Riwayat perubahan

Versi terkini: **1.0.4**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
