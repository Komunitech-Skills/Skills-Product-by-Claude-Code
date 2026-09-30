# Changelog

## 1.0.3 (2026-09-30)
- Script: angka Rupiah (`--kurs`, `--anggaran`, harga paket IDR bila ditulis teks) kini dibaca format Indonesia: `16.500`, `Rp16.500`, `1.250.000`, `16.500,25`, `500rb`, `1,5jt`. Sebelumnya `--kurs 16.500` diam-diam terbaca 16,5 (biaya Rp479, seharusnya Rp478.500).
- Bentuk ragu (`16.5`, `1,5`, `16,500` pada Rupiah; `1.500` pada menit/jumlah video) ditolak dengan pesan jelas, tidak ditebak. Uji regresi bertambah (19 tes).

## 1.0.1 (2026-09-29)
- Perbaikan hasil uji independen: contoh 01 memakai paket nyata saja; rekomendasi tidak melebihi anggaran dan tidak memilih paket "kurang".
- Script: opsi `--anggaran`, status `lewat-anggaran`, "termurah yang mencukupi" hanya untuk paket cukup dan masuk anggaran, peringatan bila tidak ada yang muat; angka raksasa (mis. 1e999) kini GALAT rapi. Uji regresi bertambah (13 tes).
- Fakta harga dicek ulang di halaman resmi (2026-09-29): ElevenLabs klon instan mulai Starter, klon profesional mulai Creator; Synthesia: jumlah avatar pribadi per paket tidak konsisten antar-pengecekan → ditandai wajib cek ulang; HeyGen diperbarui.
- Formulir persetujuan: bagian UU PDP No. 27/2022 (data biometrik, persetujuan, penarikan, retensi/penghapusan, pemrosesan pihak ketiga).
- Label contoh-paket sebagai ilustrasi; catatan iklan kesehatan/kosmetik; README menautkan pembanding A/B.

## 1.0.0 (2026-09-29)
- Rilis awal.
