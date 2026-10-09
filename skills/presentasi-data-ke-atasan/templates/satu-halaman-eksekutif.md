# Template: Satu Halaman Eksekutif

Struktur piramida — kesimpulan di paling atas, detail di bawah. Cocok ditempel ke
dokumen/slide tunggal atau dikirim sebagai PDF satu halaman.

```
<Judul: topik singkat, mis. "Kinerja Penjualan September 2026">

KESIMPULAN
<1 kalimat inti, dicetak tebal/besar. Contoh:>
Omzet turun 23% di bulan puasa, tapi margin masih aman berkat efisiensi biaya
lain — perlu keputusan soal biaya iklan yang naik tidak sebanding omzet.

ANGKA KUNCI
┌─────────────────────┬─────────────────────┬─────────────────────┐
│ Omzet                │ Biaya Iklan          │ Rasio Biaya/Omzet    │
│ Rp24,5 juta (-23%)   │ Rp5,6 juta (+40%)    │ 23% (naik dari 12%)  │
└─────────────────────┴─────────────────────┴─────────────────────┘

GRAFIK
<Sebutkan jenis grafik yang dipakai sesuai references/pilih-grafik.md, mis.
"Grafik garis: Omzet & Biaya Iklan per Bulan (Jun–Sep 2026)" — grafik dibuat lewat
tool visualisasi yang tersedia, bukan script skill ini>

RISIKO
<1-2 poin dengan angka, mis.>
- Bila rasio biaya iklan/omzet terus naik, margin bersih bisa turun di bawah
  ambang aman (biasanya dibicarakan bersama pemilik/akuntan) dalam 2 bulan.

REKOMENDASI
1. <Aksi> — PIC: <nama>, tenggat: <tanggal>
2. <Aksi> — PIC: <nama>, tenggat: <tanggal>

────────────────────────────────────────────────────────────────
Sumber data: <nama file/sistem>. Periode: <tanggal>. Dibuat: <tanggal dibuat>.
```

## Catatan pemakaian
- "Angka kunci" selalu 3 kartu, bukan lebih — kalau ada lebih dari 3 angka penting,
  pilih 3 yang paling mendukung kalimat kesimpulan, sisanya boleh dilampirkan terpisah
  bila diminta.
- Baris sumber data & periode di bagian bawah **wajib ada** — transparansi asal angka.
- Bila dibuat sebagai artifact/HTML/slide (mis. digabung dengan `presentasi-instan`),
  struktur di atas tetap dipakai sebagai kerangka isi, hanya tampilannya yang lebih
  visual.
