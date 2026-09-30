# Ceklis Serah-Terima — Solusi VIP Klinik

Satu halaman. **Jangan tulis nama pasien, nomor rekam medis, atau diagnosis di ceklis ini** —
hanya status ya/tidak.

## Prasyarat
- [ ] OpenClaw terpasang & bisa diajak chat biasa.
- [ ] Mesin Gateway sudah dipilih: ☐ komputer resepsionis jam praktik ☐ mini PC/laptop 24 jam
      ☐ VPS klinik ☐ jasa setup Komunitech.
- [ ] Dokter/tenaga kesehatan penanggung jawab materi edukasi sudah ditunjuk (nama tidak perlu
      dicatat di sini, cukup dipastikan ada).

## Pemasangan skill
- [ ] 11 skill terpasang: `karyawan-ai-mulai`, `cek-privasi-openclaw`, `edukasi-pasien-klinik`,
      `agen-cs-toko`, `balas-ulasan-pelanggan`, `konten-mingguan`, `laporan-status-kantor`,
      `kebijakan-privasi-pdp`, `sop-onboarding`, `kontrak-kerja-pkwt`, `pengingat-pasien-klinik`.
- [ ] (Opsional) `program-referral-loyalitas` (versi tanpa imbalan rujukan, PERLU REVIEW tenaga
      medis/hukum) dan `iterasi-dari-masukan-pelanggan` terpasang; tidak ada hadiah untuk merujuk pasien.
- [ ] `karyawan-ai-mulai` sudah dijalankan sekali, ada 1 hasil nyata.
- [ ] `cek-privasi-openclaw` sudah dijalankan, termasuk ringkasan UU PDP data kesehatan.

## Kanal
- [ ] Bot Telegram tersambung, pairing disetujui, ID chat dicatat di catatan pribadi (bukan di
      dokumen bersama tim/repo).
- [ ] **Kalau memakai WhatsApp:**
  - [ ] Nomor **terpisah** dari nomor pendaftaran/CS pasien.
  - [ ] Persetujuan risiko **tertulis** diperoleh.
  - [ ] `dmPolicy` = `allowlist` (BUKAN `pairing`/`open`), diset **sebelum** nomor dibagikan ke
        siapa pun.
  - [ ] `allowFrom` hanya berisi nomor pemilik/PIC.

## Otomasi
| Otomasi | Jadwal | Diuji sekali? | Sudah dicek TIDAK ada nama/diagnosis pasien? | Aktif? |
|---|---|---|---|---|
| Rekap CS harian (Copilot) | 20.00 WIB | ☐ | ☐ | ☐ |
| Laporan operasional klinik | Mingguan/harian | ☐ | ☐ | ☐ |
| Konten edukasi kesehatan | Jumat 16.00 WIB | ☐ | — (bukan data pasien) | ☐ |
| Ringkasan pengingat pasien harian | 07.30 WIB | ☐ | ☐ (tanpa nomor WA) | ☐ |

## Pengingat pasien (`pengingat-pasien-klinik`)
- [ ] Data disimpan **lokal** di komputer klinik (`pasien/DAFTAR.csv`), minimal: nama panggilan,
      nomor WA, jenis kunjungan umum, tanggal berikutnya. **Tidak ada** diagnosis/rekam medis/NIK.
- [ ] Persetujuan (`--persetujuan ya/tidak`) ditanyakan secara eksplisit ke setiap pasien
      sebelum dicatat — tidak pernah diasumsikan "ya".
- [ ] Pasien yang menolak (`persetujuan: tidak`) **tidak pernah** muncul di daftar harian
      (H-3/H-1/hari ini/terlambat) maupun draf pesan.
- [ ] Draf pesan WA (daftar harian) hanya **disalin & dikirim staf** dari WA klinik — tidak ada
      pengiriman otomatis maupun broadcast lewat OpenClaw.
- [ ] Ringkasan terjadwal ke Telegram pemilik/PIC memakai `--samarkan` dan **tidak pernah**
      memuat nomor WA.
- [ ] Permintaan hapus data pasien (`hapus --id/--wa`) dijalankan **segera**, tidak ditunda.

## Privasi & batasan medis (wajib dicentang semua)
- [ ] Tidak ada skrining/diagnosis/kalkulator medis/dosis/interpretasi lab/triase dijalankan
      lewat paket ini.
- [ ] Semua instruksi medis di leaflet/pengingat berasal **persis** dari dokter — tidak ditebak
      AI.
- [ ] Laporan operasional **hanya** berisi angka agregat, tanpa nama/NIK/diagnosis.
- [ ] Basis pengetahuan CS **tidak** berisi data pasien individual.
- [ ] Log CS harian hanya berisi kategori pertanyaan, bukan isi chat/nama pasien lengkap.
- [ ] Konten edukasi kesehatan sudah/akan ditinjau dokter sebelum diposting, mencantumkan sumber
      resmi + nama & alamat klinik + tanggal (Permenkes 1787/2010).
- [ ] Tidak ada klaim menyembuhkan/testimoni/before-after/superlatif di materi publikasi.
- [ ] Agen CS mode Copilot: draf disiapkan AI, **staf yang mengirim** ke pasien. Tidak ada
      auto-reply otomatis ke pasien lewat WA Web.
- [ ] Tidak ada broadcast/promo massal dikirim lewat OpenClaw.
- [ ] Pasien diberi tahu bila berbicara dengan asisten virtual, dan boleh minta bicara staf.

## Dokumen tambahan (dipicu manual, isi bila sudah dipakai)
- [ ] Kebijakan privasi klinik (`kebijakan-privasi-pdp`) sudah dibuat/ditinjau, mencakup data
      kesehatan pasien, berlabel "bukan nasihat hukum".
- [ ] Kontrak kerja staf kontrak non-medis (bila ada) dibuat dengan `kontrak-kerja-pkwt` dan
      ditinjau sebelum ditandatangani.
- [ ] Paket onboarding staf baru (`sop-onboarding`) sudah dipakai bila ada staf baru mulai kerja.

## Tanda tangan/paraf serah-terima
Tanggal: __________  PIC klinik: __________  Teknisi/pendamping (bila ada): __________
