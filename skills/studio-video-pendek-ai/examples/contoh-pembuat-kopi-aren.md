# Contoh dari pembuat skill (bukan hasil uji independen)

**Input pengguna:** "Bikin video 30 detik untuk kopi susu gula aren, Rp22.000, jualan lewat WhatsApp."

## 0. Asumsi & Brief
Asumsi: 30 dtk, tujuan jualan, rekam HP, gaya santai, TikTok + Reels + Shorts. Produk: kopi susu gula aren. Janji utama: manis pas, tidak eneg. Bukti yang ada: diseduh per pesanan, susu segar, gula aren dari Garut (dikonfirmasi pengguna).

## 1. Pilihan Hook
1. Masalah: "Jam tiga sore, mata udah setengah watt?"
2. Angka jujur: "Dua puluh dua ribu, kopi susu diseduh baru."
3. Visual: gula aren cair dituang ke susu, tanpa suara 2 detik.
Rekomendasi: nomor 1, karena dekat dengan kebiasaan penonton kerja/kuliah.

## 2. Naskah & Timing
| # | Waktu | Sulih suara | Teks di layar |
|---|---|---|---|
| 1 | 0-4 | Jam tiga sore, mata udah setengah watt? [jeda] | JAM 3 SORE NGANTUK? |
| 2 | 4-8 | Kopi susu biasa sering kemanisan, bikin eneg. [jeda 0.5] | Kemanisan? Eneg? |
| 3 | 8-13 | Coba kopi susu gula aren kami. Manisnya pas, wangi aren-nya kerasa. | Kopi Susu Gula Aren |
| 4 | 13-19 | Diminum dingin, pas banget buat nemenin kerja atau nunggu macet. [jeda 1] | Dingin, segar |
| 5 | 19-25 | Kami seduh baru setiap pesanan, pakai susu segar, dan gula aren asli dari Garut. | Seduh baru per pesanan |
| 6 | 25-30 | Cuma dua puluh dua ribu rupiah. Pesan lewat WhatsApp di profil kami ya. | Rp22.000 - Pesan via WA (profil) |

Keluaran `python3 scripts/durasi_naskah.py examples/naskah-kopi-aren.txt --target 30`:
```
Adegan                   Kata  Jeda  Detik
Hook                        7   0.5    3.6
Masalah                     7   0.5    3.6
Produk                     11   0.0    4.7
Suasana                    10   1.0    5.3
Bukti                      14   0.0    5.9
CTA                        13   0.0    5.2
Total 28.3 dtk (target 30 dtk, 150 kata/menit) -> PAS
Ini perkiraan; ukur ulang dengan rekaman suara asli.
```
(Urutan adegan di berkas naskah sama dengan tabel di atas, dengan label singkat.)

## 3. Storyboard & Shot List
| # | Visual | Jalur A: rekam HP | Jalur B: prompt video AI |
|---|---|---|---|
| 1 | Wajah/tangan mengucek mata di meja kerja | Tangan + laptop, dekat, cahaya jendela samping, 3 dtk | `[Subject] hands rubbing tired eyes at a laptop desk [Action] slow blink then reach for phone [Setting] home office afternoon light [Camera] vertical 9:16, medium close-up, static [Style] realistic, natural color [Duration] 4s [Avoid] real people's faces, logos, garbled text` |
| 2 | Gelas kopi susu manis berlebih, close-up | Es kopi susu biasa (properti), 30 cm, HP ditopang | `[Subject] iced milk coffee in clear glass [Action] hand stirs, syrup swirls [Setting] wooden table, soft window light [Camera] 9:16, close-up, slow push-in [Style] realistic product commercial [Duration] 4s [Avoid] logos, text` |
| 3 | Gula aren cair dituang ke susu | Rekam tuangan dari samping, latar polos, 4 dtk | `[Subject] dark palm sugar syrup pouring into white milk in clear glass [Action] slow swirl [Setting] cafe counter, warm light [Camera] 9:16, macro, slight tilt-down [Style] realistic, condensation on glass [Duration] 5s [Avoid] text, logos` |
| 4 | Gelas dingin di meja kerja/dalam mobil | Genggam gelas, embun tampak, 5 dtk | Gambar-ke-video dari foto produk sendiri, gerakan: kamera mengitari gelas perlahan |
| 5 | Proses seduh: susu, gula aren, kopi | Tiga klip 2 dtk, tangan saja | Tidak disarankan AI (proses nyata lebih meyakinkan); rekam asli |
| 6 | Produk + layar harga | Foto/klip produk, teks harga ditambah di aplikasi edit | Gambar-ke-video foto produk; teks harga ditambah manual, bukan dari AI |

## 4. Teks Sulih Suara Final
Jam tiga sore, mata udah setengah watt? [jeda] Kopi susu biasa sering kemanisan, bikin eneg. [jeda] Coba kopi susu gula aren kami. Manisnya pas, wangi aren-nya kerasa. Diminum dingin, pas banget buat nemenin kerja atau nunggu macet. [jeda] Kami seduh baru setiap pesanan, pakai susu segar, dan gula aren asli dari Garut. Cuma dua puluh dua ribu rupiah. Pesan lewat WhatsApp di profil kami ya.

## 5. Caption & Hashtag
- Santai: "Ngantuk jam 3? Kopi susu gula aren, manisnya pas, Rp22.000. Pesan via WA di profil. Video ini dibuat dengan bantuan AI (sebagian visual)."
- Singkat: "Kopi susu gula aren Rp22.000. Pesan via WA di profil."
- Hashtag: #kopitiktok #kopisusu #kopisusugularen #kopigarut #jajanbandung #kopikerja

## 6. Checklist Label AI & Etika
Jalur rekam HP penuh: tidak ada unsur AI, label tidak perlu; cukup pastikan musik dari perpustakaan platform. Jalur campuran (klip AI pada adegan 1-2): cek label platform, pakai kalimat "dibuat dengan bantuan AI", jangan hapus penanda alat. Tidak ada testimoni rekaan; klaim "gula aren asli dari Garut" hanya dipakai bila benar.

## 7. Langkah Produksi Cepat
1. Siapkan properti dan cahaya jendela. 2. Rekam adegan 1-6 masing-masing dua kali. 3. Rekam sulih suara sendiri di ruang tenang, ukur durasinya. 4. Susun di aplikasi edit, tambah teks di layar dan musik dari perpustakaan platform. 5. Centang label bila perlu, unggah manual.
