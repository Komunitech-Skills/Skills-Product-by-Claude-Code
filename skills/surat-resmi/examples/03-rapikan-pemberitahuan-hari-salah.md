# Contoh 03 – Merapikan surat pemberitahuan: ejaan tidak baku dan nama hari salah

## Skenario
S3, permintaan normal jenis "rapikan surat sesuai EYD". Pemilik toko grosir menempel draf surat pemberitahuan. Draf ini berisi banyak kesalahan umum: "Kepada Yth. :", "ijin", "Jum'at", "jam 7 pagi", "di-Pekalongan", "Hormat Kami", dan kalimat usang. Nama harinya juga salah: ditulis "Jum'at, 3 Oktober 2026", padahal 3 Oktober 2026 adalah hari Sabtu. Skill harus menangkap kesalahan hari dengan script dan bertanya, bukan menebak. Semua nama fiktif.

## Input pengguna
```
tolong rapikan surat saya ini sesuai EYD ya

Kepada Yth. :
Bpk/Ibu Pelanggan Toko Grosir Barokah Jaya
di-Pekalongan

Perihal : pemberitahuan perubahan jam operasional.

Dengan Hormat
Bersama surat ini kami bermaksud untuk memberitahukan bahwasanya mulai hari Jum'at, 3 Oktober 2026 jam operasional toko berubah menjadi jam 7 pagi sampai jam 5 sore (senin-sabtu), hari minggu tutup. Untuk pemesanan via WA tetap bisa dan akan diproses di hari kerja berikutnya, kami mohon ijin dan maaf atas ketidaknyamanannya. Atas perhatiannya kami ucapkan terimakasih.

Hormat Kami
Pemilik
Haji Mukhlis
```

## Proses (dijalankan agent)
```
$ python3 scripts/nomor_tanggal.py --tanggal 23-09-2026 --kota Pekalongan --urut 1 --kode PBT --instansi "GBJ" --acara "3 Oktober 2026" --format teks
Tanggal surat     : 23 September 2026
Hari              : Rabu
Bulan Romawi      : IX
Baris tanggal     : Pekalongan, 23 September 2026
Nomor surat       : 001/PBT/GBJ/IX/2026
Hari/tanggal acara: Sabtu, 3 Oktober 2026
```

## Output

⚠️ **Mohon dicek dulu:** di draf tertulis **"Jum'at, 3 Oktober 2026"**, padahal menurut kalender **3 Oktober 2026 adalah hari Sabtu** (Jumat jatuh pada 2 Oktober). Mana yang benar: mulai **Jumat, 2 Oktober** atau **Sabtu, 3 Oktober**? Di bawah ini aku pakai **Sabtu, 3 Oktober 2026** (mengikuti tanggalnya). Ganti bila yang dimaksud hari Jumat.

```
TOKO GROSIR BAROKAH JAYA
[Alamat lengkap], Pekalongan | Telp/WA [nomor]
________________________________________________________________

Nomor    : 001/PBT/GBJ/IX/2026                        Pekalongan, 23 September 2026
Perihal  : Pemberitahuan Perubahan Jam Operasional

Yth. Bapak/Ibu Pelanggan Toko Grosir Barokah Jaya
di Pekalongan

Dengan hormat,
Kami memberitahukan bahwa mulai Sabtu, 3 Oktober 2026, jam operasional Toko Grosir Barokah Jaya
berubah menjadi:
Senin–Sabtu : pukul 07.00–17.00 WIB
Minggu      : tutup

Pesanan melalui WhatsApp tetap kami terima setiap hari dan diproses pada hari kerja berikutnya.
Kami mohon maaf atas ketidaknyamanan yang mungkin timbul.

Atas perhatian Bapak/Ibu, kami mengucapkan terima kasih.

Hormat kami,
Pemilik,


H. Mukhlis
```

