# Skenario 4 — Input tidak lengkap

## Input pengguna
```
Bantu saya cari calon pelanggan dong
```

## Output

```
Siap, saya bantu. Sebelum mulai, boleh jawab beberapa hal ini (santai saja):

1. Produk/jasa apa yang Anda jual?
2. Target pasarnya B2B (jual ke bisnis lain) atau B2C (langsung ke konsumen)?
   Kalau tahu industrinya atau area geografisnya, sebutkan juga.
3. Sudah punya gambaran profil pelanggan ideal (ICP), atau mau saya bantu susun
   dari nol?
4. Sudah punya daftar calon pelanggan (di CSV/teks), atau masih butuh arahan
   sumber pencarian?
5. Mau outreach lewat WA, email, atau LinkedIn?

Kalau mau cepat, jawab poin 1 saja dulu (produk/jasa) dan saya bisa mulai dengan
asumsi wajar untuk sisanya — nanti tinggal dikoreksi.
```

## Catatan penguji
- Sesuai aturan Input SKILL.md: bertanya sekali, maksimal 5 pertanyaan bernomor,
  dan hanya "Produk/jasa" yang benar-benar wajib (baris pertama tabel Input) —
  agent dengan tepat menandai itu sebagai satu-satunya yang wajib dijawab, sisanya
  opsional/boleh pakai asumsi.
- Tidak ada cacat ditemukan pada skenario ini.
