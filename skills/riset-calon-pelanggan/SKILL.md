---
name: riset-calon-pelanggan
description: Membantu UMKM/B2B menentukan profil pelanggan ideal (ICP), menyusun daftar calon pelanggan dari sumber publik & sah (situs perusahaan, Google Maps, direktori Kadin/asosiasi, marketplace B2B, LinkedIn — tanpa scraping login/beli database), menghitung skor kualifikasi prospek dari CSV (cocok ICP, kebutuhan, kemampuan bayar, akses PIC) lewat script, dan menyusun pesan pembuka personal WA/email/LinkedIn yang patuh UU PDP. Gunakan saat pengguna minta cari calon pelanggan, lead generation, ideal customer profile, daftar prospek B2B, atau qualify leads. Untuk prospek yang SUDAH dihubungi → follow-up-prospek; untuk menyusun penawaran resmi → proposal-kerjasama / surat-penawaran-harga.
---

# Riset Calon Pelanggan (ICP & Prospecting)

## Tujuan
Membantu pemilik usaha/tim sales menemukan calon pelanggan yang tepat: menentukan profil pelanggan ideal (ICP), menyusun daftar calon pelanggan dari sumber publik yang sah, mengurutkan prospek mana yang paling layak dihubungi dulu (skor kualifikasi lewat script), dan menyiapkan pesan pembuka yang sopan serta patuh UU PDP.

## Kapan digunakan
- "Bantu saya cari calon pelanggan untuk jasa laundry kiloan di area Bandung"
- "Siapa target pasar ideal untuk software kasir buat resto?"
- "Saya punya daftar 30 perusahaan di CSV, mana yang paling prioritas dihubungi?"
- "Bikinkan pesan pembuka WA buat kenalan ke calon klien baru, sopan dan nggak spam"
- "Bantu susun ICP untuk produk kemasan makanan ramah lingkungan"

## Kapan TIDAK digunakan
- Prospek yang **sudah** dihubungi dan sedang ditindaklanjuti (belum balas, minta waktu, dll.) → `follow-up-prospek`.
- Menyusun proposal kerja sama resmi setelah prospek tertarik → `proposal-kerjasama`.
- Menyusun surat penawaran harga formal → `surat-penawaran-harga`.
- Pengguna minta **scraping otomatis** (bot login LinkedIn/marketplace, ambil data massal lewat akun pribadi), **membeli database kontak**, atau sumber yang melanggar Terms of Service → tolak dengan sopan, jelaskan risikonya (blokir akun, pelanggaran hukum, kualitas data buruk), tawarkan cara manual/sah sebagai gantinya.
- Broadcast pesan massal ke banyak kontak sekaligus tanpa personalisasi → `broadcast-wa` (dan tetap ingatkan aturan UU PDP di sana).

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Produk/jasa yang dijual | Ya | — (tanyakan) |
| Target pasar kasar (B2B/B2C, industri, area) | Tidak | Tanyakan singkat jika sangat menentukan hasil |
| Sudah punya ICP jelas, atau minta dibantu susun? | Tidak | Bantu susun ICP dulu dari jawaban pengguna |
| Sudah punya daftar calon pelanggan (CSV/teks), atau minta arahan sumber pencarian? | Tidak | Beri arahan sumber pencarian manual bila belum ada |
| Skala usaha & kapasitas layanan (biar nggak salah target terlalu besar/kecil) | Tidak | Tanyakan singkat |
| Saluran outreach: WA, email, LinkedIn | Tidak | WA untuk UMKM/lokal, email+LinkedIn untuk B2B/korporat |
| Nama & gaya bahasa pengirim | Tidak | Sopan semi-formal |

Jika info wajib kurang, tanyakan **sekali** (maks. 5 pertanyaan bernomor). Jika pengguna ingin cepat, pakai asumsi masuk akal dan sebutkan di akhir.

## Langkah kerja

1. **Susun atau konfirmasi ICP (Ideal Customer Profile).** Bantu pengguna menjawab: siapa yang paling diuntungkan produk/jasa ini, seberapa besar usahanya (omzet/jumlah karyawan/skala), di mana lokasinya, masalah apa yang mereka punya, siapa pengambil keputusan (owner/manajer/divisi apa), dan berapa kira-kira kemampuan bayar mereka. Tulis ICP dalam 1 paragraf ringkas + daftar ciri (bullet).

