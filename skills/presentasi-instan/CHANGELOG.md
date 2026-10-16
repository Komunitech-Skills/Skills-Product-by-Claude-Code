# Riwayat perubahan — presentasi-instan

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.1.6 (2026-10-16)
- Dari uji bot Telegram asli (gelombang 19): deck HTML 13 slide berisi bagus, tetapi file tidak ikut terkirim ke chat (balasan hanya menyebut nama file di komputer bot). Kini di kanal chat file `.html` WAJIB dilampirkan sebagai dokumen setelah lolos validator; bila kanal tidak bisa kirim file, tidak ada jalur/folder disebut, isi diringkas per slide dan hanya ditawarkan "balas 'kirim file'" (mengikuti `ekstrak-nota-faktur`).
- Balasan memakai bahasa awam: baris "Hasil cek otomatis: LULUS" diganti "Sudah dicek: ..." (file bisa dibuka tanpa internet dan siap dicetak jadi PDF; bila ada peringatan, sebutkan apa yang perlu diperbaiki).
- Larangan menyebut nama skill/alat internal ke pengguna (mis. "skill laporan keuangan", `pengajuan-kur`); cukup sebut hasilnya. Tambah butir checklist akhir untuk kanal chat dan bahasa awam.

## Catatan revisi 1.1.5 (2026-10-01)
- Dari uji OpenClaw sebelum/sesudah: AI sempat menulis klaim di slide yang tidak pernah diberikan pengguna ("pelanggan bertambah tiap tahun", "selesai 1–2 hari"). Kini klaim kinerja/kecepatan/tren hanya dari fakta pengguna; selain itu ditandai `[isi: ...]` untuk dilengkapi.
