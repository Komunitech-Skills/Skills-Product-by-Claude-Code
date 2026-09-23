# Contoh 04 – Input tidak lengkap

## Skenario
S4, input tidak lengkap. Pengguna hanya menyebut platform (WA Status) dan jenis produk yang sangat umum ("sambal"). Harga/promo, cara order, dan keunggulan tidak ada. WA Status maksimal 30 kata dan harus "langsung ke promo & cara order", jadi tanpa harga dan cara order caption-nya tidak berguna. Skill harus bertanya **sekali** dengan daftar singkat.

## Input pengguna
```
caption buat wa status dong, jual sambal
```

## Output

Siap! Biar caption WA Status-nya langsung bikin orang order, aku perlu beberapa info dulu. Jawab singkat aja:

1. **Sambal apa & keunggulannya?** (contoh: sambal bawang, sambal cumi, level pedas, isi berapa gram)
2. **Harga / promo?** (contoh: Rp20.000 per botol, beli 2 gratis ongkir)
3. **Cara order?** (contoh: balas status ini, WA 0812-0000-xxxx, Shopee)
4. **Target pembeli** (opsional; contoh: ibu rumah tangga, anak kos, pekerja kantoran)

Kalau mau cepat, balas "pakai asumsi aja". Nanti aku buatkan 3 variasi dengan asumsi yang wajar, dan harga serta cara order kutulis sebagai [isi harga] / [isi cara order] supaya tinggal kamu ganti.

## Catatan penguji
- Bagus: satu pesan, satu daftar singkat, sesuai langkah 1 SKILL.md. Poin wajib dan opsional dibedakan, contoh jawabannya bahasa awam, dan ada jalan pintas "pakai asumsi aja".
- Bagus: tidak memaksakan caption dengan harga atau keunggulan karangan, yang akan melanggar aturan "jangan membuat klaim yang tidak diberikan pengguna".
- Kurang: SKILL.md tidak menentukan kapan harus bertanya dan kapan boleh langsung memakai asumsi. Contoh 03 memakai asumsi, contoh 04 bertanya. Keputusan ini diserahkan ke penilaian agent. Sebaiknya ada aturan eksplisit, misalnya: "Jika produk ATAU cara order tidak diketahui, tanya dulu; selain itu pakai asumsi."
- Kurang: format output di SKILL.md tidak menyebut placeholder seperti [isi harga]. Sebaiknya distandarkan.
