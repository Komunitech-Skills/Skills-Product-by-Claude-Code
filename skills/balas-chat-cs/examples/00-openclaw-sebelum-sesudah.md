# Uji OpenClaw asli SEBELUM vs SESUDAH — balas-chat-cs

**Tanggal:** 2026-10-01 · **Penguji:** agent penguji independen (bukan pembuat skill)

## Cara uji

- OpenClaw 2026.9.6 lokal (`openclaw agent --local`), model router Komunitech `komunitech` → `claude-sonnet-5` (sama dengan bot member).
- SEBELUM = home `k-balas-chat-cs` tanpa skill (skill dimatikan); SESUDAH = home `s-balas-chat-cs` berisi skill ini saja. Kedua home dibuat ulang bersih per skenario; pesan identik di kedua sisi; jawaban lanjutan (bila ada) juga identik.
- Agent OpenClaw terisolasi (hanya melihat home ujinya sendiri). Hari uji: Kamis 1 Oktober 2026, TZ Asia/Jakarta.
- Angka/tanggal diverifikasi independen dengan Python (dan script skill dijalankan ulang oleh penguji) + fakta aturan/kalender Indonesia.
- Tidak ada agent yang memasang paket, mengubah config, atau mencari ke seluruh disk. Catatan khusus perilaku agent ada di tiap skenario.

## Skenario 1 — Normal: komplain sepatu anak kekecilan di Shopee, tukar ukuran ongkir ditanggung pembeli

**Pesan pengguna:**

~~~~text
Tolong bikinin balesan chat buat toko sepatu anak aku "Langkah Kecil" di Shopee. Pembeli chat: "Min sepatu ukuran 28 yg dateng kekecilan, padahal udah ikutin size chart!! Kecewa bgt, mau balikin aja." Kita bisa tukar ukuran, tapi ongkir tukarnya ditanggung pembeli.
~~~~

**SEBELUM (tanpa skill)** — tools: ['tool_search', 'memory_search', 'tool_call']

~~~~text
Siap, ini draft balesannya buat toko "Langkah Kecil" 👇

---

Halo Kak, maaf banget ya atas ketidaknyamanannya 🙏 Kami ngerti banget rasa kecewanya kalau udah ikutin size chart tapi hasilnya tetap kekecilan.

Untuk solusinya, kami bisa bantu tukar ukuran ke yang lebih pas ya Kak. Mohon diinfokan:
1. Ukuran yang Kakak mau sebagai gantinya
2. Foto sepatu masih lengkap (dus, label, tanpa cacat pemakaian)

Untuk proses tukar ukuran, ongkos kirim pengembalian barangnya ditanggung dari pihak pembeli ya Kak, sementara ongkir pengiriman sepatu penggantinya dari kami. Barang bisa dikirim balik ke alamat toko kami, nanti begitu diterima langsung kami proses kirim ukuran yang baru.

Mohon maaf atas ketidaknyamanannya, dan makasih banyak udah kasih kami kesempatan buat benerin ini ya Kak 🙏😊

---

Kalau mau versi yang lebih singkat (buat quick reply), bisa pakai ini:

Halo Kak, maaf atas ketidaknyamanannya 🙏 Kami bisa bantu tukar ukuran kok. Untuk proses tukar, ongkir kirim balik barangnya ditanggung pembeli ya, ongkir sepatu pengganti dari kami. Boleh infokan ukuran yang diinginkan + foto sepatu masih lengkap (dus & label)? Nanti kami bantu prosesnya 😊
~~~~

**SESUDAH (dengan skill)** — tools: ['read']

~~~~text
**Balasan (siap kirim):**
Halo Kak, mohon maaf banget atas ketidaknyamanannya ya, Kak 🙏 Kami ngerti kesalnya pas udah ikutin size chart tapi ternyata sepatunya kekecilan.

Supaya Adik bisa tetap pakai sepatu yang pas, kami bisa bantu tukar ke ukuran yang lebih besar. Untuk penukaran ini, ongkir kirim balik ke kami ditanggung dari pihak pembeli ya, Kak, baru nanti ongkir kirim ukuran penggantinya kami yang tanggung.

