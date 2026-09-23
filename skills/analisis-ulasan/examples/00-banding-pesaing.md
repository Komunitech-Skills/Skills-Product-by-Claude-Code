# 00 — Uji banding pesaing (S1)

## Pencarian
- Kata kunci: "SKILL.md customer review analysis", "review analysis themes complaints claude skill", "analisis ulasan skill", "sentiment review skill", "Shopee review".
- Sumber dicek: github.com/anthropics/skills (tidak ada skill ulasan), github.com/manairalabs/bicara-skills (wa-reply-id, invoice-extract-id: tidak relevan), github.com/alvinindra/bahasa-skills (bahasa-inti/marketing/seo/website/peneliti: tidak relevan), github.com/VoltAgent/awesome-openclaw-skills (yang ada hanya ekstraktor API ulasan Amazon/Google Maps dan skor sentimen generik, tanpa analisis tema; ClawHub/clawskills.sh tidak dibuka langsung), skills.sh (hasil pencarian web), github.com/coreyhaines31/marketingskills (`customer-research`, riset umum).
- **Pesaing paling sebanding:** `review-objection-miner-ecommerce`, dari github.com/mardab96/ecommerce-claude-skills, file `review-objection-miner-ecommerce/SKILL.md`, **lisensi MIT**. Isinya instruksi saja, tanpa script.
- Script pihak ketiga tidak dijalankan. Isi pesaing tidak disalin ke skill kita.

## Output dengan instruksi pesaing (disimulasikan, input S1 yang sama)
Instruksi pesaing: konfirmasi tujuan dulu (PDP/iklan/FAQ/perbaikan produk), kelompokkan per tema (buying trigger, benefit, objection, confusion, quality, shipping/packaging, sizing/fit, usage), dan tiap temuan diberi tag bukti, severity, confidence, dampak bisnis, effort, keputusan. Outputnya: Review verdict, Theme table, Objection map, Angle ideas.

> **Review verdict:** Pembeli membeli kaos ini karena ukurannya pas dan sesuai foto. Yang menghambat adalah pengiriman lambat, salah kirim, dan kualitas sablon/jahitan. (confidence: medium)
>
> | Theme | Evidence | Customer language | Business implication | Recommended use |
> |---|---|---|---|---|
> | Shipping delay | review_cluster | "pengirimannya lama bgt", "5 hari baru dikirim" | conversion, retention | FAQ estimasi kirim; perbaiki operasional |
> | Wrong item | review_cluster | "salah kirim warna" | support_load | QC packing |
> | Quality | review_cluster | "sablon luntur sekali cuci" | retention | product improvement |
> | Sizing | review_cluster | "size L kayak M" | returns | size chart di PDP |
> | Fit praised | review_cluster | "ukurannya pas di badan" | conversion | proof block di PDP |
>
> | Finding | Evidence | Severity | Confidence | Business impact | Effort | Owner decision |
> |---|---|---|---|---|---|---|
> | Keterlambatan proses kirim paling sering dikeluhkan | review_cluster | high | medium | retention | S | do_now |
> | Salah kirim varian | review_cluster | high | medium | support_load | XS | do_now |
>
> **Objection map:** "Ukurannya pas nggak?" → tabel ukuran di foto ke-4; "Lama nggak dikirim?" → estimasi kirim di deskripsi.
> **Angle ideas:** "Size chart yang beneran akurat", "Persis kayak di foto", "Adem dipakai seharian".

(Pesaing tidak memberi jumlah atau persen per tema, tidak ada sebaran bintang, dan tidak ada aturan menyamarkan data pribadi selain "jangan publikasikan kutipan tanpa izin".)

## Output dengan skill kita
Lihat `01-toko-kaos-160-ulasan-csv.md`.

## Penilaian
| Kriteria | Pesaing (`review-objection-miner-ecommerce`) | Skill kita (`analisis-ulasan`) |
|---|---|---|
| Kualitas analisis | Baik secara kerangka (objection map, angle iklan, tag bukti/severity) | Baik: angka pasti per tema, prioritas × keparahan, ukuran keberhasilan |
| Akurasi angka | Tidak ada angka (hanya "review_cluster", confidence) | Sebaran & rata-rata terverifikasi 100%; tema diverifikasi. Ada bug regex yang harus dikoreksi agent |
| Konteks Indonesia | Bahasa Inggris, konteks DTC/Shopify. Tidak paham "brg/bgt/ga sesuai/mantul" | Kamus ±250 slang, marketplace Indonesia, UU PDP, istilah "Seller Center" |
| Privasi | Hanya "jangan publikasikan kutipan tanpa izin" | Kolom nama diabaikan; nomor, email, resi, @akun disamarkan otomatis (dengan celah kecil pada email) |
| Siap pakai untuk UMKM | Cocok untuk tim marketing; istilah (PDP, severity, effort XS) asing bagi awam | Tabel sederhana, tindakan "siapa melakukan apa", ide konten langsung pakai |
| Skala 150+ ulasan | Bergantung kemampuan model membaca semua ulasan | Script deterministik, bisa sampai ribuan |
| **Keseluruhan** | Kompetitif untuk angle marketing | **Skill kita menang** (akurasi & konteks Indonesia) |

## Yang bisa dipelajari dari pesaing (ide, bukan salinan)
1. **Tag keyakinan (confidence) per temuan.** Tema dengan kutipan sedikit atau hasil koreksi agent bisa diberi label "yakin/sedang/dugaan" agar pemilik tahu mana yang perlu dicek.
2. **Peta "pertanyaan calon pembeli → di mana dijawab"** (foto ke berapa, deskripsi, FAQ chat). Ini cocok sekali dengan skill `foto-produk-brief` dan `listing-marketplace` kita.
3. **Memisahkan ulasan milik sendiri dan ulasan pesaing** bila pengguna menempel keduanya, dan tidak pernah memakai kutipan pesaing sebagai testimoni.
4. **"Apa yang jangan dilakukan dulu"**: satu baris peringatan di akhir laporan (mis. "jangan ganti ekspedisi sebelum data waktu proses dicek").
