# Notebook Riset Lokal: NotebookLM Pribadi yang Tetap di Komputer Anda

**Kumpulkan PDF regulasi, katalog supplier, notulen rapat, atau artikel riset ke satu "notebook" — lalu tanya apa saja ke AI Anda dan dapatkan jawaban lengkap dengan kutipan sumbernya. Semua data tetap di komputer/server Anda sendiri, tidak dititipkan ke Google atau siapa pun.**

> Komunitech **tidak berafiliasi** dengan proyek Open Notebook. Open Notebook adalah software open-source (MIT) milik komunitasnya sendiri (lfnovo); skill dan panduan ini adalah karya orisinal Komunitech untuk mempermudah pemakaiannya bagi profesional dan pemilik usaha Indonesia.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan: Open Notebook (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Alternatif NotebookLM yang privat.** Dokumen usaha, riset kompetitor, atau kontrak Anda tidak pernah dikirim ke server Google — semuanya jalan di komputer/server sendiri lewat Docker.
- ✅ **Tanya, jangan cari manual.** "Berapa tarif PPh final UMKM di dokumen ini?" — AI menjawab lengkap dengan kutipan sumbernya, bukan Anda yang harus buka satu-satu PDF.
- ✅ **Satu tempat untuk banyak dokumen.** Kumpulkan regulasi, katalog supplier, notulen rapat, artikel riset dalam satu notebook, lalu tanya lintas semua dokumen sekaligus.
- ✅ **Pencarian cepat tanpa AI bila hanya butuh kata kunci.** `cari` langsung ke database, tanpa menunggu model AI dan tanpa memakai kuota.
- ✅ **Podcast dari dokumen (opsional).** Ubah kumpulan riset jadi audio percakapan untuk didengar sambil jalan/nyetir, bila model text-to-speech tersedia.
- ✅ **Aman untuk data usaha.** Menambah sumber/notebook selalu lewat pratinjau dan butuh persetujuan Anda. Kata sandi API tidak pernah ditampilkan.

## Cocok untuk siapa
- Profesional (konsultan, praktisi hukum internal, akuntan) yang perlu tanya-jawab cepat ke tumpukan regulasi/dokumen.
- Pemilik usaha yang mengumpulkan katalog banyak supplier dan ingin bandingkan cepat tanpa buka satu-satu.
- Siapa pun yang sering menerima notulen rapat/artikel panjang dan ingin ringkasan siap pakai.

**Kurang cocok:** belum siap memasang Docker (lihat instalasi — satu lapis teknis tambahan, atau pakai jasa setup Komunitech); butuh mengunggah banyak file PDF langsung lewat AI chat (v1.0.1 mengarahkan Anda seret-lepas file ke tampilan web Open Notebook, bukan lewat skill); komputer dengan RAM terbatas dan ingin memakai model AI lokal gratis (Ollama butuh RAM cukup besar — API berbayar jadi alternatif).

## Contoh sebelum & sesudah
**Sebelum:** buka folder berisi belasan PDF PP/PMK pajak UMKM satu-satu, `Ctrl+F` di tiap file, catat manual angka yang cocok, masih tidak yakin sudah baca semua yang relevan.

**Sesudah:** *"Di notebook Regulasi Pajak UMKM, berapa tarif PPh final terbaru?"*
```json
{
  "pertanyaan": "Berapa tarif PPh final terbaru?",
  "jawaban": "PPh final UMKM 0,5% dari omzet, berdasarkan PP 55/2022...",
  "catatan": "Jawaban disusun model AI dari sumber di notebook Anda. Selalu periksa ulang isi penting (regulasi, angka, kutipan) di sumber aslinya."
}
```
(Bentuk respons diverifikasi lewat uji end-to-end terhadap Open Notebook 1.14.0 ASLI, termasuk perbaikan bug `tambah-sumber` yang sempat gagal total di versi awal — lihat `ATTRIBUTION.md` dan `examples/HASIL-UJI.md`.)

## Cara pakai
Setelah Open Notebook terpasang dan tersambung, cukup ketik permintaan biasa:
- "Cek Open Notebook saya sudah nyambung belum"
- "Kumpulkan PDF/artikel ini ke notebook riset kompetitor"
- "Apa isi dokumen ini soal [topik]?"
- "Ringkas semua yang sudah saya kumpulkan di notebook X"
- "Cari kata 'force majeure' di kontrak-kontrak ini"
- "Jadikan ringkasan ini podcast" (bila profil episode sudah dibuat)

## Instalasi singkat
1. **Open Notebook** sudah terpasang dan menyala. Belum? Ikuti `docs/panduan-open-notebook.md` di paket (pasang Docker Desktop ±20–30 menit), **termasuk langkah pengamanan wajib** (batasi ke `127.0.0.1`, jangan buka ke jaringan lain), atau pakai **jasa setup Komunitech**.
2. Salin folder `notebook-riset-lokal` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

(Rincian & verifikasi lokasi instalasi ada di `docs/instalasi.md`.)

3. Atur minimal satu model AI **Default** di `http://127.0.0.1:8502` → Settings → Models (Ollama gratis, atau kunci API pilihan Anda) — lihat `docs/panduan-open-notebook.md` §5.
4. Bila mengaktifkan kata sandi API: simpan sekali (di terminal Anda sendiri, bukan di chat): `python3 ~/.openclaw/skills/notebook-riset-lokal/scripts/notebook.py simpan-kunci` (Windows: `python`/`py`).
5. Coba: "Cek Open Notebook saya sudah nyambung belum?"

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.0.7), skor 1–10: tanpa skill **4,5** → dengan skill **8,25** (LULUS). Tarif PPh final UMKM dijawab dari dokumen notebook ("0,5% omzet, PP 55/2022"); permintaan buka ke `192.168.1.20` ditolak setelah cek kata sandi API belum aktif — tanpa Docker/SSH. Sumber: `examples/00-openclaw-sebelum-sesudah.md`, `promosi/sebelum-sesudah.jsonl`. Uji server Open Notebook **1.14.0 asli** (Akun B): skor 9/10 di `examples/HASIL-UJI.md`.

