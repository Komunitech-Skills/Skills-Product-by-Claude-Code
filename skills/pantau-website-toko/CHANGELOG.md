# Riwayat perubahan — pantau-website-toko

Catatan teknis per versi (dipindah dari README agar halaman pembeli ringkas).

## Catatan revisi 1.0.11 (2026-10-17)

- `SKILL.md`: contoh keluaran `ringkasan` di bagian Format Output disamakan dengan keluaran skrip pada data uji: nama status page "Toko Scenario2 (toko-scenario2)" dan "ping 240 ms" (sebelumnya tertulis "Toko Saya" dan 210 ms, padahal pengecekan terakhir 240 ms). Cara kerja tidak berubah.

## Catatan revisi 1.0.10 (2026-10-13)

- `SKILL.md`: rujukan ke catatan riset internal diganti kalimat yang berdiri sendiri; konstanta VERSI skrip dan penanda versi di SKILL.md disamakan; cara kerja tidak berubah.

## Catatan revisi 1.0.9 (2026-10-03)

- Description melarang eksplisit tawaran balik "aku setup/aktifkan pemantauan/alert/cek tiap jam"; pemicu ditambah ("pantau tiap jam", "cek otomatis", "kabari kalau down").

## Catatan revisi 1.0.8 (2026-10-03)

- `description` kini memuat batas keras (tidak memasang Uptime Kuma/alert, tidak mengecek situs pesaing, termasuk cek sekali) beserta kata pemicu, karena model sering menjawab tanpa membuka SKILL.md; ditambah "ATURAN WAJIB" di awal SKILL.md.

## Catatan revisi 1.0.7 (2026-10-01)

- Kata pemicu ditambah di description ("kabari ke WA kalau web down", "pasang alert website", "pantau/cek website saingan atau kompetitor") agar skill terbaca pada permintaan jebakan; uji ulang putaran 2 menunjukkan agent tidak membaca SKILL.md di skenario itu.

## Catatan revisi 1.0.6 (2026-10-01)
- Batas layanan dipertegas di bagian paling awal skill dan di deskripsinya: AI tidak memasang Uptime Kuma, monitor, maupun alert WA/notifikasi — dipasang Anda sendiri (dipandu) atau lewat jasa setup Komunitech; notifikasi resmi lewat Telegram.
- Kalimat baku penolakan untuk permintaan memantau website pesaing/orang lain, tanpa tawaran cek terjadwal ke situs mereka.
- Contoh balasan yang benar ditambahkan di `examples/10-contoh-balasan-pantau-saingan-dan-minta-pasang.md`.

## Catatan revisi 1.0.5 (2026-10-01)
- Ringkasan kini menghitung **kejadian** down (beberapa cek gagal berurutan = 1 kejadian) lengkap dengan jam mulai–selesai (WIB) dan durasinya — tidak lagi "turun 5x" yang membingungkan.
- Angka menit & persen disampaikan persis seperti hasil script.
- Batas layanan diperjelas: AI tidak memasang Uptime Kuma atau notifikasi untuk Anda; pemasangan dilakukan sendiri (dipandu) atau lewat jasa setup Komunitech. Notifikasi resmi lewat Telegram; WhatsApp hanya dengan nomor terpisah sesuai kebijakan Komunitech.
