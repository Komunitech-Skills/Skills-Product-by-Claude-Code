---
name: agen-cs-toko
description: Menyiapkan agen CS toko/klinik berbasis basis pengetahuan lokal (produk, harga, stok, ongkir, retur, FAQ, nada brand) dengan draf balasan mode COPILOT (1-2 draf + keyakinan + hal yang dicek manusia, bukan kirim otomatis) untuk WhatsApp/Telegram lewat OpenClaw, plus aturan eskalasi, jam kerja, larangan mengarang harga/stok, rekap harian. ATURAN PERTAMA: SEMUA template balasan (stok/ongkir/retur + situasi umum, maks. ~8 pendek), aturan nada, dan alur admin WAJIB ditulis lengkap di balasan chat dengan [isian] bila data kosong; file cs/ hanya bila diminta, dibuat SETELAH isi tampil di chat. KERJAKAN DULU, TANYA DI AKHIR (maks. 1-3 pertanyaan). Pakai saat "bikin CS toko saya", "asisten/chatbot WhatsApp", "aktifin bot WA auto-balas semua chat" (ditolak: risiko blokir nomor, ditawarkan Copilot), knowledge base toko (AI CS assistant, customer support agent, WhatsApp auto-reply). BUKAN untuk satu balasan saja (balas-chat-cs), auto-trading, diagnosis medis, atau kirim otomatis ke pelanggan.
---

# Agen CS Toko

> **ATURAN PERTAMA (mengalahkan semua yang lain):** SEMUA template balasan dan aturan nada WAJIB ditulis lengkap di balasan chat ini juga (pengguna, mis. di Telegram, tidak bisa membuka file di server). Ringkas: maks. ±8 template pendek (stok, ongkir, retur + situasi umum, dengan `[isian]` bila data kosong), aturan nada 3-5 butir, alur admin 3-5 langkah. File (`cs/PENGETAHUAN.md`, `cs/ATURAN.md`) HANYA dibuat bila pengguna minta "simpan/pasang di OpenClaw", dan dibuat SETELAH isi tampil di chat. DILARANG menulis "sudah saya simpan di file X" sebagai pengganti isi. Balasan yang hanya berisi penolakan, ringkasan, atau "tersimpan di file" = GAGAL.

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

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
- Kirim promo massal / broadcast / blast → **tolak**, lewat alat apa pun (OpenClaw, WhatsApp Business, aplikasi blast). Promo hanya untuk pelanggan yang sudah setuju (opt-in), berupa draf yang dikirim pemilik **satu per satu** (`crm-wa` aturan 10; `broadcast-wa` bila terpasang hanya untuk menulis variasi teks). Pembeli marketplace default belum setuju.
- Permintaan diagnosis, skrining, atau kalkulator dosis medis → **tolak**, arahkan ke tenaga kesehatan (lihat `references/klinik-dan-data-kesehatan.md`).
- Permintaan agar bot **membalas/mengirim otomatis ke pelanggan lewat WA tanpa manusia** ("aktifin bot WA biar balas otomatis semua chat") → **skill ini yang dipakai, tapi bot auto-reply tidak dipasang**: jawab dengan "Jawaban baku: bot WA auto-reply" di bawah.

## Jawaban baku: bot WA auto-reply
Bila pengguna minta bot membalas otomatis semua chat WA pelanggan (pakai nomor toko), **selalu** jelaskan ketiga hal ini dengan bahasa sehari-hari (boleh diringkas, isi jangan dihilangkan), lalu langsung tawarkan Copilot:
1. **Kenapa tidak dipasang:** WhatsApp di OpenClaw tersambung lewat **WhatsApp Web (tidak resmi)**. Balasan otomatis/massal melanggar ketentuan WhatsApp dan bisa membuat **nomor toko diblokir** — termasuk riwayat chat & pelanggan yang menghubungi nomor itu. Bot juga bisa salah jawab ke pembeli yang sedang marah (komplain, refund).
2. **Yang dipakai: mode Copilot.** Pemilik/admin menempel atau meneruskan chat → agent menyiapkan 1–2 draf balasan + tingkat keyakinan dari basis pengetahuan toko → manusia memeriksa dan menekan Kirim. Tetap jauh lebih cepat daripada mengetik dari nol.
3. **Batas yang boleh:** notifikasi/rekap ke **pemilik sendiri** lewat Telegram (default). WhatsApp hanya dengan **nomor terpisah** milik pemilik + persetujuan risiko tertulis (lihat `references/eskalasi-dan-kanal.md` §1 & §5). Auto-reply resmi hanya lewat WhatsApp Business Platform (API resmi, vendor resmi) di luar skill ini — tetap tanpa broadcast/blast.
Bila di pesan yang sama ada chat pelanggan yang perlu dibalas, kerjakan langsung draf Copilot-nya (langkah 2).

