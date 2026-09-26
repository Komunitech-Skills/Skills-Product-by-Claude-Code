# Uji A/B — Skenario 01 TANPA skill vs DENGAN skill

> Penguji independen, 2026-09-25. Permintaan sama dengan `01-op-umkm-karyawan-okt26-mar27.md`:
> "Saya punya warung sembako, bayar pajak 0,5% yang UMKM itu, karyawan 3 orang. Tolong bikinin jadwal pajak dari Oktober sampai Maret tahun depan, sekalian file buat Google Calendar di HP."
>
> **Metode (jujur):** tidak tersedia sesi agent kedua yang benar-benar bersih; jawaban "TANPA skill" disusun penguji dengan meniru jawaban tipikal agent umum yang hanya mengandalkan pengetahuan umum (aturan tgl 15/20/akhir bulan PMK 81/2024 dikenal umum), **tanpa** script dan **tanpa** data SKB libur 2027 (baru terbit 15 Sep 2026). Diasumsikan agent itu *menyebut* aturan geser hari libur tetapi tidak menerapkannya per tanggal — pola paling umum pada jawaban LLM. Ini perkiraan, bukan rekaman sesi.

## A. Jawaban TANPA skill (simulasi, dipersingkat)
> Berikut jadwal pajak Anda (PMK 81/2024):
> | Bulan | Setor PPh Final 0,5% | Setor PPh 21 | Lapor SPT Masa PPh 21 |
> |---|---|---|---|
> | Okt 2026 | 15 Okt | 15 Okt | 20 Okt |
> | Nov 2026 | 15 Nov | 15 Nov | 20 Nov |
> | Des 2026 | 15 Des | 15 Des | 20 Des |
> | Jan 2027 | 15 Jan | 15 Jan | 20 Jan |
> | Feb 2027 | 15 Feb | 15 Feb | 20 Feb |
> | Mar 2027 | 15 Mar | 15 Mar | 20 Mar |
> SPT Tahunan OP: 31 Maret 2027. Jika tanggal jatuh pada hari libur, batasnya hari kerja berikutnya.
> Untuk Google Calendar, buat acara berulang "tiap tanggal 15" dan "tiap tanggal 20" dengan pengingat.

## B. Jawaban DENGAN skill
Tabel 20 tenggat bertanggal pasti + hari, alasan pergeseran per baris, catatan per kewajiban, disclaimer, dan file .ics valid (20 acara, pengingat H-3 & H-1). Lengkap: lihat `01-op-umkm-karyawan-okt26-mar27.md`.

## C. Perbandingan per kriteria
| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| Ketepatan tanggal (acuan: penghitung independen penguji + SKB 2026/2027) | 13/20 benar. **7 salah** bila diikuti apa adanya: 15 Nov 2026 (Minggu) ×2, 20 Des 2026 (Minggu), 20 Feb 2027 (Sabtu), 15 Mar 2027 (cuti bersama Idulfitri) ×2, 20 Mar 2027 (Sabtu) | **20/20 benar** |
| Pergeseran libur | Hanya kalimat umum; pengguna harus cek sendiri. Tidak tahu cuti bersama 15 Mar 2027 | Diterapkan per tanggal + alasan ("15 Mar Cuti bersama Idulfitri 1448 H") |
| Kelengkapan kewajiban | Tidak ada BPA1 (bukti potong tahunan karyawan, 31 Jan); tidak menjelaskan PPh 0,5% dianggap lapor saat setor & batas omzet Rp500 juta; tidak menyebut SPT Tahunan tidak bergeser | Lengkap untuk profil: PPh final, PPh 21 setor+lapor, BPA1, SPT Tahunan OP + catatan per kewajiban |
| Siap pakai | Acara berulang "tiap tgl 15/20" di kalender justru mengunci tanggal yang salah saat libur | File .ics siap impor, tanggal sudah digeser, UID stabil, checklist bulanan tersedia |
| Keamanan/disclaimer | Minim | Disclaimer + dasar aturan + tanggal cek + butir PERLU REVIEW |

## D. Kesimpulan
Dengan skill **jelas lebih baik**: 7 tenggat yang akan meleset/membingungkan tanpa skill menjadi benar, plus file kalender yang langsung bisa dipakai. Syarat A/B terpenuhi (tidak ada batas skor maks. 6 dari kriteria ini).
