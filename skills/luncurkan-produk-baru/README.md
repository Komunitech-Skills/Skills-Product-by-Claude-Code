# Luncurkan Produk Baru: Rencana T-30 sampai T+30

**Dari "mau launching" ke jadwal, teks, dan hitungan stok yang siap dijalankan.**

Diuji AI penguji independen di bot Telegram asli: 5,5 → 8,5 dari 10 (pembedanya untuk produk yang izin BPOM-nya belum terbit: tanpa skill, AI masih menyarankan pre-order dan harga promo; dengan skill semua jalur jual ditutup sampai izin terbit dan jadwal digeser).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- Jadwal bertanggal otomatis dari tanggal peluncuran (T-30 = 30 hari sebelum hari peluncuran, T+30 = 30 hari sesudahnya), sudah menghindari hari libur nasional 2026-2027 untuk urusan pemasok/kemasan/izin.
- Alur lengkap: teaser (cuplikan pancingan), daftar tunggu WA/Google Form, soft launch (peluncuran terbatas untuk uji), launching resmi, pasca-peluncuran.
- Checklist kanal (IG, TikTok, marketplace, grup WA, bazar, KOL mikro, yaitu kreator/influencer kecil) dan runbook hari-H (panduan kerja per jam di hari peluncuran).
- Stok dan margin promo dihitung dengan rumus, bukan dikira.
- Pengingat izin halal, BPOM/PIRT (izin edar), dan label dengan tautan situs resmi (pengingat, bukan jaminan izin).

## Cocok untuk siapa
- Pemilik usaha makanan/minuman, fashion, kriya, kosmetik, dan jasa yang akan merilis produk baru.
- Admin/marketing UMKM yang butuh rencana rapi tanpa tim besar.
- Penjual marketplace yang mau menambah varian besar.
Tidak cocok: peluncuran aplikasi/startup teknologi, atau kebutuhan nasihat hukum.

## Contoh sebelum & sesudah
**Sebelum:** "Aku mau launching sambal botol, bingung mulai dari mana. Posting dulu? Kapan pesan botol? Takut stok kurang."

**Sesudah (cukup ketik):** "Bantu rencana peluncuran sambal botol 180 g, tanggal 14 November, stok 150, kontak WA 120, IG 800, anggaran promo 500 ribu."

Cuplikan jadwal (dipotong; NIB = nomor induk berusaha; contoh fiktif dari `examples/01-jadwal-sambal-botol.md`):
```
# Jadwal peluncuran: Sambal Botol Bu Rina
- Tanggal peluncuran (T0): Sabtu, 2026-11-14
- Jumlah tugas: 43
## Perhatian
- Waktu tersisa 25 hari (<30): tugas sebelum hari ini ditandai LEWAT; padatkan atau geser peluncuran.
### Kamis, 2026-10-15
- [ ] T-30 [Legalitas | Izin] Cek status izin & label: NIB, PIRT/BPOM, sertifikat halal (pangan). Ini pengingat; keputusan tetap di instansi resmi _(LEWAT: kerjakan secepatnya atau padatkan jadwal)_
### Sabtu, 2026-10-31
- [ ] T-14 [Soft launch | Waitlist] Buka soft launch untuk daftar tunggu: pre-order terbatas (mis. 30-50 unit) dengan tanggal kirim jelas (paling lambat T-10); catat jumlah pre-order (dipakai untuk hitungan stok/kapasitas)
### Jumat, 2026-11-06
- [ ] T-7 [Stok & operasional | Stok] Hitung stok awal = (pre-order soft launch + perkiraan pesanan minggu 1) x 1,3 dan bandingkan dengan stok; tetapkan batas 'stok habis' dan pesan ulang _(digeser dari 2026-11-07 (Sabtu) karena bukan hari kerja)_
```
Hasil lengkapnya juga memuat pesan WA/IG siap tempel, stok awal yang dihitung, keputusan Go/No-Go (jalan atau tunda) di H-1, dan pengingat halal/BPOM.

## Cara pakai
Ketik permintaan biasa, misalnya:
- "Buatkan jadwal launching produk baruku tanggal 5 Desember."
- "Aku mau pre-order dulu sebelum launching, gimana caranya?"
- "Cek rencana launching ini, apa yang kurang?"
Jadwal bertanggal dihitung oleh skrip bawaan (cara menjalankannya sendiri ada di bagian Instalasi); tanpa skrip pun skill tetap menyusun jadwal manual.

## Instalasi singkat
Salin folder `luncurkan-produk-baru` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket (`docs/instalasi.md`).

Skrip jadwal (opsional): `python3 scripts/jadwal_peluncuran.py --tanggal 2026-11-14 --produk "Nama" --jenis pangan` (Windows: `python` atau `py`).

## Skill pelengkap
hitung modal & harga jual (`hitung-hpp`), harga jual marketplace (`harga-jual-marketplace`), paket konten mingguan dengan caption siap tempel (`konten-mingguan`), listing marketplace (`listing-marketplace`), naskah live jualan (`naskah-live-jualan`), laporan iklan mingguan (`laporan-iklan-mingguan`), KPI tim (`kpi-tim`), dan kalender promo (`promo-kalender`).

**Hasil uji (jujur):** dua sumber yang terpisah, skor 1–10.
- **Uji OpenClaw, uji otomatis agent, v1.0.4** (angka dari `examples/00-openclaw-sebelum-sesudah.md`): rata-rata nilai 5,5 tanpa skill menjadi 9,0 dengan skill. Pada rencana launching kosmetik pencerah yang izin BPOM-nya belum terbit (kandidat peluncuran 12 Oktober 2026), AI tanpa skill menolak dua klaim terlarang tetapi masih menjadwalkan pre-order 10 Oktober; dengan skill penjualan, pre-order, dan promo ditunda sampai izin terbit, hanya daftar tunggu tanpa uang yang dibuka, dan Go/No-Go otomatis No-Go. Pada rencana nastar 20 November, stok awal dihitung rumus: (40 + 20) x 1,3 = 78 toples.
- **Uji di bot Telegram asli:** angkanya ada di bagian berikutnya.

**Status uji (jujur):** baru diuji di OpenClaw (uji otomatis agent); Codex, Claude Code, dan Cursor belum diuji langsung (format skill-nya sama).

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

**Seberapa tepat daftar libur nasionalnya?**
Berasal dari SKB 3 Menteri (surat keputusan bersama tentang hari libur dan cuti bersama) 2026 dan 2027 (sudah dicocokkan dengan lampiran resmi per 2026-09-29). Pemerintah dapat mengubahnya; cocokkan dengan pengumuman terbaru atau tambahkan lewat `--libur-tambahan`.

Kredit sumber terbuka dan lisensi: lihat `ATTRIBUTION.md`. Tidak berafiliasi dengan pembuat sumber.

## Riwayat perubahan

Versi terkini: **1.0.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
