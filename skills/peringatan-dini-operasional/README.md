# Tahu Masalah Operasional Sebelum Jadi Besar

**Isi log harian sederhana (catatan angka usaha per hari), AI memberi tahu angka mana yang mulai tidak normal, seberapa gawat, dan apa yang perlu dicek hari ini.**

*Diuji AI penguji independen di OpenClaw: 7,0 → 9,0 dari 10 (pembeda: laporan 1 halaman dihitung skrip dan tanpa nama karyawan, sedangkan AI biasa menawarkan mengirimnya ke grup WA karyawan; memakai data contoh).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk menjalankan skrip pendukung skill ini; tanpa Python skill tetap berjalan, AI mengerjakannya langsung tetapi hasil angka sebaiknya Anda cek ulang. Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Peringatan berwarna yang jelas:** 🔴 bahaya, 🟠 waspada, 🟡 perhatikan, masing-masing dengan alasan berangka ("reject (barang cacat) naik 3 hari berturut-turut, 6,8σ di atas rata-rata, lewat target maks 50"; σ = ukuran seberapa jauh angka menyimpang dari kebiasaan). Dirancang agar oranye/merah muncul hanya untuk lonjakan jelas atau yang bertahan, supaya Anda tidak "kebal alarm"; keluhan/kecelakaan yang biasanya nol ditandai begitu muncul
- ✅ **Tahu lebih awal kalau stok akan habis:** sisa stok diubah jadi "cukup ±3,2 hari, perkiraan habis Jumat", dibandingkan dengan lama pemasok mengirim
- ✅ **Langsung tahu apa yang dicek:** daftar pertanyaan akar masalah (bahan, mesin, orang, cara kerja) + pancingan "5 kenapa" (bertanya "kenapa" berulang sampai ketemu akar masalah), tanpa mencari kambing hitam
- ✅ **Angka dihitung, bukan dikira:** rata-rata 7 hari, tren, banding target, banding hari yang sama 4 minggu lalu, dan batas kendali (batas wajar naik-turun angka) dihitung skrip. Angka kosong tidak diisi tebakan
- ✅ **Otomatis tiap malam:** bisa dijadwalkan di OpenClaw, laporan 1 halaman (hanya angka, tanpa nama orang) masuk ke Telegram (jadwal otomatis ini belum diuji langsung)

## Cocok untuk siapa
- Pemilik & manajer pabrik kecil-menengah, konveksi, percetakan
- Dapur usaha makanan dan minuman (F&B), katering, bakery, cloud kitchen (dapur khusus pesanan online)
- Toko/retail, gudang, dan distributor yang mencatat pengiriman & keluhan
- Supervisor yang tiap hari mengisi angka di Excel tapi belum sempat menganalisanya

## Contoh sebelum & sesudah
**Sebelum:** Tiap hari mengisi Excel produksi. Reject naik pelan-pelan 30 → 34 → 39 → 46 dan tidak ada yang sadar, sampai hari ke-5 reject 63 roti dan tepung ternyata tinggal cukup 3 hari. Baru ketahuan saat pelanggan komplain dan produksi hampir berhenti.

**Sesudah (cukup ketik):** "Ini log produksi 30 hari. Ada yang perlu diwaspadai? Pemasok tepung butuh 2 hari."
```
🚨 PERINGATAN DINI OPERASIONAL
Roti Bu Ratna (fiktif) — Sel, 29 Sep 2026
Data 31 Agu–29 Sep (29 hari tercatat)
Ringkas: 2 🔴 · 1 🟠 · 1 🟡 · 4 normal
…
🔴 Reject (pcs): 63 hari ini (kemarin 46)
   6,8σ di atas rata-rata 27 hari sebelumnya (31,15) -- lewat batas bahaya 3σ (2 dari 3 hari terakhir); melewati target maks 50 (+26%); naik 3 hari berturut-turut.
🟠 Stok tepung (kg): sisa 169 = ±3,2 hari pemakaian (rata-rata 52,29/hari) -> cukup sampai Jum, 2 Okt, mulai kurang Sab, 3 Okt; pemasok butuh 2 hari -- siapkan pesanan
🟡 Penjualan (Rp): Rp 8.644.500 hari ini (kemarin Rp 8.730.000)
   turun 3 hari berturut-turut; di bawah target min Rp 9.000.000 (-4%); 2 dari 7 hari terakhir di bawah target.
✅ Normal: Output (pcs), Keluhan, Telat kirim, Absen
❓ Cek hari ini (cari akar masalah, bukan cari kambing hitam):
…
```
(Contoh dengan data fiktif dari `examples/01-pabrik-roti-30-hari.md`, dipotong.) Lengkapnya juga memuat pertanyaan cek untuk tim.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent Anda, misalnya:
- "Cek log produksi ini, ada yang aneh nggak?" (lampirkan file CSV, yaitu tabel sederhana, atau Excel; atau tempel tabelnya)
- "Reject minggu ini kok naik terus? Target saya maksimal 50 sehari."
- "Stok bahan saya cukup berapa hari lagi? Pemasok kirim 3 hari setelah pesan."
- "Tiap malam jam 8 kirimi saya peringatan dini ke Telegram." (jadwal otomatis ini belum diuji langsung)

