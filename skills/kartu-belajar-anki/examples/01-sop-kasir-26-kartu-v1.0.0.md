# Contoh 1: SOP kasir menjadi 26 kartu basic

> Hasil uji OpenClaw 2026-10-12 oleh penguji independen (sisi SESUDAH, skill aktif). Perbandingan lengkap dengan sisi SEBELUM: `00-openclaw-sebelum-sesudah.md`.

## Masukan pengguna

> Bikinin kartu belajar Anki dari SOP kasir toko kami buat karyawan baru ya. Ini SOP-nya (fiktif, dari Toko Sumber Rejeki):
>
> SOP KASIR TOKO SUMBER REJEKI
> 1. Buka kasir: kasir datang 15 menit sebelum toko buka (toko buka jam 08.00, jadi kasir datang 07.45). Hitung uang modal awal di laci, harus Rp500.000 pas. Kalau selisih, lapor ke supervisor sebelum transaksi pertama.
> 2. Setiap transaksi: sapa pelanggan dalam 5 detik, scan barang satu per satu, sebutkan total belanja dengan jelas, tanya metode bayar (tunai, QRIS, atau kartu debit).
> 3. Pembayaran tunai: ucapkan jumlah uang yang diterima, taruh uang pelanggan di atas laci dulu, baru ambil kembalian, baru uang pelanggan dimasukkan ke laci. Tujuannya biar tidak ada salah paham soal nominal.
> 4. QRIS: cek notifikasi masuk di HP kasir toko sebelum menyerahkan barang. Jangan percaya screenshot bukti bayar dari pelanggan.
> 5. Retur: barang boleh diretur maksimal 3 hari setelah beli, wajib bawa struk dan barang belum dibuka. Retur di atas Rp200.000 harus disetujui supervisor. Retur tidak dikembalikan tunai kalau bayar QRIS, tapi lewat QRIS lagi.
> 6. Void (batal item): wajib dengan PIN supervisor. Kasir tidak boleh void sendiri.
> 7. Tutup kasir: hitung uang akhir, cocokkan dengan laporan sistem, selisih lebih dari Rp10.000 wajib ditulis di berita acara. Setor uang ke brankas, modal awal Rp500.000 ditinggal di laci untuk besok.
> 8. Larangan: kasir tidak boleh pinjam uang laci, tidak boleh memakai HP pribadi saat melayani, dan tidak boleh memberi diskon tanpa kode dari supervisor.

## Keluaran di chat (SESUDAH)

