# Uji 02 — Klinik Gigi, Perawat Gigi PKWT 1 Tahun (mulai 1 Desember 2026)

Penguji independen (Tahap 6), 25 September 2026.

## Input pengguna
> "Klinik gigi saya di Bandung terima perawat gigi baru, kontrak PKWT 1 tahun mulai 1 Desember 2026. Klinik
> buka Senin–Sabtu, 2 shift. Buatkan paket onboarding, tolong tekankan soal kerahasiaan data pasien."

## Perintah script
File libur disusun agent dari SKB 3 Menteri (libur nasional & cuti bersama 2026–2027):
```
tanggal
2026-12-24   (cuti bersama Natal)
2026-12-25   (Natal)
2027-01-01   (Tahun Baru)
2027-01-05   (Isra Mikraj)
2027-02-05   (cuti bersama Imlek)
2027-02-06   (Imlek)
2027-03-08 … 2027-03-15 (Nyepi, Idul Fitri & cuti bersama)
```
(komentar dalam kurung tidak ditulis di file; file hanya berisi tanggal.)
```bash
python3 scripts/jadwal_onboarding.py --mulai "1 Desember 2026" --hari-kerja 6 --jenis pkwt \
  --nama "Perawat Gigi" --libur libur-nasional-2026-2027.csv --format markdown
```
Exit code 0.

---

# Paket Onboarding — Perawat Gigi, [isi: Nama Klinik] Bandung

**Penting sejak awal — status PKWT:** karyawan kontrak (PKWT) **tidak boleh** diberi masa percobaan. Bila
tetap dicantumkan, ketentuan itu batal demi hukum dan masa kerja tetap dihitung (UU 13/2003 Pasal 58 jo.
UU 6/2023 Pasal 81 angka 14; PP 35/2021 Pasal 12). Evaluasi 30/60/90 di bawah adalah **pemantauan kinerja
biasa**, bukan kelulusan percobaan. Draf kontrak PKWT 1 tahun → pakai skill `kontrak-kerja-pkwt` (pastikan
juga pekerjaan ini memenuhi syarat PKWT).

**Di luar cakupan skill ini:** STR/SIP perawat gigi (wajib untuk tenaga kesehatan) — verifikasi ke bagian
legal klinik/Dinas Kesehatan. Skill ini tidak membuat materi kompetensi klinis, skrining, atau diagnosis.

## 1. Checklist Pra-Hari-Pertama
| # | Item | Selesai? | Catatan |
|---|---|---|---|
| 1 | Salinan KTP | ☐ | |
| 2 | NPWP/NIK terintegrasi | ☐ | |
| 3 | Rekening gaji | ☐ | |
| 4 | Ijazah & **STR/SIP yang masih berlaku** (salinan) | ☐ | Verifikasi keabsahan oleh legal/Dinkes — di luar cakupan skill |
| 5 | Surat keterangan sehat / riwayat vaksinasi (mis. hepatitis B) sesuai kebijakan klinik | ☐ | [isi: kebijakan klinik] |
| 6 | KK hanya bila mendaftarkan tanggungan BPJS Kesehatan | ☐ | Minimisasi data |
| 7 | **Perjanjian PKWT 1 tahun** ditandatangani sebelum/saat H1 | ☐ | Rujuk `kontrak-kerja-pkwt`; **tanpa** klausul masa percobaan |
| 8 | Pernyataan kerahasiaan + poin kerahasiaan rekam medis | ☐ | Lihat bagian 4 |
| 9 | Daftar BPJS Ketenagakerjaan (wajib, paling lambat 30 hari → sebelum 31 Desember 2026) | ☐ | Berlaku juga untuk PKWT |
| 10 | Daftar BPJS Kesehatan (wajib) | ☐ | |
| 11 | Akun sistem rekam medis/aplikasi klinik dengan hak akses sesuai peran | ☐ | Akun pribadi, bukan akun bersama |
| 12 | Seragam, name tag, APD (masker, sarung tangan, pelindung mata) | ☐ | |
| 13 | Buddy: perawat senior di shift yang sama | ☐ | [isi nama] |

## 2. Jadwal Onboarding (H1 – 90 Hari)
| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 1 Desember 2026 | 1 Desember 2026 | Tidak | Pemilik/Atasan langsung | Penyambutan, serah terima perangkat & akun, penjelasan buku saku karyawan |
| Akhir minggu 1 | 7 Desember 2026 | 7 Desember 2026 | Tidak | Buddy/rekan pendamping | Cek pemahaman tugas dasar & SOP harian, tanya kendala |
| Evaluasi 30 hari | 30 Desember 2026 | 30 Desember 2026 | Tidak | Atasan langsung | Evaluasi checklist tugas dasar; beri umpan balik tertulis singkat |
| Evaluasi 60 hari | 29 Januari 2027 | 29 Januari 2027 | Tidak | Atasan langsung | Evaluasi kemandirian kerja & kepatuhan SOP |
| Evaluasi 90 hari / akhir orientasi | 28 Februari 2027 | 1 Maret 2027 | Ya | Pemilik/Atasan | Evaluasi akhir masa orientasi (isi formulir evaluasi) |
| Masa percobaan | - | - | Tidak | - | Tidak berlaku untuk PKWT |

