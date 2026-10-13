# Uji OpenClaw SEBELUM vs SESUDAH — analisis-rasio-keuangan-usaha

Sumber (ada di paket VIP): `solusi-vip/kantor-manajemen/UJI-OPENCLAW.md` (rincian: `solusi-vip/kantor-manajemen/uji-openclaw/03-rasio-keuangan-bahan-komisaris.md` dan `03-rasio-keuangan-ulang3.md`). Tanggal uji: 2026-10-01 (Asia/Jakarta). Versi skill saat uji: uji pertama tidak dicatat di sumber (sebelum revisi 1.0.4); uji ulang ke-3 = 1.0.4 (versi katalog saat ini 1.0.5). Penguji: agent penguji independen (bukan pembuat skill).

Berkas ini hanya menyalin ringkasan dari catatan uji internal di atas; balasan utuh kedua sisi ada di berkas sumber.

## Cara uji
- OpenClaw lokal (`openclaw agent --local`, tanpa Telegram/gateway), model router Komunitech yang sama dengan bot member (`ninerouter/komunitech`, jawaban `claude-sonnet-5`).
- SEBELUM = home tanpa skill; SESUDAH = home dengan paket skill Kantor & Manajemen. Kedua home dibuat ulang bersih sebelum skenario.
- Pesan member: neraca 31 Des 2025 dan laba rugi 2025 sebuah perusahaan dagang (penjualan Rp9,6 M, kas Rp420 jt, utang bank jangka pendek Rp900 jt), "dicek sehat ga perusahaannya, buat bahan rapat sama komisaris".
- Semua rasio dihitung ulang penguji dengan Python (rasio lancar 1,657; cepat 1,066; kas 0,253; DER 1,390; cakupan bunga 2,290; margin kotor 22,5%; dan seterusnya).

## Skor (skala 10)

| # | Skenario | Tanpa skill | Dengan skill (uji pertama) | Dengan skill (uji ulang ke-3, v1.0.4) | Pembeda satu kalimat |
|---|---|---|---|---|---|
| 1 | Rasio keuangan neraca + laba rugi untuk bahan rapat komisaris | 8 | 8 | 9 | Uji pertama seri: semua angka benar di kedua sisi, tanpa skill menangkap risiko utang bank jangka pendek (Rp900 jt) melebihi kas (Rp420 jt) sedangkan dengan skill salah menenangkan ("tidak ada risiko gagal bayar jangka pendek", rasio kas hijau); setelah revisi: risiko likuiditas "SEDANG", kas hanya menutup 47% utang bank jangka pendek, rasio kas kuning, semua angka dari script. |
| | **Rata-rata** (satu skenario) | **8** | **8** | **9** | |

## Verdik
**LULUS uji ulang ke-3** (9). Pada uji pertama hasilnya SERI, dan sumber melarang memakai skenario ini sebagai bukti sebelum/sesudah; setelah uji ulang sumber menyebut cuplikan jualan kini layak.

## Catatan jujur
- Selisih terhadap sisi tanpa skill hanya 1,0 poin (9 melawan 8) dan sisi tanpa skill tidak diulang; untuk laporan yang rapi, model tanpa skill sudah pandai menghitung rasio dasar.
- Cacat uji pertama sisi dengan skill: ambang UMKM dipakai untuk perusahaan menengah, rasio kas 0,25 diberi tanda hijau, dan jenis usaha "dagang" diasumsikan tanpa disebut. Dua cacat pertama hilang pada uji ulang ke-3; jenis usaha tertulis di kepala laporan ("Usaha dagang, skala kecil") tetapi belum diberi label asumsi (README skill mencatat perbaikan di 1.0.5; tidak ada catatan uji ulang OpenClaw untuk 1.0.5 di sumber).
- Uji ulang ke-3 mengoreksi laporan uji pertama: omzet Rp9,6 M tergolong usaha kecil menurut PP 7/2021 (bukan menengah).
- Regresi kecil uji ulang: saran no. 3 tumpang tindih dengan saran no. 1, dan label "ROA/ROE disetahunkan" tidak perlu untuk data setahun penuh.
- Hanya satu skenario di OpenClaw.
