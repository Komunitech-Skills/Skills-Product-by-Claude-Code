---
name: agen-cs-toko
description: Menyiapkan agen CS toko/klinik berbasis "basis pengetahuan" lokal (produk & harga, stok, jam buka, ongkir & cara bayar, kebijakan retur, FAQ, nada brand) yang menghasilkan draf balasan mode COPILOT (1-2 draf + tingkat keyakinan + yang perlu dicek manusia — bukan kirim otomatis) untuk WhatsApp/Telegram lewat OpenClaw, lengkap aturan eskalasi (komplain berat, refund, ancaman, data sensitif, pertanyaan medis/hukum), jam kerja, larangan mengarang harga/stok, dan rekap harian pertanyaan. Gunakan saat pengguna minta "bikin CS otomatis toko saya", "asisten WhatsApp/chatbot CS", "agen CS klinik", knowledge base toko, auto-reply pelanggan (AI CS assistant, customer support agent, WhatsApp auto-reply). BUKAN untuk membalas satu chat / bank jawaban saja (pakai balas-chat-cs) dan BUKAN untuk auto-trading, diagnosis medis, atau kirim pesan otomatis ke pelanggan di WA Web.
---

# Agen CS Toko

## Tujuan
Membantu pemilik toko/klinik membangun "karyawan CS AI" yang **selalu tahu isi tokonya** (dari basis pengetahuan lokal, bukan karangan) dan **menyiapkan draf balasan** untuk chat pelanggan — pemilik/admin yang memutuskan dan mengirim. Skill ini merangkai basis pengetahuan + aturan eskalasi + jam kerja + rekap harian menjadi satu paket siap pakai, dan memakai `balas-chat-cs` untuk gaya bahasa draf.

## Kapan digunakan
- "Bikinkan asisten CS untuk toko saya, biar chat pelanggan gak numpuk."
- "Buatkan basis pengetahuan toko dari daftar harga ini."
- "Saya mau AI bantu siapin balasan chat WhatsApp, saya yang kirim."
- "Setup CS otomatis untuk klinik saya" (dengan batasan kesehatan, lihat di bawah).
- Membuat rekap harian pertanyaan pelanggan/pasien untuk perbaikan FAQ.

## Kapan TIDAK digunakan
- Hanya butuh **satu balasan cepat** atau bank jawaban tanpa basis pengetahuan terstruktur → `balas-chat-cs`.
- Membalas **ulasan/rating publik** → `balas-ulasan-pelanggan`.
- Menagih piutang / follow-up prospek → `tagih-piutang` / `follow-up-prospek`.
- Kirim promo massal / broadcast → **dilarang lewat WA Web** (pakai `broadcast-wa` untuk menyiapkan teks, kirim manual/WA Business resmi).
- Permintaan diagnosis, skrining, atau kalkulator dosis medis → **tolak**, arahkan ke tenaga kesehatan (lihat `references/klinik-dan-data-kesehatan.md`).
- Permintaan agar bot **mengirim otomatis ke pelanggan lewat WA Web tanpa manusia** → jelaskan risiko blokir nomor & arahkan ke mode Copilot atau WhatsApp resmi (WABA), bukan dijalankan begitu saja.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama toko/klinik & jenis usaha | Ya | — (tanyakan) |
| Daftar produk/layanan & harga (atau file price list) | Ya | — (tanyakan; boleh mulai dari sebagian, tandai sisanya `[isi ...]`) |
| Stok umum, jam buka, ongkir & cara bayar, kebijakan retur/garansi | Tidak* | `[isi ...]`; jangan mengarang |
| Nada brand & sapaan | Tidak | Ramah-sopan, sapaan "Kak" (ikut `balas-chat-cs`) |
| Kanal yang dipakai (Telegram/WA nomor sendiri/WA nomor terpisah) | Tidak | Tanyakan sekali; default disarankan **Telegram** |
| Jam kerja admin | Tidak | Senin–Sabtu 09.00–17.00 WIB; ubah sesuai jawaban |
| Chat pelanggan yang mau dibalas (untuk mode Copilot sehari-hari) | Ya (saat minta draf) | — (tanyakan) |