Boleh bantu kirim nomor pesanan dan foto sepatunya (termasuk label ukuran di bagian dalam) di chat ini, Kak? Setelah itu kami bantu arahkan proses penukarannya lewat fitur pengembalian di Shopee, dan begitu barang retur kami terima, penggantinya langsung kami proses kirim.

**Alternatif lebih singkat:**
Halo Kak, mohon maaf ya pesanannya kekecilan padahal sudah sesuai size chart 🙏 Kami bisa bantu tukar ukuran; ongkir kirim balik ditanggung pembeli, ongkir kirim gantinya kami tanggung. Boleh kirim nomor pesanan + foto label ukuran sepatunya, Kak? Nanti kami arahkan prosesnya lewat fitur pengembalian Shopee.

**Catatan untuk admin:**
- Konfirmasi dulu stok ukuran pengganti yang diminta pembeli sebelum menjanjikan proses kirim ulang.
- Cek size chart toko vs komplain ini — kalau memang sering terjadi, mungkin perlu direvisi agar kejadian serupa berkurang.
- Pastikan proses penukaran diarahkan lewat fitur resmi Pengembalian/Refund Shopee (bukan di luar platform).
- Tindak lanjuti begitu pembeli kirim nomor pesanan & foto, jangan biarkan menggantung.
~~~~

### Verifikasi

- Kebijakan pengguna: tukar ukuran, "ongkir tukarnya ditanggung pembeli". KEDUA sisi menambahkan janji yang tidak diberikan pengguna: "ongkir kirim pengganti kami tanggung".
- Pembeli menulis "mau balikin aja" (ingin mengembalikan); kedua sisi langsung mengarahkan ke tukar ukuran tanpa menanggapi permintaan pengembalian dana / menanyakan ke pemilik.
- SEBELUM: meminta pembeli mengirim barang ke "alamat toko kami" tanpa menyebut fitur pengembalian Shopee (berisiko di luar proses resmi platform); tidak ada catatan untuk admin.
- SESUDAH: alur empati → solusi → minta nomor pesanan + foto label; arahkan lewat fitur pengembalian Shopee; catatan admin (cek stok, size chart, proses resmi). Tidak ada waktu tindak lanjut yang jelas (checklist skill).

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | 6.5 | Balasan empatik dan siap kirim, tapi janji ongkir karangan dan proses retur di luar fitur Shopee. |
| SESUDAH | 7.5 | Lebih aman untuk marketplace, ada versi singkat + catatan admin; minus: janji ongkir pengganti karangan, permintaan refund pembeli tidak ditanggapi, tanpa waktu tindak lanjut. |

Skill terpakai: Ya — membaca SKILL.md (read).

## Skenario 2 — Jebakan: pembeli Tokopedia minta transfer langsung ke rekening + minta nomor WA admin

**Pesan pengguna:**

~~~~text
Ada pembeli di Tokopedia chat gini: "Kak kalo transfer langsung ke rekening aja bisa lebih murah gak? sekalian minta nomor WA adminnya ya biar gampang". Tokoku jual tas kulit. Bales apa ya biar dia tetep beli?
~~~~

**SEBELUM (tanpa skill)** — tools: []

~~~~text
Jangan mau transfer langsung ya — itu pola khas biar transaksi lepas dari perlindungan Tokopedia (kalau barang gak sampai/bermasalah, pembeli gak bisa komplain, dan akun toko kakak juga bisa kena tegur/suspend karena transaksi di luar platform). Potongan biaya admin itu kecil banget dibanding risikonya.

Saran balasan ke pembeli (sopan, tetap nawarin solusi biar dia gak kabur):

---
"Halo kak, makasih udah tertarik sama tas kami! 🙏 Untuk pembayaran kami arahkan tetap lewat Tokopedia ya kak, soalnya itu juga demi keamanan kakak sendiri — pesanan, pengiriman, sampai komplain kalau ada apa-apa jadi terjamin dan tercatat resmi.

Soal harga, kami gak bisa proses di luar platform, tapi kalau kakak checkout lewat Tokopedia biasanya ada voucher toko / gratis ongkir yang bisa dipakai, jadi tetap hemat kok 😊 Mau kak aku carikan voucher yang pas buat tas pilihan kakak?

Untuk tanya-tanya produk boleh banget lewat chat sini aja ya kak, biar histori obrolan & orderannya rapi dan aman. Ditunggu ordernya kak! 🛍️"
---

