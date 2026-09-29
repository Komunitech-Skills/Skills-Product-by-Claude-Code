# Uji 04 — Input tidak lengkap: "bikinin KPI tim saya"

> Penguji independen, 2026-09-29. Simulasi agent (claude-code) mengikuti tabel Input SKILL.md.

## Permintaan pengguna
"bikinin KPI tim saya"

## Respons agent (satu pesan, bertanya sekali)
> Siap, saya buatkan. Supaya KPI-nya pas, jawab singkat saja ya:
> 1. **Siapa saja timnya?** Nama panggilan, divisi, dan tugasnya (mis. "Rini admin, Dodi sales, Tejo gudang").
> 2. Dinilai **bulanan atau mingguan**? (kalau tidak dijawab: bulanan, mulai Oktober 2026)
> 3. Sudah punya angka/target 3 bulan terakhir? (kalau belum: saya pakai target contoh yang **harus
>    disesuaikan**)
> 4. Data realisasinya biasanya dari mana: Excel/Google Sheets, rekap grup WA, atau kertas?
>    (default: lembar isian CSV/Excel yang saya buatkan)
> 5. Laporannya untuk siapa? (default: hanya Bapak/Ibu sebagai pemilik, bukan grup)
>
> Kalau mau cepat, cukup jawab nomor 1, sisanya saya pakai default di atas.

Hanya nomor 1 yang wajib (sesuai SKILL.md: "Wajib; tanpa ini tidak bisa"). Agent **tidak** mengarang
daftar karyawan.

## Balasan pengguna (lanjutan simulasi)
"Rini admin, Dodi sales, Tejo gudang, Sinta kasir, Pak Min cleaning service. Default aja."

## Tindakan agent
```
$ python3 scripts/skor_kpi.py template --tim tim.csv --periode 2026-10 --keluar KPI
Dibuat: KPI/rencana-kpi.csv, KPI/rencana-kpi.xlsx, KPI/realisasi-2026-10.csv
16 baris KPI.
Perlu diisi manual:
- Pak Min: peran 'cleaning service' tidak ada di katalog (...) -> isi KPI-nya manual.
$ python3 scripts/skor_kpi.py cek --rencana KPI/rencana-kpi.xlsx
✅ Rencana KPI valid: 16 KPI, 4 orang, 4 divisi.
```
XLSX dibuka openpyxl: 17 baris, 0 selisih dengan CSV.

Agent menyampaikan asumsi: bulanan mulai 2026-10, target katalog **hanya contoh** (perlu disesuaikan
dengan data 3 bulan terakhir), laporan hanya ke pemilik. Untuk Pak Min, agent mengusulkan 2–3 KPI
hasil kerja yang bisa dikendalikan (mis. "area bersih sesuai checklist harian %", arah naik) untuk
disetujui pemilik, bukan pengawasan gerak-gerik.

## Catatan penguji
- Peran di luar katalog ditangani jujur (dilewati + diminta isi manual), bukan ditebak.
- Risiko: `--periode 2026-10` mengunci rencana ke Oktober; bulan November akan gagal "Tidak ada rencana
  KPI untuk periode 2026-11" kecuali kolom periode dikosongkan. SKILL.md tidak mengingatkan (temuan S-3).

**Hasil: LULUS** (bertanya sekali, default jelas, tidak mengarang data).
