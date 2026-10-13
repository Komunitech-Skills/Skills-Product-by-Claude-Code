# Riwayat perubahan — checklist-keamanan-pangan-usaha

Catatan teknis per versi.

## Catatan revisi 1.0.2 (2026-10-12)
- Fakta keamanan pangan diperiksa ulang ke WHO 5 Kunci Keamanan Pangan, FDA Food Code 2022, USDA FSIS, BPOM, dan BPJPH (dicek 2026-10-12) setelah uji Telegram menemukan ada fakta yang salah.
- Ayam/unggas dalam bentuk apa pun (utuh, potong, goreng, giling) selalu dimasak sampai suhu inti minimal 74 °C, tidak pernah 63 °C; daging giling dan hidangan telur 71 °C; ikan, telur langsung saji, dan daging sapi/kambing utuh 63 °C.
- Pendinginan dua tahap (60 ke 21 °C dalam 2 jam, lalu 5 °C dalam 4 jam berikutnya); suhu ruang maksimal 2 jam (1 jam bila ruangan di atas 32 °C).
- Daftar alergen mengikuti label BPOM (santan/kelapa bukan susu). Sertifikat halal ditulis wajib, tidak pernah "opsional", dengan tenggat bertahap sesuai UU 33/2014 dan PP 42/2024 (usaha mikro-kecil 18 Oktober 2026).
- Agent tidak boleh melonggarkan standar walau diminta; ia menjelaskan alasannya dalam satu kalimat. Sesudah uji ulang (skor 5,6 naik ke 8,25), script tidak lagi menyatakan "aman" bila tidak ada baris data yang terbaca; berkas rusak total dilaporkan sebagai "tidak ada baris terbaca". Uji regresi ditambah.

## Catatan revisi 1.0.1 (2026-10-06)
- Revisi dari uji pertama (skor 6,0 naik ke 8,4): script `cek_log_suhu.py` mengenali alat dingin lebih dulu daripada kata menu ("kulkas ayam" dibaca kulkas), menangani koma desimal yang terbagi kolom (dengan peringatan), dan menulis durasi di zona bahaya sebagai rentang ("minimal X menit terukur, bisa sampai Y menit").
- Zona bahaya disamakan menjadi 5-60 °C; ditambah catatan bahwa termometer inframerah hanya mengukur permukaan. Saran menilai aman dari bau atau rasa dihapus; contoh "bebas alergen" diganti pernyataan dapur yang juga mengolah alergen umum.

## Catatan revisi 1.0.0 (2026-10-06)
- Rilis awal (uji internal), ditulis ulang bersih dari daftar ide (bukan salinan sumber): checklist harian dan kartu staf untuk usaha makanan/minuman, log suhu dengan script `cek_log_suhu.py`, peta bahan berisiko, dan ringkasan perizinan (PIRT, SLHS, halal) yang ditandai PERLU REVIEW.
