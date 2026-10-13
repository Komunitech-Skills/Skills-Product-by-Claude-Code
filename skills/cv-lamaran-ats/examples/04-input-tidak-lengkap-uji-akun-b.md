# Skenario 4 (Akun B) — Input Tidak Lengkap

## Input pengguna
```
Bikinin CV yang cocok buat lowongan Staff Admin dong.
```
(Tidak ada teks lowongan lengkap, tidak ada data diri/riwayat pengguna, tidak jelas
apakah sudah punya profil induk dari sesi sebelumnya.)

## Output yang diharapkan (mengikuti SKILL.md Langkah 1 & aturan "Input")
```
Sebelum saya bantu, saya perlu beberapa info (jawab dalam satu pesan ya):
1. Tolong tempel teks lengkap lowongan Staff Admin ini (posisi, kualifikasi,
   tanggung jawab, kalau ada nama perusahaan & lokasi).
2. Apakah kamu sudah pernah membuat "profil pengalaman induk" lewat skill ini
   sebelumnya? Kalau sudah, tempel lagi teksnya. Kalau belum, boleh tempel CV
   lama kamu, atau ceritakan bebas: nama, kontak, pendidikan, dan pengalaman
   kerja/organisasi/magang yang pernah dijalani.
3. Ekspektasi gaji kamu berapa? (boleh perkiraan, tapi dari kamu sendiri —
   bukan yang saya karang)
4. Domisili kamu di mana, dan bersedia WFO/hybrid/remote/relokasi?
5. Butuh surat lamaran & pesan WA/LinkedIn ke rekruter juga, atau CV saja dulu?
```

## Verifikasi kepatuhan
- Pertanyaan diajukan **sekali**, dalam **satu pesan**, **bernomor**, tidak lebih
  dari 5 pertanyaan — sesuai aturan Input SKILL.md baris "Jika data wajib kurang
  ... tanyakan sekali dalam satu pesan bernomor, maksimal 5 pertanyaan."
- Tidak ada bagian riwayat kerja yang diisi tebakan/karangan menunggu jawaban.
- Pertanyaan #2 secara eksplisit mengecek keberadaan profil induk sebelum
  meminta ulang data — sesuai Langkah 1 ("Jika pengguna sudah menempelkan
  profil induknya ... pakai itu langsung, jangan minta ulang"), meski dalam
  kasus ini belum ada riwayat sesi sehingga tetap wajar ditanyakan.
- **Temuan RINGAN:** SKILL.md tidak secara eksplisit membatasi urutan prioritas
  pertanyaan bila jawaban pengguna nanti tetap tidak lengkap (mis. hanya
  menjawab 3 dari 5 poin) — apakah agent boleh bertanya sekali lagi atau harus
  jalan dengan asumsi. Berdasarkan prinsip umum pedoman kurasi Komunitech ("pakai default yang
  masuk akal dan sebutkan asumsinya" bila pengguna ingin cepat), interpretasi
  wajar: lanjut dengan default/asumsi untuk poin yang tidak dijawab kecuali itu
  riwayat pengalaman inti (yang wajib, tidak boleh dikarang). SKILL.md sendiri
  tidak menuliskan aturan susulan ini secara eksplisit untuk kasus campuran
  (sebagian dijawab, sebagian tidak).
