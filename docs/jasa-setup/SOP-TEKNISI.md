# SOP Teknisi Jasa Setup Komunitech (internal)

Untuk teknisi/admin Komunitech. Layanan dan harga ada di `MENU-LAYANAN.md` (usulan, diputuskan
pemilik). Dokumen ini **tidak menduplikasi** langkah teknis; ia menunjuk dokumen terverifikasi
di repo. **Jangan menulis perintah OpenClaw dari ingatan.** Salin dari dokumen yang dirujuk;
bila perlu perintah yang tidak ada di dokumen, jalankan `--help` di mesin member, lalu laporkan
ke kurator agar dicatat di repo.

## 0. Aturan wajib semua layanan

1. **Token, password, kunci API, kode OTP: member yang mengetik/menempel sendiri** di
   komputernya. Teknisi tidak meminta dikirim lewat chat/email/formulir, tidak difoto/di-screenshot,
   tidak direkam, dan **tidak disimpan** di sistem Komunitech (CRM, spreadsheet, catatan,
   tiket, repo, log chat). Rekam layar (bila ada) dimatikan saat bagian itu.
2. Tidak menyimpan data pelanggan/pasien member. Catatan sesi hanya berisi: nama usaha, layanan,
   tanggal, ID job jadwal (bukan ID chat Telegram), hasil ceklis.
3. **Telegram = default.** WhatsApp hanya via jalur khusus (lampiran 1).
4. Tidak ada broadcast/blast lewat OpenClaw. Agen CS di WA = Copilot (draf, manusia mengirim).
5. Perubahan pengaturan **satu per satu, dengan persetujuan member**. Sebelum menjalankan
   jadwal/skill, tampilkan ringkasan dan tanya "Lanjut? (ya/tidak)".
6. Bila member meminta hal di luar cakupan (auto-trading/rekomendasi beli-jual kripto,
   skrining/diagnosis medis, klon suara/wajah, posting otomatis yang tidak didukung, scraping
   marketplace lewat login browser): **tolak sopan** dan jelaskan alasannya.
7. Status paket VIP: pastikan skill yang dipasang berasal dari ZIP/member area member (bukan
   salinan liar), dan sesuai hak member (VIP atau beli ecer).

## 1. Sebelum sesi (semua layanan)

- [ ] Member sudah menerima dan mengisi `FORMULIR-PERSIAPAN.md`.
- [ ] Konfirmasi layanan, jadwal, cara (jarak jauh/datang), dan harga yang disepakati.
- [ ] Baca paket solusi yang dipilih: `solusi-vip/<paket>/PANDUAN.md`, `jadwal-openclaw.md`,
      `CEKLIS.md`.
- [ ] Cocokkan versi OpenClaw di mesin member terhadap catatan verifikasi di
      `solusi-vip/README.md` (diverifikasi pada OpenClaw 2026.9.5/2026.9.6). Bila versi berbeda,
      cek `--help` perintah yang akan dipakai.
- [ ] Siapkan cara akses jarak jauh yang **dikendalikan member** (member yang menyetujui dan
      dapat menghentikan sesi).

## 2. Layanan A: OpenClaw + Telegram + 1 paket solusi-vip

| Langkah | Kerjakan | Rujukan (salin, jangan tulis ulang) |
|---|---|---|
| A1 | Cek OpenClaw member bisa membalas "halo". Bila belum, pasang mengikuti instalasi resmi OpenClaw (lihat prasyarat 1 di PANDUAN) | `solusi-vip/<paket>/PANDUAN.md` §0 |
| A2 | Pilih mesin penjalan (laptop jam kerja / mini PC / VPS). Jelaskan: mesin mati = laporan tidak terkirim | `PANDUAN.md` §0 no. 2; `skills/laporan-otomatis-terjadwal/references/mesin-24-jam.md` |
| A3 | Pasang skill paket (`openclaw skills install ./<skill> --global`, cek `openclaw skills list`) | `PANDUAN.md` §1; `docs/instalasi.md` (bagian OpenClaw) |
| A4 | Jalankan `karyawan-ai-mulai` bersama member (satu hasil nyata) | `PANDUAN.md` §2 |
| A5 | **Bot Telegram: lihat A5 rinci di bawah** | `PANDUAN.md` §4 |
| A6 | Buat dan uji sampai 3 jadwal, satu per satu; uji dengan `run --wait` sebelum dinyatakan aktif | `jadwal-openclaw.md` paket (§ jadwal; §"Mengelola jadwal") |
| A7 | Jalankan `cek-privasi-openclaw` (lihat bagian 6) | `PANDUAN.md` §3; `skills/cek-privasi-openclaw/SKILL.md` |
| A8 | Serah terima (bagian 7) | `CEKLIS.md` paket |

