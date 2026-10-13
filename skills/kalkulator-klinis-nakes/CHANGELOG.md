# Riwayat perubahan — kalkulator-klinis-nakes

Catatan teknis per versi.

## Catatan revisi 1.0.6 (2026-10-02)
- Revisi dari temuan uji OpenClaw: daftar "belum ditanyakan" pada skrining preeklampsia kini juga memuat hipertensi kronik (selain diabetes, penyakit ginjal, autoimun/APS, proteinuria), dan script menuliskannya otomatis di catatan hasil.
- Uji regresi ditambah untuk perubahan ini. Skill tetap berstatus PERLU REVIEW tenaga medis.

## Catatan revisi 1.0.5 (2026-10-02)
- Label hasil skrining preeklampsia pedoman Buku KIA diubah menjadi "BERISIKO PREEKLAMPSIA - perlu rujukan terencana (>= 2 faktor risiko sedang)" agar sesuai makna pedoman (bukan "risiko sedang/menengah"); pedoman NICE memakai label serupa.
- Ditambah "Template balasan untuk awam" yang wajib dipakai bila yang bertanya pasien/ibu hamil/keluarga: bukan diagnosis, tidak menjalankan script, tidak menyebut nama obat maupun dosis, tanda bahaya di baris paling atas. Pesan jelas dari orang awam langsung dijawab dengan template ini tanpa bertanya peran lagi.
- Kalimat baku di `references/batasan-dan-kalimat-baku.md` diperketat (tidak boleh menyebut obat atau angka mg, juga tidak "sebagai info umum").

## Catatan revisi 1.0.4 (2026-10-01)
- SKILL.md kini menyebut bahwa script ada di subfolder `scripts/` di folder skill, dan agent tidak boleh mencari file ke seluruh disk (mis. `find /`). Logika tidak berubah.

## Catatan revisi 1.0.3 (2026-09-30)
- Ditambah baris "Aturan kerja" di SKILL.md: tidak memasang paket/aplikasi sendiri, tidak membuka file di luar yang diberikan pengguna dan isi folder skill, dan menyebut lokasi file baru. Logika tidak berubah.

## Catatan revisi 1.0.2 (2026-09-29)
- Lapisan tanda bahaya ditambah penanda tekanan darah rendah (sistolik < 90 atau diastolik < 60) sebagai penanda konservatif dengan sumber NHLBI; ditandai PERLU REVIEW medis.
- Tekanan darah yang hanya satu angka (mis. sistolik saja) tetap dinilai terhadap ambang tanda bahaya; MAP tidak dihitung dan angka yang kurang disebut. Tanpa tekanan darah sama sekali, hasil menulis bahwa tanda bahaya belum diperiksa, bukan "ANC rutin".
- Kode gejala atau faktor yang tidak dikenal tidak lagi membatalkan hasil: tanda bahaya dicetak dulu, lalu kode yang tidak dikenal dilaporkan.
- CSV `imt-batch` mengenali pemisah koma atau titik koma (;); baris dengan koma desimal tanpa tanda kutip ditandai "GAGAL" disertai petunjuk, baris lain tetap dihitung.
- Opsi `--json` harus diletakkan sebelum sub-perintah (dijelaskan di SKILL.md). Uji regresi diperluas.

## Catatan revisi 1.0.1 (2026-09-29)
- Revisi setelah uji pertama (skor 6/10): ditambah lapisan tanda bahaya yang diperiksa lebih dulu (TD ≥ 160/110 atau gejala bahaya → segera evaluasi/rujuk; TD ≥ 140/90 → evaluasi hari ini) dengan sumber NICE NG133 dan ACOG PB 222. Hasil skrining tidak pernah berakhir dengan "lanjutkan ANC rutin" bila ada tanda bahaya.
- Skrining preeklampsia memakai Buku KIA edisi terbaru (cetakan 2025); ambang MAP menjadi ≥ 90; tindak lanjut ditulis sesuai Buku KIA (ANC, persalinan, dan nifas di rumah sakit; rujukan terencana). Bagian "Belum ditanyakan" ditambahkan di hasil.
- Opsi `--gejala` ditambahkan; IMT dewasa bisa untuk banyak pasien sekaligus lewat CSV (`imt-batch`).
- Bagian "Instrumen kognitif" ditambahkan: alat hanya menafsirkan skor total MMSE/MoCA/AMT, tidak menampilkan, menulis ulang, atau memandu pelaksanaan formulir/butirnya.
- Pesan untuk orang awam yang bertanya soal kehamilan diberi arahan periksa hari ini bila ada gejala. Daftar sumber pedoman dan uji regresi diperluas.

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): skrining faktor risiko preeklampsia + MAP, kalkulator kehamilan (HPL Naegele, usia kehamilan dari HPHT/USG), IMT pra-hamil dan kenaikan BB hamil (IOM 2009), IMT dewasa + lingkar perut, tafsir skor total MMSE/MoCA/AMT, dan templat catatan sesi stimulasi kognitif. Khusus tenaga kesehatan; ditandai PERLU REVIEW tenaga medis.
