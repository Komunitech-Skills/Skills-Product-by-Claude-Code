# Riwayat perubahan — bot-trading-kripto

Catatan teknis per versi.

## Catatan revisi 1.0.6 (2026-10-01)
- SKILL.md kini menyebut bahwa script ada di subfolder `scripts/` di folder skill, dan agent tidak boleh mencari file ke seluruh disk (mis. `find /`). Logika bot tidak berubah.

## Catatan revisi 1.0.5 (2026-09-30)
- Pembacaan kolom harga pada CSV backtest mengenali format angka Indonesia (titik ribuan, koma desimal, mis. "1.908.238.000" atau "38.000,50"; awalan Rp/IDR dibuang) selain format bursa (titik desimal, mis. "114311.97"). Satu kolom ditentukan gayanya sekaligus.
- Bentuk yang meragukan ("38.000" bisa 38000 atau 38) atau campuran dua gaya dalam satu kolom ditolak dengan pesan jelas, tidak ditebak diam-diam. Uji regresi ditambah.

## Catatan revisi 1.0.4 (2026-09-29)
- Kunci akun antar-proses (per bursa + API key publik, tanpa menyimpan rahasia): salinan folder bot yang berjalan bersamaan tidak bisa lagi membeli melebihi batas modal total.
- Buku live global per akun/pasangan: menghapus `state.json` lalu paper ulang tidak membuka jatah modal baru; sebelum setiap pembelian live, modal terpakai diambil dari angka terbesar antara buku folder, buku global, dan selisih saldo koin di bursa. Buku global rusak berarti tidak ada pembelian.
- Argumen `--kurs` memahami format Indonesia (`16.500` = 16500); bentuk yang ambigu (`16,500`, `16.5`, notasi ilmiah, negatif, nol) ditolak, dan angka raksasa tidak lagi membuat traceback.
- Batas yang tidak bisa dicegah script (mis. menghapus buku global bersama state bot, kunci API baru untuk akun yang sama, dua komputer berbeda) ditulis jujur di SKILL.md dan README. 128 tes regresi lulus.

## Catatan revisi 1.0.3 (2026-09-29)
- Pindah mode (live ke paper ke live) tidak lagi mengosongkan buku live: buku disimpan per mode. `KONFIRMASI-LIVE.json` kini sekali pakai, bersegel, berlaku maksimal 24 jam, dan batal bila mode atau konfigurasi berubah; konfirmasi format lama ditolak.
- Sebelum setiap pembelian live, modal terpakai juga dicocokkan dengan saldo koin di bursa lewat endpoint baca-saja (rekonsiliasi saldo).
- Rekap pajak dan biaya dipisah per mata uang kutipan (tidak pernah menjumlahkan USDC/BTC sebagai rupiah); rupiah hanya lewat `--kurs` dari pengguna dan diberi label perkiraan.
- Hasil backtest memuat disclaimer. Batas rugi harian juga dihitung 24 jam bergulir agar jam komputer yang dimajukan lalu dimundurkan tidak memberi jatah rugi tambahan. 109 tes regresi lulus.

## Catatan revisi 1.0.2 (2026-09-29)
- Singkatan opsi konfirmasi (mis. `--saya-s...`) ditolak di script bot (`allow_abbrev=False`), agar pintu pengaman tidak bisa terlewati lewat awalan opsi. Perbaikan ini dikerjakan lintas banyak skill sekaligus.

## Catatan revisi 1.0.1 (2026-09-29)
- Revisi setelah uji independen pertama: jam komputer yang dimundurkan tidak lagi me-reset batas rugi harian (tanggal tidak pernah mundur, patokan per tanggal disimpan 14 hari).
- Permintaan bertanda tangan (kunci API) tidak pernah mengikuti pengalihan (redirect) HTTP.
- PPh transaksi tukar kripto-kripto dihitung sesuai PMK 50/2025 untuk sisi beli dan jual, dan rekap pajak menjumlahkannya.
- Tombol berhenti menulis berkas STOP di empat lokasi (folder bot, folder konfigurasi, global, `STOP-SEMUA`), tidak lagi bergantung pada `--folder-bot`.
- Indodax: skill tidak memanggil metode tarik dana apa pun; mode live wajib daftar periksa izin tarik dana MATI di layar bursa lalu `siapkan_live.py --saya-sudah-cek-tanpa-withdraw`.
- Live butuh minimal 3 putaran paper dengan harga dan jam asli dalam 24 jam; pola angka ribuan ("500.000") ditolak dengan saran penulisan; kunci putaran dibuat atomik. 87 tes regresi lulus.

## Catatan revisi 1.0.0 (2026-09-29)
- Rilis awal (uji internal): backtest, simulasi (paper), dan testnet untuk strategi buatan member sendiri (beli rutin/DCA, grid, take-profit/stop-loss, rebalancing) di Indodax dan Binance. Batas risiko wajib (modal maksimal, stop-loss, batas rugi harian), tombol berhenti, kunci API tanpa izin tarik dana, mode live berlapis konfirmasi, dan penghitung pajak/biaya. Tanpa sinyal beli/jual dan tanpa janji profit.
