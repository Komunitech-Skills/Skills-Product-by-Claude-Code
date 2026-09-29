# Luncurkan Produk Baru: Rencana Bertanggal dari T-30 sampai T+30

**Dari "mau launching" ke jadwal, teks, dan hitungan stok yang siap dijalankan.**

## Manfaat
- Jadwal bertanggal otomatis dari tanggal peluncuran, sudah menghindari hari libur nasional 2026-2027 untuk urusan pemasok/kemasan/izin.
- Alur lengkap: teaser, daftar tunggu WA/Google Form, soft launch, launching resmi, pasca-peluncuran.
- Checklist kanal (IG, TikTok, marketplace, grup WA, bazar, KOL mikro) dan runbook hari-H per jam.
- Stok dan margin promo dihitung dengan rumus, bukan dikira.
- Pengingat halal/BPOM/PIRT/label dengan tautan situs resmi.

## Cocok untuk
- Pemilik usaha makanan/minuman, fashion, kriya, kosmetik, dan jasa yang akan merilis produk baru.
- Admin/marketing UMKM yang butuh rencana rapi tanpa tim besar.
- Penjual marketplace yang mau menambah varian besar.
Tidak cocok: peluncuran aplikasi/startup teknologi, atau kebutuhan nasihat hukum.

## Contoh sebelum & sesudah
**Sebelum:** "Aku mau launching sambal botol, bingung mulai dari mana. Posting dulu? Kapan pesan botol? Takut stok kurang."

**Sesudah (cukup ketik):** "Bantu rencana peluncuran sambal botol 180 g, tanggal 14 November, stok 150, kontak WA 120, IG 800, anggaran promo 500 ribu."
-> asumsi, 42 tugas bertanggal (mulai 15 Okt; pesan kemasan dan cek label sebelum akhir pekan), pesan WA/IG siap tempel, stok awal dihitung, Go/No-Go H-1, dan pengingat halal/BPOM. Lihat `examples/`.

## Cara pakai
Ketik permintaan biasa, misalnya:
- "Buatkan jadwal launching produk baruku tanggal 5 Desember."
- "Aku mau pre-order dulu sebelum launching, gimana caranya?"
- "Cek rencana launching ini, apa yang kurang?"
Script jadwal (opsional): `python3 scripts/jadwal_peluncuran.py --tanggal 2026-11-14 --produk "Nama" --jenis pangan` (Windows: `python` atau `py`). Tanpa script pun skill tetap menyusun jadwal manual.

## Instalasi singkat
Salin folder `luncurkan-produk-baru` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket (`docs/instalasi.md`).

## Skill pelengkap
`hitung-hpp`, `harga-jual-marketplace` (harga & margin), `caption-sosmed-umkm`, `kalender-konten-30hari`, `listing-marketplace`, `naskah-live-jualan`, `laporan-iklan-mingguan`, `kpi-tim`, `promo-kalender`.

## FAQ
**Apakah bisa dipakai kalau tanggal launching kurang dari 30 hari?**
Bisa. Tugas yang sudah lewat ditandai dan skill menyarankan cara memadatkan jadwal.

**Apakah skill ini memastikan produk saya legal/halal?**
Tidak. Ia hanya mengingatkan hal yang perlu dicek dan menautkan situs resmi (oss.go.id, halal.go.id, cekbpom.pom.go.id). Keputusan ada di instansi berwenang.

**Apakah daftar libur selalu benar?**
Berasal dari SKB 3 Menteri 2026 dan 2027 (data 2027 perlu ditinjau ulang terhadap lampiran resmi). Pemerintah dapat mengubahnya; cocokkan dengan pengumuman terbaru atau tambahkan lewat `--libur-tambahan`.

Kredit sumber terbuka dan lisensi: lihat `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.
