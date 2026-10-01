# Uji ulang ke-3 — Kantor 04 · Umur piutang dari CSV + draf tagihan (tagih-piutang 1.0.4)

Tanggal: 2026-10-01 (Asia/Jakarta) · Penguji independen ke-3 (bukan pembuat skill). OpenClaw asli lokal (`openclaw agent --local`), model router Komunitech (`ninerouter/komunitech`, jawaban `claude-sonnet-5`), sama dengan bot member. Home `sol3-kantor-manajemen` direset (`reset3-*.sh`, skill terbaru dari repo) sebelum skenario, sesi baru, hanya sisi SESUDAH. Pesan member (dan jawaban lanjutan) **sama persis** dengan uji pertama, file `piutang.csv` identik (kolom `no_faktur,pelanggan,tanggal_faktur,jatuh_tempo,nilai_faktur,sudah_dibayar,no_wa`). Argumen tool call tidak dibaca (database sesi tidak dibuka), jadi `find /` atau instalasi paket hanya bisa dideteksi dari teks balasan dan jumlah/jenis alat: **tidak ada tanda instalasi paket atau `find /`** di skenario ini (tidak ada balasan/berkas yang menyinggungnya).

## Pesan member giliran 1 (sama persis)

> ini daftar piutang kami per hari ini (file piutang.csv). mana aja yg udah telat bayar & total berapa? terus bikinin pesan WA buat nagih yg paling parah ya, sopan tapi tegas

## Balasan SESUDAH (ulang ke-3) — giliran 1 (utuh)

_alat: `exec, read` · 7 panggilan, 0 gagal · durasi 75 dtk_

> Sudah saya hitung pakai script `tagih-piutang` (bukan tebak-tebak manual) dari `piutang.csv`, per hari ini 1 Oktober 2026.
>
> ## Ringkasan Piutang
>
> **Total piutang: Rp 279.800.000** (7 invoice)
> **Sudah lewat jatuh tempo: Rp 221.800.000** (5 invoice)
>
> | Pelanggan | Invoice | Sisa | Jatuh tempo | Telat | Status |
> |---|---|---|---|---|---|
> | Toko Bangunan Sentosa | INV-2606-030 | Rp 5.000.000 | 20 Jul | 73 hari | Tahap 5 (resmi) |
> | CV Maju Bersama | INV-2607-011 | Rp 28.500.000 | 9 Agt | 53 hari | Tahap 5 (resmi) |
> | **PT Sinar Jaya Logistik** | **INV-2607-019** | **Rp 126.750.000** | **21 Agt** | **41 hari** | **Tahap 5 (resmi)** |
> | Toko Bangunan Sentosa | INV-2608-004 | Rp 17.250.000 | 4 Sep | 27 hari | Tahap 4 (tegas-sopan) |
> | PT Sinar Jaya Logistik | INV-2609-021 | Rp 44.300.000 | 25 Sep | 6 hari | Tahap 3 (konfirmasi) |
>
> Belum jatuh tempo (jangan ditagih dulu): UD Berkah Tani Rp 22.400.000 (JT 2 Okt) dan CV Maju Bersama Rp 35.600.000 (JT 8 Okt).
>
> **Yang paling parah: PT Sinar Jaya Logistik.** Bukan yang paling lama telat (Toko Bangunan Sentosa 73 hari), tapi nominalnya jauh paling besar — satu invoice saja Rp 126.750.000 (lebih dari separuh total yang telat), dan ditambah invoice satunya lagi Rp 44.300.000, **total tunggakan mereka Rp 171.050.000**. Belum pernah diingatkan sama sekali, jadi menurut aturan skill mulai dari Tahap 5 (pemberitahuan resmi), bukan langsung somasi.
>
> Karena belum pernah ditagih, jalur utamanya surat/email resmi + WA pengantar singkat (bukan WA panjang) — ikut aturan skill biar nggak terkesan "lompat galak" untuk tagihan pertama. Ini saya siapkan dua-duanya, fokus di invoice terbesar (INV-2607-019):
>
> ---
>
> ### Pesan WA Pengantar (kirim sekarang)
>
> > Selamat siang, Bapak/Ibu PIC PT Sinar Jaya Logistik 🙏
> > Kami ingin menyampaikan bahwa Invoice INV-2607-019 senilai Rp 126.750.000 (jatuh tempo 21 Agustus 2026) hingga hari ini belum kami terima pembayarannya, sudah lewat 41 hari dari jatuh tempo. Kami lampirkan surat pemberitahuan resminya di pesan ini.
> > Mohon konfirmasi rencana pembayarannya ya, Pak/Bu. Jika ada kendala, kami terbuka membicarakan jadwal pembayaran. Terima kasih.
> > _(Catatan: ada lagi Invoice INV-2609-021 Rp 44.300.000 yang juga sudah lewat jatuh tempo 6 hari — boleh sekalian ditanyakan dalam pesan yang sama kalau Bapak/Ibu mau.)_
>
> ### Surat Pemberitahuan Resmi (lampirkan PDF/email)
>
> > **Perihal: Pemberitahuan Tagihan Lewat Jatuh Tempo – Invoice INV-2607-019**
> >
> > Dengan hormat,
> > Bersama ini kami sampaikan bahwa Invoice INV-2607-019 tertanggal 22 Juli 2026 senilai Rp 126.750.000 telah jatuh tempo pada 21 Agustus 2026, dan hingga 1 Oktober 2026 belum ada pembayaran yang kami terima (41 hari keterlambatan).
> >
> > Kami mohon pembayaran dapat diselesaikan paling lambat **8 Oktober 2026** ke rekening [Bank – No. Rek – a.n. Usaha Anda]. Apabila diperlukan, kami bersedia membahas jadwal pembayaran bertahap yang dituangkan secara tertulis.
> >
> > Atas perhatian dan kerja samanya, kami ucapkan terima kasih.
> >
> > Hormat kami,
> > [Nama Anda] – [Jabatan/Usaha]
>
> ---
>
> ### Tahap berikutnya
> Kalau sampai 8 Oktober 2026 belum ada respons/pembayaran, naik ke pengingat ke-2; kalau 7 hari lagi tetap diam, baru layak ke Tahap 6 (surat teguran/somasi).
>
> ### Saran tindakan
> - Isi `[rekening]` dan `[Nama/Jabatan]` sebelum kirim.
> - Simpan bukti kirim (screenshot WA, email terkirim) untuk jaga-jaga kalau perlu eskalasi nanti.
> - Toko Bangunan Sentosa (73 hari, Rp 5jt) dan CV Maju Bersama (53 hari, Rp 28,5jt) juga sudah layak Tahap 5 — bilang aja kalau mau saya buatkan pesannya juga.
> - Toko Bangunan Sentosa INV-2608-004 (27 hari) masih Tahap 4 — cukup WA tegas minta tanggal pasti, belum perlu surat resmi.
>
> **Catatan hukum:** Ini bukan nasihat hukum. Dasar umum: KUHPerdata (wanprestasi/pemberitahuan tertulis sebelum somasi) — per 1 Oktober 2026. Tidak ada denda keterlambatan saya cantumkan karena tidak ada kesepakatan tertulis yang Anda sebutkan — kalau memang ada klausul denda di PO/kontrak, kasih tahu saya, nanti saya hitungkan ulang.

