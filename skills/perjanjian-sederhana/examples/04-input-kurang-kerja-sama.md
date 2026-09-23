# 04 — Input tidak lengkap: "buatin perjanjian kerja sama"

## Skenario
S4, input tidak lengkap. Jenis perjanjian dan objek tidak jelas. "Kerja sama" bisa berarti reseller, bagi hasil, supplier, atau bahkan investasi (yang harus ditolak). SKILL.md: jenis perjanjian wajib (tebak dari konteks lalu konfirmasi) dan tanyakan **sekali** maks 5 pertanyaan bernomor.

## Input pengguna
> tolong buatin surat perjanjian kerja sama sama temenku ya

## Output

Siap, saya bantu. Supaya drafnya pas, saya perlu tahu beberapa hal dulu (jawab singkat saja):

1. **Kerja samanya seperti apa?** Pilih yang paling mirip:
   a. Patungan/bagi hasil usaha (satu modal, satu mengelola, untung dibagi)
   b. Teman jadi reseller/agen produkmu
   c. Teman memasok barang/bahan ke usahamu
   d. Sewa tempat/alat, atau jasa (desain, foto, dll.)
   e. Lainnya, ceritakan singkat
2. **Nama usaha dan apa yang dijalankan?** (mis. kedai kopi di Malang)
3. **Siapa menyetor apa?** Uang (berapa), tempat, alat, atau tenaga. Kamu di posisi yang mana?
4. **Bagaimana pembagian hasil/harganya?** (mis. laba dibagi 60:40 tiap bulan, atau harga beli Rp ... per barang)
5. **Berapa lama kerja samanya, dan di kota mana kalian tinggal?** (untuk jangka waktu dan pengadilan bila ada sengketa)

Nama lengkap, NIK, dan alamat bisa diisi belakangan. Di draf akan saya beri tanda `[[...]]`.

Catatan singkat: kalau temanmu **menjanjikan keuntungan tetap** (mis. "pasti dapat 5% per bulan") atau dananya dikumpulkan dari **banyak orang**, itu masuk kategori investasi. Untuk itu saya tidak membuat draf dan akan menyarankan ke pengacara/notaris, karena berisiko melanggar aturan penghimpunan dana.

## Catatan penguji
- Sesuai SKILL.md: satu pesan, 5 pertanyaan bernomor, jenis perjanjian dikonfirmasi lewat pilihan (bukan ditebak), posisi pengguna ditanyakan, data pribadi boleh menyusul (`[[...]]`).
- Nilai tambah: agent memberi peringatan dini soal "imbal hasil pasti/banyak investor" (dari `references/batasan-rujukan.md` dan PANDUAN AGENT `bagi-hasil.md`), karena "kerja sama sama teman" sering berupa titip modal dengan janji keuntungan tetap.
- Tidak ada kekurangan berarti. Pilihan (a)–(e) memudahkan pengguna awam.
