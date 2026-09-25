---
name: sop-onboarding
description: Menyusun paket onboarding karyawan baru untuk UMKM dan kantor kecil Indonesia: checklist pra-hari-pertama (dokumen, BPJS, kontrak, perangkat kerja), jadwal H1/minggu 1/30-60-90 hari dengan penanggung jawab (dihitung script), pesan sambutan WA/email & pengumuman tim, buku saku karyawan, dan formulir evaluasi akhir orientasi/masa percobaan. Varian toko, kafe, bengkel, klinik, kantor jasa, gudang. Gunakan saat pengguna minta "onboarding karyawan baru", "induction plan", "employee onboarding", "rencana 30-60-90 hari", atau "paket karyawan baru". Bukan untuk SOP proses kerja umum atau kontrak kerja itu sendiri.
---

# SOP Onboarding Karyawan Baru

## Tujuan
Menyiapkan karyawan baru agar **siap kerja lebih cepat dan tidak merasa dilepas begitu saja**: dokumen
& administrasi beres sebelum hari pertama, jadwal orientasi jelas dengan penanggung jawab, pesan
sambutan siap kirim, aturan sehari-hari tertulis di buku saku, dan evaluasi akhir orientasi yang objektif.

## Kapan digunakan
- "Buatkan paket onboarding untuk kasir baru di toko saya."
- "Karyawan baru mulai kerja Senin depan, apa saja yang perlu disiapkan?"
- "Bikinkan rencana 30-60-90 hari untuk staf baru." / "induction plan" / "employee onboarding checklist".
- "Buatkan buku saku karyawan" atau "formulir evaluasi masa percobaan".

## Kapan TIDAK digunakan
- **SOP proses kerja rutin** (buka toko, packing, closing kasir, dll.) → `sop-writer`. SOP onboarding ini
  hanya merujuk SOP tersebut di buku saku, tidak menulis ulang isinya.
- **Draf kontrak kerja PKWT** atau cek klausul kontrak → `kontrak-kerja-pkwt`. Skill ini hanya
  mengingatkan kelengkapan kontrak di checklist, tidak menyusun pasal kontrak.
- **Slip gaji & iuran BPJS** (perhitungan) → `slip-gaji-bpjs`. Skill ini hanya mengingatkan kewajiban
  pendaftaran BPJS, bukan menghitung iuran.
- **Lowongan kerja/iklan rekrutmen** → `lowongan-kerja`.
- **Surat peringatan** karyawan yang bermasalah → `surat-peringatan-karyawan`. Bila karyawan baru
  bermasalah selama orientasi, evaluasi di sini mencatatnya; SP tetap dibuat lewat skill itu.
- **Diagnosis/skrining kompetensi medis, sertifikasi profesi (STR/SIP)** → di luar cakupan, arahkan ke
  bagian legal/Dinkes/lembaga sertifikasi terkait.

## Input
Tanyakan **sekali** dalam satu pesan bernomor, maksimal 8 butir; bila pengguna ingin cepat, buat dengan
data yang ada dan tandai sisanya `[isi: ...]`, sebutkan asumsinya.
```
1. Nama usaha & jenis usaha (toko/kafe/bengkel/klinik/kantor jasa/gudang/lainnya)
2. Nama & jabatan karyawan baru (boleh "[Nama]" bila untuk template umum)
3. Tanggal mulai kerja
4. Jenis hubungan kerja: PKWT (kontrak) atau PKWTT (tetap, dengan/tanpa masa percobaan)?
5. Hari kerja per minggu (5 atau 6) dan ada shift atau tidak
6. Siapa penanggung jawab onboarding (pemilik/atasan langsung) dan siapa buddy pendamping?
7. Jam kerja, aturan cuti/izin, dan hal khusus buku saku yang perlu dicantumkan (kosongkan bila belum ada)
8. Ada dokumen yang sudah lengkap atau masih kurang? (KTP, NPWP/NIK, rekening, dll.)
```

## Langkah kerja
1. **Tentukan cakupan permintaan**: pengguna mungkin minta paket lengkap, atau hanya satu bagian
   (checklist saja, jadwal saja, pesan sambutan saja, buku saku saja, atau formulir evaluasi saja).
   Buat bagian yang diminta; tawarkan bagian lain sebagai lanjutan.
2. **Checklist pra-hari-pertama**: isi `templates/checklist-pra-hari-pertama.md` dengan data pengguna.
   Ingatkan dokumen diminta **seperlunya saja** dan disimpan aman (UU 27/2022 PDP). Untuk PKWT, rujuk
   `kontrak-kerja-pkwt` dan jangan menulis pasal kontrak sendiri. Tandai kewajiban BPJS Ketenagakerjaan
   & BPJS Kesehatan sebagai wajib, bukan opsional.
