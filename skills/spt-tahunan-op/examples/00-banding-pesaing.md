# 00 — Uji banding pesaing

Penguji independen, 2026-09-30. Pesaing hanya **dibaca/dinilai**, tidak disalin.

## Pencarian
- GitHub: "SPT tahunan orang pribadi kalkulator", "PPh pasal 17 python", "SKILL.md pajak indonesia" → hanya kalkulator PPh 21 sederhana (mis. github.com/kurabaya/python-pph-21), tidak ada skill agent SPT OP.
- ClawHub / skills.sh / anthropics/skills: kata kunci "SPT", "Indonesia tax", "PPh" → tidak ditemukan skill SPT Tahunan OP Indonesia (per pencarian web; direktori tidak diperiksa langsung).
- Kalkulator online: **kalkulatorpajak.id/kalkulator/spt-tahunan-pph-orang-pribadi-coretax** (pesaing terkuat), klikpajak.id (artikel simulator), simulator resmi DJP spt-simulasi.pajak.go.id (perlu login, tidak diuji).

## Skenario 06 (K/2, neto 180 jt, PPh 21 10,5 jt)
Kalkulator kalkulatorpajak.id memakai rumus sama (PTKP, tarif Ps. 17, pembulatan ribuan) → hasil yang diharapkan sama: KB Rp375.000. Kalkulator ini **tidak dijalankan interaktif** oleh penguji; penilaian berdasarkan fitur yang dibaca dari halamannya.

| Aspek | kalkulatorpajak.id | Skill spt-tahunan-op |
|---|---|---|
| Cakupan | **Lebih luas**: PPh 24 luar negeri, kompensasi kerugian 5 tahun, pembukuan, harta/utang, cetak ringkasan | Karyawan, NPPN, pembukuan (neto ≥ 0), zakat, PPh 21/22/23/25; rugi & PPh 24 di luar cakupan |
| Input | Formulir web, harus tahu istilah | Bahasa sehari-hari; agent memetakan & bertanya sekali |
| Validasi angka | Formulir angka | Menolak angka ambigu (1,500 · 2.5jt · 5m), status tanggungan > 3, NPPN ≥ Rp4,8 M |
| Syarat NPPN (pemberitahuan ≤ 3 bulan) | Tidak disebut jelas | Ditanyakan + peringatan konsekuensi |
| Penjelasan awam & langkah Coretax | Minim | Ada (kenapa KB/LB, peta lampiran, langkah bayar) |
| Privasi | Klien-side | Lokal, tanpa jaringan |

**Kesimpulan:** skill kita unggul untuk pengguna awam (input bahasa biasa, penjelasan, validasi, peringatan NPPN, checklist), tetapi kalah cakupan (rugi/kompensasi, PPh 24). Tidak kalah pada skenario uji. Pelajaran (tulis ulang dengan cara sendiri bila dikembangkan): pertimbangkan dukungan kompensasi kerugian & PPh 24 di versi berikutnya.
