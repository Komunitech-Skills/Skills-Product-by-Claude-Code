# Tahu Masalah Operasional Sebelum Jadi Besar

**Isi log harian sederhana, AI memberi tahu angka mana yang mulai tidak normal, seberapa gawat, dan apa yang perlu dicek hari ini.**

## Manfaat
- ✅ **Peringatan berwarna yang jelas:** 🔴 bahaya, 🟠 waspada, 🟡 perhatikan, masing-masing dengan alasan berangka ("reject naik 3 hari berturut-turut, 6,8σ di atas rata-rata, lewat target maks 50"). Oranye/merah hanya untuk lonjakan jelas atau yang bertahan, jadi tidak bikin "kebal alarm"; keluhan/kecelakaan yang biasanya nol langsung ditandai begitu muncul
- ✅ **Stok tidak habis mendadak:** sisa stok diubah jadi "cukup ±3,2 hari, perkiraan habis Jumat", dibandingkan dengan lama pemasok mengirim
- ✅ **Langsung tahu apa yang dicek:** daftar pertanyaan akar masalah (bahan, mesin, orang, cara kerja) + pancingan 5 kenapa, tanpa mencari kambing hitam
- ✅ **Angka dihitung, bukan dikira:** rata-rata 7 hari, tren, banding target, banding hari yang sama 4 minggu lalu, dan batas kendali dihitung script. Angka kosong tidak diisi tebakan
- ✅ **Otomatis tiap malam:** bisa dijadwalkan di OpenClaw, laporan 1 halaman (hanya angka, tanpa nama orang) masuk ke Telegram

## Cocok untuk siapa
- Pemilik & manajer pabrik kecil-menengah, konveksi, percetakan
- Dapur F&B, katering, bakery, cloud kitchen
- Toko/retail, gudang, dan distributor yang mencatat pengiriman & keluhan
- Supervisor yang tiap hari mengisi angka di Excel tapi belum sempat menganalisanya

## Contoh sebelum & sesudah
**Sebelum:** Tiap hari mengisi Excel produksi. Reject naik pelan-pelan 30 → 34 → 39 → 46 dan tidak ada yang sadar, sampai hari ke-5 reject 63 roti dan tepung ternyata tinggal cukup 3 hari. Baru ketahuan saat pelanggan komplain dan produksi hampir berhenti.

**Sesudah (cukup ketik):** "Ini log produksi 30 hari. Ada yang perlu diwaspadai? Pemasok tepung butuh 2 hari."
→ Satu pesan: 🔴 Reject 63 (6,8σ di atas rata-rata, +112% dibanding Selasa biasanya, lewat target maks 50) · 🟠 Stok tepung cukup ±3,2 hari, habis Jumat, segera pesan · 🟡 Penjualan turun 3 hari. Plus 6 pertanyaan cek untuk tim.

## Cara pakai
Setelah terpasang, cukup ketik permintaan biasa ke AI agent kamu, misalnya:
- "Cek log produksi ini, ada yang aneh nggak?" (lampirkan file CSV/Excel atau tempel tabel)
- "Reject minggu ini kok naik terus? Target saya maksimal 50 sehari."
- "Stok bahan saya cukup berapa hari lagi? Pemasok kirim 3 hari setelah pesan."
- "Tiap malam jam 8 kirimi saya peringatan dini ke Telegram."

Belum punya log? Pakai `templates/log-harian-template.csv`: satu baris per hari, kolom boleh ditambah/dihapus (mis. pesanan, retur, downtime_menit). Minimal 7 hari data; hasil paling tajam setelah 4–5 minggu.

## Instalasi singkat
Salin folder `peringatan-dini-operasional` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket. Tidak perlu API key, akun, atau instalasi tambahan (hitungan memakai Python bawaan). Jadwal otomatis hanya tersedia di OpenClaw dan butuh komputer yang menyala di jam kirim.

## FAQ
**Apakah ini bisa meramal masalah dengan pasti?**
Tidak. Ini peringatan dini statistik: memberi tahu angka yang "tidak biasa" dibanding pola usahamu sendiri, supaya dicek lebih awal. Perkiraan (mis. "±4 hari lagi melewati target", "stok habis Jumat") selalu ditandai sebagai perkiraan kasar. Penyebab tetap dicari bersama tim lewat pertanyaan cek dan 5 kenapa.

**Data saya baru seminggu, bisa dipakai?**
Bisa, tapi terbatas: yang jalan baru banding target, naik/turun beruntun, dan sisa stok. Batas kendali (σ) butuh ±15 hari, banding hari yang sama butuh 2 minggu. Laporan akan menyebut ini terus terang, dan hasilnya makin tajam tiap minggu kamu mengisi log.

**Angka saya ditulis macam-macam (1.250, 1,2rb, Rp 9 jt) dan ada hari libur. Masalah?**
Tidak. Format angka Indonesia dibaca otomatis; hari libur/kosong dilewati (tidak diisi tebakan), baris rusak dilaporkan. Hari luar biasa seperti Lebaran atau bazar bisa dikecualikan supaya tidak mengacaukan rata-rata.
