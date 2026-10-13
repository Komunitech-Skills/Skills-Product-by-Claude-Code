# Kanboard Papan Kerja: Pantau Order & Produksi Lewat Chat

**Tanya "order mana yang telat?", "kartu apa yang macet?", atau "pindahkan pesanan Pak Joko ke Dikirim" — AI Anda langsung membaca dan mengatur papan kerja Kanboard, aplikasi kanban gratis yang jalan di komputer sendiri.**

> Komunitech **tidak berafiliasi** dengan proyek Kanboard. Kanboard adalah software open-source (lisensi MIT) milik pembuatnya; skill dan panduan ini adalah karya orisinal Komunitech untuk memudahkan pemilik usaha Indonesia memakainya.

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan: Kanboard (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tanpa biaya bulanan per user.** Kanboard gratis dan jalan di laptop/PC/server Anda sendiri — pengganti Trello/ClickUp berbayar untuk tim kecil.
- ✅ **Papan siap pakai sesuai usaha dalam 1 menit.** Template kolom untuk **produksi** (konveksi, makanan, percetakan), **order & pengiriman** (toko online, distributor), **konten** medsos, dan **proyek jasa** — lengkap dengan batas kartu di tahap yang sering menumpuk.
- ✅ **Tahu yang telat & macet tanpa membuka aplikasi.** Kartu jatuh tempo hari ini, yang terlambat, dan yang **tidak bergerak N hari** — dihitung pasti dari data Kanboard, bukan kira-kira.
- ✅ **Laporan pagi siap kirim Telegram** (lewat OpenClaw): satu pesan ringkas, aman di bawah batas panjang Telegram.
- ✅ **Aman.** Tidak ada perintah hapus. Buat papan, tambah kartu, dan pindah kartu selalu lewat pratinjau + persetujuan Anda. Token disimpan terkunci dan tidak pernah ditampilkan; hanya bicara dengan Kanboard milik Anda.

## Cocok untuk siapa
- Usaha **produksi & distribusi** (konveksi, katering, percetakan, mebel, distributor) yang ingin tahu posisi tiap order.
- **Toko online** yang melacak pesanan dari "baru" sampai "diterima" di luar aplikasi marketplace.
- **Agensi/konsultan/freelancer/tim konten** yang mengelola banyak pekerjaan klien sekaligus.
- Pemilik yang ingin cukup bertanya ke AI (OpenClaw, Claude Code, Codex, Cursor) tanpa menghafal menu Kanboard.

**Kurang cocok:** butuh aplikasi di HP untuk tim lapangan (Kanboard berbasis browser; bisa dibuka di HP bila di jaringan kantor), butuh Gantt/anggaran proyek rumit, atau belum ada komputer yang bisa menyala saat jam kerja.

## Contoh sebelum & sesudah
**Sebelum:** buka Kanboard → buka papan satu per satu → lihat tanggal di tiap kartu → kira-kira mana yang sudah lama tidak digeser → ketik ulang ringkasan ke grup WA.

**Sesudah:** ketik *"laporan papan hari ini"* (hasil nyata, Kanboard v1.2.54):
```
LAPORAN PAPAN KERJA - Rabu, 30 September 2026 19:44 WIB
Papan: semua papan aktif | kartu terbuka: 8
Terlambat 3 | Jatuh tempo hari ini 2 | Macet >= 3 hari 3

TERLAMBAT (3)
- #6 Jaket himpunan 40 pcs (jatuh tempo 28 Sep 2026 17:00; papan: Produksi Konveksi Ayu; kolom: Siapkan Bahan)
- #3 INV-0922 Pak Joko - kemeja L (jatuh tempo 30 Sep 2026 15:00; papan: Order Batik Laras; kolom: Dikirim)
...
MACET >= 3 HARI (3)
- #6 Jaket himpunan 40 pcs (diam 6 hari; papan: Produksi Konveksi Ayu; kolom: Siapkan Bahan)
- #2 INV-0921 Bu Wati - 2 kain tulis (diam 5 hari; papan: Order Batik Laras; kolom: Menunggu Bayar)
```
Atau *"buatkan papan produksi untuk konveksi saya"* → AI menunjukkan 6 kolom (Order Masuk → Siapkan Bahan → Produksi → Cek Kualitas → Siap Kirim → Selesai), dan baru membuatnya setelah Anda bilang "ya". Lihat `examples/`.

## Cara pakai
- "Cek Kanboard saya sudah nyambung?"
- "Buatkan papan order & pengiriman untuk toko batik saya"
- "Tambah kartu: seragam SD Harapan 120 pcs, deadline Jumat jam 10, PIC Ayu"
- "Order apa yang jatuh tempo hari ini?", "Mana yang telat?", "Kartu apa yang macet lebih dari 5 hari?"
- "Pindahkan kartu #3 ke Dikirim"
- "Kirim laporan papan ke Telegram saya tiap jam 7 pagi" (OpenClaw)

## Instalasi singkat
1. **Kanboard** terpasang dan menyala — ikuti `docs/panduan-kanboard.md` di paket (Docker, ±20–40 menit, termasuk **pengamanan wajib**), atau pakai **jasa setup Komunitech**.
2. Salin folder `kanboard-papan-kerja` ke folder skills AI agent:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Rincian lengkap per platform: **`docs/instalasi.md`**.

3. Buat token di Kanboard (avatar → Profil saya → API → Generate token baru), lalu simpan sekali **di terminal Anda sendiri** (bukan di chat): `python3 scripts/kanboard.py simpan-kunci` (Windows: `python`/`py`).
4. Coba: "Cek Kanboard saya sudah nyambung?"

**Hasil uji (angka nyata):** uji OpenClaw sebelum/sesudah otomatis agent dengan Kanboard v1.2.54 asli (data contoh), 2026-10-02, skor 1–10 penguji independen. Sumber: `examples/00-openclaw-sebelum-sesudah.md`.
- Uji ulang v1.0.3 (2 skenario, 2 sesi): tanpa skill **4,8** → dengan skill **8,8** (LULUS; pratinjau + "ya" wajib walau diminta "langsung kerjakan").
- Skenario baca laporan (telat/macet/jatuh tempo): tanpa skill sudah cukup baik; dengan skill nomor kartu (#id) dan aturan kolom terakhir lebih konsisten.

**Status uji (jujur):** sudah diuji di OpenClaw (uji otomatis agent, 2026-10-02). Claude Code, Codex, Cursor, dan jadwal Telegram belum kami uji langsung. Panduan Docker/Kanboard di Windows/macOS belum dicoba end-to-end di perangkat pembeli.

## FAQ
**Apakah data order saya dikirim ke Komunitech atau pihak lain?**
Tidak. Script hanya menghubungi Kanboard **milik Anda** (biasanya `127.0.0.1`). Tidak ada data ke Komunitech; laporan ke Telegram hanya bila Anda sendiri memasang jadwalnya.

**Bisakah AI menghapus papan atau kartu saya?**
Tidak. Skill ini tidak punya perintah hapus/tutup, dan daftar perintah yang boleh dikirim ke Kanboard dikunci di dalam script. Membuat papan, menambah, dan memindah kartu selalu menunggu jawaban "ya" dari Anda.

**Saya belum pernah pakai Docker. Susah?**
Cukup memasang Docker Desktop lalu menempel satu baris perintah dari panduan. Bila tetap ragu, Komunitech menyediakan jasa setup berbayar (pasang, amankan, buat papan & token, jadwal laporan Telegram, backup).

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