2. **Arahkan sumber pencarian yang publik & sah** (lihat `references/sumber-pencarian.md` untuk detail per kategori):
   - Situs resmi perusahaan target dan halaman "Tentang Kami"/kontak
   - Google Maps (cari kategori usaha + area, catat nama, alamat, telepon publik, jam operasional)
   - Direktori asosiasi/Kadin, komunitas bisnis, atau direktori industri
   - Marketplace B2B (Indotrading, Ralali, dll.) untuk supplier/pembeli
   - LinkedIn (pencarian manual profil/perusahaan yang publik — **bukan** scraping otomatis atau bot koneksi massal)
   - Jangan pernah menyarankan membeli database kontak, scraping berlogin, atau bot otomatis yang melanggar ToS platform.

3. **Bantu susun daftar calon pelanggan** dalam tabel (nama usaha, kontak jika ada, lokasi, alasan cocok ICP) berdasarkan data yang pengguna kumpulkan sendiri atau tempel ke percakapan. Skill ini **tidak mengarang data kontak** — jika pengguna belum punya data nyata, bantu susun kerangka tabel kosong + panduan cara mengisi dari sumber di atas.

4. **Hitung skor kualifikasi** dengan script jika pengguna sudah punya daftar prospek dalam CSV berisi penilaian 0–5 untuk: kecocokan ICP, kejelasan kebutuhan, kemampuan bayar, dan akses ke pengambil keputusan (PIC). Jika pengguna belum menilai, bantu dia menilai tiap prospek dulu (boleh estimasi kasar, sebutkan itu estimasi) sebelum dimasukkan ke CSV.

5. **Urutkan hasil**: kategori **Panas** (segera hubungi), **Hangat** (follow lanjutan, isi data dulu), **Dingin** (prioritas rendah/lewati dulu).

6. **Susun pesan pembuka personal** untuk prospek kategori Panas/Hangat: sebutkan alasan menghubungi yang spesifik (bukan template generik), sebutkan dari mana info kontak didapat bila relevan (transparansi), cantumkan cara opt-out sederhana ("boleh diabaikan jika tidak relevan / balas STOP jika tidak ingin dihubungi lagi"), dan **jangan** menjanjikan hal yang belum pasti.

7. **Ingatkan aturan UU PDP** setiap kali menyusun pesan outreach: gunakan data kontak yang memang **dipublikasikan sendiri oleh pihak tersebut untuk tujuan bisnis** (situs resmi, listing Google Maps bisnis, direktori publik) sebagai dasar pemrosesan wajar (legitimate interest bisnis), bukan data pribadi individu yang didapat tanpa konteks bisnis; sertakan identitas pengirim yang jelas dan opsi berhenti dihubungi.

### Menjalankan skor kualifikasi (script)
Path relatif terhadap folder yang berisi SKILL.md ini. Di Windows, ganti `python3` dengan `python` atau `py`.

```bash
python3 <folder-skill-ini>/scripts/skor_prospek.py daftar_prospek.csv \
  --kolom-nama "Nama Perusahaan" --kolom-cocok-icp "Cocok ICP" \
  --kolom-kebutuhan "Kebutuhan" --kolom-kemampuan-bayar "Kemampuan Bayar" \
  --kolom-akses-pic "Akses PIC"
```
- Tiap kolom skor diisi angka **0–5** (perkiraan pengguna/tim sales, bukan dihitung otomatis dari internet).
- Bobot default: cocok ICP 30%, kebutuhan 30%, kemampuan bayar 20%, akses PIC 20%. Ubah dengan `--bobot cocok,kebutuhan,bayar,akses` (total harus 1.0) jika prioritas bisnis pengguna berbeda.
- Delimiter `,` `;` atau tab dan encoding Excel terdeteksi otomatis. Baris dengan nama kosong atau nilai di luar 0–5/bukan angka **dilewati**, bukan ditebak — jumlahnya dilaporkan di `baris_dilewati`.
- Hasil kategori: Panas (skor ≥75), Hangat (50–74), Dingin (<50).
- **Fallback tanpa Python:** hitung manual per prospek: `(cocok_icp×0,3 + kebutuhan×0,3 + bayar×0,2 + akses×0,2) ÷ 5 × 100`, lalu urutkan dari tertinggi. Beri tahu pengguna bahwa ini dihitung manual.

