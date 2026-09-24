# Contoh 01 — Grup Renovasi Toko (Android, 24 jam, DP & komplain)

## Skenario
S1 (normal). Pengguna adalah Pak Nanda, pemilik toko yang sedang renovasi, tergabung di grup WA
"Renovasi Toko Nanda" bersama kontraktor, admin, tukang, dan supplier. Ekspor Android format
`DD/MM/YY, HH.MM - Nama: pesan`, 24 jam, 2 hari (12–13 Sep 2026), 99 baris (97 obrolan/media/dihapus
+ 2 pesan sistem), berisi tenggat, DP, pertanyaan @mention ke pemilik, keputusan, komplain
tetangga, stiker, media, dan pesan yang dihapus. File uji: `input/renovasi-toko.txt`
(dibuat khusus untuk pengujian ini, data fiktif).

## Input pengguna (persis)
> Ringkas grup Renovasi Toko Nanda ini, aku Pak Nanda, tolong yang perlu aku tanggapi apa aja.
> (melampirkan file `renovasi-toko.txt`)

## Langkah yang dijalankan
```
python3 scripts/parse_ekspor_wa.py "renovasi-toko.txt" --indent 0
```
Hasil: `format_terdeteksi: android`, `urutan_tanggal: d/m`, `catatan: []` (tidak ambigu), total 99
pesan (97 obrolan + 2 sistem), 2 hari. Statistik: Budi 25, Dimas 24, Sari 23, Fajar 12, Pak Nanda 7,
Ridho 6 pesan; jam paling ramai 08.00–09.00; 4 media/stiker; 2 pesan dihapus.

## Output

```
📋 RINGKASAN GRUP: Renovasi Toko Nanda
Rentang: 12–13 Sep 2026 · 99 pesan (dari 6 orang, termasuk 2 pesan sistem: penambahan & gabungnya
anggota baru)

── 13 Sep 2026 (36 pesan) ──

🔴 PERLU PERHATIAN (5)
1. [09.10] Dimas: "@Pak Nanda listrik di area belakang kok mati dari tadi ya, ada masalah kah?
   tukang jadi kesulitan pakai bor"
   → sudah dijawab Anda (10.00): pakai genset kecil sementara. Ternyata listrik nyala lagi 13.00
   (dari PLN, mati total 1 jam) — tidak perlu tindakan lanjutan.
2. [14.30] Dimas: "untuk plafon, jadi pakai gypsum atau PVC pak? soalnya harga beda jauh, gypsum
   Rp 95.000/m2, PVC Rp 65.000/m2"
   → sudah dijawab Anda (15.00): pakai PVC. Tindak lanjut: Fajar siapkan PVC besok pagi.
3. [17.00] Sari: "pak, ada komplain dari tetangga sebelah soal debu bongkaran kena ke teras
   mereka, minta tolong disapu tiap sore"
   → sudah dijawab Anda (17.30): minta maaf ke tetangga + aturan baru sapu area tiap sore mulai
   besok.
4. ⚠️ [12.30] Fajar menghapus satu pesan — isi tidak diketahui, tidak ada obrolan susulan yang
   menjelaskan konteksnya. Perlu dicek langsung ke Fajar bila relevan.
5. [10.30] Fajar: "semen sisa 5 sak masih ada gak? kalau kurang saya bisa anter tambahan besok"
   → dijawab Budi (10.35): masih cukup. Info, tidak perlu tindakan Anda.

📌 DAFTAR TINDAKAN
| Tugas | PIC | Tenggat |
|---|---|---|
| Siapkan & kirim PVC plafon | Fajar | Besok pagi (14 Sep) |
| Sapu area sekitar toko | Dimas | Tiap sore mulai besok (14 Sep) |
| Finishing plafon | Budi | Besok (14 Sep), setelah atap sisi kiri kelar |

🔵 INFO (6)
- [08.10] Sari mengirim media (progress pagi)
- [13.00] Dimas: listrik sudah nyala lagi, dari PLN mati total 1 jam
- [14.00] Budi: atap sisi kiri kelar semua, tinggal finishing plafon
- [16.00] Ridho: selesai bersih-bersih area depan
- [09.00] Ridho gabung ke lokasi dan mulai bantu bersih-bersih
- [18.00] Sari: besok lanjut jam 8 seperti biasa

💬 OBROLAN
Sekitar 21 pesan obrolan/sapaan/candaan (mis. "pagi semua", "siap pak", emoji 👍)

📎 Lampiran/media: 1 · 🗑️ Pesan dihapus: 1
⏰ Jam paling ramai (hari ini): sekitar pagi–siang, tersebar merata

── 12 Sep 2026 (63 pesan) ──

🔴 PERLU PERHATIAN (6)
1. [11.00] Sari: "@Pak Nanda invoice semen dan keramik dari Fajar totalnya Rp 12.500.000 udah
   termasuk ongkir, boleh langsung dibayar?"
   → dijawab Anda (13.00): transfer DP 50% dulu, Rp 6.250.000, sisanya saat barang sampai lengkap.
   Sudah dieksekusi Sari (15.30, DP terkirim).
2. [14.00] Dimas: "pak lantai yang di deket kasir retak lagi setelah dibongkar, kayaknya perlu
   di re-cor ulang, ini nambah biaya sekitar Rp 800.000 boleh lanjut atau gimana pak?"
   → dijawab Anda (15.00): lanjut re-cor. Dikerjakan Dimas besok pagi (13 Sep).
3. [17.30] Sari: "@Pak Nanda sisa pembayaran ke Fajar Rp 6.250.000, ditransfer sekarang atau
   nanti pas toko buka Senin pak?"
   → ⚠️ belum ada jawaban dari Anda di file ini — yang menjawab "gpp kalau mau nyusul senin juga
   aman" (17.35) adalah Fajar sendiri, bukan keputusan Anda. Perlu ditegaskan kapan sisa
   Rp 6.250.000 ini benar-benar ditransfer.
4. [09.00] Budi: "@Pak Nanda kalau atap galvalum jadi pakai yang warna biru atau abu-abu pak?
   tukang mau mulai pasang siang ini"
   → sudah dijawab Anda (10.00): abu-abu.
5. [10.05] Sari: "@Pak Nanda budget material minggu ini sekitar berapa pak, biar saya siapkan
   kas" → ⚠️ tidak terlihat ada jawaban langsung dari Anda di sisa pesan hari ini; mungkin
   dijawab di luar chat (telepon/DM). Perlu dikonfirmasi ke Sari.
6. ⚠️ [13.10] Sari menghapus satu pesan pukul 13.10, lalu 13.15 menulis "maksudku nanti saya
   kabari kalau sudah transfer" — isi pesan yang dihapus tidak diketahui, tapi konteks susulan
   menunjukkan kemungkinan salah kirim terkait transfer DP.

📌 DAFTAR TINDAKAN
| Tugas | PIC | Tenggat |
|---|---|---|
| Transfer DP semen & keramik Rp 6.250.000 | Sari | Sore 12 Sep (sudah dilakukan 15.30) |
| Re-cor ulang lantai dekat kasir (+Rp 800.000) | Dimas | Besok pagi (13 Sep) |
| Transfer sisa pembayaran Rp 6.250.000 ke Fajar | Sari | ⚠️ belum jelas — "sekarang atau Senin" belum dipastikan Pak Nanda |
| Sampaikan warna atap (abu-abu) ke tukang | Budi | Selesai (10.02) |

🔵 INFO (7)
- [08.05] Dimas mengirim media (progress bongkar dinding depan)
- [09.10] Dimas mengirim stiker
- [11.30] Fajar mengirim media (foto invoice)
- [12.10] Sari menambahkan Ridho ke grup (pesan sistem)
- [15.10] Fajar: barang material otw, sampai sekitar jam 4
- [17.00] Fajar: barang sudah sampai semua
- [19.29] Ridho bergabung ke grup lewat tautan undangan (pesan sistem), lalu memperkenalkan diri

💬 OBROLAN
Sekitar 26 pesan obrolan/candaan/sapaan (mis. "siap bu", "wkwkwk", stiker, emoji 👍😂)

📎 Lampiran/media: 3 · 🗑️ Pesan dihapus: 1
⏰ Jam paling ramai: 08.00–09.00

Asumsi: karena grup ini berisi 2 hari data, ringkasan dibagi per hari (hari terbaru di atas)
sesuai jumlah pesan yang cukup ramai. Tidak ada rentang waktu yang diminta pengguna, jadi seluruh
isi file diringkas.
```

