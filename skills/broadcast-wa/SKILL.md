---
name: broadcast-wa
description: Membuat pesan broadcast WhatsApp promosi yang personal ({nama}, {sapaan}) dalam 3–5 variasi, lengkap dengan teks berhenti (opt-out) wajib, saran jadwal kirim bertahap, pengingat UU PDP, dan — bila ada file kontak CSV — daftar kirim siap pakai yang hanya berisi kontak yang setuju plus link wa.me per kontak. Gunakan saat pengguna minta pesan broadcast/blast WA, promo lewat WhatsApp, atau info promo ke pelanggan (WhatsApp broadcast, WA marketing message, bulk message). Berlaku juga saat permintaan ditolak (kontak tanpa izin/database beli): draf pesan yang tetap ditulis wajib lolos cek fakta dan tanpa klaim/urgensi karangan ("Khusus hari ini", "sebelum kehabisan", "stok terbatas"). Bukan untuk membalas chat satu pelanggan (balas-chat-cs) atau menagih utang (tagih-piutang).
---

# Broadcast WA

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## ATURAN WAJIB (berlaku di SEMUA jalur, termasuk saat menolak permintaan)

1. Setiap draf teks pesan yang ditulis, **juga di jalur penolakan tanpa file kontak** (database beli, nomor tanpa izin) dan draf "siap dipakai nanti", WAJIB lolos `python3 <folder-skill-ini>/scripts/cek_fakta.py --teks-file pesan.txt --fakta-file fakta.txt --abaikan jam` (`HASIL: LULUS`) sebelum ditampilkan.
2. DILARANG menulis sifat produk/rasa/tekstur ("empuk", "fresh", "favorit"), urgensi/kelangkaan ("Khusus hari ini", "Hari ini ada promo", "sebelum kehabisan", "stok terbatas"), periode, atau layanan yang tidak diberikan pengguna. Pakai `[isi: periode promo]` atau tanyakan. Hanya angka & frasa dari pengguna.
3. Jalur penolakan: tolak daftar kirim, jelaskan UU PDP singkat, tawarkan cara kumpulkan izin, lalu bila menulis draf pakai hanya fakta pengguna + placeholder.

## Tujuan
Membantu pemilik usaha mengirim promo lewat WhatsApp yang terasa personal, tidak mengganggu, dan patuh
aturan: hanya ke pelanggan yang setuju, selalu ada cara berhenti, dikirim bertahap supaya nomor aman.

## Kapan digunakan
- "Bikinin pesan broadcast WA promo gajian buat pelanggan laundry saya"
- Menyiapkan info produk baru, pre-order, restock, atau pengingat event ke daftar pelanggan
- Mengolah file kontak (CSV/Excel) menjadi daftar kirim terjadwal

## Kapan TIDAK digunakan
- Membalas chat/komplain satu pelanggan → `balas-chat-cs`; menagih pembayaran → `tagih-piutang`
- Menindaklanjuti calon klien B2B satu per satu → `follow-up-prospek`
- Caption WA Status dan rencana konten → `konten-mingguan`
- Mengirim ke nomor yang tidak memberi izin (database beli, nomor dari grup), atau meminta cara
  mengakali sistem anti-spam/alat blast tidak resmi → **tolak dengan sopan**, jelaskan risikonya
  (UU PDP, nomor diblokir), dan tawarkan cara mengumpulkan persetujuan.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Isi promo/info (produk, harga, periode, syarat) | Ya | — (tanyakan) |
| Nama toko & cara order | Ya | — (tanyakan) |
| Target penerima (pelanggan lama, member, reseller) | Tidak | Pelanggan yang sudah setuju menerima info |
| Nada bahasa | Tidak | Santai-sopan, sapaan {sapaan} (default "Kak") |
| File kontak CSV (nama, nomor, persetujuan, opsional kota dll.) | Tidak | Tanpa file → hanya teks pesan & jadwal saran |
| Waktu mulai kirim & zona waktu | Tidak | Saran jadwal umum, WIB |
| Jumlah variasi | Tidak | 3 variasi |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat,
pakai default dan sebutkan asumsinya di akhir.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Baca `references/aturan-pdp-wa.md`.** Pastikan penerima adalah kontak yang setuju. Jika pengguna
   belum punya data persetujuan, tetap bantu buat pesannya, tapi sertakan cara mengumpulkan izin.
