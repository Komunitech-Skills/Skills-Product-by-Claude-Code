# KPI Tim: Target Jelas, Skor Dihitung Otomatis

**Target per orang dan per divisi, skor pencapaian hijau/kuning/merah yang dihitung benar, dari Excel, Google Sheets, atau rekap grup WA. Tanpa aplikasi berlangganan.**

## Manfaat
- ✅ **Tidak bingung lagi "KPI apa yang cocok".** Ada katalog KPI siap pakai untuk 9 peran yang umum di UMKM: sales, CS, produksi, gudang, keuangan, marketing, admin, kurir, dan kasir. Setiap KPI dilengkapi rumus, satuan, arah (makin tinggi atau makin rendah makin baik), dan sumber datanya.
- ✅ **Template Excel/Google Sheets jadi dalam semenit.** Sebutkan nama, divisi, dan peran tim. AI membuat file rencana KPI (bobot sudah 100%, target contoh, lembar petunjuk) dan lembar isian realisasi.
- ✅ **Rekap grup WA langsung jadi angka.** Tempel pesan seperti "Andi closing 14 deal, target 15, omzet 162 jt". AI menyusunnya jadi tabel draf untuk kamu cek dulu, tanpa perlu mengetik ulang.
- ✅ **Skor dihitung script, bukan dikira.** KPI "makin rendah makin baik" (komplain, reject, telat) dihitung dengan rumus yang benar. Capaian dibatasi 120% supaya satu KPI tidak menutupi yang lain. Hasilnya berupa skor tertimbang per orang, divisi, dan perusahaan, lengkap dengan tren dibanding bulan lalu.
- ✅ **Dasbor KPI di komputermu sendiri.** Riwayat skor semua bulan disimpan ke satu file database, lalu bisa dilihat di browser (Datasette lewat skill `dasbor-lokal`) atau diimpor ke Grist: perusahaan → divisi → orang, tren per bulan, dan daftar KPI merah. Ada mode **anonim** untuk layar bersama: nama diganti kode, divisi kecil digabung, dan orang yang bisa ditebak dari daftar KPI-nya tidak ditampilkan per orang. Tanpa software baru, tanpa langganan.
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
- Data berupa file di komputermu sendiri: CSV atau Excel (.xlsx). Untuk Google Sheets: unduh sebagai .xlsx/.csv, lalu impor kembali template yang dibuat AI.
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

Panduan lengkap (termasuk Windows): lihat `CARA-INSTAL.md` di dalam paket.

## FAQ
**Apakah skor KPI ini bisa dipakai untuk memecat atau memotong gaji karyawan?**
Tidak. Skor ini bahan diskusi dan pembinaan. Sebelum keputusan kepegawaian, dengarkan penjelasan karyawan, periksa hambatan di luar kendalinya, dan ikuti peraturan perusahaan serta UU Ketenagakerjaan. Untuk surat peringatan, gunakan skill `surat-peringatan-karyawan`. Untuk sengketa, konsultasikan ke HR atau konsultan hukum.

**Data kinerja karyawan disimpan di mana, dan siapa yang bisa melihat?**
Di komputermu sendiri. Script tidak mengirim data ke mana pun. Laporan per orang disarankan hanya untuk pemilik/manajer. Untuk grup kantor tersedia mode tanpa nama (skor perusahaan & divisi saja). Daftar orang diurutkan per divisi dan nama, bukan peringkat, supaya tidak ada yang dipermalukan.

**Tim saya belum punya target. Apakah target di template bisa langsung dipakai?**
Target di katalog hanya contoh. Target yang adil berasal dari data 3 bulan terakhir usahamu, ditambah kenaikan wajar, dan dibicarakan dengan orangnya. Kalau belum ada data, pakai bulan pertama untuk mengukur saja, lalu pasang target di bulan berikutnya.

