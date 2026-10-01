---
name: surat-resmi
description: Menulis surat resmi/surat dinas berbahasa Indonesia sesuai EYD V dan siap cetak, yaitu surat permohonan, pemberitahuan, undangan, surat kuasa, surat keterangan (kerja/domisili usaha), dan surat pengantar, lengkap dengan kop, nomor surat bulan Romawi, lampiran, perihal, salam, isi, penutup, dan tanda tangan. Gunakan saat pengguna minta buat surat resmi, surat dinas, surat undangan rapat, surat izin, surat keterangan kerja, atau official letter, formal letter Indonesian. Bukan untuk surat penawaran harga, SP karyawan, atau kontrak.
---

# Surat Resmi (EYD V)

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya, dan simpan hasil di folder kerja yang disepakati (bukan /tmp).

## Tujuan
Menghasilkan surat resmi yang benar strukturnya, benar ejaannya (EYD Edisi V), sopan, ringkas, dan langsung bisa disalin ke Word/Google Docs lalu dicetak, untuk pemilik usaha, pengurus organisasi/RT/koperasi, sekolah, dan profesional.

## Kapan digunakan
- Surat **permohonan** (izin kegiatan, izin keramaian, sponsor non-komersial, peminjaman tempat, cuti).
- Surat **pemberitahuan** (libur toko, perubahan jam operasional, pemadaman, kenaikan iuran).
- Surat **undangan** (rapat, syukuran, RAT koperasi, arisan resmi, peresmian toko).
- **Surat kuasa** (pengambilan dokumen/barang, pengurusan izin, pengambilan paket, perwakilan rapat).
- **Surat keterangan** (keterangan kerja, keterangan magang, keterangan usaha dari pemilik usaha).
- **Surat pengantar** (pengiriman dokumen/barang, pengantar karyawan ke instansi).
- Merapikan/mengoreksi surat resmi yang sudah ada sesuai EYD V (output: surat hasil perbaikan + tabel `Draf | Perbaikan | Alasan`, maks 15 baris).

## Kapan TIDAK digunakan
- Surat penawaran harga → `surat-penawaran-harga`. Proposal kerja sama → `proposal-kerjasama`.
- Surat peringatan karyawan → `surat-peringatan-karyawan`. Kontrak/perjanjian → `perjanjian-sederhana`.
- Surat tagihan → `tagih-piutang`. Invoice → `buat-invoice`. Loker → `lowongan-kerja`.
- Naskah dinas instansi pemerintah yang punya pedoman internal khusus → boleh bantu draf, tapi ingatkan untuk menyesuaikan dengan tata naskah dinas instansi tersebut.
- Dokumen yang harus dibuat notaris/pejabat (akta, surat kuasa khusus untuk beracara di pengadilan) → arahkan ke notaris/advokat.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Jenis surat & tujuan/isi pokok | Ya | — (tanyakan) |
| Pengirim (nama usaha/organisasi, alamat, kontak) | Ya | `[isi kop]` jika pengguna ingin cepat |
| Penerima (nama/jabatan, instansi, alamat) | Ya (kecuali surat keterangan) | `Yth. [jabatan penerima]` |
| Penanda tangan (nama & jabatan) | Tidak | `[Nama]`, `[Jabatan]` |
| Kota & tanggal surat | Tidak | Tanggal hari ini, kota `[Kota]` |
| Nomor urut & kode surat | Tidak | Urut 001, kode sesuai jenis (lihat `references/aturan-eyd-dan-format.md`) |
| Detail acara (undangan): hari, tanggal, jam, tempat, acara | Ya untuk undangan | — (tanyakan) |
| Lampiran | Tidak | Baris lampiran dihapus jika tidak ada |
| Gaya | Tidak | Formal-sopan, ringkas |

Jika info wajib kurang, tanyakan **sekali** (maks 5 pertanyaan bernomor). Jika pengguna ingin cepat, buat dengan placeholder `[...]` dan sebutkan asumsinya.

## Langkah kerja