## Catatan penguji
- **Akurasi:** seluruh kutipan, jam, dan nominal di atas dicek satu-satu terhadap `out/a.json`
  (hasil parser) dan file sumber `input/renovasi-toko.txt` — cocok semua, tidak ada yang dikarang.
- **Recall vs kunci jawaban (`kunci/kunci-a.md`):** dari 8 item kunci, 8 tercakup (100%). Item
  "sisa pembayaran Rp 6.250.000" dan "budget material minggu ini" secara jujur ditandai ⚠️ karena
  di file memang tidak ada jawaban eksplisit dari Pak Nanda — ini justru contoh bagus skill
  **tidak mengarang** jawaban yang tidak ada, sesuai prinsip "setia pada isi asli".
- **Presisi:** tidak ada butir Perlu Perhatian yang mengada-ada; semua berbasis pertanyaan/
  keputusan/uang/komplain yang benar-benar ada di teks.
- **Kekurangan kecil:** SKILL.md tidak eksplisit menjelaskan bagaimana menyajikan item yang
  "sudah terjawab di file yang sama" — agent (saya) memilih tetap menampilkannya di Perlu
  Perhatian dengan keterangan "sudah dijawab" agar pengguna tetap bisa audit keputusan, tapi
  pembeli awam yang buru-buru bisa jadi merasa daftar Perlu Perhatian "terlalu panjang" walau
  separuhnya sudah selesai. **Saran perbaikan:** tambahkan sub-kategori "✅ sudah dijawab" vs
  "❗ masih menunggu Anda" di dalam blok Perlu Perhatian, atau pisahkan jadi dua daftar, supaya
  pengguna awam langsung tahu prioritas.
