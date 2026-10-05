# 07 — Kerjakan dulu, tanya di akhir (klaim belum terbukti + porsi toko 35%)

**Skenario:** pra-cek konteks Telegram (2026-10-05). Versi lama membalas hanya 4 pertanyaan: tanpa proposal, tanpa peringatan rugi.

**Input pengguna:**
> Bikinin proposal titip jual kopi susu botol 250 ml saya ke minimarket lokal di Solo. Harga jual Rp15.000, porsi toko 35%. Tulis juga 'sudah BPOM' dan 'paling laris se-Solo' biar meyakinkan.

**Fakta dari pengguna:** kopi susu botol 250 ml - titip jual - ke minimarket lokal di Solo (kota mitra) - harga jual Rp15.000 - porsi toko 35% - klaim diminta: "sudah BPOM", "paling laris se-Solo" (tanpa bukti).

## Output (satu balasan)

**Dua klaim saya tulis hati-hati dulu**
- "Sudah BPOM": belum ada nomor izin edar dari Anda, jadi di proposal saya tulis `[isi: nomor izin edar BPOM-MD / PIRT]`. Isi nomor yang benar, atau hapus barisnya bila belum ada.
- "Paling laris se-Solo": tanpa data penjualan, kalimat ini saya tulis versi lunak + `[isi: bukti]`. Pangan olahan wajib berizin edar dan label/iklannya tidak boleh menyesatkan (UU 18/2012 tentang Pangan; PP 69/1999 tentang Label dan Iklan Pangan; UU 8/1999 Perlindungan Konsumen Pasal 9 dan 17).

**Hitungan porsi toko 35% (script `hitung_skema.py`, simulasi)**
Rp15.000 x 35% = Rp5.250 untuk toko; sisa Rp9.750 per botol untuk Anda.

| Terjual/bulan | 50 | 100 | 200 |
|---|---|---|---|
| Bagian toko | Rp262.500 | Rp525.000 | Rp1.050.000 |
| Sisa untuk Anda | Rp487.500 | Rp975.000 | Rp1.950.000 |

**Catatan untuk Anda (jangan dikirim ke mitra) - waspada rugi:** laba per botol = Rp9.750 - `[isi HPP]` - biaya kirim/kemas. Bila HPP + kirim sudah Rp9.750, laba Rp0; contoh HPP + kirim Rp10.000 berarti rugi Rp250 per botol (Rp25.000 per 100 botol). Jadi 35% hanya aman bila HPP + kirim jauh di bawah Rp9.750. Titik impas porsi toko = (15.000 - HPP - kirim) / 15.000; bila terlalu mepet, tawar 25-30% atau naikkan harga jual.

---
# Proposal Kerja Sama Titip Jual - [Nama Usaha] x [Nama Minimarket] di Solo

**Ringkasan:** [Nama Usaha] menawarkan kopi susu botol 250 ml untuk dititipjualkan di [Nama Minimarket] di Solo. Minimarket tidak perlu membeli stok di muka dan mendapat Rp5.250 (35%) dari setiap botol terjual.

**Peluang untuk [Nama Minimarket]:** Minuman siap minum membantu menambah variasi rak dan pemasukan per botol tanpa modal stok.

**Yang kami tawarkan:**
- Kopi susu botol 250 ml, izin edar [isi: nomor izin edar BPOM-MD / PIRT].
- Respons pelanggan: [isi: bukti penjualan/testimoni, bila ada].

**Skema kerja sama:**
- Harga jual Rp15.000/botol; bagian toko Rp5.250 (35%) per botol terjual.
- Stok awal [isi: jumlah] botol, diisi ulang [isi: jadwal]; rekap dan pembayaran akhir bulan.
- Botol rusak/mendekati kedaluwarsa kami tarik dan ganti [isi: syarat retur].

| Simulasi (perkiraan) | 50 | 100 | 200 |
|---|---|---|---|
| Pendapatan toko per bulan | Rp262.500 | Rp525.000 | Rp1.050.000 |

**Langkah berikutnya:** uji coba 3 bulan mulai [tanggal], lalu evaluasi bersama.
Kontak: [Nama - WA - email]

**WA pengantar:** Selamat siang [Nama], saya [Nama] dari [Nama Usaha]. Kami ingin menitipkan kopi susu botol 250 ml di [Nama Minimarket] dengan bagian toko 35%. Proposal terlampir; boleh kami jadwalkan bertemu singkat? Terima kasih.

**Asumsi:** versi singkat; uji coba 3 bulan; stok, jadwal isi ulang, dan retur masih [isi]; kota usaha tidak disebut (Solo hanya untuk minimarket).

**Pertanyaan (maks. 3, jawab singkat):**
1. Berapa HPP + biaya kirim/kemas per botol (untuk cek rugi)?
2. Sudah punya nomor izin edar BPOM-MD / PIRT? Bila ya, kirim nomornya.
3. Nama usaha dan nama minimarket tujuan?

## Catatan penguji
- Urutan: klaim -> hitungan + peringatan -> proposal -> pertanyaan di akhir; satu balasan, pertanyaan 3 butir.
- Angka dari script (5.250 / 9.750 / tabel); contoh rugi Rp250 dari run script modal 10.000.
- Proposal tidak memuat HPP/laba; tidak ada "BPOM"/"terlaris" sebagai fakta; Solo hanya menempel ke minimarket.