> **Lokasi script:** semua script skill ini ada di subfolder `scripts/` di folder yang sama dengan SKILL.md ini (folder skill). Jalankan dari sana; jangan mencari script atau file pengguna ke seluruh disk (mis. `find /`) — itu lambat dan menyentuh data pribadi di luar folder kerja.
1. **Tentukan jenis surat** dan ambil kerangkanya dari `references/template-surat.md`.
2. **Buat tanggal, hari, dan nomor surat dengan script** (bulan Romawi dan nama hari sering salah bila ditebak). Path relatif terhadap folder SKILL.md ini; Windows: `python` atau `py`:
   ```bash
   python3 <folder-skill-ini>/scripts/nomor_tanggal.py --tanggal "<tanggal surat>" --kota "<kota>" \
     --urut <no> --kode <KODE> --instansi "<SINGKATAN>" [--acara "<tanggal acara>"] --format teks
   ```
   - Pola default: `{urut}/{kode}/{instansi}/{romawi}/{tahun}` → `007/UND/CV-MJ/IX/2026`. Jika pengguna punya pola sendiri, pakai `--pola`.
   - `--acara` memberi nama hari yang benar untuk undangan (mis. "Sabtu, 3 Oktober 2026") dan peringatan bila acara lebih awal dari tanggal surat.
   - **Wajib: bandingkan nama hari yang ditulis pengguna** (mis. "Jumat, 3 Oktober 2026") dengan `hari`/`acara` dari script. Jika berbeda, **jangan memilih sendiri** dan jangan mengganti diam-diam. Tampilkan di awal jawaban:
     `⚠️ "Jumat, 3 Oktober 2026" tidak cocok: 3 Oktober 2026 jatuh pada hari Sabtu. Mana yang benar: (a) Sabtu, 3 Oktober 2026 atau (b) Jumat, 2 Oktober 2026?`
     Tunggu jawaban pengguna. Jika pengguna minta draf tetap dibuat, tulis bagian tanggal itu sebagai `[hari, tanggal: menunggu konfirmasi]`.
   - **Fallback tanpa Python:** tanggal ditulis `23 September 2026` (bulan lengkap, tanpa nol di depan); bulan Romawi I–XII sesuai bulan surat; hitung nama hari dengan kalender dan beri tahu pengguna bahwa hari perlu dicek.
3. **Tulis surat** dengan struktur baku (lihat Format output). Terapkan aturan EYD V dari `references/aturan-eyd-dan-format.md`, terutama:
   - `Yth.` (bukan "Kepada Yth." yang berlebihan bila sudah ada "Yth."), `Bapak`/`Ibu` kapital sebagai sapaan.
   - Perihal ringkas, huruf awal kapital, tanpa titik: `Perihal: Permohonan Izin Kegiatan`.
   - Salam pembuka `Dengan hormat,` dan salam penutup `Hormat kami,` (koma).
   - Angka jam `pukul 09.00–12.00 WIB`; rupiah default `Rp1.500.000,00` (EYD V: tanpa spasi setelah Rp); pakai `Rp 1.500.000` hanya bila pengguna meminta gaya internalnya; konsisten dalam satu surat.
   - Hindari kalimat usang: "Bersama surat ini kami beritahukan bahwa..." → "Kami memberitahukan bahwa...".
4. **Surat kuasa & surat keterangan:** tambahkan identitas lengkap (nama, NIK/nomor identitas bila perlu, alamat, jabatan), batas kewenangan yang jelas, dan catatan meterai (lihat Batasan).
5. **Susun untuk siap cetak:** kop di atas, satu halaman bila memungkinkan, blok tanda tangan cukup ruang (3–4 baris kosong), tembusan paling bawah.
6. Periksa checklist. Tawarkan: versi bahasa Inggris, versi lebih singkat, atau surat balasan.

## Format output
```
[NAMA USAHA / ORGANISASI]
[Alamat lengkap] | Telp/WA [..] | Email [..]
________________________________________________________________

Nomor    : 007/UND/CV-MJ/IX/2026                    Surabaya, 23 September 2026
Lampiran : 1 (satu) berkas
Perihal  : Undangan Rapat Evaluasi Mitra

Yth. [Jabatan/Nama Penerima]
[Instansi]
[Alamat]

Dengan hormat,
[Paragraf pembuka: maksud surat]
[Paragraf isi: rincian; gunakan daftar bila > 2 hal]
[Paragraf penutup: harapan + terima kasih]

Hormat kami,
[Jabatan]


[Nama Lengkap]

Tembusan:
1. ...
```
Setelah surat, tambahkan bagian singkat **"Catatan untuk kamu"** (tidak dicetak): asumsi yang dipakai, placeholder yang harus diisi, dan catatan meterai bila relevan.

