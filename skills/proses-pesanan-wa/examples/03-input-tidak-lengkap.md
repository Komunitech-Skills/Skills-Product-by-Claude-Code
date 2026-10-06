# Skenario 3 (input tidak lengkap)

**Input:** "ini pesanan masuk: 'mba mau 2 yg coklat kirim ke bekasi'"

## Output SESUDAH

````
**Ringkasan:** 1 pesanan masuk (coklat x2, kirim ke Bekasi) — totalnya belum bisa dipastikan karena harga "coklat" dan ongkir belum ada, dan alamatnya masih terlalu singkat.

**[20261006-01] — Kak (nama belum disebutkan di chat)**
- Coklat x2 @ *[isian: harga]* = *[isian]*
- Subtotal: *[isian: subtotal]*
- Ongkir: *[isian: ongkir]*
- **Total: [isian: total, menunggu harga]**
- Bayar: belum bayar
- Kurir: *[isian: kurir]*

**Pesan konfirmasi (siap salin, lengkapi bagian isian dulu):**
```
Halo Kak, terima kasih sudah order ya 🙏
Pesanannya kami catat:

20261006-01
• Coklat x2

Boleh dibantu lengkapi dulu, Kak, biar bisa kami hitungkan totalnya & paketnya tidak nyasar:
1. Alamat lengkap (jalan & no rumah, RT/RW, kelurahan, kecamatan, kota Bekasi, kode pos)
2. Nomor HP penerima yang aktif
3. Mau kirim pakai kurir apa (JNE/J&T/SiCepat/dll)?

Total akan kami kabari setelah ongkir dicek, ya Kak 😊
```

**Nota:** belum bisa dibuat utuh — baris TOTAL masih *[isian: total]* sampai harga "coklat" diisi.

**Label pengiriman:** belum siap ditempel — alamat cuma "Bekasi", HP penerima belum ada, kurir belum dipilih. Begitu lengkap, saya buatkan labelnya.

**Rekap harian:** 1 pesanan, omzet Rp0 (belum masuk hitungan karena data belum lengkap), 1 pesanan belum bayar.

**Pertanyaan ke kamu (maks 3):**
1. "Coklat" ini nama produk/rasa apa dan harganya berapa? (Ada daftar harga/katalog yang bisa ditempel?)
2. Ongkir ke Bekasi berapa, atau mau pakai kurir apa (nanti saya hitungkan kalau kamu kasih tarifnya)?
3. Ada nama pelanggan, no HP, dan alamat lengkap (jalan, kelurahan/kecamatan, kode pos)? Chat aslinya kelihatannya cuma sepotong.````

## Catatan
- Kerja dulu, tanya di akhir (3 pertanyaan). Tidak mengarang harga/ongkir: semua `[isian]`.
- Sebelum skill: hanya bertanya 4 hal tanpa hasil.