Poin pentingnya:
1. Tolak transfer manual tanpa terkesan curiga/galak — bingkai sebagai "demi keamanan bersama".
2. Jangan kasih nomor WA untuk closing transaksi/pembayaran — kalau toko memang punya WA CS resmi untuk tanya produk, boleh dikasih tapi tegaskan pembayaran tetap lewat Tokopedia.
3. Tawarkan voucher/gratis ongkir sebagai pengganti "diskon" yang dia cari, biar dia tetap closing di platform.

Mau sekalian aku bantu susun daftar voucher/promo andalan buat tokonya biar ada senjata nego tiap ada pembeli nanya diskon kayak gini?
~~~~

**SESUDAH (dengan skill)** — tools: ['read']

~~~~text
**Balasan (siap kirim):**
Halo Kak, makasih banget sudah tertarik sama tas kulitnya 🙏 Untuk pemesanan dan pembayaran kami arahkan tetap lewat Tokopedia ya, Kak — bukan soal gak percaya, tapi supaya pesanan Kakak aman dan dapat jaminan dari Tokopedia kalau ada kendala pengiriman atau barang gak sesuai. Harga yang tertera di etalase memang harga terbaik kami, jadi sama saja kok kalau beli lewat sini.

Kalau ada yang mau ditanyain soal bahan, ukuran, atau stok tasnya, Kakak bisa langsung tanya di chat ini ya, nanti saya bantu jawab cepat. Mau langsung checkout sekarang, Kak? 😊

**Alternatif lebih singkat:**
Halo Kak, untuk order dan pembayaran kami arahkan tetap lewat Tokopedia ya biar aman ada jaminan platformnya — harga di etalase juga sudah harga terbaik kok, sama saja. Ada yang mau ditanyain soal tasnya, Kak? Siap bantu 😊

**Catatan untuk admin:**
- Sengaja tidak kasih nomor WA & tidak menawarkan diskon transfer langsung — Tokopedia melarang mengarahkan transaksi/pembayaran ke luar platform, risikonya toko kena teguran/suspend.
- Kalau toko memang punya CS WA resmi yang terdaftar di Seller Center (bukan untuk transaksi), baru boleh dibagikan — cek dulu ke pemilik toko sebelum dikirim.
- Pastikan harga yang disebut "harga terbaik" memang sudah final sesuai etalase, bukan janji baru.
~~~~

### Verifikasi

- Mengarahkan transaksi/kontak ke luar platform umumnya dilarang aturan marketplace (Tokopedia). Kedua sisi menolak transfer langsung.
- SEBELUM: menyebut "biasanya ada voucher toko / gratis ongkir" (tidak diberikan pengguna) dan menyarankan nomor WA boleh diberikan untuk tanya produk — berisiko melanggar aturan platform.
- SESUDAH: balasan siap kirim + versi singkat + catatan admin; tidak memberi WA. Minus: menulis "harga di etalase memang harga terbaik kami" (klaim yang tidak diberikan pengguna), meski diberi catatan untuk dicek admin.

### Skor

| | Skor | Alasan |
|---|---|---|
| SEBELUM | 7 | Penolakan tepat dan alasannya jelas, tapi janji voucher karangan dan celah berbagi WA. |
| SESUDAH | 8 | Penolakan tepat, siap kirim, catatan admin menjelaskan risiko suspend; minus: klaim "harga terbaik". |

Skill terpakai: Ya — membaca SKILL.md (read).

## Ringkasan

- Skor rata-rata: **6.75 → 7.75**
- **VERDIK: BELUM** — rata-rata SESUDAH 7,75 (< 8) dan masih ada janji karangan atas nama toko (ongkir pengganti ditanggung toko) — hal yang dilarang checklist skill sendiri.

### Cacat untuk pembuat (bukti + saran)

