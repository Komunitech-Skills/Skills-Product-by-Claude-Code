# Uji banding pesaing - skenario normal 1 (toko hijab)
Penguji independen, 2026-09-29. Skill pesaing hanya dibaca untuk dinilai, tidak disalin.

## Pencarian
- GitHub: `phuryn/pm-skills` (MIT, commit terakhir 2026-09-14) - `pm-market-research/skills/sentiment-analysis`,
  `pm-product-discovery/skills/analyze-feature-requests`; `product-on-purpose/pm-skills` (Apache-2.0, 2026-09-10) - `skills/measure-survey-analysis`,
  `discover-interview-synthesis`.
- Web: "skills.sh customer feedback synthesis skill", ClawHub/clawskills.sh `customer-feedback` (jk-0001), mcpmarket "insight-synthesis-framework",
  artikel Enterpret "feedback-synthesizer". Yang terakhir-terakhir ini minim bukti pemakaian/berbasis vendor; dipilih pesaing bersumber terkuat.
- **Pesaing terpilih: `phuryn/pm-skills` sentiment-analysis** (repo PM paling populer, pembuat kredibel). Catatan: ini juga salah satu sumber ATM
  skill kita, jadi banding ini sekaligus menguji "nilai tambah BESAR". `measure-survey-analysis` dibaca sebagai pembanding kedua.

## Hasil pesaing pada skenario 1 (dijalankan penguji mengikuti instruksinya)
Keluaran mengikuti struktur skill: minimal 3 segmen (mis. "Pembeli pertama marketplace", "Pelanggan loyal WA", "Calon pembeli IG"), profil segmen,
Jobs-to-be-Done ("tampil rapi & nyaman untuk kegiatan harian"), skor sentimen -1..+1 per segmen (mis. -0,2 / +0,1 / 0), tema positif/negatif
dengan kutipan, "product-segment fit", 2-3 rekomendasi per segmen. Bahasa Inggris, tidak ada perhitungan, tidak ada penyamaran data.

## Penilaian berdampingan (1-5)
| Kriteria | Pesaing (sentiment-analysis) | Skill kita |
|---|---|---|
| Relevan untuk UMKM awam Indonesia | 2 (segmen/JTBD/NPS terlalu PM-korporat, 34 masukan dipaksa jadi 3 segmen) | 5 |
| Angka dapat diulang | 1 (skor sentimen ditaksir) | 4 (script; aritmetika terverifikasi, klasifikasi perlu koreksi) |
| Privasi data pelanggan | 1 (tidak dibahas) | 4 |
| Multi-kanal (WA export, CSV marketplace, tempelan) | 2 (umum) | 4 (tetapi CSV marketplace gagal di uji 06) |
| Tindakan siap pakai (backlog, pemilik, tenggat, ukuran) | 2 | 5 |
| Menutup lingkaran ke pelanggan & siklus bulanan | 1 | 5 |
| Kejujuran batas data | 3 (ada "flag small sample") | 4 |
| Ketahanan klasifikasi slang Indonesia | 3 (LLM membaca langsung, tidak salah baca "pas"/"kurang") | 2 (kata kunci; lihat 06-08) |

Kelebihan pesaing yang perlu dipelajari (ditulis ulang dengan cara sendiri, bukan disalin): membaca langsung oleh model lebih tahan sarkasme/
slang daripada kata kunci; `measure-survey-analysis` punya label kepercayaan dan bagian "apa yang tidak boleh disimpulkan" yang eksplisit per temuan.

**Kesimpulan: skill kita MENANG** untuk audiens target (total 33 vs 15). Kelemahan kita ada di akurasi tema script, bukan di alur.
