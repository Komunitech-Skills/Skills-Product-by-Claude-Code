# Uji Banding Pesaing — Skenario 02 (4 utang, Avalanche vs Snowball)

> Penguji independen, 2026-09-26. Skill pesaing hanya **dibaca untuk dinilai** (script pesaing tidak dijalankan, tidak disalin).

## Pencarian pesaing
- Kata kunci: `"debt payoff" agent skill SKILL.md avalanche snowball github clawhub OR skills.sh`, `personal finance skill`, `debt payoff`.
- Hasil relevan (format Agent Skills):
  1. **openaccountant/skills** — `personal/debt-payoff` (57 baris) & `personal/zero-based-budget` (81 baris), MIT, commit `f5abe381` (9 Apr 2026). Sumber ATM skill ini. https://github.com/openaccountant/skills
  2. **joellewis/finance_skills** — `plugins/wealth-management/skills/debt-management` (145 baris + `scripts/debt_management.py` butuh numpy), MIT, commit `5c498eac` (18 Jul 2026); tercantum di skills.sh: https://www.skills.sh/joellewis/finance_skills/debt-management (halaman skills.sh diblokir proxy; isi dibaca dari GitHub https://github.com/joellewis/finance_skills).
- Non-skill (aplikasi/CLI, bukan pesaing langsung): iLanis-agent/debtdown, erikolvera/DebtPilot, vyle1208/debt-payoff-strategist.
- Tidak ditemukan skill pesaing berbahasa Indonesia / berkonteks OJK-BI.
- Audit singkat: grep pola mencurigakan di folder openaccountant → nihil; script joellewis tidak dijalankan.

## Cara uji
Agent mengikuti instruksi masing-masing skill secara harfiah untuk input skenario 02. Kedua pesaing tidak punya script tanpa-dependensi yang bisa langsung dipakai (openaccountant: alat "Wilson" proprietary / spreadsheet; joellewis: script butuh `numpy`, tidak dijalankan sesuai aturan uji), jadi agent membuat simulasi bulanan sesuai rumus pesaing: bunga bulanan = saldo × APR/12. Angka hasil dihitung penguji dengan simulasi independen memakai interpretasi yang diarahkan pesaing:
- KTA "flat 0,9%/bln" → tidak ada panduan flat → dipakai sebagai APR 10,8% (bunga dari sisa saldo).
- Pinjol 0,1%/hari → APR 36,5% (×365) ÷ 12 = 3,042%/bln.

## Hasil berdampingan
| Aspek | openaccountant `debt-payoff` | joellewis `debt-management` | **atur-keuangan-pribadi (kita)** |
|---|---|---|---|
| Urutan Avalanche/Snowball | Pinjol → Paylater → KK → KTA (benar) | sama (benar) | sama (benar) |
| Bulan lunas | 1/2/5/10, total 10 | 1/2/5/10, total 10 | 1/2/5/10, total 10 ✓ |
| Total bunga | **Rp2.666.730** (KTA dianggap 10,8% efektif) | **Rp2.666.730** (sama) | **Rp4.226.895** ✓ (cocok simulasi independen) |
| Selisih dari angka benar | −Rp1.560.165 (−37%) | −Rp1.560.165 (−37%) | Rp0 |
| Bunga flat → efektif | Tidak ada | Tidak ada | Ada (`konversi-flat`, cocok rumus RATE) |
| Bunga harian/bulanan/tahunan | Hanya APR | Hanya APR | %/th, %/bln, %/hari |
| Cek cicilan ≤ bunga | Tidak | Tidak eksplisit | Ada (peringatan + "tidak akan lunas") |
| Regulasi | AS (APR, DTI 36% gross, FHA) | AS (DTI, refinance, tax-deductible) | BI 1,75%/bln, OJK 0,1%/hari 2026, 157/WA, gali lubang tutup lubang |
| Mata uang & konteks | Dolar, unbury.me, NerdWallet, "$1,000 starter emergency fund" | Dolar, student loan, mortgage | Rupiah, paylater, pinjol, KTA, kiriman ortu, THR |
| Rekomendasi investasi | Tidak | **Ya, secara tersirat**: "investing likely wins (7–10% equity returns)" — bertentangan dengan kebijakan Komunitech | Tidak ada; imbal hanya asumsi pengguna |
| Kelebihan pesaing | Ringkas; format jadwal jelas | Konsep refinance/konsolidasi & DTI lengkap; contoh angka terverifikasi dengan `--verify` | — |
| Bahasa | Inggris | Inggris | Indonesia, awam |

## Kesimpulan
**Skill kita unggul jelas.** Kedua pesaing menghasilkan urutan dan bulan lunas yang sama, tetapi total bunga meleset 37% karena tidak menangani bunga flat — jebakan utama KTA/leasing di Indonesia — dan tidak punya pagar OJK/BI. 

Pelajaran dari pesaing (untuk ditulis ulang dengan cara kita, bukan disalin):
1. joellewis punya bagian **refinance/konsolidasi** (breakeven biaya, jebakan tenor lebih panjang). Skill kita belum punya pembanding "take over KTA/konsolidasi" — kasus yang sering ditawarkan bank di Indonesia (lihat temuan T-6 di HASIL-UJI.md).
2. joellewis memverifikasi contoh di SKILL.md dengan `--verify`; kita sudah punya `tests/uji_regresi.py` (setara).
