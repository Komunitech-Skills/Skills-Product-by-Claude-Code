# Skenario 4 — Input tidak lengkap

## Input pengguna
```
CV saya kenapa nggak lolos ATS ya? Tolong perbaiki dong.
```

## Output

```
Siap, saya bantu. Sebelum mulai, saya perlu beberapa info ya (jawab santai saja,
nggak perlu formal):

1. Lowongan mana yang mau dituju? Tolong tempel teks lengkapnya (atau minimal:
   nama posisi + kualifikasi + tanggung jawab).
2. CV yang sekarang gimana? Boleh tempel isi CV lama Anda, atau ceritakan bebas:
   riwayat kerja (jabatan, perusahaan, tahun, tugas utama), pendidikan, dan
   keahlian.
3. Data kontak untuk di CV: nama lengkap, kota domisili, no. HP, email (LinkedIn
   kalau ada).
4. Selain perbaikan CV, perlu juga surat lamaran / email singkat / pesan WA ke
   HRD? (default: saya buatkan surat lamaran + email singkat sekalian)
5. Anda fresh graduate, pindah karier, atau sudah berpengalaman di bidang yang
   sama? (biar saya tahu sudut penekanan yang pas)

Begitu dua yang wajib (lowongan + data riwayat Anda) saya terima, saya langsung
jalankan skor kecocokan kata kunci dan susun CV versi ATS-nya.
```

## Catatan penguji
- Sesuai Langkah 1 SKILL.md ("Jangan lanjut tanpa dua-duanya") dan aturan Input
  ("tanyakan sekali dalam satu pesan bernomor, maksimal 5 pertanyaan") — pertanyaan
  bernomor, satu pesan, 5 poin, tidak lebih.
- Tidak mengarang isi CV meski pengguna hanya bilang "CV saya kenapa nggak
  lolos" tanpa detail — benar-benar berhenti dan bertanya, bukan menebak riwayat
  kerja.
- Tidak ada cacat ditemukan pada skenario ini.