2. **Tulis 3–5 variasi pesan** (±300–600 karakter, maks. ±700) dengan pembuka, isi, dan penutup yang
   berbeda-beda, bukan sekadar ganti satu kata. Setiap variasi wajib:
   - menyapa dengan `{sapaan} {nama}` (hasilnya mis. "Bu Siti", "Kak Rina"). Bila CSV punya kolom sapaan
     (Sapaan/Panggilan), script memakai isinya; kolom kosong → awalan nama/gelar → default "Kak";
   - menyebut nama toko dan alasan singkat mereka menerima pesan (mis. "pelanggan setia Laundry X");
   - isi promo yang **persis** dari pengguna (harga, periode, syarat) — **jangan menghitung angka baru**
     (persen hemat, total); jika pengguna ingin menyebut "hemat X%", minta angkanya;
   - satu CTA jelas (balas chat, klik 1 link, datang ke toko);
   - **teks berhenti**, mis. "Tidak ingin menerima info promo lagi? Balas STOP."
     Harus berupa instruksi tindakan: balas/ketik/kirim + STOP/BERHENTI (mis. "Balas STOP", "Balas dengan kata
     STOP", "balas: STOP"). Script menolak kalimat tanpa instruksi itu ("tidak ingin menerima...", "promo
     non-stop", "stop-motion") dan kalimat yang melarang ("jangan balas STOP").
   Pakai satu sapaan yang konsisten dalam satu pesan: jika menyapa "{sapaan} {nama}", jangan ganti ke "Kamu"
   di kalimat berikutnya (pakai "{sapaan}" lagi).
   Emoji secukupnya (maks. 3), tanpa huruf kapital semua, tanpa "URGENT!!!", maks. 1 link.
   - **Anti-karang:** klaim urgensi/reputasi/label/layanan ("stok terbatas", "terlaris", "halal", "gratis ongkir",
     "besok harga naik") hanya boleh bila **disebut pemilik**. Tidak disebut → jangan ditulis (boleh tanya).
   - **Versi daftar siaran** (WhatsApp Business, tanpa `{nama}`, sapaan umum "Halo Kak") ditulis di bagian
     **terpisah** dan **tidak** dimasukkan ke file pesan untuk daftar kirim personal — script menolak variasi tanpa
     `{nama}` bila CSV punya kolom nama.
3. **Saran jadwal kirim** sesuai audiens: jam kirim, hari, bertahap per batch (lihat references).
4. **Jika pengguna memberi file kontak CSV**, simpan variasi personal ke file teks (dipisah baris `---`), salin
   **kata-kata pengguna tentang promo apa adanya** ke `fakta.txt` (jangan ditambah), lalu jalankan
   (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/siapkan_broadcast.py --kontak pelanggan.csv --pesan pesan.txt \
     --fakta-file fakta.txt --mulai "2026-09-28 10:00" --jam-kirim 09:00-20:00 --output broadcast_siap.csv
   ```
   Cek fakta berjalan **otomatis** di script ini (tanpa `--fakta-file`, semua klaim dianggap karangan dan script GAGAL).
   Bila script menolak karena "klaim yang tidak disebut pemilik", hapus klaim itu dari variasi (atau tanyakan ke
   pemilik) lalu jalankan ulang — jangan melewati pemeriksaan ini. Tanpa CSV, cek variasi dengan
   `python3 <folder-skill-ini>/scripts/cek_fakta.py --teks-file pesan.txt --fakta-file fakta.txt --abaikan jam`
   (harus `HASIL: LULUS`). Kolom sapaan terdeteksi otomatis (Sapaan, Panggilan, Sebutan; atau `--kolom-sapaan`).
   Script hanya meloloskan kontak yang setuju, membuang yang minta berhenti (kolom Berhenti berisi apa pun
   selain kosong/tidak/0/-, misalnya "ya", "STOP", "x", atau tanggal; juga `--daftar-berhenti stop.txt`).
   Nomor yang pernah berhenti/tidak setuju di satu baris tetap dikecualikan walau muncul lagi di baris lain. Script juga
   merapikan nomor ke 628xxx, membuang duplikat, menggilir variasi, membuat jadwal & link wa.me per
   kontak, dan melewati Jumat 11.30–13.00 (geser ke 13.00; matikan dengan `--kirim-saat-jumatan` bila
   audiens tidak relevan). Script **menolak** berjalan bila ada variasi tanpa teks berhenti atau file tanpa kolom
   persetujuan. **Jangan** memakai `--saya-pastikan-semua-setuju` bila pengguna menyebut nomor berasal dari
   database beli, grup, atau sumber tanpa izin. Laporkan ringkasan (siap kirim, dilewati + alasannya, sebaran variasi, jadwal pertama/terakhir).
   Jangan tampilkan seluruh daftar nomor di chat — cukup sebutkan nama file hasilnya.
   - **Format daftar berhenti (`stop.txt`):** paling aman satu nomor per baris, mis. `0812-3456-7890`. Nama,
     catatan, nomor urut ("5. ", "1) "), dan tanggal di baris yang sama boleh ("Galih 0812 0000 0139 (minta stop
     25 September)"); angka catatan di belakang nomor tidak ikut tergabung. Ringkasan menyebut
     `daftar_berhenti_terbaca`. Status **PERIKSA DULU** muncul bila ada `daftar_berhenti_tidak_terbaca` (baris
     tak terbaca) atau `daftar_berhenti_tidak_cocok_kontak` (nomor stop yang tidak cocok dengan kontak mana pun —
     bisa memang bukan pelanggan di file ini, bisa juga salah baca). Sampaikan baris mana yang perlu dicek dan
     **sarankan tidak mengirim** sampai dicocokkan. Sebagai pengaman tambahan, kontak yang nomornya muncul
     sebagai deretan angka di baris stop mana pun juga dikecualikan.
   - Alasan "nilai ... tidak baku" di `dilewati` menunjukkan sel yang isinya tidak standar (mis. "ya (lisan)");
     sebutkan ke pengguna agar dirapikan. Gelar (H., Hj., H.M., dr., Ir., Prof., Muh., juga tanpa spasi seperti
     "Hj.Nurul") otomatis dilewati dari nama, termasuk gelar belakang (S.E., M.Si., M.Pd.) pada `--nama-lengkap`;
     tanpa sapaan, "Hj."/"Ny." menjadi "Bu" dan "H."/"Tn." menjadi "Pak".
   - **Konfirmasi sebelum kirim:** sebutkan jumlah siap kirim, jumlah dilewati per alasan, dan sel yang perlu
     dicek, lalu minta pengguna mengonfirmasi ("Siap kirim ke 142 kontak?") sebelum mulai mengirim.
   **Jika Python tidak bisa dijalankan:** beri langkah manual: saring kolom Persetujuan = ya di
   spreadsheet, hapus yang berhenti & duplikat, bagi per 20 kontak, kirim satu per satu dengan jeda.
5. Tutup dengan checklist PDP singkat dan tawarkan versi lain (lebih formal, bahasa daerah, lebih pendek).

## Format output
```
## Broadcast WA — <topik promo>

### Variasi 1
<pesan siap tempel, placeholder {sapaan} {nama} dipertahankan>

### Variasi 2
...

### Versi daftar siaran WhatsApp Business (tanpa nama — JANGAN dipakai untuk kirim personal)
<pesan dengan sapaan umum, tanpa placeholder>

### Jadwal kirim yang disarankan
- <hari/tanggal>, <jam> <zona>, bertahap <n> pesan per batch, jeda <...>

### Hasil pengolahan kontak (jika ada file)
Siap kirim: <n> | Dilewati: <rincian alasan> | File: <nama file>

### Sebelum kirim (UU PDP)
- [ ] Semua penerima sudah setuju menerima info promo
- [ ] Yang membalas STOP dicatat & tidak dikirimi lagi
- [ ] File kontak disimpan aman, tidak dibagikan

📝 Asumsi: ...
```
Jika pengguna mengirim ke daftar siaran WhatsApp Business (bukan per kontak), ingatkan bahwa `{nama}`
tidak terisi otomatis — pakai versi tanpa placeholder ("Halo Kak") yang juga disertakan.

## Contoh
**Input pengguna:** "Buatin broadcast WA buat pelanggan Laundry Kilat Bersih Depok. Promo gajian 25–30
September: cuci setrika Rp 8.000/kg jadi Rp 7.000/kg, minimal 3 kg, antar-jemput gratis area Beji.
Order balas chat aja. Aku punya file pelanggan.csv."

**Output (cuplikan):**
```
### Variasi 1
Halo {sapaan} {nama} 👋
Ini dari Laundry Kilat Bersih Depok. Khusus 25–30 September, cuci setrika cuma Rp 7.000/kg
(biasanya Rp 8.000/kg), minimal 3 kg. Antar-jemput gratis untuk area Beji.
Mau dijemput kapan? Balas chat ini aja ya.
Tidak ingin menerima info promo lagi? Balas STOP.

### Variasi 2
Selamat gajian, {sapaan} {nama}! 🎉 Biar weekend bebas nyetrika, Laundry Kilat Bersih kasih harga
Rp 7.000/kg untuk cuci setrika (min. 3 kg) sampai 30 September. Area Beji dijemput & diantar gratis.
Balas "JEMPUT" + jam yang pas ya.
Pesan ini dikirim karena {sapaan} terdaftar sebagai pelanggan kami. Balas BERHENTI untuk berhenti.

### Hasil pengolahan kontak
Siap kirim: 142 | Dilewati: 31 belum setuju, 4 minta berhenti, 6 nomor tidak valid, 3 duplikat
File: broadcast_siap.csv (berisi jadwal & link wa.me per kontak — simpan, jangan dibagikan)
```
(Angka hasil pengolahan di atas ilustrasi; angka sebenarnya selalu dari output script.)

## Checklist sebelum mengirim hasil
- [ ] Setiap variasi punya {sapaan} {nama}, nama toko, CTA, dan teks berhenti
- [ ] Angka promo persis dari pengguna; tidak ada angka hasil hitungan sendiri
- [ ] Tidak ada klaim yang tidak diberikan pengguna (halal, BPOM, terlaris, "stok terbatas/terakhir") — dicek
      script `--fakta-file` / `cek_fakta.py`
- [ ] Sapaan mengikuti kolom Sapaan pengguna bila ada; versi daftar siaran terpisah dari variasi personal
- [ ] Variasi benar-benar berbeda (pembuka, susunan, CTA), maks. 1 link, emoji ≤ 3
- [ ] Ada saran jadwal bertahap & pengingat UU PDP
- [ ] Jika memakai file kontak: ringkasan script dilaporkan, daftar nomor tidak ditempel di chat

## Batasan & penanganan error
- Skill tidak mengirim pesan dan tidak terhubung ke WhatsApp; pengiriman tetap dilakukan pengguna
  (manual lewat link wa.me, daftar siaran, atau layanan resmi WhatsApp Business Platform).
- Batas fitur WhatsApp (mis. jumlah kontak per daftar siaran) bisa berubah → sebut "cek ketentuan terbaru".
- Error script umum: kolom nomor/persetujuan tidak ditemukan (pakai `--kolom-nomor "No WA"` dll.),
  placeholder tidak dikenal (nama kolom harus sama, mis. `{kota}` untuk kolom "Kota"), file bukan UTF-8
  (simpan ulang sebagai "CSV UTF-8"). Kontak dengan kolom placeholder kosong dilewati, bukan dikirimi teks bolong.
- Disclaimer: ringkasan UU PDP di skill ini bukan nasihat hukum; untuk database besar atau data sensitif,
  konsultasikan dengan konsultan hukum.
