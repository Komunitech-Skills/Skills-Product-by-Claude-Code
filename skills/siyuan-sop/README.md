# SiYuan SOP: Basis Pengetahuan Usaha Tanpa Langganan

**Simpan SOP, notulen, dan FAQ toko di komputer sendiri lewat SiYuan (gratis, seperti Notion tapi lokal) - lalu tinggal minta AI mencarikan, membacakan, atau menambahkannya. Tidak ada biaya bulanan, data tidak wajib naik ke server siapa pun.**

*Diuji AI penguji independen: 4,3 → 9,0 dari 10 (tanpa skill, agent memakai kunci akses yang ditempel di chat dan menimpa dokumen tanpa pratinjau; dengan skill ada pratinjau dan cadangan isi lama).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **"Cari SOP retur" langsung ketemu.** AI mencari lewat isi seluruh SOP/FAQ/notulen di SiYuan, bukan menebak-nebak dari ingatan model. Diuji dengan data contoh dan server SiYuan tiruan (bukan aplikasi SiYuan sungguhan); lihat Hasil uji.
- ✅ **Simpan hasil skill pembuat SOP (`sop-writer`) atau skill notulen rapat (`notulen-rapat`) sekali perintah.** Tidak perlu buka aplikasi, cari folder, klik-klik - tinggal minta "simpan ini ke SiYuan".
- ✅ **Basis pengetahuan CS (layanan pelanggan) yang benar-benar dipakai.** Ekspor satu perintah menggabungkan semua FAQ jadi satu file yang bisa langsung dipakai skill agen CS toko (`agen-cs-toko`) atau skill balas chat CS (`balas-chat-cs`), jadi balasan AI berdasar data toko Anda, bukan karangan (info yang belum ada di sana ditandai untuk Anda lengkapi).
- ✅ **Audit SOP basi.** "SOP mana yang belum diupdate 3 bulan?" dijawab dalam sekejap; bisa dijadwalkan mingguan ke Telegram (diuji di bot Telegram uji 2026-10-13, one-shot `lama --hari 90`).
- ✅ **Dirancang hati-hati untuk data usaha.** Menambah dokumen baru/isi baru lewat pratinjau + persetujuan; menimpa dokumen lama hanya dengan konfirmasi eksplisit dan cadangan isi lama; kunci akses (token) disimpan di komputer Anda dan tidak ditampilkan.

## Cocok untuk siapa
- Pemilik toko online, klinik, atau kantor kecil yang selama ini menyimpan SOP di kepala, grup WA, atau dokumen Word yang berserakan.
- Yang ingin pengganti Notion **tanpa langganan bulanan** dan data tetap di komputer sendiri.
- Pengguna skill agen CS toko, balas chat CS, pembuat SOP, atau notulen rapat Komunitech yang ingin hasilnya tersimpan rapi dan bisa dicari, bukan hilang di riwayat chat.

**Kurang cocok:** belum siap memasang aplikasi tambahan (SiYuan) - kalau hanya butuh SOP sekali jadi tanpa penyimpanan, cukup pakai skill pembuat SOP (`sop-writer`) atau skill notulen rapat (`notulen-rapat`) saja. Butuh berbagi basis pengetahuan ke banyak orang lewat internet (di luar cakupan; SiYuan dipakai lokal, bukan server publik).

## Contoh sebelum & sesudah
**Sebelum:** SOP tersebar di grup WA, Google Docs beberapa akun, dan ingatan pemilik. Karyawan baru bertanya berulang; tidak ada yang tahu SOP mana yang terbaru.

**Sesudah:** ketik *"cari SOP jam buka"*:
```
HASIL PENCARIAN 'jam buka' (1 dokumen)
- Jam Buka 🕐  [/FAQ/Jam Buka 🕐]
    ...Toko buka jam 09.00-21.00 setiap hari, termasuk Minggu...
```
(Contoh nyata dari uji dengan mesin inti SiYuan resmi v3.8.5 versi Linux.)

## Cara pakai
Setelah SiYuan terpasang & tersambung, cukup ketik permintaan biasa:
- "Simpan SOP packing pesanan ini ke SiYuan"
- "Cari di basis pengetahuan soal kebijakan retur"
- "Tampilkan SOP closing kasir"
- "Tambahkan poin baru ke SOP itu"
- "SOP mana yang sudah lama tidak diupdate?"
- "Gabungkan semua FAQ toko jadi satu file untuk agen CS"

