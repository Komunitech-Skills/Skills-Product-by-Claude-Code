# Template Pesan Pembuka WA (3 Varian)

Isi bagian `[...]`. Jalankan tiap varian lewat `python3 scripts/cek_pesan.py cek --pesan "..." --jam-kirim "HH.MM" --zona WIB/WITA/WIT` sebelum dikirim. Target panjang per varian (v1.0.1): singkat ≤ 300 karakter, sedang ≤ 400 karakter, dengan nilai tambah ≤ 500 karakter — kalau draf melebihi target, gabungkan/pangkas kalimat, jangan biarkan peringatan panjang jadi rutin.

## Varian 1 — Singkat (± 2-3 kalimat, target ≤ 300 karakter; cocok C-level/pemilik usaha sibuk atau B2C santai)
```
Selamat [pagi/siang/sore], [Pak/Bu/Kak] [Nama]. Saya [nama pengirim] dari [nama usaha],
dapat nomor [Bapak/Ibu/Kakak] dari [asal kontak: referral/pameran/Google Maps/IG/grup].
[Satu ajakan ringan yang mudah dijawab ya/tidak]. Boleh diabaikan bila belum relevan ya, [sapaan].
```

## Varian 2 — Sedang (± 3-5 kalimat, target ≤ 400 karakter; umum untuk UMKM/profesional)
```
Selamat [pagi/siang/sore], [Pak/Bu/Kak] [Nama]. Perkenalkan saya [nama pengirim] dari [nama usaha].
Saya dapat nomor [Bapak/Ibu/Kakak] dari [asal kontak spesifik].
Kami [satu kalimat: apa yang dikerjakan/ditawarkan], yang mungkin relevan untuk [alasan spesifik terkait penerima].
[Satu pertanyaan/ajakan ringan]. Mohon maaf mengganggu, dan boleh diabaikan bila tidak relevan, [sapaan].
```

## Varian 3 — Dengan nilai tambah (± 4-6 kalimat, target ≤ 500 karakter; untuk B2B/nilai penawaran perlu dijelaskan)
```
Selamat [pagi/siang/sore], [Pak/Bu/Kak] [Nama]. Saya [nama pengirim] dari [nama usaha],
dapat nomor [Bapak/Ibu] dari [asal kontak spesifik].
[Satu kalimat: akibat/masalah yang biasanya dialami usaha sejenis penerima terkait topik ini
— tulis dengan kata sendiri sesuai konteks nyata, JANGAN jadi daftar fitur produk kita].
Kami bantu mengatasi itu lewat [manfaat spesifik/hasil, sebutkan bukti nyata hanya jika ada dan benar].
Kalau [Bapak/Ibu] terbuka, boleh saya kirim [info singkat/katalog/contoh]? Boleh diabaikan bila
belum relevan, [sapaan]. Terima kasih.
```

## Catatan pengisian
- **Asal kontak** harus spesifik (lihat `references/pola-pembuka.md`), bukan "dari internet" atau "random".
- **Ajakan/CTA** harus satu, ringan, mudah dijawab ya/tidak — hindari minta waktu telepon/meeting di pesan pertama.
- **Bukti/klaim** hanya boleh ditulis kalau benar-benar ada dan disetujui pengguna — jangan mengarang jumlah pelanggan, testimoni, atau hasil.
- **Detail layanan yang tidak diberikan pengguna** (mis. "bisa datang ke lokasi", "ada garansi 1 tahun") ditulis sebagai `[isi: ...]` di draf, atau dipindah ke bagian Asumsi — jangan diisi sendiri berdasarkan tebakan.
- Ganti sapaan sesuai konteks: "Pak/Bu" untuk B2B/formal, "Kak" untuk B2C/santai, sesuaikan dengan gaya yang diminta pengguna.
