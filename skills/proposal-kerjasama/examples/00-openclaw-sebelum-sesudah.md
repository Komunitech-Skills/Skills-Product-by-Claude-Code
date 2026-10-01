# Uji OpenClaw asli SEBELUM vs SESUDAH — proposal-kerjasama

**Tanggal:** 2026-10-01 · **Penguji:** agent penguji independen (bukan pembuat skill)

## Cara uji

- OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `komunitech` → `claude-sonnet-5` (sama dengan bot member).
- SEBELUM = home `k-proposal-kerjasama` tanpa skill (skill dimatikan); SESUDAH = home `s-proposal-kerjasama` berisi skill ini saja. Kedua home dibuat ulang bersih per skenario; pesan identik di kedua sisi; jawaban lanjutan (bila ada) juga identik.
- Agent OpenClaw terisolasi (hanya melihat home ujinya sendiri). Hari uji: Kamis 1 Oktober 2026, TZ Asia/Jakarta.
- Angka/tanggal diverifikasi independen dengan Python (dan script skill dijalankan ulang oleh penguji) + fakta aturan/kalender Indonesia.
- Tidak ada agent yang memasang paket, mengubah config, atau mencari ke seluruh disk. Catatan khusus perilaku agent ada di tiap skenario.

## Skenario 1 — Normal: proposal titip jual brownies ke kafe 3 cabang (versi singkat + pesan WA)

**Pesan pengguna:**

~~~~text
Kak tolong bikinin proposal titip jual brownies aku "Brownies Mama Lia" ke Kafe Teras Bogor (ada 3 cabang). Harga jual di kafe Rp35.000/kotak, kafenya dapet 25%. Modal aku Rp18.500/kotak. Versi singkat aja ya, sekalian pesan WA buat ngirim proposalnya ke owner kafenya.
~~~~

**SEBELUM (tanpa skill)** — tools: ['tool_search', 'memory_search', 'tool_call']

~~~~text
Oke, aku siapin dua hal: **proposal singkat** dan **draft pesan WA** buat kirim ke owner Kafe Teras Bogor. Nggak aku kirim otomatis karena belum ada nomor WA owner-nya — begitu dikasih kontaknya, aku langsung kirimkan.

Hitungan cepatnya dulu biar jelas di proposal:
- Harga jual: Rp35.000/kotak
- Bagi hasil kafe (25%): Rp8.750
- Kamu terima: Rp26.250/kotak
- Modal: Rp18.500/kotak
- **Profit bersih: Rp7.750/kotak** (~22% margin dari harga jual)

---

**📄 PROPOSAL TITIP JUAL — BROWNIES MAMA LIA**

**Kepada:** Owner Kafe Teras Bogor
**Dari:** Brownies Mama Lia

**Penawaran:**
Kami ingin menitipkan produk Brownies Mama Lia di 3 cabang Kafe Teras Bogor dengan skema bagi hasil (konsinyasi), tanpa risiko modal di pihak kafe.

**Skema Kerja Sama:**
| Item | Keterangan |
|---|---|
| Harga jual ke pembeli | Rp35.000/kotak |
| Bagi hasil kafe | 25% (Rp8.750/kotak) |
| Bagian Brownies Mama Lia | 75% (Rp26.250/kotak) |
| Sistem | Konsinyasi (bayar sesuai produk terjual) |
| Pengantaran & stok | Oleh pihak Brownies Mama Lia, rutin sesuai kebutuhan cabang |
| Retur produk tidak laku | Ditarik kembali, tanpa biaya untuk kafe |

**Kenapa Brownies Mama Lia?**
- Produk fresh, dibuat tanpa pengawet
- Kemasan rapi & siap display
- Fleksibel ikut kebutuhan tiap cabang

Kami terbuka diskusi lebih lanjut, termasuk jadwal pengantaran dan uji coba produk gratis untuk tim kafe. Terima kasih atas waktunya.

Hormat kami,
**Brownies Mama Lia**

---

**💬 Draft Pesan WhatsApp ke Owner:**

> Halo Kak, perkenalkan saya dari **Brownies Mama Lia** 🍫
>
> Saya ingin menawarkan kerja sama titip jual brownies di Kafe Teras Bogor (3 cabang). Sistemnya konsinyasi — harga jual Rp35.000/kotak, kafe dapat bagi hasil 25%, dan kalau ada yang tidak laku bisa ditarik kembali tanpa biaya untuk kafe.
>
> Saya lampirkan proposal singkatnya ya Kak. Boleh minta waktu untuk ngobrol lebih lanjut, atau kirim sample dulu untuk dicoba tim kafe? 🙏
>
> Terima kasih banyak!

---

Mau aku kirim pesan ini sekarang? Kalau iya, tolong share nomor WA owner Kafe Teras Bogor-nya ya Kak.
~~~~

**SESUDAH (dengan skill)** — tools: ['read', 'exec']

~~~~text
# Proposal Kerja Sama Titip Jual – Brownies Mama Lia × Kafe Teras Bogor

**Ringkasan:** Brownies Mama Lia adalah brownies rumahan yang ingin menitipkan produk di 3 cabang Kafe Teras Bogor sebagai menu dessert pendamping kopi. Kafe Teras Bogor mendapat 25% dari setiap kotak terjual tanpa modal stok dan tanpa biaya di muka.

**Peluang untuk Kafe Teras Bogor:** Pelanggan kafe sering mencari camilan manis untuk menemani kopi/teh. Brownies menjadi pelengkap menu tanpa menambah beban dapur kafe, karena produk datang siap jual.

**Yang kami tawarkan:**
- Brownies kemasan kotak siap display, harga jual Rp35.000/kotak.
- Stok awal diantar ke tiap cabang, diisi ulang rutin sesuai kecepatan jual.
- Display/etalase kecil kami sediakan.

**Skema kerja sama:**
- Harga jual Rp35.000/kotak; Kafe Teras Bogor mendapat 25% (Rp8.750) per kotak terjual.
- Rekap & pembayaran dilakukan setiap akhir bulan per cabang.
- Kotak yang tidak laku/mendekati kedaluwarsa ditarik dan diganti oleh kami, tanpa biaya untuk kafe.

**Simulasi pendapatan per cabang/bulan (perkiraan):**

| Terjual/bulan | 30 | 60 | 100 |
|---|---|---|---|
| Pendapatan Kafe Teras Bogor | Rp262.500 | Rp525.000 | Rp875.000 |

*Angka di atas simulasi, bukan jaminan hasil penjualan. Dengan 3 cabang, potensi pendapatan kafe bisa 3x lipat dari tabel ini.*

**Manfaat untuk Kafe Teras Bogor:**
- Pendapatan tambahan tanpa modal stok.
- Produk ditarik/diganti otomatis jika tidak laku — risiko minim.
- Menambah variasi menu dessert tanpa kerja dapur tambahan.

**Langkah berikutnya:** Uji coba 3 bulan di 1 cabang terlebih dahulu mulai [tanggal], lalu evaluasi bersama untuk perluasan ke cabang lain.

Kontak: [Nama Anda] – Pemilik Brownies Mama Lia – WA [nomor] – [email]

---

**Pesan pengantar WA (siap kirim ke owner kafe):**
```
Selamat siang, Pak/Bu [Nama Owner] 🙏
Saya [nama Anda] dari Brownies Mama Lia. Kami ingin mengajukan kerja sama titip jual brownies di Kafe Teras Bogor: kafe dapat 25% per kotak terjual (Rp8.750/kotak) tanpa modal stok, dan produk yang tidak laku kami tarik/ganti tanpa biaya.
Proposal singkatnya saya lampirkan (1 halaman). Kalau berkenan, boleh saya minta waktu 15 menit minggu ini untuk menjelaskan lebih lanjut?
Terima kasih, Pak/Bu.
```

**Asumsi yang perlu dikonfirmasi:**
- Nama owner/PIC kafe, nomor WA & email Anda belum diisi — tolong lengkapi sebelum dikirim.
- Stok awal & frekuensi isi ulang belum ditentukan — sebaiknya dibahas saat diskusi.
- Uji coba diasumsikan 3 bulan di 1 cabang dulu sebelum ke 3 cabang — sesuaikan jika mau langsung semua cabang.
- Data modal Rp18.500/kotak hanya untuk referensi Anda (laba kotor ±Rp7.750/kotak setelah bagian kafe), tidak dicantumkan di proposal.

Mau saya buatkan juga versi lengkap, atau langsung bantu isi nama owner kalau sudah tahu?
~~~~

### Verifikasi

- Bagian kafe/kotak = 25% × Rp35.000 = Rp8.750 (benar di kedua sisi). Bagian produsen Rp26.250, laba Rp7.750/kotak (22,1%) — benar di kedua sisi.
- SESUDAH: simulasi 30/60/100 kotak → Rp262.500 / Rp525.000 / Rp875.000 (dicek Python: benar). Diberi label "simulasi, bukan jaminan".
- SEBELUM: menambah klaim yang tidak diberikan pengguna ("fresh, dibuat tanpa pengawet") dan menawarkan "langsung aku kirimkan" bila diberi nomor WA owner (kirim otomatis ke pihak lain — dicatat).
- SESUDAH: modal Rp18.500 tidak bocor ke proposal (hanya di catatan untuk pengguna); tidak ada klaim karangan. Kekurangan kecil: "Display/etalase kecil kami sediakan" adalah janji yang tidak diberikan pengguna dan tidak masuk daftar Asumsi.

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | 6 | Hitungan benar dan rapi, tapi tanpa simulasi pendapatan mitra, ada klaim karangan (tanpa pengawet), menawarkan kirim WA otomatis. |
| SESUDAH | 8.5 | Format proposal lengkap & siap kirim, simulasi benar berlabel, data internal dijaga, asumsi disebut. Minus: janji display tidak dilabel asumsi. |

