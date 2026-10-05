# Menu Jasa Setup Komunitech

> **HARGA DI BAWAH = USULAN KURATOR, DIPUTUSKAN PEMILIK.** Belum ada harga final. Angka dipakai
> sebagai bahan diskusi; pemilik boleh mengubah kapan saja. Jangan dikutip ke calon pelanggan
> sebelum pemilik menyetujui. (Disusun 2026-09-29 dari keputusan pemilik jalur 3 di `CLAUDE.md`.)

Jasa ini untuk pengusaha & profesional yang **tidak mau repot** memasang sendiri. Semua
panduan gratis-nya tetap ada di paket (lihat `docs/instalasi.md`, `docs/panduan-*.md`,
`solusi-vip/*/PANDUAN.md`); yang dijual di sini adalah **waktu, ketelitian, dan jaminan jalan**.

## Ringkasan paket dan harga usulan

| Kode | Layanan | Usulan harga (IDR) | Durasi kerja | Cara |
|---|---|---|---|---|
| **A** | Setup OpenClaw + bot Telegram + 1 paket solusi-vip (jadwal) | **Rp 750.000** | 2-3 jam | Jarak jauh (default) |
| **B** | Tambahan: pasang 1 aplikasi lokal | **Rp 450.000** (ringan) atau **Rp 900.000** (berat) per aplikasi | 1-2 jam (ringan), 3-4 jam (berat) | Jarak jauh atau datang |
| **C1** | Mesin 24 jam: mini PC/laptop milik member | **Rp 450.000** | 1,5-2 jam | Jarak jauh atau datang |
| **C2** | Mesin 24 jam: VPS milik member | **Rp 650.000** | 2-3 jam | Jarak jauh |
| **D1** | Pendampingan bulanan Dasar | **Rp 250.000 / bulan** | 1 sesi 30 menit + pantauan ringan | Jarak jauh |
| **D2** | Pendampingan bulanan Plus | **Rp 500.000 / bulan** | 2 sesi 30 menit + 1 tambahan jadwal/perubahan kecil | Jarak jauh |
| Ongkos datang | Kunjungan ke lokasi (onsite) | **Rp 350.000** dalam kota/area layanan; luar kota sesuai biaya nyata | per kunjungan | Datang |

Aplikasi **ringan**: Vikunja, Uptime Kuma, Datasette, SiYuan, Grist (sesuai panduannya).
Aplikasi **berat**: Dolibarr, Frappe Books (bila perlu pengaturan awal akun/COA), Open Notebook.
Penggolongan final dicocokkan teknisi dengan panduan aplikasinya sebelum penawaran.

**Paket hemat (usulan):** A + C1 atau C2 sekaligus = diskon Rp 100.000. A + 1 aplikasi ringan =
diskon Rp 50.000. Pendampingan bulan pertama gratis untuk pembeli A + C.

## Alasan angka (untuk pemilik)
- Kerja teknisi lepas untuk setup software di Indonesia lazim diberi tarif kira-kira
  Rp 150.000-300.000 per jam (perkiraan kurator, **belum dicek ulang ke pasar**, lihat
  `research/harga.md` untuk cara Komunitech membahas harga). A = 2-3 jam x ±Rp 250.000.
- Nilai bagi member: laporan harian jalan tanpa harus paham terminal; risiko salah pengaturan
  privasi (kanal terbuka, perintah komputer tanpa persetujuan) ditutup sejak awal.
- B dibedakan ringan/berat karena Dolibarr/Open Notebook punya langkah pengamanan & cadangan
  lebih banyak (lihat `docs/panduan-dolibarr.md`, `docs/panduan-open-notebook.md`).
- C dipisah dari A karena tidak semua member butuh (yang laptopnya menyala jam kerja tidak
  perlu). VPS lebih mahal dari mini PC karena ada pengamanan server.
- D dibuat bulanan agar ada pemasukan berulang dan member tidak "ditinggal" setelah serah
  terima, tetapi tanpa janji layanan 24 jam.
- Catatan: harga jasa **tidak** memuat harga skill/paket VIP. Member VIP sudah punya skill-nya.
  Non-member membeli skill terpisah.

## Apa saja yang termasuk dan tidak termasuk

### A. OpenClaw + Telegram + 1 paket solusi-vip
**Termasuk:**
1. Cek OpenClaw member sudah bisa chat; pasang skill paket pilihan (satu dari 6 paket di
   `solusi-vip/`), jalankan `karyawan-ai-mulai`.
2. Pembuatan bot Telegram lewat @BotFather (member yang mengetik/menempel token sendiri),
   pairing, dan pencatatan ID chat Telegram di komputer member.
