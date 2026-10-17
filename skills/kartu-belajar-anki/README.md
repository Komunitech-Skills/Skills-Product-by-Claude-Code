# Kartu Hafalan Siap Anki

**Tempel catatan Anda, dapat satu set kartu hafalan + jadwal belajar, tanpa ribet aturan penulisan.**

Diuji AI penguji independen di OpenClaw: 5,75 → 8,5 dari 10 pada uji ulang v1.0.1 (12 Okt 2026, empat skenario; uji pertama v1.0.0 6,1 → 7,75 belum lulus). Pembeda dalam uji dengan konteks kanal Telegram: dengan skill kartu, jadwal belajar, dan cara impor tampil utuh di chat; tanpa skill kartu hanya tersimpan sebagai berkas. Di bot Telegram asli (13 Okt 2026) selisihnya kecil: 7,5 → 8.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

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
- **Sesudah:** agent menyusun puluhan kartu + jadwal; Anda tinggal impor. Cuplikan keluarannya (dipotong; dari uji OpenClaw dengan konteks kanal Telegram oleh penguji independen, 12 Okt 2026, data fiktif, `examples/01-sop-kasir-21-kartu.md`; deck = satu paket kartu):

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

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, 12 Okt 2026, v1.0.1 (`examples/00-openclaw-sebelum-sesudah.md`), skor 1–10 penguji independen: tanpa skill **5,75** → dengan skill **8,5** (lulus acuan kami; uji pertama v1.0.0 pada hari yang sama 6,1 → 7,75, belum lulus), empat skenario (SOP kasir 21 kartu di konteks Telegram, kosakata Inggris, input kurang, jebakan bocoran UTBK). Tanpa skill kartu cenderung hanya disimpan sebagai berkas; dengan skill isi kartu, jadwal belajar, dan cara impor tampil utuh di chat. Catatan jujur: model biasa pun sudah membuat kartu yang akurat; pembeda skill ini adalah kartu yang sampai ke chat, rencana belajar berangka, dan format konsisten. Format impor Anki hanya diperiksa skrip, belum dicoba di aplikasi Anki sungguhan.

**Status uji (jujur):** sudah diuji OpenClaw (uji otomatis agent) dan bot Telegram uji (13 Okt 2026). Claude Code, Codex, dan Cursor belum diuji langsung (format skill-nya sama).

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 13 Okt 2026, versi 1.0.1): tanpa skill skor **7,5** → dengan skill skor **8**, selisih +0,5. Belum lulus acuan kami: skor dengan skill sudah 8, tetapi selisihnya masih di bawah 1,5 poin karena tanpa skill pun bot sudah membuat 10 kartu plus berkas CSV. Dengan skill, 16 kartu tampil utuh di chat beserta pratinjau, rencana belajar 5 hari, dan cara impor. Catatan jujur: tab pemisah kartu hilang saat teks lewat Telegram, jadi salin-tempel langsung tidak bisa diimpor; minta bot mengirim berkas TSV/CSV. Uji sebelumnya, di OpenClaw biasa (12 Okt 2026), 5,75 → 8,5 dan lulus acuan kami.

## FAQ

**Apakah Anki wajib?**  
Tidak untuk menyusun kartu; impor paling mudah ke Anki desktop (gratis). File teks berpemisah tab (TSV) juga bisa dipakai di aplikasi kartu hafalan lain.

**Bisa dari PDF buku?**  
Tempel ringkasan/ catatan **Anda**; skill tidak menyalin buku berbayar utuh.

**Apakah agent menginstal Anki?**  
Tidak. Anda impor manual lewat menu File → Import.

## Riwayat perubahan

Versi terkini: **1.0.2** (hanya merapikan satu contoh di panduan agent; cara kerja sama dengan 1.0.1 yang diuji). Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
