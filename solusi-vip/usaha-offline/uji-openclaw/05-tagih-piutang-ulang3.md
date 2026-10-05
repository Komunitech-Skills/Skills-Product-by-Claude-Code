# Uji ulang ke-3 — Usaha Offline 05 · Tagih piutang laundry tetangga, info kurang (tagih-piutang 1.0.4)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen ke-3 (bukan pembuat skill). OpenClaw asli lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`), sama dengan bot member. Home `sol3-usaha-offline` direset (`reset3-*.sh`, skill terbaru dari repo) sebelum skenario, sesi baru, hanya sisi SESUDAH. Pesan member (dan jawaban lanjutan) **sama persis** dengan uji pertama. Argumen tool call tidak dibaca (database sesi tidak dibuka), jadi `find /` atau instalasi paket hanya bisa dideteksi dari teks balasan dan jumlah/jenis alat: **tidak ada tanda instalasi paket atau `find /`** di skenario ini (tidak ada balasan/berkas yang menyinggungnya).

## Pesan member giliran 1 (sama persis)

> tolong bikinin pesan wa buat nagih pelanggan laundry yg ngutang ya, udh lama ga bayar2

## Pesan member giliran 2 (sama persis)

> Bu Rina, langganan laundry kiloan. Utang Juli 420rb, Agustus 465rb, September 465rb, totalnya 1.350.000. Janji bayar tgl 25 September tapi sampe skrg belum. Udah saya ingetin sekali lisan. Ga ada denda. Orangnya baik, tetangga, jangan sampe tersinggung tapi harus bayar. Laundry saya Laundry Wangi, rek BCA 1234567890 a.n. Siti.

## Balasan SESUDAH (ulang ke-3) — giliran 1 (utuh)

_alat: `read` · 1 panggilan, 0 gagal · durasi 11 dtk_

> Oke, siap bantu bikin pesan tagihan laundry. Supaya nominal & tenggatnya pas, aku butuh beberapa info ini dulu:
>
> 1. **Nama pelanggan** yang ditagih?
> 2. **Total tagihan** (dan sudah ada yang dibayar sebagian atau belum sama sekali)?
> 3. **Tanggal jatuh tempo**-nya kapan (atau sejak kapan mulai ngutang)?
> 4. Sudah pernah diingatkan sebelumnya nggak? Kalau sudah, berapa kali & kapan terakhir?
> 5. Pelanggan ini langganan tetap/kenalan dekat, atau pelanggan biasa (B2B/umum)?
>
> Kalau mau cepat, kasih aja nominal + kira-kira udah berapa lama nunggak, nanti aku pakai asumsi untuk sisanya dan aku tandai di hasil.

## Balasan SESUDAH (ulang ke-3) — giliran 2 (utuh)

_alat: `exec` · 1 panggilan, 0 gagal · durasi 22 dtk_

