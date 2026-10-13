# KPI Tim: Target Jelas, Skor Dihitung Otomatis

**Target per orang dan per divisi, skor pencapaian hijau/kuning/merah yang dihitung benar, dari Excel, Google Sheets, atau rekap grup WA. Tanpa aplikasi berlangganan.**

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan: Datasette, Grist (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tidak bingung lagi "KPI apa yang cocok".** Ada katalog KPI siap pakai untuk 9 peran yang umum di UMKM: sales, CS, produksi, gudang, keuangan, marketing, admin, kurir, dan kasir. Setiap KPI dilengkapi rumus, satuan, arah (makin tinggi atau makin rendah makin baik), dan sumber datanya.
- ✅ **Template Excel/Google Sheets jadi dalam semenit.** Sebutkan nama, divisi, dan peran tim. AI membuat file rencana KPI (bobot sudah 100%, target contoh, lembar petunjuk) dan lembar isian realisasi.
- ✅ **Rekap grup WA langsung jadi angka.** Tempel pesan seperti "Andi closing 14 deal, target 15, omzet 162 jt". AI menyusunnya jadi tabel draf untuk kamu cek dulu, tanpa perlu mengetik ulang.
- ✅ **Skor dihitung script, bukan dikira.** KPI "makin rendah makin baik" (komplain, reject, telat) dihitung dengan rumus yang benar. Capaian dibatasi 120% supaya satu KPI tidak menutupi yang lain. Hasilnya berupa skor tertimbang per orang, divisi, dan perusahaan, lengkap dengan tren dibanding bulan lalu.
- ✅ **Dasbor KPI dari file lokal.** Riwayat skor semua bulan disimpan ke satu file database, lalu bisa dilihat di browser (Datasette lewat skill `dasbor-lokal`) atau diimpor ke Grist: perusahaan → divisi → orang, tren per bulan, dan daftar KPI merah. Ada mode **anonim** untuk layar bersama: nama diganti kode, divisi kecil digabung, dan orang yang bisa ditebak dari daftar KPI-nya tidak ditampilkan per orang. Tanpa software baru, tanpa langganan.
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
- "Buatkan dasbor KPI dari data ini, tanpa nama karyawan." / "Siapkan file KPI untuk diimpor ke Grist."
- "Kirim laporan KPI ke Telegram saya tiap tanggal 2 jam 7 pagi." (OpenClaw)

## Syarat
- Python 3.8 atau lebih baru (di Mac/Linux biasanya sudah ada; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, API key, atau instalasi paket.
- Data berupa file di folder kerja yang kita sepakati (path-nya selalu saya sebutkan; bukan folder sementara /tmp): CSV atau Excel (.xlsx). Untuk Google Sheets: unduh sebagai .xlsx/.csv, lalu impor kembali template yang dibuat AI.
- Jadwal otomatis ke Telegram hanya untuk OpenClaw, dan komputer harus menyala saat jam jadwal.

## Dasbor KPI (opsional)
Setelah rencana dan realisasi siap, minta: **"Buatkan dasbor KPI-nya."** AI menjalankan `ekspor-db` dan menghasilkan folder berisi `kpi.db` + `kpi-metadata.yml` (dan CSV untuk Grist bila diminta). Membukanya di browser butuh Datasette (gratis, panduan: `docs/panduan-datasette.md`); yang sudah memakai Grist cukup mengimpor CSV (`docs/panduan-grist.md`). Tanpa keduanya, laporan teks tetap jalan.

**Penting soal privasi:** dasbor hanya boleh dibuka di komputer ini (alamat `127.0.0.1`), tidak ke internet, tidak ke HP/kantor cabang lain, dan filenya jangan dibagikan. Skor per orang adalah data pribadi karyawan. Kalau perlu ditampilkan ke orang lain, minta **mode anonim**; daftar "kode = nama" disimpan terpisah (`kunci-kode-RAHASIA.csv`).

## Instalasi singkat
Salin folder `kpi-tim` ke folder skills AI agent kamu:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.1.6), skor 1–10: tanpa skill **7,25** → dengan skill **8,25** (LULUS, selisih tipis). Contoh September dari rekap WA: **Andi 99,8 · Sari 107,2 · Budi 75,6 · Joko 74,6** (script tertimbang; cap 120%). Sumber: `examples/00-openclaw-sebelum-sesudah.md`, `promosi/sebelum-sesudah.jsonl`.

**Status uji (jujur):** sudah diuji OpenClaw sebelum/sesudah otomatis (2026-10-01) + muat CLI. Claude Code (simulasi agent). Dasbor Datasette/Grist opsional belum diuji di semua platform. Codex/Cursor belum uji platform asli.

## FAQ
**Apakah skor KPI ini bisa dipakai untuk memecat atau memotong gaji karyawan?**
Tidak. Skor ini bahan diskusi dan pembinaan. Sebelum keputusan kepegawaian, dengarkan penjelasan karyawan, periksa hambatan di luar kendalinya, dan ikuti peraturan perusahaan serta UU Ketenagakerjaan. Untuk surat peringatan, gunakan skill `surat-peringatan-karyawan`. Untuk sengketa, konsultasikan ke HR atau konsultan hukum.

**Data kinerja karyawan disimpan di mana, dan siapa yang bisa melihat?**
Di folder kerja pada mesin yang menjalankan OpenClaw (komputer atau VPS milik Anda), path-nya disebut sebelum file ditulis. Script tidak mengirim data ke mana pun. Agen AI membaca data KPI saat bekerja, dan laporan Telegram hanya berisi skor yang Anda pilih untuk dikirim. Laporan per orang disarankan hanya untuk pemilik/manajer. Untuk grup kantor tersedia mode tanpa nama (skor perusahaan & divisi saja). Daftar orang diurutkan per divisi dan nama, bukan peringkat, supaya tidak ada yang dipermalukan.

**Tim saya belum punya target. Apakah target di template bisa langsung dipakai?**
Target di katalog hanya contoh. Target yang adil berasal dari data 3 bulan terakhir usahamu, ditambah kenaikan wajar, dan dibicarakan dengan orangnya. Kalau belum ada data, pakai bulan pertama untuk mengukur saja, lalu pasang target di bulan berikutnya.

## Riwayat perubahan

Versi terkini: **1.1.6**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
