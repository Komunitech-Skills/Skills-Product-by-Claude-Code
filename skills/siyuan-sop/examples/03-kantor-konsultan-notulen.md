# Skenario 03 — Kantor konsultan: simpan notulen rapat + tambah catatan susulan (normal)

**Penguji:** pembuat skill (BUKAN penguji independen), 2026-09-26. **Kernel SiYuan resmi v3.8.5**
(biner Linux resmi, headless, workspace kosong). Data fiktif: "Kantor Konsultan Maju Bersama".

## Permintaan pengguna
> "Simpan notulen rapat hari ini ke SiYuan. Tanggal 26 September 2026, peserta Andi (PM), Sari (Konsultan Pajak), Budi (Klien). Keputusan: laporan bulanan dikirim tiap tanggal 5, dan Sari siapkan draf SPT sebelum 10 Oktober. Tindak lanjut: Sari - draf SPT - 10 Oktober; Andi - kirim undangan rapat berikutnya - 1 Oktober."

(Catatan: notulen sudah dalam bentuk rapi - dalam pemakaian nyata, ini biasanya hasil jadi dari
skill `notulen-rapat` yang lalu diminta pengguna untuk disimpan.)

## Langkah agent
1. `daftar-buku` → "Kantor Konsultan Maju Bersama" (id `20260926095007-5phna9m`).
2. Judul dokumen memuat tanggal supaya mudah dicari/diurutkan (`references/template-sop-faq.md` §3):
   ```
   $ python3 scripts/siyuan.py buat --notebook 20260926095007-5phna9m \
       --path "/Notulen/2026-09-26 - Rencana Proyek Klien ABC" --ya --md "**Tanggal:** 26 September 2026
   **Peserta:** Andi (PM), Sari (Konsultan Pajak), Budi (Klien)

   ## Keputusan
   1. Laporan bulanan dikirim tiap tanggal 5.
   2. Sari menyiapkan draf SPT sebelum 10 Oktober 2026.

   ## Tindak Lanjut
   | Siapa | Apa | Tenggat |
   |---|---|---|
   | Sari | Draf SPT | 2026-10-10 |
   | Andi | Kirim undangan rapat berikutnya | 2026-10-01 |"

   TERSIMPAN: dokumen '/Notulen/2026-09-26 - Rencana Proyek Klien ABC' dibuat di SiYuan (id 20260926095138-d6s6m74).
   ```
3. Sepuluh menit kemudian, pengguna: "eh tambahin, Budi mau kirim data pendukung sebelum 30 September."
   ```
   $ python3 scripts/siyuan.py tambah --id 20260926095138-d6s6m74 --ya \
       --md "## Catatan Tambahan
   Budi akan mengirim data pendukung sebelum 30 September 2026."

   TERSIMPAN: isi ditambahkan ke dokumen/blok 20260926095138-d6s6m74.
   ```
4. Dibaca ulang (`baca --id 20260926095138-d6s6m74`) - isi lama (Keputusan, Tindak Lanjut) **tetap
   utuh**, catatan baru muncul di bawahnya sebagai bagian terpisah, tabel Markdown tampil dengan
   pemformatan ulang oleh SiYuan (tetap 3 kolom & isi sama, hanya spasi kolom disesuaikan) - contoh
   nyata:
   ```
   ## Tindak Lanjut

   |Siapa|Apa|Tenggat|
   | -------| ---------------------------------| ------------|
   |Sari|Draf SPT|2026-10-10|
   |Andi|Kirim undangan rapat berikutnya|2026-10-01|

   ## Catatan Tambahan

   Budi akan mengirim data pendukung sebelum 30 September 2026.
   ```

## Jawaban agent ke pengguna
> "Notulen 26 September sudah tersimpan di SiYuan (folder /Notulen), dan catatan soal Budi sudah ditambahkan di bagian bawah - isi sebelumnya tidak berubah. Rapat ini menyangkut klien & konsultan pajak; kalau nanti mau dikirim ke Budi, ingat itu tetap harus lewat draf yang dicek konsultan dulu, bukan otomatis."
