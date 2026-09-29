# Ceklis Serah-Terima — Solusi VIP Kantor & Manajemen

Satu halaman. **Jangan tulis nama/nomor karyawan, pelanggan, atau pemasok di ceklis ini** —
hanya status ya/tidak.

## Prasyarat
- [ ] OpenClaw terpasang & bisa diajak chat biasa.
- [ ] Mesin Gateway dipilih: ☐ komputer kantor jam kerja ☐ mini PC 24 jam ☐ VPS perusahaan
      ☐ jasa setup Komunitech.
- [ ] Pimpinan paham: bila mesin mati/tidur di jam laporan, laporan **tidak terkirim**.

## Pemasangan skill
- [ ] Skill inti terpasang: `karyawan-ai-mulai`, `cek-privasi-openclaw`,
      `laporan-otomatis-terjadwal`, `laporan-harian-usaha`, `laporan-status-kantor`,
      `ringkas-grup-wa`, `notulen-rapat`, `analisis-excel`, `analisis-rasio-keuangan-usaha`,
      `arus-kas-13minggu`, `presentasi-data-ke-atasan`, `buku-piutang`, `tagih-piutang`,
      `buku-stok`, `laporan-insiden-usaha`, `dasbor-lokal`.
- [ ] `vikunja-tugas` terpasang (bila tim memakai daftar tugas) — aplikasi Vikunja sudah
      berjalan: ☐ dipasang sendiri ☐ jasa setup Komunitech.
- [ ] Satu dari `frappe-books-usaha` / `dolibarr-usaha` (bila memakai): ☐ Frappe Books
      ☐ Dolibarr ☐ tidak dipakai. Aplikasinya sudah terpasang: ☐ sendiri ☐ jasa setup.
- [ ] `karyawan-ai-mulai` dijalankan sekali, ada 1 hasil nyata.
- [ ] `cek-privasi-openclaw` dijalankan (termasuk ringkasan UU PDP untuk data karyawan/pelanggan).

## Kanal
- [ ] Bot Telegram tersambung, pairing disetujui, ID chat dicatat di catatan pribadi (bukan di
      dokumen bersama/repo).
- [ ] Tiap penerima laporan (mis. direktur, manajer keuangan) punya jadwal **sendiri** dengan
      ID chat pribadinya; tidak ada laporan ke grup.
- [ ] **Bila memakai WhatsApp:** nomor **terpisah**, hanya ke pemilik sendiri, persetujuan risiko
      **tertulis** diperoleh, `dmPolicy` = `allowlist`, `allowFrom` hanya nomor pemilik.

## Otomasi
| Otomasi | Jadwal | Diuji sekali (`run --wait`)? | Aktif? |
|---|---|---|---|
| Laporan harian manajemen (laporan-harian-usaha) | 21.00 WIB | ☐ | ☐ |
| Laporan mingguan manajemen | Senin 07.00 WIB | ☐ | ☐ |
| Tugas hari ini (vikunja-tugas, opsional) | 07.00 WIB | ☐ | ☐ |
| Tugas terlambat (vikunja-tugas, opsional) | 07.05 WIB | ☐ | ☐ |
| Ringkasan piutang (buku-piutang) | 07.45 WIB | ☐ | ☐ |
| Stok menipis (buku-stok) | 07.00 WIB | ☐ | ☐ |
| Laporan harian Frappe Books/Dolibarr (opsional) | 21.00 WIB | ☐ | ☐ |

## Tugas dari grup WA & pelacakan tugas (wajib dicentang semua)
- [ ] Ringkasan grup memakai **ekspor chat** (Tanpa Media). Tidak ada bot yang masuk ke grup.
- [ ] Daftar tindakan dari grup/notulen diperlakukan sebagai **draf**; tugas baru masuk Vikunja
      hanya setelah **manusia mengonfirmasi**.
- [ ] Tim sudah diberi tahu ada daftar tugas bersama yang dibantu AI.
- [ ] Pelacakan = **daftar tugas & tenggat**. Tidak ada pemantauan layar, lokasi, atau chat
      pribadi karyawan.
- [ ] Grup berisi urusan pribadi/SDM/sengketa **tidak** diekspor ke AI.

## Privasi
- [ ] Tidak ada pesan penagihan/pengumuman yang dikirim **otomatis** ke pelanggan atau
      karyawan; semua draf disalin & dikirim manual.
- [ ] Tidak ada broadcast/kirim massal lewat OpenClaw.
- [ ] Token API Vikunja untuk jadwal = **baca-saja**; token tidak ditulis di perintah jadwal.
- [ ] Pimpinan tahu isi yang diproses dikirim ke penyedia model AI pilihannya (kecuali model
      lokal) dan tahu cara menjalankan `cek-privasi-openclaw` kapan saja.
- [ ] Pimpinan paham paket ini bukan pengganti akuntan/auditor/penasihat hukum.

## Tanda tangan/paraf serah-terima
Tanggal: __________  Pimpinan: __________  Teknisi/pendamping (bila ada): __________
