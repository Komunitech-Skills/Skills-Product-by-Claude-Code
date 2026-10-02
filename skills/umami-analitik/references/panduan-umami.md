# Panduan Umami: Analitik Website Gratis Pengganti Google Analytics (bahasa awam)

Umami adalah program **gratis dan open-source** (lisensi MIT) untuk menghitung **pengunjung website**: berapa orang yang datang, halaman apa yang dibuka, datang dari Instagram/TikTok/Google/WhatsApp, pakai HP atau laptop, dari kota mana, dan berapa yang **klik tombol WhatsApp / Beli**. Umami **tidak memakai cookie** dan tidak menyimpan alamat IP, jadi tidak perlu spanduk "setuju cookie". Program ini jalan di **server Anda sendiri**: data tidak dititipkan ke Google, tanpa biaya bulanan. Panduan ini menyiapkan Umami agar bisa dibaca skill **Umami Analitik** (`umami-analitik`).

> **Tidak ingin repot?** Komunitech menyediakan **jasa setup berbayar**: sewa & siapkan VPS, domain + HTTPS, pasang Umami, pasang kode lacak di website/landing page Anda, tombol WA terlacak, tautan UTM untuk IG/TikTok/WA, akun + kunci API untuk AI, jadwal laporan mingguan ke Telegram, dan cadangan otomatis. Hubungi admin komunitech.com.

> Komunitech **tidak berafiliasi** dengan Umami Software, Inc.; "Umami" adalah nama milik pengembangnya.

**Status panduan (29 September 2026).** Dicocokkan dengan kode sumber & `docker-compose.yml` resmi Umami **3.4.0** (rilis terbaru, tag `v3.4.0`, 16 Sep 2026). Komunitech **menjalankan Umami 3.4.0 sungguhan** lewat **Docker** (image resmi `ghcr.io/umami-software/umami:3.4.0` + `postgres:15-alpine`, port hanya `127.0.0.1`), membuat website, akun "hanya lihat" lewat tim, kunci API, tautan pelacak, lalu mengirim kunjungan fiktif dan mencocokkan semua angka skill. **Belum dicoba langsung:** instalasi tanpa Docker (lampiran), HTTPS lewat Caddy di VPS sungguhan (bagian 4), Windows/macOS. Bila tampilan di layar Anda berbeda, ikuti tulisan di layar atau hubungi kami.

## Daftar isi
1. Sebelum mulai — di mana Umami dipasang?
2. Pasang dengan Docker Compose (cara resmi)
3. Menyalakan, login pertama, ganti sandi admin
4. **Pengamanan wajib** & HTTPS
5. Tambah website & pasang kode lacak (website, landing page, halaman link-bio)
6. Melacak klik tombol WhatsApp / Beli (event konversi)
7. Akun khusus AI ("hanya lihat") & kunci API
8. Tautan UTM untuk Instagram, TikTok, WhatsApp
9. Privasi: tanpa cookie & UU PDP
10. Cadangan, update, copot pasang
11. Masalah umum
12. Lampiran: pasang tanpa Docker (Node.js + PostgreSQL, untuk teknisi)

---

## 1. Sebelum mulai — di mana Umami dipasang?
Kode lacak di website Anda dijalankan oleh **browser pengunjung** (HP pembeli), lalu mengirim catatan kunjungan ke server Umami. Artinya:

| Pilihan | Cocok untuk | Catatan |
|---|---|---|
| **VPS milik sendiri** (mis. Rp50–150 ribu/bulan, RAM ≥ 1 GB) + domain/subdomain (mis. `analitik.tokosaya.id`) | **Pemakaian sungguhan** — website/landing page yang dibuka publik | Wajib HTTPS (bagian 4). Satu Umami bisa untuk banyak website |
| Laptop/PC sendiri (`http://localhost:3000`) | **Coba-coba** dan belajar menu | Pengunjung dari internet **tidak bisa** mengirim data ke laptop Anda → angka tetap 0 |

Kebutuhan: **Docker** + Docker Compose (gratis), ±20–40 menit, bisa menyalin-tempel perintah di terminal. Tidak perlu bisa memprogram.

**Sudah pakai Umami Cloud (umami.is)?** Skill ini dirancang dan diuji untuk Umami **yang Anda pasang sendiri**; Umami Cloud memakai alamat & kunci yang berbeda dan belum diuji Komunitech.

