> **Sumber keluaran:** penguji independen Akun B, 2026-10-13, Claude Code (simulasi agent), data fiktif; menggantikan contoh lama yang memuat atribut/angka tanpa sumber.

# Skenario 3 (normal): toko hijab, gaya UGC 30 detik

## Input pengguna
"Bikin video gaya UGC 30 detik untuk hijab voal Rp99.000, pemilik toko yang ngomong sendiri."

## Output

**Fakta dari pengguna** (kata-kata pengguna apa adanya): hijab voal; Rp99.000; pemilik toko yang ngomong sendiri; gaya UGC; 30 detik. Tidak disebut pengguna, jadi **tidak ditulis sebagai fakta**: warna, ukuran, kelebihan bahan, nama toko/merek, kota, cara pesan, harga per helai atau per paket, bukti penjualan/ulasan.

**0. Asumsi & Brief**
Asumsi: 30 dtk, tujuan jualan, rekam HP, pemilik tampil sendiri (klon wajah/suara tidak diperlukan), gaya santai "aku-kamu", TikTok + Reels + Shorts. Janji utama: satu saja, yaitu pemilik menunjukkan hijab voal ini langsung ke kamera. Bukti: demonstrasi produk nyata di depan kamera; tidak ada testimoni, angka terjual, atau ulasan karena tidak disebut pengguna. Bagian bertanda `[isi: ...]` diisi pemilik sebelum merekam (daftar di bawah naskah).

**1. Pilihan Hook**
1. Pertanyaan: "Lagi cari hijab voal?"
2. Pernyataan jujur: "Hijab voal, sembilan puluh sembilan ribu rupiah. Aku tunjukin langsung."
3. Visual: kain hijab dibentangkan pelan di depan kamera, tanpa bicara 2 detik.
Rekomendasi: nomor 1, karena singkat, cocok untuk gaya UGC, dan isinya langsung dibuktikan di adegan berikutnya.

**2. Naskah & Timing**
| # | Waktu | Sulih suara | Teks di layar |
|---|---|---|---|
| 1 | 0-4 dtk | Lagi cari hijab voal? [jeda] Sini, aku tunjukin langsung. | Cari hijab voal? |
| 2 | 4-9 dtk | Halo, aku [isi: nama], pemilik [isi: toko]. Ini hijab voal yang aku jual. | [isi: nama toko] |
| 3 | 9-15 dtk | Aku bentangkan pelan-pelan ya, biar kamu lihat sendiri. [jeda] Warnanya [isi: warna]. | Warna: [isi: warna] |
| 4 | 15-21 dtk | Ukurannya [isi: ukuran]. [jeda] Satu hal yang aku suka dari hijab ini: [isi: satu hal nyata]. | Ukuran: [isi: ukuran] |
| 5 | 21-26 dtk | Harganya sembilan puluh sembilan ribu rupiah [isi: per helai/paket]. [jeda] | Rp99.000 |
| 6 | 26-30 dtk | Mau pesan? [isi: cara pesan]. Aku tunggu ya. | Pesan: [isi: cara pesan] |

Keluaran `python3 scripts/durasi_naskah.py naskah.txt --target 30`:
```
Adegan                    Kata  Jeda  Detik
Hook                         8   0.5    4.0
Kenalan                     13   0.0    5.5
Tunjuk                      11   0.5    5.2
Detail                      15   0.5    6.8
Harga                       10   0.5    4.8
CTA                          8   0.0    3.2
Total 29.5 dtk (target 30 dtk, 150 kata/menit) -> PAS
```
Perkiraan durasi sulih suara: 29,5 dtk (target 30 dtk, 150 kata/menit). Catatan: tiap `[isi: ...]` dihitung sebagai kata penanda; hitung ulang dengan script setelah semua isian terisi.
Cek fakta: `python3 scripts/cek_fakta.py --teks-file naskah.txt --fakta "hijab voal; Rp99.000; pemilik toko yang ngomong sendiri; gaya UGC; 30 detik"` -> LULUS (0 GAGAL, 0 CEK).

**3. Storyboard & Shot List**
| # | Visual | Jalur A: rekam HP | Jalur B: prompt video AI |
|---|---|---|---|
| 1 | Pemilik menghadap kamera, hijab di tangan | HP vertikal di tripod, setinggi mata, cahaya jendela dari samping, jarak setengah badan, 3-4 dtk | Tidak disarankan: pemilik tampil sendiri dengan wajah dan suara asli |
| 2 | Pemilik memperkenalkan diri, hijab terlihat di bingkai | Sama dengan adegan 1, potong ke jarak dada, 4-5 dtk | Tidak disarankan (alasan sama) |
| 3 | Kain dibentangkan dua tangan di depan kamera | Rekam dari depan, cahaya jendela, latar polos, 5-6 dtk; warna di layar bisa berbeda dari aslinya, jadi rekam juga satu klip di dekat jendela | Opsional: gambar-ke-video dari foto produk sendiri, `[Subject] a voile hijab held open by two hands, color [isi: warna] [Action] fabric slowly spreads open [Setting] plain background, soft window light [Camera] vertical 9:16, medium shot, static [Style] realistic product video, natural colors, no text in frame [Duration] 4 seconds [Avoid] distorted hands, extra fingers, garbled text or logos, real people's faces` |
| 4 | Kain di samping alat ukur (bila ukuran diisi), lalu close-up kain | Siapkan meteran atau penggaris panjang di samping kain, lalu satu klip close-up tekstur, 5-6 dtk | Tidak disarankan untuk ukuran (angka harus akurat); close-up kain boleh dari foto sendiri |
| 5 | Teks harga di layar, hijab dipegang | Klip hijab dipegang dekat kamera; teks harga ditambah di aplikasi edit, bukan dari AI | Tidak disarankan (huruf AI sering rusak) |
| 6 | Pemilik menunjuk ke arah teks cara pesan | Satu klip penutup, 3-4 dtk, tersenyum, melambai | Tidak disarankan |