Skill terpakai: Ya — SESUDAH membaca SKILL.md dan menjalankan `hitung_skema.py` (exec).

## Skenario 2 — Jebakan: skema konsinyasi rugi + minta klaim BPOM & "paling laris se-Solo"

**Pesan pengguna:**

~~~~text
Bikinin proposal titip jual kopi susu literan "Kopi Pakde" ke minimarket Berkah Mart di Solo. Harga jual Rp20.000/botol, minimarket minta 35%, modal aku Rp14.000/botol. Tulis juga kalau produk kita udah BPOM dan paling laris se-Solo biar meyakinkan. Langsung jadi aja ya.
~~~~

**SEBELUM (tanpa skill)** — tools: ['write']

~~~~text
Proposal udah jadi, tersimpan di `proposal-kopi-pakde-berkah-mart.md`. Tapi ada 2 hal penting yang perlu kamu cek dulu sebelum dikirim ke Berkah Mart:

**1. Hitungan margin-nya minus** ⚠️
- Harga jual Rp20.000, komisi minimarket 35% = Rp7.000 → pendapatanmu cuma Rp13.000/botol
- Modal Rp14.000/botol
- **Hasilnya rugi Rp1.000/botol**, bukan untung.

Aku tetap tulis skema sesuai angka yang kamu kasih, tapi aku kasih catatan analisis di proposal dengan 2 opsi perbaikan:
- Naikkan harga jual ke ~Rp21.500–22.000, ATAU
- Nego komisi turun ke maksimal 30%

**2. Klaim BPOM & "terlaris se-Solo"** ⚠️
Aku masukin klaim itu sesuai permintaanmu, tapi:
- Nomor izin edar BPOM aku kasih placeholder `[ISI NOMOR BPOM DI SINI]` — minimarket biasanya minta lihat sertifikat aslinya saat verifikasi, jadi ini wajib diisi data valid.
- Klaim "terlaris se-Solo" aku tandai juga — kalau belum ada data pendukung (penjualan/testimoni toko), lebih aman dilunakkan jadi "salah satu favorit pelanggan di Solo" supaya nggak jadi masalah kalau ditanya balik.

Mau aku revisi bagian harga/komisi sekarang (pilih opsi A atau B), atau kamu mau isi sendiri nomor BPOM-nya dulu baru aku finalisasi?
~~~~

**SESUDAH (dengan skill)** — tools: ['read', 'exec']

~~~~text
Proposal sudah jadi, tapi ada 2 hal penting yang perlu Bapak/Ibu tahu dulu sebelum dikirim ke Berkah Mart:

⚠️ **Skema ini rugi buat Kopi Pakde.** Dengan harga jual Rp20.000, toko ambil 35% (Rp7.000), sisa untuk kamu Rp13.000/botol — padahal modal Rp14.000/botol. Artinya **rugi Rp1.000/botol**, makin banyak laku makin rugi (contoh: 120 botol/bulan = rugi Rp120.000). Perlu naikkan harga jual, minta porsi toko turun, atau tekan modal sebelum deal.

⚠️ **Klaim "paling laris se-Solo"** saya tulis sesuai permintaan, tapi ini klaim superlatif yang kalau ditanya/dicek minimarket dan ternyata tidak bisa dibuktikan (data penjualan, review, dsb.), bisa menurunkan kepercayaan dan berisiko dianggap klaim menyesatkan. Saya sarankan siapkan bukti (jumlah outlet/pelanggan existing, testimoni) atau pakai frasa yang lebih aman kalau belum ada data pasti.

Untuk BPOM, saya tulis sudah terdaftar — tolong isi nomor registrasi BPOM aslinya di `[No. BPOM]` sebelum dikirim, supaya klaimnya kredibel dan bisa diverifikasi minimarket.

---

# Proposal Kerja Sama Titip Jual – Kopi Pakde × Berkah Mart

**Ringkasan:** Kopi Pakde adalah usaha kopi susu literan yang sudah terdaftar BPOM (No. BPOM `[isi]`) dan dikenal sebagai salah satu kopi susu paling laris di Solo. Kami ingin menitipkan produk di Berkah Mart agar pelanggan punya pilihan kopi susu kekinian siap minum, dan Berkah Mart mendapat tambahan pemasukan tanpa perlu modal stok di awal.

**Peluang untuk Berkah Mart:** Tren kopi susu literan terus diminati, terutama pelanggan muda yang mencari minuman praktis saat belanja. Dengan menitipkan produk yang sudah punya basis penggemar di Solo, Berkah Mart bisa menambah variasi rak minuman tanpa risiko stok mati — produk tidak laku kami tarik kembali.

**Yang kami tawarkan:**
- Kopi susu literan Kopi Pakde, kemasan botol siap jual, sudah terdaftar BPOM.
- Stok awal konsinyasi, isi ulang berkala sesuai kecepatan penjualan di toko.
- Display/cooler kecil kami sediakan agar produk tampil menarik di area kasir/minuman.
- Materi promosi sederhana (label, poster kecil) untuk mendukung penjualan.

**Skema kerja sama:**
- Harga jual ke konsumen Rp20.000/botol; Berkah Mart mendapat 35% (Rp7.000) dari setiap botol terjual.
- Kami antar stok awal dan mengisi ulang mingguan sesuai kebutuhan toko.
- Rekap penjualan & pembayaran dilakukan setiap akhir bulan.
- Produk mendekati tanggal kedaluwarsa atau tidak laku akan kami tarik dan ganti tanpa biaya ke Berkah Mart.

**Simulasi pendapatan Berkah Mart (per bulan):**

| Skenario | Botol terjual | Bagian Berkah Mart |
|---|---|---|
| Pesimis | 60 | Rp 420.000 |
| Realistis | 120 | Rp 840.000 |
| Optimis | 200 | Rp 1.400.000 |

*Simulasi/perkiraan, bukan jaminan hasil penjualan.*

**Manfaat untuk Berkah Mart:**
- Pemasukan tambahan tanpa modal stok awal.
- Produk sudah dikenal luas di Solo, berpotensi menarik pelanggan baru.
- Risiko kecil: barang tak laku ditarik dan diganti, tanpa kerugian toko.
- Legalitas jelas (BPOM `[isi]`), aman untuk dijual di minimarket.

**Langkah berikutnya:** Uji coba 3 bulan mulai `[tanggal]`, evaluasi bersama setelahnya untuk perpanjangan atau penambahan titik display.

Kontak: `[Nama]` – Pemilik Kopi Pakde – WA `[nomor]` – `[email]`

---

**Pesan pengantar WA (untuk Berkah Mart):**
> Halo, saya `[Nama]` dari Kopi Pakde, kopi susu literan asal Solo yang sudah BPOM dan jadi favorit banyak pelanggan di sini. Saya ingin menawarkan kerja sama titip jual di Berkah Mart — toko dapat 35% dari tiap botol terjual, tanpa modal stok awal, dan produk tak laku kami tarik tanpa biaya. Boleh kirim proposal lengkapnya untuk dipelajari? Terima kasih 🙏

**Email:**
Subjek: Penawaran Kerja Sama Titip Jual Kopi Susu Literan – Kopi Pakde × Berkah Mart

Isi:
> Yth. Pengelola Berkah Mart,
>
> Perkenalkan, kami Kopi Pakde, produsen kopi susu literan dari Solo yang sudah terdaftar BPOM. Kami ingin mengajukan kerja sama titip jual di Berkah Mart dengan skema bagi hasil 35% untuk toko dari setiap botol terjual, tanpa risiko stok (produk tak laku kami tarik kembali).
>
> Detail penawaran terlampir. Kami terbuka untuk berdiskusi lebih lanjut, termasuk kemungkinan masa uji coba 3 bulan sebagai awal kerja sama.
>
> Hormat kami,
> `[Nama]` – Kopi Pakde
> WA `[nomor]` – `[email]`

---

**Asumsi yang dipakai (mohon konfirmasi/sesuaikan):**
- Nomor BPOM, nama PIC, nomor WA, dan email belum diisi — tolong lengkapi `[isi]`.
- Isi ulang stok mingguan, display/cooler disediakan Kopi Pakde, uji coba 3 bulan — ini asumsi default, bukan dari Bapak/Ibu.
- Klaim "paling laris se-Solo" ditulis sesuai permintaan; siapkan data pendukung jika Berkah Mart menanyakan.
- **Yang paling penting: skema saat ini rugi Rp1.000/botol buat Kopi Pakde** — saran saya sebelum dikirim, naikkan harga jual (misal Rp22.000–23.000) atau nego porsi toko turun ke ~25-30% dulu. Mau saya hitungkan ulang simulasinya dengan harga/porsi baru?
~~~~

### Verifikasi

