# Kanboard Papan Kerja: Pantau Order & Produksi Lewat Chat

**Tanya "order mana yang telat?", "kartu apa yang macet?", atau "pindahkan pesanan Pak Joko ke Dikirim" — AI Anda langsung membaca dan mengatur papan kerja Kanboard, aplikasi kanban gratis yang jalan di komputer sendiri.**

> Komunitech **tidak berafiliasi** dengan proyek Kanboard. Kanboard adalah software open-source (lisensi MIT) milik pembuatnya; skill dan panduan ini adalah karya orisinal Komunitech untuk memudahkan pemilik usaha Indonesia memakainya.

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

(Rincian lengkap: `docs/instalasi.md`.)

3. Buat token di Kanboard (avatar → Profil saya → API → Generate token baru), lalu simpan sekali **di terminal Anda sendiri** (bukan di chat): `python3 ~/.openclaw/skills/kanboard-papan-kerja/scripts/kanboard.py simpan-kunci` (Windows: `python`/`py`).
4. Coba: "Cek Kanboard saya sudah nyambung?"

## FAQ
**Apakah data order saya dikirim ke Komunitech atau pihak lain?**
Tidak. Script hanya menghubungi Kanboard **milik Anda** (biasanya `127.0.0.1`). Tidak ada data ke Komunitech; laporan ke Telegram hanya bila Anda sendiri memasang jadwalnya.

**Bisakah AI menghapus papan atau kartu saya?**
Tidak. Skill ini tidak punya perintah hapus/tutup, dan daftar perintah yang boleh dikirim ke Kanboard dikunci di dalam script. Membuat papan, menambah, dan memindah kartu selalu menunggu jawaban "ya" dari Anda.

**Saya belum pernah pakai Docker. Susah?**
Cukup memasang Docker Desktop lalu menempel satu baris perintah dari panduan. Bila tetap ragu, Komunitech menyediakan jasa setup berbayar (pasang, amankan, buat papan & token, jadwal laporan Telegram, backup).

## Riwayat versi
- **1.0.1 (2026-09-30):** pembacaan jam bahasa Indonesia diperbaiki ("jam 3 sore" = 15:00, "10.00" = 10:00; jam 1-6 tanpa keterangan ditanyakan); tanggal tanpa tahun yang sudah lewat kini diberi PERINGATAN (tidak diam-diam ke tahun depan); kartu di kolom Selesai tidak muncul di "hari ini"; pesan ramah (tanpa traceback) untuk data aneh dari server; "kemarin" dikenali; pencocokan PIC sebagian ditegaskan.
- **1.0.0:** rilis awal.