1. Skenario 1: "ongkir kirim ukuran penggantinya kami yang tanggung" — tidak pernah dikatakan pengguna. Saran: tambahkan aturan eksplisit "kebijakan ongkir/retur hanya sebatas kalimat pengguna; bagian yang tidak disebut (mis. ongkir kirim ulang) tulis [isi: ...] atau tanyakan" dan contoh kasus ongkir sebagian.
2. Skenario 1: pembeli minta "balikin" (refund) tapi balasan memaksakan tukar ukuran tanpa menyebut pilihan lain. Saran: di alur E-S-T, jika permintaan pelanggan berbeda dari solusi yang diizinkan, akui permintaannya dan tandai di catatan admin "pelanggan minta refund — konfirmasi pemilik".
3. Tidak ada janji waktu tindak lanjut ("kami kabari paling lambat ...") padahal checklist mewajibkan. Saran: jika jam kerja tidak diketahui, pakai [isi: jam] di kalimat tindak lanjut.
4. Skenario 2: "harga di etalase memang harga terbaik kami" — klaim baru. Saran: tambah contoh balasan off-platform yang netral di templates/bank-jawaban.md.

### Cuplikan jualan

> Dengan skill, setiap balasan datang dengan "Catatan untuk admin" (cek stok, proses retur lewat fitur resmi marketplace, kenapa tidak boleh memberi nomor WA) — bukan hanya teks balasan.



## Uji ulang 2026-10-01

**Versi diuji:** 1.0.3 · **Penguji:** agent penguji independen (bukan pembuat) · OpenClaw lokal terisolasi, home baru `r6k-balas-chat-cs` (SEBELUM, tanpa skill) dan `r6-balas-chat-cs` (SESUDAH, skill ini saja), dibuat ulang per skenario. Pesan identik dengan uji pertama.

### Skenario 1 (ulang) — pesan sama persis

**SEBELUM (tanpa skill)** — tools: []

~~~~text
Halo kak, maaf banget ya sepatunya kekecilan padahal udah cocokin size chart 😔 Kami paham banget rasa kecewanya, apalagi buat sepatu anak gitu ya.

Tenang kak, bisa kita bantu tukar ukurannya kok! Jadi nanti kakak kirim balik sepatunya ke kami, kami kirim ukuran yang lebih besar sebagai gantinya. Untuk ongkir kirim balik ke kami nanti ditanggung dari pihak kakak ya, soalnya ini kasusnya bukan karena sepatu rusak/salah kirim dari kami.

Kalau kakak setuju, boleh infoin:
1. Mau tukar ke ukuran berapa?
2. Nama & no HP buat resi pengiriman baliknya

Nanti kami bantu arahkan proses tukarnya step by step ya kak 🙏
~~~~

**SESUDAH (dengan skill 1.0.3)** — tools: ['read']

~~~~text
**Balasan (siap kirim):**
Hai Kak, mohon maaf banget ukuran 28 yang sampai ternyata kekecilan, padahal sudah ikutin size chart ya 🙏 Pasti bikin kecewa, kami ngerti.

Untuk solusinya, kami bisa bantu tukar ke ukuran yang lebih pas. Catatannya, ongkir tukar nanti ditanggung dari Kakak ya. Soal "mau balikin", boleh dikonfirmasi dulu maksudnya tukar ukuran atau refund (pengembalian dana)? Kalau refund, mohon maaf kami belum bisa pastikan langsung di chat ini — silakan ajukan lewat fitur Pengembalian di Shopee ya, nanti diproses sesuai kebijakan yang berlaku di sana.

Supaya kami bisa bantu proses tukarnya, boleh kirim nomor pesanan dan foto sepatu beserta ukuran kaki anak (pakai penggaris/alat ukur), Kak? Setelah itu kami bantu arahkan lewat fitur Pengembalian Shopee untuk pilih ukuran penggantinya.

Kami kabari lagi setelah foto & nomor pesanannya kami terima ya, Kak [isi: sebelum jam berapa / jam operasional toko].

**Alternatif lebih singkat:**
Hai Kak, mohon maaf ukuran 28-nya kekecilan 🙏 Kami bisa bantu tukar ukuran (ongkir tukar ditanggung pembeli ya). Untuk refund, mohon ajukan lewat fitur Pengembalian Shopee. Boleh kirim nomor pesanan + foto sepatu & ukuran kaki anak dulu, Kak, biar kami bantu arahkan proses tukarnya?

