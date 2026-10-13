# Draf Chat Jadi Word Rapi

**Tempel draf berantakan, dapatkan dokumen Indonesia siap cetak—plus file Word bila diminta.**

## Manfaat
- Mengubah bullet hasil AI jadi surat, laporan, atau notulen lengkap dengan kop dan bagian jelas.
- Isi utuh langsung di chat; tidak perlu mengetik ulang struktur.
- File `.docx` tanpa instal Pandoc (script Python standar).
- Placeholder `[isi: ...]` untuk data yang belum Anda beri—tidak dikarang.
- Cocok untuk UMKM, admin kantor, pengurus organisasi, dan guru yang menyiapkan dokumen dari catatan.

## Cocok untuk siapa
- Pemilik usaha yang menyalin draf dari chat AI ke surat/laporan resmi.
- Sekretaris rapat yang merapikan notulen.
- Admin yang menerima draf dari tim dalam bentuk poin-poin.

**Bukan untuk:** menulis surat resmi dari nol tanpa draf (`surat-resmi`), proposal B2B dengan hitungan skema (`proposal-kerjasama`), atau mengolah PDF (`pdf-lokal`).

## Contoh sebelum & sesudah
**Sebelum:** 20 baris bullet acak dari ChatGPT tanpa kop dan tanpa penutup.

**Sesudah:** satu dokumen dengan kop, judul, paragraf rapi, tabel tindak lanjut, dan penutup siap tanda tangan. 

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.1):** rata-rata nilai 5,63 tanpa skill menjadi 8,28 dengan skill (skala 10). Tanpa skill, notulen hanya disimpan sebagai berkas sehingga tidak terlihat di chat, dan data yang belum diberikan ditebak; dengan skill isi dokumen utuh di chat dan yang belum diputuskan ditandai `[isi: ...]`. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

## Cara pakai
Ketik, misalnya: "Tolong rapikan draf ini jadi surat resmi siap kirim ke pelanggan, pakai kop usaha saya" lalu tempel drafnya. Ingin file Word? Tambahkan "buatkan file Word-nya" atau balas "kirim file". Berkas `.docx` dibuat dengan script bawaan; pembukaannya di aplikasi Word asli belum diuji tim Komunitech, jadi bila ada masalah, salin teks dari chat.

## Instalasi singkat
Salin folder `ubah-draf-ke-dokumen` ke folder skills agent Anda. Detail: `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Python opsional (hanya untuk file Word otomatis).

## FAQ
**Apakah wajib Pandoc?** Tidak. Word dibuat dengan script bawaan skill.

**Bisa PDF?** Buka `.docx` di Word/Google Docs lalu simpan sebagai PDF.

**Apakah kop/logo saya otomatis?** Beri teks kop sekali; skill memakainya di dokumen berikutnya bila Anda sebutkan.
