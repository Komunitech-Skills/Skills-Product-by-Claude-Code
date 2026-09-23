# Contoh 04 – Input tidak lengkap: minta notulen tanpa menempel catatan

## Skenario
S4, input tidak lengkap. Pengguna minta notulen "rapat tadi", tapi tidak menempel catatan apa pun. Menurut SKILL.md, catatan adalah satu-satunya info wajib ("Jika catatan tidak ada, minta ditempel. Info lain tidak perlu ditanyakan dulu"). Skill tidak boleh mengarang isi rapat.

## Input pengguna
```
buatin notulen rapat tadi dong, yg rapat evaluasi bulanan
```

## Output

Siap! Supaya notulennya akurat, aku butuh **isi rapatnya dulu**, karena aku tidak ikut rapat dan tidak mau mengarang keputusan.

Tempel salah satu dari ini:
- **Catatan rapat** (boleh berantakan, singkatan, atau poin-poin cepat), atau
- **Transkrip** dari Zoom/Google Meet/Teams, atau dari aplikasi perekam di HP, atau
- **Ringkasan voice note** yang sudah diketik.

Info lain (tanggal, tempat, siapa saja yang hadir) tidak wajib. Yang tidak ada nanti aku tandai di bagian **"Perlu dikonfirmasi"**.

💡 Kalau rapatnya direkam dan belum ada transkrip: Google Meet dan Zoom punya fitur transkrip otomatis, dan banyak aplikasi perekam HP juga bisa mengubah suara menjadi teks. Salin teksnya ke sini.

## Catatan penguji
- **Bagus:** persis sesuai tabel Input dan kalimat "Info lain tidak perlu ditanyakan dulu". Hanya satu permintaan (catatan), bukan daftar pertanyaan panjang. Ini tepat untuk skill yang inputnya "tempel teks".
- **Bagus:** menjelaskan 3 bentuk input yang diterima dan menawarkan cara mendapatkan transkrip, tanpa menjanjikan transkripsi audio (sesuai *Kapan TIDAK digunakan*).
- **Catatan:** saran fitur transkrip Meet/Zoom bersifat umum dan tidak menyebut paket berbayar atau nama aplikasi tertentu. Aman dari klaim yang bisa kedaluwarsa.
