# 00 — Uji A/B: S1 dengan vs tanpa skill

**Input pengguna (sama persis dengan S1):**
> Kak, tolong buatin caption IG buat keripik singkong pedas daun jeruk aku. Harganya 15rb per bungkus 200gr, kalau beli 3 jadi 40rb. Targetnya anak kos sama mahasiswa di Malang. Ordernya lewat WA 0812-0000-1234 atau DM aja.

## Output TANPA skill (AI agent biasa, tanpa membaca skill apa pun)
```
Berikut caption Instagram untuk keripik singkong kamu:

🌶️ KERIPIK SINGKONG PEDAS DAUN JERUK 🍃

Camilan wajib anak kos Malang! 😍

Renyah, gurih, pedasnya nampol, plus aroma daun jeruk yang bikin nagih! Dibuat dari singkong pilihan dan diolah secara higienis 👌

💰 Harga:
➡️ 1 bungkus (200gr): Rp15.000
➡️ Paket 3 bungkus: Rp40.000 (lebih hemat!)

Cocok buat nemenin nugas, begadang, atau nongkrong bareng teman kos 📚🎮

📲 Order sekarang via WA 0812-0000-1234 atau DM!
Stok terbatas, buruan sebelum kehabisan! 🔥

#keripiksingkong #keripikpedas #camilanmalang #anakkosmalang #jajananmalang #snackpedas #umkm #kulinermalang #mahasiswamalang #cemilanenak

Semoga membantu! Mau dibuatkan versi lain?
```

## Output DENGAN skill
Lihat `01-instagram-keripik-mahasiswa.md` (3 variasi: storytelling, langsung jualan, santai; masing-masing 81–82 kata tanpa hashtag, 6–8 hashtag campuran, tips posting).

## Berdampingan

| Aspek | TANPA skill | DENGAN skill |
|---|---|---|
| Jumlah pilihan | 1 caption | 3 variasi dengan gaya berbeda (A storytelling, B langsung jualan, C santai) |
| Hook baris pertama | Judul produk kapital + emoji (bukan hook) | Hook nyata: "Jam 11 malam, tugas numpuk…", "Rp40.000 dapat 3 bungkus…", "Dosen boleh killer…" |
| Panjang (tanpa hashtag) | 62 kata — **di bawah** rentang IG 80–150 dari skill | 81 / 81 / 82 kata (dicek penghitung kata) |
| Klaim yang tidak diberikan pengguna | **"singkong pilihan", "diolah secara higienis"** | Tidak ada |
| Urgensi palsu | **"Stok terbatas, buruan sebelum kehabisan!"** (tidak ada data stok) | Tidak ada |
| Emoji | ±12 emoji, judul kapital semua | Maks. ±1 per kalimat, tanpa huruf kapital semua |
| Hashtag | 10, campuran (bagus) | 6–8, campuran umum/niche/lokal (setara) |
| Tips posting | Tidak ada | Jam posting + ide carousel |
| Harga & cara order | Benar | Benar |

## Penilaian
- **Lebih baik berkat skill:** (1) tidak ada klaim karangan ("singkong pilihan", "higienis") dan urgensi palsu ("stok terbatas") yang muncul spontan
  pada versi tanpa skill — ini risiko nyata bagi UMKM (komplain/teguran iklan); (2) tiga gaya berbeda sehingga pengguna bisa memilih atau menggilir
  untuk beberapa posting; (3) hook sungguhan di baris pertama; (4) panjang sesuai pedoman platform; (5) tips posting.
- **Setara:** harga, paket, cara order, dan campuran hashtag sama-sama benar; gaya bahasa versi tanpa skill juga terasa lokal dan bisa dipakai.
- **Selisih:** lebih kecil dibanding skill yang punya script (tidak ada angka yang dihitung), tetapi tetap nyata dan konsisten pada aspek kejujuran klaim.
- **Kesimpulan:** hasil dengan skill **jelas lebih baik** (terutama pada kepatuhan klaim dan pilihan variasi), sehingga **tidak** termasuk cacat
  "skill tidak memberi nilai tambah".