\*Wajib diisi sebelum basis pengetahuan dipakai untuk menjawab kategori itu. Jika kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor) atau tulis `[isi ...]` bila pengguna ingin cepat, dan sebutkan bagian mana yang masih kosong.

## Langkah kerja

### 1. Bangun basis pengetahuan (sekali di awal, atau saat diminta perbarui)
1. Wawancara singkat (satu pesan, bernomor) atau impor dari price list/katalog yang dikirim pengguna.
2. Tulis **`cs/PENGETAHUAN.md`** (pakai `templates/PENGETAHUAN.template.md`): produk & harga, stok/jam buka, ongkir & cara bayar, kebijakan retur, FAQ, nada brand. Tandai bagian kosong `[isi ...]`.
3. Tulis **`cs/ATURAN.md`** (pakai `templates/ATURAN.template.md`): jam kerja, daftar pemicu eskalasi, pesan penahan, dan identitas bot.
4. Tunjukkan ringkasan ke pengguna, minta konfirmasi sebelum dipakai untuk menjawab pelanggan sungguhan.

### 2. Siapkan draf balasan — mode COPILOT (satu-satunya mode untuk chat ke pelanggan)
Pemilik/admin **menempel atau meneruskan** chat pelanggan (atau membacanya sendiri di kanal pribadi pemiliknya). Agent **tidak pernah mengirim langsung ke pelanggan** lewat WA Web — lihat `references/eskalasi-dan-kanal.md` §1 untuk alasannya.
1. Cocokkan pertanyaan dengan `PENGETAHUAN.md`. Jika jawaban ada → siapkan **1–2 draf** (gaya `balas-chat-cs`: FAQ langsung jawab, komplain pakai alur empati→solusi→tindak lanjut).
2. Beri **tingkat keyakinan** per draf: **Tinggi** (semua fakta ada persis di basis pengetahuan), **Sedang** (sebagian perlu dicek/diasumsikan, ditandai jelas), **Rendah** (banyak yang tidak ada di basis pengetahuan — sarankan eskalasi, jangan asal jawab).
3. Cek daftar pemicu eskalasi (langkah 3). Jika kena, tandai `**Eskalasi: YA**` di bagian atas jawaban dan tetap beri draf pesan penahan, bukan draf jawaban penuh.
4. Cek jam kerja (langkah 4) untuk janji waktu tindak lanjut.
5. Bila ada script `scripts/periksa_draf.py` dan Python bisa dijalankan, jalankan untuk memeriksa draf sebelum ditampilkan (langkah "Periksa otomatis" di bawah). Jika tidak bisa dijalankan, periksa manual dengan checklist di bawah.

### 3. Aturan eskalasi ke manusia (WAJIB, tidak bisa dinonaktifkan agent)
Eskalasikan (jangan coba selesaikan sendiri) bila chat mengandung salah satu:
- Komplain berat / berulang, ancaman (lapor polisi, media sosial, BPSK), nada sangat marah.
- Permintaan refund, pembatalan pesanan besar, atau masalah pembayaran.
- Permintaan bicara langsung dengan manusia/pemilik.
- Data sensitif: KTP/NIK, nomor rekening/kartu, OTP, PIN, password — **jangan minta atau teruskan data ini**; arahkan ke kanal resmi.
- Pertanyaan medis (gejala, dosis, diagnosis) atau hukum di luar kebijakan toko → `references/klinik-dan-data-kesehatan.md`.
- Pertanyaan yang jawabannya **tidak ada** di `PENGETAHUAN.md` dan bukan sekadar salam/basa-basi.

Saat eskalasi: kirim **ringkasan 3 baris** ke pemilik (siapa, inti masalah, yang diminta) + draf **pesan penahan** yang sopan untuk pelanggan (mis. "Terima kasih infonya, Kak, tim kami cek dulu ya, mohon tunggu sebentar").