- **Masa percobaan**: PKWT (karyawan kontrak) DILARANG mensyaratkan masa percobaan; bila ada, batal demi
  hukum (UU 13/2003 Pasal 58 jo. UU 6/2023; PP 35/2021 Pasal 12). Evaluasi hari 30/60/90 di atas tetap
  dipakai sebagai pemantauan kinerja biasa, bukan syarat kelulusan percobaan.

Catatan libur: minggu ke-4 (24–25 Desember 2026, cuti bersama & Natal) dan 1 Januari 2027 libur nasional —
bila klinik tetap buka di hari tersebut, jangan jadwalkan perawat baru bertugas tanpa buddy. Tidak ada
tanggal evaluasi yang jatuh di hari libur kecuali hari 90 (28 Februari 2027, Minggu → Senin 1 Maret 2027).

## 3. Pesan Sambutan (email formal) & Pengumuman Tim
```
Subjek: Selamat Bergabung di [Nama Klinik] — [Nama Perawat]

Yth. Ibu/Bapak [Nama],

Selamat bergabung dengan [Nama Klinik]. Kami dengan senang hati menyambut Ibu/Bapak sebagai
Perawat Gigi, efektif mulai Selasa, 1 Desember 2026.

Informasi hari pertama:
- Waktu & lokasi: Selasa, 1 Desember 2026, pukul [isi], [isi: alamat klinik]
- Penanggung jawab penyambutan: [isi: nama, jabatan, kontak]
- Dokumen yang perlu dibawa: KTP asli (dicocokkan), STR/SIP asli (dicocokkan, salinan kami simpan),
  nomor rekening
- Perlengkapan yang kami siapkan: seragam, name tag, APD, akun aplikasi klinik

Jadwal orientasi 90 hari akan disampaikan pada hari pertama.

Hormat kami,
[Nama pengirim], [Jabatan], [Nama Klinik]
```
Pengumuman tim: "Mulai Selasa 1 Desember 2026, [Nama] bergabung sebagai Perawat Gigi, shift [isi]. Buddy:
[isi]. Mohon dibantu adaptasi di 2 minggu pertama."

## 4. Buku Saku (ringkas) — fokus kerahasiaan pasien
1. Jam kerja/shift: [isi]. Cuti/izin: [isi]. Tukar shift: [isi].
2. **Kerahasiaan data pasien:**
   - Data & rekam medis pasien hanya dibuka untuk keperluan pelayanan sesuai tugas; akun aplikasi tidak
     dipinjamkan; logout setelah dipakai.
   - Dilarang memotret layar/rekam medis/wajah pasien atau membagikan info pasien di WA pribadi/media sosial.
   - Tidak membicarakan kondisi pasien di ruang tunggu atau di luar klinik.
   - Permintaan data pasien oleh pihak lain (keluarga, asuransi, media) → teruskan ke [isi: penanggung
     jawab], jangan dijawab sendiri.
   - Laporkan segera bila ada dugaan kebocoran data ke [isi].
   Dasar: UU 27/2022 PDP (data kesehatan = data pribadi spesifik) + kode etik profesi & aturan rekam medis
   yang berlaku — rincian ketentuan medis dikonfirmasi ke bagian legal/Dinkes (di luar cakupan skill).
3. APD & pengendalian infeksi: ikuti SOP klinik [isi / buat dengan `sop-writer`].
4. Siapa dihubungi: buddy [isi], kepala klinik/dokter penanggung jawab [isi], HR/pemilik [isi].

## 5. Formulir Evaluasi
Judul diubah menjadi **"Evaluasi Kinerja Orientasi (bukan masa percobaan)"**. Tanggal: 30 Des 2026, 29 Jan
2027, 1 Mar 2027. Bagian D disesuaikan: pilihan "lulus percobaan" dihapus; hasil evaluasi dipakai untuk
pembinaan. **Pemutusan PKWT sebelum berakhir bukan hal otomatis** — dapat menimbulkan kewajiban ganti rugi
sisa kontrak; konsultasikan ahli hukum/Disnaker.

Catatan penyesuaian: varian **Klinik** (STR/SIP diarahkan keluar, APD, kerahasiaan rekam medis, email formal).
Data yang perlu dilengkapi: nama klinik & perawat, jam shift, buddy, kontak, kebijakan vaksinasi.
Disclaimer: bukan nasihat hukum/medis; dasar aturan dicek 25 September 2026.

---
## Penilaian penguji
| Kriteria | Hasil |
|---|---|
| Tanpa masa percobaan, dasar hukum disebut | ✅ script & teks |
| Libur Natal/cuti bersama | ⚠️ hanya diperhitungkan karena agent menyiapkan file libur sendiri. Script **tidak punya daftar libur bawaan** dan SKILL.md hanya menyuruh `--libur` "bila pengguna punya daftar" |
| Kerahasiaan data pasien | ✅ (template kerahasiaan klinik tipis; agent menambah poin sendiri) |
| STR/SIP diarahkan keluar | ✅ |
| Verifikasi tanggal mandiri | ✅ 30=30 Des, 60=29 Jan, 90=28 Feb (Minggu) → 1 Mar 2027 |
| Catatan | Formulir evaluasi bawaan menyebut "masa percobaan" & opsi "Perpanjang masa pemantauan" — untuk PKWT agent harus mengubah sendiri; SKILL.md tidak memberi instruksi eksplisit |
