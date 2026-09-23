# 04 — Input kurang: hanya nama pembeli

**Skenario:** S4 — input tidak lengkap. Penjual dan item (wajib) tidak ada.

**Input pengguna (persis):**
> Tolong buatin invoice ke Pak Budi ya

## Output (bertanya sekali)

Siap, saya buatkan invoice untuk Pak Budi. Saya perlu beberapa info dulu:

1. **Nama usaha Anda** (penjual), plus alamat/nomor WA kalau mau dicantumkan.
2. **Barang/jasa yang ditagih**: nama, jumlah, dan harga satuan (plus diskon kalau ada). Contoh: *"50 box nasi @25rb, ongkir 50rb"*.
3. Apakah **sudah ada DP/pembayaran** yang masuk? Kalau ya, berapa dan tanggal berapa?
4. **Rekening** tujuan pembayaran dan **jatuh tempo** (kalau tidak disebut, saya pakai 14 hari).
5. Anda sudah **PKP**? Kalau belum, invoice dibuat tanpa PPN (dan memang tidak boleh ada PPN).

Kalau ada nomor invoice terakhir, sebutkan juga supaya nomornya berurutan.

## Catatan penguji
- Bertanya sekali, tepat 5 pertanyaan bernomor + satu permintaan opsional (nomor terakhir), dengan default yang disebut (jatuh tempo 14 hari, tanpa PPN). Sesuai SKILL.md.
- Tidak mengarang item atau harga. Bagus.
