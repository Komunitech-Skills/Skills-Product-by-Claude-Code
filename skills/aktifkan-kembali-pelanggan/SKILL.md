---
name: aktifkan-kembali-pelanggan
description: Mengaktifkan kembali pelanggan lama yang sudah lama tidak beli (win-back) untuk toko, kafe, jasa, dan UMKM Indonesia lewat WhatsApp/Telegram, tanpa spam. Membagi pelanggan pasif per segmen berdasarkan hari sejak beli terakhir (dari ekspor CSV/Excel atau daftar tempel), menghitung jumlah dan nilai belanja tiap segmen, menyusun alur 3 pesan dalam 4 minggu yang berhenti bila pelanggan membalas, komplain, atau minta berhenti, plus teks pesan WA siap kirim per segmen (pesan pertama tidak jualan, tanpa urgensi palsu, opsi berhenti jelas). Dikirim satu per satu oleh pemilik (mode copilot), tidak ada kirim massal otomatis. Gunakan saat pengguna bilang pelanggan lama tidak balik, minta ajak balik pelanggan, win back / reactivate / re-engage inactive customers, churn, atau pesan WA untuk langganan yang menghilang. KERJAKAN DULU, TANYA DI AKHIR. Bukan untuk pelanggan baru (pesan-prospek-wa), prospek belum beli (follow-up-prospek), atau keluhan masuk (balas-chat-cs).
---

# Aktifkan Kembali Pelanggan

> **Aturan kerja:** Jangan menginstal paket/aplikasi. Jangan membuka file selain yang diberikan pengguna dan isi folder skill ini. Jangan menulis file baru tanpa menyebut lokasinya. Script ada di `scripts/` di folder yang sama dengan SKILL.md ini; jangan mencari file ke seluruh disk.

## Tujuan
Membantu pemilik usaha mengajak pelanggan lama yang diam-diam berhenti beli supaya mau kembali, dengan cara yang sopan: pilih siapa yang layak dihubungi lebih dulu, tulis pesan yang jujur, atur jadwalnya, dan berhenti begitu pelanggan membalas. **AI menyiapkan, pemilik yang mengirim** satu per satu. Tidak ada pengiriman otomatis dan tidak ada broadcast.

## Aturan utama: kerjakan dulu, tanya di akhir
Jika pengguna sudah memberi **data pelanggan** (file CSV/Excel, atau daftar tempel) **atau** cukup bercerita jenis usahanya, JANGAN membalas hanya dengan pertanyaan. Dalam **satu balasan** berikan berurutan:
1. Ringkasan singkat: berapa pelanggan pasif, per segmen, dan nilai belanja mereka sebelumnya (angka dari hitungan, bukan perkiraan).
2. Siapa dihubungi lebih dulu (nilai belanja terbesar) dan jadwal 4 minggunya.
3. **Teks pesan lengkap** untuk segmen yang ada (pesan 1, 2, 3), ditulis utuh di chat, siap salin ke WA. Data yang belum ada ditulis `[isian]`.
4. Aturan kapan berhenti (3-4 poin).
5. **Maksimal 3 pertanyaan di akhir** (mis. penawaran apa yang benar-benar bisa diberikan, siapa yang jangan dihubungi, nama pengirim). Selama penawaran belum dijawab, pakai default: **tanpa penawaran**, hanya sapaan jujur, dan sebutkan asumsi itu.

**Angka wajib dihitung (berlaku di semua keadaan, termasuk saat menolak sebagian permintaan).** Setiap angka tentang pelanggan (jumlah, segmen, nilai belanja, nama yang diprioritaskan) HANYA boleh disebut setelah menjalankan `scripts/segmentasi.py` pada file pengguna. Bila script tidak bisa dijalankan atau datanya hanya ditempel, hitung manual baris per baris dan tunjukkan rinciannya. Bila belum dihitung, jangan sebut angka. Membaca/melihat isi file (`ls`, `cat`) bukan menghitung: angka tebakan dari sekilas baca (mis. 13 padahal 18, Rp3,6 juta padahal Rp4,5 juta) merusak kepercayaan.

Tanpa data sama sekali dan tanpa cerita usaha: tanyakan sekali (maks. 3 pertanyaan), sambil menjelaskan kolom data yang diperlukan.