## 2. Pasang dengan Docker Compose (cara resmi)
Sumber resmi: https://github.com/umami-software/umami (README bagian "Installing with Docker"). Umami terdiri dari 2 "kotak" (container): **aplikasi Umami** dan **database PostgreSQL**. Komunitech membaca `docker-compose.yml` resmi versi 3.4.0 dan skrip awalnya: tidak ada perintah unduh-lalu-jalankan otomatis; saat menyala, Umami hanya menyiapkan tabel database lalu menjalankan server.

1. Buat folder, mis. `umami` di folder rumah Anda:
   ```bash
   mkdir -p ~/umami && cd ~/umami
   ```
2. Buat 2 kata sandi acak (salin hasilnya):
   ```bash
   openssl rand -hex 32     # untuk APP_SECRET
   openssl rand -hex 16     # untuk sandi database
   ```
   (Windows tanpa `openssl`: ketik 40+ huruf/angka acak sendiri.)
3. Buat file `docker-compose.yml` (Linux/Mac: `nano docker-compose.yml`, simpan Ctrl+O Enter, keluar Ctrl+X; Windows: Notepad, "Simpan sebagai" → Semua file). Isi — ini `docker-compose.yml` resmi 3.4.0 dengan **4 perubahan pengamanan** (ditandai `# UBAH`):
   ```yaml
   services:
     umami:
       image: ghcr.io/umami-software/umami:3.4.0        # UBAH: kunci versi (resmi: latest)
       ports:
         - "127.0.0.1:3000:3000"                        # UBAH: hanya komputer ini (resmi: "3000:3000")
       environment:
         DATABASE_URL: postgresql://umami:SANDI_DB@db:5432/umami
         APP_SECRET: ISI_HASIL_OPENSSL_32               # UBAH: jangan pakai contoh resmi
         DISABLE_TELEMETRY: 1                           # UBAH: tidak mengirim statistik pemakaian ke pembuat
       depends_on:
         db:
           condition: service_healthy
       init: true
       restart: always
       healthcheck:
         test: ["CMD-SHELL", "curl http://localhost:3000/api/heartbeat"]
         interval: 5s
         timeout: 5s
         retries: 5
     db:
       image: postgres:15-alpine
       environment:
         POSTGRES_DB: umami
         POSTGRES_USER: umami
         POSTGRES_PASSWORD: SANDI_DB                    # sama dengan SANDI_DB di atas
       volumes:
         - umami-db-data:/var/lib/postgresql/data
       restart: always
       healthcheck:
         test: ["CMD-SHELL", "pg_isready -U $${POSTGRES_USER} -d $${POSTGRES_DB}"]
         interval: 5s
         timeout: 5s
         retries: 5
   volumes:
     umami-db-data:
   ```
   Ganti `SANDI_DB` (2 tempat) dan `ISI_HASIL_OPENSSL_32`. Ingin verifikasi 2 langkah (2FA) untuk login admin? Tambahkan `TWO_FACTOR_ENCRYPTION_KEY: <hasil openssl rand -hex 32 lainnya>` di bawah `APP_SECRET` (baris ini ada di file resmi berisi contoh; **jangan** biarkan nilai contohnya).
4. Nyalakan (pertama kali mengunduh ±300–500 MB, beberapa menit):
   ```bash
   docker compose up -d
   ```
5. Cek: `docker compose ps` → kedua kotak `running`/`healthy`. Buka http://localhost:3000.

## 3. Menyalakan, login pertama, ganti sandi admin
- Login pertama: nama **`admin`**, sandi **`umami`** (bawaan resmi). **Segera ganti**: menu profil kanan atas → **Profile / Profil** → **Change password / Ganti kata sandi** → sandi panjang (simpan di pengelola sandi).
- Bahasa Indonesia: menu profil → **Language / Bahasa** → *Bahasa Indonesia*. Panduan ini menyebut nama menu Inggris / Indonesia.
- Cek dari AI: "Cek Umami saya sudah nyambung belum?" (skill memakai `http://localhost:3000` secara bawaan).
- Docker menyalakan ulang Umami otomatis setelah komputer restart (`restart: always`), selama Docker ikut menyala. Manual: `cd ~/umami && docker compose up -d`. Mematikan: `docker compose down` (data aman).

