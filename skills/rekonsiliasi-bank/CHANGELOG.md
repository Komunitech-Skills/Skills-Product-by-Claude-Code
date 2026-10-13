# Riwayat perubahan — rekonsiliasi-bank

Catatan teknis per versi.

## Catatan revisi 1.2.2 (2026-10-01)
- Petunjuk lokasi script ditambahkan di SKILL.md: script ada di subfolder `scripts/` di folder skill. Agent dilarang mencari script atau file pengguna ke seluruh disk (mis. `find /`).

## Catatan revisi 1.2.1 (2026-09-29)
- Baris "Aturan kerja" ditambahkan di SKILL.md: agent tidak boleh memasang paket/aplikasi sendiri, tidak membuka atau mencari file di luar yang diberikan pengguna, dan hasil yang ditulis ke file harus disebut lokasinya (folder kerja, bukan `/tmp`).

## Catatan revisi 1.2.0 (2026-09-24)
- Versi saat skill pertama masuk repo. Pembaruan lanjutan dari hasil uji internal; rincian di riwayat git.

## Catatan revisi 1.1.0 (sebelum 2026-09-24)
- Perbaikan dari uji pertama (skor 6, perlu revisi), menurut `examples/HASIL-UJI.md`: pencocokan yang berpetunjuk nama kini didahulukan dan pasangan yang berpotensi tertukar diberi label KEMUNGKINAN TERTUKAR; nama dicocokkan per kata utuh (mis. "andi" tidak lagi cocok dengan "ANDIKA") dan referensi angka minimal 4 digit; `--toleransi-nominal` tidak lagi membuat selisih tidak seimbang; kolom keterangan ganda tidak saling menimpa (`--bank-keterangan` bisa diulang); alasan mengikuti arah (masuk/keluar); transaksi PEND dilaporkan terpisah; nomor rekening bertanda hubung ikut disamarkan.

## Catatan revisi 1.0.0 (sebelum 2026-09-24)
- Rilis awal (uji internal).