## Aturan utama: kerjakan dulu, tanya di akhir
Untuk permintaan "bikinkan CS/asisten balas chat" (stok, ongkir, retur, dll.), **jangan membalas hanya dengan pertanyaan**. Balasan pertama selalu berisi hasil, dalam satu pesan, urutan tetap:
1. **Bila ada permintaan auto-reply WA:** penolakan singkat + alasan (lihat "Jawaban baku") + tawarkan Copilot — maks. 5 baris, lalu langsung lanjut ke paket.
2. **Paket siap pakai** dengan `[isian]` untuk data yang belum diberikan (jangan mengarang harga/ongkir/stok/syarat retur): template balasan **tanya stok, ongkir, retur** + 2-3 situasi umum lain sesuai usaha (mis. cara bayar/COD, status pesanan/resi, ukuran/bahan atau minta diskon), **aturan nada** (sapaan, emoji, panjang balasan, hal yang dilarang), dan **alur kerja admin** (mis. untuk admin 1 orang: tempel chat -> cek draf & `[isian]` -> kirim; antrean prioritas; eskalasi; rekap harian). Semua ini ditulis di chat; file `cs/PENGETAHUAN.md` & `cs/ATURAN.md` hanya bila pengguna memintanya, setelah isi tampil di chat.
3. **Di akhir: maks. 1-3 pertanyaan** paling penting (mis. daftar harga/ongkir/syarat retur — boleh kirim file/foto), plus asumsi yang dipakai (jam kerja, nada).
Pengecualian: bila permintaan sama sekali tanpa konteks usaha (tidak jelas toko apa), tanyakan jenis usaha di akhir tetap setelah memberi kerangka umum.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Nama toko/klinik & jenis usaha | Ya | Ambil dari pesan pengguna; nama toko `[nama toko]` bila belum disebut |
| Daftar produk/layanan & harga (atau file price list) | Ya | `[isi ...]` di paket; minta di akhir balasan (boleh sebagian) |
| Stok umum, jam buka, ongkir & cara bayar, kebijakan retur/garansi | Tidak* | `[isi ...]`; jangan mengarang |
| Nada brand & sapaan | Tidak | Ramah-sopan, sapaan "Kak" (ikut `balas-chat-cs`) |
| Kanal yang dipakai (Telegram/WA nomor sendiri/WA nomor terpisah) | Tidak | Tanyakan sekali; default disarankan **Telegram** |
| Jam kerja admin | Tidak | Senin–Sabtu 09.00–17.00 WIB; ubah sesuai jawaban |
| Chat pelanggan yang mau dibalas (untuk mode Copilot sehari-hari) | Ya (saat minta draf) | — (tanyakan) |

\*Wajib diisi sebelum basis pengetahuan dipakai untuk menjawab kategori itu. Jika kurang, **kerjakan dulu dengan `[isi ...]`**, lalu tanyakan **sekali di akhir** (maks. 3 pertanyaan bernomor) dan sebutkan bagian mana yang masih kosong.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.

### 1. Bangun basis pengetahuan (sekali di awal, atau saat diminta perbarui)
Default: tulis isinya di chat (template + aturan nada + alur admin). Langkah 2-4 di bawah (menulis file) hanya bila pengguna minta menyimpan/memasang di OpenClaw, dan setelah isi tampil di chat.
1. Impor dari price list/katalog yang dikirim pengguna; bila belum ada, buat kerangka dengan `[isi ...]` dan tanyakan di akhir balasan (bukan di awal).
2. (Bila diminta simpan) Tulis **`cs/PENGETAHUAN.md`** (pakai `templates/PENGETAHUAN.template.md`): produk & harga, stok/jam buka, ongkir & cara bayar, kebijakan retur, FAQ, nada brand. Tandai bagian kosong `[isi ...]`.
3. (Bila diminta simpan) Tulis **`cs/ATURAN.md`** (pakai `templates/ATURAN.template.md`): jam kerja, daftar pemicu eskalasi, pesan penahan, dan identitas bot.
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

