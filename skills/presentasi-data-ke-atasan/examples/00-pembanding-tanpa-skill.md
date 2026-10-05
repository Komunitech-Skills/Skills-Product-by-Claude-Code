# Uji A/B — Tanpa Skill vs Dengan Skill

Skenario dipakai: Normal #1 (Uji 03) — manajer cabang lapor omzet 3 bulan ke pemilik.

## Input pengguna
> "Tolong buatkan ringkasan buat pemilik. Omzet cabang saya Juli Rp45.000.000, Agustus
> Rp48.000.000, September Rp52.000.000. Ini laporan bulanan rutin ke owner."

## A. TANPA skill (respons agen generik, tanpa akses ke skill ini)
Simulasi respons agent umum yang hanya diberi prompt di atas, tanpa SKILL.md ini:

```
Berikut ringkasan omzet cabang:

Omzet cabang pada bulan Juli, Agustus, dan September 2026 masing-masing tercatat
sebesar Rp45.000.000, Rp48.000.000, dan Rp52.000.000. Terlihat adanya tren
peningkatan omzet dari bulan ke bulan selama periode tersebut. Peningkatan ini
menunjukkan kinerja yang cukup baik. Diharapkan tren positif ini dapat terus
berlanjut di bulan-bulan berikutnya.

Demikian laporan ini disampaikan, mohon menjadi perhatian.
```

Masalah versi ini:
- Kesimpulan ("kinerja cukup baik") **muncul di akhir**, bukan di kalimat pertama —
  pemilik yang sibuk harus membaca semua paragraf dulu.
- **Tidak ada angka persen perubahan** — "peningkatan" tidak dikuantifikasi (15,6%
  dari Juli ke September, dihitung Decimal, tidak muncul sama sekali).
- Kata "cukup baik" tanpa angka — persis jargon yang dilarang di
  `references/gaya-komunikasi.md` ("signifikan/cukup besar/lumayan tanpa satuan").
- **Tidak ada rekomendasi konkret** (aksi + PIC + tenggat) — hanya harapan umum
  ("diharapkan tren ini berlanjut").
- **Hanya satu format** — tidak ada versi WA singkat, skrip bicara, atau 1 halaman
  eksekutif; pengguna harus menulis ulang sendiri untuk tiap kanal.
- Tidak ada rata-rata/angka pendukung terpilih; angka hanya diulang, bukan diringkas
  jadi 3 angka kunci yang mendukung kesimpulan.

## B. DENGAN skill `presentasi-data-ke-atasan`
Lihat `examples/03-omzet-3-bulan-manajer-cabang-uji-akun-b.md` untuk proses lengkap.
Ringkasan WA yang dihasilkan:

```
📊 *Omzet Cabang Jul–Sep 2026*
Omzet naik konsisten 3 bulan berturut-turut, dari Rp45 juta jadi
Rp52 juta (+15,6%).
• Omzet Juli: Rp45.000.000
• Omzet September: Rp52.000.000 (+15,6% dari Juli)
• Rata-rata 3 bulan: Rp48.333.333
👉 Pertahankan alokasi stok & jadwal promo yang sama untuk Oktober.
```
Plus versi email formal, 1 halaman eksekutif, dan skrip bicara — semua angka identik,
dihitung lewat `scripts/hitung_perubahan.py` dan diverifikasi manual (lihat Uji 03).

## Kesimpulan uji A/B
Versi **dengan skill** unggul telak pada: kesimpulan di depan (piramida terbalik),
angka persen yang dihitung presisi (bukan kata "cukup baik"), rekomendasi konkret
(aksi + PIC + tenggat), format Rupiah/persen konsisten, dan 4 format siap pakai
sekaligus dari satu input yang sama. Versi tanpa skill setara draf mentah yang masih
perlu ditulis ulang manusia sebelum layak dikirim. **Skill memberi nilai tambah jelas**
— tidak memenuhi kondisi "skor maks. 6" pada Tahap 6 poin 4.
