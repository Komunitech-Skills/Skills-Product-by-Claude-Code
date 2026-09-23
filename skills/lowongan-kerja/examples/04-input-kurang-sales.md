# Contoh 04 – Input tidak lengkap: "buatin loker sales ya"

## Skenario
S4, input tidak lengkap. Pengguna hanya menyebut posisi. Tiga info wajib (nama usaha & bidang, lokasi) tidak ada. Skill harus bertanya **sekali**, maksimal 5 pertanyaan bernomor, dan menawarkan jalan cepat dengan placeholder.

## Input pengguna
```
buatin loker sales ya
```

## Output

Siap, aku buatkan. Supaya lowongannya pas dan menarik pelamar yang tepat, aku perlu beberapa info dulu (jawab singkat saja):

1. **Nama usaha dan jualannya apa?** (mis. "CV Sumber Rasa, distributor snack ke warung". Boleh ditulis "Rahasia" kalau tidak mau disebut.)
2. **Kota dan jenis kerjanya?** Sales lapangan/kanvas (keliling ke toko), sales toko/showroom, atau sales online?
3. **Status kerja:** tetap, kontrak, freelance, atau part-time?
4. **Gaji & benefit:** gaji pokok/rentang, insentif atau komisi, uang bensin, BPJS? (Boleh dikosongkan, tapi loker yang mencantumkan gaji biasanya dapat lebih banyak pelamar.)
5. **Cara melamar:** email atau nomor WA, dan sampai kapan?

Kalau mau cepat, balas **"langsung aja"**. Aku buatkan sekarang dengan tugas umum sales lapangan dan placeholder `[isi ...]` untuk data yang belum ada, lalu kamu tinggal mengisinya.

## Catatan penguji
- **Bagus:** tepat sesuai aturan "tanyakan sekali dalam satu pesan (maks 5 pertanyaan bernomor)" dan opsi cepat dengan placeholder. Pertanyaan 2 sekaligus menentukan daftar tugas (sales lapangan vs toko) dari `references/contoh-posisi.md`.
- **Bagus:** tidak langsung mengarang nama usaha atau gaji.
- **Catatan:** tabel Input SKILL.md memisahkan "Nama usaha & bidang usaha" (wajib) dan "Lokasi" (wajib). Keduanya tercakup di pertanyaan 1–2. Pertanyaan 3–5 adalah info opsional yang ditanyakan bersamaan, masih dalam batas 5 pertanyaan.
- **Simulasi lanjutan:** bila pengguna membalas "langsung aja", agent menghasilkan loker "Sales Lapangan (Canvasser)" dengan `[Nama Usaha]`, `[Kota]`, `[isi status kerja]`, dan gaji "dibicarakan saat interview", ditambah Asumsi di akhir. Perilaku ini sesuai SKILL.md.
