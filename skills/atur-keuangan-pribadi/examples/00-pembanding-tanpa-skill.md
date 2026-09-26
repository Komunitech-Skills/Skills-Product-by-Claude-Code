# Uji A/B — Skenario 02 TANPA skill vs DENGAN skill

> Penguji independen, 2026-09-26. Kriteria: ketepatan angka bunga & bulan lunas, kejelasan, keamanan.
> Kebenaran acuan = simulasi Fraction independen penguji (`HASIL-UJI.md` §4): Avalanche = Snowball = **10 bulan**, total bunga **Rp4.226.895**, lunas pinjol b-1 / paylater b-2 / KK b-5 / KTA b-10; KTA flat 0,9%/bln ≡ efektif **1,6275%/bln (19,53%/th)**.
>
> **Keterbatasan metode:** penguji tidak punya alat untuk menjalankan agent terpisah yang benar-benar "bersih". Jawaban TANPA skill di bawah ditulis penguji sebagai asisten umum **tanpa membuka folder skill dan tanpa menjalankan kode** (hanya hitung di kepala), dengan data yang sama (paylater 2,5%/bln min 300 rb; pinjol 0,1%/hari min 500 rb). Karena penguji sudah membaca skill, ada risiko bias; untuk mengimbanginya jawaban dibuat sebaik yang wajar dari asisten umum yang cakap.

## Input (sama)
Kartu kredit Rp12 jt 1,75%/bln min 5%; KTA Rp30 jt flat 0,9%/bln 24 bln; paylater Rp3 jt (2,5%/bln, min Rp300 rb); pinjol legal Rp2 jt (0,1%/hari, min Rp500 rb); dana lebih Rp2,5 jt/bln.

## A. TANPA skill (jawaban asisten umum)
> Metode **avalanche** (bunga tertinggi dulu) paling hemat, **snowball** (saldo terkecil dulu) paling memotivasi. Urutan bunga: pinjol (0,1%/hari ≈ 3%/bln) > paylater 2,5% > kartu kredit 1,75% > KTA 0,9%/bln. Kebetulan urutan saldo terkecil juga sama, jadi kedua metode praktis sama.
>
> Cicilan minimum: KK Rp600 rb, KTA Rp1,52 jt (30 jt/24 + 0,9% × 30 jt), paylater Rp300 rb, pinjol Rp500 rb → total Rp2,92 jt + ekstra Rp2,5 jt = Rp5,42 jt/bln.
> - Pinjol lunas ±bulan 1, paylater ±bulan 2, kartu kredit ±bulan 5, KTA ±bulan 10.
> - Total utang Rp47 jt ÷ Rp5,42 jt ≈ 9 bulan + bunga → **sekitar 9–10 bulan**.
> - Perkiraan total bunga **±Rp2,5–3 juta** (KTA bunganya rendah, 0,9%).
>
> Tips: jangan pakai kartu kredit lagi, pertimbangkan konsolidasi/take over KTA ke bunga lebih rendah, tanyakan penalti pelunasan KTA. Ini bukan nasihat keuangan.

## B. DENGAN skill
Lihat lengkap di `02-karyawan-4-utang-avalanche-snowball.md`. Inti: konversi KTA flat → **1,628%/bln = 19,53%/th** (script), jadwal per bulan, **10 bulan, total bunga Rp4.226.895** (Avalanche = Snowball, urutan sama), per utang 60.000 / 120.875 / 730.469 / 3.315.551; cek batas OJK 0,1%/hari & BI 1,75%/bln; kontak OJK 157 & WA; peringatan gali lubang tutup lubang; asumsi & 5 langkah minggu ini; catatan nilai pelunasan dipercepat KTA.

## Penilaian berdampingan
| Kriteria | Tanpa skill | Dengan skill |
|---|---|---|
| Bunga KTA | **Salah kaprah:** memperlakukan flat 0,9%/bln seolah bunga dari sisa saldo ("rendah"). Bila dihitung dengan 0,9% efektif, total bunga jadi Rp2.665.788 — **kurang Rp1.561.107 (−37%)** dari yang benar | Dikonversi ke efektif 1,628%/bln (verifikasi penguji: 1,6275%) ✓ |
| Total bunga | "±Rp2,5–3 juta" (kisaran, di bawah nilai benar Rp4,23 jt) | Rp4.226.895 — sama persis dengan simulasi independen ✓ |
| Bulan lunas per utang | Perkiraan "±" (kebetulan benar 1/2/5/10) | Pasti, cocok simulasi ✓ |
| Total bulan | "9–10 bulan" | 10 bulan ✓ |
| Urutan & banding metode | Benar, tanpa angka selisih | Benar + selisih biaya (Rp0) + kemenangan pertama ✓ |
| Jadwal bulanan | Tidak ada | Ada (`--jadwal`), terverifikasi baris per baris ✓ |
| Keamanan/regulasi | Tidak cek batas OJK/BI, tidak ada kontak OJK; menyarankan "take over/konsolidasi" tanpa peringatan gali lubang | Alarm batas OJK/BI, cek legalitas 157/WA, larangan gali lubang, restrukturisasi resmi ✓ |
| Kejelasan untuk awam | Cukup, tapi angka "kira-kira" | Tabel + ringkasan 3 kalimat + langkah minggu ini ✓ |
| Disclaimer | Singkat | Lengkap + tanggal cek aturan ✓ |

## Kesimpulan
**Dengan skill jelas lebih baik.** Pembeda terbesar adalah angka: tanpa skill, bunga flat KTA — jebakan paling umum di Indonesia — membuat total bunga meleset ±37% dan membuat KTA tampak "murah". Dengan skill, semua angka tepat sampai rupiah dan ada pagar keamanan khas Indonesia (batas OJK/BI, kanal pengaduan). Bahan "sebelum/sesudah" README: sebelum = "bunga ±Rp2,5–3 juta, KTA murah"; sesudah = "KTA sebenarnya 19,53%/th, total bunga Rp4.226.895, lunas bulan ke-10".
