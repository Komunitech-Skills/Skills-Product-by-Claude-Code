# Riwayat perubahan — rapor-mingguan-ai

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.2 (2026-10-16)
Perbaikan dari pra-cek dengan pengaturan kanal Telegram (penguji independen, versi 1.0.1):
- **Angka rapor selalu benar dan saling cocok.** Sebelumnya jumlah percakapan "bersih" bisa dikira (pada data contoh tertulis 5 dari 10, seharusnya 4). Sekarang AI menulis dulu penilaian tiap percakapan, lalu semua angka (persen tiap kriteria dan percakapan bersih) dihitung dari penilaian itu: lewat skrip bila komputer bisa menjalankan Python, atau dengan rumus tetap bila tidak. Sebelum menulis, AI wajib mencocokkan angka: percakapan bersih tidak boleh melebihi angka lolos terendah, dan angka di ringkasan, tabel, serta teks harus sama. Bila semua kriteria kebetulan sama persen, rapor memberi satu kalimat penjelas.
- **Rapor ringkas untuk chat.** Balasan pertama paling banyak 3.000 karakter (batas satu pesan Telegram 4.096): tabel 3 kolom pendek atau daftar berbutir, PR maksimal 3 kalimat per butir, keputusan maksimal 3 butir. Rincian per percakapan dan cara cek tiap PR dikirim bila pengguna membalas "rinci".
- **Tanpa nama skill teknis di hasil.** Skill lain disebut dengan bahasa awam (mis. "pemeriksaan privasi bot"), bukan nama bertanda hubung.
- Aturan privasi diseragamkan: nomor pelanggan tidak ditulis sama sekali di rapor, termasuk 4 digit akhir.
- Skrip: pilihan baru `--nilai "P1=lolos; P2=nyambung,panjang"` (tanpa perlu berkas), baris "cek konsistensi", daftar percakapan yang gagal per kriteria, persen bergaya Indonesia (83,3%); penilaian yang kosong atau salah ketik tidak lagi dihitung "lolos". Tes unit ditambah (25 tes). Contoh format ringkas baru: `examples/06-format-ringkas-chat.md`.

## Catatan revisi 1.0.1 (2026-10-06)
- Revisi dari uji OpenClaw (skor 4,75 naik ke 8,25): urutan tetap pada "3 kesalahan teratas" dan PR minggu ini: kriteria kritis (salah fakta, janji yang tidak bisa ditepati, bocor data pribadi) selalu didahulukan dan masing-masing jadi butir terpisah; nada atau panjang hanya mengisi sisa kuota. PR wajib menutup kesalahan kritis dulu.
- Privasi: nama, inisial, dan potongan nomor pelanggan (termasuk 4 digit terakhir) tidak ditulis di rapor, diganti "pelanggan A/B". PR berisi fakta usaha hanya dari info yang diberikan pengguna (selain itu `[isian]`); nama berkas internal tidak disebut ke pengguna.

## Catatan revisi 1.0.0 (2026-10-06)
- Rilis awal (status uji).