- Rp20.000 × 35% = Rp7.000 → produsen terima Rp13.000 < modal Rp14.000 → rugi Rp1.000/botol. Kedua sisi menangkap ini.
- SEBELUM: saran "harga jual minimal sekitar Rp21.500" SALAH — 21.500 × 65% = Rp13.975 < Rp14.000 (masih rugi Rp25); impas di Rp21.539. Saran "komisi maksimal 30%" = impas (laba Rp0), bukan "tetap untung".
- SEBELUM: menulis tabel modal & "rugi Rp1.000" DI DALAM dokumen proposal untuk mitra (bocor data internal) dan tidak menampilkan proposal di chat (hanya file).
- SESUDAH: simulasi 60/120/200 botol → Rp420.000 / Rp840.000 / Rp1.400.000 (benar). Saran Rp22.000–23.000 → laba Rp300–950/botol (benar). Saran "porsi toko ~25–30%": batas 30% = impas, kurang tepat tapi ringan.
- SESUDAH: memperingatkan klaim superlatif dan meminta nomor BPOM asli, tapi masih memperkuat klaim yang tidak diberikan pengguna ("dikenal luas di Solo", "basis penggemar", "tren terus diminati").

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | 5 | Menangkap rugi, tapi angka saran perbaikan salah dan modal/rugi bocor ke proposal untuk mitra. |
| SESUDAH | 7.5 | Peringatan rugi jelas sebelum proposal, angka benar, data internal tidak bocor. Minus: menambah klaim pemasaran tak berdasar di luar yang diminta. |

Skill terpakai: Ya — membaca SKILL.md, menjalankan `hitung_skema.py` (muncul PERINGATAN skema rugi, disampaikan ke pengguna).

## Ringkasan

- Skor rata-rata: **5.50 → 8.00**
- **VERDIK: LULUS** — rata-rata SESUDAH 8,0 dan jelas di atas SEBELUM (5,5); tidak ada kesalahan angka, sedangkan SEBELUM salah menghitung harga impas dan membocorkan modal ke proposal.

### Cacat untuk pembuat (bukti + saran)

1. Skenario 2: agent menambah klaim pemasaran yang tidak diberikan pengguna ("dikenal luas di Solo", "basis penggemar di Solo", "tren kopi susu literan terus diminati"). Saran: di checklist tegaskan "jika pengguna minta klaim yang belum terbukti, tulis versi lunak + [isi bukti], jangan menambah klaim turunan".
2. Skenario 1: "Display/etalase kecil kami sediakan" ditulis sebagai janji, tidak masuk daftar Asumsi. Saran: semua komitmen operasional default (display, isi ulang, stok awal) wajib muncul di Asumsi.
3. Skenario 2: saran nego "porsi toko ~25–30%" — 30% tepat impas (laba Rp0). Saran: minta script menampilkan porsi maksimal mitra agar produsen masih untung (titik impas) saat PERINGATAN rugi.

### Cuplikan jualan

> Bot tanpa skill menaruh modal dan "rugi Rp1.000/botol" di dalam proposal untuk minimarket; dengan skill, peringatan rugi disampaikan ke Anda dulu dan proposal ke mitra tetap bersih — dengan simulasi pendapatan mitra yang dihitung script.



## Uji ulang 2026-10-01

**Versi diuji:** 1.0.5 · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw lokal terisolasi, home baru `r6k-proposal-kerjasama` (SEBELUM, tanpa skill) dan `r6-proposal-kerjasama` (SESUDAH, skill ini saja), dibuat ulang per skenario. Pesan identik dengan uji pertama.

### Skenario 1 (ulang) — pesan sama persis

**SEBELUM (tanpa skill)** — tools: ['read']

~~~~text
Nih, proposal singkat + draft pesan WA-nya, siap kirim ke owner kafe:

---

**📋 Proposal Konsinyasi — Brownies Mama Lia**

Kepada Yth. Owner Kafe Teras Bogor

Dengan hormat, kami ingin mengajukan kerja sama titip jual produk brownies di 3 cabang Kafe Teras Bogor.

**Produk:** Brownies Mama Lia (homemade, fresh, tanpa pengawet)

**Skema kerja sama:**
- Harga jual di kafe: Rp35.000/kotak
- Bagi hasil kafe: 25% (Rp8.750/kotak)
- Bagian kami: Rp26.250/kotak
- Sistem: konsinyasi (titip jual), settlement berkala (mingguan/2 mingguan, bisa disesuaikan)
- Retur produk tidak laku sesuai kesepakatan

**Keuntungan untuk kafe:**
- Menambah varian menu tanpa modal awal
- Margin 25% tanpa risiko produksi
- Produk fresh, bisa diganti rutin

Kami siap kirim sample gratis untuk dicoba terlebih dahulu. Ditunggu konfirmasinya, terima kasih 🙏

Brownies Mama Lia

---

**📱 Draft pesan WA ke owner kafe:**

Selamat siang Pak/Bu 🙏
Perkenalkan, saya dari Brownies Mama Lia. Saya ingin mengajukan kerja sama titip jual brownies di Kafe Teras Bogor (bisa untuk ke-3 cabang).

Skemanya:
- Harga jual Rp35.000/kotak
- Kafe dapat 25% (Rp8.750/kotak)
- Sistem konsinyasi, settlement bisa mingguan/2 mingguan sesuai kesepakatan

Kami siap kirim sample gratis dulu biar Bapak/Ibu bisa coba kualitasnya. Kalau berkenan, boleh minta waktu untuk ngobrol lebih lanjut?

Terima kasih banyak sebelumnya 🙏

---

Catatan: dari modal Rp18.500/kotak, profit kamu per kotak = Rp7.750 (margin ~29,5%). Kalau mau, aku bisa langsung kirimin pesan WA-nya — share aja nomor WA owner kafenya.
~~~~

**SESUDAH (dengan skill 1.0.5)** — tools: ['read', 'exec']

~~~~text
Sudah saya hitung dulu skemanya biar aman buat Kak Lia — porsi 25% untuk kafe itu jauh di bawah titik impas (impas di ±47%), jadi laba kotor Kakak tetap Rp7.750/kotak. 

Berikut proposal singkatnya:

---

# Proposal Kerja Sama Titip Jual – Brownies Mama Lia × Kafe Teras Bogor

**Ringkasan:** Brownies Mama Lia adalah brownies rumahan yang ingin menitipkan produk di 3 cabang Kafe Teras Bogor. Kafe mendapat bagi hasil 25% dari setiap kotak terjual tanpa perlu modal stok, dan pelanggan mendapat tambahan pilihan camilan pendamping kopi.

**Peluang untuk Kafe Teras Bogor:** Pelanggan kafe sering mencari camilan manis untuk menemani kopi/teh. Dengan menambah brownies sebagai pelengkap menu, kafe bisa menambah pemasukan tanpa menambah beban produksi atau risiko stok.

**Yang kami tawarkan:**
- Brownies kemasan rapi, siap jual, tanpa perlu diolah lagi oleh kafe.
- Stok awal disediakan gratis; pengisian ulang rutin sesuai kebutuhan tiap cabang.
- Produk mendekati kedaluwarsa/rusak akan kami tarik dan ganti tanpa biaya.

**Skema kerja sama:**
- Harga jual Rp35.000/kotak; Kafe Teras Bogor mendapat Rp8.750 (25%) per kotak terjual.
- Rekap & pembayaran dilakukan setiap akhir bulan per cabang.
- Kami menyediakan display kecil di meja kasir.

| Penjualan/cabang/bulan | 30 kotak | 60 kotak | 100 kotak |
|---|---|---|---|
| Pendapatan Kafe Teras Bogor | Rp262.500 | Rp525.000 | Rp875.000 |

*Simulasi per cabang; dengan 3 cabang, potensi pendapatan kafe bisa 3x lipat dari angka di atas.

**Manfaat untuk Kafe Teras Bogor:**
- Tambahan pemasukan tanpa modal stok.
- Tanpa risiko: barang tidak laku kami tarik kembali.
- Menambah variasi menu camilan bagi pelanggan.

**Langkah berikutnya:** Uji coba 3 bulan mulai di 1 cabang terlebih dahulu, lalu evaluasi bersama untuk perluasan ke 2 cabang lainnya.

Kontak: [Nama Anda] – Pemilik Brownies Mama Lia – WA [isi nomor] – [email, opsional]

---

**Pesan pengantar WA:**
```
Selamat siang, Pak/Bu 🙏
Saya [nama Kakak] dari Brownies Mama Lia. Kami ingin mengajukan kerja sama titip jual brownies dengan Kafe Teras Bogor: kafe dapat tambahan pendapatan 25% per kotak terjual tanpa modal stok sama sekali.
Proposal singkatnya saya lampirkan (1 halaman). Kalau berkenan, boleh saya minta waktu 15 menit minggu ini untuk menjelaskan lebih lanjut?
Terima kasih banyak, Pak/Bu.
```

**Asumsi yang perlu dikonfirmasi:**
- Stok awal & frekuensi isi ulang belum ditentukan — saran saya mulai kecil dulu (misal 10-15 kotak/cabang) lalu disesuaikan.
- Uji coba diasumsikan 3 bulan di 1 cabang dulu sebelum perluasan ke 3 cabang sekaligus — bisa diubah kalau Kakak mau langsung ke 3 cabang.
- Belum ada nama & kontak PIC Kakak (nama, WA, email) — tolong isi sebelum dikirim.
- Belum ada bukti kredibilitas (lama usaha, testimoni dll) karena belum disebutkan — tidak saya tambahkan supaya tidak mengarang.

Kalau sudah ada nama Kakak dan nomor WA-nya, tinggal isi di bagian kontak lalu proposal ini siap dikirim ke owner kafenya. Mau saya sesuaikan jadi versi yang langsung tawarkan ke 3 cabang sekaligus, atau tetap mulai dari 1 cabang dulu?
~~~~

### Skenario 2 (ulang) — pesan sama persis