> ### Ringkasan tagihan
> - Pelanggan: Bu Rina (tetangga, langganan laundry kiloan)
> - Rincian: Juli Rp420.000 + Agustus Rp465.000 + September Rp465.000 = **Rp1.350.000**
> - Jatuh tempo (janji bayar): 25 September 2026 → sudah terlambat **6 hari**
> - Sudah diingatkan: 1x (lisan)
> - Tahap: 3 (lewat jatuh tempo, nada ramah, anggap mungkin lupa)
> - Tidak ada denda
>
> ### Pesan tahap 3 · WA · kirim hari ini (1 Oktober 2026)
>
> > Assalamu'alaikum Bu Rina, saya Siti dari Laundry Wangi 🙏
> >
> > Mau mengingatkan ya Bu, untuk laundry bulan Juli-September:
> > - Juli: Rp420.000
> > - Agustus: Rp465.000
> > - September: Rp465.000
> > Total: **Rp1.350.000**
> >
> > Kemarin Ibu sempat bilang mau transfer tanggal 25 September, tapi sampai sekarang belum masuk ke rekening saya Bu. Mungkin ke-skip atau ada kendala? Kalau sudah transfer, boleh kirim bukti ya biar saya cocokkan.
> >
> > Rekening: BCA 1234567890 a.n. Siti
> >
> > Kalau belum sempat, nggak apa-apa Bu, kabari saja kira-kira bisa transfer kapan. Makasih banyak ya Bu 🙏
>
> ### Tahap berikutnya (jika belum dibayar)
> - Tenggat bayar di pesan ini: Kamis, 15 Oktober 2026 (14 hari dari 1 Oktober). Kalau sampai tanggal itu belum ada pembayaran atau kabar, pada Jumat, 16 Oktober ajak Bu Rina ngobrol langsung dulu (bukan pesan tertulis lagi) — baru kalau tetap belum ada kabar, kirim tahap 4 tapi tetap dengan nada kekeluargaan.
>
> ### Saran tindakan
> - Karena ini tetangga/hubungan dekat, jeda antar-pengingat dibuat lebih longgar (14 hari), dan disarankan ngobrol langsung sebelum naik ke pesan yang lebih tegas.
> - Simpan bukti chat ini sebagai catatan kalau suatu saat perlu diingat lagi.
> - Kalau Bu Rina kesulitan bayar sekaligus, boleh tawarkan cicilan (misal 2x) secara lisan dulu — tidak perlu surat formal untuk hubungan sekedekat ini.
> - Laundry tetap bisa dilanjutkan seperti biasa; tidak perlu dihentikan untuk nominal sekecil ini kecuali makin menumpuk.
>
> ### Catatan hukum
> Bukan nasihat hukum. Untuk tagihan sekecil ini antar tetangga, cukup diselesaikan secara kekeluargaan — tidak perlu sampai somasi atau jalur hukum.
>
> Pesan di atas tinggal kamu copy dan kirim sendiri ya ke Bu Rina via WA.

## Cacat lama — hilang?

Uji pertama: [05-tagih-piutang-info-kurang.md](05-tagih-piutang-info-kurang.md) (belum pernah diuji ulang).

| Cacat dilaporkan | Hilang? | Bukti (kutipan) |
|---|---|---|
| Pesan tidak memuat rincian per bulan | **Ya** | Pesan WA: *"- Juli: Rp420.000 - Agustus: Rp465.000 - September: Rp465.000 Total: Rp1.350.000"*. |
| Eskalasi "tahap 4 ±3 Oktober" (2 hari) terlalu cepat untuk tetangga | **Ya** | *"Tenggat … Kamis, 15 Oktober 2026 (14 hari dari 1 Oktober). Kalau sampai tanggal itu belum ada pembayaran atau kabar, pada Jumat, 16 Oktober ajak Bu Rina ngobrol langsung dulu (bukan pesan tertulis lagi) — baru kalau tetap belum ada kabar, kirim tahap 4 tapi tetap dengan nada kekeluargaan."* |

## Verifikasi angka (Python penguji)

Python: 420.000 + 465.000 + 465.000 = 1.350.000 ✓; 25 Sep → 1 Okt 2026 = 6 hari ✓; 1 Okt + 14 hari = Kamis 15 Okt ✓, 16 Okt = Jumat ✓. Giliran 1 bertanya sekali (5 pertanyaan + opsi cepat), kini juga menanyakan hubungan (langganan/kenalan dekat) — pas untuk opsi `--hubungan dekat`.

## Regresi / temuan baru

- Kecil: *"Tenggat bayar di pesan ini: 15 Oktober"* padahal teks WA sendiri tidak menyebut tenggat (hanya "kabari saja kira-kira bisa transfer kapan") — tenggat itu sebenarnya jadwal internal pemilik.
- Pembuka *"Assalamu'alaikum … saya Siti dari Laundry Wangi"* — salam keagamaan dan nama pengirim diasumsikan (nama "Siti" dari rekening). Wajar, tetapi tidak disebut sebagai asumsi.
- Tetap tegas: *"Pesan di atas tinggal kamu copy dan kirim sendiri ya ke Bu Rina via WA."* Tidak ada tawaran kirim otomatis.

## Nilai

| | Sesudah lama | Sesudah baru (ulang ke-3) |
|---|---|---|
| Skor | 8 | **9** |

Kedua cacat hilang; jeda 14 hari + "ngobrol langsung dulu" tepat untuk tetangga; rincian bulanan masuk ke pesan; angka benar. Minus kecil: kata "tenggat di pesan ini" tidak cocok dengan isi pesan. **LULUS uji ulang ke-3.**