## Cacat lama — hilang?

Uji pertama: [04-piutang-telat-dan-draf-tagihan.md](04-piutang-telat-dan-draf-tagihan.md).

| Cacat dilaporkan | Hilang? | Bukti |
|---|---|---|
| `--file piutang.csv` gagal `kolom wajib tidak ada: ['nominal']`, agent menulis CSV konversi | **Ya** | 7 panggilan, **0 gagal**, tidak ada file konversi di workspace. Penguji menjalankan script repo pada CSV yang sama: `Kolom dipakai: pelanggan=pelanggan, no_invoice=no_faktur, nominal=nilai_faktur, jatuh_tempo=jatuh_tempo, dibayar=sudah_dibayar`, total Rp279.800.000, telat Rp221.800.000 — identik dengan balasan. |
| `find /` mencari folder script | **Tidak terdeteksi** | Argumen alat tidak bisa dibaca; tidak ada tanda di balasan. Tidak bisa dipastikan 100%. |
| Pesan tahap 5 dibuat untuk WA | **Ya** | *"jalur utamanya surat/email resmi + WA pengantar singkat (bukan WA panjang)"* — ada WA pengantar + surat resmi. |

## Verifikasi angka (Python penguji)

Per 1 Okt 2026 (Python): INV-2606-030 Rp5.000.000 (73 hr), INV-2607-011 Rp28.500.000 (53), INV-2607-019 Rp126.750.000 (41), INV-2608-004 Rp17.250.000 (27), INV-2609-021 Rp44.300.000 (6). **Total telat Rp221.800.000 ✓**, total piutang Rp279.800.000 (7 faktur bersisa) ✓, Sinar Jaya Rp171.050.000 ✓, belum jatuh tempo UD Berkah Tani (2 Okt) & CV Maju Bersama (8 Okt) ✓, tenggat 8 Okt = Kamis ✓. Salah sebut "invoice terbesar" di uji pertama tidak muncul lagi.

## Regresi / temuan baru

- **Klaim lampiran:** WA pengantar berbunyi *"Kami lampirkan surat pemberitahuan resminya di pesan ini"* dan judul *"Surat Pemberitahuan Resmi (lampirkan PDF/email)"*, padahal skill tidak membuat PDF/file. Tidak salah bila member yang melampirkan, tetapi tidak ada catatan "surat ini perlu Anda simpan/kirim sebagai PDF dulu" (pola yang sama dengan cacat `surat-penawaran-harga` 1.0.2).
- UD Berkah Tani (jatuh tempo besok): script menyarankan *"Tahap 1 – pengingat halus H-1"*, balasan menulis *"jangan ditagih dulu"*. Kecil.
- Catatan miring untuk pemilik ditaruh **di dalam** blok kutipan WA ("_(Catatan: ada lagi Invoice INV-2609-021 …)_") — bisa ikut tersalin ke pelanggan.
- Kalimat tegas "saya tidak mengirim apa pun" dari uji pertama tidak muncul lagi; tetapi juga tidak ada tawaran mengirim. Aman.

## Nilai

| | Sesudah lama (uji pertama) | Sesudah baru (ulang ke-3) |
|---|---|---|
| Skor | 8.5 | **9** |

Cacat utama (kolom CSV umum ditolak) hilang total: file langsung terbaca, rekap memuat total telat, tahap 5 kini surat + WA pengantar. Minus: kalimat "kami lampirkan" tanpa catatan bahwa file/PDF harus dibuat member, satu ketidakcocokan kecil dengan script (H-1). **LULUS uji ulang ke-3.**
