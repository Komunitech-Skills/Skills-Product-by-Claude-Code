# Uji 01 — Skenario normal 1: katering rantangan harian, Semarang

> Hasil uji independen (Tahap 6), 2026-09-29. Penguji memerankan agent yang mengikuti `SKILL.md` apa adanya. Merek "Rantang Bu Wulan" dan semua tokoh fiktif. Skor segmen dijalankan sungguhan lewat `scripts/skor_segmen.py` dan diverifikasi ulang dengan hitungan independen (pecahan eksak).

**Permintaan pengguna:**
"Aku jualan rantangan/katering harian rumahan di Semarang, daerah Tembalang & Banyumanik. Harga Rp 27 ribu per porsi, paket langganan 5 hari Rp 125 ribu. Pesan lewat WA, antar sendiri jam 10-11 siang. Pembeli sekarang kebanyakan karyawan dan anak kos yang kerja. Pesaing: warteg, GoFood/GrabFood, katering lain di grup FB. Nama usaha Rantang Bu Wulan. Tolong bikin persona dan positioning."

---

# Positioning & Persona — Rantang Bu Wulan

## Ringkasan 5 baris
- Segmen utama 90 hari: **Karyawan perantau & anak kos yang kerja** (skor 79,0/100). Segmen kedua yang hampir setara: keluarga muda suami-istri bekerja (78,0) — diuji kecil, tidak dikejar dulu.
- Persona: **Dimas, 26, staf admin gudang di Banyumanik, asal Pati, ngekos.**
- Positioning: makan siang rumahan yang diantar tiap hari kerja, supaya tidak perlu mikir menu dan tidak boros ongkir aplikasi.
- Tagline rekomendasi: **"Makan rumahan, tanpa mikir menu."**
- Langkah pertama: tanya 5 pelanggan langganan lewat WA (pertanyaan di bagian 8), lalu uji 2 tagline di status WA 3 hari.

## 1. Bahan & asumsi
| Jenis | Isi |
|---|---|
| FAKTA | Rantang harian rumahan; Rp 27.000/porsi; paket 5 hari Rp 125.000; pesan via WA; antar sendiri jam 10-11; area Tembalang & Banyumanik; pembeli sekarang: karyawan & anak kos yang kerja; pesaing: warteg, GoFood/GrabFood, katering lain di grup FB |
| Hitungan | Paket 5 hari = Rp 125.000 / 5 = **Rp 25.000 per porsi**, hemat Rp 2.000/porsi atau **Rp 10.000/minggu** dibanding beli satuan (5 x 27.000 = 135.000) |
| HIPOTESIS | Alasan utama langganan = malas mikir menu + ongkir aplikasi mahal; menu berganti tiap hari [perlu dicek]; sebagian pelanggan kerja di pabrik/gudang/kantor sekitar Banyumanik |
| Perlu dicek | Berapa pelanggan aktif sekarang; berapa yang ambil paket vs satuan; apakah ada pelanggan keluarga; batas jumlah porsi per hari yang sanggup dimasak & diantar |
Asumsi: tidak ada data ulasan; angka ukuran pasar tidak disebut karena tidak ada sumbernya.

## 2. Segmen & skor
Perintah: `python3 scripts/skor_segmen.py segmen.csv` (bobot awal).

| # | Segmen | Skor | Saran script | Alasan nilai (singkat) |
|---|---|---|---|---|
| 1 | Karyawan perantau & anak kos kerja | 79,0 | Utama | ukuran 4 (sudah jadi mayoritas pembeli [F]); daya_beli 3 (Rp 25-27 rb sedikit di atas warteg); kebutuhan 5 (makan siang tiap hari kerja); kanal 5 (WA + grup kos/kantor); cocok 4; persaingan 2 (warteg & aplikasi banyak); layani 4 |
| 2 | Keluarga muda suami-istri bekerja | 78,0 | Utama | ukuran 3 [H]; daya_beli 4; kebutuhan 4; kanal 4; cocok 5 (masakan rumahan); persaingan 3; layani 4 |
| 3 | Kantor kecil & toko (makan siang karyawan) | 66,0 | Kandidat | porsi banyak sekaligus, tapi kemampuan layani 2 (antar sendiri, kapasitas terbatas) |
| 4 | Lansia & keluarga pasien (menu rendah garam) | 57,0 | Tunda | kecocokan 2: butuh menu khusus & klaim kesehatan yang tidak dimiliki |

(Skor dari script; penilaian 1-5 = perkiraan, bukan data pasar. Verifikasi independen: 395/100x20 = 79,0; 390 → 78,0; 330 → 66,0; 285 → 57,0 — cocok.)

**Keputusan:** skor 1 dan 2 hanya selisih 1 poin, jadi dipilih yang sudah terbukti membeli (FAKTA: mayoritas pembeli sekarang). Untuk 90 hari ke depan fokus ke **segmen 1**; keluarga muda tetap dilayani dengan pesan yang sama (tanpa konten terpisah).

