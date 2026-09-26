# HASIL UJI — resi-picking v1.0.0 (penguji independen, Akun B)

**Skor kualitas: 7/10**

## Temuan (berprioritas)

1. **[Sedang] Auto-deteksi kolom gagal pada header realistis TikTok Shop & Tokopedia (skenario
   02) — 0 dari 2 file lolos tanpa override.** Akar sebab: kata sinonim < 8 huruf ("kurir",
   "invoice") tidak pernah dicocokkan sebagian di `deteksi_kolom`, hanya cocok persis. Ini
   memang sudah ditandai "PERLU REVIEW" di SKILL.md dan ada jalan keluar (`--kolom-...` +
   `pemetaan_kolom`/error jelas), tapi mengurangi janji "instan, cukup satu kalimat" — agent
   WAJIB tahu menawarkan override, bukan cuma melaporkan gagal.
2. **[Rendah] Tanpa kemampuan gabung lintas marketplace** — toko dengan 2+ kanal harus
   menjalankan skrip berkali-kali dan menggabung hasil sendiri; wajar untuk alat "sekali jalan",
   tapi perlu disebut eksplisit ke pengguna di jawaban chat.
3. **[Info, tidak kritikal] Baris ringkasan "Total" tanpa SKU/nama tetap aman** (dites, tetap
   terbuang lewat cek "tanpa identitas barang"); risiko teoritis hanya jika suatu saat ekspor
   mengisi SKU pada baris total — belum ditemukan pada data nyata mana pun.

## Yang berjalan benar (diverifikasi independen, tanpa membaca kode)
- Total qty per SKU/varian, pengelompokan & urutan per kurir, jumlah pesanan aktif vs total,
  cross-check stok kurang, deteksi SKU tak dikenal — **100% cocok** pada ketiga skenario normal.
- Penanganan file rusak (BOM, qty rusak/negatif, duplikat, baris kosong, baris ringkasan) —
  tidak crash, semua dilaporkan dengan alasan + nomor baris.
- Di luar cakupan (minta login otomatis Seller Center): kode diaudit, **tidak ada** jaringan,
  scraping, subprocess, atau kredensial tertanam — batasan dijaga lewat instruksi SKILL.md,
  dan secara teknis skrip memang tidak mampu melakukan itu.
- `python3 scripts/validate.py --skill resi-picking` ✅ lulus; 19/19 test bawaan (`tests/uji_regresi.py`) ✅ lulus.
- Uji A/B: nilai tambah signifikan untuk tugas hitungan pasti (lihat `00-pembanding-tanpa-skill.md`).
- Uji banding pesaing: tidak ada skill agent pesaing langsung; dibanding SaaS berbayar, unggul di
  privasi & tanpa biaya bulanan, kalah di integrasi lintas-marketplace otomatis (`00-banding-pesaing.md`).

## Rekomendasi
Perluas `SINONIM_PESANAN` dengan variasi header TikTok Shop/Tokopedia yang lebih realistis
(`order/adjustment id`, `sku reference no.`, `no. invoice`, `nama barang`, `nama kurir`), dan
turunkan ambang panjang kata untuk pencocokan sebagian atau tambahkan daftar sinonim pendek yang
dicek persis dengan variasi umum ("no kurir", "nama kurir", dst.) sebelum naik ke `lulus`.
Skor di bawah 7 tidak tercapai karena inti perhitungan benar dan batasan keamanan terjaga; namun
skor ditahan di 7 (bukan lebih tinggi) karena tingkat sukses auto-deteksi kolom pada data
"marketplace asli" masih rendah pada uji ini.

`platform_teruji` belum diisi oleh penguji ini (hanya uji skrip/logika, bukan uji platform asli
OpenClaw/Codex/Claude Code/Cursor sesuai Tahap 6 poin 9–10).
