# Skenario 02 — Klinik gigi: simpan SOP penerimaan pasien baru + baca ulang (normal)

**Penguji:** pembuat skill (BUKAN penguji independen), 2026-09-26. **Kernel SiYuan resmi v3.8.5**
(biner Linux resmi, headless, workspace kosong). Data fiktif: "Klinik Gigi Sehat Ceria".

## Permintaan pengguna
> "Tolong simpan SOP penerimaan pasien baru ini ke SiYuan klinik saya: resepsionis sapa pasien, tanya sudah pernah periksa atau belum, minta KTP, catat di form, tanya keluhan utama, persilakan duduk sambil kasih tahu estimasi tunggu, panggil sesuai antrean."

## Langkah agent
1. `daftar-buku` → buku catatan "Klinik Gigi Sehat Ceria" (id `20260926095006-sthe288`).
2. Agent menyusun isi SOP mengikuti struktur `references/template-sop-faq.md` (tanpa mengarang
   kebijakan yang tidak disebutkan pengguna, mis. tidak menambahkan "BPJS" karena tidak disebut).
3. Pratinjau, pengguna setuju, lalu `--ya`:
   ```
   $ python3 scripts/siyuan.py buat --notebook 20260926095006-sthe288 \
       --path "/SOP/Penerimaan Pasien Baru" --ya --md "**Tujuan:** pasien baru terdaftar rapi & menunggu nyaman.
   **Berlaku untuk:** resepsionis.

   ## Langkah
   1. Sapa pasien, tanyakan sudah pernah periksa di sini atau belum.
   2. Minta KTP/kartu identitas, catat data di form pendaftaran.
   3. Tanyakan keluhan utama, catat di form.
   4. Persilakan duduk di ruang tunggu, informasikan estimasi waktu tunggu.
   5. Panggil sesuai antrean.

   ## Checklist harian
   - [ ] Form pendaftaran tersedia
   - [ ] Ruang tunggu bersih & kursi cukup"

   TERSIMPAN: dokumen '/SOP/Penerimaan Pasien Baru' dibuat di SiYuan (id 20260926095128-pmlb4mw).
   ```
4. Pengguna: "coba tampilkan lagi SOP-nya."
   ```
   $ python3 scripts/siyuan.py baca --notebook 20260926095006-sthe288 --path "/SOP/Penerimaan Pasien Baru"
   # /SOP/Penerimaan Pasien Baru

   ---
   title: Penerimaan Pasien Baru
   date: 2026-09-26T09:51:28Z
   lastmod: 2026-09-26T09:51:28Z
   ---

   # Penerimaan Pasien Baru

   **Tujuan:**  pasien baru terdaftar rapi & menunggu nyaman.
   **Berlaku untuk:**  resepsionis.

   ## Langkah
   1. Sapa pasien, tanyakan sudah pernah periksa di sini atau belum.
   2. Minta KTP/kartu identitas, catat data di form pendaftaran.
   3. Tanyakan keluhan utama, catat di form.
   4. Persilakan duduk di ruang tunggu, informasikan estimasi waktu tunggu.
   5. Panggil sesuai antrean.

   ## Checklist harian
   - [ ] Form pendaftaran tersedia
   - [ ] Ruang tunggu bersih & kursi cukup
   ```
   Isi identik dengan yang dikirim - satu judul saja (tidak dobel), sesuai perbaikan template.

## Jawaban agent ke pengguna
> "SOP Penerimaan Pasien Baru sudah tersimpan di SiYuan (folder /SOP). Ini juga SOP untuk hal medis/klinik - kalau ada bagian yang menyangkut standar kesehatan resmi (mis. rekam medis, sterilisasi alat), sebaiknya dicek lagi ke pedoman Dinas Kesehatan/PDGI sebelum dijadikan acuan tetap."
