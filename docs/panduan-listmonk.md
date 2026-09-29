# Panduan listmonk: Newsletter Gratis Pengganti Mailchimp (bahasa awam)

listmonk adalah program **gratis dan open-source** (lisensi AGPL-3.0) untuk mengelola **daftar pelanggan email dan mengirim newsletter**: impor kontak, buat email, jadwalkan, lihat siapa yang membuka dan mengklik. Program ini jalan di **komputer/server Anda sendiri**, jadi tidak ada biaya bulanan per jumlah kontak seperti Mailchimp. Yang tetap perlu ada: **layanan pengirim email (SMTP)** dan **domain email Anda** (bagian 8-9). Panduan ini menyiapkan listmonk agar bisa dioperasikan skill **listmonk Newsletter** (`listmonk-newsletter`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: sewa & siapkan server, domain + HTTPS, pasang listmonk, sambungkan SMTP, verifikasi domain (SPF/DKIM/DMARC), formulir pendaftaran di website, akun API untuk AI, dan cadangan otomatis. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan proyek listmonk maupun pembuatnya. "listmonk" adalah nama milik pengembangnya; panduan ini tulisan sendiri.

**Status panduan (29 September 2026).** Ditulis berdasarkan dokumentasi resmi listmonk dan **uji nyata listmonk 6.2.0** oleh Komunitech (image Docker resmi + PostgreSQL 17, port hanya `127.0.0.1`, SMTP penampung lokal): instalasi, login, pengguna API berperan terbatas, impor, konfirmasi double opt-in, uji kirim, jadwal, kirim, hitung buka/klik. **Belum dicoba langsung:** pemasangan binary tanpa Docker (lampiran), HTTPS di server sungguhan, pengiriman lewat Brevo/Amazon SES sungguhan, Windows/macOS. Bila tampilan di layar berbeda, ikuti tulisan di layar atau hubungi kami. **PERLU UJI NYATA** untuk bagian-bagian itu.

## Daftar isi
1. Sebelum mulai: apa yang dibutuhkan
2. Pilih tempat memasang (komputer sendiri atau server)
3. Pasang Docker (Windows / macOS / Linux)
4. Pasang listmonk dengan Docker Compose
5. Login pertama & ganti sandi
6. Pengaturan dasar (bahasa Indonesia, alamat, pengirim)
7. Akun khusus AI (pengguna API, izin terbatas)
8. Layanan pengirim email (SMTP): Brevo, Amazon SES, dll.
9. Verifikasi domain (SPF, DKIM, DMARC)
10. Formulir pendaftaran & persetujuan (UU PDP)
11. Cadangan, update, copot pasang
12. Masalah umum
13. Lampiran: pasang tanpa Docker (binary + PostgreSQL)

---

## 1. Sebelum mulai: apa yang dibutuhkan
- **Komputer/server** yang mampu menjalankan Docker (RAM 2 GB cukup untuk ribuan kontak).
- **Alamat email pengirim di domain sendiri** (mis. `halo@tokosaya.id`). Email dari `@gmail.com`/`@yahoo.com` yang dikirim lewat server lain sering ditolak/masuk spam.
- **Akun layanan SMTP** (bagian 8). listmonk *mengelola* daftar dan isi email; ia perlu "tukang pos" untuk mengantar.
- **Daftar kontak yang sah**: hanya orang yang mendaftar/setuju menerima email Anda. Jangan pernah mengirim ke daftar hasil beli, sewa, atau scraping (bagian 10).

## 2. Pilih tempat memasang
| Pilihan | Cocok untuk | Catatan |
|---|---|---|
| **Laptop/PC Anda** | Coba-coba, newsletter jarang (bulanan) dengan jadwal manual | listmonk harus **menyala** saat email dijadwalkan/dikirim. Tautan berhenti/konfirmasi di email menunjuk ke alamat listmonk, jadi penerima **tidak bisa** mengkliknya bila listmonk hanya di laptop Anda. |
| **Server/VPS sendiri** (disarankan) | Newsletter rutin | Perlu domain + HTTPS agar tautan konfirmasi/berhenti bisa dibuka penerima. Biaya VPS kecil ±Rp50.000-150.000/bulan (cek penyedia). |
| **Jasa setup Komunitech** | Tidak mau teknis | Kami pasang & rawat. |

Kesimpulan jujur: untuk newsletter sungguhan ke pelanggan, listmonk **harus dapat diakses dari internet lewat HTTPS** (bagian 4, langkah HTTPS). Coba dulu di laptop untuk belajar, lalu pindah ke server.

## 3. Pasang Docker
Docker adalah "kotak siap pakai" untuk menjalankan program. Pasang dari situs resmi https://docs.docker.com/get-started/get-docker/.
- **Windows 10/11:** pasang *Docker Desktop*; aktifkan WSL 2 bila diminta; restart. Buka *PowerShell* untuk perintah di bawah.
- **macOS:** pasang *Docker Desktop* (pilih Apple Silicon atau Intel sesuai Mac Anda).
- **Linux (Ubuntu/Debian):** ikuti "Docker Engine" + "Docker Compose plugin" di situs resmi. Cek: `docker --version` dan `docker compose version` harus tampil.

## 4. Pasang listmonk dengan Docker Compose
1. Buat folder, mis. `listmonk`, lalu di dalamnya buat file `docker-compose.yml`:
```yaml
services:
  db:
    image: postgres:17
    restart: unless-stopped
    environment:
      POSTGRES_USER: listmonk
      POSTGRES_PASSWORD: GANTI-SANDI-DB-PANJANG-ACAK
      POSTGRES_DB: listmonk
    volumes:
      - ./data-db:/var/lib/postgresql/data
  app:
    image: listmonk/listmonk:v6.2.0
    restart: unless-stopped
    depends_on: [db]
    ports:
      - "127.0.0.1:9000:9000"   # hanya bisa dibuka dari komputer ini
    environment:
      LISTMONK_app__address: 0.0.0.0:9000
      LISTMONK_db__host: db
      LISTMONK_db__port: 5432
      LISTMONK_db__user: listmonk
      LISTMONK_db__password: GANTI-SANDI-DB-PANJANG-ACAK
      LISTMONK_db__database: listmonk
      LISTMONK_ADMIN_USER: admin
      LISTMONK_ADMIN_PASSWORD: GANTI-SANDI-ADMIN-PANJANG
    volumes:
      - ./unggahan:/listmonk/uploads
```
   Ganti kedua `GANTI-...` dengan sandi panjang dan acak (sandi DB harus sama di dua tempat). **Jangan bagikan file ini** dan jangan taruh di tempat publik. Versi dikunci (`v6.2.0`) agar tidak berubah sendiri; cek versi terbaru di https://github.com/knadh/listmonk/releases sebelum memasang.
2. **Pertama kali saja**, nyalakan database dulu, tunggu ±10 detik, lalu siapkan isinya:
```
docker compose up -d db
docker compose run --rm app ./listmonk --install --idempotent --yes
```
   Perintah kedua membuat tabel dan akun admin dari `LISTMONK_ADMIN_USER/PASSWORD` (jika muncul "connection refused", tunggu sebentar lalu ulangi). Sudah diuji: kedua perintah ini lalu langkah 3 menghasilkan halaman login yang bisa dibuka.
3. Nyalakan: `docker compose up -d`. Tunggu ±10 detik, buka **http://localhost:9000** di browser.
4. **HTTPS untuk server internet (Caddy, contoh):** arahkan domain (mis. `surat.tokosaya.id`) ke IP server; pasang Caddy dan isi `Caddyfile`:
```
surat.tokosaya.id {
    reverse_proxy 127.0.0.1:9000
}
```
   Caddy mengurus sertifikat HTTPS otomatis. Untuk Windows/macOS lokal, lewati langkah ini. Setelah HTTPS jalan, isi **Root URL** di bagian 6 dengan `https://surat.tokosaya.id`.
5. Halaman admin (`/admin`) sebaiknya **tidak** dibuka bebas ke internet: batasi lewat firewall/VPN bila memungkinkan, dan pakai sandi kuat. Portal publik (formulir & tautan berhenti) memang harus terbuka.

## 5. Login pertama & ganti sandi
Buka http://localhost:9000/admin, masuk dengan `admin` + sandi di file compose. Segera buka **Settings > Users** dan pastikan sandi admin kuat (ganti bila perlu). Hapus sandi dari file `docker-compose.yml` setelah selesai jika Anda mau (variabel admin hanya dipakai saat `--install`).

## 6. Pengaturan dasar (Settings)
- **General > Language:** pilih **Bahasa Indonesia**. Ini mengubah tampilan **dan email konfirmasi/berhenti** menjadi bahasa Indonesia (bawaan bahasa Inggris). Simpan; listmonk memuat ulang.
- **General > Root URL:** alamat listmonk yang bisa dibuka penerima (`https://surat.tokosaya.id`). Salah isi -> tautan konfirmasi/berhenti rusak.
- **General > Default 'From' e-mail:** mis. `Toko Saya <halo@tokosaya.id>` (alamat di domain yang sudah diverifikasi, bagian 9).
- **Privacy:** aktifkan **Allow blocklisting** (orang bisa menolak semua email), **Allow preferences** (kelola langganan), dan **Allow wiping** (orang bisa menghapus datanya sendiri) sesuai kebutuhan. Biarkan **pelacakan per-orang mati** bila tidak perlu (lebih ramah privasi; statistik agregat tetap ada).
- **Performance:** turunkan kecepatan kirim sesuai batas penyedia SMTP (mis. ±5-10 pesan per detik untuk paket gratis; ikuti aturan penyedia).

## 7. Akun khusus AI (pengguna API, izin terbatas)
Supaya AI tidak memegang kunci penuh:
1. **Settings > Users > User roles > Add:** buat peran, mis. `Agen Newsletter`, dengan izin: `subscribers:get`, `subscribers:get_all`, `subscribers:manage`, `subscribers:import`, `campaigns:get_all`, `campaigns:manage_all`, `campaigns:send`, `campaigns:get_analytics`, `lists:get_all`, `lists:manage_all`, `templates:get`, `media:get`, `media:manage`. **Jangan** beri `settings:*`, `users:*`, `roles:*`, `subscribers:sql_query`.
2. **Users > New:** jenis **API**, nama pengguna `agen`, pilih peran di atas. Setelah disimpan, listmonk menampilkan **token satu kali**: salin.
3. Di terminal Anda sendiri (bukan di chat AI): `python3 scripts/listmonk.py simpan-akun` (Windows: `python`/`py`), ketik nama pengguna, tempel token (tidak tampil). Cek: `python3 scripts/listmonk.py cek`.
4. Token bocor? Hapus pengguna itu di listmonk dan buat baru.
Catatan: izin `campaigns:send` memungkinkan mengirim; karena itu skill dijaga gerbang konfirmasi, tetapi **siapa pun yang memegang token itu bisa mengirim**. Simpan baik-baik.

## 8. Layanan pengirim email (SMTP)
Isi di **Settings > SMTP** lalu tombol *Test connection* dan simpan. **Harga & kebijakan berubah; cek halaman resmi sebelum memilih.**
| Pilihan | Gambaran (dicek 29 Sep 2026) | Catatan |
|---|---|---|
| **Brevo** (SMTP relay) | Paket gratis ±300 email/hari (sumber ringkasan pihak ketiga; cek https://www.brevo.com/pricing/) | Akun baru bisa ditinjau manual & wajib verifikasi pengirim/domain. Batas harian = maksimal ±9.000 email/bulan. Bila daftar lebih dari itu, perlu paket berbayar. |
| **Amazon SES** | ±US$0,10-0,16 per 1.000 email + kredit gratis untuk akun AWS baru (https://aws.amazon.com/ses/pricing/) | Sangat murah, tetapi setup lebih teknis: verifikasi domain, dan akun baru biasanya dalam mode terbatas (sandbox) sampai diajukan ke produksi. Tagihan dalam dolar. |
| **SMTP dari hosting/email domain Anda** | Biasanya ada batas kirim per jam yang kecil | Cocok untuk daftar kecil (ratusan). Batas per jam bisa membuat kiriman tertahan; cek aturan hosting. |
| **Gmail/Google Workspace SMTP** | Batas harian rendah, kebijakan ketat | Tidak disarankan untuk newsletter. |
Pesan penting: (1) verifikasi domain wajib (bagian 9); (2) mulai kirim kecil dulu ke daftar yang paling aktif; (3) penyedia dapat menangguhkan akun bila banyak email ditolak atau dilaporkan spam; (4) biaya SMTP tidak termasuk paket Komunitech.

## 9. Verifikasi domain (SPF, DKIM, DMARC)
Ini "surat izin" agar email atas nama `@tokosaya.id` dipercaya Gmail/Yahoo. Penyedia SMTP memberi **catatan DNS** (TXT/CNAME) yang harus ditambahkan di pengelola domain Anda (Niagahoster, Rumahweb, Cloudflare, dll.): **SPF** (siapa boleh mengirim), **DKIM** (tanda tangan), dan sebaiknya **DMARC** (kebijakan). Tunggu beberapa menit-jam sampai penyedia menyatakan "verified". Tanpa ini, kemungkinan besar email masuk spam atau ditolak. Cara mengujinya: kirim email uji dari skill lalu cek header "SPF/DKIM: pass" di Gmail (Tampilkan Asli).

## 10. Formulir pendaftaran & persetujuan (UU PDP)
Ringkasan praktis (bukan nasihat hukum): UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi mengharuskan dasar pemrosesan yang sah; untuk newsletter pemasaran, dasarnya adalah **persetujuan** orang tersebut.
- **Kumpulkan sendiri:** formulir di website (listmonk menyediakan halaman langganan publik untuk list bertipe *Public*), QR di kasir/kemasan, kolom "mau terima promo lewat email?" (kotak **tidak dicentang** dari awal) di formulir pesanan.
- **Jelaskan:** siapa Anda, email apa yang akan dikirim (promo/kabar), seberapa sering, dan bahwa bisa berhenti kapan saja.
- **Double opt-in:** orang menerima email konfirmasi dan harus klik. Ini bukti persetujuan terbaik dan mencegah email orang lain didaftarkan.
- **Simpan bukti:** asal & tanggal daftar (skill menyimpannya sebagai atribut saat impor).
- **Berhenti & hapus:** tiap email punya tautan berhenti; permintaan hapus data diproses (`hapus-pelanggan`).
- **Jangan:** membeli/menyewa daftar, mengambil email dari medsos/marketplace/grup, memasukkan pembeli marketplace begitu saja ke newsletter tanpa persetujuan.
Untuk kebutuhan hukum yang serius (mis. usaha besar, data sensitif), konsultasikan dengan konsultan hukum. Pastikan juga kebijakan privasi Anda mencantumkan newsletter (skill `kebijakan-privasi-pdp` dapat membantu menyusunnya).

## 11. Cadangan, update, copot pasang
- **Cadangan:** `docker compose exec db pg_dump -U listmonk listmonk > cadangan-listmonk.sql` (sekurangnya tiap minggu) + folder `unggahan`. Simpan salinan di tempat lain.
- **Update:** cadangkan dulu -> ubah nomor versi image di `docker-compose.yml` sesuai rilis baru (baca catatan rilis) -> `docker compose pull` -> `docker compose run --rm app ./listmonk --upgrade --yes` -> `docker compose up -d`.
- **Copot:** `docker compose down` (data tetap di folder `data-db`). Hapus folder itu hanya bila yakin tidak diperlukan.
- **Kewajiban lisensi AGPL-3.0:** memakai listmonk apa adanya untuk usaha Anda sendiri tidak mewajibkan apa pun. Bila Anda **mengubah kode** listmonk dan menyediakannya untuk orang lain lewat jaringan, Anda wajib membagikan kode hasil ubahan itu. Skill Komunitech adalah program terpisah dan tidak mengubah listmonk.

## 12. Masalah umum
| Gejala | Kemungkinan sebab | Solusi |
|---|---|---|
| `cek` -> "Tidak bisa menghubungi" | listmonk mati / alamat salah | `docker compose ps`; buka http://localhost:9000; `simpan-alamat` bila alamat lain |
| `cek` -> "Ditolak (403)" | Token salah/kedaluwarsa, peran kurang | Buat token baru (bagian 7) |
| Email uji tidak datang | SMTP belum benar / masuk spam / domain belum verifikasi | *Test connection* di Settings > SMTP; cek spam; bagian 9 |
| Tautan konfirmasi/berhenti mengarah ke `localhost` | Root URL belum diisi | Bagian 6 |
| Banyak email "bounce"/gagal | Alamat salah ketik, domain belum aman | Bersihkan daftar; periksa SPF/DKIM |
| "Dibuka" 0% | Wajar bila gambar diblokir/belum ada yang buka | Andalkan angka klik; tautan harus berakhiran `@TrackLink` |
| Kampanye terjadwal tidak jalan | listmonk mati pada jamnya | Pastikan komputer/server menyala |

## 13. Lampiran: pasang tanpa Docker (binary + PostgreSQL) — untuk teknisi
Belum diuji Komunitech; ikuti dokumentasi resmi https://listmonk.app/docs/installation/ sebagai acuan utama. Ringkasnya: pasang **PostgreSQL 12 atau lebih baru**, buat database dan pengguna; unduh binary rilis untuk sistem Anda dari https://github.com/knadh/listmonk/releases; jalankan `./listmonk --new-config` (menghasilkan `config.toml`, isi koneksi database), lalu `./listmonk --install` (pertama kali) dan `./listmonk`. Admin dapat diatur lewat `LISTMONK_ADMIN_USER` dan `LISTMONK_ADMIN_PASSWORD` saat `--install`. Jalankan sebagai layanan (systemd di Linux / Task Scheduler di Windows) agar hidup terus.
