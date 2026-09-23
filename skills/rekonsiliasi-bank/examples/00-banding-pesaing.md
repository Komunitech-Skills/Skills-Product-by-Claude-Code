# 00 — Uji banding pesaing (rekonsiliasi-bank)

## Pencarian (2026-09-23)
- GitHub code search: `bank reconciliation filename:SKILL.md` (±5.968 hasil; 15 teratas ditinjau), `mutasi rekening filename:SKILL.md`, `rekonsiliasi filename:SKILL.md`.
- github.com/VoltAgent/awesome-openclaw-skills README (grep "reconcil/bank"): tidak ada skill rekonsiliasi bank-vs-invoice.
- manairalabs/bicara-skills: hanya `invoice-extract-id` (ekstraksi invoice, bukan rekonsiliasi). alvinindra/bahasa-skills: tidak ada skill keuangan terkait.
- anthropics/skills: tidak ada skill rekonsiliasi bank.
- Tidak ditemukan skill **berbahasa Indonesia** untuk rekonsiliasi mutasi bank.

Kandidat yang dibaca (raw.githubusercontent.com, tidak ada script pihak ketiga yang dijalankan):
| Skill | URL | Lisensi | Catatan |
|---|---|---|---|
| PythonMuse `bank-reconciliation` | https://github.com/PythonMuse/pythonmuse-workflow-kit/blob/HEAD/skills/bank-reconciliation/SKILL.md | tidak tercantum | Prompt instruksi murni (tanpa script), gaya kontrol internal/GL, **paling sebanding** → dipakai untuk banding |
| skills-il `israeli-bank-reconciliation` | https://github.com/skills-il/accounting | MIT (frontmatter) | Mengambil data dengan **login scraping kredensial bank Israel** — tidak relevan untuk Indonesia dan bertentangan dengan prinsip privasi kita |
| webrix-ai `bank-reconciliation` | https://github.com/webrix-ai/agent-skills | tidak tercantum | Butuh QuickBooks MCP; langkahnya hanya 4 poin generik |
| Alexi5000 ClawKeeper `bank-reconciliation` | https://github.com/Alexi5000/ClawKeeper | tidak tercantum | Bagian dari sistem ClawKeeper, generik |

## S1 dengan instruksi pesaing (PythonMuse)
Mengikuti langkahnya secara harfiah: langkah 1–2 meminta konfirmasi "Use Case UC-001 approved" dan data **masked**; nama pelanggan tak disamarkan termasuk *Prohibited Inputs* → agent **berhenti dan meminta versi yang disamarkan**. Setelah pengguna menyatakan data fiktif/sampel, output:

> **Reconciliation Summary**
> | Item | Amount |
> |---|---|
> | Bank statement ending balance | Rp 20.643.376,54 |
> | Less: outstanding checks | Rp 0 |
> | Plus: deposits in transit | Rp 450.000 (PEND Joko) |
> | Adjusted bank balance | Rp 21.093.376,54 |
> | GL ending balance | *(tidak tersedia — file yang diberikan daftar invoice, bukan buku besar)* |
> | Difference | tidak dapat dihitung |
>
> **Matched:** 7 item (exact amount + date ±3 hari kerja).
> **Unmatched — Bank side:** 12/09 350.000 setoran tunai (exception); 15/09 993.500 (exception); 20/09 1.000.000 (exception); 23/09 150.000; 24/09 300.000; 30/09 12.345,67 bunga (bank fee/charge).
> **Unmatched — GL side:** INV-103 1.200.000, INV-104 800.000, INV-105 5.000.000, INV-106, INV-107, INV-108, INV-111, INV-113 … (timing/exception).
> **Items Requiring Review / Assumptions / Reviewer Checklist** (Controller sign-off).

(Pesaing hanya punya aturan exact/toleransi tanggal dan "partial matches flagged for review" tanpa definisi → gabungan, termin, dan potong biaya tidak dikenali; tunai/batal tidak dibahas.)

## Penilaian
| Kriteria | Pesaing (PythonMuse) | Skill kita |
|---|---|---|
| Kualitas output | Format audit GL; butuh saldo buku besar yang tidak dimiliki UMKM | 4 kelompok + penjelasan selisih seimbang + tindakan |
| Kesesuaian konteks Indonesia | Rendah (USD, GL, sign-off controller; tak kenal CR/DB, PEND, `'02/09`) | Tinggi (BCA/Mandiri/BRI, format angka, QRIS, tagih-piutang) |
| Akurasi | Tergantung agent; tanpa script | Total & selisih akurat; ada cacat salah pasang (lihat 01/02) |
| Siap pakai | Rendah untuk awam (berhenti minta approval UC-001) | Tinggi |
| **Skor** | 4/10 | 7/10 (sebelum perbaikan salah pasang) |

**Skill kita menang** secara keseluruhan.

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
- Membedakan **timing difference** (akan beres periode depan, mis. PEND/transfer akhir bulan) vs **exception** sejati — label ini berguna untuk pengguna awam ("tunggu" vs "selidiki").
- Aturan gaya "tandai item yang muncul di kedua daftar tak-cocok dengan nominal mirip" — persis celah yang membuat salah pasang Dewi/Hendra tidak terlihat; laporan kita bisa menambah bagian "kemungkinan pasangan yang terlewat".
- Opsi rekonsiliasi berbasis saldo (saldo bank vs saldo buku) untuk pengguna yang sudah punya pembukuan.
