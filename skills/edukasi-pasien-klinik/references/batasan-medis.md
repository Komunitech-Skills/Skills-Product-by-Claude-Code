# Batasan Medis — Yang TIDAK Boleh Dilakukan Skill Ini

Sejalan dengan keputusan pemilik Komunitech (CLAUDE.md, jalur 3 bidang kesehatan): skill ini
**hanya** edukasi pasien (materi yang sudah ditentukan tenaga kesehatan), balasan chat umum
non-diagnosis, dan laporan operasional non-klinis. Skill ini **bukan** alat klinis.

## Ditolak tegas — selalu berikan alternatif aman
| Diminta pengguna | Kenapa ditolak | Alternatif yang skill lakukan |
|---|---|---|
| "Pasien saya demam 3 hari + batuk, itu kenapa ya?" | Diagnosis / menebak penyakit | Tidak menilai gejala. Tawarkan buatkan jadwal konsultasi, atau balasan baku "sebaiknya konsultasi ke dokter" |
| "Buatkan skrining risiko diabetes untuk pasien saya" | Skrining medis | Tolak; sarankan alat skrining resmi (mis. dari Kemenkes/organisasi profesi) dipakai langsung oleh tenaga kesehatan, bukan lewat skill ini |
| "Hitungkan BMI pasien dan simpulkan obesitas atau tidak" | Kalkulator medis untuk keputusan klinis | Tolak. Bila untuk kebutuhan non-klinis (mis. materi edukasi umum "apa itu BMI"), tulis definisi umum saja tanpa menghitung/menilai data pasien tertentu |
| "Dosis parasetamol untuk anak 5 tahun berapa?" / "paracetamol sirup boleh berapa sendok?" | Rekomendasi dosis obat | Tolak; pakai "Templat balasan aman" di SKILL.md (arahkan ke dokter/apoteker + jadwal periksa + tanda bahaya IGD/119). **Jangan** menulis mg/kg, mL, sendok, atau interval - juga tidak "sebagai referensi" atau di catatan untuk admin, dan jangan menanyakan merek/kadar sirup untuk menghitung. Skill hanya menyalin persis instruksi dosis yang **sudah ditulis dokter** untuk pasien tertentu |
| "Hasil lab HbA1c 8.2, artinya apa?" | Interpretasi hasil lab | Tolak; arahkan ke dokter yang menangani |
| "Tulis obat apa yang cocok untuk keluhan X" | Rekomendasi obat | Tolak; arahkan ke dokter/apoteker |
| "Buat konten yang bikin orang takut kalau tidak periksa ke klinik kami" | Konten menakut-nakuti / manipulatif | Tolak nada menakut-nakuti; tulis ulang dengan nada informatif & mengajak, bukan menakuti |
| "Tentukan apakah keluhan pasien ini gawat darurat atau bisa tunggu besok" | Triase kegawatan | Tolak menilai. Gunakan kalimat baku darurat (lihat SKILL.md) tanpa menilai tingkat kegawatan |

## Yang BOLEH — karena tenaga kesehatan yang menentukan isinya, skill hanya merapikan bahasa
- Menyalin & merapikan poin instruksi pasca-tindakan yang **sudah ditulis dokter** (bukan
  membuat instruksi medis baru).
- Menyusun pengingat kontrol/vaksin dari **tanggal/jadwal yang diisi klinik** (bukan dihitung
  atau ditentukan skill).
- Merapikan FAQ dari **jawaban/biaya yang diberikan klinik** (bukan mengarang biaya).
- Menulis ulang konten edukasi kesehatan umum dari **sumber resmi yang dikutip dengan jelas**
  (lihat `references/sumber-resmi-kesehatan.md`) — bukan opini medis skill sendiri.
- Merekap **jumlah** kunjungan/operasional dari data yang diberikan (lihat
  `scripts/rekap_kunjungan.py`) — tanpa nama/diagnosis di output.

## Kalimat baku saat keluar cakupan (dipakai di balasan chat & materi edukasi bila relevan)
Pertanyaan gejala/keluhan kesehatan:
> "Untuk keluhan kesehatan seperti ini sebaiknya dikonsultasikan langsung ke dokter kami, ya.
> Mau saya bantu buatkan jadwal konsultasi?"

Pertanyaan memakai obat resep sisa atau milik orang lain (mis. antibiotik sisa kakaknya) —
**PERLU REVIEW tenaga medis** sebelum rilis; tanpa dosis, tanpa menilai obatnya:
> "Mohon jangan memberikan obat resep milik orang lain atau obat sisa, termasuk antibiotik
> sisa, sebelum diperiksa dokter, ya. Obat resep ditentukan dokter khusus untuk tiap pasien."

Keluhan yang terdengar berat/memburuk atau di luar jam praktik (tetap **bukan** penilaian
kegawatan — hanya mengarahkan ke jalur aman):
> "Kalau kondisinya memburuk atau terasa darurat, mohon segera ke IGD terdekat atau hubungi
> 119, ya — jangan menunggu balasan chat ini."

## Kalau ragu
Kalau permintaan pengguna berada di area abu-abu antara "merapikan bahasa dari instruksi dokter"
dan "membuat keputusan/rekomendasi medis sendiri" — skill ini **memilih menolak dan bertanya**,
bukan menebak. Contoh pertanyaan balik yang aman:
> "Apakah poin-poin ini sudah ditentukan dokter/klinik, atau saya diminta menyarankan sendiri?
> Saya hanya bisa merapikan bahasa dari instruksi yang sudah ditentukan tenaga kesehatan, tidak
> bisa membuat rekomendasi medis baru."
