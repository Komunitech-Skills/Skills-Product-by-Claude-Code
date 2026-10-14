# Uji cepat 1.0.4: data mingguan dibaca otomatis (bukan uji penuh)

- **Tanggal:** 2026-10-14
- **Penguji:** agent penguji independen Komunitech (bukan pembuat)
- **Latar:** di bot Telegram asli, 1.0.3 dijalankan tanpa `--data-per minggu` pada tabel mingguan skenario 2, sehingga total mingguan terbaca harian (pesan 75/115/105; seharusnya 47/82/75). Versi 1.0.4 mendeteksi granularitas otomatis, mencetak "Data dibaca sebagai …", dan berhenti (kode keluar 3) bila ambigu.
- **Cakupan:** (1) script langsung; (2) satu jalan sisi DENGAN skill, konteks kanal Telegram (`openclaw agent --local --channel telegram`, tanpa mengirim), OpenClaw 2026.10.2, model `claude-sonnet-5`, home baru berisi hanya skill 1.0.4, pesan skenario 2 yang sama persis dengan putaran sebelumnya. Uji regresi: `tests/uji_regresi.py` **180 cek OK**.

## 1. Script langsung

| Uji | Hasil | Sesuai? |
|---|---|---|
| Tabel mingguan apa adanya dari chat (judul "Minggu", tanggal "17 Agu" tanpa tahun), **tanpa** `--data-per` | "Data dibaca sebagai total per MINGGU (8 minggu, 17 Agu–11 Okt 2026) (otomatis: judul kolom 'Minggu'; jarak antar tanggal 7 hari)"; Beras 47, Minyak 82 (naik 27 %), Gula 75 (stabil, pesan 15 Okt); Telur ROP 28/target 139; Mie ROP 5/target 20 | Ya |
| Tabel yang sama **dengan** `--data-per minggu` | Angka identik (47/82/75, Gula stabil) | Ya |
| Tabel panjang `tanggal;nama_barang;qty` bertanggal ISO, jarak 7 hari, tanpa flag | Terbaca per minggu, angka identik | Ya |
| Data harian skenario 1 (777 baris), tanpa flag | "Data dibaca sebagai penjualan per HARI (90 hari, 16 Jul–13 Okt 2026) (otomatis: tanggal berurutan, jarak 1 hari)"; pesan sekarang **Rp10.879.000**, 1–7 hari **Rp3.351.000**, 3 barang akan kosong; hitung ulang independen **182/182 cocok** (bug presisi 1.0.1 sudah hilang: Dot habis 140 hari, 3 Mar 2027) | Ya |
| Ambigu: 2 baris (1 & 5 Okt) | Kode keluar **3**: "granularitas tidak jelas … jarak 4 hari", `perlu_tanya_pengguna: true`, saran bertanya sekali; tidak menghitung | Ya |
| Ambigu: 2 baris tanpa tahun (3 & 10 Okt, jarak 7) | Kode keluar **3**, tidak menghitung (konservatif: 2 titik belum cukup untuk menyimpulkan mingguan) | Ya |

Hitung ulang independen skenario 2 (μ = total ÷ 56; sd harian = sd laju mingguan × √7; tren 4 vs 4 minggu; batas 0,5–2×): Beras 3,14/hari, ROP 12, target 56 → 47; Minyak 165 ÷ 28 = 5,89 vs 130 ÷ 28 = 4,64 (naik 27 %) → ROP 25, target 107 → 82; Gula stabil 5,68, ROP 19, target 99, ROP tercapai 1 hari lagi → 99 − (30 − 5,68) = 74,7 → 75. Semua cocok.

## 2. Jalan sisi DENGAN skill, konteks Telegram

**Pesan (sama dengan skenario 2):**

> Ini penjualan warung sembako saya per minggu, 8 minggu terakhir (minggu mulai hari Senin):
>
> Minggu | Beras 5 kg (karung) | Minyak Goreng 2 L | Gula Pasir 1 kg | Telur (kg) | Mie Instan (dus)
> 17 Agu | 20 | 30 | 40 | 55 | 6
> 24 Agu | 22 | 32 | 38 | 50 | 5
> 31 Agu | 19 | 35 | 41 | 58 | 7
> 7 Sep | 23 | 33 | 39 | 52 | 6
> 14 Sep | 21 | 38 | 42 | 60 | 8
> 21 Sep | 24 | 40 | 40 | 57 | 6
> 28 Sep | 22 | 42 | 37 | 54 | 7
> 5 Okt | 25 | 45 | 41 | 59 | 9
>
> Stok sekarang: beras 9 karung, minyak 25, gula 30. Telur sama mie belum sempat saya hitung. Grosir langganan antar 2-3 hari. Saya harus belanja apa dan berapa?

**Yang dijalankan agent:** membaca SKILL.md, lalu `rencana_restok.py --data "Minggu;Beras 5 kg (karung);…" --barang-data … --lead-time 2-3 --hari-ini 2026-10-14 --format teks`: tabel ditempel apa adanya, **tanpa** `--data-per`, granularitas terdeteksi otomatis. 42 detik, tanpa `find /`.

**Keluaran:**

