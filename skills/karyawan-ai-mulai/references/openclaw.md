# Perintah OpenClaw yang dipakai skill ini

Semua perintah di bawah **diverifikasi** dengan `--help` di OpenClaw **2026.9.5** (mesin uji
terisolasi, tanpa login kanal apa pun). Kalau versi OpenClaw pengguna berbeda dan perintah
gagal, jalankan `<perintah> --help` dulu untuk memastikan opsinya masih sama, lalu beri tahu
pengguna.

**Fallback wajib:** kalau `exec`/perintah komputer tidak diizinkan (tidak ada respons, ditolak,
atau pengguna memakai platform selain OpenClaw seperti Claude Code/Codex/Cursor), **jangan
memaksa**. Tampilkan perintah sebagai teks yang bisa disalin-tempel pengguna sendiri di
terminal, atau jelaskan langkah manual (salin folder skill ke folder skills platform yang
dipakai — lihat `docs/instalasi.md` di paket).

## 1. Cek skill yang sudah terpasang

```bash
openclaw skills list --eligible
```
atau untuk detail lebih lengkap (termasuk yang belum siap dan alasannya):
```bash
openclaw skills list --verbose --json
```
Kalau `exec` tidak diizinkan: cek langsung isi folder skills platform yang dipakai (mis.
`~/.openclaw/skills/`, `~/.claude/skills/`) dengan `read`/`list file`, atau tanyakan ke
pengguna skill apa saja yang sudah ada.

**Prasyarat penting:** skill ini (dan hampir semua skill Komunitech yang punya `scripts/`)
butuh izin menjalankan perintah komputer (`exec`) dan membaca/menulis file. Kalau profil tool
OpenClaw pengguna sudah diperketat ke `tools.profile: "messaging"` (mis. setelah memakai
`cek-privasi-openclaw`), pemasangan otomatis **tidak akan bisa jalan** — beri tahu pengguna dan
tawarkan langkah manual (salin-tempel folder) sebagai gantinya, jangan diam saja.

## 2. Pasang skill yang belum ada (SELALU minta izin pengguna dulu)

Paket Komunitech sudah berupa **folder skill** (bukan diinstal dari ClawHub/git pihak luar).
Path folder ada di dalam Starter Kit yang diunduh & diekstrak pengguna.

