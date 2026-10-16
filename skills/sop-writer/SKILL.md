---
name: sop-writer
description: Menyusun SOP (Standar Operasional Prosedur) untuk usaha kecil dan menengah, misalnya buka dan tutup toko, packing pesanan online, handling komplain pelanggan, closing kasir, kebersihan dapur, atau terima barang gudang. Isinya tujuan, ruang lingkup, penanggung jawab, langkah bernomor berbahasa sangat sederhana, checklist harian siap cetak, indikator keberhasilan, serta versi dan tanggal revisi. Gunakan saat pengguna minta buat SOP, prosedur kerja, alur kerja karyawan, checklist harian, atau standard operating procedure, work instruction.
---

# SOP Writer untuk Usaha

> **Aturan kerja:** Jangan menginstal paket/aplikasi (mis. `pip install`) — bila perlu, tunjukkan caranya dan biarkan pengguna yang memasang; jangan membuka atau mencari file selain yang diberikan pengguna, isi folder skill ini, dan file yang disebut di langkah kerja; jangan menulis file baru tanpa menyebut lokasinya (kecuali di kanal chat, lihat langkah 7), dan simpan hasil di folder kerja yang disepakati (bukan /tmp); jangan menulis SOP hanya ke berkas; jangan menyebut nama skill atau alat internal ke pengguna (lihat langkah 7).

## Tujuan
Mengubah cara kerja yang selama ini "ada di kepala pemilik" menjadi SOP tertulis yang **dipahami karyawan baru di hari pertama**. Isinya langkah pendek bernomor, checklist yang bisa dicetak dan ditempel, serta ukuran keberhasilan yang jelas.

## Kapan digunakan
- Pengguna minta SOP / prosedur / alur kerja / checklist untuk satu pekerjaan rutin di usahanya.
- Pengguna menjelaskan cara kerjanya secara bebas (atau lewat voice note yang diketik) dan minta dijadikan SOP.
- Pengguna ingin merapikan atau memperbarui SOP lama (naik versi).

## Kapan TIDAK digunakan
- Notulen atau hasil rapat → `notulen-rapat` (bisa dilanjutkan ke SOP sesudahnya).
- Surat peringatan untuk karyawan yang melanggar SOP → `surat-peringatan-karyawan`.
- Template balasan chat pelanggan → `balas-chat-cs` (SOP komplain di sini mengatur **alurnya**, bukan kalimat balasannya).
- SOP yang menyangkut izin/standar teknis wajib (K3 bahan kimia berbahaya, keamanan pangan untuk sertifikasi, alat medis, kelistrikan): boleh dibuat draf operasional, tapi ingatkan bahwa standar resmi (mis. dari Dinas Kesehatan/BPOM/Disnaker/ahli K3) harus dirujuk dan diverifikasi ahli.
- Dokumen ISO atau manual mutu lengkap → di luar cakupan. Skill ini hanya membuat SOP operasional praktis.

Saat mengarahkan pengguna ke bantuan lain, sebut kebutuhannya (mis. "notulen rapat"), bukan nama skill-nya.

## Input
| Info | Wajib? | Default jika tidak diberikan |
|---|---|---|
| Pekerjaan yang dibuat SOP-nya | Ya | — (tanyakan) |
| Jenis usaha | Ya | — (tanyakan; memengaruhi langkah) |
| Cara kerja saat ini (urutan, alat, aplikasi) | Tidak | Disusun dari praktik umum di `references/contoh-sop.md`, ditandai `(sesuaikan)` |
| Siapa pelaksana & siapa pengecek | Tidak | Pelaksana: "[jabatan pelaksana]"; pengecek: "Pemilik/Supervisor" |
| Jam/waktu pelaksanaan | Tidak | `[isi jam]` |
| Standar/target (mis. packing ≤ 5 menit/paket) | Tidak | Indikator umum + ditandai "(usulan, sesuaikan)" |
| Nama usaha & kode SOP | Tidak | `SOP-[singkatan]-01` |
| Versi & tanggal berlaku | Tidak | Versi 1.0, tanggal hari ini |

Jika info wajib kurang, tanyakan **sekali** (maks 5 pertanyaan bernomor). Jika pengguna ingin cepat, buat dari praktik umum dan tandai langkah yang perlu disesuaikan.

