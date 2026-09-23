# 04 — Input tidak lengkap (tanya sekali)

**Skenario:** S4 — pengguna tidak menyebut pembeli, jumlah, harga, dan status PKP.

**Input pengguna:**
> buatin penawaran harga kursi lipat buat pelanggan saya ya

## Output

Siap, saya bantu buatkan surat penawarannya. Supaya hitungannya pas, saya perlu beberapa info dulu (jawab singkat saja):

1. **Nama usaha Anda** + kota, nomor WA/email untuk kop surat.
2. **Nama pelanggan** (perusahaan/instansi/perorangan) dan nama orang yang dituju.
3. **Rincian kursi lipat:** jumlah, satuan, dan harga per unit (kalau ada beberapa tipe, sebutkan masing-masing). Ada diskon atau ongkir?
4. **Usaha Anda sudah PKP** (memungut PPN) atau belum? Kalau tidak yakin, saya anggap **belum PKP** (tanpa PPN).
5. Ada syarat khusus? (masa berlaku, cara bayar, waktu kirim). Kalau tidak, saya pakai standar: berlaku 14 hari, DP 50% saat PO, pelunasan sebelum kirim, kirim 3–7 hari kerja.

Kalau mau cepat, cukup kirim poin 1–3; sisanya saya isi dengan standar di atas dan saya tulis asumsinya di bawah surat.

## Catatan penguji
- Sesuai SKILL.md: bertanya **sekali**, maksimal 5 pertanyaan bernomor, dengan default yang jelas dan jalur cepat.
- Tidak mengarang harga kursi (sesuai batasan "jangan mengarang harga pasar").
- Script tidak dijalankan karena tidak ada item — benar (script juga akan menolak: `ERROR: belum ada item`).