**Cari dulu folder hasil ekstrak sebelum memasang.** Pengguna awam sering tidak tahu di mana
ZIP-nya diekstrak. Langkah:
1. Tanyakan/duga lokasi umum: folder Unduhan/Downloads (mis. `~/Downloads/starter-kit-karyawan-ai/`
   di Mac/Linux, `%USERPROFILE%\Downloads\starter-kit-karyawan-ai\` di Windows).
2. Cari folder yang **langsung berisi** `SKILL.md` (bukan folder ZIP itu sendiri) — misalnya
   `.../starter-kit-karyawan-ai/rekap-penjualan-csv/SKILL.md`. Kalau `exec`/pencarian file
   diizinkan, cari dengan pola `**/rekap-penjualan-csv/SKILL.md` (ganti nama skill) di folder
   Unduhan. Kalau tidak diizinkan, minta pengguna menyebut/menyeret lokasi foldernya.
3. Pastikan path yang dipakai di perintah install adalah folder skill itu sendiri, bukan folder
   ZIP pembungkusnya.

```bash
openclaw skills install ./<path-folder-skill> --global
```
- `--global` memasang ke folder terkelola bersama (`~/.openclaw/skills`), dipakai semua agent.
- Skill yang baru dipasang baru terbaca pada **giliran/pesan berikutnya**. Kalau agent belum
  "melihat" skill yang baru dipasang, minta pengguna mengetik ulang permintaannya atau membuka
  sesi baru (`/new` bila tersedia).
- **Kalau muncul pesan "Skill already exists… Re-run with force/update"**: skill itu sudah
  terpasang sebelumnya. Jangan langsung menimpa — jelaskan ke pengguna dan tanya dulu apakah mau
  memperbarui ke versi Starter Kit ini. Hanya pakai `--force` **dengan izin eksplisit** untuk
  perintah itu (bukan izin umum sebelumnya).
- Setelah terpasang, verifikasi dengan `openclaw skills info <nama-skill>` (harus menunjukkan
  "Ready", "Visible to model: yes", "Available as command: yes").
- **Jangan pernah** memasang skill dari sumber di luar paket Komunitech (ClawHub publik, git
  pihak luar, dsb.) tanpa izin eksplisit pengguna — ini melanggar aturan library.
- **Jangan** mempublikasikan skill Komunitech ke ClawHub (registry publik); skill ini berlisensi
  untuk pembeli, bukan untuk dibagikan gratis.

Contoh dialog persetujuan sebelum memasang:
> "Saya akan pasang skill `rekap-penjualan-csv`, `balas-chat-cs`, dan `caption-sosmed-umkm` dari
> Starter Kit ke folder skill global OpenClaw Anda (`~/.openclaw/skills`). Lanjut? (ya/tidak)"

## 3. Menjalankan tugas pertama (quick win)

Tidak ada perintah CLI khusus — cukup memakai skill yang baru dipasang seperti biasa lewat
chat (mis. minta pengguna mengirim file CSV penjualan, atau pakai contoh data di `examples/`
skill yang bersangkutan bila pengguna belum punya data sendiri).

## 4. Menyimpan profil kerja ke memori lokal

Simpan lewat file `USER.md`/`MEMORY.md` di workspace OpenClaw pengguna (`~/.openclaw/workspace`),
BUKAN lewat perintah CLI khusus (tidak ada subperintah CLI untuk menulis memori secara langsung
di versi ini). Gunakan tool `write`/`edit` file biasa untuk menambahkan baris ringkas, misalnya:

```
## Profil kerja (diisi karyawan-ai-mulai, <tanggal>)
- Industri: F&B, skala 6–15 orang
- Kanal favorit: WhatsApp (komputer TIDAK menyala 24 jam)
- Tugas prioritas: rekap penjualan, balas chat CS, caption sosmed
```

Isi **hanya profil kerja**, bukan data pribadi pelanggan atau nomor kontak orang lain.

## 5. Otomasi (opsional, tahap "rencana 7 hari" hari ke-7 atau setelahnya)

Kalau pengguna sudah siap menjadwalkan laporan rutin, jelaskan bahwa itu perlu **komputer
menyala terus** ("Cron runs inside the Gateway process; it does not fire if the Gateway is not
running continuously" — dari FAQ resmi OpenClaw), dan arahkan ke skill `laporan-otomatis-terjadwal`
(dan `buku-stok` untuk catatan stok) yang sudah menangani penjadwalan lengkap. Kalau ingin contoh
cepat sebelum memakai skill itu, ini bentuk perintahnya (dijalankan **hanya dengan persetujuan**):

```bash
openclaw automations add "0 7 * * 1" \
  "Jalankan rekap-penjualan-csv untuk minggu lalu dari folder laporan/masuk. Tulis ringkas, Bahasa Indonesia." \
  --name "Laporan penjualan Senin" --tz "Asia/Jakarta" --session isolated \
  --announce --channel telegram --to "<ID chat pemilik>"
```
(`openclaw automations add` = alias `openclaw cron add`, terverifikasi lewat `openclaw automations create --help`.)
**Kanal default = Telegram** (bot resmi, tidak berisiko blokir). WhatsApp OpenClaw memakai
WhatsApp Web (tidak resmi) — kalau pengguna tetap ingin notifikasi lewat WA, lihat §7 di bawah.

**Sebelum menyarankan mengetatkan `tools.exec.mode` ke `ask`** (mis. lewat `cek-privasi-openclaw`):
ingatkan bahwa automation/cron yang berjalan tanpa ada klien approval (Control UI/app) yang
terhubung akan **ditolak otomatis**, bukan menunggu — ini bisa mematikan laporan otomatis yang
baru saja disiapkan. Jangan campur adukkan langkah pengetatan privasi dengan setup otomasi dalam
percakapan yang sama tanpa menjelaskan efek ini.

## 6. Privasi

Setelah paket pertama terpasang, tawarkan menjalankan skill `cek-privasi-openclaw` untuk
memeriksa pengaturan keamanan dasar — terutama bagi pengguna yang menandai "khawatir privasi"
saat wawancara.

## 7. Aturan pemilik untuk jalur "Solusi Member VIP" (WAJIB diikuti)

Sesuai keputusan pemilik di `CLAUDE.md` §1 ("Keputusan pemilik untuk jalur 3"):
- **Kanal default = Telegram** untuk laporan & notifikasi ke pemilik usaha.
- **WhatsApp OpenClaw** (berbasis WhatsApp Web, tidak resmi) hanya boleh dipakai dengan **nomor
  terpisah** untuk notifikasi ke pemilik sendiri, dan **hanya setelah pengguna menyetujui
  risikonya secara tertulis** (nomor bisa diblokir). Jangan menyarankan WA sebagai kanal utama
  tanpa peringatan ini.
- **Tidak ada broadcast/kirim massal** lewat OpenClaw dalam bentuk apa pun (skill `broadcast-wa`
  menyiapkan pesan untuk dikirim manual/lewat kanal resmi, bukan mengirim otomatis).
- **Agen CS di WhatsApp selalu mode Copilot**: AI menyiapkan draf balasan, **manusia yang
  mengirim**. Jangan menyarankan/memasang auto-reply langsung ke pelanggan di WA.
- **Kripto** (bila relevan dari jawaban wawancara): hanya riset, ringkasan berita, jurnal
  trading, dan notifikasi harga yang ambangnya diatur pengguna sendiri. **Tanpa** auto-trading,
  **tanpa** rekomendasi beli/jual.
- **Kesehatan**: hanya edukasi pasien umum, balasan chat non-diagnosis (mode Copilot), dan
  laporan operasional klinik tanpa identitas pasien. **Tanpa** skrining/diagnosis/kalkulator medis.
- **Tidak ada** scraping/menarik data marketplace lewat otomasi login browser (mis. untuk resi
  Shopee) — arahkan ke ekspor CSV manual dari marketplace, atau jasa setup resmi bila tersedia.
- **Tidak ada** clone wajah/suara tanpa izin tertulis pemilik wajah/suara, dan **tidak** menjanjikan
  posting otomatis ke media sosial yang sebenarnya tidak didukung OpenClaw.