## 4. Pengamanan wajib & HTTPS
| Langkah | Kenapa |
|---|---|
| Port `127.0.0.1:3000:3000` (bagian 2) | Umami tidak langsung terbuka ke internet; hanya lewat HTTPS (di bawah) |
| Ganti sandi admin `umami` (bagian 3) | Sandi bawaan diketahui semua orang |
| `APP_SECRET` & sandi database acak | Nilai contoh resmi sama untuk semua orang |
| Akun khusus AI "hanya lihat" (bagian 7) | Kunci yang dipegang AI tidak bisa menghapus/mengubah apa pun |
| Aktifkan 2FA untuk admin (opsional, bagian 2) | Halaman login Umami ikut terbuka ke internet |

**HTTPS di VPS (untuk website publik).** Kode lacak harus bisa dijangkau browser pengunjung lewat `https://`. Cara paling sederhana: pasang **Caddy** (gratis, sertifikat HTTPS otomatis) di VPS yang sama, arahkan DNS `analitik.tokosaya.id` ke IP VPS, lalu isi `/etc/caddy/Caddyfile`:
```
analitik.tokosaya.id {
    reverse_proxy 127.0.0.1:3000
}
```
lalu `sudo systemctl reload caddy`. Instal Caddy dari paket resmi (https://caddyserver.com/docs/install), **bukan** dari skrip tak dikenal. *(Langkah HTTPS ini mengikuti dokumentasi resmi Caddy; belum dijalankan Komunitech di VPS sungguhan — jasa setup kami menanganinya.)*

Skill hanya mau menghubungi alamat internet yang **ber-HTTPS** dan **disimpan pengguna sendiri**:
```bash
python3 ~/.openclaw/skills/umami-analitik/scripts/umami.py simpan-alamat https://analitik.tokosaya.id
```
(Windows: `python` atau `py`. Ganti `~/.openclaw/skills` dengan folder skill di platform Anda — lihat `docs/instalasi.md`.) Alamat kantor/jaringan lokal (`192.168.x.x`) boleh `http://` dengan peringatan.

## 5. Tambah website & pasang kode lacak
**a. Tambah website:** **Settings / Pengaturan → Websites / Situs web → Add website / Tambah situs web** → isi *Name* (mis. "Keripik Bu Sri") dan *Domain* (mis. `keripikbusri.id`, tanpa `https://`) → Save. Klik website itu → **Tracking code / Kode lacak** → salin kode seperti:
```html
<script defer src="https://analitik.tokosaya.id/script.js" data-website-id="1a2b3c4d-...."></script>
```

**b. Tempel kode lacak** di bagian `<head>` setiap halaman (sekali di template sudah cukup):
| Platform | Di mana menempel |
|---|---|
| HTML sendiri / hosting biasa | Sebelum `</head>` di setiap file (atau file header bersama) |
| WordPress | Plugin penyisip kode header (mis. "WPCode"/"Insert Headers and Footers") → *Header*; atau *Appearance → Theme File Editor → header.php* |
| Blogger | *Tema → Edit HTML* → tempel sebelum `</head>` |
| Pembuat landing page / toko online | Cari menu **Custom code / Header code / Tracking script / Kode kustom**. Tidak ada menu itu → pembuat itu tidak mengizinkan script; pakai tautan pelacak (c) |
| Halaman link-bio (Linktree, dll.) | Biasanya **tidak** bisa ditempeli script → pakai **tautan pelacak (c)** untuk tiap tombol, atau buat halaman link-bio sendiri (HTML sederhana) yang memakai kode lacak |

Opsi berguna (tambahkan ke tag `<script>`): `data-domains="keripikbusri.id"` = hanya menghitung dari domain asli (bukan saat Anda uji di komputer sendiri). **Jangan** pakai `data-exclude-search="true"` bila memakai UTM (UTM ada di bagian "search" alamat).

**Cek:** buka website Anda dari HP → di Umami, buka website itu → **Realtime / Waktu nyata** → kunjungan Anda muncul dalam hitungan detik. Pemblokir iklan (adblock) di browser pengunjung bisa memblokir kode lacak, jadi angka Umami biasanya **sedikit lebih rendah** dari kenyataan.

**c. Tautan pelacak (Links / Tautan)** — untuk tempat yang tidak bisa ditempeli script: bio Instagram/TikTok, QR di kemasan, tombol WA di link-bio. Menu **Links / Tautan → Create link** → isi *Name* (mis. "WA order (bio IG)"), *URL* tujuan (mis. `https://wa.me/62812xxxx?text=Halo`) dan *Slug* (min. 8 huruf, mis. `wa-busri-bio`). Hasilnya `https://analitik.tokosaya.id/q/wa-busri-bio` → pasang di bio. Setiap klik tercatat lalu diteruskan ke tujuan. Skill: "link di bio IG diklik berapa kali?" → perintah `tautan`. *(Diuji Komunitech pada Umami 3.4.0.)*

## 6. Melacak klik tombol WhatsApp / Beli (event konversi)
Tambahkan atribut `data-umami-event` pada tombol/tautan (kode lacak bagian 5 wajib sudah terpasang):
```html
<a href="https://wa.me/6281234567890?text=Halo%20mau%20pesan"
   data-umami-event="klik-wa" data-umami-event-tombol="hero">Pesan via WhatsApp</a>

<button data-umami-event="beli" data-umami-event-produk="Keripik Balado 250 g"
        data-umami-event-nilai="25000">Beli Sekarang</button>
```
- `data-umami-event` = nama event (pakai nama pendek & konsisten: `klik-wa`, `beli`, `daftar`, `unduh-katalog`).
- `data-umami-event-<nama>` = keterangan tambahan (produk, tombol mana). Keterangan bernama `nilai` dijumlahkan skill sebagai "total nilai klik" — **bukan** omzet resmi (orang bisa klik lalu batal).
- Halaman "Terima kasih" setelah pembayaran juga bisa menjadi ukuran konversi: skill menampilkan jumlah pengunjungnya di `halaman`.
- **Jangan** mengirim data pribadi pembeli (nama, nomor HP, email, alamat) ke event.

## 7. Akun khusus AI ("hanya lihat") & kunci API
Jangan berikan kunci akun admin ke AI. Di Umami 3.4.0, akun "hanya lihat" membaca website **lewat tim**:
1. **Buat tim:** Settings → **Teams / Tim** → Create team → nama mis. "Usaha Saya".
2. **Pindahkan website ke tim:** Settings → Websites → pilih website → **Transfer** → pilih tim. (Admin tetap pemilik tim; website tidak berubah.)
3. **Buat akun AI:** menu **Admin / Pengelola → Users / Pengguna → Create user** → *Username* `agen-baca`, sandi panjang acak, *Role* **View only / Hanya melihat** → Save.
4. **Masukkan ke tim:** Settings → Teams → tim itu → **Members** → **Add member / Tambah anggota** → pilih `agen-baca`, *Role* **View only** (tersimpan sebagai *team view only*).
5. **Buat kunci API (oleh akun AI itu sendiri):** logout, login sebagai `agen-baca` → **Settings → API keys** → Create → beri nama mis. `openclaw-laptop` → **kunci (diawali `umami_`) hanya tampil sekali** → langsung simpan ke skill (langkah 6), jangan ditempel di chat/catatan.
6. **Simpan kunci** di terminal Anda sendiri (bukan di chat):
   ```bash
   python3 ~/.openclaw/skills/umami-analitik/scripts/umami.py simpan-kunci
   ```
   Tersimpan di `~/.komunitech/umami-kunci.txt` (hanya bisa dibaca akun komputer Anda). Ganti kunci: ulangi dengan `--ya`.
7. **Periksa:** "Cek Umami saya" → AI menampilkan akun `agen-baca`, peran *view-only*, dan daftar website.

Catatan: fitur kunci API pada Umami self-hosted 3.4.0 (menu Settings → API keys, dipakai lewat header Bearer) **belum tercantum di dokumentasi resmi** (docs.umami.is hanya menyebut kunci API untuk Umami Cloud dan login untuk self-hosted); ini berdasarkan uji Komunitech pada Umami 3.4.0 asli, bukan dokumen resmi, dan bisa berubah di versi lain. Kunci API tidak bisa dipakai untuk menu akun/admin (Umami memblokirnya), dan akun *view-only* ditolak saat mencoba membuat website — sesuai harapan. Kunci bocor/perangkat hilang → login sebagai `agen-baca` → Settings → API keys → hapus kunci itu, buat baru. Umami versi lama tanpa menu API keys: simpan **sandi** `agen-baca` lewat `simpan-kunci` dan set ENV `UMAMI_USERNAME=agen-baca` (akun ber-2FA tidak bisa dipakai cara ini).

## 8. Tautan UTM untuk Instagram, TikTok, WhatsApp
UTM = keterangan kecil di belakang alamat website agar Umami tahu **kampanye mana** yang membawa pengunjung. Tanpa UTM, klik dari WhatsApp/Telegram/QR tercatat sebagai "Langsung" (aplikasi tidak mengirim alamat asal).

Bentuk: `https://tokoanda.id/?utm_source=SUMBER&utm_medium=JENIS&utm_campaign=NAMA-PROMO` (alamat sudah ada `?` → sambung dengan `&`).

| Dipasang di | utm_source | utm_medium | Contoh utm_campaign |
|---|---|---|---|
| Bio Instagram | `instagram` | `bio` | `katalog` |
| Story/feed Instagram | `instagram` | `story` / `post` | `promo-gajian-okt` |
| Bio TikTok | `tiktok` | `bio` | `katalog` |
| Video TikTok (komentar tersemat) | `tiktok` | `video` | `promo-gajian-okt` |
| Status WhatsApp | `whatsapp` | `status` | `promo-gajian-okt` |
| Grup WhatsApp reseller/komunitas | `whatsapp` | `grup` | `reseller-okt` |
| Balasan chat WA ke pelanggan | `whatsapp` | `chat` | `follow-up` |
| Facebook | `facebook` | `post` / `grup` | `promo-gajian-okt` |
| QR di kemasan/brosur | `qr` | `kemasan` / `brosur` | `repeat-order` |
| Iklan berbayar (Meta/TikTok Ads) | `instagram` / `tiktok` | `paid_social` | nama iklan |

Aturan: **huruf kecil semua, pakai tanda hubung**, konsisten (jangan kadang `IG` kadang `instagram`). Satu kampanye = satu nama. Alamat panjang? Masukkan alamat ber-UTM itu sebagai URL tujuan **tautan pelacak** (bagian 5c) agar pendek & rapi.

**Pembuat UTM cepat (tanpa aplikasi):** minta AI: "Buatkan tautan UTM untuk https://keripikbusri.id, promo gajian Oktober, untuk bio IG, story IG, status WA, dan grup reseller" → AI menyusun alamatnya dengan tabel di atas. Setelah kampanye jalan: "Promo gajian Oktober hasilnya gimana?" → skill `utm` + `konversi`.

Keterbatasan (diuji pada 3.4.0): Umami mencatat UTM pada halaman yang dibuka, **tidak** pada event klik. Skill bisa menyebut "promo-gajian-okt membawa 120 pengunjung" dan "klik WA total 30", tetapi tidak "30 klik WA berasal dari promo-gajian-okt". Untuk itu, pakai tautan WA/tautan pelacak khusus per kampanye.

## 9. Privasi: tanpa cookie & UU PDP
- **Tanpa cookie**: kode lacak Umami tidak memasang cookie. Browser hanya menyimpan tanda "jangan lacak saya" bila pengunjung memilih keluar.
- **Tidak menyimpan IP & identitas**: Umami membuat kode pengunjung acak dari website + IP + jenis browser + "garam" yang berganti **tiap bulan**, lalu membuang IP-nya. Yang disimpan: halaman, waktu, asal klik, jenis perangkat/browser/OS, bahasa, negara/kota perkiraan. (Diperiksa Komunitech pada tabel database Umami 3.4.0: tidak ada kolom IP maupun user-agent.)
- **Data di server Anda sendiri**, tidak dibagikan ke pihak ketiga.
- **UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi (UU PDP)**, berlaku penuh sejak 17 Oktober 2024: alamat IP tetap diproses sesaat saat kunjungan. Praktik yang disarankan: sebutkan di **kebijakan privasi** website Anda bahwa Anda memakai analitik tanpa cookie (Umami) di server sendiri untuk statistik kunjungan agregat; jangan mengirim data pribadi ke event (bagian 6); batasi akses dashboard; hapus data lama yang tidak diperlukan (Settings → Websites → *Reset* / hapus website). Ini **bukan nasihat hukum** — untuk usaha dengan data pelanggan besar, konsultasikan ke konsultan hukum/DPO.

## 10. Cadangan, update, copot pasang
**Cadangan** (minimal mingguan & sebelum update):
```bash
cd ~/umami && docker compose exec db pg_dump -U umami umami > umami-backup-$(date +%F).sql
```
Simpan file `.sql` di tempat lain (drive/flashdisk). Pulihkan (ke Umami kosong versi sama): `cat umami-backup-XXXX.sql | docker compose exec -T db psql -U umami umami`.

**Update:** backup dulu → ubah `image: ghcr.io/umami-software/umami:3.4.0` ke versi baru (lihat https://github.com/umami-software/umami/releases) → `docker compose pull && docker compose up -d` (tabel database diperbarui otomatis saat menyala). Skill diuji dengan 3.4.0; setelah update, cocokkan angka penting dengan layar Umami.

**Copot pasang:** `cd ~/umami && docker compose down -v` (**`-v` menghapus semua data** — backup dulu), hapus folder `~/umami` dan `~/.komunitech/umami-*.txt`. Hapus juga kode lacak dari website.

## 11. Masalah umum
| Gejala | Penyebab & solusi |
|---|---|
| http://localhost:3000 tidak terbuka | `docker compose ps` — ada yang tidak `running`? Lihat `docker compose logs umami`. Port 3000 dipakai program lain → ubah jadi `"127.0.0.1:3001:3000"` lalu `simpan-alamat http://localhost:3001` |
| Angka selalu 0 | Kode lacak belum terpasang / salah `data-website-id`; Umami di laptop (bagian 1); alamat Umami bukan HTTPS padahal website HTTPS (browser memblokir); `data-domains` tidak cocok dengan domain asli |
| Kunjungan sendiri ikut terhitung | Wajar. Tanpa cookie, Umami tidak bisa membedakan pemilik; kunjungan Anda kecil dibanding pengunjung asli |
| Skill: "Tidak bisa menghubungi Umami" | Umami mati, atau alamat beda → `simpan-alamat` / ENV `UMAMI_URL` |
| Skill: "kunci API salah" (401) | Kunci dihapus/salah, atau sandi akun AI diganti (bila memakai sandi) → buat kunci baru (bagian 7), `simpan-kunci --ya` |
| Skill: "TIDAK PUNYA AKSES" | Akun AI belum masuk tim website itu (bagian 7 langkah 2 & 4) |
| Skill: "cek" menampilkan 0 website | Website belum dipindah ke tim, atau akun AI belum anggota tim |
| Skill: "mengalihkan (HTTP 30x)" | Alamat yang disimpan diarahkan ke alamat lain (mis. `http://` → `https://`). Demi keamanan kunci, skill tidak mengikuti pengalihan → simpan alamat tujuan akhir (yang tampil di address bar browser) |
| Skill: "wajib HTTPS" | Alamat server internet memakai `http://` → pasang HTTPS (bagian 4) |
| Klik WA tidak tercatat | Atribut `data-umami-event` belum ada / salah ketik; kode lacak harus ada di halaman yang sama |
| Skill memakai proxy kantor? | Tidak untuk alamat komputer ini/jaringan kantor — setelan `HTTP_PROXY` sengaja diabaikan agar kunci tidak lewat proxy |

## 12. Lampiran: pasang tanpa Docker (Node.js + PostgreSQL, untuk teknisi)
Sumber resmi: README Umami ("Installing from source"). **Belum dijalankan Komunitech** (uji memakai Docker). Butuh **Node.js 22+** (sejak Umami 3.1), **pnpm**, dan **PostgreSQL 12.14+**.
```bash
git clone --depth 1 --branch v3.4.0 https://github.com/umami-software/umami.git
cd umami
pnpm install
# buat file .env berisi:
#   DATABASE_URL=postgresql://umami:SANDI@localhost:5432/umami
#   APP_SECRET=<openssl rand -hex 32>
#   DISABLE_TELEMETRY=1
pnpm run build      # membuat tabel + akun admin/umami (ganti sandi segera)
pnpm run start      # http://localhost:3000
```
Pastikan port 3000 tidak terbuka ke internet (firewall) dan pakai HTTPS lewat Caddy (bagian 4). Untuk pemakaian sehari-hari, Docker (bagian 2) lebih mudah dirawat.