## 3. Persona utama — Dimas (fiktif)
| Aspek | Isi |
|---|---|
| Usia, kota | 26, ngekos di Banyumanik (kota besar), asal Pati [H] |
| Kegiatan | Staf admin gudang, masuk 08.00, istirahat 12.00 |
| Uang | Gaji ± UMK Semarang [H, cek]; nyaman Rp 20-30 rb sekali makan siang |
| Yang memengaruhi | Teman kantor yang sudah langganan; grup WA kos |
| Kanal | WA (chat & status), GoFood/GrabFood saat malas keluar, IG/TikTok untuk hiburan |
| Bayar | Transfer/QRIS mingguan; tunai bila baru coba |
| Bahasa | Santai campur Jawa: "mbak", "nggih", "menu hari ini apa?" |
| JTBD fungsional | Ketika jam istirahat cuma 1 jam dan warteg dekat gudang penuh, aku ingin makan siang sudah datang sendiri, supaya bisa makan tenang tanpa antre |
| JTBD emosional | Merasa diurus seperti makan di rumah, tidak makan asal kenyang |
| JTBD sosial | Tidak dianggap boros oleh teman karena pesan aplikasi tiap hari |
| Pemicu beli | Awal bulan (gajian), mulai kerja di tempat baru, bosan menu warteg |
| Keberatan | "Menunya itu-itu aja?", "Kalau telat antar gimana?", "Bayar seminggu di depan, kalau aku libur?" |
| Wawasan tak terduga [H] | Dimas lebih peduli **menu diumumkan sehari sebelumnya** (supaya bisa pamer ke teman / mengatur jajan) daripada variasi menu itu sendiri |
| Anti-persona | Pencari makan termurah < Rp 15 rb; orang yang butuh menu diet medis |
| Kutipan khas [H] | "Yang penting sampai sebelum jam 12 dan nggak itu-itu aja." |

## 4. Kebutuhan (JTBD) & Value Proposition
| Kerepotan (urut paling berat) | Pereda | Bukti |
|---|---|---|
| Istirahat pendek, antre warteg | Antar jam 10-11 ke kantor/kos [F] | Jadwal antar tertulis; [isi: foto rantang sampai] |
| Bingung mau makan apa tiap hari | Menu ganti tiap hari, diumumkan di status WA [H] | [isi: foto menu 1 minggu] |
| Ongkir aplikasi bikin boros | Paket 5 hari Rp 125.000 (Rp 25.000/porsi, ongkir termasuk [perlu dicek]) | Daftar harga tertulis |

Empat Gaya: **Dorongan** = warteg penuh, ongkir aplikasi; **Tarikan** = rasa rumahan, datang sendiri; **Kebiasaan** = sudah biasa jajan dekat kantor; **Kecemasan** = telat antar, rugi kalau libur. Pereda kecemasan: aturan libur/ganti hari tertulis [isi: kebijakan], jam antar pasti.

6 bagian: Untuk karyawan perantau | butuh makan siang tiap hari kerja | sebelum: antre warteg / boros aplikasi | cara kami: rantang rumahan diantar jam 10-11, menu ganti | sesudah: makan tenang, hemat Rp 10.000/minggu vs satuan | alternatif: warteg, GoFood/GrabFood, katering grup FB, masak sendiri.

## 5. Pembeda vs pesaing
| Alternatif | Klaim mereka | Celah | Klaim kita | Bukti kita |
|---|---|---|---|---|
| Warteg dekat kantor | Murah, banyak pilihan | Antre di jam istirahat, harus keluar | Datang sendiri sebelum jam 12 | Jam antar tertulis |
| GoFood/GrabFood | Praktis, banyak pilihan | Ongkir & biaya layanan tiap pesan, bingung pilih | Harga paket jelas, menu sudah dipilihkan | Daftar harga [isi] |
| Katering lain di grup FB | Paket mingguan | [H, cek] menu jarang diumumkan dulu | Menu besok diumumkan hari ini | [isi: contoh status menu] |
| Masak sendiri | Paling hemat | Anak kos tidak punya dapur/waktu | Rasa rumahan tanpa masak | [isi: foto dapur/proses] |
Tidak dipakai: "paling enak", "termurah", "sehat" (belum ada bukti). Materi publik tidak menyebut nama pesaing.

## 6. Positioning & tagline
- **Internal:** "Untuk karyawan perantau dan anak kos yang kerja di Tembalang-Banyumanik yang butuh makan siang tiap hari, Rantang Bu Wulan adalah katering rantangan rumahan yang datang sebelum jam istirahat dengan menu yang sudah dipilihkan, karena dimasak pagi dan diantar sendiri jam 10-11. Berbeda dengan warteg dan aplikasi pesan antar, kami menghapus antre dan ongkir harian."
- **Publik:** "Masakan rumahan yang diantar tiap hari, buat kamu yang kerja dan jauh dari dapur rumah." (87 karakter)
- Tagline (jumlah kata dihitung):
  1. "Makan rumahan, tanpa mikir menu." (5 kata)
  2. "Sampai sebelum jam istirahat." (4 kata)
  3. "Rasa rumah, antar ke kantor." (5 kata)
  4. "Masak pagi, sampai siang." (4 kata)
  5. "Rantang harian, hemat tiap minggu." (5 kata)
