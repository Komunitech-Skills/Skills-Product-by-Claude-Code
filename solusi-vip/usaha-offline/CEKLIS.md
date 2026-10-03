# Ceklis Serah-Terima — Solusi VIP Usaha Offline

Satu halaman. Dicentang bersama oleh member dan pemilik/teknisi jasa setup (kalau ada
pendampingan). Simpan salinannya untuk member, **jangan** simpan salinan berisi data
pelanggan/karyawan/nomor HP di repo Komunitech.

## Prasyarat
- [ ] OpenClaw terpasang & bisa diajak chat biasa.
- [ ] Mesin yang menjalankan Gateway OpenClaw sudah dipilih dan disepakati: ☐ komputer
      kasir/kantor jam buka ☐ mini PC/laptop 24 jam ☐ VPS milik member ☐ jasa setup Komunitech.
- [ ] Member paham: kalau mesin itu mati/tidur di jam jadwal, laporan **tidak terkirim** (bukan
      error, memang tidak jalan).

## Pemasangan skill
- [ ] 16 skill paket terpasang di **folder yang sama** (`openclaw skills list` menampilkan
      semuanya): `karyawan-ai-mulai`, `cek-privasi-openclaw`, `kasir-lokal`, `buku-stok`,
      `kas-umkm`, `absensi-lokal`, `gaji-umkm`, `laporan-harian-usaha`, `buku-piutang`,
      `tagih-piutang`, `hitung-hpp`, `pph-final-umkm`, `agen-cs-toko`, `balas-chat-cs`,
      `promo-kalender`, `laporan-otomatis-terjadwal`.
- [ ] (Opsional) skill tambahan: `program-referral-loyalitas`, `strategi-harga-produk`,
      `iterasi-dari-masukan-pelanggan`, `rencana-marketing-usaha` (manual, tanpa blast).
- [ ] `karyawan-ai-mulai` sudah dijalankan sekali, member sudah punya 1 hasil nyata di tangan.
- [ ] `cek-privasi-openclaw` sudah dijalankan, laporan lampu lalu lintas sudah dibaca member, dan
      setiap perbaikan 🔴/🟡 yang disetujui sudah dijalankan **satu per satu**.

## Kanal
- [ ] Bot Telegram dibuat lewat @BotFather, tersambung ke OpenClaw (`channels add --channel
      telegram`), pairing disetujui.
- [ ] ID chat Telegram pemilik sudah dicatat (bukan di repo/dokumen bersama — simpan di catatan
      pribadi member).
- [ ] **Kalau memakai WhatsApp untuk notifikasi diri sendiri:**
  - [ ] Nomor **terpisah** dari nomor toko/CS.
  - [ ] Persetujuan risiko **tertulis** sudah diperoleh (member membalas "ya, saya mengerti
        risikonya" setelah membaca peringatan di `jadwal-openclaw.md`).
  - [ ] `dmPolicy` akun WA itu = `allowlist` (BUKAN `pairing`/`open`), `allowFrom` hanya berisi
        nomor pemilik — dicek dengan `cek-privasi-openclaw` atau `openclaw config get
        channels.whatsapp.accounts.<akun>`.
  - [ ] Tidak ada broadcast/kirim massal disiapkan lewat OpenClaw.

## Otomasi (isi id job & tanggal uji, JANGAN isi nama/nomor pelanggan/karyawan di sini)
| Otomasi | Jam/jadwal | Sudah diuji sekali (`run --wait`)? | Aktif? |
|---|---|---|---|
| Laporan usaha harian gabungan (kasir+stok+absensi) | 21.00 WIB | ☐ | ☐ |
| Ringkasan buku kas harian (kas-umkm) | 21.00 WIB | ☐ | ☐ |
| Stok menipis (bila terpisah) | 07.00 WIB | ☐ | ☐ |
| Rekap absensi harian (bila terpisah) | 10.00 WIB | ☐ | ☐ |
| Pengingat gajian/BPJS/PPh 21 | 07.00 WIB harian | ☐ | ☐ |
| Ringkasan piutang harian (bila punya pelanggan bon) | 07.45 WIB | ☐ | ☐ |
| Rekap piutang mingguan (bila punya pelanggan bon) | Senin 07.50 WIB | ☐ | ☐ |

## Privasi (wajib dicentang semua)
- [ ] Tidak ada data pelanggan/karyawan (nama, nomor HP, alamat, NIK, rekening) yang ditulis ke
      log/laporan yang dikirim ke chat — hanya ringkasan agregat atau nama disamarkan
      (`--samarkan`).
- [ ] Agen CS berjalan mode **Copilot**: draf disiapkan AI, **manusia yang mengirim** ke
      pelanggan. Tidak ada auto-reply otomatis ke pelanggan lewat WA Web.
- [ ] Tidak ada broadcast/promo massal dikirim lewat OpenClaw.
- [ ] Member sudah diberi tahu bahwa isi pesan yang diproses dikirim ke penyedia model AI
      pilihannya (Anthropic/OpenAI/Google, dll.), kecuali memakai model lokal.
- [ ] Member tahu cara menjalankan `cek-privasi-openclaw` kapan saja dan akan mengulanginya
      setiap menambah kanal/agen baru.
- [ ] **Kalau memakai `gaji-umkm`/`absensi-lokal`:** data karyawan (NIK, rekening) tidak pernah
      disalin ke chat; slip hanya untuk karyawan yang bersangkutan, bukan grup.
- [ ] **Kalau memakai `buku-piutang`:** database piutang ada di komputer member sendiri (bukan
      cloud), dan pesan tagihan **tidak pernah** dikirim otomatis — selalu draf yang diperiksa
      lalu dikirim manual oleh pemilik (`tagih-piutang`).

## Tanda tangan/paraf serah-terima
Tanggal: __________  Member: __________  Teknisi/pendamping (bila ada): __________
