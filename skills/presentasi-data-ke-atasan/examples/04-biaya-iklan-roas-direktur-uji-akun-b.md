# Uji 04 (Penguji Independen) — Staf Keuangan Lapor Biaya Iklan Naik 40% tapi ROAS Turun

## Skenario
Normal #2. Staf keuangan melapor ke direktur: biaya iklan naik 40%, tapi ROAS (return on
ad spend) turun — kabar campuran/buruk, menguji apakah skill "sopan-langsung" bukan
menutup-nutupi.

## Input pengguna (simulasi)
> "Buatkan laporan untuk direktur. Biaya iklan kita naik dari Rp10.000.000 jadi
> Rp14.000.000. Omzet yang dihasilkan dari iklan itu malah turun dari Rp50.000.000 jadi
> Rp42.000.000. ROAS turun dari 5 ke 3. Saya mau minta keputusan soal anggaran iklan
> bulan depan."

## Langkah kerja
1. Sumber angka: disebutkan langsung pengguna.
2. Hitung via script:
   ```bash
   python3 scripts/hitung_perubahan.py \
     --pasangan "Biaya iklan:10000000:14000000" \
     --pasangan "Omzet dari iklan:50000000:42000000" \
     --pasangan "ROAS:5:3"
   ```
   Output nyata:
   ```json
   {"pasangan": [
     {"label": "Biaya iklan", "nilai_lama": 10000000, "nilai_baru": 14000000,
      "selisih": 4000000, "arah": "naik", "persen_perubahan": 40.0, "catatan": null},
     {"label": "Omzet dari iklan", "nilai_lama": 50000000, "nilai_baru": 42000000,
      "selisih": -8000000, "arah": "turun", "persen_perubahan": -16.0, "catatan": null},
     {"label": "ROAS", "nilai_lama": 5, "nilai_baru": 3, "selisih": -2, "arah": "turun",
      "persen_perubahan": -40.0, "catatan": null}]}
   ```
   **Verifikasi independen:** 4.000.000/10.000.000×100=40,0% ✓; −8.000.000/50.000.000×100
   =−16,0% ✓; (3−5)/5×100=−40,0% ✓. Semua cocok dengan output script.
3. Kalimat inti (langsung, tidak menutup-nutupi, sesuai `references/gaya-komunikasi.md`):
   "Biaya iklan naik 40% tapi omzet dari iklan justru turun 16%, sehingga ROAS anjlok
   40% dari 5 kali menjadi 3 kali — efisiensi iklan menurun tajam, perlu keputusan
   anggaran."
4. 3 angka pendukung: biaya iklan (+40%), omzet dari iklan (-16%), ROAS (5→3, -40%).
5. Grafik: 2 titik waktu (bulan lalu vs bulan ini) untuk 3 metrik → batang berdampingan,
   bukan garis (sesuai `references/pilih-grafik.md` poin "sebelum vs sesudah / dua titik
   saja").
6. Risiko: bila ROAS terus turun, setiap tambahan Rp1 iklan menghasilkan omzet lebih
   kecil dari sebelumnya — anggaran iklan bisa jadi tidak lagi menguntungkan bila
   dibiarkan tanpa evaluasi.
7. Rekomendasi: hentikan sementara penambahan budget iklan bulan depan, evaluasi materi
   iklan & targeting sebelum menambah anggaran lagi — PIC: Tim Marketing, tenggat: 2
   minggu.

## Output — Ringkasan WA
```
📊 *Efisiensi Iklan Bulan Ini*
Biaya iklan naik 40% tapi omzet dari iklan malah turun 16% —
ROAS anjlok dari 5x jadi 3x (-40%).
• Biaya iklan: Rp10.000.000 → Rp14.000.000 (+40%)
• Omzet dari iklan: Rp50.000.000 → Rp42.000.000 (-16%)
• ROAS: 5x → 3x (-40%)
👉 Usul tahan dulu penambahan budget bulan depan, evaluasi
materi & targeting iklan dalam 2 minggu. Mohon arahan Bapak/Ibu.
```

## Output — Email formal (ringkas)
```
Subjek: ROAS Turun 40% — Biaya Iklan Naik, Hasil Justru Turun

Yth. Bapak/Ibu Direktur,

Biaya iklan bulan ini naik 40% (Rp10.000.000 menjadi Rp14.000.000), namun
omzet yang dihasilkan dari iklan tersebut justru turun 16% (Rp50.000.000
menjadi Rp42.000.000). Akibatnya ROAS turun dari 5 kali menjadi 3 kali
(-40%) — efisiensi iklan menurun tajam.

Angka pendukung:
- Biaya iklan: Rp10.000.000 → Rp14.000.000 (+40%)
- Omzet dari iklan: Rp50.000.000 → Rp42.000.000 (-16%)
- ROAS: 5x → 3x (-40%)

Risiko bila dibiarkan:
Bila ROAS terus turun, setiap tambahan anggaran iklan menghasilkan omzet
yang semakin kecil, membuat pengeluaran iklan tidak lagi menguntungkan.

Rekomendasi:
1. Tahan dulu penambahan budget iklan bulan depan — PIC: Tim Marketing,
   tenggat: segera.
2. Evaluasi materi iklan & targeting sebelum menambah anggaran lagi — PIC:
   Tim Marketing, tenggat: 2 minggu.

Mohon arahan/persetujuan Bapak/Ibu untuk langkah di atas.

Terima kasih,
Staf Keuangan
```

## Penilaian penguji
- Skill **tidak menghaluskan kabar buruk**: kalimat inti langsung menyebut "ROAS anjlok
  40%" dengan angka, bukan eufemisme ("kurang optimal"). Sesuai prinsip
  `references/gaya-komunikasi.md`.
- Tidak menyalahkan pihak tertentu (mis. "Tim Marketing gagal") — hanya angka +
  rekomendasi aksi, sesuai aturan "langsung tapi tidak kasar".
- ROAS dipakai sebagai pasangan angka biasa (bukan Rupiah) — script tetap menghasilkan
  hasil benar (5→3, -40%) karena tidak memaksakan format Rupiah pada `nilai_lama`/
  `nilai_baru` walau nama fungsi `rupiah()` dipakai untuk pembulatan bilangan bulat semua
  jenis angka (bukan cuma Rupiah) — sedikit membingungkan dari sisi penamaan internal
  tapi tidak memengaruhi kebenaran hasil (dicatat di HASIL-UJI.md sebagai temuan minor).
