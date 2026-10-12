# Skenario 1: SOP kasir menjadi 21 kartu (konteks Telegram)

**Input:** `data/pesan-1-sop-kasir.txt` (SOP kasir 8 butir, fiktif), dikirim lewat konteks kanal Telegram.

## Output SESUDAH (skill aktif, kartu-belajar-anki 1.0.1)

> Deck Anki buat SOP kasir Toko Sumber Rejeki udah siap. Berikut ringkasannya:
>
> **Ringkasan**
> - 21 kartu basic (depan/belakang), bahasa Indonesia
> - Tag: `sop-kasir`, `sop-kasir-tunai`, `sop-kasir-qris`, `sop-kasir-retur`, `sop-kasir-tutup`
> - Asumsi: kartu dipecah per langkah SOP (buka kasir, transaksi, tunai, QRIS, retur, void, tutup kasir, larangan) — satu ide per kartu
>
> **Pratinjau (contoh)**
>
> | Depan | Belakang |
> |---|---|
> | Berapa modal awal uang di laci saat buka kasir? | Rp500.000 pas |
> | Saat bayar tunai, di mana uang pelanggan diletakkan sebelum kembalian diambil? | Di atas laci, belum dimasukkan |
> | Sebelum serahkan barang pada pembayaran QRIS, apa yang wajib dicek kasir? | Notifikasi pembayaran masuk di HP kasir toko |
> | Retur di atas berapa rupiah yang wajib disetujui supervisor? | Di atas Rp200.000 |
> | Apa syarat untuk membatalkan item (void) dalam transaksi? | Wajib pakai PIN supervisor, kasir tidak boleh void sendiri |
>
> **Rencana belajar**
> 21 kartu, 15 kartu baru/hari, ±20 menit/hari → selesai kartu baru dalam 2 hari. Hari 1–2 fokus kartu baru, sisihkan ±5–10 menit review kartu kemarin tiap hari berikutnya.
>
> **Blok TSV lengkap (siap impor)**
>
> ```
> #separator:tab
> Berapa menit sebelum toko buka kasir harus datang?	15 menit sebelum buka (toko buka 08.00, kasir datang 07.45)	sop-kasir
> Berapa modal awal uang di laci saat buka kasir?	Rp500.000 pas	sop-kasir
> Apa yang dilakukan kasir kalau uang modal awal selisih?	Lapor ke supervisor sebelum transaksi pertama	sop-kasir
> Berapa detik batas waktu menyapa pelanggan di awal transaksi?	Maksimal 5 detik	sop-kasir
> Apa urutan langkah melayani satu transaksi?	Sapa pelanggan, scan barang satu per satu, sebutkan total belanja, tanya metode bayar	sop-kasir
> Apa saja metode bayar yang tersedia di kasir?	Tunai, QRIS, atau kartu debit	sop-kasir
> Saat bayar tunai, apa yang diucapkan kasir sebelum ambil kembalian?	Jumlah uang yang diterima dari pelanggan	sop-kasir-tunai
> Saat bayar tunai, di mana uang pelanggan diletakkan sebelum kembalian diambil?	Di atas laci, belum dimasukkan	sop-kasir-tunai
> Kapan uang pelanggan (tunai) baru boleh dimasukkan ke laci?	Setelah kembalian diberikan ke pelanggan	sop-kasir-tunai
> Apa tujuan aturan taruh uang di atas laci sebelum ambil kembalian?	Supaya tidak ada salah paham soal nominal uang yang diterima	sop-kasir-tunai
> Sebelum serahkan barang pada pembayaran QRIS, apa yang wajib dicek kasir?	Notifikasi pembayaran masuk di HP kasir toko	sop-kasir-qris
> Bolehkah kasir percaya screenshot bukti bayar QRIS dari pelanggan?	Tidak boleh, wajib cek notifikasi masuk langsung di HP kasir toko	sop-kasir-qris
> Berapa batas waktu maksimal retur barang setelah beli?	3 hari setelah pembelian	sop-kasir-retur
> Apa syarat wajib agar barang bisa diretur?	Bawa struk dan barang belum dibuka	sop-kasir-retur
> Retur di atas berapa rupiah yang wajib disetujui supervisor?	Di atas Rp200.000	sop-kasir-retur
> Bagaimana cara kembalikan dana retur kalau pembayaran awal pakai QRIS?	Tidak dikembalikan tunai, dikembalikan lewat QRIS lagi	sop-kasir-retur
> Apa syarat untuk membatalkan item (void) dalam transaksi?	Wajib pakai PIN supervisor, kasir tidak boleh void sendiri	sop-kasir
> Saat tutup kasir, uang hasil hitungan dicocokkan dengan apa?	Laporan sistem	sop-kasir-tutup
> Selisih berapa saat tutup kasir yang wajib ditulis di berita acara?	Selisih lebih dari Rp10.000	sop-kasir-tutup
> Setelah setor uang ke brankas, berapa uang yang ditinggal di laci untuk modal besok?	Rp500.000	sop-kasir-tutup
> Apa saja tiga larangan utama untuk kasir?	Tidak boleh pinjam uang laci, tidak boleh pakai HP pribadi saat melayani, tidak boleh beri diskon tanpa kode supervisor	sop-kasir
> ```
>
> **Cara impor ke Anki**
> 1. Buka Anki → File → Import
> 2. Pilih file TSV (salin teks di atas ke file .txt/.tsv dulu)
> 3. Pastikan pemisah = Tab
> 4. Petakan kolom: 1 = Front, 2 = Back, 3 = Tags
> 5. Pilih deck tujuan, klik Import
>
> **Pertanyaan**
> 1. Tagnya mau tetap dipecah per sub-topik (tunai/QRIS/retur/tutup) atau digabung jadi satu tag `sop-kasir` saja?
> 2. Mau saya buat versi tambahan khusus buat kuis lisan training (tanpa Anki), atau TSV ini sudah cukup?
>
> Balas **kirim file** bila ingin saya siapkan berkas TSV terpisah.

## Catatan penguji

- 21 kartu Basic; `validasi_dek.py` ok, `rencana_belajar.py --kartu 21` = 2 hari: cocok.
- Semua angka SOP benar; kartu utuh di chat; tanpa kata proses; ada tawaran "Balas kirim file".
- TSV disalin ke `data/v101-sesudah-1-telegram.tsv`.
- Nilai: SESUDAH 9,0 (SEBELUM 5,0).

Rincian dua sisi: `00-openclaw-sebelum-sesudah.md`.
