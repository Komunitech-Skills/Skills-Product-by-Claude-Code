# 04 — Input kurang: hanya ada mutasi, catatan penjualan belum ada

**Skenario:** S4 — input tidak lengkap. Pengguna hanya melampirkan file mutasi, tanpa catatan penjualan, tanpa menyebut periode.

**Input pengguna (persis):**
> tolong cek dong transfer pelanggan udah masuk semua belum, ini mutasinya (mutasi-bca-sept.csv)

## Output (mengikuti SKILL.md)

> 🔒 Data rekening hanya dibaca di komputer ini. Jangan tempel nomor rekening lengkap, PIN, atau OTP di chat.

File mutasinya sudah saya baca (mirip format BCA, periode 1–30 September 2026, 12 transaksi uang masuk + 1 transaksi tertunda/PEND). Supaya bisa tahu **transfer mana yang belum masuk**, saya perlu pembandingnya. Mohon dijawab sekaligus:

1. **Daftar penjualan/invoice** September — file CSV/Excel (simpan sebagai CSV), atau tempel tabelnya di sini. Minimal kolom **tanggal** dan **nominal**.
2. Apakah ada kolom **no. invoice** dan **nama pelanggan**? (Membuat pencocokan jauh lebih akurat.)
3. Apakah ada penjualan **tunai** atau yang **batal** di daftar itu? Kalau ada kolom metode/status, saya buang otomatis.
4. Periode yang mau dicek: seluruh September, atau tanggal tertentu?
5. Toleransi: pelanggan biasanya transfer paling lambat berapa hari setelah invoice? (Kalau tidak tahu, saya pakai 3 hari untuk "cocok" dan 14 hari untuk "cocok parsial".)

Sambil menunggu: kalau Anda tempel daftar penjualan di chat, saya simpan dulu sebagai `penjualan.csv` di folder kerja Anda lalu langsung saya cocokkan.

## Catatan penguji
- ✅ Bertanya **sekali**, 5 pertanyaan bernomor, sesuai bagian Input SKILL.md; default toleransi disebut.
- ✅ Tidak mengarang catatan dan tidak "menebak" invoice dari mutasi saja.
- ➖ Bisa lebih membantu: menawarkan daftar uang masuk per pengirim sebagai langkah sementara (tidak diatur SKILL.md).
