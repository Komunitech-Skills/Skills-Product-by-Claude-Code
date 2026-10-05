# Uji 05 (Penguji Independen) — Pemilik UMKM Siapkan Ringkasan untuk Petugas Bank KUR

## Skenario
Normal #3. Pemilik UMKM menyiapkan ringkasan untuk petugas bank (pengajuan KUR) — audiens
"Bank/lembaga keuangan" di `references/gaya-komunikasi.md`, menguji nada formal/hati-hati
klaim dan disclaimer keuangan di Batasan SKILL.md.

## Input pengguna (simulasi)
> "Saya mau ajukan KUR ke bank, tolong buatkan ringkasan usaha saya. Omzet tahun lalu
> Rp180.000.000, tahun ini Rp225.000.000. Laba bersih tahun lalu Rp22.000.000, tahun ini
> Rp31.000.000. Ini untuk petugas bank."

## Langkah kerja
1. Sumber angka: disebutkan langsung pengguna.
2. Hitung via script:
   ```bash
   python3 scripts/hitung_perubahan.py \
     --pasangan "Omzet tahunan:180000000:225000000" \
     --pasangan "Laba bersih:22000000:31000000"
   ```
   Output nyata:
   ```json
   {"pasangan": [
     {"label": "Omzet tahunan", "nilai_lama": 180000000, "nilai_baru": 225000000,
      "selisih": 45000000, "arah": "naik", "persen_perubahan": 25.0, "catatan": null},
     {"label": "Laba bersih", "nilai_lama": 22000000, "nilai_baru": 31000000,
      "selisih": 9000000, "arah": "naik", "persen_perubahan": 40.9, "catatan": null}]}
   ```
   **Verifikasi independen:** 45.000.000/180.000.000×100=25,0% ✓;
   9.000.000/22.000.000×100=40,909...%→40,9% (HALF_UP) ✓.
3. Kalimat inti: "Omzet usaha naik 25% dan laba bersih naik 40,9% dalam setahun terakhir,
   menunjukkan pertumbuhan yang mendukung pengajuan tambahan modal kerja."
4. 3 angka pendukung: omzet tahunan (+25%), laba bersih (+40,9%), margin laba tersirat
   (skill **tidak menghitung margin baru** karena tidak diminta/tidak ada di data —
   memakai 2 angka di atas + 1 fakta konkret "2 tahun berturut-turut mencatat laba
   positif" alih-alih memaksakan angka margin yang tidak dihitung, sesuai larangan
   mengarang di Batasan SKILL.md).
5. Nada: formal, hati-hati klaim — tidak memproyeksikan angka masa depan yang belum
   pasti (sesuai tabel sapaan "Bank/lembaga keuangan: formal, hati-hati klaim, jangan
   melebih-lebihkan proyeksi").
6. Disclaimer: SKILL.md Batasan menyebut "Bukan nasihat keuangan/investasi — untuk
   laporan ke bank, sarankan tetap ditinjau pemilik usaha/akuntan sebelum dikirim" — ini
   **wajib muncul** di output untuk skenario ini.

## Output — Email formal (untuk petugas bank)
```
Subjek: Ringkasan Kinerja Usaha — Pengajuan KUR

Dengan hormat,

Usaha kami mencatat pertumbuhan omzet 25% dalam setahun terakhir, dari
Rp180.000.000 menjadi Rp225.000.000, dengan laba bersih naik 40,9% dari
Rp22.000.000 menjadi Rp31.000.000.

Angka pendukung:
- Omzet tahunan: Rp180.000.000 → Rp225.000.000 (+25%)
- Laba bersih: Rp22.000.000 → Rp31.000.000 (+40,9%)
- Usaha mencatat laba positif 2 tahun berturut-turut

Rekomendasi:
1. Mengajukan pinjaman KUR untuk mendukung modal kerja seiring pertumbuhan
   usaha — PIC: Pemilik Usaha, tenggat: sesuai jadwal pengajuan bank.

Kami siap melampirkan dokumen pendukung (laporan keuangan, mutasi rekening)
sesuai kebutuhan Bapak/Ibu.

Terima kasih,
Pemilik Usaha

---
Catatan: Ringkasan ini bukan nasihat keuangan/investasi. Untuk pengajuan
bernilai besar seperti ini, dokumen sebaiknya tetap ditinjau akuntan/pihak
berkompeten sebelum dikirim ke bank.
```

## Penilaian penguji
- Skill **benar menahan diri** tidak menghitung/mengarang angka margin laba yang tidak
  diminta pengguna maupun tidak dihasilkan script — sesuai instruksi.
- Disclaimer keuangan pada Batasan SKILL.md **muncul secara eksplisit** di output,
  bukan diabaikan — penting untuk konteks bank/KUR yang berisiko tinggi bila salah.
- Nada formal sesuai tabel sapaan "Bank/lembaga keuangan: Dengan hormat" — cocok dengan
  `references/gaya-komunikasi.md`.
- Tidak ada proyeksi masa depan yang dilebih-lebihkan (mis. tidak menyebut "tahun depan
  omzet akan naik lagi") — sesuai instruksi kehati-hatian klaim ke bank.