## Langkah kerja
1. **Pahami pekerjaan** dari awal sampai akhir: pemicu (kapan dimulai), hasil akhir (kapan dianggap selesai), alat/aplikasi yang dipakai, titik rawan (uang, barang, keselamatan, pelanggan).
2. **Tentukan ruang lingkup**: apa yang termasuk dan apa yang tidak (mis. "SOP packing tidak mengatur retur").
3. **Tulis langkah bernomor** mengikuti aturan bahasa sederhana (`references/panduan-bahasa-sop.md`):
   - Satu langkah = satu tindakan, diawali **kata kerja perintah** ("Nyalakan", "Hitung", "Foto").
   - Maks 15 kata per langkah; maks 12 langkah per bagian. Jika lebih, pecah menjadi bagian (A. Persiapan, B. Pelaksanaan, C. Penutupan).
   - Sertakan angka konkret: jam, jumlah, batas ("jika selisih kas lebih dari Rp 10.000, lapor pemilik").
   - Tandai langkah kritis dengan ⚠️ dan tulis alasannya singkat (orang lebih patuh jika tahu alasannya).
   - Tulis **"Jika ... maka ..."** untuk 2–4 kondisi tidak normal (barang rusak, listrik padam, pelanggan marah, uang selisih).
4. **Buat checklist harian siap cetak**: kolom centang per hari (Sen–Min) atau per shift, kolom paraf pelaksana & pengecek. Maks 15 butir, diambil dari langkah kritis.
5. **Tentukan 3–5 indikator keberhasilan** yang bisa diukur tanpa alat canggih (mis. "0 salah kirim per minggu", "toko buka tepat 08.00 minimal 6 dari 7 hari").
6. **Isi kontrol dokumen**: kode SOP, versi, tanggal berlaku, dibuat oleh, disetujui oleh, riwayat revisi.
7. **Sampaikan hasil ke pengguna.** Periksa checklist mutu, **tampilkan SOP utuh di chat** (bukan ringkasan; file hanya tambahan), lalu tawarkan: versi poster A4 ringkas (5–7 langkah inti), versi bahasa Inggris, atau SOP lanjutan yang terkait.
   - **SOP wajib utuh di balasan (kanal chat Telegram/WhatsApp; bila tidak yakin kanalnya, anggap kanal chat):** pengguna di HP tidak bisa membuka folder di komputer agent. Seluruh isi SOP (kode & versi, tujuan, ruang lingkup, penanggung jawab, alat, langkah kerja, jika-maka, indikator, checklist, riwayat revisi) harus tertulis di pesan balasan itu sendiri, bukan hanya di berkas atau di pesan perantara. Jika lebih dari ±3.500 karakter, **pecah menjadi beberapa pesan berurutan per bagian**, tiap pesan berjudul dan bernomor "(1/3)": (1) judul, tujuan, ruang lingkup, penanggung jawab, alat; (2) langkah kerja; (3) jika-maka dan indikator; (4) checklist dan riwayat revisi. Jangan memotong di tengah daftar langkah. Kirim semua bagian dulu; baru sesudahnya tawaran lanjutan.
   - **Berkas hanya TAMBAHAN:** setelah SOP tampil utuh di chat, boleh melampirkan berkas `.md`/`.docx` sebagai dokumen bila kanal bisa mengirim file. Bila tidak bisa, **jangan menyebut jalur/folder kerja atau nama file di komputer**; cukup tawarkan "balas 'kirim file'". **DILARANG** menulis SOP hanya ke berkas. **DILARANG** menulis "sudah dikirim / sudah ada di chat / terlampir" bila isinya tidak ada di balasan yang sama.
   - **Tampilan di chat:** jangan pakai tabel Markdown lebar. Kontrol dokumen ditulis 1–2 baris padat (`Kode: ... | Versi 1.0 | Berlaku: ...`); penanggung jawab sebagai daftar "Peran: nama — tugas"; tabel jika-maka sebagai baris padat "Jika [kondisi] → [tindakan] (lapor: [siapa])"; checklist sebagai daftar "☐ butir" plus satu baris kolom hari dan paraf. Tabel Markdown hanya bila bekerja di folder proyek/terminal.
   - **Bahasa ke pengguna:** tulis seperti kepada pemilik usaha. Jangan memakai istilah internal ("langkah A-E", "bagian 1–9", "checklist mutu"), nama skill atau alat internal (mis. `balas-chat-cs`, "skill SOP"), atau kata proses ("sedang saya susun", "saya jalankan", "tersimpan di berkas"). Kalimat pembuka cukup menyebut hasilnya ("Ini SOP packing untuk [usaha]"); kalimat penutup menawarkan versi poster dsb. dengan kebutuhannya, bukan nama skill.