> Rencana restok per 14 Okt 2026 (data 17 Agu–11 Okt 2026, 8 minggu)
> Data dibaca sebagai total per MINGGU.
>
> Beras mau kosong sebelum kiriman sampai, minyak & gula perlu dipesan sekarang/besok, telur & mie belum bisa dihitung karena stoknya belum saya tahu.
>
> ⚠️ AKAN KOSONG SEBELUM BARANG DATANG
> • Beras 5 kg: stok 9, laku ±3,14/hari (stabil) → habis ±2 hari (16 Okt), kiriman 3 hari → kosong ±1 hari. Pilihan: pesan hari ini, minta pemasok kirim lebih cepat/ambil sebagian di pemasok terdekat, atau terima kosong ±1 hari.
>
> PESAN SEKARANG
> • Beras 5 kg: stok 9, laku ±3,14/hari (stabil) → pesan 47 karung [stok target 56 − stok 9 = 47]
> • Minyak Goreng 2 L: stok 25, laku ±5,89/hari (naik 27%) → pesan 82 pcs [stok target 107 − stok 25 = 82]
>
> PESAN BESOK (15 Okt)
> • Gula Pasir 1 kg: stok 30, laku ±5,68/hari (stabil), habis ±5 hari (19 Okt) → pesan 75 pcs [stok target 99 − perkiraan stok saat pesan 24,3 = 74,7 → 75]
>
> BELUM BISA DIHITUNG (stok belum diketahui)
> • Telur (kg): laku ±7,95/hari (stabil). Pesan bila stok ≤ 28; jumlah = 139 − stok sekarang.
> • Mie Instan (dus): laku ±1,07/hari (naik 25%). Pesan bila stok ≤ 5; jumlah = 20 − stok sekarang.
>
> Daftar pesanan (siap kirim ke grosir)
> Hari ini: Beras 47 karung, Minyak Goreng 82 pcs, total [isian: harga beli belum ada]
> Besok (~15 Okt): Gula Pasir 75 pcs, total [isian: harga beli belum ada]
>
> Draf WA #1 (pesan hari ini):
> Halo [isian: nama pemasok], saya [isian: nama Anda] dari [isian: nama toko]. Mau pesan:
> 1. Beras 5 kg: 47 karung
> 2. Minyak Goreng 2 L: 82 pcs
> Mohon konfirmasi stok, total harga, dan tanggal kirim. Terima kasih.
>
> Draf WA #2 (rencana ~15 Okt):
> Halo [isian: nama pemasok], saya [isian: nama Anda] dari [isian: nama toko]. Rencana pesan sekitar 15 Okt:
> 1. Gula Pasir 1 kg: 75 pcs
> Mohon konfirmasi stok, total harga, dan tanggal kirim. Terima kasih.
>
> Asumsi: lead time grosir 3 hari (dari info 2-3 hari Anda), tingkat layanan 95%, stok dijaga cukup 14 hari setelah barang datang, tidak ada faktor musim tambahan. Tren: minyak goreng naik 27%, mie instan naik 25% (4 minggu terakhir vs sebelumnya); beras, gula, telur stabil.
>
> Mau saya hitung pas, tolong jawab:
> 1. Stok telur dan mie instan sekarang berapa?
> 2. Harga beli terakhir beras, minyak, gula per satuan berapa?
> 3. Ada barang yang sudah dipesan ke grosir tapi belum sampai?
>
> Catatan: ini perkiraan dari pola penjualan sebelumnya, bukan jaminan — cocokkan dengan stok fisik dan kesanggupan pemasok sebelum memesan.

### Verifikasi
- Angka **cocok**: 47 karung / 82 / 75 (rumus "99 − 24,3 = 74,7 → 75" benar), Telur "≤ 28; 139 − stok", Mie "≤ 5; 20 − stok", Beras akan kosong ±1 hari, tren Minyak +27 %, Mie +25 %, Gula/Beras/Telur stabil.
- "Data dibaca sebagai total per MINGGU." disalin (dipendekkan; rentang 8 minggu 17 Agu–11 Okt ada di baris judul).
- Judul waktu nyata: "PESAN SEKARANG" dan "PESAN BESOK (15 Okt)".
- Draf WA: dua, satu per waktu pesan (hari ini; ±15 Okt), ≤ 6 baris, `[isian]` untuk nama.
- Barang tanpa stok tidak dikarang; asumsi + tren per barang; 3 pertanyaan; disclaimer.

### Nilai: 9/10
- (+) Kesalahan 1.0.3 di bot asli (mingguan dibaca harian) tidak muncul; agent tidak menebak flag.
- (−) Minyak tidak diberi "habis ±4 hari (18 Okt)", padahal itu termasuk keluaran minimum per barang; Beras hanya di bagian akan-kosong. Kalimat "Data dibaca sebagai …" dipendekkan. Satuan Minyak/Gula "pcs" (1.0.1 sempat "botol"/"kg").

## Cacat
1. Kecil: hari habis tidak tampil untuk setiap barang yang dipesan (Minyak).
2. Kecil: kalimat "Data dibaca sebagai …" dipendekkan agent; bila ingin utuh, SKILL.md bisa meminta salinan persis termasuk rentang.
3. Catatan risiko (belum diuji): toko yang benar-benar hanya mencatat penjualan tiap 7 hari dalam data harian akan terbaca mingguan; kalimat "Data dibaca sebagai …" yang wajib disalin adalah pengamannya.