### A5 rinci: BotFather + pairing dikerjakan UNTUK member (member yang mengetik token)
Urutan mengikuti `PANDUAN.md` §4. Pembagian peran:
1. Teknisi memandu; **member membuka Telegram di HP-nya**, mencari @BotFather, mengirim
   `/newbot`, memberi nama bot. **Token muncul di layar HP member.**
2. Member **menyalin token sendiri** dan menempelnya di terminal/chat OpenClaw di komputernya,
   memakai perintah dari `PANDUAN.md` §4 (`openclaw channels add --channel telegram --token
   <token>`). Teknisi hanya menunjukkan perintahnya; teknisi **tidak melihat, menyalin, atau
   mencatat token**. Bila token terlihat di layar bersama, jangan menyalin; jelaskan bahwa bila
   khawatir, member bisa menerbitkan ulang token lewat @BotFather (`/revoke`, bila tersedia
   di BotFather saat itu).
3. Member mengirim "halo" ke bot barunya (memicu pairing), lalu pairing disetujui: `openclaw
   pairing list telegram` dan `openclaw pairing approve telegram <KODE>` (kode berlaku 1 jam;
   salinan dari `PANDUAN.md` §4).
4. ID chat Telegram: member membuka @userinfobot. **Member menyimpan** angka itu di catatan
   pribadinya. Untuk membuat jadwal, member yang mengetik/menempelkan ID pada perintah `--to`.
   Jangan menulis ID itu di tiket/catatan Komunitech.
5. Uji: bot membalas "halo". Tes kiriman dari jadwal via `openclaw automations run <id> --wait`.

Bila gagal: token salah ketik (spasi), pairing belum disetujui. Ikuti "Kalau gagal" di
`PANDUAN.md` §4.

## 3. Layanan B: pasang 1 aplikasi lokal

