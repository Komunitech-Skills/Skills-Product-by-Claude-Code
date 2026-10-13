# Draf Chat Jadi Word Rapi

**Tempel draf berantakan, dapatkan dokumen Indonesia siap cetak—plus file Word bila diminta.**

Diuji AI penguji independen: 5,63 → 8,28 dari 10 (isi dokumen tampil utuh di chat, dan data yang belum Anda beri ditandai `[isi: ...]`, tidak ditebak).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Mengubah poin-poin hasil AI jadi surat, laporan, atau notulen lengkap dengan kop dan bagian jelas.
- Isi utuh langsung di chat; tidak perlu mengetik ulang struktur.
- File Word (.docx) dibuat tanpa memasang program tambahan (cukup Python standar); belum diuji dibuka di aplikasi Word asli.
- Kolom isian `[isi: ...]` untuk data yang belum Anda beri—tidak dikarang.
- Cocok untuk UMKM, admin kantor, pengurus organisasi, dan guru yang menyiapkan dokumen dari catatan.

## Cocok untuk siapa
- Pemilik usaha yang menyalin draf dari chat AI ke surat/laporan resmi.
- Sekretaris rapat yang merapikan notulen.
- Admin yang menerima draf dari tim dalam bentuk poin-poin.

**Bukan untuk:** menulis surat resmi dari nol tanpa draf (skill Surat Resmi, `surat-resmi`), proposal kerja sama antarusaha dengan hitungan skema (skill Proposal Kerja Sama, `proposal-kerjasama`), atau mengolah PDF (skill PDF Lokal, `pdf-lokal`).

## Contoh sebelum & sesudah
**Sebelum:** 20 baris poin-poin acak dari ChatGPT tanpa kop dan tanpa penutup.

**Sesudah:** satu dokumen dengan kop, judul, paragraf rapi, tabel, dan penutup siap tanda tangan. Cuplikan keluarannya dari draf WA/ChatGPT tentang kenaikan harga (contoh dengan data fiktif, dari `examples/01-surat-kenaikan-harga.md`):

```
KOPI SEDUH NUSANTARA
Jl. Dago Asri No. 12, Bandung 40135
Telp 0812-3456-7890 · Email halo@kopiseduh-nusantara.example
────────────────────────────────────────────────
Bandung, 12 Oktober 2026
Perihal: Pemberitahuan Penyesuaian Harga Biji Kopi
…
| Produk | Harga Lama | Harga Baru |
|---|---|---|
| Arabika Gayo 250 gr | Rp68.000 | Rp75.000 |
| Robusta Lampung 250 gr | Rp45.000 | Rp49.000 |
| House Blend 500 gr | Rp120.000 | Rp129.000 |
…
Bayu
Pemilik, Kopi Seduh Nusantara
```

## Cara pakai
Ketik, misalnya: "Tolong rapikan draf ini jadi surat resmi siap kirim ke pelanggan, pakai kop usaha saya" lalu tempel drafnya. Ingin file Word? Tambahkan "buatkan file Word-nya" atau balas "kirim file". Berkas `.docx` dibuat dengan program kecil bawaan skill; pembukaannya di aplikasi Word asli belum diuji tim Komunitech, jadi bila ada masalah, salin teks dari chat.

## Instalasi singkat
Salin folder `ubah-draf-ke-dokumen` ke folder skills agent Anda. Detail: `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Python opsional (hanya untuk file Word otomatis).

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.1):** rata-rata nilai 5,63 tanpa skill menjadi 8,28 dengan skill (skala 10), dari empat skenario: draf WA/ChatGPT jadi surat kenaikan harga (juga di konteks Telegram), notulen rapat dengan tabel tindak lanjut, laporan dari satu kalimat, dan jebakan (kop dinas palsu dan omzet digelembungkan). Tanpa skill, notulen hanya disimpan sebagai berkas sehingga tidak terlihat di chat, dan data yang belum diberikan ditebak; dengan skill isi dokumen utuh di chat dan yang belum diputuskan ditandai `[isi: ...]`. Catatan jujur: model biasa pun sudah menulis surat yang baik pada skenario pertama. Pembukaan file Word di aplikasi Word asli dan pengiriman lampiran Word lewat bot Telegram sungguhan belum diuji. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah wajib memasang Pandoc (program konversi dokumen)?** Tidak. File Word dibuat dengan program kecil bawaan skill.

**Bisa PDF?** Buka `.docx` di Word/Google Docs lalu simpan sebagai PDF.

**Apakah kop/logo saya otomatis?** Beri teks kop sekali; skill memakainya di dokumen berikutnya bila Anda sebutkan.
