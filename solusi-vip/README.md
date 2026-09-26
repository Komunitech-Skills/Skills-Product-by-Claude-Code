# Solusi Member VIP per Profesi (OpenClaw)

Ini adalah **jalur kerja 3** dari `CLAUDE.md`: paket siap pakai untuk member VIP komunitech.com,
yang **semuanya sudah memakai OpenClaw**. Setiap paket = (skill dari library) + (konfigurasi
OpenClaw yang sudah diverifikasi) + (panduan langkah demi langkah bahasa awam).

Dasar rancangan: `research/solusi-member-vip-2026-09-23.md` dan
`research/kebutuhan-member-vip-2026-09-23.md`. **Tidak ada data pribadi member di folder ini**,
hanya panduan generik.

**Status per 2026-09-24:** semua skill di bawah berstatus `lulus` di `catalog.csv` (lulus uji
Tahap 6), **belum** `rilis` dan **belum** punya `tier_final`/`harga_final_idr` — keduanya
diisi pemilik (lihat Tahap 7 `CLAUDE.md`). Folder ini adalah **materi panduan**, bukan penentu
harga atau status jual.

## Tiga paket

| Paket | Untuk siapa | Isi (skill) |
|---|---|---|
| `toko-online/` | Seller marketplace & toko online (offline + online) | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. Bundle tematik (`bundles/paket-toko-online.txt`): `listing-marketplace`, `harga-jual-marketplace`, `balas-ulasan-pelanggan`, `analisis-ulasan`, `promo-kalender`, `naskah-live-jualan`, `buku-stok`, `agen-cs-toko`, `foto-produk-brief`. Otomasi tambahan (akses penuh VIP): `laporan-otomatis-terjadwal` + `rekap-penjualan-csv` (laporan harian 21.00), `konten-mingguan` (paket konten mingguan) |
| `klinik/` | Klinik pratama/gigi/kecantikan/fisioterapi, praktik dokter/bidan mandiri | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. Bundle tematik (`bundles/paket-klinik.txt`): `edukasi-pasien-klinik`, `agen-cs-toko`, `balas-ulasan-pelanggan`, `konten-mingguan`, `laporan-status-kantor` |
| `konsultan/` | Konsultan, agensi, freelancer B2B | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. Bundle tematik (`bundles/paket-konsultan-freelancer.txt`): `proposal-kerjasama`, `surat-penawaran-harga`, `buat-invoice`, `tagih-piutang`, `pengingat-follow-up`, `riset-calon-pelanggan`, `asisten-tulis-riset`, `presentasi-instan` |

Kenapa lebih banyak dari isi bundle ecer di masing-masing `.txt`: member **VIP** (beda dari
pembeli ecer/bundle) punya **akses penuh ke seluruh library** (Bab 1 `CLAUDE.md`), jadi paket
solusinya menambahkan skill otomasi lintas-profesi (`laporan-otomatis-terjadwal`,
`konten-mingguan`, dll.) yang tidak selalu ada di file `.txt` bundle ecer tematik.

Setiap subfolder paket berisi:
- **`PANDUAN.md`** — langkah demi langkah dari nol sampai jalan (prasyarat → pasang skill →
  starter kit → cek privasi → hubungkan Telegram → rutinitas harian/mingguan profesi itu).
  Setiap langkah punya "cara cek berhasil" dan "kalau gagal".
- **`jadwal-openclaw.md`** — daftar jadwal (`openclaw automations`) siap salin untuk profesi itu,
  dengan tanda jelas mana yang **terverifikasi lewat CLI OpenClaw asli** (✅/📖) dan mana yang
  **belum** (⚠️) — lihat metodologi di bawah.
- **`CEKLIS.md`** — ceklis serah-terima satu halaman untuk member atau teknisi jasa setup,
  termasuk poin privasi.

## Aturan yang dipatuhi ketiga paket (keputusan pemilik, 2026-09-23)