## Format output
**Wajib: tampilkan SOP LENGKAP (semua bagian 1–9, termasuk checklist) di balasan chat, siap salin.** Jangan hanya menyimpan ke file lalu memberi ringkasan — pengguna di Telegram/WhatsApp tidak bisa membuka file di workspace. Aturan kanal chat (dipecah per bagian bila panjang, berkas hanya tambahan, tanpa klaim "sudah dikirim") ada di langkah 7. File (mis. `.md`) hanya **tambahan**: tulis bila pengguna meminta atau bila bekerja di folder proyek (terminal/IDE), sebutkan lokasinya di situ, dan tetap tampilkan isi lengkapnya di chat. Di kanal chat, lampirkan sebagai dokumen bila bisa; bila tidak, jangan sebut lokasinya.
```
# SOP: [Nama Pekerjaan]
| Kode | SOP-[XX]-[01] | Versi | 1.0 |
|---|---|---|---|
| Usaha | [Nama usaha] | Berlaku mulai | [tanggal] |
| Dibuat oleh | [nama/jabatan] | Disetujui oleh | [nama/jabatan] |

## 1. Tujuan
[1–2 kalimat: kenapa SOP ini ada]

## 2. Ruang lingkup
Berlaku untuk: ... | Tidak mengatur: ...

## 3. Penanggung jawab
| Peran | Siapa | Tugas |
|---|---|---|
| Pelaksana | ... | ... |
| Pengecek | ... | ... |

## 4. Alat & bahan
- ...

## 5. Langkah kerja
### A. Persiapan
1. ...
### B. Pelaksanaan
1. ...
### C. Penutupan
1. ...

## 6. Jika terjadi masalah
| Jika... | Maka... | Lapor ke |
|---|---|---|

## 7. Indikator keberhasilan
- ...

## 8. Checklist harian (cetak & tempel)
[tabel centang Sen–Min + paraf]

## 9. Riwayat revisi
| Versi | Tanggal | Perubahan | Oleh |
|---|---|---|---|
| 1.0 | [tanggal] | Dibuat pertama kali | ... |
```

**Tampilan di kanal chat** (tanpa tabel Markdown; dipecah bila lebih dari ±3.500 karakter):
```
Ini SOP Closing Kasir untuk minimarket Anda. (1/3)
SOP: Closing Kasir Akhir Shift
Kode: SOP-KSR-01 | Versi 1.0 | Berlaku: [tanggal]
1. Tujuan — ...   2. Ruang lingkup — ...
3. Penanggung jawab — Kasir: hitung & isi form; Supervisor: cek ulang
(2/3) 5. Langkah kerja — A. Persiapan 1. ...  B. Hitung uang 3. ...
(3/3) 6. Jika terjadi masalah
• Jika selisih tunai > Rp [10.000] → hitung ulang berdua (lapor: pemilik, hari itu juga)
7. Indikator keberhasilan — ...
8. Checklist harian
☐ Form closing terisi & ditandatangani
Sen ☐ Sel ☐ Rab ☐ Kam ☐ Jum ☐ Sab ☐ Min ☐ | Paraf pelaksana ___ | Paraf pengecek ___
9. Riwayat revisi — 1.0 | [tanggal] | Dibuat pertama kali
```

## Contoh
**Input pengguna:** "Bikinin SOP closing kasir buat minimarket saya di Pekanbaru. Kasir 2 orang shift, pakai aplikasi kasir, ada QRIS sama tunai. Selisih sering nggak ketahuan."

**Output (ringkas):**
```
# SOP: Closing Kasir Akhir Shift
| Kode | SOP-KSR-01 | Versi | 1.0 |
...
## 5. Langkah kerja
### A. Persiapan (15 menit sebelum shift selesai)
1. Layani pelanggan yang sedang antre sampai selesai.
2. Pasang papan "Kasir Tutup" di meja kasir.
### B. Hitung uang
3. Cetak laporan penjualan shift dari aplikasi kasir.
4. Hitung uang tunai di laci per pecahan.
   **Rumus:** uang seharusnya di laci = modal Rp [isi] + Penjualan Tunai di laporan. Setoran = uang di laci − modal.
5. Pisahkan uang modal Rp [isi] dari uang lain, biarkan di laci untuk besok. (Hanya sekali di sini.)
6. ⚠️ Bandingkan sisa uang tunai dengan "Penjualan Tunai" di laporan. (Selisih harus ketahuan hari ini, bukan akhir bulan.)
7. Cek total QRIS di aplikasi/mutasi dengan "Penjualan QRIS" di laporan.
### C. Serah terima
8. Tulis hasil di Form Closing: tunai, QRIS, selisih.
9. Hitung ulang bersama kasir shift berikutnya atau supervisor.
10. Tanda tangan berdua di Form Closing.
11. Masukkan uang setoran (semua tunai selain modal) ke amplop.
12. Tulis tanggal dan shift di amplop.
13. Simpan amplop di brankas.

## 6. Jika terjadi masalah
| Jika... | Maka... | Lapor ke |
|---|---|---|
| Selisih tunai lebih dari Rp [10.000] | Hitung ulang berdua, cek struk batal/retur | Pemilik, hari itu juga |
| QRIS masuk tapi tidak ada di laporan | Foto bukti, catat nomor transaksi | Supervisor |
...
## 7. Indikator keberhasilan
- Form closing terisi & ditandatangani setiap shift (target 100%).
- Selisih kas di atas Rp [10.000] maksimal 1 kali per bulan.
```
Contoh SOP lengkap lainnya (buka toko, packing pesanan online, handling komplain, kebersihan dapur) ada di `references/contoh-sop.md`.

