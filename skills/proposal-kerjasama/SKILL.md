---
name: proposal-kerjasama
description: Menyusun proposal kerja sama bisnis berbahasa Indonesia (B2B, kemitraan, reseller/agen, konsinyasi/titip jual, sponsorship event, co-branding) versi singkat 1 halaman atau lengkap: ringkasan eksekutif, masalah-solusi, penawaran, manfaat mitra, skema & simulasi angka (dihitung script), timeline, penutup + pesan pengantar WA/email. Gunakan saat pengguna minta proposal kerjasama/kemitraan/sponsor, titip jual ke toko/kafe, atau partnership/sponsorship proposal. Bukan untuk rincian harga item (surat-penawaran-harga) atau kontrak (perjanjian-sederhana).
---

# Proposal Kerja Sama

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Mengubah ide kerja sama yang masih di kepala pengguna menjadi proposal yang meyakinkan calon mitra: jelas apa untungnya bagi **mereka**, bagaimana cara kerjanya, dan langkah berikutnya. Angka simulasi (bagi hasil, margin, konsinyasi) dihitung script, bukan dikira.

## Kapan digunakan
- "Bikin proposal titip jual keripik ke kafe/minimarket."
- "Proposal sponsorship bazar kampus ke brand minuman."
- "Ajukan kerja sama supply kopi ke jaringan kafe" / "cari reseller/agen".
- "Proposal kemitraan katering dengan pabrik/kantor", "co-branding dengan UMKM lain".

