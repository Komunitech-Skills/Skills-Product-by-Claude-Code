# KPI Tim: Target Jelas, Skor Dihitung Otomatis

**Target per orang dan per divisi, skor pencapaian hijau/kuning/merah yang dihitung benar, dari Excel, Google Sheets, atau rekap grup WA. Tanpa aplikasi berlangganan.**

## Manfaat
- ✅ **Tidak bingung lagi "KPI apa yang cocok".** Ada katalog KPI siap pakai untuk 9 peran yang umum di UMKM: sales, CS, produksi, gudang, keuangan, marketing, admin, kurir, dan kasir. Setiap KPI dilengkapi rumus, satuan, arah (makin tinggi atau makin rendah makin baik), dan sumber datanya.
- ✅ **Template Excel/Google Sheets jadi dalam semenit.** Sebutkan nama, divisi, dan peran tim. AI membuat file rencana KPI (bobot sudah 100%, target contoh, lembar petunjuk) dan lembar isian realisasi.
- ✅ **Rekap grup WA langsung jadi angka.** Tempel pesan seperti "Andi closing 14 deal, target 15, omzet 162 jt". AI menyusunnya jadi tabel draf untuk kamu cek dulu, tanpa perlu mengetik ulang.
- ✅ **Skor dihitung script, bukan dikira.** KPI "makin rendah makin baik" (komplain, reject, telat) dihitung dengan rumus yang benar. Capaian dibatasi 120% supaya satu KPI tidak menutupi yang lain. Hasilnya berupa skor tertimbang per orang, divisi, dan perusahaan, lengkap dengan tren dibanding bulan lalu.
- ✅ **Laporan siap kirim dan bahan 1:1.** Ringkasan untuk Telegram pemilik (bisa dijadwalkan otomatis lewat OpenClaw), rincian per orang untuk ngobrol 1:1, dan OKR ringan untuk target kuartalan.

## Cocok untuk siapa
- Pemilik distributor, toko, pabrik kecil, konveksi, klinik, atau agensi dengan 3–30 karyawan
- Manajer/supervisor yang selama ini merekap target tim secara manual di Excel
- Usaha yang laporan hariannya masih lewat grup WA atau kertas
- Pemilik yang tidak mau data kinerja karyawannya disimpan di server pihak lain

## Contoh sebelum & sesudah
**Sebelum:** target ada di kepala pemilik, angka tersebar di grup WA dan beberapa file Excel. Menghitung manual rawan keliru. Contohnya KPI "salah kirim, target 3, realisasi 6": tanpa rumus yang disepakati, capaiannya bisa tertulis 200% ("6 dari 3") atau 50% (3 ÷ 6). Keduanya menyesatkan. Karyawan yang datanya belum masuk juga bisa dianggap nol.

**Sesudah:** "Ini rekap grup WA akhir September, hitung KPI tim saya."
→ AI menunjukkan 9 baris draf dari chat untuk dicek. Setelah kamu balas "ok", keluar laporan:
```
📊 Laporan KPI Tim — 2026-09
Perusahaan: 🟡 93,6 (▲6,3 vs 2026-08) — sebagian
🟡 Gudang & Pengiriman: 91,7 ▼4,2
🟡 Keuangan & Admin: 93,1 ▲17,6 (tanpa Tono Wijaya)
🟡 Sales: 96,1 ▲5,6
🔴 Joko Susilo (Gudang & Pengiriman): 76,7 ▼15,1 — perlu perhatian: Salah kirim 0,0%
⚪ Tono Wijaya: belum lengkap — belum ada data: Nota diarsip lengkap
```
Salah kirim 6 dari target 3 dihitung (2 − 6/3) × 100 = 0%. Tono tidak otomatis dianggap gagal karena datanya belum masuk. Tono ditandai "belum lengkap", dan aturan ini tertulis jelas.

## Cara pakai
Cukup ketik ke AI agent kamu, misalnya:
- "KPI apa yang cocok untuk admin gudang dan kurir?"
- "Buatkan template KPI untuk tim saya: Andi & Rina sales, Dewi CS, Budi gudang."
- "Ini rekap grup WA, masukkan jadi realisasi KPI September."
- "Hitung skor KPI September dari file ini, bandingkan dengan Agustus."
- "Siapkan bahan 1:1 untuk Joko."
- "Buat OKR kuartal 4 untuk divisi sales."
- "Kirim laporan KPI ke Telegram saya tiap tanggal 2 jam 7 pagi." (OpenClaw)

## Syarat
- Python 3.8 atau lebih baru (di Mac/Linux biasanya sudah ada; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, API key, atau instalasi paket.
- Data berupa file di komputermu sendiri: CSV atau Excel (.xlsx). Untuk Google Sheets: unduh sebagai .xlsx/.csv, lalu impor kembali template yang dibuat AI.
- Jadwal otomatis ke Telegram hanya untuk OpenClaw, dan komputer harus menyala saat jam jadwal.

## Instalasi singkat
Salin folder `kpi-tim` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah skor KPI ini bisa dipakai untuk memecat atau memotong gaji karyawan?**
Tidak. Skor ini bahan diskusi dan pembinaan. Sebelum keputusan kepegawaian, dengarkan penjelasan karyawan, periksa hambatan di luar kendalinya, dan ikuti peraturan perusahaan serta UU Ketenagakerjaan. Untuk surat peringatan, gunakan skill `surat-peringatan-karyawan`. Untuk sengketa, konsultasikan ke HR atau konsultan hukum.

**Data kinerja karyawan disimpan di mana, dan siapa yang bisa melihat?**
Di komputermu sendiri. Script tidak mengirim data ke mana pun. Laporan per orang disarankan hanya untuk pemilik/manajer. Untuk grup kantor tersedia mode tanpa nama (skor perusahaan & divisi saja). Daftar orang diurutkan per divisi dan nama, bukan peringkat, supaya tidak ada yang dipermalukan.

**Tim saya belum punya target. Apakah target di template bisa langsung dipakai?**
Target di katalog hanya contoh. Target yang adil berasal dari data 3 bulan terakhir usahamu, ditambah kenaikan wajar, dan dibicarakan dengan orangnya. Kalau belum ada data, pakai bulan pertama untuk mengukur saja, lalu pasang target di bulan berikutnya.
