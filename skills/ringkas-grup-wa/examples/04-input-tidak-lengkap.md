# Contoh 04 — Input Tidak Lengkap (tanpa file ekspor)

## Skenario
S4. Pengguna minta ringkasan tapi belum melampirkan file ekspor apa pun.

## Input pengguna (persis)
> ringkas grup kantor dong

## Output

```
Boleh! Tapi aku butuh file ekspor chat-nya dulu (belum ada file yang dilampirkan). Caranya cepat
kok, sekitar 30 detik:

**Android:** buka grup kantor di WhatsApp → ketuk ⋮ (titik tiga, kanan atas) → Lainnya → Ekspor
chat → pilih "Tanpa Media" → kirim file .zip/.txt yang muncul ke sini (atau simpan ke folder
Unduhan lalu beri tahu aku lokasinya).

**iPhone:** buka grup kantor → ketuk nama grup di atas → gulir ke bawah → Ekspor Chat → pilih
"Tanpa Media" → kirim ke sini atau simpan ke Files.

Setelah filenya ada, kirim ke aku ya — aku langsung proses. Kalau grupnya sangat ramai/lama,
boleh juga sebutkan rentang waktu yang mau diringkas (mis. "3 hari terakhir" atau "sejak kemarin
sore"), kalau tidak disebut aku ringkas semua isi filenya.
```

## Catatan penguji
- **Sesuai SKILL.md:** persis mengikuti aturan "Jika file ekspor tidak ada, minta pengguna
  mengekspor dulu (panduan langkah di README.md)" dan "jangan tanya lebih dari sekali" — di sini
  hanya SATU pertanyaan/permintaan (file), dengan info rentang waktu ditawarkan sebagai opsi
  tambahan, bukan pertanyaan wajib kedua, jadi tidak melanggar aturan "jangan tanya lebih dari
  sekali".
- **Tidak mengarang isi grup kantor** yang tidak diketahui — bagus, tidak ada percobaan menebak
  isi chat tanpa data.
- **Kekurangan kecil:** langkah ekspor yang ditulis di jawaban ini disalin dari README.md secara
  manual oleh agent (karena SKILL.md sendiri hanya merujuk "lihat README.md untuk caranya",
  tidak menyalin ulang teksnya). Ini berarti kualitas jawaban S4 bergantung pada agent membaca
  README.md juga, bukan cuma SKILL.md. **Saran perbaikan:** karena ini pertanyaan yang hampir
  pasti muncul di S4 (kasus umum), pertimbangkan menambahkan ringkasan langkah ekspor (2–3 baris
  per platform) langsung di SKILL.md bagian "Input" atau "Batasan", supaya agent yang hanya
  memuat SKILL.md (tanpa ikut membaca README.md) tetap bisa memberi instruksi lengkap tanpa
  mengarang langkahnya sendiri — risiko: agent lain yang tidak membaca README bisa saja menebak
  langkah ekspor secara kira-kira dan berpotensi salah menu.