Pilih panduan sesuai aplikasi dan **ikuti persis, termasuk pengamanan wajib** ("hanya bisa
dibuka dari komputer sendiri", akun admin dibuat member, cadangan, uji pulih):

| Aplikasi | Panduan acuan |
|---|---|
| Vikunja | `docs/panduan-vikunja.md` (skill `vikunja-tugas`) |
| Dolibarr | `docs/panduan-dolibarr.md` (skill `dolibarr-usaha`) |
| Grist | `docs/panduan-grist.md` (skill `grist-usaha`) |
| Uptime Kuma | `docs/panduan-uptime-kuma.md` |
| Open Notebook | `docs/panduan-open-notebook.md` (skill `notebook-riset-lokal`) |
| SiYuan | `docs/panduan-siyuan.md` (skill `siyuan-sop`) |
| Datasette | `docs/panduan-datasette.md` |
| Frappe Books | skill `frappe-books-usaha` (`skills/frappe-books-usaha/README.md`) |

Aturan tambahan:
- [ ] Unduh **hanya dari sumber resmi** dan cek checksum bila panduan mengajarkannya.
- [ ] Buat akun admin: **member yang mengetik password** (jangan dicatat).
- [ ] Jangan port forwarding/tunnel/akses dari luar jaringan (di luar cakupan; panduan
      aplikasi menjelaskan alasannya).
- [ ] Lakukan uji pengamanan dari HP (bila panduan meminta) dan uji cadangan-pulih.
- [ ] Jadwal laporan ke Telegram: ikuti bagian jadwal panduan aplikasi atau `PANDUAN.md` paket;
      uji dengan `run --wait`.
- [ ] Catat versi aplikasi yang terpasang di catatan serah terima.
- [ ] Beri tahu jujur bagian panduan yang berstatus "belum dicoba langsung" (mis. Windows/macOS
      tertentu); bila terjadi hal tak terduga, catat untuk kurator.

## 4. Layanan C: mesin 24 jam

Bacaan wajib: `skills/laporan-otomatis-terjadwal/references/mesin-24-jam.md` dan bagian
prasyarat mesin di `PANDUAN.md` paket (§0 no. 2). Jujur kepada member: perangkat/VPS **milik
dan tanggungan member**; tidak ada jaminan uptime.

**C1 mini PC/laptop:**
- [ ] Matikan mode tidur/hibernasi saat colok listrik; layar boleh mati.
- [ ] Setel agar menyala otomatis setelah listrik padam bila BIOS mendukung.
- [ ] Pastikan Gateway OpenClaw hidup setelah komputer dinyalakan ulang. **Cara membuatnya
      jalan otomatis: ikuti dokumentasi resmi OpenClaw untuk versi terpasang.** Repo ini belum
      memuat perintah terverifikasi untuk hal itu; jangan mengarang. Catat perintah yang berhasil
      untuk diusulkan ke kurator.
- [ ] **Uji restart:** matikan/nyalakan komputer, tunggu, lalu `openclaw automations run <id>
      --wait` dan cek jadwal berikutnya tiba (atau uji jadwal 5 menit kemudian dengan `--at`
      bila dokumen jadwal paket memuat contohnya).
- [ ] Laptop: setel agar tutup layar tidak membuatnya tidur; beri tahu risiko panas.

**C2 VPS milik member:**
- [ ] **Member** membuat akun VPS dan memberi akses ke teknisi sekadar sesi (kunci SSH baru
      yang dicabut setelah sesi; **jangan** simpan kunci/password member).
- [ ] Pengamanan dasar (pembaruan sistem, akun bukan root, firewall). OpenClaw tidak dibuka ke
      internet publik.
- [ ] Pasang OpenClaw mengikuti panduan VPS resmi OpenClaw.
- [ ] Uji restart VPS dan jadwal.
- [ ] Ingatkan: data tersimpan di VPS milik member (bukan server Komunitech), dan kunci model AI
      berada di VPS itu; tanggung jawab keamanan VPS pada member setelah serah terima.

## 5. Layanan D: pendampingan bulanan

Per bulan:
- [ ] Cek jadwal masih aktif: `openclaw automations list --all` (perintah dari
      `jadwal-openclaw.md` §"Mengelola jadwal"); uji satu jadwal dengan `run --wait`.
- [ ] Jalankan ulang `cek-privasi-openclaw`, terutama jika member menambah skill/kanal.
- [ ] Bantu update skill (salinan baru dari member area, `openclaw skills install ... --global`).
- [ ] Catat hasil di catatan pendampingan (tanpa data pelanggan, tanpa token).
- [ ] Plus: tambah 1 jadwal/perubahan kecil, uji, dan perbarui ceklis.

## 6. Ceklis privasi (`cek-privasi-openclaw`)

Jalankan skill **bersama member** dengan mengetik "cek privasi saya" (`PANDUAN.md` §3). Skill
memakai `openclaw security audit --json` dan pengecekan `config get`/`approvals get` yang
sudah tertulis di `skills/cek-privasi-openclaw/SKILL.md` dan `references/openclaw.md`.
Wajib terkonfirmasi sebelum serah terima:
- [ ] Laporan lampu lalu lintas sudah dibaca bersama member; setiap 🔴/🟡 yang disetujui
      diperbaiki **satu per satu** dengan penjelasan dampaknya.
- [ ] Kanal Telegram: `dmPolicy` tidak `open`; hanya pemilik yang boleh mengirim perintah.
- [ ] Perintah komputer (exec): member tahu status bawaannya dan sudah memilih setelan yang
      dipahami (lihat skill untuk rekomendasinya).
- [ ] Ada info bahwa isi pesan yang diproses dikirim ke penyedia model AI pilihan member
      (kecuali model lokal).
- [ ] Data berada di komputer/mesin member (`~/.openclaw`), bukan server Komunitech.
- [ ] Tidak ada nama/nomor/isi chat pelanggan di laporan yang dikirim ke chat.
- [ ] Bila agen CS aktif: mode Copilot, tidak ada auto-reply ke pelanggan, tidak ada broadcast.
- [ ] Bila ada data pelanggan: singgung UU PDP secara ringkas sesuai skill (bukan nasihat
      hukum).
- [ ] Jalankan ulang setelah menambah kanal/skill baru (khususnya setelah WhatsApp).

## 7. Serah terima (semua layanan)

- [ ] `CEKLIS.md` paket (`solusi-vip/<paket>/CEKLIS.md`) dicentang bersama member; salinan
      diberikan ke member (tanpa data pelanggan). Simpan di Komunitech hanya versi tanpa data
      sensitif.
- [ ] Setiap jadwal: diuji sekali (`run --wait`), nama/ID job dicatat (bukan ID chat).
- [ ] Member tahu cara: melihat jadwal (`openclaw automations list --all`), menjeda
      (`disable <id>`), dan menjalankan `cek-privasi-openclaw`.
- [ ] Member paham batasan: mesin mati = laporan tidak terkirim; OpenClaw tidak posting otomatis
      ke IG/TikTok/FB; AI menyiapkan draf, manusia yang mengirim.
- [ ] Semua token/password ada **hanya** di perangkat/catatan member. Teknisi menghapus
      apa pun yang sempat tersalin (clipboard, catatan sementara), menutup akses jarak jauh, dan
      (untuk VPS) mencabut kunci SSH sesi.
- [ ] Aplikasi (B): akun admin milik member, cadangan pertama sukses, uji pulih sudah dicoba.
- [ ] Jelaskan garansi (bila disetujui pemilik) dan cara menghubungi Komunitech.
- [ ] Tanda tangan/paraf serah terima di `CEKLIS.md`.
- [ ] Catatan internal tiket: nama usaha, layanan, tanggal, durasi, masalah yang perlu diperbaiki
      di dokumen (untuk kurator). **Tanpa** data pribadi member/pelanggan.

## 8. Bila ada masalah
- Perintah OpenClaw menolak/berubah: berhenti, jalankan `--help` perintah itu, jangan
  improvisasi; laporkan ke kurator agar dokumen diperbarui.
- Member tidak sengaja membagikan token: sarankan menerbitkan ulang token di @BotFather dan
  memperbarui kanal; jangan menyimpan token lama.
- Member ingin fitur di luar cakupan: tolak sopan (bagian 0 no. 6) atau tawarkan alternatif
  yang sesuai keputusan pemilik.

---

## Lampiran 1. Jalur WhatsApp (hanya bila semua syarat terpenuhi)

Baca `solusi-vip/<paket>/jadwal-openclaw.md` bagian "WhatsApp" dan
`skills/agen-cs-toko/references/eskalasi-dan-kanal.md` (urutan setup WA yang terverifikasi).

Syarat (semua wajib):
- [ ] **Nomor terpisah** (bukan nomor toko/klinik/CS yang dikenal pelanggan).
- [ ] Hanya untuk notifikasi ke **pemilik sendiri**.
- [ ] **Formulir persetujuan risiko** (lampiran 2) ditandatangani/dijawab tertulis oleh member.
- [ ] Tidak ada broadcast. Agen CS di WA = Copilot.
- [ ] Setelah menautkan nomor: jalankan `cek-privasi-openclaw`. Pastikan `dmPolicy` =
      `allowlist` (bukan `pairing`/`open`) dan `allowFrom` hanya nomor pemilik.

Urutan perintah (dari `skills/agen-cs-toko/references/eskalasi-dan-kanal.md` §setup dan
`skills/laporan-otomatis-terjadwal/references/openclaw.md`; ganti nama akun bila perlu):
tambahkan kanal (`openclaw channels add --channel whatsapp`), **atur allowlist dulu**, baru
login QR (`openclaw channels login --channel whatsapp`). **Member yang memindai QR dengan HP
nomor terpisahnya** dan yang mengetik nomornya sendiri. Nomor itu tidak dicatat di sistem
Komunitech. Catat: pengiriman nyata ke WA ⚠️ belum terverifikasi ujung ke ujung; sampaikan
jujur ke member.

## Lampiran 2. Formulir persetujuan risiko WhatsApp (dibaca dan dijawab member)

> **Persetujuan penggunaan nomor WhatsApp untuk OpenClaw**
>
> Saya, pemilik usaha ____________ (nama usaha), memahami bahwa:
> 1. OpenClaw memakai **WhatsApp Web** (jalur tidak resmi, tersambung lewat pemindaian QR).
>    Ketentuan layanan WhatsApp melarang pesan otomatis/massal, sehingga **nomor bisa
>    diblokir**. Untuk pesan ke diri sendiri risikonya rendah, tetapi tetap ada.
> 2. Saya memakai **nomor terpisah** yang **bukan** nomor toko/klinik/layanan pelanggan, dan
>    kehilangan nomor itu tidak akan mengganggu usaha saya.
> 3. Pesan hanya dikirim **ke saya sendiri**. Tidak ada broadcast/pesan massal. Untuk
>    pelanggan, AI hanya menyiapkan draf dan **saya/staf yang mengirim**.
> 4. Telegram tersedia sebagai alternatif tanpa risiko blokir, dan saya memilih WhatsApp atas
>    keputusan sendiri.
> 5. Komunitech tidak bertanggung jawab atas pemblokiran nomor.
>
> Tulis "Ya, saya mengerti risikonya" beserta tanggal:
> ______________________________ (diisi member)
>
> Bukti: simpan salinan **di pihak member**; Komunitech hanya mencatat "persetujuan diterima"
> dan tanggalnya, tanpa nomor telepon.
