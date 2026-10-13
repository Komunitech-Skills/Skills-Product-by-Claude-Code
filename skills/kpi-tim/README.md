# KPI Tim: Target Jelas, Skor Dihitung Otomatis

**Target kinerja (KPI) per orang dan per divisi, skor pencapaian hijau/kuning/merah yang dihitung benar, dari Excel, Google Sheets (lewat unduh .xlsx/.csv), atau rekap grup WA. Tanpa aplikasi berlangganan.**

*Diuji AI penguji independen di OpenClaw: 7,25 → 8,25 dari 10 (selisih tipis; pembeda: rekap grup WA langsung jadi skor tertimbang per orang dengan aturan yang sama tiap bulan, tanpa peringkat yang mempermalukan karyawan).*

> **Yang Anda butuhkan:** AI agent yang mendukung skill (OpenClaw, Claude Code, Codex, atau Cursor — langganan AI-nya ditanggung sendiri) di komputer Windows/Mac/Linux. Python 3 (bawaan Mac/Linux, unduh gratis di Windows) untuk skrip hitung; tanpa Python skill tetap berjalan dengan hitungan oleh AI. Software tambahan (opsional, hanya untuk dasbor di browser): Datasette atau Grist (gratis, open-source; panduan pemasangan disertakan). Tidak perlu API key atau akun tambahan dari Komunitech.

## Manfaat
- ✅ **Tidak bingung lagi "KPI apa yang cocok".** Ada katalog KPI siap pakai untuk 9 peran yang umum di UMKM: sales, CS, produksi, gudang, keuangan, marketing, admin, kurir, dan kasir. Setiap KPI dilengkapi rumus, satuan, arah (makin tinggi atau makin rendah makin baik), dan sumber datanya.
- ✅ **Template Excel jadi dalam hitungan menit.** Sebutkan nama, divisi, dan peran tim. AI membuat file rencana KPI (bobot sudah 100%, target contoh, lembar petunjuk) dan lembar isian realisasi.
- ✅ **Rekap grup WA langsung jadi angka.** Tempel pesan seperti "Andi closing 14 deal, target 15, omzet 162 jt". AI menyusunnya jadi tabel draf untuk Anda cek dulu, tanpa perlu mengetik ulang.
- ✅ **Skor dihitung skrip, bukan dikira.** KPI "makin rendah makin baik" (komplain, reject, telat) dihitung dengan rumus yang benar. Capaian dibatasi 120% supaya satu KPI tidak menutupi yang lain. Hasilnya berupa skor tertimbang per orang, divisi, dan perusahaan, lengkap dengan tren dibanding bulan lalu.
- ✅ **Dasbor KPI (tampilan ringkasan angka di layar) dari file lokal, opsional.** Riwayat skor semua bulan disimpan ke satu file data di komputer Anda, lalu bisa dilihat di browser (lewat Datasette, penampil data gratis, dibantu skill Komunitech lain bernama `dasbor-lokal`) atau diimpor ke Grist (aplikasi tabel seperti spreadsheet): perusahaan → divisi → orang, tren per bulan, dan daftar KPI merah. Ada mode **anonim** untuk layar bersama: nama diganti kode, divisi kecil digabung, dan orang yang bisa ditebak dari daftar KPI-nya tidak ditampilkan per orang (pada tim sangat kecil, tetap hati-hati sebelum menampilkannya ke orang lain). Laporan teks tidak butuh software baru; dasbor di browser butuh Datasette (gratis).
- ✅ **Laporan siap kirim dan bahan obrolan satu lawan satu.** Ringkasan untuk Telegram pemilik (bisa dijadwalkan otomatis lewat OpenClaw; jadwal otomatis belum diuji langsung), rincian per orang untuk obrolan satu lawan satu (1:1), dan OKR ringan (target kuartalan berupa tujuan beserta ukuran hasilnya).