1. **Telegram (bot resmi) = kanal default** untuk semua laporan/rekap/pengingat ke pemilik usaha.
2. **WhatsApp** hanya boleh dipakai untuk notifikasi ke pemilik **sendiri**, dengan **nomor
   terpisah** (bukan nomor toko/klinik/CS), dan **persetujuan risiko tertulis** — teks
   persetujuannya ada di tiap `PANDUAN.md`.
3. **Agen CS di WA = mode Copilot**: AI menyiapkan draf balasan, **manusia yang mengirim**. Tidak
   ada auto-reply otomatis ke pelanggan dari paket ini.
4. **Tidak ada broadcast/kirim massal** lewat OpenClaw di paket mana pun.
5. **Mesin 24 jam**: setiap `PANDUAN.md` menjelaskan tiga opsi (laptop/PC kerja yang memang
   menyala di jam laporan, mini PC/laptop bekas khusus, atau VPS milik member) dan menyebut
   **jasa setup berbayar Komunitech** sebagai opsi tanpa mencantumkan harga.
6. **Klinik**: hanya edukasi pasien, balasan chat umum non-diagnosis, dan laporan operasional
   agregat (tanpa nama/diagnosis pasien). **Tidak ada** skrining/diagnosis/kalkulator medis.
7. **Kripto**: sengaja **tidak** dimasukkan ke paket manapun di sini — menunggu keputusan pemilik
   (lihat §5 `research/solusi-member-vip-2026-09-23.md`).

## Metodologi verifikasi perintah OpenClaw

Perintah di `jadwal-openclaw.md` diambil dari `references/openclaw*.md` skill terkait, yang
sebagian besar **sudah diuji sungguhan** terhadap Gateway OpenClaw lokal (2026.9.5/2026.9.6,
`gateway run --dev --allow-unconfigured --bind loopback`, tanpa model AI & tanpa kanal login).
Untuk sesi ini, tambahan verifikasi dilakukan dengan menjalankan `bash scripts/uji_openclaw.sh
2026.9.6` (memasang OpenClaw 2026.9.6 ke `/tmp/uji-openclaw`) lalu membandingkan setiap flag yang
dipakai di paket ini terhadap `openclaw automations add --help` dan `openclaw channels add --help`
sungguhan. Hasil: **semua flag yang dipakai di ketiga paket (`--cron`/posisi, `--tz`, `--name`,
`--session`, `--announce`, `--channel`, `--to`, `--tools`, `--at`, `--best-effort-deliver`,
`--model`, `--delete-after-run`) ada persis** di `--help` OpenClaw 2026.9.6 — tidak ada flag yang
sudah berubah/hilang sejak dokumen sumbernya ditulis. Uji muat skill (`openclaw skills check
--json`) juga dijalankan ulang: 53/53 skill di repo `eligible`/`modelVisible`/`commandVisible`.

Legenda yang dipakai di `jadwal-openclaw.md`:
- ✅ = perintah ini (atau flag-flag intinya) **benar-benar dijalankan** terhadap Gateway OpenClaw
  nyata oleh tim kurasi (dicatat di `references/openclaw*.md` skill sumber).
- 📖 = flag/perintah **dicek lewat `--help`/`config schema`** (termasuk verifikasi ulang sesi ini),
  tapi kombinasi utuhnya (terutama pengiriman sungguhan ke Telegram/WhatsApp) belum dicoba.
- ⚠️ = **belum diverifikasi** — dijelaskan jujur ke pembeli sebagai "coba, kalau gagal pakai
  Control UI/terminal".

Tidak ada perintah baru yang ditebak untuk paket ini — semua diturunkan dari perintah yang sudah
ada di `references/openclaw*.md` skill terkait.

## Celah (skill yang dibutuhkan tapi belum ada di repo)