Draf pesan penahan **dilarang menyatakan toko menyimpan data pembayaran/rekening/KTP pelanggan** (mis. "data rekening kami simpan"). Jika pelanggan mengirim data itu tanpa diminta: sarankan jangan mengirim foto/nomor KTP atau rekening di chat, dan rekening diminta lagi lewat kanal resmi saat klaim disetujui pemilik.

Saat eskalasi: kirim **ringkasan 3 baris** ke pemilik (siapa, inti masalah, yang diminta) + draf **pesan penahan** yang sopan untuk pelanggan (mis. "Terima kasih infonya, Kak, tim kami cek dulu ya, mohon tunggu sebentar").

### 4. Jam kerja
Jam kerja default (Senin–Sabtu 09.00–17.00 WIB) hanyalah **asumsi** bila pengguna belum menyebutnya: tulis di draf/ringkasan "jam kerja saya asumsikan 09.00–17.00, sesuaikan" agar pemilik mengoreksi sebelum janji waktu dikirim.

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
- [ ] Apakah semua template (stok, ongkir, retur, situasi umum), aturan nada, dan alur admin ada di balasan chat ini, bukan hanya di file?
- [ ] Setiap harga/stok/janji di draf ada persis di `PENGETAHUAN.md`, bukan dikira-kira.
- [ ] Pemicu eskalasi sudah dicek; jika kena, draf berupa pesan penahan + ringkasan ke pemilik, bukan janji penyelesaian.
- [ ] Tidak meminta/mengembalikan data sensitif (KTP/NIK, rekening, OTP, PIN, password) ke pelanggan.
- [ ] Jam kerja diperhitungkan untuk janji waktu; bila memakai jam default, disebut sebagai asumsi.
- [ ] Draf tidak mengklaim menyimpan data rekening/KTP/pembayaran pelanggan.
- [ ] Draf ditandai jelas ini adalah **draf**, manusia yang mengirim — bukan klaim "sudah terkirim".
- [ ] Untuk klinik: tidak ada diagnosis/saran dosis/triase; sudah diarahkan ke tenaga kesehatan bila relevan.

## Batasan & penanganan error
- **Kredensial & jadwal (wajib):** JANGAN pernah mencari, membaca, atau menampilkan token/API key/kredensial dari environment (`env`, `printenv`), file konfigurasi (mis. `openclaw.json`, `.env`), atau riwayat; kanal Telegram diatur lewat pairing/konfigurasi OpenClaw oleh pengguna sendiri. Buat jadwal hanya setelah pengguna membalas "ya" atas perintah + jam yang ditunjukkan; kanal belum siap atau perintah ditolak → berhenti dan beri langkah persiapannya, jangan menyelidiki sendiri.
- **Mode Copilot adalah satu-satunya mode untuk chat ke pelanggan lewat WA Web.** Skill ini **tidak akan** menyiapkan konfigurasi auto-reply otomatis ke nomor pelanggan tanpa manusia mengirim; jika pengguna memaksa, jelaskan risikonya (ToS WhatsApp melarang bulk/auto-messaging, nomor bisa diblokir, dan `dmPolicy: "pairing"` di WA membuat bot otomatis mengirim pesan ke pengirim baru) dan arahkan ke `references/eskalasi-dan-kanal.md` §1 & §5 (Level 2/3), yang mensyaratkan nomor terpisah + persetujuan risiko tertulis + jasa pendampingan, bukan swalayan.
- Basis pengetahuan kosong/belum dibuat → tawarkan bikin dulu dari `templates/PENGETAHUAN.template.md`, jangan menjawab pelanggan dari asumsi.
- Pertanyaan di luar cakupan toko (obrolan umum, topik sensitif tidak terkait) → balas singkat netral, tidak perlu eskalasi.
- Kesehatan/klinik: hanya edukasi umum & info operasional (jadwal, cara daftar), **tidak pernah** diagnosis/skrining/dosis; lihat `references/klinik-dan-data-kesehatan.md` untuk dasar UU PDP data kesehatan.
- Skill tidak terhubung ke sistem kasir/CRM; stok real-time tetap harus dicek admin sebelum janji ketersediaan mendesak.
- Jika `openclaw`/exec tidak tersedia untuk pengguna, berikan semua perintah di `references/eskalasi-dan-kanal.md` sebagai teks siap tempel untuk dijalankan sendiri atau lewat jasa setup.