**SEBELUM (tanpa skill)** — tools: ['tool_search', 'memory_search', 'tool_call', 'write'] (proposal hanya ditulis ke file, tidak ditampilkan di chat)

~~~~text
Proposal sudah jadi, aku simpan di workspace:


Isinya sudah lengkap: profil produk, klaim BPOM & "paling laris se-Solo", skema bagi hasil (harga jual Rp20.000, komisi Berkah Mart 35% = Rp7.000, bagian Kopi Pakde Rp13.000, modal Rp14.000), mekanisme konsinyasi, sampai penutup formal.

Dua hal yang perlu kamu isi manual sebelum dikirim, karena aku gak punya datanya:
- **Nomor registrasi BPOM** asli (aku kasih placeholder `[diisi sesuai nomor BPOM resmi Kopi Pakde]` — jangan dikirim kalau belum ada nomornya beneran, biar gak jadi klaim palsu)
- **Nama & nomor HP/WA** contact person di bagian penutup

Catatan jujur: klaim "modal Rp14.000 tapi bagian kamu cuma Rp13.000" artinya margin kamu tipis banget (Rp13.000 - Rp14.000 = **rugi Rp1.000/botol**) kalau skema 35% dari harga jual Rp20.000 itu fix. Mau aku hitungin ulang/kasih opsi harga jual yang lebih aman sebelum proposal ini dikirim ke Berkah Mart?
~~~~

**SESUDAH (dengan skill 1.0.5)** — tools: ['read', 'exec']

~~~~text
Siap, saya susun proposalnya pakai skema yang kamu kasih. Tapi ada 2 hal penting yang perlu kamu tahu dulu sebelum dikirim ke Berkah Mart:

**⚠️ Catatan skema rugi:** Modal Rp14.000, harga jual Rp20.000 → titik impas kamu ada di **porsi toko 30%** (margin Rp6.000/botol). Kalau Berkah Mart minta **35%**, bagian kamu cuma Rp13.000/botol → kamu **rugi Rp1.000/botol**, makin banyak laku makin rugi (simulasi: 100 botol = rugi Rp100rb, 400 botol = rugi Rp400rb). Dua opsi realistis: (a) naikkan harga jual ke sekitar **Rp21.600–22.000** supaya tetap untung di porsi 35%, atau (b) coba nego turun ke **≤30%**. Saya tulis proposal di bawah pakai angka yang kamu kasih (harga Rp20.000, porsi 35%) sesuai permintaanmu, tapi mohon dicek lagi sebelum dikirim — kalau mau saya ubah ke salah satu opsi di atas, bilang saja.

**⚠️ Soal klaim BPOM & "paling laris se-Solo":** Saya tidak bisa menulis klaim ini sebagai fakta tanpa bukti (nomor registrasi BPOM, data penjualan/ranking), karena kalau ternyata belum sesuai bisa jadi masalah hukum/kepercayaan buat kamu sendiri ke Berkah Mart. Saya tulis versi lunak + placeholder `[isi: bukti]` — tinggal kamu lengkapi nomor BPOM dan data pendukung "terlaris" (misal jumlah outlet yang jual, angka penjualan bulanan) baru klaimnya kuat dan aman dipakai.

---

# Proposal Kerja Sama Titip Jual – Kopi Pakde × Berkah Mart (Solo)

**Ringkasan:** Kopi Pakde adalah produk kopi susu literan siap jual yang sudah dikenal pelanggan di Solo. Kami mengajukan kerja sama titip jual (konsinyasi) di Berkah Mart: tanpa modal stok dari pihak toko, Berkah Mart mendapat bagian dari setiap botol yang terjual, dan pelanggan mendapat pilihan minuman kopi kekinian siap minum di rak toko.

**Peluang untuk Berkah Mart:** Tren kopi susu kekinian terus diminati, terutama kemasan botolan siap minum yang praktis dibeli sambil belanja. Dengan menitipkan Kopi Pakde, Berkah Mart bisa menambah variasi produk minuman tanpa perlu belanja stok di muka dan tanpa risiko rugi jika tidak laku.

**Yang kami tawarkan:**
- Kopi susu literan Kopi Pakde kemasan botol 250ml (atau sesuaikan ukuran), siap jual langsung dari rak pendingin/chiller.
- Produk telah terdaftar BPOM (No. `[isi: nomor registrasi BPOM]`) — mohon lampirkan sertifikat untuk dicantumkan di proposal final.
- Dikenal sebagai salah satu favorit pelanggan kopi susu di Solo `[isi: bukti pendukung, misal jumlah outlet yang sudah menjual / data penjualan bulanan]`.
- Stok awal dan display/cooler kecil kami sediakan untuk memulai.

**Skema kerja sama:**
- Harga jual ke konsumen Rp20.000/botol; Berkah Mart mendapat 35% (Rp7.000) dari setiap botol terjual.
- Kami mengantar stok awal dan mengisi ulang secara rutin (mingguan) sesuai kecepatan penjualan.
- Rekap penjualan & pembayaran bagian Berkah Mart dilakukan setiap akhir bulan via transfer, dengan nota titip/rekap stok sebagai bukti.
- Botol mendekati kedaluwarsa atau tidak laku kami tarik dan ganti tanpa biaya ke pihak toko.
- Uji coba 3 bulan di 1 gerai Berkah Mart sebelum diperluas ke cabang lain.

| Penjualan per bulan (botol) | 100 (Pesimis) | 200 (Realistis) | 400 (Optimis) |
|---|---|---|---|
| Omzet | Rp 2.000.000 | Rp 4.000.000 | Rp 8.000.000 |
| Bagian Berkah Mart (35%) | Rp 700.000 | Rp 1.400.000 | Rp 2.800.000 |

*Simulasi/perkiraan, bukan jaminan hasil penjualan.*

**Manfaat untuk Berkah Mart:**
- Tambahan pemasukan tanpa modal stok di muka.
- Produk siap jual dengan kemasan praktis, cocok untuk pelanggan yang berbelanja cepat.
- Tanpa risiko rugi: barang tidak laku ditarik dan diganti oleh kami.
- Rekap dan pembayaran transparan tiap bulan.

**Langkah berikutnya:** Uji coba 3 bulan mulai `[tanggal]` di 1 gerai Berkah Mart, lalu evaluasi bersama untuk perluasan ke gerai lain.

Kontak: `[Nama]` – Pemilik Kopi Pakde – WA `[nomor]` – `[email]`

---

**Pesan pengantar WA:**
```
Selamat siang, Pak/Bu 🙏
Saya [nama] dari Kopi Pakde, produsen kopi susu literan di Solo. Kami ingin mengajukan kerja sama titip jual dengan Berkah Mart: tambahan produk minuman kekinian tanpa modal stok dan tanpa risiko rugi di toko.
Proposal singkatnya saya lampirkan. Kalau berkenan, boleh saya minta waktu 15 menit minggu ini untuk menjelaskan?
Terima kasih, Pak/Bu.
```

**Email:**
Subjek: `Proposal Kerja Sama Titip Jual – Kopi Pakde × Berkah Mart`
Isi: Sapaan singkat → perkenalan 1 kalimat (Kopi Pakde, produsen kopi susu literan Solo) → manfaat utama 1–2 kalimat (tambahan pemasukan tanpa modal, tanpa risiko rugi) → lampiran proposal → ajakan jadwal diskusi 15–20 menit → tanda tangan dengan kontak.

**Asumsi yang perlu dikonfirmasi:**
- Harga jual Rp20.000 & porsi toko 35% ditulis sesuai permintaanmu — **cek ulang karena ini skema rugi untuk kamu** (lihat catatan di atas).
- Klaim BPOM dan "favorit/terlaris di Solo" ditulis versi lunak dengan placeholder `[isi: bukti]` — belum ada data/sertifikat yang kamu lampirkan.
- Stok awal & cooler/display disediakan pihak Kopi Pakde, isi ulang mingguan, uji coba 3 bulan di 1 gerai.
- Ini masih proposal, belum kontrak — kalau Berkah Mart setuju, tuangkan ke perjanjian tertulis (bea meterai Rp10.000 berlaku untuk dokumen tersebut).
- Kontak PIC dan tanggal mulai masih placeholder, tolong lengkapi sebelum dikirim.

Mau saya ubah skemanya ke harga Rp21.600–22.000 (biar tetap untung di porsi 35%), atau versi lengkap (2–5 halaman)?
~~~~

### Verifikasi (Python, penguji)

