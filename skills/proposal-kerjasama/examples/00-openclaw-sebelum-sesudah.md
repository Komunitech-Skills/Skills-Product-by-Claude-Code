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

