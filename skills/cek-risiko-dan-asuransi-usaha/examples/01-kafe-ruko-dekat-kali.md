# 01 — Normal: kafe ruko dekat kali, Bekasi

**Input:** lihat pesan di `00-pembanding-tanpa-skill.md` (kafe 3 karyawan, biaya tetap terperinci, kas 8 jt, pernah banjir 2020).
**Data risiko:** `data/01-kafe-bekasi.json`.

**Output SESUDAH:** lihat bagian "SESUDAH" di `00-pembanding-tanpa-skill.md` (9 baris risiko, dana darurat, perlindungan generik, 3 prioritas, 3 pertanyaan).

**Verifikasi angka (independen, `data/verifikasi-independen.py`):**
- Skor: 12, 10, 9, 9, 9, 8, 6, 4, 4 → tingkat sesuai batas 1-4/5-9/10-14/15-25. Cocok.
- Biaya tetap 4.500.000 + 3×2.800.000 + 1.700.000 + 1.200.000 = 15.800.000; target 3 bln 47.400.000; kekurangan 39.400.000; 8/15,8 = 0,51 bln; cicilan 12 bln = 3.283.333,3 → Rp3.283.334 (dibulatkan ke atas agar target tercapai). Cocok.

**Catatan:**
- Script tidak menghitung cicilan menabung; SKILL.md langkah 6 menyuruh agent menghitungnya ("hitung dengan angka"), jumlah bulan cicilan tidak ditentukan. Risiko agent menghitung di kepala.
- "Gaji @2,8jt × 3": bila agent menulis `Gaji=2800000,Gaji=2800000,Gaji=2800000`, script **diam-diam** hanya menghitung satu (kunci dobel tertimpa) → biaya Rp10.200.000, target salah. Lihat HASIL-UJI cacat B1.
- Gempa 1×4 = 4 → "Terima / Tidak" (lihat cacat B3).

**Skor: SEBELUM 6,5 · SESUDAH 8.**
