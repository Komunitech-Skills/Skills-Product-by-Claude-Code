# Peta Skill — Profesi/Tugas → Skill Library Komunitech

Tabel statis ini dipakai `karyawan-ai-mulai` untuk mencocokkan jawaban wawancara ke skill yang
sudah ada di folder skills platform Anda (mis. `~/.openclaw/skills`, `~/.claude/skills`,
`~/.agents/skills`, `~/.cursor/skills`, tergantung platform yang dipakai). Jangan menebak nama
skill di luar tabel ini — kalau tidak ada padanan, katakan jujur dan tawarkan skill terdekat +
alasan.

## 1. Tugas paling menyita waktu → skill

| Kata kunci dari jawaban pengguna | Skill yang direkomendasikan | Kenapa |
|---|---|---|
| Bikin laporan penjualan/omzet, rekap harian (juga: "rekap jualan", "laporan omzet") | `rekap-penjualan-csv` | Ubah file CSV kasir/marketplace jadi rekap omzet & tren dalam hitungan menit |
| Kirim laporan rutin otomatis ke Telegram/WA (harian/mingguan/bulanan) | `laporan-otomatis-terjadwal` | Menjadwalkan `openclaw automations` supaya laporan (penjualan/keuangan/stok/piutang) terkirim sendiri — **butuh komputer/Gateway menyala terus**, lihat §"Batasan" di SKILL.md |
| Catat stok/inventori, stock opname, potong stok dari pesanan marketplace | `buku-stok` | Buku stok lokal: barang masuk/keluar, opname, impor pesanan Shopee/TikTok Shop/Tokopedia, laporan stok menipis |
| Laporan keuangan, laba rugi, neraca | `laporan-keuangan-emkm` | Susun laporan sesuai SAK EMKM dari catatan kas |
| Cek uang cukup sampai kapan, proyeksi kas | `arus-kas-13minggu` | Proyeksi kas 13 minggu + simulasi tindakan |
| Cocokkan mutasi bank dengan penjualan | `rekonsiliasi-bank` | Cocokkan transfer masuk dengan catatan penjualan |
| Ketik ulang nota/struk/faktur ke Excel | `ekstrak-nota-faktur` | Baca foto/teks nota jadi tabel & CSV |
| Balas chat pelanggan (WA/marketplace; juga: "bales wa", "balas wa") | `balas-chat-cs` | Draf balasan CS dari FAQ sampai komplain — **mode Copilot**: AI menyiapkan draf, manusia yang mengirim (lihat "Aturan pemilik" di SKILL.md) |
| Balas ulasan/review publik | `balas-ulasan-pelanggan` | Balasan ulasan Shopee/Tokopedia/Google Maps |
| Baca/rekap banyak ulasan sekaligus | `analisis-ulasan` | Ringkas ratusan ulasan jadi tema & prioritas perbaikan |
| Bikin caption/konten sosmed harian (juga: "bikin konten", "posting ig/instagram/tiktok") | `caption-sosmed-umkm` | Caption siap tempel IG/TikTok/FB/WA Status — skill menyiapkan teksnya, posting tetap manual oleh Anda (OpenClaw tidak punya kanal posting IG/TikTok resmi) |
| Rencana konten sebulan | `kalender-konten-30hari` | Kalender 30 hari dengan momen lokal Indonesia |
| Rencana promo (diskon, flash sale) | `promo-kalender` | Rencana kampanye + cek margin aman |
| Follow-up calon pembeli yang belum deal | `follow-up-prospek` | Urutan pesan follow-up H+1/3/7/14 |
| Tagih pelanggan yang telat bayar | `tagih-piutang` | Pesan penagihan bertahap sampai somasi |
| Buat invoice/kuitansi | `buat-invoice` | Invoice profesional dengan nomor & PPN |
| Buat surat penawaran harga | `surat-penawaran-harga` | SPH lengkap + versi WA |
| Broadcast promo ke banyak pelanggan | `broadcast-wa` | Pesan broadcast + opt-out + jadwal bertahap (baca peringatan risiko WA di §4 SKILL.md) |
| Notulen rapat / rangkum meeting | `notulen-rapat` | Notulen + tabel action item |
| Surat resmi/dinas (undangan, keterangan) | `surat-resmi` | Surat resmi format EYD V |
| Bikin SOP kerja karyawan | `sop-writer` | SOP + checklist harian |
| Pasang iklan lowongan kerja | `lowongan-kerja` | Iklan loker siap posting |
| Buat surat peringatan karyawan | `surat-peringatan-karyawan` | SP1/SP2/SP3 terdokumentasi |
| Hitung gaji & BPJS karyawan | `slip-gaji-bpjs` | Slip gaji + potongan BPJS + PPh 21 |
| Hitung PPh 21 karyawan | `pph21-ter` | PPh 21 metode TER |
| Hitung THR | `hitung-thr` | THR sesuai Permenaker 6/2016 |
| Hitung pajak UMKM 0,5% | `pph-final-umkm` | PPh Final UMKM + pelacak omzet |
| Hitung/pisahkan PPN | `hitung-ppn` | Kalkulator PPN 12% (DPP nilai lain) |
| Hitung modal/HPP produk | `hitung-hpp` | HPP per unit + BEP |
| Tentukan harga jual di marketplace | `harga-jual-marketplace` | Harga jual setelah potongan marketplace |
| Buat listing produk marketplace | `listing-marketplace` | Judul & deskripsi siap tempel |
| Brief foto/video produk pakai HP | `foto-produk-brief` | Shot list tanpa studio |
| Naskah live selling | `naskah-live-jualan` | Rundown live TikTok/Shopee/IG |
| Susun harga reseller/dropshipper | `katalog-reseller` | Tier harga mitra + S&K |
| Proposal kerja sama/kemitraan | `proposal-kerjasama` | Proposal B2B/reseller/sponsorship |
| Buat draf perjanjian/kontrak | `perjanjian-sederhana` | Draf perjanjian pasal standar |
| Ajukan KUR/pinjaman usaha | `pengajuan-kur` | Checklist & simulasi cicilan KUR |

