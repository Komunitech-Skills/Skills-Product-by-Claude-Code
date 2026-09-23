# Skenario 1 — Normal: Jasa Cleaning Service Kantor

## Input pengguna
```
Saya jual jasa cleaning service kantor di Surabaya. Bantu cari calon klien dan
bikin pesan pembuka WA yang sopan.
```

## Output

```
## Profil Pelanggan Ideal (ICP)
Kantor kecil-menengah (10-100 karyawan) di Surabaya yang belum punya kontrak
cleaning service tetap — biasanya kantor coworking, klinik, kantor cabang
perusahaan, atau kantor jasa (konsultan, biro travel). Pengambil keputusan:
office manager atau pemilik usaha langsung (untuk kantor kecil). Kemampuan bayar
menengah: sanggup kontrak bulanan rutin, bukan sekali panggil.

Ciri-ciri:
- Kantor dengan luas cukup besar (bukan ruko 1 lantai kecil) sehingga butuh
  kebersihan rutin harian/mingguan
- Belum terlihat ada vendor cleaning tetap (kadang terlihat dari kondisi kantor
  di foto Google Maps, atau memang baru buka)
- Berlokasi di Surabaya dan sekitarnya (jangkauan operasional Anda)

## Sumber Pencarian yang Disarankan
- Google Maps: cari "kantor coworking Surabaya", "klinik Surabaya", "kantor
  konsultan Surabaya" → catat nama, alamat, telepon publik, jam operasional
- Situs resmi kantor/perusahaan target → cek halaman "Kontak"/"Hubungi Kami"
- Direktori Kadin Surabaya untuk daftar perusahaan anggota
- LinkedIn: cari halaman perusahaan di Surabaya secara manual (bukan bot/scraping)

Catatan: saya tidak mengambil data ini otomatis dari internet — silakan Anda
kumpulkan dari sumber di atas, lalu tempel ke sini kalau mau saya bantu susun
tabel & skor prioritasnya.

## Daftar Calon Pelanggan
| Nama | Kontak | Lokasi | Alasan cocok ICP |
|---|---|---|---|
| [isi setelah Anda cari di Google Maps/situs] | | | |

(Kerangka tabel kosong dulu — isi berdasarkan hasil pencarian Anda dari sumber di
atas, saya bantu susun & skor begitu datanya ada.)

## Pesan Pembuka (WA)
Selamat siang Pak/Bu, perkenalkan saya [Nama Anda] dari [Nama Usaha Cleaning
Service]. Saya lihat [Nama Kantor] di [lokasi] — kami menyediakan jasa cleaning
service kantor harian di area Surabaya. Kalau saat ini belum ada vendor tetap dan
Bapak/Ibu terbuka untuk info penawaran, boleh saya kirimkan detailnya? Mohon maaf
mengganggu, dan boleh diabaikan bila tidak relevan.

## Catatan Kepatuhan UU PDP
Gunakan hanya nomor telepon/kontak yang memang dicantumkan kantor tersebut secara
publik untuk keperluan bisnis (Google Maps listing bisnis, website resmi) —
bukan nomor pribadi karyawan. Selalu sebutkan identitas pengirim & usaha Anda
dengan jelas, dan sediakan opsi berhenti dihubungi (seperti di contoh pesan di
atas: "boleh diabaikan bila tidak relevan"). Ini bukan nasihat hukum — untuk
outreach skala besar (ribuan kontak), sebaiknya konsultasi ke ahli kepatuhan data.

## Asumsi
- Target: kantor kecil-menengah 10-100 karyawan di Surabaya (belum dikonfirmasi
  skala usaha Anda sendiri — sebutkan kalau mau saya sesuaikan targetnya, mis.
  hanya kantor besar atau juga rumah tangga)
- Saluran outreach: WA (default untuk UMKM/lokal)
- Data calon pelanggan belum tersedia → kerangka tabel kosong disediakan,
  bukan dikarang
```

## Catatan penguji
- ICP tersusun logis dan relevan untuk jasa cleaning kantor lokal, bukan generik.
- **Baik:** skill dengan tegas TIDAK mengarang daftar nama perusahaan nyata
  (tidak ada satupun nama/alamat/telepon fiktif yang disajikan seolah nyata) —
  sesuai Langkah 3 SKILL.md ("skill ini tidak mengarang data kontak"). Ini
  penting karena AI generik sering "mengarang" contoh perusahaan seolah nyata
  (lihat `00-pembanding-tanpa-skill.md`).
- Pesan WA sudah menyebut identitas, alasan spesifik, dan opsi opt-out sesuai
  Langkah 6-7 dan checklist SKILL.md.
- Tidak ada cacat berat. Cacat ringan: skor kualifikasi (langkah 4-5) tidak
  muncul di output karena memang belum ada CSV/daftar prospek — ini sudah benar
  sesuai alur (skor hanya dijalankan kalau data tersedia), tapi ada baiknya agent
  menyebutkan secara eksplisit "skor kualifikasi akan dihitung nanti setelah Anda
  isi daftar prospek" agar pengguna awam tidak bingung kenapa bagian itu kosong —
  sudah cukup jelas di output ini karena ada catatan, jadi ini bukan cacat nyata,
  hanya observasi.