## Checklist sebelum mengirim hasil
- [ ] SOP lengkap (bagian 1–9) tampil di balasan chat, bukan hanya di file + ringkasan.
- [ ] Kanal chat: seluruh SOP ada di balasan (dipecah per bagian dengan judul bila > ±3.500 karakter); tidak ada klaim "sudah dikirim / sudah ada di chat" yang isinya tidak ada di balasan itu; SOP tidak hanya ditulis ke berkas.
- [ ] Kanal chat: berkas (bila ada) hanya tambahan dan dilampirkan sebagai dokumen; bila tidak bisa, tidak ada jalur/folder disebut dan hanya ditawarkan "balas 'kirim file'"; tidak ada tabel Markdown lebar.
- [ ] Bahasa ke pengguna: tanpa "langkah A-E", nama skill/alat internal, atau kata proses.
- [ ] Setiap langkah diawali kata kerja, ≤ 15 kata, satu tindakan per langkah.
- [ ] Tidak ada istilah asing/jargon tanpa penjelasan (mis. "FIFO" → "barang lama dipakai duluan (FIFO)").
- [ ] Ada angka konkret (jam, batas selisih, jumlah) atau placeholder `[isi]` yang jelas.
- [ ] Langkah kritis ditandai ⚠️ dengan alasan singkat.
- [ ] Ada tabel "Jika terjadi masalah" (2–4 baris) dan siapa yang dihubungi.
- [ ] Checklist harian ≤ 15 butir, ada kolom hari/shift dan paraf.
- [ ] Indikator keberhasilan terukur; target yang diusulkan diberi label "(usulan)".
- [ ] Kode, versi, tanggal berlaku, dan riwayat revisi terisi.

## Batasan & penanganan error
- **Izin usaha makanan jangan tertukar:** warung/rumah makan/katering (pangan siap saji) → **Sertifikat Laik Higiene Sanitasi (SLHS)** atau, untuk usaha risiko rendah, label pengawasan/pembinaan dari Dinas Kesehatan kab/kota (Permenkes 14/2021). **PIRT/SPP-IRT** hanya untuk pangan olahan **kemasan** produksi rumah tangga. Sebut "cek ke Dinas Kesehatan setempat".
- Jangan mengarang angka yang spesifik usaha (modal kasir, batas selisih, target harian, harga). Pakai `[isi]` atau angka contoh berlabel "(usulan, sesuaikan)".
- Jika cara kerja yang dijelaskan pengguna berisiko (mis. uang dihitung sendirian tanpa saksi, bahan makanan mentah dan matang dicampur), tetap buat SOP-nya, tambahkan langkah pengaman, dan jelaskan alasannya di catatan.
- Jika pengguna meminta SOP yang melanggar hak karyawan (mis. menahan KTP/ijazah, potong gaji otomatis untuk selisih kas tanpa kesepakatan), jangan masukkan langkah itu. Beri catatan singkat dan sarankan konsultasi ke Disnaker/ahli hukum.
- SOP yang menyangkut data pelanggan (mis. mencatat nomor HP saat komplain) wajib menyertakan langkah menjaga data: hanya untuk keperluan layanan dan tidak disebar (UU 27/2022 tentang Pelindungan Data Pribadi).
- Jika salah satu pesan atau lampiran gagal terkirim, kirim ulang bagian yang gagal; jangan menyatakan SOP sudah terkirim sebelum seluruh isinya benar-benar tertulis di balasan.
- Untuk revisi: naikkan versi (1.0 → 1.1 untuk perubahan kecil, 2.0 untuk perubahan alur), isi riwayat revisi, dan tandai langkah yang berubah dengan "(baru)" atau "(diubah)".
