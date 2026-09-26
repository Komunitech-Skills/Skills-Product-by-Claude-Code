# Catatan pembuat: siyuan-sop v1.0.0 (2026-09-26)

- **Penulis:** pembuat skill (Claude Code, agent pembuat). Ini **bukan** uji independen dan tidak
  memberi skor kualitas. Status katalog: `draft`, menunggu Tahap 6 (uji independen, uji A/B, uji
  banding pesaing, uji platform asli, beta) sebelum bisa `lulus`.
- **Lingkungan:** Linux, Python 3.11. Dua jenis pengujian dijalankan:
  1. **42 uji otomatis** (`tests/test_siyuan.py`) dengan server kernel SiYuan **tiruan**
     (`http.server` standar di thread terpisah, bentuk respons meniru API resmi).
  2. **Uji integrasi NYATA** dengan **kernel SiYuan resmi v3.8.5** (biner Linux resmi diunduh dari
     GitHub Releases, dijalankan headless `SiYuan-Kernel serve` di sandbox terisolasi, tanpa
     internet keluar). Rincian unduhan, checksum, dan hasil lengkap ada di
     `research/sources/siyuan-2026-09-26.md` §D.

## Cakupan uji integrasi nyata
Semua 8 perintah dijalankan sungguhan terhadap kernel resmi: `cek`, `daftar-buku`, `cari`, `baca`
(by id & by path), `buat` (baru, pratinjau, tolak-timpa, timpa+ya, dari stdin, judul/isi emoji &
Unicode), `tambah`, `lama`, `ekspor-basis`. Tiga skenario bisnis penuh (toko hijab, klinik gigi,
kantor konsultan - lihat `examples/01`-`03`) dijalankan end-to-end dari nol.

## Temuan nyata yang mengubah kode/dokumentasi (bukan cuma dugaan)
1. **Dokumen induk otomatis kosong** saat path bertingkat dibuat pertama kali (mis. `/FAQ/Jam Buka`
   membuat `/FAQ` kosong). `ekspor-basis` awalnya ikut menyertakannya sebagai noise - **diperbaiki**
   (fungsi `_kosong()` di `scripts/siyuan.py`, ditambah uji `test_42`) dan diverifikasi ulang
   terhadap kernel yang sama sampai benar.
2. **Judul dobel** bila isi Markdown yang dikirim ke `buat` diawali baris `# <Judul yang sama>` -
   SiYuan sudah otomatis menambahkan judul dokumen sebagai heading. **Diperbaiki** di
   `references/template-sop-faq.md` (baris judul dihapus dari template) dan dicatat di `SKILL.md`
   §Langkah D & §Batasan.
3. **Jeda pengindeksan pencarian** (~1-2 detik) antara dokumen dibuat dan bisa ditemukan lewat
   `cari` - dicatat sebagai batasan di `SKILL.md`, bukan bug script (perilaku kernel SiYuan sendiri).
4. **Temuan keamanan penting** (di luar dugaan awal): permintaan ke endpoint `/api/...` **tanpa**
   header `Authorization` sama sekali berhasil diproses kernel (termasuk yang menulis), berbeda dari
   token yang salah (ditolak). Mengatur `accessAuthCode` tidak mengubah ini untuk permintaan tanpa
   header `Origin`; permintaan dengan `Origin` asing barulah ditolak. Dituliskan lengkap di
   `research/sources/siyuan-2026-09-26.md` §D6 dan diteruskan ke pembeli lewat
   `docs/panduan-siyuan.md` §3.5 (pembatas keamanan sesungguhnya = kernel hanya boleh dijangkau dari
   komputer sendiri, bukan hanya token). Skill sendiri **selalu** mengirim token yang benar di
   setiap permintaan sebagai disiplin baku, terlepas dari temuan ini.
5. Field API SQL bernama **`stmt`**, bukan `sql` - dikoreksi setelah membaca `docs/API.md` mentah
   (beberapa ringkasan pihak ketiga yang dibaca saat riset awal keliru menyebut `sql`).

## Yang BELUM diuji (jujur)
- Aplikasi desktop SiYuan (Electron) sungguhan di Windows/macOS - baru kernel headless Linux.
- Gateway OpenClaw sungguhan untuk jadwal otomatis (`references/openclaw-jadwal.md`); pengiriman ke
  Telegram juga belum diuji (butuh token bot asli).
- Workspace SiYuan berisi ribuan dokumen (uji hanya dengan beberapa dokumen contoh) - performa
  `cari`/`lama` pada workspace besar belum diverifikasi.
- Notebook terenkripsi atau notebook yang sedang `closed` saat dibaca (hanya `buat`/`tambah` yang
  otomatis mencoba `openNotebook`).

## Uji muat OpenClaw (mekanis, bukan agent)
`scripts/uji_openclaw.sh` dijalankan dari root repo mencakup skill ini bersama semua skill lain -
hasil dicatat di laporan sesi, bukan diulang di sini.
