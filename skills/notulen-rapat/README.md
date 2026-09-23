# Notulen Rapat Rapi dari Catatan Berantakan

**Tempel catatan atau transkrip rapat, dapat notulen lengkap dan pesan ringkas siap kirim ke grup WA.**

## Manfaat
- ✅ Keputusan, poin diskusi, dan daftar tugas dipisah dengan jelas
- ✅ Tabel action item: siapa, mengerjakan apa, dan tenggatnya kapan. "Jumat depan" diubah menjadi tanggal nyata
- ✅ Tidak mengarang: usulan tidak ditulis sebagai keputusan, dan hal yang belum jelas diberi tanda ⚠️
- ✅ Bonus pesan ringkas untuk grup WhatsApp, tinggal salin dan kirim
- ✅ Bisa dari catatan tangan, transkrip Zoom/Google Meet, atau ringkasan voice note

## Cocok untuk siapa
- Pemilik usaha yang rutin rapat mingguan dengan tim
- Sekretaris, admin kantor, dan notulis organisasi
- Pengurus RT/RW, koperasi, yayasan, komite sekolah, dan panitia acara

## Contoh sebelum & sesudah
**Sebelum:** Selesai rapat, catatan berserakan di HP. Seminggu kemudian tim lupa siapa yang harus mengerjakan apa.

**Sesudah (cukup ketik):** "Rapikan jadi notulen: rapat tim toko kue, hadir Ayu, Dimas, Sari, Fajar. PO hampers dibuka 1 Okt, deal. Sari bikin poster Jumat depan..."
→ Notulen lengkap dengan tabel tugas (Sari: poster PO, Jumat 2 Oktober 2026), daftar hal yang perlu dikonfirmasi, dan pesan WA siap kirim.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Buatkan notulen dari transkrip meeting ini: [tempel]"
- "Rangkum rapat RT tadi malam jadi pesan WA untuk warga"
- "Dari catatan ini, siapa saja yang dapat tugas dan kapan tenggatnya?"

## Syarat
Skill ini tidak mentranskrip rekaman. Tempelkan teks transkrip (fitur transkrip Zoom/Meet/perekam HP) atau ringkasan voice note. Konversi tanggal memakai Python (opsional); tanpa Python, tanggal dihitung manual dan diberi tanda.

## Instalasi singkat
Salin folder `notulen-rapat` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Bagaimana kalau catatan saya campur bahasa Jawa atau Inggris?**
Tidak masalah. Notulen ditulis dalam bahasa Indonesia yang rapi, dan maksud aslinya tetap dijaga.

**Apakah AI bisa salah menulis keputusan?**
Skill ini sengaja dibuat hati-hati. Hanya hal yang jelas disepakati yang ditulis sebagai keputusan. Yang ragu masuk ke daftar "Perlu dikonfirmasi".

**Hal rahasia seperti gaji ikut masuk ke pesan WA?**
Tidak. Info sensitif hanya ada di notulen lengkap, tidak di pesan grup.