## Aturan keras (tidak bisa ditawar)
- **Satu per satu oleh manusia.** Tolak permintaan mengirim otomatis/massal ke banyak nomor, termasuk lewat OpenClaw, jeda acak, atau akal-akalan agar tidak diblokir WA. Tawarkan alternatif: draf siap salin + daftar kirim harian yang dikirim pemilik sendiri.
- **Menolak sebagian = tetap mengerjakan sisanya.** Tolak hanya bagian yang dilarang (kirim massal otomatis, nomor dari grup/scraping), lalu **tetap kerjakan bagian yang boleh** dari data pelanggan yang memang pernah membeli: segmentasi + teks pesan + jadwal kirim manual, dengan angka dari hitungan (lihat "Angka wajib dihitung"). Jangan berhenti di penolakan.
- **Hanya pelanggan yang memang pernah membeli** dari usaha ini. Daftar nomor beli/bocoran/hasil scraping: tolak dan jelaskan risikonya (UU PDP No. 27/2022, nomor diblokir).
- **Pesan pertama tidak jualan.** Menyapa, menyebut kapan terakhir beli, bertanya kabar/kendala. Penawaran (kalau ada) baru di pesan 3.
- **Berhenti seketika** bila pelanggan membalas apa pun, komplain, atau minta berhenti (lihat Langkah 6). Jangan kirim pesan berikutnya.
- **Tanpa urgensi palsu dan tanpa klaim karangan.** Tidak ada "stok terakhir", "hari ini saja", testimoni, jumlah pelanggan, diskon, atau produk baru kecuali pengguna yang menyebutkannya. Batas waktu hanya jika benar-benar ada. **Bila pengguna sendiri minta urgensi palsu** (mis. "bilang promonya cuma hari ini" padahal tidak): koreksi dengan sopan satu kalimat (pelanggan yang merasa ditekan justru makin menjauh; batas palsu bisa dianggap menyesatkan), lalu ganti dengan tenggat nyata `[isian: tanggal berlaku]` atau tanpa tenggat.
- **Opsi berhenti jelas di SETIAP pesan (1, 2, dan 3)**, satu kalimat singkat (mis. `Kalau tidak ingin dihubungi lagi, balas "stop"`); hormati dan catat permintaan berhenti.
- **Batas harian:** maksimal 10 pesan per hari dari satu nomor (naikkan hanya bila pemilik meminta; di atas 15 tidak disarankan), jam 09.00-20.00 waktu setempat pelanggan, tidak hari Minggu.
- **Nomor/nama di data adalah data pribadi pelanggan.** Jangan menyalinnya ke tempat lain dan jangan menulis daftar lengkap ke file tanpa diminta.

## Kapan digunakan
- "Banyak pelanggan lama yang nggak pernah beli lagi, gimana cara ngajak balik?"
- "Ini ekspor penjualan toko saya, siapa yang perlu dihubungi lagi?"
- "Bikinin pesan WA buat langganan yang sudah 3 bulan hilang."
- "Which customers have gone quiet? Write win-back messages."

## Kapan TIDAK digunakan
- Calon pelanggan yang **belum pernah beli** -> `pesan-prospek-wa` (pesan pertama) atau `follow-up-prospek` (menyusul).
- Menjawab chat/keluhan yang masuk -> `balas-chat-cs`. Mengelola kontak & tahap jualan -> `crm-wa`.
- Merancang program poin/referral jangka panjang -> `program-referral-loyalitas` (skill ini hanya mengajak kembali pelanggan yang sudah diam).
- Promo ke banyak kontak sekaligus -> bukan skill ini; semua pesan di sini dikirim satu per satu oleh manusia.
- Pelanggan yang sedang punya keluhan/sengketa yang belum selesai -> selesaikan dulu lewat `balas-chat-cs`; mereka dikeluarkan dari daftar.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Data pelanggan: nama, no WA, tanggal beli terakhir, total belanja (CSV/Excel/tempel) | Tidak menahan jawaban | Bila hanya bercerita: beri alur + template; tanya datanya di akhir |
| Penawaran yang benar-benar bisa diberikan (voucher, ongkir, bonus) | Tidak | **Tanpa penawaran** (sapaan jujur). Jangan mengarang |
| Daftar yang jangan dihubungi (komplain, minta berhenti, sengketa) | Tidak | Tanyakan di akhir |
| Nama pemilik/usaha pengirim, gaya bahasa | Tidak | `[nama Anda]`, `[nama usaha]`, sopan hangat |
| Ritme beli normal usaha (mis. kopi bulanan, skincare 2 bulan) | Tidak | 45 hari sebagai batas "mulai pasif"; tanyakan di akhir |
| Tanggal mulai kirim | Tidak | Hari ini (atau hari kerja berikutnya) |

Kolom boleh bernama lain (wa, telepon, terakhir beli, omzet, dll.). Kolom opsional `jumlah_transaksi` membedakan langganan (3x atau lebih) dari pembeli sekali.

