# HASIL UJI - program-referral-loyalitas v1.0.0

- **Tanggal:** 2026-09-30
- **Penguji:** agent independen (bukan pembuat), hanya membaca folder skill + CLAUDE.md. Skill disalin ke scratchpad `.../scratchpad/uji-referral/`, tidak dipasang di `.claude/skills` repo.
- **Platform:** claude-code (simulasi agent). Uji muat OpenClaw otomatis: lihat bawah.

## 1. Ringkasan
| Uji | Hasil |
|---|---|
| 06 normal: toko hijab Shopee + WA | Lulus. Semua angka cocok; aturan Shopee (tanpa ajakan pindah transaksi) ditangani |
| 07 normal: kafe poin + stempel + traktir teman | Lulus dengan catatan: **jumlah poin `52.340` ditolak** (lihat T1) |
| 08 normal: les privat, referral orang tua | Lulus; data anak tidak disebut skill (R3) |
| 09 input tidak lengkap: salon | Lulus: bertanya sekali (5 butir), jalur cepat dengan asumsi berlabel, angka ambigu ditolak |
| 10 di luar cakupan: blast 5.000 nomor + MLM 3 level + janji penghasilan | Lulus: ditolak sopan dengan dasar UU, alternatif reseller satu tingkat |
| A/B (`00-pembanding-tanpa-skill.md`) | Dengan skill jauh lebih baik (tanpa skill lupa biaya kartu, menyarankan broadcast) |
| Banding pesaing (`00-banding-pesaing.md`) | Skill kita 33/35 vs `referrals` (marketingskills) 12/35: menang telak |
| `tests/uji_regresi.py` | 26 tes OK |
| `python3 scripts/validate.py --skill program-referral-loyalitas` | ✅ 1 skill valid, 113 baris katalog sesuai |
| `bash scripts/uji_openclaw.sh` (OpenClaw 2026.9.7) | program-referral-loyalitas eligible/modelVisible/commandVisible. Skrip keseluruhan gagal hanya karena `odoo-usaha` (skill lain, belum di katalog), bukan skill ini |

## 2. Verifikasi angka independen
Dihitung ulang dengan `fractions.Fraction` (script penguji terpisah, bukan kode skill). Semua cocok:
- Hijab 180rb/40%/15rb+15rb: LPO Rp72.000, biaya Rp30.000 (16,67% / 41,67%), sisa Rp42.000, kuota Rp600.000 = 20, LTV Rp432.000, batas aman Rp129.600; simulasi 850 pelanggan: 43/43/9, 85/170/43, 128/256/77 pembeli; biaya Rp270.000 / Rp1.290.000 / Rp2.310.000; laba kotor (1 ulang) Rp1.296.000 / Rp6.192.000 / Rp11.088.000.
- Hijab 145rb/38%/20rb+10%+1.500: LPO Rp55.100, biaya Rp36.000 (24,83% / 65,34%), sisa Rp19.100, kuota 20, batas Rp99.180, pemberi maks Rp83.180; opsi 50rb+20% = Rp79.000, -Rp23.900; ROI 206,11%.
- Hadiah 10%: Rp18.000; 25 referral + biaya lain 2.500 = Rp962.500, sisa anggaran Rp37.500.
- Kafe: 3 poin/Rp900 (2,34%), LPO Rp25.025, liability 52.340 poin = Rp15.702.000, x75% = Rp11.776.500, biaya poin Rp1.350.000 / Rp1.012.500, porsi margin 4,62%; stempel 4,02% / 6,18%; traktir Rp9.000 (23,38% / 35,96%), LTV 18 pesanan Rp450.450, batas Rp135.135.
- Les: biaya Rp250.000 (20,83% / 41,67%), sisa Rp350.000, kuota 6, LTV Rp4.800.000, batas Rp1.440.000; simulasi 6/6/2 dan 12/12/5, laba kotor (5 ulang) Rp7.200.000 / Rp18.000.000.
- Poin rugi (margin 30%, 1 poin Rp3.000): 100% margin -> RUGI; 8 poin Rp24.000; laba sisa Rp1.500; liability Rp120.000.000, x80% Rp96.000.000.
- Impas hadiah Rp210.000 vs LPO Rp33.000: ceil(6,36) = pesanan ke-7. Hadiah Rp1.200.000: ceil(35,36) = 36 pesanan ulang.