## Riwayat versi
| Versi | Tanggal | Perubahan |
|---|---|---|
| 1.1.2 | 2026-09-29 | Perbaikan uji ulang independen v1.1.1 (7/10): **supresi komplementer** di `ekspor-db --anonim`. Dalam satu divisi/kelompok, baris per orang diekspor untuk SEMUA anggota atau tidak sama sekali, sehingga orang yang disembunyikan tidak bisa dihitung balik (mis. 4 × skor divisi − jumlah 3 orang yang tampil). Angka tidak dibulatkan/diacak, hanya disembunyikan. Tes regresi mereproduksi serangan itu dan membuktikannya gagal. 49 tes regresi. |
| 1.1.1 | 2026-09-29 | Perbaikan uji ulang independen v1.1.0 (8/10). **Privasi dasbor:** `ekspor-db --anonim` kini menerapkan k-anonimitas (`--k-anonim`, default 3): divisi kurang dari 3 orang digabung jadi "Lainnya", baris per orang hanya diekspor bila minimal 3 orang di kelompoknya punya daftar KPI yang sama, target/ambang/realisasi per orang dikosongkan. Nama KPI + jumlah orang tidak lagi bisa menunjuk satu orang (dibuktikan tes regresi). `--k-anonim 1` = perilaku lama (hanya kode) dengan peringatan. Riwayat versi dirapikan. 48 tes regresi. Uji ulang independen: 7/10 karena serangan selisih, diperbaiki di 1.1.2. |
| 1.1.0 | 2026-09-29 | **Dasbor KPI tanpa software baru.** Perintah `ekspor-db`: rencana + skor + riwayat semua periode ke `kpi.db` (SQLite, dibaca `dasbor-lokal`/Datasette read-only), `kpi-metadata.yml` (query siap klik: perusahaan per periode, divisi & orang periode terbaru, tren per orang, KPI merah), opsi `--grist` (CSV per tabel + petunjuk impor), mode `--anonim`/`--anonim-divisi` (kode acak, kunci terpisah, kode stabil antar ekspor), peringatan dasbor hanya 127.0.0.1. Diuji dengan Datasette 0.65.5 asli. Termasuk perubahan 1.0.2. Uji ulang independen 2026-09-29: 8/10, 45/45 tes, 0 beda angka vs `skor`; temuan privasi mode anonim diperbaiki di 1.1.1. |
| 1.0.2 | 2026-09-29 | Tidak dirilis terpisah (digabung ke 1.1.0). Sisa temuan uji ulang v1.0.1. **Teks WA:** "Wulan & Rudi void masing2 1" kini jadi draf untuk keduanya; tanpa kata "masing-masing" ditanyakan (per orang atau total?), tidak ada nama yang hilang diam-diam. **Angka konsisten:** "(dihitung dari 50,5% bobot)" memakai presisi yang sama dengan ⚠️. **Mode nol:** "perlu perhatian" menunjuk KPI tanpa data yang bobotnya paling besar (+ jumlah KPI kosong lain). **Privasi:** di `--tanpa-nama`, divisi yang hanya berisi 1 orang dinilai digabung dengan divisi lain (atau disembunyikan) agar skor pribadi tidak terbaca. Diverifikasi pada uji ulang independen 1.1.0. |
| 1.0.1 | 2026-09-29 | Perbaikan dari uji independen v1.0.0 (8/10). **Privasi:** `--tanpa-nama` tidak lagi menyebut nama di mana pun (teks "(1 orang belum lengkap)", JSON tanpa daftar nama/rata-rata individu, peringatan per orang diganti hitungan). **Angka minus:** `Rp -5.000.000`, `-Rp5jt`, `(5.000.000)` dibaca minus; sufiks jt/rb/miliar. **Rencana lintas bulan:** template mengisi periode `2026-10..` (berlaku mulai), kolom periode menerima rentang `2026-10..2026-12`; ⚠️ bila tren tidak bisa dihitung atau periode sebelumnya tidak ada. **Teks WA:** `4,4x` → 4,4, `Rp12rb` → 12.000, target/rencana ke depan dan libur/izin/sakit masuk "tidak terbaca", tanda CEK untuk satuan beda/beberapa orang/angka minus, tidak ada baris bernama/ber-KPI yang dilewati diam-diam. Perbaikan kecil: tidak ada capaian persen minus di laporan, "perlu perhatian" menunjuk KPI kosong di mode `nol`, ⚠️ untuk orang yang tetap belum lengkap di `bobot-ulang`, ⚠️ komposisi divisi berbeda saat tren, ⚠️ capaian tidak wajar, hanya `status_draf` kosong/dikonfirmasi yang dihitung, label "capaian … poin" di rincian 1:1, tanpa traceback saat output dipotong. 29 tes regresi. |
| 1.0.0 | 2026-09-29 | Rilis awal: katalog KPI 9 peran, template CSV/XLSX, baca-teks, rekap-log, skor tertimbang, OKR ringan, laporan Telegram & bahan 1:1. |
