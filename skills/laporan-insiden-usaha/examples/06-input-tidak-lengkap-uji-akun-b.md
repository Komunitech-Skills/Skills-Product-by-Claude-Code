# Uji 06 — Input Tidak Lengkap

## Input pengguna
> "Kemarin ada masalah di toko, tolong buatin laporan insiden."

## Perilaku yang diharapkan (dari SKILL.md § Input)
Tabel Input menandai wajib: "Apa yang terjadi (kronologi kasar)", "Kapan (tanggal & jam mulai/ketahuan/selesai)", dan pengecekan "Apakah menyangkut data pelanggan". Instruksi umum pedoman kurasi Komunitech/SKILL.md: tanyakan **sekali** dalam satu pesan berisi daftar pertanyaan singkat, bukan bertanya berulang-ulang satu per satu.

## Output simulasi (mengikuti SKILL.md persis)

Baik, saya bantu susun laporan insidennya. Boleh dilengkapi dulu (cukup jawab singkat, boleh sekaligus dalam satu balasan):

1. **Apa yang terjadi?** (ceritakan kejadiannya, boleh singkat)
2. **Kapan?** — tanggal kejadian, jam mulai, jam ketahuan, dan status sekarang (sudah selesai atau masih berjalan)
3. **Siapa/berapa yang terdampak?** — jumlah pesanan/pelanggan, atau estimasi kerugian, kalau ada datanya (kalau belum tahu pasti, tidak apa-apa, nanti saya tandai)
4. **Apakah kejadian ini menyangkut data pelanggan** (mis. file/nomor pelanggan tersebar ke pihak yang salah)? Ya/Tidak
5. **Nama usaha/toko** (untuk draf permintaan maaf), kalau ada

Begitu info di atas ada (boleh sebagian saja untuk yang belum pasti), saya langsung susun laporan lengkapnya.

## Catatan penguji
- Sesuai instruksi: **satu pesan**, berisi **daftar** pertanyaan singkat — bukan menanyakan satu per satu bertahap, dan bukan langsung mengarang laporan dari nol data.
- Pertanyaan mencakup seluruh kolom "Wajib: Ya" di tabel Input (apa, kapan, cek data pelanggan) plus kolom penting lain (dampak, nama usaha) tanpa memaksa semuanya wajib dijawab — konsisten dengan kolom "Tidak, tapi diminta jika ada".
- Skill tidak memaksakan menyusun laporan dengan kerangka kosong penuh `[isi: ...]` di semua bagian sebelum bertanya — sesuai semangat "instan tapi reliable": tetap minta info inti dulu, bukan mengarang kronologi.
- **Lulus.**

## Penyegaran v1.0.5 (2026-10-17)
Output dan kesimpulan di atas (Lulus) **tidak diubah** dan tetap sesuai SKILL.md v1.0.5: pesan tanpa fakta apa pun → tanya sekali dalam satu daftar singkat. Aturan baru v1.0.5 (pemisahan "Sudah dilakukan"/"Disarankan", tanda dugaan, cek konsistensi angka) berlaku begitu laporan disusun dari jawaban pengguna. Satu pertanyaan bisa ditambahkan agar daftar "Sudah dilakukan" tidak ditebak: "Apa saja yang sudah Anda lakukan sejauh ini?"
