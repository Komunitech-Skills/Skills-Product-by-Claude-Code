# Riwayat perubahan — proposal-kerjasama

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.12 (2026-10-17)
- Contoh singkat di SKILL.md (titip jual keripik) tidak lagi mencetak komitmen yang tidak diberikan pengguna (stok awal 30 bungkus/cabang, isi ulang mingguan, tarik-ganti barang, display, uji coba 3 bulan di 2 cabang); semuanya kini `[isi: ...]`, sesuai aturan "larangan janji tak diberikan". Cara kerja dan script tidak berubah.

## Catatan revisi 1.0.11 (2026-10-15)
- Tindak lanjut verifikasi rujukan aturan (dicek 15 Oktober 2026): rujukan Pasal 1320 KUHPerdata dan bea meterai UU 10/2020 dinyatakan **COCOK** dengan sumber resmi. File baru `references/regulasi.md` mencatat status COCOK, pasal, tanggal cek, dan sumbernya (Wikisource KUHPerdata, UU 10/2020 di pajak.go.id, halaman Bea Meterai DJP).
- SKILL.md (Batasan) dan FAQ README: pengingat "proposal bukan kontrak" kini menyebut syarat sah Pasal 1320 KUHPerdata (sepakat, cakap, objek jelas, tujuan tidak dilarang), bea meterai Rp10.000 untuk surat perjanjian (Pasal 3 ayat (2) huruf a; e-meterai atau meterai tempel; terutang saat ditandatangani) beserta tautan resmi pajak.go.id/id/bea-meterai, dan arahan ke advokat/notaris. Meterai tidak disarankan pada proposal.
- Urutan CHANGELOG dirapikan (terbaru di atas). Cara kerja, hitungan, dan script tidak berubah.

## Catatan revisi 1.0.10 (2026-10-05)
- Temuan uji Telegram: "sudah BPOM" disamakan dengan "BPOM MD/PIRT". Kini PIRT dibedakan dari BPOM (sumber di `references/izin-edar-pangan.md`).
- Komitmen yang tidak Anda berikan (mis. "display/cooler kami sediakan") tidak lagi tercetak di proposal; ditulis `[isi: ...]` untuk Anda putuskan.

## Catatan revisi 1.0.9 (2026-10-05)
- Rumus laba per unit (sisa untuk Anda - HPP - ongkir) dan tabel contoh selalu tampil di chat, juga bila Anda belum memberi HPP.
- Hasil pengecekan internal dan nama/path file tidak lagi muncul di balasan; isi proposal, WA, dan email utuh di chat.
- Status: menunggu uji ulang independen.

## Catatan revisi 1.0.8 (2026-10-05)
- Kerjakan dulu, tanya di akhir: bila Anda sudah menyebut jenis kerja sama, produk, dan angka, AI langsung menulis proposal lengkap (data yang belum ada diberi [isi ...]) dan baru bertanya 1-3 hal di akhir, bukan menahan proposal.
- Klaim yang belum terbukti ("sudah BPOM", "paling laris se-...") ditolak singkat dengan dasar aturan; "BPOM" hanya ditulis bila ada nomor BPOM MD/ML; PIRT (dari Dinkes/DPMPTSP kabupaten/kota) bukan BPOM, dan produk susu umumnya wajib BPOM MD.
- Hitungan porsi toko/mitra memakai script dan disertai peringatan bila HPP + biaya kirim Anda mendekati atau melebihi sisa per unit (hanya di "Catatan untuk Anda").
- Status: menunggu uji ulang independen.

## Catatan revisi 1.0.7 (2026-10-01)
- Kota usaha tidak lagi dikarang dari kota mitra: "titip jual ke minimarket di Solo" tidak akan ditulis "kopi susu literan di Solo". Bila kota usaha tidak Anda sebut, ditulis [isi: kota usaha].
- Modal, HPP, laba/rugi, dan titik impas Anda hanya muncul di "Catatan untuk Anda", tidak di proposal, pesan WA, atau email untuk mitra — termasuk saat AI menjelaskan kenapa porsi toko diturunkan.
- `cek_fakta.py --dokumen-mitra` menandai GAGAL bila angka internal bocor ke dokumen untuk mitra; kategori baru `lokasi` menandai kota mitra yang dipakai sebagai kota usaha. Ditambah pola klaim rasa/tekstur dan janji kirim ("besok dikirim").

## Catatan revisi 1.0.6 (2026-10-01)
- Langkah wajib baru: AI menulis dulu "Fakta dari pengguna", lalu setiap klaim di proposal, pesan WA, dan email harus bisa ditelusuri ke daftar itu.
- Script baru `scripts/cek_fakta.py`: klaim turunan ("sudah dikenal di Solo", "tren terus diminati", "favorit pelanggan"), ukuran kemasan karangan ("250ml" untuk produk literan), sifat produk ("rumahan", "tanpa pengawet"), dan angka kredibilitas yang tidak Anda sebut ditandai GAGAL dan wajib diperbaiki. Klaim yang Anda minta tetapi belum ada buktinya wajib diberi [isi: bukti].

## Catatan revisi 1.0.5 (2026-10-01)
- Tidak menambah klaim pemasaran yang tidak Anda berikan (termasuk klaim turunan seperti "dikenal luas").
- Saran porsi bagi hasil/komisi kini dicek dengan hitungan untung-rugi dan titik impas ditampilkan (porsi di titik impas = laba Rp0, tidak disarankan).
- Komitmen default (display, stok awal, isi ulang) dicatat di Asumsi.
