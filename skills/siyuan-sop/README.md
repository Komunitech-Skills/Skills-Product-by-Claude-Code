# SiYuan SOP: Basis Pengetahuan Usaha Tanpa Langganan

**Simpan SOP, notulen, dan FAQ toko di komputer sendiri lewat SiYuan (gratis, seperti Notion tapi lokal) - lalu tinggal minta AI mencarikan, membacakan, atau menambahkannya. Tidak ada biaya bulanan, data tidak wajib naik ke server siapa pun.**

## Manfaat
- ✅ **"Cari SOP retur" langsung ketemu.** AI mencari lewat isi seluruh SOP/FAQ/notulen di SiYuan, bukan menebak-nebak dari ingatan model.
- ✅ **Simpan hasil `sop-writer`/`notulen-rapat` sekali perintah.** Tidak perlu buka aplikasi, cari folder, klik-klik - tinggal minta "simpan ini ke SiYuan".
- ✅ **Basis pengetahuan CS yang benar-benar dipakai.** Ekspor satu perintah menggabungkan semua FAQ jadi satu file yang bisa langsung dipakai skill `agen-cs-toko`/`balas-chat-cs`, jadi balasan AI selalu berdasar data toko, bukan karangan.
- ✅ **Audit SOP basi otomatis.** "SOP mana yang belum diupdate 3 bulan?" dijawab dalam sekejap, bisa dijadwalkan mingguan ke Telegram.
- ✅ **Aman untuk data usaha.** Menambah dokumen baru/isi baru selalu lewat pratinjau + persetujuan; tidak pernah menimpa dokumen lama tanpa konfirmasi eksplisit; token disimpan aman dan tidak pernah ditampilkan.

## Cocok untuk siapa
- Pemilik toko online, klinik, atau kantor kecil yang selama ini menyimpan SOP di kepala, grup WA, atau dokumen Word yang berserakan.
- Yang ingin pengganti Notion **tanpa langganan bulanan** dan data tetap di komputer sendiri.
- Pengguna `agen-cs-toko`/`balas-chat-cs`/`sop-writer`/`notulen-rapat` yang ingin hasilnya tersimpan rapi dan bisa dicari, bukan hilang di riwayat chat.

**Kurang cocok:** belum siap memasang aplikasi tambahan (SiYuan) - kalau hanya butuh SOP sekali jadi tanpa penyimpanan, cukup pakai `sop-writer`/`notulen-rapat` saja. Butuh berbagi basis pengetahuan ke banyak orang lewat internet (di luar cakupan; SiYuan dipakai lokal, bukan server publik).

## Contoh sebelum & sesudah
**Sebelum:** SOP tersebar di grup WA, Google Docs beberapa akun, dan ingatan pemilik. Karyawan baru bertanya berulang; tidak ada yang tahu SOP mana yang terbaru.

**Sesudah:** ketik *"cari SOP jam buka"*:
```
HASIL PENCARIAN 'jam buka' (1 dokumen)
- Jam Buka 🕐  [/FAQ/Jam Buka 🕐]
    ...Toko buka jam 09.00-21.00 setiap hari, termasuk Minggu...
```
(Contoh nyata dari uji dengan kernel SiYuan resmi v3.8.5.)

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.8, 2026-10-02):** rata-rata nilai 4,3 tanpa skill menjadi 9,0 dengan skill (skala 10), pada tiga skenario (belum punya SiYuan dan minta SOP buka-tutup kafe; token ditempel di chat; menimpa dokumen lama). Tanpa skill, agent memakai token yang ditempel di chat dan menimpa dokumen tanpa pratinjau atau cadangan; dengan skill, ada pratinjau, cadangan isi lama, dan token tidak dipakai. Uji regresi v1.0.10 (menimpa SOP): 2 menjadi 9,5. Jujur: uji ini memakai data contoh dan server SiYuan tiruan di komputer uji, bukan aplikasi SiYuan sungguhan. Rincian: `examples/00-openclaw-sebelum-sesudah.md`.

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

3. Simpan token API sekali (di terminal Anda sendiri, bukan di chat): `python3 ~/.openclaw/skills/siyuan-sop/scripts/siyuan.py simpan-kunci` (Windows: `python`/`py`).

Panduan pemasangan skill lengkap: `CARA-INSTAL.md` di paket. Butuh **Python 3.8+** (gratis di python.org). Tidak butuh internet setelah SiYuan terpasang, tidak butuh akun, tidak butuh paket tambahan.

**Status uji jujur:** pada versi 1.0.0 pembuat menguji semua perintah dengan **kernel SiYuan resmi v3.8.5** (biner Linux resmi, dijalankan headless), termasuk judul/isi berisi emoji dan Unicode, plus 42 uji otomatis dengan server tiruan (kini 52 tes). Sejak itu penguji independen dan agent OpenClaw menguji dengan data contoh dan server SiYuan tiruan (lihat Hasil uji di atas). **Belum** diuji di aplikasi desktop SiYuan (Electron) sungguhan di Windows/macOS, belum diuji penguji independen terhadap kernel SiYuan asli, dan belum diuji di Gateway OpenClaw sungguhan untuk jadwal otomatis.

## FAQ
**Apakah data SOP/FAQ saya dikirim ke internet?**
Tidak oleh skill ini. Script hanya berbicara dengan SiYuan di komputer Anda (`127.0.0.1`) dan menolak alamat lain kecuali Anda menegaskannya secara eksplisit. SiYuan sendiri tidak mengirim data ke cloud kecuali Anda mengaktifkan fitur sinkronisasinya sendiri (defaultnya mati).

**Bisakah AI menghapus atau menimpa SOP saya tanpa sengaja?**
Tidak: membuat dokumen baru di path yang sudah terisi akan **ditolak** kecuali Anda memberi izin eksplisit (`--timpa` + konfirmasi "ya"), dan menambah isi (`tambah`) tidak pernah menghapus isi lama.

**Apakah SiYuan aman?**
SiYuan software sumber terbuka yang cukup populer dan aktif dikembangkan. Komunitech mengaudit celah keamanan yang diketahui sebelum merilis skill ini (lihat `research/sources/siyuan-2026-09-26.md`) - kesimpulannya aman dipakai **selama** mengikuti panduan keamanan di `references/panduan-siyuan.md` (jangan buka ke internet, jangan pasang plugin pihak ketiga, jangan aktifkan fitur "Publish").

## Riwayat versi
- **1.0.10 (2026-10-02)** — dari uji regresi OpenClaw v1.0.9 (temuan rendah): cadangan isi lama saat menimpa dokumen kini disimpan di folder data Anda `~/KomunitechData/siyuan/cadangan/` (di luar folder skill, konsisten dengan skill Komunitech lain) sehingga tidak ikut terhapus saat skill diperbarui; sebelumnya bisa tersimpan di dalam folder skill. Script mencetak path lengkap berkas cadangan dan pratinjau timpa menyebut foldernya. Folder bisa diubah dengan `--cadangan-dir` atau ENV `KOMUNITECH_SIYUAN_CADANGAN`/`KOMUNITECH_DATA`. Tes unit ditambah (52 tes).

---
Komunitech tidak berafiliasi dengan proyek SiYuan/b3log; SiYuan adalah merek milik pemiliknya.
