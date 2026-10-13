# Uji OpenClaw SEBELUM vs SESUDAH — ringkas-grup-wa

Sumber: `solusi-vip/kantor-manajemen/UJI-OPENCLAW.md` (rincian: `solusi-vip/kantor-manajemen/uji-openclaw/02-ringkas-grup-wa-gudang.md` dan `02-ringkas-grup-wa-ulang3.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.4); uji ulang ke-3 = 1.0.4 (versi katalog saat ini 1.0.5). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill Kantor & Manajemen. Kedua home dibuat ulang bersih sebelum skenario; file ekspor chat fiktif (22 pesan, 24-26 Sep 2026, 5 orang) identik di kedua sisi.
- Pesan member: "saya baru ekspor chat grup gudang, filenya chat-grup-gudang.txt. tolong ringkas dong, apa aja yg perlu saya tanggapi? saya direkturnya".
- Fakta dicek penguji terhadap file (22 pesan, 5 pengirim, 7 pesan obrolan, jam ramai, ban Rp1.850.000, kekurangan palet 48).

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang ke-3, v1.0.4) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Ringkas ekspor chat grup WA gudang untuk direktur | 7,5 | 8 | 8,5 | Tanpa skill ringkas dan benar serta satu-satunya yang menandai tenggat 29-30/9 sudah lewat, tetapi tanpa kutipan dan tabel; dengan skill ada kutipan asli bertanggal, tabel siapa-apa-tenggat, dan butir tanpa PIC ditandai (setelah revisi 1.0.4 tiap butir juga punya status LEWAT TENGGAT bertanggal). |
| | **Rata-rata** (satu skenario) | **7,5** | **8** | **8,5** | |

## Verdik
**LULUS uji ulang ke-3.** Pada uji pertama sumber menulis: "Selisih kecil, jangan dijual sebagai pembeda besar."

## Catatan jujur
- Selisih kecil: 0,5 pada uji pertama dan 1,0 jika uji ulang dibandingkan dengan sisi tanpa skill uji pertama (sisi tanpa skill tidak diulang).
- Cacat uji pertama sisi dengan skill: tenggat 26/9, 29/9, 30/9 tampil tanpa tanda "sudah lewat" dan forklift tertulis "sudah ada rencana" padahal hari uji 1 Okt; sisi tanpa skill justru menandainya. Hilang pada uji ulang ke-3 ("hari ini 01/10/2026", LEWAT TENGGAT dengan jumlah hari).
- Temuan uji ulang ke-3: judul "PERLU PERHATIAN (6)" berisi 5 butir, penutup "Tiga lainnya" menyebut 4 butir, dan pelanggan (Sinar Jaya) disebut "vendor" di penutup. README skill mencatat perbaikan di 1.0.5; tidak ada catatan uji ulang OpenClaw untuk 1.0.5 di sumber.
- Pada uji pertama kedua sisi menjalankan pencarian ke seluruh disk (`find /`) padahal file ada di folder kerja; pada uji ulang ke-3 tidak terdeteksi (argumen alat tidak dibaca, jadi tidak 100% pasti).
- Seluruh angka dan fakta di ringkasan sesuai file; tidak ada fakta karangan di kedua sisi.