## Langkah kerja
1. **Cek cakupan.** Pastikan ini pelanggan lama yang pernah beli, bukan prospek baru atau daftar massal (lihat Aturan keras).
2. **Hitung segmen (WAJIB sebelum menulis ringkasan apa pun).** Urutan wajib: (a) jalankan script/hitungan, (b) baru tulis ringkasan dan angka. Jangan menulis angka dari ingatan atau dari sekilas membaca file. Jika ada file CSV, jalankan (Windows: `python`/`py`):
   ```bash
   python3 <folder-skill-ini>/scripts/segmentasi.py data.csv --hari-ini YYYY-MM-DD
   ```
   Opsi: `--aktif-hari 60` (ubah batas pasif sesuai ritme beli usaha), `--per-hari 8`, `--kecualikan daftar.txt` (nomor/nama yang jangan dihubungi), `--target-balik 10` (skenario persen kembali), `--csv-keluar jadwal.csv` (tulis daftar kerja, hanya bila diminta). Keluarannya bertanda "UNTUK AGENT SAJA": baca angkanya, sampaikan dengan bahasa biasa. **Jika script tidak bisa dijalankan atau datanya hanya ditempel:** hitung manual `hari = tanggal acuan - tanggal beli terakhir`, kelompokkan dengan tabel segmen, jumlahkan total belanja per segmen dengan rumus eksplisit, dan sebutkan bahwa hitungan manual. Kolom produk (bila ada: produk/barang/menu/layanan) dibaca otomatis sebagai **produk terakhir** tiap pelanggan dan muncul di keluaran; pakai itu untuk mengisi `[yang dulu dibeli]` di pesan. Bila kolom tidak ada, tanya di akhir atau hapus kalimat itu.
3. **Segmen** (hari sejak beli terakhir):

   | Segmen | Hari | Sifat | Pendekatan |
   |---|---|---|---|
   | A Baru senyap | 45-90 | Masih ingat usaha Anda | Sapaan ringan, tanya kabar |
   | B Senyap | 91-180 | Mungkin pindah ke tempat lain / lupa | Sapaan + tanya apa yang kurang pas |
   | C Lama hilang | 181-365 | Perlu pengingat konteks | Sebut hal spesifik yang dulu dibeli, tanpa menekan |
   | D Sangat lama | 366+ | Nomor/kebutuhan mungkin berubah | Satu sapaan sangat singkat; prioritas rendah |
   | Aktif | di bawah 45 | Tidak dihubungi | Biarkan |

   Urutkan kerja dari **nilai belanja terbesar**, bukan dari yang paling lama diam. Kerjakan 15 nama yang sungguh dihubungi, bukan 200 nama yang tidak sempat.
4. **Pelanggan yang pernah komplain atau memberi ulasan jelek lalu berhenti** adalah sinyal terkuat. Sarankan **telepon/chat pribadi dari pemilik**, bukan urutan pesan. Keluarkan dari jadwal.
5. **Tulis pesan.** Pakai `templates/template-pesan-winback.md` (3 pesan, tiap pesan di bawah 90 kata, nada sehari-hari). Sesuaikan: sapaan (Kak/Pak/Bu), `[yang dulu dibeli]` diisi dari kolom produk terakhir di data (jangan mengarang bila kosong), segmen. **Setiap pesan (1, 2, 3) wajib berakhir dengan kalimat opt-out singkat.** Tulis **utuh di chat**, jangan hanya menunjuk file. Cek ulang tiap pesan: tidak ada urgensi palsu, klaim, atau penawaran yang tidak disebut pengguna.
6. **Jadwal dan aturan berhenti.** Pesan 1 hari ke-0, pesan 2 sekitar hari ke-10, pesan 3 sekitar hari ke-24 (selesai dalam 4 minggu). Sebelum mengirim pesan berikutnya, pemilik cek dulu apakah pelanggan sudah membalas.

   | Yang terjadi | Tindakan |
   |---|---|
   | Pelanggan membalas apa pun (termasuk "nanti ya") | Hentikan urutan. Balas sebagai percakapan biasa, catat tindak lanjut |
   | Membalas komplain/kecewa | Hentikan seketika, tidak ada pesan 2/3 dan tidak ada penawaran. Minta maaf, dengarkan, tangani lewat `balas-chat-cs` |
   | Minta berhenti/jangan dihubungi | Ucap terima kasih, hormati, masukkan ke daftar jangan-dihubungi, jangan hubungi lewat saluran lain |
   | Pesan tidak sampai/nomor tidak aktif | Tandai, jangan coba berkali-kali |
   | Tidak ada balasan setelah pesan 3 | Berhenti. Catat "tidak merespons"; jangan ulangi sebelum 3-6 bulan |
