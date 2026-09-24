# Contoh 03 — Grup Alumni Ramai 3 Hari, Rentang "sejak kemarin jam 5 sore"

## Skenario
S3. Grup alumni "Alumni SMA 5 Angkatan 2005" sangat ramai (177 pesan mentah, 3 hari: 21–23 Sep
2026), pengguna Andi (ketua panitia reuni) hanya minta bagian terbaru dengan bahasa relatif.
File: `input/alumni.txt` (fiktif). Dijalankan pada tanggal sistem 24 Sep 2026 tapi disimulasikan
seolah dijalankan malam 23 Sep 2026 (`--sekarang "2026-09-23 20:00"`) supaya "kemarin jam 5 sore"
konsisten dengan desain data uji (22 Sep 17.00).

## Input pengguna (persis)
> Ringkas grup alumni ini sejak kemarin jam 5 sore aja, males scroll dari awal.
> (melampirkan `alumni.txt`)

## Langkah yang dijalankan
```
python3 scripts/parse_ekspor_wa.py "alumni.txt" --sejak "kemarin 17:00" --sekarang "2026-09-23 20:00" --indent 0
```
Hasil: filter berhasil memotong ke `2026-09-22T17:00:00` ke atas → 106 pesan (2 hari: 22 Sep
38 pesan, 23 Sep 68 pesan) dari total 177 pesan mentah di file. `catatan: []` (tidak ada
peringatan format). `rentang_pesan_asli` menunjukkan file sebenarnya mulai 21 Sep 07.06 — jadi
ada pesan lama (21 Sep) yang sengaja tidak diikutkan sesuai permintaan pengguna.

## Output

```
📋 RINGKASAN GRUP: Alumni SMA 5 Angkatan 2005
Rentang yang diringkas: 22 Sep 2026 17.00 – 23 Sep 2026 17.05 (sesuai "sejak kemarin jam 5 sore")
· 106 pesan (dari 20 orang). Catatan: file aslinya berisi pesan sejak 21 Sep 07.06; bagian sebelum
22 Sep 17.00 tidak diikutkan karena permintaan rentang waktu Anda.

── 23 Sep 2026 (68 pesan) ──

🔴 PERLU PERHATIAN (4)
1. [09.00] Yoga: "kak @Andi ada dresscode khusus buat acara reuninya ga?" → dijawab (09.15):
   batik casual, warna bebas asal sopan
2. [09.30] Dian: "kak, aku komplain nih, kemarin transfer kontribusi tapi di form status masih
   'belum bayar', udah aku screenshot buktinya" (+ bukti foto 09.31) → **komplain uang, perlu
   ditindaklanjuti** — dijawab (09.35): kemungkinan panitia belum update manual, akan dicek ke
   bendahara & dikonfirmasi ulang hari itu juga
3. [14.00] Nadia: "kak @Andi ralat dong nama aku di daftar hadir salah tulis jadi 'Nadya',
   harusnya 'Nadia'" → dijawab (14.05): dikoreksi sebelum dicetak
4. [14.30] Hasan: "btw kontribusi kas alumni bulanan juga masih jalan kan? mau transfer
   sekalian" → dijawab Eko (14.35): masih jalan, sama seperti biasa

📌 DAFTAR TINDAKAN
| Tugas | PIC | Tenggat |
|---|---|---|
| Semua peserta transfer kontribusi reuni Rp 350.000/orang | Semua anggota | 5 Oktober 2026 |
| Semua peserta isi form pendaftaran (bit.ly/reuni2005-daftar) | Semua anggota | 1 Oktober 2026 |
| Cek & konfirmasi ulang status pembayaran Dian ke bendahara | Andi/panitia | Hari itu (23 Sep) |
| Koreksi nama Nadia di daftar hadir | Andi | ⚠️ belum ada tenggat pasti, sebelum dicetak |
| Panitia tutup rekap peserta | Panitia | H-3 sebelum acara (≈15 Okt, mengikuti pengumuman 16.45) |

🔵 INFO (5)
- [07.00] Andi: reminder deadline transfer kontribusi (5 Okt) & form (1 Okt)
- [13.00] Eko: parkiran hotel terbatas, disarankan online transport/carpool
- [13.05–13.12] Mira menawarkan tumpangan mobil dari arah Kelapa Gading, diambil Fajri
- [16.45] Andi: H-1 minggu reuni, panitia akan tutup rekap H-3 sebelum acara
- Media: 1 stiker (07.22 Rio), 1 stiker (10.27 Sinta), 1 stiker (15.05 Hasan), 1 video (13.30
  Bayu, tanpa penjelasan)

💬 OBROLAN
Sekitar 44 pesan obrolan/sapaan/candaan khas grup alumni ramai (mis. "hai semua apa kabar",
"kangen masa sekolah dulu", emoji 👍😂)

📎 Lampiran/media: 4 · 🗑️ Pesan dihapus: 0
⏰ Jam paling ramai (hari ini): tersebar merata pagi–siang

── 22 Sep 2026, sejak 17.00 (38 pesan) ──

🔴 PERLU PERHATIAN (5)
1. [17.10] Wulan: "@Andi biaya kontribusi per orang berapa ya buat reuni nanti?" → dijawab
   (17.20): Rp 350.000/orang all-in, transfer ke rekening bendahara, tenggat 5 Oktober
2. [17.30] Koko: "kalau bawa pasangan/anak gimana kak, kena biaya juga?" → dijawab (17.40):
   boleh bawa pasangan, biaya sama Rp 350.000/orang tambahan; anak di bawah 5 tahun gratis
3. [18.00] Fajri: "aku sekeluarga daftar 3 orang ya, 2 dewasa 1 anak umur 7 tahun" → dijawab
   (18.05): dihitung 2× Rp 350.000 = Rp 700.000 (anak 7 tahun tetap dihitung karena di atas 5
   tahun)
4. [18.20] Lina: "kak @Andi aku gabisa dateng soalnya lagi di luar kota, boleh titip kontribusi
   aja buat kas alumni?" → dijawab (18.25): boleh, transfer ke rekening sama, keterangan "kas
   alumni"
5. ⚠️ [20.00] Hasan menghapus satu pesan — isi tidak diketahui. Ada obrolan susulan (20.05–20.06)
   yang menyebut "salah kirim", jadi kemungkinan bukan hal penting, tapi tetap dicatat sesuai
   isi aslinya.

Juga tercatat: [20.30] Rio bertanya link form pendaftaran ke @Andi → dijawab (20.35) dengan link
bit.ly/reuni2005-daftar dan tenggat isi 1 Oktober (item ini digabung ke Daftar Tindakan di atas
karena hasilnya sama dengan info form pada 23 Sep).

📌 DAFTAR TINDAKAN (tambahan khusus 22 Sep)
| Tugas | PIC | Tenggat |
|---|---|---|
| Transfer kontribusi 2 orang (Fajri sekeluarga) Rp 700.000 | Fajri | 5 Oktober 2026 |
| Titip kontribusi kas alumni (tidak hadir) | Lina | Belum disebutkan tanggal pasti |

🔵 INFO (3)
- [17.00] Andi: pengumuman reuni akbar 18 Oktober 2026 di Hotel Merdeka, minta konfirmasi
  kehadiran
- [18.46] Tika mengirim poster reuni, minta disebar ke grup angkatan lain
- [18.40] Eko mengingatkan yang belum daftar untuk isi form

💬 OBROLAN
Sekitar 19 pesan obrolan/sapaan (mis. "wah seru, aku ikut", "mantul", "hadir", "gass")

📎 Lampiran/media: 2 (1 stiker, 1 foto poster) · 🗑️ Pesan dihapus: 1
⏰ Jam paling ramai (blok ini): sekitar jam 18.00–19.00 dan 20.00–21.00

Asumsi: "kemarin jam 5 sore" ditafsirkan sebagai 22 Sep 2026 17.00 (hari sebelum tanggal
menjalankan ringkasan ini). Pesan sebelum itu (21 Sep dan 22 Sep pagi–siang) sengaja tidak
diikutkan.
```

