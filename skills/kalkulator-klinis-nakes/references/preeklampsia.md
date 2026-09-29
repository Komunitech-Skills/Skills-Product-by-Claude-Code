# Skrining faktor risiko preeklampsia — rincian & kode

## Aturan (Buku KIA 2023, lembar skrining usia kehamilan < 20 minggu)
- **≥ 1 faktor risiko tinggi** (kolom merah) → risiko tinggi.
- **≥ 2 faktor risiko sedang** (kolom kuning) → risiko sedang yang memenuhi kriteria
  rujukan/konsultasi dokter.
- 1 faktor sedang saja → belum memenuhi kriteria; lanjutkan ANC rutin & ukur TD tiap kunjungan.

Kalimat tindak lanjut di alat ini selalu berbentuk "pertimbangkan ... sesuai PNPK/pedoman —
keputusan klinis dokter". **Tidak ada dosis obat.**

## Kode faktor
| Kode | Faktor | Buku KIA 2023 | NICE NG133 |
|---|---|---|---|
| pasangan-baru | Multipara, kehamilan oleh pasangan baru | sedang | — |
| reproduksi-berbantu | Bayi tabung / obat induksi ovulasi | sedang | — |
| usia-ibu-35 | Usia ibu ≥ 35 tahun | sedang | — |
| usia-ibu-40 | Usia ibu ≥ 40 tahun (otomatis mencakup ≥ 35) | (tercakup ≥ 35) | sedang |
| nullipara | Kehamilan pertama | sedang | sedang |
| jarak-10-tahun | Jarak kehamilan sebelumnya > 10 tahun | sedang | sedang |
| riwayat-keluarga | Preeklampsia pada ibu/saudara perempuan | sedang | sedang |
| obesitas | IMT pra-hamil > 30 | sedang | — |
| imt-35 | IMT ≥ 35 saat kunjungan pertama (otomatis mencakup > 30) | (tercakup > 30) | sedang |
| map-90 | MAP > 90 mmHg | sedang | — |
| riwayat-preeklampsia | Preeklampsia/hipertensi pada kehamilan sebelumnya | tinggi | tinggi |
| kehamilan-multipel | Kembar | **tinggi** | **sedang** |
| diabetes | Diabetes dalam kehamilan / DM tipe 1-2 | tinggi | tinggi |
| hipertensi-kronik | Hipertensi kronik | tinggi | tinggi |
| penyakit-ginjal | Penyakit ginjal | tinggi | tinggi |
| autoimun | Autoimun / SLE | tinggi | tinggi |
| antifosfolipid | Sindrom antifosfolipid | tinggi | tinggi |
| proteinuria | Dipstik > +1 dua kali berjarak 6 jam / 300 mg/24 jam | tinggi | — |

Angka yang diberikan (`--sistolik/--diastolik`, `--usia-ibu`, `--imt`) otomatis mengisi faktor
yang sesuai dan dilaporkan di baris "Faktor terisi otomatis dari angka".

## Rumus & ambang MAP
MAP = (sistolik + 2 × diastolik) / 3. Dibandingkan **tanpa pembulatan**: 110/80 → tepat 90,0 →
bukan > 90; 111/80 → 90,33 → > 90. Tampilan dibulatkan 1 desimal (setengah ke atas).

## Pemetaan bahasa sehari-hari (contoh)
- "anak pertama", "G1P0" → nullipara
- "suami baru", "anak pertama dari suami kedua" → pasangan-baru
- "program bayi tabung", "hamil dari obat penyubur" → reproduksi-berbantu
- "dulu hamil darah tinggi / kejang" → riwayat-preeklampsia (tulis asumsinya)
- "kakak/ibunya dulu keracunan kehamilan" → riwayat-keluarga
- "gula darah tinggi waktu hamil", "DM" → diabetes
- "lupus" → autoimun; "APS" → antifosfolipid

## Tanda bahaya (bukan bagian skrining)
Bila disebut TD ≥ 160/110, kejang, nyeri kepala hebat, pandangan kabur, nyeri ulu hati, sesak,
atau perdarahan → jangan lanjutkan skrining rutin; tulis: "Tangani/rujuk segera sesuai protokol
kegawatdaruratan fasilitas Anda."