1. **Laporan iklan mingguan (Meta/TikTok Ads)** — disebut di riset (`laporan-iklan-mingguan`,
   prioritas 9) untuk toko online yang beriklan, tapi skill-nya **belum dibuat**. Sampai ada,
   `PANDUAN.md` toko-online tidak menjanjikannya.
2. **Pengingat kontrol/vaksin pasien terjadwal (klinik)** — `edukasi-pasien-klinik` bisa
   *menyusun teks* pengingat kontrol, tapi tidak ada skill/pola otomasi terjadwal per-pasien
   seperti `pengingat-follow-up` untuk klinik (menyimpan tanggal per pasien di CSV lokal berisiko
   melanggar prinsip minimal data pasien tanpa dasar hukum jelas). **Usulan**: skill baru
   `pengingat-kontrol-klinik` yang hanya menyimpan **kode/inisial + tanggal + jenis kontrol**
   (bukan nama lengkap/diagnosis), dengan persetujuan tertulis pasien untuk diingatkan — perlu
   keputusan pemilik & tinjauan hukum (UU PDP, data kesehatan = data pribadi spesifik).
3. **Laporan status ke klien (konsultan)** — `pengingat-follow-up` sudah menjadwalkan rekap
   follow-up/piutang/timesheet ke **pemilik**, tapi belum ada pola siap-pakai untuk laporan
   status proyek **ke klien** secara terjadwal (mis. mingguan). Sampai ada, `jadwal-openclaw.md`
   konsultan hanya menjadwalkan rekap ke pemilik; laporan ke klien tetap disusun manual dengan
   `laporan-status-kantor`/`proposal-kerjasama` lalu dikirim manual oleh pemilik.
4. **Integrasi WABA resmi (Level 3 CS)** disebut di riset sebagai "jasa setup", bukan skill —
   tidak ada celah skill di sini, hanya dicatat sebagai batas cakupan paket ini.

## Usulan perubahan `scripts/build.py` (TIDAK diubah di sesi ini)

`build.py` saat ini hanya menyalin skill dari `skills/<nama>/` ke ZIP (lihat `pilih_skill()` dan
penyalinan folder skill). Untuk menyertakan `solusi-vip/<paket>/` ke dalam ZIP paket, usulan
(perlu review pemilik/pemelihara `build.py`):
- Tambah argumen opsional `--sertakan-panduan-vip <folder>` (mis.
  `solusi-vip/toko-online`) yang menyalin `PANDUAN.md`, `jadwal-openclaw.md`, `CEKLIS.md` ke root
  ZIP (sejajar dengan `LISENSI.txt`/`docs/instalasi.md`), **hanya** jika `a.vip` dipakai (paket ini
  untuk member VIP, bukan pembeli ecer/bundle biasa).
- Atau: perlakukan `solusi-vip/<paket>/` sebagai "bundle khusus VIP" tambahan — baca daftar skill
  dari nama paket, gabungkan dengan salinan tiga file panduannya, mirip alur `--bundle` yang sudah
  ada tapi menambah file non-skill ke root ZIP.
- Perlu keputusan: apakah panduan ini dijual sebagai bagian ZIP tiap paket VIP, atau dikirim
  terpisah (mis. lewat member area/PDF) di luar `build.py`. Tidak diubah tanpa persetujuan pemilik
  sesuai `CLAUDE.md` §5 ("Tanyakan ke pemilik sebelum ... menginstal paket/dependensi baru" dan
  larangan mengubah struktur packaging tanpa arahan).

## Privasi (ringkas — detail penuh di tiap `PANDUAN.md`)

- Data tetap di komputer/mesin milik member (`~/.openclaw`), bukan di server Komunitech.
- Isi pesan yang diproses tetap dikirim ke penyedia model AI pilihan member (Anthropic/OpenAI/
  Google, dll.) kecuali memakai model lokal.
- Tidak pernah menyimpan nama/kontak pelanggan atau pasien di file panduan ini — hanya di
  workspace lokal member sendiri, seminimal mungkin, sesuai UU PDP.