## 3. Uji ekstrem & rusak (script)
Ditolak dengan `GAGAL` kode 2 dan pesan awam (benar): margin negatif/0/100/99,5; AOV 0 / Rp0 / `abc` / `12.5` (ambigu); hadiah 150%; frekuensi 0; porsi 0; pelanggan 0; jumlah referral pecahan; skenario format salah / 110%; breakage 100%; belanja per poin 0; nilai poin 0; minimum tukar 0; poin beredar negatif; AOV Rp1 margin 1% (laba Rp0). Argumen wajib hilang/perintah salah: pesan argparse (bahasa Inggris, kode 2).
Diterima dengan PERHATIAN (benar): hadiah > laba pesanan pertama; hadiah > laba seumur (TIDAK DISARANKAN); poin = margin (RUGI); poin > nilai belanja (120%, RUGI); breakage 99%; AOV kecil -> 0 poin; poin beredar 0.

## 4. Temuan

### TINGGI
**T1. Jumlah (bukan rupiah) dengan pemisah ribuan titik dibaca salah - bisa diam-diam 1.000x lebih kecil.** `parse_angka` mengganti koma menjadi titik lalu membaca `40.000` sebagai 40,000 = 40. Berlaku untuk `--poin-beredar`, `--pelanggan-aktif`, `--jumlah-referral`, `--minimum-tukar`, `--umur-bulan`, `--frekuensi-bulan`. SKILL.md sendiri mengajarkan "uang boleh ditulis `60.000`", sehingga agent wajar meneruskan `52.340` / `40.000`.
Bukti:
```
$ python3 scripts/hitung_referral.py poin --belanja-per-poin 10rb --nilai-poin 300 --margin 65 --poin-beredar 40.000
LIABILITY (kewajiban) poin beredar 40 poin: maksimal Rp12.000 bila semua ditukar.      <- seharusnya 40.000 poin, Rp12.000.000
$ ... simulasi --pelanggan-aktif 2.000 ...   -> "2 pelanggan aktif", 0 pembeli
$ ... biaya --jumlah-referral 1.000 ...      -> "Program 1 referral berhasil"
$ ... poin --minimum-tukar 1.000 ...         -> "Minimum tukar 1 poin"
$ ... poin --poin-beredar 52.340             -> GAGAL: poin beredar harus bilangan bulat (didapat 52.340)   <- membingungkan
$ ... impas --umur-bulan 1.000               -> 1 bulan, status PERHATIAN
```
Perbaikan usulan: untuk argumen bilangan bulat (orang/poin/kali), terima `\d{1,3}(\.\d{3})+` sebagai ribuan; untuk argumen desimal (frekuensi), tolak pola ribuan yang ambigu seperti `1.000` atau minta koma desimal; tambah tes regresi `40.000 -> 40000`, `2.000 -> 2000`, `52.340 -> 52340`. Tambahkan juga baris di SKILL.md: "jumlah poin/orang boleh ditulis 40.000 atau 40000".

**T2. Pola klinik: aturan iklan pelayanan kesehatan belum dirujuk; hadiah referral klinik kemungkinan termasuk promosi penjualan yang dilarang.** Permenkes 1787/MENKES/PER/XII/2010 tentang Iklan dan Publikasi Pelayanan Kesehatan, Pasal 5, melarang iklan/publikasi fasilitas pelayanan kesehatan yang "mengiklankan promosi penjualan dalam bentuk apa pun termasuk pemberian potongan harga (diskon), imbalan atas pelayanan kesehatan dan/atau menggunakan metode penjualan multi-level marketing" (dikutip via Klinik Hukumonline; teks resmi kms.kemkes.go.id). `references/pola-per-usaha.md` bagian Klinik dan `examples/03-klinik-gigi-referral-non-medis.md` menganjurkan kartu ajakan berhadiah produk "non-medis" untuk pasien; walau ditandai PERLU REVIEW, skill tidak menyebut aturan ini sehingga pembeli awam bisa mengira hadiah non-medis sudah aman. Penguji belum memverifikasi apakah Permenkes ini sudah diganti aturan turunan UU 17/2023 Kesehatan.
Perbaikan usulan: untuk klinik/fasyankes, default = **tanpa hadiah referral**; ganti dengan edukasi, pengingat kontrol (draf dikirim staf), dan kartu info tanpa insentif. Hadiah hanya setelah pemilik klinik memastikan ke dinas kesehatan/organisasi profesi. Cantumkan Permenkes 1787/2010 Pasal 5 + tanggal cek, tandai PERLU REVIEW tenaga medis/hukum. Revisi `examples/03`.

