# Contoh 1 — Omzet Turun di Bulan Puasa, Lapor ke Owner

## Input pengguna
> "Tolong buatkan ringkasan buat owner. Omzet Agustus Rp32.000.000, September (bulan
> puasa) Rp24.500.000. Biaya iklan Agustus Rp4.000.000, September Rp5.600.000. Ini
> untuk owner, tujuannya lapor kondisi terkini dan minta persetujuan turunkan budget
> iklan."

## Langkah kerja
1. Sumber angka: disebutkan langsung oleh pengguna (bukan file) — dicatat apa adanya.
2. Hitung lewat script:
   ```bash
   python3 scripts/hitung_perubahan.py \
     --pasangan "Omzet:32000000:24500000" \
     --pasangan "Biaya iklan:4000000:5600000" \
     --pasangan "Rasio biaya iklan/omzet:0.125:0.2286"
   ```
   Hasil (ringkas):
   - Omzet: Rp32.000.000 → Rp24.500.000, selisih -Rp7.500.000, **-23,4%**
   - Biaya iklan: Rp4.000.000 → Rp5.600.000, selisih +Rp1.600.000, **+40,0%**
   - Rasio biaya iklan/omzet dihitung manual: 4.000.000/32.000.000 = 12,5% →
     5.600.000/24.500.000 = 22,9% (dibulatkan 1 desimal)
3. Kalimat inti: "Omzet September turun 23% karena bulan puasa, tapi biaya iklan justru
   naik 40% sehingga efisiensinya menurun tajam."
4. 3 angka pendukung: omzet (-23%), biaya iklan (+40%), rasio biaya/omzet (12,5% → 22,9%).
5. Grafik: batang berdampingan 2 kolom (Agustus vs September) untuk omzet & biaya iklan
   — hanya 2 titik waktu, bukan tren garis (lihat `references/pilih-grafik.md`).
6. Risiko: bila rasio terus naik, margin bisa tergerus dalam 1-2 bulan ke depan.
7. Rekomendasi: turunkan budget iklan [isian: kanal iklan] sebesar [isian: nominal]/bulan
   mulai minggu depan sambil evaluasi materi iklan — PIC: [isian: nama/jabatan], tenggat:
   minggu depan. (Kanal, besar penurunan, dan PIC tidak ada di input → `[isian: ...]`.)

## Output — Ringkasan WA
```
📊 *Kinerja September 2026*
Omzet turun 23% (bulan puasa), tapi biaya iklan justru naik 40% —
efisiensi iklan menurun tajam.
• Omzet: Rp32.000.000 → Rp24.500.000 (-23%)
• Biaya iklan: Rp4.000.000 → Rp5.600.000 (+40%)
• Rasio biaya iklan/omzet: 12,5% → 22,9%
👉 Usul turunkan budget iklan [isian: kanal iklan] sebesar [isian: nominal]/bulan
mulai minggu depan sambil evaluasi materi iklan. Mohon persetujuan Bapak/Ibu.
```

## Output — Email formal
```
Subjek: Omzet September Turun 23%, Usul Penyesuaian Budget Iklan

Selamat pagi/siang, Pak/Bu,

Omzet September 2026 tercatat Rp24.500.000, turun 23% dibanding Agustus
(Rp32.000.000), bertepatan dengan bulan puasa. Yang perlu jadi perhatian,
biaya iklan justru naik 40% pada periode yang sama, sehingga rasio biaya
iklan terhadap omzet melonjak dari 12,5% ke 22,9%.

Angka pendukung:
- Omzet: Rp32.000.000 → Rp24.500.000 (-23%)
- Biaya iklan: Rp4.000.000 → Rp5.600.000 (+40%)
- Rasio biaya iklan/omzet: 12,5% → 22,9%

Risiko bila dibiarkan:
Bila rasio ini terus naik di bulan berikutnya, margin bisa tergerus lebih
jauh sebelum omzet kembali normal pasca-puasa.

Rekomendasi:
1. Turunkan budget iklan [isian: kanal iklan] sebesar [isian: nominal]/bulan
   mulai minggu depan, sambil mengevaluasi materi iklan yang kurang efektif —
   PIC: [isian: nama/jabatan], tenggat: minggu depan.

Mohon arahan/persetujuan Bapak/Ibu untuk langkah di atas.

Terima kasih,
[isian: nama/jabatan pengirim]
```

## Output — Skrip bicara 2 menit (ringkas)
```
Selamat pagi Pak/Bu, izin sampaikan update singkat.

Omzet kita bulan September turun 23% dibanding Agustus. // Ini bertepatan
dengan bulan puasa, jadi sebagian memang pola musiman. Yang perlu jadi
perhatian, biaya iklan kita malah naik 40% di periode yang sama.

Rasio biaya iklan terhadap omzet naik dari 12,5% jadi hampir 23% //
— hampir dua kali lipat.

Kalau dibiarkan, efisiensi iklan kita bisa makin turun di bulan berikutnya.

Rekomendasi kami, budget iklan [isian: kanal iklan] diturunkan dulu sebesar
[isian: nominal] per bulan mulai minggu depan, sambil kami evaluasi materi
iklannya. // Mohon
persetujuan Bapak/Ibu untuk langkah ini.

Itu ringkasannya. // Ada yang ingin ditanyakan?
```

## Asumsi yang disebutkan ke pengguna
- Penerima: owner/pemilik usaha (sesuai permintaan)
- Kanal iklan, besar penurunan budget, dan PIC tidak disebutkan pengguna → ditulis
  `[isian: ...]` untuk diisi sebelum dikirim (revisi 2026-10-13).
- Format 1 halaman eksekutif tidak dibuat karena pengguna hanya minta "ringkasan" —
  ditawarkan sebagai opsi tambahan, tidak dipaksakan.
