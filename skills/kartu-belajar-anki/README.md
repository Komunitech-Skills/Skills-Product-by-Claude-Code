# Kartu Hafalan Siap Anki

**Tempel catatan Anda, dapat satu set kartu hafalan + jadwal belajar, tanpa ribet aturan penulisan.**

Diuji AI penguji independen: 5,75 → 8,5 dari 10 (kartu, jadwal belajar, dan cara impor tampil utuh di chat Telegram, bukan hanya tersimpan sebagai berkas).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Kartu tanya-jawab (Basic) atau kartu isian rumpang (Cloze) dalam format siap impor ke Anki, aplikasi kartu hafalan gratis (format impor belum diuji langsung di aplikasi Anki), plus label (tag) per topik.
- Rencana harian realistis (berapa kartu baru per hari) otomatis dihitung.
- Pratinjau kartu langsung di chat; isi lengkap (file teks berpemisah tab, TSV) bisa disalin.
- Cocok CPNS, UTBK, sertifikasi, bahasa, dan SOP karyawan baru.
- Menolak permintaan bocoran/hak cipta, tetap bantu dari materi Anda sendiri.

## Cocok untuk siapa
Pelajar dan mahasiswa, guru/bimbel, HR yang melatih karyawan baru, profesional yang belajar sertifikasi.

## Sebelum / sesudah
- **Sebelum:** mengetik kartu satu per satu di Anki, bingung bedanya kartu Basic dan Cloze serta cara memberi label.
- **Sesudah:** agent menyusun puluhan kartu + jadwal; Anda tinggal impor. Cuplikan keluarannya (contoh dengan data fiktif, dari `examples/01-sop-kasir-21-kartu.md`):

```
Deck Anki buat SOP kasir Toko Sumber Rejeki udah siap. Berikut ringkasannya:
**Ringkasan**
- 21 kartu basic (depan/belakang), bahasa Indonesia
…
**Pratinjau (contoh)**
| Depan | Belakang |
|---|---|
| Berapa modal awal uang di laci saat buka kasir? | Rp500.000 pas |
| Saat bayar tunai, di mana uang pelanggan diletakkan sebelum kembalian diambil? | Di atas laci, belum dimasukkan |
| Retur di atas berapa rupiah yang wajib disetujui supervisor? | Di atas Rp200.000 |
…
**Rencana belajar**
21 kartu, 15 kartu baru/hari, ±20 menit/hari → selesai kartu baru dalam 2 hari. Hari 1–2 fokus kartu baru, sisihkan ±5–10 menit review kartu kemarin tiap hari berikutnya.
```

## Cara pakai
Ketik permintaan biasa lalu tempel catatan Anda, misalnya: "Bikinin kartu belajar Anki dari SOP kasir toko kami buat karyawan baru ya" (lalu tempel SOP-nya). Info yang kurang (jumlah hari belajar, jenis kartu) ditanyakan sekali, atau agent memakai pilihan wajar dan menyebut asumsinya. Python bawaan hanya dipakai untuk memeriksa kartu dan menghitung jadwal; tanpa Python hasil tetap muncul di chat.

## Instalasi
Salin folder `kartu-belajar-anki` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` (di dalam ZIP bernama `CARA-INSTAL.md`).

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.1):** rata-rata nilai 5,75 tanpa skill menjadi 8,5 dengan skill (skala 10), dari empat skenario: SOP kasir menjadi 21 kartu (di konteks Telegram), kosakata Inggris, permintaan kurang lengkap, dan jebakan bocoran UTBK. Tanpa skill, kartu hanya disimpan sebagai berkas dan tidak sampai ke chat Telegram; dengan skill isi kartu, jadwal belajar, dan cara impor tampil utuh di chat. Catatan jujur: model biasa pun sudah membuat kartu yang akurat; pembeda skill ini adalah kartu yang benar-benar sampai ke chat, rencana belajar berangka, dan format yang konsisten. Format impor Anki hanya diperiksa dengan skrip, belum dicoba di aplikasi Anki sungguhan. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Diuji langsung di OpenClaw saja; Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## FAQ

**Apakah Anki wajib?**  
Tidak untuk menyusun kartu; impor paling mudah ke Anki desktop (gratis). File teks berpemisah tab (TSV) juga bisa dipakai di aplikasi kartu hafalan lain.

**Bisa dari PDF buku?**  
Tempel ringkasan/ catatan **Anda**; skill tidak menyalin buku berbayar utuh.

**Apakah agent menginstal Anki?**  
Tidak. Anda impor manual lewat menu File → Import.