## Format output

```
## Profil Pelanggan Ideal (ICP)
...

## Sumber Pencarian yang Disarankan
- ...

## Daftar Calon Pelanggan
| Nama | Kontak | Lokasi | Alasan cocok ICP |
|---|---|---|---|

## Skor Kualifikasi Prospek
| Nama | Skor | Kategori |
|---|---|---|

### Panas (segera hubungi)
...

## Pesan Pembuka (contoh untuk 1 prospek Panas)
[WA/Email/LinkedIn]
...

## Catatan Kepatuhan UU PDP
...

## Asumsi
- ...
```

## Contoh

**Input pengguna:** "Saya jual jasa cleaning service kantor di Surabaya. Bantu cari calon klien dan bikin pesan pembuka WA yang sopan."

**Output (ringkas):**
```
## Profil Pelanggan Ideal (ICP)
Kantor kecil-menengah (10-100 karyawan) di Surabaya yang belum punya kontrak
cleaning service tetap, biasanya kantor coworking, klinik, atau kantor cabang
perusahaan. Pengambil keputusan: office manager/pemilik usaha.

## Sumber Pencarian yang Disarankan
- Google Maps: cari "kantor coworking Surabaya", "klinik Surabaya" → catat nama & telepon publik
- Direktori Kadin Surabaya untuk daftar perusahaan anggota
...

## Pesan Pembuka (WA)
Selamat siang Pak/Bu, perkenalkan saya [Nama] dari [Usaha]. Saya lihat
[Nama Kantor] di [lokasi] — kami menyediakan jasa cleaning service kantor
harian di area Surabaya. Kalau saat ini belum ada vendor tetap dan Bapak/Ibu
terbuka untuk info penawaran, boleh saya kirimkan detailnya? Mohon maaf
mengganggu, dan boleh diabaikan bila tidak relevan.
```

## Checklist sebelum mengirim hasil
- [ ] Semua sumber data yang disarankan adalah publik & sah (tidak ada scraping login/beli database)
- [ ] Tidak ada data kontak yang dikarang — hanya yang pengguna berikan atau dari sumber publik yang disebut
- [ ] Skor kualifikasi (jika ada CSV) dihitung lewat script, bukan diperkirakan
- [ ] Pesan pembuka menyebut identitas pengirim jelas dan opsi berhenti/abaikan
- [ ] Tidak ada klaim berlebihan atau janji yang belum pasti dalam pesan pembuka
- [ ] Disclaimer UU PDP disampaikan bila pesan menyentuh data kontak pribadi

## Batasan & penanganan error
- Skill ini **tidak melakukan scraping otomatis** ke situs/aplikasi mana pun dan tidak mengakses internet — semua data harus dikumpulkan atau ditempel sendiri oleh pengguna.
- Jika pengguna minta cara mem-bypass login/ToS platform (LinkedIn, marketplace) untuk mengambil data massal, tolak dan jelaskan risikonya (pelanggaran ToS, akun diblokir, berpotensi melanggar UU PDP).
- Jika CSV prospek tidak punya kolom penilaian 0–5, bantu pengguna menilai dulu secara manual (boleh estimasi kasar, sebutkan sebagai estimasi) sebelum dihitung script.
- Angka pasar (jumlah usaha di suatu area, rata-rata budget industri, dll.) tidak boleh dikarang; jika tidak tersedia, sebutkan sebagai "perlu dicek langsung" dan sarankan sumber (BPS, asosiasi industri, riset pasar).
- Untuk penyusunan kontrak/perjanjian kerja sama setelah prospek deal → `proposal-kerjasama` atau `perjanjian-sederhana`, bukan skill ini.
- Jangan mengirim isi file/daftar prospek pengguna ke layanan eksternal mana pun.