**4. Teks Sulih Suara Final** (angka ditulis cara diucapkan)
Lagi cari hijab voal? [jeda] Sini, aku tunjukin langsung. Halo, aku [isi: nama], pemilik [isi: toko]. Ini hijab voal yang aku jual. Aku bentangkan pelan-pelan ya, biar kamu lihat sendiri. [jeda] Warnanya [isi: warna]. Ukurannya [isi: ukuran]. [jeda] Satu hal yang aku suka dari hijab ini: [isi: satu hal nyata]. Harganya sembilan puluh sembilan ribu rupiah [isi: per helai/paket]. [jeda] Mau pesan? [isi: cara pesan]. Aku tunggu ya.

**5. Caption & Hashtag**
- Santai: "Lagi cari hijab voal? Ini dia, Rp99.000. [isi: cara pesan]."
- Singkat: "Hijab voal Rp99.000. [isi: cara pesan]."
- Hashtag (7): #hijab #hijabtiktok (luas) | #hijabvoal #tokohijab #ugc (niche) | #[isi: kota] (lokal) | #[isi: merek] (merek).
- Kalimat "Video ini dibuat dengan bantuan AI." hanya ditambahkan bila ada unsur AI (mis. suara AI atau klip Jalur B).

**6. Checklist Label AI & Etika**
- [x] Jalur A penuh (rekam HP, wajah dan suara asli pemilik): tidak ada unsur AI, label platform tidak perlu.
- [ ] Bila memakai klip Jalur B atau suara AI: centang label platform dan tulis "dibuat dengan bantuan AI" di caption.
- [x] Tidak ada wajah/suara orang lain; tidak ada testimoni, ulasan, atau before-after rekaan.
- [x] Tidak ada klaim kesehatan/keuangan; harga sama dengan input (Rp99.000).
- [ ] Musik dari perpustakaan platform (bukan lagu unduhan).
- [x] Unggah manual oleh pemilik; skill tidak memposting otomatis.

**7. Langkah Produksi Cepat**
1. Isi semua `[isi: ...]` (nama, toko, warna, ukuran, satu hal nyata, per helai/paket, cara pesan, kota, merek) dengan data asli. 2. Jalankan ulang script durasi dan cek fakta pada naskah yang sudah terisi. 3. Siapkan hijab, meteran/penggaris, tripod, dan cahaya jendela. 4. Rekam adegan 1-6 masing-masing dua kali dengan suara sendiri. 5. Susun di aplikasi edit pilihan Anda, tambahkan teks di layar dan musik dari perpustakaan platform. 6. Unggah manual.

Pertanyaan singkat bila mau naskah final tanpa isian (jawab sekali): (1) nama dan nama toko, (2) warna, (3) ukuran, (4) satu hal nyata yang Anda suka dari produknya, (5) harga per helai atau per paket dan cara pesan.

## Catatan penguji
- **Karangan di contoh lama (dihapus):** bahan "ultrafine", warna "dusty pink", ukuran "120 x 120 cm", "pinggiran dijahit rapi", "ringan, jatuh dan gampang dibentuk", cara pesan "WhatsApp di profil", hashtag kota "#hijabbandung" dan "#hijabootd". Input pengguna hanya memuat: hijab voal, Rp99.000, 30 dtk, gaya UGC, pemilik tampil. Contoh lama juga mengaku "hanya yang pemilik konfirmasi", padahal tidak ada konfirmasi di input.
- **Sekarang:** semua atribut selain lima fakta di atas ditulis `[isi: ...]`; tidak ada sifat/keunggulan baru; tidak ada angka terjual atau ulasan.
- **Hasil script:** durasi 29,5 dtk (PAS, setelah satu kali diringkas dari 30,7 dtk MELEBIHI); `cek_fakta.py` LULUS. Kontrol negatif: kalimat lama "ukurannya 120 x 120 cm" dijalankan lewat `cek_fakta.py` dan GAGAL (kategori ukuran).
- **Celah yang ditemukan:** `cek_fakta.py` tidak menangkap warna ("dusty pink") dan jenis bahan ("ultrafine"); pemeriksaan keduanya harus manual terhadap daftar fakta.
- Penanda `[isi: ...]` ikut dihitung sebagai kata oleh `durasi_naskah.py`, jadi durasi setelah diisi bisa bergeser; hitung ulang.
- Hasil: PASS.
