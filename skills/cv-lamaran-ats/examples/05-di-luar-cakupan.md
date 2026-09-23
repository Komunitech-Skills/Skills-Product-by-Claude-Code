# Skenario 5 — Di luar cakupan

## Input pengguna
```
Saya HRD di PT Maju Bersama, mau pasang lowongan Staff Admin di beberapa portal
karier. Tolong bikinkan draf iklan lowongannya ya.
```

## Output

```
Skill yang sedang aktif ini (CV & Lamaran Ramah ATS) dibuat untuk PENCARI kerja —
menyesuaikan CV/surat lamaran mereka dengan lowongan yang sudah ada, bukan untuk
menyusun iklan lowongan dari sisi perusahaan/HRD.

Untuk membuat draf iklan lowongan (posisi, kualifikasi, cara melamar, dll.), skill
yang tepat adalah `lowongan-kerja`. Kalau tersedia di platform Anda, coba minta
dengan kalimat seperti: "Bikinkan draf lowongan Staff Admin untuk PT Maju Bersama,
syaratnya [...]".

Kalau nanti Anda (atau kandidat internal) justru butuh MENYESUAIKAN CV kandidat
dengan lowongan tertentu, skill ini bisa dipakai lagi.
```

## Catatan penguji
- Sesuai bagian "Kapan TIDAK digunakan" SKILL.md: "Pengguna adalah perekrut/HR
  yang mau memasang iklan lowongan → `lowongan-kerja`." Skill menolak dengan
  benar dan mengarahkan ke skill yang tepat, tidak memaksakan diri membuat draf
  iklan lowongan.
- Tidak ada cacat ditemukan pada skenario ini.