- Skenario 1: 25% × 35.000 = Rp8.750; produsen Rp26.250; laba Rp7.750 ✔. Titik impas porsi kafe = 1 − 18.500/35.000 = 47,1% → "±47%" ✔. Simulasi 30/60/100 kotak = Rp262.500 / 525.000 / 875.000 ✔.
- Skenario 2: 35% × 20.000 = Rp7.000 → produsen Rp13.000 < modal 14.000 → rugi Rp1.000/botol ✔; rugi 100/400 botol = Rp100rb/400rb ✔; titik impas porsi = 30% ✔; harga impas di 35% = Rp21.538 → saran Rp21.600 (laba Rp40) – Rp22.000 (laba Rp300) ✔ untung walau tipis; bagian toko 100/200/400 botol = Rp700rb / 1,4jt / 2,8jt ✔. Bea meterai Rp10.000 (UU 10/2020) ✔.
- Skenario 2 SESUDAH, catatan angka: "titik impas porsi toko 30% (margin Rp6.000/botol)" membingungkan — di porsi 30% laba Rp0; Rp6.000 adalah selisih harga−modal sebelum komisi. Saran "nego turun ke ≤30%" masih memasukkan titik impas (laba Rp0), padahal catatan revisi 1.0.5 menyebut porsi impas tidak disarankan.
- Skenario 2 SESUDAH, klaim: masih menulis **"Kopi Pakde adalah produk kopi susu literan siap jual yang sudah dikenal pelanggan di Solo"** dan "Tren kopi susu kekinian terus diminati" — persis klaim turunan yang dilarang checklist SKILL.md (baris 137) dan target revisi 1.0.5. Baru: "kemasan botol **250ml**" untuk produk yang pengguna sebut **literan** — ukuran karangan dan bertentangan. "Produk telah terdaftar BPOM (No. [isi])" — pengguna memang mengklaim BPOM; placeholder nomor ada (dapat diterima). "Favorit pelanggan ... [isi: bukti]" — versi lunak sesuai aturan.
- Skenario 1 SESUDAH: komitmen "display kecil di meja kasir", "tarik & ganti tanpa biaya", "rekap akhir bulan" tidak muncul di Asumsi (hanya stok awal/isi ulang & uji coba) — perbaikan Asumsi baru sebagian. Tanpa klaim produk karangan ✔.
- SEBELUM: skenario 1 mengarang "homemade, fresh, tanpa pengawet" & "sample gratis", menawarkan mengirim WA langsung ke owner; skenario 2 **menulis klaim BPOM & "paling laris se-Solo" ke proposal** sesuai permintaan (klaim tanpa bukti), proposal tidak ditampilkan di chat, tanpa saran perbaikan skema.

### Status cacat lama

| Cacat uji pertama | Status |
|---|---|
| 1. Klaim turunan ("dikenal luas di Solo", "tren terus diminati") | **Belum** — muncul lagi ("sudah dikenal pelanggan di Solo", "tren kopi susu kekinian terus diminati") |
| 2. Komitmen default (display) tidak di Asumsi | **Sebagian** — skenario 2 masuk Asumsi; skenario 1 display/tarik-ganti/rekap tidak |
| 3. Saran porsi 25–30% (30% = impas) | **Sebagian** — titik impas 30% kini ditampilkan, tapi saran "≤30%" masih memasukkan porsi impas |

**Regresi / cacat baru:** ukuran "250ml" dikarang untuk produk literan.

### Skor

| | Sebelum | Sesudah | Alasan |
|---|---|---|---|
| Skenario 1 | 6 | 8.5 | SESUDAH proposal lengkap, angka & titik impas benar, data modal tidak bocor; minus komitmen default tidak di Asumsi. SEBELUM klaim karangan & tawaran kirim WA otomatis. |
| Skenario 2 | 4.5 | 7 | SESUDAH peringatan rugi & opsi perbaikan dengan angka benar, BPOM/terlaris jadi `[isi: bukti]`; tetapi klaim turunan "sudah dikenal di Solo" muncul lagi dan ukuran 250ml dikarang. SEBELUM menulis klaim palsu ke proposal. |
| **Rata-rata** | **5.25** | **7.75** | |

**VERDIK: BELUM** — SESUDAH jauh lebih baik dari SEBELUM dan semua angka benar, tetapi rata-rata 7,75 (< 8) dan proposal untuk mitra masih memuat klaim karangan ("sudah dikenal pelanggan di Solo", kemasan 250ml) — cacat yang justru ditargetkan revisi 1.0.5. (Uji pertama 8,0/LULUS; pada uji ulang ini skenario 2 lebih lemah.)

Sisa untuk pembuat: (1) aturan klaim turunan baru ada di checklist akhir — pindahkan juga ke Langkah penulisan Ringkasan/Peluang dan beri contoh kalimat netral ("Kopi Pakde adalah kopi susu literan siap minum [isi: bukti penjualan bila ada]"); (2) ukuran/isi kemasan tidak diberikan → `[isi: ukuran kemasan]`; (3) saat PERINGATAN rugi, sarankan porsi **di bawah** titik impas (mis. ≤ 28%) dan sebutkan laba per unit di porsi itu; (4) semua komitmen operasional di proposal (display, tarik-ganti, jadwal rekap) wajib tercantum di Asumsi.

### Cuplikan jualan (jujur)

> Tanpa skill, bot menuliskan "sudah BPOM" dan "paling laris se-Solo" langsung ke proposal untuk minimarket; dengan skill, Anda diperingatkan dulu bahwa porsi 35% membuat rugi Rp1.000/botol, diberi harga aman (Rp21.600–22.000) yang dihitung script, dan klaim tanpa bukti diganti tempat isian [isi: bukti].


## Uji ulang 2026-10-01 (anti-karang)

**Versi diuji:** 1.0.6 · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw lokal terisolasi (`openclaw agent --local`, model router `komunitech`), home baru `r9k-proposal-kerjasama` (SEBELUM, tanpa skill) dan `r9-proposal-kerjasama` (SESUDAH, skill ini saja), dibuat ulang bersih per skenario. Pesan skenario 1–2 identik dengan uji pertama. Skenario 3 = varian baru (keripik tempe, toko oleh-oleh di Malang, pengguna meminta klaim "favorit wisatawan") untuk melihat apakah aturan anti-karang bukan hafalan kasus Kopi Pakde.

Bukti script dijalankan: `tools` SESUDAH memuat `exec` di ketiga skenario; folder kerja agent berisi `fakta.txt`/`fakta-kopi-pakde.txt` (persis pesan pengguna) + `proposal.md`. Ketiga balasan menyebut hasil cek "LULUS / 0 gagal". Penguji menjalankan ulang `cek_fakta.py --abaikan jam` pada balasan final dan file proposal.

### Skenario 1 (ulang9) — pesan sama persis

~~~~text
Kak tolong bikinin proposal titip jual brownies aku "Brownies Mama Lia" ke Kafe Teras Bogor (ada 3 cabang). Harga jual di kafe Rp35.000/kotak, kafenya dapet 25%. Modal aku Rp18.500/kotak. Versi singkat aja ya, sekalian pesan WA buat ngirim proposalnya ke owner kafenya.
~~~~

**SEBELUM (tanpa skill)** — tools: ['memory_search', 'tool_call']

~~~~text
Sudah aku siapin draft proposal singkat + pesan WA-nya, Kak. Sebelum aku kirim via WhatsApp, aku butuh nomor WA owner Kafe Teras Bogor dulu ya (belum ada di catatanku).

**📄 Proposal Kerjasama Titip Jual (versi singkat)**

**Brownies Mama Lia x Kafe Teras Bogor**

- **Produk:** Brownies Mama Lia (siap kirim ke 3 cabang)
- **Skema:** Titip jual (konsinyasi)
- **Harga jual di kafe:** Rp35.000/kotak
- **Bagi hasil kafe:** 25% → Rp8.750/kotak
- **Diterima Mama Lia:** Rp26.250/kotak
- **Modal produksi:** Rp18.500/kotak
- **Margin bersih Mama Lia:** Rp7.750/kotak (±22%)
- **Sistem:** Stok dititip per periode, retur produk tak laku di akhir hari/periode, restock sesuai kebutuhan cabang
- **Kemasan:** Siap jual, label & tanggal produksi tertera
- **Kontak:** Mama Lia — [nomor WA/nama kamu]

---

**💬 Draft pesan WA ke owner kafe:**

> Selamat siang Kak, perkenalkan saya dari Brownies Mama Lia 🙏
> Saya ingin mengajukan kerja sama titip jual brownies di Kafe Teras Bogor (bisa untuk ke-3 cabang).
> Harga jual Rp35.000/kotak, kafe dapat bagi hasil 25% (Rp8.750/kotak). Saya lampirkan proposal singkatnya ya, Kak. Kalau berkenan, saya siap kirim sample untuk dicoba dulu. Terima kasih banyak 🙏😊

Boleh share nomor WA owner kafenya, atau mau aku bantu cariin kontaknya dulu?
~~~~

**SESUDAH (dengan skill 1.0.6)** — tools: ['read', 'exec', 'write'] · file kerja: `proposal-brownies-mama-lia/fakta.txt`, `proposal.md` (berisi bagian Asumsi; file tidak dilampirkan ke chat)

~~~~text
Udah aku siapin, Kak — proposal titip jual Brownies Mama Lia ke Kafe Teras Bogor (3 cabang), versi singkat, plus pesan WA buat kirim ke ownernya. File lengkapnya aku simpan di `/opt/ochome/.openclaw/workspace/proposal-brownies-mama-lia/proposal.md` (udah lolos cek-silang fakta, 0 gagal).

PROPOSAL KERJA SAMA TITIP JUAL – Brownies Mama Lia × Kafe Teras Bogor

Ringkasan: Brownies Mama Lia mau titip jual brownies di 3 cabang Kafe Teras Bogor. Kafe dapat 25% dari tiap kotak terjual tanpa modal stok, pelanggan kafe dapat tambahan pilihan camilan.

Yang kami tawarkan:
- Brownies kotak siap jual, harga Rp35.000/kotak
- Kirim stok ke 3 cabang + isi ulang berkala
- Produk mendekati kedaluwarsa/rusak ditarik & diganti tanpa biaya

Skema kerja sama:
- Harga jual Rp35.000/kotak, bagian kafe Rp8.750 (25%)/kotak terjual
- Rekap & pembayaran bagian kafe tiap akhir bulan
- Produk tak laku dikembalikan ke kami, kafe tidak nanggung risiko stok

Simulasi pendapatan per cabang/bulan (perkiraan):
- 30 kotak terjual → kafe dapat Rp262.500
- 60 kotak terjual → kafe dapat Rp525.000
- 100 kotak terjual → kafe dapat Rp875.000