## Cocok untuk siapa
- Pemilik distributor, toko, pabrik kecil, konveksi, klinik, atau agensi dengan 3–30 karyawan
- Manajer/supervisor yang selama ini merekap target tim secara manual di Excel
- Usaha yang laporan hariannya masih lewat grup WA atau kertas
- Pemilik yang tidak mau data kinerja karyawannya disimpan di server pihak lain (data disimpan di komputer Anda; lihat FAQ soal AI agent)

## Contoh sebelum & sesudah
**Sebelum:** target ada di kepala pemilik, angka tersebar di grup WA dan beberapa file Excel. Menghitung manual rawan keliru. Contohnya KPI "salah kirim, target 3, realisasi 6": tanpa rumus yang disepakati, capaiannya bisa tertulis 200% ("6 dari 3") atau 50% (3 ÷ 6). Keduanya menyesatkan. Karyawan yang datanya belum masuk juga bisa dianggap nol.

**Sesudah:** "Ini rekap grup WA akhir September, hitung KPI tim saya."
→ AI menunjukkan 9 baris draf dari chat untuk dicek. Setelah Anda balas "ok", keluar laporan:
```
📊 *KPI CV Sumber Makmur Distribusi — 2026-09*
Perusahaan: 🟡 93,6 (▲6,3 vs 2026-08) — sebagian
…
🟡 Gudang & Pengiriman: 91,7 ▼4,2
🟡 Keuangan & Admin: 93,1 ▲17,6 (tanpa Tono Wijaya)
🟡 Sales: 96,1 ▲5,6
…
🔴 Joko Susilo (Gudang & Pengiriman): 76,7 ▼15,1 — perlu perhatian: Salah kirim 0,0%
⚪ Tono Wijaya (Keuangan & Admin): belum lengkap — belum ada data: Nota diarsip lengkap
…
```
Salah kirim 6 dari target 3 dihitung (2 − 6/3) × 100 = 0%. Tono tidak otomatis dianggap gagal karena datanya belum masuk. Tono ditandai "belum lengkap", dan aturan ini tertulis jelas.
(Contoh dengan data fiktif dari `examples/contoh-distributor.md`, dipotong.)

## Cara pakai
Cukup ketik ke AI agent Anda, misalnya:
- "KPI apa yang cocok untuk admin gudang dan kurir?"
- "Buatkan template KPI untuk tim saya: Andi & Rina sales, Dewi CS, Budi gudang."
- "Ini rekap grup WA, masukkan jadi realisasi KPI September."
- "Hitung skor KPI September dari file ini, bandingkan dengan Agustus."
- "Siapkan bahan 1:1 untuk Joko."
- "Buat OKR kuartal 4 untuk divisi sales."
- "Buatkan dasbor KPI dari data ini, tanpa nama karyawan." / "Siapkan file KPI untuk diimpor ke Grist."
- "Kirim laporan KPI ke Telegram saya tiap tanggal 2 jam 7 pagi." (OpenClaw; jadwal otomatis belum diuji langsung)

## Syarat
- Python 3.8 atau lebih baru (di Mac/Linux biasanya sudah ada; di Windows pasang gratis dari python.org). Tidak perlu internet, akun, API key, atau instalasi paket.
- Data berupa file di folder kerja yang Anda sepakati dengan AI (AI menyebutkan lokasi lengkap file-nya; bukan folder sementara /tmp): CSV atau Excel (.xlsx). Untuk Google Sheets: unduh sebagai .xlsx/.csv, lalu impor kembali template yang dibuat AI.
- Jadwal otomatis ke Telegram hanya untuk OpenClaw (belum diuji langsung), dan komputer harus menyala saat jam jadwal.

## Dasbor KPI (opsional)
Setelah rencana dan realisasi siap, minta: **"Buatkan dasbor KPI-nya."** AI menyiapkan folder berisi file data dasbor (`kpi.db` dan `kpi-metadata.yml`, serta file CSV untuk Grist bila diminta). Membukanya di browser butuh Datasette (gratis, panduan: `docs/panduan-datasette.md`); yang sudah memakai Grist cukup mengimpor CSV (`docs/panduan-grist.md`). Tanpa keduanya, laporan teks tetap jalan. Datasette sudah diuji pada versi 0.65.5; untuk Grist, yang diuji baru pembuatan file CSV-nya, belum impor ke aplikasi Grist.

