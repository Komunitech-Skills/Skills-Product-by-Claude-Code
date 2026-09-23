# 04 — Input tidak lengkap: tanya sekali

## Skenario
S4 — pengguna tidak menyebut produk maupun spesifikasi (keduanya **wajib**). Skill harus bertanya sekali, maks. 5 pertanyaan bernomor.

## Input pengguna
```
Buatin deskripsi produk buat toko online saya dong
```

## Output

Siap! Supaya judul dan deskripsinya mudah dicari pembeli dan tidak ada info yang salah, saya perlu beberapa hal dulu:

1. **Produknya apa?** Nama & jenisnya (mis. "sambal cumi botol", "gamis busui", "casing HP").
2. **Spesifikasinya:** ukuran/berat/isi, bahan, varian/warna. Kalau ada tabel ukuran, tempel saja.
3. **Dijual di mana?** Shopee, Tokopedia, TikTok Shop, atau ketiganya?
4. **Apa kelebihannya** dibanding produk sejenis? (cukup yang benar-benar ada, mis. "jahitan rapi", "tanpa MSG")
5. **Punya izin/sertifikat?** (halal, BPOM, P-IRT, SNI, garansi resmi) — sebutkan nomornya kalau ada. Kalau belum ada, tidak apa-apa, tidak akan saya tulis.

Kalau mau cepat, jawab nomor 1 dan 2 saja. Sisanya saya pakai default: ketiga platform, target pembeli saya simpulkan dari produknya, dan data
yang belum ada saya tandai `[isi: …]` supaya tidak ada yang dikarang.

## Catatan penguji
- **Bagus:** satu pesan, 5 pertanyaan bernomor, contoh jawaban dalam bahasa sehari-hari, jalan cepat. Pertanyaan 5 mencegah klaim izin karangan
  dan menenangkan pengguna yang belum punya sertifikat. Sesuai tabel Input SKILL.md.
