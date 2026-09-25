---
name: pesan-prospek-wa
description: Menyusun pesan PERTAMA (perkenalan/penawaran awal) via WhatsApp ke calon pelanggan B2B/B2C yang belum pernah dihubungi — dari referral, pameran, Google Maps, Instagram, atau grup komunitas — dalam 3 varian (singkat/sedang/dengan nilai), sopan, wajib menyebut asal kontak, patuh UU PDP, dan dicek otomatis lewat script (panjang, kata pemicu spam, jam kirim, opsi keluar) plus tautan wa.me siap pakai. Gunakan saat pengguna minta pesan perkenalan ke calon klien baru, cold outreach WhatsApp, pesan pembuka prospek, first contact message, atau chat pertama ke calon pelanggan. Bukan untuk menindaklanjuti prospek yang sudah dihubungi (pakai follow-up-prospek), promo massal ke banyak kontak (pakai broadcast-wa), atau mencari/menilai daftar calon pelanggan (pakai riset-calon-pelanggan).
---

# Pesan Prospek WA

## Tujuan
Membantu penjual/pemilik usaha menulis pesan **pertama** yang dikirim ke calon pelanggan yang **belum pernah dihubungi** — hasil dari referral, pameran, Google Maps, Instagram, atau grup komunitas — supaya terasa personal dan jelas alasannya, bukan seperti spam/penipuan, dan tetap patuh aturan data pribadi. Pesan dikirim **satu per satu oleh manusia** (mode copilot: AI menyiapkan draf, pengguna yang mengirim), bukan otomatis.

## Kapan digunakan
- "Saya dapat kontak toko bahan kue ini dari temen pas pameran UMKM, tolong bikinkan pesan perkenalan."
- "Lihat usaha katering ini di Google Maps, mau nawarin jasa desain kemasan, bikinin chat pembukanya."
- "Bikin pesan WA buat kenalan ke calon klien baru dari referral rekan bisnis."
- "Ada akun IG toko baju yang cocok jadi reseller produk saya, gimana cara chat pertamanya biar nggak keliatan spam?"

## Kapan TIDAK digunakan
- Prospek yang **sudah pernah dihubungi** (belum balas, minta waktu, "nanti dulu") → `follow-up-prospek`.
- Kirim promo ke **banyak kontak sekaligus** (blast/broadcast) → `broadcast-wa`. Skill ini tidak mendukung dan tidak akan membantu pengiriman massal — walau diminta "sekalian untuk 50 nomor", arahkan ke `broadcast-wa`.
- Belum punya daftar calon pelanggan / belum tahu siapa yang mau dihubungi → `riset-calon-pelanggan` dulu.
- Membalas chat yang **masuk dari pelanggan** → `balas-chat-cs`.
- Menyusun proposal/penawaran resmi setelah prospek tertarik → `proposal-kerjasama` / `surat-penawaran-harga`.
- Nomor didapat dari **database yang dibeli, bocoran data, atau scraping berlogin** → tolak dengan sopan, jelaskan risikonya (UU PDP, akun diblokir, kualitas data buruk), arahkan ke cara mendapat kontak yang sah (lihat `references/dasar-hukum-wa.md`).

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama & usaha calon pelanggan | Ya | — (tanyakan) |
| **Dari mana nomor/kontak didapat** (referral/pameran/Google Maps/IG/grup) | Ya | — (tanyakan; tanpa ini pesan tidak boleh dibuat, lihat Batasan) |
| Produk/jasa yang ditawarkan & manfaat singkatnya | Ya | — (tanyakan) |
| B2B atau B2C (menentukan sapaan & nada) | Tidak | Tebak dari konteks; B2B → Bapak/Ibu, B2C → Kak |
| Detail spesifik penerima (kebutuhan yang terlihat, konteks pertemuan) | Tidak | Pakai pola umum sumber kontak tsb tanpa detail personal tambahan |
| Bukti/nilai tambah nyata (hasil, jumlah pelanggan, keahlian) | Tidak | Tidak disebut sama sekali — jangan mengarang |
| Nomor WA calon pelanggan (untuk tautan wa.me) | Tidak | Lewati bagian tautan jika tidak ada |
| Nama & gaya pengirim | Tidak | Sopan semi-formal |
| Rencana jam kirim | Tidak | Sebutkan aturan jam wajar tanpa jam pasti |

