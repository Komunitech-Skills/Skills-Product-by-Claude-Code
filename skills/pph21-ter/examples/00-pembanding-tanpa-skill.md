# 00 — Uji A/B: S1 dengan skill vs tanpa skill

**Permintaan (sama untuk keduanya):**
> Karyawan saya statusnya K/1, gaji 12 juta sebulan. THR 12 juta dibayar bulan Maret. Iuran JHT+JP yang dipotong dari gajinya 360 ribu per bulan. PPh 21 setahun 2026 berapa aja per bulannya?

Catatan jujur tentang metode: jawaban "tanpa skill" disimulasikan oleh penguji (Claude Code) yang menjawab seperti AI agent biasa, tanpa membuka SKILL.md, tabel, atau script. Penguji sudah membaca PDF PP 58/2023 sebelumnya, jadi simulasi ini kemungkinan **lebih baik** daripada jawaban agent biasa di dunia nyata. Tetap saja, kelemahannya terlihat jelas.

## Berdampingan

| Aspek | Tanpa skill (AI agent biasa) | Dengan skill `pph21-ter` |
|---|---|---|
| Jawaban inti | "K/1 masuk TER kategori B. Untuk gaji Rp 12 juta tarifnya **sekitar 3%** → ±Rp 360.000/bulan. Bulan Maret bruto Rp 24 juta, tarif TER **kira-kira 9%** → ±Rp 2.160.000. Desember dihitung ulang: bruto setahun Rp 156 jt − biaya jabatan Rp 6 jt − iuran Rp 4,32 jt = neto Rp 145,68 jt; PKP = 145,68 − 63 = Rp 82,68 jt; pajak = 3 jt + 15% × 22,68 jt = Rp 6,402 jt; Desember ≈ Rp 642.000. **Mohon cek ulang tarif TER ke tabel resmi PP 58/2023.**" | Tabel Januari–Desember lengkap dari tabel resmi (127 baris) + hitung ulang Desember per lapisan: Jan–Feb & Apr–Nov **Rp 360.000**, Maret **Rp 2.160.000**, Desember **Rp 642.000**, setahun **Rp 6.402.000** (lihat `01-setahun-dengan-thr.md`). |
| Sumber tarif | Dari ingatan, ditandai "sekitar/kira-kira"; baris tabel tidak disebut | Baris tabel persis ("di atas Rp 11.600.000 s.d. Rp 12.600.000 → 3%") dari salinan tabel resmi yang diuji |
| Premi JKK/JKM/BPJS Kes perusahaan masuk bruto | Tidak disinggung | Ada di checklist & asumsi |
| Pembulatan (PKP ke ribuan, PPh ke bawah) | Tidak disebut | Disebut, dengan catatan Coretax |
| DTP PMK 105/2025 | Tidak disinggung | Dicek (gaji > Rp 10 jt → tidak berlaku) |
| Kelebihan potong/pengembalian | Tidak dibahas | Otomatis bila Desember negatif, termasuk tenggat pengembalian |
| Konsistensi antar-sesi | Tergantung ingatan model; tabel B/C sering tertukar/keliru (lihat banding pesaing: skill publik dengan tabel B/C salah) | Deterministik: script + 34 uji otomatis + ribuan kasus acak cocok dengan kalkulator independen |
| Siap tempel | Paragraf, bukan tabel bulanan | Tabel bulanan + ringkasan + disclaimer |

## Penilaian singkat
- Pada kasus sederhana ini angka akhirnya bisa sama, tetapi jawaban tanpa skill **tidak bisa diandalkan tanpa cek manual** (tarif "sekitar", tanpa baris tabel, tanpa pengembalian lebih potong, tanpa DTP, tanpa pembulatan). Untuk pengguna awam, itu berarti tetap harus membuka tabel sendiri.
- Skill jelas lebih baik: angka pasti dan dapat diaudit, tabel bulanan siap tempel, aturan lebih potong/DTP/berhenti kerja ditangani otomatis, dan hasil selalu konsisten.
- **Kesimpulan: dengan skill jelas lebih baik → tidak ada cacat "tanpa nilai tambah".**
