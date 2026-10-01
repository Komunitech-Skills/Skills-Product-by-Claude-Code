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

