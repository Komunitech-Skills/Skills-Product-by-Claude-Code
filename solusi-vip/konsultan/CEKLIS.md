# Ceklis Serah-Terima — Solusi VIP Konsultan/Freelancer

Satu halaman. **Jangan tulis nama/nomor klien di ceklis ini** — hanya status ya/tidak.

## Prasyarat
- [ ] OpenClaw terpasang & bisa diajak chat biasa.
- [ ] Mesin Gateway sudah dipilih: ☐ laptop kerja pagi hari ☐ mini PC 24 jam ☐ VPS sendiri
      ☐ jasa setup Komunitech.
- [ ] Member paham: kalau laptop kerja dibawa pergi/mati saat jam pengingat, pengingat **tidak
      terkirim** hari itu.

## Pemasangan skill
- [ ] 14 skill terpasang: `karyawan-ai-mulai`, `cek-privasi-openclaw`, `proposal-kerjasama`,
      `surat-penawaran-harga`, `buat-invoice`, `tagih-piutang`, `pengingat-follow-up`,
      `riset-calon-pelanggan`, `asisten-tulis-riset`, `presentasi-instan`, `tender-checklist`,
      `kontrak-kerja-pkwt`, `kebijakan-privasi-pdp`, `kalender-pajak`.
- [ ] `karyawan-ai-mulai` sudah dijalankan sekali, ada 1 hasil nyata.
- [ ] `cek-privasi-openclaw` sudah dijalankan, termasuk ringkasan UU PDP untuk data klien.

## Kanal
- [ ] Bot Telegram tersambung, pairing disetujui, ID chat dicatat di catatan pribadi member
      (bukan di dokumen bersama/repo).
- [ ] **Kalau memakai WhatsApp:**
  - [ ] Nomor **terpisah**, hanya untuk notifikasi ke diri sendiri.
  - [ ] Persetujuan risiko **tertulis** diperoleh.
  - [ ] `dmPolicy` = `allowlist` (BUKAN `pairing`/`open`), `allowFrom` hanya nomor pemilik.

## Data & otomasi
- [ ] `pengingat/DAFTAR.csv` (dan `timesheet.csv` bila dipakai) sudah diisi/diimpor, dan member
      paham ini adalah data pribadi pihak ketiga (klien) — disimpan seperlunya, tidak dibagikan
      ke luar workspace-nya sendiri.
| Otomasi | Jadwal | Diuji sekali (`run --wait`)? | Aktif? |
|---|---|---|---|
| Rekap follow-up & piutang harian | 08.00 WIB | ☐ | ☐ |
| Rekap timesheet klien | Jumat 16.00 WIB | ☐ | ☐ |
| Pengingat sekali jalan (janji spesifik) | sesuai kebutuhan | ☐ | — |
| Pengingat jadwal pajak bulanan (kalender-pajak, opsional) | Tgl 1 & 10, 07.00 WIB | ☐ | ☐ |

## Privasi (wajib dicentang semua)
- [ ] Tidak ada pesan penagihan/follow-up yang dikirim **otomatis** ke klien — semua draf
      disalin & dikirim manual oleh pemilik.
- [ ] Tidak ada broadcast/promo massal dikirim lewat OpenClaw.
- [ ] Member tahu isi pesan yang diproses dikirim ke penyedia model AI pilihannya, kecuali
      memakai model lokal.
- [ ] Member tahu cara menjalankan `cek-privasi-openclaw` kapan saja dan akan mengulanginya bila
      menambah kanal baru.

## Tanda tangan/paraf serah-terima
Tanggal: __________  Member: __________  Teknisi/pendamping (bila ada): __________
