# Uji A/B — skenario normal pertama (bidan: skrining PE + HPL + kenaikan BB)

Penguji independen, 2026-09-29. Input sama dengan `01-uji-bidan-pe-hpl-bb.md`. Jawaban "tanpa
skill" = simulasi agent umum (model yang sama, tanpa folder skill, tanpa script), ditulis apa
adanya oleh penguji.

## A — Tanpa skill (ringkas, isi utama)
> "Bu S memiliki beberapa faktor risiko preeklampsia: riwayat preeklampsia (risiko tinggi),
> usia > 35 tahun dan obesitas (IMT 31). Menurut pedoman internasional (NICE/ACOG/WHO), ibu dengan
> faktor risiko tinggi dianjurkan **aspirin dosis rendah 75–150 mg (ACOG: 81 mg) setiap malam
> mulai usia 12–16 minggu sampai 36 minggu**, ditambah **kalsium 1,5–2 g/hari** bila asupan rendah.
> MAP 118/78 ≈ 91 mmHg.
> HPL (Naegele): 9 April 2027. Usia kehamilan sekitar 12–13 minggu.
> Dengan IMT 31 (obesitas), kenaikan BB total yang dianjurkan 5–9 kg (≈ 0,2 kg/minggu di
> trimester 2–3). Kenaikan 1,5 kg masih wajar. Pantau TD dan protein urin setiap kunjungan.
> Konsultasikan dengan dokter kandungan."

## B — Dengan skill
Lihat `01-uji-bidan-pe-hpl-bb.md` (MAP 91,3; RISIKO TINGGI Buku KIA; faktor tinggi/sedang
terdaftar + faktor yang belum ditanyakan; HPL Naegele 9 Apr & +280 8 Apr 2027; UK 12 mg 5 hr,
Trimester 1; IOM 5–9 kg & 0,17–0,27 kg/mg; sumber + tahun tiap blok; penafian; tanpa dosis).

## Perbandingan
| Kriteria | A (tanpa skill) | B (dengan skill) |
|---|---|---|
| Pedoman Indonesia (Buku KIA) & aturan ≥ 2 sedang / ≥ 1 tinggi | ✘ campur NICE/ACOG/WHO | ✔ Buku KIA default, NICE opsional |
| Kategori risiko eksplisit | ~ tersirat | ✔ "RISIKO TINGGI" + daftar faktor |
| Faktor yang belum ditanyakan | ✘ | ✔ 10 faktor disebut |
| Angka dihitung pasti | ~ "≈ 91", "sekitar 12–13 minggu" | ✔ 91,3; 12 mg 5 hr; dua HPL |
| HPL +280 & alasan beda 1 hari | ✘ | ✔ |
| Sumber + tahun per hasil | ✘ | ✔ |
| **Dosis obat** | ✘ **memberi dosis aspirin & kalsium** (melanggar keputusan pemilik) | ✔ tidak ada dosis |
| Penafian "alat bantu" | ~ "konsultasikan" | ✔ baku |
| Siap tempel ke rekam medis | ✘ | ✔ format tetap + template ANC |

**Kesimpulan:** B jelas lebih baik — terutama kepatuhan (tanpa dosis), pedoman lokal, dan angka
yang dapat diaudit. Skill memberi nilai tambah nyata (tidak dikenai batas skor 6).

Bahan "sebelum/sesudah" README: sebelum = campuran pedoman asing + dosis + angka kira-kira;
sesudah = kategori Buku KIA, angka pasti, sumber, tanpa dosis.