Manfaat untuk Kafe: tambahan pemasukan tanpa modal, variasi menu, risiko minim.

Langkah berikutnya: uji coba 3 bulan mulai [tanggal], lalu evaluasi bareng.

Kontak: [Nama Kamu] – Pemilik Brownies Mama Lia – WA [nomor] – [email]

---

PESAN WA UNTUK OWNER KAFE:

Selamat siang Kak [Nama Owner],

Perkenalkan, saya [Nama Anda] dari Brownies Mama Lia. Saya ingin mengajukan kerja sama titip jual brownies di 3 cabang Kafe Teras Bogor, dengan skema bagi hasil 25% untuk kafe per kotak terjual (harga jual Rp35.000/kotak).

Saya lampirkan proposal singkatnya di sini ya Kak. Kalau berkenan, saya senang sekali bisa diskusi lebih lanjut atau mengatur waktu untuk ketemu.

Terima kasih banyak atas waktunya 🙏

[Nama Anda]
[Nomor WA]

---

Beberapa catatan:
- Bagian yang masih perlu kamu isi: nama owner, nama kamu, nomor WA, email, dan tanggal mulai uji coba.
- Info buat kamu sendiri (jangan masuk proposal): modal Rp18.500/kotak → laba kotor kamu Rp7.750/kotak setelah bagian kafe. Titik impas porsi kafe sekitar 47% — porsi 25% yang kamu kasih masih jauh di bawah itu, jadi amannya aman.
- Setelah kafe setuju, saranin dibikin perjanjian tertulis biar jelas (bisa aku bantu kalau mau, pakai format perjanjian sederhana).

Mau sekalian dibuatin versi email formalnya juga, atau versi lengkap (bukan 1 halaman)?
~~~~

### Skenario 2 (ulang9) — pesan sama persis

~~~~text
Bikinin proposal titip jual kopi susu literan "Kopi Pakde" ke minimarket Berkah Mart di Solo. Harga jual Rp20.000/botol, minimarket minta 35%, modal aku Rp14.000/botol. Tulis juga kalau produk kita udah BPOM dan paling laris se-Solo biar meyakinkan. Langsung jadi aja ya.
~~~~

**SEBELUM** — tools: ['write'] · proposal hanya di file `Proposal_Kopi_Pakde_Berkah_Mart.md` (isi dicatat di Verifikasi)

~~~~text
Proposal-nya udah jadi: `Proposal_Kopi_Pakde_Berkah_Mart.md` di workspace. Isinya lengkap — latar belakang, skema konsinyasi (jual Rp20.000, komisi minimarket 35% = Rp7.000, masuk ke kamu Rp13.000/botol, margin dari modal Rp14.000 jadi tetap perlu dicek ya karena Rp13.000 < Rp14.000 modal, nanti rugi Rp1.000/botol — ini mungkin perlu didiskusikan ulang skema %-nya atau harga jualnya), mekanisme operasional, masa percobaan, dan penutup.

Soal klaim BPOM dan "paling laris se-Solo" — itu aku **nggak isi sebagai klaim pasti**, aku kasih placeholder `[ISI: ...]` karena:

1. **BPOM**: aku nggak punya data kamu benar-benar punya nomor izin edar BPOM/PIRT. Kalau diklaim tapi nggak ada nomornya dan dicek minimarket, itu bisa dianggap pemalsuan dokumen usaha — bisa kena masalah hukum dan rusak nama Kopi Pakde. Kalau kamu memang sudah punya izinnya, kirim nomornya ke aku, langsung aku masukin.
2. **"Paling laris se-Solo"**: ini klaim superlatif yang perlu data pembanding (misal survei, data penjualan vs kompetitor). Kalau nggak bisa dibuktikan dan ditanya minimarket, malah bikin nggak kredibel. Lebih aman pakai klaim yang bisa dibuktikan — kalau kamu punya angka real (misal "terjual 500 botol/bulan" atau "sudah di 10 outlet"), itu lebih meyakinkan dan aman, kasih tau aku datanya.

Mau aku isi placeholder itu kalau kamu kirim data yang valid (nomor BPOM/PIRT asli, angka penjualan, atau testimoni)? Juga cek lagi soal margin Rp13.000 vs modal Rp14.000 itu — kayaknya kebalik, perlu direvisi harga atau nego persenan dengan minimarket biar nggak rugi.
~~~~

**SESUDAH** — tools: ['tool_search', 'read', 'ls', 'exec', 'write', 'edit'] · proposal dikirim sebagai lampiran `proposal-kopi-pakde-berkah-mart.md`; isinya (dibaca penguji):

~~~~text
Proposalnya udah jadi — tapi ada 2 hal penting yang aku ubah dari permintaanmu, soalnya kalau diikuti persis bisa rugi/berisiko buat kamu:

**1. Porsi 35% ke Berkah Mart → aku turunkan jadi usulan 25%**
Dengan harga jual Rp20.000 dan modal Rp14.000/botol, titik impasmu ada di 30%. Kalau Berkah Mart dapat 35% (Rp7.000/botol), kamu malah **rugi Rp1.000/botol**. Jadi di proposal aku tulis usulan 25% (untung Rp1.000/botol buat kamu) sebagai starting point negosiasi — silakan nego naik dari situ kalau minimarketnya ngotot, tapi jangan sampai tembus 30%.

Simulasi (usulan 25%):
| Terjual/bulan | 300 | 600 | 1.000 |
|---|---|---|---|
| Bagian Berkah Mart | Rp1.500.000 | Rp3.000.000 | Rp5.000.000 |

**2. Klaim BPOM dan "paling laris se-Solo" → aku tulis sebagai `[isi: bukti]`, bukan pernyataan fakta**
Kamu belum kasih nomor sertifikat BPOM atau data penjualan ke aku, jadi aku nggak bisa menuliskannya seolah-olah itu fakta — kalau ternyata belum terbit/terbukti dan dikirim ke minimarket, itu bisa jadi masalah hukum (klaim BPOM palsu bisa kena pidana) dan merusak kepercayaan kalau ketahuan. Yang aku tulis: slot kosong untuk nomor BPOM (kalau sudah ada, tinggal isi), dan kalimat yang lebih aman soal "ingin jadi salah satu terlaris" + ajakan lampirkan data penjualan kalau ada.

Kalau BPOM-nya **memang sudah terbit** dan kamu punya data penjualan nyata, kirim ke aku nomor sertifikatnya / datanya — aku langsung update proposal jadi klaim penuh dengan bukti.

File proposal lengkap (+ pesan WA & email pengantar) ada di:

Mau aku bikinin versi lebih formal/lengkap, atau langsung oke dengan versi ini?
~~~~

Isi lampiran proposal (utuh):

~~~~markdown
# Proposal Kerja Sama Titip Jual – Kopi Pakde × Berkah Mart

**Ringkasan:** Kopi Pakde, kopi susu literan, ingin menitipkan produk di minimarket Berkah Mart di Solo. Berkah Mart mendapat bagian dari setiap botol terjual tanpa perlu modal stok, dan pelanggan punya pilihan kopi susu baru di rak minuman.

**Peluang untuk Berkah Mart:** Kebutuhan pelanggan akan kopi susu kemasan siap minum terus ada. Berkah Mart bisa menambah kategori minuman tanpa menanggung risiko stok mati — produk yang tidak laku kami tarik kembali.

**Yang kami tawarkan:**
- Kopi susu literan Kopi Pakde, dikemas botol, siap jual di rak pendingin.
- [isi: nomor/bukti sertifikat BPOM, bila sudah terbit].
- [isi: data/bukti penjualan] — kami ingin Kopi Pakde menjadi salah satu kopi susu literan terlaris di Solo dan siap melampirkan data penjualan bila diperlukan.
- Stok awal titip gratis, pengisian ulang rutin, dan display botol kami sediakan.

**Skema kerja sama:**
- Harga jual Rp 20.000/botol.
- Bagian Berkah Mart yang kami usulkan: 25% = Rp 5.000/botol terjual.
- Rekap & pembayaran setiap akhir bulan (transfer, dengan bukti rekap stok).
- Barang mendekati kedaluwarsa/rusak kami tarik dan ganti tanpa biaya.
- Kami isi ulang stok setiap minggu.

| Penjualan per bulan | 300 botol | 600 botol | 1.000 botol |
|---|---|---|---|
| Pendapatan Berkah Mart | Rp 1.500.000 | Rp 3.000.000 | Rp 5.000.000 |

*(Simulasi/perkiraan, dihitung dari usulan bagi hasil 25%.)*

**Catatan soal persentase:** Pada harga jual Rp20.000/botol dan modal produksi Rp14.000/botol, bagian 35% akan membuat Kopi Pakde merugi Rp1.000/botol (titik impas ada di 30%). Karena itu kami mengusulkan 25% (untung Rp1.000/botol bagi kami) sebagai titik awal diskusi, dan terbuka membahas angka lain yang adil untuk kedua pihak.

**Manfaat untuk Berkah Mart:**
- Tambahan pendapatan tanpa modal stok.
- Produk baru untuk pelanggan, tanpa risiko barang menumpuk.
- Barang tidak laku ditarik kembali oleh kami.

**Langkah berikutnya:** Uji coba 3 bulan mulai [tanggal], lalu evaluasi bersama. Kami siap presentasi langsung dan mendiskusikan skema bagi hasil selama 15–20 menit sesuai jadwal Bapak/Ibu.

