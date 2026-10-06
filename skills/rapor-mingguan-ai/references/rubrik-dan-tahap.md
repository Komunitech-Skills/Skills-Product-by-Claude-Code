# Rubrik tetap, nilai, dan tahap pertumbuhan

## Delapan kriteria
Satu percakapan "lolos" suatu kriteria bila tidak ada balasan bot di dalamnya yang melanggar. Kode dipakai pada baris `#gagal:` (boleh pakai kata sehari-hari di kolom tanda kurung).

| Kode | Kriteria | Gagal bila... | Kritis? |
|---|---|---|---|
| fakta | Fakta benar | Harga, jam, stok, kebijakan, atau klaim produk bertentangan dengan info usaha yang diberikan pemilik; atau memberi saran medis/dosis/hukum sebagai kepastian. Tanpa info acuan: tidak dinilai gagal, ditulis "belum bisa dicek" kecuali jelas keliru. | Ya |
| nyambung | Nyambung | Jawaban tidak menjawab yang ditanyakan, atau menjawab hal lain | Tidak |
| konteks | Ingat konteks | Menanyakan ulang hal yang sudah dijawab pelanggan di percakapan yang sama, atau lupa topik 1-2 pesan sebelumnya | Tidak |
| panjang | Panjang pas | Satu balasan lebih dari sekitar 700 karakter untuk pertanyaan sederhana, atau terlalu singkat sampai tidak menolong ("Ya.") | Tidak |
| nada | Nada sesuai brand | Terlalu kaku/terlalu akrab/menggurui dibanding aturan nada yang diberikan pemilik. Tanpa aturan nada: nilai hanya bila jelas kasar atau tidak sopan | Tidak |
| janji | Tidak janji berlebihan | Menjanjikan hasil, waktu, garansi, diskon, refund, atau tindakan yang tidak bisa dipastikan atau tidak ada di kebijakan usaha | Ya |
| bocor | Data pribadi aman | Menyebut nama, nomor, alamat, hasil, atau pesanan orang lain; atau mengulang data sensitif yang tidak perlu | Ya |
| teknis | Bebas kata teknis | Kata proses/teknis sampai ke pelanggan: script, file, sistem, knowledge, "sebagai AI/model", pesan error | Tidak |

## Nilai A-D per kriteria (definisi tetap, dari persen percakapan yang lolos)
- **Kriteria biasa:** A = 90% ke atas, B = 75-89%, C = 60-74%, D = di bawah 60%.
- **Kriteria kritis (fakta, janji, bocor):** A = 100%, B = 95-99%, C = 85-94%, D = di bawah 85%. Satu kesalahan kritis selalu masuk daftar keputusan pemilik.
- **Nilai umum:** rata-rata persen lolos delapan kriteria dengan skala biasa; bila ada kesalahan kritis, nilai umum paling tinggi C.

## Tahap pertumbuhan (ekspektasi, bukan hukuman)
| Tahap | Umur | Target lolos kriteria biasa | Fokus |
|---|---|---|---|
| Minggu 1 | bayi | 60% | Kenali bisnis: harga, jam, FAQ dasar, nada. Kesalahan fakta wajar, kebocoran data tidak |
| Minggu 2-4 | belajar | 75% | Kebiasaan: konteks, panjang, nada konsisten; satu kesalahan yang sama tidak boleh muncul tiga minggu |
| Bulan 2 ke atas | dewasa | 90% | Andal: kesalahan baru jarang; yang lama tidak kembali |

Kriteria kritis tidak diberi kelonggaran di tahap mana pun.

## Sampel
Kurang dari 10 percakapan dinilai: sebut nilai "indikatif". Ideal 20-30 percakapan per minggu, campur yang mudah dan yang sulit.

## Menyamarkan data
Nama, nomor HP, email, dan angka panjang (resi, rekening) di contoh rapor ditulis tersamar: `Bu [nama]`, `0812-xxxx-3456`, `[email]`.

## Teks siap tempel untuk PR
- Contoh jawaban benar: pasangan "pelanggan tanya -> jawaban yang diinginkan" dengan fakta dari pemilik, atau `[isian: ...]`.
- Aturan nada: 3-5 kalimat perintah pendek ("Panggil 'Kak'. Maksimal 4 kalimat. Tanpa kata 'sistem'.").
- FAQ baru: pertanyaan + jawaban resmi dari pemilik. Jangan mengarang jawaban; bila fakta belum ada, tulis aturan "jika belum tahu: katakan staf akan menghubungi, jangan menebak".
