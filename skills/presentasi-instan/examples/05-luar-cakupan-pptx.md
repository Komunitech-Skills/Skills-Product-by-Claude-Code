# Contoh 05 — Di luar cakupan: minta file PowerPoint yang bisa diedit

## Skenario
S5. Pengguna butuh file `.pptx` untuk diedit rekan kantor di Microsoft PowerPoint.

## Input pengguna
```
Bisa bikinin file PowerPoint (.pptx) materi rapat koordinasi cabang? Nanti mau diedit-edit lagi sama tim di PowerPoint kantor.
```

## Output
```
Skill presentasi yang saya pakai menghasilkan satu file HTML (dibuka di browser, bisa tanpa internet, bisa dicetak ke PDF), bukan file .pptx asli. File HTML tidak bisa diedit di Microsoft PowerPoint.

Karena tim Anda perlu mengedit di PowerPoint, pilihannya:
1. Pakai alat/skill pembuat .pptx terpisah bila tersedia di aplikasi AI Anda — saya bisa bantu menyiapkan kerangka & isi slidenya dulu (judul + poin per slide) supaya tinggal dimasukkan.
2. Kalau tujuan akhirnya cuma ditampilkan/dikirim (tidak diedit), saya bisa buatkan versi HTML + PDF-nya sekarang.

Mau pilih yang mana? Kalau nomor 1, kirim poin-poin materi rapatnya.
```

## Catatan penguji
- Sesuai "Kapan TIDAK digunakan" poin 1 dan FAQ README: jujur bahwa hasilnya HTML, mengarahkan ke alat .pptx, tidak memaksakan.
- Nilai tambah: menawarkan kerangka isi yang tetap berguna.
- Catatan: description menyebut "tanpa PowerPoint/Canva", sehingga permintaan .pptx memang bisa memicu skill ini — penanganan penolakannya sudah benar.

## Penyegaran v1.1.6 (2026-10-17)
> Output asli di atas dan skornya **tidak diubah**. Sejak v1.1.6 balasan dilarang menyebut nama skill atau alat internal ke pengguna, jadi pembukaan "Skill presentasi yang saya pakai ..." dan pilihan "alat/skill pembuat .pptx" ditulis tanpa kata "skill". Isi penolakan dan alternatifnya sama.

Balasan ke pengguna (format v1.1.6):
```
Presentasi yang bisa saya buatkan berupa satu file HTML (dibuka di browser, bisa tanpa internet, bisa dicetak ke PDF), bukan file .pptx asli. File HTML tidak bisa diedit di Microsoft PowerPoint.

Karena tim Anda perlu mengedit di PowerPoint, pilihannya:
1. Pakai fitur pembuat file PowerPoint bila tersedia di aplikasi AI Anda — saya bisa bantu menyiapkan kerangka & isi slidenya dulu (judul + poin per slide) supaya tinggal dimasukkan.
2. Kalau tujuan akhirnya cuma ditampilkan/dikirim (tidak diedit), saya bisa buatkan versi HTML yang siap dicetak jadi PDF sekarang.

Mau pilih yang mana? Kalau nomor 1, kirim poin-poin materi rapatnya.
```