Jika info wajib kurang, tanyakan **sekali** dalam satu pesan (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat, pakai default masuk akal dan tulis "Asumsi" di akhir — **kecuali asal kontak**, yang wajib ditanyakan karena tidak boleh dikarang.

## Langkah kerja
1. **Cek cakupan.** Pastikan ini pesan PERTAMA ke kontak yang belum pernah dihubungi. Jika sudah pernah dihubungi atau ini untuk banyak kontak sekaligus, arahkan ke skill yang tepat (lihat "Kapan TIDAK digunakan") dan jangan lanjutkan.
2. **Pastikan asal kontak sah.** Baca `references/dasar-hukum-wa.md`. Jika sumbernya database beli/bocoran/scraping berlogin, tolak dengan sopan dan jelaskan risikonya.
3. **Pilih pola pembuka** sesuai sumber kontak di `references/pola-pembuka.md` (referral, pameran, Google Maps, Instagram, grup komunitas, atau kontak lama yang dingin kembali).
4. **Tulis 3 varian** memakai `templates/template-pesan-pembuka.md`: **singkat** (1-2 kalimat), **sedang** (3-4 kalimat), **dengan nilai tambah** (4-6 kalimat, untuk B2B yang butuh penjelasan value lebih). Setiap varian wajib: sapaan sesuai konteks (Pak/Bu untuk B2B/formal, Kak untuk B2C/santai), identitas pengirim jelas, **sebutkan asal kontak**, satu ajakan ringan yang mudah dijawab ya/tidak, dan **opsi keluar yang sopan** ("boleh diabaikan bila belum relevan").
5. **Jangan mengarang bukti** (jumlah pelanggan, testimoni, hasil) — hanya tulis yang benar-benar diberikan pengguna.
6. **Periksa tiap varian dengan script** (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/cek_pesan.py cek --pesan "<isi pesan>" --jam-kirim "19:30"
   ```
   Tinjau setiap peringatan yang muncul (panjang, kalimat kepanjangan, huruf kapital berlebihan, kata pemicu spam, jumlah link, asal kontak tidak terdeteksi, opsi keluar tidak terdeteksi, jam kirim di luar 08.00–20.00). Perbaiki draf sebelum ditampilkan ke pengguna. Catatan: pengecekan "asal kontak"/"opsi keluar" bersifat heuristik kata kunci — kalau kamu (agent) sudah menuliskannya dengan kalimat lain yang jelas maksudnya, sebutkan itu ke pengguna sebagai penilaian manual, bukan cuma mengandalkan skrip.
   **Jika Python tidak bisa dijalankan:** hitung manual — jumlah karakter, tandai kalimat >25 kata, cek sendiri ada/tidaknya kata pemicu spam dari daftar di `scripts/cek_pesan.py`, dan pastikan asal kontak + opsi keluar tertulis jelas.
7. **Bangun tautan wa.me** jika ada nomor calon pelanggan:
   ```bash
   python3 <folder-skill-ini>/scripts/cek_pesan.py wa --nomor "<nomor>" --pesan "<salah satu varian>"
   ```
   Jika Python tidak tersedia, encode manual (spasi → `%20`, dst.) dan minta pengguna mengecek sekali sebelum dipakai.
8. **Sarankan jam kirim wajar** untuk lokasi penerima (WIB/WITA/WIT, 08.00–20.00) — lihat `references/checklist-anti-blokir.md`.
9. **Tutup dengan checklist anti-blokir** dan ringkasan asumsi (jika ada).

## Format Output
```
### Ringkasan konteks
Nama/usaha penerima, asal kontak, apa yang ditawarkan.

### Varian 1 — Singkat
<pesan>
[Hasil pemeriksaan script: OK / daftar peringatan]

### Varian 2 — Sedang
<pesan>
[Hasil pemeriksaan script]

### Varian 3 — Dengan nilai tambah
<pesan>
[Hasil pemeriksaan script]

### Tautan WhatsApp (jika ada nomor)
https://wa.me/62... (untuk varian yang dipilih)

### Saran jam kirim
08.00–20.00 waktu [WIB/WITA/WIT] setempat penerima; hindari [catatan spesifik jika relevan]

### Checklist anti-blokir
- [ ] ...

### Asumsi (jika ada)
```

## Contoh
Lihat [examples/uji-pembuat-01-jasa-desain-kemasan.md](examples/uji-pembuat-01-jasa-desain-kemasan.md) untuk contoh lengkap dari permintaan "lihat usaha katering di Google Maps, mau nawarin jasa desain kemasan" sampai 3 varian pesan siap kirim + tautan wa.me (dibuat oleh pembuat skill, bukan pengganti pengujian independen Tahap 6).

## Batasan & Penanganan Error
- **Wajib menyebut asal kontak** di setiap pesan. Jika pengguna tidak bisa/tidak mau menyebutkan dari mana kontak didapat, tanyakan sekali lagi secara spesifik; jika tetap tidak jelas atau ternyata dari sumber tidak sah, jangan buat pesannya — jelaskan alasannya.
- **Tidak untuk kirim massal.** Skill ini untuk satu prospek per permintaan, dikirim manusia satu per satu. Permintaan "kirim ke banyak nomor sekaligus/otomatis" diarahkan ke `broadcast-wa` (yang juga tidak mendukung blast tanpa persetujuan eksplisit tiap kontak).
- **Tidak pernah mengarang** bukti, testimoni, jumlah pelanggan, atau hasil. Kosongkan bagian itu daripada mengisi angka rekaan.
- **Nomor dari sumber tidak sah** (database beli, bocoran, scraping berlogin) → tolak, jelaskan risiko UU PDP & pemblokiran akun.
- **Tautan wa.me** memakai kode negara `62` menggantikan `0` di depan nomor Indonesia; nomor format lain dikonfirmasi dulu.
- **Skrining/diagnosis, klaim medis, atau kripto (rekomendasi beli/jual, auto-trading)** di luar cakupan — kalau prospek dari industri ini, pesan tetap murni perkenalan usaha, bukan konten yang melanggar batasan domain sensitif.
- **Bukan nasihat hukum** — ringkasan UU PDP/ITE/Perlindungan Konsumen di `references/dasar-hukum-wa.md` untuk bantu menulis lebih aman, bukan pengganti konsultasi hukum untuk kasus berisiko tinggi.
- **Jika prospek langsung menolak/minta tidak dihubungi** setelah pesan pertama terkirim (di luar cakupan skill ini yang berhenti setelah 1 pesan) → hormati, jangan kirim pesan susulan; kalau ingin tetap menindaklanjuti prospek yang belum jelas menolak, itu ranah `follow-up-prospek`.
