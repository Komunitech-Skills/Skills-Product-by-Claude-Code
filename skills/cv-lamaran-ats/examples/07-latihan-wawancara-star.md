# Skenario 7 — Normal: Latihan Wawancara Metode STAR

Fitur baru versi 1.1.0. Diuji sebagai lanjutan Skenario 1 (Siti Rahma, Admin Gudang),
setelah CV & surat lamaran selesai, sesuai `references/wawancara-star.md`.

## Input pengguna
```
CV dan surat lamarannya udah oke. Sekarang latih saya wawancara buat posisi Admin
Gudang di PT Sumber Makmur Logistik ya, pakai metode STAR.
```

## Output (ringkas)
```
Sebelum latihan, saya perlu 1-2 contoh situasi kerja nyata kamu (belum ada di profil
induk). Ceritakan singkat:
1. Pernah menghadapi selisih stok atau kesalahan pencatatan? Bagaimana kamu menanganinya?
2. Pernah kerja di bawah tekanan (mis. stock opname mendadak, barang masuk banyak
   sekaligus)? Ceritakan situasinya.

(Pengguna menjawab kedua pertanyaan dengan cerita nyata)

## Latihan Wawancara STAR — Admin Gudang, PT Sumber Makmur Logistik

### Draf jawaban STAR #1 — "Ceritakan saat kamu menemukan kesalahan/selisih di gudang"
**S:** Saat stock opname akhir bulan di CV Berkah Jaya, ditemukan selisih 15 unit barang
antara catatan kartu stok manual dan fisik gudang.
**T:** Sebagai admin gudang, saya bertanggung jawab menelusuri penyebab selisih sebelum
laporan bulanan dikirim ke atasan.
**A:** Saya cek ulang mutasi barang 2 minggu terakhir satu per satu, membandingkan nota
masuk-keluar dengan kartu stok, dan menemukan ada nota keluar yang belum dicatat.
**R:** Selisih terselesaikan dalam 1 hari, laporan bulanan tetap terkirim tepat waktu,
dan sejak itu saya membuat pengecekan mingguan supaya selisih tidak menumpuk.
**Cocok dipakai untuk:** "ceritakan saat kamu teliti/detail", "menghadapi masalah di kerja"

### Draf jawaban STAR #2 — "Ceritakan saat kamu bekerja di bawah tekanan"
(disusun dari cerita kedua pengguna, format sama)

### Pertanyaan sulit umum (kerangka jawaban)
- "Kenapa keluar dari CV Berkah Jaya?" → jawaban jujur & positif (isi sesuai alasan
  pengguna, tidak menjelekkan tempat kerja lama)
- "Kenapa tertarik ke PT Sumber Makmur Logistik?" → sebut sistem WMS yang disebut di
  lowongan sebagai kesempatan belajar, bukan jawaban generik "cari pengalaman"
- "Kamu belum pernah pakai WMS, gimana?" → akui, jembatani dengan pengalaman kartu stok
  manual + Excel, tunjukkan kemauan belajar cepat

### Pertanyaan balik ke pewawancara
- "Sistem apa yang dipakai untuk stock opname di sini — manual, Excel, atau WMS?"
- "Bagaimana pembagian kerja tim gudang sehari-hari?"
- "Apa tantangan terbesar tim gudang saat ini?"

Mau langsung latihan roleplay? Saya akan berperan jadi HRD dan tanya satu per satu,
lalu kasih masukan setelah tiap jawabanmu.
```

## Verifikasi manual
- Kedua contoh STAR berasal dari cerita yang diminta langsung ke pengguna (langkah 1
  `wawancara-star.md`) — bukan karangan agent.
- Pertanyaan "kenapa belum pernah pakai WMS" dijawab dengan mengakui celah, sejalan
  aturan `Batasan & penanganan error` di SKILL.md (tidak mengarang penguasaan alat).
- Disclaimer roleplay = simulasi bantu-belajar disampaikan tersirat lewat ajakan lanjut
  latihan; pastikan versi lengkap saat implementasi selalu menyebutkannya eksplisit.
