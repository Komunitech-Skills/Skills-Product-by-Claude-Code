# Wawancara Kerja Terstruktur, Adil dan Terukur

**Satu posisi, satu paket: pertanyaan, rubrik skor, kartu penilaian, dan perbandingan kandidat setelah wawancara.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) hanya dipakai untuk menghitung skor kandidat dan membagi waktu wawancara; tanpa Python skill tetap berjalan, AI menghitung langsung tetapi angkanya sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Paket wawancara lengkap untuk satu posisi.** 4-6 kompetensi inti, pertanyaan perilaku (pola STAR) dan situasional lengkap dengan tanda jawaban kuat dan lemah, pertanyaan lanjutan, satu tes praktik singkat, dan waktu per bagian. Siap tempel atau cetak.
- ✅ **Semua pelamar dinilai dengan ukuran yang sama.** Rubrik skor 1-5 dengan contoh perilaku yang bisa diamati, dan kartu skor yang diisi pewawancara sebelum berdiskusi, jadi hasilnya bisa dibandingkan dan tidak bergantung pada kesan pertama.
- ✅ **Perbandingan kandidat setelah wawancara.** Kirim skor dari beberapa pewawancara: skill menghitung rata-rata per kompetensi, total berbobot, peringkat, dan menandai perbedaan penilaian lebih dari 1,5 poin yang perlu dibahas bersama.
- ✅ **Dirancang adil dan hati-hati.** Daftar pertanyaan yang tidak boleh ditanyakan (status menikah, rencana hamil, agama, suku, usia, kesehatan yang tidak terkait tugas) beserta padanan sah berbasis kompetensi dan ketersediaan kerja, dengan dasar UU 13/2003 Pasal 5-6 dan UU 27/2022. Bukan nasihat hukum.
- ✅ **Siap untuk 8 posisi umum UMKM** (kasir, admin, sales/CS, staf gudang, barista/kitchen, marketing konten, akuntansi junior, driver/kurir). Posisi lain disusun dari tugas utama yang Anda sebut.

## Cocok untuk siapa
- Pemilik toko, kafe, klinik, bengkel, atau kantor kecil yang mewawancarai sendiri tanpa panduan baku.
- HR/admin merangkap yang ingin wawancara lebih rapi dan hasilnya bisa dipertanggungjawabkan.
- Usaha yang diwawancarai bergantian oleh HRD, atasan langsung, dan pemilik.
- **Bukan untuk:** menyaring tumpukan CV (pakai skill Seleksi CV Pelamar, `seleksi-cv-pelamar`), menulis iklan lowongan (skill Lowongan Kerja, `lowongan-kerja`), onboarding karyawan baru (`sop-onboarding`), kontrak kerja (`kontrak-kerja-pkwt`), psikotes, atau keputusan akhir mempekerjakan.

## Contoh sebelum & sesudah
**Sebelum (ilustrasi):** tiga pelamar kasir diwawancarai bergantian dengan pertanyaan yang berbeda-beda. Penilaiannya "kesannya baik", tanpa angka, dan sulit dibandingkan. Ada pertanyaan tentang status menikah yang sebenarnya tidak boleh ditanyakan.

**Sesudah:** *akan diisi dari hasil uji.* Cuplikan paket wawancara dan perbandingan kandidat yang sebenarnya akan ditambahkan di sini setelah skill diuji.

## Cara pakai
Setelah terpasang, cukup ceritakan posisinya, misalnya:
- "Buatkan panduan wawancara untuk kasir toko, 2 pewawancara, 45 menit."
- "Ini iklan lowongan admin toko online. Siapkan pertanyaan wawancara, rubrik, dan kartu skornya."
- "Ini skor 3 kandidat dari Bu Rina dan Pak Dedi. Siapa yang paling cocok dan mana yang perlu dibahas?"

Tidak perlu lengkap: yang kurang ditandai `[isian: ...]` dan ditanyakan maksimal tiga hal di akhir. Skill tidak mengirim apa pun sendiri, tidak mencari pelamar di internet atau media sosial, dan keputusan akhir tetap di tangan Anda.

## Instalasi singkat
Salin folder `panduan-wawancara-kerja` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): `docs/instalasi.md` di dalam paket. Python hanya untuk menghitung skor dan waktu (perintah: `python3 scripts/skor_wawancara.py`, Windows: `python` atau `py`).

**Status uji (jujur):** skill ini baru selesai dibuat dan belum melewati uji sebelum/sesudah di platform mana pun. Hasil uji (skor, selisih, platform yang benar-benar diuji) akan diisi di sini setelah pengujian.

## FAQ
**Bolehkah menanyakan status menikah, rencana hamil, agama, atau usia pelamar?**
Tidak. Itu diskriminasi dalam rekrutmen (UU 13/2003 Pasal 5-6; SE Menaker M/6/HK.04/V/2025) dan juga tidak berguna untuk menilai kemampuan kerja. Skill menolak permintaan seperti itu dengan singkat, memberi pertanyaan pengganti yang sah (misalnya "Pekerjaan ini bergilir shift sampai pukul 21.00, apakah jadwal itu bisa Anda penuhi?"), lalu tetap membuat paket wawancaranya.

**Apakah skill ini yang memutuskan siapa diterima?**
Tidak. Skor dan saran adalah alat bantu untuk membandingkan kandidat dengan ukuran yang sama. Keputusan akhir tetap di Anda setelah membahas bukti bersama pewawancara lain.

**Bagaimana dengan data pelamar dan rekaman wawancara?**
Skill ini tidak mengirim data ke mana pun dan tidak mencari data pelamar di internet. Catatan, kartu skor, dan rekaman adalah data pribadi (UU 27/2022): rekam hanya dengan izin pelamar, simpan di perangkat Anda, jangan bagikan ke grup umum, dan hapus setelah proses selesai. Teks yang Anda tempel diproses oleh model AI di aplikasi agent Anda, jadi ikuti kebijakan privasi aplikasi itu.

## Catatan
Bukan nasihat hukum. Ringkasan aturan di `references/aturan-pertanyaan.md` berlaku per 14 Oktober 2026; bagian bertanda PERLU REVIEW belum dicocokkan ke naskah resmi pasal per pasal. Sengketa ketenagakerjaan sebaiknya dibawa ke ahli hukum atau Disnaker. Semua nama dan angka contoh fiktif. Merek pihak ketiga hanya disebut sebagai contoh dan tidak berafiliasi. Lihat `ATTRIBUTION.md`.

## Riwayat perubahan
Versi terkini: **1.0.0**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
