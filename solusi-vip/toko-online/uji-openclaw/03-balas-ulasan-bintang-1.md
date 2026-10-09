# Uji OpenClaw — Toko Online · Balas ulasan bintang 1 Shopee (telat, warna beda, admin lambat)

Tanggal uji: 2026-10-01 (Asia/Jakarta) · Penguji independen · Skill yang diharapkan: `balas-ulasan-pelanggan`

OpenClaw lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`) yang sama dengan bot. SEBELUM = home `kosong-toko-online` (tanpa skill). SESUDAH = home `sol-toko-online` (paket skill solusi terpasang). Pesan identik.

## Pesan member

> ada ulasan bintang 1 di shopee: 'barang dtg telat 5 hari, warna beda sm foto, adminnya slow respon. kecewa bgt gk lg2 belanja disini!!' tolong balesin yg sopan dong tp jgn kesannya kami yg salah semua, telatnya kan krn ekspedisi. warnanya emg beda dikit krn cahaya foto

## Balasan SEBELUM (tanpa skill) — utuh

_Alat yang dipakai agent: `tidak ada` · model jawaban: `claude-sonnet-5` · durasi 15 detik_

> Nih draf balasannya, sopan tapi tetap jelasin duduk perkaranya tanpa kesan playing victim:
>
> ---
>
> Halo Kak, mohon maaf atas ketidaknyamanannya ya 🙏
>
> Untuk keterlambatan pengiriman, kami turut kecewa — proses packing & kirim dari gudang kami sudah sesuai SLA, namun estimasi tiba memang di luar kendali kami karena mengikuti jadwal pihak ekspedisi. Kami paham ini tetap bikin nunggu lama dan akan terus kami kawal ke pihak kurir supaya ke depannya lebih tepat waktu.
>
> Soal warna, mohon dimaklumi bahwa foto produk kami ambil dengan pencahayaan studio, jadi kadang ada sedikit perbedaan tone warna dibanding kondisi aslinya — ini wajar terjadi di hampir semua produk fashion/aksesoris karena faktor kamera & layar HP masing-masing, bukan karena produknya tidak sesuai.
>
> Untuk respon admin yang lambat, ini jadi catatan buat kami dan akan kami perbaiki.
>
> Kalau Kakak masih kurang puas, boleh banget chat kami langsung ya, nanti kami bantu solusikan 🙏 Makasih sudah belanja dan kasih masukan, semoga next bisa lebih baik lagi.
>
> ---
>
> Mau dipendekin lagi atau nada lebih formal/kasual?

## Balasan SESUDAH (dengan paket skill) — utuh

_Alat yang dipakai agent: `read, exec` · model jawaban: `claude-sonnet-5` · durasi 66 detik_

> ## Balasan ulasan — Shopee, ★1 (negatif: campuran telat kirim + warna beda + respon CS lambat)
>
> ### Balasan publik (utama) — 469 karakter
> Kak, terima kasih sudah berbagi pengalamannya, dan mohon maaf untuk ketidaknyamanannya. Untuk keterlambatannya, memang sempat ada kendala di proses pengiriman oleh jasa kirim saat itu. Soal warna, perbedaan tipis bisa muncul karena pencahayaan saat pemotretan produk — masukan ini kami pakai untuk perbaiki hasil fotonya. Kami juga sedang membenahi respon tim CS agar lebih cepat. Mohon cek chat toko kami ya Kak, kami ingin bantu lebih lanjut. Terima kasih masukannya.
>
> ### Alternatif (lebih singkat) — 308 karakter
> Mohon maaf atas keterlambatan pengiriman dan selisih warna yang Kakak alami, Kak. Keterlambatan kemarin karena kendala di pihak ekspedisi, dan selisih warna wajar terjadi karena pencahayaan foto produk. Kami juga lagi evaluasi respon tim CS. Yuk chat toko kami, kami bantu solusinya. Terima kasih masukannya.
>
> ### Pesan chat pribadi (eskalasi)
> Halo Kak, mohon maaf ya atas keterlambatan paket dan ketidaksesuaian warna yang Kakak alami, serta maaf respon kami kemarin kurang cepat. Boleh info nomor pesanannya supaya kami bisa cek proses pengirimannya? Soal warna, boleh kirim foto barang yang diterima — kalau memang ada selisih di luar wajar, kami bantu solusinya. Terima kasih sudah sabar, Kak.
>
> ### Hasil cek (script)
> - Utama: Shopee, negatif, 469/500 karakter — LULUS, tidak ada temuan.
> - Alternatif: Shopee, negatif, 308/500 karakter — LULUS, tidak ada temuan.
>
> 📝 Catatan untuk pemilik:
> - Balasan dibuat tidak defensif tapi tetap menjelaskan duduk perkara (keterlambatan = ekspedisi, warna = pencahayaan foto) tanpa menyalahkan pembeli secara terbuka — jadi calon pembeli lain ikut paham.
> - Kirim pesan chat pribadi dulu sebelum/bareng posting balasan publik, supaya kalimat "mohon cek chat toko" sinkron.
> - Soal "tim CS lebih cepat" — pastikan ini memang sedang/akan dilakukan, jangan janji kosong. Kalau belum ada rencana perbaikan nyata, bilang saja dan saya ubah kalimatnya jadi lebih umum.
> - Tidak menjanjikan refund/ganti karena belum ada info itu diminta — kalau mau ditambahkan kompensasi, kasih tahu saya.

## Verifikasi angka & fakta (independen)

Cek panjang (Python `len`):

| Balasan | Panjang | Catatan |
|---|---|---|
| SEBELUM (satu draf) | 924 karakter | Melewati batas aman 500 karakter yang dipakai skill untuk balasan marketplace (batas resmi Shopee belum diverifikasi penguji — anggap risiko terpotong/ditolak, bukan kesalahan pasti). |
| SESUDAH utama | 469 karakter | Sesuai klaim "469" ✅ |
| SESUDAH alternatif | 308 karakter | Sesuai klaim "308" ✅ |

Kesalahan fakta/etika:
- SEBELUM mengarang fakta yang tidak diberikan pemilik: "proses packing & kirim dari gudang kami sudah sesuai SLA", "pencahayaan studio"; dan kalimat "bukan karena produknya tidak sesuai" terdengar membantah pembeli di depan umum.
- SESUDAH menulis janji "masukan ini kami pakai untuk perbaiki hasil fotonya" dan "sedang membenahi respon tim CS" — tetapi agent sendiri menandai di catatan pemilik agar tidak jadi janji kosong ✅.

## Nilai

| | SEBELUM | SESUDAH |
|---|---|---|
| Skor (1–10) | 6.0 | 8.5 |

- **SEBELUM 6/10** — sopan dan menjelaskan duduk perkara, tapi terlalu panjang untuk kolom balasan marketplace, mengarang klaim "sesuai SLA/studio", dan nadanya defensif ("bukan karena produknya tidak sesuai") — berisiko terlihat buruk oleh calon pembeli lain.
- **SESUDAH 8,5/10** — skill terpakai (`read` + `exec` `cek_balasan.py`, hasil cek ditampilkan). Dapat 2 versi publik dengan panjang tercek + pesan chat pribadi untuk eskalasi (minta no. pesanan & foto), tidak defensif tapi tetap menjelaskan ekspedisi & cahaya foto, ada catatan risiko janji. Mode Copilot dipatuhi (draf, pemilik yang memposting).

Kriteria: ketepatan, langsung siap pakai, kepatuhan aturan Indonesia, keamanan/privasi, kejelasan untuk awam.