Tugas yang **tidak ada** padanannya di tabel ini (mis. skrining medis, auto-trading kripto,
posting otomatis ke Instagram/TikTok): jangan berjanji bisa melakukannya. Jelaskan batasan
sesuai §"Batasan & penanganan error" di `SKILL.md`, dan tawarkan alternatif aman bila ada
(mis. `cek-privasi-openclaw` untuk kekhawatiran privasi).

## 2. Industri → paket kerja pertama (dipakai bila pengguna ingin cepat/pakai default)

| Industri/peran | 3 skill prioritas | 1 otomasi awal |
|---|---|---|
| Toko/retail/F&B (owner/kasir; termasuk restoran, rumah makan, warung, kafe) | `rekap-penjualan-csv`, `balas-chat-cs`, `caption-sosmed-umkm` | Laporan omzet mingguan lewat `laporan-otomatis-terjadwal` (default kanal **Telegram**, lihat §"Otomasi" di SKILL.md) |
| Jasa/konsultasi/freelancer/bengkel | `surat-penawaran-harga`, `follow-up-prospek`, `buat-invoice` | Pengingat follow-up harian |
| Kantor/admin/manager | `notulen-rapat`, `surat-resmi`, `sop-writer` | Pengingat tugas dari notulen |
| Keuangan/akuntansi | `laporan-keuangan-emkm`, `rekonsiliasi-bank`, `arus-kas-13minggu` | Laporan kas mingguan |
| HR/SDM/kepegawaian | `slip-gaji-bpjs`, `pph21-ter`, `lowongan-kerja` | Pengingat jadwal gajian |
| Manufaktur/produksi | `hitung-hpp`, `arus-kas-13minggu`, `rekap-penjualan-csv` | Laporan produksi mingguan |
| Kesehatan — dokter solo/klinik | `balas-chat-cs` (draf balasan pasien, mode Copilot — bukan auto-reply langsung), `sop-writer`, `notulen-rapat` | Laporan operasional klinik (kunjungan, jam ramai) **tanpa** nama/diagnosis pasien. **Tanpa** skrining/diagnosis/kalkulator medis — lihat batasan di SKILL.md utama (rujuk juga `cek-privasi-openclaw` untuk data pasien) |
| Properti/agen | `surat-penawaran-harga`, `follow-up-prospek`, `proposal-kerjasama` | Pengingat follow-up prospek |
| Lainnya/tidak cocok tabel | `rekap-penjualan-csv`, `balas-chat-cs`, `surat-resmi` ("paket umum") | — (tanyakan dulu) |

Kalau industri pengguna tidak ada di tabel, katakan jujur: *"Industri Anda belum ada contoh
khusus di paket kami — saya pakai paket umum dulu, boleh dikoreksi kapan saja."*