- **Rekomendasi: (1)** — menyebut dua hal yang paling dicari persona (rumahan + tidak perlu mikir), bisa dibuktikan dengan status menu harian. (2) cocok untuk listing/iklan lokal bila jam antar selalu tepat.

## 7. Message house + teks siap tempel
- **Atap:** "Makan siang rumahan yang datang sendiri, tiap hari kerja."
| Pilar | Klaim | Bukti | Contoh kalimat |
|---|---|---|---|
| Tepat waktu | Antar jam 10-11 | Jadwal tertulis [isi: foto sampai] | "Rantang sampai sebelum kamu istirahat." |
| Tanpa mikir menu | Menu ganti tiap hari | Status WA menu besok [isi] | "Menu besok sudah ada di status, tinggal makan." |
| Hemat & jelas | Paket 5 hari Rp 125.000 | Daftar harga | "Rp 25 ribu per porsi kalau ambil paket." |
- **Fondasi:** foto rantang asli, foto dapur, jadwal antar, [isi: ulasan asli pelanggan — dengan izin, tanpa nama].
- **Keberatan:** menu itu-itu saja → menu seminggu diumumkan; telat → jam antar + kabar via WA; libur → [isi: aturan ganti hari/uang kembali].
- **Pakai:** rumahan, antar, tiap hari, paket. **Hindari:** sehat, bergizi seimbang, termurah, paling enak (belum ada bukti).

Teks siap tempel:
- **Bio IG/WA Business (131 karakter):** `Rantang harian rumahan buat kamu yang kerja & jauh dari rumah. Menu ganti tiap hari, antar sebelum jam 11. Semarang. Pesan via WA 👇`
- **Judul (GoFood/marketplace bila dipakai):** `Rantang Harian Rumahan Semarang — Paket 5 Hari Antar ke Kantor` + poin: (1) antar jam 10-11 Tembalang & Banyumanik, (2) menu ganti tiap hari, (3) paket 5 hari Rp 125.000 (Rp 25 ribu/porsi). Bukti: `[isi: ulasan asli]`.
- **Caption:** "Jam 12 warteg penuh, ongkir aplikasi nambah terus? Rantang Bu Wulan datang ke kantor/kos kamu jam 10-11, masakan rumahan, menu ganti tiap hari. Paket 5 hari Rp 125 ribu. Menu besok cek status ya, pesan lewat WA."
- **Sapaan WA pelanggan baru:** "Halo mas/mbak, terima kasih sudah chat Rantang Bu Wulan 🙏 Mau coba satuan dulu (Rp 27 ribu) atau langsung paket 5 hari (Rp 125 ribu)? Boleh info alamat kantor/kos dan jam istirahatnya, nanti kami cek bisa antar jam berapa."

## 8. Uji 7 hari & pengingat
1. WA 5 pelanggan langganan (5 pertanyaan dari `references/persona-indonesia.md`), minta izin sebelum mengutip.
2. Status WA 3 hari tagline (1), 3 hari tagline (2); catat berapa yang membalas/tanya.
3. Catat 10 chat masuk: bila ≥ 4 menanyakan menu/jam antar, pilar "tanpa mikir menu + tepat waktu" dipertahankan; bila mayoritas tanya harga termurah, tinjau ulang segmen.

**Ceklis klaim:** tidak ada klaim "sehat/bergizi" tanpa dasar; ulasan hanya yang asli; jika produk pangan dijual lewat kemasan/marketplace, cek kebutuhan izin (mis. PIRT/halal) ke sumber resmi; cek nama "Rantang Bu Wulan" di pangkalan data merek DJKI bila dipakai jangka panjang.
**Asumsi:** ongkir termasuk paket, menu ganti tiap hari (belum dikonfirmasi).
**Perlu kamu cek sendiri:** kapasitas porsi per hari, aturan libur/ganti hari, apakah ongkir sudah termasuk.

---
### Catatan penguji
- Alur 9 langkah diikuti; format output sesuai urutan. Script dijalankan; semua skor cocok dengan hitungan independen.
- Skor segmen 1 dan 2 selisih 1 poin, keduanya berlabel "Utama". SKILL.md tidak memberi aturan untuk skor yang hampir seri; penguji memakai "pilih yang sudah terbukti membeli" (usul perbaikan #6 di `HASIL-UJI.md`).
- Nama segmen di tabel script terpotong 33 karakter ("Karyawan perantau & anak kos kerj"); agent harus menyalin nama lengkap dari CSV.
- Panjang keluaran ±150 baris: lengkap, tapi panjang untuk dibaca di chat Telegram/WA.
