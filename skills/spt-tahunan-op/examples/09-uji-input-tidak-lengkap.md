# 09 — Uji independen: input tidak lengkap

**Input pengguna:** "pajak tahunan saya kurang bayar ga ya? saya ngajar di 2 sekolah"

**Respons agent headless (Sonnet + skill), apa adanya:**

> Info wajib belum ada, jadi saya tanya dulu sekali sesuai skill.
> 
> Kemungkinan besar Anda **berisiko kurang bayar**. Alasannya, tiap sekolah biasanya memotong PPh 21 seolah-olah cuma dia pemberi kerja Anda. Masing-masing memakai PTKP penuh dan tarif 5% terendah. Setelah dua penghasilan digabung di SPT Tahunan, sebagian penghasilan masuk lapisan 15%, dan selisihnya belum terpotong. Angka pastinya baru bisa saya hitung dengan data Anda:
> 
> 1. **Tahun pajak berapa?** Kalau tidak dijawab, saya pakai 2025. Status Anda per **1 Januari** tahun itu juga perlu: TK/K/K-I, dan berapa tanggungan (maks. 3)?
> 2. **Bukti potong A1/A2 dari masing-masing sekolah** (dua bukti potong): angka **penghasilan neto** dan **PPh 21 yang dipotong**.
> 3. **Ada penghasilan lain?** Misalnya les privat atau usaha sampingan. Kalau ada, sebutkan pemasukan kotor setahun.
> 4. **Ada potongan pajak lain atau angsuran PPh 25** yang sudah dibayar? Totalnya berapa?
> 5. **Zakat mandiri** ke BAZNAS/LAZ resmi (bukan yang dipotong sekolah)? Berapa setahun?
> 
> **Jalur cepat:** sebutkan saja status dan neto serta PPh 21 dari kedua A1. Sisanya saya anggap 0 dan asumsinya saya tulis.
> 
> Setelah itu saya jalankan script `spt_op.py` dan beri hasil kurang/lebih bayar, peta ke Coretax, dan langkah berikutnya.


**Penilaian:** sesuai SKILL.md — bertanya sekali, 5 pertanyaan bernomor, jalur cepat, tidak menjalankan script dengan angka karangan. Penjelasan awal "berisiko kurang bayar karena 2 pemberi kerja" tepat. Lulus.
