# Luncurkan Produk Baru: Rencana T-30 sampai T+30

**Dari "mau launching" ke jadwal, teks, dan hitungan stok yang siap dijalankan.**

## Manfaat
- Jadwal bertanggal otomatis dari tanggal peluncuran, sudah menghindari hari libur nasional 2026-2027 untuk urusan pemasok/kemasan/izin.
- Alur lengkap: teaser, daftar tunggu WA/Google Form, soft launch, launching resmi, pasca-peluncuran.
- Checklist kanal (IG, TikTok, marketplace, grup WA, bazar, KOL mikro) dan runbook hari-H per jam.
- Stok dan margin promo dihitung dengan rumus, bukan dikira.
- Pengingat halal/BPOM/PIRT/label dengan tautan situs resmi.

## Cocok untuk siapa
- Pemilik usaha makanan/minuman, fashion, kriya, kosmetik, dan jasa yang akan merilis produk baru.
- Admin/marketing UMKM yang butuh rencana rapi tanpa tim besar.
- Penjual marketplace yang mau menambah varian besar.
Tidak cocok: peluncuran aplikasi/startup teknologi, atau kebutuhan nasihat hukum.

## Contoh sebelum & sesudah
**Sebelum:** "Aku mau launching sambal botol, bingung mulai dari mana. Posting dulu? Kapan pesan botol? Takut stok kurang."

**Sesudah (cukup ketik):** "Bantu rencana peluncuran sambal botol 180 g, tanggal 14 November, stok 150, kontak WA 120, IG 800, anggaran promo 500 ribu."
-> asumsi, 43 tugas bertanggal (mulai 15 Okt; pesan kemasan dan cek label sebelum akhir pekan), pesan WA/IG siap tempel, stok awal dihitung, Go/No-Go H-1, dan pengingat halal/BPOM. Lihat `examples/`.

**Hasil uji (OpenClaw, uji otomatis agent, v1.0.4):** rata-rata nilai 5,5 tanpa skill menjadi 9,0 dengan skill (skala 10). Pada rencana launching kosmetik pencerah yang izin BPOM-nya belum terbit (kandidat peluncuran 12 Oktober 2026), AI tanpa skill menolak dua klaim terlarang tetapi masih menjadwalkan pre-order 10 Oktober; dengan skill penjualan, pre-order, dan promo ditunda sampai izin terbit, hanya daftar tunggu tanpa uang yang dibuka, dan Go/No-Go otomatis No-Go. Pada rencana nastar 20 November, stok awal dihitung rumus: (40 + 20) x 1,3 = 78 toples. Rincian: `examples/00-openclaw-sebelum-sesudah.md`. Hasil di bot Telegram ada di bagian "Bukti uji di bot Telegram" di bawah. Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

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

## Catatan revisi (v1.0.5, 2026-10-05)
Pra-cek konteks Telegram: untuk "launching serum, izin BPOM masih proses" bot hanya membalas 5 pertanyaan. Perbaikan: aturan "kerjakan dulu, tanya di akhir" (peringatan izin edar + dasar aturan + rencana dengan asumsi default + maks. 1-3 pertanyaan di balasan yang sama); dasar aturan kosmetik ditambahkan di `references/legalitas-label.md`; contoh baru `examples/06-kosmetik-izin-proses-kerjakan-dulu.md`. Menunggu uji ulang independen.

## Skill pelengkap
`hitung-hpp`, `harga-jual-marketplace` (harga & margin), `caption-sosmed-umkm`, `kalender-konten-30hari`, `listing-marketplace`, `naskah-live-jualan`, `laporan-iklan-mingguan`, `kpi-tim`, `promo-kalender`.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji Komunitech, tautan hanya terbuka untuk anggota grup): gelombang 8, 2026-10-05.
- Tanpa skill: https://t.me/c/4407409583/782/792 — skor 5,5
- Dengan skill: https://t.me/c/4407409583/783/794 — skor 8,5
Verdik gelombang: LULUS — DENGAN menutup semua jalur jual sebelum notifikasi BPOM terbit (termasuk pre-order/DP), mengutip dasar aturan, menggeser hari jual ke T0 bertanggal (11 Nov 2026) dan menjadikan 12 Okt hari teaser/daftar tunggu tanpa uang; TANPA justru menyarankan "pre-order Shopee tanpa klaim BPOM", harga promo untuk pendaftar, dan testimoni before/after.

## FAQ
**Apakah bisa dipakai kalau tanggal launching kurang dari 30 hari?**
Bisa. Tugas yang sudah lewat ditandai dan skill menyarankan cara memadatkan jadwal.

**Apakah skill ini memastikan produk saya legal/halal?**
Tidak. Ia hanya mengingatkan hal yang perlu dicek dan menautkan situs resmi (oss.go.id, halal.go.id, cekbpom.pom.go.id). Keputusan ada di instansi berwenang.

**Apakah daftar libur selalu benar?**
Berasal dari SKB 3 Menteri 2026 dan 2027 (sudah dicocokkan dengan lampiran resmi per 2026-09-29). Pemerintah dapat mengubahnya; cocokkan dengan pengumuman terbaru atau tambahkan lewat `--libur-tambahan`.

Kredit sumber terbuka dan lisensi: lihat `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.
