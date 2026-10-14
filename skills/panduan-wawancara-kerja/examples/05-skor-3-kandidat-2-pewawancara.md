# 05 - Skor 3 kandidat dari 2 pewawancara -> peringkat (script)

- **Jenis skenario:** normal + script hitung skor
- **Diuji:** 2026-10-14, OpenClaw 2026.10.2 lokal, model router Komunitech (claude-sonnet-5), home berisi hanya skill ini. Penguji independen.
- **Nilai:** 9,0. Perbandingan lengkap dengan sisi tanpa skill: `00-openclaw-sebelum-sesudah.md`.

## Input (pesan pengguna, fiktif)

> Wawancara kasir kafe sudah selesai. Ini skor dari saya (Lina) dan Mas Arif, skala 1-5.
> Bobot: Ketelitian uang 30% (wajib bagus), Layanan pelanggan 25%, Kecepatan saat ramai 20%, Kejujuran 15% (wajib bagus), Kerja sama tim 10%. Urutan skor di bawah sama dengan urutan bobot ini.
>
> Dina  -> Lina: 4 / 4 / 3 / 4 / 3   | Arif: 4 / 5 / 3 / 4 / 4
> Rizal -> Lina: 3 / 4 / 4 / 4 / 4   | Arif: 5 / 4 / 4 / 3 / 4
> Wulan -> Lina: 3 / 5 / 4 / 4 / 5   | Arif: 2 / 3,5 / 4 / 4 / 4
>
> Siapa yang paling layak? Tolong bikinin peringkatnya.

## Output dengan skill (apa adanya)

> Sudah dihitung, Mbak Lina. Ketiganya dinilai dari 2 pewawancara (Lina, Arif) dengan bobot: Ketelitian uang 30% (kritis), Layanan pelanggan 25%, Kecepatan saat ramai 20%, Kejujuran 15% (kritis), Kerja sama tim 10%.
>
> **Peringkat**
> 1. **Rizal** — total **3,93 / 5** → Disarankan lanjut
> 2. **Dina** — total **3,88 / 5** → Disarankan lanjut
> 3. **Wulan** — total **3,66 / 5** → Pertimbangkan (cadangan)
>
> Rizal dan Dina sangat dekat (selisih 0,05), jadi praktisnya bisa dibilang seri kuat di posisi teratas.
>
> **Rata-rata per kompetensi**
> - Rizal: Ketelitian uang 4,00; Layanan pelanggan 4,00; Kecepatan saat ramai 4,00; Kejujuran 3,50; Kerja sama tim 4,00
> - Dina: Ketelitian uang 4,00; Layanan pelanggan 4,50; Kecepatan saat ramai 3,00; Kejujuran 4,00; Kerja sama tim 3,50
> - Wulan: Ketelitian uang **2,50**; Layanan pelanggan 4,25; Kecepatan saat ramai 4,00; Kejujuran 4,00; Kerja sama tim 4,50
>
> **Perlu dibahas** (selisih penilai > 1,5 poin)
> - Rizal, Ketelitian uang: Lina 3 vs Arif 5 (selisih 2). Ini kompetensi kritis (30%, wajib bagus) — sebaiknya dibahas dulu sebelum memutuskan. Bahan diskusi: "Bukti apa yang masing-masing catat untuk skor ini? Apakah ada jawaban yang ditangkap berbeda?"
>
> **Ringkasan tiap kandidat**
> - **Rizal**: terkuat di Ketelitian uang & konsisten di semua sisi lain; terlemah Kejujuran (3,50). Tapi ada selisih besar soal ketelitian uang antar penilai — klarifikasi dulu sebelum final.
> - **Dina**: terkuat Layanan pelanggan (4,50); terlemah Kecepatan saat ramai (3,00) — perlu dicek apakah ini akan jadi masalah di jam sibuk kafe.
> - **Wulan**: terkuat Kerja sama tim (4,50), tapi Ketelitian uang-nya paling lemah dari ketiganya (2,50) — ini kompetensi kritis dan wajib bagus, jadi jadi pertimbangan serius meski sisi layanan dan kerja samanya bagus.
>
> **Catatan**
> Ini alat bantu, keputusan akhir tetap di tangan Mbak Lina dan tim. Langkah selanjutnya yang masuk akal: diskusikan dulu selisih penilaian soal Rizal (ketelitian uang), lalu putuskan antara Rizal/Dina untuk posisi utama. Kalau mau pegang cadangan, Wulan unggul di servis dan tim tapi perlu diyakinkan dulu soal ketelitian uang — misalnya lewat tes praktik hitung kembalian kalau belum dilakukan.

## Catatan penguji
- Data uji JSON yang setara dan keluaran script: `data/skor-05-kasir-kafe.json`, `data/hasil-script-05.txt`.
- Verifikasi independen (Python, pecahan persis): rata-rata Rizal 4/4/4/3,5/4, Dina 4/4,5/3/4/3,5, Wulan 2,5/4,25/4/4/4,5; total 3,925 -> 3,93; 3,875 -> 3,88; 3,6625 -> 3,66 (setengah ke atas sekali). Semua angka di jawaban cocok.
- Perlu dibahas hanya Rizal/Ketelitian uang (3 vs 5, selisih 2); Wulan/Layanan selisih tepat 1,5 benar tidak ditandai. "Wajib bagus" dipetakan ke kritis, sehingga Wulan (Ketelitian 2,50 < 3,0) = Pertimbangkan (cadangan).
- Tanpa skill: total benar, tetapi selisih 2 poin di kompetensi kritis kandidat peringkat 1 terlewat, yang ditonjolkan justru selisih 1 poin.
- Kekurangan: Rizal disebut "terkuat di Ketelitian uang" padahal seri 4 kompetensi di 4,00 dan kompetensi itu yang perlu dibahas (cara script memilih "terkuat" saat seri).
- Nilai 9,0 vs tanpa skill 6,5.
