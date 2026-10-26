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
  tiap Senin pagi lewat skill `laporan-otomatis-terjadwal` (penjadwal ke Telegram; satu laporan iklan terjadwal sekali jalan sudah terkirim ke grup uji Telegram Komunitech pada 13 Okt 2026 dengan angka yang cocok, sedangkan jadwal berulang tiap Senin belum diuji — bukti di `examples/UJI-JADWAL-TELEGRAM-2026-10-13.md`)

## Contoh sebelum & sesudah
**Sebelum:** buka Ads Manager tiap platform satu-satu, catat angka manual di Excel, hitung sendiri
CPC/CPA/ROAS, baru bisa lapor ke bos — 30–60 menit tiap minggu, dan gampang salah hitung.

**Sesudah (cukup kirim file lalu ketik):** "Ini ekspor Meta Ads minggu ini sama minggu lalu,
buatin laporannya."
→ Dalam hitungan detik:
```
Total belanja iklan: Rp 2.900.000
Tayangan: 150.000 | Klik: 1.400 | Results: 50
CPC: Rp 2.071 | CPM: Rp 19.333 | CTR: 0,9%
Biaya per Results: Rp 58.000
ROAS: 1,9x
...
Biaya per hasil: Rp 58.000 (naik 8,9% dari minggu lalu Rp 53.261)
...
SARAN
1. Tinjau/hentikan iklan 'Retargeting - Semua Produk': sudah menghabiskan Rp 800.000 tanpa
   Results sama sekali.
2. Tinjau/matikan iklan 'Prospek Baru - Tas': biaya per Results Rp 120.000, 2,1x rata-rata
   semua iklan (Rp 58.000).
```
(Contoh dengan data fiktif; keluaran skrip versi 1.0.1, sebagian baris dipotong (tanda "..."). Lengkapnya dengan angka diverifikasi manual ada di `examples/uji-pembuat-01-meta-mingguan-vs-lalu.md`.)

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
  platform**. Karena itu, bila di file ada dua kolom yang sama-sama mungkin (mis. "Link clicks" dan
  "Clicks (all)"), bagian Catatan laporan menyebutnya dalam satu kalimat ("Saya membaca kolom ... sebagai
  jumlah klik ..."). Cek kalimat itu sekali di minggu pertama; bila keliru, kabari AI kolom yang benar.
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

**Hasil uji (angka nyata):** uji OpenClaw (lingkungan uji terpisah), 1 Okt 2026 (v1.0.9), skor 1–10 penguji independen: tanpa skill **6,0** → dengan skill **8,75**, selisih 2,75 (lulus acuan kami). Sumber: `examples/00-openclaw-sebelum-sesudah.md`. Tanpa skill angka iklan bisa meleset (kurs ditebak, biaya per hasil hanya dari sebagian kampanye); dengan skill angka pada skenario uji cocok dengan hitungan independen. Catatan jujur dari uji itu: saran "matikan" sempat mengabaikan tujuan kampanye (iklan kunjungan atau pengenalan merek yang memang tidak mengejar pesan WA) dan catatan kolom yang dibaca sempat terpotong; keduanya diperbaiki di v1.0.10 dan belum diuji ulang sebelum/sesudah.
Catatan jujur berikutnya: uji awal di bot Telegram asli (v1.0.11) mendapat skor 7,0 dengan semua angka benar, tetapi bot sempat membuka jawaban dengan istilah teknis dan menawarkan menyambungkan WhatsApp karena kata "chat WA masuk" dikira perintah (padahal itu nama hasil iklan), serta menampilkan satu baris teknis soal kolom. Keduanya diperbaiki di v1.0.12 (laporan tidak lagi memuat baris teknis itu, istilah CPC/CPM/CTR dijelaskan di Catatan) dan belum diuji ulang di bot asli.

**Status uji (jujur):** sudah diuji di OpenClaw (uji sebelum/sesudah otomatis agent, 2026-10-01; uji muat CLI) dan Claude Code (simulasi agent). Satu laporan iklan terjadwal sekali jalan terkirim ke grup uji Telegram Komunitech pada 13 Okt 2026 (tiba tepat waktu, angka cocok dengan hitungan terpisah); jadwal berulang tiap Senin belum diuji. Codex dan Cursor belum kami uji langsung.

## Bukti uji di bot Telegram

Uji terbaru: 21 Oktober 2026, versi 1.0.12, di bot OpenClaw asli (grup uji Komunitech), pesan yang sama untuk tanpa skill dan dengan skill: pemilik toko hijab mengirim data iklan minggu ini dan minggu lalu (belanja Rp4,2 juta, 114 chat WA) dan bertanya iklan mana yang sebaiknya dimatikan. Skor 1–10 dari penilai independen: tanpa skill **7,5** → dengan skill **8,5** (selisih +1), **belum memenuhi acuan kami** (dengan skill minimal 8 dan selisih minimal 1,5).

Jujurnya: tanpa skill pun bot sudah cukup baik. Angkanya benar dan sarannya sama, yaitu mematikan iklan Hijab Instan Baru (Rp91.667 per chat, sekitar 2,5 kali rata-rata). Dengan skill laporannya lebih rapi dan lengkap (CPC, CPM, CTR, catatan PPN, iklan kunjungan tidak disarankan dimatikan hanya karena 0 chat), tetapi bedanya belum cukup besar untuk kami promosikan.

Catatan jujur: penjelasan istilah CPC/CPM/CTR tidak ikut terkirim, rata-rata biaya per chat ikut menghitung iklan kunjungan sehingga kenaikannya tampak lebih ringan (untuk iklan WA saja naik sekitar 50%), dan iklan yang baru tayang belum ditandai. Ini satu pesan uji per sisi, bukan uji berulang.

## FAQ
**Data iklan saya dikirim ke internet?**
Tidak. Perhitungan berjalan di komputer Anda sendiri lewat script Python. Yang diproses AI agent
hanya ringkasan angka yang sama seperti percakapan biasa.

**Nama kolom di file ekspor saya beda dari contoh?**
AI agent akan mencoba mencocokkan otomatis (mendukung istilah Inggris & Indonesia). Kalau gagal,
Anda cukup ditanya satu kali nama kolom mana yang dimaksud — tidak ada yang ditebak sembarangan.

**Bisa langsung dikirim otomatis tiap Senin pagi ke Telegram?**
Bisa, lewat skill `laporan-otomatis-terjadwal` atau pola jadwal OpenClaw di
`references/openclaw-jadwal.md` (disarankan menjalankan skrip langsung tanpa lewat AI, agar angka tidak ditulis ulang AI). Satu
pengiriman sekali jalan ke Telegram sudah diuji di grup uji Telegram Komunitech pada 13 Okt 2026; jadwal berulang tiap Senin belum diuji. Skill ini fokus menghitung laporannya dengan benar.

## Riwayat perubahan

Versi terkini: **1.0.12**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