3. Pasang dan uji **sampai 3 jadwal** dari `jadwal-openclaw.md` paket itu (uji `run --wait`).
4. `cek-privasi-openclaw` dijalankan, perbaikan satu per satu atas izin member.
5. Serah terima memakai `CEKLIS.md` paket + sesi tanya jawab 30 menit.
**Tidak termasuk:** kunci/langganan model AI (member bayar sendiri ke penyedianya), perbaikan
komputer/jaringan member, jadwal ke-4 dst. (tambahan Rp 100.000 per jadwal, usulan), WhatsApp
(lihat catatan), pelatihan tim panjang, pembuatan skill baru khusus.

### B. Pasang aplikasi lokal
**Termasuk:** unduh dari sumber resmi + cek keaslian, pasang, **pengamanan wajib** sesuai panduan
(hanya bisa dibuka dari komputer sendiri), akun admin dibuat member sendiri, cadangan pertama +
uji pulih, satu jadwal laporan ke Telegram bila aplikasi mendukung.
Aplikasi yang dilayani: Frappe Books, Dolibarr, Vikunja, Grist, Uptime Kuma, Open Notebook,
SiYuan, Datasette. Panduan acuan: `docs/panduan-*.md` (Frappe Books lewat skill
`frappe-books-usaha`).
**Tidak termasuk:** memindahkan data lama dalam jumlah besar (tawaran terpisah), akses dari luar
jaringan/HP/cabang (butuh HTTPS + autentikasi, di luar paket ini), pelatihan mendalam, dan
dukungan bila versi aplikasi berubah setelah serah terima.
Catatan merek: Komunitech **tidak berafiliasi** dengan proyek aplikasi tersebut (aturan
`CLAUDE.md`).

### C. Mesin 24 jam
**Termasuk C1:** setelan tidur/hemat daya, menyala otomatis setelah listrik padam (bila BIOS
mendukung), OpenClaw/Gateway dipastikan jalan otomatis saat komputer menyala, uji restart.
**Termasuk C2:** pengamanan dasar VPS milik member, pemasangan OpenClaw di VPS mengikuti
dokumentasi resmi OpenClaw, uji restart.
**Tidak termasuk:** pembelian perangkat/langganan VPS (milik dan tanggungan member), UPS,
internet, dan jaminan uptime. Jelaskan jujur: mesin mati = laporan tidak terkirim.

### D. Pendampingan bulanan
**Dasar:** 1 sesi 30 menit (chat/telepon/video) per bulan, pengecekan bahwa jadwal masih
berjalan, cek privasi ulang, bantuan update skill.
**Plus:** dua sesi, ditambah 1 jadwal baru atau perubahan kecil per bulan.
**Tidak termasuk:** respons darurat 24 jam, perbaikan akibat perubahan yang dibuat member
sendiri di luar kesepakatan, dan pekerjaan besar (dihitung sebagai layanan A/B/C).

## Catatan WhatsApp (bukan layanan standar)
Default kanal = **Telegram**. WhatsApp hanya untuk notifikasi ke pemilik sendiri, dengan
**nomor terpisah** dan **persetujuan risiko tertulis** (formulir di `SOP-TEKNISI.md` lampiran 1).
Tidak ada broadcast. Agen CS di WA = mode Copilot (AI menyiapkan draf, manusia mengirim).
Usulan biaya tambahan penyiapan kanal WA: Rp 150.000 (sudah termasuk uji kirim dan cek privasi).

## Syarat dari member
Lihat `FORMULIR-PERSIAPAN.md` (bahasa awam, dikirim ke member sebelum jadwal). Ringkasnya:
OpenClaw sudah terpasang, komputer siap, akun Telegram aktif, penyedia model AI sudah
dipilih, 1-2 jam waktu tanpa gangguan, dan orang yang berwenang mengambil keputusan hadir.

## Jarak jauh atau datang
- **Jarak jauh (default):** layar dibagikan via aplikasi yang disepakati; **member yang
  mengendalikan** ketika mengetik token, password, atau membuka akun. Teknisi tidak meminta
  password dibagikan lewat chat.
- **Datang (onsite):** bila komputer tidak mendukung akses jarak jauh, ada beberapa perangkat,
  atau member awam sekali. Dikenai ongkos datang. Teknisi membawa tanda pengenal.

## Ketentuan umum (usulan)
- Pembayaran di depan (DP 50% untuk B/C berat), sisa saat serah terima.
- Garansi perbaikan **14 hari** untuk hal yang dipasang teknisi (bukan untuk perubahan member
  sesudahnya atau mesin yang dimatikan).
- Komunitech **tidak menyimpan** token, password, atau data pelanggan member (lihat SOP).
- Tidak melayani: auto-trading/rekomendasi beli-jual kripto, skrining/diagnosis medis, broadcast
  massal, pembuatan klon suara/wajah, scraping marketplace lewat login browser
  (keputusan pemilik di `CLAUDE.md`).

## Untuk pemilik: hal yang perlu diputuskan
1. Setujui/ubah semua angka di tabel (usulan, belum final).
2. Batas area layanan onsite dan ongkosnya.
3. Apakah garansi 14 hari dan DP 50% dipakai.
4. Siapa saja teknisi dan jadwal ketersediaannya.