3. **Hitung jadwal onboarding dengan script** (jangan mengira-ngira tanggal). Path relatif terhadap
   folder SKILL.md ini; Windows: ganti `python3` dengan `python`/`py`:
   ```bash
   python3 <folder-skill-ini>/scripts/jadwal_onboarding.py --mulai "<tanggal mulai>" \
     --hari-kerja <5|6> --jenis <pkwt|pkwtt> --nama "<nama karyawan>" --format markdown
   ```
   Libur nasional & cuti bersama 2026/2027 (`references/libur-nasional-2026.csv` dan `-2027.csv`, sumber
   sama dengan skill `kalender-pajak`, SKB 3 Menteri — cek ulang tiap tahun) **dimuat otomatis** oleh
   script bila ada. Tambahkan `--libur <file.csv>` hanya untuk libur **tambahan** khusus perusahaan
   (kolom `tanggal`, satu tanggal per baris, format bebas seperti `--mulai`) — file itu digabung dengan
   libur bawaan, bukan menggantinya. Salin tabel Markdown hasil script (termasuk baris peringatan `>`
   bila ada) langsung ke jawaban; jangan menghitung ulang tanggal secara manual, dan jangan hapus
   peringatan yang muncul.

   **Definisi tanggal (harus identik dengan script, lihat komentar header `scripts/jadwal_onboarding.py`):**
   - Checkpoint 30/60/90 hari = mulai + 29/59/89 hari kalender. **Ini hanya pemantauan kinerja rutin**,
     BUKAN batas keputusan masa percobaan untuk PKWTT (bisa jatuh setelah batas hukum, lihat di bawah).
   - Batas hukum akhir masa percobaan (khusus PKWTT) = tanggal yang sama persis 3 bulan kalender
     kemudian; **bila bulan target tidak punya tanggal itu, pakai hari terakhir bulan itu (tanpa dikurangi
     1 hari lagi)**; bila tanggal itu ada, **dikurangi 1 hari**. Contoh: mulai 14 Des 2026 → 14 Mar 2027 −
     1 hari = batas **13 Mar 2027**. Tanggal ini **tidak pernah digeser** walau jatuh di hari libur.
   - Evaluasi keputusan akhir masa percobaan (khusus PKWTT) = **5 hari kerja sebelum** batas hukum
     (dihitung mundur satu per satu dari hari kerja terakhir ≤ batas), supaya keputusan lanjut/tidak
     sempat diambil dan diproses **sebelum** batas hukum berakhir. Baris ini terpisah dari checkpoint 90
     hari dan **selalu** ≤ batas hukum.
   - Aturan geser: H1 **tidak pernah** digeser sendiri (hanya diberi peringatan bila jatuh di hari
     libur/akhir pekan, dengan saran tanggal kerja berikutnya — konfirmasi ke pengguna, jangan geser
     otomatis). Minggu 1 & checkpoint 30/60/90 digeser **maju** ke hari kerja berikutnya bila jatuh di hari
     libur. Evaluasi akhir masa percobaan digeser **mundur** (dihitung dari batas). Batas hukum sendiri
     tidak pernah digeser.

   **Fallback bila Python tidak bisa dijalankan:** hitung manual pakai rumus persis di atas (identik
   dengan script) dan beri tahu pengguna tanggal dihitung manual, sarankan cek dengan script. Bila
   checkpoint 90 hari (mulai+89) lebih lambat dari batas hukum, beri peringatan eksplisit dan jangan
   pakai checkpoint itu untuk keputusan lanjut/tidak. Untuk PKWT: **tidak ada** akhir masa percobaan —
   tulis dengan tegas bahwa PKWT dilarang mensyaratkan masa percobaan (lihat
   `references/dasar-hukum-onboarding.md`).
4. **Isi buku saku karyawan** dari `templates/buku-saku-karyawan.md`. **Jangan mengarang** jam kerja,
   jumlah cuti, atau aturan seragam — bila pengguna belum memberi tahu, tulis `[isi: ...]` dan sebutkan
   di catatan bahwa bagian ini perlu diisi sebelum dicetak. Rujuk SOP layanan pelanggan ke `sop-writer`
   bila pengguna sudah punya atau ingin dibuatkan.
5. **Buat pesan sambutan** dari `templates/pesan-sambutan.md`: pilih versi WA santai atau email formal
   sesuai jenis usaha (`references/varian-jenis-usaha.md`), plus pengumuman ke tim.