## Instalasi singkat
1. **Pasang SiYuan** (gratis) dan amankan sesuai `references/panduan-siyuan.md` di paket - **wajib** dibaca sebelum dipakai (matikan "network serving", set kata sandi kunci layar, ambil token API). ±10 menit.
2. Salin folder `siyuan-sop` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

3. Simpan kunci akses (token API) sekali (di terminal Anda sendiri, bukan di chat): `python3 ~/.openclaw/skills/siyuan-sop/scripts/siyuan.py simpan-kunci` (Windows: `python`/`py`).

Panduan pemasangan skill lengkap: `CARA-INSTAL.md` di paket. Butuh **Python 3.8+** (gratis di python.org). Tidak butuh internet setelah SiYuan terpasang, tidak butuh akun, tidak butuh paket tambahan.

**Hasil uji (angka nyata):**
- **Uji OpenClaw, v1.0.8, 2 Oktober 2026** (penguji AI independen; angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 4,3 tanpa skill menjadi 9,0 dengan skill (skala 10), pada tiga skenario (belum punya SiYuan dan minta SOP buka-tutup kafe; kunci akses ditempel di chat; menimpa dokumen lama). Tanpa skill, agent memakai kunci akses yang ditempel di chat dan menimpa dokumen tanpa pratinjau atau cadangan; dengan skill, ada pratinjau, cadangan isi lama, dan kunci itu tidak dipakai. Uji ulang v1.0.10 (menimpa SOP): 2 menjadi 9,5. Uji ini memakai data contoh dan server SiYuan tiruan di komputer uji, bukan aplikasi SiYuan sungguhan.
- **Uji oleh pembuat (v1.0.0):** semua perintah dicoba dengan mesin inti (kernel) SiYuan resmi v3.8.5 versi Linux, dijalankan tanpa tampilan layar (headless), termasuk judul/isi berisi emoji dan Unicode, plus 42 uji otomatis dengan server tiruan (kini 52 tes).

**Status uji (jujur):** diuji di OpenClaw (uji otomatis agent); jadwal otomatis Telegram (command-argv `lama`) diuji di bot Telegram uji 2026-10-13 (`examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`, mock SiYuan lokal). **Belum** diuji di aplikasi desktop SiYuan sungguhan di Windows/macOS, belum diuji penguji independen terhadap SiYuan asli di komputer pembeli, dan Claude Code, Codex, serta Cursor belum diuji langsung (format skill-nya sama).

## FAQ
**Apakah data SOP/FAQ saya dikirim ke internet?**
Tidak oleh skill ini. Skrip hanya berbicara dengan SiYuan di komputer Anda sendiri (alamat `127.0.0.1`) dan menolak alamat lain kecuali Anda menegaskannya secara eksplisit. SiYuan sendiri tidak mengirim data ke cloud kecuali Anda mengaktifkan fitur sinkronisasinya sendiri (defaultnya mati). Isi percakapan Anda dengan AI tetap diproses layanan AI yang Anda pakai, seperti biasa.

**Bisakah AI menghapus atau menimpa SOP saya tanpa sengaja?**
Skill dirancang agar tidak: membuat dokumen baru di lokasi yang sudah terisi akan **ditolak** kecuali Anda memberi izin eksplisit dan menjawab "ya" (isi lama dicadangkan dulu), dan perintah menambah isi tidak menghapus isi lama. Jaga juga izin kunci akses SiYuan Anda seperlunya.

**Apakah SiYuan aman?**
SiYuan software sumber terbuka yang cukup populer dan aktif dikembangkan. Komunitech memeriksa celah keamanan yang diketahui sebelum merilis skill ini; risikonya bisa ditekan **selama** Anda mengikuti panduan keamanan di `references/panduan-siyuan.md` (jangan buka ke internet, jangan pasang plugin pihak ketiga, jangan aktifkan fitur "Publish"). Tidak ada software yang bebas risiko sepenuhnya.

## Riwayat perubahan

Versi terkini: **1.0.11**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