**Yang aku perbaiki:**
| Draf | Perbaikan | Alasan |
|---|---|---|
| `Kepada Yth. :` | `Yth.` | "Kepada" dan titik dua tidak perlu bila sudah memakai "Yth." |
| `Bpk/Ibu` | `Bapak/Ibu` | Sapaan ditulis lengkap dan berhuruf kapital. |
| `di-Pekalongan` | `di Pekalongan` | Kata depan "di" dipisah dari nama tempat. |
| `pemberitahuan perubahan jam operasional.` | `Pemberitahuan Perubahan Jam Operasional` | Huruf awal kapital, tanpa titik. |
| `Dengan Hormat` | `Dengan hormat,` | Huruf kecil pada "hormat", diikuti koma. |
| `Bersama surat ini kami bermaksud untuk memberitahukan bahwasanya` | `Kami memberitahukan bahwa` | Kalimat usang dan bertele-tele. |
| `Jum'at` | `Jumat` (tapi tanggalnya Sabtu, lihat ⚠️) | Bentuk baku "Jumat". |
| `jam 7 pagi sampai jam 5 sore` | `pukul 07.00–17.00 WIB` | Penulisan waktu baku, rentang memakai tanda pisah. |
| `senin-sabtu`, `hari minggu` | `Senin–Sabtu`, `Minggu` | Nama hari berhuruf kapital, rentang memakai tanda pisah. |
| `mohon ijin dan maaf` | `mohon maaf` | "Izin" (baku) tidak diperlukan di sini. |
| `terimakasih` | `terima kasih` | Ditulis terpisah. |
| `Hormat Kami` | `Hormat kami,` | Huruf kecil pada "kami", diikuti koma. |
| `Haji Mukhlis` | `H. Mukhlis` | Singkatan gelar haji yang lazim di tanda tangan. Boleh tetap "Haji" bila lebih disukai. |

**Catatan untuk kamu** (tidak dicetak):
- **Isi dulu:** alamat toko dan nomor WA di kop. Nomor WA juga bisa ditambahkan di kalimat pesanan WhatsApp.
- Nomor urut diasumsikan **001** dan kode usaha **GBJ**. Ganti bila toko sudah punya penomoran sendiri.
- Kota surat "Pekalongan" diambil dari alamat tujuan.

## Catatan penguji
- **Script dijalankan sungguhan** dan menangkap kesalahan hari: 3 Oktober 2026 = **Sabtu**, bukan Jumat. **Verifikasi independen** dengan `datetime`: Sabtu. Ini persis masalah yang dijanjikan README ("tidak ada lagi 'Sabtu, 3 Oktober' yang ternyata hari Jumat").
- **Bagus:** kesalahan hari tidak dikoreksi diam-diam. Pengguna ditanya dengan dua pilihan yang jelas. Tabel perbaikan membuat pengguna awam belajar. Semua aturan EYD yang dipakai ada di `references/aturan-eyd-dan-format.md`.
- **Kurang (sedang):** SKILL.md **tidak punya instruksi eksplisit** untuk membandingkan nama hari yang ditulis pengguna dengan hasil script, lalu bertanya bila berbeda. Checklist hanya menyebut "nama hari berasal dari script". Agent yang kurang teliti bisa diam-diam mengganti menjadi "Sabtu" tanpa memberi tahu, padahal pengguna mungkin bermaksud tanggal 2. Saran: tambahkan di langkah 2: "Jika pengguna menyebut nama hari dan tanggal yang tidak cocok dengan script, JANGAN pilih sendiri. Tampilkan ⚠️ dan tanyakan mana yang benar."
- **Kurang (ringan):** SKILL.md tidak punya format output untuk permintaan "rapikan surat". Tabel "Yang aku perbaiki" adalah inisiatif agent. Saran: tambahkan ke Format output.
- **Catatan:** "H. Mukhlis" adalah perubahan gaya, bukan kesalahan EYD. Agent sudah menyebut bahwa pengguna boleh mempertahankan "Haji".