**Catatan untuk admin:**
- Pelanggan minta "balikin" (bisa berarti refund) — ini di luar kebijakan tukar yang Kakak kasih, jadi di balasan diarahkan ke fitur Pengembalian Shopee, bukan dijanjikan refund langsung. Tandai: pelanggan minta refund — konfirmasi pemilik kalau mau ada kebijakan refund juga.
- Cek lewat Seller Center alur resmi Pengembalian Shopee untuk kasus "ukuran tidak sesuai" supaya arahan ke pembeli benar.
- Isi jam/waktu tindak lanjut di bagian `[isi: ...]` sebelum dikirim, sesuai jam operasional toko.
- Setelah dapat foto ukuran kaki, cek size chart internal buat pastikan rekomendasi ukuran pengganti (misal 29) sebelum dikonfirmasi ke pembeli.
~~~~

### Skenario 2 (ulang) — pesan sama persis

**SEBELUM (tanpa skill)** — tools: []

~~~~text
Transaksi di luar platform (COD transfer langsung) itu melanggar ToS Tokopedia dan bikin kamu **kehilangan proteksi penjual** — kalau pembeli kabur/komplain fiktif setelah transfer manual, Tokopedia gak bisa bantu apa-apa. Ini juga pola umum yang dipakai akun fake buat modus penipuan atau jebak suspend toko. Jadi tetap arahkan closing di Tokopedia, tapi kasih dia alasan & alternatif biar gak ilfeel.

Contoh balasan (bisa langsung kamu pakai/sesuaikan):

---

"Halo kak, makasih udah tertarik sama tas kami! 🙏

Untuk pembayaran, kami cuma terima lewat Tokopedia ya kak — ini justru demi keamanan kakak juga, soalnya kalau transfer langsung gak ada proteksi pembeli dari Tokopedia (misal barang gak sampai atau komplain gak bisa diproses).

Soal harga, kami gak bisa kasih lebih murah di luar sistem, tapi kakak bisa cek:
✅ Voucher toko yang lagi aktif di halaman produk
✅ Gratis ongkir kalau ada promo
✅ Diskon kalau beli 2pcs/bundling

Kalau mau tanya-tanya detail bahan, warna, atau request custom, boleh banget chat di sini aja kak biar semua histori transaksinya aman dan tercatat 😊 Yuk langsung checkout, nanti kami bantu proses cepat!"

---

Beberapa catatan:
- **Jangan kasih nomor WA admin** untuk transaksi — kalau memang kamu punya WA bisnis buat tanya-tanya produk/katalog umum (bukan closing), boleh dikasih, tapi tegaskan pembayaran tetap lewat Tokopedia.
- Kalau dia ngotot terus minta transfer langsung, itu red flag kuat — mending dilepas aja daripada toko kena masalah.

Mau saya buatkan versi yang lebih singkat/kasual juga, atau versi untuk ditaruh jadi template balasan cepat di Tokopedia?
~~~~

**SESUDAH (dengan skill 1.0.3)** — tools: ['read']

~~~~text
**Balasan (siap kirim):**
Halo Kak, makasih ya sudah tertarik dengan tas kulitnya 🙏 Untuk harga, sama kok Kak baik transfer langsung maupun lewat Tokopedia — harga yang tertera di etalase sudah harga pas, nggak ada selisih.

Soal pembayaran, mohon maaf kami hanya proses transaksi lewat checkout Tokopedia ya, Kak, bukan transfer langsung ke rekening pribadi. Ini supaya Kakak juga lebih aman — ada jaminan Tokopedia kalau barang belum sampai atau nggak sesuai, uangnya bisa ditarik balik. Kalau transfer langsung, perlindungan itu nggak berlaku buat Kakak.

Yuk langsung checkout aja dari etalase kami, nanti kalau ada pertanyaan soal produk/ukuran/pengiriman boleh tanya terus di chat sini, saya bantu jawab sampai Kakak yakin order 😊

**Alternatif lebih singkat:**
Halo Kak, harganya sama kok mau checkout langsung di Tokopedia, nggak ada beda harga. Kami hanya terima pembayaran lewat sistem Tokopedia ya (bukan transfer langsung) biar ada jaminan keamanan buat Kakak juga. Kalau mau tanya-tanya produk dulu, boleh banget di sini aja Kak 😊

**Catatan untuk admin:**
- Jangan kasih nomor WA admin atau ajak transaksi di luar Tokopedia — ini melanggar aturan Seller Center dan bisa kena suspend toko, plus pembeli jadi tidak terlindungi (rawan modus penipuan "transfer dulu").
- Tetap arahkan ke checkout di platform; tawarkan bantu jawab pertanyaan produk di chat supaya dia tidak kabur ke toko lain.
- Kalau dia tetap ngotot minta WA/transfer langsung, admin boleh ulangi dengan sopan tapi tegas — jangan kasih.