> Selesai, ini deck Anki buat SOP kasir Toko Sumber Rejeki.
>
> **Ringkasan**
> - 26 kartu, format **Basic** (pertanyaan–jawaban), bahasa Indonesia
> - Tag per bagian SOP: `sop-kasir-buka`, `sop-transaksi`, `sop-tunai`, `sop-qris`, `sop-retur`, `sop-void`, `sop-tutup`, `sop-larangan`
> - Divalidasi otomatis: **26/26 kartu valid, 0 error**
>
> **Pratinjau (contoh)**
>
> | Depan | Belakang | Tag |
> |---|---|---|
> | Berapa nominal modal awal yang dihitung kasir saat buka kasir? | Rp500.000 pas | sop-kasir-buka |
> | Pada pembayaran tunai, apa yang pertama diucapkan kasir? | Jumlah uang yang diterima dari pelanggan | sop-tunai |
> | Apa yang wajib dicek kasir sebelum serahkan barang di pembayaran QRIS? | Notifikasi masuk di HP kasir toko | sop-qris |
> | Apa syarat wajib agar void (batal item) boleh dilakukan? | PIN supervisor | sop-void |
> | Selisih uang saat tutup kasir yang wajib ditulis di berita acara? | Selisih lebih dari Rp10.000 | sop-tutup |
>
> **Rencana belajar** (20 menit/hari, 15 kartu baru/hari)
> - Hari 1–2: pelajari 15 kartu baru per hari (hari 1: 15, hari 2: 11 sisa)
> - Mulai hari 2, sisihkan ±5–10 menit review kartu kemarin (Anki akan jadwalkan otomatis)
> - Total kartu baru tuntas dalam **2 hari belajar**, selanjutnya tinggal review berkala
>
> **Blok TSV lengkap (siap impor)**
>
> ```
> Jam berapa kasir Toko Sumber Rejeki harus datang, kalau toko buka jam 08.00?	15 menit sebelum buka, yaitu jam 07.45	sop-kasir-buka
> Berapa nominal modal awal yang harus dihitung kasir di laci saat buka kasir?	Rp500.000 pas	sop-kasir-buka
> Apa yang harus dilakukan kasir kalau modal awal di laci selisih dari Rp500.000?	Lapor ke supervisor sebelum transaksi pertama	sop-kasir-buka
> Dalam berapa detik kasir harus menyapa pelanggan saat mulai transaksi?	Dalam 5 detik	sop-transaksi
> Bagaimana cara kasir memindai barang belanjaan pelanggan?	Scan barang satu per satu	sop-transaksi
> Apa yang wajib disebutkan kasir dengan jelas setelah selesai scan semua barang?	Total belanja pelanggan	sop-transaksi
> Apa 3 metode bayar yang boleh ditawarkan kasir ke pelanggan?	Tunai, QRIS, atau kartu debit	sop-transaksi
> Pada pembayaran tunai, apa yang pertama kali diucapkan kasir ke pelanggan?	Jumlah uang yang diterima dari pelanggan	sop-tunai
> Setelah pelanggan menyerahkan uang tunai, di mana kasir menaruhnya lebih dulu?	Di atas laci dulu, belum dimasukkan ke laci	sop-tunai
> Setelah uang pelanggan ditaruh di atas laci, apa langkah kasir berikutnya sebelum uang itu dimasukkan ke laci?	Ambil dan berikan kembalian dulu, baru uang pelanggan dimasukkan ke laci	sop-tunai
> Apa tujuan aturan "uang pelanggan ditaruh di atas laci dulu, baru ambil kembalian" pada pembayaran tunai?	Supaya tidak ada salah paham soal nominal uang yang diberikan pelanggan	sop-tunai
> Apa yang wajib dicek kasir sebelum menyerahkan barang pada pembayaran QRIS?	Notifikasi pembayaran masuk di HP kasir toko	sop-qris
> Bolehkah kasir menyerahkan barang hanya berdasarkan screenshot bukti bayar QRIS dari pelanggan?	Tidak boleh, kasir wajib cek notifikasi masuk di HP kasir toko sendiri	sop-qris
> Berapa lama batas waktu maksimal pelanggan boleh mengajukan retur barang?	Maksimal 3 hari setelah pembelian	sop-retur
> Apa 2 syarat wajib agar retur barang bisa diproses?	Bawa struk dan barang belum dibuka	sop-retur
> Retur dengan nilai berapa yang wajib disetujui supervisor dulu?	Retur di atas Rp200.000	sop-retur
> Kalau pelanggan bayar pakai QRIS lalu melakukan retur, uangnya dikembalikan dalam bentuk apa?	Lewat QRIS lagi, bukan tunai	sop-retur
> Apa yang wajib dimiliki kasir untuk bisa melakukan void (batal item)?	PIN supervisor	sop-void
> Bolehkah kasir melakukan void (batal item) sendiri tanpa supervisor?	Tidak boleh	sop-void
> Saat tutup kasir, uang akhir di laci dicocokkan dengan apa?	Laporan sistem	sop-tutup
> Selisih uang sebesar apa saat tutup kasir yang wajib ditulis di berita acara?	Selisih lebih dari Rp10.000	sop-tutup
> Setelah tutup kasir, uang hasil penjualan disetor ke mana?	Ke brankas	sop-tutup
> Berapa uang yang ditinggal di laci saat tutup kasir untuk modal besok?	Rp500.000	sop-tutup
> Bolehkah kasir meminjam uang dari laci kasir untuk keperluan pribadi?	Tidak boleh	sop-larangan
> Bolehkah kasir memakai HP pribadi saat sedang melayani pelanggan?	Tidak boleh	sop-larangan
> Bolehkah kasir memberi diskon ke pelanggan tanpa kode dari supervisor?	Tidak boleh	sop-larangan
> ```
>
> **Cara impor ke Anki**
> 1. Buka Anki → **File** → **Import**
> 2. Pilih berkas TSV ini (simpan dulu sebagai file `.txt` atau `.tsv`)
> 3. Pastikan pemisah = **Tab**
> 4. Atur kolom: kolom 1 → Front, kolom 2 → Back, kolom 3 → Tags
> 5. Klik **Import**
>
> **Asumsi yang dipakai:**
> - Jenis kartu Basic (bukan cloze), karena isinya langkah & aturan SOP, bukan kalimat definisi panjang
> - 1 deck gabungan dengan 8 tag per bagian SOP (bukan 8 deck terpisah) biar gampang filter saat review
> - Target belajar 20 menit/hari, 15 kartu baru/hari (standar pemula)
>
> Pertanyaan:
> 1. Mau dipecah per topik jadi beberapa deck terpisah (misal "SOP Kasir - Pembukaan", "SOP Kasir - Transaksi", dst), atau satu deck gabungan seperti di atas sudah cukup?
> 2. Perlu kartu tambahan versi "studi kasus" (skenario pelanggan rewel/selisih uang) buat latihan, atau cukup hafalan prosedur seperti ini dulu?

## Catatan penguji

- TSV di chat diekstrak ke `data/hasil-sesudah-1-sop-kasir.tsv`; `validasi_dek.py` = ok, 26 kartu; `rencana_belajar.py --kartu 26 --menit 20 --baru-per-hari 15` = 2 hari (cocok dengan jawaban agent).
- Semua angka SOP dicek ke teks sumber: benar. Tidak ada fakta karangan.
- Konteks Telegram: 22 kartu utuh di chat (`data/hasil-sesudah-1-telegram.tsv`, validasi ok), tanpa tawaran 'kirim file'.
- Cacat kecil: frasa 'Divalidasi otomatis'; tidak ada header `#separator:tab`.