**Status uji (jujur):** sudah diuji OpenClaw (sebelum/sesudah otomatis 2026-10-01; muat CLI) dan Claude Code (simulasi agent). Codex dan Cursor belum uji platform asli. Butuh Docker/panduan Open Notebook — lihat `docs/panduan-open-notebook.md`. Jawaban AI dari dokumen Anda wajib dicek ulang (regulasi/angka).

## FAQ
**Apakah dokumen saya dikirim ke server Komunitech atau Google?**
Tidak. Script ini hanya menghubungi Open Notebook **milik Anda sendiri** (`127.0.0.1`, komputer/server Anda). Bila Anda memilih memakai model AI berbayar (OpenAI/Anthropic/dll.) di Open Notebook, isi pertanyaan dikirim ke penyedia model itu (bukan ke Komunitech) — pilih model AI lokal (Ollama) bila ingin 100% tanpa data keluar komputer.

**Apakah saya perlu server mahal?**
Tidak — komputer/laptop biasa dengan RAM cukup (≥8 GB, ≥16 GB bila memakai model AI lokal) sudah bisa. Untuk pemakaian sehari-hari, komputer perlu menyala saat dipakai; untuk jadwal ringkasan otomatis, lihat `docs/panduan-open-notebook.md` §7 atau jasa setup Komunitech.

**Bisakah AI menghapus dokumen atau notebook saya tanpa sepengetahuan saya?**
Tidak. Skill ini sengaja **tidak punya** perintah hapus sumber/notebook. Menambah sumber, membuat notebook, dan memulai podcast selalu menunjukkan pratinjau dulu dan baru berjalan setelah Anda menjawab "ya".

**Bisakah tim di kantor cabang ikut membuka Open Notebook saya?**
Skill ini sengaja tidak membukanya. `127.0.0.1` artinya "komputer ini sendiri" — hanya bisa dibuka dari komputer tempat Open Notebook menyala, dan di komputer itu tidak perlu VPN apa pun. Open Notebook punya kata sandi opsional (`OPEN_NOTEBOOK_PASSWORD`); skill bisa memeriksa apakah sedang aktif lewat perintah cek. Bila tetap butuh akses bersama, itu penyiapan jaringan lanjutan (kata sandi aktif, koneksi terenkripsi, tidak dibuka ke internet) — sebaiknya lewat orang yang paham atau jasa setup Komunitech, karena dokumen usaha bisa terbaca orang lain bila salah atur.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
