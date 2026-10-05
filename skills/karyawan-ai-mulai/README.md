# Starter Kit Karyawan AI — Mulai dalam 5 Menit

**Cukup ketik "mulai", AI langsung wawancara singkat lalu kerjakan tugas pertama Anda.**

## Manfaat
- ✅ Tidak perlu tahu istilah teknis atau nama-nama skill — cukup jawab 5 pertanyaan singkat.
- ✅ Dapat rekomendasi paket kerja yang sesuai profesi & tugas Anda, bukan daftar 30+ skill yang membingungkan.
- ✅ Langsung lihat **hasil nyata** di menit pertama (bukan sekadar penjelasan).
- ✅ Rencana 7 hari sederhana supaya kebiasaan baru terbentuk, satu langkah per hari.
- ✅ Diingatkan soal privasi sejak awal — cocok untuk yang khawatir data bocor.
- ✅ Menawarkan memasang "Aturan kerja Komunitech" ke `AGENTS.md` OpenClaw Anda (setelah Anda setujui), supaya aturan aman tetap berlaku di setiap percakapan.

## Cocok untuk siapa
- Pemilik usaha/profesional yang **sudah pakai OpenClaw** tapi belum tahu mulai dari mana.
- Yang merasa "terlalu teknis" atau tidak punya waktu bereksperimen sendiri.
- Yang ingin dipandu, bukan disodori manual panjang.

## Contoh sebelum & sesudah
**Sebelum:** Punya OpenClaw terpasang, tapi bingung mau dipakai untuk apa. Skill Komunitech
menumpuk tanpa tahu mana yang relevan.

**Sesudah (cukup ketik):** "mulai karyawan AI, saya owner toko kopi kecil, tim 4 orang..."
→ Dalam satu percakapan: rekomendasi 3 skill yang pas, dipasang dengan izin Anda, satu tugas
nyata langsung selesai (misalnya 3 caption promo siap posting), dan rencana 7 hari untuk
membiasakan diri.

## Cara pakai
Setelah terpasang, cukup ketik ke AI agent OpenClaw Anda, misalnya:
- "mulai karyawan AI"
- "bantu saya mulai pakai AI di bisnis"
- "setup asisten"

## Instalasi singkat
Salin folder `karyawan-ai-mulai` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah AI langsung memasang skill lain tanpa izin saya?**
Tidak. Setiap pemasangan skill baru selalu ditawarkan dulu dan menunggu jawaban "ya" dari Anda.

**Kalau industri saya tidak ada di daftar, apa yang terjadi?**
Skill akan jujur bilang belum ada paket khusus, lalu menawarkan paket umum yang bisa Anda
koreksi kapan saja.

**Apakah data usaha saya dikirim ke Komunitech?**
Tidak. Semua berjalan di OpenClaw milik Anda sendiri; data tetap di komputer Anda. Skill ini
juga akan menawarkan pengecekan privasi dasar (skill `cek-privasi-openclaw`) di langkah terakhir.

## Catatan revisi 1.1.8 (2026-10-01)

- Uji OpenClaw 2026-10-01: (a) "Hasil Tugas Pertama" kini wajib di balasan yang sama dengan rekomendasi, tanpa menunggu pemasangan skill; (b) blok Aturan kerja ditampilkan utuh kata per kata sebelum minta "ya" (tidak diringkas); (c) folder skill hanya dicari di Unduhan/folder yang disebut pengguna, path sumber disebut sebelum minta izin, tidak menyalin dari `/tmp`/instalasi OpenClaw lain; (d) istilah jujur — "Starter Kit/paket Anda" hanya untuk folder unduhan yang benar-benar ditemukan; (e) tidak ada placeholder klaim hasil untuk kosmetik di tugas pertama.

## Catatan revisi 1.1.7 (2026-10-01)

- Blok Aturan kerja Komunitech v3: aturan 16 tidak lagi menyebut nama skill auto-trading (agent sempat menawarkan skill yang tidak terpasang); aturan 12 melarang menyarankan layanan lain (mis. UptimeRobot) untuk memantau situs pesaing; aturan 11 menambah "sebelum kehabisan" ke daftar urgensi palsu. Hasil uji v2: risiko 2/18 (v1 4/16, tanpa blok 13/16).

## Catatan revisi 1.1.6 (2026-10-01)
- Blok "Aturan kerja Komunitech" diperbarui ke v2 setelah uji independen (risiko 13/16 → 4/16, 2 skenario masih gagal): (a) daftar kata/klaim produk yang dilarang bila tidak disebut pemilik (homemade, fresh, tanpa pengawet, halal/BPOM, asal, ukuran, "stok terbatas/promo terakhir", dll.) → pakai `[ISI: ...]` atau tanya; (b) fakta PPN eksplisit: tarif 12% sejak 1 Jan 2025, tetapi barang/jasa non-mewah memakai DPP nilai lain 11/12 (efektif 11%), 12% penuh hanya barang mewah (PMK 131/2024); angka pajak lewat skill/script atau rumus; (c) hanya menyebut kemampuan/skill yang benar-benar terpasang dan sudah dicek; Telegram dulu untuk notifikasi; cek alat sebelum usul pasang; tidak me-restart proses; cek uptime pesaing termasuk larangan pantau. Pengguna dengan blok v1 akan ditawari mengganti blok lama.

## Catatan revisi 1.1.5 (2026-10-01)
- Langkah baru: menawarkan memasang blok "Aturan kerja Komunitech" (`references/aturan-kerja-agents.md`) ke `AGENTS.md` workspace OpenClaw. Isi blok selalu ditampilkan dulu, hanya ditambahkan di akhir file setelah Anda menjawab "ya" (isi lain tidak diubah), dan tidak dipasang dua kali. Alasannya: uji OpenClaw 2026-10-01 menunjukkan perilaku berisiko (menawarkan kirim WA otomatis, mengulang password, `find /`, `pip install`, mengubah konfigurasi sendiri, mengarang fakta produk) justru muncul saat skill tidak dibuka; `AGENTS.md` dibaca OpenClaw di setiap percakapan.
