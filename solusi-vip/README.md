# Solusi Member VIP per Profesi (OpenClaw)

Ini adalah **jalur kerja 3** dari `CLAUDE.md`: paket siap pakai untuk member VIP komunitech.com,
yang **semuanya sudah memakai OpenClaw**. Setiap paket = (skill dari library) + (konfigurasi
OpenClaw yang sudah diverifikasi) + (panduan langkah demi langkah bahasa awam).

Dasar rancangan: `research/solusi-member-vip-2026-09-23.md` dan
`research/kebutuhan-member-vip-2026-09-23.md`. **Tidak ada data pribadi member di folder ini**,
hanya panduan generik.

**Status skill:** lihat `catalog.csv` (banyak skill inti sudah `beta`/`lulus` per 2026-10-14).
Folder ini adalah **materi panduan**, bukan penentu harga — harga bundle ecer di
`bundles/README.md` dan `harga_final_idr` di katalog.

## Enam paket

| Paket | Untuk siapa | Isi (skill) |
|---|---|---|
| `toko-online/` | Seller marketplace & toko online (offline + online) | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. Bundle ecer **16 skill** (`bundles/paket-toko-online.txt`, rincian di `bundles/README.md`): listing/harga/ulasan/promo/live, stok, CS toko & foto, piutang, picking, dasbor, SOP, `balas-chat-cs`, `crm-wa`, `rencana-restok-barang`. Otomasi tambahan (akses penuh VIP), lihat `toko-online/PANDUAN.md` §5: `laporan-otomatis-terjadwal` + `rekap-penjualan-csv` (laporan harian 21.00), `konten-mingguan`, `pesan-prospek-wa` (prospek harian; `crm-wa` sudah di bundle), `analisis-excel`, `kas-umkm`, `laporan-iklan-mingguan`. Tambahan opsional (§5m): `program-referral-loyalitas`, `iterasi-dari-masukan-pelanggan`, `umami-analitik`, `listmonk-newsletter`, `luncurkan-produk-baru`, `uji-pasar-produk-cepat`, `studio-video-pendek-ai` |
| `klinik/` | Klinik pratama/gigi/kecantikan/fisioterapi, praktik dokter/bidan mandiri | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. Bundle tematik (`bundles/paket-klinik.txt`): `edukasi-pasien-klinik`, `agen-cs-toko`, `balas-chat-cs`, `balas-ulasan-pelanggan`, `konten-mingguan`, `laporan-status-kantor`, `pengingat-pasien-klinik`. **Wajib:** blok aturan kerja + aturan klinik di `AGENTS.md` (`klinik/PANDUAN.md` §1a). Otomasi tambahan (akses penuh VIP), lihat `klinik/PANDUAN.md` §5i: `pengingat-pasien-klinik` (buku jadwal kontrol/vaksin lokal minimal, draf WA disalin staf, ringkasan terjadwal 07.30 WIB). Tambahan opsional (§5j): `program-referral-loyalitas` (versi tanpa imbalan rujukan, PERLU REVIEW), `iterasi-dari-masukan-pelanggan` |
| `konsultan/` | Konsultan, agensi, freelancer B2B | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. Bundle tematik (`bundles/paket-konsultan-freelancer.txt`): `proposal-kerjasama`, `surat-penawaran-harga`, `buat-invoice`, `tagih-piutang`, `pengingat-follow-up`, `riset-calon-pelanggan`, `asisten-tulis-riset`, `presentasi-instan`. Otomasi tambahan (akses penuh VIP), lihat `konsultan/PANDUAN.md` §5: `hledger-usaha` (pembukuan berpasangan freelancer/agensi tanpa aplikasi berbayar, bulanan tgl 1), `buku-piutang` (invoice retainer/termin yang belum lunas, harian 07.45), `gaji-umkm` (opsional, bila agensi punya staf tetap, pengingat harian 07.00), `laporan-klien-konsultan` (draf laporan progres mingguan ke klien, Jumat 16.00 — draf saja, dikirim manual). Tambahan opsional (§5o, manual): `strategi-merek-usaha`, `positioning-persona-usaha`, `analisis-pesaing-strategis`, `strategi-harga-produk`, `rencana-marketing-usaha` |
| `usaha-offline/` | Kafe/resto/warung makan, warung/toko kelontong, bengkel, laundry — usaha tatap muka | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. Paket VIP lengkap (16 skill inti, `usaha-offline/PANDUAN.md` §1): kasir, stok, kas, absensi, gaji, laporan harian, piutang, HPP, PPh final, CS, promo, laporan terjadwal. Bundle ecer tematik **10 skill** (`bundles/paket-kafe-warung.txt`): `kasir-lokal`, `buku-stok`, `hitung-hpp`, `konten-mingguan`, ulasan/promo, `kas-umkm`, `dasbor-lokal`, `rencana-restok-barang`, `bandingkan-pemasok-vendor`. Tambahan opsional VIP (§5m): `program-referral-loyalitas`, `strategi-harga-produk`, `iterasi-dari-masukan-pelanggan`, `rencana-marketing-usaha` |
| `kantor-manajemen/` | Direktur/manajer manufaktur, distribusi, logistik, kantor besar (16–50+ staf) | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. Bundle ecer `bundles/paket-kantor-manajemen.txt` (subset, lihat `bundles/README.md`): `laporan-otomatis-terjadwal`, `laporan-status-kantor`, `ringkas-grup-wa`, `vikunja-tugas`, `notulen-rapat`, `analisis-excel`, `analisis-rasio-keuangan-usaha`, `arus-kas-13minggu`, `presentasi-data-ke-atasan`, `dasbor-lokal`, `buku-piutang`, `tagih-piutang`, `buku-stok`, `laporan-insiden-usaha`. Tambahan akses penuh VIP: `laporan-harian-usaha` (laporan harian 21.00 & mingguan Senin 07.00 ke Telegram), serta `frappe-books-usaha` atau `dolibarr-usaha` (pilih satu; perlu dipasang, tawarkan jasa setup); `odoo-usaha` sebagai pilihan ERP ketiga untuk usaha mapan (§5l2, laporan 21.00). Tambahan VIP: `kpi-tim` (bulanan tgl 2, 07.00) dan `peringatan-dini-operasional` (harian 20.00), keduanya hanya ke pimpinan. Tugas dari grup WA = draf yang dikonfirmasi manusia; pelacakan = daftar tugas, bukan pengawasan karyawan |
| `kripto-keuangan/` | Member yang meriset kripto dan merapikan keuangan pribadi | Starter: `karyawan-ai-mulai`, `cek-privasi-openclaw`. **Khusus VIP** (tanpa bundle ecer). Skill: `atur-keuangan-pribadi`, `notebook-riset-lokal`, `asisten-tulis-riset`, dan inti paket `pantau-pasar-kripto` (ringkasan pagi & notifikasi ambang yang ditetapkan member sendiri, checklist riset, jurnal trading). **Tanpa** auto-trading, rekomendasi beli/jual, atau pembuatan bot |

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

