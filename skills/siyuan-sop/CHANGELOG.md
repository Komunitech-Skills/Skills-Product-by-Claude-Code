# Riwayat perubahan — siyuan-sop

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Riwayat versi
- **1.0.11 (2026-10-13)** — rujukan ke catatan riset internal kurator dan ke panduan yang tidak ikut paket diganti kalimat yang berdiri sendiri atau `references/panduan-siyuan.md` (SKILL.md, references/panduan-siyuan.md, references/api-endpoints.md); cara kerja tidak berubah.
- **1.0.10 (2026-10-02)** — dari uji regresi OpenClaw v1.0.9 (temuan rendah): cadangan isi lama saat menimpa dokumen kini disimpan di folder data Anda `~/KomunitechData/siyuan/cadangan/` (di luar folder skill, konsisten dengan skill Komunitech lain) sehingga tidak ikut terhapus saat skill diperbarui; sebelumnya bisa tersimpan di dalam folder skill. Script mencetak path lengkap berkas cadangan dan pratinjau timpa menyebut foldernya. Folder bisa diubah dengan `--cadangan-dir` atau ENV `KOMUNITECH_SIYUAN_CADANGAN`/`KOMUNITECH_DATA`. Tes unit ditambah (52 tes).

---
Komunitech tidak berafiliasi dengan proyek SiYuan/b3log; SiYuan adalah merek milik pemiliknya.