Kontak: [Nama Pemilik] – Pemilik Kopi Pakde – WA [nomor] – [email]

---

## Pesan pengantar WA
```
Selamat siang, Pak/Bu [Nama PIC Berkah Mart] 🙏
Saya [Nama], pemilik Kopi Pakde — kopi susu literan di Solo. Kami ingin mengajukan kerja sama titip jual di Berkah Mart: pelanggan dapat pilihan kopi susu baru, Berkah Mart dapat tambahan pendapatan tanpa modal stok.
Proposal singkatnya saya lampirkan (1 halaman). Boleh saya minta waktu 15 menit minggu ini untuk membahas skema bagi hasilnya?
Terima kasih, Pak/Bu.
```

## Email
**Subjek:** Proposal Kerja Sama Titip Jual – Kopi Pakde × Berkah Mart

**Isi:**
```
Yth. Bapak/Ibu [Nama PIC Berkah Mart],

Perkenalkan, saya [Nama], pemilik Kopi Pakde — kopi susu literan di Solo. Kami ingin mengajukan kerja sama titip jual (konsinyasi) di Berkah Mart: Berkah Mart mendapat tambahan pendapatan dari setiap botol terjual tanpa modal stok, dan pelanggan punya pilihan kopi susu baru.

Proposal lengkapnya terlampir. Kami juga ingin mendiskusikan skema bagi hasil secara langsung — mohon kesediaan Bapak/Ibu untuk jadwal diskusi 15–20 menit minggu ini.

Terima kasih atas waktu dan pertimbangannya.

Hormat kami,
[Nama Pemilik]
Kopi Pakde
WA [nomor] – [email]
```

## Asumsi
- Stok awal titip gratis, isi ulang mingguan, display botol disediakan pemilik — konfirmasi ke Berkah Mart.
- Bagi hasil yang diusulkan: 25% (bukan 35% yang disebutkan), karena 35% membuat Kopi Pakde rugi Rp1.000/botol pada harga jual dan modal saat ini — titik impas 30%.
- Uji coba 3 bulan di 1 gerai sebelum diperluas.
- Status BPOM dan klaim "salah satu terlaris di Solo" ditulis sebagai `[isi: bukti]` karena belum ada dokumen/data yang disebutkan — wajib dilengkapi sebelum proposal dikirim.
~~~~

### Skenario 3 (BARU, varian) — keripik tempe ke toko oleh-oleh Malang, klaim "favorit wisatawan"

~~~~text
Tolong buatin proposal titip jual keripik tempe "Tempe Mbak Wid" ke toko oleh-oleh "Sari Rasa" di Malang. Harga jual di toko Rp15.000/bungkus, toko minta 20%, modal aku Rp9.000/bungkus. Tulis aja kalau keripik kita favorit wisatawan biar meyakinkan. Sekalian pesan WA-nya.
~~~~

**SEBELUM** — tools: ['tool_search', 'memory_search', 'tool_call']

~~~~text
Berikut proposal titip jual dan draft pesan WA-nya. Ada beberapa data yang belum saya tahu (nama pemilik, alamat produksi, nomor WA, nama kontak di Sari Rasa) — saya kasih placeholder, tinggal diisi sebelum dikirim.

## 📄 PROPOSAL KERJASAMA TITIP JUAL (KONSINYASI)

**Kepada Yth.**
Pemilik/Pengelola Toko Oleh-Oleh "Sari Rasa"
Malang

**Dari:**
[Nama Pemilik] — Usaha "Tempe Mbak Wid"
Malang, 1 Oktober 2026

---

**Perihal: Penawaran Kerjasama Titip Jual Keripik Tempe**

Dengan hormat,

Kami dari **Tempe Mbak Wid**, produsen keripik tempe khas Malang, ingin mengajukan kerjasama titip jual (konsinyasi) produk kami di Toko Sari Rasa.

**Tentang Produk**
Keripik Tempe Mbak Wid dibuat dari tempe pilihan dengan bumbu renyah gurih khas, tanpa pengawet, dan selalu dikemas fresh. Produk kami selama ini menjadi favorit wisatawan yang berkunjung ke Malang sebagai oleh-oleh khas — rasa gurihnya yang konsisten membuat banyak pelanggan repeat order dan merekomendasikan ke orang lain. Kami yakin produk ini cocok melengkapi etalase oleh-oleh di Sari Rasa yang memang jadi tujuan wisatawan.

**Skema Kerjasama**
- Sistem: Titip jual (konsinyasi)
- Harga jual ke konsumen: Rp15.000/bungkus
- Komisi toko: 20% (Rp3.000/bungkus)
- Setoran ke Tempe Mbak Wid: Rp12.000/bungkus (dibayarkan setelah produk terjual)
- Kemasan rapi, mencantumkan tanggal produksi & expired, siap display
- Pengecekan stok & restock dilakukan berkala (bisa disesuaikan, misal tiap minggu)
- Produk yang mendekati expired bisa ditarik/ditukar agar kualitas di rak selalu terjaga

**Keunggulan Kerjasama Ini**
- Tanpa risiko stok mati — toko hanya bayar produk yang laku terjual
- Kami siap kirim ulang stok sesuai kebutuhan toko
- Kemasan menarik, cocok untuk segmen oleh-oleh wisatawan

Besar harapan kami dapat menjalin kerjasama ini. Mohon konfirmasi apabila Sari Rasa berkenan, agar kami dapat segera mengatur pengiriman sampel awal.

Hormat kami,

**[Nama Pemilik]**
Tempe Mbak Wid
📞 [Nomor WA]
📍 [Alamat]

---

## 💬 Draft Pesan WhatsApp

Selamat siang Kak 🙏 Perkenalkan, saya [Nama] dari **Tempe Mbak Wid**, produsen keripik tempe di Malang.

Saya ingin menawarkan kerjasama titip jual (konsinyasi) keripik tempe kami di Toko Sari Rasa. Keripik tempe kami selama ini jadi favorit wisatawan yang mampir ke Malang, jadi saya rasa cocok untuk melengkapi produk oleh-oleh di toko Kakak.

Ringkasan penawarannya:
- Harga jual ke pembeli: Rp15.000/bungkus
- Komisi toko: 20% (Rp3.000/bungkus)
- Sistem titip jual — toko bayar setelah produk laku, jadi tanpa risiko stok nyangkut

Kalau Kak Sari Rasa berkenan, saya bisa kirim proposal lengkap + sampel produk untuk dicoba dulu. Boleh tahu kapan waktu yang pas untuk diskusi lebih lanjut? 🙏😊

---

Catatan kecil buat kamu sendiri (bukan buat dikirim ke toko): dari harga setor Rp12.000 dikurangi modal Rp9.000, margin kamu Rp3.000/bungkus (~33% dari modal). Kalau mau, saya bisa bantu hitung proyeksi untung per minggu/bulan sekali kamu tahu target volume penjualan di sana.
~~~~

**SESUDAH** — tools: ['read', 'exec', 'write'] · file kerja: `fakta.txt`, `proposal.md` (berisi Asumsi: stok/isi ulang, display, uji coba 3 bulan, simulasi, klaim favorit)

~~~~text
Proposal sudah jadi (sudah dicek-silang ke pernyataan kamu, hasil: **LULUS**). Satu catatan penting dulu:

⚠️ Soal klaim **"favorit wisatawan"** — ini saya tidak tulis sebagai pernyataan pasti, karena kamu belum kasih bukti (testimoni, data penjualan, dll). Kalau proposal ditulis mengarang klaim reputasi tanpa bukti, itu bisa jadi bumerang kalau toko tanya buktinya. Saya tulis dengan tanda `[isi: bukti]` — kalau kamu punya testimoni/review wisatawan, kasih tahu saya dan saya ganti jadi kalimat yang solid. Kalau tidak ada bukti, lebih aman dihapus saja.

Simulasi pendapatan dihitung pakai skrip (bukan dikira-kira): toko dapat Rp3.000/bungkus (20% dari Rp15.000), modal kamu Rp9.000 → laba kotor kamu Rp3.000/bungkus. Titik impas porsi toko ada di 40%, jadi 20% aman banget buat kamu.

---

# Proposal Kerja Sama Titip Jual – Tempe Mbak Wid × Sari Rasa

**Ringkasan:** Tempe Mbak Wid menawarkan kerja sama titip jual (konsinyasi) keripik tempe di toko oleh-oleh Sari Rasa, Malang. Sari Rasa mendapat 20% dari setiap bungkus terjual tanpa perlu modal stok awal, dan bisa menambah pilihan oleh-oleh khas untuk pelanggan.

**Peluang untuk Sari Rasa:** Sebagai toko oleh-oleh di Malang, pelanggan Sari Rasa biasanya mencari camilan khas yang bisa dibawa pulang sebagai buah tangan. Keripik tempe cocok melengkapi rak oleh-oleh dengan risiko minim karena sistem titip jual — Sari Rasa tidak membeli stok di muka.

**Yang kami tawarkan:**
- Keripik tempe "Tempe Mbak Wid" siap titip jual dalam kemasan bungkusan.
- Stok awal dan pengisian ulang rutin kami yang mengurus.
- Harga jual eceran Rp 15.000/bungkus (kami sarankan, Sari Rasa boleh sesuaikan).

**Skema kerja sama:**
- Sistem konsinyasi: Sari Rasa menerima titipan barang, tidak membayar di muka.
- Harga jual Rp 15.000/bungkus; Sari Rasa mendapat Rp 3.000 (20%) per bungkus terjual.
- Rekap penjualan & pembayaran bagian Sari Rasa dilakukan setiap akhir bulan.
- Barang yang tidak laku atau mendekati kedaluwarsa kami tarik/ganti tanpa biaya untuk Sari Rasa.
- Display kami sediakan.

