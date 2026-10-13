# Riwayat perubahan — harga-jual-marketplace

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.6 (2026-10-13)
- Koreksi tanggal PPh 22 marketplace: bukan "berlaku 1 Agustus 2026" melainkan **dipungut sejak 1 Oktober 2026** oleh Shopee, Tokopedia, Lazada, Blibli (Siaran Pers DJP SP-23/2026, 1 Okt 2026; rencana 1 Agustus 2026 ditunda lewat PENG-46/PJ.09/2026, lalu penunjukan ulang 24 Sep 2026). Diperbarui di catatan script, SKILL.md, README, `references/regulasi.md`, dan tes. `TANGGAL_ATURAN` → 2026-10-13.
- `references/regulasi.md`: judul lengkap & tanggal PMK 37/2025, riwayat jadwal, sumber resmi DJP. Dasar pungutan setelah voucher toko ditandai PERLU REVIEW (definisi peredaran bruto PMK 37/2025 disebut "sebelum dikurangi potongan penjualan").
- Contoh di `examples/` adalah rekaman uji 2026-09-23/10-01 dan sengaja tidak diubah (masih memuat tanggal lama).

## Catatan revisi 1.0.3 (2026-10-01)
- AI wajib menyalin blok "Catatan & asumsi" dari script **kata per kata** ke balasan: dasar aturan PPh 22 marketplace (PMK 37/2025, berlaku 1 Agustus 2026), syarat pengecualian omzet ≤ Rp500 juta, tanggal berlaku, dan disclaimer (temuan uji OpenClaw: sempat diringkas jadi "per PMK terbaru").
- Perbaikan: `harga_marketplace.py --help` sebelumnya error; kini tampil normal.
- Instruksi: script dijalankan dari subfolder `scripts/` di folder skill. 3 tes otomatis baru (`tests/`).

## Catatan revisi 1.0.5 (2026-10-01)

- Catatan PPh 22 di keluaran script tidak lagi menampilkan teks perintah (`--pph22 tidak`) yang ikut tersalin ke chat member; kini berbunyi "bila sudah, minta hitung ulang tanpa PPh 22". Temuan uji ulang OpenClaw putaran 2.

## Catatan revisi 1.0.4 (2026-10-01)
- Script kini mencetak **status target** ("MEMENUHI target …" / "DI BAWAH target … laba kurang Rp …") pada harga rekomendasi dan pada mode cek harga bila target disebut (`--harga-jual 62.900 --target-margin 25`).
- Opsi baru `--banding-harga "62.900;59.900"`: cek beberapa harga lain (mis. harga psikologis) sekaligus terhadap target, lengkap dengan laba, margin, dan status. AI wajib mengutip status ini, tidak menilai sendiri (temuan uji ulang OpenClaw: Rp62.900 disebut "di bawah target" padahal margin 25,1% ≥ 25%).
- 4 tes otomatis baru (`tests/`), semua lulus.