## Contoh
**Input pengguna:** "Buatin surat undangan rapat anggota koperasi Sejahtera Bersama, Sabtu 3 Oktober 2026 jam 9 pagi di balai RW 05 Kelurahan Ketintang, bahas rencana SHU. Yang tanda tangan ketua, Pak Hendra Wijaya. Surat ke-12 bulan ini."

**Output (ringkas):**
```
KOPERASI SEJAHTERA BERSAMA
[Alamat] | Telp/WA [..]
________________________________________________________________

Nomor    : 012/UND/KSB/IX/2026                        Surabaya, 23 September 2026
Perihal  : Undangan Rapat Anggota

Yth. Bapak/Ibu Anggota Koperasi Sejahtera Bersama
di tempat

Dengan hormat,
Kami mengundang Bapak/Ibu untuk menghadiri rapat anggota yang akan dilaksanakan pada
hari, tanggal : Sabtu, 3 Oktober 2026
pukul         : 09.00 WIB–selesai
tempat        : Balai RW 05, Kelurahan Ketintang
acara         : Pembahasan rencana pembagian Sisa Hasil Usaha (SHU)

Mengingat pentingnya acara tersebut, kami mengharapkan kehadiran Bapak/Ibu tepat waktu.
Atas perhatian Bapak/Ibu, kami mengucapkan terima kasih.

Hormat kami,
Ketua,


Hendra Wijaya

Catatan untuk kamu: kota "Surabaya" diasumsikan dari Kelurahan Ketintang — ganti bila berbeda.
Hari "Sabtu" sudah dicek dengan script.
```
Contoh lain (surat kuasa ambil BPKB, surat keterangan kerja, pemberitahuan libur toko, permohonan izin keramaian): `references/template-surat.md`.

## Checklist sebelum mengirim hasil
- [ ] Struktur lengkap: kop, nomor, (lampiran bila ada), perihal, tanggal, alamat tujuan, salam pembuka, isi, penutup, salam penutup, tanda tangan, (tembusan).
- [ ] Tanggal tanpa nol di depan & bulan ditulis lengkap; bulan Romawi dan nama hari berasal dari script (atau diberi label "cek manual").
- [ ] Nama hari yang ditulis pengguna sudah dibandingkan dengan script; jika berbeda, ⚠️ ditampilkan dan pengguna ditanya (tidak dipilihkan).
- [ ] Ejaan EYD V: `Yth.`, `di tempat`/`di Jakarta` (di- dipisah), `pukul 09.00`, `Rp`, huruf kapital sapaan, tanpa "Kepada Yth." ganda.
- [ ] Tidak ada paragraf bertele-tele; isi pokok muncul di paragraf pertama/kedua.
- [ ] Placeholder yang belum terisi disebut di "Catatan untuk kamu".
- [ ] Untuk surat kuasa/keterangan: identitas lengkap, batas kewenangan/masa berlaku jelas, catatan meterai.

## Batasan & penanganan error
- **Meterai:** jangan menyatakan surat "tidak sah tanpa meterai". Meterai (Rp10.000, UU 10/2020) adalah pajak atas dokumen, antara lain surat keterangan/pernyataan/sejenisnya yang dibuat sebagai alat bukti. Sarankan membubuhkan meterai pada surat kuasa/keterangan yang akan dipakai sebagai bukti; kewajiban akhir mengikuti aturan & permintaan instansi tujuan.
- **Surat kuasa** di skill ini adalah surat kuasa sederhana (mis. ambil dokumen, wakili rapat). Kuasa untuk beracara di pengadilan, jual beli tanah, atau yang harus notariil → arahkan ke advokat/notaris.
- **Surat keterangan** hanya boleh berisi fakta yang diberikan pengguna. Jangan membuat keterangan palsu (mis. keterangan kerja untuk orang yang tidak bekerja, keterangan penghasilan yang dinaikkan untuk KPR). Tolak dengan sopan bila diminta.
- Jangan meniru kop, logo, atau nama instansi pemerintah/perusahaan lain yang bukan milik pengguna.
- Jika script error, baca pesan error (mis. format tanggal), perbaiki input, jalankan ulang; jika tetap gagal, pakai fallback manual.
- Dasar aturan & sumber: `references/aturan-eyd-dan-format.md` (berlaku per 23 September 2026).