### 4. Jam kerja
Di luar jam kerja (dari `ATURAN.md`), FAQ tetap boleh dijawab (info tidak berubah di luar jam), tapi **janji tindak lanjut manusia** (retur, refund, jadwal) harus jatuh di jam kerja berikutnya, dan tambahkan kalimat "di luar jam operasional" bila relevan. Jangan menjanjikan respons cepat di luar jam kerja.

### 5. Identitas jujur
Draf pembuka pertama ke pelanggan baru menyebut "asisten virtual [nama toko]" saat relevan, dan pelanggan boleh minta bicara dengan manusia kapan saja.

### 6. Rekap harian (opsional, perlu OpenClaw automation)
Setiap kali membuat draf atau menandai eskalasi, tambahkan **satu baris log** ke `cs/log/<YYYY-MM-DD>.md` (kategori pertanyaan, eskalasi ya/tidak, ada-di-pengetahuan ya/tidak — **tanpa nama/nomor pelanggan/pasien**). Rekap harian otomatis membaca file log ini (bukan mengira-ngira), lalu mengirim ke Telegram pemilik: jumlah chat dibalas, 5 kategori pertanyaan terbanyak, daftar yang dieskalasi, dan **pertanyaan yang tidak ada jawabannya di `PENGETAHUAN.md`** (bahan perbaikan FAQ). Format log & perintah OpenClaw ada di `references/eskalasi-dan-kanal.md` §3. Tanyakan dulu jadwal & kanal tujuan, tunjukkan ringkasan, minta konfirmasi "Lanjut? (ya/tidak)" sebelum menjalankan perintah apa pun yang mengubah config.

### 7. Setup kanal
Jelaskan pilihan kanal memakai `references/eskalasi-dan-kanal.md` (Telegram default dengan `dmPolicy: "pairing"` + persetujuan manual; WA **hanya** nomor terpisah + persetujuan risiko tertulis dengan `dmPolicy: "allowlist"`, **tidak pernah** `"pairing"` di WA — lihat alasannya di referensi tsb). Jangan pernah menuliskan/menjalankan `allowFrom: ["*"]` untuk kanal yang menerima chat pelanggan baru. Level 2 (auto-reply nomor WA CS otomatis) hanya dijelaskan sebagai jasa setup berpendamping (`references/eskalasi-dan-kanal.md` §5), bukan langkah yang dijalankan sendiri oleh pengguna awam.

### 8. Nada bicara draf
Ikuti nada brand dari `PENGETAHUAN.md`. Bila belum diisi, tentukan dari **petunjuk pesan pengguna**: bahasa formal/istilah bisnis, chat B2B, atau produk profesional (mis. jasa cetak, kantor, korporat) → pakai nada **formal-ringkas** tanpa emoji; chat santai, produk konsumen sehari-hari (F&B, fashion, skincare) → pakai nada **ramah-sopan** default (sapaan "Kak", emoji secukupnya, mengikuti `balas-chat-cs`). Sebutkan nada yang dipakai di catatan bila diasumsikan, bukan ditanyakan.

## Periksa otomatis draf (opsional)
```
python3 <folder-skill-ini>/scripts/periksa_draf.py --pengetahuan cs/PENGETAHUAN.md --draf draf.txt
```
Script memeriksa (Python standar, tanpa dependensi): (a) apakah ada nominal **Rupiah** (dengan/tanpa "Rp", termasuk format "89rb"/"1,5 juta") di draf yang **tidak** ditemukan di `PENGETAHUAN.md` (potensi mengarang harga), (b) apakah draf memuat pola data sensitif (16 digit mirip NIK, nomor kartu, kode OTP/verifikasi, kata "PIN"/"password") yang seharusnya tidak dibocorkan balik ke pelanggan. **Script ini TIDAK memeriksa klaim stok** ("tinggal 2", "masih ada", dst.) — itu tetap wajib dicek manual oleh admin. Keluaran JSON + ringkasan teks, exit code 0 jika bersih, 1 jika ada temuan yang harus dicek. Jika Python tidak bisa dijalankan, periksa manual: cocokkan tiap angka Rupiah di draf ke `PENGETAHUAN.md` satu per satu, dan cek stok ke data toko sebenarnya.