**Penting soal privasi:** dasbor hanya boleh dibuka di komputer ini (alamat `127.0.0.1`, artinya komputer Anda sendiri), tidak ke internet, tidak ke HP/kantor cabang lain, dan filenya jangan dibagikan. Skor per orang adalah data pribadi karyawan. Kalau perlu ditampilkan ke orang lain, minta **mode anonim**; daftar "kode = nama" disimpan terpisah (`kunci-kode-RAHASIA.csv`).

## Instalasi singkat
Salin folder `kpi-tim` ke folder skills AI agent Anda:

| Platform | Folder tujuan |
|---|---|
| OpenClaw | `~/.openclaw/skills/` |
| Codex | `~/.agents/skills/` |
| Claude Code | `~/.claude/skills/` |
| Cursor | `~/.cursor/skills/` |

Panduan lengkap (termasuk Windows): lihat `docs/instalasi.md` yang disertakan dalam paket.

**Hasil uji (angka nyata):** uji OpenClaw otomatis agent, Okt 2026 (v1.1.6), skor 1–10: tanpa skill **7,25** → dengan skill **8,25** (LULUS, selisih tipis). Contoh September dari rekap WA pada uji itu: **Andi 99,8 · Sari 107,2 · Budi 75,6 · Joko 74,6** (skrip tertimbang; batas 120%); datanya berbeda dari contoh distributor di atas. Sumber skor: `examples/00-openclaw-sebelum-sesudah.md`.

**Status uji (jujur):** sudah diuji OpenClaw sebelum/sesudah otomatis (2026-10-01) + muat CLI. Claude Code (simulasi agent). Dasbor Datasette diuji oleh penguji terpisah (bukan lewat OpenClaw); Grist hanya sampai file CSV. Jadwal Telegram belum diuji langsung. Codex/Cursor belum uji platform asli.

## FAQ
**Apakah skor KPI ini bisa dipakai untuk memecat atau memotong gaji karyawan?**
Tidak. Skor ini bahan diskusi dan pembinaan. Sebelum keputusan kepegawaian, dengarkan penjelasan karyawan, periksa hambatan di luar kendalinya, dan ikuti peraturan perusahaan serta UU Ketenagakerjaan. Untuk surat peringatan, gunakan skill Komunitech lain untuk menyusun surat peringatan karyawan (`surat-peringatan-karyawan`). Untuk sengketa, konsultasikan ke HR atau konsultan hukum.

**Data kinerja karyawan disimpan di mana, dan siapa yang bisa melihat?**
Di folder kerja pada mesin yang menjalankan OpenClaw (komputer atau VPS, yaitu server sewaan, milik Anda), path-nya disebut sebelum file ditulis. Script tidak mengirim data ke mana pun. Agen AI membaca data KPI saat bekerja, dan laporan Telegram hanya berisi skor yang Anda pilih untuk dikirim. Laporan per orang disarankan hanya untuk pemilik/manajer. Untuk grup kantor tersedia mode tanpa nama (skor perusahaan & divisi saja). Daftar orang diurutkan per divisi dan nama, bukan peringkat, supaya tidak ada yang dipermalukan.

**Tim saya belum punya target. Apakah target di template bisa langsung dipakai?**
Target di katalog hanya contoh. Target yang adil berasal dari data 3 bulan terakhir usaha Anda, ditambah kenaikan wajar, dan dibicarakan dengan orangnya. Kalau belum ada data, pakai bulan pertama untuk mengukur saja, lalu pasang target di bulan berikutnya.

## Riwayat perubahan

Versi terkini: **1.1.7**. Rincian teknis tiap versi ada di `CHANGELOG.md` di folder skill ini.