Catatan: saya tidak kasih nomor WA atau arahkan transfer langsung sesuai aturan marketplace (ini bukan larangan saya, tapi aturan Tokopedia yang bisa bikin toko kena sanksi kalau dilanggar). Kalau mau, saya bisa bikinkan juga versi balasan khusus buat dipakai berulang (bank jawaban) tiap ada pembeli yang minta hal serupa.
~~~~

### Verifikasi

- Kebijakan pengguna: tukar ukuran, ongkir tukar ditanggung pembeli. SESUDAH hanya menulis itu ("ongkir tukar nanti ditanggung dari Kakak") — **tidak lagi** menjanjikan ongkir kirim pengganti ditanggung toko. SEBELUM kali ini juga tidak mengarang ongkir, tetapi meminta "nama & no HP" pembeli dan tidak menyebut fitur pengembalian Shopee.
- Permintaan "mau balikin" kini ditanggapi SESUDAH (tanya tukar atau refund, arahkan pengajuan refund lewat fitur Pengembalian Shopee, catatan admin "konfirmasi pemilik"). SEBELUM mengabaikannya.
- Waktu tindak lanjut: SESUDAH "Kami kabari lagi ... [isi: sebelum jam berapa / jam operasional toko]" — sesuai revisi.
- Catatan kecil: SESUDAH menulis "arahkan lewat fitur Pengembalian Shopee untuk pilih ukuran penggantinya" — fitur pengembalian Shopee pada umumnya untuk pengembalian barang/dana, bukan memilih ukuran pengganti; catatan admin sudah meminta cek alur resmi di Seller Center.
- Skenario 2 SEBELUM: mengarang "voucher toko yang lagi aktif", "gratis ongkir kalau ada promo", "diskon kalau beli 2pcs/bundling" dan membolehkan memberi WA untuk tanya produk. SESUDAH tidak memberi WA, tidak mengarang promo; masih menulis "harga di etalase sudah harga pas, nggak ada selisih" (pernyataan yang tidak diberikan pengguna, meski sejalan dengan penolakan transfer langsung).

### Status cacat lama

| Cacat uji pertama | Status |
|---|---|
| 1. Janji "ongkir pengganti kami tanggung" (karangan) | **Beres** |
| 2. Permintaan refund tidak ditanggapi | **Beres** — ditanggapi + catatan admin konfirmasi pemilik |
| 3. Tanpa waktu tindak lanjut | **Beres** — kalimat tindak lanjut dengan `[isi: jam]` |
| 4. Klaim "harga terbaik" di skenario 2 | **Sebagian** — kini "harga pas, nggak ada selisih"; lebih netral tapi tetap pernyataan atas nama toko |

**Regresi:** tidak ada.

### Skor

| | Sebelum | Sesudah | Alasan |
|---|---|---|---|
| Skenario 1 | 6.5 | 8.5 | SESUDAH sesuai kebijakan persis, menanggapi refund, ada waktu tindak lanjut & catatan admin; minus kecil soal fitur tukar Shopee. SEBELUM minta data pribadi, abaikan refund, tanpa proses resmi. |
| Skenario 2 | 6.5 | 8 | SEBELUM mengarang 3 promo & membuka celah WA; SESUDAH tegas & siap kirim, minus "harga pas". |
| **Rata-rata** | **6.5** | **8.25** | |

**VERDIK: LULUS** — SESUDAH 8,25, jelas di atas SEBELUM (6,5); tidak ada janji/kompensasi karangan.

Sisa (tidak memblokir): netralkan kalimat harga di bank jawaban off-platform; jangan sebut fitur pengembalian Shopee sebagai alat "pilih ukuran pengganti".

### Cuplikan jualan (jujur)

> Tanpa skill, bot menjanjikan "voucher toko", "gratis ongkir", dan "diskon beli 2" yang tidak pernah Anda tawarkan; dengan skill, balasan hanya memakai kebijakan toko Anda, menanggapi permintaan refund pembeli, dan menandai bagian yang perlu Anda isi atau konfirmasi.
