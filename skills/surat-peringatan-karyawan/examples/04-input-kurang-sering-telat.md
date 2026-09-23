# Contoh 04 – Input tidak lengkap: "karyawan saya sering telat"

## Skenario
S4, input tidak lengkap. Pengguna tidak menyebut nama, jabatan, tanggal keterlambatan, bukti, maupun riwayat SP. Sesuai langkah 1 SKILL.md ("Jika tidak ada fakta terukur, minta dulu; jangan menulis tuduhan umum"), skill harus bertanya sekali, maksimal 5 pertanyaan.

## Input pengguna
```
Buatin SP buat karyawan saya yang sering telat
```

## Output

Bisa. Supaya SP-nya kuat dan adil (bukan sekadar "sering telat"), aku perlu data berikut. Jawab singkat saja:

1. **Nama dan jabatan/bagian** karyawannya, serta nama usahamu dan kota.
2. **Tanggal-tanggal terlambat dan berapa lama.** Contoh: "2, 5, 9 September, masing-masing lebih dari 30 menit." Buktinya dari mana: absen fingerprint, buku absen, atau CCTV?
3. **Pernah ditegur atau dapat SP sebelumnya?** Jika pernah SP, sebutkan tingkat (SP1/SP2) dan tanggal terbitnya. Aku akan cek apakah SP itu masih berlaku.
4. **Aturan jam masuknya ada di mana?** Misalnya Peraturan Perusahaan pasal berapa, kontrak kerja, atau tata tertib tertulis. Boleh jawab "tidak ada tertulis".
5. **Sudah dipanggil dan ditanya alasannya?** Kalau belum, aku sertakan draf berita acara klarifikasi.

Kalau mau cepat, balas **"template aja"**. Aku buatkan SP1 dengan kolom `[...]` yang tinggal kamu isi.

## Catatan penguji
- **Bagus:** sesuai tabel Input (nama/jabatan, kronologi, dan riwayat SP adalah info wajib) dan batas 5 pertanyaan. Pertanyaan 3 langsung terhubung ke fungsi script (`--cek`). Pertanyaan 4 menyiapkan dasar aturan. Pertanyaan 5 menyiapkan berita acara.
- **Bagus:** tidak langsung membuat SP berisi tuduhan umum "sering terlambat", yang dilarang langkah 1.
- **Simulasi lanjutan:** bila dijawab "template aja", agent menghasilkan SP1 dengan `[Nama]`, `[tanggal-tanggal keterlambatan]`, masa berlaku dari script (23 September 2026 s.d. 22 Maret 2027), dan asumsi "belum pernah SP → SP1". Ini sesuai default di tabel Input.
- **Catatan:** pertanyaan 1 menggabungkan 2 info (karyawan + usaha) agar tetap 5 butir. Masih mudah dijawab.