## Aturan yang dipatuhi keenam paket (keputusan pemilik, 2026-09-23)

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
7. **Kripto** (keputusan pemilik 2026-09-23, paket `kripto-keuangan/`): hanya riset, ringkasan
   berita, jurnal trading, dan notifikasi harga dengan ambang yang ditetapkan member sendiri.
   **Tanpa** auto-trading, **tanpa** rekomendasi beli/jual/sinyal, tanpa bot; wajib disclaimer
   bukan nasihat investasi.
8. **Kantor & manajemen** (`kantor-manajemen/`): tugas dari grup WA hanya **draf** yang
   dikonfirmasi manusia; pelacakan = daftar tugas, bukan pengawasan karyawan; aplikasi yang
   perlu dipasang (Frappe Books/Dolibarr/Vikunja) ditawarkan lewat jasa setup berbayar.

## Metodologi verifikasi perintah OpenClaw

Perintah di `jadwal-openclaw.md` diambil dari `references/openclaw*.md` skill terkait, yang
sebagian besar **sudah diuji sungguhan** terhadap Gateway OpenClaw lokal (2026.9.5/2026.9.6,
`gateway run --dev --allow-unconfigured --bind loopback`, tanpa model AI & tanpa kanal login).
Untuk sesi ini, tambahan verifikasi dilakukan dengan menjalankan `bash scripts/uji_openclaw.sh
2026.9.6` (memasang OpenClaw 2026.9.6 ke `/tmp/uji-openclaw`) lalu membandingkan setiap flag yang
dipakai di paket ini terhadap `openclaw automations add --help` dan `openclaw channels add --help`
sungguhan. Hasil: **semua flag yang dipakai di paket-paket ini (`--cron`/posisi, `--tz`, `--name`,
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

1. ~~Laporan iklan mingguan (Meta/TikTok Ads)~~ — **selesai** (sesi 2026-09-26): skill
   `laporan-iklan-mingguan` sudah `lulus` dan langkahnya sudah ditulis penuh di
   `toko-online/PANDUAN.md` §5l dan `toko-online/jadwal-openclaw.md` §10 (jadwal Senin 08.00
   WIB, perintah disalin dari `skills/laporan-iklan-mingguan/references/openclaw-jadwal.md`).
2. ~~Pengingat kontrol/vaksin pasien terjadwal (klinik)~~ — **selesai** (sesi 2026-09-26): skill
   `pengingat-pasien-klinik` (sudah `lulus`, skor 9/10) dirangkai penuh di `klinik/PANDUAN.md` §5i
   dan `klinik/jadwal-openclaw.md` §4 (ringkasan harian 07.30 WIB ke Telegram pemilik/PIC, tanpa
   nomor WA). Sesuai keputusan pemilik: data lokal minimal (nama panggilan, nomor WA, jenis &
   tanggal kunjungan berikutnya, tanpa diagnosis/rekam medis), persetujuan pasien wajib dicatat,
   dan draf pengingat WA **hanya disalin & dikirim staf** — tidak pernah otomatis.
3. ~~Laporan status ke klien (konsultan)~~ — **selesai** (sesi 2026-09-26): skill
   `laporan-klien-konsultan` (sudah `lulus`) dirangkai penuh di `konsultan/PANDUAN.md` §5n dan
   `konsultan/jadwal-openclaw.md` §8e (draf mingguan Jumat 16.00 WIB, per klien, perintah
   disalin dari `skills/laporan-klien-konsultan/references/openclaw-jadwal.md`). Tetap sesuai
   keputusan pemilik: hanya **draf** yang dikirim ke konsultan sendiri, **konsultan yang mengirim
   manual** ke klien — tidak pernah otomatis.
4. **Integrasi WABA resmi (Level 3 CS)** disebut di riset sebagai "jasa setup", bukan skill —
   tidak ada celah skill di sini, hanya dicatat sebagai batas cakupan paket ini.

## Packaging `scripts/build.py` (keputusan pemilik 2026-09-26: diimplementasikan)

`build.py --vip` menyalin seluruh `solusi-vip/**/*.md` (semua paket, apa adanya) ke ZIP VIP,
sejajar dengan folder skill dan `LISENSI.txt`/`CARA-INSTAL.md` (lihat blok `if a.vip:` di
`scripts/build.py`). Diverifikasi ulang di Tahap C sesi ini dengan
`python3 scripts/build.py --pembeli "UJI INTERNAL" --vip --izinkan-draft`: ZIP berisi
`solusi-vip/usaha-offline/PANDUAN.md`, `jadwal-openclaw.md`, `CEKLIS.md` (dan paket
lain). Tidak ada perubahan lanjutan yang diperlukan untuk menyertakan paket baru — cukup tambah
folder `solusi-vip/<paket-baru>/`.

## Privasi (ringkas — detail penuh di tiap `PANDUAN.md`)

- Data tetap di komputer/mesin milik member (`~/.openclaw`), bukan di server Komunitech.
- Isi pesan yang diproses tetap dikirim ke penyedia model AI pilihan member (Anthropic/OpenAI/
  Google, dll.) kecuali memakai model lokal.
- Tidak pernah menyimpan nama/kontak pelanggan atau pasien di file panduan ini — hanya di
  workspace lokal member sendiri, seminimal mungkin, sesuai UU PDP.