## Format output

**Draf balasan (mode Copilot):**
```
**Keyakinan:** Tinggi / Sedang / Rendah
**Eskalasi:** Tidak / YA — [alasan singkat]

**Draf 1:**
[teks balasan siap tempel]

**Draf 2 (alternatif, opsional):**
[teks balasan]

**Perlu dicek admin sebelum kirim:**
- [fakta yang perlu dikonfirmasi / kosong di basis pengetahuan]

**Jika eskalasi — ringkasan untuk pemilik:**
[siapa – inti masalah – yang diminta, 3 baris]
```

## Contoh
**Input pengguna:** "Ini chat WA pelanggan toko kopi 'Kedai Pagi': 'Kak espresso 250ml sama americano beda harga gak? Bisa cash on delivery gak area Bintaro?' Basis pengetahuan sudah ada: espresso 250ml Rp 22.000, americano 250ml Rp 20.000, COD hanya area radius 5km termasuk Bintaro."

**Output:**
```
**Keyakinan:** Tinggi
**Eskalasi:** Tidak

**Draf 1:**
Halo Kak! Beda ya — espresso 250ml Rp 22.000, americano 250ml Rp 20.000 🙏
Untuk COD, area Bintaro termasuk yang kami layani (radius 5km). Mau pesan berapa cup, Kak?

**Perlu dicek admin sebelum kirim:**
- (tidak ada — semua fakta ada di basis pengetahuan)
```

## Checklist sebelum mengirim hasil
- [ ] Setiap harga/stok/janji di draf ada persis di `PENGETAHUAN.md`, bukan dikira-kira.
- [ ] Pemicu eskalasi sudah dicek; jika kena, draf berupa pesan penahan + ringkasan ke pemilik, bukan janji penyelesaian.
- [ ] Tidak meminta/mengembalikan data sensitif (KTP/NIK, rekening, OTP, PIN, password) ke pelanggan.
- [ ] Jam kerja diperhitungkan untuk janji waktu.
- [ ] Draf ditandai jelas ini adalah **draf**, manusia yang mengirim — bukan klaim "sudah terkirim".
- [ ] Untuk klinik: tidak ada diagnosis/saran dosis/triase; sudah diarahkan ke tenaga kesehatan bila relevan.

## Batasan & penanganan error
- **Mode Copilot adalah satu-satunya mode untuk chat ke pelanggan lewat WA Web.** Skill ini **tidak akan** menyiapkan konfigurasi auto-reply otomatis ke nomor pelanggan tanpa manusia mengirim; jika pengguna memaksa, jelaskan risikonya (ToS WhatsApp melarang bulk/auto-messaging, nomor bisa diblokir, dan `dmPolicy: "pairing"` di WA membuat bot otomatis mengirim pesan ke pengirim baru) dan arahkan ke `references/eskalasi-dan-kanal.md` §1 & §5 (Level 2/3), yang mensyaratkan nomor terpisah + persetujuan risiko tertulis + jasa pendampingan, bukan swalayan.
- Basis pengetahuan kosong/belum dibuat → tawarkan bikin dulu dari `templates/PENGETAHUAN.template.md`, jangan menjawab pelanggan dari asumsi.
- Pertanyaan di luar cakupan toko (obrolan umum, topik sensitif tidak terkait) → balas singkat netral, tidak perlu eskalasi.
- Kesehatan/klinik: hanya edukasi umum & info operasional (jadwal, cara daftar), **tidak pernah** diagnosis/skrining/dosis; lihat `references/klinik-dan-data-kesehatan.md` untuk dasar UU PDP data kesehatan.
- Skill tidak terhubung ke sistem kasir/CRM; stok real-time tetap harus dicek admin sebelum janji ketersediaan mendesak.
- Jika `openclaw`/exec tidak tersedia untuk pengguna, berikan semua perintah di `references/eskalasi-dan-kanal.md` sebagai teks siap tempel untuk dijalankan sendiri atau lewat jasa setup.