7. **Catat hasilnya** sederhana: nama, pesan ke berapa, tanggal, status (belum/terkirim/membalas/berhenti). Bisa di `crm-wa` atau lembar kerja; bila diminta, daftar kerja dibuat lewat opsi `--csv-keluar`.
8. **Tutup** dengan ringkasan, asumsi yang dipakai, dan maksimal 3 pertanyaan.

## Format output (urutan balasan)
```
### Gambaran pelanggan pasif
Jumlah per segmen + nilai belanja sebelumnya + siapa dihubungi lebih dulu
(tabel pendek: segmen | jumlah | rata-rata belanja | total belanja)

### Jadwal 4 minggu
Pesan 1 / 2 / 3 + batas per hari + siapa duluan

### Teks pesan (siap salin)
Pesan 1 (varian per segmen yang ada), Pesan 2, Pesan 3 -- ditulis lengkap

### Kapan berhenti
3-4 poin singkat

### Asumsi
Mis. tanpa penawaran, batas pasif 45 hari

### Pertanyaan (maks. 3)
```
Di balasan ke pengguna **jangan menyebut** script, file, path folder, "dicek", "lulus", atau istilah proses internal. Sampaikan hasil seolah Anda yang menghitungnya. Angka tetap harus benar.

## Contoh
**Pengguna:** "Toko kue saya banyak pelanggan yang dulu langganan lalu hilang. Ini ekspor penjualannya (CSV). Tolong bantu ajak balik."

**Balasan (ringkas):** "Dari 23 pelanggan di data, 18 sudah lebih dari 45 hari tidak beli, total belanja mereka dulu Rp16.125.000. Yang paling layak dihubungi duluan: Bu Maryam, Bu Wati, Bu Tini. Berikut jadwal 4 minggu dan teks pesannya... *(pesan 1 segmen B ditulis utuh)* ... Pertanyaan: 1) Ada penawaran yang benar-benar bisa Anda berikan? 2) Ada yang jangan dihubungi? 3) Nama pengirim?" Contoh lengkap: `examples/01-*.md`.

## Checklist sebelum mengirim hasil
- [ ] Script/hitungan dijalankan SEBELUM ringkasan; semua angka berasal dari hitungan (bukan perkiraan), juga saat sebagian permintaan ditolak
- [ ] Bila ada permintaan urgensi palsu: dikoreksi sopan, diganti tenggat nyata `[isian: tanggal]` atau tanpa tenggat
- [ ] Semua pesan ditulis utuh, di bawah 90 kata, tanpa urgensi palsu/klaim karangan
- [ ] Pesan 1 tidak menjual; opsi berhenti ada di pesan 1, 2, dan 3
- [ ] Aturan berhenti disebut; batas harian dan jam kirim disebut
- [ ] Penawaran hanya yang disebut pengguna; bila belum ada, tertulis asumsi "tanpa penawaran"
- [ ] Tidak ada kata proses (script/file/path) di balasan; maks. 3 pertanyaan di akhir

## Batasan & penanganan error
- **Privasi di rekap:** di ringkasan/daftar pelanggan yang ditulis ke chat, tulis nomor HP tersamar (mis. 0812-xxxx-3456) dan nama panggilan saja; nomor lengkap hanya di file di komputer pengguna. Setiap varian pesan, termasuk yang tanpa penawaran, wajib berakhir dengan kalimat opt-out ("balas stop").

- **Kolom wajib kurang** (nama, nomor, tanggal beli terakhir, total belanja): sebutkan kolom yang kurang dan kolom yang ada; tetap beri alur + template, tanya di akhir.
- **Baris rusak** (tanggal tidak ada di kalender, tanggal masa depan, nomor salah/format ilmiah Excel, total bukan angka) tidak dipakai; sebutkan jumlah dan contoh barisnya agar pemilik memperbaiki, jangan menebak. Nomor ganda digabung.
- **Format tanggal** dibaca hari/bulan/tahun (dd/mm/yyyy). Jika data berformat bulan/hari/tahun, minta ekspor ulang.
- **File .xlsx**: minta simpan sebagai CSV. **Semua pelanggan masih aktif**: katakan jujur, tidak ada yang perlu diaktifkan; tawarkan pantau berkala.
- **Tidak ada penawaran dan pemilik ragu**: pesan jujur tanpa penawaran sudah cukup untuk pesan 1 dan 2.
- **Kategori sensitif** (klinik, kesehatan, keuangan): jangan menyebut diagnosis atau riwayat layanan; hanya pengingat umum berupa draf yang dikirim staf.
- **Bukan nasihat hukum.** Dasar hukum ringkas ada di `references/etika-dan-hukum.md` (dicek 2026-10-05).
