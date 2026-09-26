# Uji 03 (Penguji Independen) — Manajer Cabang Lapor Omzet 3 Bulan ke Pemilik

## Skenario
Normal #1 (uji sesi ini). Manajer toko cabang melapor omzet 3 bulan ke pemilik usaha
(bukan investor/bank), format tidak disebut → dibuat 4 format.

## Input pengguna (simulasi)
> "Tolong buatkan ringkasan buat pemilik. Omzet cabang saya Juli Rp45.000.000, Agustus
> Rp48.000.000, September Rp52.000.000. Ini laporan bulanan rutin ke owner."

## Langkah kerja (mengikuti SKILL.md langkah 1–8)
1. Sumber angka: disebutkan langsung pengguna — dicatat apa adanya, tidak menambah data.
2. Hitung via script (path relatif folder skill, sesuai contoh di SKILL.md):
   ```bash
   python3 scripts/hitung_perubahan.py \
     --pasangan "Omzet (Jul vs Sep):45000000:52000000" \
     --daftar "Omzet 3 bulan (Jul,Ags,Sep)=45000000,48000000,52000000"
   ```
   Output nyata (dijalankan penguji):
   ```json
   {"pasangan": [{"label": "Omzet (Jul vs Sep)", "nilai_lama": 45000000, "nilai_baru": 52000000,
     "selisih": 7000000, "arah": "naik", "persen_perubahan": 15.6, "catatan": null}],
    "daftar": [{"label": "Omzet 3 bulan (Jul,Ags,Sep)", "jumlah_data": 3, "total": 145000000,
     "rata_rata": 48333333, "min": 45000000, "max": 52000000}]}
   ```
   **Verifikasi independen (Decimal manual):** 52.000.000 − 45.000.000 = 7.000.000;
   7.000.000 ÷ 45.000.000 × 100 = 15,555...% → 15,6% (1 desimal, HALF_UP) ✓ cocok.
   Rata-rata: 145.000.000 ÷ 3 = 48.333.333,33 → 48.333.333 (dibulatkan ke rupiah
   terdekat) ✓ cocok.
3. Kalimat inti: "Omzet cabang naik konsisten 3 bulan berturut-turut, dari Rp45 juta
   (Juli) menjadi Rp52 juta (September), naik 15,6% dari awal periode."
4. 3 angka pendukung: omzet Juli→September (+15,6%), rata-rata bulanan (Rp48,3 juta),
   tren naik 3 bulan berturut-turut (bukan lonjakan satu bulan).
5. Grafik (sesuai `references/pilih-grafik.md`): 3 titik waktu berurutan → grafik garis,
   judul "Omzet Cabang Naik 3 Bulan Berturut-turut", bukan "Omzet per Bulan".
6. Risiko: skill dengan benar **tidak mengarang risiko** karena data tren positif tanpa
   sinyal negatif eksplisit — diisi dengan catatan netral ("tidak ada risiko mendesak
   dari tren ini; perlu dipantau bila pola musiman berubah") alih-alih memaksakan risiko
   yang tidak ada di data. Ini sesuai Batasan SKILL.md (tidak boleh mengarang).
7. Rekomendasi: karena tren positif, rekomendasi diarahkan ke "pertahankan" bukan aksi
   korektif — spesifik: pertahankan alokasi stok & jadwal promo yang sama untuk Oktober,
   PIC: Manajer Cabang, tenggat: awal Oktober.

## Output — Ringkasan WA (5 baris)
```
📊 *Omzet Cabang Jul–Sep 2026*
Omzet naik konsisten 3 bulan berturut-turut, dari Rp45 juta jadi
Rp52 juta (+15,6%).
• Omzet Juli: Rp45.000.000
• Omzet September: Rp52.000.000 (+15,6% dari Juli)
• Rata-rata 3 bulan: Rp48.333.333
👉 Pertahankan alokasi stok & jadwal promo yang sama untuk Oktober.
```

## Output — Email formal (ringkas)
```
Subjek: Omzet Cabang Naik 15,6% dalam 3 Bulan (Jul–Sep 2026)

Selamat pagi/siang, Pak/Bu,

Omzet cabang tercatat naik konsisten selama 3 bulan terakhir: dari
Rp45.000.000 (Juli) menjadi Rp52.000.000 (September), naik 15,6%.
Rata-rata omzet bulanan periode ini Rp48.333.333.

Angka pendukung:
- Omzet Juli: Rp45.000.000
- Omzet September: Rp52.000.000 (+15,6%)
- Rata-rata 3 bulan: Rp48.333.333

Tidak ada risiko mendesak dari tren ini; akan terus dipantau bila pola
musiman berubah di bulan berikutnya.

Rekomendasi:
1. Pertahankan alokasi stok & jadwal promo yang sama untuk Oktober — PIC:
   Manajer Cabang, tenggat: awal Oktober.

Demikian laporan ini kami sampaikan, terima kasih atas perhatiannya.

Terima kasih,
Manajer Cabang
```
(Laporan rutin, bukan minta persetujuan → kalimat penutup memakai versi alternatif
sesuai catatan pemakaian di `templates/email-formal.md`.)

## Output — Satu halaman eksekutif & Skrip bicara
Dibuat mengikuti kerangka `templates/satu-halaman-eksekutif.md` dan
`templates/skrip-bicara.md` dengan angka identik di atas; tidak diulang di sini demi
ringkas — polanya sama dengan `examples/01-omzet-turun-bulan-puasa.md` dan
`examples/02-stok-menumpuk-satu-halaman.md`, hanya kalimat inti & angka yang berbeda.

## Penilaian penguji
- Angka 100% berasal dari script, bukan dikarang. ✓
- Format Rupiah & persen konsisten dengan `references/gaya-komunikasi.md`
  (`Rp45.000.000`, `15,6%`). ✓
- Skill menahan diri dari mengarang "risiko" saat data memang tidak menunjukkan risiko —
  ini justru bukti kepatuhan pada larangan mengarang, bukan cacat.
- Asumsi disebutkan di akhir (lihat SKILL.md langkah 8): penerima = pemilik usaha sesuai
  permintaan eksplisit pengguna, tidak perlu ditebak.