Belum punya log? Pakai `templates/log-harian-template.csv`: satu baris per hari, kolom boleh ditambah/dihapus (mis. pesanan, retur, downtime_menit, yaitu menit mesin berhenti). Minimal 7 hari data; hasil paling tajam setelah 4–5 minggu.

## Instalasi singkat
Salin folder `peringatan-dini-operasional` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket. Tidak perlu API key atau akun tambahan (hitungan memakai Python 3, lihat kotak "Yang Anda butuhkan" di atas). Jadwal otomatis hanya tersedia di OpenClaw (belum diuji langsung) dan butuh komputer yang menyala di jam kirim.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (diuji pada v1.0.5; versi terbaru 1.0.7), skor 1–10: tanpa skill **7,0** → dengan skill **9,0** (LULUS). Contoh log dapur 4 minggu: stok beras sisa **255 kg = ±2 hari** pemakaian, pemasok butuh 2 hari → **pesan HARI INI**; tanpa nama karyawan. Sumber skor: `examples/00-openclaw-sebelum-sesudah.md`. Catatan jujur: tanpa skill pun angka inti sudah benar; daftar cek dari skill kadang masih generik dan sempat merujuk skill lain yang tidak terpasang. Contoh "Sesudah" di atas (pabrik roti fiktif) adalah hasil skrip dari pembuat skill, bukan dari uji OpenClaw.

**Status uji (jujur):** sudah diuji OpenClaw sebelum/sesudah otomatis (2026-10-02). Claude Code/Codex/Cursor belum uji platform asli. Jadwal otomatis ke Telegram belum diuji langsung. Perkiraan stok/hari = estimasi kasar, bukan ramalan pasti.

## Bukti uji di bot Telegram

Diuji di bot OpenClaw asli (grup uji internal Komunitech, 16 Okt 2026) dengan pesan yang sama: "Ini log harian pabrik roti saya 30 hari terakhir (fiktif), filenya data/log-roti-30hari.csv. Ada yang perlu saya waspadai? Pemasok tepung biasanya kirim 2 hari setelah dipesan. Nama usaha: Roti Bu Ratna Fiktif. (Catatan:…". Tanpa skill skor **5** → dengan skill skor **8,5** (selisih +3,5, lulus acuan kami). Hanya versi dengan skill yang menghitung tepat kapan tepung habis (cukup sampai Jumat 2 Okt, mulai kurang Sabtu 3 Okt) dan memberi tanda merah/oranye/kuning untuk tiap angka tanpa salah hitung; versi tanpa skill salah menghitung hari telat kirim (9, padahal 8). Salah angka yang ditemukan penilai: TANPA: telat kirim disebut terjadi di 9 dari 29 hari kerja (~31%); hitung ulang dari CSV = 8 hari (2, 8, 11, 14, 16, 19, 20, 25 Sep) = 27,6%; TANPA (tidak tepat, bukan salah angka): 'dari situ [28 Sep, tepung baru] reject naik tajam: 34 → 39 → 46 → 63'; angka 34 dan 39 terjadi pada 26–27 Sep, sebelum tepung baru dipakai. Catatan jujur: Laporan memakai istilah statistik (σ, batas 3σ) yang bisa membingungkan pembaca awam. Laporan juga tidak menyebut tegas bahwa kiriman tepung mingguan dari pemasok berhenti sejak 19 Sep; laporan hanya menanyakan kapan terakhir memesan.

## FAQ
**Apakah ini bisa meramal masalah dengan pasti?**
Tidak. Ini peringatan dini statistik: memberi tahu angka yang "tidak biasa" dibanding pola usaha Anda sendiri, supaya dicek lebih awal. Perkiraan (mis. "±4 hari lagi melewati target", "stok habis Jumat") ditandai sebagai perkiraan kasar. Penyebab tetap dicari bersama tim lewat pertanyaan cek dan 5 kenapa.

**Data saya baru seminggu, bisa dipakai?**
Bisa, tapi terbatas: yang jalan baru banding target, naik/turun beruntun, dan sisa stok. Batas kendali (σ) butuh ±15 hari, banding hari yang sama butuh 2 minggu. Laporan akan menyebut ini terus terang, dan hasilnya makin tajam tiap minggu Anda mengisi log.

**Angka saya ditulis macam-macam (1.250, 1,2rb, Rp 9 jt) dan ada hari libur. Masalah?**
Umumnya tidak. Format angka Indonesia dibaca otomatis; hari libur/kosong dilewati (tidak diisi tebakan), baris rusak dilaporkan. Hari luar biasa seperti Lebaran atau bazar bisa dikecualikan supaya tidak mengacaukan rata-rata.

**Kenapa hampir tiap minggu ada tanda 🟡?**
Wajar. 🟡 artinya "angka agak di luar kebiasaan, cukup dilirik" — pada data yang stabil pun sekitar 1 dari 4 hari akan ada satu angka (misalnya reject atau penjualan) berstatus 🟡 (per angka hanya ±2–8% hari). Yang perlu ditindaklanjuti adalah 🟠 dan 🔴; dalam simulasi data stabil keduanya muncul di kurang dari 5% hari.

## Riwayat perubahan

Versi terkini: **1.0.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
