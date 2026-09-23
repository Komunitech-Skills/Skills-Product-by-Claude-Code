---
name: sop-writer
description: Menyusun SOP (Standar Operasional Prosedur) untuk usaha kecil dan menengah, misalnya buka dan tutup toko, packing pesanan online, handling komplain pelanggan, closing kasir, kebersihan dapur, atau terima barang gudang. Isinya tujuan, ruang lingkup, penanggung jawab, langkah bernomor berbahasa sangat sederhana, checklist harian siap cetak, indikator keberhasilan, serta versi dan tanggal revisi. Gunakan saat pengguna minta buat SOP, prosedur kerja, alur kerja karyawan, checklist harian, atau standard operating procedure, work instruction.
---

# SOP Writer untuk Usaha

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
7. Periksa checklist mutu, lalu tawarkan: versi poster A4 ringkas (5–7 langkah inti), versi bahasa Inggris, atau SOP lanjutan yang terkait.

## Format output
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
5. Kurangi uang modal awal (Rp [isi]) dari total tunai.
6. ⚠️ Bandingkan tunai dengan "Penjualan Tunai" di laporan. (Selisih harus ketahuan hari ini, bukan akhir bulan.)
7. Cek total QRIS di aplikasi/mutasi dengan "Penjualan QRIS" di laporan.
### C. Serah terima
8. Tulis hasil di Form Closing: tunai, QRIS, selisih.
9. Hitung ulang bersama kasir shift berikutnya atau supervisor.
10. Tanda tangan berdua di Form Closing.
11. Masukkan uang setoran ke amplop.
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
- [ ] Setiap langkah diawali kata kerja, ≤ 15 kata, satu tindakan per langkah.
- [ ] Tidak ada istilah asing/jargon tanpa penjelasan (mis. "FIFO" → "barang lama dipakai duluan (FIFO)").
- [ ] Ada angka konkret (jam, batas selisih, jumlah) atau placeholder `[isi]` yang jelas.
- [ ] Langkah kritis ditandai ⚠️ dengan alasan singkat.
- [ ] Ada tabel "Jika terjadi masalah" (2–4 baris) dan siapa yang dihubungi.
- [ ] Checklist harian ≤ 15 butir, ada kolom hari/shift dan paraf.
- [ ] Indikator keberhasilan terukur; target yang diusulkan diberi label "(usulan)".
- [ ] Kode, versi, tanggal berlaku, dan riwayat revisi terisi.

## Batasan & penanganan error
- Jangan mengarang angka yang spesifik usaha (modal kasir, batas selisih, target harian, harga). Pakai `[isi]` atau angka contoh berlabel "(usulan, sesuaikan)".
- Jika cara kerja yang dijelaskan pengguna berisiko (mis. uang dihitung sendirian tanpa saksi, bahan makanan mentah dan matang dicampur), tetap buat SOP-nya, tambahkan langkah pengaman, dan jelaskan alasannya di catatan.
- Jika pengguna meminta SOP yang melanggar hak karyawan (mis. menahan KTP/ijazah, potong gaji otomatis untuk selisih kas tanpa kesepakatan), jangan masukkan langkah itu. Beri catatan singkat dan sarankan konsultasi ke Disnaker/ahli hukum.
- SOP yang menyangkut data pelanggan (mis. mencatat nomor HP saat komplain) wajib menyertakan langkah menjaga data: hanya untuk keperluan layanan dan tidak disebar (UU PDP).
- Untuk revisi: naikkan versi (1.0 → 1.1 untuk perubahan kecil, 2.0 untuk perubahan alur), isi riwayat revisi, dan tandai langkah yang berubah dengan "(baru)" atau "(diubah)".
