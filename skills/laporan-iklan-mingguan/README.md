# Laporan Iklan Mingguan, Bahasa Awam

**Kirim file ekspor (CSV) dari Meta/TikTok/Shopee/Google Ads, dapat laporan mingguan siap kirim ke bos atau tim —
lengkap dengan saran iklan mana yang perlu ditinjau atau dimatikan.**

Diuji AI penguji independen di OpenClaw: 6,0 → 8,75 dari 10 (tanpa skill menebak kurs dolar dan menghitung biaya per hasil dari sebagian kampanye saja; dengan skill AI berhenti menanyakan kurs lalu menghitung seluruh belanja).

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ CPC (biaya per klik), CPM (biaya per 1.000 tayangan), CTR (persentase yang mengeklik), biaya per hasil (CPA/CPL), dan ROAS (omzet per rupiah iklan) dihitung dari angka mentah — bukan
  dari kolom rata-rata bawaan file yang bisa salah kalau dijumlah langsung
- ✅ Perbandingan % otomatis vs minggu lalu, dengan aturan pembulatan yang konsisten
- ✅ 3 kampanye terbaik & 3 yang perlu perhatian (termasuk yang 0 hasil tapi tetap makan biaya)
- ✅ Saran tindakan dengan angka jelas ("tinjau iklan X: Rp120.000/hasil, 2,1× rata-rata"),
  dengan catatan "sampel kecil" bila hasilnya masih sedikit. Tanpa janji hasil, keputusan tetap
  di tangan Anda
- ✅ Baca file ekspor (CSV) Meta Ads, TikTok Ads Manager, Shopee Ads, TikTok Shop Ads (dulu Tokopedia Ads), dan
  Google Ads — bahkan bisa digabung jadi satu laporan lintas platform
- ✅ Langsung dari file ekspor apa adanya: baris judul, baris "Total", sel kosong, dan kolom
  rata-rata bawaan ditangani otomatis dan dicatat di laporan, bukan dihitung dua kali atau dibuang.
  Kampanye bernama "Total 12.12 Flash Sale" atau "Jumlah 2 Pcs Bundling" tetap dihitung, dan setiap
  baris yang dikecualikan sebagai total disebut nama & biayanya di bagian ⚠️
- ✅ Tidak menghitung dolar sebagai Rupiah: kalau file ternyata mata uang asing, AI berhenti
  dan menanyakan kurs dulu

## Cocok untuk siapa
- Pemilik toko online/UMKM yang beriklan di 1 platform atau lebih dan lelah membuka Ads Manager
  tiap minggu cuma untuk tahu "habis berapa, dapat apa"
- Admin/tim marketing kecil yang bikin laporan mingguan manual ke bos lewat WA/Telegram
- Member VIP komunitech.com yang sudah pakai OpenClaw — laporan ini bisa dijadwalkan otomatis
  tiap Senin pagi lewat skill `laporan-otomatis-terjadwal` (penjadwal ke Telegram; pengiriman laporan iklan terjadwal sudah diuji bot Telegram uji 2026-10-13 — bukti di `examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`)

## Contoh sebelum & sesudah
**Sebelum:** buka Ads Manager tiap platform satu-satu, catat angka manual di Excel, hitung sendiri
CPC/CPA/ROAS, baru bisa lapor ke bos — 30–60 menit tiap minggu, dan gampang salah hitung.

**Sesudah (cukup kirim file lalu ketik):** "Ini ekspor Meta Ads minggu ini sama minggu lalu,
buatin laporannya."
→ Dalam hitungan detik:
```
Total belanja iklan: Rp 2.900.000
CPC: Rp 2.071 | CPM: Rp 19.333 | CTR: 0,9%
Biaya per Results: Rp 58.000 (naik 8,9% dari minggu lalu Rp 53.261)
ROAS: 1,9x

SARAN
1. Tinjau/hentikan iklan 'Retargeting - Semua Produk': sudah menghabiskan Rp 800.000 tanpa
   Results sama sekali.
2. Tinjau/matikan iklan 'Prospek Baru - Tas': biaya per Results Rp 120.000, 2,1x rata-rata
   semua iklan (Rp 58.000).
```
(Contoh dengan data fiktif; lengkapnya dengan angka diverifikasi manual ada di `examples/uji-pembuat-01-meta-mingguan-vs-lalu.md`.)

## Cara pakai
Setelah terpasang, ekspor CSV dari Ads Manager platform Anda (menu "Export"/"Download" di masing-
masing dashboard iklan — tetap manual, 1-2 menit, skill ini **tidak** login/menarik data otomatis
demi keamanan akun Anda), lalu cukup ketik ke AI agent Anda, misalnya:
- "Ini ekspor iklan minggu ini, buatin laporannya."
- "Bandingkan biaya iklan minggu ini vs minggu lalu, ini dua filenya."
- "Gabungkan laporan Meta Ads dan Shopee Ads minggu ini jadi satu, omzet toko 20 juta."

## Yang perlu Anda ketahui (jujur)
- Nama kolom Meta Ads dan bentuk ekspor Google Ads/TikTok di skill ini disusun dari dokumentasi
  resmi dan sumber pihak ketiga, **belum dicocokkan dengan file ekspor asli dari setiap
  platform**. Karena itu setiap laporan mencantumkan "Kolom dibaca: ..." di baris ke-3 laporan. Cek
  sekali di minggu pertama; bila ada yang keliru, AI bisa diberi tahu kolom yang benar.
- Biaya di file ekspor biasanya belum termasuk PPN yang ditagihkan platform. Cek invoice platform
  untuk angka tagihan sebenarnya.

## Syarat
File berformat **CSV** (Excel `.xlsx` disimpan ulang sebagai CSV dulu: *File → Save As → CSV*).
Butuh Python di komputer (biasanya sudah ada di Mac/Linux; di Windows bisa dipasang gratis dari
python.org) — tapi kalau tidak ada Python pun, langkah hitung manual & rumusnya tetap dijelaskan
di dalam skill.

## Instalasi singkat
Salin folder `laporan-iklan-mingguan` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` (di dalam paket bernama `CARA-INSTAL.md`).

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.0.10), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **8,75** (LULUS). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill angka iklan bisa meleset (kurs ditebak, biaya per hasil hanya dari sebagian kampanye); dengan skill angka pada skenario uji cocok dengan hitungan independen dan rekomendasi kanal jelas.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01; uji muat CLI) dan Claude Code (simulasi agent). Jadwal laporan iklan ke Telegram (automations one-shot, command-argv) diuji bot uji 2026-10-13. Codex dan Cursor belum kami uji langsung.

## FAQ
**Data iklan saya dikirim ke internet?**
Tidak. Perhitungan berjalan di komputer Anda sendiri lewat script Python. Yang diproses AI agent
hanya ringkasan angka yang sama seperti percakapan biasa.

**Nama kolom di file ekspor saya beda dari contoh?**
AI agent akan mencoba mencocokkan otomatis (mendukung istilah Inggris & Indonesia). Kalau gagal,
Anda cukup ditanya satu kali nama kolom mana yang dimaksud — tidak ada yang ditebak sembarangan.

**Bisa langsung dikirim otomatis tiap Senin pagi ke Telegram?**
Bisa, lewat skill `laporan-otomatis-terjadwal` atau pola `openclaw automations` di
`references/openclaw-jadwal.md` (command-argv disarankan agar angka tidak ditulis ulang AI). Pengiriman
one-shot ke Telegram sudah diuji bot uji 2026-10-13. Skill ini fokus menghitung laporannya dengan benar.

## Riwayat perubahan

Versi terkini: **1.0.11**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