## Catatan penguji
- **Filter --sejak "kemarin 17:00" bekerja benar:** dicek di `out/c.json`, `filter.sejak` =
  `2026-09-22T17:00:00`, dan pesan pertama yang lolos memang jam 17.00 tanggal 22 Sep — sama
  persis dengan target di `kunci/kunci-c.md`. Pengumuman penting tanggal 21 Sep ("besok ada
  rapat komite alumni... WAJIB dateng semua pengurus", di luar rentang) **benar-benar tidak
  muncul** di ringkasan — item negatif di kunci jawaban terpenuhi (skill tidak salah
  mengikutkan data di luar rentang).
- **Recall vs kunci jawaban:** 10/10 item Perlu Perhatian dalam rentang tercakup (4 di hari 23,
  5+1 gabungan di 22 Sep — total sama).
- **Presisi:** tidak ada item yang mengada-ada; kutipan & jam dicek cocok dengan `out/c.json`.
- **Cacat ringan:** karena pengguna sekaligus adalah salah satu peserta aktif di chat (Andi),
  SKILL.md tidak punya aturan eksplisit soal "pesan dari pengguna sendiri jangan dianggap
  Perlu Perhatian untuk dirinya sendiri" — agent (saya) terpaksa menafsirkan sendiri (pesan
  reminder dari Andi dimasukkan ke Info, bukan Perlu Perhatian). Ini keputusan yang masuk akal,
  tapi berpotensi tidak konsisten antar-sesi kalau agent lain menafsirkan beda. **Saran
  perbaikan:** tambahkan di SKILL.md langkah 4 kalimat eksplisit: "pesan yang dikirim oleh
  pengguna sendiri (nama pengguna, bila diketahui) tidak dimasukkan ke Perlu Perhatian, kecuali
  ada balasan orang lain yang menunggunya."
- **Cacat ringan lain:** blok "Juga tercatat" pada 22 Sep sedikit keluar dari format standar
  SKILL.md (harusnya nomor urut Perlu Perhatian konsisten 1-6 bukan disisipkan terpisah) —
  akibat saya menghindari duplikasi dengan info form di hari 23 Sep. **Saran:** SKILL.md perlu
  aturan eksplisit soal item yang relevan untuk >1 hari (mis. link form yang berlaku lintas
  hari) supaya tidak menimbulkan format ad hoc seperti ini.