### SEDANG
**S1. Status `impas` "AMAN" muncul bersamaan dengan rugi di pesanan pertama.** Contoh: 145rb/38%, hadiah Rp50.000 + 20% = Rp79.000 (-Rp23.900 di pesanan pertama) tetap "AMAN" terhadap batas Rp99.180; `examples/01` menulis status AMAN untuk opsi rugi Rp8.000. Script `biaya` sudah memberi PERHATIAN, tetapi label tunggal "AMAN" mudah disalahpahami awam. Usulan: status "AMAN (rugi di pesanan pertama, balik modal di pesanan ke-N)" bila `laba_setelah < 0`.

**S2. Baris "Hadiah pemberi maksimal" bisa dibaca sebagai anjuran menaikkan hadiah** (mis. Rp1.290.000 untuk les, Rp114.600 untuk hijab, padahal laba pesanan pertama hanya Rp72.000). `pola-per-usaha.md` (laundry) juga menulis "masih ada ruang untuk hadiah lebih menarik". Usulan: tulis "batas atas teoretis, bukan anjuran" di output dan batasi juga dengan laba pesanan pertama.

### RENDAH
- R1. Pesan galat persen tercetak ganda: `hadiah teman 150%% di luar batas wajar`.
- R2. `biaya --anggaran 1rb` dengan biaya Rp0: anggaran diam-diam diabaikan (tidak ada baris anggaran).
- R3. Skill tidak menyebut data anak (UU 27/2022 Pasal 25, persetujuan orang tua) untuk les/bimbel/PAUD.
- R4. `simulasi` menghitung omzet dari nilai pesanan penuh walau teman mendapat diskon (laba sudah benar). ROI selalu sama di tiap skenario (sifat rumus); bisa disebutkan agar tidak dikira "ROI tidak bergantung jumlah".
- R5. Kedaluwarsa poin hanya lewat `--breakage` (perkiraan); tidak ada perhitungan masa berlaku. Cukup untuk UMKM.
- R6. Pesan argparse (argumen hilang/perintah salah) berbahasa Inggris.
- R7. Pesaing punya saran uji A/B hadiah (nominal vs persen); skill bisa menambah satu butir di rencana 30 hari.

## 5. Etika & kepatuhan
- Tanpa blast/spam: lulus (SKILL.md, template, contoh 05 & 10; "balas STOP", tidak meminta nomor teman).
- Hadiah tidak menyesatkan: lulus (UU 8/1999; larangan "gratis" bersyarat tersembunyi, kuota ditulis).
- UU PDP: lulus (data minimal, tujuan, penghapusan, tidak dibagikan); kurang data anak (R3).
- Klinik non-medis: **belum cukup** (T2).
- Beda dari MLM/piramida: lulus (satu tingkat, dari penjualan nyata, tanpa biaya daftar; UU 7/2014).
- Keamanan script: hanya Python standar, tanpa jaringan/berkas/eksekusi eksternal; aman.

## 6. Skor: **6/10 -> REVISI** (jangan naik ke `lulus`)
Alasan: isi, struktur, lokalisasi, dan akurasi rumus sangat baik (A/B dan banding pesaing menang telak; semua angka valid cocok hitungan independen), tetapi (T1) script bisa **diam-diam** memberi liability/simulasi 1.000x lebih kecil dari input format Indonesia yang wajar, bertentangan dengan prinsip "reliable", dan (T2) pola klinik belum menyebut larangan promosi penjualan di iklan pelayanan kesehatan. Keduanya mudah diperbaiki; setelah T1 + T2 (+S1/S2) diperbaiki dan diuji ulang oleh penguji independen, perkiraan skor 8,5-9.

## 7. File uji
`00-pembanding-tanpa-skill.md`, `00-banding-pesaing.md`, `06-uji-toko-hijab-shopee-wa.md`, `07-uji-kafe-poin-stempel.md`, `08-uji-les-privat-referral-orang-tua.md`, `09-uji-input-kurang-salon.md`, `10-uji-di-luar-cakupan-blast-mlm.md`.

Sumber rujukan T2: https://www.hukumonline.com/klinik/a/ketentuan-iklan-pelayanan-kesehatan-alternatif-di-televisi-lt5ad4049e8a0df/ ; https://kms.kemkes.go.id/contents/1715917225382-bukuperaturaniklanpublikasikes.pdf
