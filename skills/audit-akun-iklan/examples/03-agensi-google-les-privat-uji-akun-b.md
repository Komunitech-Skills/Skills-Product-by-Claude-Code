# Uji 03 (penguji independen, Akun B) - Agensi kecil mengaudit Google Ads klien les privat

> Uji simulasi agent oleh penguji terpisah, 2026-09-26. Data fiktif. Skenario: **normal 3**.

## Permintaan pengguna
"Saya freelancer iklan, baru pegang klien les privat tatap muka di Jakarta Selatan. Belanja Google
Ads-nya Rp6 jt/bulan. Sebelum saya kelola, tolong audit dulu dari screenshot ini, hasilnya mau saya
tunjukkan ke klien." (screenshot: Konversi, Setelan kampanye, Kata kunci, Istilah penelusuran 30 hari, Aset)

## Perilaku agent
- `daftar --platform google`. Tidak meminta akses/login; agensi memberi screenshot.
- Harga paket Rp1,2 jt/bulan, modal pengajar Rp400rb, biaya lain Rp50rb →
  `roas-impas --harga "Rp 1,2 jt" --modal 400.000 --biaya-lain 50rb` → laba Rp750.000, impas 1,60
  (dipakai untuk G11).
- `hitung ... --belanja google=6jt --usaha "Les Privat Cerdas (klien agensi)"` (tanpa `--mulai`).

## Output script (ringkas)
```
Skor gabungan: 36,5 / 100 (Kritis) - FINAL; bobot: porsi belanja
- Google Ads: 36,5/100 (Kritis); bukti 100,0% (final); belanja Rp 6.000.000
    Pelacakan 42,9 | Struktur 13,6 | Audiens 0,0 | Anggaran 100,0 | Materi 37,5 | Halaman 50,0 | Pengecualian 0,0
PRIORITAS: 1 G02 (15, +8,9) · 2 G05 (15, +6,8) · 3 G15 (9, +11,3) · 4 G03 (9, +5,4) · 5 G08 (9, +5,0)
           6 G07 (9, +4,1) · 7 G12 (9, +3,8) · 8 G09 (6, +5,0) · 9 G06 (6, +2,0) · 10 G14 (3, +5,0) · G16 (3) · G13 (3)
Rencana: H1 G02,G05,G15 · H2 G03,G08,G07 · H3 G12,G09 · H4 G06 · H5 G14 · H6 diam · H7 laporan; antrean G16, G13
```

## Jawaban akhir agent (ringkas, siap ditunjukkan ke klien)
Skor **36,5/100 – Kritis – final (bukti 100%)**.
1. **Kunjungan halaman /jadwal dihitung sebagai konversi utama** – Google mengira iklan sukses padahal
   belum ada yang daftar. Jadikan Sekunder (±10 menit). Sekaligus ubah hitungan formulir ke "Satu".
2. **Mantan freelancer klien masih Admin** – hapus, nyalakan 2FA (±10 menit).
3. **18% biaya ke pencarian "les privat gratis" & "lowongan guru les"** – pasang kata kunci negatif
   (±30 menit), lalu buat daftar negatif bersama.
Juga: lokasi "Kehadiran atau minat" → "Kehadiran" (les tatap muka), matikan Jaringan Display di kampanye Penelusuran.

## Catatan penguji
- Angka cocok 100% dengan verifikasi independen.
- Cek Google (G03 hitungan One/Every, G07 Display di Search, G08 opsi Kehadiran, G12 Kekuatan iklan,
  15 judul/4 deskripsi) sesuai dokumentasi Google Ads.
- G10 "15–30 konversi/30 hari" diberi label patokan umum — wajar (Google Help menyebut 15 konversi
  sebagai minimum lama tROAS dan menyarankan lebih banyak data). Frasa "Maksimalkan klik/konversi
  **dengan batas**" agak kabur untuk awam (batas CPC hanya ada di Maksimalkan klik).
- Skill cocok untuk agensi (format rapi, tanpa akses akun). Belum ada versi "laporan ke klien"
  ber-kop, tapi itu di luar janji README.

## Penyegaran v1.0.7 (2026-10-17)
> Hasil, angka, dan skor di atas **tidak diubah**. `roas-impas --harga "Rp 1,2 jt" --modal 400.000 --biaya-lain 50rb` dijalankan ulang dengan skrip v1.0.7: laba kotor Rp750.000, ROAS impas 1,60 (cocok; Decimal: 1.200.000 − 400.000 − 50.000 = 750.000; 1.200.000 ÷ 750.000 = 1,60). Bukti 100% → Format output audit lengkap, tidak berubah di v1.0.7. Bila ada pertanyaan lanjutan, letaknya di akhir balasan, maks. 5. Laporan untuk klien ditulis tanpa nama skrip/berkas internal dan tanpa istilah proses.