6. **Siapkan panduan buddy & check-in mingguan** dari `templates/panduan-buddy.md`: isi nama buddy, jadwal
   check-in (harian minggu 1, mingguan bulan 1–3), dan target checkpoint 30/60/90 sesuai jabatan dari
   `references/varian-jenis-usaha.md` (tabel "Target per jabatan"); bila jabatan tidak ada di tabel, buat
   3 target realistis berdasarkan tugas utama yang disebut pengguna, jangan mengarang angka spesifik
   (omzet, unit) tanpa data.
7. **Siapkan formulir evaluasi** — untuk PKWTT pakai `templates/formulir-evaluasi-orientasi.md` (ada
   opsi "lulus masa percobaan"); untuk PKWT pakai
   `templates/formulir-evaluasi-orientasi-pkwt.md` (evaluasi kinerja biasa, **tanpa** istilah "lulus masa
   percobaan" karena PKWT tidak boleh punya masa percobaan). Isi target hari 30/60/90 dari langkah 6.
   Ingatkan: keputusan tidak lanjut/PHK **bukan otomatis** dan tetap perlu konsultasi ahli hukum
   ketenagakerjaan/Disnaker, termasuk saat masih masa percobaan.
8. **Siapkan retrospektif onboarding** dari `templates/retrospektif-onboarding.md` (diisi sekitar H90,
   setelah checkpoint/evaluasi selesai) — untuk perbaikan proses onboarding berikutnya, tawarkan sebagai
   bagian opsional, bukan wajib disertakan di paket awal.
9. **Sesuaikan dengan jenis usaha** memakai `references/varian-jenis-usaha.md` (dokumen tambahan, buku
   saku, shift, buddy, target per jabatan) — sebutkan penyesuaian yang dibuat.
10. Periksa checklist mutu di bawah, lalu tawarkan bagian lain yang belum dibuat (mis. kontrak PKWT, SOP
    terkait, slip gaji) dengan menyebut skill yang tepat.

## Format output
Untuk permintaan paket lengkap, urutkan:
```
# Paket Onboarding — [Nama Karyawan/Jabatan], [Nama Usaha]

## 1. Checklist Pra-Hari-Pertama
[isi dari templates/checklist-pra-hari-pertama.md]

## 2. Jadwal Onboarding (H1 – 90 Hari)
[tabel Markdown dari scripts/jadwal_onboarding.py]

## 3. Pesan Sambutan & Pengumuman Tim
[pesan WA/email untuk karyawan baru + pengumuman tim]

## 4. Buku Saku Karyawan (ringkas)
[isi dari templates/buku-saku-karyawan.md]

## 5. Panduan Buddy, Check-in Mingguan & Target per Jabatan
[isi dari templates/panduan-buddy.md, target dari references/varian-jenis-usaha.md]

## 6. Formulir Evaluasi Akhir Orientasi
[isi dari templates/formulir-evaluasi-orientasi.md (PKWTT) atau -pkwt.md (PKWT), tautan/salin saat
mendekati H90/evaluasi akhir masa percobaan]

## 7. Retrospektif Onboarding (opsional, isi setelah H90)
[tautan/salin templates/retrospektif-onboarding.md]

Catatan penyesuaian jenis usaha: [ringkas]
Data yang masih perlu dilengkapi: [daftar [isi: ...] yang tersisa]
Disclaimer: [lihat Batasan & penanganan error]
```

## Contoh
**Input pengguna:** "Tolong buatin paket onboarding buat kasir baru namanya Sinta di toko bangunan saya
di Sidoarjo, mulai kerja Senin 28 September 2026, kontraknya PKWTT langsung, buddy-nya Rina (kasir
senior), kerja 6 hari seminggu."

**Output (ringkas, hasil nyata `jadwal_onboarding.py --mulai "28 September 2026" --hari-kerja 6 --jenis
pkwtt`, hari libur nasional dimuat otomatis — tidak ada yang jatuh di rentang ini):**
```
## 2. Jadwal Onboarding (H1 – 90 Hari)
| Tahap | Tanggal target | Tanggal disesuaikan | Digeser? | Penanggung jawab | Kegiatan |
|---|---|---|---|---|---|
| Hari pertama (H1) | 28 September 2026 | 28 September 2026 | Tidak | Pemilik/Atasan langsung | ... |
| Akhir minggu 1 | 4 Oktober 2026 | 5 Oktober 2026 | Ya | Buddy: Rina | ... |
| Checkpoint 30 hari | 27 Oktober 2026 | 27 Oktober 2026 | Tidak | Atasan langsung | ... |
| Checkpoint 60 hari | 26 November 2026 | 26 November 2026 | Tidak | Atasan langsung | ... |
| Checkpoint 90 hari | 26 Desember 2026 | 26 Desember 2026 | Tidak | Pemilik/Atasan | Pemantauan rutin |
| Batas hukum akhir masa percobaan (PKWTT) | 27 Desember 2026 | 27 Desember 2026 | Tidak | - | Tanggal hukum, tidak digeser |
| Evaluasi keputusan akhir masa percobaan (PKWTT) | 19 Desember 2026 | 19 Desember 2026 | Tidak | Pemilik/Atasan | Keputusan lanjut/tidak |
```
Di sini checkpoint 90 hari (26 Des) masih sebelum batas hukum (27 Des), jadi tidak ada peringatan. Bila
tanggal mulai membuat checkpoint 90 hari jatuh **setelah** batas hukum, script menambah baris peringatan
`⚠️` di atas tabel — salin juga baris itu, dan pakai baris "Evaluasi keputusan akhir masa percobaan"
(bukan checkpoint 90 hari) untuk keputusan lanjut/tidak.

Contoh lengkap lain (varian bengkel, karyawan PKWT, input tidak lengkap, tanggal mulai di hari libur) di
`examples/`.

## Checklist sebelum mengirim hasil
- [ ] Tanggal jadwal berasal dari script (atau ditandai "dihitung manual").
- [ ] Untuk PKWT: tidak ada tanggal/klausul masa percobaan; disebutkan dasar larangannya; formulir
  evaluasi versi PKWT dipakai (tanpa istilah "lulus masa percobaan").
- [ ] Untuk PKWTT: masa percobaan maks. 3 bulan, upah selama percobaan tidak boleh di bawah upah minimum
  (kecuali usaha mikro/kecil — lihat `references/dasar-hukum-onboarding.md`); baris "evaluasi keputusan
  akhir masa percobaan" (bukan checkpoint 90 hari) dipakai untuk keputusan lanjut/tidak.
- [ ] Bila script memberi peringatan (H1 di hari libur, checkpoint 90 hari melewati batas hukum),
  peringatan itu **disalin ke jawaban**, tidak dihilangkan.
- [ ] Checklist dokumen meminta data **seperlunya** dan mengingatkan penyimpanan aman (PDP).
- [ ] Kewajiban pendaftaran BPJS Ketenagakerjaan & Kesehatan disebutkan sebagai wajib.
- [ ] Buku saku tidak berisi angka/aturan karangan; semua yang belum diisi pengguna diberi `[isi: ...]`.
- [ ] Formulir evaluasi mengingatkan bahwa pemutusan hubungan kerja perlu konsultasi ahli hukum/Disnaker.
- [ ] Disclaimer & tanggal dasar hukum dicantumkan.

## Batasan & penanganan error
- Jangan mengarang nama, tanggal, jam kerja, jumlah cuti, atau angka BPJS/gaji spesifik usaha. Pakai
  `[isi: ...]` dan tanyakan bila penting.
- Jangan menyusun pasal kontrak kerja di sini — arahkan ke `kontrak-kerja-pkwt` untuk PKWT; untuk PKWTT,
  klausul masa percobaan cukup dicatat sebagai referensi di checklist, bukan pasal lengkap.
- Jika script gagal (format tanggal salah, file libur tidak terbaca), baca pesan error, perbaiki input,
  jalankan ulang; jangan menyalin `Traceback` ke pengguna.
- Jika pengguna minta buku saku tanpa info jam kerja/cuti sama sekali, buat kerangka lengkap dengan semua
  bagian `[isi: ...]` dan jelaskan bagian mana yang wajib diisi sebelum dicetak.
- Jika permintaan menyangkut kompetensi/sertifikasi tenaga medis, alat berat bersertifikat, atau K3
  teknis wajib, buat draf checklist administratif saja dan ingatkan verifikasi ke ahli/lembaga terkait.
- Data karyawan bersifat pribadi: jangan menyarankan menyimpan salinan dokumen identitas di tempat yang
  bisa diakses banyak orang; rujuk `references/dasar-hukum-onboarding.md` bagian PDP.
- Aturan ketenagakerjaan sedang dalam proses perubahan (RUU Pelindungan Ketenagakerjaan ditargetkan
  disahkan Oktober 2026). Dasar aturan & tanggal verifikasi ada di `references/dasar-hukum-onboarding.md`.