## Kapan TIDAK digunakan
- Sekadar daftar harga barang/jasa + PPN → `surat-penawaran-harga`.
- Kontrak/MoU yang akan ditandatangani → `perjanjian-sederhana` (proposal ini bisa jadi bahan awalnya).
- Proposal hibah/pendanaan pemerintah, proposal skripsi, atau business plan investor lengkap: beri kerangka umum saja dan sarankan format resmi pemberi dana.
- Surat undangan/pengantar resmi tanpa isi penawaran → `surat-resmi`.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Siapa pengaju (nama usaha, produk/jasa, keunggulan singkat) | Ya | — (tanyakan) |
| Calon mitra (nama + jenis usaha) | Ya | `[Nama Mitra]` bila belum ditentukan |
| Jenis kerja sama | Ya | Tebak dari konteks; sebutkan asumsi |
| Apa yang diminta dari mitra & apa yang diberikan ke mitra | Ya | — (tanyakan) |
| Angka skema (harga jual, % bagi hasil, harga titip, nilai paket sponsor) | Tidak | Tanpa simulasi angka; tulis `[isi]` |
| Bukti/kredibilitas (lama usaha, jumlah pelanggan, testimoni, follower) | Tidak | Tidak dicantumkan (jangan dikarang) |
| Versi: singkat (1 halaman) atau lengkap | Tidak | Singkat |
| Masa uji coba | Tidak | 3 bulan uji coba lalu evaluasi |
| Kontak PIC | Tidak | `[Nama – WA – email]` |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat, isi dengan default, beri `[isi ...]` pada data spesifik, dan tulis "Asumsi" di akhir.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
0. **Tulis "Fakta dari pengguna" dulu (wajib, sebelum menulis proposal).** Daftar butir yang *benar-benar*
   disebut pengguna, dengan kata-kata pengguna: nama usaha & produk (persis, mis. "kopi susu literan"), kota &
   konteksnya (kota usaha? kota mitra?), angka, klaim yang diminta pengguna, bukti yang dilampirkan. Setiap klaim
   tentang produk, asal, ukuran/kemasan, reputasi ("dikenal", "favorit", "laris"), pasar ("tren terus
   diminati"), legalitas, dan komitmen di proposal **harus bisa ditelusuri ke satu butir di daftar ini**; yang
   tidak ada → hapus, `[isi: ...]`, atau tulis di Asumsi. Simpan salinan persis pesan pengguna sebagai `fakta.txt`.
   Yang paling sering dikarang AI (dilarang):
   - Reputasi/kalimat turunan: "sudah dikenal pelanggan di Solo", "favorit warga", "tren kopi susu terus diminati".
     Klaim yang diminta pengguna ("paling laris se-Solo") ditulis versi lunak + `[isi: bukti]`, bukan diperluas.
   - Ukuran/kemasan: produk "literan" jangan ditulis "botol 250ml"; tulis kata pengguna atau `[isi: ukuran kemasan]`.
   - Sifat produk yang tidak disebut ("rumahan", "tanpa pengawet", "premium") dan kota asal yang hanya kota mitra.
1. **Pahami sudut pandang mitra.** Tulis dulu (untuk diri sendiri) 3 hal yang mitra pedulikan: tambahan pemasukan, risiko kecil, kerja tambahan minimal, citra/brand, kebutuhan pelanggannya. Semua bagian proposal harus menjawab ini.
2. **Pilih kerangka** sesuai jenis kerja sama di `references/kerangka-per-jenis.md` (B2B supply, konsinyasi, reseller/agen, sponsorship, co-branding/kolaborasi).
3. **Hitung simulasi angka dengan script** bila ada angka (path relatif terhadap folder SKILL.md ini; Windows: `python`/`py`):
   ```bash
   # Konsinyasi (toko dapat 20% atau pakai --harga-titip), 3 skenario penjualan per bulan
   python3 <folder-skill-ini>/scripts/hitung_skema.py konsinyasi --harga-jual "Rp 25.000" --porsi-toko 20% --modal 14000 --skenario "50;100;200"
   # Bagi hasil (dasar omzet atau laba)
   python3 <folder-skill-ini>/scripts/hitung_skema.py bagi-hasil --porsi-mitra 30% --dasar omzet --skenario "10jt;25jt;50jt"
   # Reseller (harga jual yang disarankan/HET-SRP vs harga reseller)
   python3 <folder-skill-ini>/scripts/hitung_skema.py reseller --het 150000 --diskon-reseller 20% --modal 90rb --skenario "20;50;100"
   ```
   - Pisahkan skenario dengan `;` (maks. 5), mis. `"50;100;200"`. Label otomatis: Pesimis/Realistis/Optimis. Input ambigu seperti `30,60` ditolak script dengan pesan `ambigu` — tulis ulang dengan `;`.
   - Ada `test_hitung_skema.py` di folder `scripts/` untuk uji regresi (opsional, `python3 scripts/test_hitung_skema.py`).
   - Tabel "Bagian toko/mitra" masuk ke proposal; kolom modal/laba produsen **hanya untuk pengguna**, jangan dimasukkan ke proposal kecuali pengguna minta.
   - **Saran porsi bagi hasil/komisi/diskon wajib dicek dengan hitungan untung/rugi eksplisit** sebelum disarankan atau dituliskan, dan tampilkan titik impasnya ke pengguna: porsi maksimal mitra/toko agar pemilik tidak rugi = (harga jual − modal) ÷ harga jual (mis. Rp20.000, modal Rp14.000 → 30% = impas, laba Rp0). Jangan menyarankan porsi yang sama dengan atau di atas titik impas; jalankan script dengan porsi yang disarankan dan pastikan laba per unit > 0 (tabel laba hanya untuk pengguna). Untuk bagi hasil laba/reseller, hitung juga margin pemilik/reseller per unit pada porsi tersebut.
   - Jika script menampilkan `PERINGATAN` (skema rugi), sampaikan ke pengguna sebelum menulis proposal.
   - Sponsorship: nilai paket biasanya angka tetap; tidak perlu script kecuali ada potongan/perhitungan. Jika menjumlahkan beberapa paket, jumlahkan manual dan tulis rinciannya.
4. **Tulis proposal** dengan format di bawah. Versi singkat ≤ ±350 kata; versi lengkap boleh 2–5 halaman.
5. **Buat pesan pengantar** WA (≤ 8 baris) dan subjek + isi email singkat untuk mengirim proposal.
6. **Cek-silang fakta dengan script (wajib bila Python bisa jalan).** Simpan proposal + pesan WA + email ke
   `proposal.md` (di folder kerja), lalu:
   ```bash
   python3 <folder-skill-ini>/scripts/cek_fakta.py --teks-file proposal.md --fakta-file fakta.txt --abaikan jam
   ```
   `fakta.txt` = salinan **persis** pesan pengguna (bukan ringkasan, jangan ditambah). GAGAL ditandai untuk
   klaim reputasi/pasar/sifat/label/layanan, asal produk, ukuran/kemasan, dan angka kredibilitas (jumlah
   pelanggan, "sejak 2019") yang tidak ada di fakta. **Semua GAGAL wajib diperbaiki**, lalu jalankan ulang
   sampai `HASIL: LULUS`. CEK = klaim dari pengguna yang belum ada `[isi: bukti]`. Tanpa Python: lakukan
   cek-silang manual memakai checklist "Cek-silang fakta" di bawah.
7. **Periksa** dengan checklist; tawarkan versi lain (singkat ↔ lengkap, lebih formal, bahasa Inggris).

### Fallback jika Python tidak bisa dijalankan
Hitung manual dan tulis rumusnya; beri tahu pengguna "angka dihitung manual, mohon dicek":
- Konsinyasi: bagian toko = harga jual × % toko × jumlah terjual (atau (harga jual − harga titip) × jumlah); bagian pemilik = omzet − bagian toko (agar selalu menjumlah tepat).
- Bagi hasil: bagian mitra = dasar (omzet/laba) × % mitra; sisanya pemilik usaha.
- Reseller: harga reseller = harga jual yang disarankan (HET/SRP) × (100% − diskon); untung reseller/unit = HET/SRP − harga reseller.
- Bulatkan ke rupiah terdekat (0,5 ke atas).

## Format output
**Versi singkat (1 halaman):**
```
# Proposal Kerja Sama [Jenis] – [Usaha Pengaju] × [Nama Mitra]

**Ringkasan:** [2–3 kalimat: siapa kami, apa yang ditawarkan, untung utama bagi mitra.]

**Peluang untuk [Mitra]:** [1 paragraf: masalah/kebutuhan mitra atau pelanggannya.]

**Yang kami tawarkan:**
- ...

**Skema kerja sama:**
- [Cara kerja 3–5 poin: alur barang/uang, periode pembayaran, retur, tanggung jawab]
- [Tabel simulasi dari script, bila ada]

**Manfaat untuk [Mitra]:**
- ...

**Langkah berikutnya:** [uji coba X bulan mulai ..., ajakan bertemu/diskusi]

Kontak: [Nama] – [Jabatan] – WA [..] – [email]
```

**Versi lengkap**, urutan bagian:
1. Sampul (judul, nama mitra, tanggal, logo `[logo]`)
2. Ringkasan eksekutif (≤ 1/2 halaman — ditulis terakhir, diletakkan pertama)
3. Tentang kami (profil singkat, bukti kredibilitas yang **diberikan pengguna**)
4. Latar belakang: masalah/peluang mitra
5. Solusi & penawaran
6. Manfaat untuk mitra (poin konkret, angka jika ada)
7. Skema kerja sama (alur, pembagian peran, pembayaran, retur/klaim, laporan) + tabel simulasi
8. Timeline pelaksanaan (tabel minggu/bulan)
9. Evaluasi & ukuran keberhasilan (KPI sederhana)
10. Penutup + langkah berikutnya + kontak
11. Lampiran (katalog, foto, legalitas — hanya jika pengguna punya: NIB, sertifikat, dsb.)

Setelah proposal, beri **Pesan pengantar WA** dan **Email (subjek + isi)**, lalu **Asumsi** (jika ada).

## Contoh
**Input pengguna:** "Aku punya usaha keripik singkong pedas 'Kriuk Mbok Darmi' di Bantul, mau titip jual di 5 cabang Kopi Senja Jogja. Harga jual 25rb/bungkus, toko dapat 20%. Modalku 14rb. Buat versi singkat."

**Fakta dari pengguna:** keripik singkong pedas "Kriuk Mbok Darmi" · di Bantul · titip jual di 5 cabang Kopi Senja Jogja · harga jual 25rb/bungkus · toko 20% · modal 14rb · versi singkat.

**Output (ringkas):** script konsinyasi skenario 50/100/200 bungkus per cabang per bulan → bagian toko Rp 250.000 / Rp 500.000 / Rp 1.000.000 per cabang. Proposal singkat:
```
# Proposal Kerja Sama Titip Jual – Kriuk Mbok Darmi × Kopi Senja Jogja

**Ringkasan:** Kriuk Mbok Darmi, keripik singkong pedas dari Bantul, ingin menitipkan produk di 5 cabang Kopi Senja. Kopi Senja mendapat 20% dari setiap bungkus terjual tanpa modal stok, dan pelanggan punya camilan pendamping kopi.

**Skema kerja sama:**
- Kami antar stok awal 30 bungkus/cabang dan mengisi ulang tiap minggu.
- Harga jual Rp 25.000/bungkus; Kopi Senja mendapat Rp 5.000 (20%) per bungkus terjual.
- Rekap & pembayaran setiap akhir bulan; produk mendekati kedaluwarsa/rusak kami tarik dan ganti tanpa biaya.
- Display toples kecil kami sediakan.

| Penjualan per cabang/bulan | 50 | 100 | 200 |
|---|---|---|---|
| Pendapatan Kopi Senja per cabang | Rp 250.000 | Rp 500.000 | Rp 1.000.000 |

**Langkah berikutnya:** uji coba 3 bulan di 2 cabang mulai [tanggal], lalu evaluasi bersama.
```
(Tabel modal/laba Rp 6.000 per bungkus hanya ditunjukkan ke pengguna, tidak masuk proposal.)
Asumsi yang disebut di akhir: stok awal 30 bungkus/cabang, isi ulang mingguan, display disediakan, uji coba 3 bulan di 2 cabang — konfirmasi ke pengguna.

## Cek-silang fakta (wajib, sebelum mengirim)
Telusuri setiap kalimat proposal, pesan WA, email, dan Asumsi terhadap daftar "Fakta dari pengguna":
- [ ] Nama & jenis produk, kemasan/ukuran persis kata pengguna (tidak ada "250ml"/"500gr" yang tidak disebut)
- [ ] Tidak ada reputasi/pasar turunan ("sudah dikenal di …", "favorit …", "tren … terus diminati") tanpa butir fakta
- [ ] Klaim yang diminta pengguna tanpa bukti (BPOM, terlaris) memakai versi lunak + `[isi: bukti]`
- [ ] Kota hanya dipakai dalam konteks yang disebut pengguna (kota mitra ≠ kota asal produk)
- [ ] `cek_fakta.py` menulis `HASIL: LULUS` (atau cek manual sudah dilakukan dan disebut ke pengguna)

## Checklist sebelum mengirim hasil
- [ ] Setiap bagian menjawab "apa untungnya untuk mitra", bukan hanya memuji produk sendiri.
- [ ] Angka dari output script (atau hitung manual tertulis + peringatan); tidak ada angka yang dikarang.
- [ ] Tidak ada klaim yang tidak diberikan pengguna (halal, BPOM, SNI, "terlaris", jumlah pelanggan, follower), termasuk klaim turunan ("dikenal luas di ...", "tren terus diminati"). Bila pengguna meminta klaim yang belum terbukti, tulis versi lunak + `[isi: bukti]`.
- [ ] Porsi/komisi yang disarankan sudah dicek untung-rugi dan titik impasnya disebut ke pengguna.
- [ ] Komitmen operasional default (display, stok awal, isi ulang) tercantum di Asumsi.
- [ ] Skema jelas: alur barang & uang, jadwal bayar, retur/klaim, siapa menanggung apa.
- [ ] Ada langkah berikutnya yang konkret (uji coba, jadwal meeting) dan kontak.
- [ ] Data internal (modal, laba) tidak bocor ke proposal kecuali diminta.
- [ ] Panjang sesuai versi (singkat ≤ ±350 kata).

## Batasan & penanganan error
- Proposal bukan kontrak. Ingatkan: setelah mitra setuju, tuangkan dalam perjanjian tertulis (skill `perjanjian-sederhana`); perjanjian dikenai bea meterai Rp10.000 (UU 10/2020).
- Jangan menjanjikan hasil penjualan pasti; tabel simulasi selalu diberi label "simulasi/perkiraan".
- Sponsorship: jangan mengarang jumlah pengunjung/peserta/reach; minta data atau tulis `[perkiraan peserta]`.
- Konsinyasi/penjualan bila salah satu pihak PKP: ada aspek PPN atas penyerahan barang titipan; sarankan konsultasi ke konsultan pajak (skill tidak menghitungnya).
- Kerja sama yang menyangkut izin khusus (pangan olahan, obat, kosmetik, alkes, keuangan/investasi, waralaba): sarankan pengguna memastikan izin terkait sendiri; skill tidak menilai legalitas.
- Skema yang terlihat seperti investasi dengan janji imbal hasil tetap dari dana publik: jangan dibantu menjadi penawaran ke masyarakat umum; sarankan konsultasi hukum (terkait ketentuan OJK).