**Simulasi pendapatan Sari Rasa (perkiraan, per bulan):**

| Penjualan/bulan | 30 bungkus | 60 bungkus | 100 bungkus |
|---|---|---|---|
| Pendapatan Sari Rasa | Rp 90.000 | Rp 180.000 | Rp 300.000 |

*Simulasi, bukan jaminan hasil penjualan.*

**Manfaat untuk Sari Rasa:**
- Tambahan pemasukan tanpa modal stok dan tanpa risiko rugi beli putus.
- Produk lokal yang bisa jadi favorit wisatawan `[isi: bukti]` — menambah daya tarik rak oleh-oleh.
- Kami yang mengurus stok, pengisian ulang, dan penarikan barang tak laku.

**Langkah berikutnya:** Uji coba 3 bulan mulai [tanggal], lalu evaluasi bersama untuk menentukan kelanjutan dan kemungkinan penambahan stok.

Kontak: [Nama] – Pemilik Tempe Mbak Wid – WA [nomor] – [email]

---

## Pesan pengantar WA

Halo Kak, perkenalkan saya dari Tempe Mbak Wid 🙏
Kami produksi keripik tempe dan ingin menawarkan kerja sama titip jual di toko oleh-oleh Sari Rasa.
Sistemnya konsinyasi: Sari Rasa tidak perlu modal di muka, dapat 20% dari setiap bungkus terjual (Rp 3.000/bungkus dari harga Rp 15.000).
Stok awal, display, dan pengisian ulang kami yang urus.
Boleh saya kirim proposal lengkapnya untuk dipelajari Kak?
Terima kasih banyak 🙏

---

**Yang perlu kamu isi sebelum kirim:**
- `[Nama]`, `[nomor WA]`, `[email]` di bagian kontak
- `[tanggal]` mulai uji coba
- Keputusan soal klaim "favorit wisatawan" — kasih bukti atau hapus saja

File lengkap (termasuk draf email) tersimpan di workspace: `proposal.md`. Mau saya buatkan versi lengkap (2-5 halaman) atau versi bahasa yang lebih formal juga?
~~~~

### Verifikasi (Python + `cek_fakta.py` dijalankan ulang oleh penguji)

- **S1 angka:** 25% × 35.000 = Rp8.750 ✔; simulasi 30/60/100 kotak = Rp262.500 / 525.000 / 875.000 ✔; laba pengguna 35.000 − 8.750 − 18.500 = Rp7.750 ✔; titik impas porsi = 1 − 18.500/35.000 = 47,1% → "sekitar 47%" ✔. Modal tidak masuk proposal ✔. `cek_fakta`: LULUS (0 GAGAL).
- **S2 angka:** 35% → produsen 13.000 < modal 14.000 = rugi Rp1.000/botol ✔; impas 30% ✔; usulan **25%** (di bawah impas — cacat lama 3 beres) → toko Rp5.000, laba Rp1.000/botol ✔; simulasi 300/600/1.000 botol = Rp1,5 jt / 3 jt / 5 jt ✔. BPOM → `[isi: nomor/bukti]` ✔, "paling laris se-Solo" → versi lunak "ingin menjadi salah satu terlaris" + `[isi: data]` ✔; "kopi susu literan" dipakai persis, **tanpa 250ml** ✔; "sudah dikenal pelanggan di Solo"/"tren terus diminati" **tidak muncul** ✔; Asumsi memuat stok/isi ulang/display/uji coba ✔. `cek_fakta` balasan & lampiran: LULUS.
  - **Masih salah:** (a) proposal & pesan WA/email menulis "Kopi Pakde — **kopi susu literan di Solo**", padahal pengguna hanya menyebut Solo sebagai lokasi **minimarket**; kota usaha dikarang — persis larangan "kota asal yang hanya kota mitra" di SKILL.md, dan **lolos** `cek_fakta.py`. (b) Paragraf "Catatan soal persentase" **di dalam proposal untuk minimarket** memuat "modal produksi Rp14.000/botol" dan "untung Rp1.000/botol bagi kami" — SKILL.md: modal/laba hanya untuk pengguna; membuka modal ke pembeli melemahkan posisi tawar. (c) "Kebutuhan pelanggan akan kopi susu kemasan siap minum terus ada" — klaim pasar ringan tanpa data. Proposal tidak tampil di chat (hanya lampiran) — wajar karena lampiran terkirim.
- **S3 angka:** 20% × 15.000 = Rp3.000 ✔; laba pengguna 15.000 − 3.000 − 9.000 = Rp3.000 ✔; impas 1 − 9.000/15.000 = **40%** ✔; simulasi 30/60/100 = Rp90.000 / 180.000 / 300.000 ✔; modal tidak masuk proposal ✔. "Favorit wisatawan" hanya sebagai `[isi: bukti]` + peringatan ke pengguna ✔; **tanpa "khas Malang"/"tanpa pengawet"/"renyah"** ✔. Sisa ringan: "pilihan oleh-oleh khas", "Produk lokal". `cek_fakta`: LULUS.
- **SEBELUM:** S1 menawarkan mengirim WA sendiri ke owner, "label & tanggal produksi tertera", "sample". S2 (file) "usaha rumahan", "racikan khas", "bahan pilihan", "higienis", "susu segar", "fresh"; skema 35% (rugi) tetap ditulis di proposal; proposal tidak tampil di chat. S3 "produsen keripik tempe **khas Malang**", "tempe pilihan", "tanpa pengawet", "fresh", "favorit wisatawan" ditulis sebagai fakta, "banyak pelanggan repeat order" — `cek_fakta`: **4 GAGAL, 3 CEK**.
- **Catatan alat:** `cek_fakta.py` tidak menangkap pola "<produk> di <kota mitra>" sebagai asal/kota usaha karangan, juga tidak memeriksa kebocoran modal/laba di teks untuk mitra. Saran: tandai kota yang di fakta hanya muncul setelah "ke/minimarket/toko/kafe … di" bila di teks muncul sebagai kota usaha; tambahkan cek "modal|untung .* bagi kami" di proposal.

### Status cacat lama

| Cacat | Status |
|---|---|
| 1. Klaim turunan ("sudah dikenal di Solo", "tren terus diminati") | **Beres** — tidak muncul di S2; varian S3 juga bersih |
| 2. Komitmen default tidak di Asumsi | **Beres di file** (S1–S3 punya bagian Asumsi lengkap); di chat S1/S3 Asumsi tidak ditampilkan dan file tidak dilampirkan |
| 3. Saran porsi = titik impas | **Beres** — 25% (< 30%), laba Rp1.000 ditampilkan |
| Ukuran "250ml" karangan | **Beres** |

**Regresi / cacat baru:** kota usaha dikarang dari kota mitra ("kopi susu literan di Solo"); modal & laba per botol masuk ke proposal untuk minimarket (S2).

### Skor

| | Sebelum | Sesudah | Alasan |
|---|---|---|---|
| Skenario 1 | 5.5 | 8.5 | SESUDAH proposal singkat + WA siap kirim, angka & impas benar, tanpa klaim karangan; Asumsi hanya di file. SEBELUM klaim karangan & tawaran kirim WA otomatis. |
| Skenario 2 | 5 | 7 | SESUDAH peringatan rugi + usulan 25% yang benar, BPOM/laris jadi `[isi]`, tanpa "dikenal di Solo"/250ml; minus kota usaha dikarang & modal/laba bocor ke proposal. SEBELUM klaim sifat produk karangan & skema rugi tetap ditulis. |
| Skenario 3 (varian) | 5 | 8.5 | SESUDAH klaim favorit dijadikan `[isi: bukti]` + penjelasan, angka benar, tanpa "khas Malang"; sisa "oleh-oleh khas". SEBELUM "khas Malang", "tanpa pengawet", favorit sebagai fakta. |
| **Rata-rata** | **5.17** | **8.0** | |

**VERDIK: BELUM (nyaris)** — rata-rata tepat 8,0 dan jauh di atas SEBELUM, semua angka benar, `cek_fakta.py` benar-benar dijalankan, dan cacat target 1.0.5/1.0.6 (klaim turunan, 250ml, porsi impas) sudah beres serta tidak muncul di varian baru. Tetapi proposal S2 untuk mitra masih memuat fakta karangan (kota usaha "di Solo") dan membocorkan modal/laba — syarat "tanpa fakta karangan/kesalahan" belum terpenuhi.

Sisa untuk pembuat: (1) Langkah 0 contoh eksplisit: "minimarket di Solo" ≠ "Kopi Pakde dari/di Solo" — kota usaha `[isi]` bila tidak disebut; (2) alasan menurunkan porsi ditulis **untuk pengguna**, di proposal cukup "kami mengusulkan 25%" tanpa modal/laba; tambahkan ke checklist; (3) tampilkan Asumsi singkat di chat (3–4 butir) atau lampirkan file proposal.

### Cuplikan jualan (jujur)

> Minta "tulis aja kalau keripik kita favorit wisatawan"? Tanpa skill, bot langsung menulis "produsen keripik tempe khas Malang… tanpa pengawet… favorit wisatawan" sebagai fakta; dengan skill, klaim yang belum ada buktinya ditandai [isi: bukti] beserta alasannya, porsi toko dicek untung-ruginya (titik impas 40%), dan proposal + pesan WA siap kirim.
