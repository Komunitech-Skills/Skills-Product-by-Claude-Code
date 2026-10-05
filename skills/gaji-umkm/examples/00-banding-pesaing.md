# 00 — Uji banding pesaing (skenario 01)

> Penguji independen Akun B, 26-09-2026. Skill/produk pesaing hanya **dibaca untuk dinilai**, tidak disalin.

## Pencarian
- skills.sh API: `payroll`, `pph21`, `bpjs`, `gaji`, `slip gaji`, `indonesia payroll`; ClawHub API: `payroll indonesia`, `gaji`, `payroll` (ClawHub: 0 hasil).
- Web: "SKILL.md payroll Indonesia PPh 21 BPJS", "Gadjian Talenta Mekari fitur payroll … 2026".
- Ditemukan: `openaccountants/openaccountants` → `id-payroll-pph21` (repo 407★, lisensi AGPL-3.0 kode / OA Guide License konten, 1 instal, pertama terlihat 16 Agu 2026, status "source-cited draft, validated by: pending"); `adamriofc/indonesian-business-agent-skills` (`bpjs-calculator`, `pph21-grossup`, 2 instal — tidak dinilai, tanpa sinyal pemakaian); `anthropics/knowledge-work-plugins/payroll-prep` (1.599 instal, generik/AS, bukan aturan Indonesia). SaaS: Gadjian (mulai ± Rp 12.500/karyawan/bulan), Mekari Talenta (± Rp 30–50 rb/karyawan/bulan).

## Skill pesaing `id-payroll-pph21` pada data skenario 01 (aturan tertulisnya diterapkan penguji)
| Kode | Bruto pesaing | PPh 21 pesaing | JP karyawan pesaing | PPh 21 benar (gaji-umkm = penguji) | JP benar |
|---|---:|---:|---:|---:|---:|
| K03 Citra | 13.000.000 | 520.000 | 105.474 | 543.568 | 110.863 |
| K05 Eka | 15.000.000 | 900.000 | 105.474 | 1.092.420 | 110.863 |
| K08 Hadi | 22.000.000 | 1.980.000 | 105.474 | 2.039.832 | 110.863 |
| K04 Dedi | 9.500.000 | 142.500 | 95.000 | 149.397 | 95.000 |
| K01 Andi | 7.650.000 | 76.500 | 67.500 | 79.767 | 67.500 |

Kelemahan pesaing (dari teksnya): batas JP Rp 10.547.400 (usang untuk 2026); bruto TER tanpa premi JKK/JKM/Kes perusahaan (kurang potong); dasar BPJS Kes tanpa batas bawah UMK; Desember hanya mengurangkan iuran JP (JHT karyawan terlewat); menyarankan "pro-rate PTKP" untuk karyawan baru (bertentangan dengan contoh Tuan B PMK 168/2023); masih menyebut tambahan 20% tanpa NPWP & DJP Online e-Bupot; tanpa script, tanpa penyimpanan, tanpa Lina (Masa Pajak Terakhir) — referensi berbahasa Inggris untuk agent, bukan alat operasional. Lisensi AGPL/OA → tidak boleh dijadikan bahan.

## SaaS (Gadjian / Talenta) vs gaji-umkm
| Aspek | SaaS | gaji-umkm |
|---|---|---|
| Biaya 12 karyawan | ± Rp 150 rb–600 rb/bulan (Rp 1,8–7,2 jt/tahun) | sekali beli (usulan Rp 199.000) |
| Data | server vendor | file lokal pemilik |
| PPh 21 TER, BPJS, THR, Desember | ya | ya (terverifikasi 13 karyawan) |
| Portal slip mandiri karyawan, aplikasi absen HP, cuti | ya | tidak (slip file per karyawan; absensi lewat skill `absensi-lokal`) |
| Ekspor e-Bupot/Coretax & laporan format BPJS (SIPP) | ya (Talenta: bukti potong A1, laporan BPJS) | **tidak** — hanya angka bahan BPA1; input manual ke Coretax |
| Transfer bank terintegrasi | sebagian (payroll bank) | CSV untuk diunggah manual |
| Dioperasikan lewat chat bahasa sehari-hari | tidak | ya |

## Kesimpulan
Di antara **agent skill**, gaji-umkm menang telak (pesaing salah di 4 dari 5 karyawan yang dibandingkan dan tidak punya alur bulanan). Terhadap SaaS, gaji-umkm menang di biaya & kepemilikan data, kalah di ekspor Coretax/BPJS, portal karyawan, dan integrasi bank — sebutkan dengan jujur di materi jualan (sudah: "Tidak terhubung ke bank, BPJS, atau Coretax").

Sumber: https://skills.sh/openaccountants/openaccountants/id-payroll-pph21 ; https://github.com/openaccountants/openaccountants (agent-skills/id-payroll-pph21/SKILL.md, commit 25-09-2026) ; https://albatech.id/blog/gadjian-vs-gajihub-vs-talenta-hris-umkm-indonesia-2026 ; https://www.total-erp.com/blog/software-payroll-terbaik/ ; https://www.talenta.co/en/features/payroll-software/payroll-app-calculator/
