# Uji 04 — Input Tidak Lengkap

Penguji independen (Tahap 6), 25 September 2026.

## Input pengguna
> "bikin onboarding karyawan"

## Perilaku agent (sesuai bagian Input SKILL.md: tanya sekali, satu pesan bernomor, maks. 8 butir)
Script **tidak dijalankan** karena tanggal mulai belum ada (menjalankan dengan tanggal karangan melanggar
"jangan mengarang tanggal").

## Output agent
```
Siap, saya bantu siapkan paket onboarding karyawan baru. Supaya hasilnya langsung bisa dipakai,
boleh jawab singkat poin-poin ini (yang belum tahu, kosongkan saja):

1. Nama & jenis usaha (toko/kafe/bengkel/klinik/kantor jasa/gudang/lainnya)?
2. Nama & jabatan karyawan baru? (boleh "[Nama]" kalau untuk template umum)
3. Tanggal mulai kerja?
4. Karyawan kontrak (PKWT) atau karyawan tetap (PKWTT)? Kalau tetap, pakai masa percobaan atau tidak?
5. Kerja 5 atau 6 hari seminggu? Ada shift?
6. Siapa penanggung jawab onboarding (pemilik/atasan) dan siapa buddy pendampingnya?
7. Jam kerja, aturan cuti/izin, atau aturan khusus yang mau dimasukkan ke buku saku? (boleh kosong)
8. Dokumen apa yang sudah ada/masih kurang? (KTP, NPWP/NIK, rekening, dll.)

Mau yang lengkap (checklist, jadwal 90 hari, pesan sambutan, buku saku, formulir evaluasi) atau
bagian tertentu saja? Kalau mau cepat, sebutkan saja jenis usaha + tanggal mulai — sisanya saya
isi dengan tanda [isi: ...] dan saya sebutkan asumsinya.
```

## Penilaian penguji
| Kriteria | Hasil |
|---|---|
| Bertanya sekali, satu pesan, ≤ 8 butir | ✅ (8 butir + 1 kalimat pilihan cakupan) |
| Bahasa awam, tanpa jargon berlebihan | ✅ (PKWT/PKWTT dijelaskan "kontrak/tetap") |
| Tidak mengarang tanggal / tidak menjalankan script dengan tanggal fiktif | ✅ |
| Jalan pintas "cepat" ditawarkan | ✅ |
| Catatan | SKILL.md tidak menyebut data **minimum** untuk mode cepat (jenis usaha + tanggal mulai). Agent menyimpulkan sendiri; sebaiknya ditulis eksplisit. |
