# Ceklis Serah-Terima — Solusi VIP Toko Online

Satu halaman. Dicentang bersama oleh member dan pemilik/teknisi jasa setup (kalau ada
pendampingan). Simpan salinannya untuk member, **jangan** simpan salinan berisi data
pelanggan/nomor HP di repo Komunitech.

## Prasyarat
- [ ] OpenClaw terpasang & bisa diajak chat biasa.
- [ ] Mesin yang menjalankan Gateway OpenClaw sudah dipilih dan disepakati: ☐ laptop/PC jam kerja
      ☐ mini PC/laptop 24 jam ☐ VPS milik member ☐ jasa setup Komunitech.
- [ ] Member paham: kalau mesin itu mati/tidur di jam jadwal, laporan **tidak terkirim** (bukan
      error, memang tidak jalan).

## Pemasangan skill
- [ ] 21 skill paket terpasang (`openclaw skills list` menampilkan semuanya):
      `karyawan-ai-mulai`, `cek-privasi-openclaw`, `listing-marketplace`,
      `harga-jual-marketplace`, `balas-ulasan-pelanggan`, `analisis-ulasan`, `promo-kalender`,
      `naskah-live-jualan`, `buku-stok`, `agen-cs-toko`, `foto-produk-brief`,
      `laporan-otomatis-terjadwal`, `rekap-penjualan-csv`, `konten-mingguan`, `pesan-prospek-wa`,
      `crm-wa`, `analisis-excel`, `brainstorming-ide-usaha`, `kas-umkm`, `buku-piutang`,
      `laporan-iklan-mingguan`.
- [ ] (Opsional) skill tambahan sesuai kebutuhan: `program-referral-loyalitas`,
      `iterasi-dari-masukan-pelanggan`, `umami-analitik`, `listmonk-newsletter`,
      `luncurkan-produk-baru`, `uji-pasar-produk-cepat`, `studio-video-pendek-ai`. Umami/listmonk
      perlu dipasang (jasa setup); tidak ada blast, email hanya ke yang mendaftar sendiri.
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

## Otomasi (isi id job & tanggal uji, JANGAN isi nama/nomor pelanggan di sini)
| Otomasi | Jam/jadwal | Sudah diuji sekali (`run --wait`)? | Aktif? |
|---|---|---|---|
| Laporan toko harian | 21.00 WIB | ☐ | ☐ |
| Stok menipis (bila terpisah) | — | ☐ | ☐ |
| Paket konten mingguan | Jumat 16.00 WIB | ☐ | ☐ |
| Pengingat posting harian | 08.00 WIB | ☐ | ☐ |
| Rekap CS harian (Copilot) | 20.00 WIB | ☐ | ☐ |
| Follow-up CRM harian (crm-wa, opsional) | 08.00 WIB | ☐ | ☐ |
| Ringkasan kas harian (kas-umkm, opsional) | 21.00 WIB | ☐ | ☐ |
| Ringkasan piutang reseller (buku-piutang, opsional) | 07.45 WIB | ☐ | ☐ |
| Laporan iklan mingguan (laporan-iklan-mingguan, opsional) | Senin 08.00 WIB | ☐ | ☐ |

## Privasi (wajib dicentang semua)
- [ ] Tidak ada data pelanggan/pasien (nama, nomor HP, alamat) yang ditulis ke log/laporan yang
      dikirim ke chat — hanya ringkasan agregat.
- [ ] Agen CS berjalan mode **Copilot**: draf disiapkan AI, **manusia yang mengirim** ke
      pelanggan. Tidak ada auto-reply otomatis ke pelanggan lewat WA Web.
- [ ] Tidak ada broadcast/promo massal dikirim lewat OpenClaw.
- [ ] Member sudah diberi tahu bahwa isi pesan yang diproses dikirim ke penyedia model AI
      pilihannya (Anthropic/OpenAI/Google, dll.), kecuali memakai model lokal.
- [ ] Member tahu cara menjalankan `cek-privasi-openclaw` kapan saja dan akan mengulanginya
      setiap menambah kanal/agen baru.
- [ ] **Kalau memakai `crm-wa`:** database CRM ada di komputer member sendiri (bukan cloud), dan
      member tahu ekspor CSV-nya (`ekspor`) berisi data pribadi calon pembeli — tidak disimpan di
      repo/dokumen bersama.
- [ ] **Kalau memakai `pesan-prospek-wa`:** setiap pesan mencantumkan asal kontak dan opsi
      keluar; tidak dipakai untuk kirim ke banyak nomor sekaligus.

## Tanda tangan/paraf serah-terima
Tanggal: __________  Member: __________  Teknisi/pendamping (bila ada): __________
