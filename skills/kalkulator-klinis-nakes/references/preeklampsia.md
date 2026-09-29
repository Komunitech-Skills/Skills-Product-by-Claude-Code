# Skrining faktor risiko preeklampsia — rincian & kode

Acuan Indonesia: **Buku KIA edisi terbaru** — unduhan resmi Kemenkes
(https://ayosehat.kemkes.go.id/buku-kia-kesehatan-ibu-dan-anak), kolofon "Direktorat Jenderal
Kesehatan Primer dan Komunitas 2025", ISBN 978-623-301-149-5 (ISBN sama dengan edisi 2023),
lembar skrining preeklampsia < 20 minggu (hlm. cetak 102–103). Dibaca penguji independen
2026-09-29. Cetakan lain yang beredar bisa berbeda (mis. salinan sekunder menulis "MAP > 90") —
**cocokkan dengan buku yang dipakai fasilitas Anda** (PERLU REVIEW).

## Urutan pemeriksaan di script
1. **Lapisan tanda bahaya** (lihat bawah) — bila ada, hasil = SEGERA/HARI INI evaluasi/rujuk.
2. Klasifikasi faktor risiko menurut **satu** pedoman terpilih (default Buku KIA). Faktor yang
   tidak ada di pedoman terpilih tidak dihitung dan disebut di catatan beserta kategorinya di
   pedoman lain — **tidak dicampur diam-diam**.

## Aturan per pedoman
**Buku KIA (cetakan 2025):**
- **≥ 2 faktor risiko sedang dan/atau ≥ 1 faktor risiko tinggi** → ibu berisiko preeklampsia.
- Tindak lanjut (bunyi Buku KIA): pemeriksaan kehamilan, proses melahirkan, dan pemeriksaan
  nifas dilaksanakan di **Rumah Sakit**; lakukan **rujukan terencana** (tidak perlu menunggu
  inpartu). Script menambahkan "sesuai protokol fasilitas & keputusan dokter".
- 1 faktor sedang saja → belum memenuhi kriteria; ANC rutin & ukur TD tiap kunjungan
  (hanya bila **tidak** ada tanda bahaya).

**NICE NG133 (2019, diperbarui 2023), rek. 1.1.2–1.1.3** (opsi `--pedoman nice`):
- ≥ 1 faktor tinggi atau > 1 faktor sedang → kelompok yang dipertimbangkan untuk pencegahan
  sesuai pedoman (keputusan dokter). **Tidak ada dosis obat di alat ini.**

## Kode faktor
| Kode | Faktor | Buku KIA (2025) | NICE NG133 |
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
| map-90 | **MAP ≥ 90 mmHg** | sedang | — |
| proteinuria | Dipstik > +1 dua kali berjarak 6 jam / 300 mg/24 jam | **sedang** | — |
| riwayat-preeklampsia | Multipara dengan riwayat preeklampsia sebelumnya | tinggi | tinggi |
| riwayat-hipertensi-kehamilan | Hipertensi pada kehamilan sebelumnya **tanpa** diagnosis preeklampsia | — (tidak tercantum) | tinggi |
| kehamilan-multipel | Kembar | **tinggi** | **sedang** |
| diabetes-pregestasional | DM tipe 1/2 sejak sebelum hamil | tinggi ("diabetes dalam kehamilan") | tinggi |
| diabetes-gestasional | Diabetes yang muncul saat hamil | tinggi ("diabetes dalam kehamilan") | — (NICE hanya DM tipe 1/2) |
| diabetes | Diabetes dalam kehamilan, jenis tidak disebut | tinggi | ditolak — sebutkan jenisnya |
| hipertensi-kronik | Hipertensi kronik | tinggi | tinggi |
| penyakit-ginjal | Penyakit ginjal | tinggi | tinggi |
| autoimun | Autoimun / SLE | tinggi | tinggi |
| antifosfolipid | Sindrom antifosfolipid | tinggi | tinggi |

Angka yang diberikan (`--sistolik/--diastolik`, `--usia-ibu`, `--imt`) otomatis mengisi faktor
yang sesuai dan dilaporkan di baris "Faktor terisi otomatis dari angka".

## Rumus & ambang MAP
MAP = (sistolik + 2 × diastolik) / 3. Dibandingkan **tanpa pembulatan** dengan ambang Buku KIA
cetakan 2025 **MAP ≥ 90**: 110/80 → tepat 90,0 → **memenuhi**; 109/80 → 89,67 → tidak
(tampil 89,7, tidak dibulatkan ke 90 sebelum dibandingkan). Tampilan 1 desimal (setengah ke atas).

## Lapisan tanda bahaya (diperiksa lebih dulu)
| Kondisi | Hasil script | Sumber |
|---|---|---|
| TD ≥ 160 sistolik **atau** ≥ 110 diastolik | TANDA BAHAYA — SEGERA evaluasi/rujuk sesuai protokol kegawatdaruratan fasilitas | NICE NG133 (hipertensi berat ≥ 160/110); ACOG PB 222 (2020) |
| TD ≥ 140 sistolik **atau** ≥ 90 diastolik | TD rentang hipertensi — ukur ulang, evaluasi/rujuk HARI INI (kronik bila < 20 mg; gestasional/preeklampsia bila ≥ 20 mg) | NICE NG133 (≥ 140/90) |
| Gejala (`--gejala`): nyeri-kepala-hebat, pandangan-kabur, nyeri-ulu-hati, kejang, penurunan-kesadaran, sesak, bengkak-mendadak, perdarahan, ketuban-pecah, gerak-janin-berkurang, demam-tinggi, muntah-terus | TANDA BAHAYA — SEGERA evaluasi/rujuk | Buku KIA (tanda bahaya ibu hamil); NICE NG133 (gejala preeklampsia berat) |

Hasil dengan tanda bahaya **tidak pernah** memuat "Lanjutkan ANC rutin". Ambang & daftar gejala
**PERLU REVIEW** terhadap protokol fasilitas/PNPK yang dipakai.

## Pemetaan bahasa sehari-hari (contoh)
- "anak pertama", "G1P0" → nullipara
- "suami baru", "anak pertama dari suami kedua" → pasangan-baru
- "program bayi tabung", "hamil dari obat penyubur" → reproduksi-berbantu
- "dulu hamil darah tinggi" → **tanyakan**: didiagnosis preeklampsia/eklampsia (protein urin,
  kejang) → riwayat-preeklampsia; hanya darah tinggi → riwayat-hipertensi-kehamilan
- "kakak/ibunya dulu keracunan kehamilan" → riwayat-keluarga
- "gula darah tinggi waktu hamil" → diabetes-gestasional; "DM sejak sebelum hamil" →
  diabetes-pregestasional; "gula tinggi" tanpa keterangan (KIA) → diabetes
- "lupus" → autoimun; "APS" → antifosfolipid
- "pusing berat", "sakit kepala tidak hilang" → gejala nyeri-kepala-hebat; "mata berkunang/
  kabur" → pandangan-kabur; "bengkak tiba-tiba di muka/tangan" → bengkak-mendadak
